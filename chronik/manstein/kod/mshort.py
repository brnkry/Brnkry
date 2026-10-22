# Chronik der Macht: Erich von Manstein Shorts (Deutsch, 1080x1920, ~115 s).
# CDM look: Anton/Bebas titles in cream, gold for the key word, red stamps, no plates, no burned-in captions.
# Key words are written into the photos (paper map, sky, forest, barn door, wood panelling, curtain), every swastika blurred (lib9.BLUR),
# the newsreel is used in full and every crop keeps clear of the archive watermark (bottom left of the film).
import sys, subprocess, re, os
from lib9 import *
from scipy.ndimage import map_coordinates
CX = 540
TXT = open(B + 'code/script.txt').read().strip()
ST = []; _i = 0
for _s in re.split(r'(?<=[^\d][.!?])\s+', TXT): ST.append(WORDS[_i][1]); _i += len(_s.split())
def w(word, k): return wt(word, ST[k])
VEND = WORDS[-1][2]; T = VEND + 1.0
INK = (34, 30, 28); PAPER = (226, 216, 192); GOLD = YEL
def prog(t, w0, w1): return clamp((t - w0) / (w1 - w0))
def nxt(t0): n_ = [x for x in ST if x > t0 + 0.05]; return (n_[0] - 0.22) if n_ else None
@functools.lru_cache(None)
def caveat(z, wg=600):
    f = ImageFont.truetype(F + 'Caveat.ttf', z)
    try: f.set_variation_by_axes([wg])
    except Exception: pass
    return f

def grade(can, warm=0.12, sat=0.78):
    rgb = ImageEnhance.Color(can.convert('RGB')).enhance(sat)
    rgb = Image.blend(rgb, Image.new('RGB', (W, H), (80, 64, 44)), warm * 0.5); rgb = ImageEnhance.Contrast(rgb).enhance(1.08)
    return rgb.convert('RGBA')

# ---------- CDM text ----------
@functools.lru_cache(maxsize=512)
def _spr(s, fname, size, col):
    f = {'anton': anton, 'bebas': bebas}[fname](size); bb = f.getbbox(s); w_, h_ = bb[2] - bb[0] + 80, bb[3] - bb[1] + 80
    L = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); ImageDraw.Draw(L).text((40 - bb[0], 40 - bb[1]), s, font=f, fill=col + (255,))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 210), (0, 0), L.getchannel('A')); sh = sh.filter(ImageFilter.GaussianBlur(9))
    out = Image.new('RGBA', L.size, (0, 0, 0, 0)); out.alpha_composite(sh, (3, 7)); out.alpha_composite(L); return out
def title(can, t, t0, s, y, size=110, col=CREAM, t1=None, fname='anton', x=CX, maxw=760):
    """focus pull: soft and slightly large, settles sharp in 0.35 s; fades in 0.25 s at t1"""
    if t < t0 or (t1 is not None and t > t1 + 0.25): return
    f = {'anton': anton, 'bebas': bebas}[fname]
    while f(size).getlength(s) > maxw and size > 24: size -= 4
    k = eout((t - t0) / 0.35); a = k * (1.0 if t1 is None else 1 - clamp((t - t1) / 0.25))
    sp = _spr(s, fname, size, col); sc = lerp(1.08, 1.0, k)
    if k < 1: sp = sp.filter(ImageFilter.GaussianBlur((1 - k) * 6)); sp = sp.resize((int(sp.width * sc), int(sp.height * sc)), Image.BICUBIC)
    if a < 1: sp = sp.copy(); sp.putalpha(sp.getchannel('A').point(lambda v: int(v * a)))
    can.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height / 2)))
def stamp(can, t, t0, s, xy, size=96, rot=-8, t1=None, col=RED):
    if t < t0 or (t1 is not None and t > t1 + 0.25): return
    k = eout((t - t0) / 0.22); f = anton(size); tw_ = f.getlength(s); bw, bh = tw_ + size * 0.6, size * 1.45
    L = Image.new('RGBA', (int(bw + 40), int(bh + 40)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((20, 20, 20 + bw, 20 + bh), outline=col + (235,), width=10); d.text((20 + bw / 2, 20 + bh / 2), s, font=f, fill=col + (240,), anchor='mm')
    rng = np.random.default_rng(len(s)); m = (rng.random((L.height, L.width)) > 0.12).astype(np.uint8) * 255   # worn ink
    L.putalpha(Image.fromarray(np.minimum(np.asarray(L.getchannel('A')), m)))
    L = L.rotate(rot, expand=True, resample=Image.BICUBIC); sc = lerp(1.6, 1.0, k); L = L.resize((max(1, int(L.width * sc)), max(1, int(L.height * sc))), Image.BICUBIC)
    a = k * (1.0 if t1 is None else 1 - clamp((t - t1) / 0.25))
    if a < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
    can.alpha_composite(L, (int(xy[0] - L.width / 2), int(xy[1] - L.height / 2)))
def hand(can, t, t0, s, xy, size=96, col=CREAM, dur=0.8, t1=None):
    """handwriting, the pen moving left to right"""
    if t < t0 or (t1 is not None and t > t1 + 0.25): return
    f = caveat(size, 650); bb = f.getbbox(s); w_, h_ = bb[2] - bb[0] + 60, bb[3] - bb[1] + 60
    L = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); ImageDraw.Draw(L).text((30 - bb[0], 30 - bb[1]), s, font=f, fill=col + (255,))
    u = eio((t - t0) / dur); m = np.clip((u * (w_ + 40) - np.arange(w_)) / 40, 0, 1)
    a = np.asarray(L.getchannel('A'), np.float32) * m[None, :] * (1.0 if t1 is None else 1 - clamp((t - t1) / 0.25)); L.putalpha(Image.fromarray(a.astype(np.uint8)))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 200), (0, 0), L.getchannel('A'))
    x, y = int(xy[0] - w_ / 2), int(xy[1] - h_ / 2); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), (x + 2, y + 5)); can.alpha_composite(L, (x, y))
    return (x + 30, y + 30, x + w_ - 30, y + h_ - 30)
