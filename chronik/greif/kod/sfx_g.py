# sound effects for the Unternehmen Greif short: transitions, the night barrage, engines under the vehicle films, typing, stamps, pen, map pings
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import gshort as V
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
    if tr and tr[0] == 'whip': add(s - 0.2, whoosh(0.6, 300, 2400), 0.11, 0.5 * tr[1])
    else: add(s - 0.08, whoosh(0.5, 200, 1400), 0.045, rng.uniform(-0.3, 0.3))
add(0.02, impact(), 0.12); add(0.0, fio(wind(5.8), 0.5, 1.0), 0.03)
hit(ws('Dezember'), 0.07, 80); pen(ws('beweisen'), 0.75, 0.05)
hit(ws('hinter', 6), 0.06, 85); add(ws('deutsche'), scratch(0.5), 0.05); hit(ws('Uniformen'), 0.08, 70)
paper(ws('Der', 10)); stamp_(ws('Unternehmen'))
hit(ws('Otto'), 0.07, 80); add(ws('Skorzeny'), swell(2.2, 50), 0.06); hit(ws('Skorzeny'), 0.10, 60); hit(ws('SS-Offizier'), 0.07, 75)
hit(ws('Mussolini'), 0.07, 80); hit(ws('befreit'), 0.07, 75)
add(ws('Ardennenoffensive'), scratch(0.7), 0.06); hit(ws('Truppe'), 0.07, 80)
pen(ws('aussah'), 0.5, 0.05); pen(ws('sprach'), 0.5, 0.05)
paper(ws('Doch', 26.3)); typing(ws('Freiwillige'), 11); typing(ws('gutem'), 18); stamp_(ws('wenige'))
add(ws('und', 29.9) - 0.2, fio(engine(3.0, 75, 0.35, 650), 0.4, 0.6), 0.05); add(ws('Hunderter'), scratch(0.5), 0.05); add(ws('bekam') - 0.25, scratch(0.3), 0.06)
paper(ws('Skorzeny', 32.9) - 0.3); typing(ws('Jeeps', 34), 12); typing(ws('Lastwagen'), 9)
add(ws('und', 35.6) - 0.2, fio(engine(2.2, 62, 0.45, 600), 0.2, 0.5), 0.08); hit(ws('Sherman'), 0.10, 60)
add(ws('Blech'), metal(240, 1.0), 0.04); add(ws('Farbe'), scratch(0.4), 0.05); hit(ws('getarnt'), 0.08, 70)
for k, dt in enumerate((0.0, 0.5, 0.9, 1.5, 2.0)): add(ws('Am', 40.3) - 0.1 + dt, boom_far(2.2), 0.10 - 0.012 * k, rng.uniform(-0.4, 0.4))
add(ws('Kleine') - 0.2, fio(engine(2.4, 95, 0.3, 900), 0.3, 0.5), 0.05); hit(ws('erbeuteten'), 0.06, 85)
add(ws('um', 46) - 0.15, whoosh(0.5, 400, 1800), 0.06); add(ws('um', 46), metal(380, 0.6), 0.03)
stamp_(ws('kappten') + 0.1, 0.16); add(ws('kappten') + 0.1, metal(900, 0.3), 0.03)
add(ws('schickten'), whoosh(0.6, 200, 1200), 0.05); add(ws('falsche'), scratch(0.5), 0.05)
for i in range(4): add(ws('wenige', 50.6) + i * 0.12, tick(), 0.04)
for i in range(3): add(ws('durch') + i * 0.08, ping(520, 0.8), 0.03)
for k in range(4): add(ws('Gerücht') + k * 0.9, ping(880, 1.4), 0.035)
hit(ws('Kreuzung'), 0.06, 85); stamp_(ws('Fangfragen'))
paper(ws('Wer', 59) - 0.15); pen(ws('Wer', 59), 0.7, 0.05); pen(ws('Wie', 60.5), 0.6, 0.05); pen(ws('Micky'), 0.45, 0.05)
hit(ws('Omar'), 0.08, 75); pen(ws('Hauptstadt'), 0.7, 0.05)
add(ws('unterwegs'), whoosh(1.0, 150, 900), 0.06); add(ws('Eisenhower'), ping(700, 1.4), 0.04); pen(ws('töten') - 0.1, 0.6, 0.05)
stamp_(ws('Belegt')); hit(ws('Weihnachten', 75), 0.07, 80); hit(ws('strenger'), 0.08, 70)
hit(ws('Drei'), 0.07, 80); add(ws('Drei') - 0.1, fio(engine(2.8, 90, 0.3, 850), 0.3, 0.6), 0.04); hit(ws('Aywaille'), 0.08, 70)
stamp_(ws('Passwort'))
paper(ws('ein', 82.3)); typing(ws('Militärgericht'), 14); typing(ws('verurteilte'), 16); typing(ws('Spione'), 20)
add(ws('Weihnachten', 85), scratch(0.6), 0.05); hit(ws('erschossen'), 0.12, 50); add(ws('erschossen'), swell(2.2, 46), 0.06)
add(ws('1947'), scratch(0.5), 0.05); add(ws('Dachau'), scratch(0.5), 0.05); hit(ws('Gericht', 91), 0.07, 75)
stamp_(ws('freigesprochen'), 0.2)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.3)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
