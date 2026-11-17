# "Die Schlacht um Berlin" CDM Short (9:16): animated map story in the channel style.
# Full-screen dark map; every spoken event is drawn at that moment (arrows, front, ring, pins, counters);
# archive film cards pop in over the map; word-by-word text up top with yellow key words.
import os, sys, json, math, re, functools, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
W, H, FPS = 1080, 1920, 30
OFF = 0.2
WD = json.load(open(B + 'words.json'))
GEO = json.load(open(B + 'geo.json'))
F = '/tmp/claude-0/fonts/'
@functools.lru_cache(None)
def font(n, s): return ImageFont.truetype(F + n + '.ttf', s)
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lerp(a, b, u): return a + (b - a) * u
def eout(u): u = clamp(u); return 1 - (1 - u) ** 3
def eio(u): u = clamp(u); return u * u * (3 - 2 * u)
def _n(w): return re.sub(r'[^a-zäöüß0-9]', '', w.lower())
TOK = [_n(w[0]) for w in WD]
def K(ph, i=0):
    p = [_n(x) for x in ph.split()]; h = [k for k in range(len(TOK) - len(p) + 1) if TOK[k:k + len(p)] == p]
    assert len(h) == 1, (ph, h); return WD[h[0] + i][1] + OFF
T_END = WD[-1][2] + OFF + 1.6
RED, SRED, YEL, BLUE, WHITE = (205, 30, 34), (150, 20, 24), (246, 198, 46), (70, 120, 210), (245, 245, 242)
LAND, WATER, BORDER = (196, 168, 120), (28, 64, 120), (150, 120, 84)

# ---------------- camera over lon/lat ----------------
def my(lat): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
CAM = []          # (t, lon, lat, px_per_deg)
def cam(t):
    if t <= CAM[0][0]: return CAM[0][1:]
    for a, b in zip(CAM, CAM[1:]):
        if a[0] <= t <= b[0]:
            u = eio((t - a[0]) / (b[0] - a[0])); z = math.exp(lerp(math.log(a[3]), math.log(b[3]), u))
            return (lerp(a[1], b[1], u), lerp(a[2], b[2], u), z)
    return CAM[-1][1:]
class P:
    def __init__(s, t): s.lon, s.lat, s.k = cam(t); s.cy = my(s.lat)
    def __call__(s, lon, lat): return (W / 2 + (lon - s.lon) * s.k, H * 0.60 - (my(lat) - s.cy) * s.k)

