# Teil 1 cover background: the speech close-up (3.mp4 at 117 s, both fists raised), upscaled into the top of a dark 9:16 canvas;
# the party badge on the lapel blurred (German channel). covers4.py then adds the fixed Yamamoto layout.
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
D = sys.argv[1]; src = Image.open(D + '/cov/' + sys.argv[2]).convert('RGB')
X0, X1, Y0, Y1, TOP = 130, 470, 0, 300, 250
k = 1080 / (X1 - X0); fr = src.crop((X0, Y0, X1, Y1)).resize((1080, int((Y1 - Y0) * k)), Image.LANCZOS)
fr = fr.filter(ImageFilter.UnsharpMask(3, 80, 2))
bx, by, r = [float(v) for v in sys.argv[3:6]]   # badge in frame pixels
cx, cy, R = (bx - X0) * k, (by - Y0) * k, r * k
reg = fr.filter(ImageFilter.GaussianBlur(R * 0.6)); m = Image.new('L', fr.size, 0); ImageDraw.Draw(m).ellipse((cx - R, cy - R, cx + R, cy + R), fill=255)
fr = Image.composite(reg, fr, m.filter(ImageFilter.GaussianBlur(R * 0.25)))
can = Image.new('RGB', (1080, 1920), (12, 12, 14))
a = np.ones((fr.height, 1080), np.float32); n = 160
a[:n] *= np.linspace(0, 1, n)[:, None]; a[-n:] *= np.linspace(1, 0, n)[:, None]
can.paste(fr, (0, TOP), Image.fromarray((a * 255).astype(np.uint8)))
g = np.random.default_rng(1).normal(0, 7, (1920, 1080, 1)); can = Image.fromarray(np.clip(np.asarray(can, np.float32) + g, 0, 255).astype(np.uint8))
can.save(D + '/cov/cov.jpg', quality=95); print('ok')
