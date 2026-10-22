# Chronicle of Power: Jonathan Wainwright short (English, 1080x1920, ~62 s). Real Missouri footage frozen on the signature, words written into photos, captions on.
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
def _spr(s, fname, size, col, bold=0):
    f = {'anton': anton, 'bebas': bebas}[fname](size); bb = f.getbbox(s); w_, h_ = bb[2] - bb[0] + 80, bb[3] - bb[1] + 80
    L = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); ImageDraw.Draw(L).text((40 - bb[0], 40 - bb[1]), s, font=f, fill=col + (255,), stroke_width=bold, stroke_fill=col + (255,))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 210), (0, 0), L.getchannel('A')); sh = sh.filter(ImageFilter.GaussianBlur(9))
    out = Image.new('RGBA', L.size, (0, 0, 0, 0)); out.alpha_composite(sh, (3, 7)); out.alpha_composite(L); return out
def title(can, t, t0, s, y, size=110, col=CREAM, t1=None, fname='anton', x=CX, maxw=760, bold=0):
    """focus pull: soft and slightly large, settles sharp in 0.35 s; fades in 0.25 s at t1"""
    if t < t0 or (t1 is not None and t > t1 + 0.25): return
    f = {'anton': anton, 'bebas': bebas}[fname]
    while f(size).getlength(s) > maxw and size > 24: size -= 4
    k = eout((t - t0) / 0.35); a = k * (1.0 if t1 is None else 1 - clamp((t - t1) / 0.25))
    sp = _spr(s, fname, size, col, bold); sc = lerp(1.08, 1.0, k)
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
    p = ph[-1]; ws = [x[0].replace('ß', '\u1e9e').upper() for x in p]; f = oswald(64, 600)
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
WM = (-10, 2000, -5, 2001)   # this film has no watermark
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

# ================= Wainwright scenes =================
def ws(word, after=0.0): return wt(word, after) - 0.05
def fr(ct):   # newsreel frame at newsreel time ct (s)
    return cframe(int(round(ct * FPS)) + 1)
def film(ct, cx, cy=540, z=1.0, sat=1.0, warm=0.18):
    """9:16 window from the 1920x1080 newsreel coordinates, centre (cx, cy), zoom z; returns canvas and a film->screen mapper"""
    im = fr(ct); S = im.width / 1920; ch = 1080 / z; cw = ch * W / H
    x0 = cx - cw / 2; y0 = min(max(cy - ch / 2, 0), 1080 - ch)
    can = grade(im.resize((W, H), Image.BICUBIC, box=(x0 * S, y0 * S, (x0 + cw) * S, (y0 + ch) * S)).convert('RGBA'), warm, sat); shade(can, 200, 0.55)
    return can, (lambda x, y: ((x - x0) * W / cw, (y - y0) * H / ch))
def arrow_to(can, a, b, u, col=YEL, w_=14, head=44):
    if u <= 0: return
    e = (lerp(a[0], b[0], u), lerp(a[1], b[1], u)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line((a, e), fill=(0, 0, 0, 150), width=w_ + 8); d.line((a, e), fill=col + (255,), width=w_)
    d.polygon([(e[0] + 12 * math.cos(ang), e[1] + 12 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))], fill=col + (255,))
    can.alpha_composite(L)

def typed(can, t, t0, s_, y, size=120, col=CREAM, step=0.075, x=CX, t1=None, font=None):
    """letters arrive one by one (flat, centred)"""
    if t < t0 or (t1 is not None and t > t1 + 0.25): return
    f = font or anton(size); a = 1.0 if t1 is None else 1 - clamp((t - t1) / 0.25)
    tw_ = f.getlength(s_); xx = x - tw_ / 2
    for i, ch in enumerate(s_):
        k = eout((t - t0 - i * step) / 0.18)
        if k > 0 and ch != ' ':
            sp = _spr(ch, 'anton', f.size, col) if font is None else None
            if sp is not None:
                sp = sp.copy(); sp.putalpha(sp.getchannel('A').point(lambda v: int(v * k * a)))
                can.alpha_composite(sp, (int(xx - 40 + f.getbbox(ch)[0]), int(y - sp.height / 2 + (1 - k) * 18)))
        xx += f.getlength(ch)