# ---------------- base map ----------------
NOISE = (np.random.default_rng(3).random((H // 4, W // 4)) * 24 - 12).astype(np.float32)
NOISE = np.asarray(Image.fromarray((NOISE + 128).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) - 128
def basemap(t):
    p = P(t); im = Image.new('RGB', (W, H), WATER); d = ImageDraw.Draw(im)
    for name, pts in GEO['countries']:
        d.polygon([p(*q) for q in pts], fill=LAND)
    for name, pts in GEO['countries']:
        d.line([p(*q) for q in pts] + [p(*pts[0])], fill=BORDER, width=2)
    for name, pts in GEO['lakes']: d.polygon([p(*q) for q in pts], fill=WATER)
    wd = max(2, int(p.k / 120))
    for name, pts in GEO['rivers']:
        big = name in ('Elbe', 'Oder', 'Luzicka Nisa', 'Spree')
        d.line([p(*q) for q in pts], fill=(70, 110, 150) if big else (60, 84, 104), width=wd + (2 if big else 0), joint='curve')
    a = np.asarray(im, np.float32) + NOISE[..., None]
    yy = np.linspace(-1, 1, H)[:, None]; xx = np.linspace(-1, 1, W)[None, :]; v = np.clip(1.12 - 0.38 * (xx ** 2 + yy ** 2), 0.45, 1)
    return Image.fromarray((a * v[..., None]).clip(0, 255).astype(np.uint8)).convert('RGBA')

# ---------------- map elements ----------------
def label(im, t, t0, s, xy, size=40, col=WHITE, anchor='mm', box=None):
    if t < t0: return
    k = eout((t - t0) / 0.25); f = font('Oswald', size); d = ImageDraw.Draw(im)
    x, y = xy; y += 14 * (1 - k)
    if box:
        b = d.textbbox((x, y), s, font=f, anchor=anchor); d.rectangle((b[0] - 12, b[1] - 8, b[2] + 12, b[3] + 8), fill=box + (int(235 * k),))
    d.text((x, y), s, font=f, fill=col + (int(255 * k),), anchor=anchor, stroke_width=0 if box else 4, stroke_fill=(10, 10, 12, int(220 * k)))
def pin(im, t, t0, xy, col=RED, r=12):
    if t < t0: return
    k = eout((t - t0) / 0.3); rr = r * (1.8 - 0.8 * k); d = ImageDraw.Draw(im)
    pul = (t - t0) % 1.4 / 1.4
    if t - t0 > 0.3: d.ellipse((xy[0] - r - 28 * pul, xy[1] - r - 28 * pul, xy[0] + r + 28 * pul, xy[1] + r + 28 * pul), outline=col + (int(200 * (1 - pul)),), width=3)
    d.ellipse((xy[0] - rr, xy[1] - rr, xy[0] + rr, xy[1] + rr), fill=col + (int(255 * k),), outline=WHITE + (int(255 * k),), width=3)
def flagchip(im, xy, kind, k=1.0):
    x, y = xy; d = ImageDraw.Draw(im); w, h = 58, 38; a = int(255 * k)
    if kind == 'us':
        for i in range(7): d.rectangle((x, y + i * h / 7, x + w, y + (i + 1) * h / 7), fill=((190, 30, 40) if i % 2 == 0 else WHITE) + (a,))
        d.rectangle((x, y, x + 26, y + 20), fill=(40, 60, 130, a))
    elif kind == 'su':
        d.rectangle((x, y, x + w, y + h), fill=(200, 20, 24, a)); d.text((x + 8, y + 2), '★', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18), fill=YEL + (a,))
    d.rectangle((x, y, x + w, y + h), outline=(20, 20, 20, a), width=2)
def path_pts(p, pts, n=60):
    Q = [p(*q) for q in pts]; out = []
    for a, b, c in zip([Q[0]] + Q, Q, Q[1:] + [Q[-1]]):
        pass
    # Catmull-Rom through the points
    Q = [Q[0]] + Q + [Q[-1]]
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        for s in range(n // max(1, len(Q) - 3)):
            u = s / (n // max(1, len(Q) - 3))
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u * u + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u ** 3) for j in (0, 1)))
    out.append(Q[-2]); return out
def arrow(im, t, t0, dur, p, pts, col=RED, wd=26, upto=1.0):
    if t < t0: return
    u = eio((t - t0) / dur) * upto; P_ = path_pts(p, pts, 90); n = max(2, int(len(P_) * u))
    seg = P_[:n]; d = ImageDraw.Draw(im)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).line(seg, fill=(0, 0, 0, 150), width=wd + 8, joint='curve'); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d.line(seg, fill=col + (255,), width=wd, joint='curve')
    (ax, ay), (bx, by) = seg[-2], seg[-1]; ang = math.atan2(by - ay, bx - ax); L = wd * 2.2
    d.polygon([(bx + L * 0.9 * math.cos(ang), by + L * 0.9 * math.sin(ang)), (bx + L * math.cos(ang + 2.4), by + L * math.sin(ang + 2.4)), (bx + L * math.cos(ang - 2.4), by + L * math.sin(ang - 2.4))], fill=col + (255,))
def dashed(im, t, t0, dur, a, b, col=YEL, wd=6):
    if t < t0: return
    u = eout((t - t0) / dur); L = math.hypot(b[0] - a[0], b[1] - a[1]); d = ImageDraw.Draw(im); s = 0
    while s < L * u:
        e = min(s + 22, L * u); d.line((a[0] + (b[0] - a[0]) * s / L, a[1] + (b[1] - a[1]) * s / L, a[0] + (b[0] - a[0]) * e / L, a[1] + (b[1] - a[1]) * e / L), fill=col + (255,), width=wd); s += 38
FRONT = [(14.12, 53.9), (14.3, 53.4), (14.62, 52.6), (14.7, 52.3), (14.75, 51.95), (14.85, 51.6), (14.95, 51.2), (15.0, 50.9)]   # Oder-Neisse line
def soviet_area(im, t, t0, p, k_extra=1.0):
    if t < t0: return
    k = eout((t - t0) / 0.8) * k_extra
    poly = [p(*q) for q in FRONT] + [p(17.5, 50.9), p(17.5, 53.9)]
    L = Image.new('L', im.size, 0); ImageDraw.Draw(L).polygon(poly, fill=255)
    yy, xx = np.mgrid[0:H, 0:W]; hatch = ((xx + yy) % 26 < 9).astype(np.uint8) * 255
    A = (np.asarray(L, np.float32) / 255) * (0.28 + 0.32 * (hatch / 255)) * k
    lay = Image.new('RGBA', im.size, SRED + (0,)); lay.putalpha(Image.fromarray((A * 255).astype(np.uint8))); im.alpha_composite(lay)
    ImageDraw.Draw(im).line(poly[:len(FRONT)], fill=RED + (int(255 * k),), width=7, joint='curve')
def ring(im, t, t0, dur, c, rx, ry, col=RED, wd=10, fill_a=0):
    if t < t0: return
    u = eio((t - t0) / dur); n = int(160 * u) + 2; d = ImageDraw.Draw(im)
    pts = [(c[0] + rx * math.cos(-math.pi / 2 + 2 * math.pi * i / 160) * (1 + 0.03 * math.sin(i * 0.4)), c[1] + ry * math.sin(-math.pi / 2 + 2 * math.pi * i / 160) * (1 + 0.03 * math.sin(i * 0.4))) for i in range(n)]
    if fill_a and u >= 1:
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).polygon(pts, fill=col + (fill_a,)); im.alpha_composite(lay)
    d.line(pts, fill=col + (255,), width=wd, joint='curve')
