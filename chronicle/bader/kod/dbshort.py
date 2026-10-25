# Chronicle of Power: Douglas Bader short (English, 1080x1920, ~63 s). Real RAF newsreel and gun-camera film, words written into photos, captions on.
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

# ================= Douglas Bader scenes =================
def ws(word, after=0.0): return wt(word, after) - 0.05
def fr(ct): return cframe(int(round(ct * FPS)) + 1)
FULL, BOX = (0, 1920), (250, 1665)   # picture width of the full-frame shots and of the 4:3 newsreel shots (1920 coords)
def film(ct, cx, cy=540, z=1.0, sat=1.0, warm=0.14, pic=BOX, night=0.0):
    """9:16 window into the archive film (1920x1080 coords) kept inside the picture (no black side bars); returns canvas and a film->screen mapper"""
    im = fr(ct); S = im.width / 1920; ch = 1080 / z; cw = ch * W / H
    x0 = min(max(cx - cw / 2, pic[0] + 4), pic[1] - 4 - cw); y0 = min(max(cy - ch / 2, 0), 1080 - ch)
    can = grade(im.resize((W, H), Image.BICUBIC, box=(x0 * S, y0 * S, (x0 + cw) * S, (y0 + ch) * S)).convert('RGBA'), warm, sat); shade(can, 200, 0.55)
    return can, (lambda x, y: ((x - x0) * W / cw, (y - y0) * H / ch))
def arrow_to(can, a, b, u, col=YEL, w_=14, head=44):
    if u <= 0: return
    e = (lerp(a[0], b[0], u), lerp(a[1], b[1], u)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line((a, e), fill=(0, 0, 0, 150), width=w_ + 8); d.line((a, e), fill=col + (255,), width=w_)
    d.polygon([(e[0] + 12 * math.cos(ang), e[1] + 12 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))], fill=col + (255,))
    can.alpha_composite(L)
def chute(can, x, y, s=1.0, a=1.0, sway=0.0, q=False):
    """a small crate under a parachute, drawn in cream with a dark edge; q puts a question mark on the crate"""
    if a <= 0: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); A = int(255 * a); r = 70 * s; cy = y - 150 * s
    for wd, c in ((7, (10, 10, 12, int(170 * a))), (3, CREAM + (A,))):
        d.pieslice((x - r + sway, cy - r * 0.8, x + r + sway, cy + r * 0.8), 180, 360, fill=None if wd == 3 else c, outline=c, width=wd)
        for k in (-1, -0.35, 0.35, 1):
            d.line((x + sway + k * r, cy, x + k * 14 * s, y - 22 * s), fill=c, width=max(2, wd - 4))
    d.pieslice((x - r + sway + 3, cy - r * 0.8 + 3, x + r + sway - 3, cy + r * 0.8 - 3), 180, 360, fill=CREAM + (int(215 * a),))
    d.rectangle((x - 26 * s, y - 24 * s, x + 26 * s, y + 24 * s), fill=(150, 116, 70, A), outline=(10, 10, 12, A), width=4)
    if q: d.text((x, y + 2), '?', font=anton(int(40 * s)), fill=CREAM + (A,), anchor='mm')
    can.alpha_composite(L)
def ringp(can, t, t0, x, y, r, col=YEL, label=None, ly=None, size=58):
    """a circle drawn round a face, with its name under or over it"""
    if t < t0: return
    u = eio((t - t0) / 0.45); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for wd, c in ((14, (0, 0, 0, 140)), (8, col + (255,))): d.arc((x - r, y - r, x + r, y + r), -90, -90 + 360 * u, fill=c, width=wd)
    can.alpha_composite(L)
    if label and 120 < x < 960: title(can, t, t0 + 0.2, label, ly if ly is not None else y + r + 50, size, col, None, 'bebas', x)   # the name stays with the face
