# Jean Laidlaw Short: photo-led, Kammhuber palette; chalk-on-floor drawings of the convoy game and the Raspberry counter-move
import sys, math, subprocess
import base
from base import *
base.BLUR.clear()
# italic = the same Anton letters, only slanted (no font change)
_sprite = base.sprite
@functools.lru_cache(maxsize=4096)
def sprite(txt, fk, size, color, shadow=True, track=0, blur=0):
    if not fk.endswith('_i'): return _sprite(txt, fk, size, color, shadow, track, blur)
    im = _sprite(txt, fk[:-2], size, color, shadow, track, blur); k = 0.2; h = im.height; ex = int(k * h)
    return im.transform((im.width + ex, h), Image.AFFINE, (1, k, -k * h, 0, 1, 0), Image.BICUBIC)
base.sprite = sprite; FK['serif_i'] = FK['serif']

TEND = 109.2

def shot(c, grad=GRAD):
    can = c.frame(); can.alpha_composite(grad); return can
GR = [np.random.default_rng(i).normal(0, 4.0, (H // 2, W // 2)).astype(np.int16) for i in range(6)]
def grain(img, n):
    a = np.asarray(img).astype(np.int16); g = np.kron(GR[n % 6], np.ones((2, 2), np.int16))[..., None]
    return Image.fromarray(np.clip(a + g, 0, 255).astype(np.uint8))
def ui_overlay(im):
    im = im.convert('RGBA'); L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((0, 0, W, 290), fill=(255, 0, 0, 60)); d.rectangle((930, 680, W, 1580), fill=(255, 0, 0, 80)); d.rectangle((0, 1580, W, H), fill=(255, 0, 0, 80))
    im.alpha_composite(L); return im.convert('RGB')
def dim(can, a):
    if a > 0: can.alpha_composite(Image.new('RGBA', (W, H), (4, 6, 8, int(a))))
def fade_out(t, t1, d=0.3): return 1.0 if t1 is None else 1 - ease((t - t1) / d)
def layer(can, a, fn):
    """draw fn onto a transparent layer, composite with alpha a (lets arrows and labels leave together)"""
    if a <= 0.01: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(L)
    if a < 0.999: L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
    can.alpha_composite(L)

# ---------- motion: constant slow speed for the whole time the photo is on screen ----------
SPEED = 34.0
def pan_lin(p, t, w0, w1, fx, d, cy=None):
    im = src(p); scale = H / im.height; w = min(im.width, im.height * 9 / 16)
    span = SPEED * (w1 - w0) / scale
    lo, hi = w / 2, im.width - w / 2
    a, b = fx - d * span / 2, fx + d * span / 2
    if min(a, b) < lo: sh = lo - min(a, b); a += sh; b += sh
    if max(a, b) > hi: sh = max(a, b) - hi; a -= sh; b -= sh
    u = clamp((t - w0) / (w1 - w0))
    return PCam(p, lerp(a, b, u), im.height / 2 if cy is None else cy, w)
def zoom_lin(p, t, w0, w1, cx, cy, z1=1.06, z0=1.0):
    im = src(p); w = min(im.width, im.height * 9 / 16); u = clamp((t - w0) / (w1 - w0))
    return PCam(p, cx, cy, w / lerp(z0, z1, u))
def wide(p, t, w0, w1, fx, d, hh=1240, yc=860):
    """landscape photo shown wider than full height: sharp band of height hh over a blurred, darkened copy"""
    im = src(p); scale = hh / im.height; sw = W / scale
    span = SPEED * (w1 - w0) / scale; lo, hi = sw / 2, im.width - sw / 2
    a, b = fx - d * span / 2, fx + d * span / 2
    if min(a, b) < lo: sh = lo - min(a, b); a += sh; b += sh
    if max(a, b) > hi: sh = max(a, b) - hi; a -= sh; b -= sh
    x = lerp(a, b, clamp((t - w0) / (w1 - w0)))
    bg = PCam(p, x, im.height / 2, 99999).frame().filter(ImageFilter.GaussianBlur(28))
    bg = Image.blend(bg, Image.new('RGBA', (W, H), (8, 10, 12, 255)), 0.5)
    bd = im.resize((W, hh), Image.BILINEAR, box=(x - sw / 2, 0, x + sw / 2, im.height)).convert('RGBA')
    m = Image.new('L', (W, hh), 255); dm = ImageDraw.Draw(m)
    for i in range(40): dm.line((0, i, W, i), fill=int(255 * i / 40)); dm.line((0, hh - 1 - i, W, hh - 1 - i), fill=int(255 * i / 40))
    bg.paste(bd, (0, yc - hh // 2), m); bx = x - sw / 2
    return bg, (lambda sx, sy: ((sx - bx) * scale, sy * scale + yc - hh / 2))

# ---------- text helpers ----------
def digits(can, t, t0, txt, cy, size=330, col=GOLD, step=0.28, fk='serif_i', t1=None):
    """big italic number, its digits arriving one after another"""
    if t < t0 or (t1 is not None and t > t1 + 0.3): return
    out = fade_out(t, t1)
    size = fit(txt, fk, size, maxw_at(cy)); f = FK[fk](size); x = 540 - textw(txt, fk, size) / 2
    for i, ch in enumerate(txt):
        k = eout((t - t0 - i * step) / 0.3); w = f.getlength(ch)
        if k > 0: put(can, sprite(ch, fk, size, col), x + w / 2, cy + (1 - k) * 30, lerp(1.25, 1.0, k), k * out)
        x += w
def strike(can, t, t0, t1, txt, cy, size=130, col=CREAM):
    if t < t0: return
    focus(can, t, t0, txt, 'serif', size, col, cy, dur=0.35)
    if t >= t1:
        sz = fit(txt, 'serif', size, maxw_at(cy)); tw = textw(txt, 'serif', sz)
        k = eio((t - t1) / 0.35); x0 = 540 - tw / 2 - 20
        stroke(can, [(x0, cy + 18), (x0 + (tw + 40) * k, cy - 8 * k)], RUST, 14)
def typewriter(can, t, t0, txt, cy, cps=16, size=58):
    """paper slip, text typed letter by letter in the typewriter face"""
    if t < t0: return
    f = FK['type'](size); tw = f.getlength(txt); k = eout((t - t0) / 0.3)
    w, h = tw + 90, size + 70; L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    y = cy + (1 - k) * 30
    d.rectangle((540 - w / 2 + 8, y - h / 2 + 10, 540 + w / 2 + 8, y + h / 2 + 10), fill=(0, 0, 0, int(120 * k)))
    d.rectangle((540 - w / 2, y - h / 2, 540 + w / 2, y + h / 2), fill=PAPER + (int(250 * k),))
    n = int(clamp((t - t0 - 0.25) * cps / len(txt)) * len(txt))
    d.text((540 - tw / 2, y - size * 0.62), txt[:n], font=f, fill=INK + (255,))
    if n < len(txt) and int(t * 4) % 2 == 0:
        cx = 540 - tw / 2 + f.getlength(txt[:n]); d.rectangle((cx + 2, y - size * 0.45, cx + 6, y + size * 0.45), fill=RUST + (255,))
    can.alpha_composite(L)

# ---------- chalk ----------
CHALK = (236, 234, 222); CH_Y = (246, 206, 70); CH_R = (226, 78, 66)
_cr = np.random.default_rng(11)
_cn = _cr.random((H, W)).astype(np.float32)
_cl = np.asarray(Image.fromarray((_cr.random((H // 3, W // 3)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) / 255
CHALK_A = np.clip(0.35 + 0.55 * _cn + 0.35 * _cl, 0, 1)   # grainy, uneven pressure
def chalkify(L, soft=0.7):
    a = np.asarray(L.getchannel('A')).astype(np.float32) * CHALK_A
    L.putalpha(Image.fromarray(a.clip(0, 255).astype(np.uint8)))
    return L.filter(ImageFilter.GaussianBlur(soft))
def cline(d, pts, col, w=5, a=1.0):
    if len(pts) >= 2: d.line(pts, fill=col + (int(255 * a),), width=w, joint='curve')
def cdash(d, pts, col, w=5, a=1.0, on=16, off=12):
    """dashed polyline"""
    acc = 0.0; per = on + off
    for i in range(len(pts) - 1):
        p, q = pts[i], pts[i + 1]; s = math.dist(p, q)
        if s == 0: continue
        u = 0.0
        while u < s:
            ph = (acc + u) % per; run = (on - ph) if ph < on else (per - ph)
            v = min(s, u + run)
            if ph < on: d.line((lerp(p[0], q[0], u / s), lerp(p[1], q[1], u / s), lerp(p[0], q[0], v / s), lerp(p[1], q[1], v / s)), fill=col + (int(255 * a),), width=w)
            u = v + 0.01
        acc += s

@functools.lru_cache(None)
def floor_bg():
    """dark wooden floor seen from above, faint chalk grid of the game board"""
    rng = np.random.default_rng(4); a = np.zeros((H, W, 3), np.float32)
    y = 0
    while y < H:
        h = int(rng.uniform(120, 170)); c = np.array((40, 33, 27), np.float32) * rng.uniform(0.82, 1.12)
        a[y:y + h] = c; a[y:y + 3] *= 0.45; y += h
    streak = np.asarray(Image.fromarray((rng.random((H // 40, W // 2)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) / 255
    a *= (0.85 + 0.3 * streak)[..., None]
    a *= (1 + (PAPER_TEX[..., None] - 1) * 0.12)
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2)
    a *= (1 - 0.45 * np.clip(r - 0.4, 0, 1))[..., None]
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(6):   # old smudges of rubbed-out chalk
        x, y_, r_ = rng.uniform(100, 980), rng.uniform(400, 1600), rng.uniform(80, 220)
        d.ellipse((x - r_, y_ - r_ * 0.5, x + r_, y_ + r_ * 0.5), fill=CHALK + (16,))
    L = L.filter(ImageFilter.GaussianBlur(30)); im.alpha_composite(L)
    G = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(G)
    for x in range(90, W, 90): d.line((x, 300, x, 1620), fill=CHALK + (34,), width=2)
    for y in range(300, 1621, 90): d.line((0, y, W, y), fill=CHALK + (34,), width=2)
    im.alpha_composite(chalkify(G)); return im

def ship_pts(cx, cy, l=112, w=46):
    return [(cx, cy - l / 2), (cx + w / 2, cy - l / 2 + w * 0.8), (cx + w / 2, cy + l / 2), (cx - w / 2, cy + l / 2), (cx - w / 2, cy - l / 2 + w * 0.8), (cx, cy - l / 2)]
def sub_pts(cx, cy, l=110, w=28):
    pts = [(cx + w / 2 * math.sin(a), cy - l / 2 * math.cos(a)) for a in np.linspace(0, 2 * math.pi, 28)]
    return pts
def sub_draw(d, cx, cy, col, a=1.0, k=1.0, dashed=False):
    pts = partial(sub_pts(cx, cy), k)
    (cdash if dashed else cline)(d, pts, col, 5, a)
    if k >= 1: d.rectangle((cx - 7, cy - 12, cx + 7, cy + 10), outline=col + (int(255 * a),), width=4)
def burst(d, cx, cy, u, col=CH_R):
    """chalk explosion star, grows then stays"""
    for i in range(10):
        ang = i * math.pi / 5 + 0.3; r0 = 18; r1 = r0 + (40 + 18 * (i % 2)) * eout(u)
        d.line((cx + r0 * math.cos(ang), cy + r0 * math.sin(ang), cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)), fill=col + (255,), width=5)
def flash(can, t, t0, cx, cy):
    u = (t - t0) / 0.5
    if 0 <= u < 1:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); r = 40 + 120 * u
        ImageDraw.Draw(L).ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 190, 90, int(150 * (1 - u))))
        can.alpha_composite(L.filter(ImageFilter.GaussianBlur(18)))
def xmark(d, cx, cy, k, col=CH_R, s=34):
    if k <= 0: return
    p = partial([(cx - s, cy - s), (cx + s, cy + s)], clamp(k * 2)); cline(d, p, col, 7)
    if k > 0.5: cline(d, partial([(cx + s, cy - s), (cx - s, cy + s)], clamp(k * 2 - 1)), col, 7)
def cone(L, cx, cy, ang, spread, r, a, col=CH_Y):
    """translucent search sector of an escort"""
    pts = [(cx, cy)] + [(cx + r * math.cos(ang + s), cy + r * math.sin(ang + s)) for s in np.linspace(-spread, spread, 16)]
    S = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(S).polygon(pts, fill=col + (int(60 * a),)); L.alpha_composite(S)
    cdash(ImageDraw.Draw(L), pts[1:], col, 4, a, 10, 10)

# convoy layout on the floor
COLS = (390, 540, 690); ROWS = (730, 865, 1000, 1135)
SHIPS = [(x, y) for y in ROWS for x in COLS]
ESC0 = [(420, 590), (660, 590), (250, 935), (830, 935)]
ESC1 = [(300, 1300), (780, 1300), (440, 1450), (640, 1450)]
SUBP = [(615, 1560), (615, 1300), (615, 1068)]
HIT1 = (690, 1135); HIT2 = (390, 1135); SUBD = (600, 1355)

def convoy_board(t, T0):
    """the whole chalk drawing at time t (T0 = scene start)"""
    can = floor_bg().copy(); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    tw = {k: wt(*v) for k, v in {'ub': ('U-Boote', 55), 'hin': ('hinten', 55), 'inn': ('Inneren', 58), 'an': ('an', 60.5), 'tau': ('tauchten', 61),
                                 'beg': ('Begleitschiffe', 62), 'dar': ('Daraus', 65), 'geg': ('Gegenmaßnahme', 66), 'ang': ('Angriff', 68),
                                 'fie': ('fielen', 69), 'suc': ('suchten', 72), 'geb': ('Gebiet', 72), 'gel': ('Geleitzug', 74)}.items()}
    # convoy ships draw in one after another
    for i, (x, y) in enumerate(SHIPS):
        k = eio((t - T0 - 0.05 - i * 0.06) / 0.35)
        if k > 0: cline(d, partial(ship_pts(x, y), k), CHALK, 6)
    # escorts
    fb = eio((t - tw['fie']) / 2.4)
    for i, (p0, p1) in enumerate(zip(ESC0, ESC1)):
        k = eio((t - T0 - 0.6 - i * 0.08) / 0.35)
        if k <= 0: continue
        side = -1 if p0[0] < 540 else 1
        path = bez(p0, (p0[0] + side * 230, (p0[1] + p1[1]) / 2), p1, 30)
        if fb > 0:
            cdash(d, partial(path, fb), CH_Y, 3, 0.7, 10, 10)
            q = partial(path, fb)[-1]
        else: q = p0
        cline(d, partial(ship_pts(q[0], q[1], 84, 34), k), CH_Y, 6)
    # the U-boat: from behind, into the convoy, attacks, dives and stays behind
    t_ub = tw['ub']
    if t >= t_ub:
        if t < tw['hin'] - 0.2: pos = SUBP[0]
        elif t < tw['inn']: u = eio((t - tw['hin'] + 0.2) / 1.0); pos = (lerp(SUBP[0][0], SUBP[1][0], u), lerp(SUBP[0][1], SUBP[1][1], u))
        else: u = eio((t - tw['inn']) / 0.9); pos = (lerp(SUBP[1][0], SUBP[2][0], u), lerp(SUBP[1][1], SUBP[2][1], u))
        dv = clamp((t - tw['tau']) / 0.6); back = eio((t - tw['tau'] - 0.4) / 2.2)
        if dv > 0: pos = (lerp(SUBP[2][0], SUBD[0], back), lerp(SUBP[2][1], SUBD[1], back))
        k = eio((t - t_ub) / 0.5)
        found = t >= tw['gel']
        if found: sub_draw(d, *pos, CH_R, 1.0, 1.0)
        else: sub_draw(d, *pos, CH_R, lerp(1.0, 0.45, dv), k, dashed=dv > 0.5)
        if k >= 1 and dv < 1 and not found:
            put(L, sprite('U-BOOT', 'cond', 40, CH_R, False, 2), pos[0] + 92, pos[1] + 4, 1.0, 1 - dv)
        # dive ripples
        for j in range(3):
            u = (t - tw['tau'] - j * 0.35) / 1.4
            if 0 < u < 1: r = 20 + 80 * u; d.ellipse((SUBP[2][0] - r, SUBP[2][1] - r * 0.6, SUBP[2][0] + r, SUBP[2][1] + r * 0.6), outline=CHALK + (int(200 * (1 - u)),), width=3)
        # torpedo and hit
        ta = tw['an'] - 0.35
        if t >= ta:
            u = clamp((t - ta) / 0.35); cdash(d, partial([(SUBP[2][0] + 8, SUBP[2][1] - 30), (HIT1[0] - 12, HIT1[1] - 10)], u), CHALK, 3, 1.0, 8, 8)
        if t >= tw['an']: burst(d, *HIT1, (t - tw['an']) / 0.4); xmark(d, *HIT1, (t - tw['an'] - 0.3) / 0.5)
    # escorts look ahead (in the wrong place)
    ah = clamp((t - tw['beg']) / 0.5) * (1 - clamp((t - tw['dar']) / 0.5))
    if ah > 0:
        for i, (x, y) in enumerate(ESC0[:2]):
            sw = 0.5 * math.sin((t - tw['beg']) * 2.2 + i * 1.5)
            cone(L, x, y - 45, -math.pi / 2 + sw, 0.32, 95, ah)
        put(L, sprite('?', 'serif', 110, CH_Y, False), 540, 560, 1.0, ah)
    # second attack
    if t >= tw['ang']: burst(d, *HIT2, (t - tw['ang']) / 0.4); xmark(d, *HIT2, (t - tw['ang'] - 0.3) / 0.5)
    # search behind the convoy: hatched area + rotating sectors
    if t >= tw['suc']:
        k = eio((t - tw['suc']) / 1.6); x0, x1, y0, y1 = 200, 880, 1230, 1530
        A = Image.new('RGBA', (W, H), (0, 0, 0, 0)); da = ImageDraw.Draw(A)
        da.rectangle((x0, y0, lerp(x0, x1, k), y1), fill=CH_Y + (38,))
        for s in range(-400, 900, 34):
            xa, xb = x0 + s, x0 + s + (y1 - y0)
            seg = [(max(x0, xa), y1 - (max(x0, xa) - xa)), (min(lerp(x0, x1, k), xb), y1 - (min(lerp(x0, x1, k), xb) - xa))]
            if seg[1][0] > seg[0][0]: da.line(seg, fill=CH_Y + (110,), width=3)
        cdash(da, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], CH_Y, 4, k, 14, 10)
        L.alpha_composite(A)
        for i, (x, y) in enumerate(ESC1):
            cone(L, x, y + 35, math.pi / 2 + 0.6 * math.sin((t - tw['suc']) * 2.0 + i), 0.3, 100, k)
    if t >= tw['gel']:
        for j in range(2):
            u = ((t - tw['gel']) * 0.9 + j * 0.5) % 1.0
            r = 40 + 70 * u; d.ellipse((SUBD[0] - r, SUBD[1] - r, SUBD[0] + r, SUBD[1] + r), outline=CH_R + (int(230 * (1 - u)),), width=5)
    can.alpha_composite(chalkify(L))
    if t >= tw.get('an', 1e9): flash(can, t, tw['an'], *HIT1)
    if t >= tw['ang']: flash(can, t, tw['ang'], *HIT2)
    return can, tw

# ---------- scenes ----------
def sc_hook(t, w0, w1):
    c = pan_lin('j09', t, w0, w1, 1150, 1); can = shot(c, GRAD_SOFT)
    tK, tH, tT = wt('Kreide'), wt('Holzmodelle'), wt('Taktik')
    focus(can, t, 0.1, 'EIN FUSSBODEN', 'serif', 120, CREAM, 1060, t1=tK - 0.1)
    plate(can, t, wt('Liverpool') - 0.05, 'LIVERPOOL', 1190, size=62, bg=GOLD, fg=DEEP, t1=tK - 0.1)
    def chalk_arrow(L):
        k = eio((t - tK) / 0.55); tip = c.pt(1430, 1440)
        curved_arrow(L, t, tK + 0.05, (330, 1180), (300, 1420), (tip[0] - 40, tip[1] - 6), CHALK, 6)
        plate(L, t, tK, 'KREIDE', 1120, cx=330, size=56, bg=CREAM, fg=DEEP)
    if tK <= t < tH + 0.1: layer(can, fade_out(t, tH - 0.3), chalk_arrow)
    def model_arrow(L):
        tip = c.pt(1480, 1250)
        curved_arrow(L, t, tH + 0.05, (720, 1020), (760, 1240), (tip[0] + 30, tip[1] - 10), CH_Y, 6)
        plate(L, t, tH, 'HOLZMODELLE', 960, cx=700, size=52, bg=GOLD, fg=DEEP)
    if tH <= t < tT: layer(can, fade_out(t, tT - 0.4), model_arrow)
    reveal(can, t, tT - 0.05, 'EINE TAKTIK GEGEN', 'cond', 66, CREAM, 1060)
    focus(can, t, wt('U-Boote') - 0.05, 'DEUTSCHE U-BOOTE', 'serif', 120, GOLD, 1190)
    return can
def sc_name(t, w0, w1):
    can, pt = wide('j07', t, w0, w1, 1600, 1, hh=1200, yc=700); can.alpha_composite(GRAD_SOFT)
    focus(can, t, wt('Jean') - 0.04, 'JEAN', 'serif_i', 170, CREAM, 1220, dur=0.3)
    focus(can, t, wt('Laidlaw.') - 0.04, 'LAIDLAW', 'serif_i', 190, GOLD, 1400, dur=0.3); return can

def ship_icon(col, s=1.0):
    w, h = int(150 * s), int(60 * s); L = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.polygon([(10, 10 + h * 0.45), (w + 10, 10 + h * 0.45), (w - 10, h + 10), (30, h + 10)], fill=col + (255,))
    d.rectangle((w * 0.4, 10 + h * 0.1, w * 0.62, 10 + h * 0.45), fill=col + (255,)); d.rectangle((w * 0.47, 10, w * 0.53, 10 + h * 0.1), fill=col + (255,))
    return halo(L)
def halo(L, a=170, r=8):
    sh = Image.new('RGBA', (L.width + 40, L.height + 40), (0, 0, 0, 0)); m = L.getchannel('A')
    sh.paste(Image.new('RGBA', L.size, (4, 4, 6, a)), (20, 20), m); sh = sh.filter(ImageFilter.GaussianBlur(r)); sh.alpha_composite(L, (20, 20)); return sh
SHIP_C = ship_icon(CREAM, 0.8)
def sinking(can, t, t0, n, cy, gap=180, step=0.2):
    """ship icons in two rows, each one gets a red cross and settles lower, one after another"""
    for i in range(n):
        r, cidx = divmod(i, 4); x = 540 + (cidx - 1.5) * gap; y = cy + r * 120; ti = t0 + i * step
        if t < ti: break
        k = eout((t - ti) / 0.25); sk = eio((t - ti - 0.25) / 0.6)
        put(can, SHIP_C, x, y + 14 * sk, 1.0, k * (1 - 0.45 * sk))
        if sk > 0:
            L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); xmark(ImageDraw.Draw(L), x, y + 6, sk, RUST, 30); can.alpha_composite(L)
def sc_loss(t, w0, w1):
    can, pt = wide('j12', t, w0, w1, 1250, 1); can.alpha_composite(GRAD_SOFT)
    tA = wt('Atlantik')
    focus(can, t, wt('Anfang') - 0.05, 'ANFANG', 'cond', 80, CREAM, 1080, t1=tA - 0.3)
    digits(can, t, wt('1942') - 0.05, '1942', 1250, 260, step=0.15, t1=tA - 0.3)
    plate(can, t, tA - 0.05, 'NORDATLANTIK', 1110, size=60, bg=RUST, fg=CREAM)
    sinking(can, t, wt('Schiff') - 0.05, 8, 1260, step=0.11); return can

def sc_night(t, w0, w1):
    """night sea: a convoy steams on, ships explode, nobody sees where the attacks come from"""
    y = np.linspace(0, 1, H)[:, None]
    can = night_bg().copy()
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); dr = (t - w0) * 14
    for j in range(14):   # waves
        yy = 620 + j * 70 + ((t - w0) * 10) % 70; ph = j * 1.7
        pts = [(x, yy + 6 * math.sin(x / 70 + ph + (t - w0) * 0.8)) for x in range(0, W + 1, 30)]
        d.line(pts, fill=(120, 150, 180, 26), width=2)
    xs = (300, 420, 540, 660, 780); ys = (760, 880, 1000, 1120, 1240)
    hits = {(1, 3): wt('verstand') - 0.05, (3, 1): wt('genau') + 0.1, (0, 1): wt('U-Boote', 17) + 0.1, (4, 4): wt('Geleitzüge') + 0.2}
    for a, x in enumerate(xs):
        for b, y_ in enumerate(ys):
            yy = y_ - dr; th = hits.get((a, b))
            sunk = th is not None and t >= th
            col = (210, 214, 220, 230) if not sunk else (150, 60, 50, int(230 * (1 - clamp((t - th) / 2.5)) + 40))
            d.polygon(ship_pts(x, yy, 54, 20), fill=col)
    can.alpha_composite(L)
    for (a, b), th in hits.items():
        x, yy = xs[a], ys[b] - dr
        if t >= th: flash(can, t, th, x, yy)
        u = (t - th) / 0.9
        if 0 < u < 1: ring(can, x, yy, 20 + 90 * u, (255, 170, 80), 1 - u, 4)
    tq = wt('wie', 16.5)
    if t >= tq:
        k = eout((t - tq) / 0.35); put(can, sprite('?', 'serif', 300, GOLD), 540, 470 - (1 - k) * 30, lerp(1.3, 1.0, k), k)
    plate(can, t, wt('niemand') - 0.05, 'NIEMAND VERSTAND', 1420, size=58, bg=CREAM, fg=DEEP, t1=wt('U-Boote', 17) - 0.3)
    plate(can, t, wt('U-Boote', 17) - 0.05, 'WIE GREIFEN DIE U-BOOTE AN?', 1420, size=54, bg=RUST, fg=CREAM)
    return can
@functools.lru_cache(None)
def night_bg():
    y = np.linspace(0, 1, H)[:, None, None]
    a = np.array((12, 19, 30), np.float32) * (1 - y) + np.array((4, 7, 12), np.float32) * y
    a = np.repeat(a, W, 1) * (1 + (PAPER_TEX[..., None] - 1) * 0.15)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')

def sc_hall(t, w0, w1):
    can, pt = wide('j13', t, w0, w1, 1200, -1); can.alpha_composite(GRAD_SOFT)
    tP = wt('Problem')
    plate(can, t, wt('Liverpool', 20) - 0.05, 'LIVERPOOL', 1130, size=62, bg=GOLD, fg=DEEP)
    reveal(can, t, wt('kleine') - 0.05, 'EINE KLEINE EINHEIT', 'cond', 66, CREAM, 1260, t1=tP - 0.25)
    focus(can, t, tP - 0.05, 'DAS PROBLEM NACHSPIELEN', 'serif', 92, CREAM, 1300); return can
def sc_door(t, w0, w1):
    can, pt = wide('j10', t, w0, w1, 1213, 1); can.alpha_composite(GRAD_SOFT)
    tW = wt('Western')
    if t >= tW - 0.1:   # the painted letters light up
        for sx, sy, r in ((660, 800, 70), (900, 800, 70), (1510, 800, 70), (1750, 800, 70)):
            x, y = pt(sx, sy); ring(can, x, y, r * 0.75, GOLD, 0.8 * clamp((t - tW + 0.1) / 0.3), 4)
    for i, (word, key) in enumerate((('WESTERN', 'Western'), ('APPROACHES', 'Approaches'), ('TACTICAL', 'Tactical'), ('UNIT', 'Unit'))):
        ti = wt(key) - 0.05
        if t < ti: continue
        cy = 1000 + i * 120; k = eout((t - ti) / 0.3); size = 104
        f = FK['serif'](size); tw = f.getlength(word); x = 540 - tw / 2
        put(can, sprite(word[0], 'serif', size, GOLD), x + f.getlength(word[0]) / 2, cy, lerp(1.2, 1.0, k), k)
        rest = sprite(word[1:], 'serif', size, CREAM); put(can, rest, x + f.getlength(word[0]) + rest.width / 2 - 40, cy, 1.0, clamp((t - ti - 0.12) / 0.3))
    return can
def sc_roberts(t, w0, w1):
    can = shot(zoom_lin('j14', t, w0, w1, 740, 1000, 1.06))
    plate(can, t, wt('Kapitän') - 0.05, 'KAPITÄN', 1230, size=64, bg=CREAM, fg=DEEP)
    focus(can, t, wt('Gilbert') - 0.05, 'GILBERT ROBERTS', 'serif', 130, GOLD, 1380); return can
def sc_wrens(t, w0, w1):
    can, pt = wide('j05', t, w0, w1, 1250, 1); can.alpha_composite(GRAD_SOFT)
    tWr = wt('Wrens.')
    reveal(can, t, wt('Mitarbeiter') - 0.1, 'FAST ALLE MITARBEITER', 'cond', 66, CREAM, 1110)
    focus(can, t, wt('Frauen') - 0.05, 'FRAUEN', 'serif', 140, GOLD, 1250)
    plate(can, t, wt('Marinehelferinnendienstes,') - 0.05, "WOMEN'S ROYAL NAVAL SERVICE", 1400, size=48, bg=CREAM, fg=DEEP, t1=tWr - 0.25)
    plate(can, t, tWr - 0.05, 'DIE WRENS', 1400, size=66, bg=GOLD, fg=DEEP); return can
def sc_first(t, w0, w1):
    can = shot(pan_lin('j01', t, w0, w1, 760, 1)); t21 = wt('21') - 0.05; tS = wt('Schottin')
    plate(can, t, max(w0 + 0.3, wt('erste', 36) - 0.05), 'DIE ERSTE', 1110, size=58, bg=CREAM, fg=DEEP, t1=t21 - 0.3)
    focus(can, t, wt('Jean', 37) - 0.04, 'JEAN LAIDLAW', 'serif', 130, GOLD, 1250, t1=t21 - 0.3)
    digits(can, t, t21, '21', 1170, 300, step=0.15, t1=tS - 0.3)
    plate(can, t, wt('Jahre', 39) - 0.05, 'JAHRE ALT', 1380, size=60, bg=CREAM, fg=DEEP, t1=tS - 0.3)
    focus(can, t, tS - 0.05, 'SCHOTTIN', 'serif', 130, CREAM, 1200)
    plate(can, t, wt('ausgebildete') - 0.05, 'AUSGEBILDETE BUCHHALTERIN', 1360, size=54, bg=GOLD, fg=DEEP); return can
def sc_models(t, w0, w1):
    c = pan_lin('j04', t, w0, w1, 1200, -1, ); can = shot(c, GRAD_SOFT); tR = wt('Raster')
    if t >= tR - 0.05:   # chalk grid spreads over the table
        k = eio((t - tR + 0.05) / 0.8); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for x in range(60, W, 80): d.line((x, 1140, x, lerp(1140, 1560, k)), fill=CHALK + (120,), width=3)
        for y in range(1140, int(lerp(1140, 1560, k)) + 1, 80): d.line((40, y, W - 40, y), fill=CHALK + (120,), width=3)
        can.alpha_composite(chalkify(L, 0.5))
    plate(can, t, wt('Schiffsmodelle') - 0.05, 'SCHIFFSMODELLE', 760, size=64, bg=GOLD, fg=DEEP)
    reveal(can, t, tR - 0.1, 'AUF EINEM RASTER AM BODEN', 'cond', 60, CREAM, 880); return can
def sc_slit(t, w0, w1):
    c = pan_lin('j11', t, w0, w1, 1350, 1); can = shot(c); tS = wt('Schlitze')
    plate(can, t, wt('Offiziere') - 0.05, 'DIE OFFIZIERE', 1150, size=60, bg=CREAM, fg=DEEP, t1=tS - 0.3)
    reveal(can, t, wt('Spielfeld') - 0.1, 'SAHEN DAS SPIELFELD', 'cond', 66, CREAM, 1270, t1=tS - 0.3)
    if t >= tS - 0.1:   # the screen closes down to a narrow slit
        k = eio((t - tS + 0.1) / 0.6); y0, y1 = lerp(0, 830, k), lerp(H, 990, k)
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((0, y0, W, y1), fill=255); m = m.filter(ImageFilter.GaussianBlur(10))
        dark = Image.new('RGBA', (W, H), (10, 9, 8, 238)); dark.putalpha(Image.fromarray(255 - np.asarray(m)).point(lambda v: int(v * 0.93)))
        can.alpha_composite(dark)
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.line((0, y0, W, y0), fill=CREAM + (int(120 * k),), width=2); d.line((0, y1, W, y1), fill=CREAM + (int(120 * k),), width=2); can.alpha_composite(L)
        focus(can, t, tS - 0.05, 'NUR DURCH SCHLITZE', 'serif', 110, GOLD, 1180)
        reveal(can, t, wt('wie', 51) - 0.1, 'WIE EIN KOMMANDANT AUF SEE', 'cond', 62, CREAM, 1320)
    return can
def sc_muster(t, w0, w1):
    can = shot(pan_lin('j02', t, w0, w1, 900, -1, 1200))
    reveal(can, t, wt('Spiele') - 0.1, 'DIE SPIELE ZEIGTEN', 'cond', 70, CREAM, 1220)
    focus(can, t, wt('Muster.') - 0.05, 'EIN MUSTER', 'serif', 150, GOLD, 1370); return can

def sc_chalk(t, w0, w1):
    can, tw = convoy_board(t, w0)
    LAB = [(tw['ub'] - 0.05, 'DIE U-BOOTE', CREAM), (tw['hin'] - 0.05, 'GREIFEN VON HINTEN AN', GOLD), (tw['inn'] - 0.05, 'ODER AUS DEM INNEREN', GOLD),
           (tw['tau'] - 0.05, 'UND TAUCHEN AB', CREAM), (tw['beg'] - 0.05, 'BEGLEITSCHIFFE SUCHEN VORNE', CREAM),
           (tw['geg'] - 0.05, 'GEGENMASSNAHME', GOLD), (tw['fie'] - 0.05, 'ALLE FALLEN ZURÜCK', CREAM), (tw['suc'] - 0.05, 'UND SUCHEN HINTEN AB', GOLD)]
    for i, (ti, txt, col) in enumerate(LAB):
        t1 = LAB[i + 1][0] - 0.3 if i + 1 < len(LAB) else None
        if txt == 'GEGENMASSNAHME': cascade(can, t, ti, txt, 'serif', 110, col, 400, t1=t1)
        else: focus(can, t, ti, txt, 'serif', 84, col, 400, t1=t1, dur=0.35)
    return can
def sc_rasp(t, w0, w1):
    can, pt = wide('j06', t, w0, w1, 1200, -1); can.alpha_composite(GRAD_SOFT); tR = wt('Raspberry,')
    reveal(can, t, wt('Namen') - 0.1, 'DEN NAMEN GAB SIE SELBST', 'cond', 66, CREAM, 1180, t1=tR - 0.3)
    seal(can, t, tR - 0.05, 'RASPBERRY', 540, 1130, r=180, col=RUST, rot=-8)
    plate(can, t, wt('englischen') - 0.05, 'NACH EINER ENGLISCHEN SPOTTGESTE', 1430, size=46, bg=CREAM, fg=DEEP); return can
def sc_noble(t, w0, w1):
    can = shot(zoom_lin('j15', t, w0, w1, 760, 1000, 1.06))
    plate(can, t, wt('Admiral') - 0.05, 'ADMIRAL', 1110, size=64, bg=CREAM, fg=DEEP)
    focus(can, t, wt('Percy') - 0.05, 'PERCY NOBLE', 'serif', 140, GOLD, 1250)
    typewriter(can, t, wt('sofort') - 0.1, 'SOFORT AN DIE FLOTTE', 1420); return can

def officer(col, s=60):
    L = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse((s * 0.32, s * 0.2, s * 0.68, s * 0.56), fill=col); d.rectangle((s * 0.26, s * 0.12, s * 0.74, s * 0.24), fill=col)
    d.pieslice((s * 0.08, s * 0.6, s * 0.92, s * 1.4), 180, 360, fill=col); return halo(L, 150, 5)
OFF_C = officer(CREAM + (255,)); OFF_G = officer(GOLD + (255,))
@functools.lru_cache(None)
def navy_bg():
    a = np.ones((H, W, 3), np.float32) * np.array((14, 20, 30), np.float32)
    a *= (1 + (PAPER_TEX[..., None] - 1) * 0.25)
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA'); im.alpha_composite(VIG); return im
def sc_5000(t, w0, w1):
    can = navy_bg().copy(); tN = wt('5.000') - 0.05
    focus(can, t, wt('Kriegsende') - 0.05, 'BIS KRIEGSENDE', 'serif', 100, CREAM, 470)
    if t >= tN:
        v = int(round(5000 * eout((t - tN) / 1.4) / 50)) * 50; s = f'{v:,}'.replace(',', '.')
        put(can, sprite(s, 'serif_i', 260, GOLD), 540, 700, 1.0, clamp((t - tN) / 0.2))
    n = 50
    for i in range(n):
        ti = tN + i * 1.4 / n
        if t < ti: break
        r, c = divmod(i, 10); k = eout((t - ti) / 0.2)
        put(can, OFF_G if i == n - 1 else OFF_C, 540 + (c - 4.5) * 84, 930 + r * 92 - (1 - k) * 20, 1.0, k)
    plate(can, t, wt('Marineoffiziere') - 0.05, 'MARINEOFFIZIERE AUSGEBILDET', 1440, size=54, bg=CREAM, fg=DEEP); return can
def sc_award(t, w0, w1):
    can, pt = wide('j08', t, w0, w1, 1180, 1); can.alpha_composite(GRAD_SOFT); tF = wt('Frauen', 95)
    def rob(L):
        tip = pt(1160, 850)
        curved_arrow(L, t, wt('Roberts', 92) + 0.05, (540, 1180), (600, 1000), (tip[0], tip[1] + 30), GOLD, 7)
        plate(L, t, wt('Roberts', 92) - 0.05, 'GILBERT ROBERTS', 1240, size=58, bg=GOLD, fg=DEEP)
        plate(L, t, wt('ausgezeichnet,') - 0.05, 'AUSGEZEICHNET', 1350, size=54, bg=CREAM, fg=DEEP)
    layer(can, fade_out(t, tF - 0.3), rob)
    if t >= tF - 0.05:
        for i, (sx, sy) in enumerate(((560, 787), (827, 773), (1433, 773), (1687, 753), (547, 573), (800, 553), (1367, 560), (1573, 560), (1827, 553))):
            x, y = pt(sx, sy); k = eout((t - tF - i * 0.06) / 0.35); ring(can, x, y, 52 * k, CREAM, 0.85 * k, 4)
        focus(can, t, tF - 0.05, 'DIE FRAUEN', 'serif', 110, CREAM, 1220)
        plate(can, t, wt('keine', 96) - 0.05, 'KEINE OFFIZIELLE ANERKENNUNG', 1360, size=52, bg=RUST, fg=CREAM)
    return can
def sc_later(t, w0, w1):
    can, pt = wide('j03', t, w0, w1, 1420, 1, hh=1060, yc=820); can.alpha_composite(GRAD_SOFT); t08 = wt('2008.') - 0.05
    reveal(can, t, wt('Krieg', 100) - 0.1, 'NACH DEM KRIEG', 'cond', 66, CREAM, 1200)
    plate(can, t, wt('Beruf') - 0.05, 'ZURÜCK IN DEN BERUF', 1320, size=56, bg=GOLD, fg=DEEP)
    focus(can, t, t08, '† 2008', 'serif', 120, CREAM, 1450); return can
def sc_end(t, w0, w1):
    # back on the game floor: the finished Raspberry drawing, quieter
    can, _ = convoy_board(wt('Geleitzug', 74) + 1.5 + (t - w0) * 0.3, 55.67); dim(can, 120)
    focus(can, t, wt('Kanntet'), 'KANNTET IHR', 'serif', 120, CREAM, 1180)
    focus(can, t, wt('diese', 104), 'DIESE GESCHICHTE?', 'serif', 120, GOLD, 1320)
    plate(can, t, wt('Schreibt'), 'SCHREIBT ES IN DIE KOMMENTARE!', 1450, size=46); return can

def st(s, after=0.0): return wt(s, after) - 0.15
SCN = [(0.0, sc_hook, 'cut'), (st('Jean'), sc_name, 'flash'), (st('Anfang'), sc_loss, 'dip'), (st('und', 15.3), sc_night, 'fade'),
       (st('In', 20), sc_hall, 'dip'), (st('die', 24.8), sc_door, 'fade'), (wt('Kapitän') - 0.12, sc_roberts, 'slide_l'),
       (st('Fast'), sc_wrens, 'fade'), (wt('erste', 36) + 0.3, sc_first, 'fade'), (st('Nun'), sc_models, 'slide_r'),
       (st('Offiziere') - 0.3, sc_slit, 'fade'), (st('Die', 53.5), sc_muster, 'fade'), (st('Die', 55.7), sc_chalk, 'dip'),
       (st('Den', 75.6), sc_rasp, 'flash'), (st('Admiral'), sc_noble, 'slide_l'), (st('Bis'), sc_5000, 'dip'),
       (st('Roberts', 92), sc_award, 'fade'), (st('Jean', 98), sc_later, 'fade'), (st('Kanntet'), sc_end, 'dip')]
OV = 0.22
SC = []
for i, (t0, fn, tr) in enumerate(SCN):
    s = 0.0 if i == 0 else t0 - OV
    e = TEND if i == len(SCN) - 1 else SCN[i + 1][0] + OV
    SC.append((s, e, fn, tr))

DIPC = Image.new('RGBA', (W, H), (4, 6, 8, 255)); FLASHC = Image.new('RGBA', (W, H), (250, 244, 225, 255))
def run(sc, t): return sc[2](t, sc[0], sc[1])
def frame(t):
    act = [s for s in SC if s[0] <= t < s[1]] or [SC[-1]]
    if len(act) == 1: img = run(act[0], t)
    else:
        a, b = act[0], act[1]; u = ease((t - b[0]) / (a[1] - b[0])); tr = b[3]
        if tr in ('slide_l', 'slide_r'):
            A = run(a, t); B_ = run(b, t); s = 1 if tr == 'slide_l' else -1; off = int(W * u)
            img = Image.new('RGBA', (W, H), (0, 0, 0, 255)); img.paste(A, (-s * off, 0)); img.paste(B_, (s * (W - off), 0))
        elif tr == 'dip':
            img = Image.blend(run(a, t), DIPC, min(1, u * 2)) if u < 0.5 else Image.blend(DIPC, run(b, t), (u - 0.5) * 2)
        elif tr == 'flash':
            img = Image.blend(run(a, t), FLASHC, min(1, u * 2) * 0.75) if u < 0.5 else Image.blend(FLASHC, run(b, t), 0.25 + 0.75 * (u - 0.5) * 2)
        else: img = Image.blend(run(a, t), run(b, t), u)
    img.alpha_composite(VIG)
    if t > TEND - 0.6: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * clamp((t - TEND + 0.6) / 0.5)))))
    return img.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; ims = [ui_overlay(frame(t)).resize((270, 480)) for t in ts]
        cols = 6; rows = (len(ims) + cols - 1) // cols; Sh = Image.new('RGB', (270 * cols, 480 * rows))
        for i, im in enumerate(ims):
            Sh.paste(im, ((i % cols) * 270, (i // cols) * 480)); ImageDraw.Draw(Sh).text(((i % cols) * 270 + 4, (i // cols) * 480 + 4), f'{ts[i]}', fill=(0, 255, 0))
        Sh.save(B + sys.argv[2], quality=90)
    elif sys.argv[1] == 'still':
        frame(float(sys.argv[3])).save(B + sys.argv[2], quality=90)
    else:
        out = sys.argv[2]; a, b = float(sys.argv[3]), float(sys.argv[4])
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
        for n in range(int(round(a * FPS)), int(round(b * FPS))):
            p.stdin.write(grain(frame(n / FPS), n).tobytes())
        p.stdin.close(); p.wait(); print('rc', p.returncode)
