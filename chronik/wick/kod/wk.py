# Helmut Wick, CDM Short in style A (Schnaufer engine) (engine of prien/code/pr.py, Egon Mayer v6 way):
# hook = full-bleed blue-toned film of bombers in the night sky with the words typing on; at his name his portrait drops in;
# then one big table of prints, the camera travelling from group to group. Colourised photos (Boran's upscale, symbols blurred
# small), black-and-white photos in a warm archive tone, films where they exist (DW 744 Diamonds, night raid, RAF bombers, Lancasters).
import sys, os, json, math, subprocess, functools, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, E + '../egon/code')
import eg
from eg import W, H, FPS, CREAM, YEL, eout, eio, lerp, clamp, card, paste, print_im, quote, title, strip, label, tone, DARK, LIGHT, finish, dblur
WORDS = json.load(open(E + 'words.json'))
def ws(s, after=0.0):
    for w, a, b in WORDS:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a - 0.04
    raise KeyError(s)

# ---------- footage ----------
CL = E + 'clipL/'
@functools.lru_cache(None)
def nfr(k): return len(os.listdir(CL + k))
@functools.lru_cache(maxsize=64)
def _fr(k, i): return Image.open(CL + '%s/%05d.jpg' % (k, i)).convert('RGB')
def film(k, tt): return _fr(k, min(nfr(k), max(1, int(max(0.0, tt) * 25) + 1)))   # forward only
def warm(im):
    """black-and-white film in a slightly warm archive tone (the photos are in colour, the films stay old footage)"""
    g = np.asarray(ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=0.5), np.float32)[..., None] / 255
    return Image.fromarray(np.clip(g * np.array((246, 236, 218), np.float32) + (1 - g) * np.array((18, 16, 14), np.float32), 0, 255).astype(np.uint8))
def FP(k, tt, wd, seed, cap=None, sp=1.0): return print_im(warm(film(k, tt * sp)), wd, False, cap, seed)
@functools.lru_cache(maxsize=32)
def SP(n, wd, seed, cap=None): return print_im(Image.open(E + 'img/%s.jpg' % n).convert('RGB'), wd, False, cap, seed)   # colourised photo print (Boran's upscale; symbols blurred again after it)
@functools.lru_cache(maxsize=32)
def BW(n, wd, seed, cap=None): return print_im(warm(Image.open(E + 'img/%s.jpg' % n).convert('RGB')), wd, False, cap, seed)   # black-and-white photo, warm archive tone
# hook background: bombers over the night sky, cut to 9:16 (clip/hook, 30 fps), blue-toned like the Egon hook
HC = E + 'clip/hook/'
@functools.lru_cache(maxsize=16)
def _hk(i): return Image.open(HC + '%05d.jpg' % i).convert('RGB')
def hookbg(tt, dark=0.62):
    n = len(os.listdir(HC)); im = _hk(min(n, max(1, int(tt * 30) + 1))); g = np.asarray(ImageOps.grayscale(im).resize((W, H), Image.BICUBIC), np.float32) / 255
    g = np.clip((g - 0.5) * 1.15 + 0.5, 0, 1); a = DARK + g[..., None] * (LIGHT * 1.25 - DARK)
    yy = np.linspace(0, 1, H)[:, None, None]; a *= (1.0 - (1 - dark) * np.clip((yy - 0.35) / 0.35, 0, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')

# ---------- the table ----------
TW, TH = 2700, 3300
PILE = ['kampf', 'sea', 'takeoff', 'board', 'dog']
def pile_im(i):
    k = PILE[i % len(PILE)]; return _fr(k, max(1, int(nfr(k) * ((i * 0.37) % 0.8 + 0.1))))
@functools.lru_cache(None)
def table():
    cache = E + 'table.png'
    if os.path.exists(cache): return Image.open(cache).convert('RGB')
    rng = np.random.default_rng(5); can = Image.new('RGBA', (TW, TH), (20, 24, 40, 255))
    for k in range(90):
        P_ = print_im(pile_im(int(rng.integers(1000))), int(rng.uniform(560, 820)), True, None, seed=int(rng.integers(50))).rotate(rng.uniform(-30, 30), expand=True, resample=Image.BICUBIC)
        x, y = int(rng.uniform(0, TW)), int(rng.uniform(0, TH))
        sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.6))); sh = sh.filter(ImageFilter.GaussianBlur(10))
        for dx in (-TW, 0, TW):
            for dy in (-TH, 0, TH): paste(can, sh, x + dx + 8, y + dy + 16); paste(can, P_, x + dx, y + dy)
    T_ = tone(can, DARK, LIGHT * 0.5, 1.2).filter(ImageFilter.GaussianBlur(3.0))
    big = Image.new('RGB', (TW + 1400, TH + 2300))
    for dx in (0, TW):
        for dy in (0, TH): big.paste(T_, (dx, dy))
    big.save(cache); return big
