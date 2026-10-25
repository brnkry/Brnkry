# sound for the Udet / Ju 87 short: the original dive sound in the intro (heard alone in the pause), engines on the film,
# the siren rising under the drawing, the bomb, transitions and the stamp
import sys
sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, sfxlib
from sfxlib import *
from scipy.io import wavfile as wf
import jshort as V
T = V.T; ws = V.ws
sfxlib.out = np.zeros((int(SR * T), 2))
def fio(x, a=0.3, b=0.6):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))[:, None] if x.ndim == 2 else x * np.minimum(1, np.minimum(t / a, (n / SR - t) / b))
def wav(p): sr, x = wf.read(p); return x.astype(np.float64) / 32768
def addst(t0, x, g):
    i = int(t0 * SR); n = min(len(x), len(sfxlib.out) - i); sfxlib.out[i:i + n] += x[:n] * g
def hit(t0, g=0.10, f=85): add(t0, thud(0.9, f), g)
# intro: the old film's own sound; under the first words, then alone and full in the pause before the name
A = wav(V.B + 'introa.wav'); tt = np.arange(len(A)) / SR; cut, G = [float(v) for v in open(V.B + 'gap.txt').read().split()]
gain = np.where(tt < cut - 0.1, 0.42, np.minimum(1.0, 0.42 + (tt - cut + 0.1) / 0.6 * 0.58)); gain *= np.clip((V.ws('Sein', 11) + 0.35 - tt) / 0.45, 0, 1)
gain = np.where(tt < cut - 0.1, 0.32, np.minimum(1.0, 0.32 + (tt - cut + 0.1) / 0.6 * 0.68)); gain *= np.clip((V.ws('Sein', 11) + 0.35 - tt) / 0.45, 0, 1)
I_ = A * gain[:, None]; I_ /= max(1.0, np.abs(I_).max() / 0.95); wavfile.write(sys.argv[1] + '/intro_trk.wav', SR, (I_ * 32767).astype(np.int16))   # own track in the mix
for s, fn, tr in V.ANCH[2:]: add(s - 0.08, whoosh(0.5, 200, 1400), 0.045, rng.uniform(-0.3, 0.3))
hit(ws('Ernst'), 0.09, 75); add(ws('Ernst'), swell(2.2, 52), 0.05)
add(ws('62') - 0.05, mg_burst(5), 0.04); hit(ws('62'), 0.08, 80)
hit(ws('Manfred'), 0.07, 80)
add(ws('In', 21), fio(engine(2.5, 85, 0.35, 800), 0.3, 0.6), 0.05); add(ws('In', 21), fio(rustle(2.5), 0.3, 0.5), 0.05)   # the crowd
hit(ws('Sturzkampfbomber', 22), 0.08, 75)
add(ws('die', 23.5), fio(engine(3.0, 110, 0.3, 1100), 0.2, 0.6), 0.07); add(ws('die', 23.5) + 0.4, whistle(1.8, 1300, 700), 0.03)
hit(ws('Göring'), 0.08, 70); hit(ws('1933'), 0.07, 80)
add(ws('brachte'), fio(engine(1.8, 80, 0.3, 700), 0.2, 0.5), 0.06)
add(ws('Viele'), fio(engine(5.3, 95, 0.3, 900), 0.4, 0.8), 0.06); add(ws('doch', 36) - 0.05, scratch(0.4), 0.06)
add(ws('Er', 38.5), fio(engine(5.0, 70, 0.35, 650), 0.4, 0.8), 0.09); hit(ws('Junkers', 40), 0.09, 70); hit(ws('Stuka', 42), 0.11, 60)
# the drawing: the siren winds up with the dive
S_ = wav(V.B + 'sirena.wav'); ta = ws('An', 43)
add(ta, swell(2.0, 50), 0.04)
for k in range(5): add(ta + 0.2 + k * 0.12, tick(), 0.03)
tw, tf, tl, tj = ws('Fahrtwind'), ws('je', 47), ws('lauter', 49), ws('Jericho')
add(tw, fio(wind(7.4), 0.5, 1.0), 0.05)
n = int(SR * (ws('In', 54) + 0.2 - tf)); xs = S_[:n]; t_ = np.arange(len(xs)) / SR
g = np.clip(t_ / 1.6, 0, 1) * 0.35 + np.clip((t_ - (tl - tf)) / 0.8, 0, 1) * 0.65; g *= np.clip((len(xs) / SR - t_) / 0.5, 0, 1)
addst(tf, xs * g[:, None], 0.30)
hit(tj, 0.10, 60)
add(ws('In', 54), fio(engine(3.0, 75, 0.35, 700), 0.2, 0.6), 0.08); hit(ws('Polen', 54), 0.07, 80); hit(ws('Frankreich', 54), 0.07, 80)
add(ws('Soldaten'), fio(engine(2.5, 120, 0.3, 1200), 0.2, 0.5), 0.07); add(ws('Soldaten') + 0.2, whistle(1.6, 1500, 600), 0.03)
add(ws('Bombe') - 0.5, whistle(1.0, 1300, 500), 0.04); add(ws('fiel') + 0.25, bomb(3.0), 0.12)
xs = S_[int(SR * 4.0):int(SR * 4.0) + int(SR * (ws('später', 63) - ws('Doch', 61)))]; t_ = np.arange(len(xs)) / SR
addst(ws('Doch', 61), xs * (np.clip(t_ / 0.3, 0, 1) * np.clip((len(xs) / SR - t_) / 0.6, 0, 1))[:, None], 0.18)
hit(ws('bremsten'), 0.10, 65); add(ws('bremsten'), wind(1.4), 0.05)
add(ws('später', 63), fio(engine(2.8, 80, 0.3, 750), 0.3, 0.6), 0.07); add(ws('abgebaut') - 0.05, metal(200, 1.0), 0.05); hit(ws('abgebaut'), 0.08, 75)
hit(ws('Generalluftzeugmeister'), 0.08, 70); add(ws('Generalluftzeugmeister'), swell(2.2, 55), 0.04)
for k in range(5): add(ws('Generalluftzeugmeister') + k * 0.16, clack(), 0.03)
add(ws('Flugzeugproduktion'), fio(engine(2.1, 60, 0.4, 600), 0.3, 0.5), 0.06)
add(ws('Für', 72.5), fio(engine(3.4, 95, 0.3, 900), 0.3, 0.7), 0.06)
add(ws('Als', 76), fio(engine(2.8, 75, 0.35, 700), 0.2, 0.5), 0.08); add(ws('Maschinen', 77) + 0.3, crack(), 0.05); add(ws('verlor') + 0.1, crack(), 0.05)
hit(ws('Göring', 78), 0.08, 75); add(ws('Schuld') - 0.03, stampthump(), 0.15)
add(ws('Am', 80.5), swell(4.0, 45), 0.07); hit(ws('17.'), 0.09, 60); hit(ws('erschoss'), 0.11, 55)
hit(ws('Offiziell'), 0.08, 75); add(ws('verunglückt') - 0.03, stampthump(), 0.20)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.4)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
