# Chronik der Macht (German) vertical short, adapted from the Chronicle of Power kit: shared helpers (1080x1920), Shorts/Reels safe zones. Channel colours, Anton/Bebas/Special Elite, dark map style.
import math, json, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
F = B + '../sch/fonts/'
W, H, FPS = 1080, 1920, 30
CX, MAXW = 520, 800          # text centre a bit left of the like/comment buttons, max text width
YT, Y1, Y2, Y3 = 420, 1180, 1310, 1435   # top title line (below the top UI), three lower lines (above the caption area)
def shrink(font, s, maxw=None):
    maxw = maxw or MAXW; L_ = font.getlength(s)
    return font if L_ <= maxw else ImageFont.truetype(font.path, max(18, int(font.size * maxw / L_)))
YEL, RED, WHITE, DARK, CREAM, GREY = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18), (232, 226, 210), (190, 196, 204)
@functools.lru_cache(None)
def anton(s): return ImageFont.truetype(F + 'Anton-Regular.ttf', s)
@functools.lru_cache(None)
def bebas(s): return ImageFont.truetype(F + 'BebasNeue-Regular.ttf', s)
@functools.lru_cache(None)
def typew(s): return ImageFont.truetype(F + 'SpecialElite-Regular.ttf', s)
@functools.lru_cache(None)
def oswald(s, wg=700):
    f = ImageFont.truetype(F + 'Oswald%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
@functools.lru_cache(None)
def playfair(s, wg=600):
    f = ImageFont.truetype(F + 'PlayfairDisplay%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
def clamp(x): return max(0.0, min(1.0, x))
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def lerp(a, b, u): return a + (b - a) * u

WORDS = json.load(open(B + 'words.json'))
def wt(s, after=0.0):
    for w, a, b in WORDS:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a
    raise KeyError(s)

# ---------- photos ----------
# German channel: small exact blur on every readable swastika (centre x, centre y, diameter in source px; boxes checked on zoomed crops)
BLUR = {}
@functools.lru_cache(None)
def src(n):
    im = Image.open(B + 'img/' + n + '.jpg').convert('RGB')
    for x, y, d in BLUR.get(n, []):
        r = d / 2; pad = int(d); box = (int(x - pad), int(y - pad), int(x + pad), int(y + pad)); reg = im.crop(box)
        bl = reg.resize((max(1, reg.width // 10), max(1, reg.height // 10)), Image.BILINEAR).resize(reg.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(d * 0.15))
        m = Image.new('L', reg.size, 0); c = reg.width / 2; ImageDraw.Draw(m).ellipse((c - r, c - r, c + r, c + r), fill=255)
        im.paste(Image.composite(bl, reg, m.filter(ImageFilter.GaussianBlur(r * 0.15))), box[:2])
    return im
def crop(n, cx, cy, w, ow=W, oh=H):
    im = src(n); w = min(w, im.width, im.height * ow / oh); h = w * oh / ow
    x0 = min(max(cx - w / 2, 0), im.width - w); y0 = min(max(cy - h / 2, 0), im.height - h)
    return im.resize((ow, oh), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h)).convert('RGBA')
SPEED = 30.0   # screen px per second, always the same, always one direction
def pan(n, t, w0, w1, d=1, cy=0.5, zoom=1.12):
    """landscape photo: fixed framing, slides horizontally at a constant speed for the whole time it is on screen"""
    im = src(n); w = min(im.width, im.height * W / H) / zoom; sc = W / w; need = SPEED * (w1 - w0) / sc
    if im.width - w < need * 0.6: w = max(im.width - need * 0.6, im.width / 1.35); sc = W / w; need = SPEED * (w1 - w0) / sc   # square/narrow photos: zoom in a little so they can still move
    travel = min(need, im.width - w); mid = im.width / 2
    a, b = mid - d * travel / 2, mid + d * travel / 2
    u = clamp((t - w0) / (w1 - w0)); return crop(n, lerp(a, b, u), im.height * cy, w)
@functools.lru_cache(None)
def _bg(n):
    im = src(n); s = max(W / im.width, H / im.height) * 1.15; b = im.resize((int(im.width * s), int(im.height * s)), Image.BILINEAR)
    b = b.crop(((b.width - W) // 2, (b.height - H) // 2, (b.width - W) // 2 + W, (b.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(28))
    return Image.blend(ImageEnhance.Color(b).enhance(0.6), Image.new('RGB', (W, H), (8, 9, 11)), 0.55).convert('RGBA')
def fit(n, t, w0, w1, z1=1.05, top=0.0, blur=0.0):
    """portrait photo: whole picture sharp in the middle (fixed panel), blurred copy behind, slow straight zoom-in inside the panel"""
    im = src(n); can = _bg(n).copy(); u = clamp((t - w0) / (w1 - w0)); z = lerp(1.0, z1, u)
    pw = int(round(im.width * H / im.height)); cw, ch = im.width / z, im.height / z; cy = im.height * (0.5 - top * (1 - 1 / z))
    sh = im.resize((pw, H), Image.BICUBIC, box=(im.width / 2 - cw / 2, cy - ch / 2, im.width / 2 + cw / 2, cy + ch / 2)).convert('RGBA')
    if blur > 0.3: sh = sh.filter(ImageFilter.GaussianBlur(blur))
    can.paste(sh, ((W - pw) // 2, 0), _fmask(pw)); return can
@functools.lru_cache(None)
def _fmask(pw, fe=70):
    m = Image.new('L', (pw, H), 255); dm = ImageDraw.Draw(m)
    for i in range(fe): v = int(255 * i / fe); dm.line((i, 0, i, H), fill=v); dm.line((pw - 1 - i, 0, pw - 1 - i, H), fill=v)
    return m
def shade(can, a=210, start=0.5):
    g = (np.clip((np.arange(H) - H * start) / (H * (1 - start)), 0, 1) ** 1.4 * a).astype(np.uint8)
    L = Image.new('RGBA', (W, H), (6, 7, 9, 0)); L.putalpha(Image.fromarray(np.repeat(g[:, None], W, 1))); can.alpha_composite(L); return can
def dim(can, a): can.alpha_composite(Image.new('RGBA', (W, H), (6, 7, 9, int(a)))); return can

# ---------- text (logo fonts, no plates) ----------
def shadowed(can, fn, blur=12, off=(4, 8), a=210):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(L))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, a), (0, 0), L.getchannel('A'))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), off); can.alpha_composite(L)
def txt(can, t, t0, xy, s, font, col=WHITE, t1=None, rise=16, anchor='mm', dur=0.4):
    if t < t0: return
    font = shrink(font, s); k = eout((t - t0) / dur); out = 1.0 if t1 is None else 1 - clamp((t - t1) / 0.35); a = int(255 * k * out)
    if a > 2: shadowed(can, lambda d: d.text((xy[0], xy[1] + (1 - k) * rise), s, font=font, fill=col + (a,), anchor=anchor))
def words(can, t, parts, cy, size, t1=None, gap=0.28):
    """one line of Anton words, each appearing on its own time: parts = [(word, colour, t0)]"""
    f = anton(size); ws = [f.getlength(p[0]) for p in parts]; g = size * gap; tot = sum(ws) + g * (len(parts) - 1)
    if tot > MAXW: size = int(size * MAXW / tot); f = anton(size); ws = [f.getlength(p[0]) for p in parts]; g = size * gap; tot = sum(ws) + g * (len(parts) - 1)
    x = CX - tot / 2
    for (w_, col, t0), wd in zip(parts, ws):
        txt(can, t, t0, (x, cy), w_, f, col, t1, 22, 'lm', 0.35); x += wd + g
def typewriter(can, t, t0, xy, s, font, col=CREAM, step=0.07, t1=None):
    if t < t0: return
    font = shrink(font, s); n = min(len(s), int((t - t0) / step) + 1); out = 1.0 if t1 is None else 1 - clamp((t - t1) / 0.35)
    cur = '_' if n < len(s) and int(t * 4) % 2 == 0 else ''; x = xy[0] - font.getlength(s) / 2
    shadowed(can, lambda d: d.text((x, xy[1]), s[:n] + cur, font=font, fill=col + (int(255 * out),), anchor='lm'))
def chapter(can, t, t0, num, title, t1):
    """chapter card at the top of the frame; fades out on its own"""
    if t < t0 or t > t1 + 0.5: return
    out = 1 - clamp((t - t1) / 0.5)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    txt(L, t, t0, (CX, 330), f'KAPITEL {num}', bebas(50), YEL, None, 8)
    txt(L, t, t0 + 0.15, (CX, 400), title, anton(78), WHITE, None, 10)
    k = eio((t - t0 - 0.3) / 0.6); ImageDraw.Draw(L).line((CX - 200 * k, 460, CX + 200 * k, 460), fill=YEL + (255,), width=4)
    if out < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * out)))
    can.alpha_composite(L)

