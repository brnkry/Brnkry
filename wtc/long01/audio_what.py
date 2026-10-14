import json, subprocess, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
DUR = 41.2
N = int(SR * DUR)
rng = np.random.default_rng(7)

def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'lowpass', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'highpass', fs=SR, output='sos'), x)
def tt(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.standard_normal(int(SR * d))
def expenv(d, k): return np.exp(-tt(d) * k)
def fade(x, a=0.005, b=0.02):
    n = len(x); ia = min(n, int(a * SR)); ib = min(n, int(b * SR))
    if ia: x[:ia] *= np.linspace(0, 1, ia)
    if ib: x[-ib:] *= np.linspace(1, 0, ib)
    return x
def sweep_sine(f0, f1, d, curve='exp'):
    t = tt(d)
    f = f0 * (f1 / f0) ** (t / d) if curve == 'exp' else f0 + (f1 - f0) * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def norm(x, peak=1.0):
    m = np.max(np.abs(x)) + 1e-9
    return x / m * peak

# ---------------- SFX ----------------
def whoosh(d=0.6):
    x = noise(d); t = tt(d)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    # sweeping band: split into chunks
    out = np.zeros_like(x); step = int(0.02 * SR)
    for i in range(0, len(x), step):
        c = 400 + 3000 * (i / len(x))
        seg = bp(x[max(0, i - 2000):i + step], c * 0.6, min(c * 1.6, 18000))[-min(step, len(x) - i):]
        out[i:i + len(seg)] = seg
    return norm(out * env, 0.6)
def thud(): return norm(sweep_sine(140, 45, 0.35) * expenv(0.35, 11), 0.9)
def pop(): return norm((sweep_sine(900, 380, 0.09) * expenv(0.09, 40)) + 0.3 * hp(noise(0.09), 2000) * expenv(0.09, 120), 0.55)
def tick(): return norm(np.sin(2 * np.pi * 2600 * tt(0.03)) * expenv(0.03, 160), 0.35)
def ping():
    t = tt(0.6); x = np.sin(2 * np.pi * 1318.5 * t) + 0.4 * np.sin(2 * np.pi * 2637 * t)
    return norm(x * expenv(0.6, 7), 0.25)
def key():
    a = hp(noise(0.03), 1500) * expenv(0.03, 150); b = hp(noise(0.05), 900) * expenv(0.05, 90)
    x = np.zeros(int(0.2 * SR)); x[:len(a)] += a; x[int(0.09 * SR):int(0.09 * SR) + len(b)] += b
    x[int(0.09 * SR):int(0.09 * SR) + int(0.08 * SR)] += 0.5 * np.sin(2 * np.pi * 220 * tt(0.08)) * expenv(0.08, 40)
    return norm(x, 0.7)
def start():
    t = tt(0.25); x = (np.sin(2 * np.pi * 880 * t) + 0.5 * np.sin(2 * np.pi * 1320 * t)) * expenv(0.25, 12)
    return norm(x + 0.4 * thud()[:len(x)], 0.55)
def engine_off_thunk(): return norm(lp(noise(0.25), 400) * expenv(0.25, 20), 0.5)
def boot():
    out = np.zeros(int(0.5 * SR))
    for i, f in enumerate([660, 880, 1320]):
        s = int(i * 0.09 * SR); seg = np.sin(2 * np.pi * f * tt(0.14)) * expenv(0.14, 25)
        out[s:s + len(seg)] += seg
    return norm(out, 0.4)
def check():
    t = tt(0.12); return norm(np.sin(2 * np.pi * (1500 + 900 * t / 0.12) * t) * expenv(0.12, 30), 0.35)
def pump(d):
    t = tt(d); f = 95 + 60 * (t / d) ** 0.6
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
    x = lp(saw, 1400) * (0.85 + 0.15 * np.sin(2 * np.pi * 31 * t))
    x += 0.15 * bp(noise(d), 2000, 5000)
    env = np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.25)
    return norm(x * env, 0.38)
def zapon():
    x = hp(noise(0.18), 3000) * expenv(0.18, 25) + 0.5 * sweep_sine(200, 1200, 0.18) * expenv(0.18, 15)
    return norm(x, 0.5)
