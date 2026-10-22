# Manstein 9:16 covers in the CDM style (logo band on top, name as the biggest line in yellow, swastikas blurred via lib9.src)
#  A: 1940 victor above, 1949 defendant below (like the Hartmann cover)
#  B: the studio portrait with the birth name written on the uniform and struck through, as in the video
import sys
from lib9 import *
OUT = B + 'thumbs/'
os.makedirs(OUT, exist_ok=True)
def badge(can, x, y, h=100):
    f = anton(int(h * 0.82)); d = ImageDraw.Draw(can); wc = d.textlength('C', font=f); gap, pad = h * 0.07, h * 0.06; cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'DM', font=f, anchor='lm')
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.06, b[2] + pad, b[3] + h * 0.05), fill=YEL)
    d.text((xd, cy), 'DM', font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.12, b[0] + h * 0.42, b[3] + h * 0.16), fill=RED)
def band(n, x0, y0, w, bh):
    im = src(n); h = w * bh / W
    return im.resize((W, bh), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h)).convert('RGBA')
def T(can, xy, s, size, col=WHITE, maxw=1000, bold=2):
    f = anton(size)
    while f.getlength(s) + 2 * bold > maxw: f = anton(f.size - 4)
    shadowed(can, lambda d: d.text(xy, s, font=f, fill=col + (255,), anchor='mm', stroke_width=bold, stroke_fill=col + (255,)), 14, (5, 9), 230)
def grad(can, rows):
    """rows: (a, b, k, y0, y1): darkness ramps from 0 at y=a to k at y=b, only between y0 and y1"""
    g = np.zeros(H, np.float32); y = np.arange(H)
    for a, b, k, y0, y1 in rows: g = np.maximum(g, np.clip((y - a) / (b - a), 0, 1) * k * ((y >= y0) & (y < y1)))
    L = Image.new('RGBA', (W, H), (6, 7, 9, 0)); L.putalpha(Image.fromarray(np.repeat(g[:, None], W, 1).astype(np.uint8))); can.alpha_composite(L)
def tag(d, x, y, s, bg):
    f = bebas(70); b = d.textbbox((x, y), s, font=f, anchor='mm'); d.rectangle((b[0] - 20, b[1] - 10, b[2] + 20, b[3] + 10), fill=bg); d.text((x, y), s, font=f, fill=DARK, anchor='mm')

def cover_a():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    can.alpha_composite(band('m03', 330, 0, 1150, 890), (0, 170))      # face and collar, 1940s portrait
    can.alpha_composite(band('m07', 980, 40, 1000, 860), (0, 1060))    # Hamburg 1949, in the dock
    grad(can, [(720, 1040, 230, 0, 1060), (260, 170, 220, 0, 1060), (1460, 1760, 240, 1060, H), (1140, 1060, 160, 1060, H)])
    d = ImageDraw.Draw(can); d.line((0, 1060, W, 1060), fill=YEL, width=8)
    tag(d, 150, 230, '1940', YEL); tag(d, 150, 1110, '1949', WHITE)
    badge(can, W / 2 - 75, 50, 92)
    T(can, (CX + 20, 960), 'SIEG IN 6 WOCHEN', 130, WHITE)
    T(can, (CX + 20, 1650), '18 JAHRE HAFT', 110, RED, bold=1)
    T(can, (CX + 20, 1810), 'ERICH VON MANSTEIN', 150, YEL)
    can.convert('RGB').save(OUT + 'DE_A_Sieg_und_Haft.jpg', quality=93)

def cover_b():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    im = src('m03'); s = 1750 / im.height; w = int(im.width * s); p = im.resize((w, 1750), Image.LANCZOS).convert('RGBA')
    can.alpha_composite(p.crop(((w - W) // 2 + 30, 0, (w - W) // 2 + 30 + W, 1750)), (0, 170))
    grad(can, [(1250, 1620, 245, 0, H), (260, 170, 220, 0, H)])
    d = ImageDraw.Draw(can); badge(can, W / 2 - 75, 50, 92)
    # the birth name, handwritten on the uniform (left chest) and struck through in red, as in the video
    def toS(x, y): return ((x - (im.width - W / s) / 2 - 30 / s) * s, y * s + 170)
    f = ImageFont.truetype(F + 'Caveat.ttf', 66)
    try: f.set_variation_by_axes([650])
    except Exception: pass
    x, y = toS(290, 1430)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(L); dl.text((x, y), 'Fritz Erich', font=f, fill=CREAM + (240,), anchor='lm'); dl.text((x, y + 70), 'von Lewinski', font=f, fill=CREAM + (240,), anchor='lm')
    wl = f.getlength('von Lewinski'); dl.line((x - 8, y + 78, x + wl + 8, y + 66), fill=RED + (250,), width=9)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 200), (0, 0), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), (2, 5)); can.alpha_composite(L)
    T(can, (CX, 1500), 'DER SAUBERE STRATEGE?', 96, WHITE, bold=1)
    a, b_ = anton(96), 'DER SAUBERE STRATEGE?'; tw = a.getlength(b_); x0 = CX - tw / 2 + a.getlength('DER '); x1 = x0 + a.getlength('SAUBERE')
    d = ImageDraw.Draw(can); d.line((x0 - 6, 1506, x1 + 6, 1494), fill=RED, width=11)
    T(can, (CX, 1650), 'ERICH VON', 130, WHITE)
    T(can, (CX, 1800), 'MANSTEIN', 190, YEL)
    can.convert('RGB').save(OUT + 'DE_B_Der_saubere_Stratege.jpg', quality=93)
if __name__ == '__main__': cover_a(); cover_b(); print('ok')
