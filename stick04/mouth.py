# VO -> per-frame mouth openness (30 fps) for lip sync. usage: python3 mouth.py 01_hook.mp3 mouth_01_hook.js
import sys, subprocess, numpy as np, json
SR = 16000
raw = subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-f','s16le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float64) / 32768
hop = SR // 30
fr = [np.sqrt(np.mean(x[i:i+hop]**2)) for i in range(0, len(x), hop)]
fr = np.array(fr); ref = np.percentile(fr[fr > 0.01], 85)
m = np.clip((fr - 0.012) / (ref - 0.012), 0, 1) ** 0.8
m = np.convolve(m, [0.25, 0.5, 0.25], 'same')
open(sys.argv[2], 'w').write('window.MOUTH=' + json.dumps([round(float(v), 2) for v in m]) + ';')
print(len(m))
