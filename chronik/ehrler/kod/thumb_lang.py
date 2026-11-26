# 16:9 cover for the long Ehrler film: the capsized Tirpitz dark behind, Ehrler's portrait right, text left (bottom right kept clear for the duration badge)
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/ehrler/kod')
import ee
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
W, H = 1280, 720; FD = '/tmp/claude-0/fonts/'; anton = lambda z: ImageFont.truetype(FD + 'Anton.ttf', z)
YEL, RED, WHITE, DARK = (244, 196, 22), (200, 22, 26), (246, 244, 238), (14, 14, 16)
def cover(im, w, h, fx=.5, fy=.5):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
bg = ImageOps.grayscale(cover(ee.load_img(3), W, H)); g = np.asarray(bg, np.float32) * 0.5
c = Image.fromarray(np.stack([g * 1.05 + 8, g * 0.97 + 6, g * 0.85 + 4], -1).clip(0, 255).astype(np.uint8)).convert('RGBA')
p = cover(ee.load_img(12), 560, H, .5, .0); m = np.ones((H, 560), np.float32); m *= np.clip(np.arange(560)[None, :] / 140, 0, 1)
c.paste(p.convert('RGBA'), (W - 560, 0), Image.fromarray((m * 255).astype(np.uint8)))
x = np.arange(W, dtype=np.float32)[None, :]; a = np.clip((W * 0.62 - x) / (W * 0.62), 0, 1) ** 0.8 * 200
L = Image.new('RGBA', (W, H), (8, 8, 10, 0)); L.putalpha(Image.fromarray(np.broadcast_to(a, (H, W)).astype(np.uint8))); c.alpha_composite(L)
def st(xy, s, f, col):
    T = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(T).text(xy, s, font=f, fill=col + (255,))
    S = Image.new('RGBA', c.size, (0, 0, 0, 0)); S.paste((0, 0, 0, 240), (0, 0), T.getchannel('A')); c.alpha_composite(S.filter(ImageFilter.GaussianBlur(10)), (4, 6)); c.alpha_composite(T)
def fit(s, w, z):
    while anton(z).getlength(s) > w: z -= 2
    return anton(z)
st((48, 120), 'SEIN LETZTER', fit('SEIN LETZTER', 680, 130), WHITE); st((48, 270), 'FUNKSPRUCH', fit('FUNKSPRUCH', 680, 150), YEL)
f = fit('RAMMTE ER WIRKLICH?', 640, 74); d = ImageDraw.Draw(c); b = d.textbbox((60, 490), 'RAMMTE ER WIRKLICH?', font=f); px, py = 22, 10
d.rectangle((b[0] - px, b[1] - py, b[2] + px, b[3] + py), fill=YEL); d.text((60, 490), 'RAMMTE ER WIRKLICH?', font=f, fill=DARK); d.rectangle((b[0] - px, b[3] + py + 8, b[0] - px + 150, b[3] + py + 16), fill=RED)
d = ImageDraw.Draw(c); fl = anton(44); x0, y0 = 48, 30
d.rounded_rectangle((x0 - 12, y0 - 8, x0 + 120, y0 + 58), 6, fill=(8, 9, 11, 210)); d.text((x0, y0 + 25), 'C', font=fl, fill=WHITE, anchor='lm')
bb = d.textbbox((x0 + 34, y0 + 25), 'DM', font=fl, anchor='lm'); d.rectangle((bb[0] - 4, bb[1] - 4, bb[2] + 4, bb[3] + 4), fill=YEL); d.text((x0 + 34, y0 + 25), 'DM', font=fl, fill=DARK, anchor='lm')
c.convert('RGB').save('/home/user/Brnkry/chronik/ehrler/thumbnails/DE_Ehrler_Lang.jpg', quality=94); print('ok')
