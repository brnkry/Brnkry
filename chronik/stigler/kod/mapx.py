# old-atlas map: parchment land, slate sea, sepia ink borders, rust routes
import json, math, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from base import *

SEA = (150, 166, 165); SEA_D = (126, 143, 144); LAND = (226, 210, 172); LAND_HI = (208, 180, 126); BORDER = (112, 84, 52); GRID = (120, 110, 90)

def merc(lat): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
GJ = json.load(open(B + 'ne50.geojson'))
POLYS = []
for ft in GJ['features']:
    name = ft['properties'].get('ADMIN') or ft['properties'].get('NAME')
    g = ft['geometry']; cs = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    for poly in cs:
        rg = np.array(poly[0])
        if rg[:, 0].max() < -170 or rg[:, 0].min() > 60 or rg[:, 1].max() < -60 or rg[:, 1].min() > 84: continue
        xy = np.stack([rg[:, 0], np.degrees(np.log(np.tan(np.pi / 4 + np.radians(np.clip(rg[:, 1], -75, 82)) / 2)))], 1)
        POLYS.append((name, xy))

class Cam:
    def __init__(s, lon, lat, span): s.x, s.y, s.sc = lon, merc(lat), W / span
    def p(s, lon, lat): return (W / 2 + (lon - s.x) * s.sc, H / 2 - (merc(lat) - s.y) * s.sc)
def camlerp(a, b, u): return (lerp(a[0], b[0], u), lerp(a[1], b[1], u), math.exp(lerp(math.log(a[2]), math.log(b[2]), u)))

@functools.lru_cache(maxsize=48)
def _map(cx, cy, sp, hi):
    cam = Cam(cx, cy, sp); S = 2
    im = Image.new('RGB', (W * S, H * S), SEA); d = ImageDraw.Draw(im)
    step = 5 if sp < 40 else 15
    for lon in range(-180, 180, step):
        x = (W / 2 + (lon - cam.x) * cam.sc) * S
        if -10 < x < W * S + 10: d.line([(x, 0), (x, H * S)], fill=SEA_D, width=S)
    for lat in range(0, 85, step):
        y = (H / 2 - (merc(lat) - cam.y) * cam.sc) * S
        if -10 < y < H * S + 10: d.line([(0, y), (W * S, y)], fill=SEA_D, width=S)
    # coastal halo (old engraved maps): draw land slightly enlarged in darker sea first
    for name, xy in POLYS:
        X = (W / 2 + (xy[:, 0] - cam.x) * cam.sc) * S; Y = (H / 2 - (xy[:, 1] - cam.y) * cam.sc) * S
        if X.max() < 0 or X.min() > W * S or Y.max() < 0 or Y.min() > H * S or len(X) < 3: continue
        d.line(list(zip(X.tolist(), Y.tolist())), fill=(136, 154, 153), width=22 * S // 2)
    for name, xy in POLYS:
        X = (W / 2 + (xy[:, 0] - cam.x) * cam.sc) * S; Y = (H / 2 - (xy[:, 1] - cam.y) * cam.sc) * S
        if X.max() < 0 or X.min() > W * S or Y.max() < 0 or Y.min() > H * S or len(X) < 3: continue
        pts = list(zip(X.tolist(), Y.tolist()))
        d.polygon(pts, fill=LAND_HI if name in hi else LAND)
        d.line(pts + [pts[0]], fill=BORDER, width=3)
    im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) * (1 + (PAPER_TEX[..., None] - 1) * 0.10)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def draw_map(c, hi=()):
    return _map(round(c[0], 3), round(c[1], 3), round(c[2], 3), tuple(hi)).convert('RGBA'), Cam(*c)

def ink_dot(can, x, y, r=9, col=INK):
    d = ImageDraw.Draw(can); d.ellipse((x - r - 4, y - r - 4, x + r + 4, y + r + 4), fill=PAPER + (255,)); d.ellipse((x - r, y - r, x + r, y + r), fill=col + (255,))
def maplabel(can, t, t0, txt, x, y, size=46, col=INK, side='r', fk='cond', track=4):
    if t < t0: return
    k = eout((t - t0) / 0.35); spr = sprite(txt, fk, size, col, False, track)
    halo = sprite(txt, fk, size, PAPER, False, track, 5)
    w = spr.width - 80
    cx = x + 22 + w / 2 if side == 'r' else (x - 22 - w / 2 if side == 'l' else x)
    put(can, halo, cx, y, 1, k * 0.9); put(can, halo, cx, y, 1, k * 0.9); put(can, spr, cx, y, 1, k)

def route(can, pts, u, col=RUST, w=8, dashed=False, alpha=1.0):
    pp = partial(pts, u)
    if len(pp) < 2: return pp
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    if dashed:
        tot = 0
        for i in range(len(pp) - 1):
            a, b = pp[i], pp[i + 1]; s = math.dist(a, b); n = max(1, int(s / 6))
            for k in range(n):
                if int((tot + k * s / n) / 26) % 2 == 0:
                    d.line([(lerp(a[0], b[0], k / n), lerp(a[1], b[1], k / n)), (lerp(a[0], b[0], (k + 1) / n), lerp(a[1], b[1], (k + 1) / n))], fill=col + (int(255 * alpha),), width=w)
            tot += s
    else: d.line(pp, fill=col + (int(255 * alpha),), width=w, joint='curve')
    can.alpha_composite(L); return pp

def heading(pp):
    if len(pp) < 2: return 0
    a, b = pp[-2], pp[-1]; return math.atan2(b[1] - a[1], b[0] - a[0])