# ---------- maps ----------
GJ = json.load(open(B + '../sch/ne50.geojson'))
def merc(lat): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(max(-80, min(82, lat))) / 2)))
ALLP = []
for ft in GJ['features']:
    nm = ft['properties'].get('ADMIN') or ft['properties'].get('NAME'); g = ft['geometry']
    for poly in (g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]):
        rg = np.array(poly[0]); ALLP.append((nm, rg[:, 0], np.array([merc(v) for v in rg[:, 1]]), rg[:, 0].min(), rg[:, 0].max(), rg[:, 1].min(), rg[:, 1].max()))
SEA, LAND, LAND_HI, BORDER, GRID = (9, 12, 17), (34, 40, 50), (60, 54, 26), (88, 100, 116), (15, 20, 27)
class Map:
    def __init__(s, lon, lat, span, hi=(), extra=()):
        s.c = (lon, merc(lat)); s.sc = W / span; s.hi = hi; s.extra = extra
    def p(s, lon, lat, z=1.0):
        x = (lon - s.c[0]) * s.sc + W / 2; y = H / 2 - (merc(lat) - s.c[1]) * s.sc
        return (W / 2 + (x - W / 2) * z, H / 2 + (y - H / 2) * z)
    @functools.lru_cache(None)
    def base(s):
        k = 2; im = Image.new('RGB', (W * k, H * k), SEA); d = ImageDraw.Draw(im); span = W / s.sc
        lon0, lon1 = s.c[0] - span, s.c[0] + span
        step = 5 if span > 12 else 1
        for lon in range(int(lon0) - 1, int(lon1) + 2):
            if lon % step == 0: x = ((lon - s.c[0]) * s.sc + W / 2) * k; d.line((x, 0, x, H * k), fill=GRID, width=2)
        for lat in range(0, 85):
            if lat % step == 0: y = (H / 2 - (merc(lat) - s.c[1]) * s.sc) * k; d.line((0, y, W * k, y), fill=GRID, width=2)
        for nm, xs, ys, a, b_, c, e in ALLP:
            if b_ < lon0 - 5 or a > lon1 + 5: continue
            pts = [(((x - s.c[0]) * s.sc + W / 2) * k, (H / 2 - (y - s.c[1]) * s.sc) * k) for x, y in zip(xs, ys)]
            if len(pts) < 3: continue
            d.polygon(pts, fill=LAND_HI if nm in s.hi else LAND); d.line(pts + [pts[0]], fill=BORDER, width=3)
        for poly, col in s.extra:
            d.polygon([tuple(v * k for v in s.p(*q)) for q in poly], fill=col, outline=BORDER)
        return im.resize((W, H), Image.LANCZOS)
    def frame(s, z=1.0):
        b = s.base(); cw, ch = W / z, H / z
        return b.resize((W, H), Image.BILINEAR, box=(W / 2 - cw / 2, H / 2 - ch / 2, W / 2 + cw / 2, H / 2 + ch / 2)).convert('RGBA')
