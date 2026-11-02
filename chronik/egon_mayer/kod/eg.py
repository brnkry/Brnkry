# Egon Mayer, CDM Short in style A (reference a.mov), "one table" version:
# every print lies on one big table of blue-toned photos; the camera travels left/right/up/down from one group of prints to the next
# (a large out-of-focus print passes close to the lens during every move, like the 15 s transition Boran liked);
# prints are placed with sub-pixel accuracy so the slow drift is smooth; all type is centred (x = 540) and sized to the safe area.
import sys, os, json, math, subprocess, functools, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, E + '../style/code')
import styleA as A
from styleA import W, H, FPS, CREAM, YEL, INK, mont, grunge, finish, put, eout, eio, lerp, clamp
CX = 540; MAXW = 700
WORDS = json.load(open(E + 'words.json'))
def wt(s, after=0.0):
    for w, a, b in WORDS:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a
    raise KeyError(s)
def ws(s, after=0.0): return wt(s, after) - 0.04
def we(s, after=0.0):
    for w, a, b in WORDS:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return b
    raise KeyError(s)

# ---------- sources (swastikas blurred small, positions read off zoomed crops) ----------
BLUR = {'08': [(392, 491, 20), (288, 884, 24), (1145, 922, 22)], '16': [(830, 2240, 34)], '18': [(567, 170, 46), (467, 1595, 50), (686, 1168, 30), (1267, 1667, 34), (528, 1968, 72)],
        '14': [(834, 2075, 34)], '15': [(1450, 625, 170)]}
@functools.lru_cache(None)
def src(n):
    im = Image.open(glob.glob(E + 'drive/%s_*.jpg' % n)[0]).convert('RGB')
    for x, y, d in BLUR.get(n, []):
        r = d / 2; pad = int(d); box = (int(x - pad), int(y - pad), int(x + pad), int(y + pad)); reg = im.crop(box)
        bl = reg.resize((max(1, reg.width // 10), max(1, reg.height // 10)), Image.BILINEAR).resize(reg.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(d * 0.15))
        m = Image.new('L', reg.size, 0); c = reg.width / 2; ImageDraw.Draw(m).ellipse((c - r, c - r, c + r, c + r), fill=255)
        im.paste(Image.composite(bl, reg, m.filter(ImageFilter.GaussianBlur(r * 0.15))), box[:2])
    return im
CL = E + 'clip/'
@functools.lru_cache(maxsize=64)
def _fr(k, i): return Image.open(CL + '%s/%05d.jpg' % (k, i)).convert('RGB')
@functools.lru_cache(None)
def nfr(k): return len(os.listdir(CL + k))
def film(k, tt, off=0.0):
    n = nfr(k); i = min(n - 1, int(max(0.0, tt + off) * 25))   # plays forward once (clips are cut long enough for their scene)
    return _fr(k, i + 1)
def print_im(src_, wd, tone_=True, cap=None, seed=1):
    """old print with a thin white deckled border (as thin as in the reference)"""
    im = src_.convert('RGB'); ph = int(wd * im.height / im.width); im = im.resize((wd, ph), Image.LANCZOS)
    if tone_:
        g = ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.15); im = Image.merge('RGB', (g.point(lambda v: int(v * 0.93)), g.point(lambda v: int(v * 0.96)), g))
    bw = max(7, wd // 75); bb = bw * 5 if cap else bw; P_ = Image.new('RGBA', (wd + 2 * bw, ph + bw + bb), (238, 236, 230, 255)); P_.paste(im, (bw, bw))
    rng = np.random.default_rng(seed); a = np.asarray(P_.getchannel('A')).copy()
    for x in range(0, P_.width, 5):
        a[:int(rng.uniform(0, 3)), x:x + 5] = 0; a[P_.height - int(rng.uniform(0, 3)):, x:x + 5] = 0
    for y in range(0, P_.height, 5):
        a[y:y + 5, :int(rng.uniform(0, 3))] = 0; a[y:y + 5, P_.width - int(rng.uniform(0, 3)):] = 0
    gm = grunge(seed).resize(P_.size); P_ = Image.composite(P_, Image.new('RGBA', P_.size, (205, 205, 200, 255)), gm.point(lambda v: 255 if v > 120 else 215))
    P_.putalpha(Image.fromarray(a))
    if cap: ImageDraw.Draw(P_).text((bw + 10, ph + bw + bb * 0.5), cap, font=A.script(int(bb * 0.8)), fill=(70, 70, 80, 235), anchor='lm')
    return P_
@functools.lru_cache(maxsize=96)
def PR(n, wd, seed, crop=None, cap=None):
    im = src(n)
    return print_im(im.crop(crop) if crop else im, wd, True, cap, seed)
def FP(k, tt, wd, seed, cap=None, off=0.0, sp=1.0): return print_im(film(k, tt * sp, off), wd, True, cap, seed)

# ---------- smooth (sub-pixel) print placement ----------
def card(can, P_, cx, cy, rot, mb=(0, 0), alpha=1.0, sc=1.0):
    w0, h0 = P_.size; a = math.radians(rot); ca, sa = math.cos(a) * sc, math.sin(a) * sc
    hw = (abs(ca) * w0 + abs(sa) * h0) / 2; hh = (abs(sa) * w0 + abs(ca) * h0) / 2
    ix, iy = math.floor(cx - hw) - 1, math.floor(cy - hh) - 1; ow, oh = int(2 * hw) + 4, int(2 * hh) + 4
    if ix > W + 40 or iy > H + 40 or ix + ow < -40 or iy + oh < -40: return
    if ow * oh > 9e6: return
    # output pixel (u, v) -> source: inverse of (scale, rotate about the centre, translate to (cx, cy))
    ux, uy = cx - ix, cy - iy; k = 1.0 / (sc * sc)
    m = (ca * k, -sa * k, w0 / 2 - (ca * ux - sa * uy) * k, sa * k, ca * k, h0 / 2 - (sa * ux + ca * uy) * k)
    P_ = P_.transform((ow, oh), Image.AFFINE, m, resample=Image.BICUBIC)
    if alpha < 1: P_.putalpha(P_.getchannel('A').point(lambda v: int(v * alpha)))
    sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.6 * alpha)))
    paste(can, sh.filter(ImageFilter.GaussianBlur(18)), ix + 12, iy + 26)
    L = abs(mb[0]) + abs(mb[1])
    if L > 3:
        mx, my = int(abs(mb[0])) + 2, int(abs(mb[1])) + 2; loc = np.zeros((P_.height + 2 * my, P_.width + 2 * mx, 4), np.float32); a = np.asarray(P_, np.float32); n = 9
        a[..., :3] *= a[..., 3:4] / 255
        for k in range(n):
            f = (k - (n - 1) / 2) / (n - 1); dx, dy = int(round(mb[0] * f)), int(round(mb[1] * f)); loc[my + dy:my + dy + P_.height, mx + dx:mx + dx + P_.width] += a
        loc /= n; rgb = loc[..., :3] / np.maximum(loc[..., 3:4], 1e-3) * 255
        paste(can, Image.fromarray(np.dstack([np.clip(rgb, 0, 255), loc[..., 3:4]]).astype(np.uint8), 'RGBA'), ix - mx, iy - my); return
    paste(can, P_, ix, iy)