def paper(can, t, w0, w1, lines_, top=360, pw=780, ph=760, rot=-1.2):
    """a typed message on a sheet of paper, lines typed in at their own times"""
    k0 = eout((t - w0 - 0.05) / 0.45); L = Image.new('RGBA', (pw + 60, ph + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((30, 30, 30 + pw, 30 + ph), fill=(232, 227, 212, 255)); d.rectangle((30, 30, 30 + pw, 30 + ph), outline=(150, 140, 120, 255), width=3)
    y = 110
    for s_, sz, ts, col in lines_:
        if sz:
            n = max(0, min(len(s_), int((t - ts) / 0.025))); d.text((30 + pw / 2, y), s_[:n], font=typew(sz), fill=col + (255,), anchor='mm')
        y += (sz or 24) * 1.75
    L = L.rotate(rot, expand=True, resample=Image.BICUBIC)
    if k0 < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * k0)))
    sc = lerp(1.0, 1.04, prog(t, w0, w1)); L = L.resize((int(L.width * sc), int(L.height * sc)), Image.BICUBIC)
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (int(CX - L.width / 2 + 14), int(top + 22)), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    can.alpha_composite(L, (int(CX - L.width / 2), int(top + (1 - k0) * 40)))
def film_fit(ct, cy=760, wscale=1.0):
    """the whole 16:9 frame across the screen (no crop into the face), the empty space above and below filled with a blurred copy"""
    im = fr(ct).convert('RGB'); bg = im.resize((int(H * 16 / 9), H), Image.BILINEAR); x0 = (bg.width - W) // 2
    bg = bg.crop((x0, 0, x0 + W, H)).filter(ImageFilter.GaussianBlur(28)); bg = ImageEnhance.Brightness(bg).enhance(0.55)
    fw = int(W * wscale); fh = int(fw * 9 / 16); fg = im.resize((fw, fh), Image.BICUBIC)
    bg.paste(fg, ((W - fw) // 2, int(cy - fh / 2))); return grade(bg.convert('RGBA'), 0.14, 1.0)
def rquad(cx, cy, s_, h, ang, font=None):
    """quad (source coords) for s_ with its true aspect, h high, centred on (cx, cy), turned by ang degrees (along a slanted surface)"""
    f = font or anton(200); bb = f.getbbox(s_); w = h * (bb[2] - bb[0] + 20) / (bb[3] - bb[1] + 20); a = math.radians(ang)
    ux, uy, vx, vy = math.cos(a) * w / 2, math.sin(a) * w / 2, -math.sin(a) * h / 2, math.cos(a) * h / 2
    return [(cx - ux - vx, cy - uy - vy), (cx + ux - vx, cy + uy - vy), (cx + ux + vx, cy + uy + vy), (cx - ux + vx, cy - uy + vy)]
def tquad(cx, cy, s_, h, font=None, tilt=0.0):
    """quad (source coords) for s_ with its true aspect, h high, centred on (cx, cy); tilt lifts the right end"""
    f = font or anton(200); bb = f.getbbox(s_); w = h * (bb[2] - bb[0] + 20) / (bb[3] - bb[1] + 20)
    return [(cx - w / 2, cy - h / 2 + tilt), (cx + w / 2, cy - h / 2 - tilt), (cx + w / 2, cy + h / 2 - tilt), (cx - w / 2, cy + h / 2 + tilt)]
def night(can, k=1.0):
    rgb = can.convert('RGB'); n = Image.blend(rgb, ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(0.3)).enhance(0.45), k)
    return Image.blend(n, Image.new('RGB', (W, H), (18, 30, 58)), 0.28 * k).convert('RGBA')

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

# --- planes over occupied France (what was in the box stays open until the end)
def s_open(t, w0, w1):
    can, m = film(17.0 + (t - w0), 960, 620, 1.05)   # the formation, the bomber, the fighters: the film at its own speed
    sky(can, t, ws('occupied'), 'OCCUPIED FRANCE', CX, 430, 104, CREAM, None, 0.5)
    title(can, t, ws('August'), 'AUGUST 1941', 1290, 110, YEL)
    return can
# --- who it was for: the man himself, close up (post-war footage)
def s_name(t, w0, w1):
    can = film_fit(0.4 + (t - w0), 760); shade(can, 200, 0.55)
    title(can, t, ws('prisoner') - 0.1, 'ONE PRISONER', 300, 96, CREAM, ws('Douglas') - 0.1)
    title(can, t, ws('Douglas'), 'DOUGLAS', 1150, 130, CREAM, None, bold=1)
    title(can, t, ws('Bader'), 'BADER', 1290, 170, YEL, None, bold=1)
    return can
# --- 1931: the wrecked Bulldog; the year in the sky, both legs lost
def s_crash(t, w0, w1):
    can = grade(fit('d06', t, w0, w1, 1.06), 0.1, 0.8); shade(can, 220, 0.5)
    sky(can, t, ws('Ten') - 0.05, '1931', CX, 320, 150, CREAM, None, 0.5)
    t2 = ws('both') - 0.05; q = lambda x, y: fitpt('d06', t, w0, w1, 1.06, x, y)
    if t > t2: on_quad(can, [q(*v) for v in tquad(1060, 1250, 'BOTH LEGS', 150, tilt=22)], 'BOTH LEGS', 150, clamp((t - t2) / 0.06), (178, 62, 40), anton(150), eio((t - t2) / 0.4), 0.9, mod=0.45, op=0.95, glow=((10, 6, 4), 8, 0.45))
    title(can, t, ws('crash'), 'AMPUTATED', 1370, 70, CREAM, None, 'bebas')
    return can
# --- back in a Spitfire (his initials DB on the side): arrow to the legs as he climbs in
FLY0 = None   # set after ANCH (start of s_fly): the map keeps this film running behind it
CANOPY = [(14.4, 1370, 598), (15.0, 1410, 615), (15.6, 1420, 620), (16.2, 1520, 622), (16.8, 1540, 628)]   # centre of the canopy glass (film coords)
def canopy(ct):
    for (a, x0, y0), (b, x1, y1) in zip(CANOPY, CANOPY[1:]):
        if ct <= b: u = clamp((ct - a) / (b - a)); return lerp(x0, x1, u), lerp(y0, y1, u)
    return CANOPY[-1][1:]
def s_fly(t, w0, w1):
    ct = 14.4 + (t - w0); gx, gy = canopy(ct); can, m = film(ct, gx - 150, 560, 1.0)   # the window follows the glass, so the words stay put on it
    t1 = ws('artificial', 11) - 0.1
    if t > t1:
        a = clamp((t - t1) / 0.06)
        on_quad(can, [m(*v) for v in tquad(gx - 40, gy - 27, 'ARTIFICIAL', 40, tilt=2)], 'ARTIFICIAL', 120, a, YEL, anton(120), eio((t - t1) / 0.35), 0.7, mod=0.25, op=0.95, glow=((0, 0, 0), 8, 0.6))
        on_quad(can, [m(*v) for v in tquad(gx - 40, gy + 24, 'LEGS', 40, tilt=2)], 'LEGS', 120, a, YEL, anton(120), eio((t - t1 - 0.2) / 0.3), 0.7, mod=0.25, op=0.95, glow=((0, 0, 0), 8, 0.6))
    return can
# --- the Channel: from England to Saint-Omer, shot down over France
CH = MapNB(1.55, 51.05, 4.4, hi=('United Kingdom',))
def s_map(t, w0, w1):
    z = lerp(1.0, 1.05, prog(t, w0, w1)); p = lambda lon, lat: CH.p(lon, lat, z)
    bg, _ = film(14.4 + (t - FLY0), 1500, 560, 1.1); bg = bg.filter(ImageFilter.GaussianBlur(9))   # the film keeps running behind the map
    can = Image.blend(bg, grade(CH.frame(z), 0.1, 1.0), 0.5)
    title(can, t, w0 + 0.1, '9 AUGUST 1941', 430, 110, CREAM)
    for nm, lon, lat in (('ENGLAND', 0.2, 51.75), ('FRANCE', 2.7, 49.95)):
        x, y = p(lon, lat); title(can, t, w0 + 0.3, nm, y, 54, (150, 160, 172), None, 'bebas', min(max(x, 170), 820))
    a = p(0.9, 51.25); b = p(1.95, 50.72); t1 = w0 + 0.3; ts_ = ws('shot', 13) - 0.05
    dashed(can, [a, b], eio((t - t1) / max(0.4, ts_ - t1)), YEL, 7, 22, 30)
    x, y = p(2.25, 50.75)
    if t > ts_ - 0.2:
        dot(can, x, y, CREAM, 10); title(can, t, ts_ - 0.2, 'SAINT-OMER', y - 55, 52, CREAM, None, 'bebas', min(x + 40, 880))
    if t > ts_:
        k = eout((t - ts_) / 0.25); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); r = 34 * k
        bx, by = b
        for wd, c in ((18, (0, 0, 0, 160)), (11, RED + (255,))): d.line((bx - r, by - r, bx + r, by + r), fill=c, width=wd); d.line((bx - r, by + r, bx + r, by - r), fill=c, width=wd)
        can.alpha_composite(L); title(can, t, ts_, 'SHOT DOWN', by + 110, 100, RED, None, 'anton', min(max(bx, 260), 820))
    return can
