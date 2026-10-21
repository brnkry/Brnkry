# sound effects for the Yamamoto short
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
def typing(t0, n, step=0.03, g=0.035):
    for i in range(n): add(t0 + i * step, clack(), g * rng.uniform(0.7, 1.0), rng.uniform(-0.2, 0.2))
for s, fn, tr in V.ANCH[1:]:
    if tr and tr[0] == 'whip': add(s - 0.2, whoosh(0.6, 300, 2400), 0.11, 0.5 * tr[1])
    else: air(s - 0.08)
add(0.02, impact(), 0.18); panned(0.3, fio(engine(5.5, 85, 0.3, 900), 0.6, 1.2), 0.07, -0.7, 0.7); hit(w('sixteen', 0), 0.10, 80); hit(w('one', 0), 0.12, 65)
add(w('because', 1) - 0.4, flip(), 0.08); typing(w('because', 1) - 0.25, 60, 0.018); add(w('because', 1) + 0.95, stampthump(), 0.20)
hit(w('Isoroku', 2), 0.12, 65); add(w('Isoroku', 2), swell(2.0, 52), 0.07); panned(w('who', 2), fio(jet(1.6), 0.2, 0.6), 0.06, 0.6, -0.6)
add(ST[3], tone(98, 2.5), 0.05); hit(w('fingers', 4), 0.10, 75)
hit(w('Harvard', 5), 0.08, 95); hit(w('Washington', 5), 0.08, 95); add(ST[6], fio(wind(3.0)), 0.04)
hit(w('six', 7), 0.09, 85); hit(w('maybe', 7), 0.09, 85); add(w('confidence', 7) - 0.2, fio(drone4(2.0, 46), 0.3, 0.8), 0.06)
panned(w('and', 8), fio(engine(2.0, 95, 0.3, 900), 0.3, 0.6), 0.06, -0.6, 0.6); hit(w('four', 9), 0.10, 70)
add(ST[10], sonar_ping(900, 2.0), 0.05); add(w('codebreakers', 10), static(1.2, 0.6), 0.03)
hit(w('time', 11), 0.10, 80)
panned(ST[12], fio(engine(2.6, 95, 0.35, 900), 0.4, 0.6), 0.07, -0.6, 0.6); hit(w('P-38s', 12), 0.11, 70); add(w('went', 12) - 0.1, mg_burst(7), 0.08, 0.2); add(w('down', 12) + 0.3, impact(2.5), 0.15)
hit(w('one', 13), 0.09, 70); add(ST[14] - 0.35, whoosh(0.7, 250, 1800), 0.09, 0.4); add(w('live', 14), swell(2.0, 49), 0.08)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.6)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