def poly_fill(can, pts, col, a, outline=True):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.polygon(pts, fill=col + (int(a),))
    if outline: d.line(pts + [pts[0]], fill=col + (min(255, int(a * 1.6)),), width=4)
    can.alpha_composite(L)
def dot(can, x, y, col=YEL, r=11, a=1.0):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse((x - r * 2.4, y - r * 2.4, x + r * 2.4, y + r * 2.4), fill=col + (int(60 * a),)); L = L.filter(ImageFilter.GaussianBlur(r)); d = ImageDraw.Draw(L)
    d.ellipse((x - r, y - r, x + r, y + r), fill=col + (int(255 * a),)); can.alpha_composite(L)
def label(can, t, t0, x, y, s, size=56, col=WHITE, anchor='lm', t1=None):
    txt(can, t, t0, (x, y), s, bebas(size), col, t1, 8, anchor, 0.35)
def arrow(can, a, b, u, col=RED, w=16, head=46, alpha=1.0):
    """thick arrow growing from a to b (u = 0..1), slightly curved"""
    if u <= 0: return
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; nx, ny = -(b[1] - a[1]) * 0.12, (b[0] - a[0]) * 0.12; c = (mx + nx, my + ny)
    pts = [((1 - v) ** 2 * a[0] + 2 * (1 - v) * v * c[0] + v * v * b[0], (1 - v) ** 2 * a[1] + 2 * (1 - v) * v * c[1] + v * v * b[1]) for v in np.linspace(0, u, 30)]
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line(pts, fill=(0, 0, 0, int(150 * alpha)), width=w + 8, joint='curve'); d.line(pts, fill=col + (int(255 * alpha),), width=w, joint='curve')
    e, q = pts[-1], pts[-3]; ang = math.atan2(e[1] - q[1], e[0] - q[0])
    d.polygon([(e[0] + 14 * math.cos(ang), e[1] + 14 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))], fill=col + (int(255 * alpha),))
    can.alpha_composite(L)