BGN = 560
@functools.lru_cache(None)
def bg_list():
    rng = np.random.default_rng(11); xs = [a[0] for a in ANC]; ys = [a[1] for a in ANC]
    x0, x1, y0, y1 = min(xs) - 900, max(xs) + W + 900, min(ys) - 900, max(ys) + H + 900
    return [(int(rng.integers(48)), rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(-30, 30), rng.uniform(-7, 7), rng.uniform(-7, 7), rng.uniform(-0.3, 0.3)) for _ in range(BGN)]
@functools.lru_cache(maxsize=64)
def bg_img(i):
    P_ = print_im(pile_im(i * 7 + 3), 520 + (i * 37) % 260, True, None, i)
    T_ = tone(P_.convert('RGB'), DARK, LIGHT * 0.92, 1.1).filter(ImageFilter.GaussianBlur(1.3)).convert('RGBA'); T_.putalpha(P_.getchannel('A'))
    return T_
def bg_layer(can, t, cx, cy):
    for i, x, y, r, vx, vy, vr in bg_list():
        X, Y = x + vx * t - cx, y + vy * t - cy
        if X < -650 or X > W + 650 or Y < -650 or Y > H + 650: continue
        card(can, bg_img(i), X, Y, r + vr * t)
def table_view(cx, cy):
    T_ = table(); x0, y0 = cx % TW, cy % TH
    return T_.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + W, y0 + H))

# ---------- prints scattering in with the camera (eg.enter) ----------
CUR = [0.0]; CNT = [0]; CURJ = [0]
def enter(c, P_, t, to, r1, ox, oy, drift=(0, 0, 0), main=False):
    a = CUR[0]; i = CNT[0]; CNT[0] += 1; j = CURJ[0]
    if j > 0: dx, dy = ANC[j][0] - ANC[j - 1][0], ANC[j][1] - ANC[j - 1][1]
    else: dx, dy = 1.0, 0.0
    n = math.hypot(dx, dy) or 1.0; dx, dy = dx / n, dy / n
    t0 = a - PRE + 0.12 * i
    if t < t0: return
    jit = ((i * 97 + j * 31) % 7 - 3) * 70.0
    def pos(tt):
        u = eout(clamp((tt - t0) / 1.35)); d = tt - a
        fx, fy = to[0] + dx * 680 - dy * jit, to[1] + dy * 680 + dx * jit
        sc = 1.0 + 0.32 * (1 - u) + (0.10 if main else 0.07) * (1 - eout(clamp((tt - t0) / 3.4))) - 0.008 * max(0.0, d)
        return lerp(fx, to[0], u) + drift[0] * d + ox, lerp(fy, to[1], u) + drift[1] * d + oy, lerp(r1 + (16 if i % 2 else -16), r1, u) + drift[2] * d, sc
    x, y, r, sc = pos(t); x2, y2, _, _ = pos(t + 1 / FPS)
    card(c, P_, x, y, r, ((x2 - x) * 1.4, (y2 - y) * 1.4), sc=sc)
