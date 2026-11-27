# six 16:9 covers for the long Bäke film: three ideas, two photos each.
# Text left, portrait right; the bottom-right corner stays free of text (duration badge).
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/baeke/kod')
import blur as ee
ee.load_img = ee.load
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
W, H = 1280, 720; FD = '/tmp/claude-0/fonts/'; anton = lambda z: ImageFont.truetype(FD + 'Anton.ttf', z)
YEL, RED, WHITE, DARK = (244, 196, 22), (200, 22, 26), (246, 244, 238), (14, 14, 16)
O = '/home/user/Brnkry/chronik/baeke/thumbnails/'
def cover(im, w, h, fx=.5, fy=.5):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
def base(bgkey, tint):
    bg = ImageOps.grayscale(cover(ee.load_img(bgkey), W, H)).filter(ImageFilter.GaussianBlur(3)); g = np.asarray(bg, np.float32) * 0.38
    t = np.array(tint, np.float32) / 255; return Image.fromarray((g[..., None] * (0.55 + t) + 6).clip(0, 255).astype(np.uint8)).convert('RGBA')
def portrait(c, key, pw, fx, fy, zoom=1.0):
    im = ee.load_img(key); p = cover(im, int(pw / zoom), int(H / zoom), fx, fy).resize((pw, H), Image.LANCZOS)
    m = np.clip(np.arange(pw)[None, :] / 160, 0, 1).repeat(H, 0); c.paste(p.convert('RGBA'), (W - pw, 0), Image.fromarray((m * 255).astype(np.uint8)))
def shade(c, w0=0.6, a=215):
    x = np.arange(W, dtype=np.float32)[None, :]; g = np.clip((W * w0 - x) / (W * w0), 0, 1) ** 0.7 * a
    L = Image.new('RGBA', (W, H), (6, 6, 8, 0)); L.putalpha(Image.fromarray(np.broadcast_to(g, (H, W)).astype(np.uint8))); c.alpha_composite(L)
def st(c, xy, s, f, col):
    T = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(T).text(xy, s, font=f, fill=col + (255,))
    S = Image.new('RGBA', c.size, (0, 0, 0, 0)); S.paste((0, 0, 0, 240), (0, 0), T.getchannel('A')); c.alpha_composite(S.filter(ImageFilter.GaussianBlur(10)), (4, 6)); c.alpha_composite(T)
def fit(s, w, z):
    while anton(z).getlength(s) > w: z -= 2
    return anton(z)
def plate(c, y, s, maxw, z=60):
    f = fit(s, maxw, z); d = ImageDraw.Draw(c); b = d.textbbox((60, y), s, font=f); px, py = 20, 10
    d.rectangle((b[0] - px, b[1] - py, b[2] + px, b[3] + py), fill=YEL); d.text((60, y), s, font=f, fill=DARK)
    d.rectangle((b[0] - px, b[3] + py + 8, b[0] - px + 150, b[3] + py + 16), fill=RED)
def logo(c):
    d = ImageDraw.Draw(c); fl = anton(44); x0, y0 = 48, 30
    d.rounded_rectangle((x0 - 12, y0 - 8, x0 + 120, y0 + 58), 6, fill=(8, 9, 11, 210)); d.text((x0, y0 + 25), 'C', font=fl, fill=WHITE, anchor='lm')
    bb = d.textbbox((x0 + 34, y0 + 25), 'DM', font=fl, anchor='lm'); d.rectangle((bb[0] - 4, bb[1] - 4, bb[2] + 4, bb[3] + 4), fill=YEL); d.text((x0 + 34, y0 + 25), 'DM', font=fl, fill=DARK, anchor='lm')
def make(name, bgkey, tint, pkey, pw, fx, fy, lines, plate_txt, zoom=1.0):
    c = base(bgkey, tint); portrait(c, pkey, pw, fx, fy, zoom); shade(c)
    maxw = W - pw + 60; tot = sum(int(fit(a, maxw, b).size * 1.18) for a, b, _ in lines) + 110; y = max(115, (H - tot) // 2 + 10)
    for s, z, col in lines:
        f = fit(s, maxw, z); st(c, (48, y), s, f, col); y += int(f.size * 1.18)
    plate(c, y + 25, plate_txt, maxw - 40); logo(c); c.convert('RGB').save(O + name, quality=94); print(name)
A = [('VOM ZAHNARZT', 118, WHITE), ('ZUM PANZERGENERAL', 104, YEL)]
B = [('ER BOHRTE ZÄHNE', 112, WHITE), ('DANN FÜHRTE', 112, WHITE), ('ER TIGER', 140, YEL)]
C = [('DER ZAHNARZT', 124, WHITE), ('MIT DEN', 110, WHITE), ('TIGERN', 160, YEL)]
make('Baeke_A1_Zahnarzt_Panzergeneral.jpg', 3, (40, 60, 90), 22, 600, .5, .0, A, 'DR. FRANZ BÄKE')
make('Baeke_A2_Zahnarzt_Panzergeneral.jpg', 7, (60, 45, 30), 17, 580, .6, .0, A, 'DR. FRANZ BÄKE')
make('Baeke_B1_Bohrte_Zaehne.jpg', 4, (90, 30, 25), 15, 580, .5, .0, B, 'DIE GESCHICHTE VON FRANZ BÄKE')
make('Baeke_B2_Bohrte_Zaehne.jpg', 8, (50, 50, 60), 21, 580, .5, .0, B, 'DIE GESCHICHTE VON FRANZ BÄKE')
make('Baeke_C1_Zahnarzt_Tiger.jpg', 7, (40, 55, 80), 0, 580, .5, .0, C, 'SCHWERES PANZER-REGIMENT BÄKE')
make('Baeke_C2_Zahnarzt_Tiger.jpg', 3, (70, 50, 30), 14, 580, .5, .0, C, 'SCHWERES PANZER-REGIMENT BÄKE')
