# Style A, version 2: a closer copy of the reference a.mov, frame by frame.
# Reference mechanics:
#  1) quote over a full-bleed blue-toned photo, words fading in one by one, a small yellow line; out: the words fade away from the last one
#  2) title scene: prints slide in from the frame edges and never stop moving; the yellow title types letter by letter,
#     the number counts in digit by digit, a torn white strip wipes in from the left, then its small text appears
#  3) whip: the camera rushes over the table, the next prints come in from above with motion blur
#  4) sweep: a large out-of-focus print passes close to the camera from the left, behind it the next scene; the main print slides in from the left
# Under every scene a blue-toned pile of photos (the reference's dark pile), drifting slowly.
import sys, os, math, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import styleA as A
from styleA import W, H, FPS, CREAM, YEL, INK, mont, grunge, finish, print_, put, film, eout, eio, lerp, clamp, ws, wt, L9
B = A.B; CX = 480
DARK = np.array((14, 18, 32), np.float32); LIGHT = np.array((120, 134, 165), np.float32)

def tone(im, lo=DARK, hi=LIGHT, gamma=1.0):
    g = np.asarray(ImageOps.grayscale(im), np.float32) / 255
    if gamma != 1: g = g ** gamma
    return Image.fromarray(np.clip(lo + g[..., None] * (hi - lo), 0, 255).astype(np.uint8)).convert('RGBA')

# ---------- backgrounds ----------
@functools.lru_cache(None)
def hookbg():
    im = L9.src('l_8576'); s = H * 1.12 / im.height; im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.1); T_ = tone(im, np.array((10, 14, 28), np.float32), np.array((112, 128, 162), np.float32))
    yy = np.linspace(0, 1, T_.height)[:, None, None]; a = np.asarray(T_.convert('RGB'), np.float32) * (1.0 - 0.45 * np.clip((yy - 0.42) / 0.4, 0, 1))
    return Image.fromarray(a.astype(np.uint8)).convert('RGBA')
def hook_bg(t):
    im = hookbg(); z = 1.0 + 0.012 * t; cw, ch = W * 1.0 / z * (im.height / H) / 1.12 * 1.0, None
    cw = im.width / 1.0; ch = im.height
    bw, bh = W * im.height / H / z, im.height / z; x0 = (im.width - bw) / 2; y0 = (im.height - bh) * 0.35
    return im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + bw, y0 + bh))
PILE_SRC = ['l_16794965', 'l_16794966', 'l_16794967', 'l_16794972', 'l_2005', 'l_220963', 'l_ascension', 'l_b24', 'l_hart2', 'l_hss', 'l_img', 'l_img1', 'l_img2', 'l_sen', 'l_survivors', 'l_u156hit']
PILE_CLIP = ['b24fly', 'boom', 'crew', 'gl2', 'pax', 'ship', 'side', 'tow', 'uair', 'water', 'wdive', 'women']
@functools.lru_cache(None)
def pile(seed, bright):
    """a table covered in old prints, toned dark blue, a little soft (the reference's background pile)"""
    rng = np.random.default_rng(seed); PW, PH = 1500, 2700; can = Image.new('RGBA', (PW, PH), (20, 24, 40, 255))
    srcs = [('i', n) for n in PILE_SRC] + [('c', n) for n in PILE_CLIP]
    for k in range(70):
        kind, n = srcs[rng.integers(len(srcs))]
        im = L9.src(n) if kind == 'i' else A._fr(n, len(os.listdir(A.CLIPS + n)) // 2)
        P_ = A._print_im(im, int(rng.uniform(380, 640)), seed=int(rng.integers(50)))
        P_ = P_.rotate(rng.uniform(-28, 28), expand=True, resample=Image.BICUBIC)
        x, y = int(rng.uniform(-200, PW - 200)), int(rng.uniform(-200, PH - 200))
        sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.6)))
        can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (x + 8, y + 16)); can.alpha_composite(P_, (x, y))
    hi = LIGHT * bright
    T_ = tone(can, DARK, hi, 1.15).filter(ImageFilter.GaussianBlur(2.2))
    rng2 = np.random.default_rng(3); yy, xx = np.mgrid[0:PH, 0:PW]   # soft vignette spots like the reference's uneven light
    return T_
