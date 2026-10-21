# Rommel voice: two parts joined, every pause longer than 0.26 s shortened to 0.20 s (fast narration, sentences still separate)
import numpy as np, subprocess, re
from scipy.io import wavfile
SR = 48000
def load(f):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'drive/' + f, '-ac', '1', '-ar', str(SR), '/tmp/_p.wav'])
    sr, x = wavfile.read('/tmp/_p.wav'); x = x.astype(np.float32) / 32768
    e = np.abs(x) > 0.01; i0 = max(0, np.argmax(e) - int(0.04 * SR)); i1 = len(x) - max(0, np.argmax(e[::-1]) - int(0.08 * SR))
    return x[i0:i1]
x = np.concatenate([load('intro-1to8.mp3'), np.zeros(int(0.2 * SR), np.float32), load('outro9.mp3')])
wavfile.write('vjoin.wav', SR, (x * 32767).astype(np.int16))
log = subprocess.run(['ffmpeg', '-i', 'vjoin.wav', '-af', 'silencedetect=noise=-36dB:d=0.26', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r'silence_start: ([0-9.]+)', log)]; en = [float(v) for v in re.findall(r'silence_end: ([0-9.]+)', log)]
KEEP = 0.20; out = []; pos = 0.0; rem = 0.0; n = 0
for a, b in zip(st, en):
    ca, cb = a + KEEP / 2, b - KEEP / 2
    if cb <= ca: continue
    out.append(x[int(pos * SR):int(ca * SR)]); pos = cb; rem += cb - ca; n += 1
out.append(x[int(pos * SR):]); y = np.concatenate(out)
wavfile.write('vcut.wav', SR, (y * 32767).astype(np.int16))
print('joined %.2f s -> %.2f s, %d pauses, %.2f s removed' % (len(x) / SR, len(y) / SR, n, rem))
