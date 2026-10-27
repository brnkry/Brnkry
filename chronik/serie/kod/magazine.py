# "Deutschland im Zweiten Weltkrieg" series, magazine look: an open glossy magazine (two pages) lies askew on a light desk
# and fills the 9:16 frame; the camera sits on one page at a time. Clean editorial layout: running head, serif headlines,
# body text set word by word as the narration speaks, one accent colour for key words and numbers, archive film as a
# captioned photo, fine ink illustrations drawn on. A page turns with a curl; the camera follows to the left page, then right.
import math, sys, os, functools, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
S = os.path.dirname(B.rstrip('/')) + '/'
W, H, FPS = 1080, 1920, 30
PW, PH = 1240, 2200                      # one page (page coords)
SW = 2 * PW                              # spread: left page [0, PW], spine at PW, right page [PW, 2 PW]
ANG = 3.0                                # the magazine lies a little askew
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


# ---------- magazine materials ----------
TXT, GREY, ACC, RULE = (24, 24, 28), (120, 120, 124), (178, 32, 36), (140, 150, 140)
@functools.lru_cache(None)
def serif(s, wg=400):
    f = ImageFont.truetype(S + 'sch/fonts/PlayfairDisplay%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
@functools.lru_cache(None)
def sans(s, wg=500):
    f = ImageFont.truetype(S + 'sch/fonts/Montserrat%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
@functools.lru_cache(None)
def italic(s, wg=400):
    f = ImageFont.truetype(S + 'sch/fonts/Montserrat-Italic%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
def _noise(r, h, w, scale):
    n = r.random((h // scale + 2, w // scale + 2)).astype(np.float32)
    return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
@functools.lru_cache(None)
def gloss(seed=1, spine_right=False):
    """coated magazine paper: near white, very fine grain"""
    r = np.random.default_rng(seed); t = _noise(r, PH, PW, 3) * 0.5 + _noise(r, PH, PW, 200) * 0.5
    return Image.fromarray((np.array([249, 248, 245], np.float32)[None, None] * (0.985 + 0.02 * t[..., None])).clip(0, 255).astype(np.uint8))
@functools.lru_cache(None)
def desk():
    r = np.random.default_rng(3); g = _noise(r, H, W, 200) * 0.7 + _noise(r, H, W, 4) * 0.3
    return Image.fromarray(np.stack([196 + 22 * g, 196 + 22 * g, 198 + 22 * g], -1).astype(np.uint8)).convert('RGBA')
def runhead(pg, left_side, page_no):
    """running head with three small dots and a hairline, page number at the foot"""
    d = ImageDraw.Draw(pg); x0, x1 = (150, PW - 210) if not left_side else (90, PW - 150)
    for k, c in enumerate((ACC, (150, 150, 150), (205, 205, 205))): d.ellipse((x0 + k * 34, 150, x0 + k * 34 + 22, 172), fill=c)
    d.text((x0 + 120, 161), 'CHRONIK DER MACHT', font=sans(26, 600), fill=GREY, anchor='lm')
    d.text((x1, 161), 'SERIE · TEIL 1', font=sans(26, 600), fill=GREY, anchor='rm')
    d.line((x0, 200, x1, 200), fill=(200, 200, 200), width=2)
    d.text((x0 if left_side else x1, PH - 140), str(page_no), font=sans(30, 500), fill=GREY, anchor='lm' if left_side else 'rm')

def stamp_ink(pg, A, xy, col, strength=1.0):
    """ink printed into the paper: paper * (1 - a) + ink * a"""
    x, y = int(xy[0]), int(xy[1]); reg = pg.crop((x, y, x + A.width, y + A.height)); a = np.asarray(A, np.float32)[..., None] / 255 * strength
    p = np.asarray(reg, np.float32); out = p * (1 - a) + np.array(col, np.float32) * a
    pg.paste(Image.fromarray(out.clip(0, 255).astype(np.uint8)), (x, y))

# ---------- text set word by word ----------
def words_in(pg, t, x, y, spec, font_of, lh, maxw, fade=0.22):
    """spec: list of (word, t_on, style); style 'n' normal, 'b' bold, 'a' accent bold. Words fade up into place as they are
    spoken; lines break at maxw. Returns the y under the paragraph."""
    L = Image.new('RGBA', pg.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); cx, cy = x, y
    for w_, t0, st in spec:
        f = font_of(st); ww = f.getlength(w_ + ' ')
        if cx + f.getlength(w_) > x + maxw: cx = x; cy += lh
        k = eout((t - t0) / fade) if t >= t0 else 0
        if k > 0:
            col = ACC if st == 'a' else TXT
            d.text((cx, cy + (1 - k) * 14), w_, font=f, fill=col + (int(255 * k),))
        cx += ww
    pg.paste(Image.alpha_composite(pg.convert('RGBA'), L).convert('RGB')); return cy + lh

# ---------- fine ink illustration ----------
def ink(pg, t, t0, dur, paths, col=(30, 28, 26), wd=3, a=0.95, seed=2):
    """fine pen: paths drawn in order at an even speed, no wobble"""
    if t < t0: return
    tot = sum(len(p) for p in paths); done = clamp((t - t0) / dur) * tot
    L = Image.new('L', pg.size, 0); d = ImageDraw.Draw(L)
    for p in paths:
        n = len(p); k = min(n, done); done -= n
        if k < 2: break
        d.line(p[:int(k)], fill=255, width=wd, joint='curve')
        if done <= 0: break
    bx = L.getbbox()
    if not bx: return
    A = L.crop(bx).filter(ImageFilter.GaussianBlur(0.5)).point(lambda v: int(v * a)); stamp_ink(pg, A, bx[:2], col)
def poly(pts, n=8):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = max(2, int(math.hypot(x1 - x0, y1 - y0) / n)); out += [(lerp(x0, x1, i / seg), lerp(y0, y1, i / seg)) for i in range(seg)]
    return out + [pts[-1]]
def arc(cx, cy, r, a0=0, a1=360, n=None):
    n = n or max(8, int(r / 3)); return [(cx + r * math.cos(math.radians(lerp(a0, a1, i / n))), cy + r * math.sin(math.radians(lerp(a0, a1, i / n)))) for i in range(n + 1)]
def hatch(poly_pts, step=11, ang=55):
    """diagonal shading lines clipped to a polygon"""
    m = Image.new('L', (PW, PH), 0); ImageDraw.Draw(m).polygon(poly_pts, fill=255); M = np.asarray(m) > 0
    xs = [p[0] for p in poly_pts]; ys = [p[1] for p in poly_pts]; out = []
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang)); L = max(max(xs) - min(xs), max(ys) - min(ys)) * 1.6
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    for o in np.arange(-L / 2, L / 2, step):
        pts = [(cx + o * sa + s_ * ca, cy - o * ca + s_ * sa) for s_ in np.linspace(-L / 2, L / 2, int(L / 4))]
        seg = []
        for x_, y_ in pts:
            inside = 0 <= int(x_) < PW and 0 <= int(y_) < PH and M[int(y_), int(x_)]
            if inside: seg.append((x_, y_))
            elif len(seg) > 1: out.append(seg); seg = []
            else: seg = []
        if len(seg) > 1: out.append(seg)
    return out
def tank_ink(cx, cy, s=1.0):
    """an interwar-style light tank in side view, pen outlines first, then shading"""
    P = lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
    hull = P([(-330, -10), (-300, -95), (250, -95), (330, -30), (330, 25), (-330, 25)])
    deck = P([(-300, -95), (-270, -110), (210, -110), (250, -95)])
    tur = P([(-150, -110), (-120, -205), (120, -205), (165, -110)])
    cup = P([(-80, -205), (-70, -240), (10, -240), (20, -205)])
    gun = P([(150, -170), (470, -168), (470, -150), (150, -146)])
    mant = P([(140, -185), (178, -185), (178, -132), (140, -132)])
    track = P([(-360, 20), (330, 20), (380, 70), (330, 150), (-330, 150), (-385, 75), (-360, 20)])
    lines = [poly(hull + [hull[0]]), poly(deck), poly(tur + [tur[0]]), poly(cup + [cup[0]]), poly(gun + [gun[0]]), poly(mant + [mant[0]]), poly(track)]
    for wx in np.linspace(-270, 230, 7): lines.append(arc(cx + wx * s, cy + 105 * s, 34 * s))
    lines.append(arc(cx + 330 * s, cy + 72 * s, 40 * s)); lines.append(arc(cx - 335 * s, cy + 75 * s, 40 * s))
    for wx in (-180, 0, 180): lines.append(arc(cx + wx * s, cy + 42 * s, 14 * s))
    for k in range(34): x_ = lerp(-350, 350, k / 33); lines.append(poly(P([(x_, 146), (x_ + 6, 156)])))
    for k in range(9): lines.append(arc(cx + lerp(-260, 220, k / 8) * s, cy - 70 * s, 4 * s, n=6))   # rivets
    shade = hatch(P([(-330, -10), (330, -30), (330, 25), (-330, 25)]), 10, 60) + hatch(tur[1:3] + [tur[3], P([(140, -140)])[0], P([(-140, -140)])[0]], 12, 60) + hatch(P([(-330, 120), (330, 120), (330, 150), (-330, 150)]), 8, 60)
    return lines, shade
@functools.lru_cache(None)
def ju87_lines():
    """the Ju 87 B side view traced from the plan sheet (pdf/ju87_side.png of the Ju 87 project)"""
    a = Image.open(S + 'ju87/pdf/ju87_side.png').getchannel('A'); return a.resize((a.width // 6, a.height // 6), Image.LANCZOS)
def plan_reveal(pg, t, t0, dur, xy):
    """the plan drawing appears as if inked from nose to tail"""
    if t < t0: return
    A = ju87_lines(); u = clamp((t - t0) / dur); m = np.clip((u * (A.width + 60) - np.arange(A.width)) / 60, 0, 1)[None, :]
    a = (np.asarray(A, np.float32) * 1.7 * m).clip(0, 255).astype(np.uint8); stamp_ink(pg, Image.fromarray(a), xy, (34, 34, 40))
def flag_print(pg, t, t0, x, y, w=150, h=90):
    """a printed flag of the Weimar Republic (1919), black, red, gold, with a caption"""
    if t < t0: return
    k = eout((t - t0) / 0.3); d = ImageDraw.Draw(pg)
    for i, c in enumerate(((22, 22, 22), (205, 24, 24), (250, 196, 0))):
        c2 = tuple(int(lerp(249, v, k)) for v in c); d.rectangle((x, y + i * h / 3, x + w, y + (i + 1) * h / 3), fill=c2)
    d.text((x + w + 22, y + h / 2 - 16), 'Weimarer Republik', font=sans(30, 600), fill=tuple(int(lerp(249, v, k)) for v in TXT), anchor='lm')
    d.text((x + w + 22, y + h / 2 + 20), 'Flagge ab 1919', font=italic(26), fill=tuple(int(lerp(249, v, k)) for v in GREY), anchor='lm')
def strike_red(pg, t, t0, a_, b_, wd=8):
    if t < t0: return
    u = eout((t - t0) / 0.25); e = (lerp(a_[0], b_[0], u), lerp(a_[1], b_[1], u)); ImageDraw.Draw(pg).line((a_, e), fill=ACC, width=wd)
def label(pg, t, t0, s, xy, font, col=ACC, anchor='la'):
    if t < t0: return
    k = eout((t - t0) / 0.3); ImageDraw.Draw(pg).text(xy, s, font=font, fill=tuple(int(lerp(249, v, k)) for v in col), anchor=anchor)

# ---------- archive film as a magazine photo ----------
@functools.lru_cache(maxsize=4)
def film_frame(ct):
    im = Image.open(S + 'ju87/vfull/f%05d.jpg' % max(1, int(round(ct * FPS)) + 1)).convert('RGB').crop((0, 760, 1080, 1520))
    return ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(0.15)).enhance(1.12)
def photo(pg, t, t0, ct0, box, caption):
    if t < t0: return
    k = eout((t - t0) / 0.4); x0, y0, w_, h_ = box
    fr = film_frame(ct0 + (t - t0)).resize((w_, h_), Image.LANCZOS)
    if k < 1: fr = Image.blend(Image.new('RGB', fr.size, (249, 248, 245)), fr, k)
    pg.paste(fr, (x0, y0)); d = ImageDraw.Draw(pg)
    d.line((x0, y0 + h_ + 26, x0 + 140, y0 + h_ + 26), fill=ACC, width=5)
    d.text((x0, y0 + h_ + 50), caption, font=italic(28), fill=tuple(int(lerp(249, v, k)) for v in GREY))

# ---------- the pages of this 12 s sample (narration starts at 0) ----------
T_TURN = (4.6, 5.5)
CAM = [(0.0, 'R'), (4.7, 'R'), (5.6, 'L'), (8.5, 'L'), (9.1, 'R')]
@functools.lru_cache(None)
def r1_base():
    pg = gloss(1).copy(); runhead(pg, False, 2); d = ImageDraw.Draw(pg)
    d.text((150, 245), 'DEUTSCHLAND', font=serif(112, 900), fill=TXT)
    d.text((150, 380), 'IM ZWEITEN WELTKRIEG', font=serif(68, 400), fill=TXT)
    d.text((150, 488), 'TEIL 1', font=sans(32, 700), fill=ACC); d.text((290, 484), 'Der Weg in den Krieg', font=serif(38, 400), fill=GREY)
    d.line((150, 555, 980, 555), fill=(215, 215, 215), width=2)
    return pg
def page_r1(t):
    pg = r1_base().copy()
    label(pg, t, 0.05, '1919', (150, 575), serif(124, 800), ACC)
    sp = [('20', 0.25, 'a'), ('Jahre', 0.45, 'n'), ('vor', 0.65, 'n'), ('dem', 0.8, 'n'), ('Zweiten', 0.95, 'b'), ('Weltkrieg', 1.25, 'b'), ('durfte', 1.75, 'n'),
          ('Deutschland', 2.0, 'b'), ('keinen', 2.7, 'a'), ('einzigen', 2.95, 'a'), ('Panzer', 3.25, 'a'), ('besitzen.', 3.6, 'n')]
    words_in(pg, t, 150, 760, sp, lambda st: serif(60, 700 if st in 'ab' else 400), 80, 840)
    flag_print(pg, t, 2.0, 150, 1105, 130, 78)
    lines, shade = tank_ink(540, 1360, 0.74)
    ink(pg, t, 3.0, 0.8, lines, wd=3); ink(pg, t, 3.6, 0.5, shade, wd=2, a=0.6)
    strike_red(pg, t, 4.05, (230, 1200), (900, 1500))
    label(pg, t, 4.15, 'Abb. 1 · Panzer: verboten', (150, 1530), italic(30), GREY)
    return pg
@functools.lru_cache(None)
def l2_base():
    pg = gloss(2).copy(); runhead(pg, True, 3); return pg
def page_l2(t):
    pg = l2_base().copy()
    label(pg, t, 5.6, 'Der Vertrag', (90, 280), serif(104, 400), TXT)
    label(pg, t, 6.0, 'von Versailles', (90, 400), serif(104, 800), ACC)
    label(pg, t, 6.4, '28. Juni 1919', (90, 545), sans(36, 600), GREY)
    photo(pg, t, 6.7, 9.6, (90, 640, 980, 650), 'Archivaufnahme, 1919')
    return pg
@functools.lru_cache(None)
def r2_base():
    pg = gloss(3).copy(); runhead(pg, False, 4); return pg
def page_r2(t):
    pg = r2_base().copy()
    label(pg, t, 9.1, 'Heer', (150, 280), sans(40, 700), GREY)
    label(pg, t, 9.3, '100.000', (140, 320), serif(230, 800), ACC)
    label(pg, t, 9.7, 'Mann, nicht mehr.', (150, 600), serif(64, 400), TXT)
    d = ImageDraw.Draw(pg)
    if t > 10.2: d.line((150, 720, lerp(150, 1000, eout((t - 10.2) / 0.4)), 720), fill=(215, 215, 215), width=2)
    sp = [('Luftwaffe', 10.3, 'b'), ('und', 10.65, 'n'), ('U-Boote:', 10.8, 'b'), ('verboten.', 11.1, 'a')]
    words_in(pg, t, 150, 770, sp, lambda st: serif(62, 700 if st in 'ab' else 400), 88, 900)
    plan_reveal(pg, t, 10.4, 0.9, (130, 1000))
    strike_red(pg, t, 11.35, (150, 1060), (1060, 1300))
    return pg

# ---------- the spread and the page turn ----------
def spread_base(left, right):
    """both pages on one canvas; the paper darkens where it curves into the spine"""
    can = Image.new('RGBA', (SW, PH), (0, 0, 0, 0))
    if left is not None: can.paste(left.convert('RGBA'), (0, 0))
    if right is not None: can.paste(right.convert('RGBA'), (PW, 0))
    g = np.clip(1 - np.abs(np.arange(SW) - PW) / 190, 0, 1) ** 2.2 * 110
    L = Image.new('RGBA', (SW, PH), (20, 20, 24, 0)); L.putalpha(Image.fromarray(np.repeat(g[None, :].astype(np.uint8), PH, 0)))
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
@functools.lru_cache(None)
def l0_page():
    pg = gloss(9).copy(); runhead(pg, True, 1); return pg
def spread(t):
    if t < T_TURN[0]: return spread_base(l0_page(), page_r1(t))
    if t < T_TURN[1]: return turn(spread_base(l0_page(), page_r2(t)), page_r1(t), page_l2(t), (t - T_TURN[0]) / (T_TURN[1] - T_TURN[0]))
    return spread_base(page_l2(t), page_r2(t))

def cam(t):
    """x of the spread the camera looks at: right page or left page, gliding between them"""
    pos = {'R': PW + 640, 'L': 600}
    for (a, pa), (b, pb) in zip(CAM, CAM[1:]):
        if t < b: return lerp(pos[pa], pos[pb], eio((t - a) / (b - a)) if pa != pb else 0)
    return pos[CAM[-1][1]]
def frame(t):
    sp = spread(t); z = 1.0 + 0.02 * math.sin(t * 0.25); a = math.radians(ANG); cx, cy = cam(t), 960
    ca, sa = math.cos(a) / z, math.sin(a) / z
    co = (ca, sa, cx - ca * W / 2 - sa * H / 2, -sa, ca, cy + sa * W / 2 - ca * H / 2)
    view = sp.transform((W, H), Image.AFFINE, co, Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    # soft studio light and a faint gloss sheen sweeping across the coated paper
    yy, xx = np.mgrid[0:H:8, 0:W:8].astype(np.float32); lg = (1.0 - 0.06 * (xx / W * 0.4 + yy / H * 0.6)).clip(0, 1)
    sheen = np.exp(-((xx * 0.6 + yy * 0.35 - (900 + 120 * math.sin(t * 0.3))) / 260) ** 2) * 0.05
    lgi = Image.fromarray(((lg) * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    view = Image.merge('RGBA', [ImageChops.multiply(b, lgi) for b in view.split()[:3]] + [view.split()[3]])
    shi = Image.fromarray((sheen * 255 / 0.05 * 0.05).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    view = Image.merge('RGBA', [ImageChops.add(b, ImageChops.multiply(shi, view.split()[3])) for b in view.split()[:3]] + [view.split()[3]])
    can = desk().copy(); sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 120), (14, 20), view.getchannel('A'))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26))); can.alpha_composite(view)
    px = np.asarray(can.convert('RGB')).astype(np.int16) + np.random.default_rng(int(t * FPS)).normal(0, 1.6, (H, W))[..., None].astype(np.int16)
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
