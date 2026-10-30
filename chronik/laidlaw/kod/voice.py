# Laidlaw voice: one ElevenLabs file, sentence pauses shortened (>0.5 s -> 0.42 s)
import numpy as np, subprocess, re
from scipy.io import wavfile
SR = 48000
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'jean.mp3', '-ac', '1', '-ar', str(SR), 'vraw.wav'])
sr, x = wavfile.read('vraw.wav'); x = x.astype(np.float32) / 32768
log = subprocess.run(['ffmpeg', '-i', 'vraw.wav', '-af', 'silencedetect=noise=-35dB:d=0.5', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r'silence_start: ([0-9.]+)', log)]; en = [float(v) for v in re.findall(r'silence_end: ([0-9.]+)', log)]
KEEP = 0.42; out = []; pos = 0.0; removed = 0.0
for a, b in zip(st, en):
    if a < 0.3: continue
    cut_a = a + KEEP / 2; cut_b = b - KEEP / 2
    if cut_b <= cut_a: continue
    out.append(x[int(pos * SR):int(cut_a * SR)]); pos = cut_b; removed += cut_b - cut_a
out.append(x[int(pos * SR):]); y = np.concatenate(out)
wavfile.write('v.wav', SR, (y * 32767).astype(np.int16))
print('raw %.2f s, cut %.2f s, removed %.2f s' % (len(x) / SR, len(y) / SR, removed))