def hum(d):
    t = tt(d); x = sum(np.sin(2 * np.pi * 100 * k * t) / k for k in (1, 2, 3, 5)) + 0.2 * bp(noise(d), 3000, 6000)
    env = np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.3)
    return norm(x * env, 0.16)
def whir(d):
    t = tt(d); f = 180 + 800 * (t / d) ** 0.7
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    env = np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.4)
    return norm(x * env, 0.3)
def riser(d, f0=300, f1=1800):
    t = tt(d); x = sweep_sine(f0, f1, d) + 0.25 * bp(noise(d), 2000, 8000)
    return norm(x * (t / d) ** 1.5 * np.minimum(1, (d - t) / 0.05 + 0.0), 0.32)
def riserE(d):
    t = tt(d); f = 120 * (40) ** (t / d)
    ph = 2 * np.pi * np.cumsum(f) / SR; saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
    x = lp(saw, 6000) + 0.3 * hp(noise(d), 4000)
    return norm(x * (0.2 + 0.8 * (t / d) ** 2) * np.minimum(1, (d - t) / 0.03 + .0), 0.35)
def clack():
    x = 0.8 * lp(noise(0.12), 2500) * expenv(0.12, 45) + np.sin(2 * np.pi * 160 * tt(0.12)) * expenv(0.12, 30)
    return norm(x, 0.7)
def clunk():
    x = lp(noise(0.2), 900) * expenv(0.2, 25) + np.sin(2 * np.pi * 110 * tt(0.2)) * expenv(0.2, 18)
    return norm(x, 0.6)
def crank(d, t0=None):
    t = tt(d); rate = 4.3
    off = 0 if t0 is None else (t0 - 37.0)
    puls = (0.5 + 0.5 * np.cos(2 * np.pi * rate * (t + off))) ** 3
    whine = np.sin(2 * np.pi * np.cumsum(330 + 20 * np.sin(2 * np.pi * rate * t)) / SR)
    x = 0.9 * lp(noise(d), 500) * puls + 0.35 * whine * (0.6 + 0.4 * puls) + 0.5 * np.sin(2 * np.pi * 70 * t) * puls
    env = np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.12)
    return norm(x * env, 0.42)
def air(d):
    t = tt(d); x = bp(noise(d), 300, 1800) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.4 * t)) * np.sin(np.pi * t / d)
    return norm(x, 0.3)
def hiss(d):
    t = tt(d); x = hp(noise(d), 5000) * (np.abs(np.sin(2 * np.pi * 1.8 * t)) ** 2) * np.minimum(1, (d - t) / 0.2)
    return norm(x, 0.25)
def zap():
    x = hp(noise(0.25), 2500) * expenv(0.25, 18) * (1 + (rng.random(int(0.25 * SR)) > 0.97) * 3)
    return norm(x, 0.7)
def boom(v=1):
    t = tt(1.2); x = sweep_sine(110, 32, 1.2) * expenv(1.2, 4.5) + 0.6 * lp(noise(1.2), 300) * expenv(1.2, 6)
    return norm(x, 0.95)
def idle(d):
    t = tt(d); fire = 26.7
    d = max(d, 0.5); t = tt(d)
    puls = (0.5 + 0.5 * np.cos(2 * np.pi * fire * t)) ** 4
    x = lp(noise(d), 260) * puls * 2 + 0.6 * np.sin(2 * np.pi * fire * 2 * t) + 0.3 * np.sin(2 * np.pi * 53 * t)
    x = lp(x, 400)
    env = np.minimum(1, t / 0.25) * np.minimum(1, (d - t) / 0.6) * (1 + 0.5 * np.exp(-t * 3))
    x = x + 0.12 * np.sin(2 * np.pi * 0.7 * t) * x
    return norm(x * env, 0.5)
def charge(d):
    t = tt(d); f = 300 + 500 * (t / d)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 12 * t))
    return norm(x * np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.2), 0.22)
def ding():
    t = tt(1.0); x = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(1046.5, 1), (1568, .5), (2093, .3)])
    return norm(x * expenv(1.0, 5), 0.3)