def later(c, P_, t, t0, to, r1, ox, oy, frm=(1, 0), drift=(2, 3, 0.06)):
    """a print that joins a group later in its scene (on a word): from the side, big and turning, then slowly pulling back"""
    if t < t0: return
    def pos(tt):
        u = eout(clamp((tt - t0) / 1.2)); d = tt - t0
        sc = 1.0 + 0.30 * (1 - u) + 0.08 * (1 - eout(clamp(d / 3.4))) - 0.008 * d
        return lerp(to[0] + frm[0] * 760, to[0], u) + drift[0] * d + ox, lerp(to[1] + frm[1] * 760, to[1], u) + drift[1] * d + oy, lerp(r1 + (16 if frm[0] + frm[1] > 0 else -16), r1, u) + drift[2] * d, sc
    x, y, r, sc = pos(t); x2, y2, _, _ = pos(t + 1 / FPS)
    card(c, P_, x, y, r, ((x2 - x) * 1.4, (y2 - y) * 1.4), sc=sc)
def lt(t, j): return t - (SCN[j][0] - PRE)   # film clock of a scene's prints: they start playing as they scatter in
def circle_arrow(can, t, t0, cx, cy, rx, ry, dur=1.1):
    if t < t0: return
    u = eio(clamp((t - t0) / dur)); a0 = math.radians(200); a1 = a0 + u * math.radians(320)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pts = [(cx + rx * math.cos(a0 + (a1 - a0) * i / 80), cy + ry * math.sin(a0 + (a1 - a0) * i / 80)) for i in range(81)]
    d.line(pts, fill=CREAM + (240,), width=7, joint='curve')
    if u > 0.05:
        (xa, ya), (xb, yb) = pts[-4], pts[-1]; ang = math.atan2(yb - ya, xb - xa)
        for s in (2.6, -2.6): d.line((xb, yb, xb - 30 * math.cos(ang + s * 0.2), yb - 30 * math.sin(ang + s * 0.2)), fill=CREAM + (240,), width=7)
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.5))); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)), (3, 5)); can.alpha_composite(L)

# ---------- scenes on the table ----------
BWS = {'101I-337-0043-16', '146-1986-013-04', '101I-404-0512-17', '101I-600-1150-30A', '101I-404-0529-11', '183-L09694', '146-1971-116-29'}
def PH(n, wd, seed, cap=None): return (BW if n in BWS else SP)(n, wd, seed, cap)
def s_born(c, t, ox, oy):
    enter(c, PH('101I-404-0532-18A', 520, 11, cap='Helmut Wick'), t, (380, 600), -3, ox, oy, (2, 3, 0.08), main=True)
def s_ausb(c, t, ox, oy):
    enter(c, PH('101I-337-0043-16', 980, 21), t, (540, 540), 2, ox, oy, (-2, 3, -0.08), main=True)
    later(c, PH('101I-337-0012-09', 420, 22), t, ws('Lehrgang') - 0.1, (760, 900), -5, ox, oy, (1, 0.2))
def s_jg53(c, t, ox, oy):
    enter(c, PH('101I-058-1784A-14', 980, 31), t, (540, 540), -2, ox, oy, (3, 2, 0.08), main=True)
    later(c, PH('183-L14164', 480, 32, cap='Werner Mölders'), t, ws('Werner') - 0.1, (760, 880), 5, ox, oy, (1, 0.2))
def s_jg2(c, t, ox, oy):
    j = 4; enter(c, FP('stab', lt(t, j), 1000, 41), t, (540, 540), 2, ox, oy, (-3, 2, -0.08), main=True)
    later(c, PH('101I-404-0549-25', 480, 42), t, ws('Richthofen') - 0.1, (770, 880), -5, ox, oy, (1, 0.2))
def s_first(c, t, ox, oy):
    j = 5; enter(c, FP('kampf', lt(t, j), 1000, 51), t, (540, 540), -2, ox, oy, (3, 2, 0.08), main=True)
    later(c, PH('101I-342-0628-07', 480, 52), t, ws('französisches') - 0.1, (770, 880), 5, ox, oy, (1, 0.2))
