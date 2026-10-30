# German forced alignment with pocketsphinx + the CMU Sphinx VoxForge German model (script words -> start/end)
# usage: align_de.py <dir> <wav> <out.json> [free]   ("free" also runs plain recognition, to check the recording matches the script)
import sys, re, json, subprocess, os
from pocketsphinx import Decoder
D, WAV, OUT = sys.argv[1:4]
M = os.path.join(D, '../models_de/cmusphinx-ptm-voxforge-de-r20171217/')
TEXT = open(D + '/code/script.txt').read().split()
# words not in the dictionary: split into dictionary words (numbers spoken out, compounds split)
EXP = {'1941': 'neunzehn hundert ein und vierzig', 'beinprothese': 'bein prothese', 'ersatzbein': 'ersatz bein', 'fliegerass': 'flieger ass', 'flugplatz': 'flug platz', 'holzkiste': 'holz kiste', 'krankenhauses': 'kranken hauses', 'siegesüberflug': 'sieges über flug', 'wegzunehmen': 'weg zu nehmen', 'zusammengeknoteten': 'zusammen geknoteten', 'abgeschossen': 'ab geschossen', 'absprang': 'ab sprang', 'bettlaken': 'bett laken', '2': 'zweiten', '6': 'sechsten', '1945': 'neunzehn hundert fünf und vierzig', 'kapitulationsbefehle': 'kapitulations befehle', 'inselfestung': 'insel festung', 'radiosender': 'radio sender', 'kriegsgefangene': 'kriegs gefangene', 'zurückgelassenen': 'zurück gelassenen', 'mandschurei': 'mandschu rei', '13': 'dreizehnten', '18': 'achtzehn', '1940': 'neunzehn hundert vierzig', '1942': 'neunzehn hundert zwei und vierzig', '1944': 'neunzehn hundert vier und vierzig', '1893': 'achtzehn hundert drei und neunzig', '1948': 'neunzehn hundert acht und vierzig', '1980': 'neunzehn hundert achtzig',
       '1982': 'neunzehn hundert zwei und achtzig', '25': 'fünf und zwanzig', '11': 'elften', 'artilleriekommandeur': 'artillerie kommandeur',
       'einsatzbereiten': 'einsatz bereiten', 'feldzug': 'feld zug', 'gefangenschaft': 'gefangen schaft', 'gerichtsverfahren': 'gerichts verfahren',
       'heeresgruppe': 'heeres gruppe', 'kriegsende': 'kriegs ende', 'oberbefehlshaber': 'ober befehls haber', 'nationalsozialisten': 'national sozialisten',
       'panzerarmee': 'panzer armee', 'panzerdivision': 'panzer division', 'panzern': 'panzer n_', 'schützenregiment': 'schützen regiment',
       'siebenmal': 'sieben mal', 'tagsüber': 'tags über', 'verteidigungsministerium': 'verteidigungs ministerium'}
ADD = {'bader': 'B AAH D EX', 'prothese': 'P RR OO T EEH Z AX', 'prothesen': 'P RR OO T EEH Z AX N', 'beschossen': 'B AX SH OO S AX N', 'laken': 'L AAH K AX N', 'bomber': 'B OO M B EX', 'britischer': 'B RR IH T IH SH EX', 'cockpit': 'K OO K P IH T', 'colditz': 'K OO L D IH TS', 'flieger': 'F L IIH G EX', 'ass': 'Q AH S', 'galland': 'G AH L AH N T', 'lud': 'L UUH T', 'messerschmitt': 'M EH S EX SH M IH T', 'reparierten': 'RR EH P AH RR IIH EX T AX N', 'sperrten': 'SH P EH EX T AX N', 'spitfire': 'S P IH T F AY EX', 'thelma': 'T EH L M AH', 'geknoteten': 'G AX K N OOH T AX T AX N', 'befreiten': 'B AX F RR AY T AX N', 'beschuss': 'B AX SH UU S', 'corregidor': 'K OO RR EH G IH D OO EX', 'füller': 'F YY L EX', 'gelassenen': 'G AX L AH S AX N AX N', 'honor': 'Q OO N EX', 'japans': 'Y AAH P AAH N S', 'kapitulations': 'K AH P IIH T UUH L AH TS Y OOH N S', 'kapituliert': 'K AH P IIH T UUH L IIH EX T', 'kapitulierte': 'K AH P IIH T UUH L IIH EX T AX', 'macarthur': 'M AX K AAH TH EX', 'mandschu': 'M AH N D SH UU', 'rei': 'RR AY', 'manila': 'M AH N IIH L AH', 'medal': 'M EH D AX L', 'missouri': 'M IH Z UUH RR IIH', 'philippinen': 'F IH L IH P IIH N AX N', 'ranghöchste': 'RR AH NG HH OHH K S T AX', 'ständigem': 'SH T EH N D IH G AX M', 'unterschrieb': 'Q UU N T EX SH RR IIH P', 'uss': 'Y UUH Q EH S Q EH S', 'verlesen': 'F EH EX L EEH Z AX N', 'wainwright': 'V EH N RR AY T', 'kommandeur': 'K OO M AH N D OE EX', 'betrunken': 'B AX T RR UU NG K AX N', 'erschießen': 'Q EH EX SH IIH S AX N', 'erschießung': 'Q EH EX SH IIH S UU NG',
       'heeres': 'HH EEH RR AX S', 'interviews': 'Q IH N T EX V Y UU S', 'kriegs': 'K RR IIH K S', 'kämpft': 'K EH M PF T', 'lothringen': 'L OOH T RR IH NG AX N',
       'maas': 'M AAH S', 'befehls': 'B AX F EEH L S', 'haber': 'HH AAH B EX', 'sozialisten': 'Z OO TS IY AAH L IH S T AX N', 'regiment': 'RR EEH G IH M EH N T',
       'sowjets': 'Z OO V Y EH T S', 'westlich': 'V EH S T L IH CC', 'verteidigungs': 'F EH EX T AY D IIH G UU NG S', 'planern': 'P L AAH N EX N',
       'danzig': 'D AH N TS IH CC', 'schaft': 'SH AH F T', 'gerichts': 'G AX RR IH CC T S', 'balck': 'B AH L K', 'mellenthin': 'M EH L AX N T IIH N',
       'patton': 'P EH T AX N', 'sedan': 'S EH D AA N', 'tschir': 'T SH IH EX', 'army': 'Q AAH M IIH', 'n_': 'N', 'stalingrad': 'SH T AAH L IH N K RR AAH T', 'kanntet': 'K AH N T AX T', 'us': 'Q UUH Q EH S', 'elften': 'Q EH L F T AX N'}
