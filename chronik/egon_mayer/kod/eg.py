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
BLUR = {'16': [(830, 2240, 34)], '18': [(567, 170, 46), (467, 1595, 50), (686, 1168, 30), (1267, 1667, 34), (528, 1968, 72)],
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
    n = nfr(k); i = int(max(0.0, tt + off) * 25); p = 2 * (n - 1); i = i % p; i = i if i < n else p - i   # ping-pong, never freezes
    return _fr(k, i + 1)
@functools.lru_cache(maxsize=96)
def PR(n, wd, seed, crop=None, cap=None):
    im = src(n)
    return A._print_im(im.crop(crop) if crop else im, wd, None, True, cap, seed)
def FP(k, tt, wd, seed, cap=None, off=0.0): return A._print_im(film(k, tt, off), wd, None, True, cap, seed)

# ---------- smooth (sub-pixel) print placement ----------
def card(can, P_, cx, cy, rot, mb=(0, 0), alpha=1.0):
    P_ = P_.rotate(rot, expand=True, resample=Image.BICUBIC)
    x, y = cx - P_.width / 2, cy - P_.height / 2; ix, iy = math.floor(x), math.floor(y); fx, fy = x - ix, y - iy
    if ix > W + 40 or iy > H + 40 or ix + P_.width < -40 or iy + P_.height < -40: return
    P_ = P_.transform((P_.width + 1, P_.height + 1), Image.AFFINE, (1, 0, -fx, 0, 1, -fy), resample=Image.BICUBIC)   # fractional shift
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
CUR = [0.0]   # start time of the scene being drawn (drift of prints that already lie there)
def deal(can, P_, t, t0, frm, to, r0, r1, ox, oy, dur=1.0, drift=(0, 0, 0)):
    """print at local position `to` (+ table offset ox, oy). t0=None: already lying there. Otherwise slides in from `frm`. Always drifting."""
    def pos(tt):
        if t0 is None: u = 1.0; d = tt - CUR[0]
        else: u = eout((tt - t0) / (dur * SLOW)); d = tt - t0
        return lerp(frm[0], to[0], u) + drift[0] * d + ox, lerp(frm[1], to[1], u) + drift[1] * d + oy, lerp(r0, r1, u) + drift[2] * d
    if t0 is not None and t < t0: return
    x, y, r = pos(t); x2, y2, _ = pos(t + 1 / FPS)
    card(can, P_, x, y, r, ((x2 - x) * 1.6, (y2 - y) * 1.6))

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
        if t >= t_small:
            n0 = 0
            for i, s in enumerate(small):
                L = gtext_a(s, fs, YEL, typed(s, t, t_small + n0 / cps, cps), -3); n0 += len(s)
                put(can, L, CX + ox, cy - ssize * 0.5 * len(small) + size * 0.62 + ssize * 0.55 + i * ssize * 0.95, 'm')
        if strp: strip(can, t, t_strip, strp, CX + ox, cy - ssize * 0.5 * len(small) + size * 0.62 + ssize * 0.95 * len(small) + 50)
        return
    tot = wb + gap + wsm; x0 = CX - tot / 2 + ox; cy += oy
    xb, xs = (x0, x0 + wb + gap) if big_first else (x0 + wsm + gap, x0)
    if t >= t_big: put(can, gtext_a(big, fb, CREAM, typed(big, t, t_big, 6, 0.25), -6), xb, cy, 'l')
    if small and t >= t_small:
        n0 = 0
        for i, s in enumerate(small):
            L = gtext_a(s, fs, YEL, typed(s, t, t_small + n0 / cps, cps), -3); n0 += len(s)
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
        P_ = A._print_im(im, int(rng.uniform(560, 820)), seed=int(rng.integers(50))).rotate(rng.uniform(-30, 30), expand=True, resample=Image.BICUBIC)
        x, y = int(rng.uniform(0, TW)), int(rng.uniform(0, TH))
        sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.6))); sh = sh.filter(ImageFilter.GaussianBlur(10))
        for dx in (-TW, 0, TW):
            for dy in (-TH, 0, TH):   # wrap so the tile is seamless
                paste(can, sh, x + dx + 8, y + dy + 16); paste(can, P_, x + dx, y + dy)
    T_ = tone(can, DARK, LIGHT * 0.62, 1.25).filter(ImageFilter.GaussianBlur(3.2))
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
def s_birth(c, t, ox, oy):
    deal(c, PR('19', 520, 21, cap='Egon Mayer'), t, None, (0, 0), (520, 620), 0, -5, ox, oy, drift=(3, 4, 0.12))
    deal(c, PR('09', 560, 22), t, T2 + 1.2, (W + 700, 380), (860, 460), -20, -11, ox, oy, drift=(-4, 3, -0.15))
    title(c, t, '1917', ['GEBOREN IN', 'KONSTANZ'], 1330, ws('1917'), ws('Konstanz') - 0.1, ox, oy, True, 170, 74, ['1937: EINTRITT IN DIE LUFTWAFFE'], ws('1937'))
