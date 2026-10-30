# Manstein 9:16 covers in the CDM style (logo band on top, name as the biggest line in yellow, swastikas blurred via lib9.src)
#  A: Hamburg 1949, in the dock, 18 years
#  B: the studio portrait with the legend 'der saubere Stratege' struck through
#  no heroic framing: no victories on the cover
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

SAFE = (330, 1450)   # what a phone shows of a 9:16 cover in the feed and the profile grid: all text and the logo stay inside
def photo(can, n, x0, y0, w, top):
    """source box (x0, y0, w wide) scaled to the canvas width, placed from y=top down"""
    im = src(n); s_ = W / w; h = min(im.height - y0, (H - top) / s_)
    p = im.resize((W, int(h * s_)), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h)).convert('RGBA'); can.alpha_composite(p, (0, top)); return s_
def cover_a():   # Hamburg 1949: in the dock
    can = Image.new('RGBA', (W, H), DARK + (255,))
    photo(can, 'm07', 990, 0, 1010, 400)
    grad(can, [(520, 400, 255, 0, 640), (980, 1240, 235, 0, H)])
    d = ImageDraw.Draw(can); badge(can, W / 2 - 75, 330, 92)
    tag(d, 300, 520, 'HAMBURG 1949', YEL)
    T(can, (CX, 1120), 'ERICH VON', 124, WHITE)
    T(can, (CX, 1265), 'MANSTEIN', 210, YEL)
    T(can, (CX, 1405), '18 JAHRE HAFT', 92, RED, bold=1)
    can.convert('RGB').save(OUT + 'DE_A_18_Jahre_Haft.jpg', quality=93)
def cover_b():   # the portrait, with the legend struck through
    can = Image.new('RGBA', (W, H), DARK + (255,))
    photo(can, 'm03', 330, 0, 1140, 400)
    grad(can, [(520, 400, 255, 0, 640), (960, 1200, 235, 0, H)])
    d = ImageDraw.Draw(can); badge(can, W / 2 - 75, 330, 92)
    T(can, (CX, 1120), 'ERICH VON', 124, WHITE)
    T(can, (CX, 1265), 'MANSTEIN', 210, YEL)
    f = anton(84); s_ = 'DER SAUBERE STRATEGE?'
    while f.getlength(s_) > 900: f = anton(f.size - 4)
    T(can, (CX, 1405), s_, f.size, WHITE, bold=1)
    x0 = CX - f.getlength(s_) / 2 + f.getlength('DER '); x1 = x0 + f.getlength('SAUBERE')
    d = ImageDraw.Draw(can); d.line((x0 - 6, 1412, x1 + 6, 1400), fill=RED, width=10)
    can.convert('RGB').save(OUT + 'DE_B_Der_saubere_Stratege.jpg', quality=93)
if __name__ == '__main__': cover_a(); cover_b(); print('ok')
