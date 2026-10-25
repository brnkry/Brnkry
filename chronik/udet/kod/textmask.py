# pass 1: letter masks of every intro frame, saved per frame (npz) so pass 2 can union a short window around each frame
import cv2, numpy as np, sys, glob
sys.path.insert(0, 'code'); from detext import Y0, Y1, X0, X1
fs = sorted(glob.glob('intro/o[0-9][0-9][0-9][0-9].jpg')); L = []
for f in fs:
    roi = cv2.imread(f)[Y0:Y1, X0:X1]; h = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV); s = h[..., 1].astype(int); v = h[..., 2].astype(int)
    m = ((s < 130) & (v > 105) & (v - s > 25)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8); H, W = m.shape; keep = np.zeros(n, np.uint8)
    for i in range(1, n):
        x, y, w, hh, a = st[i]
        if x <= 1 or y <= 1 or x + w >= W - 1 or y + hh >= H - 1 or a > 40000 or a < 5 or hh > 70: continue
        keep[i] = 1
    L.append(np.packbits(keep[lab]))
np.save('intro/lets.npy', np.array(L)); print(len(L))
