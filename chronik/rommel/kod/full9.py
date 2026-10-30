# Erwin Rommel, vertical version 1080x1920 of the long video (same voice, same timing, no channel logo at the end).
# Shorts/Reels safe zones: nothing important above y 290, right of x 930 between y 680 and 1580 (buttons), or below y 1580 (caption).
import sys, subprocess, re, os
from lib9 import *

TXT = open(B + 'code/script.txt').read().strip()
ST = []; _i = 0
for _s in re.split(r'(?<=[.!?])\s+', TXT): ST.append(WORDS[_i][1]); _i += len(_s.split())
def w(word, k): return wt(word, ST[k])
VEND = WORDS[-1][2]; T = VEND + 1.6
INK = (40, 32, 24); SAND = (214, 190, 140); BLUE = (110, 150, 190)
XL, XR = 70, 900                     # usable width for drawings (buttons start at x 930)

# ---------- backgrounds ----------
_rr = np.random.default_rng(9)
_n = Image.fromarray((_rr.normal(128, 30, (H // 6, W // 6))).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(4))
_yy, _xx = np.mgrid[0:H, 0:W]; _rad = np.sqrt(((_xx - CX) / (W * 0.7)) ** 2 + ((_yy - 900) / (H * 0.5)) ** 2)
_a = np.ones((H, W, 3)) * np.array(DARK, float) * (1 + 0.9 * np.clip(1 - _rad, 0, 1))[..., None] * (0.92 + 0.08 * np.asarray(_n)[..., None] / 128)
PLAIN = Image.fromarray(_a.clip(0, 255).astype(np.uint8)).convert('RGBA')
def plain(): return PLAIN.copy()
def prog(t, w0, w1): return clamp((t - w0) / (w1 - w0))

# ---------- line drawing ----------
def circ(cx, cy, r, n=48, a0=-90, a1=270):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
def lines(can, t, t0, polys, dur=1.0, col=YEL, wd=6, a=1.0):
    if t < t0 or a <= 0: return
    lens = [sum(math.dist(p[i], p[i + 1]) for i in range(len(p) - 1)) for p in polys]; goal = sum(lens) * eio((t - t0) / dur); outs = []
    for p, l in zip(polys, lens):
        if goal <= 0: break
        out = [p[0]]; acc = 0
        for i in range(len(p) - 1):
            s_ = math.dist(p[i], p[i + 1])
            if acc + s_ >= goal: f = (goal - acc) / s_ if s_ else 0; out.append((lerp(p[i][0], p[i + 1][0], f), lerp(p[i][1], p[i + 1][1], f))); break
            out.append(p[i + 1]); acc += s_
        outs.append(out); goal -= l
    shadowed(can, lambda d: [d.line(o, fill=col + (int(255 * a),), width=wd, joint='curve') for o in outs if len(o) > 1], 8, (3, 5), 160)
def shape(can, pts, fill=DARK, col=YEL, wd=5, a=1.0):
    shadowed(can, lambda d: d.polygon(pts, fill=fill + (int(255 * a),), outline=col + (int(255 * a),), width=wd), 8, (3, 5), int(150 * a))
def car(can, x, y, s=1.0, col=YEL, a=1.0):
    body = [(0, 50), (6, 24), (70, 18), (105, -16), (190, -16), (232, 18), (292, 26), (300, 50)]
    shape(can, [(x + px * s, y + py * s) for px, py in body], DARK, col, 5, a)
    for wx in (62, 236): shape(can, circ(x + wx * s, y + 52 * s, 25 * s, 24), DARK, col, 5, a)
def plane(can, x, y, s=1.0, ang=0.0, col=WHITE, a=1.0):
    body = [(-75, 0), (-50, -9), (40, -8), (62, -2), (70, 0), (62, 4), (-50, 7), (-62, -26), (-72, -26)]; wing = [(-5, 0), (25, 0), (5, 16), (-15, 16)]
    rot = lambda q: [(x + s * (px * math.cos(ang) - py * math.sin(ang)), y + s * (px * math.sin(ang) + py * math.cos(ang))) for px, py in q]
    shape(can, rot(body), DARK, col, 4, a); shape(can, rot(wing), DARK, col, 4, a)
def tank_icon(can, x, y, s=1.0, col=YEL, a=1.0):
    shape(can, [(x - 40 * s, y), (x + 40 * s, y), (x + 34 * s, y + 18 * s), (x - 34 * s, y + 18 * s)], DARK, col, 4, a)
    shape(can, [(x - 18 * s, y), (x - 14 * s, y - 16 * s), (x + 14 * s, y - 16 * s), (x + 18 * s, y)], DARK, col, 4, a)
    lines(can, 0, -1, [[(x + 14 * s, y - 9 * s), (x + 50 * s, y - 12 * s)]], 0.01, col, 4, a)
def plane_icon(can, x, y, s=1.0, col=YEL, a=1.0):
    lines(can, 0, -1, [[(x - 36 * s, y), (x + 36 * s, y)], [(x, y - 30 * s), (x, y + 26 * s)], [(x - 14 * s, y + 22 * s), (x + 14 * s, y + 22 * s)]], 0.01, col, 6, a)
def can_icon(can, x, y, s=1.0, col=YEL, a=1.0):
    shape(can, [(x - 20 * s, y - 28 * s), (x + 20 * s, y - 28 * s), (x + 20 * s, y + 28 * s), (x - 20 * s, y + 28 * s)], DARK, col, 4, a)
    lines(can, 0, -1, [[(x - 20 * s, y - 28 * s), (x + 20 * s, y + 28 * s)], [(x + 20 * s, y - 28 * s), (x - 20 * s, y + 28 * s)]], 0.01, col, 3, a)
def person(can, x, y, s=1.0, col=YEL, a=1.0):
    lines(can, 0, -1, [circ(x, y - 150 * s, 22 * s, 20), [(x, y - 128 * s), (x, y - 50 * s)], [(x - 34 * s, y - 100 * s), (x, y - 118 * s), (x + 34 * s, y - 100 * s)],
                       [(x - 26 * s, y), (x, y - 50 * s), (x + 26 * s, y)]], 0.01, col, 5, a)

# ---------- text in the safe area: one top line and three lower lines ----------
_CHAPK = (11, 23, 27, 38, 56, 67, 78, 89, 101)
def top(can, t, t0, s, size=66, col=CREAM, y=YT):
    for k in _CHAPK:     # the chapter card owns the top of the frame for its 3.4 s: the top line waits until it has faded
        if ST[k] - 0.3 <= t0 < ST[k] + 3.45: t0 = ST[k] + 3.45
    typewriter(can, t, t0, (CX, y), s, typew(size), col, 0.06)
def l1(can, t, t0, s, size=96, col=WHITE, t1=None): txt(can, t, t0, (CX, Y1), s, anton(size), col, t1)
def l2(can, t, t0, s, size=66, col=CREAM, t1=None): txt(can, t, t0, (CX, Y2), s, bebas(size), col, t1)
def l3(can, t, t0, s, size=58, col=CREAM, t1=None): txt(can, t, t0, (CX, Y3), s, bebas(size), col, t1)
def fitpt(n, t, w0, w1, z1, sx, sy):
    """screen position of a source pixel inside fit(): the photo fills the frame height, centred"""
    im = src(n); u = clamp((t - w0) / (w1 - w0)); z = lerp(1.0, z1, u); pw = im.width * H / im.height
    cw, ch = im.width / z, im.height / z; x0 = (W - pw) / 2
    return (x0 + (sx - (im.width / 2 - cw / 2)) * pw / cw, (sy - (im.height / 2 - ch / 2)) * H / ch)

# ---------- scene builders ----------
def P(n, mode='pan', d=1, ov=None, sh=0.5, grey=0.0, **kw):
    def fn(t, w0, w1):
        can = pan(n, t, w0, w1, d, **kw) if mode == 'pan' else fit(n, t, w0, w1, **kw)
        if grey: can = Image.blend(can, ImageEnhance.Color(can).enhance(0.0), grey * prog(t, w0, w1))
        if sh: shade(can, 215, sh)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
CLIPN = len([f for f in os.listdir(B + 'clip') if f.endswith('.jpg')])
@functools.lru_cache(maxsize=6)
def cframe(i): return Image.open(B + 'clip/f%05d.jpg' % max(1, min(CLIPN, i))).convert('RGB')
def C(a, b, ov=None, cx=0.5, z1=1.06, sh=0.5):
    """muted clip part, vertical crop around cx (share of the frame width), slowed down if the scene is longer"""
    def fn(t, w0, w1):
        rate = min(1.0, (b - a) / max(0.1, w1 - w0)); s_ = min(a + (t - w0) * rate, b - 0.05)
        im = cframe(int(s_ * FPS) + 1); z = lerp(1.0, z1, prog(t, w0, w1)); ch = 1080 / z; cw = ch * W / H
        x0 = min(max(cx * 1920 - cw / 2, 0), 1920 - cw); y0 = (1080 - ch) / 2
        can = im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')
        if sh: shade(can, 215, sh)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
def MAP(m, ov, z1=1.06):
    def fn(t, w0, w1):
        z = lerp(1.0, z1, prog(t, w0, w1)); can = m.frame(z); ov(can, t, w0, w1, z); return can
    return fn

# ================= INTRO =================
@functools.lru_cache(None)
def _ibg():
    im = src('r43'); s = H / (im.height * 0.8); b = im.resize((int(im.width * s), int(im.height * s)), Image.BICUBIC)
    b = b.crop((int(b.width * 0.08), int(b.height * 0.06), int(b.width * 0.08) + W, int(b.height * 0.06) + H)).filter(ImageFilter.GaussianBlur(7))
    g = ImageEnhance.Color(b).enhance(0.25); return Image.blend(g, Image.new('RGB', (W, H), (60, 48, 30)), 0.25).convert('RGBA')
MX0, MY0, MX1, MY1 = 90, 520, 880, 1010
def mp(lon, lat): return (MX0 + (lon - 9.74) / (10.06 - 9.74) * (MX1 - MX0), MY1 - (lat - 48.33) / (48.48 - 48.33) * (MY1 - MY0))
ROAD = [(10.05, 48.395), (9.99, 48.40), (9.95, 48.405), (9.92, 48.412), (9.89, 48.42)]
BLAU = [(9.76, 48.41), (9.80, 48.414), (9.84, 48.418), (9.88, 48.422), (9.92, 48.41), (9.96, 48.402), (10.0, 48.396)]
def s_intro(t, w0, w1):
    z = lerp(1.0, 1.06, prog(t, w0, w1)); b = _ibg(); cw, ch = W / z, H / z
    can = b.resize((W, H), Image.BILINEAR, box=(W / 2 - cw / 2, H / 2 - ch / 2, W / 2 + cw / 2, H / 2 + ch / 2)); dim(can, 110)
    a = clamp((t - 0.3) / 0.8); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((MX0, MY0, MX1, MY1), fill=(214, 200, 168, int(225 * a)), outline=(120, 100, 70, int(255 * a)), width=4)
    for gx in range(MX0 + 79, MX1, 79): d.line((gx, MY0, gx, MY1), fill=(160, 140, 105, int(120 * a)), width=1)
    for gy in range(MY0 + 70, MY1, 70): d.line((MX0, gy, MX1, gy), fill=(160, 140, 105, int(120 * a)), width=1)
    can.alpha_composite(L)
    lines(can, t, 0.5, [[mp(*q) for q in BLAU]], 1.2, (90, 120, 150), 4, a); lines(can, t, 0.7, [[mp(*q) for q in ROAD]], 1.2, (70, 56, 40), 6, a)
    ul, hr = mp(9.99, 48.40), mp(9.89, 48.42)
    for p_, nm, off in ((ul, 'ULM', (0, 44)), (hr, 'HERRLINGEN', (0, -46))):
        if t > 1.0: dot(can, *p_, (70, 56, 40), 9, a)
        txt(can, t, 1.0, (p_[0] + off[0], p_[1] + off[1]), nm, typew(38), INK)
    txt(can, t, 1.2, ((MX0 + MX1) / 2, MY1 - 28), 'BLAU', typew(26), (60, 90, 120))
    ta, tg, tl = ST[1] + 0.8, w('Zwei', 2), w('steigt', 4) - 0.2; path = [mp(*q) for q in ROAD]
    def along(v):
        v = clamp(v); tot = sum(math.dist(path[i], path[i + 1]) for i in range(len(path) - 1)); g = tot * v; acc = 0
        for i in range(len(path) - 1):
            s_ = math.dist(path[i], path[i + 1])
            if acc + s_ >= g: f = (g - acc) / s_; return (lerp(path[i][0], path[i + 1][0], f), lerp(path[i][1], path[i + 1][1], f))
            acc += s_
        return path[-1]
    if t > ta:
        v = eio((t - ta) / 3.0); cp = along(v); dashed(can, [along(k / 20 * v) for k in range(21)], 1.0, RED, 4, 12, 0)
        if t > tl: e = mp(9.83, 48.417); u = eio((t - tl) / 2.5); cp = (lerp(hr[0], e[0], u), lerp(hr[1], e[1], u)); dashed(can, [hr, cp], 1.0, YEL, 4, 12, 0)
        dot(can, *cp, RED, 12)
    if t > tg: ring(can, t, tg, *hr, RED, 30, False)
    top(can, t, 0.4, '14. OKTOBER 1944', 70)
    rows = [(ST[1], 'MITTAGS', 'Ein dunkler Wagen hält vor dem Haus'), (w('Zwei', 2), 'KURZ DANACH', 'Zwei Generäle steigen aus'), (ST[4], 'KURZ DARAUF', 'Der Hausherr steigt in den Wagen')]
    for i, (t0, hd, tx) in enumerate(rows):
        y = 1110 + i * 150
        if t > t0:
            lines(can, t, t0, [[(100, y - 28), (100, y + 74)]], 0.3, YEL, 4); dot(can, 100, y - 28, YEL, 8)
            txt(can, t, t0, (130, y - 28), hd, bebas(58), YEL, anchor='lm'); f = shrink(typew(36), tx, 760)
            typewriter(can, t, t0 + 0.2, (130 + f.getlength(tx) / 2, y + 30), tx, f, CREAM, 0.03)
    return can
def s_official(t, w0, w1):
    can = fit('r09', t, w0, w1, 1.1)
    can = Image.blend(can, ImageEnhance.Color(can).enhance(0.0), clamp((t - w0) / 1.2)); dim(can, 140 * clamp((t - ST[6] + 0.3) / 0.6)); shade(can, 215, 0.5)
    l1(can, t, w('tot', 5) - 0.2, 'WENIG SPÄTER IST ER TOT', 90, WHITE, ST[6] - 0.4)
    doc(can, t, ST[6] - 0.1, [('AMTLICHE MITTEILUNG', 44, INK), ('', 18, INK), ('Generalfeldmarschall Rommel', 32, INK), ('ist an den Folgen seiner', 32, INK), ('Verwundung gestorben.', 32, INK)], CX, 820, 790)
    return can
def ov_lying(can, t, w0, w1):
    l1(can, t, w('Staatsbegräbnis', 7), 'STAATSBEGRÄBNIS', 96, WHITE, ST[8] - 0.3); l2(can, t, w('Ehren', 7), 'MIT ALLEN EHREN', 64, YEL, ST[8] - 0.3)
    stamp(can, t, w('gelogen', 8), 'GELOGEN', (CX, 1180), RED, 130, -12)
def ov_name(can, t, w0, w1):
    k = 9; t2 = w('geschrieben', k)
    txt(can, t, w('Generalfeldmarschall', k), (CX, Y1 - 110), 'GENERALFELDMARSCHALL', bebas(62), YEL, t2 - 0.3)
    txt(can, t, w('Erwin', k), (CX, Y1), 'ERWIN ROMMEL', anton(120), WHITE, t2 - 0.3)
    for i, (wd, s, col) in enumerate((('geschrieben', 'GESCHRIEBEN', WHITE), ('bewundert', 'BEWUNDERT', YEL), ('gestritten', 'GESTRITTEN', RED))):
        txt(can, t, w(wd, k), (CX, Y1 - 120 + i * 125), s, anton(100), col)
def ov_who(can, t, w0, w1): l1(can, t, w('Wer', 10), 'WER WAR ER WIRKLICH?', 92); l2(can, t, w('Legende', 10), 'WIE WURDE ER ZUR LEGENDE?', 66, YEL)

# ================= K1 =================
ISO = Map(11.6, 47.3, 7.0, hi=('Italy',))
KOB = (13.58, 46.25); STU = (9.18, 48.78); ISONZO = [(13.75, 46.55), (13.6, 46.3), (13.62, 46.1), (13.6, 45.9), (13.55, 45.75)]
def ov_iso(can, t, w0, w1, z):
    k = 12; m = ISO; st, kb = m.p(*STU, z), m.p(*KOB, z)
    dot(can, *st, YEL, 12); label(can, t, w('Württemberg', k), st[0] + 24, st[1] - 40, 'WÜRTTEMBERG', 60, YEL)
    dashed(can, route([STU, (11.2, 47.6), (12.8, 46.7), KOB], m, z), eio((t - w('Abteilung', k)) / 2.0))
    lines(can, t, w('Front', k), [route(ISONZO, m, z, 8)], 0.8, RED, 9); dot(can, *kb, RED, 12)
    label(can, t, w('Berge', k), kb[0] - 30, kb[1] - 60, 'KARFREIT', 56, WHITE, 'rm')
    l2(can, t, w('Front', k), 'ITALIENISCHE FRONT', 76, RED)
def ov_sleep(can, t, w0, w1): l1(can, t, w('ohne', 13), 'FAST OHNE SCHLAF', 96)
def s_tactic(t, w0, w1):
    can = plain(); k = 14
    topo = [circ(260, 900, r, 60) for r in (130, 80)] + [circ(640, 640, r, 60) for r in (170, 110, 55)]
    lines(can, t, w0, topo, 1.2, (70, 78, 90), 3)
    for i, (x, y) in enumerate(((280, 860), (480, 760), (650, 700))):
        if t > w0 + 0.4 + i * 0.25: shape(can, [(x - 45, y - 25), (x + 45, y - 25), (x + 45, y + 25), (x - 45, y + 25)], (60, 20, 20), RED, 5)
    lines(can, t, w('frontal', k) - 0.6, [[(150, 1020), (760, 560)]], 0.6, (110, 110, 110), 4, 0.5)
    pts = [(150, 1060), (330, 1030), (500, 980), (640, 900), (760, 820), (820, 700), (800, 600), (760, 520)]
    dashed(can, pts, eio((t - w('umgehen', k)) / 2.4), YEL, 8)
    if t > w('auf', k): ring(can, t, w('auf', k), 760, 520, YEL, 46, False)
    l1(can, t, w('umgehen', k), 'UMGEHEN', 110, YEL); l2(can, t, w('frontal', k), 'STATT FRONTAL ANZUGREIFEN', 66); return can
RIDGE = [(0, 1130), (120, 1060), (230, 1000), (300, 1030), (400, 880), (480, 780), (560, 640), (600, 600), (650, 650), (740, 760), (840, 830), (1080, 960)]
def s_matajur(t, w0, w1):
    can = plain(); k = 15; lines(can, t, w0, [RIDGE], 1.6, CREAM, 6)
    lines(can, t, w0 + 0.6, [[(60, 1180), (200, 1100), (330, 1040), (430, 920), (520, 780), (600, 660)]], 1.6, YEL, 5)
    tg = w('Gipfel', k)
    if t > tg:
        u = eout((t - tg) / 0.6); lines(can, t, tg, [[(600, 600), (600, 600 - 130 * u)]], 0.3, WHITE, 6)
        shape(can, [(600, 600 - 130 * u), (690, 600 - 108 * u), (600, 600 - 86 * u)], RED, RED, 2)
    l1(can, t, w('Monte', k), 'MONTE MATAJUR', 100); l2(can, t, w('Matajur', k) + 0.2, '1.641 M', 70, YEL); return can
def s_9000(t, w0, w1):
    can = plain(); k = 16; t0 = w('9.000', k)
    top(can, t, w('eigener', k), 'NACH EIGENER DARSTELLUNG', 50, GREY)
    counter(can, t, t0, 0, 9000, (CX, 640), 230, YEL, 1.6)
    n = int(90 * eio((t - t0) / 1.6)) if t > t0 else 0
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(n): x = 155 + (i % 15) * 52; y = 830 + (i // 15) * 52; d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=CREAM + (220,)); d.rectangle((x - 9, y + 13, x + 9, y + 32), fill=CREAM + (220,))
    can.alpha_composite(L)
    l2(can, t, t0 + 0.4, 'ITALIENISCHE SOLDATEN GEFANGEN', 66, WHITE); l3(can, t, t0 + 0.8, '1 FIGUR = 100 MANN', 46, GREY); return can
def ov_pour(can, t, w0, w1):
    k = 17; t0 = w('Pour', k); x, y = fitpt('r17', t, w0, w1, 1.12, 466, 828); ring(can, t, t0, x, y, YEL, 80, False)
    l1(can, t, t0, 'POUR LE MÉRITE', 100, YEL); l2(can, t, w('höchsten', k), 'HÖCHSTER PREUSSISCHER', 60); l3(can, t, w('höchsten', k) + 0.2, 'TAPFERKEITSORDEN', 60)
GER = Map(10.1, 48.75, 2.6, hi=('Germany',))
def ov_heid(can, t, w0, w1, z):
    k = 18; m = GER
    for nm, ll, tt in (('STUTTGART', STU, w0 + 0.3), ('ULM', (9.99, 48.40), w0 + 0.5)):
        p = m.p(*ll, z); dot(can, *p, WHITE, 9); label(can, t, tt, p[0] + 22, p[1] + 4, nm, 52, WHITE)
    hp = m.p(10.15, 48.68, z); dot(can, *hp, YEL, 14); ring(can, t, w('Heidenheim', k), *hp, YEL, 40, False)
    top(can, t, w('1891', k), '1891', 90); l1(can, t, w('Heidenheim', k), 'HEIDENHEIM AN DER BRENZ', 86, YEL); l2(can, t, w('Lehrers', k), 'SOHN EINES LEHRERS', 70, WHITE)
def s_three(t, w0, w1):
    can = plain(); k = 20
    for i, (wd, lab, col) in enumerate((('schnell', 'SCHNELL SEIN', YEL), ('vorne', 'SELBST VORNE STEHEN', WHITE), ('Gegner', 'DEN GEGNER ÜBERRASCHEN', RED))):
        t0 = w(wd, k) - 0.1; y = 640 + i * 200
        lines(can, t, t0, [[(CX - 300, y + 60), (CX + 300, y + 60)]], 0.4, col, 3); txt(can, t, t0, (CX, y), lab, anton(84), col)
    top(can, t, w0 + 0.2, 'WAS IHN PRÄGTE', 60, GREY); return can

# ================= K2 =================
def s_type(t, w0, w1):
    can = plain(); doc(can, t, w0 + 0.05, [('INFANTERIE GREIFT AN', 50, INK), ('Erlebnis und Erfahrung', 32, INK), ('', 14, INK), ('von Erwin Rommel', 30, INK)], CX, 820, 800)
    top(can, t, w('Zwanzig', 21), '1937', 90); return can
def ov_book(can, t, w0, w1): stamp(can, t, w('Bestseller', 22), 'BESTSELLER', (CX, 1180), RED, 90, -10)
POL = Map(18.3, 52.0, 12.0, hi=('Poland',))
def ov_pol(can, t, w0, w1, z):
    k = 24; m = POL; top(can, t, w0 + 0.2, 'SEPTEMBER 1939', 66)
    for i, (a, b) in enumerate((((14.6, 53.6), (18.0, 53.2)), ((15.2, 51.3), (18.8, 51.6)), ((18.8, 49.6), (20.2, 50.6)), ((20.5, 54.3), (21.0, 53.2)))):
        arrow(can, m.p(*a, z), m.p(*b, z), eio((t - w('Angriff', k) - i * 0.25) / 1.0), RED, 18, 48)
    l1(can, t, w('Polen', k), 'ANGRIFF AUF POLEN', 92, YEL)
def ov_hq(can, t, w0, w1):
    k = 24; l1(can, t, w('Sicherheit', k), 'SICHERHEIT DES', 92); l2(can, t, w('Sicherheit', k) + 0.2, 'OBERSTEN HAUPTQUARTIERS', 72, WHITE); l3(can, t, w('nah', k), 'TÄGLICH NAH AN DER STAATSSPITZE', 60, YEL)
def ov_pzdiv(can, t, w0, w1): l2(can, t, w('eigenes', 25), 'EIN EIGENES KOMMANDO', 66, WHITE); l1(can, t, w('Panzerdivision', 25), '7. PANZERDIVISION', 100, YEL)
def s_units(t, w0, w1):
    can = plain(); k = 26
    for y, wd, lab, col in ((560, 'Infanterist', 'INFANTERIST', YEL), (960, 'Panzer', 'PANZER', GREY)):
        t0 = w(wd, k) - 0.1; x = CX - 160
        box = [(x - 130, y - 90), (x + 130, y - 90), (x + 130, y + 90), (x - 130, y + 90), (x - 130, y - 90)]
        inner = [[(x - 130, y - 90), (x + 130, y + 90)], [(x + 130, y - 90), (x - 130, y + 90)]] if col == YEL else \
                [[(x - 80, y - 40), (x + 80, y - 40), (x + 100, y), (x + 80, y + 40), (x - 80, y + 40), (x - 100, y), (x - 80, y - 40)]]
        lines(can, t, t0, [box] + inner, 0.8, col, 7); txt(can, t, t0 + 0.2, (x + 200, y), lab, anton(80), col, anchor='lm')
    tn = w('nie', k)
    if t > tn: lines(can, t, tn, [[(CX - 300, 860), (CX - 20, 1060)], [(CX - 20, 860), (CX - 300, 1060)]], 0.4, RED, 12)
    l2(can, t, tn + 0.3, 'NIE PANZER GEFÜHRT', 76, RED); return can

# ================= K3 =================
FR = Map(2.6, 50.0, 7.6, hi=('France', 'Belgium'))
MEUSE = [(5.6, 49.0), (5.25, 49.6), (4.95, 49.95), (4.9, 50.25), (4.85, 50.47), (5.2, 50.85)]
def ov_fr(can, t, w0, w1, z):
    k = 29; m = FR; lines(can, t, w0, [route(MEUSE, m, z, 8)], 1.0, BLUE, 7)
    p = m.p(5.05, 49.75, z); label(can, t, w0 + 0.4, p[0] - 20, p[1], 'MAAS', 50, BLUE, 'rm')
    dn = m.p(4.91, 50.26, z); dot(can, *dn, YEL, 12); label(can, t, w('Dinant', k), dn[0] - 24, dn[1] - 46, 'DINANT', 60, YEL, 'rm')
    tgt = m.p(0.75, 49.87, z); arrow(can, dn, tgt, eio((t - w('Westen', k) + 0.6) / 1.8), RED, 22, 56)
    tq = w('weiß', k)
    if t > tq and int((t - tq) * 3) % 2 == 0: txt(can, t, tq, (tgt[0] + 10, tgt[1] - 110), '?', anton(120), YEL)
    l1(can, t, w('Westen', k), '7. PANZERDIVISION', 92, WHITE); l2(can, t, tq, 'SELBST DIE EIGENE FÜHRUNG', 62); l3(can, t, tq + 0.2, 'WEISS NICHT, WO SIE STEHT', 62)
def s_ghost(t, w0, w1):
    base = pan('r19', t, w0, w1, 1); g = base.copy(); ph = (t - w0)
    for k_, dx in enumerate((18, -26)):
        sh_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh_.paste(ImageEnhance.Color(base).enhance(0.2), (int(dx * math.sin(ph * 1.7 + k_)), 0)); g = Image.blend(g, sh_, 0.22)
    g = ImageEnhance.Color(g).enhance(0.6); shade(g, 215, 0.5)
    l1(g, t, w('Gespensterdivision', 30), 'DIE GESPENSTER-', 104); l2(g, t, w('Gespensterdivision', 30) + 0.15, 'DIVISION', 100, WHITE); return g
def ov_front(can, t, w0, w1): l1(can, t, w('vorne', 31), 'FÜHRUNG VON VORNE', 96)
def ov_valery(can, t, w0, w1):
    k = 32; l1(can, t, w('Kanalküste', k), 'AN DER KANALKÜSTE', 90); l2(can, t, w('Kanalküste', k) + 0.2, 'ST-VALERY-EN-CAUX, JUNI 1940', 58); l3(can, t, w('Cherbourg', k), 'SPÄTER: CHERBOURG', 62, YEL)
def s_bars(t, w0, w1):
    can = plain(); k = 35; base = 1020
    top(can, t, ST[33], 'DIE KEHRSEITE', 74, YEL)
    lines(can, t, w0, [[(XL, base), (XR, base)]], 0.6, GREY, 4)
    tv = w('Verluste', k); u = eout((t - tv) / 1.0) if t > tv else 0
    if u: shape(can, [(150, base), (330, base), (330, base - 420 * u), (150, base - 420 * u)], (90, 24, 26), RED, 5)
    txt(can, t, tv, (240, base - 470), '7. PZ.DIV.', bebas(54), WHITE)
    tn = w('Nachbarverbände', k); tk = w('kleinzureden', k)
    for i, x in enumerate((520, 670, 820)):
        if t > tn + i * 0.15:
            hh = 320 * eout((t - tn - i * 0.15) / 0.6) * lerp(1.0, 0.35, eio((t - tk) / 1.0)); shape(can, [(x - 55, base), (x + 55, base), (x + 55, base - hh), (x - 55, base - hh)], (50, 54, 60), GREY, 4)
    txt(can, t, tn, (670, base - 470), 'NACHBARN', bebas(54), GREY)
    l1(can, t, tv, 'HOHE VERLUSTE', 96, RED); l2(can, t, tk, 'LEISTUNG DER NACHBARN KLEINGEREDET', 60, YEL); return can
def ov_cam(can, t, w0, w1):
    k = 36; x, y = fitpt('r28', t, w0, w1, 1.06, 950, 1344); ring(can, t, w('Bilder', k), x, y, YEL, 70, False)
    l1(can, t, w('Bilder', k), 'DIE MACHT DER BILDER', 92, YEL)
def ov_report(can, t, w0, w1):
    k = 37; x, y = fitpt('r31', t, w0, w1, 1.05, 154, 317); ring(can, t, w('Kameras', k), x, y, YEL, 80, False)
    l1(can, t, w('Kameras', k), 'KAMERAS', 100, WHITE); l2(can, t, w('Kriegsberichterstatter', k), 'UND KRIEGSBERICHTERSTATTER', 66, YEL)
def s_leader(t, w0, w1):
    can = plain(); u = t - w0; n = 3 - int(u / 0.4); cy = 900
    if n >= 1:
        L = Image.new('RGBA', (W, H), (28, 26, 22, 255)); d = ImageDraw.Draw(L)
        d.line((CX, 0, CX, H), fill=(90, 86, 78, 255), width=3); d.line((0, cy, W, cy), fill=(90, 86, 78, 255), width=3)
        for r in (300, 340): d.ellipse((CX - r, cy - r, CX + r, cy + r), outline=(200, 194, 180, 255), width=5)
        a = (u % 0.4) / 0.4 * 360; d.pieslice((CX - 300, cy - 300, CX + 300, cy + 300), -90, -90 + a, fill=(60, 56, 50, 255))
        d.text((CX, cy), str(n), font=anton(380), fill=(230, 224, 210, 255), anchor='mm'); can.alpha_composite(L)
    else: txt(can, t, w0 + 1.2, (CX, 820), 'ROMMEL', anton(200), WHITE); l2(can, t, w0 + 1.4, 'IN DER HEIMAT BEKANNT', 76, YEL)
    return can

# ================= K4 =================
def ov_libya(can, t, w0, w1): top(can, t, w0 + 0.3, 'FEBRUAR 1941', 70); l1(can, t, w0 + 0.6, 'LANDUNG IN LIBYEN', 96)
def ov_dak(can, t, w0, w1):
    k = 39; l2(can, t, w('italienischen', k), 'ITALIENISCHE TRUPPEN', 66, WHITE, w('Afrikakorps', k) - 0.6); l3(can, t, w('italienischen', k) + 0.2, 'VOR DEM ZUSAMMENBRUCH', 62, CREAM, w('Afrikakorps', k) - 0.6)
    l1(can, t, w('Afrikakorps', k) - 0.3, 'DEUTSCHES AFRIKAKORPS', 92, YEL)
def s_order(t, w0, w1):
    can = dim(fit('r01', t, w0, w1, 1.06), 150); k = 40
    doc(can, t, w('Auftrag', k), [('BEFEHL', 50, INK), ('', 14, INK), ('VERTEIDIGEN', 44, INK), ('UND ABWARTEN', 44, INK)], CX, 820, 640); return can
def ov_trotz(can, t, w0, w1): l1(can, t, w('trotzdem', 41), 'TROTZDEM: ANGRIFF', 100, YEL)
LIB = Map(22.4, 30.6, 9.5, hi=('Libya',))
TOB = (23.96, 32.08)
def ov_lib(can, t, w0, w1, z):
    m = LIB; k = 42; a, b = m.p(19.6, 30.4, z), m.p(25.0, 31.4, z)
    p = m.p(20.6, 29.6, z); label(can, t, w0, p[0], p[1], 'LIBYEN', 76, GREY, 'mm')
    lines(can, t, w0 + 0.2, [[m.p(25.0, 31.6, z), m.p(25.0, 27.0, z)]], 0.8, (150, 150, 150), 4)
    arrow(can, a, b, eio((t - w('jagt', k)) / 1.6), RED, 22, 56)
    tb = m.p(*TOB, z); dot(can, *tb, YEL, 12)
    if t > w('Tobruk', 43): ring(can, t, w('Tobruk', 43), *tb, YEL, 48, False)
    label(can, t, w('Tobruk', 43), tb[0] - 30, tb[1] - 70, 'TOBRUK', 80, YEL, 'rm')
    l2(can, t, w('Grenze', k), 'BIS AN DIE GRENZE ÄGYPTENS', 64, WHITE, w('Tobruk', 43) - 0.3); l1(can, t, w('Tobruk', 43), 'NUR TOBRUK HÄLT STAND', 88, YEL)
def ov_siege(can, t, w0, w1): l1(can, t, w0 + 0.3, 'BELAGERUNG VON TOBRUK', 88); l2(can, t, w('vergeblich', 44), 'MONATELANG VERGEBLICH', 66, YEL)
def ov_supply(can, t, w0, w1): l1(can, t, w('Nachschub', 45), 'NACHSCHUB', 130, YEL)
MED = Map(22.0, 35.0, 22.0, hi=('Libya', 'Italy'))
COAST = [(13.19, 32.89), (15.1, 32.3), (17.5, 31.0), (19.4, 30.3), (20.07, 32.12), (21.8, 32.8), (23.96, 32.08), (25.15, 31.57), (27.2, 31.35), (28.95, 30.83)]
def ov_med(can, t, w0, w1, z):
    k = 46; m = MED; sea = route([(14.27, 40.85), (13.5, 38.6), (12.5, 36.5), (13.19, 32.89)], m, z)
    ts = w('Mittelmeer', k) - 0.5; u = eio((t - ts) / 1.8); dashed(can, sea, u, WHITE, 6, 20, 0)
    if 0 < u: i = min(len(sea) - 2, int(u * (len(sea) - 1))); p0, p1 = sea[i], sea[i + 1]; ship(can, *p0, math.atan2(p1[1] - p0[1], p1[0] - p0[0]), 50)
    for nm, ll, off, an in (('NEAPEL', (14.27, 40.85), (24, 0), 'lm'), ('TRIPOLIS', (13.19, 32.89), (-30, 50), 'lm'), ('EL ALAMEIN', (28.95, 30.83), (-20, 60), 'rm')):
        p = m.p(*ll, z); dot(can, *p, WHITE, 9); label(can, t, w0 + 0.3, p[0] + off[0], p[1] + off[1], nm, 50, WHITE, an)
    tk = w('Küstenstraße', k) - 1.2; dashed(can, route(COAST, m, z, 10), eio((t - tk) / 2.2), YEL, 7)
    top(can, t, w('Liter', k), 'JEDER LITER, JEDE GRANATE', 52)
    l1(can, t, w('Hunderte', k), 'HUNDERTE KILOMETER', 92, YEL); l2(can, t, w('Küstenstraße', k), 'ÜBER EINE EINZIGE KÜSTENSTRASSE', 60)
def ov_plan(can, t, w0, w1): l1(can, t, w('weiter', 47), 'PLANT WEITER,', 96); l2(can, t, w('Versorgung', 47), 'ALS DIE VERSORGUNG REICHT', 66, YEL)
def s_paper(t, w0, w1):
    can = plain(); u = prog(t, w0, w1); k = 49
    L = Image.new('RGBA', (860, 1000), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.rectangle((0, 0, 860, 1000), fill=(226, 220, 204, 255))
    d.line((40, 110, 820, 110), fill=INK + (255,), width=4); d.line((40, 118, 820, 118), fill=INK + (255,), width=1)
    hl = 'THE DESERT FOX'; n = int(clamp((t - w('Spitznamen', k)) / 0.9) * len(hl)) if t > w('Spitznamen', k) else 0
    d.text((430, 230), hl[:n], font=anton(118), fill=INK + (255,), anchor='mm')
    for c in range(2):
        for r_ in range(18): d.rectangle((40 + c * 400, 360 + r_ * 32, 40 + c * 400 + 360 - (r_ % 4 == 3) * 130, 374 + r_ * 32), fill=(150, 144, 130, 255))
    L = L.rotate(lerp(-4, -2, u), expand=True, resample=Image.BICUBIC); sc = lerp(0.9, 1.0, u); L = L.resize((int(L.width * sc), int(L.height * sc)), Image.BICUBIC)
    cy = 860; sh_ = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh_.paste((0, 0, 0, 150), (int(CX - L.width / 2 + 14), int(cy - L.height / 2 + 22)), L.getchannel('A'))
    can.alpha_composite(sh_.filter(ImageFilter.GaussianBlur(16))); can.alpha_composite(L, (int(CX - L.width / 2), int(cy - L.height / 2)))
    top(can, t, w('britischen', k), 'BRITISCHE PRESSE', 60, YEL)
    l1(can, t, w('beiden', 48), 'RUF AUF BEIDEN SEITEN', 88, WHITE, w('britischen', k) - 0.3); return can
def ov_fox(can, t, w0, w1): l1(can, t, w0 + 0.2, 'DER WÜSTENFUCHS', 112, YEL)
def ov_auch(can, t, w0, w1):
    k = 50; l2(can, t, w('Oberbefehlshaber', k), 'BRITISCHER OBERBEFEHLSHABER', 60, YEL); l1(can, t, w('Claude', k), 'CLAUDE AUCHINLECK', 90)
def s_letter(t, w0, w1):
    can = plain()
    doc(can, t, w0 + 0.05, [('AN ALLE KOMMANDEURE', 42, INK), ('', 16, INK), ('Rommel wird zu einer Art', 32, INK), ('ZAUBERER', 56, (150, 30, 30)), ('oder', 30, INK), ('SCHRECKGESPENST', 52, (150, 30, 30))], CX, 860, 800); return can
def s_strike(t, w0, w1):
    can = plain(); k = 52; txt(can, t, w0 + 0.1, (CX, 700), 'ROMMEL', anton(200), WHITE)
    lines(can, t, w('nicht', k), [[(180, 720), (860, 680)]], 0.5, RED, 22)
    txt(can, t, w('Deutschen', k) - 0.3, (CX, 1000), 'DIE DEUTSCHEN', anton(130), YEL); top(can, t, w0 + 0.2, 'NICHT MEHR VON ROMMEL SPRECHEN', 44, GREY); return can
def ov_tob42a(can, t, w0, w1): top(can, t, w0 + 0.3, 'JUNI 1942', 70); l1(can, t, w('Tobruk', 53), 'TOBRUK FÄLLT', 110, YEL)
def ov_tob42(can, t, w0, w1):
    k = 53; t0 = w('30.000', k); txt(can, t, t0 - 0.3, (CX, Y1 - 150), 'MEHR ALS', bebas(66), WHITE); counter(can, t, t0, 0, 30000, (CX, Y1 + 10), 190, YEL, 1.3); l3(can, t, t0 + 0.6, 'IN GEFANGENSCHAFT', 64, WHITE)
def ov_gfm(can, t, w0, w1): l1(can, t, w('Generalfeldmarschall', 54), 'GENERALFELDMARSCHALL', 96, YEL); l2(can, t, w('50', 55), 'MIT 50 JAHREN', 70, WHITE); l3(can, t, w('jüngste', 55), 'DER JÜNGSTE IM HEER', 66, CREAM)

# ================= K5 =================
EGY = Map(27.9, 30.6, 5.2, hi=('Egypt',))
def ov_egy(can, t, w0, w1, z):
    k = 57; m = EGY; ea, al = m.p(28.95, 30.83, z), m.p(29.92, 31.20, z)
    arrow(can, m.p(25.6, 31.3, z), (ea[0] - 30, ea[1]), eio((t - w0 - 0.2) / 1.4), RED, 22, 56)
    dot(can, *ea, YEL, 12); label(can, t, w('El', k), ea[0] - 20, ea[1] - 60, 'EL ALAMEIN', 66, YEL, 'rm')
    dot(can, *al, WHITE, 10); label(can, t, w('Alexandria', k), al[0] - 10, al[1] - 50, 'ALEXANDRIA', 52, WHITE, 'mm')
    dashed(can, [ea, al], eio((t - w('100', k)) / 0.8), WHITE, 5, 16, 0)
    lines(can, t, w('stecken', k) - 0.3, [[m.p(29.0, 30.95, z), m.p(28.4, 30.2, z), m.p(27.9, 29.5, z)]], 0.6, RED, 14)
    l1(can, t, w('100', k), 'RUND 100 KM VOR ALEXANDRIA', 78, WHITE); l2(can, t, w('stecken', k), 'DER VORMARSCH BLEIBT STECKEN', 66, RED)
def s_monty(t, w0, w1):
    can = plain(); k = 58; top(can, t, w0 + 0.1, 'AUF DER ANDEREN SEITE', 52, GREY); l1(can, t, w('Bernard', k), 'BERNARD MONTGOMERY', 92, WHITE)
    for row, (wd, lab, fn) in enumerate((('Panzer', 'PANZER', tank_icon), ('Flugzeuge', 'FLUGZEUGE', plane_icon), ('Treibstoff', 'TREIBSTOFF', can_icon))):
        t0 = w(wd, k) - 0.2; y = 600 + row * 170; txt(can, t, t0, (XL, y - 60), lab, bebas(52), YEL, anchor='lm')
        n = int(clamp((t - t0) / 2.2) * 8) if t > t0 else 0
        for i in range(n): fn(can, 120 + i * 100, y + 10, 1.0, WHITE)
    l2(can, t, w('immer', k), 'IMMER MEHR', 70, YEL); return can
def ov_battle(can, t, w0, w1): top(can, t, w0 + 0.2, 'OKTOBER 1942', 70); l1(can, t, w('nicht', 59), 'ROMMEL IST NICHT', 96, YEL); l2(can, t, w('nicht', 59) + 0.2, 'EINMAL IN AFRIKA', 76, WHITE)
EUA = Map(21.5, 39.0, 28.0, hi=('Austria',))
def ov_kur(can, t, w0, w1, z):
    k = 60; m = EUA; sm, ea = m.p(15.83, 47.63, z), m.p(28.95, 30.83, z)
    dot(can, *sm, YEL, 12); label(can, t, w('krank', k), sm[0] + 26, sm[1] - 30, 'KUR IN ÖSTERREICH', 56, YEL)
    dot(can, *ea, RED, 12); label(can, t, w0 + 0.3, ea[0] - 26, ea[1] + 50, 'EL ALAMEIN', 54, RED, 'rm')
    dashed(can, route([(15.83, 47.63), (17.5, 40.0), (24.0, 34.5), (28.95, 30.83)], m, z), eio((t - w('eilt', k)) / 1.6), WHITE, 6)
    l1(can, t, w('krank', k), 'KRANK ZUR KUR', 92, WHITE); l2(can, t, w('eilt', k), 'UND EILT ZURÜCK', 70, YEL)
def ov_12(can, t, w0, w1):
    k = 61; counter(can, t, w('zwölf', k), 1, 12, (CX, Y1), 170, YEL, 1.0, '{:,}', ' TAGE'); l2(can, t, w('nicht', k), 'DIE FRONT IST NICHT ZU HALTEN', 64, WHITE)
def s_order2(t, w0, w1):
    can = plain()
    doc(can, t, w0 + 0.05, [('FUNKSPRUCH AUS DEM HAUPTQUARTIER', 30, INK), ('', 16, INK), ('KEIN SCHRITT ZURÜCK', 46, INK), ('', 10, INK), ('SIEG ODER TOD', 60, (150, 30, 30))], CX, 860, 820); return can
def ov_retreat(can, t, w0, w1): l2(can, t, w('zögert', 63), 'EIN TAG ZÖGERN', 70, WHITE); l1(can, t, w('zieht', 63), 'DANN DER RÜCKZUG', 96, YEL)
NA = Map(19.8, 33.5, 20.0, hi=('Tunisia',))
def ov_tun(can, t, w0, w1, z):
    k = 64; m = NA; path = route(list(reversed(COAST)) + [(11.1, 33.6), (10.2, 36.8)], m, z, 10)
    dashed(can, path, eio((t - w0 - 0.2) / 3.0), RED, 8)
    tn = m.p(10.18, 36.8, z); dot(can, *tn, YEL, 12); label(can, t, w('Tunesien', k), tn[0] + 30, tn[1] - 20, 'TUNESIEN', 64, YEL)
    top(can, t, w('Mai', k), 'MAI 1943', 72); l1(can, t, w('kapitulieren', k), 'KAPITULATION', 110, WHITE)
def s_250(t, w0, w1):
    can = plain(); k = 65; t0 = w('250.000', k) - 0.2
    counter(can, t, t0, 0, 250000, (CX, 560), 190, YEL, 1.5)
    n = int(clamp((t - t0) / 1.8) * 50) if t > t0 else 0
    for i in range(n): person(can, 110 + (i % 10) * 82, 860 + (i // 10) * 70 + 40, 0.38, CREAM, 0.85)
    l1(can, t, t0 + 0.3, 'IN GEFANGENSCHAFT', 92, WHITE); l3(can, t, t0 + 1.0, '1 FIGUR = 5.000 MANN', 46, GREY); return can

# ================= K6 =================
def ov_ende43(can, t, w0, w1): top(can, t, w0 + 0.5, 'ENDE 1943', 70); l1(can, t, w('Aufgabe', 67), 'EINE NEUE AUFGABE', 92)
WALL = Map(0.8, 50.0, 8.5, hi=('France',))
WALLC = [(4.3, 52.4), (3.6, 51.4), (2.5, 51.05), (1.6, 50.9), (1.6, 50.2), (0.2, 49.7), (-0.2, 49.3), (-1.2, 49.36), (-1.6, 49.65), (-1.85, 49.7), (-1.6, 48.8), (-2.5, 48.6), (-3.5, 48.8)]
def ov_wall(can, t, w0, w1, z):
    lines(can, t, w('Küste', 68) - 0.3, [route(WALLC, WALL, z, 8)], 2.2, YEL, 12)
    l1(can, t, w('Küste', 68), 'DIE KÜSTE FRANKREICHS', 88); l2(can, t, w('Landung', 68), 'GEGEN DIE ERWARTETE LANDUNG', 64, YEL)
def ov_mines(can, t, w0, w1): l1(can, t, w('Millionen', 69), 'MILLIONEN MINEN', 110, YEL)
def s_obst(t, w0, w1):
    can = plain(); k = 69; gy = 980
    lines(can, t, w0, [[(0, gy), (W, gy)]], 0.6, SAND, 5)
    wave = [(x, 860 + 14 * math.sin(x / 50 + (t - w0) * 2)) for x in range(0, W + 1, 30)]; lines(can, t, w0, [wave], 0.01, BLUE, 4)
    for i, x in enumerate((110, 260, 410)):
        lines(can, t, w('schräge', k) + i * 0.15, [[(x, gy), (x + 110, gy - 160)], [(x + 55, gy), (x + 35, gy - 28)]], 0.4, CREAM, 9)
    for i, x in enumerate((620, 800)):
        lines(can, t, w('Stahlkreuze', k) + i * 0.15, [[(x - 65, gy), (x + 65, gy - 130)], [(x + 65, gy), (x - 65, gy - 130)], [(x, gy), (x, gy - 140)]], 0.4, GREY, 10)
    tb = w('Landungsboote', k); u = eout((t - tb) / 1.4) if t > tb else 0
    if u:
        bx = lerp(1200, 760, u); shape(can, [(bx - 120, 840), (bx + 150, 840), (bx + 170, 790), (bx - 100, 790)], DARK, WHITE, 5)
        if u > 0.95: ring(can, t, tb + 1.3, bx - 100, 820, RED, 40, True)
    txt(can, t, w('schräge', k), (260, 640), 'SCHRÄGE PFÄHLE', bebas(56), CREAM); txt(can, t, w('Stahlkreuze', k), (710, 640), 'STAHLKREUZE', bebas(56), GREY)
    l1(can, t, w('schräge', k), 'HINDERNISSE AM STRAND', 84, WHITE); l2(can, t, tb, 'GEGEN LANDUNGSBOOTE', 70, YEL); return can
def s_spargel(t, w0, w1):
    can = plain(); k = 70; gy = 1020
    lines(can, t, w0, [[(0, gy), (W, gy)]], 0.5, (120, 160, 90), 5)
    for i in range(6):
        x = 120 + i * 150; lines(can, t, w('Holzstämme', k) + i * 0.08, [[(x, gy), (x + (i % 2) * 8, gy - 200 - (i % 3) * 30)]], 0.3, SAND, 10)
    tg = w('Lastensegler', k) - 0.3; u = clamp((t - tg) / 2.0)
    if t > tg: plane(can, lerp(1150, 560, u), lerp(480, gy - 230, u), 1.4, 0.3 if u < 1 else 0.6, WHITE)
    if u >= 1: ring(can, t, tg + 2.0, 560, gy - 220, RED, 46, True)
    top(can, t, w('Wiesen', 70), 'GEGEN LASTENSEGLER', 56, GREY)
    l1(can, t, w('Rommelspargel', k), '„ROMMELSPARGEL“', 110, YEL); return can
def s_clock(t, w0, w1):
    can = plain(); k = 71; cx, cy, r = CX, 780, 300; t0 = w('24', k) - 0.4
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); a = 360 * eio((t - t0) / 2.6) if t > t0 else 0
    if a: d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, -90 + a, fill=RED + (150,))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=CREAM + (255,), width=8)
    for i in range(24):
        an = math.radians(i * 15 - 90); r0 = r - (30 if i % 6 == 0 else 16); d.line((cx + r0 * math.cos(an), cy + r0 * math.sin(an), cx + r * math.cos(an), cy + r * math.sin(an)), fill=CREAM + (255,), width=5)
    can.alpha_composite(L); txt(can, t, t0, (cx, cy), '24', anton(200), WHITE)
    l1(can, t, t0 + 0.3, 'DIE ERSTEN 24 STUNDEN', 90, YEL); l2(can, t, w('Strand', k), 'AM STRAND ENTSCHIEDEN', 70); return can
def s_tanks(t, w0, w1):
    can = plain(); cy = 520
    wave = [(x, cy + 18 * math.sin(x / 90)) for x in range(0, W + 1, 30)]; lines(can, t, w0, [wave], 0.8, BLUE, 6)
    txt(can, t, w0 + 0.3, (CX, cy - 70), 'KÜSTE', bebas(58), BLUE)
    tc = w('Küste', 72); tb = w('hinten', 73); tk = w('Kompromiss', 74)
    for i in range(4):
        x = 180 + i * 190
        if t > tc: y = lerp(640, 820, eio((t - tk) / 1.4)) if i % 2 else 640; tank_icon(can, x, y, 1.3, YEL, clamp((t - tc) / 0.4))
        if t > tb: tank_icon(can, x + 40, lerp(1060, 860, eio((t - tk) / 1.4)) if i % 2 == 0 else 1060, 1.3, GREY, clamp((t - tb) / 0.4))
    l2(can, t, tc, 'ROMMEL: PANZER AN DIE KÜSTE', 62, YEL, tk - 0.2); l3(can, t, tb, 'ANDERE: WEIT HINTEN', 62, GREY, tk - 0.2)
    l1(can, t, tk, 'EIN KOMPROMISS', 100, WHITE); return can
NOR = Map(4.8, 48.9, 15.0, hi=('France',))
def ov_dday(can, t, w0, w1, z):
    m = NOR; nb, hr = m.p(-0.6, 49.35, z), m.p(9.89, 48.42, z)
    top(can, t, w('Morgen', 75), '6. JUNI 1944', 80)
    dot(can, *nb, RED, 13); label(can, t, w('Normandie', 76), nb[0] + 10, nb[1] - 60, 'NORMANDIE', 60, RED, 'lm')
    if t > w('nicht', 76): ring(can, t, w('nicht', 76), *nb, RED, 50, True)
    dashed(can, route([(-0.6, 49.35), (4.5, 49.6), (9.89, 48.42)], m, z), eio((t - w('Herrlingen', 77) + 0.6) / 1.4), YEL, 6)
    dot(can, *hr, YEL, 13); label(can, t, w('Herrlingen', 77), hr[0] - 20, hr[1] + 60, 'HERRLINGEN', 60, YEL, 'rm')
    l1(can, t, w('nicht', 76), 'ROMMEL IST NICHT DA', 92, WHITE); l2(can, t, w('Lucie', 77), 'LUCIE ROMMEL HAT GEBURTSTAG', 64, YEL)

# ================= K7 =================
def ov_lost(can, t, w0, w1): l1(can, t, w('verloren', 78), 'DER KRIEG IST VERLOREN', 90, YEL); l2(can, t, w('offen', 78), 'SAGT ER SEINEN VORGESETZTEN', 62)
def s_strafe(t, w0, w1):
    can = plain(); gy = 960; k = 80
    lines(can, t, w0, [[(0, gy + 60), (W, gy + 60)]] + [[(x, gy + 60), (x, gy - 100)] for x in range(100, W, 240)] + [circ(x, gy - 150, 55, 30) for x in range(100, W, 240)], 1.2, (90, 120, 80), 4)
    top(can, t, w0 + 0.1, '17. JULI 1944', 74); ta = w('greift', k); th = ta + 1.6
    cx_ = lerp(-200, 300, eout((t - w0) / (th - w0 + 0.6))) if t < th + 0.6 else 300
    car(can, cx_, gy, 1.1, YEL)
    if t > ta:
        u = clamp((t - ta) / 1.8); px, py = lerp(1150, 150, u), lerp(480, 600, u); plane(can, px, py, 1.4, 0.12, WHITE)
        if 0.3 < u < 0.95: dashed(can, [(px - 60, py + 20), (cx_ + 180, gy)], 1.0, RED, 5, 14, 0)
    if t > th: ring(can, t, th, cx_ + 150, gy + 10, RED, 70, True)
    l1(can, t, w('Jagdflugzeug', k), 'TIEFFLIEGERANGRIFF', 92, WHITE); l2(can, t, w('schwer', 81), 'SCHWER AM KOPF VERLETZT', 70, RED); return can
def s_files(t, w0, w1):
    can = plain(); top(can, t, w0 + 0.1, '20. JULI 1944', 80); tv = w('Verhaftungswelle', 83)
    for i in range(5):
        t0 = tv + i * 0.22
        if t < t0: continue
        u = eout((t - t0) / 0.5); x = 170 + i * 150; y = lerp(1700, 830 + (i % 2) * 40, u)
        L = Image.new('RGBA', (260, 350), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.rectangle((0, 0, 260, 350), fill=(214, 200, 166, 255)); d.rectangle((0, 0, 260, 350), outline=(120, 100, 70, 255), width=3)
        for r_ in range(6): d.rectangle((26, 110 + r_ * 36, 234 - (r_ % 3) * 44, 124 + r_ * 36), fill=(150, 136, 110, 255))
        if i == 2 and t > w('Rommels', 84): d.text((130, 54), 'ROMMEL', font=anton(48), fill=(150, 30, 30, 255), anchor='mm')
        else: d.rectangle((36, 40, 224, 68), fill=(120, 104, 80, 255))
        L = L.rotate((i - 2) * 3, expand=True, resample=Image.BICUBIC); can.alpha_composite(L, (int(x - L.width / 2), int(y - L.height / 2)))
    if t > w('Rommels', 84): ring(can, t, w('Rommels', 84), 470, 705, RED, 110, False)
    l1(can, t, w('scheitert', 82), 'DAS ATTENTAT SCHEITERT', 86, WHITE, tv - 0.2); l1(can, t, tv, 'VERHAFTUNGSWELLE', 100, YEL); l2(can, t, w('Rommels', 84), 'AUCH ROMMELS NAME FÄLLT', 66, RED)
    return can
def ov_q(can, t, w0, w1): l1(can, t, w('Wie', 85), 'WIE VIEL WUSSTE ER?', 96); l2(can, t, w('umstritten', 85), 'BIS HEUTE UMSTRITTEN', 66, YEL)
def s_net(t, w0, w1):
    can = plain(); R, S_, V = (CX, 520), (CX - 200, 820), (CX + 160, 1080)
    def node(p, lab, sub_, t0, col):
        lines(can, t, t0, [circ(*p, 115, 48)], 0.6, col, 7); txt(can, t, t0 + 0.2, p, lab, anton(52 if len(lab) < 9 else 40), col); txt(can, t, t0 + 0.3, (p[0] + 140, p[1]), sub_, bebas(46), GREY, anchor='lm')
    node(R, 'ROMMEL', '', w0 + 0.1, YEL); node(S_, 'SPEIDEL', 'STABSCHEF', w('Speidel', 86) - 0.4, WHITE); node(V, 'VERSCHWÖRER', '', w('Verschwörern', 86) - 0.4, RED)
    lines(can, t, w('Speidel', 86), [[(R[0] - 70, R[1] + 92), (S_[0] + 60, S_[1] - 100)]], 0.5, WHITE, 6)
    lines(can, t, w('Kontakt', 86), [[(S_[0] + 80, S_[1] + 85), (V[0] - 85, V[1] - 80)]], 0.5, RED, 6)
    to = w('Ob', 87)
    if t > to:
        dashed(can, [(R[0] + 100, R[1] + 60), (R[0] + 250, 800), (V[0] + 50, V[1] - 112)], eio((t - to) / 1.0), GREY, 5, 16, 0)
        txt(can, t, to + 0.6, (R[0] + 300, 790), '?', anton(120), YEL)
    l2(can, t, w('Kontakt', 86), 'KONTAKT ZU DEN VERSCHWÖRERN', 60, WHITE, w('belegen', 87) - 0.3); l1(can, t, w('belegen', 87), 'NICHT BELEGT', 100, YEL); return can
def s_verdacht(t, w0, w1):
    can = plain(); k = 88
    doc(can, t, w0 + 0.05, [('BERLIN, 1944', 34, INK), ('', 14, INK), ('Betr.: Generalfeldmarschall', 32, INK), ('Erwin Rommel', 40, INK)], CX, 820, 760)
    stamp(can, t, w('Verdacht', k), 'VERDACHT', (CX + 40, 900), RED, 110, -10); l2(can, t, w('Führung', k), 'FÜR BERLIN GENUG', 70, WHITE); return can

# ================= K8 =================
GER2 = Map(9.93, 48.42, 1.2, hi=('Germany',))
def ov_back(can, t, w0, w1, z):
    m = GER2; ul, hr = m.p(9.99, 48.40, z), m.p(9.89, 48.42, z)
    dot(can, *ul, WHITE, 9); label(can, t, w0 + 0.3, ul[0] + 24, ul[1] + 30, 'ULM', 54, WHITE)
    dot(can, *hr, YEL, 14); ring(can, t, w('Herrlingen', 89), *hr, YEL, 44, False); label(can, t, w('Herrlingen', 89), hr[0] - 40, hr[1] - 60, 'HERRLINGEN', 66, YEL, 'rm')
    top(can, t, w('14.', 89), '14. OKTOBER 1944', 74); l1(can, t, w('wieder', 89), 'ZURÜCK IN HERRLINGEN', 90)
def s_generals(t, w0, w1):
    can = plain(); k = 91
    for i, (wd, nm) in enumerate((('Wilhelm', 'WILHELM BURGDORF'), ('Ernst', 'ERNST MAISEL'))):
        t0 = w(wd, k) - 0.3; y = 640 + i * 230
        txt(can, t, t0, (CX, y), nm, anton(104), WHITE); txt(can, t, t0 + 0.2, (CX, y + 85), 'GENERAL', bebas(50), GREY)
    l1(can, t, w('Wahl', k), 'BRINGEN ROMMEL EINE WAHL', 86, YEL); return can
def s_choice(t, w0, w1):
    can = plain(); k = 92; tg = w('Wählt', 93)
    lines(can, t, w0, [[(XL + 40, 900), (XR - 40, 900)]], 0.6, GREY, 4)
    dl = 1 - 0.65 * eio((t - tg) / 0.8); L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    txt(L, t, w('Prozess', k), (CX, 520), 'PROZESS', anton(110), WHITE); txt(L, t, w('Volksgerichtshof', k), (CX, 640), 'VOLKSGERICHTSHOF', bebas(66), CREAM)
    txt(L, t, w('Folgen', k), (CX, 730), 'FOLGEN FÜR FAMILIE UND STAB', bebas(56), GREY)
    if dl < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * dl)))
    can.alpha_composite(L)
    txt(can, t, w('Gift', k), (CX, 1010), 'GIFT', anton(130), RED)
    l2(can, t, w('Frau', 93), 'FRAU UND SOHN GESCHONT', 66, WHITE); l3(can, t, w('Staatsbegräbnis', 93), 'STAATSBEGRÄBNIS', 66, YEL)
    top(can, t, w('Entweder', k), 'ENTWEDER ODER', 56, GREY); return can
def ov_farewell(can, t, w0, w1): l1(can, t, w('Lucie', 94), 'ABSCHIED VON LUCIE', 88); l2(can, t, w('Manfred', 94), 'UND SOHN MANFRED (15)', 70, YEL)
def s_capsule(t, w0, w1):
    can = plain(); tk = w('Kapsel', 95)
    if t > tk:
        u = eout((t - tk) / 0.5); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); cx, cy = CX, 820
        d.rounded_rectangle((cx - 120 * u, cy - 44 * u, cx + 120 * u, cy + 44 * u), radius=int(44 * u) + 1, fill=(220, 220, 210, 255), outline=WHITE + (255,), width=4)
        d.line((cx, cy - 44 * u, cx, cy + 44 * u), fill=(150, 150, 140, 255), width=4); can.alpha_composite(L)
    top(can, t, w0 + 0.3, 'KURZ HINTER DEM ORT', 60); l1(can, t, w('Zyankali', 95), 'ZYANKALI', 130, RED); return can
def ov_ulm(can, t, w0, w1):
    k = 96; top(can, t, w0 + 0.3, 'ULM, 18. OKTOBER 1944', 62)
    l2(can, t, w('Trauerrede', k) - 0.6, 'TRAUERREDE', 66, YEL); l1(can, t, w('Gerd', k), 'GERD VON RUNDSTEDT', 90)
def s_quote(t, w0, w1):
    can = plain(); k = 97
    for i, (s, ww) in enumerate((('„EIN HELD,', 'Helden'), ('DER SEINEN', 'Helden'), ('VERWUNDUNGEN', 'Verwundungen'), ('ERLEGEN SEI“', 'Verwundungen'))):
        typewriter(can, t, w(ww, k) - 0.3 + (i % 2) * 0.5, (CX, 640 + i * 120), s, typew(80), CREAM, 0.05)
    top(can, t, w0 + 0.2, 'DIE OFFIZIELLE VERSION', 54, GREY)
    lines(can, t, w('erlegen', k) + 0.6, [[(120, 700), (900, 1000)]], 0.5, RED, 10); return can
def ov_mask(can, t, w0, w1): l1(can, t, w('Totenmaske', 98), 'TOTENMASKE', 120, WHITE)
def s_vitrine(t, w0, w1):
    can = plain(); k = 99; cx = CX
    lines(can, t, w0, [[(cx - 220, 920), (cx - 220, 500), (cx + 220, 500), (cx + 220, 920), (cx - 220, 920)], [(cx - 260, 920), (cx + 260, 920), (cx + 260, 1000), (cx - 260, 1000), (cx - 260, 920)],
                       [(cx - 190, 530), (cx - 140, 580)]], 1.0, CREAM, 5)
    lines(can, t, w0 + 0.6, [circ(cx, 700, 110, 40), [(cx - 45, 680), (cx - 15, 680)], [(cx + 15, 680), (cx + 45, 680)], [(cx, 695), (cx - 8, 745), (cx + 8, 745)], [(cx - 30, 780), (cx + 30, 780)]], 1.0, GREY, 4)
    top(can, t, w('Rommel-Museums', k), 'ROMMEL-MUSEUM HERRLINGEN', 52)
    l1(can, t, w('jahrzehntelang', k), 'JAHRZEHNTELANG', 96, WHITE, w('2019', k) - 0.2)
    stamp(can, t, w('2019', k), '2019 GESCHLOSSEN', (CX, Y1), RED, 70, -6)
    l2(can, t, w('überholt', k), 'DIE AUSSTELLUNG GALT ALS ÜBERHOLT', 60, WHITE); return can
def s_manfred(t, w0, w1):
    can = plain(); k = 100; u = (t - w0) / 3.0 % 1.6
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); x = lerp(-600, 1700, u / 1.6)
    d.polygon([(x, 0), (x + 260, 0), (x - 140, H), (x - 400, H)], fill=(255, 240, 200, 26)); can.alpha_composite(L.filter(ImageFilter.GaussianBlur(30)))
    top(can, t, w('Wahrheit', k), 'DIE WAHRHEIT KOMMT ANS LICHT', 50, YEL)
    txt(can, t, w('Manfred', k), (CX, 760), 'MANFRED', anton(150), WHITE); txt(can, t, w('Manfred', k) + 0.1, (CX, 920), 'ROMMEL', anton(150), WHITE)
    l2(can, t, w('Oberbürgermeister', k), 'SPÄTER OBERBÜRGERMEISTER', 66, CREAM); l3(can, t, w('Stuttgart', k), 'VON STUTTGART', 66, YEL); return can

# ================= K9 =================
def ov_1945(can, t, w0, w1): top(can, t, w0 + 0.5, 'NACH 1945', 74); l1(can, t, w('Ruhm', 101), 'DER RUHM WÄCHST', 96); l2(can, t, w('Gegner', 101), 'DURCH DIE FRÜHEREN GEGNER', 64, YEL)
def s_books(t, w0, w1):
    can = plain(); k = 102; tb = w('Bücher', k) - 0.4
    cols = [(150, 40, 40), (40, 70, 110), (200, 170, 90), (60, 90, 60), (120, 100, 80)]
    for i in range(5):
        t0 = tb + i * 0.18
        if t < t0: continue
        y = lerp(-200, 760 - i * 62, eout((t - t0) / 0.5)); x0 = 140 + (i % 2) * 20; shape(can, [(x0, y), (x0 + 330, y), (x0 + 330, y + 56), (x0, y + 56)], cols[i], CREAM, 3)
    txt(can, t, tb, (320, 420), 'BÜCHER', anton(80), WHITE)
    th = w('Hollywood', k)
    if t > th:
        off = ((t - th) * 160) % 150; L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); X0, Y0, X1, Y1_ = 540, 880, 900, 1080
        d.rectangle((X0, Y0, X1, Y1_), fill=(20, 20, 22, 255))
        for j in range(-1, 4): x = X0 + j * 130 - off * 0.87; d.rectangle((x + 12, Y0 + 32, x + 118, Y1_ - 32), outline=(200, 194, 180, 255), width=3)
        for j in range(-1, 12): x = X0 + j * 36 - (off * 0.8) % 36; d.rectangle((x, Y0 + 8, x + 16, Y0 + 22), fill=(200, 194, 180, 255)); d.rectangle((x, Y1_ - 22, x + 16, Y1_ - 8), fill=(200, 194, 180, 255))
        m_ = Image.new('L', (W, H), 0); ImageDraw.Draw(m_).rectangle((X0, Y0, X1, Y1_), fill=int(255 * clamp((t - th) / 0.4)))
        L.putalpha(Image.fromarray(np.minimum(np.asarray(L.getchannel('A')), np.asarray(m_)))); can.alpha_composite(L)
        txt(can, t, th, (720, 820), 'HOLLYWOOD', anton(70), YEL)
    l1(can, t, w('Großbritannien', k), 'IN GROSSBRITANNIEN', 86, WHITE, th - 0.2); l1(can, t, th, 'HOLLYWOOD DREHT EINEN FILM', 76, YEL); return can
