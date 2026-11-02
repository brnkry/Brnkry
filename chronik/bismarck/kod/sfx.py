# Bismarck sound design: sea and a dark drone under everything, a soft whoosh on every camera move (half volume),
# low hits on the counters, a torpedo run on "Torpedo". No paper tears, no photo slaps.
# The colour clips 00 and 02 carry their own sea, wind and gunfire (no music, no narration): that sound runs under their scenes, in sync with the film.
# 01 and 12 carry music, 07 and 08 narration: not used.
import sys; sys.path.insert(0, sys.argv[1] + '/code'); sys.argv_dir = sys.argv[1]
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
import glob
sys.argv = ['x', 'none']; import extract as X   # segment table only (nothing is cut)
def src_audio(n, ss, d):
    f = glob.glob(sys.argv_dir + '/drive/%s_*' % n)[0]
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '%.3f' % ss, '-t', '%.3f' % d, '-i', f, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
CLIPGAIN = 0.55
for j, (b, parts, _, _) in enumerate(V.SC):
    starts = [V.t_in(j)] + [aa for _, aa in parts[1:]]
    for q, (k, _) in enumerate(parts):
        n, ss, dur, _ = X.FULL[k]
        if n not in ('00', '02'): continue
        ps = starts[q]; pe = starts[q + 1] if q + 1 < len(parts) else (V.t_in(j + 1) + V.D if j + 1 < len(V.SC) else T)
        x = src_audio(n, ss, min(dur, pe - ps)); m = len(x); f = int(0.25 * SR); env = np.ones(m, np.float32)
        if j > 0 or q > 0: env[:f] = np.linspace(0, 1, f)
        env[-f:] *= np.linspace(1, 0, f); add(ps, x * env[:, None], CLIPGAIN)
bed(drone, 0.12, 0, T, 0.05); bed(sea, 0.07, 0, ws('Ihr', 60), 0.05)
for a, *_ in V.SC[1:]: add(a - V.PRE - 0.05, swish, 0.13)
for w, af in (('1941', 0), ('acht', 0), ('drei', 0), ('15', 0), ('114', 0), ('fünf', 65)): add(ws(w, af), hit, 0.28)
add(ws('Torpedo') - 0.1, torp, 0.30)
o = out[:int(SR * T)]; t = np.arange(len(o)) / SR; o *= np.minimum(1, (T - t) / 1.0)[:, None]; o /= max(1.0, np.abs(o).max() / 0.95)
wavfile.write(sys.argv_dir + '/sfx.wav', SR, (o * 32767).astype(np.int16)); print('sfx ok', T)
