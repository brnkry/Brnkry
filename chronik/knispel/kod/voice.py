# knispel short: pauses shortened but not removed (fast, still breathing): sentence breaks keep 0.24 s, shorter pauses 0.16 s
import numpy as np, subprocess, re
from scipy.io import wavfile
SR = 48000
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'drive/Kurtkksinpel_elevenlabs.mp3', '-ac', '1', '-ar', str(SR), 'vraw.wav'])
sr, x = wavfile.read('vraw.wav'); x = x.astype(np.float32) / 32768
e = np.abs(x) > 0.01; i0 = max(0, np.argmax(e) - int(0.04 * SR)); i1 = len(x) - max(0, np.argmax(e[::-1]) - int(0.08 * SR)); x = x[i0:i1]
wavfile.write('vtrim.wav', SR, (x * 32767).astype(np.int16))
log = subprocess.run(['ffmpeg', '-i', 'vtrim.wav', '-af', 'silencedetect=noise=-36dB:d=0.22', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r'silence_start: ([0-9.]+)', log)]; en = [float(v) for v in re.findall(r'silence_end: ([0-9.]+)', log)]
out = []; pos = 0.0; rem = 0.0; n = 0
for a, b in zip(st, en):
    KEEP = 0.24 if b - a >= 0.38 else 0.16; ca, cb = a + KEEP / 2, b - KEEP / 2
    if cb <= ca: continue
    out.append(x[int(pos * SR):int(ca * SR)]); pos = cb; rem += cb - ca; n += 1
out.append(x[int(pos * SR):]); y = np.concatenate(out)
wavfile.write('vcut.wav', SR, (y * 32767).astype(np.int16))
print('%.2f s -> %.2f s, %d pauses, %.2f s removed' % (len(x) / SR, len(y) / SR, n, rem))