def s_bob(c, t, ox, oy):
    enter(c, PH('146-1968-015-19', 520, 61), t, (360, 600), -3, ox, oy, (2, 3, 0.08), main=True)
    later(c, PH('101I-404-0529-24', 520, 62), t, ws('England') - 0.1, (740, 780), 4, ox, oy, (1, 0.2))
def s_eich(c, t, ox, oy):
    enter(c, PH('146-1986-013-04', 540, 71, cap='Oktober 1940'), t, (540, 560), 2, ox, oy, (-2, 3, -0.08), main=True)
def s_kommo(c, t, ox, oy):
    enter(c, PH('146-2015-0025', 520, 81, cap='Sperrle und Wick'), t, (360, 600), -3, ox, oy, (2, 3, 0.08), main=True)
    later(c, PH('101I-404-0512-19', 520, 82), t, ws('jüngste') - 0.1, (740, 780), 4, ox, oy, (1, 0.2))
def s_prop(c, t, ox, oy):
    j = 9; enter(c, FP('goering', lt(t, j) + 3.5, 1000, 91, cap='Wochenschau, November 1940'), t, (540, 540), -2, ox, oy, (3, 2, 0.08), main=True)
    later(c, PH('101I-404-0529-12', 470, 92), t, ws('Presse') - 0.1, (770, 880), 5, ox, oy, (1, 0.2))
def s_28(c, t, ox, oy):
    j = 10; enter(c, FP('board', lt(t, j), 1000, 101), t, (540, 540), 2, ox, oy, (-3, 2, -0.08), main=True)
    later(c, PH('101I-404-0546-09', 400, 102), t, ws('Stabsschwarm') - 0.1, (780, 900), -5, ox, oy, (1, 0.2))
    later(c, PH('146-1971-116-29', 380, 103, cap='Mölders'), t, ws('Mölders', 65.02) - 0.1, (300, 920), 4, ox, oy, (-1, 0.2))
def s_cher(c, t, ox, oy):
    enter(c, PH('101II-MW-2370-18', 980, 111, cap='Cherbourg, 1940'), t, (540, 540), -2, ox, oy, (3, 2, 0.08), main=True)
    later(c, PH('146-1997-026-32A', 420, 112), t, ws('tanken') - 0.1, (770, 900), 5, ox, oy, (1, 0.2))
def s_insel(c, t, ox, oy):
    j = 12; enter(c, FP('takeoff', lt(t, j), 1000, 121), t, (540, 540), 2, ox, oy, (-3, 2, -0.08), main=True)
    later(c, FP('gun', t - ws('weitere'), 480, 122), t, ws('weitere') - 0.1, (770, 880), -5, ox, oy, (1, 0.2))
def s_609(c, t, ox, oy):
    j = 13; enter(c, FP('raf', lt(t, j), 1000, 131), t, (540, 540), -2, ox, oy, (3, 2, 0.08), main=True)
    later(c, FP('spit2', t - ws('Wicks') + 5.0, 480, 132), t, ws('Wicks') - 0.1, (770, 880), 5, ox, oy, (1, 0.2))
def s_pflanz(c, t, ox, oy):
    j = 14; enter(c, FP('dog', lt(t, j), 1000, 141), t, (540, 540), 2, ox, oy, (-3, 2, -0.08), main=True)
    later(c, PH('146-1969-094-18', 480, 142), t, ws('Dundas', 86.52) - 0.1, (770, 880), -5, ox, oy, (1, 0.2))
def s_boot(c, t, ox, oy):
    enter(c, PH('183-B13755', 520, 151), t, (360, 600), -3, ox, oy, (2, 3, 0.08), main=True)
    later(c, PH('101II-MN-1527-06', 480, 152), t, ws('Torpedoboote') - 0.1, (750, 800), 4, ox, oy, (1, 0.2))
def s_nie(c, t, ox, oy):
    j = 16; enter(c, FP('sea', lt(t, j), 1000, 161), t, (540, 540), 2, ox, oy, (-3, 2, -0.08), main=True)
    later(c, PH('101II-MN-1527-11', 470, 162), t, ws('gefunden') - 0.1, (770, 880), -5, ox, oy, (1, 0.2))