def rev(d):
    t = tt(d); rpm = 900 + 5200 * np.sin(np.pi / 2 * np.clip(t / (d * 0.55), 0, 1)) - 1600 * np.clip((t - d * .6) / (d * .4), 0, 1)
    fire = rpm / 60 * 2
    ph = 2 * np.pi * np.cumsum(fire) / SR
    x = np.sign(np.sin(ph)) * 0.5 + np.sin(ph) + 0.4 * np.sin(2 * ph)
    x = lp(x, 900) + 0.3 * lp(noise(d), 1500) * (0.5 + 0.5 * np.sin(ph))
    env = np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.35)
    return norm(x * env, 0.45)
def starter(d):
    # classic "rrr-rrr-rrr": electric starter whine slowed by each compression stroke
    t = tt(d); rate = 6.2
    comp = (0.5 + 0.5 * np.cos(2 * np.pi * rate * t)) ** 4
    f = 1050 * (1 - 0.18 * comp) * np.minimum(1, 0.6 + t / 0.25)
    ph = 2 * np.pi * np.cumsum(f) / SR
    whine = np.sin(ph) + 0.45 * np.sin(2 * ph) + 0.25 * np.sin(3.01 * ph)
    whine = bp(whine, 400, 4000) * (0.55 + 0.45 * (1 - comp))
    chug = lp(noise(d), 260) * comp * 3.0 + 0.9 * np.sin(2 * np.pi * 62 * t) * comp
    grind = bp(noise(d), 1500, 5000) * 0.18 * (0.5 + 0.5 * comp)
    x = 0.55 * whine + chug + grind
    env = np.minimum(1, t / 0.04) * np.minimum(1, (d - t) / 0.05 + 0.15)
    return norm(x * env, 0.85)
def catch():
    # engine fires: a few uneven combustion pops, then a rev and settle
    out = np.zeros(int(SR * 1.3))
    for k, tp in enumerate([0.0, 0.07, 0.12, 0.17, 0.21, 0.25]):
        st = int(tp * SR); seg = lp(noise(0.06), 400) * expenv(0.06, 45) * 2 + np.sin(2 * np.pi * 55 * tt(0.06)) * expenv(0.06, 30)
        out[st:st + len(seg)] += seg
    r = rev(1.0); st = int(0.22 * SR); out[st:st + len(r)] += norm(r, 1.0) * 1.1
    return norm(out, 0.85)
def gearticks(d):
    out = np.zeros(int(SR * d)); rate = 8.0
    for k in range(int(d * rate)):
        st = int(k / rate * SR); seg = hp(noise(0.012), 3000) * expenv(0.012, 300) + 0.4 * np.sin(2 * np.pi * 1800 * tt(0.012)) * expenv(0.012, 250)
        out[st:st + len(seg)] += seg[:len(out) - st]
    return norm(out, 0.22)
def stinger():
    t = tt(2.2); notes = [146.83, 220.0, 293.66, 349.23, 440.0, 659.25]
    x = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) for f in notes)
    x = x * expenv(2.2, 1.6) * np.minimum(1, t / 0.01)
    th = thud(); x[:len(th)] += 0.8 * th
    bell = np.sin(2 * np.pi * 1760 * t) * expenv(2.2, 3) * 0.4
    return norm(x + bell, 0.6)


def run4(d):
    # engine running at a fast idle, firing pulses
    t = tt(d); fire = 30.0
    puls = (0.5 + 0.5 * np.cos(2 * np.pi * fire * t)) ** 4
    x = lp(noise(d), 300) * puls * 2 + 0.5 * np.sin(2 * np.pi * fire * 2 * t)
    x = lp(x, 500)
    env = np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.08)
    return norm(x * env, 0.45)
def thump():
    t = tt(0.3); x = np.sin(2 * np.pi * np.cumsum(90 * np.exp(-t * 6)) / SR) * expenv(0.3, 14) + 0.5 * lp(noise(0.3), 500) * expenv(0.3, 20)
    return norm(x, 0.7)
def tapestop():
    d = 0.55; t = tt(d); f = 120 * (1 - t / d) ** 2 + 5
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sign(np.sin(ph)) * 0.4 + np.sin(ph)) * (1 - t / d)
    x = lp(x, 900) + 0.3 * lp(noise(d), 600) * (1 - t / d) ** 2
    return norm(x, 0.7)
