# sound for the style test: soft whooshes on the cuts, small pops when shapes land, a typewriter for the typed lines
import sys; sys.path.insert(0, sys.argv[1] + '/code'); sys.path.insert(0, sys.argv[1] + '/../lac/code')
import numpy as np, sfxlib
from sfxlib import *
import test30 as V
T = V.TEND; ws = V.ws
sfxlib.out = np.zeros((int(SR * T) + SR, 2))
def pop(t0, g=0.05): add(t0, thud(0.4, 160), g)
for a, _ in V.SC[1:]: add(a - 0.12, whoosh(0.4, 300, 2200), 0.035, 0.4)
add(0.05, whoosh(0.6, 200, 1600), 0.04); pop(ws('ein', 0.5), 0.06)
pop(V.SC[1][0] + 0.05); pop(ws('Hunderte'), 0.07)
add(V.SC[2][0], whoosh(0.8, 150, 1200), 0.05); pop(ws('bombardiert'), 0.08)
for i in range(14): add(ws('September') + i * 0.05, clack(), 0.025)
pop(ws('U', 7.5), 0.06)
for i in range(21): add(ws('12.') + i * 0.04, clack(), 0.02)
pop(ws('torpedierte'), 0.07); pop(ws('Werner'), 0.05)
pop(V.SC[5][0] + 0.05); pop(ws('Laconia'), 0.07)
for i in range(7): add(ws('2.700') + i * 0.13, tick(), 0.03)
pop(ws('Menschen', 19.5), 0.06); pop(ws('1.800'), 0.08)
o = sfxlib.out[:int(SR * T)]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
