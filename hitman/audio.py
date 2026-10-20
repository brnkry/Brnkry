# Soundtrack for "First Day as a Hitman": synthesized pizzicato score + foley, timed to film.js shots.
# usage: python3 audio.py out.wav
import sys, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
SR = 48000; DUR = 61.6; rng = np.random.default_rng(5)
N = int(SR * DUR); mus = np.zeros(N); sfx = np.zeros(N); amb = np.zeros(N)
def tt(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.standard_normal(int(SR * d))
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'lowpass', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'highpass', fs=SR, output='sos'), x)
def norm(x, p=1.): return x / (np.max(np.abs(x)) + 1e-9) * p
def put(o, x, t0, g=1.):
    s = int(t0 * SR); e = min(len(o), s + len(x))
    if e > s and s >= 0: o[s:e] += x[:e - s] * g
def fade(x, a=.005, b=.02):
    n = len(x); e = np.ones(n); ia, ib = int(a * SR), int(b * SR)
    if ia: e[:ia] = np.linspace(0, 1, ia)
    if ib: e[-ib:] *= np.linspace(1, 0, ib)
    return x * e
def hz(m): return 440 * 2 ** ((m - 69) / 12)
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def mid(n):  # 'F#4'
    k = NOTE[n[0]]; i = 1
    if n[1] in '#b': k += 1 if n[1] == '#' else -1; i = 2
    return k + 12 * (int(n[i:]) + 1)

# ---------- instruments ----------
def pluck(f, d=.5, bright=.5, decay=.996):
    n = int(SR * d); L = max(2, int(SR / f)); buf = rng.uniform(-1, 1, L); buf = lp(buf, 800 + bright * 5000, 1) if L > 8 else buf
    out = np.zeros(n); b = buf.copy()
    for i in range(0, n, L):  # vectorized-ish Karplus-Strong
        seg_ = b[:min(L, n - i)]; out[i:i + len(seg_)] = seg_
        b = decay * .5 * (b + np.roll(b, -1))
    return fade(lp(out, 6000), .002, .03)
def bell(f, d=1.2, k=4):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 3) + .15 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t * 6)) * np.exp(-t * k) * np.minimum(1, t / .003)
def saw(f, d, vib=0, vr=5.5):
    t = tt(d); ph = np.cumsum(f * (1 + vib * np.sin(2 * np.pi * vr * t)) / SR); return 2 * (ph % 1) - 1
def trombone(f0, f1, d, wob=0):
    t = tt(d); f = f0 + (f1 - f0) * np.minimum(1, t / max(d * .8, .01)); ph = np.cumsum(f * (1 + .012 * np.sin(2 * np.pi * (5 + wob * 2) * t) + wob * .04 * np.sin(2 * np.pi * 6 * t)) / SR)
    x = 2 * (ph % 1) - 1; x = lp(x, 1400, 2) + .3 * bp(x, 400, 900)
    return fade(x * np.minimum(1, t / .04), .01, .12)
def woodblock(f=900): t = tt(.12); return np.sin(2 * np.pi * f * t) * np.exp(-t * 45) + .2 * bp(noise(.12), 1500, 4000) * np.exp(-t * 80)

# ---------- score ----------
def seq(o, t0, bpm, notes, inst, g=1., **kw):
    """notes: list of (beat, name|None, beats). places notes from t0."""
    sb = 60 / bpm
    for b, n, l in notes:
        if n is None: continue
        for nn in n.split('+'): put(o, inst(hz(mid(nn)), l * sb, **kw) if inst is not pluck else pluck(hz(mid(nn)), max(.25, l * sb + .2), **kw), t0 + b * sb, g)
# A: bedroom, bouncy and a bit nervous (F major), 0 - 11.4
bpmA = 132; sb = 60 / bpmA
bassA = []; chordA = []
prog = [('F2', 'A3+C4+F4'), ('C3', 'G3+C4+E4'), ('D2', 'A3+D4+F4'), ('C2', 'G3+Bb3+E4')]
for bar in range(6):
    b0, (bn, ch) = bar * 4, prog[bar % 4]
    hi = bn[:-1] + str(int(bn[-1]) + 1)
    bassA += [(b0, bn, 1), (b0 + 2, hi if bar % 2 else bn, 1)]
    chordA += [(b0 + 1, ch, .5), (b0 + 3, ch, .5)]