def suck(d):
    t = tt(d); x = bp(noise(d), 250, 1400) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.2
    x += 0.2 * np.sin(2 * np.pi * np.cumsum(140 + 60 * t / d) / SR) * np.sin(np.pi * t / d)
    return norm(x, 0.32)
def inject(d):
    t = tt(d); out = hp(noise(d), 4500) * np.minimum(1, t / 0.02) * np.exp(-t * 3)
    for k in range(3):
        st = int(k * 0.22 * SR); c = hp(noise(0.01), 2000) * expenv(0.01, 300); out[st:st + len(c)] += c * 2
    return norm(out, 0.35)
def squeeze(d):
    t = tt(d); f = 110 * (3.2) ** (t / d)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    x = x * (0.25 + 0.75 * (t / d) ** 1.5) + 0.15 * bp(noise(d), 800, 3000) * (t / d)
    return norm(x * np.minimum(1, (d - t) / 0.05), 0.3)
def bloom(d):
    # controlled flame: soft swelling whoosh, no bang
    t = tt(d); x = lp(noise(d), 700) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.8 + 0.4 * np.sin(2 * np.pi * 70 * t) * np.exp(-t * 2)
    return norm(x, 0.45)
def push(d):
    t = tt(d); x = sweep_sine(160, 60, d) * np.exp(-t * 2.5) + 0.4 * lp(noise(d), 400) * np.exp(-t * 3)
    return norm(x, 0.5)
def puff(d):
    t = tt(d); x = bp(noise(d), 200, 1200) * np.sin(np.pi * np.clip(t / d, 0, 1)) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t))
    return norm(x, 0.35)
def stop():
    return norm(lp(noise(0.35), 300) * expenv(0.35, 12) + sweep_sine(200, 70, 0.35) * expenv(0.35, 10), 0.4)
def knock():
    # metallic ping of detonation
    t = tt(0.35); x = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(3100, 1), (4650, .6), (6900, .35)]) * expenv(0.35, 22)
    x += hp(noise(0.35), 3000) * expenv(0.35, 120) * 0.8
    return norm(x, 0.5)
def crack():
    t = tt(0.4); x = hp(noise(0.4), 1200) * expenv(0.4, 30) + sweep_sine(220, 50, 0.4) * expenv(0.4, 12)
    return norm(x, 0.8)
def alarm():
    out = np.zeros(int(0.9 * SR))
    for k in range(3):
        st = int(k * 0.28 * SR); t = tt(0.16); seg = (np.sign(np.sin(2 * np.pi * 740 * t)) * 0.3 + np.sin(2 * np.pi * 740 * t)) * np.minimum(1, (0.16 - t) / 0.02)
        out[st:st + len(seg)] += lp(seg, 3000)
    return norm(out, 0.32)
def typing(d):
    out = np.zeros(int(SR * d))
    for k in range(int(d * 7)):
        st = int((k / 7 + 0.03 * rng.random()) * SR); c = bp(noise(0.02), 2000, 6000) * expenv(0.02, 200)
        out[st:st + len(c)] += c[:len(out) - st]
    return norm(out, 0.2)
def chime():
    out = np.zeros(int(1.4 * SR))
    for k, f in enumerate([988, 988]):
        st = int(k * 0.35 * SR); t = tt(0.9); seg = (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2 * f * t)) * expenv(0.9, 6)
        out[st:st + len(seg)] += seg
    return norm(out, 0.35)