def s_bilanz(c, t, ox, oy):
    enter(c, PH('101I-600-1150-30A', 980, 171), t, (540, 540), -2, ox, oy, (3, 2, 0.08), main=True)
    later(c, PH('101I-404-0529-11', 470, 172), t, ws('Feindflug') - 0.1, (770, 880), 5, ox, oy, (1, 0.2))
def s_end(c, t, ox, oy):
    enter(c, PH('101I-404-0512-17', 560, 181, cap='1915 bis 1940'), t, (540, 580), 2, ox, oy, (-2, 3, -0.08), main=True)

# ---------- hook (Egon: film full-bleed, words typing on, the name brings prints, then it pulls back onto the table) ----------
H1 = ws('Helmut')
ZS = ws('Er', 8.17) - 0.25; ZE = ZS + 0.55
T2b = ZE + 0.15
ZH = 1.8
HOOKP = [('101I-404-0512-17', 600, 540, 560, -3, 0.0)]   # Schnaufer's portrait drops in at his name: (photo, width, x, y, rotation, delay)
def hookcard_print(tt): return print_im(hookbg(tt).convert('RGB').resize((600, 1067), Image.LANCZOS), 600, False, None, 7)
def hook_prints(c, t, f=1.0, ox=0.0, oy=0.0, blur=True):
    for i, (k, wd, x1, y1, r1, dl) in enumerate(HOOKP):
        t0 = H1 + dl
        if t < t0: continue
        def pos(tt):
            u = eout((tt - t0) / (1.0 * eg.SLOW)); return x1 + 2 * (tt - t0), lerp(-800, y1, u) + 3 * (tt - t0), lerp(r1 + 9, r1, u)
        x, y, r = pos(t); x2, y2, _ = pos(t + 1 / FPS); d = t - t0; sc = 1.0 + 0.25 * (1 - eout(d / 2.8)) - 0.01 * d
        P_ = PH(k, wd, 30 + i)
        card(c, P_, 540 + (x - 540) * f + ox, 960 + (y - 960) * f + oy, r, ((x2 - x) * 1.6 * f, (y2 - y) * 1.6 * f) if blur else (0, 0), sc=sc * f)
def s_hookcard(c, t, ox, oy):
    card(c, hookcard_print(t), 540 + ox, 960 + oy, 0)
    hook_prints(c, t, 1 / ZH, ox, oy, False)
def qlines(can, t, lines, y0, size, tout, cols=None, lh=1.04):
    """hook type: one line per call so short lines stay big and only long words shrink to the 700 px width"""
    y = y0
    for i, l in enumerate(lines):
        sz = eg.fit([' '.join(w_ for w_, _ in l)], size, 900, -2)
        quote(can, t, [l], y + sz * 0.5, size=sz, tout=tout, col={0: (cols or {}).get(i, CREAM)}); y += sz * lh
def hook_frame(t):
    can = hookbg(t)
    quote(can, t, [[('ER', ws('Er')), ('WURDE', ws('wurde'))], [('DER', ws('der')), ('ERFOLGREICHSTE', ws('erfolgreichste'))], [('JAGDFLIEGER', ws('Jagdflieger'))], [('DER', ws('der', 1.86)), ('LUFTWAFFE,', ws('Luftwaffe'))]],
          900, size=84, tout=ws('und') - 0.08, lh=1.02, col={2: YEL})
    quote(can, t, [[('UND', ws('und')), ('NUR', ws('nur'))], [('ZWEI', ws('zwei')), ('STUNDEN', ws('Stunden'))], [('SPÄTER', ws('später'))], [('VERSCHWAND', ws('verschwand')), ('ER', ws('er', 4.72))],
                    [('ÜBER', ws('über')), ('DEM', ws('dem'))], [('ÄRMELKANAL.', ws('Ärmelkanal'))]], 900, size=84, tout=ws('Sein') - 0.12, lh=1.02, col={5: YEL})
    hook_prints(can, t)
    quote(can, t, [[('SEIN', ws('Sein')), ('NAME', ws('Name')), ('WAR', ws('war', 6.62))], [('HELMUT', ws('Helmut'))], [('WICK.', ws('Wick'))]], 1000, size=96, tout=ZS - 0.12, lh=1.02, col={1: YEL, 2: YEL})
    return can

