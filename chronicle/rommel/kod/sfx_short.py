# sound effects for the English Rommel short
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import short as V
T = V.T; w = V.w; ST = V.ST
sfxlib.out = np.zeros((int(SR * T), 2))
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def hit(t0, g=0.10, f=85): add(t0, thud(0.9, f), g)
def air(t0, g=0.045): add(t0, whoosh(0.5, 200, 1400), g, rng.uniform(-0.3, 0.3))
def typing(t0, n, step=0.05, g=0.04):
    for i in range(n): add(t0 + i * step, clack(), g * rng.uniform(0.7, 1.0), rng.uniform(-0.2, 0.2))
for s, fn in V.ANCH[1:]: air(s - 0.08)
add(0.02, impact(), 0.20); hit(w('Hitler', 0), 0.10, 70); hit(w('trial', 0), 0.12, 80); add(w('poison', 0), impact(2.5), 0.16)
hit(w('Erwin', 1), 0.13, 65); add(w('Erwin', 1), swell(2.0, 52), 0.08)
hit(w('lieutenant', 2), 0.08, 95); add(w('stormed', 2), fio(whoosh(1.4, 400, 2000)), 0.05); add(w('Matajur', 2), metal(220, 1.0), 0.04)
for i in range(20): add(w('9,000', 2) - 0.3 + i * 0.05, tick(), 0.03)
hit(w('9,000', 2) + 0.7, 0.11, 75)
add(ST[3], fio(engine(3.5, 55, 0.4, 500), 0.4, 0.8), 0.07); add(w('even', 3), fio(whoosh(1.2, 200, 900)), 0.07); hit(w('lost', 3), 0.10, 90)
add(w('Ghost', 4) - 0.3, fio(drone4(2.2, 52), 0.3, 0.8), 0.08); hit(w('Ghost', 4), 0.10, 70)
panned(ST[5] - 0.2, fio(engine(2.2, 95, 0.3, 900), 0.4, 0.8), 0.07, -0.7, 0.7); hit(w('Africa', 5), 0.12, 65)
for i in range(5): add(w('drove', 6) + i * 0.6, boom_far(), 0.12, -0.4 + i * 0.2)
hit(w('Egypt', 6) - 0.3, 0.10, 80)
add(ST[7], fio(wind(2.0)), 0.04); add(w('stop', 7), scratch(0.35), 0.08); hit(w('stop', 7), 0.10, 90)
add(ST[8], flip(), 0.08); typing(w('press', 8), 14, 0.055); add(w('Desert', 8) - 0.15, impact(2.5), 0.16)
hit(w('youngest', 9), 0.12, 70); add(w('youngest', 9), metal(200, 1.4), 0.04)
for i in range(3): add(ST[10] + i * 0.9, boom_far(), 0.10, -0.3 + i * 0.3)
hit(w('lost', 10), 0.12, 60)
for i in range(5): add(w('July', 10) - 0.2 + i * 0.12, flip(), 0.05)
hit(w('name', 10), 0.12, 70)
typing(ST[11] + 0.1, 16, 0.045); add(w('goodbye', 11), tone(110, 2.5), 0.05); add(w('got', 11), door(), 0.07)
add(w('cyanide', 11) - 0.2, fio(drone4(2.0, 41), 0.2, 0.8), 0.09); hit(w('cyanide', 11), 0.12, 55)
add(ST[12], swell(3.0, 49), 0.10); add(w('hero', 12) - 0.1, impact(3.0), 0.18)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.9)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