EXP.update({'62': 'zwei und sechzig', '1933': 'neunzehn hundert drei und dreißig', '17': 'siebzehn ten', '87': 'sieben und achtzig', 'sturzkampfbomber': 'sturz kampf bomber', 'herabstürzten': 'herab stürzten', 'fahrwerksbeinen': 'fahrwerks beinen', 'fahrtwind': 'fahrt wind', 'jerichotrompeten': 'jericho trompeten', 'generalluftzeugmeister': 'general luft zeug meister', 'flugzeugproduktion': 'flugzeug produktion', 'kunstflieger': 'kunst flieger', 'zugeschrieben': 'zu geschrieben', 'weltkrieg': 'welt krieg'})
ADD.update({'tödlich': 'T OHH T L IH CC', 'erschoss': 'Q EH EX SH OO S', 'offiziell': 'Q OO F IH TS Y EH L', 'kaufte': 'K AW F T AX', 'brachte': 'B RR AH CC T AX', 'versetzte': 'F EH EX Z EH TS T AX', 'zivilisten': 'TS IH V IH L IH S T AX N', 'ten': 'T AX N', 'luftwaffe': 'L UU F T V AH F AX', 'einstige': 'Q AY N SH T IH G AX', 'bremsten': 'B RR EH M S T AX N', 'sirenen': 'Z IIH RR EEH N AX N', 'propeller': 'P RR OO P EH L EX', 'junkers': 'Y UU NG K EX S', 'förderer': 'F OHH EX D AX RR EX', 'stürzten': 'SH T YY RR TS T AX N', 'udet': 'Q UUH D EH T', 'richthofen': 'RR IH CC T HH OOH F AX N', 'göring': 'G OHH RR IH NG', 'stuka': 'SH T UUH K AH', 'stukas': 'SH T UUH K AH S', 'ju': 'Y UUH', 'jericho': 'Y EEH RR IH CC OO', 'vertuscht': 'F EH EX T UU SH T', 'erproben': 'Q EH EX P RR OOH B AX N', 'fahrwerks': 'F AAH EX V EH EX K S', 'herab': 'HH EH RR AH P', 'heulten': 'HH OY L T AX N', 'zeug': 'TS OY K', 'verunglückt': 'F EH EX Q UU N G L YY K T', 'trompeten': 'T RR OO M P EEH T AX N', 'manfred': 'M AH N F RR EH T'})
EXP.update({'1936': 'neunzehn hundert sechs und dreißig', '1939': 'neunzehn hundert neun und dreißig', '1938': 'neunzehn hundert acht und dreißig', '1935': 'neunzehn hundert fünf und dreißig', '1923': 'neunzehn hundert drei und zwanzig', '1932': 'neunzehn hundert zwei und dreißig', '1': 'ersten', '4': 'vier', '45': 'fünf und vierzig', '30': 'dreißigsten', 'uboote': 'u boote', 'reichskanzler': 'reichs kanzler', 'linienschiff': 'linien schiff', 'entmilitarisierte': 'ent militarisierte', 'sudetenland': 'sudeten land'})
ADD.update({'reichs': 'RR AY CC S', 'ent': 'Q EH N T', 'rüstete': 'RR YY S T AX T AX', 'westerplatte': 'V EH S T EX P L AH T AX', 'versailles': 'V EH EX Z AH Y', 'hofften': 'HH OO F T AX N', 'schaltete': 'SH AH L T AX T AX', 'militarisierte': 'M IH L IH T AAH RR IH Z IIH EX T AX', 'sudeten': 'Z UU D EEH T AX N', 'u': 'Q UUH'})
EXP.update({'100000': 'hundert tausend', '132': 'hundert zwei und dreißig', '1918': 'neunzehn hundert achtzehn', '1919': 'neunzehn hundert neunzehn', '1928': 'neunzehn hundert acht und zwanzig',
            '1929': 'neunzehn hundert neun und zwanzig', '1934': 'neunzehn hundert vier und dreißig', '23': 'drei und zwanzigsten', '42': 'vier komma zwei', '26': 'zwei komma sechs',
            '28': 'acht und zwanzigsten', '31': 'ein und dreißigsten', '37': 'sieben und dreißig', '48': 'acht und vierzig', '7': 'siebten', 'einmarsch': 'ein marsch',
            'gebiets': 'gebiet s_', 'gegenangriffs': 'gegen angriffs', 'goldmark': 'gold mark', 'grenzgebiete': 'grenz gebiete', 'nichtangriffspakt': 'nicht angriffs pakt',
            'reichspräsident': 'reichs präsident', 'ruhrgebiet': 'ruhr gebiet', 'ssmänner': 'ss männer', 'staatsoberhaupt': 'staats ober haupt', 'zusatzprotokoll': 'zusatz protokoll',
            'fernab': 'fern ab', 'gleichgeschaltet': 'gleich geschaltet', 'aufgerüstet': 'auf gerüstet', 'unbesiegt': 'un besiegt'})