melA = [(0, 'F4', .5), (.5, 'A4', .5), (1, 'C5', 1), (2, 'A4', .5), (2.5, 'C5', .5), (3, 'F5', 1),
        (4, 'E5', .5), (4.5, 'D5', .5), (5, 'C5', .5), (5.5, 'G4', .5), (6, 'C5', 2),
        (8, 'D5', .5), (8.5, 'C5', .5), (9, 'A4', .5), (9.5, 'F4', .5), (10, 'D5', 1), (11, 'C#5', .5), (11.5, 'D5', .5),
        (12, 'E5', .5), (12.5, 'G5', .5), (13, 'Bb4', .5), (13.5, 'C5', .5), (14, 'E5', 2),
        (16, 'F4', .5), (16.5, 'A4', .5), (17, 'C5', 1), (18, 'A4', .5), (18.5, 'C5', .5), (19, 'F5', 1)]
seq(mus, 0, bpmA, bassA, pluck, .9, bright=.3, decay=.993)
seq(mus, 0, bpmA, chordA, pluck, .35, bright=.6, decay=.99)
seq(mus, 0, bpmA, melA, pluck, .55, bright=.8, decay=.995)
# 1d thumbs up: "ta-da" (lands at 10.0)
for i, n in enumerate(['C5', 'E5', 'G5', 'C6']): put(mus, pluck(hz(mid(n)), .9, .9), 9.85 + i * .06, .5)
# B: sneaking, D minor tiptoe, 11.4 - 21.6 and 24.3 - 35.5
def sneak(t0, t1, g=1.):
    bpm = 112; sb = 60 / bpm; bars = int((t1 - t0) / (4 * sb)) + 1
    bassP = [(0, 'D2'), (1, 'A2'), (2, 'D2'), (2.5, 'F2'), (3, 'G#2'), (3.5, 'A2')]
    melP = [[(0, 'A4'), (.5, 'Bb4'), (1, 'A4'), (2.5, 'F4'), (3, 'E4')], [(0, 'D4'), (.75, 'F4'), (1.5, 'A4'), (2, 'G#4'), (3, 'A4')],
            [(0, 'D5'), (.5, 'C#5'), (1, 'D5'), (2, 'A4'), (3, 'F4'), (3.5, 'E4')], [(0, 'D4'), (1, 'E4'), (1.5, 'F4'), (2, 'G4'), (2.5, 'G#4'), (3, 'A4')]]
    for bar in range(bars):
        b0 = t0 + bar * 4 * sb
        for b, n in bassP:
            if b0 + b * sb < t1: put(mus, pluck(hz(mid(n)), .45, .25, .99), b0 + b * sb, .95 * g)
        for b, n in melP[bar % 4]:
            if b0 + b * sb < t1 and bar > 0: put(mus, pluck(hz(mid(n)), .5, .7, .992), b0 + b * sb, .45 * g)
        for b in [.5, 1.5, 2.5, 3.5]:
            if b0 + b * sb < t1: put(mus, woodblock(1100), b0 + b * sb, .12 * g)
sneak(11.4, 21.6); sneak(24.3, 35.4, .9)
# Tony turns: stab
for n in ['D3', 'G#3', 'D4', 'F4']: put(mus, pluck(hz(mid(n)), 1.2, .9, .997), 21.58, .45)
put(mus, norm(lp(noise(.8), 300) * np.exp(-tt(.8) * 5), .5), 21.58)
# lick reaction: proud mini fanfare at 34.6
for i, n in enumerate(['A4', 'D5', 'F#5', 'A5']): put(mus, pluck(hz(mid(n)), .8, .9), 34.55 + i * .07, .4)
# woozy slide 36.3 - 37.9
t = tt(1.6); f = 900 * 2 ** (-t * 1.6) * (1 + .06 * np.sin(2 * np.pi * 7 * t)); put(mus, fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * .5 * np.minimum(1, t / .1), .01, .2), 36.3, .35)
put(mus, trombone(196, 160, 1.4, wob=1), 36.4, .25)
# 6b: plinks while Tony looks around
for tp, n in [(41.4, 'A5'), (42.0, 'F5'), (42.6, 'A5'), (43.3, 'D5')]: put(mus, pluck(hz(mid(n)), .6, .9), tp, .35)
# C: hospital music box 45.1 - 53.1
bpmC = 84; sb = 60 / bpmC
mb = ['C6', 'E6', 'G6', 'E6', 'F6', 'D6', 'B5', 'G5', 'A5', 'C6', 'E6', 'C6', 'D6', 'G5', 'C6', 'C6']
for i, n in enumerate(mb):
    tp = 45.4 + i * sb * .5
    if tp < 53.0: put(mus, bell(hz(mid(n)), 1.0, 5), tp, .18)