def pile_bg(t, seed, bright, ox, oy, vx=-10, vy=-14, z=1.0):
    """window onto the pile, drifting slowly"""
    P_ = pile(seed, bright); s = 1.0 / (1.0 + 0.010 * t) / z; bw, bh = 1150 * s, 2044 * s
    x0 = min(max(ox + vx * t, 0), P_.width - bw); y0 = min(max(oy + vy * t, 0), P_.height - bh)
    im = P_.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + bw, y0 + bh))
    yy, xx = np.mgrid[0:H, 0:W]; return vig(im)
@functools.lru_cache(None)
def _vig():
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.48) / (H * 0.62)) ** 2)
    return (1.0 - 0.55 * np.clip(r, 0, 1.4) ** 2)[..., None].astype(np.float32)
def vig(im):
    a = np.asarray(im.convert('RGB'), np.float32) * _vig(); return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')

# ---------- prints in motion ----------
def card(can, P_, cx, cy, rot, sc=1.0, mb=(0, 0), alpha=1.0):
    if sc != 1: P_ = P_.resize((max(1, int(P_.width * sc)), max(1, int(P_.height * sc))), Image.BICUBIC)
    P_ = P_.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 1: P_ = P_.copy(); P_.putalpha(P_.getchannel('A').point(lambda v: int(v * alpha)))
    x, y = int(cx - P_.width / 2), int(cy - P_.height / 2)
    if x > W or y > H or x + P_.width < 0 or y + P_.height < 0: return
    sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.6 * alpha)))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (x + 12, y + 26))
    L = abs(mb[0]) + abs(mb[1])
    if L > 3:   # smear along the motion, on a local canvas
        mx, my = int(abs(mb[0])) + 2, int(abs(mb[1])) + 2; loc = np.zeros((P_.height + 2 * my, P_.width + 2 * mx, 4), np.float32); a = np.asarray(P_, np.float32); n = 9
        for k in range(n):
            f = (k - (n - 1) / 2) / (n - 1); dx, dy = int(mb[0] * f), int(mb[1] * f); loc[my + dy:my + dy + P_.height, mx + dx:mx + dx + P_.width] += a
        loc /= n; rgb = loc[..., :3] / np.maximum(loc[..., 3:4], 1e-3) * 255; out = np.dstack([np.clip(rgb, 0, 255), loc[..., 3:4]]).astype(np.uint8)
        can.alpha_composite(Image.fromarray(out, 'RGBA'), (x - mx, y - my)); return
    can.alpha_composite(P_, (x, y))
def deal(can, P_, t, t0, frm, to, r0, r1, dur=0.65, drift=(0, 0, 0), sc=1.0):
    """a print slides in from off-frame and keeps drifting afterwards (the reference never lets a print stand still)"""
    if t < t0: return
    def pos(tt):
        u = eout((tt - t0) / dur); d = tt - t0
        return lerp(frm[0], to[0], u) + drift[0] * d, lerp(frm[1], to[1], u) + drift[1] * d, lerp(r0, r1, u) + drift[2] * d
    x, y, r = pos(t); x2, y2, _ = pos(t + 1 / FPS)
    card(can, P_, x, y, r, sc, ((x2 - x) * 2.2, (y2 - y) * 2.2))
def fprint(k, tt, wd, seed, cap=None, stop=None):
    if stop is not None: tt = min(tt, stop)
    return print_(None, wd, src=film(k, max(0, tt)), seed=seed, cap=cap)
P = lambda name, wd, seed, crop=None, cap=None: print_(name, wd, crop=crop, seed=seed, cap=cap)