def ov_fair(can, t, w0, w1): l1(can, t, w('fairen', 103), '„DER FAIRE KRIEG', 92, YEL); l2(can, t, w('Wüste', 103), 'IN DER WÜSTE“', 80, YEL)
def ov_sand(can, t, w0, w1): l1(can, t, w('keine', 103), '„KEINE IDEOLOGIE,', 88, WHITE); l2(can, t, w('nur', 103), 'NUR ZWEI ARMEEN IM SAND“', 70, WHITE)
def s_kaserne(t, w0, w1):
    can = plain(); k = 104; gy = 1060
    lines(can, t, w0, [[(0, gy), (W, gy)], [(110, gy), (110, 640), (200, 640), (200, gy)], [(740, gy), (740, 640), (830, 640), (830, gy)], [(200, 1000), (740, 1000)], [(200, 880), (740, 880)]], 1.2, CREAM, 6)
    for x in range(240, 740, 55): lines(can, t, w0 + 0.8, [[(x, 880), (x, 1000)]], 0.4, GREY, 4)
    tk = w('Kasernen', k)
    if t > tk:
        u = eout((t - tk) / 0.5); shape(can, [(140, 560 - 40 * u), (800, 560 - 40 * u), (800, 560 + 40 * u), (140, 560 + 40 * u)], (40, 44, 50), WHITE, 4)
        if u > 0.9: txt(can, t, tk + 0.4, (470, 560), 'ROMMEL-KASERNE', anton(60), WHITE)
    top(can, t, w('Bundeswehr', k), 'DIE NEUE BUNDESWEHR', 60, YEL); l1(can, t, w('Vorbilder', k), 'SUCHT VORBILDER', 96, WHITE); return can
