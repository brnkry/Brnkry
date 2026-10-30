# dog tag photo k10 -> RGBA cut-out (img/tag.png): the tag is a half oval (measured on the photo), with its two punched holes left see-through
import cv2, numpy as np, math, sys
im = cv2.imread('img/k10.jpg'); H, W = im.shape[:2]
L, R, AP = (195, 900), (2190, 962), (1200, 204)   # chord ends and the top of the arc (source px)
cx, cy = (L[0] + R[0]) / 2, (L[1] + R[1]) / 2; ang = math.atan2(R[1] - L[1], R[0] - L[0]); a = math.dist(L, R) / 2; b = cy - AP[1]
pts = []
for t in np.linspace(math.pi, 2 * math.pi, 200):
    x, y = a * math.cos(t), b * math.sin(t); pts.append((cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)))
m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [np.array(pts, np.int32)], 255)
for hx, hy in ((930, 381), (1515, 381)): cv2.circle(m, (hx, hy), int(sys.argv[1]) if len(sys.argv) > 1 else 70, 0, -1)
m = cv2.GaussianBlur(m, (0, 0), 2.5)
if len(sys.argv) > 2:   # check: outline on the photo
    c = im.copy(); cv2.polylines(c, [np.array(pts, np.int32)], True, (0, 0, 255), 5)
    for hx, hy in ((930, 381), (1515, 381)): cv2.circle(c, (hx, hy), 70, (0, 0, 255), 4)
    cv2.imwrite('chk/tagline.jpg', cv2.resize(c, (W // 3, H // 3)))
x, y, w, h = cv2.boundingRect((m > 10).astype(np.uint8))
cv2.imwrite('img/tag.png', np.dstack([im, m])[y:y + h, x:x + w]); print('tag', w, h)
