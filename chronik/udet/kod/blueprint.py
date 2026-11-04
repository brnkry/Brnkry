# Ju 87 B-2 side profile from the plan sheet (deLooff / Marutaka, sheet 1): keeps the profile, the main gear and the tail wheel,
# drops the sections, the 3D sketch, the title block and the lettering (small isolated blobs) -> pdf/ju87_side.png (alpha = line)
import cv2, numpy as np
g = cv2.imread('pdf/hi-1.pgm', 0)
ink = (g < 150).astype(np.uint8)
keep = np.zeros_like(ink)
def box(x0, y0, x1, y1): keep[y0 * 5:y1 * 5, x0 * 5:x1 * 5] = 1
box(10, 15, 1100, 256)        # fuselage, canopy, mast, fin
box(238, 250, 425, 415)       # main gear leg, spat, wheel
box(960, 200, 1045, 258)      # tail wheel
keep[0:118 * 5, 0:335 * 5] = 0; keep[241 * 5:262 * 5, 700 * 5:960 * 5] = 0; keep[0:62 * 5, 315 * 5:455 * 5] = 0; keep[0:128 * 5, 630 * 5:930 * 5] = 0   # title block, spec table, notes
ink &= keep
n, lab, st, _ = cv2.connectedComponentsWithStats(ink, 8)
ok = np.zeros(n, np.uint8)
for i in range(1, n):
    x, y, w, h, a = st[i]
    if max(w, h) >= 48: ok[i] = 1
line = ok[lab] * 255
ys, xs = np.where(line > 0); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); print(x0, x1, y0, y1)
out = np.zeros((y1 - y0 + 21, x1 - x0 + 21, 4), np.uint8); out[..., :3] = 255; out[10:-10, 10:-10, 3] = line[y0:y1 + 1, x0:x1 + 1]
cv2.imwrite('pdf/ju87_side.png', out)
sm = cv2.resize(255 - out[..., 3], (out.shape[1] // 4, out.shape[0] // 4), interpolation=cv2.INTER_AREA); cv2.imwrite('pdf/side_s.png', sm)