def ov_krit(can, t, w0, w1): l2(can, t, w('Historiker', 105), 'HISTORIKER HEUTE:', 70, WHITE); l1(can, t, w('kritischer', 105), 'DEUTLICH KRITISCHER', 92, YEL)
RANKS = [('1939', 'GENERALMAJOR'), ('1941', 'GENERALLEUTNANT'), ('1941', 'GENERAL DER PANZERTRUPPE'), ('1942', 'GENERALOBERST'), ('1942', 'GENERALFELDMARSCHALL')]
def s_stairs(t, w0, w1):
    can = plain(); k = 106; t0 = w('steilen', k) - 0.3
    for i, (yr, rk) in enumerate(RANKS):
        ti = t0 + i * 0.55; x = 90 + i * 90; y = 1060 - i * 115
        lines(can, t, ti, [[(x, y + 115 if i else 1120), (x, y), (x + 90, y)]], 0.4, YEL if i == 4 else CREAM, 7)
        txt(can, t, ti + 0.1, (x + 110, y - 4), yr + '  ' + rk, bebas(46), YEL if i == 4 else WHITE, anchor='lm')
    top(can, t, w0 + 0.2, 'STEILER AUFSTIEG', 64, YEL); l1(can, t, w('nahe', k), 'UND STAND IHR LANGE NAHE', 80, WHITE); return can
