import sys, json
sys.path.insert(0, sys.argv[1])
import sfxlib
from sfxlib import *
D = sys.argv[2]
TT = 109.2
sfxlib.out = np.zeros((int(SR * TT), 2))
WD = json.load(open(D + '/words.json'))
def wt(s, after=0.0):
    for w, a, b in WD:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a
    raise KeyError(s)
def fio(x, a=0.6, b=0.8):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def hit(t0, g=0.12, f=80): add(t0, thud(0.9, f), g)
def air(t0, g=0.05): add(t0, whoosh(0.5, 200, 1200), g)
def chalk(t0, d=0.4, g=0.06): add(t0, scratch(d), g, rng.uniform(-0.3, 0.3))
def sea(a, b, g=0.05): add(a, fio(waves(b - a), 0.8, 1.0), g)
S = lambda s, a=0.0: wt(s, a)

# hook: chalk floor
add(0.05, impact(), 0.20); add(0.0, fio(drone4(8.4), 0.4, 1.0), 0.05)
hit(S('Liverpool'), 0.10, 90); chalk(S('Kreide'), 0.6, 0.08); air(S('Holzmodelle'), 0.05); add(S('Holzmodelle') + 0.3, clack(), 0.06)
air(S('Taktik') - 0.1); hit(S('U-Boote'), 0.12, 70)
add(S('Jean') - 0.2, swell(2.0, 49), 0.10); hit(S('Jean'), 0.10, 90); hit(S('Laidlaw.'), 0.12, 75)
# 1942 losses
sea(10.0, 15.5, 0.05); add(10.0, boom_far(), 0.10); hit(S('1942'), 0.12, 85); add(S('Atlantik'), thud(1.0, 65), 0.10)
for i in range(8): add(S('Schiff') + i * 0.11 + 0.25, tick(), 0.05)
add(S('Schiff') + 0.4, boom_far(), 0.08, 0.4)
# night convoy
sea(15.3, 20.3, 0.06); add(15.3, fio(drone4(5.0, 52), 0.6, 0.8), 0.06)
for k in (S('verstand') - 0.05, S('genau') + 0.1, S('U-Boote', 17) + 0.1, S('Geleitzüge') + 0.2): add(k, boom_far(), 0.12, rng.uniform(-0.5, 0.5))
hit(S('wie', 16.5), 0.12, 70)
# Liverpool, W.A.T.U.
air(20.0); hit(S('Liverpool', 20), 0.09, 95); air(S('Problem'), 0.04)
add(24.9, door(), 0.06)
for k in ('Western', 'Approaches', 'Tactical', 'Unit'): hit(S(k), 0.08, 100)
air(S('Kapitän') - 0.15); hit(S('Gilbert'), 0.11, 80)
# Wrens
air(31.1); hit(S('Frauen'), 0.09, 95); add(S('Marinehelferinnendienstes,'), rustle(0.6), 0.04); hit(S('Wrens.'), 0.12, 80)
hit(S('Jean', 37), 0.10, 85); hit(S('21'), 0.11, 90); hit(S('21') + 0.15, 0.09, 95); air(S('Schottin')); add(S('ausgebildete'), clack(), 0.06)
# models, grid, slit
air(43.0); add(S('Schiffsmodelle'), clack(), 0.07); add(S('Schiffsmodelle') + 0.25, clack(), 0.05)
chalk(S('Raster'), 0.8, 0.07)
hit(S('Offiziere'), 0.08, 95); add(S('Schlitze') - 0.1, rustle(0.7), 0.07); add(S('Schlitze') + 0.1, thud(1.0, 60), 0.10)
add(S('wie', 51), fio(waves(2.0), 0.4, 0.8), 0.04)
air(53.3); hit(S('Muster.'), 0.12, 75)
# chalk game
add(55.6, impact(), 0.12)
for i in range(12): chalk(55.75 + i * 0.06, 0.25, 0.035)
for i in range(4): chalk(56.3 + i * 0.08, 0.25, 0.04)
add(S('U-Boote', 55), sonar_ping(), 0.05); chalk(S('hinten', 55) - 0.2, 1.0, 0.05); chalk(S('Inneren', 58), 0.9, 0.05)
add(S('an', 60.5) - 0.35, whoosh(0.4, 600, 2000), 0.05); add(S('an', 60.5), bomb(), 0.13)
add(S('tauchten', 61), under(2.5), 0.08); add(S('tauchten', 61) + 0.3, sonar_ping(700), 0.05)
add(S('Begleitschiffe', 62), sonar_ping(900), 0.05); air(S('Begleitschiffe', 62), 0.04)
add(S('Gegenmaßnahme'), swell(2.0, 46), 0.10); hit(S('Gegenmaßnahme'), 0.13, 75)
add(S('Angriff', 68), bomb(), 0.11)
chalk(S('fielen', 69), 2.2, 0.06); air(S('fielen', 69), 0.05)
chalk(S('suchten', 72), 1.6, 0.06); add(S('Gebiet', 72), sonar_ping(820), 0.06); add(S('Geleitzug', 74), sonar_ping(1000, 2.0), 0.07); hit(S('Geleitzug', 74), 0.10, 85)
# Raspberry
air(75.5); add(S('Raspberry,') - 0.05, stampthump(), 0.24); air(S('englischen'), 0.04)
# Noble
air(82.5); hit(S('Admiral'), 0.08, 95); hit(S('Percy'), 0.11, 80)
tw0 = S('sofort') + 0.15
for i in range(20): add(tw0 + i / 16, clack(), 0.05, rng.uniform(-0.2, 0.2))
# 5000
add(87.4, swell(2.0, 44), 0.08); hit(S('Kriegsende'), 0.10, 90); ticks = [add(S('5.000') + i * 0.028, tick(), 0.035) for i in range(50)]
hit(S('5.000') + 1.4, 0.12, 75); add(S('Marineoffiziere'), thud(0.8, 90), 0.08)
# award and no recognition
air(92.7); add(S('Roberts', 92) + 0.05, whoosh(0.5, 300, 1500), 0.05); hit(S('ausgezeichnet,'), 0.09, 95)
for i in range(9): add(S('Frauen', 95) + i * 0.06, tick(), 0.03)
add(S('keine', 96), thud(1.2, 55), 0.14)
# later life
add(98.5, swell(3.0, 41), 0.08); air(S('Krieg', 100)); hit(S('Beruf'), 0.08, 95); add(S('2008.'), tone(110, 3.0), 0.09)
hit(S('Kanntet'), 0.10, 90); hit(S('Schreibt'), 0.09, 100)
o = sfxlib.out; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(D + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('ok')
