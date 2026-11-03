# Günther Prien, CDM Short in style A, the Egon Mayer v6 way (egon/code/eg.py, via bism/code/bm2.py):
# hook = full-bleed blue-toned film of a U-boat bow in the sea with the words typing on; at "Günther Prien" his portrait drops in;
# the hook pulls back onto one big table of blue-toned prints; the camera travels left/right/up/down from group to group,
# each new group scattering in with the move. Prints play film where film exists (U-boat, periscope, return of U 47, crew),
# photos elsewhere (portraits, Royal Oak, Scapa Flow map, the bull emblem); swastikas on caps and Knight's Crosses blurred small.
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
def SP(n, wd, seed, cap=None): return print_im(Image.open(E + 'img/c_%d.jpg' % n).convert('RGB'), wd, False, cap, seed)   # colourised photo print (Boran's upscale; symbols blurred again after it)
# hook background: the U-boat bow cutting through the sea, cut to 9:16 (clip/hook, 30 fps), blue-toned like the Egon hook
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
PILE = ['sea', 'launch', 'peri', 'peri2', 'dive', 'arrive', 'deck', 'march']
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
def s_born(c, t, ox, oy):
    enter(c, SP(754, 560, 11, cap='Günther Prien'), t, (380, 610), -3, ox, oy, (2, 3, 0.08), main=True)
    later(c, SP(835, 420, 12), t, ws('See') - 0.1, (770, 860), 5, ox, oy, (1, 0.2))
    title(c, t, '1908', ['OSTERFELD'], 1380, ws('1908'), ws('Osterfeld'), ox, oy, True, 200, 80, ['ZUERST AUF EINEM SEGELSCHIFF'], ws('zuerst') - 0.3, cps=20)
def s_crisis(c, t, ox, oy):
    enter(c, SP(790, 560, 21), t, (380, 600), 3, ox, oy, (-2, 3, -0.08), main=True)
    later(c, SP(15, 430, 22), t, ws('Reichsmarine') - 0.2, (780, 880), -5, ox, oy, (1, 0.2))
    quote(c, t, [[('WELTWIRTSCHAFTSKRISE', ws('Weltwirtschaftskrise'))]], 1270, ox, oy, 62)
    quote(c, t, [[('REICHSMARINE', ws('Reichsmarine'))]], 1380, ox, oy, 86, col={0: YEL})
def s_u47(c, t, ox, oy):
    j = 3; enter(c, FP('launch', lt(t, j), 1000, 31), t, (540, 560), -2, ox, oy, (3, 2, 0.08), main=True)
    later(c, SP(744, 600, 32), t, ws('U', 25.9) - 0.1, (720, 930), 5, ox, oy, (1, 0.2))
    title(c, t, 'U 47', ['KOMMANDANT'], 1390, ws('U', 25.9), ws('kommandierte'), ox, oy, True, 200, 70, cps=20)
def s_night(c, t, ox, oy):
    j = 4; enter(c, FP('sea', lt(t, j), 1000, 41), t, (540, 560), 2, ox, oy, (-3, 2, -0.08), main=True)
    title(c, t, '1939', ['14. OKTOBER', 'SCAPA FLOW'], 1390, ws('1939'), [ws('14.'), ws('Scapa', 31)], ox, oy, True, 200, 66, cps=20)
def s_map(c, t, ox, oy):
    enter(c, SP(152, 960, 51), t, (540, 560), -2, ox, oy, (3, 2, 0.08), main=True)
    quote(c, t, [[('SCHMALE', ws('schmale')), ('DURCHFAHRT', ws('Durchfahrt'))]], 1270, ox, oy, 62)
    quote(c, t, [[('BLOCKSCHIFFE', ws('Blockschiffen'))]], 1380, ox, oy, 86, col={0: YEL})
def s_oak(c, t, ox, oy):
    enter(c, SP(156, 1000, 61, cap='HMS Royal Oak'), t, (540, 560), 2, ox, oy, (-3, 2, -0.08), main=True)
    quote(c, t, [[('ROYAL', ws('Royal', 42)), ('OAK', ws('Oak', 42))]], 1290, ox, oy, 100, col={0: YEL})
    quote(c, t, [[('VOR', ws('vor', 43)), ('ANKER', ws('Anker'))]], 1400, ox, oy, 62)
def s_attack(c, t, ox, oy):
    j = 7; enter(c, FP('peri', lt(t, j), 1000, 71), t, (540, 560), -2, ox, oy, (3, 2, 0.08), main=True)
    quote(c, t, [[('NUR', ws('nur', 45)), ('DER', ws('den', 45.5)), ('BUG', ws('Bug'))]], 1260, ox, oy, 62, tout=ws('Prien', 46) - 0.1)
    quote(c, t, [[('ZWEITER', ws('zweites')), ('ANGRIFF', ws('Mal', 48))]], 1260, ox, oy, 62)
    title(c, t, '3', ['TORPEDOS'], 1390, ws('drei', 50), ws('Torpedos'), ox, oy, True, 210, 80, cps=24)