def ov_civ(can, t, w0, w1): l2(can, t, w('weniger', 107), '„WENIGER BRUTAL“ ALS IM OSTEN', 64, WHITE); l1(can, t, w('Zivilisten', 107), 'AUCH DORT LITTEN ZIVILISTEN', 80, YEL)
TUNM = Map(9.6, 35.0, 6.0, hi=('Tunisia',))
def ov_tunj(can, t, w0, w1, z):
    k = 107; m = TUNM; tn = m.p(10.18, 36.8, z); dot(can, *tn, YEL, 12); label(can, t, w0 + 0.2, tn[0] - 26, tn[1] - 10, 'TUNIS', 60, YEL, 'rm')
    label(can, t, w0 + 0.3, m.p(9.0, 35.9, z)[0], m.p(9.0, 35.9, z)[1], 'TUNESIEN', 90, GREY, 'mm')
    l2(can, t, w('Juden', k), 'JUDEN UNTER DEUTSCHER BESATZUNG', 60, WHITE); l1(can, t, w('Zwangsarbeit', k), 'ZWANGSARBEIT', 110, RED)
def ov_resp(can, t, w0, w1): l2(can, t, w('Verantwortlich', 108), 'VERANTWORTLICH: ANDERE DIENSTSTELLEN', 60, WHITE); l1(can, t, w('nicht', 108), 'NICHT ROMMELS STAB', 90, YEL)
def ov_open(can, t, w0, w1): l1(can, t, w('offen', 109) - 0.3, 'WAS ER WUSSTE: OFFEN', 90, YEL)
def s_minefield(t, w0, w1):
    can = plain(); k = 110; gy = 700
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.rectangle((0, gy, W, 1090), fill=(70, 60, 40, int(255 * clamp((t - w0) / 0.6)))); can.alpha_composite(L)
    lines(can, t, w0, [[(x, gy + 6 * math.sin(x / 70)) for x in range(0, W + 1, 30)]], 0.8, SAND, 6)
    tm = w('Minen', k)
    for i, (x, y) in enumerate(((150, 840), (380, 930), (600, 830), (820, 940), (260, 1040), (700, 1040))):
        if t > tm + i * 0.15:
            a = clamp((t - tm - i * 0.15) / 0.3); shape(can, [(x - 65, y), (x - 46, y - 24), (x + 46, y - 24), (x + 65, y), (x + 46, y + 15), (x - 46, y + 15)], (40, 40, 36), GREY, 4, a)
            lines(can, t, tm + i * 0.15, [[(x, y - 24), (x, gy)]], 0.3, (120, 110, 90), 3)
    top(can, t, w('Nordafrika', k), 'MINEN IN NORDAFRIKA', 62, WHITE); l1(can, t, w('heute', k), 'BIS HEUTE IM BODEN', 96, YEL); return can
