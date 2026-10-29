# sound effects for the Tiger 131 short: transitions, digit pings, hits, paper, typewriter, and the real engine sound of Tiger 131 (from the mud-and-rain film, no commentary) under its own scenes
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import tshort as V
T = V.T; ws = V.ws
sfxlib.out = np.zeros((int(SR * T), 2))
_, TANK = wavfile.read(sys.argv[1] + '/m_audio.wav'); TANK = TANK.astype(np.float32).mean(1) / 32768
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def tank(t0, a, dur, g): add(t0, fio(TANK[int(a * SR):int((a + dur) * SR)], 0.4, 0.6), g)
def hit(t0, g=0.10, f=85): add(t0, thud(0.9, f), g)
def typing(t0, n, step=0.03, g=0.03):
    for i in range(n): add(t0 + i * step, clack(), g * rng.uniform(0.7, 1.0), rng.uniform(-0.2, 0.2))
def paper(t0, g=0.09): add(t0 - 0.05, flip(), g, rng.uniform(-0.3, 0.3)); add(t0 + 0.22, thud(0.5, 140), 0.05)
for s, fn, tr in V.ANCH[1:]:
    if tr and tr[0] == 'whip': add(s - 0.2, whoosh(0.6, 300, 2400), 0.11, 0.5 * tr[1])
    else: add(s - 0.08, whoosh(0.5, 200, 1400), 0.045, rng.uniform(-0.3, 0.3))
add(0.02, impact(), 0.13); add(0.0, fio(engine(6.2, 60, 0.5, 600), 0.6, 1.0), 0.06); hit(ws('Tunesien'), 0.08, 75)
tank(ws('und', 6.2) - 0.1, 41.0, 2.8, 0.35); hit(ws('fährt', 7), 0.07, 80)
for w_, a_ in (('erste', 12.3), ('dritter', 13.5), ('erster', 14.3)): add(ws(w_, a_), ping(900, 1.0), 0.05); hit(ws(w_, a_), 0.05, 100)
add(ws('Medjez'), ping(700, 1.2), 0.04); add(ws('Churchill-Panzer'), fio(engine(1.6, 75, 0.4, 700), 0.2, 0.5), 0.05)
add(ws('Treffer'), crack(), 0.10); hit(ws('Drehkranz'), 0.11, 60); add(ws('zweiter', 25.4), crack(), 0.09); hit(ws('Höhenrichtung'), 0.10, 65)
add(ws('stieg'), metal(300, 1.0), 0.05); hit(ws('auf', 30.5), 0.09, 70)
paper(ws('nie', 34.9)); paper(ws('untersuchen'))
add(ws('Luken'), metal(220, 1.2), 0.05); add(ws('instand'), metal(260, 1.0), 0.04)
hit(ws('König'), 0.06, 95); add(ws('Oktober'), whoosh(1.8, 150, 900), 0.06); add(ws('England'), ping(760, 1.3), 0.04)
for w_, a_, n_ in (('Schule', 48, 24), ('vermaß', 50, 31), ('Panzerung', 51, 22), ('Motor', 52, 21), ('Kanone', 53, 21), ('Schwäche', 55, 23)): typing(ws(w_, a_), n_, 0.022)
hit(ws('1951'), 0.07, 85); hit(ws('zerlegt'), 0.08, 75); hit(ws('restauriert'), 0.07, 85)
tank(ws('Als', 66) - 0.1, 99.0, 5.6, 0.18); tank(ws('fährt', 71.5) - 0.1, 2.0, 4.2, 0.40)
hit(ws('Originalplänen'), 0.06, 95); hit(ws('Fury'), 0.10, 60); add(ws('Fury'), swell(2.0, 50), 0.06)
tank(ws('Heute', 85.3) - 0.1, 60.0, T - ws('Heute', 85.3), 0.22); add(ws('einzige'), swell(2.6, 46), 0.05)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.3)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
