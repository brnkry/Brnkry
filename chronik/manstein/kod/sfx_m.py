# sound effects for the Manstein short: every transition, stamp, arrow, written word and film shot gets its own sound
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import mshort as V
T = V.T; w = V.w; ST = V.ST
sfxlib.out = np.zeros((int(SR * T), 2))
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def hit(t0, g=0.10, f=85): add(t0, thud(0.9, f), g)
def air(t0, g=0.045): add(t0, whoosh(0.5, 200, 1400), g, rng.uniform(-0.3, 0.3))
def stamp_(t0): add(t0, stampthump(), 0.20)
def pen(t0, dur, g=0.05):
    for i in range(int(dur / 0.16)): add(t0 + i * 0.16, scratch(0.18), g * rng.uniform(0.6, 1.0), rng.uniform(-0.2, 0.2))
def typing(t0, n, step=0.03, g=0.03):
    for i in range(n): add(t0 + i * step, clack(), g * rng.uniform(0.7, 1.0), rng.uniform(-0.2, 0.2))
for s, fn, tr in V.ANCH[1:]:
    if tr and tr[0] == 'whip': add(s - 0.2, whoosh(0.6, 300, 2400), 0.11, 0.5 * tr[1])
    else: air(s - 0.08)
# film shots
add(0.02, impact(), 0.16); add(0.0, fio(wind(3.0)), 0.03)
panned(ST[1] - 0.1, fio(engine(3.2, 80, 0.3, 900), 0.5, 0.8), 0.07, -0.6, 0.6)
panned(V.at(8) - 0.1, fio(engine(1.9, 85, 0.3, 900), 0.3, 0.5), 0.06, 0.6, -0.6)
add(V.at(5, 'ein'), fio(wind(4.5)), 0.04); add(V.at(5, 'ein') + 0.3, boom_far(), 0.07)
add(V.at(13), boom_far(), 0.08); add(V.at(13, 'Sewastopol') + 0.2, boom_far(), 0.08); add(V.at(13, 'und') + 0.1, impact(2.5), 0.12)
for k in range(4): add(ST[15] + 0.2 + k * 0.85, boom_far(2.5), 0.07)
add(ST[16], fio(static(2.0, 0.6), 0.3, 0.6), 0.03); add(ST[16] + 0.2, boom_far(2.0), 0.05)
# hook, France
stamp_(w('nicht', 0) - 0.03)
add(w('sechs', 1) - 0.05, whoosh(0.8, 200, 1200), 0.07)
# name
hit(w('Manstein', 2), 0.10, 70); add(w('Manstein', 2), swell(2.0, 52), 0.06)
pen(w('Fritz', 2) - 0.05, 0.5); pen(w('Lewinski', 2) - 0.35, 0.5); add(w('Namen', 3) - 0.05, scratch(0.35), 0.08)
add(w('Ersten', 4) - 0.05, whoosh(0.7, 200, 1200), 0.06)
# the plan
pen(w('Ardennen', 5) - 0.1, 0.9, 0.06); add(w('passierbar', 5) - 0.25, whoosh(0.6, 250, 1500), 0.06)
stamp_(w('beiseite', 6) - 0.05); add(w('Korpskommando', 6) - 0.05, scratch(0.35), 0.06)
add(w('oben', 7) - 0.25, scratch(0.35), 0.06); add(w('oben', 7) - 0.05, whoosh(0.5, 400, 2400), 0.06)
# map 1940
hit(V.at(8) + 0.2, 0.08, 85); add(w('stießen', 8) - 0.05, whoosh(2.2, 150, 900), 0.08); hit(w('Ärmelkanal', 8), 0.08, 75)
# Crimea, the order
hit(w('Krim', 9), 0.09, 75)
add(V.at(10), flip(), 0.08); typing(ST[10] + 0.3, 40, 0.018); typing(w('20.', 10) - 0.1, 38, 0.018); pen(w('Befehl', 10) - 0.2, 0.66)
add(w('Verständnis', 11) - 0.1, scratch(0.6), 0.05); add(w('Verständnis', 11) + 0.5, scratch(0.5), 0.05)
add(ST[12], fio(drone4(4.5, 46), 0.5, 1.0), 0.06); hit(w('Zehntausende', 12), 0.10, 60)
# 1942
hit(w('Generalfeldmarschall', 13), 0.10, 70)
hit(w('Stalingrad', 14), 0.09, 70); hit(w('50', 15), 0.10, 65); stamp_(w('abgebrochen', 16) - 0.03)
stamp_(w('abgesetzt', 17) - 0.03)
# trial
add(w('In', 19) - 0.2, whoosh(0.8, 250, 1600), 0.07)
for i in range(9): add(w('neun', 19) - 0.1 + i * 0.055, tick(), 0.05)
for i in range(8): add(w('siebzehn', 19) - 0.1 + 0.33 + i * 0.035, tick(), 0.04)
stamp_(w('18', 20) - 0.05)
hit(ST[21] + 0.05, 0.07, 90)
# book, ending
add(w('Buch', 22) - 0.25, flip(), 0.09); hit(w('Verlorene', 22), 0.09, 70)
hit(w('kaum', 24), 0.08, 70)
add(w('Jahrzehntelang', 25) + 0.6, whoosh(0.8, 250, 1600), 0.07); hit(w('saubere', 25), 0.07, 80); add(w('anders', 26) - 0.1, scratch(0.35), 0.09)
add(ST[27], swell(3.0, 49), 0.07)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.6)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