def strike(can, t, t0, box, col=RED, wd=9, dur=0.35):
    if t < t0: return
    u = eio((t - t0) / dur); x0, y0, x1, y1 = box; ym = (y0 + y1) / 2 + 6
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.line((x0 - 10, ym + 6, lerp(x0 - 10, x1 + 10, u), ym - 6 * u), fill=col + (255,), width=wd); can.alpha_composite(L)

# ---------- captions: the spoken phrase, current word in yellow (same look as the English shorts) ----------
CAPY0 = 1520
PHR = []; _cur = [WORDS[0]]
for a_, b_ in zip(WORDS, WORDS[1:]):
    if b_[1] - a_[2] > 0.1 or a_[0][-1] in '.,:?!' or len(_cur) >= 4: PHR.append(_cur); _cur = [b_]
    else: _cur.append(b_)
PHR.append(_cur)
def captions(can, t, y=CAPY0):
    ph = [p for p in PHR if p[0][1] - 0.05 <= t <= p[-1][2] + 0.25]
    if not ph: return
    p = ph[-1]; ws = [x[0].upper() for x in p]; f = oswald(64, 600)
    while f.getlength(' '.join(ws)) > 760 and f.size > 40: f = oswald(f.size - 4, 600)
    sp = f.getlength(' '); tot = sum(f.getlength(s) for s in ws) + sp * (len(ws) - 1); x = CX - tot / 2
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); nx_ = [q[1] for q in p[1:]] + [p[-1][2] + 0.25]
    for s, (_, a_, b_), n_ in zip(ws, p, nx_):
        on = a_ - 0.03 <= t; col = YEL if a_ - 0.03 <= t < n_ - 0.03 else (WHITE if on else (150, 146, 138))
        d.text((x, y), s, font=f, fill=col + (255,), anchor='lm'); x += f.getlength(s) + sp
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 220), (0, 0), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (3, 6)); can.alpha_composite(L)

# ---------- writing on surfaces inside a photo ----------
def ink_text(s_, size, font=None, reveal=1.0):
    f = font or anton(size); bb = f.getbbox(s_); w_ = int(bb[2] - bb[0]) + 20; h_ = int(bb[3] - bb[1]) + 20
    L = Image.new('L', (w_, h_), 0); ImageDraw.Draw(L).text((10 - bb[0], 10 - bb[1]), s_, font=f, fill=255); A = np.asarray(L).astype(np.float32) / 255
    if reveal < 1: A = A * np.clip((reveal * (w_ + 40) - np.arange(w_)) / 40, 0, 1)[None, :]
    return A
def _lum(can, box, big=25):
    g = can.crop(box).convert('L'); a = np.asarray(g, np.float32); m = np.asarray(g.filter(ImageFilter.GaussianBlur(big)), np.float32)
    return a / np.maximum(m, 8)
def _coeffs(dst, src_):
    M = []
    for (x, y), (X, Y) in zip(dst, src_): M += [[x, y, 1, 0, 0, 0, -X * x, -X * y], [0, 0, 0, x, y, 1, -Y * x, -Y * y]]
    return np.linalg.solve(np.array(M, float), np.array([c for p in src_ for c in p], float)).tolist()
def on_quad(can, quad, s_, size, a, col, font=None, reveal=1.0, blur=0.8, mod=0.0, op=0.9, glow=None):
    """write s_ into a screen quad (TL, TR, BR, BL): ink on paper, paint on wood, chalk on a wall, smoke in the sky"""
    if a <= 0.01: return
    A = ink_text(s_, size, font, reveal); h_, w_ = A.shape; T_ = Image.fromarray((A * 255 * a * op).astype(np.uint8))
    M_ = T_.transform((W, H), Image.PERSPECTIVE, _coeffs(quad, [(0, 0), (w_, 0), (w_, h_), (0, h_)]), Image.BICUBIC)
    if blur: M_ = M_.filter(ImageFilter.GaussianBlur(blur))
    if glow:
        G = Image.new('RGBA', (W, H), glow[0] + (0,)); G.putalpha(M_.filter(ImageFilter.GaussianBlur(glow[1])).point(lambda v: int(v * glow[2]))); can.alpha_composite(G)
    bx = M_.getbbox()
    if not bx: return
    al = np.asarray(M_.crop(bx), np.float32)
    if mod: al = al * np.clip(1 - mod + mod * np.clip(_lum(can, bx), 0.3, 1.8), 0, 1.2)
    L = Image.new('RGBA', (bx[2] - bx[0], bx[3] - bx[1]), col + (0,)); L.putalpha(Image.fromarray(np.clip(al, 0, 255).astype(np.uint8))); can.alpha_composite(L, bx[:2])