# --- gun camera: a fighter going down; the leg that stayed in the cockpit
def s_bail(t, w0, w1):
    ct = 23.95 + (t - w0) * min(1.0, 3.7 / (w1 - w0)); can, m = film(ct, 960, 540, 1.0)
    title(can, t, ws('right', 17) - 0.05, 'HIS RIGHT LEG', 430, 100, CREAM)
    typed(can, t, ws('torn', 20) - 0.05, 'TORN OFF', 1260, 130, RED)
    return can
# --- Adolf Galland, the German ace
def s_galland(t, w0, w1):
    can = grade(fit('d05', t, w0, w1, 1.05, 0.15)); shade(can, 230, 0.5)
    title(can, t, ws('Adolf', 21), 'ADOLF', 1150, 120, CREAM, None, bold=1)
    title(can, t, ws('Galland', 21), 'GALLAND', 1290, 160, YEL, None, bold=1)
    title(can, t, ws('German', 21) - 0.05, 'LUFTWAFFE ACE', 430, 80, CREAM, None, 'bebas')
    return can
# --- at Galland's airfield: the two men in one picture, rings on both
def s_airfield(t, w0, w1):
    ti, tsit = ws('invited', 23) - 0.05, ws('sit', 25)   # hold on Galland, then glide to Bader
    can, m = side('d03', 0, 800, t, w0, w1, 1.04, eio((t - ti - 0.9) / max(0.3, tsit - ti - 1.0)) if t > ti + 0.9 else 0.0); shade(can, 200, 0.55)
    gx, gy = m(345, 360); bx, by = m(1275, 500); k = m(1, 0)[0] - m(0, 0)[0]   # head centres and screen scale
    ringp(can, t, ws('invited', 23) - 0.05, gx, gy, 185 * k, CREAM, 'GALLAND')
    ringp(can, t, ws('sit', 25), bx, by, 195 * k, YEL, 'BADER')
    title(can, t, ws('Messerschmitt') - 0.3, 'HIS OWN', 1150, 80, CREAM, None, 'bebas')
    title(can, t, ws('Messerschmitt') - 0.1, 'MESSERSCHMITT', 1260, 110, YEL)
    return can
