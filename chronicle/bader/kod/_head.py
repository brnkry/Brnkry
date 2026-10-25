import sys, subprocess, re, os
from lib9 import *
from scipy.ndimage import map_coordinates
CX = 540
TXT = open(B + 'code/script.txt').read().strip()
ST = []; _i = 0
for _s in re.split(r'(?<=[^\d][.!?])\s+', TXT): ST.append(WORDS[_i][1]); _i += len(_s.split())
def w(word, k): return wt(word, ST[k])
VEND = WORDS[-1][2]; T = VEND + 0.55
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
    if b_[1] - a_[2] > 0.1 or (a_[0][-1] in '.,:?!' and not re.fullmatch(r'\d+\.', a_[0])) or len(_cur) >= 4: PHR.append(_cur); _cur = [b_]
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
