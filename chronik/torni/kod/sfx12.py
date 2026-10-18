# sound effects for intro + chapter 1
import sys, json
sys.path.insert(0, sys.argv[1])
import numpy as np, sfxlib
from sfxlib import *
D = sys.argv[2]; T = 81.95
sfxlib.out = np.zeros((int(SR * T), 2))
W_ = json.load(open(D + '/words.json'))
def wt(s, after=0.0):
    for w, a, b in W_:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a
def fio(x, a=0.6, b=0.8):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def rotor(dur, rate=5.2):
    n = int(SR * dur); t = np.arange(n) / SR
    y = lp(rng.normal(0, 1, n), 380) * (0.35 + 0.65 * np.maximum(0, np.sin(2 * np.pi * rate * t)) ** 6) + 0.25 * engine(dur, 96, 0.2, 900)
    return norm(y) * np.minimum(1, np.minimum(t / 1.5, (dur - t) / 1.2))
def typing(t0, s, step, g=0.06):
    for i, c in enumerate(s):
        if c != ' ': add(t0 + i * step, clack(), g, rng.uniform(-0.2, 0.2))
def hit(t0, g=0.11, f=80): add(t0, thud(0.9, f), g)
def air(t0, g=0.05): add(t0, whoosh(0.6, 200, 1200), g)
# intro
add(0.0, fio(wind(7.0), 1.0, 1.5), 0.03); panned(0.2, rotor(6.5), 0.12, -0.7, 0.6)
typing(0.25, '18. OKTOBER 1965', 0.075); hit(wt('Vietnams'), 0.10, 85)
air(3.3); add(wt('Hubschrauber') - 0.2, fio(static(1.4, 1.0), 0.05, 0.6), 0.04); add(wt('Hubschrauber') - 0.2, thud(1.2, 58), 0.13)
air(6.9); hit(wt('Larry'), 0.10, 90); add(wt('Thorne'), impact(), 0.16)
for i in range(14): add(wt('34') + i * 0.1, tick(), 0.04)
hit(wt('Jahre', 12) + 0.1, 0.11, 75)
add(16.8, swell(3.0, 44), 0.07)
for w in ('Finnland', 'Waffen-SS,', 'Army.'): k = wt(w, 20) - 0.25; add(k, whoosh(0.5, 250, 1400), 0.06); add(k + 0.3, thud(0.8, 95), 0.08)
add(29.0, swell(3.0, 41), 0.07); hit(wt('Lauri', 32), 0.10, 85); add(wt('Törni', 33), impact(), 0.24)
# chapter 1
add(35.0, whoosh(0.8, 200, 1000), 0.06); add(35.3, tone(98, 3.0), 0.06)
typing(wt('28.'), '28. MAI 1919', 0.08); hit(wt('Viipuri', 40), 0.10, 90)
air(43.8); add(wt('heute'), scratch(0.5), 0.04); hit(wt('Russland'), 0.10, 80)
air(49.9); hit(wt('1938'), 0.10, 90)
typing(wt('November'), 'NOVEMBER 1939', 0.07)
for i in range(5): add(wt('griff') - 0.2 + i * 0.18, whoosh(0.7, 150, 900), 0.05, rng.uniform(-0.4, 0.4))
add(wt('griff'), boom_far(), 0.10); add(wt('griff') + 0.9, boom_far(), 0.08); hit(wt('Sowjetunion', 57) + 0.3, 0.12, 70)
add(60.4, fio(wind(4.5), 0.8, 1.0), 0.05); add(61.2, boom_far(), 0.05)
air(64.5); hit(wt('Lemetti'), 0.10, 85)
for i in range(6): add(wt('eingekesselte') - 0.1 + i * 0.08, whoosh(0.4, 300, 1600), 0.035)
add(wt('zerschlugen'), thud(1.2, 60), 0.13)
add(69.9, fio(wind(6.0), 1.0, 1.0), 0.04); typing(wt('März', 70), 'MÄRZ 1940', 0.08); hit(wt('Leutnant'), 0.10, 90)
air(75.9); add(wt('Teile', 77), swell(2.5, 41), 0.08); add(wt('abgeben'), thud(1.2, 58), 0.13); add(wt('Viipuri', 79), tone(147, 2.5), 0.06)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 1.0)[:, None]
o /= max(1.0, np.abs(o).max() / 0.9); wavfile.write(D + '/sfx12.wav', SR, (o * 32767).astype(np.int16)); print('ok')
