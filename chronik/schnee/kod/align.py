import re, sys, json, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, find_peaks
D = sys.argv[1]
TEXT = open(D + '/code/script.txt').read().split()
SP = {'500':'fünfhundert','1913':'neunzehnhundertdreizehn','1934':'neunzehnhundertvierunddreißig','U-23':'U dreiundzwanzig','U-201':'U zweihunderteins',
      '21':'einundzwanzig','1942':'neunzehnhundertzweiundvierzig','XXI':'einundzwanzig','U-2511':'U fünfundzwanzig elf','30.':'dreißigsten','1945':'neunzehnhundertfünfundvierzig',
      '9.':'neunten','1982':'neunzehnhundertzweiundachtzig','U-Boot':'U Boot','U-Boot-Fahrer.':'U Boot Fahrer','U-201.':'U zweihunderteins','U-2511,':'U fünfundzwanzig elf'}
def syl(w):
    w = SP.get(w, SP.get(w.rstrip('.,:'), w))
    return sum(max(1, len(re.findall(r'(?:ei|ie|au|eu|äu|aa|ee|oo|[aeiouyäöü])', p.lower()))) for p in w.split())
P = [(2.71,2.93),(3.71,3.85),(5.08,5.63),(6.75,7.68),(14.16,14.82),(16.99,17.20),(20.65,21.39),(24.32,24.46),(25.75,26.33),(29.04,29.43),(31.12,31.72),(34.09,34.80),(39.01,39.67),(43.52,43.70),(45.88,46.63),(48.86,49.38),(52.81,52.95),(56.03,56.66),(59.71,60.02),(62.28,62.93),(67.24,67.79),(69.75,70.00),(71.53,72.20),(73.12,73.26),(74.47,74.69),(77.80,78.42),(82.85,83.43),(84.55,84.90),(86.04,86.60),(87.88,88.51),(91.24,91.75),(94.87,95.51),(96.23,96.55),(99.64,100.31),(103.59,103.80),(106.65,107.27),(110.16,110.87),(112.20,112.62)]
segs = []; s = 0.05
for a, b in P: segs.append((s, a)); s = b
segs.append((s, 114.03))
W = TEXT; sy = [syl(w) for w in W]; cs = np.concatenate([[0], np.cumsum(sy)])
r = sum(b - a for a, b in segs) / cs[-1]
def bpen(i):
    w = W[i - 1]
    if w[-1] in '.!?:': return 0
    if w[-1] == ',': return 0.3
    return 2.5
N = len(W); M = len(segs); INF = 1e9
Dm = np.full((M + 1, N + 1), INF); Bk = np.zeros((M + 1, N + 1), int); Dm[0, 0] = 0
for m in range(1, M + 1):
    a, b = segs[m - 1]; d = b - a
    for j in range(1, N + 1):
        for i in range(max(0, j - 45), j):
            if Dm[m - 1, i] >= INF: continue
            n = cs[j] - cs[i]; c = (d - n * r) ** 2 / max(d, 0.5) + (bpen(j) if j < N else 0)
            if Dm[m - 1, i] + c < Dm[m, j]: Dm[m, j] = Dm[m - 1, i] + c; Bk[m, j] = i
j = N; cuts = []
for m in range(M, 0, -1): i = Bk[m, j]; cuts.append((i, j)); j = i
cuts = cuts[::-1]
sr, x = wavfile.read(D + '/v.wav'); x = x.astype(float) / 32768
x = sosfilt(butter(4, [300, 2500], 'band', fs=sr, output='sos'), x)
hop = int(sr * 0.01); e = np.sqrt(np.convolve(x ** 2, np.ones(hop * 3) / (hop * 3), 'same'))[::hop]
e = np.convolve(e, np.hanning(7) / np.hanning(7).sum(), 'same'); ed = 20 * np.log10(e + 1e-6)
pk, _ = find_peaks(ed, distance=9, prominence=2.5, height=ed.max() - 38); nuc = pk * 0.01
out = []
for (i, j), (a, b) in zip(cuts, segs):
    ws = W[i:j]; sl = [syl(w) for w in ws]; n = sum(sl)
    nn = [t for t in nuc if a - 0.02 <= t <= b + 0.02]
    if len(nn) >= 2 and abs(len(nn) - n) <= max(3, 0.35 * n):
        g = np.interp(np.linspace(0, len(nn) - 1, n), np.arange(len(nn)), nn); on = np.concatenate([[a], (g[:-1] + g[1:]) / 2])
    else: on = a + (b - a) * np.arange(n) / n
    k = 0
    for w, s_ in zip(ws, sl):
        x0 = float(on[k]); k += s_; y0 = float(on[k]) if k < n else b
        out.append([w, round(x0, 2), round(y0, 2)])
    print(f"{a:6.2f}-{b:6.2f} {b-a:5.2f} syl{n:3d} exp{n*r:5.2f} | {' '.join(ws)}")
json.dump(out, open(D + '/words.json', 'w'), ensure_ascii=False)
