# Yeşil zeminli görselleri şeffaf PNG'ye çevirir (en büyük parça + delik doldurma + despill)
import sys, numpy as np, cv2
from scipy import ndimage as ndi
src, dst = sys.argv[1], sys.argv[2]
keep = int(sys.argv[3]) if len(sys.argv) > 3 else 1
im = cv2.imread(src).astype(np.float32)
if len(sys.argv) > 4:
    x0, x1 = map(int, sys.argv[4].split(':'))
    im[:, :x0] = (64, 177, 0); im[:, x1:] = (64, 177, 0)
b, g, r = im[..., 0], im[..., 1], im[..., 2]
score = g - np.maximum(r, b)
a = 1 - np.clip((score - 18) / 40, 0, 1)
m = a > 0.5
lab, n = ndi.label(m)
sizes = ndi.sum(m, lab, range(1, n + 1))
order = np.argsort(sizes)[::-1][:keep]
mask = np.isin(lab, order + 1)
mask = ndi.binary_dilation(mask, iterations=3)
a = a * mask
g2 = np.minimum(g, np.maximum(r, b) + 6)
out = np.dstack([b, g2, r, a * 255]).clip(0, 255).astype(np.uint8)
ys, xs = np.where(a > 0.02)
out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
cv2.imwrite(dst, out)
print(dst, out.shape, 'offset', xs.min(), ys.min())
