import sys
sys.path.insert(0, sys.argv[1])
import numpy as np, sfxlib
from sfxlib import *
def mk(T, events, out):
    sfxlib.out = np.zeros((int(SR * T), 2))
    for fn in events: fn()
    o = sfxlib.out; o /= max(1.0, np.abs(o).max() / 0.9); wavfile.write(out, SR, (o * 32767).astype(np.int16))
mk(12.0, [lambda: add(0.0, whoosh(0.5, 250, 1400), 0.07), lambda: add(0.15, thud(0.8, 95), 0.10),
          lambda: add(1.5, whoosh(0.5, 250, 1400), 0.07), lambda: add(1.65, thud(0.8, 90), 0.10),
          lambda: add(3.1, whoosh(0.5, 250, 1400), 0.07), lambda: add(3.25, thud(0.8, 85), 0.10),
          lambda: add(4.9, swell(2.0, 41), 0.08), lambda: add(5.6, impact(), 0.22), lambda: add(6.6, thud(0.6, 140), 0.08), lambda: add(6.6, tick(), 0.06)], 'social/story_sfx.wav')
mk(4.0, [lambda: add(0.0, impact(), 0.18), lambda: add(0.6, thud(0.6, 140), 0.07)], 'social/end_sfx.wav')
print('ok')
