# sound for the style test: soft whooshes on the cuts, small pops when shapes land, a typewriter for the typed lines
import sys; sys.path.insert(0, sys.argv[1] + '/code'); sys.path.insert(0, sys.argv[1] + '/../lac/code')
import numpy as np, sfxlib
from sfxlib import *
import styleA as V
T = V.TEND; ws = V.ws
sfxlib.out = np.zeros((int(SR * T) + SR, 2))
def pop(t0, g=0.05): add(t0, thud(0.4, 160), g)
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
for a, _ in V.SC[1:]: add(a - 0.15, whoosh(0.5, 200, 1600), 0.03, 0.3)
def deal(t0, g=0.035): add(t0, flip(), g, 0.3); add(t0 + 0.3, thud(0.4, 140), g * 0.8)
for t0 in (0.0, 0.15, 0.3, 0.45): deal(t0 + 0.1)
for a, _ in V.SC[1:]: deal(a + 0.05)
deal(ws('britische', 20.7))
hit = lambda t0, g=0.06, f=80: add(t0, thud(0.8, f), g)
hit(ws('Hunderte')); hit(ws('bombardiert'), 0.07, 60); hit(ws('September') - 0.1); hit(ws('torpedierte'), 0.07, 65); hit(ws('Laconia') - 0.15)
for i in range(6): add(ws('2.700') + i * 0.12, tick(), 0.025)
hit(ws('1.800'), 0.07, 65)
o = sfxlib.out[:int(SR * T)]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
