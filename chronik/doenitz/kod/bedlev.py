# music bed with an even level: 4 s loudness envelope -> gain so every part sits at the level of the loud sections
# usage: bedlev.py <in.mp3> <start s> <length s> <out.wav>
import sys, subprocess, numpy as np
from scipy.io import wavfile
from scipy.ndimage import uniform_filter1d
src, ss, ln, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(ln), '-i', src, '-ar', '48000', '-ac', '2', '-af', 'afade=t=in:d=0.4', out + '.raw.wav'], check=True)
sr, x = wavfile.read(out + '.raw.wav'); x = x.astype(np.float32) / 32768
hop = sr // 4; n = len(x) // hop
rms = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean() + 1e-9) for i in range(n)])
env = np.sqrt(uniform_filter1d(rms ** 2, 16, mode='nearest')); g = uniform_filter1d(np.clip(np.percentile(env, 75) / env, 0.6, 3.0), 8, mode='nearest')
y = x * np.interp(np.arange(len(x)), np.arange(n) * hop + hop / 2, g)[:, None]; y /= max(1.0, np.abs(y).max() / 0.98)
wavfile.write(out, sr, (y * 32767).astype(np.int16)); print('bed', len(y) / sr)
