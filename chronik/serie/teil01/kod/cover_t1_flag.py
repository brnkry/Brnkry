# Teil 1 cover background, flag version: Hitler (3.mp4 at 117 s, fists raised) cut out by a hand-drawn silhouette and set
# on a softly blurred, waving black-red-gold flag. Lapel badge blurred (German channel). covers4.py adds the fixed layout.
import sys, math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
D = sys.argv[1]; src = Image.open(D + '/cov/raw.png').convert('RGB')
X0, X1, Y0, Y1, TOP = 130, 470, 0, 300, 250
k = 1080 / (X1 - X0); fr = src.crop((X0, Y0, X1, Y1)).resize((1080, int((Y1 - Y0) * k)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(3, 80, 2))
cx, cy, R = (342 - X0) * k, (218 - Y0) * k, 11 * k
m = Image.new('L', fr.size, 0); ImageDraw.Draw(m).ellipse((cx - R, cy - R, cx + R, cy + R), fill=255)
fr = Image.composite(fr.filter(ImageFilter.GaussianBlur(R * 0.6)), fr, m.filter(ImageFilter.GaussianBlur(R * 0.25)))
# silhouette, in the 2x preview coordinates of the crop (680x600)
SIL = [(300, 128), (350, 132), (385, 165), (398, 215), (400, 265), (388, 300), (380, 340), (430, 352), (495, 378), (535, 410), (545, 450), (560, 440), (600, 418),
       (640, 425), (650, 470), (615, 500), (580, 500), (560, 520), (560, 600), (130, 600), (120, 540), (105, 500), (92, 455), (100, 415), (140, 405), (170, 415),
       (185, 395), (240, 360), (268, 338), (252, 300), (238, 250), (242, 195), (265, 150)]
s2 = k / 2; mask = Image.new('L', fr.size, 0); ImageDraw.Draw(mask).polygon([(x * s2, y * s2) for x, y in SIL], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(6))
a = np.asarray(mask, np.float32) / 255; n = 220; a[-n:] *= np.linspace(1, 0, n)[:, None]   # body fades out at the bottom
# the flag: three bands, a slow wave with light and shade, blurred, a little dark so the white text stays strong
F = np.zeros((1920, 1080, 3), np.float32); yy, xx = np.mgrid[0:1920, 0:1080].astype(np.float32)
wave = 70 * np.sin(xx / 260 + yy / 900) ; band = np.clip(((yy + wave) / 640).astype(int), 0, 2)
cols = np.array([(20, 20, 22), (200, 22, 26), (240, 190, 20)], np.float32); F = cols[band]
shade = 0.78 + 0.22 * np.sin(xx / 170 + yy / 520 + 1.3); F *= shade[..., None]
flag = Image.fromarray(np.clip(F, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))
flag = ImageEnhance.Brightness(flag).enhance(0.72)
can = flag.copy(); can.paste(fr, (0, TOP), Image.fromarray((a * 255).astype(np.uint8)))
g = np.random.default_rng(1).normal(0, 6, (1920, 1080, 1)); can = Image.fromarray(np.clip(np.asarray(can, np.float32) + g, 0, 255).astype(np.uint8))
can.save(D + '/cov/cov_flag.jpg', quality=95); print('ok')
