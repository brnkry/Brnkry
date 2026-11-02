# sound design for style A v2: night sea + dark drone beds, a soft whoosh on each transition (half volume), low hits on the counters,
# the torpedo on "torpedierte". No paper tear, no photo slaps (Boran: they did not work).
import sys; sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, subprocess
from scipy.io import wavfile
import styleB as V
SR = 48000; T = V.TEND; ws = V.ws; D = sys.argv[1] + '/el/'
def load(n):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', D + n + '.mp3', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
out = np.zeros((int(SR * T) + SR * 5, 2), np.float32)
def add(t0, x, g):
    i = int(t0 * SR); n = min(len(x), len(out) - i)
    if n > 0 and i >= 0: out[i:i + n] += x[:n] * g
def bed(x, g, fin=1.5):
    n = int(SR * T); y = np.tile(x, (n // len(x) + 1, 1))[:n]; t = np.arange(n) / SR
    out[:n] += y * g * np.minimum(1, t / fin)[:, None]
sea, drone, swish, hit, torp = load('sea'), load('drone'), load('swish'), load('hit'), load('torp')
bed(sea, 0.13); bed(drone, 0.15)
for b, kind in V.TR.items(): add(b - 0.25, swish, 0.14 if kind != 'fade' else 0.10)
add(ws('bombardiert'), hit, 0.35); add(ws('1942'), hit, 0.3); add(ws('torpedierte'), torp, 0.55)
add(ws('Laconia') - 0.1, hit, 0.35); add(ws('2.700'), hit, 0.3); add(ws('1.800'), hit, 0.35)
o = out[:int(SR * T)]; t = np.arange(len(o)) / SR; o *= np.minimum(1, (T - t) / 0.8)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx_B.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
