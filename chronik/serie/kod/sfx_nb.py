# sound for the notebook sample: cover thump, page turns (paper rustle sweeping across), pen scratching while words are written,
# pencil on paper while sketching, the tape on the photo
import sys, numpy as np
sys.path.insert(0, sys.argv[1] + '/code')
import sfxlib
from sfxlib import *
T = float(sys.argv[2]); sfxlib.out = np.zeros((int(SR * T), 2))
def page_turn(dur=0.9):
    n = int(SR * dur); t = np.arange(n) / SR; x = rng.normal(0, 1, n)
    x = bp(x, 1200, 7000) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    x *= 0.6 + 0.4 * np.abs(np.sin(t * 38))              # crinkle
    flap = np.zeros(n); k = int(SR * (dur - 0.12)); fl = thud(0.25, 110); flap[k:k + len(fl)] = fl[:n - k]
    return norm(x) * 0.8 + flap * 0.6
def pen(t0, dur, g=0.05):
    for i in range(int(dur / 0.11)): add(t0 + i * 0.11, scratch(0.14), g * rng.uniform(0.6, 1.0), rng.uniform(-0.15, 0.15))
add(0.05, wind(1.0) * 0.3, 0.02)
add(1.0, page_turn(1.0), 0.16, -0.1); add(1.95, thud(0.6, 70), 0.10)
for t0, d in ((2.15, 0.5), (2.6, 1.0), (3.4, 0.8), (4.3, 0.9)): pen(t0, d, 0.05)
pen(4.5, 1.5, 0.035); pen(6.0, 0.4, 0.06)
add(6.6, page_turn(1.0), 0.16, -0.2)
for t0, d in ((7.7, 0.6), (8.2, 0.8)): pen(t0, d, 0.05)
add(8.7, scratch(0.3), 0.05); pen(9.0, 0.3, 0.05)
for t0, d in ((11.0, 0.5), (11.4, 0.9), (12.6, 0.7), (13.0, 0.6)): pen(t0, d, 0.05)
pen(12.3, 0.35, 0.05); pen(12.8, 1.0, 0.035)
o = sfxlib.out; o /= max(1.0, np.abs(o).max() / 0.9); wavfile.write(sys.argv[1] + '/out/sfx_nb.wav', SR, (o * 32767).astype(np.int16)); print('ok')