def s_memorial(t, w0, w1):
    can = plain(); k = 111; gy = 1080
    lines(can, t, w0, [[(0, gy), (W, gy)], [(170, gy), (170, 560), (450, 560), (450, gy)], [(140, 560), (480, 560)], [(140, 530), (480, 530), (480, 560)]], 1.2, CREAM, 6)
    txt(can, t, w('Denkmal', k), (310, 820), 'DENKMAL', bebas(56), CREAM)
    tf = w('Figur', k)
    if t > tf:
        a = clamp((t - tf) / 0.6); x = 690
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = (20, 20, 22, int(255 * a)); o = YEL + (int(255 * a),)
        d.ellipse((x - 40, 690, x + 40, 770), fill=c, outline=o, width=4); d.polygon([(x - 55, 790), (x + 55, 790), (x + 45, 940), (x - 45, 940)], fill=c, outline=o, width=4)
        d.polygon([(x - 40, 940), (x - 8, 940), (x - 14, gy), (x - 40, gy)], fill=c, outline=o, width=4); d.polygon([(x + 8, 940), (x + 40, 940), (x + 36, gy), (x + 14, gy)], fill=c, outline=o, width=4)
        can.alpha_composite(L)
    top(can, t, w('Heidenheim', k), 'HEIDENHEIM, SEIT 2020', 60); l1(can, t, tf, 'FIGUR EINES MINENOPFERS', 84, YEL); return can
