# shorten pauses between phrases; write new voice wav, the time map and remapped words
import json, sys, numpy as np
from scipy.io import wavfile
D = sys.argv[1]
sr, x = wavfile.read(D + '/v48.wav'); x = x.astype(np.float32)
P = [(2.71,2.93),(3.71,3.85),(5.08,5.63),(6.75,7.68),(14.16,14.82),(16.99,17.20),(20.65,21.39),(24.32,24.46),(25.75,26.33),(29.04,29.43),(31.12,31.72),(34.09,34.80),(39.01,39.67),(43.52,43.70),(45.88,46.63),(48.86,49.38),(52.81,52.95),(56.03,56.66),(59.71,60.02),(62.28,62.93),(67.24,67.79),(69.75,70.00),(71.53,72.20),(73.12,73.26),(74.47,74.69),(77.80,78.42),(82.85,83.43),(84.55,84.90),(86.04,86.60),(87.88,88.51),(91.24,91.75),(94.87,95.51),(96.23,96.55),(99.64,100.31),(103.59,103.80),(106.65,107.27),(110.16,110.87),(112.20,112.62)]
KEEP = 0.30; KEEP_HOOK = 0.38
segs = []; pos = 0.0; outp = []; newt = 0.0; fade = int(0.03 * sr)
for a, b in P:
    keep = KEEP_HOOK if a < 6 else KEEP
    if b - a <= keep: continue
    cut0 = a + keep / 2; cut1 = b - keep / 2           # drop the middle of the pause
    segs.append((pos, cut0, newt)); outp.append(x[int(pos * sr):int(cut0 * sr)]); newt += cut0 - pos; pos = cut1
segs.append((pos, len(x) / sr, newt)); outp.append(x[int(pos * sr):])
for i in range(1, len(outp)):   # short crossfade at each join
    f = min(fade, len(outp[i - 1]), len(outp[i])); r = np.linspace(0, 1, f)
    outp[i - 1][-f:] *= (1 - r) if outp[i - 1].ndim == 1 else (1 - r)[:, None]
    outp[i][:f] *= r if outp[i].ndim == 1 else r[:, None]
y = np.concatenate(outp)
wavfile.write(D + '/v_cut.wav', sr, y.astype(np.int16))
json.dump(segs, open(D + '/timemap.json', 'w'))
def M(t):
    for s0, s1, n0 in segs:
        if t < s1 + 1e-6: return n0 + max(0.0, t - s0)
    s0, s1, n0 = segs[-1]; return n0 + t - s0
W = json.load(open(D + '/words.json'))
json.dump([[w, round(M(a), 3), round(M(b), 3)] for w, a, b in W], open(D + '/words_cut.json', 'w'), ensure_ascii=False)
print('old', len(x) / sr, 'new', len(y) / sr)
