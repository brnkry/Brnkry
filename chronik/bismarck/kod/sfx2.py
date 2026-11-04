# Bismarck (Egon-style table) sound design: dark drone and sea under everything, a soft whoosh on every camera move (half volume),
# low hits on the counters, a torpedo run on "Torpedo". No paper tears, no photo slaps.
# The colour clips 00 and 02 carry their own sea, wind and gunfire (no music, no narration): that sound runs low under the scenes whose main print plays them.
import sys; D0 = sys.argv[1]; sys.path.insert(0, D0 + '/code')
import numpy as np, subprocess, glob
from scipy.io import wavfile
import bm2 as V, extractL as X
SR = 48000; T = V.TEND; ws = V.ws; D = D0 + '/../style/el/'
def load(n):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', D + n + '.mp3', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
def src_audio(n, ss, d):
    f = glob.glob(D0 + '/drive/%s_*' % n)[0]
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '%.3f' % ss, '-t', '%.3f' % d, '-i', f, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
out = np.zeros((int(SR * T) + SR * 5, 2), np.float32)
def add(t0, x, g):
    i = int(t0 * SR); n = min(len(x), len(out) - i)
    if n > 0 and i >= 0: out[i:i + n] += x[:n] * g
def bed(x, g, a=0.0, b=None, f=1.0):
    b = b or T; i0, i1 = int(a * SR), int(b * SR); n = i1 - i0; y = np.tile(x, (n // len(x) + 1, 1))[:n]; tt = np.arange(n) / SR
    env = np.minimum(1, np.minimum(tt / f, (n / SR - tt) / f)); out[i0:i1] += y * g * env[:, None]
def clip_sound(n, ss, a, b, g=0.38, fade=0.3):
    x = src_audio(n, ss, b - a); m = len(x); f = int(fade * SR); env = np.ones(m, np.float32)
    if a > 0.01: env[:f] = np.linspace(0, 1, f)
    env[-f:] *= np.linspace(1, 0, f); add(a, x * env[:, None], g)
drone, sea, swish, hit, torp = load('drone'), load('sea'), load('swish'), load('hit'), load('torp')
bed(drone, 0.12, 0, T, 0.05); bed(sea, 0.07, 0, ws('Ihr', 60), 0.05)
for a, _ in V.SCN[1:]: add(a - V.PRE - 0.05, swish, 0.13)
add(V.ZS - 0.05, swish, 0.10)
for w, af in (('1941', 0), ('acht', 0), ('drei', 0), ('15', 0), ('114', 0), ('fünf', 65)): add(ws(w, af), hit, 0.28)
add(ws('Torpedo') - 0.1, torp, 0.30)
clip_sound('02', 91.5, 0.0, V.ZS + 0.6)                     # hook film (the Bismarck behind the guns)
MAIN = {'s_1941': 'dist', 's_dk': 'fire1', 's_fire': 'flash', 's_three': 'smk', 's_leak': 'bow', 's_circ': 'hor', 's_scut': 'scut'}
for j, (b, fn) in enumerate(V.SCN):
    k = MAIN.get(fn.__name__)
    if not k: continue
    n, ss, dur, _ = X.CUT[k]; a = b - V.PRE; e = (V.SCN[j + 1][0] + V.POST) if j + 1 < len(V.SCN) else T
    clip_sound(n, ss, a, min(e, a + dur))
o = out[:int(SR * T)]; t = np.arange(len(o)) / SR; o *= np.minimum(1, (T - t) / 0.25)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(D0 + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
