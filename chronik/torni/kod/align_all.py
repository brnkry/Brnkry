import re, sys, json, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, find_peaks
D = sys.argv[1]
TEXT = open(D + '/code/script.txt').read().split()
SP = {'18.':'achtzehnten','1965':'neunzehnhundertfünfundsechzig','34':'vierunddreißig','Waffen-SS,':'Waffen S S','Waffen-SS.':'Waffen S S','Waffen-SS':'Waffen S S','US':'U S','28.':'achtundzwanzigsten','1919':'neunzehnhundertneunzehn','1938':'neunzehnhundertachtunddreißig','1939':'neunzehnhundertneununddreißig','1940':'neunzehnhundertvierzig','Special':'Speschel','Army.':'Armi','1941':'neunzehnhunderteinundvierzig','1943':'neunzehnhundertdreiundvierzig','1944':'neunzehnhundertvierundvierzig','1945':'neunzehnhundertfünfundvierzig','1948':'neunzehnhundertachtundvierzig','1949':'neunzehnhundertneunundvierzig','1954':'neunzehnhundertvierundfünfzig','1962':'neunzehnhundertzweiundsechzig','3.800':'dreitausendachthundert','1963':'neunzehnhundertdreiundsechzig','1999':'neunzehnhundertneunundneunzig','2003':'zweitausenddrei','26.':'sechsundzwanzigsten','US-Flugzeugs':'U S Flugzeugs','amerikanisch-vietnamesisches':'amerikanisch vietnamesisches','Mannerheim-Kreuz,':'Mannerheim Kreuz','Zagros-Gebirge':'Zagros Gebirge','Green':'Grien','Berets,':'Berrehs','20.':'zwanzigsten'}
def syl(w):
    w = SP.get(w, SP.get(w.rstrip('.,:'), w))
    return sum(max(1, len(re.findall(r'(?:ei|ie|au|eu|äu|aa|ee|oo|[aeiouyäöü])', p.lower()))) for p in w.split())
P = [(3.24,3.38),(6.26,6.69),(9.96,10.24),(11.52,11.94),(13.69,13.92),(15.43,15.86),(19.06,19.25),(24.31,24.53),(25.39,25.59),(27.62,28.06),(31.36,31.65),(33.04,33.47),(41.74,42.10),(46.10,46.33),(47.36,47.79),(51.17,51.36),(55.33,55.51),(57.65,58.08),(61.86,62.11),(64.12,64.27),(66.66,67.08),(70.61,70.79),(72.43,72.86),(78.60,79.02),(81.80,82.22),(90.13,90.55),(95.46,95.90),(101.55,101.67),(103.20,103.62),(110.64,111.06),(113.74,113.97),(117.44,117.87),(120.02,120.24),(121.91,122.39),(125.18,125.61),(129.69,129.99),(132.63,133.05),(140.41,140.88),(146.50,146.75),(149.32,149.74),(151.34,151.46),(154.62,154.80),(158.45,158.62),(160.15,160.29),(161.32,161.75),(167.53,167.84),(170.73,170.98),(171.83,172.25),(177.10,177.52),(179.58,180.01),(182.12,182.54),(185.98,186.24),(190.83,191.26),(193.64,193.79),(196.72,197.14),(199.92,200.34),(202.91,203.17),(207.07,207.51),(210.46,210.69),(211.68,212.10),(213.69,213.84),(215.34,215.59),(216.92,217.21),(218.15,218.57),(219.65,219.79),(221.14,221.58),(222.86,223.01),(224.35,224.56),(226.58,226.78),(228.88,229.31),(231.00,231.18),(233.46,233.66),(234.76,234.99),(236.71,237.13),(239.21,239.35),(240.56,240.81),(241.86,242.12),(242.85,243.00),(243.61,244.04),(245.78,245.90),(249.87,250.29),(254.28,254.51),(258.73,258.95),(260.86,261.05),(263.38,263.82),(267.93,268.36),(270.17,270.32),(272.67,272.83),(276.50,276.93),(279.89,280.21),(284.16,284.31),(285.44,285.86),(287.04,287.18),(290.13,290.34),(291.94,292.37),(294.20,294.63),(296.49,296.63),(298.78,299.21),(301.34,301.53),(304.36,304.58),(305.71,306.07),(307.35,307.78),(310.26,310.38),(310.38,310.67),(312.81,312.95),(314.37,314.66),(315.46,315.77),(316.87,317.29),(318.47,318.78),(319.70,319.99),(320.89,321.05),(322.04,322.47),(324.73,324.86),(326.87,327.20),(327.31,327.45),(330.75,331.18),(332.44,332.78),(334.96,335.16),(337.18,337.41),(339.88,340.32),(342.15,342.58),(344.09,344.52),(346.52,346.64),(346.64,346.76),(348.70,348.88),(351.31,351.49)]
segs = []; s = 0.05
for a, b in P: segs.append((s, a)); s = b
segs.append((s, 351.3))
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
sr, x = wavfile.read(D + '/vcut.wav'); x = x.astype(float) / 32768
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