# ---------- type ----------
def gtext_a(s, font, col, alphas, track=-2):
    """one line of extra-bold type, each letter with its own opacity"""
    xs = []; x = 0
    for ch in s: xs.append(x); x += font.getlength(ch) + track
    asc, desc = font.getmetrics(); L = Image.new('RGBA', (int(x) + 20, asc + desc + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for ch, xx, a in zip(s, xs, alphas):
        if a > 0: d.text((10 + xx, 10), ch, font=font, fill=col + (int(255 * a),))
    gm = grunge(len(s)).crop((0, 0, L.width, L.height)); L.putalpha(ImageChops.multiply(L.getchannel('A'), gm.point(lambda v: min(255, int(v * 1.08)))))
    return L
def typed(s, t, t0, cps=16, fade=0.12, tout=None):
    al = [clamp((t - t0 - i / cps) / fade) for i in range(len(s))]
    if tout is not None: al = [a * clamp(1 - (t - tout - (len(s) - 1 - i) * 0.02) / 0.15) for i, a in enumerate(al)]
    return al
def strip(can, t, t0, lines, cx, cy):
    """torn white paper strip wiping in from the left, then its small dark caps fade in"""
    if t < t0: return
    k = eout((t - t0) / 0.4); f = mont(32, 800)
    w_ = int(max(f.getlength(s) for s in lines) + 64); h_ = 24 + 42 * len(lines)
    P_ = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); rng = np.random.default_rng(len(lines[0]))
    top = [(x, rng.uniform(0, 7)) for x in range(0, w_ + 1, 10)]; bot = [(x, h_ - rng.uniform(0, 7)) for x in range(w_, -1, -10)]
    d = ImageDraw.Draw(P_); d.polygon(top + bot, fill=(232, 230, 224, 255))
    ka = clamp((t - t0 - 0.35) / 0.25)
    if ka > 0:
        for i, s_ in enumerate(lines): d.text((32, 14 + i * 42), s_, font=f, fill=INK + (int(255 * ka),))
    gm = grunge(9).crop((0, 0, w_, h_)); P_.putalpha(ImageChops.multiply(P_.getchannel('A'), gm))
    m = np.clip((k * (w_ + 60) - np.arange(w_)) / 60, 0, 1); P_.putalpha(Image.fromarray((np.asarray(P_.getchannel('A'), np.float32) * m[None, :]).astype(np.uint8)))
    put(can, P_, cx, cy)
def title(can, t, big, small, cy, t_big, t_small, big_first=True, size=220, ssize=88, strp=None, t_strip=None, maxw=790, cps=16):
    """the reference title: big white number counting in digit by digit + two yellow lines typing on + torn strip"""
    while True:
        fb, fs = mont(size, 900), mont(ssize, 900)
        wb = sum(fb.getlength(c) - 6 for c in big) + 20; wsm = max(sum(fs.getlength(c) - 3 for c in s) + 20 for s in small); gap = 20
        if wb + gap + wsm <= maxw or size < 60: break
        size = int(size * 0.94); ssize = int(ssize * 0.94)
    tot = wb + gap + wsm; x0 = CX - tot / 2
    xb, xs = (x0, x0 + wb + gap) if big_first else (x0 + wsm + gap, x0)
    if t >= t_big: put(can, gtext_a(big, fb, CREAM, typed(big, t, t_big, cps=8, fade=0.16), -6), xb, cy, 'l')
    if t >= t_small:
        n0 = 0
        for i, s in enumerate(small):
            L = gtext_a(s, fs, YEL, typed(s, t, t_small + n0 / cps, cps), -3); n0 += len(s)
            yy = cy - (len(small) - 1) * ssize * 0.46 + i * ssize * 0.92
            put(can, L, xs if big_first else xs + wsm - L.width, yy, 'l')
    if strp: strip(can, t, t_strip, strp, CX, cy + max(size * 0.5, ssize * 0.92 * len(small) / 2) + 34 + (24 + 42 * len(strp)) / 2)
def quote(can, t, lines, cy, size=70, sub=None, t_sub=None, tout=None, lh=1.05, maxw=800):
    """white caps, words fading in with the voice (no movement, like the reference); out: words vanish from the last one"""
    f = mont(size, 900)
    while size > 30 and max(sum(f.getlength(w_) for w_, _ in l) + f.getlength(' ') * 0.8 * (len(l) - 1) for l in lines) > maxw: size -= 2; f = mont(size, 900)
    allw = [w_ for l in lines for w_ in l]; N = len(allw); idx = 0
    for li, l in enumerate(lines):
        Ls = []
        for w_, t0 in l:
            a = clamp((t - t0) / 0.28)
            if tout is not None: a *= clamp(1 - (t - tout - (N - 1 - idx) * 0.035) / 0.18)
            Ls.append((gtext_a(w_, f, CREAM, [a] * len(w_), -2), a)); idx += 1
        sp = f.getlength(' ') * 0.8; tot = sum(L.width for L, _ in Ls) + sp * (len(Ls) - 1); x = CX - tot / 2; y = cy + li * size * lh
        for L, a in Ls:
            if a > 0: put(can, L, x, y, 'l', 1.0)
            x += L.width + sp
    if sub and t >= t_sub:
        a = clamp((t - t_sub) / 0.3)
        if tout is not None: a *= clamp(1 - (t - tout) / 0.2)
        fs = mont(34, 800); put(can, gtext_a(sub, fs, YEL, [a] * len(sub), 1), CX, cy + len(lines) * size * lh + 10, 'm')
def cam(can, t, a, zr=0.011, rr=0.10, cx=CX, cy=960):
    """the slow camera push over the table"""
    d = max(0.0, t - a); z = 1.035 + zr * d; r = rr * d
    im = can.rotate(r, resample=Image.BICUBIC, center=(cx, cy)) if abs(r) > 0.01 else can
    bw, bh = W / z, H / z; x0, y0 = cx - cx / z, cy - cy / z
    return im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + bw, y0 + bh))

