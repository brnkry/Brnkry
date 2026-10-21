# sound effects for the Rommel long video: scene changes, stamps, typewriters, counters, maps, clips
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
import full as V
T = V.T; w = V.w; ST = V.ST
sfxlib.out = np.zeros((int(SR * T), 2))
def fio(x, a=0.6, b=0.8):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def hit(t0, g=0.10, f=85): add(t0, thud(0.9, f), g)
def air(t0, g=0.035): add(t0, whoosh(0.6, 200, 1200), g, rng.uniform(-0.3, 0.3))
def draw(t0, dur, g=0.04): add(t0, fio(whoosh(dur, 500, 2200), 0.1, 0.2), g); add(t0, scratch(min(dur, 1.0)), g * 0.8)
def typing(t0, n, step=0.06, g=0.05):
    for i in range(n): add(t0 + i * step, clack(), g * rng.uniform(0.7, 1.0), rng.uniform(-0.2, 0.2))
def stampsnd(t0, g=0.22): add(t0, stampthump(), g)
def ticks(t0, n, dur, g=0.035):
    for i in range(n): add(t0 + i * dur / max(1, n), tick(), g * rng.uniform(0.8, 1.0), rng.uniform(-0.3, 0.3))
def docsnd(t0, nchars): add(t0, flip(), 0.08); typing(t0 + 0.45, min(40, nchars), 0.028 * max(1, nchars / 40), 0.035)

