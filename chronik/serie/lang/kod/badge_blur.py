# the party badge on Hitler's lapel (clips/hitler): tracked frame to frame by template matching from a known position, then
# blurred in place (German channel rule: every party / state symbol unrecognisable). Writes clips/hitler_b/.
import cv2, numpy as np, os, json, sys
D = sys.argv[1] + '/clips/'; src, dst = D + 'hitler/', D + 'hitler_b/'; os.makedirs(dst, exist_ok=True)
fs = sorted(os.listdir(src)); N = len(fs); im = [cv2.imread(src + f, 0) for f in fs]
K0, P0 = 157, (289, 218)   # frame 117.25 s in the source: badge centre
R = 9
def track(order):
    pos = {}; p = P0; tpl = im[K0][P0[1] - R:P0[1] + R, P0[0] - R:P0[0] + R].astype(np.float32)
    for k in order:
        g = im[k].astype(np.float32); x0, y0 = max(0, p[0] - R - 22), max(0, p[1] - R - 22)
        win = g[y0:p[1] + R + 22, x0:p[0] + R + 22]
        if win.shape[0] > 2 * R and win.shape[1] > 2 * R:
            r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED); _, mx, _, ml = cv2.minMaxLoc(r)
            if mx > 0.45: p = (x0 + ml[0] + R, y0 + ml[1] + R)
        pos[k] = (p, mx)
    return pos
pos = track(range(K0, N)); pos.update(track(range(K0, -1, -1)))
for k, f in enumerate(fs):
    g = im[k].copy(); (x, y), sc = pos[k]; r = 15
    y0, y1, x0, x1 = max(0, y - r), min(g.shape[0], y + r), max(0, x - r), min(g.shape[1], x + r)
    reg = g[y0:y1, x0:x1]; bl = cv2.GaussianBlur(cv2.resize(cv2.resize(reg, (max(1, reg.shape[1] // 6), max(1, reg.shape[0] // 6))), (reg.shape[1], reg.shape[0])), (0, 0), 3)
    m = np.zeros_like(reg, np.float32); cv2.circle(m, (x - x0, y - y0), 11, 1, -1); m = cv2.GaussianBlur(m, (0, 0), 3)
    g[y0:y1, x0:x1] = (reg * (1 - m) + bl * m).astype(np.uint8); cv2.imwrite(dst + f, g, [cv2.IMWRITE_JPEG_QUALITY, 95])
json.dump({k: [list(map(int, v[0])), float(v[1])] for k, v in pos.items()}, open(D + 'hitler_badge.json', 'w'))
lo = [k for k, v in pos.items() if v[1] < 0.45]; print('frames', N, 'weak', len(lo))
