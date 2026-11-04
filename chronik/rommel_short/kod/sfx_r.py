# sound effects for the Rommel short: transitions, engines under the desert films, map arrow, typewriter, stamps, pen, the funeral bell
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import rshort as V
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
add(0.02, impact(), 0.13); add(0.0, fio(engine(5.8, 70, 0.4, 700), 0.6, 1.0), 0.06); add(0.0, fio(wind(6.0), 0.6, 1.0), 0.03)
hit(ws('Wüstenfuchs'), 0.08, 75); hit(ws('Regime'), 0.10, 60)
hit(ws('Erwin'), 0.08, 75); add(ws('Rommel', 6.8), swell(2.0, 52), 0.07); hit(ws('Rommel', 6.8), 0.10, 60)
add(ws('12.'), fio(waves(3.0), 0.4, 0.8), 0.05); hit(ws('Tripolis'), 0.07, 85); add(ws('landete'), metal(260, 1.0), 0.04)
add(ws('griff') - 0.05, whoosh(1.4, 150, 900), 0.08); add(ws('griff'), fio(engine(3.0, 60, 0.5, 650), 0.3, 0.6), 0.06); add(ws('Grenze'), ping(760, 1.3), 0.04)
add(ws('vorne') - 0.4, fio(engine(3.2, 140, 0.25, 1500), 0.4, 0.8), 0.06)
add(ws('Tobruk', 22.3), boom_far(2.4), 0.08); hit(ws('fast', 23.6), 0.06, 95)
typing(ws('Kommandeuren'), 20); typing(ws('nicht', 31.7), 34); typing(ws('sondern', 33.3), 28)
add(ws('Juni'), fio(engine(2.4, 70, 0.4, 700), 0.3, 0.6), 0.05); hit(ws('fiel', 36.9), 0.09, 70); hit(ws('Generalfeldmarschall'), 0.10, 60); add(ws('Generalfeldmarschall'), swell(2.0, 50), 0.05)
add(ws('El', 42.9), boom_far(2.6), 0.08); stamp_(ws('scheiterte'))
hit(ws('Sieg'), 0.11, 55); add(ws('zog'), whoosh(1.0, 150, 900), 0.07); add(ws('zog'), fio(engine(2.0, 75, 0.4, 700), 0.3, 0.5), 0.05)
hit(ws('Atlantikwall'), 0.07, 85); hit(ws('Millionen'), 0.07, 80)
paper(ws('und', 52.2)); paper(ws('Rommelspargel') - 0.1); pen(ws('Rommelspargel'), 0.7, 0.06)
hit(ws('verloren'), 0.10, 60); hit(ws('Attentat'), 0.09, 70); stamp_(ws('Verhören'))
hit(ws('14.'), 0.07, 85); add(ws('hielten'), door(), 0.06); hit(ws('Herrlingen'), 0.07, 80)
hit(ws('Volksgerichtshof'), 0.08, 75); hit(ws('Gift'), 0.12, 50); add(ws('Gift'), swell(2.6, 46), 0.07)
add(ws('Wagen'), door(), 0.05); add(ws('tot'), swell(3.0, 44), 0.06); stamp_(ws('Verwundungen'), 0.18)
for k in range(3): add(ws('Kranz') + k * 1.3, ping(330, 2.5), 0.05)
pen(ws('Sein', 87), 1.0, 0.05); hit(ws('Wahrheit'), 0.08, 75); add(ws('Manfred'), swell(2.4, 49), 0.05)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.3)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