def dashed(can, pts, u, col=YEL, w=7, seg=22, head=34):
    if u <= 0: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    tot = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)); goal = tot * u; acc = 0; on = True; tip = pts[0]; ang = 0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]; L_ = math.dist(a, b); s_ = 0
        while s_ < L_ and acc + s_ < goal:
            e = min(L_, s_ + seg, goal - acc); p0 = (lerp(a[0], b[0], s_ / L_), lerp(a[1], b[1], s_ / L_)); p1 = (lerp(a[0], b[0], e / L_), lerp(a[1], b[1], e / L_))
            if on: d.line((p0, p1), fill=(0, 0, 0, 140), width=w + 6); d.line((p0, p1), fill=col + (255,), width=w)
            on = not on; s_ = e; tip = p1; ang = math.atan2(b[1] - a[1], b[0] - a[0])
        acc += L_
    if head:
        hp = [(tip[0] + 12 * math.cos(ang), tip[1] + 12 * math.sin(ang)), (tip[0] - head * math.cos(ang - .5), tip[1] - head * math.sin(ang - .5)), (tip[0] - head * math.cos(ang + .5), tip[1] - head * math.sin(ang + .5))]
        d.polygon(hp, fill=col + (255,), outline=(0, 0, 0, 140))
    can.alpha_composite(L)
def route(lonlat, m, z=1.0, n=24):
    """smooth path through map points (for ship and flight routes)"""
    P = [m.p(*q, z) for q in lonlat]; out = []
    for i in range(len(P) - 1):
        a, b = P[i], P[i + 1]; c = P[i + 2] if i + 2 < len(P) else b; pre = P[i - 1] if i else a
        for k in range(n):
            v = k / n; t1 = ((b[0] - pre[0]) * 0.25, (b[1] - pre[1]) * 0.25); t2 = ((c[0] - a[0]) * 0.25, (c[1] - a[1]) * 0.25)
            h00, h10, h01, h11 = 2*v**3-3*v**2+1, v**3-2*v**2+v, -2*v**3+3*v**2, v**3-v**2
            out.append((h00*a[0]+h10*t1[0]+h01*b[0]+h11*t2[0], h00*a[1]+h10*t1[1]+h01*b[1]+h11*t2[1]))
    out.append(P[-1]); return out
def ring(can, t, t0, x, y, col=RED, r=40, cross=True):
    if t < t0: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); k = eout((t - t0) / 0.4)
    for j in range(3):
        u = ((t - t0) * 0.7 + j / 3) % 1.0; rr = r + 90 * u; d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=col + (int(200 * (1 - u) * k),), width=5)
    d.ellipse((x - r * k, y - r * k, x + r * k, y + r * k), outline=col + (255,), width=8)
    if cross:
        q = r * 0.45 * k; d.line((x - q, y - q, x + q, y + q), fill=col + (255,), width=8); d.line((x - q, y + q, x + q, y - q), fill=col + (255,), width=8)
    can.alpha_composite(L)