@functools.lru_cache(maxsize=256)
def _b17(size, deg, col):
    S = size * 2; L = Image.new('RGBA', (S * 2, S * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = S; s = S * 0.9
    # nose points to +x
    d.ellipse((c - s * 0.9, c - s * 0.075, c + s * 0.95, c + s * 0.075), fill=col)                       # fuselage
    d.polygon([(c + s * 0.22, c), (c + s * 0.05, c - s * 1.0), (c - s * 0.18, c - s * 0.98), (c - s * 0.12, c),
               (c - s * 0.18, c + s * 0.98), (c + s * 0.05, c + s * 1.0)], fill=col)                     # wings
    for e in (-0.72, -0.38, 0.38, 0.72):
        d.ellipse((c + s * 0.05 - s * 0.02 * abs(e), c + e * s - s * 0.06, c + s * 0.32, c + e * s + s * 0.06), fill=col)   # engines
    d.polygon([(c - s * 0.72, c), (c - s * 0.80, c - s * 0.42), (c - s * 0.92, c - s * 0.40), (c - s * 0.9, c),
               (c - s * 0.92, c + s * 0.40), (c - s * 0.80, c + s * 0.42)], fill=col)                    # tailplane
    L = L.rotate(-deg, resample=Image.BICUBIC).resize((size * 2, size * 2), Image.LANCZOS)
    return L
@functools.lru_cache(maxsize=256)
def _bf109(size, deg, col):
    S = size * 2; L = Image.new('RGBA', (S * 2, S * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = S; s = S * 0.9
    d.polygon([(c + s * 0.95, c), (c + s * 0.6, c - s * 0.1), (c - s * 0.85, c - s * 0.05), (c - s * 0.85, c + s * 0.05), (c + s * 0.6, c + s * 0.1)], fill=col)
    d.polygon([(c + s * 0.35, c - s * 0.08), (c + s * 0.12, c - s * 0.85), (c - s * 0.08, c - s * 0.82), (c - s * 0.05, c - s * 0.06),
               (c - s * 0.05, c + s * 0.06), (c - s * 0.08, c + s * 0.82), (c + s * 0.12, c + s * 0.85), (c + s * 0.35, c + s * 0.08)], fill=col)
    d.polygon([(c - s * 0.62, c), (c - s * 0.72, c - s * 0.32), (c - s * 0.84, c - s * 0.30), (c - s * 0.82, c), (c - s * 0.84, c + s * 0.30), (c - s * 0.72, c + s * 0.32)], fill=col)
    L = L.rotate(-deg, resample=Image.BICUBIC).resize((size * 2, size * 2), Image.LANCZOS)
    return L
def icon(can, kind, x, y, ang, size=46, col=NAVY, alpha=1.0, halo=True):
    deg = int(round(math.degrees(ang) / 3) * 3)
    spr = (_b17 if kind == 'b17' else _bf109)(size, deg, col + (255,))
    if halo:
        hl = (_b17 if kind == 'b17' else _bf109)(size, deg, PAPER + (255,)).filter(ImageFilter.GaussianBlur(4))
        put(can, hl, x, y, 1.0, alpha); put(can, hl, x, y, 1.0, alpha)
    put(can, spr, x, y, 1.0, alpha)

def flak(can, t, t0, x, y, r=26):
    """ink-blot flak burst: dark core, expanding ragged ring, slow fade"""
    if t < t0 or t > t0 + 2.6: return
    u = (t - t0) / 2.6; k = eout((t - t0) / 0.25)
    L = Image.new('RGBA', (int(r * 6), int(r * 6)), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = r * 3
    rr = r * (0.6 + 0.9 * eout(u * 1.6))
    rng = np.random.default_rng(int(x * 7 + y))
    for i in range(7):
        ox, oy = rng.normal(0, rr * 0.35, 2); q = rr * rng.uniform(0.45, 0.8)
        d.ellipse((c + ox - q, c + oy - q, c + ox + q, c + oy + q), fill=(48, 40, 34, int(200 * k * (1 - u) ** 0.8)))
    L = L.filter(ImageFilter.GaussianBlur(3))
    if u < 0.2:
        d = ImageDraw.Draw(L); q = r * 0.35 * (1 - u * 5); d.ellipse((c - q, c - q, c + q, c + q), fill=(225, 140, 60, 230))
    put(can, L, x, y)

def compass(can, x, y, r=80, alpha=0.75):
    L = Image.new('RGBA', (int(r * 3), int(r * 3)), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = r * 1.5
    col = INK + (int(255 * alpha),)
    d.ellipse((c - r, c - r, c + r, c + r), outline=col, width=3); d.ellipse((c - r * 0.82, c - r * 0.82, c + r * 0.82, c + r * 0.82), outline=col, width=1)
    for a in range(4):
        an = a * math.pi / 2; p1 = (c + r * math.cos(an), c + r * math.sin(an)); pl = (c + r * 0.18 * math.cos(an + math.pi / 4), c + r * 0.18 * math.sin(an + math.pi / 4))
        pr = (c + r * 0.18 * math.cos(an - math.pi / 4), c + r * 0.18 * math.sin(an - math.pi / 4))
        d.polygon([p1, pl, (c, c)], fill=col); d.polygon([p1, pr, (c, c)], outline=col)
    f = FK['serif'](int(r * 0.45)); d.text((c - f.getlength('N') / 2, c - r - r * 0.62), 'N', font=f, fill=col)
    put(can, L, x, y)
