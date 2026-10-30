# fallback when the forced alignment loses the path: free recognition with the German LM, then the script words are matched
# to the recognised words (difflib); matched words take the recognised times, the rest are spread between their matched neighbours
import sys, re, json, subprocess, os, difflib
from pocketsphinx import Decoder
D, WAV, OUT = sys.argv[1:4]
M = os.path.join(D, '../models_de/cmusphinx-ptm-voxforge-de-r20171217/')
TEXT = open(D + '/code/script.txt').read().split()
def norm(w): return re.sub(r'[^a-zäöüß0-9]', '', w.lower())
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', WAV, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
d = Decoder(hmm=M + 'model_parameters/voxforge.cd_ptm_5000', dict=M + 'etc/voxforge.dic', lm=M + 'etc/voxforge.lm.bin', samprate=16000, loglevel='ERROR')
d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
rec = [(re.sub(r'\(\d+\)$', '', s.word), s.start_frame / 100, (s.end_frame + 1) / 100) for s in d.seg()]
rec = [r for r in rec if r[0] not in ('<s>', '</s>', '<sil>', '[NOISE]', '(NULL)', '++garbage++')]
a = [norm(w) for w in TEXT]; b = [r[0] for r in rec]
T = [None] * len(TEXT)
for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
    for k in range(blk.size): T[blk.a + k] = [rec[blk.b + k][1], rec[blk.b + k][2]]
# fuzzy pass: unmatched script word vs recognised words inside the gap, by similarity
known = [i for i, t in enumerate(T) if t]
end = rec[-1][2]
for i in range(len(TEXT)):
    if T[i]: continue
    p = max([j for j in known if j < i], default=None); n = min([j for j in known if j > i], default=None)
    t0 = T[p][1] if p is not None else 0.0; t1 = T[n][0] if n is not None else end
    cand = [r for r in rec if r[1] >= t0 - 0.05 and r[2] <= t1 + 0.05]
    best = max(cand, key=lambda r: difflib.SequenceMatcher(None, a[i], r[0]).ratio(), default=None)
    if best and difflib.SequenceMatcher(None, a[i], best[0]).ratio() >= 0.6: T[i] = [best[1], best[2]]; known = sorted(known + [i])
# spread the rest by letter count inside each gap
i = 0
while i < len(TEXT):
    if T[i]: i += 1; continue
    j = i
    while j < len(TEXT) and not T[j]: j += 1
    t0 = T[i - 1][1] if i else 0.0; t1 = T[j][0] if j < len(TEXT) else end
    L = [max(2, len(a[k])) for k in range(i, j)]; tot = sum(L); c = t0
    for k, l in zip(range(i, j), L): T[k] = [c, c + (t1 - t0) * l / tot]; c = T[k][1]
    i = j
out = [[w, round(t[0], 3), round(t[1], 3)] for w, t in zip(TEXT, T)]
for k in range(len(out) - 1): out[k][2] = min(out[k][2], out[k + 1][1])
json.dump(out, open(OUT, 'w'), ensure_ascii=False)
print('matched', sum(1 for x in a if x), len(known)); print(' '.join(f'{w}@{s:.2f}' for w, s, e in out))
