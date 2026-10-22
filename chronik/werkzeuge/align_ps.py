# forced alignment with pocketsphinx (acoustic model, phone level), script words -> start/end times
# usage: align_ps.py <dir> <wav> <out.json>
import sys, re, json, subprocess
from pocketsphinx import Decoder
D, WAV, OUT = sys.argv[1:4]
TEXT = open(D + '/code/script.txt').read().split()
EXP = {'18': 'eighteenth', '1943': 'nineteen forty three'}
ADD = {'isoroku': 'IY S OW R OW K UW', 'tsushima': 'T S UW SH IY M AH', 'p-38s': 'P IY TH ER T IY EY T S', 'bougainville': 'B UW G AH N V IH L'}
d = Decoder(samprate=16000, bestpath=False, loglevel='ERROR')
for k, v in ADD.items():
    if d.lookup_word(k) is None: d.add_word(k, v, True)
toks, owner = [], []
for i, w in enumerate(TEXT):
    k = re.sub(r"[^a-z0-9'-]", '', w.lower())
    for t in EXP.get(k, k).split(): toks.append(t); owner.append(i)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', WAV, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
d.set_align_text(' '.join(toks)); d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
al = [(s.word, s.start_frame / 100, (s.end_frame + 1) / 100) for s in d.seg()]
al = [(re.sub(r'\(\d+\)$', '', a[0]),) + a[1:] for a in al if a[0] not in ('<s>', '</s>', '<sil>', '[NOISE]', '(NULL)')]
print('tokens', len(toks), 'aligned', len(al))
assert len(al) == len(toks)
out = []
for i, w in enumerate(TEXT):
    seg = [a for a, o in zip(al, owner) if o == i]
    out.append([w, round(seg[0][1], 3), round(seg[-1][2], 3)])
json.dump(out, open(OUT, 'w')); print(' '.join(f'{w}@{a:.2f}' for w, a, b in out))