def rect_quad(cx, cy, w_, h_, skew=0.0):
    return [(cx - w_ / 2, cy - h_ / 2 + skew), (cx + w_ / 2, cy - h_ / 2 - skew), (cx + w_ / 2, cy + h_ / 2 - skew), (cx - w_ / 2, cy + h_ / 2 + skew)]
def sky(can, t, t0, s, cx, cy, size, col=CREAM, font=None, dur=0.6, skew=0.0, t1=None):
    """soft smoke-like writing in the sky"""
    if t <= t0: return
    f = font or anton(size); bb = f.getbbox(s); w_, h_ = bb[2] - bb[0] + 20, bb[3] - bb[1] + 20
    a = clamp((t - t0) / 0.06) * (1.0 if t1 is None else 1 - clamp((t - t1) / 0.3))
    on_quad(can, rect_quad(cx, cy, w_, h_, skew), s, size, a, col, f, eio((t - t0) / dur), 1.4, op=0.92, glow=((8, 10, 14), 12, 0.75))

# ---------- shots ----------
def fitpt(n, t, w0, w1, z1, sx, sy):
    im = src(n); z = lerp(1.0, z1, clamp((t - w0) / (w1 - w0))); pw = im.width * H / im.height
    cw, ch = im.width / z, im.height / z; x0 = (W - pw) / 2
    return (x0 + (sx - (im.width / 2 - cw / 2)) * pw / cw, (sy - (im.height / 2 - ch / 2)) * H / ch)
def P(n, z1=1.07, ov=None):
    def fn(t, w0, w1):
        can = grade(fit(n, t, w0, w1, z1)); shade(can, 200, 0.55)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
def side(n, sxa, sxb, t, w0, w1, z1=1.05, u=None):
    """landscape photo at full height, the frame sliding from source x sxa to sxb; returns the canvas and a source to screen mapper"""
    im = src(n); sc = H / im.height; u = prog(t, w0, w1) if u is None else u; z = lerp(1.0, z1, prog(t, w0, w1)); vw, vh = W / (sc * z), H / (sc * z)
    sx0 = lerp(sxa, sxb, u) + (W / sc - vw) / 2; sy0 = (im.height - vh) / 2
    can = grade(im.resize((W, H), Image.BICUBIC, box=(sx0, sy0, sx0 + vw, sy0 + vh)).convert('RGBA'))
    return can, lambda x, y: ((x - sx0) * sc * z, (y - sy0) * sc * z)
CLIPN = len([f for f in os.listdir(B + 'clip4k') if f.endswith('.jpg')])
@functools.lru_cache(maxsize=4)
def cframe(i): return Image.open(B + 'clip4k/f%05d.jpg' % max(1, min(CLIPN, i))).convert('RGB')
WM = (90, 880, 460, 1020)   # archive watermark, in 1920x1080 film coordinates: no crop may touch it
def C(a, b, ov=None, cx=0.5, z1=1.06, speed=1.0, z0=1.0, cy=0.5, dim_=0):
    def fn(t, w0, w1):
        rate = min(speed, (b - a) / max(0.1, w1 - w0)); s_ = min(a + (t - w0) * rate, b - 0.04)
        im = cframe(int(s_ * FPS) + 1); S = im.width / 1920; z = lerp(z0, z1, prog(t, w0, w1)); ch = 1080 / z; cw = ch * W / H
        x0 = min(max(cx * 1920 - cw / 2, 0), 1920 - cw); y0 = min(max(cy * 1080 - ch / 2, 0), 1080 - ch)
        if x0 < WM[2] and y0 + ch > WM[1]:   # would show the watermark: zoom in on the part above it
            ch = min(ch, WM[1] - 6); cw = ch * W / H; y0 = min(y0, WM[1] - 6 - ch); x0 = min(max(cx * 1920 - cw / 2, 0), 1920 - cw)
        can = grade(im.resize((W, H), Image.BICUBIC, box=(x0 * S, y0 * S, (x0 + cw) * S, (y0 + ch) * S)).convert('RGBA'), 0.18, 1.0); shade(can, 200, 0.55)
        if dim_: dim(can, dim_)
        if ov: ov(can, t, w0, w1)
        return can
    return fn

# ---- scenes ----
def s_hook(t, w0, w1):   # seg 9: Manstein on the observation post
    can = C(21.25, 23.35, None, 0.66, 1.18, 1.0, 1.08, 0.35)(t, w0, w1)
    stamp(can, t, w('nicht', 0) - 0.03, 'ABGELEHNT', (CX, 1360), 104, -7, nxt(w('nicht', 0)))
    return can
def s_france(t, w0, w1):   # seg 1, framed on the planes at the left: the flag and its swastika stay outside the crop
    can = C(0.2, 5.3, None, 0.15, 1.3, 1.0, 1.3, 0.3)(t, w0, w1); k = 1
    sky(can, t, w('sechs', k) - 0.04, '6 WOCHEN', CX, 520, 170, CREAM, None, 0.5)
    return can