for s, fn in V.ANCH[1:]: air(s - 0.1)
for k, num, title in V.CHAP: add(ST[k] + 0.05, fio(whoosh(1.0, 250, 1500), 0.1, 0.4), 0.07); hit(ST[k] + 0.2, 0.08, 70)
# intro
add(0.05, impact(), 0.18); typing(0.4, 16); add(1.0, fio(engine(5.5, 60, 0.25, 500), 1.0, 1.5), 0.04)
hit(w('Zwei', 2), 0.09, 90); add(w('Hausherr', 4), door(), 0.06)
add(w('tot', 5) - 0.2, tone(98, 3.0), 0.08); docsnd(ST[6] - 0.1, 90)
add(w('Staatsbegräbnis', 7), swell(2.2, 49), 0.08); stampsnd(w('gelogen', 8))
hit(w('Erwin', 9), 0.12, 70); for_ = [hit(w(x, 9), 0.08, 95) for x in ('geschrieben', 'bewundert', 'gestritten')]
add(w('Legende', 10) - 0.2, swell(2.0, 55), 0.08)
# K1
typing(w('1917', 11), 12); draw(w('Abteilung', 12), 2.0); hit(w('Front', 12), 0.09, 80)
draw(w('umgehen', 14), 2.4); add(w('auf', 14), ping(900), 0.04)
draw(ST[15] - 0.1, 1.6); hit(w('Gipfel', 15), 0.10, 80)
ticks(w('9.000', 16), 22, 1.6, 0.03); hit(w('9.000', 16) + 1.6, 0.11, 75)
add(w('Pour', 17), ping(1200), 0.04); typing(w('1891', 18), 4, 0.1); add(w('Heidenheim', 18), ping(800), 0.04)
for x in ('schnell', 'vorne', 'Gegner'): hit(w(x, 20), 0.08, 95)
# K2
docsnd(ST[21], 60); typing(w('Zwanzig', 21), 4, 0.1); stampsnd(w('Bestseller', 22))
typing(ST[24], 14); [add(w('Angriff', 24) + i * 0.25, boom_far(), 0.06, -0.5 + i * 0.3) for i in range(4)]
hit(w('Panzerdivision', 25), 0.11, 70); add(w('Panzerdivision', 25), metal(160, 1.6), 0.04); draw(w('Infanterist', 26), 0.8); draw(w('Panzer', 26), 0.8); hit(w('nie', 26), 0.10, 90)
# K3
typing(ST[27] + 0.4, 8); add(ST[27] + 0.2, fio(engine(3.5, 55, 0.4, 500), 0.8, 1.0), 0.05)
add(w('Westen', 29) - 0.6, fio(whoosh(1.8, 200, 900), 0.2, 0.5), 0.07); add(w('Westen', 29) - 0.5, fio(engine(3.0, 60, 0.4, 500), 0.6, 1.0), 0.05)
add(w('Gespensterdivision', 30) - 0.3, fio(drone4(3.0, 52), 0.4, 1.0), 0.07)
hit(w('Verluste', 35), 0.10, 70); hit(w('kleinzureden', 35), 0.08, 100)
add(w('Bilder', 36), ping(1000), 0.04); add(w('Kameras', 37), scratch(0.2), 0.05)
for i in range(3): add(w('Heimat', 37) - 0.1 + i * 0.4, tick(), 0.08)
hit(w('Heimat', 37) + 1.1, 0.10, 80)
# K4
panned(ST[38], fio(engine(4.0, 95, 0.3, 900), 0.8, 1.0), 0.06, -0.7, 0.7); typing(ST[38] + 0.3, 20)
hit(w('Afrikakorps', 39), 0.10, 75); docsnd(w('Auftrag', 40), 30); hit(w('trotzdem', 41), 0.12, 70)
draw(w('jagt', 42), 1.6); add(w('Tobruk', 43), ping(800), 0.04)
for i in range(4): add(ST[44] + 0.2 + i * 0.8, boom_far(), 0.10, -0.4 + i * 0.25)
add(ST[45], fio(wind(3.5), 0.8, 1.0), 0.05); add(w('Mittelmeer', 46) - 0.5, fio(waves(2.5), 0.5, 0.8), 0.05); draw(w('Küstenstraße', 46) - 1.2, 2.2)
typing(w('Spitznamen', 49), 14, 0.065); add(w('Wüstenfuchs', 49) - 0.2, swell(2.2, 52), 0.09); hit(w('Wüstenfuchs', 49), 0.10, 75)
docsnd(ST[51], 70); draw(w('nicht', 52), 0.5); hit(w('Deutschen', 52), 0.10, 85)
typing(ST[53] + 0.3, 9); ticks(w('30.000', 53), 20, 1.3, 0.03); hit(w('30.000', 53) + 1.3, 0.11, 75)
hit(w('Generalfeldmarschall', 54), 0.12, 70); add(w('Generalfeldmarschall', 54), metal(200, 1.6), 0.04)
# K5
add(ST[56], fio(wind(3.0), 0.6, 1.0), 0.05); draw(ST[57], 1.4); hit(w('stecken', 57), 0.11, 65)
for x in ('Panzer', 'Flugzeuge', 'Treibstoff'): ticks(w(x, 58) - 0.2, 12, 2.2, 0.025)
typing(ST[59] + 0.2, 12); [add(ST[59] + 0.2 + i * 0.7, boom_far(), 0.10, -0.5 + i * 0.3) for i in range(4)]
draw(w('eilt', 60), 1.6); panned(w('eilt', 60), fio(engine(2.0, 90, 0.3, 900), 0.4, 0.8), 0.04, -0.6, 0.6)
ticks(w('zwölf', 61), 12, 1.0, 0.04); docsnd(ST[62], 60); stampsnd(w('Sieg', 62) + 0.4, 0.12)
add(w('zieht', 63), fio(whoosh(1.2, 200, 900), 0.2, 0.4), 0.06); draw(ST[64] + 0.2, 3.0); typing(w('Mai', 64), 8)
ticks(w('250.000', 65) - 0.2, 24, 1.5, 0.03); hit(w('250.000', 65) + 1.3, 0.12, 70)
add(ST[66], fio(wind(3.0), 0.6, 1.0), 0.05)
# K6
typing(ST[67] + 0.5, 24); add(ST[67], fio(waves(4.0), 0.8, 1.0), 0.05); draw(w('Küste', 68) - 0.3, 2.2)
hit(w('Millionen', 69), 0.11, 75); add(w('schräge', 69), fio(waves(5.0), 0.6, 1.0), 0.04)
for x in ('schräge', 'Stahlkreuze'): [add(w(x, 69) + i * 0.15, metal(140 + 30 * i, 1.0), 0.04) for i in range(3)]
add(w('Landungsboote', 69) + 1.3, crack(), 0.06)
add(w('Holzstämme', 70), rustle(1.2), 0.05); add(w('Lastensegler', 70) - 0.3, fio(wind(2.2), 0.4, 0.4), 0.07); add(w('Lastensegler', 70) + 1.7, crack(), 0.07)
ticks(w('24', 71) - 0.4, 24, 2.6, 0.035); hit(w('24', 71) + 2.2, 0.10, 80)
for x in ('Küste', 'hinten', 'Kompromiss'): hit(w(x, 72 if x == 'Küste' else 73 if x == 'hinten' else 74), 0.08, 95)
typing(w('Morgen', 75), 12); add(w('nicht', 76), ping(700), 0.04); draw(w('Herrlingen', 77) - 0.6, 1.4)
# K7
hit(w('verloren', 78), 0.10, 70)
typing(ST[79] + 0.1, 13); add(ST[79], fio(engine(4.0, 70, 0.3, 600), 0.6, 0.6), 0.04)
panned(w('greift', 80) - 0.3, fio(jet(2.2), 0.4, 0.8), 0.10, 0.8, -0.6); add(w('greift', 80) + 0.6, mg_burst(8), 0.08, 0.1); add(w('greift', 80) + 1.6, crack(), 0.09)
add(w('schwer', 81), tone(82, 2.5), 0.07)
typing(ST[82] + 0.1, 13); hit(w('scheitert', 82), 0.10, 75)
for i in range(7): add(w('Verhaftungswelle', 83) + i * 0.22, flip(), 0.05)
add(w('Rommels', 84), ping(900), 0.04)
for x in ('Speidel', 'Kontakt'): draw(w(x, 86), 0.5)
draw(w('Ob', 87), 1.0); docsnd(ST[88], 50); stampsnd(w('Verdacht', 88))
# K8
typing(w('14.', 89), 16); add(w('Herrlingen', 89), ping(800), 0.04)
hit(w('Wilhelm', 91), 0.09, 80); hit(w('Ernst', 91), 0.09, 80); add(w('Wahl', 91) - 0.2, swell(2.0, 49), 0.08)
hit(w('Prozess', 92), 0.10, 80); hit(w('Gift', 92), 0.12, 60); add(w('Gift', 92), tone(73, 3.0), 0.06)
add(ST[94] + 0.3, door(), 0.06); add(w('Kapsel', 95) - 0.2, fio(drone4(3.5, 41), 0.4, 1.0), 0.07)
typing(ST[96] + 0.3, 21); add(ST[96], fio(wind(4.0), 1.0, 1.0), 0.03)
typing(w('Helden', 97) - 0.3, 21, 0.05); typing(w('Verwundungen', 97) - 0.2, 25, 0.05); draw(w('erlegen', 97) + 0.6, 0.5)
add(w('Totenmaske', 98) - 0.2, swell(2.4, 46), 0.09)
draw(ST[99], 1.0); stampsnd(w('2019', 99)); add(w('Wahrheit', 100) - 0.2, swell(2.4, 58), 0.08); hit(w('Manfred', 100), 0.10, 75)
# K9
typing(ST[101] + 0.5, 9); for_ = [add(w('Bücher', 102) - 0.4 + i * 0.18, thud(0.5, 140), 0.05) for i in range(5)]
add(w('Hollywood', 102), fio(engine(2.5, 24, 0.1, 400), 0.2, 0.5), 0.04); for_ = [add(w('Hollywood', 102) + i * 0.0417, tick(), 0.012) for i in range(60)]
add(ST[103], fio(wind(4.0), 0.8, 1.0), 0.04); draw(ST[104], 1.2); hit(w('Kasernen', 104), 0.09, 85)
hit(w('kritischer', 105), 0.10, 70)
for i in range(5): hit(w('steilen', 106) - 0.3 + i * 0.55, 0.07, 100 + i * 8)
add(ST[107], fio(boom_far(4.0), 0.3, 1.5), 0.06); hit(w('Zwangsarbeit', 107), 0.10, 65)
hit(w('Minen', 110), 0.08, 70); for_ = [add(w('Minen', 110) + i * 0.15, metal(110, 0.8), 0.025) for i in range(6)]
draw(ST[111], 1.2); add(w('Figur', 111), swell(2.0, 52), 0.07)
add(ST[112], swell(3.0, 55), 0.06); add(w('Tod', 113) - 0.3, tone(73, 3.0), 0.07)
hit(w('Wie', 114), 0.10, 90); hit(w('Erwin', 114), 0.10, 75); hit(w('Schreibt', 115), 0.09, 100)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 1.2)[:, None]
o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