def ov_officer(can, t, w0, w1): l1(can, t, w('vorne', 112), 'FÜHRTE VON VORNE', 96); l2(can, t, w('Gespür', 112), 'GESPÜR FÜR BILDER', 76, YEL)
def ov_general(can, t, w0, w1): l1(can, t, w('missachtete', 113), 'MISSACHTETE BEFEHLE', 88); l2(can, t, w('Tod', 113) - 0.3, 'VON DER EIGENEN FÜHRUNG', 66, YEL); l3(can, t, w('Tod', 113), 'IN DEN TOD GEZWUNGEN', 66, YEL)
def s_ask(t, w0, w1):
    can = plain(); k = 114
    txt(can, t, w('Wie', k), (CX, 640), 'WIE SEHT IHR', anton(110), WHITE); txt(can, t, w('Erwin', k), (CX, 800), 'ERWIN ROMMEL?', anton(130), YEL)
    l1(can, t, w('Schreibt', 115), 'SCHREIBT ES IN DIE', 80, CREAM); l2(can, t, w('Schreibt', 115) + 0.2, 'KOMMENTARE', 80, CREAM); return can

# ---------- timeline (identical anchors to the 16:9 version) ----------
def at(k, word=None): return (ST[k] if word is None else w(word, k)) - 0.15
ANCH = [
 (0.0, s_intro),
 (at(5), s_official), (at(7), P('r41', 'pan', 1, ov_lying)),
 (at(9), P('r12', 'fit', ov=ov_name, z1=1.08)), (at(10), P('r43', 'fit', ov=ov_who, z1=1.08)),
 (at(11), P('r11', 'fit', ov=lambda c, t, a, b: top(c, t, w('1917', 11), 'OKTOBER 1917', 70), z1=1.06)), (at(12), MAP(ISO, ov_iso)), (at(13), P('r04', 'pan', -1, ov_sleep)),
 (at(14), s_tactic), (at(15), s_matajur), (at(16), s_9000), (at(17), P('r17', 'fit', ov=ov_pour, z1=1.12)), (at(18), MAP(GER, ov_heid, 1.05)),
 (at(19), P('r16', 'fit', z1=1.06)), (at(20), s_three), (at(21), s_type), (at(22), P('r42', 'fit', ov=ov_book, z1=1.1)),
 (at(24), MAP(POL, ov_pol)), (at(24, 'Sicherheit'), P('r15', 'pan', 1, ov_hq)), (at(25), P('r13', 'pan', -1, ov_pzdiv)), (at(26), s_units),
 (at(27), P('r23', 'pan', 1, lambda c, t, a, b: (top(c, t, a + 0.5, 'MAI 1940', 72), l1(c, t, a + 0.8, 'ANGRIFF AUF FRANKREICH', 88)))), (at(28), MAP(FR, ov_fr)), (at(30), s_ghost), (at(31), P('r18', 'pan', 1, ov_front)),
 (at(32), P('r21', 'pan', -1, ov_valery)), (at(33), s_bars), (at(36), P('r28', 'fit', ov=ov_cam, z1=1.06)),
 (at(37), P('r31', 'fit', ov=ov_report)), (at(37, 'Heimat'), s_leader),
 (at(38), C(0.2, 4.1, ov_libya)), (at(39), C(8.3, 13.6, ov_dak, 0.42)), (at(40), s_order), (at(41), P('r25', 'fit', ov=ov_trotz, z1=1.1)), (at(42), MAP(LIB, ov_lib)),
 (at(44), C(33.0, 35.6, ov_siege, 0.45)), (at(45), P('r05', 'pan', 1, ov_supply)), (at(46), MAP(MED, ov_med, 1.04)), (at(47), P('r14', 'fit', ov=ov_plan)),
 (at(48), s_paper), (at(49, 'Wüstenfuchs'), P('r07', 'fit', ov=ov_fox, z1=1.1)), (at(50), C(27.3, 32.4, ov_auch)), (at(51), s_letter), (at(52), s_strike),
 (at(53), C(38.0, 40.9, ov_tob42a, 0.4)), (at(53, 'mehr'), C(41.0, 43.0, ov_tob42)), (at(54), P('r24', 'fit', ov=ov_gfm, z1=1.08)),
 (at(56), C(22.2, 27.2, None, 0.4)), (at(57), MAP(EGY, ov_egy)), (at(58), s_monty), (at(59), C(35.6, 38.0, ov_battle, 0.45)), (at(60), MAP(EUA, ov_kur, 1.04)),
 (at(61), P('r26', 'fit', ov=ov_12)), (at(62), s_order2), (at(63), P('r30', 'pan', 1, ov_retreat)), (at(64), MAP(NA, ov_tun)), (at(65), s_250), (at(66), P('r27', 'pan', -1, grey=0.8)),
 (at(67), P('r33', 'pan', 1, ov_ende43)), (at(68), MAP(WALL, ov_wall)), (at(69), P('r20', 'pan', 1, ov_mines)), (at(69, 'schräge'), s_obst), (at(70), s_spargel), (at(71), s_clock),
 (at(72), s_tanks), (at(75), MAP(NOR, ov_dday)),
 (at(78), P('r38', 'pan', -1, ov_lost)), (at(79), s_strafe), (at(82), s_files), (at(85), P('r32', 'pan', -1, ov_q)), (at(86), s_net), (at(88), s_verdacht),
 (at(89), MAP(GER2, ov_back, 1.06)), (at(91), s_generals), (at(92), s_choice), (at(94), P('r34', 'fit', ov=ov_farewell, z1=1.08)), (at(95), s_capsule),
 (at(96), P('r29', 'pan', -1, ov_ulm)), (at(97), s_quote), (at(98), P('r40', 'fit', ov=ov_mask, z1=1.1)), (at(99), s_vitrine), (at(100), s_manfred),
 (at(101), C(13.8, 18.4, ov_1945, 0.55)), (at(102), s_books), (at(103), C(4.2, 8.1, ov_fair, 0.45)), (at(103, 'Hier'), C(18.7, 22.0, ov_sand, 0.5)), (at(104), s_kaserne),
 (at(105), P('r22', 'pan', -1, ov_krit, grey=0.5)), (at(106), s_stairs), (at(107), C(55.2, 60.7, ov_civ)), (at(107, 'Tunesien'), MAP(TUNM, ov_tunj)),
 (at(108), P('r06', 'pan', 1, ov_resp)), (at(109), P('r08', 'pan', -1, ov_open)), (at(110), s_minefield), (at(111), s_memorial),
 (at(112), P('r35', 'pan', 1, ov_officer)), (at(113), P('r10', 'fit', ov=ov_general, z1=1.08)), (at(114), s_ask)]
