# sound for the logo outro: arrival hits, a sweep while it opens, a deep impact when it settles
import sys
sys.path.insert(0, sys.argv[1])
import numpy as np, sfxlib
from sfxlib import *
sfxlib.out = np.zeros((int(SR * 6.0), 2))
add(0.15, whoosh(0.45, 250, 1600), 0.10, -0.3)
add(0.30, thud(0.9, 85), 0.16)
add(0.55, tick(), 0.05)
add(1.35, whoosh(1.1, 200, 1400), 0.13, 0.2)
add(1.40, swell(2.6, 41), 0.10)
add(2.40, impact(), 0.30)
add(2.50, scratch(0.35), 0.05)
add(2.75, tone(110, 2.6), 0.06)
o = sfxlib.out; n = len(o); t = np.arange(n) / SR; o *= np.minimum(1, (6.0 - t) / 0.8)[:, None]
o /= max(1.0, np.abs(o).max() / 0.9); wavfile.write(sys.argv[2], SR, (o * 32767).astype(np.int16)); print('ok')
