# cleans intro frames 265..1140 (old video 12.4 s .. 27 s, every 2nd frame = 30 fps) -> intro/c%04d.jpg
import cv2, numpy as np, sys
sys.path.insert(0, 'code'); from detext import clean, static, Y0, Y1, X0, X1
S2 = static(cv2.imread('intro/o0300.jpg')[Y0:Y1, X0:X1]); S3 = static(cv2.imread('intro/o0545.jpg')[Y0:Y1, X0:X1])
k = 0
for i in range(265, 1141, 2):
    im = cv2.imread('intro/o%04d.jpg' % i)
    st = S2 if i < 418 else S3 if i < 748 else None
    o, _ = clean(im, st) if i < 760 else (im, None)
    cv2.imwrite('intro/c%04d.jpg' % k, o, [cv2.IMWRITE_JPEG_QUALITY, 94]); k += 1
print(k)
