# sound effects for the whole Törni video: every arrow, route, stamp, counter and transition gets its sound
import sys, json
sys.path.insert(0, sys.argv[1])
import numpy as np, sfxlib
from sfxlib import *
D = sys.argv[2]; sfxlib.out = np.zeros((int(SR * T), 2))
W_ = json.load(open(D + '/words.json'))
sys.path.insert(0, D + '/code'); import full
T = full.T; M = full.M
sfxlib.out = np.zeros((int(SR * T), 2))
def w(s, after=0.0):
    after = M(after) if after else 0.0
    for x, a, b in W_:
        if a >= after - 0.01 and x.lower().startswith(s.lower()): return a
    raise KeyError(s)
def fio(x, a=0.6, b=0.8):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def rotor(dur, rate=5.2):
    n = int(SR * dur); t = np.arange(n) / SR
    y = lp(rng.normal(0, 1, n), 380) * (0.35 + 0.65 * np.maximum(0, np.sin(2 * np.pi * rate * t)) ** 6) + 0.25 * engine(dur, 96, 0.2, 900)
    return norm(y) * np.minimum(1, np.minimum(t / 1.5, (dur - t) / 1.2))
def typing(t0, s, step, g=0.06):
    for i, c in enumerate(s):
        if c != ' ': add(t0 + i * step + rng.uniform(-0.005, 0.005), clack(), g * rng.uniform(0.8, 1), rng.uniform(-0.2, 0.2))
def hit(t0, g=0.11, f=80): add(t0, thud(0.9, f), g)
def air(t0, g=0.05, d=0.6): add(t0, whoosh(d, 200, 1200), g, rng.uniform(-0.3, 0.3))
def draw(t0, dur, g=0.05, p0=-0.5, p1=0.5):   # a line or arrow being drawn: rising swish + pen scratch
    panned(t0, whoosh(dur, 250, 1600), g, p0, p1); add(t0, scratch(min(1.2, dur)), g * 0.6)
def pop(t0, g=0.07): add(t0, thud(0.4, 160), g); add(t0, tick(), g * 0.6)
def stampsnd(t0, g=0.24): add(t0, stampthump(), g)
def ticks(t0, n, dur, g=0.04):
    for i in range(n): add(t0 + i * dur / n, tick(), g * rng.uniform(0.8, 1))
def wave(a, b, g=0.05): add(a, fio(waves(b - a), 1.0, 1.0), g)
def windb(a, b, g=0.04): add(a, fio(wind(b - a), 1.0, 1.0), g)
def boom(t0, g=0.08): add(t0, boom_far(), g, rng.uniform(-0.5, 0.5))

# transitions: a soft whoosh into every scene
for s, e, fn in full.SC[1:]: air(s + 0.1, 0.035, 0.7)

