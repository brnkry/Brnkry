# Stigler / Brown Shorts: shared helpers (atlas / ink style)
import json, math, functools, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
TEND = 112.77
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
F = B + 'fonts/'
IMG = B + 'img/'

CREAM = (243, 234, 214); INK = (44, 34, 22); RUST = (168, 58, 36); GOLD = (212, 165, 74)
NAVY = (36, 52, 78); PAPER = (231, 219, 190); SEPIA = (92, 66, 40); DEEP = (22, 17, 12)
ZX = 540

WORDS = json.load(open(B + 'words.json'))
def wt(s, after=0.0):
    for w, a, b in WORDS:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a
    raise KeyError(s)

@functools.lru_cache(None)
def font(name, size, w=None):
    f = ImageFont.truetype(F + name, size)
    if w: f.set_variation_by_axes([w])
    return f
# same fonts as the Kammhuber video: Anton, Bebas Neue, Montserrat Italic, Special Elite
FK = {'serif': lambda s: font('Anton-Regular.ttf', s), 'serifm': lambda s: font('Anton-Regular.ttf', s),
      'cond': lambda s: font('BebasNeue-Regular.ttf', int(s * 1.12)), 'condl': lambda s: font('Montserrat-Italic%5Bwght%5D.ttf', s, 800),
      'type': lambda s: font('SpecialElite-Regular.ttf', s)}

def clamp(x): return min(1.0, max(0.0, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2
def lerp(a, b, u): return a + (b - a) * u

def fit(txt, fk, size, maxw, track=0):
    while size > 18 and textw(txt, fk, size, track) > maxw: size -= 2
    return size
def textw(txt, fk, size, track=0):
    f = FK[fk](size); return f.getlength(txt) + track * max(0, len(txt) - 1)

@functools.lru_cache(maxsize=4096)
def sprite(txt, fk, size, color, shadow=True, track=0, blur=0):
    f = FK[fk](size); asc, desc = f.getmetrics()
    w = int(textw(txt, fk, size, track)) + 80; h = asc + desc + 80
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    def draw(d, off, fill):
        x = 40
        if track == 0: d.text((x + off[0], 40 + off[1]), txt, font=f, fill=fill); return
        for ch in txt:
            d.text((x + off[0], 40 + off[1]), ch, font=f, fill=fill); x += f.getlength(ch) + track
    if shadow:
        sh = Image.new('RGBA', (w, h), (0, 0, 0, 0)); draw(ImageDraw.Draw(sh), (0, 4), (8, 5, 2, 200))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(10)))
        sh2 = Image.new('RGBA', (w, h), (0, 0, 0, 0)); draw(ImageDraw.Draw(sh2), (0, 2), (8, 5, 2, 150))
        im = Image.alpha_composite(im, sh2.filter(ImageFilter.GaussianBlur(2)))
    draw(ImageDraw.Draw(im), (0, 0), color)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    return im

def put(can, spr, cx, cy, scale=1.0, alpha=1.0, anchor='c'):
    if alpha <= 0.01 or scale <= 0.01: return
    s = spr
    if abs(scale - 1) > 0.005: s = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.BICUBIC)
    if alpha < 0.999:
        s = s.copy(); s.putalpha(s.getchannel('A').point(lambda v: int(v * alpha)))
    x = int(cx - s.width / 2) if anchor == 'c' else int(cx - 40 * scale)
    paste_clip(can, s, x, int(cy - s.height / 2))
def paste_clip(can, s, x, y):
    sx0, sy0 = max(0, -x), max(0, -y); sx1, sy1 = min(s.width, can.width - x), min(s.height, can.height - y)
    if sx1 <= sx0 or sy1 <= sy0: return
    if (sx0, sy0, sx1, sy1) != (0, 0, s.width, s.height): s = s.crop((sx0, sy0, sx1, sy1))
    can.alpha_composite(s, (x + sx0, y + sy0))

def maxw_at(cy): return 940 if cy < 680 else 760
def safe(cy, size):  # lower zone: shrink a bit, keep within 1470
    return (cy, size) if cy < 680 else (min(cy, 1470), size)

