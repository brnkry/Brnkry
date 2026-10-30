# sound for the 30 s sample: rotor, radio static, typewriter, hits, music handled in the mix
import sys, json
sys.path.insert(0, sys.argv[1])
import numpy as np, sfxlib
from sfxlib import *
sfxlib.out = np.zeros((int(SR * 30), 2))
def rotor(dur, rate=5.2):
    n = int(SR * dur); t = np.arange(n) / SR
    y = lp(rng.normal(0, 1, n), 380) * (0.35 + 0.65 * np.maximum(0, np.sin(2 * np.pi * rate * t)) ** 6) + 0.25 * engine(dur, 96, 0.2, 900)
    return norm(y) * np.minimum(1, np.minimum(t / 1.5, (dur - t) / 1.2))
def fio(x, a=0.6, b=0.8):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
add(0.0, fio(wind(10.0), 1.5, 2.0), 0.04)                     # jungle air
panned(0.3, rotor(9.5), 0.16, -0.7, 0.6)                       # helicopter passing
for i, c in enumerate('18. OKTOBER 1965'):
    if c != ' ': add(0.7 + i * 0.08, clack(), 0.07, rng.uniform(-0.2, 0.2))
add(2.3, thud(0.9, 80), 0.12)
add(5.0, whoosh(0.7, 200, 1200), 0.07)
add(6.4, whoosh(1.2, 300, 1500), 0.05, -0.4)
add(7.6, fio(static(1.6, 1.0), 0.05, 0.6), 0.05)              # radio contact lost
add(7.7, thud(1.2, 58), 0.15)
add(10.6, swell(2.5, 44), 0.08); add(10.8, impact(), 0.22)
for i in range(18): add(15.2 + i * 0.1, tick(), 0.045)
add(17.1, thud(1.0, 70), 0.14)
for k in (19.4, 20.5, 21.6): add(k, whoosh(0.5, 250, 1400), 0.07); add(k + 0.35, thud(0.8, 95), 0.09)
add(23.0, scratch(0.4), 0.05)
add(25.9, swell(3.0, 41), 0.09); add(26.7, impact(), 0.30)
o = sfxlib.out; o /= max(1.0, np.abs(o).max() / 0.9); wavfile.write(sys.argv[2], SR, (o * 32767).astype(np.int16)); print('ok')
