# sound effects for the Bader short: engines, the falling crate, the gun camera, typed message, stamps, transitions
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import ddshort as V
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
# bombers over France
add(0.0, fio(engine(7.2, 70, 0.35, 700), 0.4, 1.0), 0.09); add(ws('Holzkiste') + 0.2, wind(3.0), 0.03)
hit(ws('August'), 0.08, 85)
hit(ws('Douglas'), 0.09, 75); add(ws('Douglas'), swell(2.2, 52), 0.06)
add(ws('Zehn') - 0.05, metal(160, 1.8), 0.05); hit(ws('beide'), 0.11, 60)
add(ws('doch', 14.8), fio(engine(2.2, 95, 0.3, 900), 0.3, 0.6), 0.06); pen(ws('Prothesen', 15) - 0.1, 0.5, 0.05)
for k in range(4): add(ws('Anfang', 16.9) + 0.4 + k * 0.4, tick(), 0.04)
add(ws('abgeschossen', 17) - 0.05, mg_burst(6), 0.06); hit(ws('abgeschossen', 17), 0.12, 60)
add(ws('Als', 20.6), fio(jet(2.4), 0.2, 0.8), 0.05); add(ws('Als', 20.6) + 0.3, wind(4.4), 0.05); hit(ws('riss', 24), 0.10, 70)
hit(ws('Adolf', 25), 0.09, 75); add(ws('Adolf', 25), swell(2.0, 49), 0.05)
add(ws('lud', 27.5) - 0.05, ping(900, 1.2), 0.03); add(ws('ließ', 29.5), ping(1100, 1.2), 0.03)
hit(ws('Bein', 33.5), 0.07, 90); pen(ws('reparierten', 34.5) - 0.05, 0.4, 0.05); hit(ws('Flucht', 37), 0.10, 70)
add(ws('Er', 38.4) - 0.1, fio(wind(5.6), 0.5, 0.8), 0.05); add(ws('kletterte', 38.4), rustle(2.6), 0.05); stamp_(ws('gefasst', 43) - 0.03)
for w_ in ('Schickt', 'Ersatzbein', 'wird', 'beschossen'):
    for k in range(9): add(ws(w_, 46) - 0.1 + k * 0.06, clack(), 0.05)
add(ws('Gefallen', 52) - 0.1, scratch(0.4), 0.06); hit(ws('Feind', 51), 0.08, 80)
add(ws('Einer', 53.3), fio(engine(3.6, 75, 0.35, 750), 0.3, 0.6), 0.08)
add(ws('Darin', 56.8), impact(2.2), 0.10); add(ws('neues', 57), swell(2.0, 55), 0.06)
for k in range(4): add(ws('versuchte', 60) - 0.1 + k * 0.35, scratch(0.15), 0.06)
add(ws('drohten', 63.5) - 0.1, scratch(0.3), 0.07); hit(ws('drohten', 63.5), 0.09, 70); add(ws('nachts', 64) - 0.3, wind(2.0), 0.04)
add(ws('Am', 66.1), door(), 0.08); hit(ws('Colditz', 66), 0.10, 60)
hit(ws('befreiten', 69.5), 0.10, 70); add(ws('befreiten', 69.5), swell(3.0, 55), 0.06)
add(ws('Thelma') - 0.2, swell(2.2, 52), 0.04)
add(ws('im', 75.6), fio(engine(3.4, 80, 0.3, 800), 0.3, 0.6), 0.08); hit(ws('London', 77.5), 0.08, 80)
add(ws('Und', 78.8), swell(5.0, 49), 0.07); hit(ws('Feind', 80), 0.09, 65); hit(ws('Freund', 84.5), 0.09, 65)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.6)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