def s_name(t, w0, w1):   # m03, the whole of sentences 2 and 3: the birth name is written and then crossed out
    can = grade(fit('m03', t, w0, w1, 1.08)); shade(can, 230, 0.5); k = 2
    title(can, t, w('Manstein', k) - 0.05, 'ERICH VON MANSTEIN', 1060, 104, CREAM, ST[4] - 0.22)
    if t > w('Lewinski', k) - 0.3:
        bx = hand(can, t, w('Lewinski', k) - 0.3, 'Fritz Erich von Lewinski', (CX, 1285), 84, CREAM, 0.7, ST[4] - 0.22)
        if bx and t < ST[4]: strike(can, t, w('Namen', 3) - 0.05, bx)
    if t > w('Namen', 3): hand(can, t, w('Namen', 3) + 0.25, 'von Manstein', (CX, 1390), 92, GOLD, 0.55, ST[4] - 0.22)
    return can
def s_ww1(t, w0, w1):   # m02, sky behind him
    can = grade(fit('m02', t, w0, w1, 1.07)); shade(can, 200, 0.55); k = 4
    sky(can, t, w('Ersten', k) - 0.05, '1914', 330, 470, 190, CREAM, None, 0.5)
    return can
def s_plan(t, w0, w1):   # m05, the sickle arrow is drawn on the paper map on the table
    can = grade(fit('m05', t, w0, w1, 1.06)); shade(can, 200, 0.6); k = 5
    t0 = w('Ardennen', k) - 0.1
    if t > t0:
        q = lambda x, y: fitpt('m05', t, w0, w1, 1.06, x, y)
        pts = [q(*p) for p in MAP05]; u = eio((t - t0) / 0.9); n = max(2, int(len(pts) * u))
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.line(pts[:n], fill=RED + (235,), width=12, joint='curve')
        e, p_ = pts[n - 1], pts[max(0, n - 3)]; ang = math.atan2(e[1] - p_[1], e[0] - p_[0]); hd = 40
        d.polygon([(e[0] + 10 * math.cos(ang), e[1] + 10 * math.sin(ang)), (e[0] - hd * math.cos(ang - .5), e[1] - hd * math.sin(ang - .5)), (e[0] - hd * math.cos(ang + .5), e[1] - hd * math.sin(ang + .5))], fill=RED + (235,))
        can.alpha_composite(L.filter(ImageFilter.GaussianBlur(0.8)))
        on_quad(can, [q(*p) for p in ARD05], 'ARDENNEN', 120, clamp((t - t0) / 0.06), INK, anton(120), eio((t - t0) / 0.4), 0.8, mod=0.4, op=0.85)
    return can
MAP05 = [(820, 1720), (700, 1660), (560, 1640), (420, 1680), (300, 1760), (190, 1820)]   # on the paper, east to west
ARD05 = [(500, 1560), (860, 1545), (880, 1620), (515, 1640)]
def s_forest(t, w0, w1):   # seg 3: wooded hills from the air, the words laid onto the forest
    can = C(7.95, 10.0, None, 0.62, 1.1, 0.6, 1.0, 0.5)(t, w0, w1); k = 5
    t0 = w('passierbar', k) - 0.25
    if t > t0: on_quad(can, [(170, 1080), (910, 1040), (960, 1250), (130, 1300)], 'KAUM PASSIERBAR', 150, clamp((t - t0) / 0.06), CREAM, anton(150), eio((t - t0) / 0.45), 1.0, mod=0.35, op=0.92, glow=((8, 10, 14), 10, 0.6))
    return can
def s_reject(t, w0, w1):   # m21: the plan put aside, a stamp on the table map
    can = grade(side('m21', 300, 420, t, w0, w1)[0]); shade(can, 200, 0.6); k = 6
    _, m = side('m21', 300, 420, t, w0, w1)
    if t > w('beiseite', k) - 0.05:
        stamp(can, t, w('beiseite', k) - 0.05, 'BEISEITE GELEGT', (CX, 1400), 92, -5)
    return can
def s_car(t, w0, w1):   # m16: sent off to a corps
    can, m = side('m16', 990, 1030, t, w0, w1); shade(can, 200, 0.6); k = 6; t0 = w('Korpskommando', k) - 0.05
    if t > t0: on_quad(can, [m(*p) for p in CAR16], 'KORPSKOMMANDO', 120, clamp((t - t0) / 0.06), CREAM, anton(120), eio((t - t0) / 0.4), 0.8, mod=0.45, op=0.9)
    return can
CAR16 = [(1120, 720), (1720, 692), (1730, 815), (1125, 852)]
def s_up(t, w0, w1):   # m04: 'nach oben' chalked on the barn door with an arrow going up
    can = grade(fit('m04', t, w0, w1, 1.06)); shade(can, 200, 0.6); k = 7; t0 = w('oben', k) - 0.25
    if t > t0:
        q = lambda x, y: fitpt('m04', t, w0, w1, 1.06, x, y)
        on_quad(can, [q(*p) for p in DOOR04], 'NACH OBEN', 120, clamp((t - t0) / 0.06), (240, 238, 228), anton(120), eio((t - t0) / 0.35), 1.0, mod=0.45, op=0.9)
        u = eio((t - t0 - 0.2) / 0.4)
        if u > 0:
            a, b = q(860, 660), q(860, 330 + 330 * (1 - u)); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            d.line((a, b), fill=(240, 238, 228, 220), width=12); d.polygon([(b[0], b[1] - 34), (b[0] - 28, b[1] + 14), (b[0] + 28, b[1] + 14)], fill=(240, 238, 228, 220)); can.alpha_composite(L.filter(ImageFilter.GaussianBlur(1)))
    return can