class MapNB(Map):
    """coastlines only: no modern borders on a 1940s map"""
    @functools.lru_cache(None)
    def base(s):
        k = 2; im = Image.new('RGB', (W * k, H * k), SEA); d = ImageDraw.Draw(im); span = W / s.sc
        lon0, lon1 = s.c[0] - span, s.c[0] + span
        for nm, xs, ys, a, b_, c, e in ALLP:
            if b_ < lon0 - 5 or a > lon1 + 5: continue
            pts = [(((x - s.c[0]) * s.sc + W / 2) * k, (H / 2 - (y - s.c[1]) * s.sc) * k) for x, y in zip(xs, ys)]
            if len(pts) >= 3: d.polygon(pts, fill=LAND_HI if nm in s.hi else LAND, outline=LAND_HI if nm in s.hi else LAND)
        return im.resize((W, H), Image.LANCZOS)

# Missouri: MacArthur signs (film 0..3.30), the picture freezes on 'signed', the words are written on the open document, then it runs on
# and the frame slides left with him as he turns and hands the pen to Wainwright (film 5.03..5.63)
FREEZE_AT = 3.30; RESUME = None   # set below from the words
DOC1 = [(1045, 724), (1320, 721), (1342, 776), (1063, 780)]   # upper page of the open folder, above the fold (film coords)
DOC2 = [(1075, 798), (1395, 793), (1430, 860), (1103, 866)]   # lower page
def s_sign(t, w0, w1):
    t_res = ws('Then') + 0.05
    if t < FREEZE_AT: ct = t
    elif t < t_res: ct = FREEZE_AT
    else: ct = FREEZE_AT + (t - t_res)
    cx = 1230; z = 1.0
    if FREEZE_AT <= t < t_res + 0.2: z = lerp(1.0, 1.1, eio((t - FREEZE_AT) / 0.8)) if t < t_res else lerp(1.1, 1.0, eio((t - t_res) / 0.2))
    u = eio((t - ws('turned') - 0.05) / 1.3) if t > ws('turned') else 0.0
    fz = eio((t - FREEZE_AT) / 0.8) if FREEZE_AT <= t < t_res else (1 - eio((t - t_res) / 0.3) if t_res <= t < t_res + 0.3 else 0.0)
    cx = lerp(1230, 540, u) + 45 * fz
    can, m = film(ct, cx, 540 + 50 * fz, z)
    if FREEZE_AT <= t < t_res + 0.25:   # frozen frame: a touch of desaturation, the words written on the document, an arrow onto it
        out = 1 - clamp((t - t_res) / 0.25)
        t1 = ws("Japan's") - 0.1; t2 = ws('surrender') - 0.05
        if t > t1: on_quad(can, [m(*p) for p in DOC1], "JAPAN'S", 120, out, INK, anton(120), eio((t - t1) / 0.35), 0.7, mod=0.35, op=0.92)
        if t > t2: on_quad(can, [m(*p) for p in DOC2], 'SURRENDER', 120, out, RED, anton(120), eio((t - t2) / 0.4), 0.7, mod=0.3, op=0.95)
        if t > FREEZE_AT + 0.15:
            tip = m(1180, 718); arrow_to(can, (tip[0] - 160, tip[1] - 330), (tip[0] - 15, tip[1] - 25), eio((t - FREEZE_AT - 0.15) / 0.35) * out)
    if t > ws('thin') - 0.15:   # an arrow from the right, stopping short of his head, following him as he moves
        hx, hy = HEAD(ct); tip = m(hx + 95, hy); tip = (tip[0] + 10, tip[1]); tail = (min(tip[0] + 330, 900), tip[1] - 170)
        arrow_to(can, tail, tip, eio((t - ws('thin') + 0.15) / 0.35) * (1 - clamp((t - ws('Three') + 0.35) / 0.25)), YEL, 14, 46)
    return can
HEADK = [(5.0, 330, 225), (5.4, 390, 240), (5.75, 480, 330), (6.3, 410, 265), (7.0, 300, 230), (9.6, 295, 230)]   # Wainwright's head centre (film)
def HEAD(ct):
    for (a, x0, y0), (b, x1, y1) in zip(HEADK, HEADK[1:]):
        if ct <= b: u = clamp((ct - a) / (b - a)); return lerp(x0, x1, u), lerp(y0, y1, u)
    return HEADK[-1][1:]
