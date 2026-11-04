# German forced alignment with pocketsphinx + the CMU Sphinx VoxForge German model (script words -> start/end)
# usage: align_de.py <dir> <wav> <out.json> [free]   ("free" also runs plain recognition, to check the recording matches the script)
import sys, re, json, subprocess, os
from pocketsphinx import Decoder
D, WAV, OUT = sys.argv[1:4]
M = os.path.join(D, '../models_de/cmusphinx-ptm-voxforge-de-r20171217/')
TEXT = open(D + '/code/script.txt').read().split()
# words not in the dictionary: split into dictionary words (numbers spoken out, compounds split)
EXP = {'1887': 'achtzehn hundert sieben und achtzig', '1939': 'neunzehn hundert neun und dreißig', '1940': 'neunzehn hundert vierzig',
       '1941': 'neunzehn hundert ein und vierzig', '1942': 'neunzehn hundert zwei und vierzig', '1944': 'neunzehn hundert vier und vierzig',
       '1949': 'neunzehn hundert neun und vierzig', '1953': 'neunzehn hundert drei und fünfzig', '11': 'elfte', '20': 'zwanzigsten', '6': 'sechste',
       '50': 'fünfzig', '18': 'achtzehn', 'waldgebiet': 'wald gebiet', 'heeresführung': 'heeres führung', 'korpskommando': 'korps kommando',
       'ärmelkanal': 'ärmel kanal', 'befehlsbereich': 'befehls bereich', 'einsatzgruppe': 'einsatz gruppe', 'zehntausende': 'zehn tausende',
       'generalfeldmarschall': 'general feld marschall', 'militärgericht': 'militär gericht', 'anklagepunkten': 'anklage punkten', 'niederlagen': 'nieder lagen'}
ADD = {'manstein': 'M AH N SH T AY N', 'lewinski': 'L EH V IH N S K IIH', 'ardennen': 'AH RR D EH N AX N', 'passierbar': 'P AH S IIH RR B AAH RR',
       'stießen': 'SH T IIH S AX N', 'krim': 'K RR IH M', 'unterschrieb': 'UH N T EX SH RR IIH P', 'ermordete': 'EH RR M OO RR D AX T AX',
       'sewastopol': 'Z EH V AH S T OOH P OO L', 'stalingrad': 'SH T AAH L IH N K RR AAH T', 'saubere': 'Z AW B AX RR AX', 'stratege': 'SH T RR AH T EEH G AX',
       'kanntet': 'K AH N T AX T', 'heeres': 'HH EEH RR AX S', 'befehls': 'B AX F EEH L S', 'marschall': 'M AH RR SH AH L', 'korps': 'K OOH RR'}
def norm(w): return re.sub(r'[^a-zäöüß0-9]', '', w.lower())
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', WAV, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
if 'free' in sys.argv:
    d = Decoder(hmm=M + 'model_parameters/voxforge.cd_ptm_5000', dict=M + 'etc/voxforge.dic', lm=M + 'etc/voxforge.lm.bin', samprate=16000, loglevel='ERROR')
    d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt(); print('HEARD:', d.hyp().hypstr if d.hyp() else None)
d = Decoder(hmm=M + 'model_parameters/voxforge.cd_ptm_5000', dict=M + 'etc/voxforge.dic', samprate=16000, bestpath=False, loglevel='ERROR')
for k, v in ADD.items():
    if d.lookup_word(k) is None: d.add_word(k, v, True)
toks, owner = [], []
for i, w in enumerate(TEXT):
    for t in EXP.get(norm(w), norm(w)).split():
        if d.lookup_word(t) is None: raise SystemExit('missing word: ' + t)
        toks.append(t); owner.append(i)
d.set_align_text(' '.join(toks)); d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
al = [(re.sub(r'\(\d+\)$', '', s.word), s.start_frame / 100, (s.end_frame + 1) / 100) for s in d.seg()]
al = [a for a in al if a[0] not in ('<s>', '</s>', '<sil>', '[NOISE]', '(NULL)', '++garbage++')]
print('tokens', len(toks), 'aligned', len(al))
assert len(al) == len(toks)
out = []
for i, w in enumerate(TEXT):
    seg = [a for a, o in zip(al, owner) if o == i]
    out.append([w, round(seg[0][1], 3), round(seg[-1][2], 3)])
for i in range(len(out) - 1): out[i][2] = min(out[i][2], out[i + 1][1])
json.dump(out, open(OUT, 'w'), ensure_ascii=False); print(' '.join(f'{w}@{a:.2f}' for w, a, b in out))
