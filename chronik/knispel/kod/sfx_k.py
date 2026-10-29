# sound effects for the Knispel short: transitions, engines and tracks under the tank films, counter ticks, pen, dig, the hit
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import kshort as V
T = V.T; ws = V.ws
sfxlib.out = np.zeros((int(SR * T), 2))
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def hit(t0, g=0.10, f=85): add(t0, thud(0.9, f), g)
def pen(t0, dur, g=0.05):
    for i in range(int(dur / 0.16)): add(t0 + i * 0.16, scratch(0.18), g * rng.uniform(0.6, 1.0), rng.uniform(-0.2, 0.2))
for s, fn, tr in V.ANCH[1:]:
    if tr and tr[0] == 'whip': add(s - 0.2, whoosh(0.6, 300, 2400), 0.11, 0.5 * tr[1])
    else: add(s - 0.08, whoosh(0.5, 200, 1400), 0.045, rng.uniform(-0.3, 0.3))
add(0.02, impact(), 0.13); add(0.0, fio(wind(3.0), 0.5, 1.0), 0.03); hit(ws('siebzig'), 0.07, 85); hit(ws('namenlosen'), 0.09, 65)
add(ws('Metallmarke'), ping(1200, 1.2), 0.04); hit(ws('Kurt', 7.5), 0.08, 75); add(ws('Knispel', 8), swell(2.0, 52), 0.07); hit(ws('Knispel', 8), 0.10, 60)
for w_, a_ in (('Ladeschütze', 10.5), ('Richtschütze', 11.5), ('Kommandant', 13)): add(ws(w_, a_), metal(240, 0.9), 0.05); hit(ws(w_, a_), 0.06, 95)
add(ws('Tigers') - 0.1, fio(engine(3.2, 62, 0.5, 650), 0.3, 0.6), 0.09); hit(ws('Ostfront'), 0.07, 85)
add(ws('1943') - 0.05, fio(engine(2.6, 55, 0.5, 500), 0.4, 0.8), 0.05); add(ws('Kursk', 20), boom_far(2.4), 0.07)
for i in range(18): add(ws('168') + i * 0.06, tick(), 0.05)
hit(ws('168') + 1.1, 0.09, 70); add(ws('126'), scratch(0.4), 0.05); add(ws('42', 29), scratch(0.3), 0.05)
add(ws('nicht', 33), scratch(0.35), 0.09); hit(ws('nicht', 33), 0.10, 60)
pen(ws('ausgeschmückt'), 0.6, 0.06); hit(ws('1944'), 0.07, 85); hit(ws('Deutsche', 44), 0.06, 95)
pen(ws('Ritterkreuz'), 0.6, 0.06); add(ws('nie', 47.5), scratch(0.35), 0.09); hit(ws('Feldwebels'), 0.08, 75)
pen(ws('unbequem'), 0.6, 0.06); hit(ws('Haare'), 0.06, 95)
add(ws('Ende', 59) - 0.1, fio(engine(6.8, 58, 0.55, 600), 0.6, 1.0), 0.08); add(ws('getroffen') - 0.05, bomb(3.0), 0.12); add(ws('getroffen'), crack(), 0.07)
add(ws('Nach', 66), fio(static(3.6, 0.4), 0.4, 0.8), 0.02); hit(ws('Kopf'), 0.08, 70)
add(ws('Urbau'), ping(700, 1.4), 0.04); add(ws('Spur') + 0.2, swell(2.4, 46), 0.05)
hit(ws('2013'), 0.08, 80); add(ws('Erst', 76), fio(rustle(2.2), 0.3, 0.6), 0.05); hit(ws('sechzehn'), 0.09, 70)
add(ws('Bei', 81), metal(900, 1.2), 0.04); add(ws('Erkennungsmarke'), ping(1400, 1.6), 0.05)
hit(ws('2014'), 0.07, 85); add(ws('Brünn'), swell(3.0, 49), 0.06); add(ws('Soldatenfriedhof'), ping(880, 1.0), 0.03)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.3)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