def s_jg2(c, t, ox, oy):
    deal(c, PR('24', 820, 31), t, None, (0, 0), (540, 640), 0, 4, ox, oy, drift=(-4, 3, -0.1))
    deal(c, PR('11', 520, 32), t, T3 + 1.0, (-700, 900), (260, 930), 20, 9, ox, oy, drift=(3, -3, 0.15))
    title(c, t, '1939', ['JAGDGESCHWADER 2', '„RICHTHOFEN“'], 1340, ws('1939'), ws('Jagdgeschwader'), ox, oy, True, 200, 62)
def s_bob(c, t, ox, oy):
    deal(c, FP('spit', t - T4 + 5, 820, 41, off=0), t, None, (0, 0), (540, 720), 0, -4, ox, oy, drift=(4, 3, 0.12))
    deal(c, PR('15', 640, 42), t, ws('Einmal') - 0.1, (W + 800, 1000), (700, 1020), -22, -8, ox, oy, drift=(-3, 4, -0.15))
    quote(c, t, [[('LUFTSCHLACHT', ws('Luftschlacht')), ('UM', ws('um', 17.5)), ('ENGLAND', ws('England'))]], 330, ox, oy, 64)
    quote(c, t, [[('EINE', ws('eine', 20)), ('STUNDE', ws('Stunde'))], [('IM', ws('im', 21.5)), ('ÄRMELKANAL', ws('Ärmelkanal'))]], 1340, ox, oy, 84, col={0: YEL})
def s_1942(c, t, ox, oy):
    deal(c, PR('22', 780, 51), t, None, (0, 0), (520, 620), 0, 5, ox, oy, drift=(-3, 4, -0.12))
    deal(c, FP('b17cloud', t - T5 + 5, 600, 52), t, T5 + 1.0, (-700, 1000), (330, 980), 18, 8, ox, oy, drift=(3, -3, 0.15))
    title(c, t, '1942', ['B-17 BEI TAG', 'ÜBER FRANKREICH'], 1350, ws('1942', 24), ws('B-17', 26), ox, oy, True, 200, 70)
def s_nose(c, t, ox, oy):
    deal(c, FP('contr', t - T6 + 5, 760, 61), t, None, (0, 0), (540, 690), 0, -4, ox, oy, drift=(3, 3, 0.12))
    deal(c, PR('04', 760, 62, crop=(300, 0, 2976, 1428)), t, ws('Nur') - 0.2, (W + 800, 1060), (560, 1060), -20, -6, ox, oy, drift=(-3, 3, -0.12))
    quote(c, t, [[('DICHTE', ws('dichten')), ('FORMATIONEN', ws('Formationen'))]], 320, ox, oy, 62)
    quote(c, t, [[('NUR', ws('Nur')), ('DIE', ws('die', 35)), ('NASE', ws('Nase'))], [('SCHWACH', ws('schwach')), ('BEWAFFNET', ws('bewaffnet'))]], 1440, ox, oy, 70, col={0: YEL})
def s_nazaire(c, t, ox, oy):
    deal(c, PR('23', 720, 71), t, None, (0, 0), (540, 520), 0, 4, ox, oy, drift=(-3, 4, -0.1))
    deal(c, FP('hit', t - ws('frontal'), 640, 72), t, ws('frontal') - 0.2, (540, -800), (380, 800), -16, -7, ox, oy, drift=(3, 3, 0.15))
    deal(c, PR('26', 500, 73), t, ws('meldete') - 0.1, (W + 700, 900), (800, 900), 18, 10, ox, oy, drift=(-3, -2, -0.15))
    title(c, t, '23.11.', ['ST. NAZAIRE', '1942'], 1340, ws('23.'), ws('St.'), ox, oy, True, 160, 70, ['ZWEI B-17 UND EINE B-24 GEMELDET'], ws('meldete'))
