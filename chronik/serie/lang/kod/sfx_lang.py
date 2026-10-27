# sound for the long Teil 1: page turns, a whoosh when the camera flies into a film and back out, stamps, strike lines and map
# hatching, low hits on big numbers, engines under the tank films, gunfire under the Schleswig-Holstein. Music and voice mixed apart.
import sys, numpy as np
sys.path.insert(0, sys.argv[1] + '/code')
import sfxlib
from sfxlib import *
OUTD = sys.argv[2]; sys.argv = [sys.argv[0], 'T']
import lang as V
P = V.P; T = V.T_END; sfxlib.out = np.zeros((int(SR * T) + SR, 2))
def page_turn(dur=0.95):
    n = int(SR * dur); t = np.arange(n) / SR; x = rng.normal(0, 1, n)
    x = bp(x, 1200, 7000) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5 * (0.6 + 0.4 * np.abs(np.sin(t * 38)))
    flap = np.zeros(n); k = int(SR * (dur - 0.12)); fl = thud(0.25, 110); flap[k:k + len(fl)] = fl[:n - k]
    return norm(x) * 0.8 + flap * 0.6
def swish(dur=0.3):
    n = int(SR * dur); t = np.arange(n) / SR; return norm(bp(rng.normal(0, 1, n), 2500, 8000)) * np.sin(np.pi * t / dur) ** 2
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
for B in (V.BOOK_A, V.BOOK_C, V.BOOK_E, V.BOOK_G):
    for a in B.turns: add(a, page_turn(), 0.16, -0.2)
segs = V.SEG
for i, (a, fn) in enumerate(segs):
    if i and V.isbook(segs[i - 1][1]) and not V.isbook(fn): add(a - 0.3, whoosh(1.0, 200, 1500), 0.05, 0.2)       # into a film
    if i and not V.isbook(segs[i - 1][1]) and V.isbook(fn): add(a - 0.7, whoosh(0.9, 250, 1700), 0.04, -0.2)    # back out to the page
for t0 in (P('erdolcht'), P('verboten', 54), P('nichts', 88), P('scheiterte'), P('gleichgeschaltet') + 0.4, P('Bruch'), P('inszeniert')): add(t0, stampthump(), 0.13)
for t0 in (P('Panzer', 4) + 0.15, P('zerschlagen'), P('verboten', 164), P('gleichgeschaltet'), V.T_RH, V.T_AT, V.T_SU, V.T_BM, V.T_DZ, V.T_PL, P('verlor')): add(t0, swish(), 0.05)
for t0 in (P('100.000'), P('132'), P('Dollar') + 1.3, P('sechs', 120), P('stärkste'), P('um', 311), P('sechzig')): add(t0, thud(0.6, 85), 0.06)
add(0.0, impact(3.0), 0.12); add(0.0, fio(engine(3.6, 70, 0.4, 700), 0.2, 0.6), 0.07)
for tb in (P('Und', 10) + 0.4, P('Und', 10) + 2.4, P('Und', 10) + 4.0): add(tb, boom_far(2.6), 0.12)
add(P('Wie', 15), swell(2.6, 52), 0.06)
add(P('Im', 264.5), fio(engine(4.0, 75, 0.35, 750), 0.4, 0.8), 0.06)
for tb in (P('eröffnete') + 0.2, P('eröffnete') + 1.6, P('eröffnete') + 3.1, P('eröffnete') + 4.3): add(tb, boom_far(2.6), 0.13)
add(P('eröffnete') + 0.2, impact(2.5), 0.08)
add(P('und', 318.5), fio(engine(3.8, 70, 0.4, 700), 0.3, 0.8), 0.07)
add(V.T_PA, swell(2.6, 49), 0.05); add(V.VEND + 0.3, swell(3.0, 55), 0.05)
o = sfxlib.out[:int(SR * T)]; o /= max(1.0, np.abs(o).max() / 0.9); wavfile.write(OUTD + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