# --- the Germans with his repaired leg; REPAIRED painted on the brick wall
WALL13 = [(1960, 820), (2330, 790), (2335, 930), (1965, 960)]
def s_leg(t, w0, w1):
    tw = ws('He', 31.6) - 0.1; tc = ws('climbed', 31.5) - 0.05
    u = 0.25 * clamp((t - w0) / (tw - w0)) + 0.75 * eio((t - tw) / 0.9) if t > tw else 0.25 * clamp((t - w0) / (tw - w0))
    can, m = side('d13', 900, 1392, t, w0, w1, 1.06, u); nk = eio((t - tw) / 0.9) if t > tw else 0.0
    if nk > 0: can = night(can, nk)
    shade(can, 200, 0.55)
    if t < tw + 0.4: can = leg_marks(can, m, t, 1 - clamp((t - tw) / 0.4))
    window_rope(can, m, t, tc)
    title(can, t, ws('knotted', 32) - 0.05, 'KNOTTED BEDSHEETS', 440, 92, CREAM)
    stamp(can, t, ws('caught', 34) - 0.03, 'CAUGHT', (CX, 1210), 130, 0)
    title(can, t, ws('next', 34.5), 'THE NEXT DAY', 1370, 80, CREAM, None, 'bebas')
    return can
def leg_marks(can, m, t, a):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    t1 = ws('leg', 27.5) - 0.1
    if t > t1:
        lx, ly = m(1400, 980); arrow_to(L, (lx + 300, ly - 380), (lx + 60, ly - 60), eio((t - t1) / 0.35), YEL, 14, 46)
    sky(L, t, ws('repaired', 29) - 0.05, 'REPAIRED', CX - 60, 430, 130, CREAM, None, 0.45)
    title(L, t, ws('escape', 30.5) - 0.05, 'ESCAPE', 1290, 140, RED)
    if a < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
    can.alpha_composite(L); return can
