# sound effects for the Balck short: newsreel shots, maps, stamps, written words, transitions
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import bshort as V
T = V.T; ws = V.ws
sfxlib.out = np.zeros((int(SR * T), 2))
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def hit(t0, g=0.10, f=85): add(t0, thud(0.9, f), g)
def stamp_(t0): add(t0, stampthump(), 0.20)
def pen(t0, dur, g=0.05):
    for i in range(int(dur / 0.16)): add(t0 + i * 0.16, scratch(0.18), g * rng.uniform(0.6, 1.0), rng.uniform(-0.2, 0.2))
def typing(t0, n, step=0.03, g=0.03):
    for i in range(n): add(t0 + i * step, clack(), g * rng.uniform(0.7, 1.0), rng.uniform(-0.2, 0.2))
for s, fn, tr in V.ANCH[1:]:
    if tr and tr[0] == 'whip': add(s - 0.2, whoosh(0.6, 300, 2400), 0.11, 0.5 * tr[1])
    else: add(s - 0.08, whoosh(0.5, 200, 1400), 0.045, rng.uniform(-0.3, 0.3))
add(0.02, impact(), 0.14); add(0.0, fio(engine(6.4, 70, 0.4, 700), 0.6, 1.0), 0.07); hit(0.25, 0.08, 80); add(ws('Rote'), whoosh(0.6, 200, 1200), 0.06)
add(ws('Es', 6), fio(static(5.0, 0.4), 0.4, 0.8), 0.02); stamp_(ws('verurteilt', 9) - 0.03)
hit(ws('Hermann'), 0.11, 65); add(ws('Hermann'), swell(2.2, 52), 0.07); hit(ws('1893'), 0.06, 100)
for i in range(7): add(ws('siebenmal') + i * 0.085, scratch(0.12), 0.07)
hit(ws('siebenmal') + 0.6, 0.08, 75)
hit(ws('Am', 17.5) + 0.2, 0.07, 90); add(ws('führte', 18) - 0.05, whoosh(1.6, 150, 900), 0.08); add(ws('Durchbruch', 18) - 0.1, whoosh(1.2, 150, 900), 0.08)
hit(ws('Im', 25.5) + 0.2, 0.07, 90); add(ws('Tschir', 26) - 0.1, whoosh(0.6, 300, 1500), 0.05); add(ws('Stalingrad', 26), ping(700, 1.4), 0.04)
add(ws('Eine', 32.5), boom_far(), 0.08); add(ws('Eine', 32.5) + 0.3, fio(engine(2.4, 60, 0.5, 600), 0.3, 0.6), 0.07)
add(ws('nachts', 35), fio(wind(2.4)), 0.04); add(ws('und', 37.5), fio(engine(1.6, 75, 0.4, 800), 0.2, 0.4), 0.08)
hit(ws('25', 39), 0.08, 80); pen(ws('25', 39), 0.4, 0.06); add(ws('Angreifern', 39) - 0.1, whoosh(1.0, 200, 1400), 0.08)
hit(ws('Heeresgruppe', 44), 0.08, 75); hit(ws('Herbst', 47.5), 0.06, 95); add(ws('Lothringen', 49), whoosh(0.6, 200, 1200), 0.05); hit(ws('Patton', 51), 0.08, 75)
for k in range(3): add(ws('Im', 53) + 0.1 + k * 0.9, boom_far(2.0), 0.09)
stamp_(ws('ohne', 55) - 0.03); add(ws('erschießen', 55), crack(), 0.10); stamp_(ws('erschießen', 55) - 0.03)
stamp_(ws('abgelöst', 60) - 0.03); hit(ws('Ungarn', 60), 0.06, 95); hit(ws('Kriegsende', 63), 0.07, 85); hit(ws('Gefangenschaft', 63), 0.07, 80)
hit(ws('1948', 66), 0.07, 85); stamp_(ws('drei', 70) - 0.03); hit(ws('18', 72), 0.06, 95); stamp_(ws('Interviews', 76) - 0.03)
typing(ws('Erst', 79) + 0.3, 40, 0.02); typing(ws('Mellenthin', 79) - 0.6, 60, 0.02); typing(ws('amerikanischen', 82), 40, 0.02); stamp_(ws('Sowjets', 84) - 0.05)
hit(ws('überzeugten', 90), 0.08, 75); hit(ws('Nationalsozialisten', 90), 0.10, 60)
add(ws('Hermann', 94.5), swell(2.5, 46), 0.06); hit(ws('1982', 94), 0.09, 65)
hit(ws('Lehrer', 97), 0.08, 80); add(ws('Täter', 99) - 0.05, scratch(0.35), 0.09); hit(ws('Täter', 99), 0.12, 55)
add(ws('Kanntet', 102.5), swell(3.0, 49), 0.06)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.6)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