for i, n in enumerate(['C4', 'A3', 'F3', 'G3']): put(mus, pluck(hz(mid(n)), 1.6, .3, .997), 45.4 + i * sb * 2, .45)
# wink sparkle 50.5
for i, f in enumerate([2093, 2637, 3136]): put(mus, bell(f, .6, 7), 50.5 + i * .05, .14)
# D: tension tremolo 53.1 - 59.1
t = tt(6.0); f = hz(mid('D3')) * 2 ** (t / 6.0 * 5 / 12); ph = np.cumsum(f / SR); x = 2 * (ph % 1) - 1
x = lp(x, 1200) * (.55 + .45 * np.sign(np.sin(2 * np.pi * 9 * t))) * np.minimum(1, t / 1.5)
put(mus, fade(x, .2, .15), 53.1, .22)
# sad trombone ending
for i, (a, b, d) in enumerate([(233, 233, .38), (220, 220, .38), (208, 208, .38), (196, 185, 1.25)]): put(mus, trombone(a, b, d, wob=1 if i == 3 else 0), 59.55 + i * .4, .42)

# ---------- foley ----------
def tap(f=320, d=.1, g=1.): t = tt(d); return (np.sin(2 * np.pi * f * t) * np.exp(-t * 50) + .4 * bp(noise(d), 800, 4000) * np.exp(-t * 70)) * g
def thump(f=110, d=.25): t = tt(d); return norm(np.sin(2 * np.pi * f * (1 + 1.5 * np.exp(-t * 30)) * t) * np.exp(-t * 18) + .4 * lp(noise(d), 600) * np.exp(-t * 30))
def click(): t = tt(.05); return norm(hp(noise(.05), 2500) * np.exp(-t * 200) + np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 150))
def rustle(d): t = tt(d); return norm(bp(noise(d), 1500, 7000) * (np.abs(np.sin(2 * np.pi * 6 * t)) ** 2 + .2) * np.sin(np.pi * t / d), .5)
def whoosh(d, lo=300, hi=2500): t = tt(d); return norm(bp(noise(d), lo, hi) * np.sin(np.pi * t / d) ** 2, .6)
def squeak():
    t = tt(.32); f = 1500 + 900 * np.sin(np.pi * t / .32); return fade(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .3 * np.sin(np.pi * t / .32), .005, .02)
def slurp(): t = tt(.35); f = 300 + 500 * t / .35; return norm(bp(noise(.35), 400, 2500) * (np.sin(2 * np.pi * 18 * t) > 0) * np.sin(np.pi * t / .35) + .3 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / .35), .5)
def splat(): t = tt(.6); return norm(lp(noise(.6), 900) * np.exp(-t * 9) + .6 * np.sin(2 * np.pi * 70 * t) * np.exp(-t * 12) + .4 * bp(noise(.6), 1500, 5000) * np.exp(-t * 20), .9)
def clink(f=3200): return norm(bell(f, .4, 14) + .5 * bell(f * 1.5, .4, 18), .4)
def pop(): t = tt(.12); return norm(np.sin(2 * np.pi * np.cumsum(500 + 700 * np.exp(-t * 40)) / SR) * np.exp(-t * 35), .5)
def sprinkle(d):
    o = np.zeros(int(SR * d))
    for i in range(int(d * 60)): put(o, hp(noise(.01), 4000) * rng.uniform(.2, 1), rng.uniform(0, d - .02))
    return norm(o, .25)
def scrape(d): t = tt(d); return norm(bp(noise(d), 600, 2500) * (.6 + .4 * np.sin(2 * np.pi * 23 * t)) * np.sin(np.pi * t / d), .35)
def gulp(): t = tt(.22); return norm(np.sin(2 * np.pi * np.cumsum(180 + 260 * np.exp(-t * 18)) / SR) * np.exp(-t * 14), .6)
def plip(): t = tt(.1); return norm(np.sin(2 * np.pi * np.cumsum(1400 + 1800 * t / .1) / SR) * np.exp(-t * 40), .35)
def blip(): t = tt(.07); return norm(np.sin(2 * np.pi * 1300 * t) * np.exp(-t * 60), .25)
def breath(d=.6): t = tt(d); return norm(bp(noise(d), 300, 2500) * np.sin(np.pi * t / d) ** 1.5, .3)
def beep(f=1050, d=.11): t = tt(d); return fade(np.sin(2 * np.pi * f * t) * .5, .003, .02)
def mmm(d): t = tt(d); x = saw(118, d, .02); return norm(bp(x, 150, 700) * np.sin(np.pi * t / d), .35)
def chirp(): t = tt(.18); return norm(np.sin(2 * np.pi * np.cumsum(3500 + 1500 * np.sin(2 * np.pi * 14 * t)) / SR) * np.sin(np.pi * t / .18), .2)
def cricket():
    o = np.zeros(int(SR * .5))
    for k in range(3): put(o, np.sin(2 * np.pi * 4300 * tt(.04)) * np.sin(np.pi * tt(.04) / .04), k * .055)
    return o * .25

