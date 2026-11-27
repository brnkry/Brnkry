# finds archive shots whose window is mostly empty (fog, grey sea, sky, black) and proposes a better start nearby
import sys, os, subprocess, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ee, build, ks
def frames(key, a, b, step=0.5):
    src, cr = ee.VID[key]; vf = (f'crop={cr[2]}:{cr[3]}:{cr[0]}:{cr[1]},' if cr else '') + f'fps={1/step},scale=160:120,format=gray'
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(max(a, 0)), '-i', src, '-t', str(b - a), '-vf', vf, '-f', 'rawvideo', '-'], capture_output=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, 120, 160).astype(np.float32); return f
def score(f):
    gx = np.abs(np.diff(f, axis=2)).mean(axis=(1, 2)); gy = np.abs(np.diff(f, axis=1)).mean(axis=(1, 2)); sd = f.std(axis=(1, 2)); mean = f.mean(axis=(1, 2))
    return (gx + gy) * 0.5 + sd * 0.15 - np.where((mean < 35) | (mean > 220), 6, 0)
items = {}
for SH, K, T in ((build.SH, build.K, build.TOTAL), (ks.SH, ks.K, ks.TOTAL)):
    st = [K(s[0]) for s in SH]; st[0] = 0.0
    for i, s in enumerate(SH):
        if s[1] == 'vid':
            d = (st[i + 1] if i + 1 < len(SH) else T) - st[i] + ee.XF; items[(s[2], s[3])] = max(items.get((s[2], s[3]), 0), d)
res = {}
for (k, ss), d in sorted(items.items()):
    f = frames(k, ss, ss + d); sc = score(f); bad = float((sc < 7).mean())
    line = f'{k:6s} {ss:7.1f} d={d:4.1f} mean={sc.mean():5.1f} low={bad:.2f}'
    if bad > 0.25:
        best = None
        for s2 in np.arange(max(ss - 15, 0), ss + 15.1, 0.5):
            g = frames(k, s2, s2 + d, 1.0); c = score(g); b2 = (c < 7).mean()
            v = c.mean() - 20 * b2
            if best is None or v > best[0]: best = (v, float(s2), float(b2))
        line += f'  -> best start {best[1]:.1f} (low {best[2]:.2f})'; res[f'{k}|{ss}'] = best[1]
    print(line, flush=True)
json.dump(res, open(ee.E + 'scan.json', 'w'))
