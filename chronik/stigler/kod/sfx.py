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
def typing(t0, n, step=0.06, g=0.075):
    for i in range(n): add(t0 + i * step + rng.uniform(-0.008, 0.008), clack(), g * rng.uniform(0.75, 1.0), rng.uniform(-0.2, 0.2))
def pen(t0, dur, g=0.06): add(t0, scratch(dur), g)
def paper_in(t0, g=0.07): add(t0, rustle(0.5), g); add(t0 + 0.35, thud(0.6, 120), g * 1.2)
def soft(t0, g=0.06): add(t0, whoosh(0.5, 200, 1200), g)

# ---- S1 hook (0 to 6.4) ----
add(0.0, fadeio(drone4(5.8), 1.2, 0.35), 0.11); add(0.0, swell(3.0, 41), 0.18)
add(0.24, thud(1.2, 62), 0.14); add(wt('Jagdflieger'), whoosh(0.5, 200, 1200), 0.05)
add(2.17, thud(1.2, 58), 0.12); add(wt('amerikanischen'), whoosh(0.5, 200, 1200), 0.05)
add(wt('direkt'), whoosh(0.5, 200, 1200), 0.05)
add(wt('schoss') - 0.03, impact(), 0.34)
# ---- S2 split screen names ----
add(6.35, whoosh(0.9, 150, 800), 0.08)
typing(wt('Geschichte'), 16, 0.035, 0.06)
paper_in(wt('Franz') - 0.35, 0.09); paper_in(wt('Charlie') - 0.35, 0.09)
add(wt('Charlie') + 0.2, thud(0.8, 90), 0.10)
# ---- S3 calendar ----
t20 = wt('20.')
for i in range(4): add(t20 - 0.08 - i * 0.12, flip(), 0.12)
add(t20 + 0.05, thud(0.9, 75), 0.12)
add(wt('Dezember') - 0.1, stampthump(), 0.12)
typing(wt('1943'), 4, 0.09, 0.09)
# ---- S4 Brown / S5 crew ----
add(15.3, whoosh(0.8, 150, 700), 0.08); add(wt('21-j'), thud(0.8, 80), 0.10)
add(wt('Leutnant'), whoosh(0.5, 300, 1500), 0.06); add(wt('ersten'), thud(0.8, 85), 0.10)
add(19.45, whoosh(0.7, 200, 900), 0.08, 0.3); add(wt('Kommandant') - 0.2, scratch(0.6), 0.05)
add(wt('Kommandant'), thud(0.7, 95), 0.12); add(wt('namens'), whoosh(0.6, 200, 1200), 0.06)
panned(19.6, fadeio(drone4(4.2, 50, 360), 1.5, 0.6), 0.05, -0.3, 0.3)   # engines warming behind the crew photo
# ---- S6 map: flight to Bremen and the battle ----
add(23.5, fadeio(drone4(5.4), 0.6, 0.8), 0.15)
add(wt('Bremen'), thud(0.9, 80), 0.10)
r = np.random.default_rng(4)
for i in range(10): add(wt('Flak') + i * 0.28, crack() if i % 2 else boom_far(2.4), 0.13, r.uniform(-0.7, 0.7))
for i, tb in enumerate((25.9, 26.6, 27.3, 28.0)): add(tb, bomb(), 0.09, r.uniform(-0.5, 0.5))
panned(wt('Jäger'), engine(2.2, 115, 0.3, 900), 0.10, 0.8, -0.2)
add(wt('Jäger') + 0.6, mg_burst(8), 0.07, 0.4); add(wt('Jäger') + 1.3, mg_burst(6), 0.06, -0.3)
add(wt('schwer'), metal(180, 1.6), 0.09)
# ---- S7 damage callouts ----
add(28.5, fadeio(drone4(5.8, 52, 380) * np.linspace(1, 0.4, int(SR * 5.8)), 0.4, 0.8), 0.08)
for k in ('Motoren', 'Bugkanzel', 'Leitwerk'):
    add(wt(k), thud(1.0, 72), 0.16); add(wt(k) + 0.05, metal(140, 1.4), 0.05); add(wt(k) + 0.55, whoosh(0.4, 300, 1500), 0.04)