E = [  # (time, sound, gain)
    (3.1, rustle(.35), .5), (4.8, thump(160, .2), .45), (4.55, tap(500), .3), (5.75, thump(200, .15), .3),
    (6.15, tap(700, .08), .3), (7.08, squeak(), .5), (8.35, thump(220, .15), .3),
    (9.3, thump(90, .3), .75), (9.5, click(), .5), (9.7, click(), .5), (10.6, plip(), .6),
    (14.7, rustle(.5), .5), (16.3, rustle(.3), .45), (15.1, blip(), 1), (15.6, blip(), 1), (16.1, blip(), 1),
    (21.6, whoosh(.3, 500, 3000), .5), (23.85, whoosh(.4, 400, 2500), .4), (24.4, breath(.8), .7),
    (25.3, pop(), .6), (26.1, sprinkle(1.3), .9), (29.45, slurp() * .5, .5), (30.0, plip(), .5),
    (31.2, blip(), 1), (31.6, blip(), 1), (32.2, blip(), 1), (32.8, slurp(), .7), (33.5, slurp(), .7), (34.15, slurp(), .7),
    (38.55, whoosh(.65, 200, 1500), .7), (39.15, splat(), 1.0), (39.2, clink(2900), .35),
    (43.3, clink(2600), .35), (43.35, scrape(1.0), .7),
    (47.7, scrape(1.4), .6), (53.5, plip(), .6), (53.9, scrape(1.2), .6),
    (55.85, gulp(), .8), (56.15, gulp(), .8), (56.45, gulp(), .8), (57.0, clink(2600), .3),
    (59.1, whoosh(.3, 200, 1200), .6), (59.38, thump(80, .3), .7),
]
for tp, x, g in E: put(sfx, x, tp, g)
for k in range(8): put(sfx, tap(260, .08), 18.1 + k * .4, .35)                      # tiptoe steps
for k in range(int(1.2 * 2.2)): put(sfx, clink(3600 + k * 50), 28.15 + k / 2.2, .25)  # stirring
for tp in np.arange(11.6, 45.0, 2.4): put(sfx, clink(3000), tp + 1.0, .12)           # Tony's fork on the plate
for tp in [12.2, 15.2, 19.8, 26.0]: put(sfx, mmm(.7), tp, .5)                          # Tony "mmm"
for tp in [12.8, 17.0, 20.3, 27.4, 33.1, 41.0]: put(amb, chirp(), tp, .6)
for k in range(9): put(amb, cricket(), 22.0 + k * .26, .4)
# ECG beeps: shot 7 (45.1-53.1) steady 72 bpm; shot 8 rising, frantic, flatline, recovery
tb = 45.1 + .3 * 60 / 72
while tb < 53.1: put(sfx, beep(), tb, .18); tb += 60 / 72
tb = 53.1
while tb < 59.1: bpm = 72 + min(1, (tb - 53.1) / 2) * 60; put(sfx, beep(), tb + .1, .2); tb += 60 / bpm
for k in range(4): put(sfx, beep(), 59.1 + k * .06, .2)
put(sfx, beep(1050, .65), 59.35, .25)
# ambience beds
def bed(t0, t1, kind):
    d = t1 - t0; t = tt(d); env_ = np.minimum(1, np.minimum(t / .15, (d - t) / .15))
    if kind == 'room': x = lp(noise(d), 250) * .05
    if kind == 'cafe': x = bp(noise(d), 250, 1800) * (.5 + .5 * lp(np.abs(noise(d)), 3)) * .05 + lp(noise(d), 150) * .03
    if kind == 'hosp': x = lp(noise(d), 300) * .04 + np.sin(2 * np.pi * 60 * t) * .006
    put(amb, x * env_, t0)
bed(0, 11.4, 'room'); bed(11.4, 45.1, 'cafe'); bed(45.1, 61.6, 'hosp')

mus = lp(mus, 9000) * .5; mix = mus / (np.max(np.abs(mus)) + 1e-9) * .45 + sfx / (np.max(np.abs(sfx)) + 1e-9) * .8 + amb * 2.5
mix = np.tanh(mix * 1.1) * .9
st = np.stack([mix, np.concatenate([np.zeros(int(SR * .0007)), mix[:-int(SR * .0007)]])], 1)
wavfile.write(sys.argv[1], SR, (st * 32767).astype(np.int16))
print('ok', DUR)