# ---------- text animations (none of these exist in the Kammhuber kit) ----------
def cascade(can, t, t0, txt, fk, size, col, cy, cx=ZX, t1=None, track=2, step=0.035, dur=0.22):
    """letters settle in one after another, small drop + fade"""
    if t < t0 or (t1 is not None and t > t1 + 0.3): return
    size = fit(txt, fk, size, maxw_at(cy), track); f = FK[fk](size)
    total = textw(txt, fk, size, track); x = cx - total / 2
    out = 1.0 if t1 is None else 1 - ease((t - t1) / 0.3)
    for i, ch in enumerate(txt):
        k = eout((t - t0 - i * step) / dur)
        if ch != ' ' and k > 0:
            spr = sprite(ch, fk, size, col)
            can_a = k * out
            put(can, spr, x + f.getlength(ch) / 2, cy - (1 - k) * 22, 1.0, can_a)
        x += f.getlength(ch) + track

def focus(can, t, t0, txt, fk, size, col, cy, cx=ZX, t1=None, dur=0.45, track=0):
    """blur to sharp focus pull with a slight scale settle"""
    if t < t0 or (t1 is not None and t > t1 + 0.3): return
    size = fit(txt, fk, size, maxw_at(cy), track); k = eout((t - t0) / dur)
    r = int(round((1 - k) * 14 / 2)) * 2
    out = 1.0 if t1 is None else 1 - ease((t - t1) / 0.3)
    put(can, sprite(txt, fk, size, col, True, track, r), cx, cy, lerp(1.07, 1.0, k), k * out)

def reveal(can, t, t0, txt, fk, size, col, cy, cx=ZX, t1=None, dur=0.6, track=0):
    """soft-edged left-to-right ink reveal, no bar"""
    if t < t0 or (t1 is not None and t > t1 + 0.3): return
    size = fit(txt, fk, size, maxw_at(cy), track); spr = sprite(txt, fk, size, col, True, track)
    k = eio((t - t0) / dur); out = 1.0 if t1 is None else 1 - ease((t - t1) / 0.3)
    if k < 1:
        m = np.clip((np.arange(spr.width) - (k * (spr.width + 120) - 120)) / -120.0, 0, 1)
        a = (np.asarray(spr.getchannel('A')).astype(np.float32) * m[None, :]).astype(np.uint8)
        spr = spr.copy(); spr.putalpha(Image.fromarray(a))
    put(can, spr, cx, cy, 1.0, out)

def plate(can, t, t0, txt, cy, cx=ZX, size=50, fg=CREAM, bg=(26, 20, 14), edge=GOLD, t1=None, fk='cond', track=3):
    """label plate that opens from the centre outward, thin gold rules above and below"""
    if t < t0 or (t1 is not None and t > t1 + 0.3): return
    size = fit(txt, fk, size, maxw_at(cy) - 70, track)
    tw = textw(txt, fk, size, track); f = FK[fk](size); asc, desc = f.getmetrics()
    k = eout((t - t0) / 0.4); out = 1.0 if t1 is None else 1 - ease((t - t1) / 0.3)
    ww = (tw + 70) * k; hh = asc + desc + 24
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2), fill=bg + (int(215 * out),))
    d.line((cx - ww / 2, cy - hh / 2 - 6, cx + ww / 2, cy - hh / 2 - 6), fill=edge + (int(255 * out),), width=3)
    d.line((cx - ww / 2, cy + hh / 2 + 6, cx + ww / 2, cy + hh / 2 + 6), fill=edge + (int(255 * out),), width=3)
    can.alpha_composite(L)
    ka = clamp((t - t0 - 0.2) / 0.25) * out
    put(can, sprite(txt, fk, size, fg, False, track), cx, cy + 2, 1.0, ka)

