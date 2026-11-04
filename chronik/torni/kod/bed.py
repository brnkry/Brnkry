# music bed of any length: Steel_and_Salt up to 146 s (before its fade-out), then loops back to 24 s with 4 s equal-power crossfades; gently levelled
import sys, subprocess, numpy as np
from scipy.io import wavfile
L, OUT = float(sys.argv[1]), sys.argv[2]; SR = 48000
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'music.mp3', '-ar', str(SR), '-ac', '2', 'music48.wav'], check=True)
sr, m = wavfile.read('music48.wav'); m = m.astype(np.float32) / 32768
A, B, X = int(24 * SR), int(146 * SR), int(4 * SR)
out = m[:B].copy(); fi = np.sin(np.linspace(0, np.pi / 2, X))[:, None]; fo = np.cos(np.linspace(0, np.pi / 2, X))[:, None]
while len(out) < L * SR:
    seg = m[A:B]; out[-X:] = out[-X:] * fo + seg[:X] * fi; out = np.concatenate([out, seg[X:]])
out = out[:int(L * SR)]
# slow level smoothing: 3 s RMS window, pull toward the median
win = int(3 * SR); c = np.concatenate([[0], np.cumsum((out ** 2).mean(1), dtype=np.float64)]); i = np.arange(len(out)); lo = np.clip(i - win // 2, 0, len(out)); hi = np.clip(i + win // 2, 0, len(out))
e = np.sqrt((c[hi] - c[lo]) / np.maximum(1, hi - lo)).astype(np.float32) + 1e-6
g = np.clip(np.median(e) / e, 0.7, 1.6) ** 0.7; out *= g[:, None]
out /= max(1.0, np.abs(out).max() / 0.95)
wavfile.write(OUT, SR, (out * 32767).astype(np.int16)); print('bed', len(out) / SR)
