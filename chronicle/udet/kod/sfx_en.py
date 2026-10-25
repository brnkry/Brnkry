# sound for the Udet / Ju 87 short: the original dive sound in the intro (heard alone in the pause), the siren rising under the drawing,
# soft hits, transitions and the stamps (no engine or whistle effects on the archive film)
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
gain = np.where(tt < cut - 0.1, 0.32, np.minimum(1.0, 0.32 + (tt - cut + 0.1) / 0.6 * 0.68)); gain *= np.clip((V.ws('His') + 0.35 - tt) / 0.45, 0, 1)
I_ = A * gain[:, None]; I_ /= max(1.0, np.abs(I_).max() / 0.95); wavfile.write(sys.argv[1] + '/intro_trk.wav', SR, (I_ * 32767).astype(np.int16))   # own track in the mix
for s, fn, tr in V.ANCH[2:]: add(s - 0.08, whoosh(0.5, 200, 1400), 0.045, rng.uniform(-0.3, 0.3))
hit(ws('Ernst', 9), 0.09, 75); add(ws('Ernst', 9), swell(2.2, 52), 0.05)
hit(ws('62'), 0.08, 80)
hit(ws('Red'), 0.07, 80)
hit(ws('dive', 17), 0.08, 75)
hit(ws('Hermann'), 0.08, 70); hit(ws('bought'), 0.07, 80)
add(ws('but', 26) - 0.05, scratch(0.4), 0.06)
hit(ws('Junkers'), 0.09, 70); hit(ws('Stuka'), 0.11, 60)
# the drawing: the siren winds up with the dive
S_ = wav(V.B + 'sirena.wav'); ta = ws('Small')
add(ta, swell(2.0, 50), 0.04)
for k in range(5): add(ta + 0.2 + k * 0.12, tick(), 0.03)
tw, tf, tl, tj = ws('rushing'), ws('faster'), ws('louder'), ws('Trumpets')
n = int(SR * (ws('Over') + 0.2 - tf)); xs = S_[:n]; t_ = np.arange(len(xs)) / SR
g = np.clip(t_ / 1.6, 0, 1) * 0.35 + np.clip((t_ - (tl - tf)) / 0.8, 0, 1) * 0.65; g *= np.clip((len(xs) / SR - t_) / 0.5, 0, 1)
addst(tf, xs * g[:, None], 0.30)
hit(tj, 0.10, 60)
hit(ws('Poland'), 0.07, 80); hit(ws('France'), 0.07, 80)
hit(ws('entire'), 0.08, 70); add(ws('entire'), swell(2.2, 55), 0.04)
for k in range(5): add(ws('entire') + k * 0.16, clack(), 0.03)
hit(ws('Göring', 52), 0.08, 75); add(ws('blamed') - 0.03, stampthump(), 0.15)
add(ws('On', 54), swell(4.0, 45), 0.07); hit(ws('November'), 0.09, 60); hit(ws('shot', 55), 0.11, 55)
hit(ws('Officially'), 0.08, 75); add(ws('died', 58) - 0.03, stampthump(), 0.20)
o = sfxlib.out; n = len(o); tt = np.arange(n) / SR; o *= np.minimum(1, (T - tt) / 0.4)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