ADD.update({'s_': 'S', 'achtel': 'Q AH X T AX L', 'alliierten': 'Q AH L IH IIH EX T AX N', 'aufregendsten': 'Q AW F RR EEH G AX N T S T AX N', 'belgische': 'B EH L G IH SH AX',
            'besiedelte': 'B AX Z IIH D AX L T AX', 'boykottiert': 'B OY K OO T IIH EX T', 'chamberlain': 'T SH EEH M B EX L IH N', 'daladier': 'D AH L AH D Y EEH', 'druckte': 'D RR UU K T AX',
            'entmilitarisiert': 'Q EH N T M IH L IH T AAH RR IH Z IIH EX T', 'erdolcht': 'Q EH EX D OO L CC T', 'ermächtigungsgesetz': 'Q EH EX M EH CC T IH G UU NG S G AX Z EH TS',
            'fabriken': 'F AH B RR IIH K AX N', 'feindlicher': 'F AY N T L IH CC EX', 'garantierten': 'G AH RR AH N T IIH EX T AX N', 'geliehenem': 'G AX L IIH AX N AX M',
            'gleiwitz': 'G L AY V IH TS', 'grenz': 'G RR EH N TS', 'hindenburg': 'HH IH N D AX N B UU EX K', 'mussolini': 'M UU S OO L IIH N IIH', 'nsdap': 'Q EH N Q EH S D EEH Q AAH P EEH',
            'polens': 'P OOH L AX N S', 'polnische': 'P OO L N IH SH AX', 'profitierten': 'P RR OO F IIH T IIH EX T AX N', 'protektorat': 'P RR OO T EH K T OO RR AAH T',
            'protesten': 'P RR OO T EH S T AX N', 'putsch': 'P UU T SH', 'reichs': 'RR AY CC S', 'rollten': 'RR OO L T AX N', 'ss': 'Q EH S Q EH S', 'synagogen': 'Z YY N AH G OOH G AX N',
            'teilten': 'T AY L T AX N', 'unterzeichnete': 'Q UU N T EX TS AY CC N AX T AX', 'verrätern': 'F EH EX RR EEH T EX N', 'versailler': 'V EH EX Z AH Y EX',
            'wehrmacht': 'V EEH EX M AH X T', 'zerschlagen': 'TS EH EX SH L AAH G AX N', 'überfielen': 'Q YYH B EX F IIH L AX N', 'übten': 'Q YYH P T AX N', 'pakt': 'P AH K T',
            'geschaltet': 'G AX SH AH L T AX T', 'gerüstet': 'G AX RR YY S T AX T', 'besiegt': 'B AX Z IIH K T', 'un': 'Q UU N'})
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
        t = rough[e][2]; cand = [x for x in sil if x > cuts[-1] + 0.3 and abs(x - t) < 0.8]   # the pause right after this sentence, never one already used
        cuts.append((min(cand, key=lambda x: abs(x - t)) if cand else t) + 0.06)
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
