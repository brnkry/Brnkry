# sound design for the style-A Laconia test from ElevenLabs sound effects (flow "Laconia Short – Sounddesign"):
# beds = night sea + dark drone + projector rattle (all generated as loops); one-shots = photo slap, paper swish, torn strip, impact hit, torpedo
import sys; sys.path.insert(0, sys.argv[1] + '/code')
import numpy as np, subprocess
from scipy.io import wavfile
import styleA as V
SR = 48000; T = V.TEND; ws = V.ws; D = sys.argv[1] + '/el/'
def load(n):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', D + n + '.mp3', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
out = np.zeros((int(SR * T) + SR * 5, 2), np.float32)
def add(t0, x, g, pan=0.0):
    i = int(t0 * SR); l, r = (1 - max(0, pan)), (1 + min(0, pan)); n = min(len(x), len(out) - i)
    if n > 0 and i >= 0: out[i:i + n, 0] += x[:n, 0] * g * l; out[i:i + n, 1] += x[:n, 1] * g * r
def bed(x, g, fin=1.5):
    n = int(SR * T); y = np.tile(x, (n // len(x) + 1, 1))[:n]; t = np.arange(n) / SR
    out[:n] += y * g * np.minimum(1, t / fin)[:, None]
sea, drone, proj = load('sea'), load('drone'), load('proj')
slap, swish, tear, hit, torp = load('slap'), load('swish'), load('tear'), load('hit'), load('torp')
bed(sea, 0.16); bed(drone, 0.20); bed(proj, 0.05)
deal = lambda t0, g=0.35, p=0.0: (add(t0 - 0.05, swish, g * 0.5, p), add(t0 + 0.35, slap, g, p))
for t0, p in ((0.1, -0.3), (0.25, 0.3), (0.4, 0.3), (0.55, 0.0)): deal(t0, 0.32, p)
for a, _ in V.SC[1:]:
    add(a - 0.2, swish, 0.28); deal(a + 0.05, 0.3, -0.2); deal(a + 0.2, 0.25, 0.2)
deal(ws('britische', 20.7), 0.3, -0.2); deal(ws('britische', 20.7) + 0.2, 0.25, 0.2)
add(ws('Hunderte'), hit, 0.35); add(ws('bombardiert'), hit, 0.45)
add(ws('September') - 0.1, hit, 0.35); add(ws('U', 7.5) + 0.1, tear, 0.4)
add(ws('torpedierte'), torp, 0.6); add(ws('Werner') + 0.05, tear, 0.4)
add(ws('Laconia') - 0.15, hit, 0.4); add(ws('2.700'), hit, 0.35); add(ws('1.800'), hit, 0.4)
o = out[:int(SR * T)]; t = np.arange(len(o)) / SR; o *= np.minimum(1, (T - t) / 0.8)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv[1] + '/sfx_el.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