# ---- intro
windb(M(0.0), M(7.0), 0.03); panned(M(0.2), rotor(6.5), 0.12, -0.7, 0.6); typing(M(0.25), '18. OKTOBER 1965', 0.075)
draw(M(3.45), 1.6, 0.06); pop(w('Vietnams'), 0.06)
add(w('Hubschrauber') - 0.2, fio(static(1.4, 1.0), 0.05, 0.6), 0.05); add(w('Hubschrauber') - 0.2, thud(1.2, 58), 0.14); add(w('Hubschrauber'), heartbeat(3), 0.10)
hit(w('Larry'), 0.10, 90); add(w('Thorne'), impact(), 0.16)
ticks(w('34'), 14, 1.4); hit(w('Jahre', 11) + 0.1, 0.11, 75)
add(M(15.7), swell(3.0, 44), 0.07)
for x in ('Finnland', 'Waffen-SS,', 'Army.'): k = w(x, 19); add(k - 0.2, whoosh(0.5, 250, 1400), 0.06); hit(k + 0.1, 0.08, 95)
add(M(27.9), swell(3.0, 41), 0.07); hit(w('Lauri', 30), 0.10, 85); add(w('Törni', 31), impact(), 0.24)
# ---- chapter 1
add(M(33.6), tone(98, 3.0), 0.06); typing(w('28.'), '28. MAI 1919', 0.08); hit(w('Viipuri', 38), 0.10, 90)
add(w('heute'), whoosh(0.9, 200, 900), 0.06); add(w('Wyborg'), scratch(0.4), 0.05); hit(w('Russland'), 0.10, 80)
hit(w('1938'), 0.10, 90); pop(w('Wehrdienst'))
windb(M(51.2), M(58.3), 0.05); typing(w('November', 50), 'NOVEMBER 1939', 0.07); add(w('griff'), mg_burst(6), 0.06, 0.3); boom(w('griff') + 0.3, 0.10); boom(w('griff') + 1.4, 0.08); hit(w('griff'), 0.12, 70)
windb(M(57.9), M(62.4), 0.05); boom(M(59.0), 0.05); pop(w('Ladogasees') - 0.2)
pop(w('Lemetti'), 0.08)
for i in range(6): add(w('eingekesselte') - 0.1 + i * 0.08, whoosh(0.45, 300, 1600), 0.04, -0.8 + i * 0.3)
draw(w('eingekesselte') + 0.7, 0.8, 0.05); add(w('zerschlugen'), thud(1.2, 60), 0.14)
windb(M(66.9), M(73.0), 0.04); typing(w('März', 65), 'MÄRZ 1940', 0.08); hit(w('Leutnant'), 0.10, 90)
add(w('Teile', 70) - 0.2, swell(2.5, 41), 0.08); add(w('abgeben'), thud(1.2, 58), 0.13); add(w('Viipuri', 75), tone(147, 2.5), 0.06)
# ---- chapter 2
add(M(79.0), tone(110, 3.0), 0.06); typing(w('Juni', 80), 'JUNI 1941', 0.07)
add(w('reiste'), fio(engine(2.4, 70, 0.3, 600), 0.4, 0.8), 0.05); draw(w('reiste'), 1.6, 0.06); pop(w('Wien', 80))
hit(w('mehrwöchige'), 0.10, 85); boom(M(91.5), 0.06); hit(w('Fortsetzungskrieg'), 0.12, 70)
hit(w('1943'), 0.10, 90); add(w('Abteilung'), impact(), 0.15)
windb(M(103.5), M(111.3), 0.04); draw(w('operierten'), 2.2, 0.06, -0.7, 0.7)
for i in range(2): add(w('Hinterhalte') + i * 0.35, mg_burst(4), 0.04, 0.5); hit(w('Hinterhalte') + i * 0.35, 0.07, 110)
draw(w('kehrten', 105), 1.6, 0.04, 0.7, -0.7)
stampsnd(w('Kopfgeld') - 0.1); ticks(w('drei', 112) - 0.2, 24, 1.6, 0.035); hit(w('Finnmark'), 0.11, 80)
boom(M(117.8), 0.07); boom(M(119.5), 0.06); typing(w('Sommer', 115), 'SOMMER 1944', 0.05, 0.05); hit(w('Ilomantsi'), 0.12, 75)
pop(w('Mauno')); hit(w('Koivisto'), 0.10, 90)
typing(w('Juli'), 'JULI 1944', 0.08); add(w('Mannerheim-Kreuz,') - 0.05, impact(), 0.20); add(w('höchste'), tone(196, 3.0), 0.06)
# ---- chapter 3
add(M(140.9), tone(98, 3.0), 0.06); add(w('September'), rustle(0.7), 0.07); typing(w('September') + 0.5, 'WAFFENSTILLSTAND', 0.05, 0.05)
add(w('Krieg', 146), thud(1.0, 65), 0.12); hit(w('Widerstand'), 0.09, 90)
typing(w('Januar'), 'JANUAR 1945', 0.07); draw(w('ging', 152), 1.6, 0.06, 0.6, -0.4); pop(w('Deutschland', 152)); hit(w('Saboteur'), 0.10, 85)
boom(M(162.0), 0.07); boom(M(164.5), 0.06); add(w('Mai', 165), thud(1.0, 70), 0.12)
stampsnd(w('Gefangenenlager'), 0.18); draw(w('floh', 170), 2.4, 0.07, -0.4, 0.6); pop(w('Finnland', 172))
for x in ('verhaftete', 'Aufnahmen', 'Akte'): add(w(x), flip(), 0.10); hit(w(x) + 0.05, 0.06, 120)
stampsnd(w('Akte') + 0.3)
add(w('Wegen', 180) - 0.2, rustle(0.7), 0.07); typing(w('Wegen', 180) + 0.3, 'URTEIL LANDESVERRAT', 0.05, 0.05); stampsnd(w('verurteilt') + 0.2, 0.26)
add(w('Zweimal'), metal(160, 1.6), 0.08); add(w('zweimal', 188), metal(130, 1.8), 0.10); hit(w('zweimal', 188), 0.12, 70)
typing(w('Dezember'), 'DEZEMBER 1948', 0.07); add(w('begnadigte'), impact(), 0.16)
# ---- chapter 4
add(M(200.4), tone(110, 3.0), 0.06); add(w('Zukunft') + 0.1, thud(1.0, 70), 0.10)
wave(M(203.0), M(221.8), 0.05); add(w('Schiff', 205), fio(engine(6.0, 48, 0.35, 380), 1.0, 1.0), 0.06); draw(w('Schiff', 205), 3.0, 0.04, 0.6, -0.4)
pop(w('Venezuela')); add(w('fuhr', 208), fio(engine(3.4, 52, 0.35, 380), 0.6, 0.8), 0.05); draw(w('fuhr', 208), 3.4, 0.04, 0.2, -0.6)
add(w('sprang'), whoosh(0.5, 300, 1500), 0.06); add(w('sprang') + 0.35, fio(waves(2.0), 0.02, 1.4), 0.14); pop(w('Alabamas'))
add(w('Gesetz') - 0.1, rustle(0.7), 0.07); typing(w('Gesetz') + 0.4, 'LODGE ACT', 0.06); stampsnd(w('Staatsbürgerschaft'), 0.14)
typing(w('1954'), '1954', 0.1); ticks(w('Namen', 233), 12, 1.2, 0.05); add(w('Larry', 233) + 0.6, impact(), 0.16)
hit(w('Special', 238), 0.10, 85); hit(w('Green'), 0.10, 90); pop(w('Staatsbürger', 240))
typing(w('1962'), '1962', 0.1); add(w('Tölz'), fio(engine(2.0, 90, 0.25, 800), 0.4, 0.8), 0.05); draw(w('Tölz'), 1.8, 0.06); pop(w('Iran', 245))
windb(M(250.1), M(264.1), 0.07); ticks(w('3.800') - 0.2, 20, 1.4, 0.035); hit(w('3.800') + 1.2, 0.10, 80); hit(w('geheimes'), 0.08, 95)
# ---- chapter 5
add(M(263.9), tone(98, 3.0), 0.06); hit(w('1963'), 0.10, 90)
stampsnd(w('geheimen')); pop(w('Laos', 270))
typing(w('18.', 270), '18. OKTOBER 1965', 0.07); panned(w('startete') - 0.3, rotor(6.0), 0.13, -0.6, 0.4)
add(w('Wetter') - 0.3, fio(rustle(5.0), 1.0, 1.0), 0.05); add(w('Wetter'), fio(wind(4.0), 0.5, 1.0), 0.06)
add(w('stürzte'), fio(static(1.4, 1.0), 0.05, 0.6), 0.05); add(w('stürzte'), thud(1.4, 52), 0.16); add(w('stürzte') + 0.3, heartbeat(3), 0.10)
add(w('Suche', 290), swell(3.0, 41), 0.07); stampsnd(w('vermisst')); hit(w('Major'), 0.10, 90)
ticks(w('1999') - 0.6, 18, 1.2, 0.04); hit(w('1999') + 0.6, 0.12, 75); pop(w('amerikanisch-vietnamesisches'))
typing(w('26.'), '26. JUNI 2003', 0.07); add(w('Nationalfriedhof'), tone(147, 3.5), 0.07); hit(w('Larry', 312), 0.09, 85)
# ---- outro
add(M(317.0), swell(3.0, 41), 0.07)
for x, a in (('Uniformen', 315), ('Namen', 316), ('Leben', 318)): k = w(x, a); add(k - 0.15, whoosh(0.5, 250, 1400), 0.05); hit(k + 0.1, 0.07, 95)
hit(w('Fronten', 318), 0.10, 75); pop(w('Kriegsheld')); pop(w('erinnern'))
add(w('Schicksale'), tone(110, 3.0), 0.06); add(w('Wie', 335), impact(), 0.12)
_lw = wavfile.read(D + '/../logo/logo_sfx.wav')[1].astype(np.float32) / 32768
sfxlib.out[int(full.LOGO_T * SR):int(full.LOGO_T * SR) + len(_lw)] += _lw[:len(sfxlib.out) - int(full.LOGO_T * SR)] * 0.9
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 1.0)[:, None]
o /= max(1.0, np.abs(o).max() / 0.9); wavfile.write(D + '/sfx_full.wav', SR, (o * 32767).astype(np.int16)); print('ok')
