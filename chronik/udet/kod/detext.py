# removes the old burned-in white headline from the intro frames: bright low-saturation letters (blobs that do not touch the
# zone border, unlike the cloud masses) plus their drop shadow are masked and refilled from the nearby sky (normalised blur)
import cv2, numpy as np, sys
Y0, Y1, X0, X1 = 230, 800, 40, 1040
def mask(roi):
    h = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV); s = h[..., 1].astype(int); v = h[..., 2].astype(int)
    m = ((s < 60) & (v > 195)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    H, W = m.shape; keep = np.zeros(n, np.uint8)
    for i in range(1, n):
        x, y, w, hh, a = st[i]
        if x <= 1 or y <= 1 or x + w >= W - 1 or y + hh >= H - 1 or a > 40000 or a < 5 or y + hh > 370: continue
        keep[i] = 1
    let = keep[lab]
    d = cv2.dilate(let, np.ones((13, 13), np.uint8))
    sh = np.zeros_like(d); sh[10:, 8:] = d[:-10, :-8]          # drop shadow sits below right
    return ((d | sh) > 0).astype(np.uint8) * 255, (keep == 0)[lab] & (m > 0)
def fillv(roi, m, sig):
    k = (1 - m / 255.0).astype(np.float32)
    num = cv2.GaussianBlur(roi * k[..., None], (0, 0), sig); den = cv2.GaussianBlur(k, (0, 0), sig)[..., None]
    return num / (den + 1e-4), den
def static(im):
    m, _ = mask(im); return m
def clean(im, st=None):
    roi = im[Y0:Y1, X0:X1].astype(np.float32); m, cloud = mask(im[Y0:Y1, X0:X1])
    if st is not None: m = m | st
    f1, d1 = fillv(roi, m, 10); f2, _ = fillv(roi, m, 36)
    w = np.clip((d1 - 0.04) / 0.2, 0, 1); fill = f1 * w + f2 * (1 - w)
    fill += np.random.normal(0, 1.8, fill.shape).astype(np.float32)
    a = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 2)[..., None]
    out = im.copy(); out[Y0:Y1, X0:X1] = np.clip(roi * (1 - a) + fill * a, 0, 255).astype(np.uint8)
    return out, m
if __name__ == '__main__':
    for f in sys.argv[1:]:
        im = cv2.imread(f); o, m = clean(im)
        cv2.imwrite(f.replace('.jpg', '_c.jpg'), np.hstack([im, o]))