def paste(can, L, x, y):
    """alpha_composite that accepts negative positions"""
    cx0, cy0 = max(0, -x), max(0, -y)
    if cx0 >= L.width or cy0 >= L.height or x >= can.width or y >= can.height: return
    if cx0 or cy0: L = L.crop((cx0, cy0, L.width, L.height))
    can.alpha_composite(L, (x + cx0, y + cy0))
SLOW = 1.15
VIS = 1.6   # a print that already lies on the table comes into view about this long before its scene
CUR = [0.0]   # start time of the scene being drawn (drift of prints that already lie there)
def deal(can, P_, t, t0, frm, to, r0, r1, ox, oy, dur=1.0, drift=(0, 0, 0), sc0=1.25):
    """print at local position `to` (+ table offset ox, oy). t0=None: already lying there. Otherwise slides in from `frm`. Always drifting."""
    def pos(tt):
        if t0 is None: u = 1.0; d = tt - CUR[0]
        else: u = eout((tt - t0) / (dur * SLOW)); d = tt - t0
        return lerp(frm[0], to[0], u) + drift[0] * d + ox, lerp(frm[1], to[1], u) + drift[1] * d + oy, lerp(r0, r1, u) + drift[2] * d
    if t0 is not None and t < t0: return
    x, y, r = pos(t); x2, y2, _ = pos(t + 1 / FPS)
    d = t - (t0 if t0 is not None else CUR[0])
    sc = 1.0 + (sc0 - 1.0) * (1 - eout(d / 2.8)) - 0.010 * max(0.0, d) if t0 is not None else 1.0 - 0.010 * max(0.0, d)   # big on arrival, slowly further away
    card(can, P_, x, y, r, ((x2 - x) * 1.6, (y2 - y) * 1.6), sc=sc)