_ch = subprocess.run(['ffmpeg','-v','error','-i','../chime.mp3','-t','2.15','-f','s16le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
_CH = np.frombuffer(_ch, np.int16).astype(np.float64) / 32768
_CH = _CH * np.minimum(1, (len(_CH) - np.arange(len(_CH))) / (0.3 * SR))
def chime_bmw(d=2.15):
    x = _CH[:int(d * SR)].copy(); n = len(x); f = int(0.35 * SR); x[-f:] *= np.linspace(1, 0, f)
    return norm(x, 0.8)
def stutter(d):
    # misfiring engine: firing pulses with missing beats
    t = tt(d); fire = 13.0
    puls = (0.5 + 0.5 * np.cos(2 * np.pi * fire * t)) ** 5
    miss = (np.floor(t * fire) % 4 == 1)
    x = lp(noise(d), 280) * puls * 2.2 * (~miss) + 0.5 * np.sin(2 * np.pi * fire * 2 * t) * (0.4 + 0.6 * (~miss))
    x = lp(x, 450)
    env = np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.3)
    return norm(x * env, 0.5)

GEN = dict(whoosh=lambda d: whoosh(max(d, .3)), thud=lambda d: thud(), pop=lambda d: pop(), tick=lambda d: tick(),
           ping=lambda d: ping(), key=lambda d: key(), start=lambda d: start(), engine_off_thunk=lambda d: engine_off_thunk(),
           boot=lambda d: boot(), check=lambda d: check(), pump=pump, zapon=lambda d: zapon(), hum=hum, whir=whir,
           riser=lambda d: riser(d), riserE=riserE, clack=lambda d: clack(), clunk=lambda d: clunk(), crank=crank,
           air=air, hiss=hiss, zap=lambda d: zap(), boom=lambda d: boom(), idle=idle, charge=charge, ding=lambda d: ding(),
           rev=rev, stinger=lambda d: stinger(), catch=lambda d: catch(), gearticks=gearticks, starter=starter, run4=run4, thump=lambda d: thump(), tapestop=lambda d: tapestop(), suck=suck, inject=inject, squeeze=squeeze, bloom=bloom, push=push, puff=puff, stop=lambda d: stop(), knock=lambda d: knock(), crack=lambda d: crack(), alarm=lambda d: alarm(), typing=typing, chime=lambda d: chime(), chime_bmw=lambda d: chime_bmw(d), stutter=stutter)

def slurp(d=0.65):
    t = tt(d); x = bp(noise(d), 1200, 7000) * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * t + 3 * np.sin(2 * np.pi * 3 * t))) ** 2
    x += 0.3 * bp(noise(d), 300, 900) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t))
    return norm(x * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.7, 0.45)
def gulp():
    t = tt(0.16); x = np.sin(2 * np.pi * np.cumsum(320 * np.exp(-t * 9) + 110) / SR) * expenv(0.16, 22)
    return norm(x + 0.3 * lp(noise(0.16), 600) * expenv(0.16, 30), 0.55)
def click():
    x = hp(noise(0.02), 2500) * expenv(0.02, 250) + 0.5 * np.sin(2 * np.pi * 1900 * tt(0.02)) * expenv(0.02, 200)
    return norm(x, 0.5)
def splash(d=0.5):
    t = tt(d); x = bp(noise(d), 800, 6000) * expenv(d, 9) * (1 + 0.6 * (rng.random(len(t)) > 0.995))
    return norm(x, 0.4)

GEN.update(slurp=slurp, gulp=lambda d: gulp(), click=lambda d: click(), splash=splash)
sfx = np.zeros(N + SR * 3)
for t0, typ, d, v in json.load(open('events_scene02_what.json')):
    x = (crank(d, t0) if typ == 'crank' else GEN[typ](d)) * v
    s = int(t0 * SR); sfx[s:s + len(x)] += x
sfx = sfx[:N]

# ---------------- MUSIC ----------------
BPM = 104; beat = 60 / BPM; bar = beat * 4
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
chords = [[53, 57, 60, 64, 67], [48, 52, 55, 59, 62], [50, 53, 57, 60, 64], [46, 50, 53, 57, 60]]  # Fmaj7, Cmaj7, Dm7, Bbmaj7
roots = [41, 36, 38, 34]
music_end = 40.9
pad = np.zeros(N); bass = np.zeros(N); arp = np.zeros(N); drums = np.zeros(N); duck = np.ones(N)
nbars = int(np.ceil(DUR / bar))
def saw(f, d, det=0.0):
    ph = (np.arange(int(SR * d)) * f * (1 + det) / SR) % 1
    return 2 * ph - 1