def s_eder(c, t, ox, oy):
    deal(c, PR('14', 520, 81, crop=(0, 150, 1824, 2314), cap='Georg-Peter Eder'), t, None, (0, 0), (330, 640), 0, 6, ox, oy, drift=(2, 3, 0.1))
    deal(c, FP('front', t - T8 + 2, 560, 82), t, T8 + 0.9, (W + 600, 760), (780, 800), -16, -7, ox, oy, drift=(-2, 3, -0.12))
    for i, (s_, w_) in enumerate((('VON VORNE ANFLIEGEN', 'von'), ('KURZ FEUERN', 'kurz'), ('STEIL WEGZIEHEN', 'steil'))):
        quote(c, t, [[(s_, ws(w_, 50))]], 1250 + i * 96, ox, oy, 66, col={0: YEL if i == 0 else CREAM})
def s_turret(c, t, ox, oy):
    deal(c, FP('close', t - T9 + 5, 640, 91), t, None, (0, 0), (540, 700), 0, 4, ox, oy, drift=(-3, 3, -0.12))
    deal(c, PR('03', 760, 92, crop=(1900, 500, 3207, 1500)), t, ws('Amerikaner') - 0.1, (W + 900, 1130), (540, 1130), -14, -3, ox, oy, drift=(-1, 1, -0.04))
    quote(c, t, [[('WEITGEHEND', ws('weitgehend')), ('STANDARD', ws('Standardverfahren'))]], 330, ox, oy, 62, col={0: YEL})
    label(c, t, ws('Waffenturm') - 0.1, 'zusätzlicher Waffenturm', 400, 1530, 705, 1240, ox, oy, 62)
def s_kommo(c, t, ox, oy):
    deal(c, PR('18', 600, 101, crop=(0, 0, 1686, 2300)), t, None, (0, 0), (540, 680), 0, -4, ox, oy, drift=(3, 3, 0.1))
    title(c, t, '1943', ['KOMMODORE', 'DES JG 2'], 1400, ws('1943', 63), ws('Kommodore'), ox, oy, True, 200, 74)
def s_19(c, t, ox, oy):
    deal(c, FP('gun2', t - T11 + 5, 720, 111), t, None, (0, 0), (540, 600), 0, 5, ox, oy, drift=(-3, 4, -0.12))
    deal(c, PR('17', 400, 112), t, T11 + 1.0, (-700, 900), (250, 900), 16, 8, ox, oy, drift=(3, -3, 0.12))
    title(c, t, '19', ['MINUTEN,', 'DREI B-17'], 1380, ws('19'), ws('drei', 69), ox, oy, True, 230, 80, ['SEPTEMBER 1943'], ws('zugeschrieben', 72) + 0.2)
def s_100(c, t, ox, oy):
    deal(c, PR('16', 540, 121, crop=(0, 0, 1696, 2476)), t, None, (0, 0), (500, 640), 0, 5, ox, oy, drift=(-3, 3, -0.1))
    deal(c, PR('10', 480, 122), t, T12 + 1.0, (W + 700, 940), (800, 940), -16, -9, ox, oy, drift=(-3, -3, -0.15))
    title(c, t, '100', ['LUFTSIEGE AN', 'DER KANALFRONT'], 1400, ws('100'), ws('Luftsiege', 79), ox, oy, True, 170, 64, ['FEBRUAR 1944'], ws('Februar') + 0.3)
def s_death(c, t, ox, oy):
    deal(c, FP('p47', t - T13 + 5, 820, 131), t, None, (0, 0), (540, 600), 0, -4, ox, oy, drift=(3, 3, 0.12))
    deal(c, FP('p47b', t - ws('Begleitjäger'), 520, 132), t, ws('Begleitjäger') - 0.1, (-700, 900), (290, 930), 18, 8, ox, oy, drift=(3, -3, 0.15))
    title(c, t, '1944', ['2. MÄRZ', 'BEI SEDAN'], 1390, ws('1944', 80), ws('März'), ox, oy, True, 170, 70, ['ABSTURZ BEI MONTMÉDY'], ws('Montmédy') - 0.2)
