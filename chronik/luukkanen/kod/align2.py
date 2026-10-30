import re, sys, json, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, find_peaks
D = sys.argv[1]
TEXT = open(D + '/code/script.txt').read().split()
SP = {'56':'sechsundfünfzig','1930er':'neunzehnhundertdreißiger','30.':'dreißigsten','1939':'neunzehnhundertneununddreißig','24.':'vierundzwanzig','D.XXI':'D einundzwanzig','SB-Bomber':'S B Bomber',
 '1940,':'neunzehnhundertvierzig','1941':'neunzehnhunderteinundvierzig','14,5':'vierzehneinhalb','1943':'neunzehnhundertdreiundvierzig','34,':'vierunddreißig','109':'einhundertneun','Bf':'Be Eff','G':'Ge',
 '1944':'neunzehnhundertvierundvierzig','18.':'achtzehnten','5.':'fünften','56.':'sechsundfünfzigsten','1951':'neunzehnhunderteinundfünfzig','1964':'neunzehnhundertvierundsechzig','54':'vierundfünfzig','USA':'U S A','Mannerheim-Kreuz,':'Mannerheim Kreuz'}
def syl(w):
    w = SP.get(w, SP.get(w.rstrip('.,:'), w))
    return sum(max(1, len(re.findall(r'(?:ei|ie|au|eu|äu|aa|ee|oo|[aeiouyäöü])', p.lower()))) for p in w.split())
P = [(2.20,2.35),(6.55,6.69),(7.22,7.35),(8.23,8.98),(13.27,13.90),(22.18,22.84),(32.13,32.69),(39.75,40.28),(44.17,44.91),(51.61,51.75),(53.59,54.28),(59.47,60.15),(61.93,62.03),(66.67,66.74),(69.09,69.78),(73.85,74.04),(76.84,77.83),(83.97,84.06),(85.33,85.48),(86.06,86.14),(87.39,87.49),(88.03,88.76),(94.86,95.55),(102.23,102.41),(103.87,104.02),(106.37,106.55),(108.03,108.74),(111.14,111.30),(113.35,114.02),(118.86,119.55),(123.51,124.26),(125.68,126.32)]
segs = []; s = 0.13
for a, b in P: segs.append((s, a)); s = b
segs.append((s, 128.15))
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
    print(len(nn), f"{a:6.2f}-{b:6.2f} {b-a:5.2f} syl{n:3d} exp{n*r:5.2f} | {' '.join(ws)}")
json.dump(out, open(D + '/words.json', 'w'), ensure_ascii=False)