def s_capsize(c, t, ox, oy):
    enter(c, SP(162, 1000, 81), t, (540, 560), 2, ox, oy, (-3, 2, -0.08), main=True)
    quote(c, t, [[('IN', ws('innerhalb')), ('13', ws('13')), ('MINUTEN', ws('Minuten', 53))]], 1240, ox, oy, 62)
    title(c, t, '835', ['TOTE'], 1380, ws('835'), ws('starben'), ox, oy, True, 200, 84, ['MEHR ALS 100 JUNGEN UNTER 18'], ws('mehr', 56.5) - 0.3, cps=24)
def s_escape(c, t, ox, oy):
    j = 9; enter(c, FP('arrive', lt(t, j), 1000, 91), t, (540, 560), -2, ox, oy, (3, 2, 0.08), main=True)
    quote(c, t, [[('U 47', ws('U', 60)), ('ENTKAM', ws('entkam'))]], 1340, ox, oy, 86, col={0: YEL})
def s_berlin(c, t, ox, oy):
    j = 10; enter(c, FP('march', lt(t, j), 1000, 101), t, (540, 560), 2, ox, oy, (-3, 2, -0.08), main=True)
    later(c, SP(220, 400, 102), t, ws('Stier') - 0.2, (780, 900), 6, ox, oy, (1, 0.2))
    quote(c, t, [[('IN', ws('In', 62.9)), ('BERLIN', ws('Berlin'))]], 1270, ox, oy, 60)
    quote(c, t, [[('STIER', ws('Stier')), ('VON', ws('von', 67.3)), ('SCAPA', ws('Scapa', 67.5)), ('FLOW', ws('Flow', 67.9))]], 1380, ox, oy, 76, col={0: YEL})
def s_atlantic(c, t, ox, oy):
    j = 11; enter(c, FP('deck', lt(t, j), 1000, 111), t, (540, 560), -2, ox, oy, (3, 2, 0.08), main=True)
    later(c, SP(820, 420, 112), t, ws('Atlantik', 69) - 0.1, (770, 900), -5, ox, oy, (1, 0.2))
    title(c, t, '30', ['HANDELSSCHIFFE'], 1390, ws('30'), ws('Handelsschiffe'), ox, oy, True, 210, 70, cps=26)
def s_arandora(c, t, ox, oy):
    j = 12; enter(c, FP('peri2', lt(t, j), 1000, 121), t, (540, 560), 2, ox, oy, (-3, 2, -0.08), main=True)
    quote(c, t, [[('ARANDORA', ws('Arandora')), ('STAR', ws('Star'))]], 1270, ox, oy, 86, col={0: YEL})
    quote(c, t, [[('MEHR', ws('mehr', 77.5)), ('ALS', ws('als', 77.8)), ('800', ws('800')), ('TOTE', ws('Menschen', 78))]], 1390, ox, oy, 64)
def s_lost(c, t, ox, oy):
    j = 13; enter(c, FP('dive', lt(t, j), 1000, 131), t, (540, 560), -2, ox, oy, (3, 2, 0.08), main=True)
    quote(c, t, [[('KEIN', ws('kein', 86.5)), ('FUNKSPRUCH', ws('Funkspruch')), ('MEHR', ws('mehr', 87.5))]], 1180, ox, oy, 58)
    title(c, t, '1941', ['MÄRZ'], 1390, ws('1941'), ws('März'), ox, oy, True, 200, 84, cps=20)
def s_silence(c, t, ox, oy):
    enter(c, SP(843, 560, 141), t, (380, 600), 3, ox, oy, (-2, 3, -0.08), main=True)
    quote(c, t, [[('VERSCHWIEGEN', ws('verschwieg'))]], 1200, ox, oy, 60)
    quote(c, t, [[('ÜBER', ws('über', 90)), ('ZEHN', ws('zehn', 90)), ('WOCHEN', ws('Wochen', 90))]], 1300, ox, oy, 80, col={0: YEL})
    quote(c, t, [[('GERÜCHT:', ws('hieß', 91.5)), ('STRAFLAGER', ws('Straflager'))]], 1410, ox, oy, 54)
def s_end(c, t, ox, oy):
    enter(c, SP(873, 600, 151), t, (540, 620), -2, ox, oy, (-2, 3, -0.08), main=True)
    title(c, t, '45', ['MANN', 'VERSCHOLLEN'], 1250, ws('45'), [ws('Mann', 97.5), ws('geschah')], ox, oy, True, 170, 62, cps=22)
    quote(c, t, [[('33', ws('33')), ('JAHRE', ws('Jahre', 101))]], 1450, ox, oy, 110, col={0: YEL})