def pen_rule(can, t, t0, cy, w, cx=ZX, col=GOLD, dur=0.5, th=6):
    """tapered ink underline drawn by a pen"""
    if t < t0: return
    k = eio((t - t0) / dur); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0 = cx - w / 2; n = 40
    for i in range(int(n * k)):
        u = i / n; th_i = th * math.sin(math.pi * (u * 0.9 + 0.05)) + 1
        xa = x0 + w * u; xb = x0 + w * (u + 1 / n); ya = cy + 3 * math.sin(u * 5)
        d.line((xa, ya, xb, cy + 3 * math.sin((u + 1 / n) * 5)), fill=col + (255,), width=max(1, int(th_i)))
    can.alpha_composite(L)

def seal(can, t, t0, txt, cx, cy, r=170, col=RUST, rot=-12, sub=None):
    """round rubber seal: double ring, text, presses down"""
    if t < t0: return
    k = eout((t - t0) / 0.28)
    S = int(r * 2.4); L = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = S / 2
    d.ellipse((c - r, c - r, c + r, c + r), outline=col + (235,), width=10)
    d.ellipse((c - r + 20, c - r + 20, c + r - 20, c + r - 20), outline=col + (235,), width=4)
    size = fit(txt, 'cond', 74, r * 1.55, 2); f = FK['cond'](size)
    tw = textw(txt, 'cond', size, 2); x = c - tw / 2
    for ch in txt:
        d.text((x, c - size * 0.62 - (14 if sub else 0)), ch, font=f, fill=col + (240,)); x += f.getlength(ch) + 2
    if sub:
        f2 = FK['condl'](int(size * 0.42)); sw = f2.getlength(sub); d.text((c - sw / 2, c + size * 0.38), sub, font=f2, fill=col + (230,))
    # worn ink texture
    rng = np.random.default_rng(3); a = np.asarray(L.getchannel('A')).astype(np.float32)
    a *= (rng.random(a.shape) > 0.12) * 0.25 + 0.75
    L.putalpha(Image.fromarray(a.astype(np.uint8)))
    L = L.rotate(rot, resample=Image.BICUBIC)
    put(can, L, cx, cy, lerp(1.35, 1.0, k), k)

# ---------- annotations on photos ----------
def bez(p0, p1, p2, n=40):
    return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in np.linspace(0, 1, n)]
def partial(pts, u):
    if u <= 0: return pts[:1]
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; L = sum(seg); tg = L * clamp(u); out = [pts[0]]; acc = 0
    for i, s in enumerate(seg):
        if acc + s >= tg:
            f = (tg - acc) / s if s else 0; out.append((lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f))); return out
        out.append(pts[i + 1]); acc += s
    return out
def stroke(can, pts, col, w, outline=True, alpha=1.0):
    if len(pts) < 2: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    if outline: d.line(pts, fill=(10, 7, 4, int(150 * alpha)), width=w + 6, joint='curve')
    d.line(pts, fill=col + (int(255 * alpha),), width=w, joint='curve')
    can.alpha_composite(L)
def arrowhead(can, p, ang, col, s=30, alpha=1.0):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pts = [p, (p[0] - s * math.cos(ang - 0.45), p[1] - s * math.sin(ang - 0.45)), (p[0] - s * math.cos(ang + 0.45), p[1] - s * math.sin(ang + 0.45))]
    d.polygon(pts, fill=col + (int(255 * alpha),), outline=(10, 7, 4, int(150 * alpha)))
    can.alpha_composite(L)
def curved_arrow(can, t, t0, a, ctrl, b, col=CREAM, w=7, dur=0.6):
    if t < t0: return
    pts = bez(a, ctrl, b); k = eio((t - t0) / dur); pp = partial(pts, k)
    stroke(can, pp, col, w)
    if len(pp) >= 2:
        q, r = pp[-2], pp[-1]; arrowhead(can, r, math.atan2(r[1] - q[1], r[0] - q[0]), col, 34)
def ring(can, x, y, r, col, a, w=5):
    if a > 0.01: ImageDraw.Draw(can).ellipse((x - r, y - r, x + r, y + r), outline=col + (int(255 * a),), width=w)