# ---------- frame assembly ----------
y_, x_ = np.mgrid[0:H, 0:W]; _r = np.sqrt(((x_ - W / 2) / (W * 0.62)) ** 2 + ((y_ - H / 2) / (H * 0.62)) ** 2)
VIG = Image.new('RGBA', (W, H), (0, 0, 0, 0)); VIG.putalpha(Image.fromarray((np.clip(_r - 0.6, 0, 1) * 1.5 * 170).clip(0, 255).astype(np.uint8)))
_rng = np.random.default_rng(3)
def assemble(SC, t, T):
    act = [s for s in SC if s[0] <= t < s[1]] or [SC[-1]]
    img = act[0][2](t, act[0][0], act[0][1])
    if len(act) > 1: img = Image.blend(img, act[1][2](t, act[1][0], act[1][1]), eio((t - act[1][0]) / (act[0][1] - act[1][0])))
    img.alpha_composite(VIG)
    fade = clamp(1 - t / 0.5) if t < 0.5 else clamp((t - (T - 0.8)) / 0.8)
    if fade > 0: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * fade))))
    a = np.asarray(img.convert('RGB')).astype(np.int16) + _rng.normal(0, 3, (H, W))[..., None].astype(np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

# ---------- more graphics ----------
def blurred(n, t, w0, w1, t_sharp, mode='fit', **kw):
    """photo that starts out of focus and sharpens at t_sharp"""
    r = 22 * (1 - eio((t - t_sharp) / 0.9))
    if mode == 'fit': return fit(n, t, w0, w1, blur=r, **kw)
    im = pan(n, t, w0, w1, **kw); return im.filter(ImageFilter.GaussianBlur(r)) if r > 0.3 else im
def stamp(can, t, t0, s, xy, col=RED, size=96, rot=-12):
    """rubber stamp: double frame, worn ink, presses down"""
    if t < t0: return
    k = eout((t - t0) / 0.25); f = anton(size); tw = f.getlength(s); bw, bh = tw + size * 0.8, size * 1.55
    L = Image.new('RGBA', (int(bw + 40), int(bh + 40)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((20, 20, 20 + bw, 20 + bh), outline=col + (235,), width=10); d.rectangle((34, 34, 6 + bw, 6 + bh), outline=col + (235,), width=3)
    d.text((20 + bw / 2, 20 + bh / 2 + 4), s, font=f, fill=col + (240,), anchor='mm')
    a = np.asarray(L.getchannel('A')).astype(np.float32); rr = np.random.default_rng(len(s)); a *= (rr.random(a.shape) > 0.15) * 0.3 + 0.7
    L.putalpha(Image.fromarray(a.astype(np.uint8))); L = L.rotate(rot, expand=True, resample=Image.BICUBIC)
    sc = lerp(1.6, 1.0, k); L = L.resize((max(1, int(L.width * sc)), max(1, int(L.height * sc))), Image.BICUBIC)
    if k < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * k)))
    can.alpha_composite(L, (int(xy[0] - L.width / 2), int(xy[1] - L.height / 2)))
def doc(can, t, t0, lines, cx=CX, cy=H / 2, w=820, t1=None):
    """aged paper sheet sliding in; typewriter lines [(text, size, colour)]"""
    if t < t0: return
    k = eout((t - t0) / 0.5); out = 1.0 if t1 is None else 1 - clamp((t - t1) / 0.4)
    h = 120 + sum(sz * 1.5 for _, sz, _ in lines); L = Image.new('RGBA', (int(w + 60), int(h + 60)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((36, 40, 30 + w, 36 + h), fill=(0, 0, 0, 120)); L = L.filter(ImageFilter.GaussianBlur(12)); d = ImageDraw.Draw(L)
    d.rectangle((30, 30, 30 + w, 30 + h), fill=(226, 216, 192, 255)); d.rectangle((30, 30, 30 + w, 30 + h), outline=(150, 135, 105, 255), width=3)
    y = 90; tt = t - t0 - 0.45
    for txt_, sz, col in lines:
        n = max(0, min(len(txt_), int(tt / 0.028))); tt -= len(txt_) * 0.028 + 0.1
        d.text((30 + w / 2, y + sz * 0.5), txt_[:n], font=shrink(typew(sz), txt_, w - 60), fill=col + (255,), anchor='mm'); y += sz * 1.5
    L = L.rotate(-2.5, expand=True, resample=Image.BICUBIC)
    if out * k < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * out * k)))
    can.alpha_composite(L, (int(cx - L.width / 2), int(cy - L.height / 2 + (1 - k) * 80)))
def counter(can, t, t0, a, b, xy, size=200, col=WHITE, dur=1.4, fmt='{:,}', suffix=''):
    if t < t0: return
    v = int(round(lerp(a, b, eio((t - t0) / dur)))); s = fmt.format(v).replace(',', '.') + suffix
    shadowed(can, lambda d: d.text(xy, s, font=anton(size), fill=col + (255,), anchor='mm'))
def ship(can, x, y, ang, s=60, col=WHITE):
    L = Image.new('RGBA', (s * 2, s * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = s
    d.polygon([(c - s * 0.8, c - s * 0.18), (c + s * 0.55, c - s * 0.18), (c + s * 0.85, c), (c + s * 0.55, c + s * 0.18), (c - s * 0.8, c + s * 0.18)], fill=col + (255,))
    d.rectangle((c - s * 0.35, c - s * 0.1, c + s * 0.1, c + s * 0.1), fill=DARK + (255,))
    L = L.rotate(-math.degrees(ang), resample=Image.BICUBIC); can.alpha_composite(L, (int(x - s), int(y - s)))
