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
LAND, WATER, BORDER = (58, 56, 52), (30, 34, 40), (110, 106, 98)

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

# ================= timeline =================
T_HOOK_END = K('Eisenhower hatte') - 0.25
BERLIN = (13.40, 52.52); ELBE_US = (11.70, 52.30); KUESTRIN = (14.62, 52.58); SEELOW = (14.38, 52.53); ZOSSEN = (13.45, 52.22); TORGAU = (13.00, 51.56); NEISSE = (14.95, 51.45)
CAM[:] = [(0, 12.6, 52.42, 470), (T_HOOK_END, 12.6, 52.42, 470), (K('Gleichzeitig befahl'), 12.9, 52.42, 470), (K('Am 16. April'), 13.9, 52.3, 420), (K('Schukow sollte'), 13.9, 52.15, 400), (K('An den Seelower'), 14.25, 52.5, 1000), (K('Konew kam schneller'), 13.9, 52.25, 520),
          (K('Am 25. April'), 13.45, 52.45, 620), (K('Am selben Tag'), 13.2, 51.9, 440), (K('Torgau an der Elbe.', 3), 13.2, 51.9, 440), (K('In der Stadt'), 13.4, 52.5, 1700), (K('Am Nachmittag nahm') - 0.3, 13.39, 52.5, 2600), (T_END, 13.39, 52.5, 2700)]