def s_then(t, w0, w1):   # w09, pre-war portrait: 'three years earlier'
    ts = ws('surrendered', 10); bw = eio((t - ts) / 0.4) if t > ts else 0.0   # the photo turns black and white on 'surrendered'
    can = grade(fit('w09', t, w0, w1, 1.06), 0.12, lerp(0.78, 0.0, bw)); shade(can, 220, 0.5)
    if bw > 0: can.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(70 * bw))))
    title(can, t, ts, 'SURRENDERED', 900, 104, CREAM, None, 'anton')
    title(can, t, ts + 0.25, '1942', 1035, 150, YEL, None, 'anton')
    return can
def s_name(t, w0, w1):   # w08, the name
    can = grade(fit('w08', t, w0, w1, 1.06)); shade(can, 220, 0.5)
    title(can, t, ws('Jonathan'), 'JONATHAN', 1150, 120, CREAM, bold=1)
    title(can, t, ws('Wainwright'), 'WAINWRIGHT', 1290, 150, YEL, bold=1)
    return can
def s_pt(t, w0, w1):   # PT boat (MacArthur leaves), 'MARCH 1942' in the grey sky
    ct = 9.7 + (t - w0) * 0.95; can, m = film(min(ct, 17.4), 960, 540, 1.0, 1.0)
    sky(can, t, ws('March'), 'MARCH 1942', CX, 420, 130, CREAM, None, 0.5)
    return can
def s_command(t, w0, w1):   # w01, the two men in 1941: names on the sky with pointers
    can, m = side('w01', 700, 820, t, w0, w1, 1.04); shade(can, 200, 0.55)
    tt = ws('Wainwright', w0 - 0.5)
    if t > tt: f = m(1030, 235); ring(can, t, tt, f[0], f[1], YEL, 190, False)
    return can
def s_corr(t, w0, w1):   # the island under fire, the ships, the landing craft: one continuous run of the newsreel
    ct = 20.85 + (t - w0); can, m = film(min(ct, 29.3), 900 if ct < 22.95 else 960, 540, 1.0)
    sky(can, t, ws('Corregidor'), 'CORREGIDOR', CX, 470, 130, CREAM, None, 0.5, 0.0, ws('under', 22) - 0.1)
    title(can, t, ws('May', 23), 'MAY 6, 1942', 450, 120, CREAM, ws('surrendered', 24.5) - 0.35)
    typed(can, t, ws('surrendered', 24.5) - 0.05, 'SURRENDER', 450, 130, RED)
    return can
def s_ships(t, w0, w1):   # warships firing; the date on the cliff behind
    ct = 22.99 + (t - w0) * 0.55; can, m = film(min(ct, 24.15), 960, 540, 1.0)
    on_quad(can, [(150, 560), (930, 520), (940, 700), (160, 740)], 'MAY 6, 1942', 130, clamp((t - ws('May', w0)) / 0.06) if t > ws('May', w0) else 0, CREAM, anton(130), eio((t - ws('May', w0)) / 0.45), 1.0, mod=0.3, op=0.92, glow=((8, 10, 14), 10, 0.7))
    return can
def s_beach(t, w0, w1):   # men on the beach: the surrender
    ct = 29.4 + (t - w0) * 1.0; can, m = film(min(ct, 32.85), 980, 540, 1.0, 0.9)
    stamp(can, t, ws('surrendered', w0 - 0.5) - 0.03, 'SURRENDER', (CX, 1300), 110, -6)
    return can
def s_radio(t, w0, w1):   # w03, KZRH Manila: across the studio to him at the microphone, ON AIR written on the cabinet
    can, m = side('w03', 150, 1250, t, w0, w1, 1.03); shade(can, 200, 0.55)
    tt = ws('Manila', w0 - 0.5)
    title(can, t, tt, 'MANILA', 1250, 120, CREAM, None)
    t2 = ws('air', w0)
    if t > t2 - 0.25: on_quad(can, [m(*p) for p in CAB03], 'ON AIR', 130, clamp((t - t2 + 0.25) / 0.06), RED, anton(130), eio((t - t2 + 0.25) / 0.35), 0.8, mod=0.25, op=0.95, glow=((200, 30, 30), 14, 0.55))
    return can