for b in range(nbars):
    t0 = b * bar
    if t0 > music_end: break
    ch = chords[b % 4]; s = int(t0 * SR); d = bar + 0.3
    seg = sum(saw(mtof(m), d, det) for m in ch for det in (-0.004, 0.0, 0.0045))
    env = np.minimum(1, tt(d) / 0.35) * np.minimum(1, (d - tt(d)) / 0.3)
    seg = seg * env
    e = min(N, s + len(seg)); pad[s:e] += seg[:e - s]
    # bass: 8th notes with pattern
    if b >= 2:
        for k in range(8):
            if k in (3, 7): continue
            m = roots[b % 4] + (12 if k == 6 else 0)
            st = int((t0 + k * beat / 2) * SR); dd = beat / 2 * 0.9
            x = (np.sin(2 * np.pi * mtof(m) * tt(dd)) + 0.35 * saw(mtof(m), dd)) * expenv(dd, 6)
            x = fade(x); e = max(st, min(N, st + len(x))); bass[st:e] += x[:e - st]
    # arp: 16ths from chord
    if b >= 4:
        seq = [ch[i % len(ch)] + 12 for i in (0, 2, 4, 1, 3, 4, 2, 1)]
        for k in range(16):
            m = seq[k % 8]; st = int((t0 + k * beat / 4) * SR); dd = beat / 4
            ph = (np.arange(int(SR * dd)) * mtof(m) / SR) % 1
            tri = 2 * np.abs(2 * ph - 1) - 1
            x = fade(tri * expenv(dd, 18)); e = max(st, min(N, st + len(x))); arp[st:e] += x[:e - st] * (0.8 if k % 4 == 0 else 0.5)
    # drums
    if b >= 2:
        for k in range(4):
            bt = t0 + k * beat
            if k in (0, 2) or (k == 3 and b % 2 == 1):
                kk = sweep_sine(130, 42, 0.3) * expenv(0.3, 12); st = int(bt * SR); e = max(st, min(N, st + len(kk))); drums[st:e] += kk[:e - st]
                dl = int(0.28 * SR); e2 = max(st, min(N, st + dl)); duck[st:e2] = np.minimum(duck[st:e2], 0.45 + 0.55 * np.linspace(0, 1, e2 - st) ** 0.7)
            if k in (1, 3):
                cp = bp(noise(0.18), 900, 3500) * expenv(0.18, 22); st = int(bt * SR); e = max(st, min(N, st + len(cp))); drums[st:e] += 0.45 * cp[:e - st]
            for hh in (0.5,):
                h = hp(noise(0.04), 7000) * expenv(0.04, 90); st = int((bt + hh * beat) * SR); e = max(st, min(N, st + len(h))); drums[st:e] += 0.35 * h[:e - st]
pad = lp(pad, 1100) ; pad = norm(pad, 1)
bass = lp(bass, 500); bass = norm(bass, 1); arp = bp(arp, 400, 4000); arp = norm(arp, 1); drums = norm(drums, 1)
music = 0.32 * pad * duck + 0.55 * bass * duck + 0.16 * arp + 0.5 * drums
fo = np.ones(N); ts = np.arange(N) / SR
fo *= np.clip(ts / 1.5, 0, 1); fo *= np.clip((music_end + 0.4 - ts) / 1.6, 0, 1)
music *= fo

# ---------------- VOICE + MIX ----------------
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', '02_what.mp3', '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
voice = np.frombuffer(raw, np.int16).astype(np.float64) / 32768
v = np.zeros(N); v[:min(N, len(voice))] = voice[:N]
# voice activity envelope for ducking music
win = int(0.08 * SR)
env = np.sqrt(np.convolve(v ** 2, np.ones(win) / win, 'same'))
act = np.clip(env / (np.percentile(env[env > 0.01], 50) + 1e-9), 0, 1)
act = np.convolve(act, np.ones(int(0.25 * SR)) / int(0.25 * SR), 'same')
mduck = 1 - 0.55 * np.clip(act, 0, 1)
rms = lambda x: np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2))
vr = rms(v)
music = music / rms(music) * vr * 0.32 * mduck
sfx_level = vr / (rms(sfx) + 1e-9) * 0.55
mix = v + music + sfx * sfx_level
mix = mix / np.max(np.abs(mix)) * 0.93
wavfile.write('mix_02_what.wav', SR, (mix * 32767).astype(np.int16))
wavfile.write('music_02_what.wav', SR, (norm(music, .9) * 32767).astype(np.int16))
print('ok', rms(v), rms(music), rms(sfx * sfx_level))
