# Erich Hartmann, vertical 9:16 documentary: tightened voice, every scene on its sentence, text clear of the Shorts/Reels UI,
# new animations (jet streak, pin drop, glider, progress bar, loop, fuel gauge, range ruler, bar chart, radio waves, method cycle,
# award stairs, diamond grid, cell, verdict timeline, Starfighter, logbook, loss lists, number compare, book), ends after the comment call
import sys, subprocess, re
from lib9 import *
from lib9 import _bg

S_ = []                                                     # sentence start times
_c = []
for w_, a_, b_ in WORDS:
    _c.append(a_)
    if w_[-1] in '.!?' and not re.fullmatch(r'\d+\.', w_): S_.append(_c[0]); _c = []
def ss(i): return S_[i]
def w(s, after=0.0): return wt(s, after)
INK_ = (40, 32, 24); OR = (232, 140, 40)
_rr = np.random.default_rng(9)
_n = Image.fromarray((_rr.normal(128, 30, (H // 6, W // 6))).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(4))
_yy, _xx = np.mgrid[0:H, 0:W]; _rad = np.sqrt(((_xx - W / 2) / (W * 0.6)) ** 2 + ((_yy - H / 2) / (H * 0.6)) ** 2)
_a = np.ones((H, W, 3)) * np.array(DARK, float) * (1 + 0.9 * np.clip(1 - _rad, 0, 1))[..., None] * (0.92 + 0.08 * np.asarray(_n)[..., None] / 128)
PLAIN = Image.fromarray(_a.clip(0, 255).astype(np.uint8)).convert('RGBA')
# second background: cool steel-blue night sky with a faint horizon glow (for flight animations)
_s = np.ones((H, W, 3)) * np.array((10, 16, 26), float); _s += (np.clip(1 - np.abs(_yy - 1250) / 600, 0, 1) ** 2 * 28)[..., None] * np.array((1.0, 0.8, 0.6))
_s *= (0.94 + 0.06 * np.asarray(_n)[..., None] / 128)
SKY = Image.fromarray(_s.clip(0, 255).astype(np.uint8)).convert('RGBA')
def plain(): return PLAIN.copy()
def sky(): return SKY.copy()
def L_(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def poly(can, pts, col, a=255, w_=6, closed=False):
    L = L_(); d = ImageDraw.Draw(L); P = pts + [pts[0]] if closed else pts
    d.line(P, fill=(0, 0, 0, int(a * 0.55)), width=w_ + 6, joint='curve'); d.line(P, fill=col + (int(a),), width=w_, joint='curve'); can.alpha_composite(L)
def partial(pts, u):
    if u <= 0: return pts[:1]
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = sum(seg); g = tot * clamp(u); out = [pts[0]]; acc = 0
    for i, s_ in enumerate(seg):
        if acc + s_ >= g: f = (g - acc) / s_ if s_ else 0; out.append((lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f))); return out
        out.append(pts[i + 1]); acc += s_
    return out
def plane_icon(s=70, col=WHITE, jet=False):
    """top-down aircraft pointing right"""
    L = Image.new('RGBA', (s * 2, s * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = s
    d.polygon([(c - s * 0.75, c - s * 0.07), (c + s * 0.8, c - s * 0.07), (c + s * 0.95, c), (c + s * 0.8, c + s * 0.07), (c - s * 0.75, c + s * 0.07)], fill=col + (255,))
    if jet: d.polygon([(c + s * 0.1, c), (c - s * 0.35, c - s * 0.6), (c - s * 0.5, c - s * 0.6), (c - s * 0.25, c), (c - s * 0.5, c + s * 0.6), (c - s * 0.35, c + s * 0.6)], fill=col + (255,))
    else: d.rectangle((c + s * 0.05, c - s * 0.75, c + s * 0.3, c + s * 0.75), fill=col + (255,))
    d.polygon([(c - s * 0.75, c - s * 0.28), (c - s * 0.6, c - s * 0.28), (c - s * 0.55, c + s * 0.28), (c - s * 0.75, c + s * 0.28)], fill=col + (255,))
    return L
def put_icon(can, L, x, y, ang=0.0, a=1.0, sc=1.0):
    if a <= 0.01: return
    if ang: L = L.rotate(-math.degrees(ang), resample=Image.BICUBIC)
    if sc != 1: L = L.resize((max(1, int(L.width * sc)), max(1, int(L.height * sc))), Image.BICUBIC)
    if a < 1: L = L.copy(); L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), (0, 0), L.getchannel('A')); sh = sh.filter(ImageFilter.GaussianBlur(5))
    can.alpha_composite(sh, (int(x - L.width / 2 + 3), int(y - L.height / 2 + 6))); can.alpha_composite(L, (int(x - L.width / 2), int(y - L.height / 2)))
def point_at(can, t, t0, tip, lab, tail=None):
    """yellow arrow from free space to a person or object, short label under its tail"""
    side = -1 if tip[0] > CX else 1
    tail = tail or (min(860, max(200, tip[0] + side * 230)), tip[1] + 300)
    arrow(can, tail, (tip[0] + side * 20, tip[1] + 50), eio((t - t0) / 0.6), YEL, 13, 42)
    label(can, t, t0 + 0.4, tail[0], tail[1] + 50, lab, 60, YEL, 'mm')
def fitpt(n, t, w0, w1, z1, sx, sy):
    im = src(n); u = clamp((t - w0) / (w1 - w0)); z = lerp(1.0, z1, u); pw = im.width * H / im.height
    cw, ch = im.width / z, im.height / z; x0 = (W - pw) / 2
    return (x0 + (sx - (im.width / 2 - cw / 2)) * pw / cw, (sy - (im.height / 2 - ch / 2)) * H / ch)
def photo(n, t, w0, w1, d=1, cy=0.42, zoom=1.04):
    """full-screen 9:16 photo: portrait photos zoom slowly (fit), landscape photos pan at constant speed"""
    im = src(n)
    if im.width / im.height < 0.8: return fit(n, t, w0, w1, zoom)
    return pan(n, t, w0, w1, d, cy, zoom)
def sh(can, a=225, start=0.5): return shade(can, a, start)
def line_draw(can, t, t0, pts, col=YEL, wd=6, dur=0.8):
    if t < t0: return
    poly(can, partial(pts, eio((t - t0) / dur)), col, 255, wd)
def bar(can, x0, y0, x1, y1, col, a=255): L = L_(); ImageDraw.Draw(L).rectangle((x0, y0, x1, y1), fill=col + (int(a),)); can.alpha_composite(L)
def glow_dot(can, x, y, col=YEL, r=12, a=1.0): dot(can, x, y, col, r, a)

# ================= intro =================
def s_352(t, w0, w1):
    can = sh(photo('h22', t, w0, w1), 230, 0.42); t0 = w('352') - 0.1
    if t >= t0:
        v = int(round(352 * eout((t - t0) / 1.1))); f = anton(300)
        shadowed(can, lambda d: d.text((CX, 1120), str(v), font=f, fill=YEL + (255,), anchor='mm'))
    txt(can, t, w('Luftsiege'), (CX, Y2 + 40), 'LUFTSIEGE', anton(96), WHITE)
    txt(can, t, w('zugeschrieben.') - 0.05, (CX, Y3 + 40), 'ZUGESCHRIEBEN', bebas(60), CREAM); return can
def s_haft(t, w0, w1):
    can = sh(photo('h45', t, w0, w1, 1, 0.45, 1.05), 230, 0.45)
    txt(can, t, w('sowjetisches'), (CX, Y1), 'EIN SOWJETISCHES GERICHT', bebas(66), CREAM)
    t25 = w('25')
    if t >= t25:   # bars of a cell slide in behind the number
        k = eout((t - t25) / 0.5); L = L_(); d = ImageDraw.Draw(L)
        for i in range(5): x = CX - 260 + i * 130; d.rectangle((x - 6, Y2 - 120 * k, x + 6, Y2 + 120 * k), fill=(30, 30, 34, int(200 * k)))
        can.alpha_composite(L)
    txt(can, t, t25 - 0.05, (CX, Y2 + 10), '25 JAHRE HAFT', anton(120), RED); return can
def s_jet(t, w0, w1):        # a jet streaks across the night sky, contrail stays
    can = sky(); u = clamp((t - w0 - 0.2) / max(1.0, w1 - w0 - 0.6)); x = lerp(-150, W + 150, eio(u)); y = lerp(1000, 700, eio(u))
    L = L_(); d = ImageDraw.Draw(L)
    for i in range(40):
        q = (i / 40); xx = lerp(-150, x, q); yy = lerp(1000, y, q); a = int(120 * q)
        d.ellipse((xx - 14 * q, yy - 14 * q, xx + 14 * q, yy + 14 * q), fill=(220, 225, 235, a))
    can.alpha_composite(L.filter(ImageFilter.GaussianBlur(6)))
    if 0 < u < 1: put_icon(can, plane_icon(80, WHITE, True), x, y, math.atan2(-300, W + 300))
    txt(can, t, w('später', 7), (CX, YT + 40), 'UND SPÄTER', bebas(64), CREAM)
    txt(can, t, w('Düsenjagdgeschwader'), (CX, Y2), 'DAS ERSTE DÜSENJAGDGESCHWADER', anton(84), WHITE)
    txt(can, t, w('Bundeswehr.') - 0.05, (CX, Y3 + 10), 'DER BUNDESWEHR', anton(96), YEL); return can
def s_name(t, w0, w1):
    can = sh(photo('h17', t, w0, w1, 1, 0.45, 1.05), 235, 0.45)
    words(can, t, [('ERICH', WHITE, w('Erich') - 0.05), ('HARTMANN', YEL, w('Hartmann.') - 0.05)], Y2, 140)
    if t > w('Hartmann.') + 0.2:
        k = eio((t - w('Hartmann.') - 0.2) / 0.5); L = L_(); ImageDraw.Draw(L).line((CX - 330 * k, Y2 + 95, CX + 330 * k, Y2 + 95), fill=YEL + (255,), width=6); can.alpha_composite(L)
    return can

# ================= chapter 1 =================
DE = Map(10.4, 50.2, 10.5, hi=('Germany',))
def s_born(t, w0, w1):       # pin drops on Weissach
    z = lerp(1.0, 1.12, eio((t - w0) / (w1 - w0))); can = DE.frame(z)
    chapter(can, t, w0 + 0.3, 1, 'KINDHEIT ZWISCHEN CHINA UND SCHWABEN', w0 + 3.3)
    x, y = DE.p(8.93, 48.85, z); tp = w('Weissach') - 0.25
    label(can, t, w0 + 0.5, *DE.p(10.4, 51.3, z), 'DEUTSCHLAND', 76, CREAM, 'mm')
    if t >= tp:
        k = eout((t - tp) / 0.45); yy = y - (1 - k) * 220
        for j in range(2):
            u = ((t - tp - 0.45) * 0.8 + j * 0.5) % 1.0
            if t > tp + 0.45: L = L_(); r = 18 + 80 * u; ImageDraw.Draw(L).ellipse((x - r, y - r * 0.5, x + r, y + r * 0.5), outline=YEL + (int(200 * (1 - u)),), width=4); can.alpha_composite(L)
        L = L_(); d = ImageDraw.Draw(L); d.polygon([(x, yy), (x - 24, yy - 50), (x + 24, yy - 50)], fill=RED + (255,)); d.ellipse((x - 26, yy - 96, x + 26, yy - 44), fill=RED + (255,)); d.ellipse((x - 10, yy - 80, x + 10, yy - 60), fill=WHITE + (255,)); can.alpha_composite(L)
        label(can, t, tp + 0.3, x + 40, y - 70, 'WEISSACH', 68, YEL)
    typewriter(can, t, w('April') - 0.05, (CX, 640), 'APRIL 1922', typew(76), CREAM, 0.07)
    txt(can, t, w('Württemberg'), (CX, Y3 + 10), 'WÜRTTEMBERG', anton(84), YEL); return can
def s_parents(t, w0, w1):
    can = sh(photo('h11', t, w0, w1), 230, 0.55)
    point_at(can, t, w('Vater') - 0.05, fitpt('h11', t, w0, w1, 1.04, 330, 760), 'VATER: ARZT', (300, 1250))
    point_at(can, t, w('Mutter', 21) - 0.05, fitpt('h11', t, w0, w1, 1.04, 700, 470), 'MUTTER: SEGELFLIEGERIN', (640, 1420)); return can
CHINA = Map(61.0, 40.0, 130.0, hi=('China', 'Germany'))
def s_china(t, w0, w1):
    can = sh(photo('h13', t, w0, w1, 1, 0.5, 1.03), 220, 0.5)
    txt(can, t, w('Wirtschaftslage') - 0.1, (CX, Y1), 'WIRTSCHAFTSKRISE', bebas(64), CREAM)
    txt(can, t, w('China') - 0.05, (CX, Y2 + 10), 'NACH CHINA', anton(110), YEL)
    txt(can, t, w('aufwuchs') - 0.1, (CX, Y3 + 20), 'HIER WUCHS ERICH AUF', bebas(60), WHITE); return can
def s_back(t, w0, w1):      # long way home from Changsha to Germany, a glowing line with a travelling dot
    z = 1.0; can = CHINA.frame(z); a = CHINA.p(112.9, 28.2); b = CHINA.p(9.2, 48.8)
    pts = route([(112.9, 28.2), (88.0, 42.0), (60.0, 50.0), (35.0, 52.0), (9.2, 48.8)], CHINA)
    glow_dot(can, *a, RED, 12); label(can, t, w0 + 0.2, a[0] - 20, a[1] + 50, 'CHANGSHA', 54, RED, 'rm')
    txt(can, t, w('1928') - 0.05, (CX, YT), '1928: BÜRGERKRIEG', anton(80), RED)
    u = eio((t - w('Deutschland', 30) + 0.4) / 2.0)
    if u > 0:
        pp = partial(pts, u); poly(can, pp, YEL, 255, 6); glow_dot(can, *pp[-1], YEL, 10)
    if u >= 1: glow_dot(can, *b, YEL, 12); label(can, t, w('Deutschland', 30) + 1.6, b[0] + 20, b[1] - 50, 'DEUTSCHLAND', 54, YEL)
    txt(can, t, w('zurückkehrte.') - 0.1, (CX, Y3 + 10), 'RÜCKKEHR NACH DEUTSCHLAND', anton(76), WHITE); return can
def glider(s=110, col=WHITE):
    L = Image.new('RGBA', (s * 2, s), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = s
    d.polygon([(c - s * 0.9, s * 0.45), (c + s * 0.9, s * 0.45), (c + s * 0.9, s * 0.52), (c - s * 0.9, s * 0.52)], fill=col + (255,))
    d.polygon([(c - s * 0.08, s * 0.3), (c + s * 0.08, s * 0.3), (c + s * 0.04, s * 0.95), (c - s * 0.04, s * 0.95)], fill=col + (255,))
    d.polygon([(c - s * 0.25, s * 0.9), (c + s * 0.25, s * 0.9), (c + s * 0.25, s * 0.95), (c - s * 0.25, s * 0.95)], fill=col + (255,)); return L
def s_glider(t, w0, w1):    # a glider drifts down across the photo, thin trail
    can = sh(photo('h14', t, w0, w1, 1, 0.4, 1.05), 230, 0.5); tg = w('Fliegen') - 0.2
    if t >= tg:
        u = clamp((t - tg) / (w1 - tg)); x = lerp(120, 940, u); y = 520 + 60 * math.sin(u * 6)
        trail = [(lerp(120, 940, v), 520 + 60 * math.sin(v * 6) + 25) for v in np.linspace(0, u, 40)]
        poly(can, trail, CREAM, 120, 2); put_icon(can, glider(), x, y, 0.08 * math.cos(u * 6), clamp((t - tg) / 0.3))
    txt(can, t, w('Mutter', 35) - 0.05, (CX, Y1), 'DIE MUTTER LEHRT IHN FLIEGEN', bebas(64), CREAM)
    txt(can, t, w('14') - 0.05, (CX, Y2 + 20), 'MIT 14 JAHREN', anton(110), YEL)
    txt(can, t, w('Segelflugunterricht.') - 0.1, (CX, Y3 + 30), 'GIBT ER SELBST SEGELFLUGUNTERRICHT', bebas(58), WHITE); return can
def s_lw(t, w0, w1):
    can = sh(photo('h16', t, w0, w1, 1, 0.4, 1.04))
    txt(can, t, w('Abitur'), (CX, Y1), 'NACH DEM ABITUR', bebas(64), CREAM)
    typewriter(can, t, w('Oktober', 42) - 0.05, (CX, Y2), 'OKTOBER 1940', typew(76), CREAM, 0.07)
    txt(can, t, w('Luftwaffe') - 0.05, (CX, Y3 + 20), 'EINTRITT IN DIE LUFTWAFFE', anton(84), YEL); return can

# ================= chapter 2 =================
def s_train(t, w0, w1):     # a progress bar fills almost two years of training
    can = sh(photo('h03', t, w0, w1, 1, 0.4, 1.05), 235, 0.45)
    chapter(can, t, w0 + 0.3, 2, 'AUSBILDUNG UND ERSTE EINSÄTZE', w0 + 3.3)
    tb = w('dauerte') - 0.1
    if t >= tb:
        k = eio((t - tb) / 1.6); x0, x1, y = 160, 880, Y1 + 20
        bar(can, x0, y - 14, x1, y + 14, (40, 44, 52), 230); bar(can, x0, y - 14, lerp(x0, x1 - 40, k), y + 14, YEL)
        label(can, t, tb, x0, y - 60, '1940', 50, CREAM, 'lm'); label(can, t, tb + 1.4, x1, y - 60, '1942', 50, CREAM, 'rm')
    txt(can, t, w('zwei', 46) - 0.05, (CX, Y2 + 30), 'FAST ZWEI JAHRE', anton(100), WHITE)
    txt(can, t, w('Rückschlag.') - 0.1, (CX, Y3 + 30), 'UND EIN RÜCKSCHLAG', bebas(64), RED); return can
def s_loop(t, w0, w1):      # forbidden aerobatics: the aircraft draws a loop and a roll
    can = sky(); t0 = w('Kunstflugfiguren') - 0.9
    pts = [(80, 1100), (300, 1080), (520, 1000), (640, 860), (620, 700), (520, 620), (400, 660), (360, 800), (440, 940), (620, 1010), (820, 1000), (1000, 940)]
    pp = route([(p[0], p[1]) for p in pts], type('M', (), {'p': staticmethod(lambda x, y, z=1: (x, y))})(), 1.0, 10)
    u = eio((t - t0) / 2.4)
    if u > 0:
        q = partial(pp, u); poly(can, q, CREAM, 150, 4)
        if len(q) > 1 and u < 1: put_icon(can, plane_icon(54), *q[-1], math.atan2(q[-1][1] - q[-2][1], q[-1][0] - q[-2][0]))
    typewriter(can, t, w('März', 52) - 0.05, (CX, YT), 'MÄRZ 1942', typew(76), CREAM, 0.07)
    txt(can, t, w('verbotene') - 0.05, (CX, Y2 + 60), 'VERBOTENER KUNSTFLUG', anton(84), WHITE)
    stamp(can, t, w('bestraft.') - 0.05, 'BESTRAFT', (CX + 60, Y3 + 30), RED, 80, -8); return can
def s_crash1(t, w0, w1):
    can = dim(sh(photo('h44', t, w0, w1, -1, 0.5, 1.03), 230, 0.5), 40)
    txt(can, t, w('Kamerad'), (CX, Y1), 'EIN KAMERAD FLIEGT FÜR IHN', bebas(64), CREAM)
    txt(can, t, w('starb') - 0.05, (CX, Y2 + 20), 'UND STIRBT', anton(110), RED)
    txt(can, t, w('Bruchlandung.') - 0.1, (CX, Y3 + 30), 'BEI EINER BRUCHLANDUNG', bebas(60), WHITE); return can
EAST = Map(36.0, 50.5, 26.0, hi=('Russia',))
FRONT42 = [(30.3, 59.9), (33.5, 57.5), (34.5, 55.0), (37.5, 53.0), (39.2, 51.7), (40.5, 50.0), (43.0, 49.0), (44.5, 48.7), (45.5, 46.5), (44.0, 44.5), (42.0, 43.4)]
def s_ostfront(t, w0, w1):
    z = lerp(1.0, 1.08, eio((t - w0) / (w1 - w0))); can = EAST.frame(z)
    typewriter(can, t, w('Herbst') - 0.05, (CX, YT), 'HERBST 1942', typew(76), CREAM, 0.07)
    line_draw(can, t, w('Ostfront.') - 0.6, [EAST.p(*q, z) for q in FRONT42], RED, 8, 1.4)
    label(can, t, w('Ostfront.') + 0.3, *EAST.p(41.5, 56.5, z), 'OSTFRONT', 76, RED, 'mm')
    x, y = EAST.p(40.1, 44.6, z)
    if t > w('Jagdgeschwader') - 0.1: glow_dot(can, x, y, YEL, 13); label(can, t, w('Jagdgeschwader') - 0.1, x - 30, y + 10, 'JG 52', 70, YEL, 'rm')
    txt(can, t, w('Jagdgeschwader') - 0.1, (CX, Y3 + 20), 'JAGDGESCHWADER 52', anton(84), YEL); return can
def s_fuel(t, w0, w1):      # first mission: separated from the leader, the fuel needle falls to zero
    can = sky(); tl = w('gelöst') - 0.3
    a = eio((t - w0) / 1.0)
    if a > 0:   # leader and wingman part ways
        u = clamp((t - tl) / 2.0)
        put_icon(can, plane_icon(46), lerp(200, 420, a) + u * 300, 600 - u * 120, -0.35 * u, 1.0)
        put_icon(can, plane_icon(46, YEL), lerp(150, 340, a) + u * 120, 700 + u * 160, 0.4 * u, 1.0)
        label(can, t, tl + 0.6, 760, 470, 'ROTTENFÜHRER', 44, CREAM, 'mm')
    cx, cy, r = CX, 1060, 190; tf = w('Treibstoff') - 0.6
    L = L_(); d = ImageDraw.Draw(L); d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(18, 22, 30, 230), outline=CREAM + (220,), width=6)
    for i in range(11):
        ang = math.radians(210 - i * 24); d.line((cx + (r - 30) * math.cos(ang), cy - (r - 30) * math.sin(ang), cx + (r - 10) * math.cos(ang), cy - (r - 10) * math.sin(ang)), fill=CREAM + (220,), width=4)
    d.arc((cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18), 120, 150, fill=RED + (255,), width=10); can.alpha_composite(L)
    label(can, t, w0, cx - 130, cy + 110, '0', 50, RED, 'mm'); label(can, t, w0, cx + 130, cy + 110, 'VOLL', 40, CREAM, 'mm')
    v = 1 - eio((t - tf) / 1.8) * 0.98 if t > tf else 0.75 - 0.25 * clamp((t - w0) / (tf - w0 + 0.01))
    ang = math.radians(210 - 240 * v); L = L_(); d = ImageDraw.Draw(L)
    d.line((cx, cy, cx + (r - 40) * math.cos(ang), cy - (r - 40) * math.sin(ang)), fill=YEL + (255,), width=10); d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=YEL + (255,)); can.alpha_composite(L)
    typewriter(can, t, w('14.') - 0.05, (CX, YT), '14. OKTOBER 1942', typew(70), CREAM, 0.07)
    stamp(can, t, w('Notlandung,') - 0.05, 'NOTLANDUNG', (CX, Y3 + 30), RED, 76, -6); return can
def s_ground(t, w0, w1):
    can = sh(photo('h43', t, w0, w1, 1, 0.45, 1.04))
    tt = w('Tage') - 0.2
    for i in range(3):   # three crossed-out days
        ti = tt + i * 0.25; x = CX - 220 + i * 220; y = 1120
        if t < ti: continue
        k = eout((t - ti) / 0.3); L = L_(); d = ImageDraw.Draw(L)
        d.rounded_rectangle((x - 80, y - 90, x + 80, y + 90), 14, fill=(232, 226, 210, int(235 * k))); d.rectangle((x - 80, y - 90, x + 80, y - 50), fill=RED + (int(235 * k),))
        d.text((x, y + 20), str(i + 1), font=anton(90), fill=INK_ + (int(255 * k),), anchor='mm'); can.alpha_composite(L)
    txt(can, t, w('Strafe'), (CX, Y2 + 30), 'DREI TAGE', anton(100), WHITE)
    txt(can, t, w('Bodendienst.') - 0.1, (CX, Y3 + 30), 'BODENDIENST', anton(80), YEL); return can
def s_rossmann(t, w0, w1):
    can = sh(photo('h30', t, w0, w1, 1, 0.4, 1.04))
    txt(can, t, w('Oberfeldwebel'), (CX, Y1 + 20), 'OBERFELDWEBEL', bebas(64), CREAM)
    txt(can, t, w('Edmund') - 0.05, (CX, Y2 + 20), 'EDMUND ROSSMANN', anton(96), YEL)
    txt(can, t, w('Lehrer.') - 0.1, (CX, Y3 + 30), 'WIRD SEIN LEHRER', bebas(64), WHITE); return can
def s_dist(t, w0, w1):      # range ruler: hold distance, fire only from close range
    can = sky(); ta, tk = w('Abstand') - 0.2, w('kurzer') - 0.2
    gap = 520 if t < tk else lerp(520, 170, eio((t - tk) / 0.9)); ty = 900; tx = 820
    put_icon(can, plane_icon(60, (190, 70, 60)), tx, ty)
    mx = tx - 120 - gap; put_icon(can, plane_icon(60, YEL), mx, ty)
    if t > ta:
        L = L_(); d = ImageDraw.Draw(L); y = ty + 120
        for x in range(int(mx), int(tx - 110), 26): d.line((x, y, x + 14, y), fill=CREAM + (220,), width=4)
        d.line((mx, y - 20, mx, y + 20), fill=CREAM + (220,), width=4); d.line((tx - 110, y - 20, tx - 110, y + 20), fill=CREAM + (220,), width=4); can.alpha_composite(L)
    if t > w('schießen.') - 0.1:
        k = (t - w('schießen.') + 0.1) % 0.3 / 0.3; L = L_(); d = ImageDraw.Draw(L)
        for j in range(3): x = mx + 70 + (k + j / 3) * (gap - 20); d.line((x, ty - 4, x + 26, ty - 4), fill=(255, 220, 120, 255), width=4)
        can.alpha_composite(L)
    txt(can, t, ta, (CX, Y1 + 40), 'ABSTAND HALTEN', anton(84), WHITE)
    txt(can, t, tk, (CX, Y2 + 40), 'ERST AUS KURZER DISTANZ', anton(76), YEL)
    txt(can, t, w('schießen.') - 0.05, (CX, Y3 + 40), 'SCHIESSEN', bebas(64), CREAM); return can
def s_quote(t, w0, w1):     # the principle as a quote card over the portrait
    can = sh(photo('h37', t, w0, w1, 1, 0.4, 1.04), 235, 0.42)
    txt(can, t, w('Grundsatz') - 0.05, (CX, 1060), 'SEIN GRUNDSATZ', bebas(62), CREAM)
    tq = w('Fliege') - 0.1
    if t >= tq:
        k = eout((t - tq) / 0.4); L = L_(); d = ImageDraw.Draw(L)
        d.rectangle((CX - 400, 1130, CX - 392, 1130 + 240 * k), fill=YEL + (255,)); can.alpha_composite(L)
        d2 = lambda s, y, t0, col: typewriter(can, t, t0, (CX + 10, y), s, typew(62), col, 0.045)
        d2('„Fliege mit dem Kopf,', 1190, tq, WHITE); d2('nicht mit den Muskeln.“', 1290, w('nicht', 96) - 0.1, YEL)
    return can
def s_first(t, w0, w1):
    can = sh(photo('h35', t, w0, w1, 1, 0.4, 1.04))
    typewriter(can, t, w('November') - 0.05, (CX, Y1 - 20), 'ANFANG NOVEMBER 1942', typew(66), CREAM, 0.06)
    txt(can, t, w('Abschuss,') - 0.1, (CX, Y2), 'ERSTER ABSCHUSS: IL-2', anton(88), YEL)
    stamp(can, t, w('notlanden.') - 0.1, 'WIEDER NOTLANDUNG', (CX + 40, Y3 + 40), RED, 60, -7); return can

# ================= chapter 3 =================
MONTHS = ['NOV', 'DEZ', 'JAN', 'FEB', 'MÄR', 'APR', 'MAI', 'JUN', 'JUL', 'AUG']
LOW = [1, 1, 1, 0, 2, 3, 6, 4, 22, 46]   # schematic, rising shape only (no exact monthly values)
def chart(can, t, n_show, t_rise=None, y0=1350, x0=150, x1=900, hmax=520):
    bw = (x1 - x0) / len(MONTHS)
    L = L_(); d = ImageDraw.Draw(L); d.line((x0 - 10, y0, x1, y0), fill=GREY + (220,), width=4)
    for i, m in enumerate(MONTHS):
        if i >= n_show: break
        v = LOW[i] if (i < 6 or t_rise is None) else LOW[i] * eio((t - t_rise - (i - 6) * 0.25) / 0.6)
        if i >= 6 and t_rise is None: v = 0
        h = max(4, v / 46 * hmax); x = x0 + i * bw + 8
        d.rectangle((x, y0 - h, x + bw - 16, y0), fill=(YEL if i < 6 else RED) + (255,))
        d.text((x + (bw - 16) / 2, y0 + 30), m, font=bebas(34), fill=CREAM + (230,), anchor='mm')
    can.alpha_composite(L)
def s_chart1(t, w0, w1):
    can = plain()
    chapter(can, t, w0 + 0.3, 3, 'DER AUFSTIEG AN DER OSTFRONT', w0 + 3.3)
    n = int(clamp((t - w('Frühjahr') + 0.2) / 1.2) * 6); chart(can, t, n)
    txt(can, t, w('Frühjahr') - 0.1, (CX, 640), 'BIS ZUM FRÜHJAHR 1943', anton(80), WHITE)
    txt(can, t, w('wenige') - 0.1, (CX, 740), 'NUR WENIGE ABSCHÜSSE', bebas(62), YEL)
    label(can, t, w0 + 1.0, CX, 1470, 'SCHEMATISCHE DARSTELLUNG', 34, GREY, 'mm'); return can
def s_bubi(t, w0, w1):
    can = sh(photo('h07', t, w0, w1, 1, 0.4, 1.05))
    txt(can, t, w('jungen') - 0.1, (CX, Y1), 'WEGEN SEINES JUNGEN AUSSEHENS', bebas(60), CREAM)
    tb = w('Bubi.') - 0.1
    if t >= tb:
        k = eout((t - tb) / 0.35); f = anton(int(200 * lerp(1.3, 1.0, k)))
        shadowed(can, lambda d: d.text((CX, Y2 + 60), '„BUBI“', font=f, fill=YEL + (int(255 * k),), anchor='mm'))
    return can
def s_krupi(t, w0, w1):     # radio waves from the other pilot
    can = sh(photo('h23', t, w0, w1, 1, 0.4, 1.04)); tf = w('Funk') - 0.1
    if t >= tf:
        L = L_(); d = ImageDraw.Draw(L); cx, cy = 230, 900
        for j in range(4):
            u = ((t - tf) * 0.9 + j / 4) % 1.0; r = 40 + 200 * u
            d.arc((cx - r, cy - r, cx + r, cy + r), -40, 40, fill=YEL + (int(220 * (1 - u)),), width=6)
        can.alpha_composite(L); label(can, t, w('näher') - 0.05, 560, 820, '„NÄHER RAN!“', 72, YEL, 'mm')
    txt(can, t, w('Walter') - 0.05, (CX, Y2 + 20), 'WALTER KRUPINSKI', anton(90), WHITE)
    txt(can, t, w('Funk') - 0.1, (CX, Y3 + 30), 'IM FUNK', bebas(62), CREAM); return can
def s_summer(t, w0, w1):
    can = dim(photo('h27', t, w0, w1, 1, 0.4, 1.04), 110)
    chart(can, t, 10, w('rasch') - 0.4, 1380, 150, 900, 560)
    txt(can, t, w('Sommer') - 0.05, (CX, 560), 'SOMMER 1943', anton(96), WHITE)
    txt(can, t, w('rasch') - 0.05, (CX, 670), 'DIE ZAHLEN STEIGEN RASCH', bebas(64), YEL); return can
KURSK = Map(36.4, 51.6, 7.0, hi=('Russia',))
BULGE = [(35.6, 52.6), (36.6, 52.3), (37.6, 51.9), (38.1, 51.2), (37.4, 50.7), (36.3, 50.8), (35.4, 51.0), (34.9, 51.6), (35.0, 52.2)]
def s_kursk(t, w0, w1):     # the Kursk salient drawn, seven marks for seven victories
    z = lerp(1.0, 1.08, eio((t - w0) / (w1 - w0))); can = KURSK.frame(z)
    line_draw(can, t, w('Kursk,') - 0.6, [KURSK.p(*q, z) for q in BULGE + BULGE[:1]], RED, 7, 1.0)
    kx, ky = KURSK.p(36.19, 51.73, z); glow_dot(can, kx, ky, WHITE, 11); label(can, t, w('Kursk,') - 0.1, kx + 24, ky, 'KURSK', 64, WHITE)
    for i, (a, b) in enumerate([((36.1, 53.4), (36.2, 52.6)), ((36.6, 49.9), (36.6, 50.8))]):
        arrow(can, KURSK.p(*a, z), KURSK.p(*b, z), eio((t - w('Schlacht') - i * 0.2) / 0.7), RED, 12, 36)
    typewriter(can, t, w('7.') - 0.05, (CX, YT), '7. JULI 1943', typew(76), CREAM, 0.07)
    ts = w('sieben') - 0.05
    for i in range(7):
        if t < ts + i * 0.12: break
        k = eout((t - ts - i * 0.12) / 0.2); x = CX - 300 + i * 100; L = L_(); ImageDraw.Draw(L).rectangle((x - 12, Y2 - 60, x + 12, Y2 + 60 - (1 - k) * 60), fill=YEL + (255,)); can.alpha_composite(L)
    txt(can, t, w('Tag.', 133) - 0.1, (CX, Y3 + 30), 'SIEBEN LUFTSIEGE AN EINEM TAG', anton(72), WHITE); return can
def s_method(t, w0, w1):    # four-step cycle, each step lights up on its word
    can = plain(); cx, cy, R = CX, 1010, 280
    steps = [('BEOBACHTEN', 'beobachten,'), ('ENTSCHEIDEN', 'entscheiden,'), ('ANGREIFEN', 'angreifen'), ('ABDREHEN', 'abdrehen.')]
    txt(can, t, w('Methode') - 0.1, (CX, YT + 40), 'SEINE METHODE', anton(90), WHITE)
    for i, (lab, key) in enumerate(steps):
        ti = w(key) - 0.1; ang = -math.pi / 2 + i * math.pi / 2; x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        if t >= ti:
            k = eout((t - ti) / 0.35); col = YEL if i == 2 else WHITE
            L = L_(); d = ImageDraw.Draw(L); r = 95 * k; d.ellipse((x - r, y - r, x + r, y + r), fill=(28, 32, 40, 235), outline=col + (255,), width=6); can.alpha_composite(L)
            label(can, t, ti, x, y, str(i + 1), 80, col, 'mm'); label(can, t, ti + 0.1, x, y + (-135 if i == 0 else 135), lab, 50, col, 'mm')
            a0 = ang + 0.35; a1 = ang + math.pi / 2 - 0.35
            arc = [(cx + R * math.cos(a), cy + R * math.sin(a)) for a in np.linspace(a0, a1, 16)]
            if i < 3: line_draw(can, t, ti + 0.2, arc, GREY, 5, 0.4)
    return can
def s_capt(t, w0, w1):
    can = sh(photo('h29', t, w0, w1, 1, 0.45, 1.04))
    typewriter(can, t, w('August') - 0.05, (CX, Y1 - 20), 'AUGUST 1943', typew(72), CREAM, 0.07)
    txt(can, t, w('sowjetische') - 0.1, (CX, Y2), 'KURZ IN SOWJETISCHER HAND', anton(80), RED)
    txt(can, t, w('fliehen.') - 0.1, (CX, Y3 + 30), 'FLUCHT', anton(96), YEL)
    label(can, t, w('eigener') - 0.1, CX, Y3 + 120, 'NACH EIGENER SCHILDERUNG', 40, GREY, 'mm'); return can
def s_staffel(t, w0, w1):
    can = sh(photo('h10', t, w0, w1, 1, 0.45, 1.04))
    typewriter(can, t, w('2.') - 0.05, (CX, Y1 - 20), '2. SEPTEMBER 1943', typew(70), CREAM, 0.07)
    txt(can, t, w('9.') - 0.05, (CX, Y2), 'STAFFELKAPITÄN', anton(96), YEL)
    txt(can, t, w('Jagdgeschwaders') - 0.1, (CX, Y3 + 20), '9. STAFFEL, JG 52', bebas(64), WHITE); return can
def s_16(t, w0, w1):        # sixteen emergency landings as small plane icons tilting down
    can = sky(); t0 = w('16') - 0.15; ic = plane_icon(40)
    for i in range(16):
        ti = t0 + i * 0.07
        if t < ti: break
        k = eout((t - ti) / 0.3); r, c = divmod(i, 4); x = CX - 300 + c * 200; y = 640 + r * 150
        put_icon(can, ic, x, y + (1 - k) * 30, 0.35 * k, k)
    f = anton(260); v = int(clamp((t - t0) / 1.1) * 16)
    if t >= t0: shadowed(can, lambda d: d.text((CX, 1300), str(v), font=f, fill=YEL + (255,), anchor='mm'))
    txt(can, t, t0 + 0.3, (CX, 1470), 'NOTLANDUNGEN', anton(70), WHITE); return can
def s_never(t, w0, w1):
    can = sh(photo('h06', t, w0, w1, 1, 0.4, 1.04))
    txt(can, t, w('Gegner', 159), (CX, Y1 + 20), 'VON EINEM GEGNER IM LUFTKAMPF', bebas(62), CREAM)
    txt(can, t, w('nie') - 0.05, (CX, Y2 + 30), 'NIE ABGESCHOSSEN', anton(104), YEL); return can

# ================= chapter 4 =================
def s_rk(t, w0, w1):
    can = sh(photo('h25', t, w0, w1, 1, 0.4, 1.04), 235, 0.5)
    chapter(can, t, w0 + 0.3, 4, 'AUSZEICHNUNGEN UND DAS KRIEGSENDE', w0 + 3.3)
    typewriter(can, t, w('29.') - 0.05, (CX, Y1), '29. OKTOBER 1943', typew(70), CREAM, 0.07)
    txt(can, t, w('148') - 0.05, (CX, Y2 + 20), '148 LUFTSIEGE', anton(96), WHITE)
    txt(can, t, w('Ritterkreuz.') - 0.1, (CX, Y3 + 30), 'RITTERKREUZ', anton(90), YEL); return can
def s_heart(t, w0, w1):
    can = sh(photo('h54', t, w0, w1, 1, 0.5, 1.04), 220, 0.6)
    point_at(can, t, w('Herz') - 0.05, pan_pt('h54', t, w0, w1, 1, 0.5, 1.04, 1010, 1180), 'HERZ FÜR „USCH“', (300, 1380))
    txt(can, t, w('Ursula') - 0.05, (CX, YT + 60), 'FÜR URSULA', anton(84), WHITE); return can
def pan_pt(n, t, w0, w1, d, cy, zoom, sx, sy):
    """screen position of a source pixel inside pan()"""
    im = src(n); w_ = min(im.width, im.height * W / H) / zoom; sc = W / w_; need = SPEED * (w1 - w0) / sc
    if im.width - w_ < need * 0.6: w_ = max(im.width - need * 0.6, im.width / 1.35); sc = W / w_; need = SPEED * (w1 - w0) / sc
    travel = min(need, im.width - w_); mid = im.width / 2; a, b = mid - d * travel / 2, mid + d * travel / 2
    cx = lerp(a, b, clamp((t - w0) / (w1 - w0))); h_ = w_ * H / W; x0 = min(max(cx - w_ / 2, 0), im.width - w_); y0 = min(max(im.height * cy - h_ / 2, 0), im.height - h_)
    return ((sx - x0) * sc, (sy - y0) * sc)
def stairs(can, t, steps, y0=1450, x0=130, sw=200, sh_=110):
    """award staircase: each step rises when named"""
    for i, (num, lab, ti, col) in enumerate(steps):
        if t < ti: continue
        k = eout((t - ti) / 0.4); x = x0 + i * sw; top = y0 - (i + 1) * sh_ * k
        L = L_(); d = ImageDraw.Draw(L); d.rectangle((x, top, x + sw - 14, y0), fill=(30, 34, 42, 230), outline=col + (255,), width=4); can.alpha_composite(L)
        label(can, t, ti + 0.1, x + (sw - 14) / 2, top - 70, num, 64, col, 'mm'); label(can, t, ti + 0.2, x + (sw - 14) / 2, top + 40, lab, 34, CREAM, 'mm')
def s_stairs(t, w0, w1):
    can = dim(photo('h21', t, w0, w1, 1, 0.4, 1.04), 90)
    stairs(can, t, [('148', 'RITTERKREUZ', w0 + 0.2, GREY), ('202', 'EICHENLAUB', w('202') - 0.05, YEL), ('268', 'SCHWERTER', w('268') - 0.05, YEL)])
    typewriter(can, t, w('März', 176) - 0.05, (CX, YT), 'MÄRZ / JULI 1944', typew(66), CREAM, 0.06); return can
def s_300(t, w0, w1):
    can = sh(photo('h32', t, w0, w1, 1, 0.4, 1.04), 235, 0.45)
    typewriter(can, t, w('24.') - 0.05, (CX, Y1 - 30), '24. AUGUST 1944', typew(70), CREAM, 0.07)
    txt(can, t, w('elf') - 0.05, (CX, Y2 - 10), '11 AN EINEM TAG', anton(90), WHITE)
    tm = w('300.') - 0.2
    if t >= tm:
        k = eout((t - tm) / 0.4); f = anton(int(170 * lerp(1.3, 1.0, k)))
        shadowed(can, lambda d: d.text((CX, Y3 + 30), 'ÜBER 300', font=f, fill=YEL + (int(255 * k),), anchor='mm'))
    return can
def s_crit(t, w0, w1):      # the number under scrutiny: magnifier sweeps over it, then "umstritten"
    can = plain(); f = anton(330)
    shadowed(can, lambda d: d.text((CX, 820), '300', font=f, fill=(150, 150, 150, 255), anchor='mm'))
    u = clamp((t - w0) / 2.2); mx = lerp(260, 780, u); my = 820 + 40 * math.sin(u * 6)
    L = L_(); d = ImageDraw.Draw(L); d.ellipse((mx - 120, my - 120, mx + 120, my + 120), outline=WHITE + (255,), width=10)
    d.line((mx + 85, my + 85, mx + 180, my + 180), fill=WHITE + (255,), width=22); can.alpha_composite(L)
    txt(can, t, w0 + 0.2, (CX, YT + 40), 'FORSCHER SEHEN DIESE ZAHL KRITISCH', bebas(60), CREAM)
    txt(can, t, w('ganzen') - 0.1, (CX, Y2), 'ERFOLGE DER GANZEN GRUPPE', anton(78), YEL)
    txt(can, t, w('zugeschrieben', 195) - 0.1, (CX, Y3), 'IHM ZUGESCHRIEBEN?', anton(78), WHITE); return can
def s_diamonds(t, w0, w1):  # 27 awards of the Diamonds, one lights up
    can = dim(photo('h04', t, w0, w1, 1, 0.4, 1.04), 80)
    txt(can, t, w('301') - 0.05, (CX, YT + 40), '301: BRILLANTEN', anton(84), YEL)
    t27 = w('27') - 0.1
    for i in range(27):
        ti = t27 + i * 0.04
        if t < ti: break
        r, c = divmod(i, 9); x = CX - 360 + c * 90; y = 1180 + r * 90; k = eout((t - ti) / 0.25); hi = (i == 26)
        L = L_(); d = ImageDraw.Draw(L); s_ = 26 * k
        d.polygon([(x, y - s_), (x + s_, y), (x, y + s_), (x - s_, y)], fill=(YEL if hi else (200, 210, 225)) + (255,)); can.alpha_composite(L)
    txt(can, t, t27 + 0.6, (CX, Y3 + 50), 'EINE VON NUR 27', anton(70), WHITE); return can
def s_wedding(t, w0, w1):
    can = sh(photo('h39', t, w0, w1, 1, 0.5, 1.04), 230, 0.55)
    typewriter(can, t, w('10.') - 0.05, (CX, Y1 + 20), '10. SEPTEMBER 1944', typew(68), CREAM, 0.07)
    txt(can, t, w('heiratete') - 0.05, (CX, Y2 + 30), 'HOCHZEIT MIT URSULA PAETSCH', anton(78), YEL)
    txt(can, t, w('Schulzeit') - 0.1, (CX, Y3 + 40), 'SEINE LIEBE AUS DER SCHULZEIT', bebas(58), WHITE); return can
def s_jets(t, w0, w1):
    can = sh(photo('h53', t, w0, w1, 1, 0.45, 1.04))
    txt(can, t, w('Düsenjägern') - 0.1, (CX, Y1 + 20), 'WECHSEL ZU DEN DÜSENJÄGERN?', bebas(62), CREAM)
    stamp(can, t, w('lehnte') - 0.05, 'ABGELEHNT', (CX, Y2 + 70), RED, 90, -8); return can
CZ = Map(16.0, 49.6, 9.0, hi=('Czechia',))
def s_bruenn(t, w0, w1):
    z = lerp(1.0, 1.1, eio((t - w0) / (w1 - w0))); can = CZ.frame(z); x, y = CZ.p(16.61, 49.2, z)
    typewriter(can, t, w('8.') - 0.05, (CX, YT), '8. MAI 1945', typew(76), CREAM, 0.07)
    if t > w('Brünn') - 0.2:
        glow_dot(can, x, y, YEL, 12); label(can, t, w('Brünn') - 0.2, x + 26, y - 6, 'BRÜNN', 72, YEL)
        k = eout((t - w('letzten') + 0.1) / 0.4)
        if k > 0:
            L = L_(); d = ImageDraw.Draw(L); r = 60 * k
            d.polygon([(x + r * math.cos(math.radians(a)) * (1 if i % 2 == 0 else 0.45), y + r * math.sin(math.radians(a)) * (1 if i % 2 == 0 else 0.45)) for i, a in enumerate(range(-90, 270, 36))], outline=WHITE + (255,), width=4); can.alpha_composite(L)
    txt(can, t, w('letzten') - 0.1, (CX, Y3 + 20), 'LETZTER LUFTSIEG', anton(90), WHITE); return can
def s_1404(t, w0, w1):
    can = sh(photo('h08', t, w0, w1, 1, 0.45, 1.04), 235, 0.45)
    counter(can, t, w('1.404') - 0.3, 0, 1404, (CX, Y2 - 30), 190, YEL, 1.4, '{:,}')
    txt(can, t, w('Einsätze') - 0.05, (CX, Y3 + 40), 'EINSÄTZE', anton(90), WHITE); return can
def s_surrender(t, w0, w1):  # aircraft blown up on the ground, then a white flag
    can = plain(); td = w('zerstören') - 0.2
    for i in range(4):
        x = 190 + i * 230; y = 900; ti = td + i * 0.18
        put_icon(can, plane_icon(70, GREY), x, y, -math.pi / 2, 1.0 if t < ti + 0.3 else 0.35)
        if t >= ti:
            u = (t - ti) / 0.8
            if u < 1: L = L_(); r = 30 + 140 * u; ImageDraw.Draw(L).ellipse((x - r, y - r, x + r, y + r), fill=(255, 170, 70, int(170 * (1 - u)))); can.alpha_composite(L.filter(ImageFilter.GaussianBlur(10)))
    tf = w('ergab') - 0.2
    if t >= tf:
        k = eout((t - tf) / 0.6); L = L_(); d = ImageDraw.Draw(L); fx, fy = CX - 60, 1300
        d.line((fx, fy, fx, fy - 260 * k), fill=CREAM + (255,), width=8)
        wv = [(fx + 8 + i * 12, fy - 260 * k + 10 * math.sin(t * 6 + i * 0.6)) for i in range(15)]
        d.polygon(wv + [(p[0], p[1] + 110) for p in wv[::-1]], fill=WHITE + (int(255 * k),)); can.alpha_composite(L)
    txt(can, t, w('Einheit') - 0.1, (CX, YT + 40), 'DIE FLUGZEUGE WERDEN ZERSTÖRT', bebas(62), CREAM)
    txt(can, t, tf + 0.1, (CX, Y3 + 30), 'KAPITULATION VOR DEN AMERIKANERN', anton(70), YEL); return can

# ================= chapter 5 =================
EAST2 = Map(26.0, 52.0, 34.0, hi=('Russia',))
def s_handover(t, w0, w1):
    z = lerp(1.0, 1.06, eio((t - w0) / (w1 - w0))); can = EAST2.frame(z)
    chapter(can, t, w0 + 0.3, 5, 'ZEHN JAHRE GEFANGENSCHAFT', w0 + 3.3)
    a = EAST2.p(14.15, 49.3, z); b = EAST2.p(37.6, 55.75, z)
    glow_dot(can, *a, WHITE, 11); label(can, t, w0 + 3.5, a[0] + 20, a[1] + 50, 'BÖHMEN', 54, WHITE)
    arrow(can, a, b, eio((t - w('übergaben') + 0.1) / 1.6), RED, 14, 44)
    if t > w('Rote') + 0.5: glow_dot(can, *b, RED, 12); label(can, t, w('Rote'), b[0] - 20, b[1] - 50, 'SOWJETUNION', 60, RED, 'rm')
    typewriter(can, t, w('14.', 237) - 0.05, (CX, Y2 + 20), '14. MAI 1945', typew(72), CREAM, 0.07)
    txt(can, t, w('Rote') - 0.05, (CX, Y3 + 30), 'ÜBERGABE AN DIE ROTE ARMEE', anton(74), RED); return can
def s_cell(t, w0, w1):      # isolation cell: dark room, one small barred window, light slowly fading
    can = plain(); L = L_(); d = ImageDraw.Draw(L)
    d.rectangle((140, 520, 940, 1440), outline=(70, 74, 82, 255), width=8)
    wx, wy = CX, 720; lt = 0.6 + 0.4 * math.sin(t * 0.8)
    d.rectangle((wx - 110, wy - 80, wx + 110, wy + 80), fill=(210, 220, 235, int(200 * lt)))
    for i in range(4): x = wx - 82 + i * 55; d.line((x, wy - 80, x, wy + 80), fill=(40, 42, 48, 255), width=10)
    can.alpha_composite(L)
    beam = L_(); ImageDraw.Draw(beam).polygon([(wx - 110, wy + 80), (wx + 110, wy + 80), (wx + 330, 1440), (wx - 110, 1440)], fill=(210, 220, 235, int(40 * lt))); can.alpha_composite(beam.filter(ImageFilter.GaussianBlur(20)))
    txt(can, t, w('lehnte', 244) - 0.05, (CX, 1060), 'KEINE ZUSAMMENARBEIT', anton(80), WHITE)
    txt(can, t, w('Isolationshaft.') - 0.1, (CX, 1200), 'ISOLATIONSHAFT', anton(96), RED)
    label(can, t, w('eigenen', 244) - 0.1, CX, 1310, 'NACH EIGENEN ANGABEN', 40, GREY, 'mm'); return can
def s_verdicts(t, w0, w1):  # verdict timeline: 1949 then 1951
    can = plain(); x0, x1, y = 160, 900, 980
    line_draw(can, t, w0 + 0.1, [(x0, y), (x1, y)], GREY, 5, 0.8)
    for x, yr, lab, ti in [(330, '1949', '20 JAHRE', w('1949') - 0.05), (730, '1951', '25 JAHRE', w('1951') - 0.05)]:
        if t >= ti:
            dot(can, x, y, RED, 15); txt(can, t, ti, (x, y - 90), yr, typew(64), CREAM); stamp(can, t, ti + 0.4, lab, (x, y + 150), RED, 56, -6 if x < 500 else 6)
    txt(can, t, w0 + 0.2, (CX, YT + 40), 'VERURTEILT', anton(96), WHITE)
    txt(can, t, w('zweiten') - 0.1, (CX, Y3 + 30), 'ZWEITES VERFAHREN', bebas(62), CREAM); return can
def s_charge(t, w0, w1):
    can = plain()
    doc(can, t, w('warf') - 0.2, [('ANKLAGE', 66, INK_), ('780 ZIVILISTEN GETÖTET', 40, (150, 30, 30)), ('EINE BÄCKEREI ANGEGRIFFEN', 40, (150, 30, 30))], CX, 820, 800)
    stamp(can, t, w('bestritt') - 0.05, 'BESTRITTEN', (CX + 120, 1120), RED, 66, -10)
    txt(can, t, w('politisch') - 0.05, (CX, Y3 + 30), 'HEUTE: POLITISCH MOTIVIERT', anton(76), YEL); return can
def s_son(t, w0, w1):
    can = sh(photo('h56', t, w0, w1, 1, 0.45, 1.04), 235, 0.45); ty = Y2
    txt(can, t, w('Sohn') - 0.05, (CX, Y1 - 10), 'SEIN SOHN ERICH PETER', bebas(62), CREAM)
    ta = w('1945', 273) - 0.05
    if t >= ta:
        txt(can, t, ta, (260, ty), '1945', anton(90), WHITE); k = eio((t - w('starb', 276) + 0.3) / 0.8)
        L = L_(); ImageDraw.Draw(L).line((380, ty + 4, lerp(380, 690, k), ty + 4), fill=GREY + (255,), width=6); can.alpha_composite(L)
        if k >= 0.98: txt(can, t, w('1948.') - 0.05, (800, ty), '1948', anton(90), GREY)
    txt(can, t, w('nie', 278) - 0.05, (CX, Y3 + 40), 'HARTMANN SAH IHN NIE', anton(78), YEL); return can
def s_free(t, w0, w1):
    can = sh(photo('h46', t, w0, w1, 1, 0.45, 1.04))
    typewriter(can, t, w('Oktober', 281) - 0.05, (CX, Y1), 'OKTOBER 1955', typew(76), CREAM, 0.07)
    txt(can, t, w('frei.') - 0.1, (CX, Y2 + 30), 'FREI', anton(150), YEL)
    txt(can, t, w('letzten', 283) - 0.1, (CX, Y3 + 40), 'MIT DEN LETZTEN KRIEGSGEFANGENEN', bebas(56), WHITE); return can
def s_annul(t, w0, w1):
    can = plain()
    doc(can, t, w0 + 0.2, [('URTEIL GEGEN E. HARTMANN', 46, INK_), ('1949 / 1951', 44, INK_), ('', 30, INK_)], CX, 880, 780)
    stamp(can, t, w('Urteile') - 0.05, 'AUFGEHOBEN', (CX + 40, 960), RED, 84, -9)
    typewriter(can, t, w('1997') - 0.05, (CX, YT + 40), '1997', typew(80), CREAM, 0.1)
    txt(can, t, w('Militärstaatsanwaltschaft') - 0.1, (CX, Y3 + 30), 'RUSSISCHE MILITÄRSTAATSANWALTSCHAFT', bebas(56), WHITE); return can

# ================= chapter 6 =================
def s_usa(t, w0, w1):
    can = sh(photo('h48', t, w0, w1, 1, 0.45, 1.04), 230, 0.5)
    chapter(can, t, w0 + 0.3, 6, 'BUNDESWEHR UND STARFIGHTER', w0 + 3.3)
    txt(can, t, w('Bundeswehr', 293) - 0.05, (CX, Y1 + 10), '1956: BUNDESWEHR', anton(84), WHITE)
    txt(can, t, w('USA') - 0.05, (CX, Y2 + 20), 'AUSBILDUNG IN DEN USA', anton(80), YEL)
    txt(can, t, w('Düsenflugzeugen') - 0.1, (CX, Y3 + 30), 'AUF DÜSENFLUGZEUGEN', bebas(60), CREAM); return can
def s_jg71(t, w0, w1):
    can = sh(photo('h09', t, w0, w1, 1, 0.45, 1.04))
    typewriter(can, t, w('1959') - 0.05, (CX, Y1 - 20), '1959 BIS 1962', typew(72), CREAM, 0.07)
    txt(can, t, w('Jagdgeschwader', 303) - 0.05, (CX, Y2), 'JG 71 „RICHTHOFEN“', anton(90), YEL)
    txt(can, t, w('ersten', 303) - 0.1, (CX, Y3 + 20), 'ERSTER REINER DÜSENJÄGERVERBAND', bebas(58), WHITE); return can
def f104(s=380, col=WHITE):
    """side view of a slender Starfighter silhouette"""
    L = Image.new('RGBA', (s * 2, s), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = s
    d.polygon([(c - s * 0.95, s * 0.5), (c + s * 0.85, s * 0.46), (c + s * 0.98, s * 0.5), (c + s * 0.85, s * 0.54), (c - s * 0.95, s * 0.58)], fill=col + (255,))
    d.polygon([(c - s * 0.75, s * 0.5), (c - s * 0.95, s * 0.18), (c - s * 0.82, s * 0.18), (c - s * 0.55, s * 0.5)], fill=col + (255,))
    d.polygon([(c - s * 0.05, s * 0.55), (c - s * 0.3, s * 0.66), (c - s * 0.2, s * 0.66), (c + s * 0.15, s * 0.55)], fill=col + (255,))
    d.ellipse((c + s * 0.35, s * 0.4, c + s * 0.6, s * 0.52), fill=col + (255,)); return L
def s_f104(t, w0, w1):
    can = sky(); tx = w('ungeeignet') - 0.1
    put_icon(can, f104(), CX, 820, 0.0, clamp((t - w0) / 0.5))
    if t >= tx: line_draw(can, t, tx, [(CX - 300, 640), (CX + 300, 1000)], RED, 16, 0.35); line_draw(can, t, tx + 0.2, [(CX + 300, 640), (CX - 300, 1000)], RED, 16, 0.35)
    txt(can, t, w('Starfighter') - 0.05, (CX, YT + 40), 'DER STARFIGHTER', anton(90), WHITE)
    txt(can, t, tx, (CX, Y1 - 40), 'FÜR UNGEEIGNET GEHALTEN', bebas(62), YEL)
    tc = w('stürzten') - 0.1
    if t >= tc:
        n = int(clamp((t - tc) / 2.0) * 100); L = L_(); d = ImageDraw.Draw(L)
        for i in range(n):
            r, c = divmod(i, 20); x = 130 + c * 42; y = 1230 + r * 40; d.line((x - 10, y, x + 10, y), fill=CREAM + (220,), width=4); d.line((x, y - 14, x, y + 14), fill=CREAM + (220,), width=4)
        can.alpha_composite(L)
    txt(can, t, w('100') - 0.05, (CX, 1480), 'MEHR ALS 100 TOTE PILOTEN', anton(66), RED); return can
def s_retire(t, w0, w1):
    can = sh(photo('h51', t, w0, w1, 1, 0.45, 1.04))
    txt(can, t, w('1970', 324) - 0.05, (CX, Y1), '1970', anton(110), WHITE)
    txt(can, t, w('Ruhestand') - 0.1, (CX, Y2 + 20), 'VORZEITIGER RUHESTAND', anton(80), YEL)
    txt(can, t, w('Kritik.') - 0.1, (CX, Y3 + 30), 'WOHL AUCH WEGEN SEINER KRITIK', bebas(58), WHITE); return can
def s_teacher(t, w0, w1):
    can = sh(photo('h52', t, w0, w1, 1, 0.45, 1.04))
    txt(can, t, w('Fluglehrer') - 0.05, (CX, Y2), 'FLUGLEHRER', anton(110), YEL)
    txt(can, t, w('Hangelar') - 0.05, (CX, Y3 + 30), 'IN HANGELAR BEI BONN', bebas(62), WHITE); return can
def s_death(t, w0, w1):
    can = sh(photo('h02', t, w0, w1, 1, 0.45, 1.04), 235, 0.45); ty = Y2 + 20
    typewriter(can, t, w('20.', 335) - 0.05, (CX, Y1 - 10), '20. SEPTEMBER 1993', typew(70), CREAM, 0.07)
    txt(can, t, w('71', 335) - 0.05, (260, ty), '1922', anton(90), WHITE)
    k = eio((t - w('71', 335)) / 0.8); L = L_(); ImageDraw.Draw(L).line((380, ty + 4, lerp(380, 690, k), ty + 4), fill=YEL + (255,), width=6); can.alpha_composite(L)
    if k > 0.98: txt(can, t, w('71', 335) + 0.8, (800, ty), '1993', anton(90), YEL)
    txt(can, t, w('Weil', 335) - 0.05, (CX, Y3 + 40), 'WEIL IM SCHÖNBUCH', bebas(62), WHITE); return can

# ================= chapter 7 =================
def logbook(can, x, y, a=1.0, open_=1.0):
    L = L_(); d = ImageDraw.Draw(L); w_ = 300 * open_
    d.rectangle((x - w_, y - 200, x + w_, y + 200), fill=(226, 216, 192, int(240 * a)), outline=(120, 100, 70, int(255 * a)), width=4)
    d.line((x, y - 200, x, y + 200), fill=(120, 100, 70, int(255 * a)), width=4)
    for i in range(9):
        yy = y - 160 + i * 40; d.line((x - w_ + 30, yy, x - 30, yy), fill=(150, 140, 120, int(200 * a)), width=2); d.line((x + 30, yy, x + w_ - 30, yy), fill=(150, 140, 120, int(200 * a)), width=2)
    can.alpha_composite(L)
def s_logbook(t, w0, w1):   # two logbooks, the second one fades and its pages blow away
    can = plain(); chapter(can, t, w0 + 0.3, 7, 'DIE ABSCHUSSZAHLEN IM FAKTENCHECK', w0 + 3.3)
    logbook(can, CX, 830, 1.0, 0.75); label(can, t, w0, CX, 830 - 240, 'FLUGBUCH 1', 48, CREAM, 'mm')
    tv = w('verloren.') - 0.2; a = 1 - eio((t - tv) / 0.9)
    logbook(can, CX, 1290, a, 0.75); label(can, t, w0 + 0.2, CX, 1290 - 240, 'FLUGBUCH 2', 48, CREAM, 'mm', tv)
    if t > tv:
        rr = np.random.default_rng(3); L = L_(); d = ImageDraw.Draw(L)
        for i in range(10):
            u = clamp((t - tv - i * 0.06) / 1.2); x = CX + rr.uniform(-180, 180) + u * rr.uniform(200, 500); y = 1290 + rr.uniform(-150, 150) - u * rr.uniform(200, 500)
            d.rectangle((x - 30, y - 40, x + 30, y + 40), fill=(226, 216, 192, int(230 * (1 - u))))
        can.alpha_composite(L)
    txt(can, t, tv + 0.2, (CX, 1290), 'VERLOREN', anton(110), RED); return can
def s_sources(t, w0, w1):
    can = sh(photo('h42', t, w0, w1, 1, 0.45, 1.04))
    txt(can, t, w('Biografen') - 0.05, (CX, Y1), 'SEINE BIOGRAFEN', bebas(64), CREAM)
    txt(can, t, w('anderen') - 0.1, (CX, Y2 + 20), 'ANDERE QUELLEN', anton(100), YEL); return can
def s_lists(t, w0, w1):     # claims vs Soviet loss lists: rows get ticks or red question marks
    can = plain(); f = typew(40)
    label(can, t, w0, 260, 560, 'MELDUNGEN', 52, YEL, 'mm'); label(can, t, w0 + 0.2, 720, 560, 'SOWJ. VERLUSTE', 52, RED, 'mm')
    rr = np.random.default_rng(5)
    for i in range(9):
        ti = w0 + 0.3 + i * 0.12
        if t < ti: break
        y = 660 + i * 80; L = L_(); d = ImageDraw.Draw(L)
        d.rectangle((100, y - 26, 420, y + 26), fill=(226, 216, 192, 230)); d.rectangle((560, y - 26, 880, y + 26), fill=(226, 216, 192, 230))
        for j in range(5): d.line((120 + j * 60, y, 158 + j * 60, y), fill=INK_ + (200,), width=3); d.line((580 + j * 60, y, 618 + j * 60, y), fill=INK_ + (200,), width=3)
        can.alpha_composite(L)
        tm = w('Einklang') - 0.4 + i * 0.1
        if t >= tm: label(can, t, tm, 490, y, '?' if i in (1, 4, 7) else '=', 54, RED if i in (1, 4, 7) else GREY, 'mm')
    txt(can, t, w('Einklang') - 0.1, (CX, Y3 + 60), 'NICHT IN EINKLANG', anton(84), WHITE); return can
def s_compare(t, w0, w1):   # 352 against the estimate of 70 to 80
    can = plain(); y0 = 1360; hmax = 640; tc = w('70') - 0.2
    k1 = eio((t - w0 - 0.2) / 1.0); L = L_(); d = ImageDraw.Draw(L)
    d.rectangle((230, y0 - hmax * k1, 430, y0), fill=YEL + (255,)); can.alpha_composite(L)
    label(can, t, w0 + 0.4, 330, y0 - hmax * k1 - 50, '352', 70, YEL, 'mm'); label(can, t, w0 + 0.4, 330, y0 + 50, 'OFFIZIELL', 40, CREAM, 'mm')
    if t >= tc:
        k2 = eio((t - tc) / 0.8); h2 = hmax * 80 / 352; L = L_(); d = ImageDraw.Draw(L)
        d.rectangle((650, y0 - h2 * k2, 850, y0), fill=RED + (255,)); can.alpha_composite(L)
        label(can, t, tc + 0.4, 750, y0 - h2 - 50, '70 BIS 80', 64, RED, 'mm'); label(can, t, tc, 750, y0 + 50, 'CHASANOW 2005', 40, CREAM, 'mm')
    txt(can, t, w('Dmitri') - 0.05, (CX, YT + 40), 'DMITRI CHASANOW', anton(84), WHITE)
    txt(can, t, w('meisten') - 0.1, (CX, 1480), 'DIE MEISTEN HISTORIKER FOLGEN IHM NICHT', bebas(52), CREAM); return can
def s_book(t, w0, w1):
    can = plain(); k = eout((t - w0 - 0.1) / 0.6); x, y = CX, 860
    L = L_(); d = ImageDraw.Draw(L); bw, bh = 300 * k, 420 * k
    d.rectangle((x - bw + 16, y - bh + 16, x + bw + 16, y + bh + 16), fill=(0, 0, 0, 120)); d.rectangle((x - bw, y - bh, x + bw, y + bh), fill=(36, 54, 88, 255))
    d.rectangle((x - bw, y - bh, x - bw + 30 * k, y + bh), fill=(24, 36, 60, 255)); can.alpha_composite(L)
    if k > 0.9:
        for s_, yy, sz in (('THE BLOND', y - 170, 70), ('KNIGHT', y - 80, 84), ('OF GERMANY', y + 10, 62)): label(can, t, w0 + 0.5, x + 10, yy, s_, sz, YEL, 'mm')
        label(can, t, w0 + 0.6, x + 10, y + 300, '1970', 50, CREAM, 'mm')
    stamp(can, t, w('einseitig') - 0.05, 'EINSEITIG', (x + 60, y + 150), RED, 84, -10)
    txt(can, t, w('Smelser') - 0.1, (CX, Y3 + 40), 'KRITIK: SMELSER UND DAVIES', anton(66), WHITE); return can
def s_grave(t, w0, w1):
    can = sh(photo('h59', t, w0, w1, 1, 0.45, 1.03), 230, 0.5)
    txt(can, t, w('Friedhof') - 0.1, (CX, Y2), 'NEUER FRIEDHOF', anton(90), WHITE)
    txt(can, t, w('Weil', 376) - 0.05, (CX, Y3 + 30), 'WEIL IM SCHÖNBUCH', bebas(62), YEL); return can
def s_ask(t, w0, w1):
    can = sh(photo('h60', t, w0, w1, 1, 0.45, 1.04), 240, 0.4)
    txt(can, t, w('Wusstet'), (CX, Y1 - 20), 'WER STECKTE WIRKLICH', anton(80), WHITE)
    txt(can, t, w('Namen', 381) - 0.05, (CX, Y2), 'HINTER DEM NAMEN', anton(80), WHITE)
    txt(can, t, w('Hartmann', 382) - 0.05, (CX, Y2 + 120), 'ERICH HARTMANN?', anton(96), YEL)
    txt(can, t, w('Schreibt'), (CX, Y3 + 120), 'SCHREIBT ES IN DIE KOMMENTARE', bebas(62), CREAM); return can

# ---- scene list: (start, scene); most scenes start on the first word of their sentence
def sw(i): return ss(i) - 0.15
SCN = [(0.0, s_352), (sw(1), s_haft), (sw(2), s_jet), (sw(3), s_name), (sw(4), s_born), (sw(5), s_parents), (sw(6), s_china),
       (w('1928') - 0.35, s_back), (sw(7), s_glider), (sw(8), s_lw), (sw(9), s_train), (sw(10), s_loop), (sw(11), s_crash1),
       (sw(12), s_ostfront), (sw(13), s_fuel), (sw(14), s_ground), (sw(15), s_rossmann), (sw(16), s_dist), (sw(17), s_quote),
       (sw(18), s_first), (sw(19), s_chart1), (sw(20), s_bubi), (sw(21), s_krupi), (sw(22), s_summer), (sw(23), s_kursk),
       (sw(24), s_method), (sw(25), s_capt), (sw(26), s_staffel), (w('Insgesamt', 150) - 0.2, s_16), (sw(27), s_never),
       (sw(28), s_rk), (sw(29), s_heart), (sw(30), s_stairs), (sw(31), s_300), (w('Forscher') - 0.2, s_crit), (sw(32), s_diamonds),
       (sw(33), s_wedding), (sw(34), s_jets), (sw(35), s_bruenn), (sw(36), s_1404), (sw(37), s_surrender), (sw(38), s_handover),
       (sw(39), s_cell), (sw(40), s_verdicts), (sw(41), s_charge), (sw(44), s_son), (sw(45), s_free), (sw(46), s_annul),
       (sw(47), s_usa), (sw(48), s_jg71), (sw(49), s_f104), (sw(51), s_retire), (sw(52), s_teacher), (sw(53), s_death),
       (sw(54), s_logbook), (sw(55), s_sources), (sw(56), s_lists), (sw(57), s_compare), (sw(59), s_book), (sw(60), s_grave), (sw(61), s_ask)]
T_VOICE = [b for w_, a, b in WORDS if w_ == 'Kommentare!'][0] + 0.18
T = T_VOICE + 1.4
OV = 0.35
SC = [(0 if i == 0 else s - OV, T if i == len(SCN) - 1 else SCN[i + 1][0] + OV, fn) for i, (s, fn) in enumerate(SCN)]
def frame(t): return assemble(SC, t, T)
def ui(im):
    im = im.convert('RGBA'); L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((0, 0, W, 290), fill=(255, 0, 0, 60)); d.rectangle((930, 680, W, 1580), fill=(255, 0, 0, 80)); d.rectangle((0, 1580, W, H), fill=(255, 0, 0, 80))
    im.alpha_composite(L); return im.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; cols = 8; P_ = Image.new('RGB', (cols * 240, ((len(ts) + cols - 1) // cols) * 427))
        for i, t in enumerate(ts):
            P_.paste(ui(frame(t)).resize((240, 427)), ((i % cols) * 240, (i // cols) * 427)); ImageDraw.Draw(P_).text(((i % cols) * 240 + 4, (i // cols) * 427 + 4), str(t), fill=(0, 255, 0))
        P_.save(B + sys.argv[2], quality=85); sys.exit()
    if sys.argv[1] == 'T': print(T, T_VOICE); sys.exit()
    if sys.argv[1] == 'still': frame(float(sys.argv[3])).save(B + sys.argv[2], quality=90); sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '8M', '-maxrate', '10M', '-bufsize', '16M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