def beams(im, t, t0, src, k=1.0):
    if t < t0: return
    u = eout((t - t0) / 0.6) * k; lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(14):
        a = math.radians(180 + 8 * (i - 6.5) + 3 * math.sin(t * 2 + i)); L = 520 * u
        x0, y0 = src[0] + (i - 7) * 12, src[1] + (i % 3) * 8
        d.polygon([(x0, y0), (x0 + L * math.cos(a - 0.04), y0 + L * math.sin(a - 0.04)), (x0 + L * math.cos(a + 0.04), y0 + L * math.sin(a + 0.04))], fill=(255, 250, 220, int(70 * u)))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(5)))
def smoke(im, t, t0, c, k=1.0):
    if t < t0: return
    u = eout((t - t0) / 1.0) * k; lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); r = np.random.default_rng(4)
    for i in range(18):
        x = c[0] + r.uniform(-260, 120); y = c[1] + r.uniform(-120, 160); s = r.uniform(60, 140) * (0.6 + 0.4 * u) + 10 * math.sin(t + i)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(150, 145, 140, int(80 * u)))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(24)))

# ---------------- film ----------------
def clip_frame(name, t, t0, speed=1.0):
    d = B + 'clip/' + name + '/'; n = len(os.listdir(d)); i = int((t - t0) * FPS * speed) % n + 1
    return Image.open(d + 'f%04d.jpg' % i).convert('RGB')
def tone(im):
    g = np.asarray(ImageEnhance.Contrast(im.convert('L')).enhance(1.18), np.float32)
    return Image.fromarray(np.stack([g * 1.02 + 6, g * 0.98 + 3, g * 0.9], -1).clip(0, 255).astype(np.uint8))
def fullfilm(name, t, t0, z0=1.04, z1=1.12):
    g = clip_frame(name, t, t0); w, h = g.size; z = lerp(z0, z1, clamp((t - t0) / 6)); ch = h / z; cw = ch * W / H
    im = tone(g.resize((W, H), Image.BICUBIC, box=((w - cw) / 2, (h - ch) / 2, (w + cw) / 2, (h + ch) / 2)))
    a = np.asarray(im, np.float32); yy = np.linspace(-1, 1, H)[:, None]; xx = np.linspace(-1, 1, W)[None, :]; v = np.clip(1.1 - 0.42 * (xx ** 2 + yy ** 2), 0.3, 1)
    return Image.fromarray((a * v[..., None]).clip(0, 255).astype(np.uint8)).convert('RGBA')
