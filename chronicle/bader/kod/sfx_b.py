# sound effects for the Bader short: engines, the falling crate, the gun camera, typed message, stamps, transitions
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import dbshort as V
T = V.T; ws = V.ws
sfxlib.out = np.zeros((int(SR * T), 2))
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def hit(t0, g=0.10, f=85): add(t0, thud(0.9, f), g)
def stamp_(t0): add(t0, stampthump(), 0.20)
def pen(t0, dur, g=0.05):
    for i in range(int(dur / 0.16)): add(t0 + i * 0.16, scratch(0.18), g * rng.uniform(0.6, 1.0), rng.uniform(-0.2, 0.2))
for s, fn, tr in V.ANCH[1:]:
    if tr and tr[0] == 'whip': add(s - 0.2, whoosh(0.6, 300, 2400), 0.11, 0.5 * tr[1])
    else: add(s - 0.08, whoosh(0.5, 200, 1400), 0.045, rng.uniform(-0.3, 0.3))
# bombers over France, the crate on its chute
add(0.0, fio(engine(5.6, 70, 0.35, 700), 0.4, 1.0), 0.09); add(ws('dropped') - 0.05, whoosh(0.8, 300, 1600), 0.05); add(ws('dropped') + 0.2, wind(3.0), 0.03)
hit(ws('August'), 0.08, 85)
hit(ws('Douglas'), 0.09, 75); add(ws('Douglas'), swell(2.2, 52), 0.06)
add(ws('Ten') - 0.05, metal(160, 1.8), 0.05); hit(ws('both'), 0.11, 60)
add(ws('but', 11), fio(engine(2.4, 95, 0.3, 900), 0.3, 0.6), 0.06); pen(ws('artificial', 11) - 0.1, 0.4, 0.05)
for k in range(4): add(ws('Earlier', 13) + 0.4 + k * 0.4, tick(), 0.04)
add(ws('shot', 13) - 0.05, mg_burst(6), 0.06); hit(ws('shot', 13), 0.12, 60)
add(ws('As', 16.8), fio(jet(2.4), 0.2, 0.8), 0.05); add(ws('As', 16.8) + 0.3, wind(3.6), 0.05); hit(ws('torn', 20), 0.10, 70)
hit(ws('Adolf', 21), 0.09, 75); add(ws('Adolf', 21), swell(2.0, 49), 0.05)
add(ws('invited', 23.4) - 0.05, ping(900, 1.2), 0.03); add(ws('sit', 25), ping(1100, 1.2), 0.03)
hit(ws('leg', 27.5), 0.07, 90); pen(ws('repaired', 29) - 0.05, 0.4, 0.05); hit(ws('escape', 30.5), 0.10, 70)
add(ws('He', 31.6), fio(wind(4.4), 0.5, 0.8), 0.05); add(ws('climbed', 31.5), rustle(2.2), 0.05); stamp_(ws('caught', 34) - 0.03)
for i, w_ in enumerate(('send', 'spare', 'will', 'shot')):
    for k in range(9): add(ws(w_, 37) - 0.1 + k * 0.06, clack(), 0.05)
add(ws('favor', 41.5) - 0.1, scratch(0.4), 0.06); hit(ws('enemy', 42.5), 0.08, 80)
add(ws('One', 43.6), fio(engine(2.6, 75, 0.35, 750), 0.3, 0.6), 0.08); add(ws('dropped', 44) - 0.05, whoosh(0.8, 300, 1600), 0.05)
add(ws('Inside', 46), impact(2.2), 0.10); add(ws('new', 46.5), swell(2.0, 55), 0.06)
for k in range(5): add(ws('escape', 49.5) - 0.1 + k * 0.4, scratch(0.15), 0.06)
hit(ws('threatened', 51.5), 0.09, 70); add(ws('night', 53) - 0.3, wind(2.0), 0.04)
add(ws('In', 54.2), door(), 0.08); hit(ws('Colditz'), 0.10, 60)
add(ws('And', 56.6), swell(4.0, 49), 0.07); hit(ws('friend', 59.5), 0.09, 65)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.6)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
