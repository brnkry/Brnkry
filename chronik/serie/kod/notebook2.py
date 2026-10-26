# "Deutschland im Zweiten Weltkrieg" series, notebook look v2: an open notebook (two pages) lies askew on a desk and fills
# the 9:16 frame; the camera sits on one page at a time. Opening: the closed notebook with the series label, the cover opens.
# Handwriting (Kalam, readable) and pencil sketches appear as the narration says them, key words in red or blue ink,
# archive film taped onto the paper. A page turns with a real curl over the spine; the camera follows it to the left page,
# then moves right to the next page, then the next turn takes it left again.
import math, sys, os, functools, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
S = os.path.dirname(B.rstrip('/')) + '/'
W, H, FPS = 1080, 1920, 30
PW, PH = 1240, 2200                      # one page (page coords)
SW = 2 * PW                              # spread: left page [0, PW], spine at PW, right page [PW, 2 PW]
ANG = 4.0                                # the notebook lies a little askew
INK, GRAPH, RED, BLUE = (18, 20, 38), (52, 50, 48), (176, 28, 26), (24, 58, 150)
def clamp(x): return max(0.0, min(1.0, x))
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def lerp(a, b, u): return a + (b - a) * u
@functools.lru_cache(None)
def hand(s): return ImageFont.truetype(B + 'fonts/Kalam-Regular.ttf', s)
@functools.lru_cache(None)
def bold(s): return ImageFont.truetype(B + 'fonts/Kalam-Bold.ttf', s)
@functools.lru_cache(None)
def typew(s): return ImageFont.truetype(S + 'sch/fonts/SpecialElite-Regular.ttf', s)

# ---------- materials ----------
def _noise(r, h, w, scale):
    n = r.random((h // scale + 2, w // scale + 2)).astype(np.float32)
    return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
@functools.lru_cache(None)
def paper(seed=1, ruled=True, spine_right=False):
    """aged but clean paper: warm cream, gentle mottling, fibres, a few foxing spots, ruling, worn outer edges"""
    r = np.random.default_rng(seed); h, w = PH, PW
    tone = _noise(r, h, w, 180) * 0.6 + _noise(r, h, w, 40) * 0.3 + _noise(r, h, w, 6) * 0.1
    base = np.array([244, 231, 200], np.float32)[None, None] * (0.95 + 0.07 * tone[..., None])
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ox = (w - xx) if spine_right else xx                                  # distance from the outer edge
    edge = np.minimum.reduce([(w - ox) / 60 + 9, ox / 70, yy / 70, (h - yy) / 70]).clip(0, 1)
    base *= (0.86 + 0.14 * edge ** 0.5)[..., None]
    im = Image.fromarray(base.clip(0, 255).astype(np.uint8)); d = ImageDraw.Draw(im, 'RGBA')
    if ruled:
        for y in range(330, h - 120, 80): d.line((40, y, w - 40, y), fill=(80, 104, 150, 70), width=2)
        mx = w - 150 if spine_right else 150
        d.line((mx, 40, mx, h - 40), fill=(190, 60, 50, 80), width=2)
    for _ in range(40):
        x, y, s = r.uniform(0, w), r.uniform(0, h), r.uniform(2, 10)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(150, 104, 56, int(r.uniform(10, 30))))
    for _ in range(700):
        x, y, a = r.uniform(0, w), r.uniform(0, h), r.uniform(0, math.pi); l = r.uniform(4, 14)
        d.line((x, y, x + l * math.cos(a), y + l * math.sin(a)), fill=(120, 100, 70, 22), width=1)
    return im
@functools.lru_cache(None)
def cover_front():
    """cloth-bound cover, dark green, worn corners, a pasted paper label with the series title"""
    r = np.random.default_rng(11); h, w = PH, PW
    weave = _noise(r, h, w, 3) * 0.5 + _noise(r, h, w, 60) * 0.5
    base = np.array([46, 60, 50], np.float32)[None, None] * (0.8 + 0.4 * weave[..., None])
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); edge = np.minimum.reduce([xx / 50 + 0.3, (w - xx) / 50, yy / 50, (h - yy) / 50]).clip(0, 1)
    base = base * (0.65 + 0.35 * edge)[..., None] + (1 - edge[..., None]) * np.array([30, 26, 18])
    im = Image.fromarray(base.clip(0, 255).astype(np.uint8)); d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((70, 70, w - 70, h - 70), outline=(150, 130, 80, 90), width=4)            # blind-stamped border
    lab = paper(21, False).crop((0, 0, 900, 760)); dl = ImageDraw.Draw(lab)
    dl.rectangle((18, 18, 882, 742), outline=(60, 50, 40), width=4); dl.rectangle((32, 32, 868, 728), outline=(60, 50, 40), width=1)
    dl.text((450, 110), 'CHRONIK DER MACHT', font=typew(40), fill=(110, 40, 34), anchor='mm')
    for i, s in enumerate(('DEUTSCHLAND', 'IM ZWEITEN', 'WELTKRIEG')): dl.text((450, 235 + i * 112), s, font=typew(96), fill=INK, anchor='mm')
    dl.line((150, 560, 750, 560), fill=(60, 50, 40), width=3)
    dl.text((450, 640), 'Der Weg in den Krieg', font=bold(62), fill=BLUE, anchor='mm')
    tl = Image.new('RGBA', (300, 120), (0, 0, 0, 0)); dt = ImageDraw.Draw(tl); dt.rectangle((6, 6, 294, 114), outline=RED + (235,), width=7)
    dt.text((150, 62), 'TEIL 1', font=typew(64), fill=RED + (240,), anchor='mm'); tl = tl.rotate(8, expand=True, resample=Image.BICUBIC)
    m_ = (np.random.default_rng(5).random((tl.height, tl.width)) > 0.15).astype(np.uint8) * 255; tl.putalpha(Image.fromarray(np.minimum(np.asarray(tl.getchannel('A')), m_)))
    lab = lab.convert('RGBA'); lab.alpha_composite(tl, (560, 440)); lab = lab.convert('RGB')
    lab = lab.rotate(-1.2, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0))
    m = Image.new('L', lab.size, 0); ImageDraw.Draw(m).rectangle((6, 6, lab.width - 6, lab.height - 6), fill=255)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), (238, 560), m); im = im.convert('RGBA'); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    im.paste(lab, (230, 545), m); return im.convert('RGB')