CAB03 = [(1560, 340), (1890, 335), (1892, 470), (1562, 476)]   # back wall right of his head
def s_pow(t, w0, w1):   # w05, the gaunt general: POW on the wall behind him
    can = grade(fit('w05', t, w0, w1, 1.05)); shade(can, 210, 0.5)
    q = lambda x, y: fitpt('w05', t, w0, w1, 1.05, x, y); t1 = ws('prisoner', w0 - 0.5)
    if t > t1 - 0.2: on_quad(can, [q(*p) for p in WALL05], 'P.O.W.', 150, clamp((t - t1 + 0.2) / 0.06), CREAM, anton(150), eio((t - t1 + 0.2) / 0.4), 1.0, mod=0.35, op=0.9, glow=((8, 8, 8), 10, 0.6))
    return can
WALL05 = [(260, 430), (660, 420), (665, 640), (262, 655)]
PAC = MapNB(124.5, 29.6, 38, hi=('Philippines',))
def s_map(t, w0, w1):   # camp to camp: Corregidor, Tarlac, Formosa, Manchuria
    z = lerp(1.0, 1.04, prog(t, w0, w1)); can = grade(PAC.frame(z), 0.1, 1.0); p = lambda lon, lat: PAC.p(lon, lat, z)
    for nm, lon, lat in (('MANCHUKUO', 126.5, 46.0), ('KOREA', 127.8, 37.0), ('CHINA', 113.5, 31.0), ('JAPAN', 138.0, 37.5)):
        x, y = p(lon, lat); title(can, t, w0 + 0.2, nm, y, 46, (150, 160, 170), None, 'bebas', min(max(x, 140), 900))
    stops = [('CORREGIDOR', 120.57, 14.38, ws('more', w0 - 0.5)), ('FORMOSA', 121.6, 23.97, ws('camp', w0 - 0.5)), ('MANCHURIA', 125.1, 42.9, ws('Manchuria', w0 - 0.5))]
    pts = [p(lon, lat) for _, lon, lat, _ in stops]
    for i, (nm, lon, lat, tt) in enumerate(stops):
        if t > tt:
            x, y = pts[i]; dot(can, x, y, YEL if i == 2 else CREAM, 11); title(can, t, tt, nm, y - 60, 60, YEL if i == 2 else CREAM, None, 'bebas', min(max(x, 220), 860))
        if i and t > stops[i - 1][3]:
            u = eio((t - stops[i - 1][3]) / max(0.4, tt - stops[i - 1][3]))
            dashed(can, [pts[i - 1], pts[i]], u, YEL, 7, 22, 30 if u < 1 else 0)
    return can
def s_fear(t, w0, w1):   # w07, the cup: GAVE UP? on the wall
    can = grade(fit('w07', t, w0, w1, 1.05)); shade(can, 210, 0.5)
    q = lambda x, y: fitpt('w07', t, w0, w1, 1.05, x, y); t1 = ws('gave', w0)
    if t > t1 - 0.1: on_quad(can, [q(*p) for p in WALL07], 'GAVE UP?', 120, clamp((t - t1 + 0.1) / 0.06), INK, anton(120), eio((t - t1 + 0.1) / 0.35), 0.8, mod=0.35, op=0.92)
    return can
WALL07 = [(1150, 480), (1460, 468), (1464, 600), (1153, 612)]
def s_free(t, w0, w1):   # the general saluting at the aircraft, August 1945
    ct = 36.0 + (t - w0) * 0.85; can, m = film(min(ct, 38.9), 1050, 560, 1.0, 1.0)
    title(can, t, ws('August', w0 - 0.5), 'AUGUST 1945', 420, 110, CREAM)
    t1 = ws('freed', w0) - 0.1
    if t > t1: on_quad(can, [m(*q) for q in PLANE11], 'FREED', 120, clamp((t - t1) / 0.06), INK, anton(120), eio((t - t1) / 0.35), 0.8, mod=0.35, op=0.92)
    return can
