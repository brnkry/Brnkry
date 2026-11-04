# German forced alignment with pocketsphinx + the CMU Sphinx VoxForge German model (script words -> start/end)
# usage: align_de.py <dir> <wav> <out.json> [free]   ("free" also runs plain recognition, to check the recording matches the script)
import sys, re, json, subprocess, os
from pocketsphinx import Decoder
D, WAV, OUT = sys.argv[1:4]
M = os.path.join(D, '../models_de/cmusphinx-ptm-voxforge-de-r20171217/')
TEXT = open(D + '/code/script.txt').read().split()
# words not in the dictionary: split into dictionary words (numbers spoken out, compounds split)
EXP = {'2': 'zweiten', '6': 'sechsten', '1945': 'neunzehn hundert fünf und vierzig', 'kapitulationsbefehle': 'kapitulations befehle', 'inselfestung': 'insel festung', 'radiosender': 'radio sender', 'kriegsgefangene': 'kriegs gefangene', 'zurückgelassenen': 'zurück gelassenen', 'mandschurei': 'mandschu rei', '13': 'dreizehnten', '18': 'achtzehn', '1940': 'neunzehn hundert vierzig', '1942': 'neunzehn hundert zwei und vierzig', '1944': 'neunzehn hundert vier und vierzig', '1893': 'achtzehn hundert drei und neunzig', '1948': 'neunzehn hundert acht und vierzig', '1980': 'neunzehn hundert achtzig',
       '1982': 'neunzehn hundert zwei und achtzig', '25': 'fünf und zwanzig', '11': 'elften', 'artilleriekommandeur': 'artillerie kommandeur',
       'einsatzbereiten': 'einsatz bereiten', 'feldzug': 'feld zug', 'gefangenschaft': 'gefangen schaft', 'gerichtsverfahren': 'gerichts verfahren',
       'heeresgruppe': 'heeres gruppe', 'kriegsende': 'kriegs ende', 'oberbefehlshaber': 'ober befehls haber', 'nationalsozialisten': 'national sozialisten',
       'panzerarmee': 'panzer armee', 'panzerdivision': 'panzer division', 'panzern': 'panzer n_', 'schützenregiment': 'schützen regiment',
       'siebenmal': 'sieben mal', 'tagsüber': 'tags über', 'verteidigungsministerium': 'verteidigungs ministerium'}
ADD = {'befreiten': 'B AX F RR AY T AX N', 'beschuss': 'B AX SH UU S', 'corregidor': 'K OO RR EH G IH D OO EX', 'füller': 'F YY L EX', 'gelassenen': 'G AX L AH S AX N AX N', 'honor': 'Q OO N EX', 'japans': 'Y AAH P AAH N S', 'kapitulations': 'K AH P IIH T UUH L AH TS Y OOH N S', 'kapituliert': 'K AH P IIH T UUH L IIH EX T', 'kapitulierte': 'K AH P IIH T UUH L IIH EX T AX', 'macarthur': 'M AX K AAH TH EX', 'mandschu': 'M AH N D SH UU', 'rei': 'RR AY', 'manila': 'M AH N IIH L AH', 'medal': 'M EH D AX L', 'missouri': 'M IH Z UUH RR IIH', 'philippinen': 'F IH L IH P IIH N AX N', 'ranghöchste': 'RR AH NG HH OHH K S T AX', 'ständigem': 'SH T EH N D IH G AX M', 'unterschrieb': 'Q UU N T EX SH RR IIH P', 'uss': 'Y UUH Q EH S Q EH S', 'verlesen': 'F EH EX L EEH Z AX N', 'wainwright': 'V EH N RR AY T', 'kommandeur': 'K OO M AH N D OE EX', 'betrunken': 'B AX T RR UU NG K AX N', 'erschießen': 'Q EH EX SH IIH S AX N', 'erschießung': 'Q EH EX SH IIH S UU NG',
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
def forced(raw, words):
    d = Decoder(hmm=M + 'model_parameters/voxforge.cd_ptm_5000', dict=M + 'etc/voxforge.dic', samprate=16000, bestpath=False, loglevel='ERROR', beam=1e-100, wbeam=1e-80, pbeam=1e-100)
    for k, v in ADD.items():
        if d.lookup_word(k) is None: d.add_word(k, v, True)
    toks, owner = [], []
    for i, w in enumerate(words):
        for t in EXP.get(norm(w), norm(w)).split():
            if d.lookup_word(t) is None: raise SystemExit('missing: ' + t)
            toks.append(t); owner.append(i)
    d.set_align_text(' '.join(toks)); d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
    if d.seg() is None: return None
    al = [(re.sub(r'\(\d+\)$', '', s.word), s.start_frame / 100, (s.end_frame + 1) / 100) for s in d.seg()]
    al = [a for a in al if a[0] not in ('<s>', '</s>', '<sil>', '[NOISE]', '(NULL)', '++garbage++')]
    if len(al) != len(toks): return None
    return [[w, round([a for a, o in zip(al, owner) if o == i][0][1], 3), round([a for a, o in zip(al, owner) if o == i][-1][2], 3)] for i, w in enumerate(words)]
if 'chunks' in sys.argv:
    # long takes: cut at the pauses between sentences (rough times from align_free.py's json), align each sentence on its own
    rough = json.load(open(sys.argv[sys.argv.index('chunks') + 1])); SR = 16000
    sil = [float(v) for v in re.findall(r'silence_start: ([0-9.]+)', subprocess.run(['ffmpeg', '-i', WAV, '-af', 'silencedetect=noise=-36dB:d=0.12', '-f', 'null', '-'], capture_output=True, text=True).stderr)]
    ends = [i for i, w in enumerate(TEXT) if w[-1] in '.?!' and not w[:-1].isdigit()]; cuts = [0.0]; prev = 0
    for e in ends[:-1]:
        t = rough[e][2]; c = min(sil, key=lambda x: abs(x - t)); cuts.append(c + 0.06)
    cuts.append(len(raw) / 2 / SR); out = []; st = 0
    for k, e in enumerate(ends):
        a, b = cuts[k], cuts[k + 1]; seg = raw[int(a * SR) * 2:int(b * SR) * 2]; ws_ = TEXT[st:e + 1]
        r = forced(seg, ws_)
        if r is None: print('chunk failed, rough times kept:', ' '.join(ws_)); r = [list(x) for x in rough[st:e + 1]]
        else: r = [[w, round(x + a, 3), round(y + a, 3)] for w, x, y in r]
        out += r; st = e + 1
else:
    out = forced(raw, TEXT)
for i in range(len(out) - 1): out[i][2] = min(out[i][2], out[i + 1][1])
json.dump(out, open(OUT, 'w'), ensure_ascii=False); print(' '.join(f'{w}@{a:.2f}' for w, a, b in out))
