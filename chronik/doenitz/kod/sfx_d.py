# sound effects for the Dönitz short: transitions, stamps, paper drops, the sinking ship, typewriter, pen
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import dshort as V
T = V.T; ws = V.ws
sfxlib.out = np.zeros((int(SR * T), 2))
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def hit(t0, g=0.10, f=85): add(t0, thud(0.9, f), g)
def stamp_(t0, g=0.20): add(t0, stampthump(), g)
def pen(t0, dur, g=0.05):
    for i in range(int(dur / 0.16)): add(t0 + i * 0.16, scratch(0.18), g * rng.uniform(0.6, 1.0), rng.uniform(-0.2, 0.2))
def typing(t0, n, step=0.03, g=0.03):
    for i in range(n): add(t0 + i * step, clack(), g * rng.uniform(0.7, 1.0), rng.uniform(-0.2, 0.2))
def paper(t0, g=0.09): add(t0 - 0.05, flip(), g, rng.uniform(-0.3, 0.3)); add(t0 + 0.22, thud(0.5, 140), 0.05)
for s, fn, tr in V.ANCH[1:]:
    if tr and tr[0] == 'whip': add(s - 0.2, whoosh(0.6, 300, 2400), 0.11, 0.5 * tr[1])
    else: add(s - 0.08, whoosh(0.5, 200, 1400), 0.045, rng.uniform(-0.3, 0.3))
add(0.02, impact(), 0.14); hit(ws('Hitlers'), 0.08, 80); hit(ws('Nachfolger'), 0.09, 65)
hit(ws('Schulklasse'), 0.08, 75); hit(ws('Karl', 4.5), 0.09, 70); add(ws('Dönitz', 5), swell(2.0, 52), 0.07); hit(ws('Dönitz', 5), 0.11, 60)
add(ws('Als', 6) - 0.1, fio(static(6.2, 0.5), 0.3, 0.6), 0.025)
add(ws('U-Boote') - 0.1, sonar_ping(820, 3.0), 0.05); add(ws('U-Boote'), fio(under(2.6), 0.4, 0.6), 0.05)
stamp_(ws('nie', 11))
typing(ws('In', 12.3) + 0.2, 30, 0.022); typing(ws('ernannte'), 17, 0.022); typing(ws('Hitler', 13.5), 18, 0.022); typing(ws('Reichspräsidenten'), 21, 0.022)
add(ws('Reichspräsidenten') + 0.5, scratch(0.35), 0.08)
add(ws('Flensburg'), ping(760, 1.4), 0.05); add(ws('drei', 17.5), tone(98, 2.5), 0.04); hit(ws('drei', 17.5), 0.08, 75); add(ws('kaum'), boom_far(2.4), 0.07)
hit(ws('Am', 20.5), 0.08, 80); add(ws('britische'), fio(engine(2.0, 70, 0.4, 650), 0.3, 0.6), 0.05)
pen(ws('verhaftet'), 0.5, 0.07); hit(ws('verhaftet'), 0.08, 60)
hit(ws('Nürnberg'), 0.09, 70); stamp_(ws('zehn', 29)); add(ws('Spandau') + 0.1, metal(180, 1.4), 0.05); add(ws('Spandau') + 0.2, door(), 0.06)
hit(ws('Tag', 32), 0.07, 90); hit(ws('Januar'), 0.08, 80); hit(ws('Geesthacht'), 0.08, 75)
pen(ws('Uwe'), 0.6, 0.06); hit(ws('später', 41), 0.07, 85)
pen(ws('Kritik'), 0.5, 0.06); add(ws('Kritik') + 0.5, scratch(0.3), 0.09); pen(ws('Reue'), 0.5, 0.06); add(ws('Reue') + 0.45, scratch(0.3), 0.09)
hit(ws('applaudierten'), 0.06, 95); paper(ws('Lokalzeitung'))
paper(ws('Spiegel')); paper(ws('Zeit', 54.5)); paper(ws('Monde')); stamp_(ws('empört'), 0.22); hit(ws('empört'), 0.10, 55)
hit(ws('Schulleiter'), 0.07, 80); hit(ws('Druck', 59.5), 0.10, 60); add(ws('Leben', 61) - 0.1, swell(2.6, 46), 0.07)
hit(ws('Dönitz', 62), 0.08, 75); hit(ws('1980'), 0.09, 65); pen(ws('Rolle', 65), 0.5, 0.07); add(ws('zuletzt'), swell(2.0, 49), 0.05)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.3)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