def target_mark(can, t, t0, x, y, col=RUST, r=34):
    """pulsing ring + small cross at a damaged part"""
    if t < t0: return
    k = eout((t - t0) / 0.3)
    for j in range(2):
        u = ((t - t0) * 0.9 + j * 0.5) % 1.0
        ring(can, x, y, r + 50 * u, col, (1 - u) * 0.7 * k, 4)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse((x - r * k, y - r * k, x + r * k, y + r * k), outline=(10, 7, 4, 160), width=10)
    d.ellipse((x - r * k, y - r * k, x + r * k, y + r * k), outline=col + (255,), width=6)
    can.alpha_composite(L)
def callout(can, t, t0, pt, lab_xy, txt, col=RUST, size=46, elbow=None):
    """leader line from a point on the photo to a label; label sits on a dark plate"""
    if t < t0: return
    target_mark(can, t, t0, *pt, col=col)
    sz = fit(txt, 'cond', size, maxw_at(lab_xy[1]) - 70, 3); hw = (textw(txt, 'cond', sz, 3) + 70) / 2
    ex = lab_xy[0] - hw if pt[0] < lab_xy[0] - hw else (lab_xy[0] + hw if pt[0] > lab_xy[0] + hw else pt[0])
    pts = [(pt[0], pt[1] + 36), (pt[0], lab_xy[1])] + ([(ex, lab_xy[1])] if ex != pt[0] else [])
    if ex == pt[0]: pts[-1] = (pt[0], lab_xy[1] - 40)
    k = eio((t - t0 - 0.15) / 0.4)
    stroke(can, partial(pts, k), CREAM, 5)
    if k >= 1: plate(can, t, t0 + 0.55, txt, lab_xy[1], cx=lab_xy[0], size=size, bg=(30, 12, 8), edge=col)
def dash_ellipse(can, t, t0, cx, cy, rx, ry, col=CREAM, dur=0.7, w=6, rot=0):
    if t < t0: return
    k = eio((t - t0) / dur); n = 90
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(int(n * k)):
        if i % 3 == 2: continue
        a0 = -math.pi / 2 + 2 * math.pi * i / n + rot; a1 = a0 + 2 * math.pi / n
        p0 = (cx + rx * math.cos(a0), cy + ry * math.sin(a0)); p1 = (cx + rx * math.cos(a1), cy + ry * math.sin(a1))
        d.line((p0, p1), fill=(10, 7, 4, 140), width=w + 5); d.line((p0, p1), fill=col + (255,), width=w)
    can.alpha_composite(L)

# ---------- photos ----------
# blur spots in source pixels: (x, y, diameter)
BLUR = {'p08': [(790, 60, 210), (540, 2095, 120)],
        'p03': [(852, 1652, 120), (324, 2088, 110), (1425, 2010, 110)],
        'p02': [(1949, 858, 140)]}