DOOR04 = [(645, 690), (1080, 678), (1080, 815), (645, 828)]
FR = Map(3.6, 49.6, 6.8, hi=('France',))
def s_map(t, w0, w1):   # Mai 1940: the sickle cut from the Ardennes to the Channel
    can = grade(FR.frame(lerp(1.0, 1.05, prog(t, w0, w1))), 0.1, 1.0); k = 8; z = lerp(1.0, 1.05, prog(t, w0, w1))
    p = lambda lon, lat: FR.p(lon, lat, z)
    title(can, t, w0 + 0.15, 'MAI 1940', 400, 120, CREAM)
    for nm, lon, lat, dx in (('PARIS', 2.35, 48.86, 0), ('SEDAN', 4.95, 49.70, 0)):
        x, y = p(lon, lat); dot(can, x, y, CREAM, 9); title(can, t, w0 + 0.3, nm, y + 50, 46, CREAM, None, 'bebas', x)
    route_ = [p(*q) for q in ((6.0, 50.05), (5.4, 49.75), (4.95, 49.62), (4.0, 49.75), (3.0, 49.95), (1.75, 50.12))]
    u = eio((t - w('stießen', k) + 0.05) / 2.2)
    if u > 0:
        sm = []
        for i in range(len(route_) - 1):
            for v in np.linspace(0, 1, 12, endpoint=False): sm.append((lerp(route_[i][0], route_[i + 1][0], v), lerp(route_[i][1], route_[i + 1][1], v)))
        sm.append(route_[-1]); n = max(2, int(len(sm) * u)); arrow(can, sm[0], sm[n - 1], 1.0, RED, 18, 52) if n < 3 else None
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.line(sm[:n], fill=(0, 0, 0, 150), width=30, joint='curve'); d.line(sm[:n], fill=RED + (255,), width=22, joint='curve')
        e, q_ = sm[n - 1], sm[max(0, n - 3)]; ang = math.atan2(e[1] - q_[1], e[0] - q_[0]); hd = 58
        d.polygon([(e[0] + 16 * math.cos(ang), e[1] + 16 * math.sin(ang)), (e[0] - hd * math.cos(ang - .5), e[1] - hd * math.sin(ang - .5)), (e[0] - hd * math.cos(ang + .5), e[1] - hd * math.sin(ang + .5))], fill=RED + (255,))
        can.alpha_composite(L)
    xa, ya = p(5.5, 50.15); title(can, t, w('Ardennen', k) - 0.05, 'ARDENNEN', ya - 70, 58, GOLD, None, 'bebas', min(xa, 800))
    xc, yc = p(1.1, 50.75); title(can, t, w('Ärmelkanal', k) - 0.05, 'ÄRMELKANAL', yc - 40, 66, GOLD, None, 'bebas', max(xc, 260))
    return can
def s_crimea(t, w0, w1):   # m13, sky behind the two men
    can = grade(fit('m13', t, w0, w1, 1.06)); shade(can, 200, 0.55); k = 9
    pass
    title(can, t, w('Krim', k) - 0.04, 'KRIM', 1320, 150, GOLD, nxt(ST[k]))
    return can
def s_order(t, w0, w1):   # sentences 10 and 11: the order of 20 November 1941
    can = Image.new('RGBA', (W, H), (16, 15, 14, 255)); k = 10
    g = np.clip(1 - np.hypot((np.arange(W)[None, :] - CX) / 700, (np.arange(H)[:, None] - 760) / 900), 0, 1) * 40
    can.alpha_composite(Image.fromarray(np.dstack([np.full((H, W), 60, np.uint8)] * 3 + [g.astype(np.uint8)]), 'RGBA'))
    k0 = eout((t - w0 - 0.1) / 0.5); pw, ph = 760, 760; L = Image.new('RGBA', (pw + 60, ph + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((30, 30, 30 + pw, 30 + ph), fill=PAPER + (255,)); d.rectangle((30, 30, 30 + pw, 30 + ph), outline=(150, 135, 105, 255), width=3)
    lines_ = [('Der Oberbefehlshaber der 11. Armee', 34, w0 + 0.3), ('ARMEEBEFEHL', 44, w0 + 0.6), ('', 0, 0), ('Armeehauptquartier, 20. November 1941', 30, w('20.', k) - 0.1)]
    y = 90
    for s_, sz, ts in lines_:
        if sz:
            n = max(0, min(len(s_), int((t - ts) / 0.018))); d.text((30 + pw / 2, y), s_[:n], font=typew(sz), fill=INK + (255,), anchor='mm')
        y += (sz or 24) * 1.7
    rng = np.random.default_rng(3)
    for i in range(7):   # body of the order, not legible on purpose
        yy = 330 + i * 46; ww = 640 - rng.integers(0, 160) if i < 6 else 300
        d.rectangle((70, yy, 70 + ww, yy + 14), fill=(120, 110, 95, 150))
    if t > w('Befehl', k) - 0.2:
        f = caveat(70, 650); s_ = 'v. Manstein'; n = max(0, min(len(s_), int((t - w('Befehl', k) + 0.2) / 0.06))); d.text((560, 690), s_[:n], font=f, fill=(30, 36, 70, 255), anchor='mm')
    if t > w('Verständnis', 11) - 0.1:   # red pencil under the passage the narration quotes
        u = eio((t - w('Verständnis', 11) + 0.1) / 0.6); d.line((66, 498, 66 + 600 * u, 494), fill=RED + (230,), width=7)
        if u >= 1: d.line((66, 544, 66 + 520 * eio((t - w('Verständnis', 11) - 0.5) / 0.5), 540), fill=RED + (230,), width=7)
    L = L.rotate(-1.5, expand=True, resample=Image.BICUBIC)
    if k0 < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * k0)))
    sc = lerp(1.0, 1.04, prog(t, w0, w1)); L = L.resize((int(L.width * sc), int(L.height * sc)), Image.BICUBIC)
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (int(CX - L.width / 2 + 14), int(330 + 22)), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    can.alpha_composite(L, (int(CX - L.width / 2), int(330 + (1 - k0) * 40)))
    pass
    return can
