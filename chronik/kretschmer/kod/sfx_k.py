# sound effects for the Otto Kretschmer short: transitions, the night barrage, engines under the vehicle films, typing, stamps, pen, map pings
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
def stamp_(t0, g=0.20): add(t0, stampthump(), g)
def pen(t0, dur, g=0.05):
    for i in range(int(dur / 0.16)): add(t0 + i * 0.16, scratch(0.18), g * rng.uniform(0.6, 1.0), rng.uniform(-0.2, 0.2))
def typing(t0, n, step=0.025, g=0.03):
    for i in range(n): add(t0 + i * step, clack(), g * rng.uniform(0.7, 1.0), rng.uniform(-0.2, 0.2))
def paper(t0, g=0.09): add(t0 - 0.05, flip(), g, rng.uniform(-0.3, 0.3)); add(t0 + 0.22, thud(0.5, 140), 0.05)
for s, fn, tr in V.ANCH[1:]:
    if tr and tr[0] == 'whip': add(s - 0.2, whoosh(0.6, 300, 2400), 0.05, 0.5 * tr[1])   # transitions at half the earlier level
    elif tr and tr[0] == 'fade': add(s - 0.08, whoosh(0.5, 200, 1400), 0.022, rng.uniform(-0.3, 0.3))
add(0.02, impact(), 0.12)
hit(0.05, 0.08, 80); hit(ws('ein', 0.6), 0.10, 60)
hit(ws('Otto'), 0.07, 80); add(ws('Kretschmer'), swell(2.0, 50), 0.06); hit(ws('Kretschmer'), 0.10, 60)
add(ws('versenkten') - 0.2, fio(waves(4.8), 0.4, 0.8), 0.05); hit(ws('erfolgreichsten'), 0.07, 80)
hit(ws('März', 10), 0.07, 80); add(ws('vorbei') + 0.2, metal(700, 0.4), 0.05); hit(ws('vorbei') + 0.45, 0.09, 65)
add(ws('99', 13.3), fio(waves(1.8), 0.2, 0.5), 0.05); hit(ws('99', 13.3), 0.07, 80)
add(ws('Geleitzüge') - 0.1, fio(engine(5.6, 55, 0.4, 500), 0.5, 0.8), 0.05); hit(ws('nachts'), 0.06, 85); add(ws('aufgetaucht'), ping(900, 1.4), 0.04)
add(ws('Statt'), sonar_ping(820, 2.0), 0.04); add(ws('einziger') - 0.4, boom_far(2.2), 0.10); hit(ws('Schuss'), 0.08, 60)
hit(ws('Feindfahrt'), 0.06, 85); add(ws('Funksprüche'), static(1.0, 0.6), 0.02); hit(ws('Otto', 31), 0.09, 60)
for k in range(4): add(ws('In', 32) + 0.3 + k * 1.4, boom_far(2.0), 0.08 - 0.01 * k, rng.uniform(-0.4, 0.4))
for i in range(7): add(ws('sieben', 35.5) + i * 0.12, tick(), 0.04)
add(ws('Gut', 38.5), boom_far(2.6), 0.07); add(ws('Laurentic') - 0.05, scratch(0.4), 0.05); add(ws('Patroclus') - 0.05, scratch(0.4), 0.05)
for i in range(6): add(ws('47', 45.5) + i * 0.13, tick(), 0.035)
for i in range(8): add(ws('274.000') + i * 0.13, tick(), 0.03)
add(ws('Hunderte'), swell(3.0, 44), 0.06)
hit(ws('März', 55), 0.07, 80); add(ws('HX'), fio(wind(2.0), 0.4, 0.8), 0.04)
hit(ws('Joachim'), 0.08, 70); hit(ws('U', 64.2), 0.07, 80)
for i in range(5): add(ws('Wasserbomben') + i * 0.45 + 1.0, boom_far(1.6), 0.09)
add(ws('U', 68.4), fio(waves(2.2), 0.2, 0.6), 0.06); hit(ws('Oberfläche') - 0.3, 0.07, 75)
add(ws('ließ'), fio(waves(2.2), 0.2, 0.6), 0.05); hit(ws('ließ'), 0.07, 70)
hit(ws('Drei', 72.8), 0.08, 60); hit(ws('40', 73.5), 0.07, 80); hit(ws('kamen', 75.3), 0.07, 75)
hit(ws('Donald'), 0.07, 80); add(ws('Fernglas'), ping(760, 1.2), 0.04); pen(ws('als', 80.9), 0.55, 0.05)
add(ws('Kanada'), ping(700, 1.0), 0.03); add(ws('Tunnel'), scratch(0.6), 0.05); add(ws('Küste'), whoosh(1.4, 150, 900), 0.06); add(ws('U-Boot', 92.5), sonar_ping(820, 2.0), 0.04)
paper(ws('Doch', 94)); pen(ws('verschlüsselten'), 0.5, 0.05)
add(ws('warteten'), fio(engine(3.0, 70, 0.4, 600), 0.4, 0.8), 0.05); hit(ws('scheiterte'), 0.09, 60); add(ws('entkam'), whoosh(1.2, 150, 900), 0.05)
for i in range(6): add(ws('Kretschmer', 102) + 0.1 + i * 0.27, tick(), 0.035)
hit(ws('Bundesmarine'), 0.06, 85); hit(ws('NATO'), 0.06, 85); hit(ws('Flottillenadmiral'), 0.08, 70)
hit(ws('1998'), 0.08, 70); add(ws('Donau'), fio(waves(2.0), 0.3, 0.8), 0.04); pen(ws('goldene'), 0.6, 0.05)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.3)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