SEC = dict(hook=(0, T_HOOK_END), street=(K('In der Stadt'), K('Am 30. April')), reich=(K('Am 30. April'), K('Am Nachmittag nahm')), toll=(K('Die Rote Armee'), K('Die Inschriften')), graf=(K('Die Inschriften'), T_END + 1))
def frame(t):
    if SEC['hook'][0] <= t < SEC['hook'][1]:
        im = fullfilm('hook', t, 0)
        say(im, t, [[(K('Die Amerikaner'), 'DIE', 'w'), (K('Die Amerikaner', 1), 'AMERIKANER', 'w')], [(K('nur 85'), 'NUR', 'w'), (K('nur 85', 1), '85 KM', 'y')], [(K('vor Berlin.'), 'VOR', 'w'), (K('vor Berlin.', 1), 'BERLIN.', 'y')]], y0=330, size=130)
        say(im, t, [[(K('Dann hielten'), 'DANN', 'w'), (K('hielten sie an.'), 'HIELTEN', 'r'), (K('hielten sie an.', 1), 'SIE AN.', 'r')]], y0=1380, size=120)
        return im.convert('RGB')
    if SEC['street'][0] <= t < SEC['street'][1]:
        im = fullfilm('street', t, SEC['street'][0])
        say(im, t, [[(K('In der Stadt'), 'UM JEDE', 'w')], [(K('jede Straße'), 'STRASSE', 'y')]], y0=300, size=140); return im.convert('RGB')
    if SEC['reich'][0] <= t < SEC['reich'][1]:
        im = fullfilm('flagup', t, SEC['reich'][0])
        say(im, t, [[(K('Am 30. April'), '30. APRIL', 'y')], [(K('stürmten sowjetische'), 'STURM AUF DEN', 'w')], [(K('den Reichstag.', 1), 'REICHSTAG', 'r')]], y0=300, size=120); return im.convert('RGB')
    if SEC['toll'][0] <= t < SEC['toll'][1]:
        im = fullfilm('ruins', t, SEC['toll'][0]); im.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, 120)))
        counter(im, t, K('über 350.000'), 350000, lambda v: de(v), (W / 2, 560), 190, (255, 70, 60)); say(im, t, [[(K('Mann an Toten'), 'SOWJETISCHE', 'w')], [(K('und Verwundeten,'), 'TOTE UND VERWUNDETE', 'w')]], y0=680, size=64)
        counter(im, t, K('rund 100.000'), 100000, lambda v: de(v), (W / 2, 1000), 170, YEL); say(im, t, [[(K('deutsche Soldaten starben,'), 'DEUTSCHE SOLDATEN TOT', 'w')]], y0=1100, size=64)
        say(im, t, [[(K('dazu Zehntausende'), '+ ZEHNTAUSENDE', 'y')], [(K('Zehntausende Zivilisten.', 1), 'ZIVILISTEN', 'w')]], y0=1300, size=96); return im.convert('RGB')
    if t >= SEC['graf'][0]:
        im = fullfilm('graffiti', t, SEC['graf'][0], 1.0, 1.1)
        say(im, t, [[(K('Die Inschriften'), 'BIS HEUTE', 'w')], [(K('an den Wänden'), 'AN DEN WÄNDEN', 'w')], [(K('des Reichstags.', 1), 'DES REICHSTAGS', 'y')]], y0=1150, size=110); return im.convert('RGB')
    # ---------- the map ----------
    im = basemap(t); p = P(t)
    tb = p(*BERLIN)
    label(im, t, T_HOOK_END, 'BERLIN', (tb[0], tb[1] - 50), 46, WHITE, box=(20, 20, 22))
    pin(im, t, T_HOOK_END, tb, WHITE, 13)
    label(im, t, T_HOOK_END + 0.2, 'ELBE', (p(11.95, 52.75)[0], p(11.95, 52.75)[1]), 36, (150, 190, 230))
    label(im, t, K('über die Oder'), 'ODER', p(14.9, 52.95), 36, (150, 190, 230))
    # US at the Elbe
    pu = p(*ELBE_US); pin(im, t, T_HOOK_END, pu, BLUE, 13); flagchip(im, (pu[0] - 80, pu[1] - 70), 'us', eout((t - T_HOOK_END) / 0.3))
    if t < K('Am 16. April'):
        dashed(im, t, T_HOOK_END + 0.2, 0.7, pu, tb); m = ((pu[0] + tb[0]) / 2, (pu[1] + tb[1]) / 2 - 40); label(im, t, T_HOOK_END + 0.5, '85 KM', m, 52, YEL)
        label(im, t, K('Eisenhower hatte'), 'EISENHOWER', (pu[0], pu[1] + 70), 44, WHITE, box=(40, 70, 150))
        label(im, t, K('Stalin antwortete,'), 'STALIN', (p(15.2, 52.3)[0], p(15.2, 52.3)[1]), 44, WHITE, box=SRED)
        if t >= K('Stalin antwortete,'): flagchip(im, (p(15.2, 52.3)[0] - 29, p(15.2, 52.3)[1] - 90), 'su')
        say(im, t, [[(K('Berlin habe keine'), '„KEINE', 'w'), (K('keine Bedeutung'), 'BEDEUTUNG', 'y'), (K('Bedeutung mehr.', 1), 'MEHR“', 'w')]], y0=300, size=92, until=K('Gleichzeitig befahl') - 0.22)
        if t >= K('Gleichzeitig befahl'): say(im, t, [[(K('Gleichzeitig befahl'), 'GLEICHZEITIG:', 'w')], [(K('den Angriff.', 1), 'ANGRIFF', 'r')]], y0=300, size=110)
    soviet_area(im, t, K('Am 16. April'), p)
    if t >= K('Am 16. April') and t < K('Schukow sollte'):
        say(im, t, [[(K('Am 16. April'), '16. APRIL 1945', 'y')]], y0=300, size=100)
        counter(im, t, K('griffen 2,5'), 2.5, lambda v: ('%.1f' % v).replace('.', ',') + ' MIO.', (W / 2, 560), 190, (255, 70, 60))
        say(im, t, [[(K('sowjetische und polnische'), 'SOWJETISCHE UND POLNISCHE', 'w')], [(K('Soldaten an.'), 'SOLDATEN', 'w')]], y0=680, size=70)
    zh_until = K('Konew kam schneller')
    arrow(im, t, K('Schukow sollte frontal'), 1.2, p, [KUESTRIN, (14.2, 52.55), (13.8, 52.53), BERLIN], RED, 30, upto=(0.42 if t < K('Am 25. April') else 1.0))
    if t >= K('Schukow sollte') and t < K('An den Seelower'):
        label(im, t, K('Schukow sollte'), 'SCHUKOW', (min(860, p(*KUESTRIN)[0] - 60), p(*KUESTRIN)[1] - 80), 48, WHITE, box=SRED)
        label(im, t, K('Konew von Süden'), 'KONEW', (min(860, p(*NEISSE)[0] - 60), min(1520, p(*NEISSE)[1] + 70)), 48, WHITE, box=SRED)
        say(im, t, [[(K('Schukow sollte'), 'SCHUKOW:', 'w'), (K('frontal über'), 'FRONTAL', 'y')], [(K('Konew von'), 'KONEW:', 'w'), (K('Süden herum.'), 'VON SÜDEN', 'y')]], y0=300, size=100)
    arrow(im, t, K('Konew von Süden'), 1.2, p, [NEISSE, (14.3, 51.75), (13.7, 51.95), ZOSSEN, (13.25, 52.42)], RED, 30, upto=(0.45 if t < zh_until else (0.75 if t < K('Am 25. April') else 1.0)))
    if K('An den Seelower') <= t < K('Konew kam schneller'):
        ps = p(*SEELOW); label(im, t, K('An den Seelower'), 'SEELOWER HÖHEN', (ps[0] - 40, ps[1] + 110), 50, WHITE, box=(20, 20, 22))
        beams(im, t, K('143 Scheinwerfer'), (p(*KUESTRIN)[0] + 60, p(*KUESTRIN)[1] - 20), k=1.0)
        smoke(im, t, K('nur Rauch'), ps)
        if t < K('Doch sie beleuchteten'):
            counter(im, t, K('143 Scheinwerfer'), 143, lambda v: '%d' % round(v), (W / 2, 420), 220, YEL)
            say(im, t, [[(K('143 Scheinwerfer', 1), 'SCHEINWERFER', 'w')]], y0=560, size=90)
            card(im, t, K('Scheinwerfer einschalten,'), K('Doch sie beleuchteten') - 0.3, 'barrage')
        else:
            say(im, t, [[(K('nur Rauch'), 'NUR RAUCH', 'y'), (K('und Staub,'), 'UND STAUB', 'y')], [(K('Panzer blieben'), 'PANZER', 'w'), (K('im Sumpf'), 'IM SUMPF', 'r')]], y0=300, size=100)
            card(im, t, K('seine Panzer'), K('Konew kam schneller') - 0.25, 'tanks')
    if K('Konew kam schneller') <= t < K('Am 25. April'):
        say(im, t, [[(K('Konew kam'), 'KONEW', 'w'), (K('kam schneller'), 'SCHNELLER', 'y')]], y0=300, size=120)
        label(im, t, K('Konew kam'), 'ZOSSEN', (p(*ZOSSEN)[0] + 120, p(*ZOSSEN)[1]), 40, WHITE)
    if t >= K('Am 25. April') and t < K('In der Stadt'):
        tb = p(*BERLIN); ring(im, t, K('Am 25. April', 1), 1.0, tb, 0.30 * p.k, 0.20 * p.k * 1.6, RED, 14, 40)
        if t < K('Am selben Tag'):
            say(im, t, [[(K('Am 25. April'), '25. APRIL', 'y')], [(K('war Berlin eingeschlossen.', 2), 'EINGESCHLOSSEN', 'r')]], y0=300, size=110)
        else:
            pt = p(*TORGAU); arrow(im, t, K('trafen sich'), 0.8, p, [(12.1, 51.75), (12.6, 51.62), TORGAU], BLUE, 24); arrow(im, t, K('trafen sich'), 0.8, p, [(13.9, 51.4), (13.4, 51.5), TORGAU], RED, 24)
            pin(im, t, K('bei Torgau'), pt, YEL, 15); label(im, t, K('bei Torgau'), 'TORGAU', (pt[0], pt[1] + 70), 50, WHITE, box=(20, 20, 22))
            say(im, t, [[(K('trafen sich'), 'AMERIKANER', 'w'), (K('und Sowjets bei'), '+ SOWJETS', 'r')], [(K('bei Torgau'), 'TREFFEN AN DER ELBE', 'y')]], y0=300, size=96)
    if K('Am Nachmittag nahm') <= t < K('Die Rote Armee'):
        tb = p(*BERLIN); rb = p(13.381, 52.5125)
        ring(im, t, K('Am Nachmittag nahm') - 0.4, 0.01, tb, 330, 300, RED, 18, 50)
        pin(im, t, K('im Bunker'), rb, YEL, 18); label(im, t, K('im Bunker'), 'FÜHRERBUNKER', (rb[0], rb[1] + 80), 52, WHITE, box=(20, 20, 22))
        if t < K('Am 2. Mai'):
            say(im, t, [[(K('Am Nachmittag'), 'AM NACHMITTAG', 'w')], [(K('nahm sich Hitler'), 'HITLER', 'w'), (K('das Leben.'), 'TOT', 'r')]], y0=300, size=110)
        else:
            say(im, t, [[(K('Am 2. Mai'), '2. MAI 1945', 'y')]], y0=300, size=120)
            stamp(im, t, K('kapitulierte Berlin.'), 'KAPITULATION', (W / 2, 560), 120)
    return im.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'T': print(round(T_END, 3)); sys.exit()
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[3:]]; Pc = Image.new('RGB', (270 * len(ts), 480))
        for i, tt in enumerate(ts):
            im = frame(tt); ImageDraw.Draw(im).text((20, 20), '%.2f' % tt, font=font('Anton', 60), fill=(255, 0, 255)); Pc.paste(im.resize((270, 480)), (i * 270, 0))
        Pc.save(B + 'sh/' + sys.argv[2], quality=85); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): pr.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    pr.stdin.close(); pr.wait(); print('rc', pr.returncode)