def s_victims(t, w0, w1):   # m19, drained of colour; the numbers on the sand slope
    can = grade(fit('m19', t, w0, w1, 1.05), 0.05, 0.25); shade(can, 220, 0.5); dim(can, 60); k = 12
    q = lambda x, y: fitpt('m19', t, w0, w1, 1.05, x, y); t1 = w('Einsatzgruppe', k) - 0.05; t2 = w('Zehntausende', k) - 0.05
    if t > t1: on_quad(can, [q(*p) for p in SLOPE19A], 'EINSATZGRUPPE D', 110, clamp((t - t1) / 0.06), CREAM, anton(110), eio((t - t1) / 0.4), 1.0, mod=0.3, op=0.9, glow=((8, 8, 8), 10, 0.6))
    if t > t2: on_quad(can, [q(*p) for p in SLOPE19B], 'ZEHNTAUSENDE', 130, clamp((t - t2) / 0.06), RED, anton(130), eio((t - t2) / 0.45), 1.0, mod=0.2, op=0.95, glow=((8, 8, 8), 10, 0.7))
    return can
SLOPE19A = [(560, 430), (1280, 405), (1290, 510), (565, 535)]
SLOPE19B = [(500, 560), (1330, 530), (1340, 690), (505, 720)]
def s_sevastopol(t, w0, w1): return C(15.5, 17.9, None, 0.6, 1.08)(t, w0, w1)
def s_dora(t, w0, w1): return C(17.95, 21.15, None, 0.55, 1.08, 1.3)(t, w0, w1)
def s_ruins(t, w0, w1):
    can = C(10.1, 11.95, None, 0.6, 1.08, 0.9)(t, w0, w1); return can
def s_sev(t, w0, w1):
    can = s_sevastopol(t, w0, w1); sky(can, t, w('Sewastopol', 13) - 0.05, 'SEWASTOPOL', CX, 520, 130, CREAM, None, 0.45); return can
def s_marshal(t, w0, w1):   # seg 10, his face, the rank on its word
    can = C(26.0, 28.4, None, 0.55, 1.12, 1.0, 1.05, 0.35)(t, w0, w1)
    title(can, t, w('Generalfeldmarschall', 13) - 0.05, 'GENERALFELDMARSCHALL', 1300, 96, GOLD, nxt(ST[13])); return can
def s_stalingrad(t, w0, w1):   # m20 over the map: the city written on the map
    can = grade(fit('m20', t, w0, w1, 1.06)); shade(can, 200, 0.6); k = 14
    pass
    title(can, t, w('Stalingrad', k) - 0.05, 'STALINGRAD', 1340, 130, GOLD, nxt(ST[k]))
    return can
MAP20 = [(330, 2190), (1050, 2170), (1060, 2290), (335, 2320)]
def s_50km(t, w0, w1):   # seg 5 and 6: guns firing, the distance
    can = C(12.0, 15.45, None, 0.6, 1.08)(t, w0, w1)
    title(can, t, w('50', 15) - 0.05, '50 KM', 1160, 210, GOLD, nxt(ST[15]))
    return can
def s_abort(t, w0, w1):   # seg 11: the burning wreck
    can = C(28.55, 33.3, None, 0.62, 1.08, 1.0)(t, w0, w1)
    stamp(can, t, w('abgebrochen', 16) - 0.03, 'ABGEBROCHEN', (CX, 1300), 100, -6, nxt(ST[16])); return can
def s_dismissed(t, w0, w1):   # m10
    can = grade(fit('m10', t, w0, w1, 1.07)); shade(can, 220, 0.5); k = 17
    stamp(can, t, w('abgesetzt', k) - 0.03, 'ABGESETZT', (CX, 1330), 110, -7, nxt(ST[k])); return can
