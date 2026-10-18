import sys, json
sys.path.insert(0, sys.argv[1])
import sfxlib
from sfxlib import *
D = sys.argv[2]
TT = 128.68
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
def ticks(t0, n, dur, g=0.04):
    for i in range(n): add(t0 + i * dur / max(1, n), tick(), g * rng.uniform(0.8, 1.0), rng.uniform(-0.3, 0.3))
def prop(a, b, g=0.06, f=62, pan0=-0.5, pan1=0.5):   # radial engine passing
    panned(a, fio(engine(b - a, f, 0.35, 520), 0.8, 1.0), g, pan0, pan1)
def winter(a, b, g=0.05): add(a, fio(wind(b - a), 0.8, 1.0), g)

# hook: three aircraft bands, then the portrait
add(0.05, impact(), 0.22)
for i, (ti, s) in enumerate(((0.05, -0.6), (0.45, 0.6), (1.25, -0.6))): add(ti, whoosh(0.5, 250, 1400), 0.07, s); hit(ti + 0.15, 0.08, 95)
panned(0.0, jet(2.4), 0.10, -0.8, 0.8)
add(2.2, swell(2.0, 44), 0.12); hit(2.30, 0.14, 70)
hit(wt('56') - 0.05, 0.13, 75); hit(wt('56') + 0.23, 0.13, 70)
add(wt('Eino') - 0.1, impact(), 0.26)
# Karelia map
add(8.75, fio(drone4(4.9 + 0.5), 0.8, 1.0), 0.06); winter(8.75, 13.9, 0.03)
hit(wt('Karelien'), 0.11, 80); add(wt('Sortavala'), tone(392, 2.0), 0.04)
# 1930s, few modern planes
air(13.6); hit(wt('1930er'), 0.10, 90); air(wt('Pilot'), 0.04)
prop(19.4, 22.9, 0.05, 55); add(wt('kaum') + 0.25, scratch(0.4), 0.06)
# Winter War begins
winter(22.5, 28.9, 0.05); add(wt('Sowjetunion'), boom_far(), 0.10); add(wt('Sowjetunion') + 1.6, boom_far(), 0.07)
add(wt('30.') - 0.05, flip(), 0.10); hit(wt('30.') + 0.35, 0.10, 100)
prop(28.7, 32.7, 0.05, 66, 0.5, -0.5); hit(wt('Jagdstaffel'), 0.11, 80)
winter(32.4, 36.8, 0.04); add(wt('Fokker'), scratch(0.4), 0.04); hit(wt('Fokker') + 0.5, 0.09, 95)
# odds
add(36.5, fio(engine(3.8, 48, 0.5, 400), 1.0, 0.8), 0.07); ticks(wt('Gegner') + 0.35, 23, 23 * 0.07, 0.03)
add(wt('weit'), thud(1.0, 65), 0.12)
# first victory
prop(40.0, 44.9, 0.06, 70); add(wt('SB-Bomber') - 0.3, mg_burst(6), 0.05, 0.3); hit(wt('SB-Bomber'), 0.12, 75)
# Karelia lost
add(44.7, fio(drone4(9.6), 1.0, 1.2), 0.06); winter(44.7, 54.3, 0.03)
hit(wt('März', 45), 0.10, 85); add(wt('große', 45), swell(2.5, 41), 0.12); add(wt('abgeben'), thud(1.2, 55), 0.15)
add(wt('Heimat') - 0.1, tone(147, 3.0), 0.07)
# Brewster
prop(54.0, 60.2, 0.06, 64); air(wt('kaufte')); add(wt('Brewster'), scratch(0.4), 0.04); hit(wt('Brewster') + 0.5, 0.10, 90)
add(wt('doch', 61), scratch(0.35), 0.08); hit(wt('Fortsetzungskrieg'), 0.12, 72)
add(64.4, boom_far(), 0.06); add(66.0, crack(), 0.04, 0.4); air(wt('überraschend'))
hit(wt('14,5'), 0.11, 85); hit(wt('14,5') + 0.36, 0.09, 95); air(wt('geteilte'), 0.04)
# JG 34, Bf 109
air(77.5); hit(wt('März', 77), 0.10, 85); add(79.5, rustle(0.6), 0.04); hit(wt('Major'), 0.10, 95); hit(wt('Jagdstaffel', 80), 0.11, 80)
panned(83.9, fio(engine(4.8, 92, 0.25, 900), 0.6, 0.8), 0.06, 0.6, -0.4); add(wt('deutsche'), scratch(0.4), 0.04)
# 1944 offensive
for k, g in ((88.7, 0.09), (90.2, 0.07), (91.9, 0.10), (93.3, 0.07)): add(k, boom_far(), g, rng.uniform(-0.5, 0.5))
hit(wt('Sommer'), 0.10, 85); add(wt('Großoffensive'), thud(1.2, 58), 0.13)
# Mannerheim Cross
add(95.2, swell(3.0, 49), 0.08); hit(wt('18.'), 0.10, 90); add(wt('Mannerheim-Kreuz,'), tone(196, 3.5), 0.08)
# last victory
prop(102.1, 108.7, 0.06, 90, -0.4, 0.4); hit(wt('5.', 100), 0.10, 90)
add(wt('56.') - 0.05, stampthump(), 0.22); add(wt('letzten'), thud(1.0, 70), 0.10)
# war ends
winter(108.4, 114.0, 0.04); add(wt('schwiegen'), swell(3.0, 41), 0.08); add(wt('Karelien', 110), thud(1.2, 55), 0.12)
air(113.7, 0.04); hit(wt('1951'), 0.09, 90); add(wt('Erinnerungen') - 0.15, scratch(1.0), 0.04)
add(wt('1964') - 0.3, tone(110, 3.5), 0.10); hit(wt('54'), 0.08, 95)
hit(wt('Kanntet'), 0.10, 90); hit(wt('Schreibt'), 0.09, 100)
o = sfxlib.out; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(D + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('ok')
