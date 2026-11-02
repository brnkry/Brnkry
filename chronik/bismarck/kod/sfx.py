# Bismarck sound design: sea and a dark drone under everything, a soft whoosh on every camera move (half volume),
# low hits on the counters, a torpedo run on "Torpedo". No paper tears, no photo slaps. (The Drive clips carry music or narration, so none of their sound is used.)
import sys; sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, subprocess
from scipy.io import wavfile
import bm as V
SR = 48000; T = V.TEND; ws = V.ws; D = sys.argv[1] + '/../style/el/'
def load(n):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', D + n + '.mp3', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
out = np.zeros((int(SR * T) + SR * 5, 2), np.float32)
def add(t0, x, g):
    i = int(t0 * SR); n = min(len(x), len(out) - i)
    if n > 0 and i >= 0: out[i:i + n] += x[:n] * g
def bed(x, g, a=0.0, b=None, f=1.0):
    b = b or T; i0, i1 = int(a * SR), int(b * SR); n = i1 - i0; y = np.tile(x, (n // len(x) + 1, 1))[:n]; tt = np.arange(n) / SR
    env = np.minimum(1, np.minimum(tt / f, (n / SR - tt) / f)); out[i0:i1] += y * g * env[:, None]
drone, sea, swish, hit, torp = load('drone'), load('sea'), load('swish'), load('hit'), load('torp')
bed(drone, 0.12, 0, T, 0.05); bed(sea, 0.10, 0, ws('Ihr', 60), 0.05)
for a, *_ in V.SC[1:]: add(a - V.PRE - 0.05, swish, 0.13)
for w, af in (('1941', 0), ('acht', 0), ('drei', 0), ('15', 0), ('114', 0), ('fünf', 65)): add(ws(w, af), hit, 0.28)
add(ws('Torpedo') - 0.1, torp, 0.30)
o = out[:int(SR * T)]; t = np.arange(len(o)) / SR; o *= np.minimum(1, (T - t) / 1.0)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
