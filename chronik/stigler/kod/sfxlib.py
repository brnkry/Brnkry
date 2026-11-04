import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
SR = 48000; T = 112.77
rng = np.random.default_rng(7)
out = np.zeros((int(SR * T), 2))
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
def env(n, att, dec):
    t = np.arange(n) / SR; return np.minimum(1, t / max(att, 1e-4)) * np.exp(-np.maximum(0, t - att) / dec)
def mkir(sec, dec, cut):
    n = int(SR * sec); ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / SR / dec); ir = lp(ir, cut); return ir / np.sqrt((ir ** 2).sum())
IR = mkir(2.0, 0.5, 4000); IRB = mkir(3.5, 1.1, 1200)
def verb(x, mix=0.25, ir=IR): return x + mix * fftconvolve(x, ir)[:len(x)]
def norm(x): return x / (np.abs(x).max() + 1e-9)
def add(t, x, gain=1.0, pan=0.0):
    i = int(t * SR); x = x[:max(0, len(out) - i)]
    l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    out[i:i + len(x), 0] += x * gain * l * 1.41; out[i:i + len(x), 1] += x * gain * r * 1.41
def panned(t, x, gain, p0, p1):
    i = int(t * SR); x = x[:max(0, len(out) - i)]; p = np.linspace(p0, p1, len(x))
    out[i:i + len(x), 0] += x * gain * np.sqrt(0.5 * (1 - p)) * 1.41; out[i:i + len(x), 1] += x * gain * np.sqrt(0.5 * (1 + p)) * 1.41

def whoosh(dur=0.7, lo=300, hi=1800):
    n = int(SR * dur); t = np.arange(n) / SR; x = rng.normal(0, 1, n); k = np.sin(np.pi * t / dur) ** 2
    return norm(verb((lp(x, lo) * 0.7 + bp(x, 350, hi) * k) * k, 0.3))
def impact(dur=3.5):  # deep cinematic impact, no harsh highs
    n = int(SR * dur); t = np.arange(n) / SR
    f = 32 + 55 * np.exp(-t / 0.18); sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.004, 0.9)
    body = lp(rng.normal(0, 1, n), 220) * env(n, 0.002, 0.25) * 1.4
    knock = lp(rng.normal(0, 1, n), 900) * env(n, 0.001, 0.035) * 0.6
    y = sub * 1.0 + body + knock
    y = verb(y, 0.5, IRB); return norm(lp(y, 2500))
def thud(dur=1.0, f0=90):
    n = int(SR * dur); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * (f0 + 50 * np.exp(-t / 0.03)) * t) * env(n, 0.002, 0.12) + 0.4 * lp(rng.normal(0, 1, n), 1200) * env(n, 0.001, 0.03)
    return norm(lp(verb(y, 0.25), 3000))
def ping(f=1000, dur=1.4):
    n = int(SR * dur); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * t) * env(n, 0.004, 0.12); return norm(lp(verb(y, 0.6), 2500))
def tick():
    n = int(SR * 0.06); y = bp(rng.normal(0, 1, n), 900, 3500) * env(n, 0.0005, 0.007) + 0.6 * np.sin(2 * np.pi * 160 * np.arange(n) / SR) * env(n, 0.001, 0.012)
    return norm(y)
def boom_far(dur=3.0):  # distant artillery
    n = int(SR * dur); y = lp(rng.normal(0, 1, n), 140) * env(n, 0.01, 0.5) + 0.5 * np.sin(2 * np.pi * 45 * np.arange(n) / SR) * env(n, 0.01, 0.4)
    return norm(verb(y, 0.6, IRB))
def whistle(dur=1.1, f0=1400, f1=500):
    n = int(SR * dur); t = np.arange(n) / SR; f = f0 + (f1 - f0) * (t / dur) ** 1.3
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.3) ; return norm(lp(y, 1800)) * 0.6
def engine(dur, f=80, rough=0.3, cut=700):
    n = int(SR * dur); t = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.01 * np.sin(2 * np.pi * 0.7 * t))) / SR
    y = np.sign(np.sin(ph)) * 0.5 + np.sin(ph * 2) * 0.3 + rough * rng.normal(0, 1, n)
    y = lp(y, cut) * (0.7 + 0.3 * np.sin(2 * np.pi * f / 4 * t)); fade = np.minimum(1, np.minimum(t / 0.5, (dur - t) / 0.6))
    return norm(y * fade)
def jet(dur=2.2):
    n = int(SR * dur); t = np.arange(n) / SR; x = rng.normal(0, 1, n); k = np.exp(-((t - dur * 0.45) / (dur * 0.28)) ** 2)
    y = lp(x, 700) * 0.8 + bp(x, 600, 2400) * k * 0.5
    return norm(y * k)
def static(dur, amt=1.0):
    n = int(SR * dur); y = bp(rng.normal(0, 1, n), 800, 4000) * (rng.random(n) < 0.3) * amt
    y = y * np.minimum(1, np.minimum(np.arange(n) / SR / 0.1, (dur - np.arange(n) / SR) / 0.2)); return norm(lp(y, 4500))
