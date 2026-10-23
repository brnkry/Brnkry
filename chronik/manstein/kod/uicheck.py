# compares each frame with and without the text layers; reports text pixels inside the Shorts UI areas
import sys, numpy as np
sys.path.insert(0, '.')
import mshort as V
a, b = float(sys.argv[1]), float(sys.argv[2])
full = {}
ts = [round(float(x), 2) for x in np.arange(a, b, 0.2)]
for t in ts: full[t] = np.asarray(V.frame(t), np.int16)
for n in ('title', 'stamp', 'hand', 'on_quad', 'sky', 'captions', 'strike'): setattr(V, n, lambda *x, **k: None)
ZONES = {'right buttons': (940, 700, 1080, 1580), 'top bar': (0, 0, 1080, 170), 'bottom title': (0, 1590, 1080, 1920)}
for t in ts:
    d = np.abs(full[t] - np.asarray(V.frame(t), np.int16)).max(2) > 40
    for z, (x0, y0, x1, y1) in ZONES.items():
        c = int(d[y0:y1, x0:x1].sum())
        if c > 30: print(f'{t:6.2f} {z}: {c} px')
print('done', a, b)
