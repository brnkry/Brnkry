# sound for the notebook sample v3: no writing noise; the stamps, the page turn, the tape, a soft swish for each red cross
import sys, numpy as np
sys.path.insert(0, sys.argv[1] + '/code')
import sfxlib
from sfxlib import *
T = float(sys.argv[2]); sfxlib.out = np.zeros((int(SR * T), 2))
def page_turn(dur=0.9):
    n = int(SR * dur); t = np.arange(n) / SR; x = rng.normal(0, 1, n)
    x = bp(x, 1200, 7000) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5 * (0.6 + 0.4 * np.abs(np.sin(t * 38)))
    flap = np.zeros(n); k = int(SR * (dur - 0.12)); fl = thud(0.25, 110); flap[k:k + len(fl)] = fl[:n - k]
    return norm(x) * 0.8 + flap * 0.6
def swish(dur=0.3):
    n = int(SR * dur); t = np.arange(n) / SR; return norm(bp(rng.normal(0, 1, n), 2500, 8000)) * np.sin(np.pi * t / dur) ** 2
add(0.05, stampthump(), 0.16)
add(4.15, swish(0.3), 0.05); add(4.6, page_turn(0.9), 0.16, -0.2)
add(6.5, stampthump(), 0.14); add(6.7, rustle(0.4), 0.05)
add(11.5, swish(0.3), 0.05)
o = sfxlib.out; o /= max(1.0, np.abs(o).max() / 0.9); wavfile.write(sys.argv[1] + '/out/sfx_nb3.wav', SR, (o * 32767).astype(np.int16)); print('ok')
