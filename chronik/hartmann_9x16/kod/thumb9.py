# 9:16 cover (Facebook Reel): 1944 smiling ace above, 1955 returning prisoner below, title in the middle band
import sys
from lib9 import *
OUT = B + 'Thumbnail_9x16_Facebook.jpg'
def badge(can, x, y, h=100):
    f = anton(int(h * 0.82)); d = ImageDraw.Draw(can); wc = d.textlength('C', font=f); gap, pad = h * 0.07, h * 0.06; cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'DM', font=f, anchor='lm')
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x - h * 0.22, y - h * 0.16, b[2] + pad + h * 0.22, y + h * 1.12), h * 0.12, fill=(8, 9, 11, 170))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(can)
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.06, b[2] + pad, b[3] + h * 0.05), fill=YEL)
    d.text((xd, cy), 'DM', font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.12, b[0] + h * 0.42, b[3] + h * 0.16), fill=RED)
def band(n, cx, cy, w, bh):
    im = src(n); h = w * bh / W; x0 = min(max(cx - w / 2, 0), im.width - w); y0 = min(max(cy - h / 2, 0), im.height - h)
    return im.resize((W, bh), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h)).convert('RGBA')
def T(can, xy, s, font, col=WHITE):
    font = shrink(font, s, 980); shadowed(can, lambda d: d.text(xy, s, font=font, fill=col + (255,), anchor='mm'), 14, (5, 9), 230)
can = Image.new('RGBA', (W, H), DARK + (255,))
top = band('h22', 590, 720, 1100, 820); can.alpha_composite(top, (0, 170))
bot = band('h45', 560, 760, 1060, 760); bot = Image.fromarray((np.asarray(bot).astype(np.float32) * np.array([0.92, 0.92, 0.92, 1.0])).astype(np.uint8)); can.alpha_composite(bot, (0, 1060))
g = np.zeros((H, W), np.float32); y = np.arange(H)[:, None]
g = np.clip(1 - np.abs(y - 1025) / 150, 0, 1) * 235 + np.clip((y - 1650) / 200, 0, 1) * 235 + np.clip((260 - y) / 120, 0, 1) * 235
L = Image.new('RGBA', (W, H), (6, 7, 9, 0)); L.putalpha(Image.fromarray(np.repeat(g, W, 1).clip(0, 255).astype(np.uint8))); can.alpha_composite(L)
d = ImageDraw.Draw(can); d.line((0, 1060, W, 1060), fill=YEL, width=8)
for (x, y_, s, bg) in [(150, 230, '1944', YEL), (150, 1110, '1955', WHITE)]:
    f = bebas(70); b = d.textbbox((x, y_), s, font=f, anchor='mm'); d.rectangle((b[0] - 20, b[1] - 10, b[2] + 20, b[3] + 10), fill=bg); d.text((x, y_), s, font=f, fill=DARK, anchor='mm')
badge(can, W / 2 - 75, 60, 92)
T(can, (CX + 20, 960), '352 LUFTSIEGE', anton(150), YEL)
T(can, (CX + 20, 1700), '10 JAHRE GEFANGEN', anton(110), WHITE)
T(can, (CX + 20, 1830), 'ERICH HARTMANN', anton(120), YEL)
can.convert('RGB').save(OUT, quality=93); print('ok')