def blur_spots(im, spots):
    for x, y, dd in spots:
        r = dd / 2 * 1.1
        box = (int(x - r * 2), int(y - r * 2), int(x + r * 2), int(y + r * 2))
        reg = im.crop(box)
        bl = reg.resize((max(1, reg.width // 7), max(1, reg.height // 7)), Image.BILINEAR).resize(reg.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(max(4, dd * 0.13)))
        m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).ellipse((reg.width / 2 - r, reg.height / 2 - r, reg.width / 2 + r, reg.height / 2 + r), fill=255)
        im.paste(Image.composite(bl, reg, m.filter(ImageFilter.GaussianBlur(r * 0.22))), box[:2])
    return im
@functools.lru_cache(None)
def src(p):
    im = Image.open(IMG + p + '.jpg').convert('RGB')
    return blur_spots(im, BLUR.get(p, []))

class PCam:
    """camera over a source photo: centre (cx, cy) and crop width w in source px (9:16)."""
    def __init__(s, p, cx, cy, w):
        im = src(p); w = min(w, im.width, im.height * 9 / 16); h = w * 16 / 9
        s.x0 = min(max(cx - w / 2, 0), im.width - w); s.y0 = min(max(cy - h / 2, 0), im.height - h); s.w, s.h, s.p = w, h, p
    def frame(s):
        return src(s.p).resize((W, H), Image.BILINEAR, box=(s.x0, s.y0, s.x0 + s.w, s.y0 + s.h)).convert('RGBA')
    def pt(s, x, y): return ((x - s.x0) * W / s.w, (y - s.y0) * H / s.h)
def pcam(p, t, t0, t1, a, b, fn=eio):
    u = fn((t - t0) / max(0.1, t1 - t0))
    w = math.exp(lerp(math.log(a[2]), math.log(b[2]), u))
    return PCam(p, lerp(a[0], b[0], u), lerp(a[1], b[1], u), w)

def vgrad(top_a, bot_a, y0b=1000, y1b=1800, y1t=380):
    y = np.arange(H)
    a = np.clip((y - y0b) / (y1b - y0b), 0, 1) ** 1.3 * bot_a + np.clip((y1t - y) / y1t, 0, 1) * top_a
    g = np.repeat(a[:, None], W, 1).astype(np.uint8)
    return Image.merge('RGBA', [Image.new('L', (W, H), 14), Image.new('L', (W, H), 10), Image.new('L', (W, H), 6), Image.fromarray(g)])
GRAD = vgrad(110, 215)
GRAD_SOFT = vgrad(90, 150)

def print_photo(p, t, t0, t1, rot0=-3.5, rot1=-1.2, wmax=980, bgdark=0.42):
    """photo shown as a paper print with a cream border, dropped onto a blurred, darkened copy of itself"""
    im = src(p)
    bgc = PCam(p, im.width / 2, im.height / 2, 99999).frame().filter(ImageFilter.GaussianBlur(26))
    bgc = Image.blend(bgc, Image.new('RGBA', (W, H), (18, 13, 8, 255)), 1 - bgdark)
    u = eout((t - t0) / 0.7); z = lerp(1.06, 1.0, u) + 0.03 * ease((t - t0) / max(1, t1 - t0))
    pw = int(wmax * z); ph = int(pw * im.height / im.width)
    pr = im.resize((pw, ph), Image.LANCZOS).convert('RGBA')
    bd = 22; card = Image.new('RGBA', (pw + 2 * bd, ph + 2 * bd), CREAM + (255,)); card.paste(pr, (bd, bd))
    sh = Image.new('RGBA', (card.width + 120, card.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((60, 72, 60 + card.width, 72 + card.height), fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(22)); sh.alpha_composite(card, (60, 60))
    sh = sh.rotate(lerp(rot0, rot1, u), resample=Image.BICUBIC, expand=True)
    bgc.alpha_composite(sh, (int(W / 2 - sh.width / 2), int(H * 0.43 - sh.height / 2)))
    return bgc, (W / 2, H * 0.43, pw, ph)

# ---------- paper texture / grading ----------
_rng = np.random.default_rng(5)
_n = Image.fromarray((_rng.normal(128, 30, (H // 4, W // 4))).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3))
PAPER_TEX = np.asarray(_n).astype(np.float32) / 128.0
def paper(col=PAPER, amt=0.07, stains=True):
    a = np.ones((H, W, 3), np.float32) * np.array(col, np.float32)
    a *= (1 + (PAPER_TEX[..., None] - 1) * amt)
    if stains:
        y, x = np.mgrid[0:H, 0:W]; r = np.sqrt(((x - W / 2) / (W * 0.7)) ** 2 + ((y - H / 2) / (H * 0.62)) ** 2)
        a *= (1 - 0.32 * np.clip(r - 0.45, 0, 1) ** 1.4)[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')

def vignette():
    y, x = np.mgrid[0:H, 0:W]; r = np.sqrt(((x - W / 2) / (W * 0.78)) ** 2 + ((y - H / 2) / (H * 0.66)) ** 2)
    a = (np.clip(r - 0.62, 0, 1) * 1.4) ** 1.6 * 200
    return Image.merge('RGBA', [Image.new('L', (W, H), 18), Image.new('L', (W, H), 12), Image.new('L', (W, H), 6), Image.fromarray(a.clip(0, 255).astype(np.uint8))])
VIG = vignette()
