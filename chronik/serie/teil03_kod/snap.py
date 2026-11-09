# Whisper glues the pause after a sentence to the next word: move the start of every word that follows punctuation
# (and its predecessor's end) to the real speech onset found in the audio energy (vcut.wav, before the page-turn gaps)
import json, numpy as np
from scipy.io import wavfile
D = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t3l/'
W = json.load(open(D + 'words_orig.json')); sr, x = wavfile.read(D + 'vcut.wav'); x = np.abs(x.astype(np.float32))
hop = int(0.01 * sr); env = np.array([x[i:i + hop].mean() for i in range(0, len(x) - hop, hop)])
thr = np.percentile(env, 60) * 0.12
def onset(a, b):
    """first 10 ms frame after a silence of >= 0.12 s inside [a, b]; None if there is no pause"""
    i0, i1 = int(a * 100), int(b * 100); q = 0
    for i in range(i0, min(i1, len(env))):
        if env[i] < thr: q += 1
        elif q >= 12: return i / 100.0 - 0.02
        else: q = 0
    return None
n = 0; big = []
for k in range(1, len(W)):
    if not W[k - 1][0][-1] in '.,:;“"': continue
    a = W[k - 1][2] - 0.25; b = min(W[k][2], W[k][1] + 0.9)
    o = onset(a, b)
    if o is not None and abs(o - W[k][1]) > 0.06:
        if o - W[k][1] > 0.2: big.append((W[k][0], round(W[k][1], 2), round(o, 2)))
        W[k][1] = round(o, 3); W[k - 1][2] = round(min(W[k - 1][2], o - 0.1), 3); n += 1
json.dump(W, open(D + 'words_orig.json', 'w'), ensure_ascii=False)
print(n, 'starts moved;', len(big), 'by more than 0.2 s'); print(big[:40])