CHAP = [(11, 1, 'EIN BERG IN DEN ALPEN'), (23, 2, 'IN DER NÄHE DER MACHT'), (27, 3, 'DIE GESPENSTERDIVISION'), (38, 4, 'DER WÜSTENFUCHS'), (56, 5, 'EL ALAMEIN'),
        (67, 6, 'DER ATLANTIKWALL'), (78, 7, 'DER 20. JULI'), (89, 8, 'DIE WAHL'), (101, 9, 'DER MYTHOS')]
OV = 0.4
SC = [(0 if i == 0 else s - OV, T if i == len(ANCH) - 1 else ANCH[i + 1][0] + OV, fn) for i, (s, fn) in enumerate(ANCH)]
def frame(t):
    act = [s for s in SC if s[0] <= t < s[1]] or [SC[-1]]
    img = act[0][2](t, act[0][0], act[0][1])
    if len(act) > 1: img = Image.blend(img, act[1][2](t, act[1][0], act[1][1]), eio((t - act[1][0]) / (act[0][1] - act[1][0])))
    img.alpha_composite(VIG)
    for k, num, title in CHAP:
        t0 = ST[k] + 0.1; chapter(img, t, t0, num, title, t0 + 2.9)
    fade = clamp(1 - t / 0.5) if t < 0.5 else clamp((t - (T - 0.9)) / 0.9)
    if fade > 0: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * fade))))
    a = np.asarray(img.convert('RGB')).astype(np.int16) + np.random.default_rng(int(t * 30)).normal(0, 3, (H, W))[..., None].astype(np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

if __name__ == '__main__':
    if sys.argv[1] == 'preview':      # with the YouTube Shorts UI zones drawn in
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); P_ = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = frame(t).convert('RGBA'); d = ImageDraw.Draw(f)
            if os.environ.get('UI'):
                d.rectangle((0, 0, W, 290), outline=(0, 255, 255, 255), width=4); d.rectangle((930, 680, W, 1580), outline=(0, 255, 255, 255), width=4); d.rectangle((0, 1580, W, H), outline=(0, 255, 255, 255), width=4)
            P_.paste(f.convert('RGB').resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P_.save(B + sys.argv[2], quality=85); sys.exit()
    if sys.argv[1] == 'list':
        for s, e, fn in SC: print(f'{s:7.2f} {e:7.2f} {getattr(fn, "__qualname__", "")}')
        sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '8M', '-maxrate', '10M', '-bufsize', '16M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