def s_end(c, t, ox, oy):
    deal(c, PR('07', 560, 141, cap='Saint-Désir-de-Lisieux'), t, None, (0, 0), (540, 680), 0, 4, ox, oy, drift=(-2, 3, -0.1))
    quote(c, t, [[('26', ws('26')), ('JAHRE', ws('Jahre', 93))]], 1330, ox, oy, 110, col={0: YEL}, tout=ws('Ihm') - 0.15)
    title(c, t, '102', ['LUFTSIEGE,', 'ALLE IM WESTEN'], 1380, ws('102'), ws('Luftsiege', 95), ox, oy, True, 180, 66)
GX, GY = 1380, 2160
PATH = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)]
SCN = [(T2, s_birth), (T3, s_jg2), (T4, s_bob), (T5, s_1942), (T6, s_nose), (T7, s_nazaire), (T8, s_eder), (T9, s_turret), (T10, s_kommo), (T11, s_19), (T12, s_100), (T13, s_death), (T14, s_end)]
ANC = [(p[0] * GX, p[1] * GY) for p in PATH]
PRE, POST = 0.5, 0.8
def campos(t):
    """camera top-left on the table, and the move speed vector (px/frame) for blur"""
    k = max(i for i, (a, _) in enumerate(SCN) if a <= t) if t >= SCN[0][0] else 0
    nxt = k + 1 if k + 1 < len(SCN) and t >= SCN[k + 1][0] - PRE else None
    if nxt is not None: k, prev = nxt, k
    else: prev = k - 1 if k > 0 and t < SCN[k][0] + POST else None
    if prev is None: return ANC[k], (0.0, 0.0), k, None
    b = SCN[k][0]; f = lambda tt: eio((tt - (b - PRE)) / (PRE + POST))
    u, u2 = f(t), f(t + 1 / FPS); (ax, ay), (bx, by) = ANC[prev], ANC[k]
    return (lerp(ax, bx, u), lerp(ay, by, u)), ((bx - ax) * (u2 - u), (by - ay) * (u2 - u)), k, (prev, u)
@functools.lru_cache(None)
def sweeper():
    P_ = A._print_im(Image.open(E + 'pile/v02_162.jpg').convert('RGB'), 1000, seed=40).rotate(-7, expand=True, resample=Image.BICUBIC)
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
    return 1.0 + 0.006 * max(0.0, t - a)
def table_frame(t):
    (cx, cy), (vx, vy), k, tr = campos(t)
    can = table_view(cx, cy).convert('RGBA')
    for j in range(max(0, k - 1), min(len(SCN), k + 2)):   # neighbouring groups lie on the same table
        CUR[0] = SCN[j][0]; SCN[j][1](can, t, ANC[j][0] - cx, ANC[j][1] - cy)
    if tr is not None:
        prev, u = tr; can = dblur(can, vx, vy)
        dx, dy = ANC[k][0] - ANC[prev][0], ANC[k][1] - ANC[prev][1]; sw = sweeper(); s = clamp((u - 0.12) / 0.76)
        if 0 < s < 1:   # a print close to the lens passes the other way
            if abs(dx) > abs(dy): x = lerp(W + 60, -sw.width - 60, s) if dx > 0 else lerp(-sw.width - 60, W + 60, s); y = H / 2 - sw.height / 2 + 150
            else: y = lerp(H + 60, -sw.height - 60, s) if dy > 0 else lerp(-sw.height - 60, H + 60, s); x = W / 2 - sw.width / 2
            paste(can, sw, int(x), int(y))
        z = lerp(zoom_at(SCN[prev][0] + (SCN[k][0] - SCN[prev][0]) - PRE), 1.0, u)
    else: z = zoom_at(t)
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
    quote(can, t, [[('EGON', ws('Egon')), ('MAYER', ws('Mayer'))], [('GRIFF', ws('griff')), ('SIE', ws('sie', 5))], [('DESHALB', ws('deshalb'))], [('VON', ws('von', 5.5)), ('VORNE', ws('vorne')), ('AN.', ws('an', 6))]],
          1000, size=92, col={0: YEL}, lh=1.02)
    return can
def frame(t):
    if t < T2 - 0.1: img = hook_frame(t)
    elif t < T2 + 0.55: img = Image.blend(hook_frame(t), table_frame(max(t, T2)), eio((t - (T2 - 0.1)) / 0.65))
    else: img = table_frame(t)
    if t < 0.3: img = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), img, eio(t / 0.3))
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
