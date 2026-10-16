import sys, json
sys.path.insert(0, sys.argv[1])
from sfxlib import *
WD = json.load(open(sys.argv[2]))
def wt(s, after=0.0):
    for w, a, b in WD:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a
    raise KeyError(s)
def fadeio(x, a=0.6, b=0.8):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
# hook
add(0.0, fadeio(drone4(5.8), 1.2, 0.35), 0.11); add(0.0, swell(3.0, 41), 0.18)
add(0.24, thud(1.2, 62), 0.14); add(2.17, thud(1.2, 58), 0.12)
add(wt('schoss') - 0.03, impact(), 0.34)
# dossier / calendar
add(6.35, rustle(0.6), 0.07); add(wt('Franz') - 0.25, thud(0.7, 120), 0.12); add(wt('Charlie') - 0.25, thud(0.7, 115), 0.12)
t20 = wt('20.')
for i in range(4): add(t20 - 0.08 - i * 0.12, flip(), 0.10)
add(wt('1943'), thud(1.0, 70), 0.14)
add(15.3, whoosh(0.8, 150, 700), 0.07); add(wt('Leutnant'), thud(0.6, 100), 0.10)
add(19.45, whoosh(0.7, 200, 900), 0.08, 0.3); add(wt('Kommandant'), thud(0.7, 95), 0.12)
# map Bremen
add(23.6, fadeio(drone4(5.2), 0.8, 0.8), 0.10)
r = np.random.default_rng(4)
for i in range(10): add(wt('Flak') + i * 0.28, boom_far(2.4), 0.10, r.uniform(-0.6, 0.6))
panned(wt('Jäger'), engine(2.0, 115, 0.3, 900), 0.07, 0.8, -0.2)
add(wt('schwer'), metal(180, 1.6), 0.07)
# damage callouts
for k in ('Motoren', 'Bugkanzel', 'Leitwerk'): add(wt(k), thud(1.0, 72), 0.16); add(wt(k) + 0.05, metal(140, 1.4), 0.04)
add(28.5, fadeio(drone4(5.8, 52, 380) * np.linspace(1, 0.4, int(SR * 5.8)), 0.4, 0.8), 0.06)
# ledger
add(34.0, whoosh(0.6, 200, 900), 0.06, -0.3); add(34.2, scratch(0.6), 0.04); add(wt('Hugh'), scratch(0.7), 0.05)
add(wt('tot') + 0.1, stampthump(), 0.24)
for i in range(4): add(wt('mehrere') + i * 0.25, scratch(0.4), 0.04)
add(wt('verwundet'), scratch(0.5), 0.05)
# Bf 109
panned(39.5, fadeio(engine(7.0, 112, 0.28, 950), 0.6, 1.0), 0.09, 0.7, -0.7)
add(wt('Bf'), thud(0.7, 90), 0.10)
# tally + heartbeat
add(wt('Ein', 46) - 0.1, scratch(0.25), 0.07); add(wt('weiterer') - 0.1, scratch(0.25), 0.07)
add(wt('Ritterkreuz'), tone(73, 3.0), 0.16); add(wt('Ritterkreuz'), thud(1.2, 60), 0.14)
add(wt('gebracht'), heartbeat(5), 0.30)
# Roedel / quote
add(54.15, whoosh(0.7, 200, 900), 0.07, 0.3); add(wt('Gustav'), thud(0.8, 90), 0.12)
add(58.25, rustle(0.5), 0.05); add(wt('selbst') + 0.2, thud(1.0, 66), 0.14)
# Sweden / escort
add(62.2, fadeio(drone4(10.2, 54, 420), 1.0, 1.2), 0.08); add(62.2, fadeio(engine(10.2, 108, 0.28, 850), 1.0, 1.2), 0.04, 0.3)
add(wt('Schweden') + 0.4, thud(0.8, 85), 0.10); add(wt('verstand'), swell(2.5, 46), 0.10)
add(67.35, whoosh(0.7, 200, 900), 0.07, -0.3)
# salute and landing
add(72.2, fadeio(drone4(6.5, 55, 420), 0.6, 1.5), 0.08)
add(wt('salutierte'), tone(98, 3.5), 0.15); add(wt('salutierte'), thud(1.4, 58), 0.12)
panned(wt('drehte'), fadeio(engine(2.4, 120, 0.25, 1000), 0.2, 1.4), 0.08, 0.0, 0.9)
add(wt('landete'), wind(2.2), 0.05); add(wt('Seething'), thud(0.9, 70), 0.14)
# report
add(78.85, whoosh(0.6, 200, 900), 0.06, 0.3)
for i in range(7): add(wt('meldete') + i * 0.06, clack(), 0.07)
add(wt('nie,'), scratch(0.3), 0.09); add(wt('Kriegsgericht'), stampthump(), 0.30)
# Canada / notice / reunion
add(wt('1953'), swell(2.6, 44), 0.12); add(wt('1953'), thud(1.0, 66), 0.12)
add(87.75, rustle(0.6), 0.06); add(wt('suchte'), thud(0.8, 90), 0.10)
add(wt('1990'), swell(3.0, 49), 0.12); add(wt('enge'), tone(87, 3.5), 0.12)
# 2008
add(wt('März'), tone(65, 3.0), 0.12); add(wt('November'), tone(65, 3.0), 0.12)
add(109.0, whoosh(0.8, 150, 700), 0.06); add(wt('Schreibt'), thud(0.7, 100), 0.09)
out /= max(1.0, np.abs(out).max() / 0.95)
wavfile.write(sys.argv[3], SR, (out * 32767).astype(np.int16))
print('ok')