# ---------- scenes ----------
T1 = ws('Im'); T2 = ws('Am', 10.9); T3 = ws('das', 15.2); T4 = ws('An', 17.9); T5 = ws('britische', 20.7); T6 = ws('und', 25.1); TEND = wt('Als') - 0.08
def s_hook(t, a, b):
    can = hook_bg(t).copy()
    L = [[('ER', ws('Er')), ('VERSENKTE', ws('versenkte'))], [('EIN', ws('ein', 0.5)), ('SCHIFF,', ws('Schiff'))], [('RETTETE', ws('rettete')), ('DANACH', ws('danach'))],
         [('HUNDERTE', ws('Hunderte'))], [('SCHIFFBRÜCHIGE', ws('Schiffbrüchige', 2.5))], [('UND', ws('und', 3.3)), ('WURDE', ws('wurde', 3.6)), ('DAFÜR', ws('dafür'))], [('BOMBARDIERT.', ws('bombardiert'))]]
    quote(can, t, L, 1010, 74, 'KOMMANDANT WERNER HARTENSTEIN, U 156', ws('bombardiert') + 0.3, tout=4.98, lh=1.0)
    return can
def s_1942(t, a, b):
    can = pile_bg(t, 1, 0.75, 120, 300)
    deal(can, P('l_sen', 640, 21), t, 5.55, (-700, 480), (230, 540), 16, 10, drift=(-4, 3, 0.25))
    deal(can, P('l_2005', 600, 22), t, 5.8, (W + 700, 900), (850, 820), -18, -11, drift=(5, 2, -0.3))
    deal(can, fprint('wdive', t - 5.05, 780, 23), t, 5.05, (520, -800), (520, 640), -14, -5, 0.8, drift=(2, 6, 0.15))
    title(can, t, '1942', ['U 156 VOR', 'WESTAFRIKA'], 1250, ws('1942'), ws('U', 7.5), True, 220, 86, ['SÜDATLANTIK, SEPTEMBER 1942'], ws('Westafrikas') - 0.1)
    return cam(can, t, a)
def s_attack(t, a, b):
    can = pile_bg(t, 2, 0.7, 200, 900, vx=8)
    deal(can, P('l_img1', 600, 31), t, a - 0.15, (900, -900), (830, 1260), 18, 9, 0.7, drift=(4, -3, 0.2))
    deal(can, fprint('torp', t - ws('torpedierte'), 360, 33), t, ws('torpedierte') - 0.1, (W + 500, 930), (880, 930), 14, 7, 0.55, drift=(-3, 4, 0.2))
    deal(can, P('l_hart2', 700, 32, crop=(300, 150, 1700, 1500), cap='Werner Hartenstein'), t, a - 0.05, (400, -1000), (400, 1130), -12, -4, 0.75, drift=(-3, -5, -0.15))
    title(can, t, '12.9.', ['DER', 'ANGRIFF'], 450, ws('12.'), a + 0.35, False, 210, 86, ['AM ABEND DES 12. SEPTEMBER 1942'], ws('September', 12) + 0.2)
    return cam(can, t, a, rr=-0.1)
