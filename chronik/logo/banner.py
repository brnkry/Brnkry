# YouTube banner 2560x1440 in style B; all text inside the 1546x423 safe area (visible on every device)
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = sys.argv[1] + '/'; F = D + '../sch/fonts/'
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
W, H = 2560, 1440; SX0, SY0, SX1, SY1 = 507, 508, 2053, 931
anton = lambda s: ImageFont.truetype(F + 'Anton-Regular.ttf', s); bebas = lambda s: ImageFont.truetype(F + 'BebasNeue-Regular.ttf', s)
rng = np.random.default_rng(3)
# dark background, soft light in the middle, film grain
y, x = np.mgrid[0:H, 0:W]; r = np.sqrt(((x - W / 2) / (W * 0.45)) ** 2 + ((y - H / 2) / (H * 0.5)) ** 2)
a = np.ones((H, W, 3)) * np.array(DARK, float) * (1.0 + 0.9 * np.clip(1 - r, 0, 1))[..., None]
a += rng.normal(0, 5, (H, W))[..., None]
can = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(can)
cy = 680
f1 = anton(186); t1 = 'CHRONIK'; t2 = 'DER MACHT'
w1 = d.textlength(t1, font=f1); w2 = d.textlength(t2, font=f1); gap = 48; pad = 34
tot = w1 + gap + w2 + 2 * pad; x0 = W / 2 - tot / 2
d.text((x0, cy), t1, font=f1, fill=WHITE, anchor='lm')
b = d.textbbox((x0 + w1 + gap + pad, cy), t2, font=f1, anchor='lm')
d.rectangle((b[0] - pad, b[1] - 30, b[2] + pad, b[3] + 26), fill=YEL)
d.text((x0 + w1 + gap + pad, cy), t2, font=f1, fill=DARK, anchor='lm')
d.rectangle((b[0] - pad, b[3] + 38, b[0] + 220, b[3] + 50), fill=RED)
d.text((W / 2, 888), 'GESCHICHTE  ·  QUELLEN  ·  ORIGINALAUFNAHMEN', font=bebas(80), fill=(205, 200, 190), anchor='mm')
can.convert('RGB').save(D + 'B_Banner_2560x1440.jpg', quality=95)
# preview with the visible areas: TV (full), desktop (2560x423), phone/safe (1546x423)
p = can.copy(); dp = ImageDraw.Draw(p)
dp.rectangle((0, SY0, W, SY1), outline=(80, 160, 255), width=6); dp.rectangle((SX0, SY0, SX1, SY1), outline=(255, 60, 60), width=6)
p.convert('RGB').resize((1280, 720)).save(D + 'banner_preview.jpg', quality=88)
print('ok', x0, x0 + tot)
