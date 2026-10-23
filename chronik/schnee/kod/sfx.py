import sys, json
sys.path.insert(0, sys.argv[1])
from sfxlib import *
WD = json.load(open(sys.argv[2]))
def wt(s, after=0.0):
    for w, a, b in WD:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a
    raise KeyError(s)
def fio(x, a=0.6, b=0.8):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def typing(t0, n, step=0.055, g=0.07):
    for i in range(n): add(t0 + i * step + rng.uniform(-0.006, 0.006), clack(), g * rng.uniform(0.75, 1.0), rng.uniform(-0.2, 0.2))
def hit(t0, g=0.12, f=80): add(t0, thud(0.9, f), g)
def air(t0, g=0.05): add(t0, whoosh(0.5, 200, 1200), g)

# beds
add(0.0, fio(waves(T), 2.0, 2.0), 0.05, 0.0)
add(0.0, fio(under(7.2), 0.05, 1.0), 0.16); add(0.0, swell(3.0, 41), 0.16)
add(0.05, sonar_ping(), 0.07); add(3.0, sonar_ping(), 0.05)
add(0.05, impact(), 0.20); add(wt('britischen') - 0.1, whoosh(0.6, 200, 900), 0.05)
add(wt('Befehl') - 0.05, thud(0.9, 70), 0.14); add(wt('Adalbert') - 0.1, impact(), 0.26)
# early life
air(6.8); hit(wt('1913'), 0.10, 90); add(10.8, whoosh(0.6, 150, 700), 0.05); hit(wt('1934'), 0.10, 90)
add(14.5, whoosh(0.8, 200, 900), 0.07, -0.3); hit(wt('Otto'), 0.11, 85); air(wt('U-23'))
# U-201
add(20.7, fio(engine(5.8, 46, 0.4, 420), 0.8, 1.0), 0.08, -0.2); add(20.7, fio(waves(5.8), 0.5, 0.8), 0.05)
hit(wt('U-201.'), 0.14, 70)
add(wt('Schneemann') - 0.05, whoosh(0.6, 300, 1500), 0.07); hit(wt('Schneemann') + 0.3, 0.10, 100); air(wt('Anspielung'))
add(31.4, whoosh(0.8, 200, 900), 0.07, 0.3); air(wt('Bootswappen'))
for i in range(12): add(wt('21', 35) + i * 0.1, tick(), 0.05)
hit(wt('21', 35) + 1.2, 0.12, 75)
# staff
add(39.4, rustle(0.7), 0.06); hit(wt('Dönitz'), 0.12, 80); add(wt('Geleitzüge') - 0.3, whoosh(0.5, 200, 1200), 0.05)
# Type XXI
add(46.2, fio(emotor(10.5), 1.2, 1.0), 0.05); add(46.2, fio(under(10.5), 1.2, 1.0), 0.06)
add(wt('völlig') - 0.1, swell(2.5, 46), 0.10); hit(wt('Typ'), 0.15, 65); air(wt('tagelang'))
add(wt('schneller') - 0.2, whoosh(0.8, 300, 1500), 0.06); add(wt('schneller') + 0.6, whoosh(0.8, 300, 1500), 0.05)
hit(wt('U-2511,'), 0.15, 68); air(wt('erste'))
# Bergen harbour
add(62.3, fio(wind(5.6), 0.8, 1.0), 0.06); add(62.3, fio(waves(5.6), 0.6, 0.8), 0.06)
hit(wt('Bergen', 62), 0.11, 85); add(wt('April'), metal(160, 1.6), 0.05)
# order
add(67.4, whoosh(0.6, 200, 900), 0.06); typing(wt('Befehl', 67) + 0.3, 33, 0.055, 0.08)
# Norfolk
add(72.5, fio(screws(6.0), 1.0, 1.0), 0.07, 0.5); add(72.5, fio(under(6.0), 1.0, 0.6), 0.08)
hit(wt('Norfolk'), 0.12, 75)
# closing in
add(78.1, fio(under(5.6), 0.6, 0.8), 0.14); add(78.1, fio(screws(5.6, 4.2), 0.8, 0.6), 0.09, 0.2)
for k in range(4): add(wt('glitt') + k * 1.6, sonar_ping(760), 0.05)
add(wt('glitt') + 0.8, heartbeat(5), 0.24); add(79.5, hull_creak(), 0.06, -0.4)
add(wt('Meter', 80) + 0.2, thud(1.2, 58), 0.16)
# feint
add(83.1, whoosh(0.7, 200, 900), 0.06); hit(wt('Übungsangriff'), 0.12, 75); add(wt('ohne'), thud(0.8, 100), 0.12)
add(wt('zog'), fio(screws(2.0, 3.0), 0.2, 1.4), 0.05, -0.6)
# doubt
add(88.3, swell(3.0, 43), 0.09); add(wt('Historiker'), stampthump(), 0.28)
# surrender, after the war
add(95.3, whoosh(0.8, 200, 900), 0.07, -0.3); hit(wt('9.'), 0.13, 70); air(wt('übergab'))
add(100.0, fio(waves(7.0), 1.0, 1.0), 0.08); add(100.0, fio(wind(7.0), 1.0, 1.0), 0.04)
air(wt('Elba')); air(wt('Verband'))
add(wt('1982') - 0.1, tone(65, 3.0), 0.12); hit(wt('Kanntet'), 0.10, 90); hit(wt('Schreibt'), 0.09, 100)
out /= max(1.0, np.abs(out).max() / 0.95)
wavfile.write(sys.argv[3], SR, (out * 32767).astype(np.int16))
x = np.abs(out).mean(1); win = SR // 2
print('quiet', [i * 0.5 for i in range(len(x) // win) if 20 * np.log10(np.sqrt((x[i * win:(i + 1) * win] ** 2).mean()) + 1e-9) < -46])