add(29.6, crack(), 0.06, 0.6); add(31.6, crack(), 0.05, -0.5)
# ---- S8 crew ledger ----
add(34.0, whoosh(0.6, 200, 900), 0.06, -0.3)
typing(34.15, 18, 0.045, 0.07); pen(34.6, 0.5, 0.05)
typing(wt('Hugh') - 0.1, 14, 0.05, 0.08); typing(wt('Heckschütze') + 0.1, 11, 0.045, 0.06)
pen(wt('tot'), 0.35, 0.09); add(wt('tot') + 0.1, stampthump(), 0.26)
for i, n in enumerate((7, 9, 9, 5)): typing(wt('mehrere') + i * 0.25, n, 0.045, 0.06)
pen(wt('verwundet'), 0.5, 0.07); pen(wt('verwundet') + 0.3, 0.5, 0.06)
# ---- S9 Bf 109 ----
panned(39.5, fadeio(engine(7.0, 112, 0.28, 950), 0.6, 1.0), 0.11, 0.7, -0.7)
add(wt('Oberleutnant'), whoosh(0.5, 300, 1500), 0.06); add(wt('Jagdgeschwader'), thud(0.8, 85), 0.10)
add(wt('Bf'), thud(0.7, 90), 0.11)
# ---- S10 tally ----
pen(wt('Ein', 46) - 0.1, 0.3, 0.10); pen(wt('weiterer') - 0.1, 0.3, 0.10); pen(wt('Abschuss'), 0.35, 0.07)
typing(46.3, 12, 0.03, 0.05)
add(wt('Ritterkreuz'), tone(73, 3.0), 0.16); add(wt('Ritterkreuz'), thud(1.2, 60), 0.14)
add(wt('gebracht'), heartbeat(5), 0.30)
# ---- S11 wreck / S12 Roedel ----
add(50.1, wind(4.0), 0.05); add(wt('Verwundeten'), whoosh(0.5, 200, 1200), 0.05)
add(54.15, whoosh(0.7, 200, 900), 0.07, 0.3); add(wt('Kommandeur'), whoosh(0.4, 300, 1500), 0.05); add(wt('Gustav'), thud(0.8, 90), 0.12)
# ---- S13 quote: a pen writes each word ----
add(58.25, rustle(0.5), 0.06)
after = 58.3
for k in ('wer', 'auf', 'einen', 'Mann', 'am', 'Fallschirm', 'schieße', 'den', 'erschieße', 'er', 'selbst'):
    tk = wt(k, after); after = tk + 0.01; pen(tk - 0.03, 0.22, 0.045)
