# Anlatımdaki uzun sessizlikleri kısaltır, hafif hızlandırır, yeni cümle zamanlarını yazar.
import sys, subprocess, json, numpy as np
from scipy.io import wavfile
src, out = sys.argv[1], sys.argv[2]
SR = 48000
raw = subprocess.run(['ffmpeg','-loglevel','error','-i',src,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
x = np.frombuffer(raw, np.float32)
segs = [(0,2.40),(2.96,5.12),(6.47,9.92),(10.52,12.63),(13.03,15.50),(16.19,18.56),(19.40,22.21),(23.01,27.31),(27.94,29.62),(30.18,32.30),(33.29,35.20),(35.73,39.77),(40.31,41.35),(41.94,42.62),(43.48,46.25),(47.02,50.36),(50.93,53.90),(54.85,57.87),(58.67,61.07),(61.90,65.11),(65.93,68.30),(69.07,71.93),(72.82,74.84)]
long_before = {10: 0.75, 12: 0.7, 13: 0.45, 17: 0.8, 21: 0.75, 22: 0.7}
PAD = 0.06; TEMPO = 1.04
parts, times, t = [], [], 0.6
parts.append(np.zeros(int(0.6*SR)))
for i,(a,b) in enumerate(segs):
    if i: 
        g = long_before.get(i, 0.38); parts.append(np.zeros(int(g*SR))); t += g
    s = x[int(max(0,a-PAD)*SR):int((b+PAD)*SR)]
    f = int(0.01*SR); s = s.copy(); s[:f]*=np.linspace(0,1,f); s[-f:]*=np.linspace(1,0,f)
    times.append((round(t/TEMPO,2), round((t+len(s)/SR)/TEMPO,2)))
    parts.append(s); t += len(s)/SR
parts.append(np.zeros(int(1.2*SR)))
y = np.concatenate(parts).astype(np.float32)
wavfile.write(out+'.tmp.wav', SR, y)
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',out+'.tmp.wav','-af',f'atempo={TEMPO}',out])
print(json.dumps(times)); print('total', round(len(y)/SR/TEMPO,2))