# ---------- hook (Egon: film full-bleed, words typing on, the name brings prints, then it pulls back onto the table) ----------
H1 = ws('Günther')
ZS = ws('Er', 10) - 0.25; ZE = ZS + 0.55
T2b = ZE + 0.15
ZH = 1.8
HOOKP = [(709, 620, 540, 560, -3, 0.0)]   # Prien's portrait drops in at his name: (photo, width, x, y, rotation, delay)
def hookcard_print(tt): return print_im(hookbg(tt).convert('RGB').resize((600, 1067), Image.LANCZOS), 600, False, None, 7)
def hook_prints(c, t, f=1.0, ox=0.0, oy=0.0, blur=True):
    for i, (k, wd, x1, y1, r1, dl) in enumerate(HOOKP):
        t0 = H1 + dl
        if t < t0: continue
        def pos(tt):
            u = eout((tt - t0) / (1.0 * eg.SLOW)); return x1 + 2 * (tt - t0), lerp(-800, y1, u) + 3 * (tt - t0), lerp(r1 + 9, r1, u)
        x, y, r = pos(t); x2, y2, _ = pos(t + 1 / FPS); d = t - t0; sc = 1.0 + 0.25 * (1 - eout(d / 2.8)) - 0.01 * d
        P_ = SP(k, wd, 30 + i)
        card(c, P_, 540 + (x - 540) * f + ox, 960 + (y - 960) * f + oy, r, ((x2 - x) * 1.6 * f, (y2 - y) * 1.6 * f) if blur else (0, 0), sc=sc * f)
def s_hookcard(c, t, ox, oy):
    card(c, hookcard_print(t), 540 + ox, 960 + oy, 0)
    hook_prints(c, t, 1 / ZH, ox, oy, False)
def qlines(can, t, lines, y0, size, tout, cols=None, lh=1.2):
    """hook type: one line per call so short lines stay big and only long words shrink to the 700 px width"""
    y = y0
    for i, l in enumerate(lines):
        sz = eg.fit([' '.join(w_ for w_, _ in l)], size, 900, -2)
        quote(can, t, [l], y + sz * 0.5, size=sz, tout=tout, col={0: (cols or {}).get(i, CREAM)}); y += sz * lh
def hook_frame(t):
    can = hookbg(t)
    qlines(can, t, [[('ER', ws('Er')), ('VERSENKTE', ws('versenkte'))], [('EIN', ws('ein')), ('BRITISCHES', ws('britisches'))], [('SCHLACHTSCHIFF', ws('Schlachtschiff'))],
                    [('MITTEN', ws('mitten')), ('IM', ws('im'))], [('WICHTIGSTEN', ws('wichtigsten'))], [('STÜTZPUNKT', ws('Stützpunkt'))], [('DER', ws('der', 3.4)), ('ROYAL', ws('Royal')), ('NAVY,', ws('Navy'))]],
           620, 110, ws('und') - 0.08, {2: YEL})
    qlines(can, t, [[('UND', ws('und')), ('ANDERTHALB', ws('anderthalb'))], [('JAHRE', ws('Jahre')), ('SPÄTER', ws('später'))], [('VERSCHWAND', ws('verschwand')), ('ER', ws('er', 6.3))],
                    [('SPURLOS', ws('spurlos'))], [('IM', ws('im', 7.1)), ('ATLANTIK.', ws('Atlantik'))]], 680, 110, ws('Sein') - 0.12, {3: YEL})
    hook_prints(can, t)
    qlines(can, t, [[('SEIN', ws('Sein')), ('NAME', ws('Name')), ('WAR', ws('war', 8.6))], [('GÜNTHER', ws('Günther')), ('PRIEN.', ws('Prien'))]], 1180, 110, ZS - 0.12, {1: YEL})
    return can

# ---------- camera (eg.campos / table_frame) ----------
GX, GY = 1380, 2160
PATH = [(-1, 0), (0, 0), (1, 0), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3)]
SCN = [(ZS, s_hookcard), (T2b, s_born), (ws('In', 16.5), s_crisis), (ws('Bei', 23.7), s_u47), (ws('In', 27.4), s_night), (ws('Er', 35.9), s_map), (ws('doch', 41), s_oak),
       (ws('Der', 44), s_attack), (ws('Die', 51), s_capsize), (ws('U', 60), s_escape), (ws('In', 62.9), s_berlin), (ws('Danach', 68.4), s_atlantic), (ws('Eines', 71.5), s_arandora),
       (ws('Im', 80.3), s_lost), (ws('Die', 88), s_silence), (ws('Was', 94.8), s_end)]
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