pen(wt('selbst') + 0.2, 0.5, 0.07); add(wt('selbst') + 0.35, thud(1.0, 66), 0.12)
# ---- S14 map Sweden: both aircraft audible ----
add(62.2, fadeio(drone4(10.4, 54, 420), 1.0, 1.2), 0.13); add(62.2, fadeio(engine(10.4, 108, 0.28, 850), 1.0, 1.2), 0.06, 0.3)
add(wt('Zeichen'), whoosh(0.8, 300, 1400), 0.05); pen(wt('Zeichen') + 0.1, 0.8, 0.04)
add(wt('Schweden') + 0.4, thud(0.8, 85), 0.10); add(wt('verstand'), swell(2.5, 46), 0.10)
add(67.35, whoosh(0.7, 200, 900), 0.07, -0.3)
for tf in (68.0, 69.4, 70.8): add(tf, boom_far(2.0), 0.04, rng.uniform(-0.6, 0.6))   # distant flak that falls silent
# ---- S16 salute and landing ----
add(72.2, fadeio(drone4(6.8, 55, 420), 0.6, 1.5), 0.13)
add(wt('salutierte'), tone(98, 3.5), 0.15); add(wt('salutierte'), thud(1.4, 58), 0.12)
panned(wt('drehte'), fadeio(engine(2.6, 120, 0.25, 1000), 0.2, 1.4), 0.11, 0.0, 0.9)
add(wt('landete'), wind(2.2), 0.06); add(wt('Seething'), thud(0.9, 70), 0.14); add(wt('England'), whoosh(0.5, 200, 1200), 0.05)
# ---- S17 report ----
add(78.85, rustle(0.6), 0.08); add(79.2, thud(0.6, 120), 0.08)
typing(wt('meldete'), 7, 0.06, 0.09)
add(wt('nie,'), scratch(0.35), 0.12); add(wt('nie,') + 0.1, whoosh(0.4, 300, 1500), 0.05)
add(wt('Kriegsgericht'), stampthump(), 0.32)
# ---- S18 Canada ----
add(83.6, whoosh(1.0, 150, 700), 0.07); add(wt('1953'), swell(2.6, 44), 0.12); add(wt('1953'), thud(1.0, 66), 0.12)
add(84.2, fadeio(wind(3.6), 0.8, 1.0), 0.05); pen(84.0, 2.2, 0.03)
add(wt('Kanada'), thud(0.8, 88), 0.10)
# ---- S19 notice ----
add(87.75, rustle(0.6), 0.08); add(88.1, thud(0.6, 120), 0.08)
typing(wt('suchte'), 7, 0.05, 0.09); add(wt('1986'), stampthump(), 0.16)
typing(wt('unbekannten'), 18, 0.035, 0.07)
# ---- S20 reunion ----
add(92.4, rustle(0.5), 0.06); add(wt('1990'), swell(3.0, 49), 0.12); add(wt('1990'), thud(0.9, 80), 0.10)
add(wt('meldete', 93), whoosh(0.5, 200, 1200), 0.05); pen(wt('beiden'), 0.7, 0.05)
add(wt('enge'), tone(87, 3.5), 0.12)
# ---- S21 2008 strip ----
for i in range(12): add(99.2 + i * 0.05, tick(), 0.05)
add(wt('2008'), thud(0.9, 80), 0.10)
add(wt('März'), tone(65, 3.0), 0.12); pen(wt('März') + 0.05, 0.4, 0.05); add(wt('92'), whoosh(0.4, 300, 1500), 0.04)
add(wt('November'), tone(65, 3.0), 0.12); pen(wt('November') + 0.05, 0.4, 0.05); add(wt('86.'), whoosh(0.4, 300, 1500), 0.04)
# ---- S22 CTA ----
add(109.0, rustle(0.5), 0.06); add(wt('Kanntet'), thud(0.8, 90), 0.09); add(wt('Schreibt'), thud(0.7, 100), 0.09)
# ---- fills for quiet stretches ----
add(0.0, fadeio(lp(rng.normal(0, 1, int(SR * T)), 380), 2.0, 2.0) * 0.18, 0.25)          # faint room tone under everything
for i in range(8): add(11.9 + i * 0.5, tick(), 0.05)                                    # desk clock under the calendar
add(15.4, fadeio(wind(4.2), 1.0, 1.0), 0.05); add(15.6, fadeio(engine(4.0, 44, 0.4, 260), 1.2, 1.0), 0.04, -0.4)   # airfield, engines idling far away
pen(35.4, 0.6, 0.04); add(38.9, whoosh(0.6, 200, 900), 0.05)
pen(47.9, 0.3, 0.05)
add(54.9, swell(3.2, 43), 0.10); add(57.2, whoosh(0.5, 300, 1500), 0.04)
pen(61.4, 0.6, 0.04)
for i in range(4): pen(79.9 + i * 0.42, 0.35, 0.05)                                   # pen running over the report lines
typing(89.8, 26, 0.085, 0.05)                                                           # body text of the notice
add(95.4, swell(3.4, 52), 0.10); add(97.3, whoosh(0.6, 200, 900), 0.04)
add(104.6, swell(3.0, 43), 0.09)
add(109.9, swell(2.6, 49), 0.08)
out /= max(1.0, np.abs(out).max() / 0.95)
wavfile.write(sys.argv[3], SR, (out * 32767).astype(np.int16))
# report quiet stretches
x = np.abs(out).mean(1); win = SR // 2
q = [i * 0.5 for i in range(len(x) // win) if 20 * np.log10(np.sqrt((x[i * win:(i + 1) * win] ** 2).mean()) + 1e-9) < -46]
print('quiet', q)