# ---------- camera (eg.campos / table_frame) ----------
GX, GY = 1380, 2160
PATH = [(-1, 0), (0, 0), (1, 0), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3), (0, 4), (1, 4), (2, 4)]
SCN = [(ZS, s_hookcard), (T2b, s_born), (ws('In', 13.96), s_ausb), (ws('Im', 19.42), s_jg53), (ws('Bei', 25.18), s_jg2), (ws('Im', 28.72), s_first), (ws('Im', 35.73), s_bob),
       (ws('Im', 40.37), s_eich), (ws('Kurz', 46.45), s_kommo), (ws('Die', 52.04), s_prop), (ws('Am', 55.5), s_28), (ws('Nach', 66.91), s_cher), (ws('Über', 70.71), s_insel),
       (ws('Kurz', 73.66), s_609), (ws('Sein', 83.04), s_pflanz), (ws('Pflanz', 89.1), s_boot), (ws('Wick', 100.49), s_nie), (ws('Ihm', 101.58), s_bilanz), (ws('Helmut', 107.97), s_end)]
ANC = [(p[0] * GX, p[1] * GY) for p in PATH]
PRE, POST = 0.25, 1.25
TEND = WORDS[-1][2] + 1.4
def campos(t):
    k = max(i for i, (a, _) in enumerate(SCN) if a <= t) if t >= SCN[0][0] else 0
    nxt = k + 1 if k + 1 < len(SCN) and t >= SCN[k + 1][0] - PRE else None
    if nxt is not None: k, prev = nxt, k
    else: prev = k - 1 if k > 0 and t < SCN[k][0] + POST else None
    if prev is None: return ANC[k], (0.0, 0.0), k, None
    b = SCN[k][0]; f = lambda tt: eio(clamp((tt - (b - PRE)) / (PRE + POST)))
    u, u2 = f(t), f(t + 1 / FPS); (ax, ay), (bx, by) = ANC[prev], ANC[k]
    return (lerp(ax, bx, u), lerp(ay, by, u)), ((bx - ax) * (u2 - u), (by - ay) * (u2 - u)), k, (prev, u)
def zoom_at(t):
    k = max([i for i, (a, _) in enumerate(SCN) if a <= t] or [0]); a = SCN[k][0] + POST
    if k == 0: return lerp(ZH, 1.0, eio((t - ZS) / (ZE - ZS)))
    return 1.0 + 0.006 * max(0.0, t - a)
def table_frame(t):
    (cx, cy), (vx, vy), k, tr = campos(t)
    can = table_view(cx, cy).convert('RGBA')
    bg_layer(can, t, cx, cy)
    for j in range(max(0, k - 1), min(len(SCN), k + 2)):
        CUR[0] = SCN[j][0]; CNT[0] = 0; CURJ[0] = j; SCN[j][1](can, t, ANC[j][0] - cx, ANC[j][1] - cy)
    if tr is not None:
        prev, u = tr; can = dblur(can, vx * 0.6, vy * 0.6)
        z = lerp(zoom_at(SCN[k][0] - PRE), 1.0, u)
    else: z = zoom_at(t)
    if z > 1.0005:
        bw, bh = W / z, H / z; can = can.resize((W, H), Image.BICUBIC, box=(540 - 540 / z, 960 - 960 / z, 540 - 540 / z + bw, 960 - 960 / z + bh))
    return can
def frame(t):
    if t < ZS: img = hook_frame(t)
    elif t < ZS + 0.15: img = Image.blend(hook_frame(t), table_frame(t), (t - ZS) / 0.15)
    else: img = table_frame(t)
    return finish(img, t)   # no fade at the end

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