def s_trial(t, w0, w1):   # m07 in one move: on him for 'Hamburg', then across the wood panelling where the counts are chalked
    k = 18; ts = w('In', 19) - 0.2; u = eio((t - ts) / 0.8) if t > ts else 0.0
    sx = lerp(lerp(1160, 1210, prog(t, w0, ts)), 120, u)
    can, m = side('m07', sx, sx, t, w0, w1, 1.03, 0.0); shade(can, 200, 0.6)
    if u > 0.02:
        sp = math.sin(math.pi * u)
        if sp > 0.1: can = can.filter(ImageFilter.BoxBlur(int(10 * sp)))
    pass
    if t > w('neun', 19) - 0.1:   # 17 chalk strokes on the panelling, 9 of them turn red
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); n17 = int(17 * clamp((t - w('siebzehn', 19) + 0.1) / 0.6)) if t > w('siebzehn', 19) - 0.1 else 0
        n9 = int(9 * clamp((t - w('neun', 19) + 0.1) / 0.5))
        for i in range(17):
            if i >= max(n17, n9): break
            x, y = m(150 + (i % 9) * 95, 420 + (i // 9) * 230); col = RED if i < n9 else CREAM
            d.line((x, y, x + 8, y + 150), fill=col + (235,), width=12)
        can.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.2)))
        title(can, t, w('neun', 19) - 0.05, '9 VON 17', 1110, 140, CREAM, ST[20] - 0.22)
    pass
    return can
def s_verdict(t, w0, w1):   # m15
    can = grade(fit('m15', t, w0, w1, 1.06)); shade(can, 220, 0.5); k = 20
    stamp(can, t, w('18', k) - 0.05, '18 JAHRE HAFT', (CX, 1330), 104, -6, nxt(ST[k])); return can
def s_free(t, w0, w1):   # m01
    can = grade(fit('m01', t, w0, w1, 1.06)); shade(can, 200, 0.55); k = 21
    title(can, t, ST[k] + 0.05, '1953', 1180, 150, CREAM, nxt(ST[k]))
    return can
def s_book(t, w0, w1):   # 1955: the memoirs
    can = Image.new('RGBA', (W, H), (16, 15, 14, 255)); k = 22
    if t > w('Buch', k) - 0.25:
        u = eout((t - w('Buch', k) + 0.25) / 0.5); bw, bh = 560, 800
        L = Image.new('RGBA', (bw + 60, bh + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rectangle((30, 30, 30 + bw, 30 + bh), fill=(64, 30, 26, 255)); d.rectangle((30, 30, 52, 30 + bh), fill=(44, 20, 18, 255))
        d.rectangle((80, 110, bw - 20, 114), fill=GOLD + (255,)); d.rectangle((80, bh - 60, bw - 20, bh - 56), fill=GOLD + (255,))
        d.text((30 + bw / 2 + 10, 190), 'ERICH VON MANSTEIN', font=bebas(54), fill=GOLD + (255,), anchor='mm')
        if t > w('Verlorene', k) - 0.1:
            n = clamp((t - w('Verlorene', k) + 0.1) / 0.45)
            d.text((30 + bw / 2 + 10, 420), 'VERLORENE', font=anton(92), fill=GOLD + (int(255 * n),), anchor='mm'); d.text((30 + bw / 2 + 10, 530), 'SIEGE', font=anton(120), fill=GOLD + (int(255 * n),), anchor='mm')
        sc = lerp(0.85, 1.0, u) * lerp(1.0, 1.03, prog(t, w0, w1)); L = L.resize((int(L.width * sc), int(L.height * sc)), Image.BICUBIC)
        if u < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * u)))
        sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); x, y = int(CX - L.width / 2), int(960 - L.height / 2 + 60)
        sh.paste((0, 0, 0, 200), (x + 18, y + 26), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22))); can.alpha_composite(L, (x, y))
    return can
def s_others(t, w0, w1):   # m08: arrows from him to the others
    can, m = side('m08', 860, 940, t, w0, w1); shade(can, 200, 0.6); k = 23
    return can
def s_silence(t, w0, w1):   # m18
    can = grade(fit('m18', t, w0, w1, 1.06), 0.1, 0.6); shade(can, 220, 0.5); k = 24
    title(can, t, w('kaum', k) - 0.05, 'KAUM ERWÄHNT', 1380, 120, RED, nxt(ST[k])); return can
def s_clean(t, w0, w1):   # m14 in one move: his face, then across to the curtain where the legend is written and struck out
    k = 25; ts = w('Jahrzehntelang', k) + 0.6; u = eio((t - ts) / 0.8) if t > ts else 0.0
    sx = lerp(1150, 60, u); can, m = side('m14', sx, sx, t, w0, w1, 1.03, 0.0); shade(can, 200, 0.6)
    if u > 0.02:
        sp = math.sin(math.pi * u)
        if sp > 0.1: can = can.filter(ImageFilter.BoxBlur(int(10 * sp)))
    t1 = w('saubere', k) - 0.05
    if t > t1:
        for s_, (x0, y0, x1, y1), tt in (('DER SAUBERE', (110, 540, 780, 700), t1), ('STRATEGE', (150, 740, 740, 920), w('Stratege', k) - 0.05)):
            if t > tt: on_quad(can, [m(x0, y0), m(x1, y0 + 10), m(x1, y1 + 10), m(x0, y1)], s_, 140, clamp((t - tt) / 0.06), CREAM, anton(140), eio((t - tt) / 0.4), 1.0, mod=0.35, op=0.9, glow=((6, 6, 8), 10, 0.6))
        if t > w('anders', 26) - 0.1:
            a, b = m(120, 650), m(790, 615); u2 = eio((t - w('anders', 26) + 0.1) / 0.35)
            L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).line((a, (lerp(a[0], b[0], u2), lerp(a[1], b[1], u2))), fill=RED + (240,), width=14); can.alpha_composite(L)
    return can