# ---------- type (always centred) ----------
def gtext_a(s, font, col, alphas, track=-2):
    xs = []; x = 0
    for ch in s: xs.append(x); x += font.getlength(ch) + track
    asc, desc = font.getmetrics(); L = Image.new('RGBA', (int(x) + 20, asc + desc + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for ch, xx, a in zip(s, xs, alphas):
        if a > 0: d.text((10 + xx, 10), ch, font=font, fill=col + (int(255 * a),))
    gm = grunge(len(s)).crop((0, 0, L.width, L.height)); L.putalpha(ImageChops.multiply(L.getchannel('A'), gm.point(lambda v: min(255, int(v * 1.08)))))
    return L
def typed(s, t, t0, cps=11, fade=0.22): return [clamp((t - t0 - i / cps) / fade) for i in range(len(s))]
def fit(lines, size, wg=900, track=-3, maxw=MAXW):
    while size > 24:
        f = mont(size, wg)
        if max(sum(f.getlength(c) + track for c in s) + 20 for s in lines) <= maxw: return size
        size -= 2
    return size
def strip(can, t, t0, lines, cx, cy):
    if t < t0: return
    k = eout((t - t0) / 0.75); fs = fit(lines, 32, 800, 0, MAXW - 64); f = mont(fs, 800)
    w_ = int(max(f.getlength(s) for s in lines) + 64); h_ = 24 + int(fs * 1.3) * len(lines)
    P_ = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); rng = np.random.default_rng(len(lines[0]))
    top = [(x, rng.uniform(0, 7)) for x in range(0, w_ + 1, 10)]; bot = [(x, h_ - rng.uniform(0, 7)) for x in range(w_, -1, -10)]
    d = ImageDraw.Draw(P_); d.polygon(top + bot, fill=(232, 230, 224, 255))
    ka = clamp((t - t0 - 0.6) / 0.4)
    if ka > 0:
        for i, s_ in enumerate(lines): d.text((32, 14 + i * int(fs * 1.3)), s_, font=f, fill=INK + (int(255 * ka),))
    gm = grunge(9).crop((0, 0, w_, h_)); P_.putalpha(ImageChops.multiply(P_.getchannel('A'), gm))
    m = np.clip((k * (w_ + 60) - np.arange(w_)) / 60, 0, 1); P_.putalpha(Image.fromarray((np.asarray(P_.getchannel('A'), np.float32) * m[None, :]).astype(np.uint8)))
    put(can, P_, cx, cy)
def title(can, t, big, small, cy, t_big, t_small, ox, oy, big_first=True, size=210, ssize=84, strp=None, t_strip=None, cps=11):
    """reference title: big white number counting in digit by digit + yellow lines typing on (+ torn strip); centred as one block"""
    s0 = size; sz0 = ssize
    while True:
        fb, fs = mont(size, 900), mont(ssize, 900)
        wb = sum(fb.getlength(c) - 6 for c in big) + 20; wsm = max(sum(fs.getlength(c) - 3 for c in s) + 20 for s in small) if small else 0; gap = 20 if small else 0
        if wb + gap + wsm <= MAXW or size < 50: break
        size = int(size * 0.95); ssize = int(ssize * 0.95)
    if small and size < s0 * 0.8:   # stacked: number on top, yellow lines centred underneath
        size = fit([big], s0, 900, -6); fb = mont(size, 900); ssize = fit(small, max(sz0, 70), 900, -3); fs = mont(ssize, 900)
        bottom = cy - ssize * 0.5 * len(small) + size * 0.62 + ssize * 0.95 * len(small) + (95 if strp else 0); cy += min(0, 1530 - bottom) + oy
        if t >= t_big: put(can, gtext_a(big, fb, CREAM, typed(big, t, t_big, 6, 0.25), -6), CX + ox, cy - ssize * 0.5 * len(small), 'm')
        if t >= (t_small[0] if isinstance(t_small, (list, tuple)) else t_small):
            n0 = 0
            for i, s in enumerate(small):
                ts = t_small[i] if isinstance(t_small, (list, tuple)) else t_small + n0 / cps
                L = gtext_a(s, fs, YEL, typed(s, t, ts, cps), -3); n0 += len(s)
                put(can, L, CX + ox, cy - ssize * 0.5 * len(small) + size * 0.62 + ssize * 0.55 + i * ssize * 0.95, 'm')
        if strp: strip(can, t, t_strip, strp, CX + ox, cy - ssize * 0.5 * len(small) + size * 0.62 + ssize * 0.95 * len(small) + 50)
        return
    tot = wb + gap + wsm; x0 = CX - tot / 2 + ox; cy += oy
    xb, xs = (x0, x0 + wb + gap) if big_first else (x0 + wsm + gap, x0)
    if t >= t_big: put(can, gtext_a(big, fb, CREAM, typed(big, t, t_big, 6, 0.25), -6), xb, cy, 'l')
    if small and t >= (t_small[0] if isinstance(t_small, (list, tuple)) else t_small):
        n0 = 0
        for i, s in enumerate(small):
            ts = t_small[i] if isinstance(t_small, (list, tuple)) else t_small + n0 / cps
            L = gtext_a(s, fs, YEL, typed(s, t, ts, cps), -3); n0 += len(s)
            yy = cy - (len(small) - 1) * ssize * 0.46 + i * ssize * 0.92
            put(can, L, xs if big_first else xs + wsm - L.width, yy, 'l')
    if strp: strip(can, t, t_strip, strp, CX + ox, cy + max(size * 0.5, ssize * 0.92 * len(small) / 2 if small else 0) + 40 + (24 + 42 * len(strp)) / 2)
def quote(can, t, lines, cy, ox=0, oy=0, size=72, sub=None, t_sub=None, tout=None, lh=1.06, col=None):
    """white caps, words fading in with the voice; out: words vanish from the last one"""
    size = fit([' '.join(w_ for w_, _ in l) for l in lines], size, 900, -2); f = mont(size, 900)
    N = sum(len(l) for l in lines); idx = 0
    for li, l in enumerate(lines):
        Ls = []
        for w_, t0 in l:
            a = clamp((t - t0) / 0.45)
            if tout is not None: a *= clamp(1 - (t - tout - (N - 1 - idx) * 0.03) / 0.2)
            c = (col or {}).get(li, CREAM)
            Ls.append((gtext_a(w_, f, c, [a] * len(w_), -2), a)); idx += 1
        sp = f.getlength(' ') * 0.8; tot = sum(L.width for L, _ in Ls) + sp * (len(Ls) - 1); x = CX - tot / 2 + ox; y = cy + oy + li * size * lh
        for L, a in Ls:
            if a > 0: put(can, L, x, y, 'l')
            x += L.width + sp
    if sub and t >= t_sub:
        a = clamp((t - t_sub) / 0.4)
        if tout is not None: a *= clamp(1 - (t - tout) / 0.2)
        fs = mont(fit([sub], 34, 800, 1), 800); put(can, gtext_a(sub, fs, YEL, [a] * len(sub), 1), CX + ox, cy + oy + len(lines) * size * lh + 6, 'm')
def label(can, t, t0, text, x, y, ax, ay, ox, oy, size=58):
    """Caveat handwriting with a drawn arrow to (ax, ay) (Boran likes the handwriting)"""
    if t < t0: return
    k = eout((t - t0) / 0.6); f = A.script(size); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    tw = f.getlength(text); d.text((x + ox - tw / 2, y + oy), text, font=f, fill=CREAM + (int(255 * clamp(k * 1.5)),), anchor='lm')
    sx, sy = x + ox, y + oy + (34 if ay > y else -34); ex, ey = lerp(sx, ax + ox, k), lerp(sy, ay + oy, k)
    d.line((sx, sy, ex, ey), fill=CREAM + (235,), width=5)
    if k > 0.95:
        ang = math.atan2(ey - sy, ex - sx)
        for s in (2.6, -2.6): d.line((ex, ey, ex - 26 * math.cos(ang + s * 0.2), ey - 26 * math.sin(ang + s * 0.2)), fill=CREAM + (235,), width=5)
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.5))); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)), (3, 5)); can.alpha_composite(L)

