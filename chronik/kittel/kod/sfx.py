# Kittel sound design (Wick recipe) (Schnaufer recipe): dark drone and a low wind under everything, a soft whoosh on every camera move (half volume),
# low hits on the numbers, a torpedo run on the second attack. No paper tears, no photo slaps.
# (The newsreel clips carry narration and music, so none of their sound is used.)
import sys; D0 = sys.argv[1]; sys.path.insert(0, D0 + '/code')
import numpy as np, subprocess
from scipy.io import wavfile
import wk as V
SR = 48000; T = V.TEND; ws = V.ws; D = D0 + '/../style/el/'
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
bed(drone, 0.12, 0, T, 0.05); bed(sea, 0.05, 0, T, 0.05)
for a, _ in V.SCN[1:]: add(a - V.PRE - 0.05, swish, 0.13)
add(V.ZS - 0.05, swish, 0.10)
for w, af in (('1917', 0), ('1939', 16), ('54', 22), ('39', 30), ('4000', 32), ('60', 40), ('100', 55), ('1944', 62), ('267', 85), ('583', 89), ('27', 96)): add(ws(w, af), hit, 0.28)

o = out[:int(SR * T)]; t = np.arange(len(o)) / SR; o *= np.minimum(1, (T - t) / 0.25)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(D0 + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
