# sound effects for the Wainwright short: film shots, the freeze on the signature, written words, stamps, transitions
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import wshort as V
T = V.T; ws = V.ws
sfxlib.out = np.zeros((int(SR * T), 2))
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def hit(t0, g=0.10, f=85): add(t0, thud(0.9, f), g)
def stamp_(t0): add(t0, stampthump(), 0.20)
def pen(t0, dur, g=0.05):
    for i in range(int(dur / 0.16)): add(t0 + i * 0.16, scratch(0.18), g * rng.uniform(0.6, 1.0), rng.uniform(-0.2, 0.2))
for s, fn, tr in V.ANCH[1:]:
    if tr and tr[0] == 'whip': add(s - 0.2, whoosh(0.6, 300, 2400), 0.11, 0.5 * tr[1])
    else: add(s - 0.08, whoosh(0.5, 200, 1400), 0.045, rng.uniform(-0.3, 0.3))
# Missouri: pen on paper, the freeze, the words, the slide to Wainwright
pen(0.1, 3.1, 0.035); add(V.FREEZE_AT, impact(2.5), 0.13); add(V.FREEZE_AT + 0.15, whoosh(0.4, 400, 2200), 0.06)
pen(ws("Japan's") - 0.1, 0.35, 0.06); pen(ws('surrender') - 0.05, 0.4, 0.06)
add(ws('turned'), whoosh(1.3, 200, 1200), 0.08, -0.5); add(ws('thin') - 0.1, ping(900, 1.2), 0.03)
stamp_(ws('surrendered', 10) - 0.03); hit(ws('Jonathan'), 0.10, 70); add(ws('Jonathan'), swell(2.0, 52), 0.06)
panned(ws('In', 13.5), fio(engine(3.3, 90, 0.35, 900), 0.4, 0.6), 0.06, 0.6, -0.6); add(ws('March'), whoosh(0.6, 200, 1200), 0.06)
add(ws('Wainwright', 17), ping(800, 1.2), 0.035)
add(ws('On', 19.5), boom_far(), 0.09); add(ws('Corregidor'), whoosh(0.6, 200, 1200), 0.06)
for k in range(4): add(ws('under', 22) + 0.15 + k * 0.55, boom_far(2.2), 0.08)
hit(ws('May', 22), 0.08, 80); stamp_(ws('surrendered', 24.5) - 0.03)
add(ws('The', 28), fio(static(5.0, 0.5), 0.4, 0.8), 0.02); hit(ws('Manila'), 0.07, 90); add(ws('air', 30) - 0.25, ping(1200, 1.0), 0.05)
pen(ws('prisoner', 33) - 0.2, 0.4, 0.07); hit(ws('prisoner', 33), 0.07, 70)
for nm in ('more', 'camp', 'Manchuria'): add(ws(nm, 36) - 0.02, tick(), 0.06)
add(ws('For', 36), fio(drone4(4.5, 49), 0.5, 1.0), 0.05); pen(ws('gave', 40) - 0.1, 0.35, 0.07)
add(ws('In', 44), fio(engine(3.4, 70, 0.3, 700), 0.4, 0.8), 0.05); hit(ws('August', 44), 0.07, 90); stamp_(ws('freed', 44) - 0.03)
hit(ws('Two', 47.5), 0.07, 85); hit(ws('USS', 47.5), 0.09, 70)
hit(ws('Medal', 51), 0.09, 70); stamp_(ws('blocked', 51) - 0.03)
add(ws('The', 56.5), swell(3.5, 49), 0.07); hit(ws('watched', 56.5), 0.10, 60); pen(ws('The', 56.5) + 0.3, 1.8, 0.03)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.6)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