# ---------- the table ----------
DARK = np.array((14, 18, 32), np.float32); LIGHT = np.array((118, 132, 164), np.float32)
def tone(im, lo=DARK, hi=LIGHT, gamma=1.0):
    g = np.asarray(ImageOps.grayscale(im), np.float32) / 255
    if gamma != 1: g = g ** gamma
    return Image.fromarray(np.clip(lo + g[..., None] * (hi - lo), 0, 255).astype(np.uint8))
TW, TH = 2700, 3300
PILE_I = ['03', '04', '09', '10', '11', '17', '21', '22', '23', '24', '26', '16', '19', '15', '14']
PILE_C = ['b17side', 'b17cloud', 'contr', 'spit', 'dogf', 'p47', 'p47b', 'gun2', 'close', 'head']
@functools.lru_cache(None)
def table():
    """a seamless (wrapping) tile of prints, toned dark blue and a little soft, padded so any window can be cut from it"""
    cache = E + 'table.png'
    if os.path.exists(cache): return Image.open(cache).convert('RGB')
    rng = np.random.default_rng(5); can = Image.new('RGBA', (TW, TH), (20, 24, 40, 255))
    srcs = [('p', f) for f in sorted(os.listdir(E + 'pile'))] + [('i', n) for n in PILE_I + ['01', '21']] + [('c', n) for n in PILE_C]
    order = list(rng.permutation(len(srcs)))
    for k in range(90):
        kind, n = srcs[order[k % len(srcs)]]
        im = src(n) if kind == 'i' else (Image.open(E + 'pile/' + n).convert('RGB') if kind == 'p' else _fr(n, nfr(n) // 2))
        P_ = print_im(im, int(rng.uniform(560, 820)), True, None, seed=int(rng.integers(50))).rotate(rng.uniform(-30, 30), expand=True, resample=Image.BICUBIC)
        x, y = int(rng.uniform(0, TW)), int(rng.uniform(0, TH))
        sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.6))); sh = sh.filter(ImageFilter.GaussianBlur(10))
        for dx in (-TW, 0, TW):
            for dy in (-TH, 0, TH):   # wrap so the tile is seamless
                paste(can, sh, x + dx + 8, y + dy + 16); paste(can, P_, x + dx, y + dy)
    T_ = tone(can, DARK, LIGHT * 0.78, 1.15).filter(ImageFilter.GaussianBlur(2.4))
    big = Image.new('RGB', (TW + 1400, TH + 2300))
    for dx in (0, TW):
        for dy in (0, TH): big.paste(T_, (dx, dy))
    big.save(cache); return big
def table_view(cx, cy, z=1.0):
    """window of the table whose top-left is (cx, cy) in table coordinates (any real numbers)"""
    T_ = table(); x0, y0 = cx % TW, cy % TH
    return T_.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + W, y0 + H))

