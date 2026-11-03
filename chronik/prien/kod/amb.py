# original film sound under the prints (U-boat engines, sea, crowd), only where the newsreel has no narration
# (speech found with a transcription of the clip audio); the 'deck' cut carries music, so it stays silent
import sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.io import wavfile
import pr
SR = 48000; E = pr.E
CLIP = {3: ('dw549.mp4', 108.0, 'launch', [(0.25, 8.25)]), 4: ('dw534.mp4', 56.0, 'sea', [(1.35, 5.75)]),
        7: ('dw534.mp4', 156.0, 'peri', [(3.05, 4.55), (12.65, 16.65)]), 9: ('feindfahrt.mp4', 209.0, 'arrive', []),
        10: ('feindfahrt.mp4', 292.0, 'march', []), 12: ('dw534.mp4', 134.0, 'peri2', [(0.95, 8.55), (12.35, 14.45)]),
        13: ('dw549.mp4', 140.0, 'dive', [])}
T = pr.TEND; out = np.zeros(int(T * SR) + SR, np.float32)
for j, (f, ss, k, speech) in CLIP.items():
    a = pr.SCN[j][0] - pr.PRE; b = (pr.SCN[j + 1][0] - pr.PRE) if j + 1 < len(pr.SCN) else T
    d = b - a + 0.4; af = 'atempo=0.6,' if k == 'march' else ''
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', E + 'dl/' + f, '-t', str(d * (0.6 if k == 'march' else 1) + 0.1),
                          '-af', af + 'highpass=f=60,lowpass=f=9000', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).copy()[:int(d * SR)]
    tt = np.arange(len(x)) / SR; m = np.ones_like(x)
    for s0, s1 in speech: m = np.minimum(m, np.clip(np.maximum(s0 - tt, tt - s1) / 0.25, 0, 1))   # narration muted, 0.25 s fades
    x *= m; x /= (np.sqrt((x[m > 0.5] ** 2).mean()) + 1e-6) if (m > 0.5).any() else 1   # same loudness for every cut
    env = np.minimum(1, np.minimum(tt / 0.3, (len(x) / SR - tt) / 0.3)); x *= env
    i = int(a * SR); n = min(len(x), len(out) - i); out[i:i + n] += x[:n] * 0.05
    print(k, '%.2f-%.2f' % (a, b))
out = out[:int(T * SR)]
sr, s = wavfile.read(E + 'sfx.wav'); s = s.astype(np.float32) / 32768; n = min(len(s), len(out)); s = s[:n] + out[:n, None]
s /= max(1.0, np.abs(s).max() / 0.95); wavfile.write(E + 'sfx2.wav', SR, (s * 32767).astype(np.int16)); print('ok')
