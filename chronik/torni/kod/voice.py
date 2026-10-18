# one voice track for the whole video: the three recordings joined, sentence pauses shortened (>0.5 s -> 0.42 s), the closing "Wir sehen uns" removed
import numpy as np, subprocess, re
from scipy.io import wavfile
SR = 48000
def rd(f, a=0, b=None):
    sr, x = wavfile.read(f); x = x.astype(np.float32) / 32768; return x[int(a * SR): int(b * SR) if b else None]
gap = np.zeros(int(0.35 * SR), np.float32)
x = np.concatenate([rd('v.wav'), gap, rd('v3.wav'), gap, rd('v45.wav', 0, 223.8)])
wavfile.write('vjoin.wav', SR, (x * 32767).astype(np.int16))
log = subprocess.run(['ffmpeg', '-i', 'vjoin.wav', '-af', 'silencedetect=noise=-35dB:d=0.5', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r'silence_start: ([0-9.]+)', log)]; en = [float(v) for v in re.findall(r'silence_end: ([0-9.]+)', log)]
KEEP = 0.42; out = []; pos = 0.0; removed = 0.0
for a, b in zip(st, en):
    if a < 0.3: continue
    cut_a = a + KEEP / 2; cut_b = b - KEEP / 2   # keep a little silence at both sides
    if cut_b <= cut_a: continue
    out.append(x[int(pos * SR):int(cut_a * SR)]); pos = cut_b; removed += cut_b - cut_a
out.append(x[int(pos * SR):]); y = np.concatenate(out)
wavfile.write('vcut.wav', SR, (y * 32767).astype(np.int16))
print('joined %.2f s, cut %.2f s, removed %.2f s in %d pauses' % (len(x) / SR, len(y) / SR, removed, len(out) - 1))
