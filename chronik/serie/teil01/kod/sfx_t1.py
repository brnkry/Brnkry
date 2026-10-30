# sound for Teil 1: page turns, a soft swish for each red strike line and each red hatching on the map, a light tick when a
# photo or a big number lands; no writing noise. Music and voice are mixed separately.
import sys, numpy as np
sys.path.insert(0, sys.argv[1] + '/code')
import sfxlib
from sfxlib import *
sys.argv = [sys.argv[0], 'x'] + sys.argv[1:]
import teil1 as V
T = V.T_END; sfxlib.out = np.zeros((int(SR * T), 2)); ws = V.ws
def page_turn(dur=0.85):
    n = int(SR * dur); t = np.arange(n) / SR; x = rng.normal(0, 1, n)
    x = bp(x, 1200, 7000) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5 * (0.6 + 0.4 * np.abs(np.sin(t * 38)))
    flap = np.zeros(n); k = int(SR * (dur - 0.12)); fl = thud(0.25, 110); flap[k:k + len(fl)] = fl[:n - k]
    return norm(x) * 0.8 + flap * 0.6
def swish(dur=0.28):
    n = int(SR * dur); t = np.arange(n) / SR; return norm(bp(rng.normal(0, 1, n), 2500, 8000)) * np.sin(np.pi * t / dur) ** 2
for a, d in V.TURNS: add(a, page_turn(d), 0.15, -0.2)
for p in V.PANS: add(p, swish(0.5), 0.025, 0.3)
for t0 in (ws('besitzen'), ws('verboten', 11), ws('wertlos'), ws('aus', 47.5), ws('Rheinland') - 0.6, ws('Österreich'), ws('Sudetenland'), ws('März')): add(t0, swish(), 0.05)
for t0 in (ws('Versailles') + 0.2, ws('Adolf') + 0.2, ws('Wehrpflicht') - 0.1, ws('eröffnete')): add(t0, tick(), 0.05)
for t0 in (ws('hunderttausend'), ws('1923'), ws('sechs'), ws('1935'), ws('Uhr', 82), ws('sechzig')): add(t0, thud(0.5, 90), 0.06)
o = sfxlib.out; o /= max(1.0, np.abs(o).max() / 0.9); wavfile.write(sys.argv[2] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