def card(im, t, t0, t1, name, box=(70, 1000, 840, 560)):
    if t < t0 or t > t1 + 0.25: return
    k = eout((t - t0) / 0.3) * (1 - eout((t - t1) / 0.25)); x, y, w, h = box
    s = lerp(0.82, 1.0, k); cw, ch = int(w * s), int(h * s); cx, cy = x + (w - cw) // 2, y + (h - ch) // 2 + int(60 * (1 - k))
    g = clip_frame(name, t, t0); gw, gh = g.size; sc = max(cw / gw, ch / gh); bw, bh = cw / sc, ch / sc
    ph = tone(g.resize((cw, ch), Image.BICUBIC, box=((gw - bw) / 2, (gh - bh) / 2, (gw + bw) / 2, (gh + bh) / 2))).convert('RGBA')
    sh = Image.new('RGBA', (cw + 80, ch + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((40, 40, cw + 40, ch + 40), fill=(0, 0, 0, int(200 * k))); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (cx - 30, cy - 20))
    fr = Image.new('RGBA', (cw + 16, ch + 16), (238, 234, 224, int(255 * k))); im.alpha_composite(fr, (cx - 8, cy - 8))
    ph.putalpha(int(255 * k)); im.alpha_composite(ph, (cx, cy))

# ---------------- text ----------------
def say(im, t, rows, y0=300, size=96, lh=None, until=None):
    """rows: list of rows, each a list of (word index start phrase, word text, style) ; style 'w' white, 'y' yellow, 'r' red"""
    if until is not None and t > until + 0.2: return
    ko = 1.0 if until is None else 1 - eout((t - until) / 0.2)
    lh = lh or int(size * 1.08); d = ImageDraw.Draw(im); y = y0
    for row in rows:
        f = font('Anton', size); words = [(w, st, ta) for (ta, w, st) in row]
        tw = sum(f.getlength(w + ' ') for w, _, _ in words) - f.getlength(' ')
        sc = min(1.0, (W - 90) / tw); f2 = font('Anton', int(size * sc)); x = (W - min(tw, W - 90)) / 2
        for w, st, ta in words:
            if t >= ta:
                k = eout((t - ta) / 0.16) * ko; col = {'w': WHITE, 'y': YEL, 'r': (255, 70, 60)}[st]
                d.text((x, y + 18 * (1 - k)), w, font=f2, fill=col + (int(255 * k),), stroke_width=7, stroke_fill=(8, 8, 10, int(255 * k)))
            x += f2.getlength(w + ' ')
        y += int(lh * sc) if sc < 1 else lh
def counter(im, t, t0, v, fmt, xy, size=170, col=YEL, dur=0.8):
    if t < t0: return
    u = eout((t - t0) / dur); s = fmt(v * u) if u < 1 else fmt(v); d = ImageDraw.Draw(im)
    d.text(xy, s, font=font('Anton', size), fill=col + (255,), anchor='mm', stroke_width=8, stroke_fill=(8, 8, 10, 255))
def de(v): return '{:,.0f}'.format(v).replace(',', '.')
def stamp(im, t, t0, s, xy, size=110, ang=-7, col=RED):
    if t < t0: return
    u = clamp((t - t0) / 0.15); sc = lerp(1.5, 1.0, eout(u)); f = font('Anton', int(size * sc)); d0 = ImageDraw.Draw(Image.new('L', (1, 1)))
    b = d0.textbbox((0, 0), s, font=f); w, h = b[2] - b[0] + 60, b[3] - b[1] + 50
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.rectangle((4, 4, w - 4, h - 4), outline=col + (255,), width=10); d.text((w / 2, h / 2), s, font=f, fill=col + (255,), anchor='mm')
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC); im.alpha_composite(L, (int(xy[0] - L.width / 2), int(xy[1] - L.height / 2)))