@functools.lru_cache(None)
def endpaper():
    """inside of the cover: plain brown endpaper"""
    r = np.random.default_rng(12); t = _noise(r, PH, PW, 30) * 0.6 + _noise(r, PH, PW, 4) * 0.4
    return Image.fromarray((np.array([150, 116, 76], np.float32)[None, None] * (0.85 + 0.25 * t[..., None])).clip(0, 255).astype(np.uint8))
@functools.lru_cache(None)
def desk():
    r = np.random.default_rng(3); g = _noise(r, H // 2, 30, 1)
    g = np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    return Image.fromarray(np.stack([44 + 30 * g, 28 + 18 * g, 18 + 10 * g], -1).astype(np.uint8)).convert('RGBA')

# ---------- ink, pencil, film ----------
def stamp_ink(pg, A, xy, col, strength=1.0):
    """ink sits in the paper: paper * (1 - a) + ink * a, the paper texture still showing through"""
    x, y = int(xy[0]), int(xy[1]); reg = pg.crop((x, y, x + A.width, y + A.height)); a = np.asarray(A, np.float32)[..., None] / 255 * strength
    p = np.asarray(reg, np.float32); out = p * (1 - a) + np.array(col, np.float32) * a * (0.9 + 0.1 * p / 255)
    pg.paste(Image.fromarray(out.clip(0, 255).astype(np.uint8)), (x, y))
def write(pg, t, t0, dur, s, xy, font, col=INK):
    """the pen writes left to right"""
    if t < t0: return
    bb = font.getbbox(s); w_, h_ = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    L = Image.new('L', (w_, h_), 0); ImageDraw.Draw(L).text((20 - bb[0], 20 - bb[1]), s, font=font, fill=255)
    edge = clamp((t - t0) / dur) * (w_ + 30); m = np.clip((edge - np.arange(w_)) / 30, 0, 1)[None, :]
    A = Image.fromarray((np.asarray(L, np.float32) * m).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    stamp_ink(pg, A, xy, col)
def poly(pts, n=14):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = max(2, int(math.hypot(x1 - x0, y1 - y0) / n)); out += [(lerp(x0, x1, i / seg), lerp(y0, y1, i / seg)) for i in range(seg)]
    return out + [pts[-1]]
def circle(cx, cy, r, n=20): return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
def strokes(pg, t, t0, paths, dur, col=GRAPH, wd=6, seed=1, a=0.9):
    """pencil sketch: paths drawn one after another, slightly wobbly, traced twice, with graphite grain"""
    if t < t0: return
    tot = sum(len(p) for p in paths); done = clamp((t - t0) / dur) * tot
    L = Image.new('L', pg.size, 0); d = ImageDraw.Draw(L); r = np.random.default_rng(seed)
    for p in paths:
        n = len(p); k = min(n, done); done -= n
        if k < 2: break
        pts = p[:int(k)]
        for o, al in ((0, 255), (1.8, 160)):
            d.line([(x + o + r.normal(0, 0.7), y + o * 0.5 + r.normal(0, 0.7)) for x, y in pts], fill=al, width=wd if o == 0 else wd - 2, joint='curve')
        if done <= 0: break
    bx = L.getbbox()
    if not bx: return
    L = L.crop(bx).filter(ImageFilter.GaussianBlur(0.7))
    gr = Image.fromarray((np.random.default_rng(seed + 5).random((L.height, L.width)) * 255).astype(np.uint8))
    L = ImageChops.multiply(L, gr.point(lambda v: 170 + v * 85 // 255)).point(lambda v: int(v * a))
    stamp_ink(pg, L, bx[:2], col)
def tank(cx, cy, s=1.0):
    P = lambda pts: poly([(cx + x * s, cy + y * s) for x, y in pts])
    return [P([(-300, 40), (260, 40), (310, 90), (270, 150), (-260, 150), (-320, 95), (-300, 40)]), P([(-280, 40), (-250, -40), (240, -40), (290, 40)]),
            P([(-130, -40), (-100, -120), (90, -120), (140, -40)]), P([(130, -90), (420, -95), (420, -75), (135, -70)]), P([(-40, -120), (-30, -150), (30, -150), (40, -120)])] + \
           [poly([(cx + x * s, cy + y * s) for x, y in circle(wx, 108, 30)]) for wx in (-210, -110, -10, 90, 190)]
def plane(cx, cy, s=1.0):
    P = lambda pts: poly([(cx + x * s, cy + y * s) for x, y in pts], 10)
    return [P([(-220, 0), (-180, -18), (200, -14), (230, 0), (200, 14), (-180, 18), (-220, 0)]), P([(-40, -14), (0, -200), (60, -200), (50, -14)]), P([(-40, 14), (0, 200), (60, 200), (50, 14)]),
            P([(170, -12), (205, -80), (230, -80), (225, -10)]), P([(170, 12), (205, 80), (230, 80), (225, 10)])]
@functools.lru_cache(maxsize=4)
def film_frame(ct):
    im = Image.open(S + 'ju87/vfull/f%05d.jpg' % max(1, int(round(ct * FPS)) + 1)).convert('RGB').crop((0, 720, 1080, 1530))
    im = Image.blend(ImageEnhance.Color(im).enhance(0.3), Image.new('RGB', im.size, (120, 98, 66)), 0.15); return ImageEnhance.Contrast(im).enhance(1.1)
def taped(pg, t, t0, ct0, box, rot=2.0):
    if t < t0: return
    k = eout((t - t0) / 0.35); x0, y0, w_, h_ = box
    card = Image.new('RGBA', (w_ + 36, h_ + 36), (240, 234, 220, 255)); card.paste(film_frame(ct0 + (t - t0)).resize((w_, h_), Image.LANCZOS), (18, 18))
    card = card.rotate(rot, expand=True, resample=Image.BICUBIC); sc = lerp(1.08, 1.0, k)
    base = pg.convert('RGBA'); sh = Image.new('RGBA', pg.size, (0, 0, 0, 0)); sh.paste((40, 28, 14, int(110 * k)), (int(x0 + 10), int(y0 + 16)), card.getchannel('A'))
    card = card.resize((int(card.width * sc), int(card.height * sc)), Image.BICUBIC)
    if k < 1: card.putalpha(card.getchannel('A').point(lambda v: int(v * k)))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10))); base.alpha_composite(card, (int(x0 - (sc - 1) * w_ / 2), int(y0 - (sc - 1) * h_ / 2)))
    for tx, ty, ta in ((x0 + 40, y0 - 10, -28), (x0 + w_ - 30, y0 + h_ + 20, -24)):
        tp = Image.new('RGBA', (170, 54), (226, 214, 170, int(150 * k))).rotate(ta, expand=True, resample=Image.BICUBIC)
        base.alpha_composite(tp, (int(tx - tp.width / 2), int(ty - tp.height / 2)))
    pg.paste(base.convert('RGB'))

# ---------- timeline of this 13 s sample ----------
T_OPEN = (1.0, 2.0)           # the cover opens
T_TURN = (6.6, 7.6)           # page 1 turns
CAM = [(0.0, 'R'), (6.75, 'R'), (7.75, 'L'), (10.3, 'L'), (11.0, 'R')]   # camera on the right / left page
def page_r1(t):
    pg = paper(1).copy()
    write(pg, t, 2.15, 0.5, '1919', (190, 380), bold(190), INK)
    write(pg, t, 2.6, 1.0, 'Zwanzig Jahre vor dem', (190, 640), bold(84), INK)
    write(pg, t, 3.4, 0.8, 'Zweiten Weltkrieg', (190, 740), bold(84), INK)
    write(pg, t, 4.3, 0.9, 'keinen einzigen Panzer', (190, 880), bold(84), RED)
    strokes(pg, t, 4.5, tank(560, 1330, 0.95), 1.5, GRAPH, 6)
    strokes(pg, t, 6.0, [poly([(220, 1100), (900, 1520)]), poly([(900, 1100), (230, 1530)])], 0.4, RED, 10, seed=4)
    return pg
def page_l2(t):
    pg = paper(2, spine_right=True).copy()
    write(pg, t, 7.7, 0.6, 'Der Vertrag', (170, 400), bold(92), INK)
    write(pg, t, 8.2, 0.8, 'von Versailles', (170, 505), bold(92), BLUE)
    strokes(pg, t, 9.0, [poly([(170, 630), (760, 620)])], 0.3, BLUE, 6, seed=8)
    taped(pg, t, 8.7, 9.6, (200, 720, 660, 495), 2.2)
    return pg
def page_r2(t):
    pg = paper(3).copy()
    write(pg, t, 11.0, 0.5, 'Heer:', (190, 400), bold(92), INK)
    write(pg, t, 11.4, 0.9, '100.000 Mann', (190, 510), bold(124), RED)
    for k, y in enumerate((690, 708)): strokes(pg, t, 12.3 + k * 0.1, [poly([(195, y), (780, y - 6)])], 0.25, RED, 7, seed=10 + k)
    write(pg, t, 12.6, 0.7, 'Luftwaffe:', (190, 820), bold(84), INK)
    write(pg, t, 13.0, 0.6, 'verboten', (640, 820), bold(84), RED)
    strokes(pg, t, 12.8, plane(520, 1250, 1.2), 1.0, GRAPH, 6, seed=14)
    return pg

# ---------- the spread and the page turn ----------
def spread_base(left, right):
    """both pages on one canvas; the paper darkens where it curves into the spine"""
    can = Image.new('RGBA', (SW, PH), (0, 0, 0, 0))
    if left is not None: can.paste(left.convert('RGBA'), (0, 0))
    if right is not None: can.paste(right.convert('RGBA'), (PW, 0))
    g = np.clip(1 - np.abs(np.arange(SW) - PW) / 150, 0, 1) ** 2 * 120
    L = Image.new('RGBA', (SW, PH), (40, 26, 10, 0)); L.putalpha(Image.fromarray(np.repeat(g[None, :].astype(np.uint8), PH, 0)))
    m = can.getchannel('A'); can.alpha_composite(L); can.putalpha(m); return can
def turn(base, front, back_img, u):
    """the right sheet (front / back_img as it will read on the left) turns over the spine with a cylindrical curl.
    u 0..1. Sheet column c (distance from the spine) goes: flat (c < F), round a cylinder of radius R (F..F+pi R), flat on top (beyond)."""
    F = lerp(PW, 0, eio(u)); R = 150 * math.sin(math.pi * clamp(u * 1.05))
    out = np.asarray(base, np.float32).copy(); fr = np.asarray(front.convert('RGBA'), np.float32); bk = np.asarray(back_img.convert('RGBA'), np.float32)[:, ::-1]
    c = np.arange(PW, dtype=np.float32)
    # shadow of the lifting sheet on the page below (right of the fold)
    xs = PW + F + np.arange(int(R * 2 + 160)); xs = xs[(xs >= PW) & (xs < SW)].astype(int)
    if len(xs): out[:, xs, :3] *= (1 - 0.45 * np.clip(1 - (xs - PW - F) / (R * 2 + 160), 0, 1) ** 1.5)[None, :, None]
    flat = c < F; out[:, (PW + c[flat]).astype(int)] = fr[:, flat]
    ph = (c - F) / max(R, 1e-3)
    cyl = (c >= F) & (ph <= math.pi) & (R > 1)
    if cyl.any():
        x = (PW + F + R * np.sin(ph[cyl])).astype(int); p_ = ph[cyl]; front_side = p_ < math.pi / 2
        for sel, src, shade in ((front_side, fr, 0.62 + 0.38 * np.cos(p_)), (~front_side, bk, 0.70 + 0.30 * np.sin(p_))):
            cols = np.where(cyl)[0][sel]; xx = x[sel]; ok = (xx >= 0) & (xx < SW)
            if ok.any():
                blk = src[:, cols[ok]].copy(); blk[..., :3] *= shade[sel][ok][None, :, None]; out[:, xx[ok]] = blk
    top = (c - F) > math.pi * R
    if top.any():
        x = (PW + F - ((c[top] - F) - math.pi * R)).astype(int); ok = (x >= 0) & (x < SW)
        blk = bk[:, top][:, ok].copy(); d = (c[top][ok] - F - math.pi * R); blk[..., :3] *= (0.86 + 0.14 * np.clip(d / 200, 0, 1))[None, :, None]
        # the sheet lying over the left page throws a soft shadow at its free edge
        edge = x[ok].min() if ok.any() else None
        if edge is not None and edge > 0:
            sx = np.arange(max(0, edge - 70), edge); out[:, sx, :3] *= (1 - 0.35 * ((sx - (edge - 70)) / 70))[None, :, None]
        out[:, x[ok]] = blk
    return Image.fromarray(out.clip(0, 255).astype(np.uint8), 'RGBA')
def spread(t):
    if t < T_OPEN[0]: return spread_base(None, cover_front())
    if t < T_OPEN[1]: return turn(spread_base(None, page_r1(t)), cover_front(), endpaper(), (t - T_OPEN[0]) / (T_OPEN[1] - T_OPEN[0]))
    if t < T_TURN[0]: return spread_base(endpaper(), page_r1(t))
    if t < T_TURN[1]: return turn(spread_base(endpaper(), page_r2(t)), page_r1(t), page_l2(t), (t - T_TURN[0]) / (T_TURN[1] - T_TURN[0]))
    return spread_base(page_l2(t), page_r2(t))

def cam(t):
    """x of the spread the camera looks at: right page or left page, gliding between them"""
    pos = {'R': PW + 640, 'L': 600}
    for (a, pa), (b, pb) in zip(CAM, CAM[1:]):
        if t < b: return lerp(pos[pa], pos[pb], eio((t - a) / (b - a)) if pa != pb else 0)
    return pos[CAM[-1][1]]
def frame(t):
    sp = spread(t); z = 1.0 + 0.025 * math.sin(t * 0.25); a = math.radians(ANG); cx, cy = cam(t), 1060
    ca, sa = math.cos(a) / z, math.sin(a) / z
    co = (ca, sa, cx - ca * W / 2 - sa * H / 2, -sa, ca, cy + sa * W / 2 - ca * H / 2)
    view = sp.transform((W, H), Image.AFFINE, co, Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    # light from the top left, a gentle fall-off
    yy, xx = np.mgrid[0:H:8, 0:W:8].astype(np.float32); lg = (1.04 - 0.10 * (xx / W * 0.4 + yy / H * 0.6)).clip(0, 1)
    lg = Image.fromarray((lg * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    view = Image.merge('RGBA', [ImageChops.multiply(b, lg) for b in view.split()[:3]] + [view.split()[3]])
    can = desk().copy(); sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (16, 22), view.getchannel('A'))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(24))); can.alpha_composite(view)
    yy, xx = np.mgrid[0:H, 0:W]; vig = np.hypot((xx - W / 2) / W, (yy - H / 2) / H) * 2
    can.alpha_composite(Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), (np.clip(vig - 0.8, 0, 1) * 150).astype(np.uint8)]), 'RGBA'))
    px = np.asarray(can.convert('RGB')).astype(np.int16) + np.random.default_rng(int(t * FPS)).normal(0, 3, (H, W))[..., None].astype(np.int16)
    return Image.fromarray(px.clip(0, 255).astype(np.uint8))

if __name__ == '__main__':
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[2:]]; P = Image.new('RGB', (len(ts) * 360, 640))
        for i, t in enumerate(ts): P.paste(frame(t).resize((360, 640)), (i * 360, 0))
        P.save(B + 'out/prev.jpg', quality=88); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