def rustle(dur):
    n = int(SR * dur); y = bp(rng.normal(0, 1, n), 2000, 6000) * (0.5 + 0.5 * np.abs(np.sin(np.arange(n) / SR * 23)))
    y *= np.minimum(1, np.minimum(np.arange(n) / SR / 0.3, (dur - np.arange(n) / SR) / 0.5)); return norm(y)
def metal(f=220, dur=1.6):
    n = int(SR * dur); t = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * m * t) * env(n, 0.001, 0.4 / m ** 0.5) / m for m in (1, 2.76, 5.4, 8.9))
    y += 0.4 * bp(rng.normal(0, 1, n), 1500, 5000) * env(n, 0.0005, 0.01); return norm(lp(verb(y, 0.3), 5000))
def wind(dur):
    n = int(SR * dur); t = np.arange(n) / SR; y = bp(rng.normal(0, 1, n), 200, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.4 * t))
    return norm(y * np.minimum(1, np.minimum(t / 0.5, (dur - t) / 0.6)))
def door():
    n = int(SR * 2.6); t = np.arange(n) / SR
    y = 0.9 * lp(rng.normal(0, 1, n), 300) * env(n, 0.002, 0.12) + 0.8 * np.sin(2 * np.pi * (55 + 40 * np.exp(-t / 0.05)) * t) * env(n, 0.002, 0.3)
    y += 0.5 * metal(95, 2.6)[:n] + 0.25 * metal(310, 2.6)[:n]
    k = int(0.32 * SR); y[k:k + int(0.06 * SR)] += 0.5 * tick()[:int(0.06 * SR)]
    return norm(verb(y, 0.45, IRB))
def swell(dur=3.0, f=55):
    n = int(SR * dur); t = np.arange(n) / SR; y = sum(np.sin(2 * np.pi * f * m * t) / m for m in (1, 1.5, 2))
    return norm(lp(y, 400) * np.sin(np.pi * t / dur) ** 2)

def drone4(dur, base=57, cut=480):
    y = sum(engine(dur, base * k, 0.35, cut) for k in (0.97, 1.0, 1.035, 1.06))
    return norm(y)
def heartbeat(n):
    y = np.zeros(int(SR * (n / 1.1 + 1)))
    for i in range(n):
        for off, g in ((0, 1.0), (0.24, 0.7)):
            k = int((i / 1.1 + off) * SR); h = thud(0.6, 52)
            y[k:k + len(h)] += h[:len(y) - k] * g
    return norm(lp(y, 300))
def scratch(dur=0.35):
    n = int(SR * dur); t = np.arange(n) / SR
    y = bp(rng.normal(0, 1, n), 1800, 6000) * (0.6 + 0.4 * np.abs(np.sin(t * 2 * np.pi * 9))) * np.sin(np.pi * t / dur) ** 0.5
    return norm(lp(y, 7000))
def clack():
    n = int(SR * 0.09); t = np.arange(n) / SR
    y = bp(rng.normal(0, 1, n), 700, 3000) * env(n, 0.0005, 0.012) + 0.7 * np.sin(2 * np.pi * 210 * t) * env(n, 0.001, 0.02)
    return norm(verb(y, 0.15))
def stampthump():
    y = thud(1.0, 78); n = len(y); y[:int(0.05 * SR)] += 0.4 * bp(rng.normal(0, 1, int(0.05 * SR)), 300, 2000) * env(int(0.05 * SR), 0.0005, 0.01)
    return norm(verb(y, 0.35))
def flip():
    n = int(SR * 0.25); t = np.arange(n) / SR
    y = bp(rng.normal(0, 1, n), 1200, 5000) * np.exp(-((t - 0.08) / 0.05) ** 2)
    return norm(y)
def tone(f=110, dur=3.0):
    n = int(SR * dur); t = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * m * t) * 0.6 ** i for i, m in enumerate((1, 2, 3.01))) * env(n, 0.01, 1.0)
    return norm(lp(verb(y, 0.6, IRB), 1500))
def mg_burst(n=7, rate=0.075):
    y = np.zeros(int(SR * (n * rate + 0.6)))
    for i in range(n):
        k = int(i * rate * SR); m = int(0.05 * SR)
        s = lp(rng.normal(0, 1, m), 2200) * env(m, 0.0005, 0.012) + 0.5 * np.sin(2 * np.pi * 95 * np.arange(m) / SR) * env(m, 0.001, 0.02)
        y[k:k + m] += s * rng.uniform(0.7, 1.0)
    return norm(lp(verb(y, 0.5, IRB), 2500))
def bomb(dur=3.4):
    y = np.zeros(int(SR * dur)); w = whistle(1.0, 1100, 380); y[:len(w)] += w * 0.5
    b = boom_far(dur - 0.9); y[int(0.9 * SR):int(0.9 * SR) + len(b)] += b * 1.0
    return norm(y)
def crack():  # mid-distance flak crack, rounded
    n = int(SR * 1.8); t = np.arange(n) / SR
    y = lp(rng.normal(0, 1, n), 900) * env(n, 0.002, 0.18) + 0.6 * np.sin(2 * np.pi * 60 * t) * env(n, 0.003, 0.25)
    return norm(verb(lp(y, 1600), 0.55, IRB))
