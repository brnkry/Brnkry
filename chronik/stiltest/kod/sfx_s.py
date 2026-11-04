# sound for the style test: soft whooshes on the cuts, small pops when shapes land, a typewriter for the typed lines
import sys; sys.path.insert(0, sys.argv[1] + '/code'); sys.path.insert(0, sys.argv[1] + '/../lac/code')
import numpy as np, sfxlib
from sfxlib import *
import test2 as V
T = V.TEND; ws = V.ws
sfxlib.out = np.zeros((int(SR * T) + SR, 2))
def pop(t0, g=0.05): add(t0, thud(0.4, 160), g)
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
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
add(V.SC[8][0] + 0.1, fio(waves(2.4), 0.3, 0.8), 0.05); pop(ws('U', 28.9), 0.07)
pen = lambda t0, d_: [add(t0 + i * 0.16, scratch(0.18), 0.04) for i in range(int(d_ / 0.16))]
pen(ws('hörte'), 0.5); pop(ws('Hilferufe'), 0.07); pop(ws('Italienisch'), 0.06)
add(V.SC[10][0], flip(), 0.07); pen(ws('begriff'), 0.4); pop(ws('Verbündeten'), 0.07); pen(ws('getroffen'), 0.5); pop(ws('begann'), 0.06)
add(V.SC[11][0] + 0.3, thud(0.5, 120), 0.07); pen(ws('Schiffbrüchige', 40.5), 0.5); pen(ws('Deck'), 0.45); pop(ws('voller'), 0.06)
add(V.SC[12][0], fio(waves(2.0), 0.3, 0.6), 0.04); pop(ws('Rettungsboote', 44), 0.06); pen(ws('Schlepptau'), 0.5)
add(V.SC[13][0], static(0.8, 0.5), 0.02); pop(ws('offen'), 0.06)
for w_ in (('Er', 47.7), ('Schiff', 48.4), ('angreifen', 0), ('solange', 0), ('angegriffen', 0)):
    for i in range(22): add(ws(*w_) + i * 0.022, clack(), 0.022)
pop(ws('Dönitz', 53), 0.07); add(ws('weitere'), whoosh(0.5, 300, 2000), 0.035); add(ws('weitere') + 0.25, whoosh(0.5, 300, 2000), 0.035); add(ws('italienisches'), whoosh(0.5, 300, 2000), 0.035); pen(ws('Hilfe'), 0.4)
o = sfxlib.out[:int(SR * T)]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