# ---------- hook backgrounds (full-bleed, blue-toned film) ----------
def hookbg(k, tt, dark=0.62):
    im = film(k, tt); g = np.asarray(ImageOps.grayscale(im).resize((W, H), Image.BICUBIC), np.float32) / 255
    g = np.clip((g - 0.5) * 1.15 + 0.5, 0, 1); a = DARK + g[..., None] * (LIGHT * 1.25 - DARK)
    yy = np.linspace(0, 1, H)[:, None, None]; a *= (1.0 - (1 - dark) * np.clip((yy - 0.35) / 0.35, 0, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')

# ---------- scenes on the table ----------
T2, T3, T4, T5, T6 = ws('Er'), ws('Ab', 12), ws('In', 16.9), ws('Ab', 24), ws('Sie', 29.9)
T7, T8, T9, T10, T11 = ws('Am', 37), ws('Mit', 47), ws('Der', 54), ws('Im', 63), ws('Im', 67.4)
T12, T13, T14 = ws('Im', 73.3), ws('Am', 79.9), ws('Egon', 92)
TEND = WORDS[-1][2] + 1.3
TOP, LEFT, RIGHT = 'top', 'left', 'right'
SW = 1.3      # swoop duration
SWOOP = []    # swooping prints are drawn last, in screen space, over everything
def enter(c, P_, t, t0, side, to, r1, ox, oy, drift=(0, 0, 0), dur=1.15, main=False):
    if main:
        t0 = CUR[0] - 0.15
        if t < t0: return
        d = t - t0
        if d < SW:
            u = eout(d / SW); end = (to[0] + drift[0] * d, to[1] + drift[1] * d)
            x, y = lerp(to[0] - 760, end[0], u), lerp(to[1] + 260, end[1], u); r = lerp(r1 - 16, r1 + drift[2] * d, u)
            sc = lerp(3.1, 1.0 - 0.010 * SW, u); bl = 26 * clamp((sc - 1.0) / 2.1) ** 1.2
            SWOOP.append((P_, x, y, r, sc, bl)); return
        x, y, r = to[0] + drift[0] * d + ox, to[1] + drift[1] * d + oy, r1 + drift[2] * d
        card(c, P_, x, y, r, sc=1.0 - 0.010 * d); return
    frm = {'top': (to[0], -1100), 'left': (-1100, to[1]), 'right': (W + 1100, to[1])}[side]; r0 = r1 + {'top': 8, 'left': -12, 'right': 12}[side]
    deal(c, P_, t, t0, frm, to, r0, r1, ox, oy, dur, drift)
def s_birth(c, t, ox, oy):
    enter(c, PR('09', 920, 22, cap='Egon Mayer'), t, T2b + 0.0, TOP, (540, 720), -3, ox, oy, (2, 3, 0.08), main=True)
    title(c, t, '1917', ['GEBOREN IN', 'KONSTANZ'], 1380, 7.55, [ws('geboren') - 0.3, ws('Konstanz')], ox, oy, True, 170, 74, ['1937: EINTRITT IN DIE LUFTWAFFE'], ws('1937'))
def s_jg2(c, t, ox, oy):
    enter(c, PR('24', 1000, 31), t, T3 + 0.35, LEFT, (540, 560), 3, ox, oy, (-3, 2, -0.08), main=True)
    enter(c, PR('11', 560, 32), t, T3 + 1.3, RIGHT, (750, 880), -6, ox, oy, (3, -2, 0.1))
    title(c, t, '1939', ['JAGDGESCHWADER 2', '„RICHTHOFEN“'], 1390, ws('1939'), [ws('Jagdgeschwader'), ws('„Richthofen')], ox, oy, True, 200, 62, cps=22)
def s_bob(c, t, ox, oy):
    enter(c, FP('spit', t - T4 + VIS, 1000, 41), t, T4 + 0.35, TOP, (540, 560), -2, ox, oy, (3, 2, 0.08), main=True)
    enter(c, PR('15', 760, 42), t, ws('Einmal') - 0.1, RIGHT, (640, 930), 6, ox, oy, (-3, 3, -0.1))
    quote(c, t, [[('LUFTSCHLACHT', ws('Luftschlacht')), ('UM', ws('um', 17.5)), ('ENGLAND', ws('England'))]], 1270, ox, oy, 60)
    quote(c, t, [[('EINE', ws('eine', 20)), ('STUNDE', ws('Stunde'))], [('IM', ws('im', 21.5)), ('ÄRMELKANAL', ws('Ärmelkanal'))]], 1380, ox, oy, 82, col={0: YEL})
def s_1942(c, t, ox, oy):
    enter(c, PR('22', 1000, 51), t, T5 + 0.35, RIGHT, (540, 560), -3, ox, oy, (-3, 2, -0.08), main=True)
    enter(c, FP('b17cloud', t - T5 - 1.0, 700, 52), t, T5 + 1.0, LEFT, (400, 900), 5, ox, oy, (3, -2, 0.1))
    title(c, t, '1942', ['B-17 BEI TAG', 'ÜBER FRANKREICH'], 1400, ws('1942', 24), [ws('B-17', 26), ws('Ziele')], ox, oy, True, 200, 70, cps=16)
def s_nose(c, t, ox, oy):
    enter(c, FP('contr', t - T6 + VIS, 1000, 61), t, T6 + 0.35, TOP, (540, 560), 2, ox, oy, (3, 2, 0.08), main=True)
    enter(c, PR('04', 820, 62, crop=(300, 0, 2976, 1428)), t, ws('Nur') - 0.2, RIGHT, (580, 960), -5, ox, oy, (-3, 2, -0.1))
    quote(c, t, [[('DICHTE', ws('dichten')), ('FORMATIONEN', ws('Formationen'))]], 1270, ox, oy, 60)
    quote(c, t, [[('NUR', ws('Nur')), ('DIE', ws('die', 35)), ('NASE', ws('Nase'))], [('SCHWACH', ws('schwach')), ('BEWAFFNET', ws('bewaffnet'))]], 1380, ox, oy, 70, col={0: YEL})
def s_nazaire(c, t, ox, oy):
    enter(c, PR('23', 1000, 71), t, T7 + 0.35, LEFT, (540, 540), -2, ox, oy, (-3, 2, -0.08), main=True)
    enter(c, FP('hit', t - ws('frontal') + 0.2, 700, 72), t, ws('frontal') - 0.2, TOP, (400, 860), 5, ox, oy, (3, 2, 0.1))
    enter(c, PR('26', 560, 73), t, ws('meldete') - 0.1, RIGHT, (790, 920), -6, ox, oy, (-3, -2, -0.1))
    title(c, t, '1942', ['23. NOVEMBER', 'ST. NAZAIRE'], 1380, ws('1942', 38), [ws('23.'), ws('St.')], ox, oy, True, 170, 70, ['ZWEI B-17 UND EINE B-24 GEMELDET'], ws('meldete'), cps=16)
def s_eder(c, t, ox, oy):
    enter(c, PR('14', 660, 81, crop=(0, 150, 1824, 2314), cap='Georg-Peter Eder'), t, T8 + 0.35, LEFT, (360, 640), -3, ox, oy, (2, 3, 0.08), main=True)
    enter(c, FP('front', t - T8 - 0.9, 680, 82), t, T8 + 0.9, RIGHT, (740, 900), 4, ox, oy, (-2, 3, -0.1))
    for i, (s_, w_) in enumerate((('VON VORNE ANFLIEGEN', 'von'), ('KURZ FEUERN', 'kurz'), ('STEIL WEGZIEHEN', 'steil'))):
        quote(c, t, [[(s_, ws(w_, 50))]], 1280 + i * 92, ox, oy, 64, col={0: YEL if i == 0 else CREAM})
def s_turret(c, t, ox, oy):
    enter(c, FP('close', t - T9 + VIS, 1000, 91), t, T9 + 0.35, TOP, (540, 540), -2, ox, oy, (-3, 2, -0.08), main=True)
    enter(c, PR('03', 860, 92, crop=(1900, 500, 3207, 1500)), t, ws('Amerikaner') - 0.1, RIGHT, (540, 900), -3, ox, oy, (-1, 1, -0.04))
    quote(c, t, [[('WEITGEHEND', ws('weitgehend')), ('STANDARD', ws('Standardverfahren'))]], 1320, ox, oy, 62, col={0: YEL})
    label(c, t, ws('Waffenturm') - 0.1, 'zusätzlicher Waffenturm', 400, 1480, 735, 1010, ox, oy, 62)
def s_kommo(c, t, ox, oy):
    enter(c, PR('10', 1000, 101), t, T10 + 0.35, TOP, (540, 640), 2, ox, oy, (3, 2, 0.08), main=True)
    title(c, t, '1943', ['KOMMODORE', 'DES JG 2'], 1420, ws('1943', 63), ws('Kommodore'), ox, oy, True, 200, 74, cps=18)
def s_19(c, t, ox, oy):
    enter(c, FP('gun2', t - T11 + VIS, 1000, 111), t, T11 + 0.35, LEFT, (540, 560), 2, ox, oy, (-3, 2, -0.08), main=True)
    enter(c, PR('17', 480, 112), t, T11 + 1.2, RIGHT, (800, 860), -5, ox, oy, (3, -2, 0.1))
    quote(c, t, [[('DREI', ws('drei', 69)), ('B-17', ws('B-17', 70))]], 1250, ox, oy, 72, col={0: YEL})
    title(c, t, '19', ['MINUTEN'], 1370, ws('19', 71), ws('Minuten', 72), ox, oy, True, 200, 80, ['SEPTEMBER 1943'], T11 + 1.2, cps=20)
def s_100(c, t, ox, oy):
    enter(c, PR('08', 1000, 121, crop=(0, 250, 1792, 1600)), t, T12 + 0.35, RIGHT, (540, 640), -2, ox, oy, (-3, 2, -0.08), main=True)
    quote(c, t, [[('AN', ws('an', 77)), ('DER', ws('der', 77.6)), ('KANALFRONT', ws('Kanalfront'))]], 1250, ox, oy, 62)
    title(c, t, '100', ['LUFTSIEGE'], 1370, ws('100'), ws('Luftsiege', 79), ox, oy, True, 200, 80, ['FEBRUAR 1944'], T12 + 1.4, cps=26)
def s_death(c, t, ox, oy):
    enter(c, FP('p47', t - T13 + VIS, 1000, 131, sp=0.8), t, T13 + 0.35, TOP, (540, 560), 2, ox, oy, (3, 2, 0.08), main=True)
    enter(c, FP('p47b', t - ws('Begleitjäger') + 0.1, 700, 132), t, ws('Begleitjäger') - 0.1, LEFT, (400, 920), -5, ox, oy, (3, -2, 0.1))
    title(c, t, '1944', ['2. MÄRZ', 'BEI SEDAN'], 1420, ws('1944', 80), ws('März'), ox, oy, True, 170, 70, ['ABSTURZ BEI MONTMÉDY'], ws('stürzte'))
def s_end(c, t, ox, oy):
    enter(c, PR('07', 680, 141, cap='Saint-Désir-de-Lisieux'), t, T14 + 0.35, TOP, (540, 700), -2, ox, oy, (-2, 3, -0.08), main=True)
    quote(c, t, [[('26', ws('26')), ('JAHRE', ws('Jahre', 93))]], 1380, ox, oy, 110, col={0: YEL}, tout=ws('Ihm') - 0.15)
    title(c, t, '102', ['LUFTSIEGE,', 'ALLE IM WESTEN'], 1420, ws('102'), ws('Luftsiege', 95), ox, oy, True, 180, 66)
ZS, ZE = 6.6, 7.15
T2b = ZE + 0.15              # the hook pulls back: its film turns out to be a print on the table
ZH = 1.8                        # zoom at which the hook card (600 px wide) fills the screen
# Mayer's three portraits in the hook: (photo, crop, width, landing x, y, rotation, delay after "Egon")
HOOKP = [('19', None, 400, 250, 600, -6, 0.0), ('18', (0, 0, 1686, 2300), 400, 830, 620, 6, 0.3), ('16', (0, 100, 1696, 2476), 430, 540, 540, 1, 0.6)]
def hookcard_print(tt): return print_im(hookbg('headbg', tt).convert('RGB').resize((600, 1067), Image.LANCZOS), 600, False, None, 7)
def hook_prints(c, t, f=1.0, ox=0.0, oy=0.0, blur=True):
    """the three portraits drop in from the top one after another (reference title scene), arrive big and pull back slowly.
    f: scale of the whole layout (1 on screen in the hook, 1/ZH on the table card)"""
    for i, (n, crop, wd, x1, y1, r1, dl) in enumerate(HOOKP):
        t0 = H1 + dl
        if t < t0: continue
        def pos(tt):
            u = eout((tt - t0) / (1.0 * SLOW)); return x1 + 2 * (tt - t0), lerp(-800, y1, u) + 3 * (tt - t0), lerp(r1 + 9, r1, u)
        x, y, r = pos(t); x2, y2, _ = pos(t + 1 / FPS); d = t - t0; sc = 1.0 + 0.25 * (1 - eout(d / 2.8)) - 0.01 * d
        card(c, PR(n, wd, 30 + i, crop=crop), 540 + (x - 540) * f + ox, 960 + (y - 960) * f + oy, r, ((x2 - x) * 1.6 * f, (y2 - y) * 1.6 * f) if blur else (0, 0), sc=sc * f)
def s_hookcard(c, t, ox, oy):
    card(c, hookcard_print(t - H1 + 0.35), 540 + ox, 960 + oy, 0)
    hook_prints(c, t, 1 / ZH, ox, oy, False)
GX, GY = 1380, 2160
PATH = [(-1, 0), (0, 0), (1, 0), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)]
SCN = [(ZS, s_hookcard), (T2b, s_birth), (T3, s_jg2), (T4, s_bob), (T5, s_1942), (T6, s_nose), (T7, s_nazaire), (T8, s_eder), (T9, s_turret), (T10, s_kommo), (T11, s_19), (T12, s_100), (T13, s_death), (T14, s_end)]
ANC = [(p[0] * GX, p[1] * GY) for p in PATH]
PRE, POST = 0.2, 1.1   # the camera leaves only when the sentence is said; the move takes 1.3 s
def campos(t):
    """camera top-left on the table, and the move speed vector (px/frame) for blur"""
    k = max(i for i, (a, _) in enumerate(SCN) if a <= t) if t >= SCN[0][0] else 0
    nxt = k + 1 if k + 1 < len(SCN) and t >= SCN[k + 1][0] - PRE else None
    if nxt is not None: k, prev = nxt, k
    else: prev = k - 1 if k > 0 and t < SCN[k][0] + POST else None
    if prev is None: return ANC[k], (0.0, 0.0), k, None
    b = SCN[k][0]; u = clamp((t - (b - PRE)) / (PRE + POST))
    return (ANC[k] if t >= b + 0.12 else ANC[prev]), (0.0, 0.0), k, (prev, u)
@functools.lru_cache(None)
def sweeper():
    P_ = print_im(Image.open(E + 'pile/v02_162.jpg').convert('RGB'), 1000, True, None, 40).rotate(-7, expand=True, resample=Image.BICUBIC)
    return P_.resize((int(P_.width * 2.0), int(P_.height * 2.0)), Image.BICUBIC).filter(ImageFilter.GaussianBlur(24))
def dblur(img, vx, vy):
    L = math.hypot(vx, vy) * 0.9
    if L < 2: return img
    a = np.asarray(img.convert('RGB'), np.float32); n = 9; pd = int(L / 2) + 2; ap = np.pad(a, ((pd, pd), (pd, pd), (0, 0)), mode='edge'); acc = np.zeros_like(a)
    for k in range(n):
        f = (k - (n - 1) / 2) / (n - 1); dx, dy = int(round(vx / max(1e-6, math.hypot(vx, vy)) * L * f)), int(round(vy / max(1e-6, math.hypot(vx, vy)) * L * f))
        acc += ap[pd + dy:pd + dy + H, pd + dx:pd + dx + W]
    return Image.fromarray((acc / n).astype(np.uint8)).convert('RGBA')
def zoom_at(t):
    k = max([i for i, (a, _) in enumerate(SCN) if a <= t] or [0]); a = SCN[k][0] + POST
    if k == 0: return lerp(ZH, 1.0, eio((t - ZS) / (ZE - ZS)))
    return 1.0 + 0.006 * max(0.0, t - a)
def table_frame(t):
    (cx, cy), (vx, vy), k, tr = campos(t)
    can = table_view(cx, cy).convert('RGBA'); SWOOP.clear()
    for j in range(max(0, k - 1), min(len(SCN), k + 2)):   # neighbouring groups lie on the same table
        if (cx, cy) != tuple(ANC[j]) and j != k: pass
        CUR[0] = SCN[j][0]; SCN[j][1](can, t, ANC[j][0] - cx, ANC[j][1] - cy)
    for P_, x, y, r, sc, bl in SWOOP:   # the print near the lens, out of focus while it is big
        Q = P_.filter(ImageFilter.GaussianBlur(bl / max(1.0, sc))) if bl > 0.6 else P_
        card(can, Q, x, y, r, sc=sc)
    z = zoom_at(t) if tr is None else 1.0
    if k == 0 and tr is None: z = zoom_at(t)
    if tr is not None and t < SCN[k][0] + 0.12: z = zoom_at(SCN[k][0] - PRE)
    if z > 1.0005:
        bw, bh = W / z, H / z; can = can.resize((W, H), Image.BICUBIC, box=(CX - CX / z, 960 - 960 / z, CX - CX / z + bw, 960 - 960 / z + bh))
    return can

# ---------- hook ----------
H1 = ws('Egon')
def hook_frame(t):
    if t < H1 + 0.1:
        can = hookbg('form', t)
        if t > H1 - 0.35: can = Image.blend(can, hookbg('headbg', t - H1 + 0.35), eio((t - (H1 - 0.35)) / 0.45))
    else: can = hookbg('headbg', t - H1 + 0.35)
    quote(can, t, [[('WER', ws('Wer'))], [('AMERIKANISCHE', ws('amerikanische'))], [('BOMBER', ws('Bomber')), ('VON', ws('von'))], [('HINTEN', ws('hinten')), ('ANGRIFF,', ws('angriff'))],
                   [('FLOG', ws('flog')), ('DIREKT', ws('direkt'))], [('IN', ws('in')), ('IHR', ws('ihr'))], [('ABWEHRFEUER.', ws('Abwehrfeuer'))]], 900, size=84, tout=H1 - 0.3, lh=1.02)
    hook_prints(can, t)
    quote(can, t, [[('EGON', ws('Egon')), ('MAYER', ws('Mayer'))], [('GRIFF', ws('griff')), ('SIE', ws('sie', 5))], [('DESHALB', ws('deshalb'))], [('VON', ws('von', 5.5)), ('VORNE', ws('vorne')), ('AN.', ws('an', 6))]],
          1000, size=92, col={0: YEL}, lh=1.02, tout=ZS - 0.12)
    return can
def frame(t):
    if t < ZS: img = hook_frame(t)
    elif t < ZS + 0.15: img = Image.blend(hook_frame(t), table_frame(t), (t - ZS) / 0.15)
    else: img = table_frame(t)
    if t > TEND - 0.6: img = Image.blend(img, Image.new('RGBA', (W, H), (0, 0, 0, 255)), eio((t - (TEND - 0.6)) / 0.6))
    return finish(img, t)

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); P_ = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = frame(t).convert('RGBA'); d = ImageDraw.Draw(f)
            if os.environ.get('UI'):
                d.rectangle((0, 0, W, 290), outline=(0, 255, 255, 255), width=4); d.rectangle((930, 680, W, 1580), outline=(0, 255, 255, 255), width=4); d.rectangle((0, 1580, W, H), outline=(0, 255, 255, 255), width=4)
            d.text((10, 300), '%.2f' % t, fill=(255, 0, 255, 255)); P_.paste(f.convert('RGB').resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P_.save(E + sys.argv[2], quality=85); sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', E + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
        if n % 30 == 0: print('t', n / FPS, flush=True)
    p.stdin.close(); p.wait(); print('rc', p.returncode)
