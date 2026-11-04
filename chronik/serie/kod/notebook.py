# "Deutschland im Zweiten Weltkrieg" series: the old notebook look, a 10 s silent test of Teil 1's opening.
# One page of an aged notebook fills the 9:16 frame, turned a few degrees; handwriting and pencil sketches appear on the
# paper as the narration would say them, archive film plays taped onto the page, pages turn over the spine on the left.
import math, sys, os, functools, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
S = os.path.dirname(B.rstrip('/')) + '/'
W, H, FPS = 1080, 1920, 30
PW, PH = 1240, 2200                     # page size (page coords), bigger than the screen so the turned page covers it
ANG = -4.0                              # the notebook lies slightly askew
INK, GRAPH, REDP = (28, 30, 48), (58, 56, 54), (168, 34, 30)
def clamp(x): return max(0.0, min(1.0, x))
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def lerp(a, b, u): return a + (b - a) * u
@functools.lru_cache(None)
def hand(s): return ImageFont.truetype(B + 'fonts/Cedarville-Cursive.ttf', s)
@functools.lru_cache(None)
def bold(s): return ImageFont.truetype(B + 'fonts/Kalam-Bold.ttf', s)

# ---------- paper ----------
@functools.lru_cache(None)
def paper(seed=1):
    """aged paper: warm base, blotchy tone, fibres, foxing, faint ruling, darker worn edges"""
    r = np.random.default_rng(seed); h, w = PH, PW
    def noise(scale, amp):
        n = r.random((h // scale + 2, w // scale + 2)).astype(np.float32)
        return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255 * amp
    tone = noise(160, 1.0) * 0.6 + noise(40, 1.0) * 0.3 + noise(6, 1.0) * 0.1
    base = np.array([236, 220, 186], np.float32)[None, None] * (0.93 + 0.1 * tone[..., None])
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    edge = np.minimum.reduce([xx / 120, (w - xx) / 90, yy / 90, (h - yy) / 90]).clip(0, 1)
    base *= (0.80 + 0.20 * edge ** 0.6)[..., None]
    im = Image.fromarray(base.clip(0, 255).astype(np.uint8)); d = ImageDraw.Draw(im, 'RGBA')
    for y in range(330, h - 120, 78): d.line((70, y, w - 40, y), fill=(92, 110, 140, 46), width=2)          # ruling, faded blue
    d.line((150, 60, 150, h - 60), fill=(170, 70, 60, 50), width=2)                                         # margin line
    for _ in range(70):                                                                                    # foxing
        x, y, s = r.uniform(0, w), r.uniform(0, h), r.uniform(2, 14)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(140, 96, 52, int(r.uniform(10, 40))))
    for _ in range(900):                                                                                   # fibres
        x, y, a = r.uniform(0, w), r.uniform(0, h), r.uniform(0, math.pi); l = r.uniform(4, 16)
        d.line((x, y, x + l * math.cos(a), y + l * math.sin(a)), fill=(120, 100, 70, 26), width=1)
    st = Image.new('L', (w, h), 0); ds = ImageDraw.Draw(st)
    for _ in range(4):                                                                                     # old stains
        x, y, s = r.uniform(100, w - 100), r.uniform(200, h - 200), r.uniform(60, 180); ds.ellipse((x - s, y - s * 0.8, x + s, y + s * 0.8), outline=60, width=5)
    st = st.filter(ImageFilter.GaussianBlur(6)); im.paste((150, 112, 66), (0, 0), st.point(lambda v: v // 2))
    return im.filter(ImageFilter.GaussianBlur(0.6))
@functools.lru_cache(None)
def back():
    """back of a page: same paper, no ruling, a touch darker, mirrored ghost of nothing"""
    return ImageEnhance.Brightness(paper(7)).enhance(0.9)
@functools.lru_cache(None)
def desk():
    r = np.random.default_rng(3); n = r.random((H // 4, 40)).astype(np.float32)
    g = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    wood = np.stack([48 + 30 * g, 30 + 18 * g, 20 + 10 * g], -1)
    return Image.fromarray(wood.astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))

# ---------- ink on paper ----------
def ink_layer(size):
    return Image.new('L', size, 0)
def write(pg, t, t0, dur, s, xy, font, col=INK, a=1.0):
    """handwriting appears left to right like a pen moving; multiplied into the paper with a little bleed"""
    if t < t0: return None
    bb = font.getbbox(s); w_, h_ = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    L = Image.new('L', (w_, h_), 0); ImageDraw.Draw(L).text((20 - bb[0], 20 - bb[1]), s, font=font, fill=255)
    u = clamp((t - t0) / dur); edge = u * (w_ + 30); m = np.clip((edge - np.arange(w_)) / 30, 0, 1)[None, :]
    A = (np.asarray(L, np.float32) * m * a).astype(np.uint8); A = Image.fromarray(A).filter(ImageFilter.GaussianBlur(0.7))
    stamp_ink(pg, A, (int(xy[0]), int(xy[1])), col)
    return (xy[0] + min(edge, w_) - 20, xy[1] + h_ * 0.62) if u < 1 else None   # pen tip
def stamp_ink(pg, A, xy, col, strength=0.92):
    """darken the paper where ink is: paper * (1 - a) + ink * a, so the paper texture shows through the strokes"""
    x, y = xy; reg = pg.crop((x, y, x + A.width, y + A.height)); a = np.asarray(A, np.float32)[..., None] / 255 * strength
    p = np.asarray(reg, np.float32); out = p * (1 - a) + np.array(col, np.float32) * a * (0.85 + 0.15 * p / 255)
    pg.paste(Image.fromarray(out.clip(0, 255).astype(np.uint8)), (x, y))
def strokes(pg, t, t0, paths, dur, col=GRAPH, wd=5, seed=1, a=0.85):
    """pencil drawing: each path drawn in turn, slightly wobbly, double-traced like a quick sketch"""
    if t < t0: return None
    tot = sum(len(p) for p in paths); done = clamp((t - t0) / dur) * tot; tip = None
    L = Image.new('L', pg.size, 0); d = ImageDraw.Draw(L); r = np.random.default_rng(seed)
    for p in paths:
        n = len(p); k = min(n, done); done -= n
        if k <= 1:
            if k > 0: tip = p[0]
            break
        pts = p[:int(k)] + ([tuple(np.add(p[int(k) - 1], np.multiply(np.subtract(p[min(n - 1, int(k))], p[int(k) - 1]), k - int(k))))] if int(k) < n else [])
        for o, al in ((0, 255), (1.6, 150)):
            jit = [(x + o + r.normal(0, 0.7), y + o * 0.5 + r.normal(0, 0.7)) for x, y in pts]
            d.line(jit, fill=al, width=wd if o == 0 else wd - 2, joint='curve')
        tip = pts[-1]
        if done <= 0: break
    L = L.filter(ImageFilter.GaussianBlur(0.8)); grain = Image.fromarray((np.random.default_rng(seed + 5).random((pg.height, pg.width)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    L = ImageChops.multiply(L, grain.point(lambda v: 150 + v * 105 // 255))
    bx = L.getbbox()
    if bx: stamp_ink(pg, L.crop(bx).point(lambda v: int(v * a)), bx[:2], col, 1.0)
    return tip
def poly(pts, n=14):
    """resample a polyline so the drawing speed is even"""
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = max(2, int(math.hypot(x1 - x0, y1 - y0) / n))
        out += [(lerp(x0, x1, i / seg), lerp(y0, y1, i / seg)) for i in range(seg)]
    return out + [pts[-1]]
def circle(cx, cy, r, n=28): return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]

# ---------- the tank sketch (a generic WW1-era-free outline: hull, tracks, turret, gun) ----------
def tank(cx, cy, s=1.0):
    P = lambda pts: poly([(cx + x * s, cy + y * s) for x, y in pts])
    trk = P([(-300, 40), (260, 40), (310, 90), (270, 150), (-260, 150), (-320, 95), (-300, 40)])
    hull = P([(-280, 40), (-250, -40), (240, -40), (290, 40)])
    tur = P([(-130, -40), (-100, -120), (90, -120), (140, -40)])
    gun = P([(130, -90), (420, -95), (420, -75), (135, -70)])
    wheels = [poly([(cx + x * s, cy + y * s) for x, y in circle(wx, 108, 30, 18)]) for wx in (-210, -110, -10, 90, 190)]
    hatch = P([(-40, -120), (-30, -150), (30, -150), (40, -120)])
    return [trk, hull, tur, gun, hatch] + wheels

# ---------- archive film taped onto the page ----------
@functools.lru_cache(maxsize=4)
def film_frame(ct):
    im = Image.open(S + 'ju87/vfull/f%05d.jpg' % max(1, int(round(ct * FPS)) + 1)).convert('RGB')
    im = im.crop((0, 720, 1080, 1530))                              # the crowd, without the black bars (4:3)
    im = ImageEnhance.Color(im).enhance(0.3); im = Image.blend(im, Image.new('RGB', im.size, (120, 98, 66)), 0.18)
    return ImageEnhance.Contrast(im).enhance(1.08)
def taped(pg, t, t0, ct0, box, rot=2.0):
    """a photo-print of the film, white border, stuck on with two strips of tape, the film running inside"""
    if t < t0: return
    k = eout((t - t0) / 0.35); x0, y0, w_, h_ = box
    fr = film_frame(ct0 + (t - t0)).resize((w_, h_), Image.LANCZOS)
    card = Image.new('RGBA', (w_ + 36, h_ + 36), (238, 232, 216, 255)); card.paste(fr, (18, 18))
    card = card.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', pg.size, (0, 0, 0, 0)); sh.paste((40, 28, 14, 110), (int(x0 + 10), int(y0 + 16)), card.getchannel('A'))
    sc = lerp(1.08, 1.0, k); card = card.resize((int(card.width * sc), int(card.height * sc)), Image.BICUBIC)
    if k < 1: card.putalpha(card.getchannel('A').point(lambda v: int(v * k)))
    base = pg.convert('RGBA'); base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10))); base.alpha_composite(card, (int(x0 - (sc - 1) * w_ / 2), int(y0 - (sc - 1) * h_ / 2)))
    for tx, ty, ta in ((x0 + 40, y0 - 10, -28), (x0 + w_ - 30, y0 + h_ + 20, -24)):
        tp = Image.new('RGBA', (170, 54), (226, 214, 170, int(150 * k))); tp = tp.rotate(ta, expand=True, resample=Image.BICUBIC)
        base.alpha_composite(tp, (int(tx - tp.width / 2), int(ty - tp.height / 2)))
    pg.paste(base.convert('RGB'))

# ---------- pages ----------
T_FLIP0, T_FLIP1 = 4.45, 5.3
def page1(t):
    pg = paper(1).copy()
    write(pg, t, 0.25, 0.5, '1919', (190, 420), bold(170), INK)
    write(pg, t, 0.8, 1.2, 'Zwanzig Jahre vor dem', (190, 660), hand(80))
    write(pg, t, 1.6, 1.0, 'Zweiten Weltkrieg', (190, 750), hand(80))
    write(pg, t, 2.35, 1.1, 'keinen einzigen Panzer', (190, 900), hand(80))
    strokes(pg, t, 2.5, tank(560, 1330, 0.95), 1.6, GRAPH, 5)
    if t > 3.95:   # crossed out in red pencil
        X = [poly([(220, 1100), (900, 1520)]), poly([(900, 1100), (230, 1530)])]
        strokes(pg, t, 3.95, X, 0.4, REDP, 9, seed=4, a=0.9)
    if t > 4.15:   # underline 'keinen'
        strokes(pg, t, 4.15, [poly([(190, 1000), (500, 992)])], 0.2, REDP, 6, seed=6, a=0.9)
    return pg
def page2(t):
    pg = paper(2).copy()
    write(pg, t, 5.4, 0.6, 'Der Vertrag', (190, 400), hand(90))
    write(pg, t, 5.9, 0.8, 'von Versailles', (190, 500), hand(90))
    if t > 6.7: strokes(pg, t, 6.7, [poly([(190, 625), (760, 616)])], 0.3, INK, 5, seed=8, a=0.85)
    taped(pg, t, 6.3, 9.6, (215, 700, 660, 495), 2.2)
    write(pg, t, 8.0, 0.6, 'Heer:', (190, 1290), hand(92))
    write(pg, t, 8.45, 0.9, '100.000 Mann', (190, 1400), bold(116), INK)
    if t > 9.35:
        for k, y in enumerate((1560, 1578)): strokes(pg, t, 9.35 + k * 0.12, [poly([(195, y), (760, y - 6)])], 0.25, REDP, 6, seed=10 + k, a=0.9)
    return pg

def spread(t):
    """the visible page, with the page turn: the top page swings over the spine (left edge) and reveals the next"""
    if t < T_FLIP0: return page1(t)
    if t >= T_FLIP1: return page2(t)
    u_ = clamp((t - T_FLIP0) / (T_FLIP1 - T_FLIP0)); p = eio(u_) ** 0.0 * u_ ** 1.6; th = p * math.pi;   # the sheet lingers while it lifts, then falls away over the spine
    under = page2(t).convert('RGBA')
    c = math.cos(th); w_ = abs(c) * PW; lift = math.sin(th) * PH * 0.05
    top = (page1(T_FLIP0) if c > 0 else back()).convert('RGBA')
    if c > 0:   # shadow thrown on the next page by the lifting sheet
        sh = Image.new('RGBA', (PW, PH), (30, 20, 8, 0)); g = np.clip(1 - (np.arange(PW) - w_) / 260, 0, 1) * (np.arange(PW) >= w_) * 150 * math.sin(th)
        sh.putalpha(Image.fromarray(np.repeat(g[None, :], PH, 0).astype(np.uint8))); under.alpha_composite(sh)
    if w_ > 2:
        quad = [(0, 0), (w_, -lift), (w_, PH + lift), (0, PH)] if c > 0 else [(0, 0), (-w_, -lift), (-w_, PH + lift), (0, PH)]
        xs = [q[0] for q in quad]; ox = int(min(xs)); sw = int(max(xs) - min(xs)) + 2
        src_q = [(0, 0), (PW, 0), (PW, PH), (0, PH)]
        M = []
        for (x, y), (X, Y) in zip([(q[0] - ox, q[1] + lift) for q in quad], src_q): M += [[x, y, 1, 0, 0, 0, -X * x, -X * y], [0, 0, 0, x, y, 1, -Y * x, -Y * y]]
        co = np.linalg.solve(np.array(M, float), np.array([v for q in src_q for v in q], float)).tolist()
        warped = top.transform((sw, int(PH + 2 * lift) + 2), Image.PERSPECTIVE, co, Image.BICUBIC)
        shade = 0.55 + 0.45 * abs(c); warped = Image.merge('RGBA', [b.point(lambda v: int(v * shade)) for b in warped.split()[:3]] + [warped.split()[3]])
        if c > 0:   # a light edge where the sheet bends, so it reads as paper
            e = Image.new('RGBA', warped.size, (0, 0, 0, 0)); de = ImageDraw.Draw(e); ex = warped.width - 3
            de.line((ex, 0, ex, warped.height), fill=(255, 250, 235, int(160 * math.sin(th))), width=5); warped.alpha_composite(e.filter(ImageFilter.GaussianBlur(3)))
        under.alpha_composite(warped, (max(0, ox), int(-lift))) if ox >= 0 else under.alpha_composite(warped.crop((-ox, 0, sw, warped.height)), (0, int(-lift)))
    return under.convert('RGB')

def frame(t):
    pg = spread(t).convert('RGBA')
    # light from the top left, a soft fall-off to the bottom right
    yy, xx = np.mgrid[0:PH:8, 0:PW:8].astype(np.float32); lg = 1.12 - 0.12 * (xx / PW * 0.4 + yy / PH * 0.6)
    lg = Image.fromarray((lg.clip(0, 1.2) / 1.2 * 255).astype(np.uint8)).resize((PW, PH), Image.BILINEAR)
    pg = Image.merge('RGBA', [ImageChops.multiply(b, lg.point(lambda v: min(255, int(v * 1.2)))) for b in pg.split()[:3]] + [pg.split()[3]])
    z = 1.0 + 0.03 * t / 10; rp = pg.rotate(ANG, expand=True, resample=Image.BICUBIC)
    rp = rp.resize((int(rp.width * z), int(rp.height * z)), Image.BICUBIC)
    can = desk().convert('RGBA'); x0, y0 = 520 - rp.width // 2, 1010 - rp.height // 2   # page centre slightly left of the screen centre: text stays clear of the buttons
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 160), (x0 + 18, y0 + 24), rp.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26)))
    can.alpha_composite(rp, (x0, y0))
    # the page curves down into the binding on the left: a soft shadow along the left edge
    g = (np.clip(1 - np.arange(W) / 120, 0, 1) ** 1.8 * 150).astype(np.uint8)
    L = Image.new('RGBA', (W, H), (24, 14, 4, 0)); L.putalpha(Image.fromarray(np.repeat(g[None, :], H, 0))); can.alpha_composite(L)
    vig = np.hypot((np.mgrid[0:H, 0:W][1] - W / 2) / W, (np.mgrid[0:H, 0:W][0] - H / 2) / H) * 2
    can.alpha_composite(Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), (np.clip(vig - 0.75, 0, 1) * 170).astype(np.uint8)]), 'RGBA'))
    a = np.asarray(can.convert('RGB')).astype(np.int16) + np.random.default_rng(int(t * FPS)).normal(0, 4, (H, W))[..., None].astype(np.int16)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

if __name__ == '__main__':
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[2:]]; P = Image.new('RGB', (len(ts) * 360, 640))
        for i, t in enumerate(ts): P.paste(frame(t).resize((360, 640)), (i * 360, 0))
        P.save(B + 'out/prev.jpg', quality=88); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', out], stdin=subprocess.PIPE)
    for n in range(int(a * FPS), int(b * FPS)): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