def window_rope(can, m, t, t1):
    """knotted sheets let down from the window, growing as he climbs"""
    u = eio((t - t1) / 2.2) if t > t1 else 0.0
    if u <= 0: return
    top = m(2200, 760); bot = m(2215, 1650); bot = (bot[0], min(bot[1], 1440)); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    yb = lerp(top[1], bot[1], u); n = int((yb - top[1]) / 120)
    for wd, c in ((22, (0, 0, 0, 150)), (14, (226, 222, 210, 255))): d.line((top[0], top[1], lerp(top[0], bot[0], u), yb), fill=c, width=wd)
    for i in range(1, n + 1):
        ky = top[1] + i * 120; kx = lerp(top[0], bot[0], (ky - top[1]) / (bot[1] - top[1])); d.ellipse((kx - 17, ky - 13, kx + 17, ky + 13), fill=(240, 236, 224, 255), outline=(0, 0, 0, 160), width=3)
    can.alpha_composite(L)
# --- Galland's message to England, typed
def s_word(t, w0, w1):
    can, _ = film(8.1 + (t - w0), 960, 540, 1.0); can = ImageEnhance.Brightness(can.filter(ImageFilter.GaussianBlur(10))).enhance(0.55)   # unused newsreel keeps running behind the sheet
    paper(can, t, w0, w1, [('FROM: LUFTWAFFE, SAINT-OMER', 28, w0 + 0.2, INK), ('TO: ROYAL AIR FORCE', 28, w0 + 0.6, INK), ('', 0, 0, INK),
                           ('SEND ONE PLANE', 60, ws('send', 37.5) - 0.1, INK), ('WITH A SPARE LEG.', 60, ws('spare', 38.5) - 0.3, INK), ('', 0, 0, INK),
                           ('IT WILL NOT', 60, ws('will', 39.5) - 0.15, RED), ('BE SHOT AT.', 60, ws('shot', 40) - 0.1, RED)])
    return can
# --- the RAF pilots: NO FAVORS written on the Hurricane
FUSE01 = tquad(1480, 300, 'NO FAVORS', 115, tilt=14)   # on the Hurricane's fuselage, tilted with it
def s_nofavor(t, w0, w1):
    can, m = side('d01', 820, 900, t, w0, w1, 1.04); shade(can, 200, 0.55)
    t1 = ws('favor', 41.5) - 0.1
    if t > t1: on_quad(can, [m(*q) for q in FUSE01], 'NO FAVORS', 110, clamp((t - t1) / 0.06), CREAM, anton(110), eio((t - t1) / 0.4), 0.8, mod=0.4, op=0.95, glow=((6, 6, 6), 10, 0.55))
    title(can, t, ws('enemy', 42.5) - 0.05, 'FROM THE ENEMY', 1260, 96, YEL)
    return can
# --- the raid: a Spitfire over France at its own speed
def s_raid(t, w0, w1):
    can, m = film(5.25 + (t - w0), 1000, 560, 1.0, pic=FULL)
    title(can, t, w0 + 0.1, '19 AUGUST 1941', 430, 100, CREAM)
    title(can, t, ws('raid', 45) - 0.1, 'DURING A RAID', 1290, 100, YEL)
    return can
# --- what was inside: the crate with the leg
def s_reveal(t, w0, w1):
    can, m = side('d14', 230, 330, t, w0, w1, 1.06); shade(can, 200, 0.55)
    t1 = ws('new', 46.5) - 0.1
    if t > t1: on_quad(can, [m(*v) for v in rquad(935, 768, 'A NEW LEG', 108, -31)], 'A NEW LEG', 120, clamp((t - t1) / 0.06), (165, 38, 30), anton(120), eio((t - t1) / 0.4), 0.8, mod=0.5, op=0.95)
    return can
