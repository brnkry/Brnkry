# German forced alignment with pocketsphinx + the CMU Sphinx VoxForge German model (script words -> start/end)
# usage: align_de.py <dir> <wav> <out.json> [free]   ("free" also runs plain recognition, to check the recording matches the script)
import sys, re, json, subprocess, os
from pocketsphinx import Decoder
D, WAV, OUT = sys.argv[1:4]
M = os.path.join(D, '../models_de/cmusphinx-ptm-voxforge-de-r20171217/')
TEXT = open(D + '/code/script.txt').read().split()
# words not in the dictionary: split into dictionary words (numbers spoken out, compounds split)
EXP = {'13': 'dreizehnten', '18': 'achtzehn', '1940': 'neunzehn hundert vierzig', '1942': 'neunzehn hundert zwei und vierzig', '1944': 'neunzehn hundert vier und vierzig', '1893': 'achtzehn hundert drei und neunzig', '1948': 'neunzehn hundert acht und vierzig', '1980': 'neunzehn hundert achtzig',
       '1982': 'neunzehn hundert zwei und achtzig', '25': 'fünf und zwanzig', '11': 'elften', 'artilleriekommandeur': 'artillerie kommandeur',
       'einsatzbereiten': 'einsatz bereiten', 'feldzug': 'feld zug', 'gefangenschaft': 'gefangen schaft', 'gerichtsverfahren': 'gerichts verfahren',
       'heeresgruppe': 'heeres gruppe', 'kriegsende': 'kriegs ende', 'oberbefehlshaber': 'ober befehls haber', 'nationalsozialisten': 'national sozialisten',
       'panzerarmee': 'panzer armee', 'panzerdivision': 'panzer division', 'panzern': 'panzer n_', 'schützenregiment': 'schützen regiment',
       'siebenmal': 'sieben mal', 'tagsüber': 'tags über', 'verteidigungsministerium': 'verteidigungs ministerium'}
ADD = {'kommandeur': 'K OO M AH N D OE EX', 'betrunken': 'B AX T RR UU NG K AX N', 'erschießen': 'Q EH EX SH IIH S AX N', 'erschießung': 'Q EH EX SH IIH S UU NG',
       'heeres': 'HH EEH RR AX S', 'interviews': 'Q IH N T EX V Y UU S', 'kriegs': 'K RR IIH K S', 'kämpft': 'K EH M PF T', 'lothringen': 'L OOH T RR IH NG AX N',
       'maas': 'M AAH S', 'befehls': 'B AX F EEH L S', 'haber': 'HH AAH B EX', 'sozialisten': 'Z OO TS IY AAH L IH S T AX N', 'regiment': 'RR EEH G IH M EH N T',
       'sowjets': 'Z OO V Y EH T S', 'westlich': 'V EH S T L IH CC', 'verteidigungs': 'F EH EX T AY D IIH G UU NG S', 'planern': 'P L AAH N EX N',
       'danzig': 'D AH N TS IH CC', 'schaft': 'SH AH F T', 'gerichts': 'G AX RR IH CC T S', 'balck': 'B AH L K', 'mellenthin': 'M EH L AX N T IIH N',
       'patton': 'P EH T AX N', 'sedan': 'S EH D AA N', 'tschir': 'T SH IH EX', 'army': 'Q AAH M IIH', 'n_': 'N', 'stalingrad': 'SH T AAH L IH N K RR AAH T', 'kanntet': 'K AH N T AX T', 'us': 'Q UUH Q EH S', 'elften': 'Q EH L F T AX N'}
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