def s_ship(t, a, b):
    can = pile_bg(t, 3, 1.15, 300, 500, vx=-12, vy=10)
    deal(can, fprint('ship', t - a, 860, 41, 'RMS Laconia'), t, a + 0.15, (-900, 720), (500, 740), 10, -4, 0.75, drift=(5, -3, -0.2))
    for s_, f, col, cy, t0, cps in (('BRITISCHES', mont(62, 900), YEL, 1180, ws('britische', 15.2), 16), ('TRUPPENTRANSPORTSCHIFF', mont(50, 900), YEL, 1250, ws('Truppentransportschiff'), 22),
                                    ('LACONIA', mont(146, 900), CREAM, 1390, ws('Laconia') - 0.35, 14)):
        if t >= t0: put(can, gtext_a(s_, f, col, typed(s_, t, t0, cps), -3 if col == YEL else -6), CX, cy, 'm')
    return cam(can, t, a, zr=0.014)
def s_paxA(t, a, b):
    can = pile_bg(t, 4, 0.72, 150, 200)
    deal(can, fprint('side', t - a - 0.3, 470, 52), t, a + 0.3, (W + 600, 980), (820, 960), -16, -8, 0.7, drift=(4, 3, -0.25))
    deal(can, fprint('pax', t - a, 860, 51), t, a - 0.12, (480, -900), (480, 660), 12, 4, 0.75, drift=(-3, 5, 0.15))
    title(can, t, '2.700', ['MENSCHEN', 'AN BORD'], 1330, ws('2.700'), ws('2.700') + 0.55, True, 220, 86, cps=20)
    return cam(can, t, a)
def s_paxB(t, a, b):
    can = pile_bg(t, 5, 1.1, 250, 800, vx=10, vy=-8)
    deal(can, P('l_survivors', 640, 61), t, a + 0.15, (-800, 520), (300, 560), 14, 8, 0.7, drift=(-4, 3, 0.25))
    deal(can, P('l_220963', 560, 62), t, ws('polnische') - 0.1, (W + 700, 820), (790, 800), -16, -9, 0.6, drift=(4, -3, -0.2))
    deal(can, fprint('women', t - ws('Zivilisten'), 640, 63), t, ws('Zivilisten') - 0.1, (W + 700, 450), (640, 640), -14, -6, 0.65, drift=(3, 4, -0.15))
    L = [[('BRITISCHE', ws('britische', 20.7)), ('SOLDATEN,', ws('Soldaten'))], [('ZIVILISTEN', ws('Zivilisten')), ('MIT', ws('mit', 22.5))], [('FRAUEN', ws('Frauen')), ('UND', ws('und', 23.1)), ('KINDERN,', ws('Kindern'))],
         [('POLNISCHE', ws('polnische'))], [('WACHSOLDATEN', ws('Wachsoldaten'))]]
    quote(can, t, L, 1150, 70, 'AN BORD DER LACONIA', ws('Wachsoldaten') + 0.4, lh=1.02)
    return cam(can, t, a, rr=-0.08)
def s_paxC(t, a, b):
    can = pile_bg(t, 6, 0.72, 100, 1200, vx=12)
    deal(can, fprint('water', t - a - 0.45, 520, 72), t, a + 0.45, (-700, 1000), (300, 960), 16, 9, 0.65, drift=(-4, 3, 0.2))
    deal(can, P('l_hss', 820, 71, crop=(150, 0, 2750, 1536)), t, a - 0.12, (520, -900), (540, 640), -10, -4, 0.75, drift=(3, 5, -0.15))
    title(can, t, '1.800', ['ITALIENISCHE', 'KRIEGSGEFANGENE'], 1360, ws('1.800'), ws('italienische') - 0.1, True, 200, 74, cps=30)
    return cam(can, t, a)