PLANE11 = [(1080, 380), (1265, 380), (1265, 470), (1080, 470)]   # white fuselage right of his head (film coords)
def s_missouri_date(t, w0, w1):   # w10, the reunion with MacArthur, two days before the ceremony
    can, m = side('w10', 500, 380, t, w0, w1, 1.04); shade(can, 200, 0.55)
    title(can, t, ws('Two', w0 - 0.5), 'SEPTEMBER 2, 1945', 1180, 92, CREAM)
    title(can, t, ws('USS', w0 - 0.5), 'USS MISSOURI', 1310, 120, YEL)
    return can
def s_medal(t, w0, w1):   # w02, Truman pins the medal; then BLOCKED 1942
    can, m = side('w02', 760, 760, t, w0, w1, 1.03); shade(can, 200, 0.55)
    tm = ws('Medal', w0 - 0.5); te = ws('award', w0) - 0.2; tb = ws('blocked', w0) - 0.05
    for i, (s_, q) in enumerate(zip(('MEDAL', 'OF', 'HONOR'), TREES02)):
        tt = tm + i * 0.15; out = 1 - clamp((t - te) / 0.25)
        if tm <= t and out > 0: on_quad(can, [m(*p) for p in q], s_, 120, clamp((t - tt) / 0.06) * out, YEL, anton(120), eio((t - tt) / 0.3), 0.8, op=0.95, glow=((6, 8, 6), 10, 0.7))
    if tm + 0.5 < t < te + 0.25:
        a = m(1080, 560); b = m(1505, 930); arrow_to(can, a, b, eio((t - tm - 0.5) / 0.4) * (1 - clamp((t - te) / 0.25)), YEL, 12, 40)
    for i, (s_, q) in enumerate(zip(('BLOCKED', 'IN', '1942'), TREES02)):
        tt = tb + i * 0.15
        if t > tt: on_quad(can, [m(*p) for p in q], s_, 120, clamp((t - tt) / 0.06), RED, anton(120), eio((t - tt) / 0.3), 0.8, op=0.95, glow=((6, 8, 6), 10, 0.7))
    return can
TREES02 = [[(840, 200), (1300, 200), (1300, 310), (840, 310)], [(980, 320), (1160, 320), (1160, 400), (980, 400)], [(840, 410), (1300, 410), (1300, 520), (840, 520)]]   # foliage left of his head
def s_end(t, w0, w1):   # back on the Missouri, MacArthur signing again: Japan does the same
    ct = 7.35 + (t - w0) * 0.5; can, m = film(min(ct, 9.45), 520, 540, lerp(1.0, 1.05, prog(t, w0, w1)))
    t1 = ws('forced', w0 - 0.5); t2 = ws('watched', w0 - 0.5)
    title(can, t, t1, 'FORCED TO', 470, 96, CREAM, None, 'anton', 650, 520)
    title(can, t, t1 + 0.2, 'SURRENDER', 580, 110, CREAM, None, 'anton', 650, 520)
    title(can, t, t2, 'WATCHED JAPAN', 760, 90, YEL, None, 'anton', 650, 520)
    title(can, t, t2 + 0.25, 'SURRENDER', 870, 110, YEL, None, 'anton', 650, 520)
    return can

ANCH = [
 (0.0, s_sign, None),
 (ws('Three') - 0.1, s_then, ('fade',)),
 (ws('His', 11) - 0.1, s_name, ('fade',)),
 (ws('In', 13.5) - 0.1, s_pt, ('whip', 1)),
 (ws('and', 17) - 0.1, s_command, ('fade',)),
 (ws('On', 19.5) - 0.1, s_corr, ('whip', -1)),
 (ws('The', 28) - 0.1, s_radio, ('fade',)),
 (ws('He', 33) - 0.1, s_pow, ('fade',)),
 (ws('For', 36) - 0.1, s_map, ('fade',)),
 (ws('afraid', 40) - 0.1, s_fear, ('fade',)),
 (ws('In', 44) - 0.1, s_free, ('whip', 1)),
 (ws('Two', 47.5) - 0.1, s_missouri_date, ('fade',)),
 (ws('Weeks', 51) - 0.1, s_medal, ('fade',)),
 (ws('The', 56.5) - 0.1, s_end, ('fade',))]

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
