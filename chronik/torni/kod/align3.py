# robust word timing: pauses split the voice into segments, a DP assigns words to segments using
# duration AND the number of detected syllable nuclei, pauses may also fall inside a sentence or be skipped,
# long pauses (sentence breaks kept at ~0.42 s) strongly prefer sentence-final punctuation
import sys, re, json, subprocess, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, find_peaks
D = sys.argv[1]; WAV = sys.argv[2]; OUT = sys.argv[3]
exec(open(D + '/code/align_all.py').read().split('def syl(w):')[0].split('TEXT =')[0])   # imports
SP = eval(re.search(r"SP = (\{.*?\})\n", open(D + '/code/align_all.py').read(), re.S).group(1))
TEXT = open(D + '/code/script.txt').read().split()
def syl(w):
    w = SP.get(w, SP.get(w.rstrip('.,:?!'), w))
    return sum(max(1, len(re.findall(r'(?:ei|ie|au|eu|äu|aa|ee|oo|[aeiouyäöü])', p.lower()))) for p in w.split())
sr, x = wavfile.read(WAV); x = x.astype(float) / 32768; dur = len(x) / sr
log = subprocess.run(['ffmpeg', '-i', WAV, '-af', 'silencedetect=noise=-33dB:d=0.11', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r'silence_start: ([0-9.]+)', log)]; en = [float(v) for v in re.findall(r'silence_end: ([0-9.]+)', log)]
pauses = [(a, b) for a, b in zip(st, en) if a > 0.2 and b < dur - 0.2]
segs = []; s = 0.03
for a, b in pauses: segs.append((s, a, b - a)); s = b
segs.append((s, dur - 0.05, 1.0))
# syllable nuclei
y = sosfilt(butter(4, [300, 2500], 'band', fs=sr, output='sos'), x); hop = int(sr * 0.01)
e = np.sqrt(np.convolve(y ** 2, np.ones(hop * 3) / (hop * 3), 'same'))[::hop]; e = np.convolve(e, np.hanning(7) / np.hanning(7).sum(), 'same'); ed = 20 * np.log10(e + 1e-6)
pk, _ = find_peaks(ed, distance=9, prominence=2.5, height=ed.max() - 38); nuc = pk * 0.01
nseg = [int(((nuc >= a - 0.02) & (nuc <= b + 0.02)).sum()) for a, b, _ in segs]
W_ = TEXT; sy = np.array([syl(w) for w in W_]); cs = np.concatenate([[0], np.cumsum(sy)])
r = sum(b - a for a, b, _ in segs) / cs[-1]; q = sum(nseg) / cs[-1]
def endpen(j, gap):
    w = W_[j - 1]; long = gap > 0.36
    if w[-1] in '.!?': return 0.0 if long else 0.8
    if w[-1] == ':': return 0.2 if long else 0.4
    if w[-1] == ',': return 1.2 if long else 0.25
    return 6.0 if long else 2.0
N = len(W_); M = len(segs); INF = 1e18
Dm = np.full((M + 1, N + 1), INF); Bk = np.zeros((M + 1, N + 1), int); Dm[0, 0] = 0
for m in range(1, M + 1):
    a, b, gap = segs[m - 1]; d = b - a; no = nseg[m - 1]
    for j in range(0, N + 1):
        best = INF; arg = -1
        if Dm[m - 1, j] < INF and d < 0.45:   # empty segment (noise / breath): allowed with a penalty
            best = Dm[m - 1, j] + 3.0; arg = j
        for i in range(max(0, j - 50), j):
            if Dm[m - 1, i] >= INF: continue
            n = cs[j] - cs[i]
            c = (d - n * r) ** 2 / max(d, 0.6) * 2.0 + (no - n * q) ** 2 / max(n * q, 3) * 0.6 + (endpen(j, gap) if j < N else 0)
            v = Dm[m - 1, i] + c
            if v < best: best = v; arg = i
        Dm[m, j] = best; Bk[m, j] = arg
j = N; cuts = []
for m in range(M, 0, -1): i = Bk[m, j]; cuts.append((i, j)); j = i
cuts = cuts[::-1]
out = []
for (i, j), (a, b, gap), no in zip(cuts, segs, nseg):
    if i == j: continue
    ws = W_[i:j]; sl = [syl(w) for w in ws]; n = sum(sl)
    nn = [t for t in nuc if a - 0.02 <= t <= b + 0.02]
    if len(nn) >= 2 and abs(len(nn) - n) <= max(3, 0.35 * n):
        g = np.interp(np.linspace(0, len(nn) - 1, n), np.arange(len(nn)), nn); on = np.concatenate([[a], (g[:-1] + g[1:]) / 2])
    else: on = a + (b - a) * np.arange(n) / n
    k = 0
    for w, s_ in zip(ws, sl):
        x0 = float(on[k]); k += s_; y0 = float(on[k]) if k < n else b
        out.append([w, round(x0, 2), round(y0, 2)])
    print(f"{a:7.2f}-{b:6.2f} {b-a:5.2f} n{no:3d}/{n:3d} gap{gap:4.2f} | {' '.join(ws)}")
assert len(out) == N
json.dump(out, open(OUT, 'w'), ensure_ascii=False)