SC = [(0.0, s_hook), (T1, s_1942), (T2, s_attack), (T3, s_ship), (T4, s_paxA), (T5, s_paxB), (T6, s_paxC)]
TR = {T1: 'fade', T2: 'whip', T3: 'sweep', T4: 'whip', T5: 'sweep', T6: 'whip'}

# ---------- transitions ----------
def vblur(img, L):
    """motion blur along y"""
    if L < 2: return img
    a = np.asarray(img.convert('RGB'), np.float32); acc = np.zeros_like(a); n = 9; pd = int(L / 2) + 2; ap = np.pad(a, ((pd, pd), (0, 0), (0, 0)), mode='edge')
    for k in range(n):
        s = int((k - (n - 1) / 2) / (n - 1) * L); acc += ap[pd + s:pd + s + H]
    return Image.fromarray((acc / n).astype(np.uint8)).convert('RGBA')
@functools.lru_cache(None)
def sweeper():
    P_ = A._print_im(L9.src('l_16794966'), 1100, seed=40); P_ = P_.rotate(-8, expand=True, resample=Image.BICUBIC)
    return P_.resize((int(P_.width * 1.9), int(P_.height * 1.9)), Image.BICUBIC).filter(ImageFilter.GaussianBlur(22))
WH0, WH1 = 0.22, 0.45; SW0, SW1 = 0.25, 0.5
def scene(i, t): a, fn = SC[i]; b = SC[i + 1][0] if i + 1 < len(SC) else TEND; return fn(t, a, b)
def frame(t):
    i = max(j for j, (a, _) in enumerate(SC) if a <= t)
    img = None
    for j in (i, i + 1):   # are we inside a transition into scene j?
        if j <= 0 or j >= len(SC): continue
        b = SC[j][0]; kind = TR[b]
        if kind == 'whip' and b - WH0 <= t < b + WH1:
            u = eio((t - (b - WH0)) / (WH0 + WH1)); u2 = eio((t + 1 / FPS - (b - WH0)) / (WH0 + WH1)); off = int(u * H * 1.02)
            Aimg, Bimg = scene(j - 1, t), scene(j, t); can = Image.new('RGBA', (W, H)); can.alpha_composite(Aimg, (0, off)) if off < H else None
            can.alpha_composite(Bimg, (0, off - int(H * 1.02))); img = vblur(can, (u2 - u) * H * 1.02 * 0.6)
        elif kind == 'sweep' and b - SW0 <= t < b + SW1:
            u = (t - (b - SW0)) / (SW0 + SW1); base = scene(j - 1, t) if u < 0.5 else scene(j, t)
            bl = 12 * (1 - abs(u - 0.5) * 2); base = base.filter(ImageFilter.GaussianBlur(bl)) if bl > 0.5 else base
            sw = sweeper(); x = lerp(-sw.width - 100, W + 100, eio(u)); base.alpha_composite(sw, (int(x), int(H / 2 - sw.height / 2 + 120)))
            img = base
        elif kind == 'fade' and b - 0.05 <= t < b + 0.45:
            k = eio((t - (b - 0.05)) / 0.5); img = Image.blend(scene(j - 1, t), scene(j, t), k)
        if img is not None: break
    if img is None: img = scene(i, t)
    if t < 0.3: img = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), img, eio(t / 0.3))
    if t > TEND - 0.35: img = Image.blend(img, Image.new('RGBA', (W, H), (0, 0, 0, 255)), eio((t - (TEND - 0.35)) / 0.35))
    return finish(img, t)

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); P_ = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = frame(t).convert('RGBA'); d = ImageDraw.Draw(f)
            if os.environ.get('UI'):
                d.rectangle((0, 0, W, 290), outline=(0, 255, 255, 255), width=4); d.rectangle((930, 680, W, 1580), outline=(0, 255, 255, 255), width=4); d.rectangle((0, 1580, W, H), outline=(0, 255, 255, 255), width=4)
            d.text((10, 300), '%.2f' % t, fill=(255, 0, 255, 255)); P_.paste(f.convert('RGB').resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P_.save(B + sys.argv[2], quality=85); sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
        if n % 30 == 0: print('t', n / FPS, flush=True)
    p.stdin.close(); p.wait(); print('rc', p.returncode)
