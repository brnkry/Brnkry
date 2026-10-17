# Synthesized no-start sounds for long 04. usage: python3 crank_sounds.py  -> demo_sounds.wav + each sound as sfx_*.wav
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
SR = 44100; rng = np.random.default_rng(3)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'lowpass', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'highpass', fs=SR, output='sos'), x)
def tt(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.standard_normal(int(SR * d))
def env(d, k): return np.exp(-tt(d) * k)
def norm(x, p=1.0): return x / (np.max(np.abs(x)) + 1e-9) * p
def put(out, x, t):
    s = int(t * SR); e = min(len(out), s + len(x)); out[s:e] += x[:e - s]
# small engine-bay / cabin room so it doesn't sound like a dry synth
IR = noise(0.18) * env(0.18, 30); IR[0] = 6; IR = lp(IR, 3500)
def room(x, wet=.35): y = fftconvolve(x, IR)[:len(x)]; return norm(x, 1) * (1 - wet) + norm(y, 1) * wet

def key_turn():
    out = np.zeros(int(SR * .45))
    for t0, a in [(0, .5), (.035, .35), (.16, 1.0), (.2, .4)]:   # keys jingle + ignition detent
        c = bp(noise(.05), 2500, 9000) * env(.05, 90) * a; put(out, c, t0)
    put(out, .6 * np.sin(2*np.pi*180*tt(.06)) * env(.06, 60), .16)
    return out
def solenoid(heavy=1.0):
    # metallic plunger snap: sharp transient + two resonances + low body thunk
    d = .09; t = tt(d)
    x = bp(noise(d), 1500, 7000) * env(d, 160) * 1.2
    x += (np.sin(2*np.pi*1850*t) * .5 + np.sin(2*np.pi*3300*t) * .3) * env(d, 70)
    x += heavy * (np.sin(2*np.pi*95*t) * 1.4 + lp(noise(d), 300) * .8) * env(d, 45)
    return x
def rapid_click(d=2.2):
    out = np.zeros(int(SR * d)); t = 0.0
    while t < d - .1:
        put(out, solenoid(.35) * (.75 + .25 * rng.random()), t)
        # dash relay buzz between clicks
        put(out, .08 * bp(noise(.03), 300, 1200) * env(.03, 60), t + .03)
        t += 1 / 13.0 * (0.85 + 0.3 * rng.random())
    return out
def single_click(): out = np.zeros(int(SR * 1.2)); put(out, solenoid(1.4) * 1.3, .0); return out
def starter(d, rate, pitch, drag):
    # starter whine + compression pulses (slower rate = weaker battery)
    t = tt(d); r = rate * (1 - drag * t / d)
    ph_c = 2*np.pi*np.cumsum(r) / SR; comp = (0.5 + 0.5 * np.cos(ph_c)) ** 4
    f = pitch * (1 - .22 * comp) * np.minimum(1, .55 + t / .2)
    ph = 2*np.pi*np.cumsum(f) / SR
    whine = bp(np.sin(ph) + .45*np.sin(2*ph) + .25*np.sin(3.01*ph), 350, 4000) * (.5 + .5 * (1 - comp))
    chug = lp(noise(d), 250) * comp * 3.2 + np.sin(2*np.pi*58*t) * comp
    grind = bp(noise(d), 1500, 5000) * .15
    e = np.minimum(1, t / .03) * np.minimum(1, (d - t) / .08)
    x = (.5 * whine + chug + grind) * e
    out = np.zeros(int(SR * (d + .3))); put(out, solenoid(1.0), 0); put(out, x, .03)
    put(out, solenoid(.6) * .6, d + .02)   # release clack
    return out
def silence(): return np.zeros(int(SR * 1.2))

S = {'rapid_click': rapid_click(), 'single_click': single_click(), 'silence': silence(),
     'slow_crank': starter(3.0, 2.6, 640, .35), 'crank_no_start': starter(3.2, 5.6, 980, 0)}
order = ['rapid_click', 'single_click', 'silence', 'slow_crank', 'crank_no_start']
demo = []
for k in order:
    x = norm(room(S[k]), .85) if k != 'silence' else S[k]
    wavfile.write(f'sfx_{k}.wav', SR, (x * 32767).astype(np.int16))
    demo += [norm(key_turn(), .5), np.zeros(int(SR * .05)), x, np.zeros(int(SR * 1.3))]
demo = np.concatenate(demo); wavfile.write('demo_sounds.wav', SR, (demo * .9 * 32767).astype(np.int16))
print('demo', len(demo) / SR)
