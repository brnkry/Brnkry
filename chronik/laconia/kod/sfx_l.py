# sound effects for the Laconia short: transitions, the night barrage, engines under the vehicle films, typing, stamps, pen, map pings
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import lshort as V
T = V.T; ws = V.ws
sfxlib.out = np.zeros((int(SR * T), 2))
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def hit(t0, g=0.10, f=85): add(t0, thud(0.9, f), g)
def stamp_(t0, g=0.20): add(t0, stampthump(), g)
def pen(t0, dur, g=0.05):
    for i in range(int(dur / 0.16)): add(t0 + i * 0.16, scratch(0.18), g * rng.uniform(0.6, 1.0), rng.uniform(-0.2, 0.2))
def typing(t0, n, step=0.025, g=0.03):
    for i in range(n): add(t0 + i * step, clack(), g * rng.uniform(0.7, 1.0), rng.uniform(-0.2, 0.2))
def paper(t0, g=0.09): add(t0 - 0.05, flip(), g, rng.uniform(-0.3, 0.3)); add(t0 + 0.22, thud(0.5, 140), 0.05)
for s, fn, tr in V.ANCH[1:]:
    if tr and tr[0] == 'whip': add(s - 0.2, whoosh(0.6, 300, 2400), 0.05, 0.5 * tr[1])   # transitions at half the earlier level
    elif tr and tr[0] == 'fade': add(s - 0.08, whoosh(0.5, 200, 1400), 0.022, rng.uniform(-0.3, 0.3))
add(0.02, impact(), 0.11)
pen(ws('Er') + 0.05, 1.2, 0.045); pen(ws('rettete'), 0.6, 0.045); hit(ws('Hunderte'), 0.07, 80); pen(ws('Schiffbrüchige', 2.5), 0.5, 0.04); pen(ws('und', 3.3), 0.5, 0.04)
hit(ws('bombardiert'), 0.10, 60); add(ws('bombardiert'), boom_far(2.2), 0.06)
add(ws('Im') - 0.1, fio(waves(5.6), 0.5, 0.8), 0.04); add(ws('U', 7.5), sonar_ping(820, 2.0), 0.04)
add(ws('Am', 10.9), fio(engine(4.2, 60, 0.4, 600), 0.4, 0.8), 0.04); add(ws('torpedierte') + 0.4, boom_far(2.6), 0.10); pen(ws('Werner'), 0.6, 0.045)
add(ws('das', 15.2), fio(waves(2.6), 0.3, 0.6), 0.04); add(ws('Laconia') - 0.05, scratch(0.5), 0.05)
for i in range(6): add(ws('2.700') + i * 0.14, tick(), 0.035)
pen(ws('Soldaten', 21), 0.5, 0.04); pen(ws('Zivilisten'), 0.6, 0.04); pen(ws('polnische'), 0.5, 0.04)
for i in range(6): add(ws('1.800') + i * 0.14, tick(), 0.035)
add(ws('Als') - 0.1, fio(waves(2.8), 0.2, 0.6), 0.06)
add(ws('hörte') - 0.1, fio(waves(3.4), 0.3, 0.6), 0.05); pen(ws('Hilferufe'), 0.6, 0.05)
pen(ws('Hartenstein', 34.5), 0.45, 0.04); pen(ws('Verbündeten'), 0.45, 0.045); hit(ws('Rettung'), 0.08, 75)
add(ws('Er', 40.2), fio(waves(5.5), 0.4, 0.8), 0.04); pen(ws('voller') - 0.1, 0.5, 0.045); pen(ws('Schlepptau') - 0.2, 0.5, 0.045)
add(ws('Dann'), static(1.0, 0.5), 0.02)
for w_ in (('Er', 47.7), ('Schiff', 48.4), ('angreifen', 0), ('solange', 0), ('angegriffen', 0)): typing(ws(*w_), 26, 0.02, 0.028)
hit(ws('Dönitz', 53), 0.07, 80); hit(ws('italienisches'), 0.06, 85)
hit(ws('16.'), 0.06, 85); add(ws('großen') - 0.3, fio(wind(2.6), 0.4, 0.8), 0.04); pen(ws('Rotkreuzflagge') + 0.1, 0.5, 0.045)
add(ws('französischen', 63.5), whoosh(1.4, 150, 900), 0.05)
add(ws('Da', 67) - 0.1, fio(jet(4.2), 0.6, 0.8), 0.05); hit(ws('B-24'), 0.08, 70)
add(ws('Ascension'), ping(700, 1.2), 0.04); typing(ws('Befehl', 74.8) + 0.2, 18, 0.05, 0.03)
add(ws('Eine', 76) + 0.4, whistle(1.2, 1400, 500), 0.05); add(ws('Dutzende') - 0.2, bomb(2.6), 0.11); pen(ws('Dutzende'), 0.6, 0.045)
add(ws('Hartenstein', 80.6), fio(waves(3.2), 0.3, 0.6), 0.05); add(ws('tauchte', 84), fio(waves(1.5), 0.1, 0.6), 0.06)
add(ws('Am', 84.9), fio(engine(2.8, 70, 0.4, 600), 0.4, 0.6), 0.04); pen(ws('Kriegsschiffe') - 0.2, 0.6, 0.04)
add(ws('Trotzdem'), swell(3.0, 44), 0.06)
for i in range(7): add(ws('1.600') + i * 0.14, tick(), 0.035)
pen(ws('italienische', 94.3), 0.7, 0.04)
hit(ws('Laconia-Befehl'), 0.09, 65); typing(ws('Laconia-Befehl') + 0.3, 18, 0.04, 0.028); add(ws('retten', 100.6) + 0.2, metal(700, 0.4), 0.05); hit(ws('retten', 100.6) + 0.45, 0.09, 65)
hit(ws('Nürnberg'), 0.07, 80); hit(ws('erwiesen'), 0.08, 70)
pen(ws('Hartenstein', 110.2), 0.55, 0.045)
add(ws('Im', 112.3), bomb(2.4), 0.09); pen(ws('Flugzeug'), 0.6, 0.04); add(ws('U', 116.4), fio(waves(1.8), 0.2, 0.6), 0.05)
pen(ws('östlich'), 0.6, 0.04); add(ws('gesamte') - 0.1, swell(2.4, 46), 0.05)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.3)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