def s_end(t, w0, w1):   # m11
    can = grade(fit('m11', t, w0, w1, 1.06)); shade(can, 220, 0.5)
    return can

# ---------- timeline: (start, scene, transition into it) ----------
def at(k, word=None): return (ST[k] if word is None else w(word, k)) - 0.05
ANCH = [
 (0.0, s_hook, None), (at(1), s_france, ('whip', 1)),
 (at(2), s_name, ('fade',)),
 (at(4), s_ww1, ('fade',)),
 (at(5), s_plan, ('fade',)), (at(5, 'ein'), s_forest, ('fade',)),
 (at(6), s_reject, ('fade',)), (at(6, 'schob'), s_car, ('whip', -1)),
 (at(7), s_up, ('fade',)),
 (at(8), C(5.45, 7.85, None, 0.6, 1.08), ('whip', 1)), (at(8, 'stießen'), s_map, ('fade',)),
 (at(9), s_crimea, ('fade',)),
 (at(10), s_order, ('fade',)),
 (at(12), s_victims, ('fade',)),
 (at(13), s_ruins, ('fade',)), (at(13, 'Sewastopol'), s_sev, ('fade',)), (at(13, 'und'), s_dora, ('whip', 1)), (at(13, 'wurde'), s_marshal, ('fade',)),
 (at(14), s_stalingrad, ('fade',)),
 (at(15), s_50km, ('fade',)),
 (at(16), s_abort, ('fade',)),
 (at(17), s_dismissed, ('fade',)),
 (at(18), s_trial, ('fade',)),
 (at(20), s_verdict, ('fade',)),
 (at(21), s_free, ('fade',)),
 (at(22), s_book, ('fade',)),
 (at(23), s_others, ('fade',)),
 (at(24), s_silence, ('fade',)),
 (at(25), s_clean, ('fade',)),
 (at(27), s_end, ('fade',))]
DUR = {'fade': 0.2, 'whip': 0.34}
SC = []
for i, (s0, fn, tr) in enumerate(ANCH):
    d_in = DUR[tr[0]] if tr else 0.0; nx = ANCH[i + 1] if i + 1 < len(ANCH) else None
    d_out = DUR[nx[2][0]] if nx else 0.0
    SC.append((s0 - d_in / 2, (nx[0] + d_out / 2) if nx else T, fn, tr))
def _shift(img, dx):
    out = Image.new('RGBA', (W, H), (0, 0, 0, 255)); out.alpha_composite(img, (int(dx), 0)) if -W < dx < W else None; return out
def whip(a, b, u, d):
    e = eio(u); amt = 90 * math.sin(math.pi * u)
    def smear(im, dx):
        acc = np.zeros((H, W, 4), np.float32)
        for k in range(-3, 4): acc += np.asarray(_shift(im, dx + k * amt / 3), np.float32)
        return acc / 7
    A = smear(a, -d * e * W); B_ = smear(b, d * (1 - e) * W)
    edge = W / 2 - d * (e - 0.5) * W; xs = np.arange(W)[None, :, None]; mask = ((xs - edge) * d > 0).astype(np.float32)
    return Image.fromarray((A * (1 - mask) + B_ * mask).clip(0, 255).astype(np.uint8), 'RGBA')
def frame(t):
    act = [s for s in SC if s[0] <= t < s[1]] or [SC[-1]]
    img = act[0][2](t, act[0][0], act[0][1])
    if len(act) > 1:
        b = act[1]; u = clamp((t - b[0]) / (act[0][1] - b[0])); nimg = b[2](t, b[0], b[1])
        img = whip(img, nimg, u, b[3][1]) if b[3] and b[3][0] == 'whip' else Image.blend(img, nimg, eio(u))
    img.alpha_composite(VIG); captions(img, t)
    fade = clamp(1 - t / 0.3)
    if fade > 0: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * fade))))
    a = np.asarray(img.convert('RGB')).astype(np.int16) + np.random.default_rng(int(t * 30)).normal(0, 5, (H, W))[..., None].astype(np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); P_ = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = frame(t).convert('RGBA'); d = ImageDraw.Draw(f)
            if os.environ.get('UI'):
                d.rectangle((0, 0, W, 290), outline=(0, 255, 255, 255), width=4); d.rectangle((930, 680, W, 1580), outline=(0, 255, 255, 255), width=4); d.rectangle((0, 1580, W, H), outline=(0, 255, 255, 255), width=4)
            d.text((10, 300), '%.2f' % t, fill=(255, 0, 255, 255), font=anton(40)); P_.paste(f.convert('RGB').resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P_.save(B + sys.argv[2], quality=85); sys.exit()
    if sys.argv[1] == 'list':
        for s, e, fn, tr in SC: print(f'{s:7.2f} {e:7.2f} {getattr(fn, "__qualname__", "")} {tr}')
        sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-maxrate', '12M', '-bufsize', '20M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