# --- with two legs again: escape after escape, then the threat at night
def s_again(t, w0, w1):
    tn = ws('night', 53); k = eio((t - tn + 0.6) / 0.6) if t > tn - 0.6 else 0.0
    can = night(fit('d08', t, w0, w1, 1.06), 0.3 + 0.7 * k); shade(can, 210, 0.5)
    q = lambda x, y: fitpt('d08', t, w0, w1, 1.06, x, y)
    t1 = ws('escape', 49.5) - 0.1; ex, ey = q(548, 950)
    title(can, t, t1, 'ESCAPE', ey, 96, CREAM, None, 'anton', ex)   # right above the raised thumb
    if t > t1:   # one stroke per attempt, in the gap between thumb and index finger
        n = min(4, int((t - t1) / 0.4) + 1); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for i in range(n):
            a, b = q(645 + i * 40, 1075), q(635 + i * 40, 1215)
            d.line((a, b), fill=(0, 0, 0, 150), width=16); d.line((a, b), fill=CREAM + (255,), width=9)
        can.alpha_composite(L)
    lx, ly = q(1180, 1330)
    title(can, t, ws('threatened', 51.5) - 0.05, 'TAKE HIS', ly - 60, 80, RED, None, 'anton', lx)   # right of the four fingers
    title(can, t, ws('threatened', 51.5) + 0.15, 'LEGS', ly + 30, 100, RED, None, 'anton', lx)
    title(can, t, tn - 0.05, 'AT NIGHT', ly + 140, 80, (190, 205, 235), None, 'anton', lx)
    return can
# --- Colditz
def s_colditz(t, w0, w1):
    can = grade(fit('d16', t, w0, w1, 1.06, 0.1)); shade(can, 210, 0.5)
    sky(can, t, ws('Colditz') - 0.15, 'COLDITZ', 200, 330, 86, CREAM, None, 0.5)
    return can
# --- after the war: Galland and Bader laughing together
def s_end(t, w0, w1):
    can, m = side('d12', 430, 530, t, w0, w1, 1.04); shade(can, 210, 0.5)
    for s_, cy, h, col, t0 in (('THE ENEMY', 280, 36, INK, ws('enemy', 57) - 0.05), ('FRIENDS', 334, 58, (150, 30, 28), ws('friend', 59.5) - 0.05), ('FOR 40 YEARS', 388, 32, INK, ws('forty', 60) - 0.05)):
        if t > t0: on_quad(can, [m(*v) for v in tquad(1095, cy, s_, h)], s_, 120, clamp((t - t0) / 0.06), col, anton(120), eio((t - t0) / 0.4), 0.7, mod=0.4, op=0.93)
    return can

ANCH = [
 (0.0, s_open, None),
 (ws('It', 5) - 0.1, s_name, ('fade',)),
 (ws('Ten', 7.5) - 0.1, s_crash, ('fade',)),
 (ws('but', 11) - 0.1, s_fly, ('fade',)),
 (ws('Earlier', 13) - 0.1, s_map, ('fade',)),
 (ws('As', 16.8) - 0.1, s_bail, ('fade',)),
 (ws('The', 21.5) - 0.1, s_galland, ('fade',)),
 (ws('invited', 23.4) - 0.1, s_airfield, ('fade',)),
 (ws('The', 27) - 0.1, s_leg, ('fade',)),
 (ws('Galland', 36) - 0.1, s_word, ('fade',)),
 (ws('The', 41.2) - 0.1, s_nofavor, ('fade',)),
 (ws('One', 43.6) - 0.1, s_raid, ('fade',)),
 (ws('Inside', 46) - 0.1, s_reveal, ('fade',)),
 (ws('With', 48.2) - 0.1, s_again, ('fade',)),
 (ws('In', 54.2) - 0.1, s_colditz, ('fade',)),
 (ws('And', 56.6) - 0.1, s_end, ('fade',))]
FLY0 = [a for a, fn, tr in ANCH if fn is s_fly][0]

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
    fade = clamp((t - (T - 0.45)) / 0.45)   # no fade in: the film starts at once; a short fade out at the very end
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
