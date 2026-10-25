# Per-line forced alignment (pocketsphinx). usage: python3 align_chunks.py audio.wav chunks.json out.json
# chunks.json: [[speaker, t0, t1, "spoken text"], ...]  -> out: [[speaker, [[word, s, e], ...]], ...]
import sys, subprocess, json, re
import numpy as np
from pocketsphinx import Decoder
SR = 16000
raw = subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-f','s16le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
x = np.frombuffer(raw, np.int16)
out = []
for spk, t0, t1, text in json.load(open(sys.argv[2])):
    words = re.sub(r"[^a-z' ]+", ' ', text.lower()).split()
    d = Decoder(samprate=SR, bestpath=False)
    fixed = []
    for w in words:
        if d.lookup_word(w) is None: w = w.replace("'", "")
        if d.lookup_word(w) is None: print('OOV', w, file=sys.stderr); continue
        fixed.append(w)
    d.set_align_text(' '.join(fixed))
    d.start_utt(); d.process_raw(np.concatenate([x[int(t0*SR):int(t1*SR)], np.zeros(SR//2, np.int16)]).tobytes(), full_utt=True); d.end_utt()
    segs = d.seg()
    if segs is None: print('FAIL', text, file=sys.stderr); out.append([spk, []]); continue
    seg = [[s.word.split('(')[0], round(t0 + s.start_frame/100, 2), round(t0 + (s.end_frame+1)/100, 2)] for s in segs if s.word not in ('<s>','</s>','<sil>','[NOISE]')]
    out.append([spk, seg]); print(spk, ' '.join(f'{w}@{s:.2f}' for w, s, e in seg))
json.dump(out, open(sys.argv[3], 'w'))
