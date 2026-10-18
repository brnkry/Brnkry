import re, sys, json, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, find_peaks
D = sys.argv[1]
TEXT = open(D + '/code/script.txt').read().split()
SP = {'18.':'achtzehnten','1965':'neunzehnhundertfünfundsechzig','34':'vierunddreißig','Waffen-SS,':'Waffen S S','US':'U S','28.':'achtundzwanzigsten','1919':'neunzehnhundertneunzehn','1938':'neunzehnhundertachtunddreißig','1939':'neunzehnhundertneununddreißig','1940':'neunzehnhundertvierzig','Special':'Speschel','Army.':'Armi'}
def syl(w):
    w = SP.get(w, SP.get(w.rstrip('.,:'), w))
    return sum(max(1, len(re.findall(r'(?:ei|ie|au|eu|äu|aa|ee|oo|[aeiouyäöü])', p.lower()))) for p in w.split())
P = [(3.24,3.38),(6.26,6.98),(10.25,10.53),(11.81,12.54),(14.29,14.52),(16.03,16.85),(20.05,20.24),(25.30,25.52),(26.38,26.58),(28.62,29.23),(32.53,32.83),(34.22,35.28),(43.55,43.91),(47.91,48.15),(49.18,50.09),(53.48,53.67),(57.64,57.82),(59.96,60.55),(64.34,64.59),(66.60,66.74),(69.13,70.09),(73.62,73.80),(75.43,76.20)]
segs = []; s = 0.05
for a, b in P: segs.append((s, a)); s = b
segs.append((s, 81.6))
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
