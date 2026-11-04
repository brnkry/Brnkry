# Erwin Rommel long video 16:9 (voice vcut.wav, 549.9 s). Photos r01-r43 (no reuse), muted clip parts from erwinrommel.mov, line-draw animations.
import sys, subprocess, re
from lib import *

TXT = open(B + 'code/script.txt').read().strip()
ST = []; _i = 0
for _s in re.split(r'(?<=[.!?])\s+', TXT): ST.append(WORDS[_i][1]); _i += len(_s.split())
def w(word, k): return wt(word, ST[k])
VEND = WORDS[-1][2]; LOGO = os.environ.get('NOLOGO') is None
LOGO_T = VEND + 1.0; T = LOGO_T + 6.0 if LOGO else VEND + 1.6
INK = (40, 32, 24); SAND = (214, 190, 140); BLUE = (110, 150, 190)

# ---------- backgrounds ----------
_rr = np.random.default_rng(9)
_n = Image.fromarray((_rr.normal(128, 30, (H // 6, W // 6))).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(4))
_yy, _xx = np.mgrid[0:H, 0:W]; _rad = np.sqrt(((_xx - W / 2) / (W * 0.6)) ** 2 + ((_yy - H / 2) / (H * 0.6)) ** 2)
_a = np.ones((H, W, 3)) * np.array(DARK, float) * (1 + 0.9 * np.clip(1 - _rad, 0, 1))[..., None] * (0.92 + 0.08 * np.asarray(_n)[..., None] / 128)
PLAIN = Image.fromarray(_a.clip(0, 255).astype(np.uint8)).convert('RGBA')
def plain(): return PLAIN.copy()
def prog(t, w0, w1): return clamp((t - w0) / (w1 - w0))

# ---------- line drawing (chalk style) ----------
def circ(cx, cy, r, n=48, a0=-90, a1=270):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
def lines(can, t, t0, polys, dur=1.0, col=YEL, wd=6, a=1.0):
    """draw polylines one after another, growing over dur seconds"""
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
    for wx in (62, 236):
        shape(can, circ(x + wx * s, y + 52 * s, 25 * s, 24), DARK, col, 5, a)
def plane(can, x, y, s=1.0, ang=0.0, col=WHITE, a=1.0):
    body = [(-75, 0), (-50, -9), (40, -8), (62, -2), (70, 0), (62, 4), (-50, 7), (-62, -26), (-72, -26)]
    wing = [(-5, 0), (25, 0), (5, 16), (-15, 16)]
    rot = lambda q: [(x + s * (px * math.cos(ang) - py * math.sin(ang)), y + s * (px * math.sin(ang) + py * math.cos(ang))) for px, py in q]
    shape(can, rot(body), DARK, col, 4, a); shape(can, rot(wing), DARK, col, 4, a)
def person(can, x, y, s=1.0, col=YEL, a=1.0):
    lines(can, 9e9 * 0, -1, [circ(x, y - 150 * s, 22 * s, 20), [(x, y - 128 * s), (x, y - 50 * s)], [(x - 34 * s, y - 100 * s), (x, y - 118 * s), (x + 34 * s, y - 100 * s)],
                          [(x - 26 * s, y), (x, y - 50 * s), (x + 26 * s, y)]], 0.01, col, 5, a)
def tank_icon(can, x, y, s=1.0, col=YEL, a=1.0):
    shape(can, [(x - 40 * s, y), (x + 40 * s, y), (x + 34 * s, y + 18 * s), (x - 34 * s, y + 18 * s)], DARK, col, 4, a)
    shape(can, [(x - 18 * s, y), (x - 14 * s, y - 16 * s), (x + 14 * s, y - 16 * s), (x + 18 * s, y)], DARK, col, 4, a)
    lines(can, 0, -1, [[(x + 14 * s, y - 9 * s), (x + 50 * s, y - 12 * s)]], 0.01, col, 4, a)
def plane_icon(can, x, y, s=1.0, col=YEL, a=1.0):
    lines(can, 0, -1, [[(x - 36 * s, y), (x + 36 * s, y)], [(x, y - 30 * s), (x, y + 26 * s)], [(x - 14 * s, y + 22 * s), (x + 14 * s, y + 22 * s)]], 0.01, col, 6, a)
def can_icon(can, x, y, s=1.0, col=YEL, a=1.0):
    shape(can, [(x - 20 * s, y - 28 * s), (x + 20 * s, y - 28 * s), (x + 20 * s, y + 28 * s), (x - 20 * s, y + 28 * s)], DARK, col, 4, a)
    lines(can, 0, -1, [[(x - 20 * s, y - 28 * s), (x + 20 * s, y + 28 * s)], [(x + 20 * s, y - 28 * s), (x - 20 * s, y + 28 * s)]], 0.01, col, 3, a)

# ---------- text helpers ----------
def cap(can, t, t0, s, y=960, size=78, col=WHITE, t1=None): txt(can, t, t0, (W / 2, y), s, anton(size), col, t1)
def sub(can, t, t0, s, y=1030, size=54, col=CREAM, t1=None): txt(can, t, t0, (W / 2, y), s, bebas(size), col, t1)
def tw(can, t, t0, s, y=150, size=64, col=CREAM): typewriter(can, t, t0, (W / 2, y), s, typew(size), col, 0.06)
def fitpt(n, t, w0, w1, z1, sx, sy):
    im = src(n); u = clamp((t - w0) / (w1 - w0)); z = lerp(1.0, z1, u); pw = im.width * H / im.height
    cw, ch = im.width / z, im.height / z; x0 = (W - pw) / 2
    return (x0 + (sx - (im.width / 2 - cw / 2)) * pw / cw, (sy - (im.height / 2 - ch / 2)) * H / ch)

# ---------- photo / clip scene builders ----------
def P(n, mode='pan', d=1, ov=None, sh=0.55, grey=0.0, **kw):
    def fn(t, w0, w1):
        can = pan(n, t, w0, w1, d, **kw) if mode == 'pan' else fit(n, t, w0, w1, **kw)
        if grey: can = Image.blend(can, ImageEnhance.Color(can).enhance(0.0), grey * prog(t, w0, w1))
        if sh: shade(can, 205, sh)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
CLIPN = len([f for f in os.listdir(B + 'clip') if f.endswith('.jpg')])
@functools.lru_cache(maxsize=6)
def cframe(i): return Image.open(B + 'clip/f%05d.jpg' % max(1, min(CLIPN, i))).convert('RGB')
def C(a, b, ov=None, z1=1.08, sh=0.55):
    """muted clip part a..b s, slowed down if the scene is longer, slow push-in"""
    def fn(t, w0, w1):
        rate = min(1.0, (b - a) / max(0.1, w1 - w0)); s_ = min(a + (t - w0) * rate, b - 0.05)
        im = cframe(int(s_ * FPS) + 1); z = lerp(1.02, z1, prog(t, w0, w1)); cw, ch = W / z, H / z
        can = im.resize((W, H), Image.BICUBIC, box=(W / 2 - cw / 2, H / 2 - ch / 2, W / 2 + cw / 2, H / 2 + ch / 2)).convert('RGBA')
        if sh: shade(can, 205, sh)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
def MAP(m, ov, z1=1.08):
    def fn(t, w0, w1):
        z = lerp(1.0, z1, prog(t, w0, w1)); can = m.frame(z); ov(can, t, w0, w1, z); return can
    return fn
def A(ov):
    def fn(t, w0, w1): can = plain(); ov(can, t, w0, w1); return can
    return fn

# ================= INTRO =================
HX0, HY = 1120, 760
HOUSE = [[(HX0 - 40, HY), (HX0 + 560, HY)], [(HX0, HY), (HX0, 520), (HX0 + 500, 520), (HX0 + 500, HY)], [(HX0 - 40, 530), (HX0 + 250, 370), (HX0 + 540, 530)],
         [(HX0 + 220, HY), (HX0 + 220, 640), (HX0 + 290, 640), (HX0 + 290, HY)], [(HX0 + 60, 580), (HX0 + 150, 580), (HX0 + 150, 650), (HX0 + 60, 650), (HX0 + 60, 580)],
         [(HX0 + 360, 580), (HX0 + 450, 580), (HX0 + 450, 650), (HX0 + 360, 650), (HX0 + 360, 580)], [(HX0 + 380, 430), (HX0 + 380, 360), (HX0 + 420, 360), (HX0 + 420, 455)]]
TREE = [[(300, HY), (300, 600)], circ(300, 540, 70, 40), [(-20, HY + 60), (2000, HY + 60)]]
def house_scene(date, t_arrive, t_out=None, t_leave=None, t_gen=None):
    def ov(can, t, w0, w1):
        lines(can, t, w0 + 0.1, HOUSE + TREE, 1.6, CREAM, 5)
        tw(can, t, w0 + 0.3, date, 140, 66); txt(can, t, w0 + 1.6, (W / 2, 225), 'HERRLINGEN BEI ULM', bebas(56), YEL)
        x = lerp(-420, 700, eout((t - t_arrive) / 2.4))
        if t_leave and t > t_leave: x = lerp(700, 2200, eio((t - t_leave) / 2.6))
        car(can, x, HY - 40, 1.25, YEL)
        if t_gen and t > t_gen and (t_out is None or t < t_out + 1.2):     # two generals walk to the door
            u = eio((t - t_gen) / 2.2); a = 1.0 if t_out is None else 1 - clamp((t - t_out) / 0.8)
            for k in (0, 1): person(can, lerp(1000 + k * 70, 1300 + k * 70, u), HY, 0.9, WHITE, a)
    return A(ov)
def s_ecg(t, w0, w1):
    can = plain(); x0, x1, y = 160, 1760, 560; tt = t - w0 - 0.2
    pts = []
    for k in range(320):
        x = lerp(x0, x1, k / 319); ph = (k % 80) / 80; amp = max(0.0, 1 - k / 240)
        yy = y - amp * (260 * math.exp(-((ph - 0.5) / 0.025) ** 2) - 90 * math.exp(-((ph - 0.56) / 0.03) ** 2))
        pts.append((x, yy))
    n = int(clamp(tt / 1.7) * 319) + 1; col = RED if n > 250 else (120, 220, 140)
    if n > 1: shadowed(can, lambda d: d.line(pts[:n], fill=col + (255,), width=6, joint='curve'))
    return can
def ov_car(can, t, w0, w1):
    tw(can, t, w0 + 0.4, '14. OKTOBER 1944', 130, 76); txt(can, t, w('Herrlingen', 1), (W / 2, 215), 'HERRLINGEN BEI ULM', bebas(60), YEL)
    sub(can, t, w('dunkler', 1), 'MITTAGS: EIN DUNKLER WAGEN', 1010, 62, WHITE, ST[2] - 0.3)
    ov_two(can, t, w0, w1)
def ov_two(can, t, w0, w1): cap(can, t, w('Zwei', 2), 'ZWEI GENERÄLE', 940, 96, WHITE); sub(can, t, w('lange', 3), 'SIE BLEIBEN NICHT LANGE', 1030, 56, YEL)
def ov_leave(can, t, w0, w1): sub(can, t, w('Hausherr', 4), 'DER HAUSHERR STEIGT ZU IHNEN IN DEN WAGEN', 1010, 58, WHITE)
def s_official(t, w0, w1):
    can = fit('r09', t, w0, w1, 1.1)
    can = Image.blend(can, ImageEnhance.Color(can).enhance(0.0), clamp((t - w0) / 1.2)); dim(can, 140 * clamp((t - ST[6] + 0.3) / 0.6)); shade(can, 205, 0.55)
    cap(can, t, w('tot', 5) - 0.2, 'WENIG SPÄTER IST ER TOT', 960, 90, WHITE, ST[6] - 0.4)
    doc(can, t, ST[6] - 0.1, [('AMTLICHE MITTEILUNG', 46, INK), ('', 20, INK), ('Generalfeldmarschall Rommel', 34, INK), ('ist an den Folgen seiner', 34, INK), ('Verwundung gestorben.', 34, INK)], W / 2, 520, 900)
    return can
def ov_lying(can, t, w0, w1):
    cap(can, t, w('Staatsbegräbnis', 7), 'STAATSBEGRÄBNIS', 930, 90, WHITE, ST[8] - 0.3); sub(can, t, w('Ehren', 7), 'MIT ALLEN EHREN', 1015, 54, YEL, ST[8] - 0.3)
    stamp(can, t, w('gelogen', 8), 'GELOGEN', (W / 2, 560), RED, 140, -12)
def ov_name(can, t, w0, w1):
    k = 9; tn = w('Generalfeldmarschall', k); t2 = w('geschrieben', k)
    txt(can, t, tn, (W / 2, 830), 'GENERALFELDMARSCHALL', bebas(62), YEL, t2 - 0.3)
    txt(can, t, w('Erwin', k), (W / 2, 935), 'ERWIN ROMMEL', anton(120), WHITE, t2 - 0.3)
    words(can, t, [('GESCHRIEBEN', WHITE, t2), ('BEWUNDERT', YEL, w('bewundert', k)), ('GESTRITTEN', RED, w('gestritten', k))], 940, 92)
def ov_who(can, t, w0, w1):
    cap(can, t, w('Wer', 10), 'WER WAR ER WIRKLICH?', 900, 96); cap(can, t, w('Legende', 10), 'DIE LEGENDE', 1010, 64, YEL)

# ---- intro: archive-style local map + timeline over a blurred Rommel portrait ----
@functools.lru_cache(None)
def _ibg():
    im = src('r43'); sc = W / im.width; b = im.resize((W, int(im.height * sc)), Image.BICUBIC).crop((0, 330, W, 330 + H)).filter(ImageFilter.GaussianBlur(7))
    g = ImageEnhance.Color(b).enhance(0.25); sep = Image.new('RGB', (W, H), (60, 48, 30))
    return Image.blend(g, sep, 0.25).convert('RGBA')
MX0, MY0, MX1, MY1 = 1010, 250, 1830, 830          # map card on the right
def mp(lon, lat): return (MX0 + (lon - 9.74) / (10.06 - 9.74) * (MX1 - MX0), MY1 - (lat - 48.33) / (48.48 - 48.33) * (MY1 - MY0))
ROAD = [(10.05, 48.395), (9.99, 48.40), (9.95, 48.405), (9.92, 48.412), (9.89, 48.42)]
BLAU = [(9.76, 48.41), (9.80, 48.414), (9.84, 48.418), (9.88, 48.422), (9.92, 48.41), (9.96, 48.402), (10.0, 48.396)]
def s_intro(t, w0, w1):
    u = prog(t, w0, w1); z = lerp(1.0, 1.06, u); b = _ibg(); cw, ch = W / z, H / z
    can = b.resize((W, H), Image.BILINEAR, box=(W / 2 - cw / 2, H / 2 - ch / 2, W / 2 + cw / 2, H / 2 + ch / 2)); dim(can, 95)
    gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gl.putalpha(Image.fromarray(np.tile((np.clip(1 - np.arange(W) / 1000, 0, 1) * 150).astype(np.uint8), (H, 1)))); can.alpha_composite(gl)
    a = clamp((t - 0.3) / 0.8)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((MX0, MY0, MX1, MY1), fill=(214, 200, 168, int(225 * a)), outline=(120, 100, 70, int(255 * a)), width=4)
    for gx in range(MX0 + 82, MX1, 82): d.line((gx, MY0, gx, MY1), fill=(160, 140, 105, int(120 * a)), width=1)
    for gy in range(MY0 + 82, MY1, 82): d.line((MX0, gy, MX1, gy), fill=(160, 140, 105, int(120 * a)), width=1)
    can.alpha_composite(L)
    lines(can, t, 0.5, [[mp(*q) for q in BLAU]], 1.2, (90, 120, 150), 4, a)
    lines(can, t, 0.7, [[mp(*q) for q in ROAD]], 1.2, (70, 56, 40), 6, a)
    ul, hr = mp(9.99, 48.40), mp(9.89, 48.42)
    for p_, nm, off in ((ul, 'ULM', (0, 46)), (hr, 'HERRLINGEN', (0, -48))):
        if t > 1.0: dot(can, *p_, (70, 56, 40), 9, a)
        txt(can, t, 1.0, (p_[0] + off[0], p_[1] + off[1]), nm, typew(40), INK)
    txt(can, t, 1.2, ((MX0 + MX1) / 2, MY1 - 30), 'BLAU', typew(28), (60, 90, 120))
    # the car: arrives along the road, waits at the house, leaves again
    ta, tg, tl = ST[1] + 0.8, w('Zwei', 2), w('steigt', 4) - 0.2
    path = [mp(*q) for q in ROAD]
    def along(v):
        v = clamp(v); tot = sum(math.dist(path[i], path[i + 1]) for i in range(len(path) - 1)); g = tot * v; acc = 0
        for i in range(len(path) - 1):
            s_ = math.dist(path[i], path[i + 1])
            if acc + s_ >= g: f = (g - acc) / s_; return (lerp(path[i][0], path[i + 1][0], f), lerp(path[i][1], path[i + 1][1], f))
            acc += s_
        return path[-1]
    if t > ta:
        v = eio((t - ta) / 3.0); cp = along(v); dashed(can, [along(k / 20 * v) for k in range(21)], 1.0, RED, 4, 12, 0)
        if t > tl: cp = (lerp(hr[0], mp(9.83, 48.417)[0], eio((t - tl) / 2.5)), lerp(hr[1], mp(9.83, 48.417)[1], eio((t - tl) / 2.5))); dashed(can, [hr, cp], 1.0, YEL, 4, 12, 0)
        dot(can, *cp, RED, 12)
    if t > tg: ring(can, t, tg, *hr, RED, 30, False)
    # left: dated timeline, typed like a report
    tw(can, t, 0.4, '14. OKTOBER 1944', 120, 74)
    rows = [(ST[1], 'MITTAGS', 'Ein dunkler Wagen hält vor dem Haus'), (w('Zwei', 2), 'KURZ DANACH', 'Zwei Generäle steigen aus'), (ST[4], 'KURZ DARAUF', 'Der Hausherr steigt in den Wagen')]
    for i, (t0, hd, tx) in enumerate(rows):
        y = 400 + i * 175
        if t > t0:
            lines(can, t, t0, [[(140, y - 30), (140, y + 80)]], 0.3, YEL, 4); dot(can, 140, y - 30, YEL, 8)
            txt(can, t, t0, (175, y - 30), hd, bebas(62), YEL, anchor='lm'); typewriter(can, t, t0 + 0.2, (175 + typew(40).getlength(tx) / 2, y + 34), tx, typew(40), CREAM, 0.03)
    return can

# ================= K1 =================
ISO = Map(11.8, 47.4, 11.0, hi=('Italy',))
KOB = (13.58, 46.25); STU = (9.18, 48.78); ISONZO = [(13.75, 46.55), (13.6, 46.3), (13.62, 46.1), (13.6, 45.9), (13.55, 45.75)]
def ov_iso(can, t, w0, w1, z):
    k = 12; m = ISO; st, kb = m.p(*STU, z), m.p(*KOB, z)
    dot(can, *st, YEL, 12); label(can, t, w('Württemberg', k), st[0] + 26, st[1] - 6, 'WÜRTTEMBERG', 62, YEL)
    dashed(can, route([STU, (11.2, 47.6), (12.8, 46.7), KOB], m, z), eio((t - w('Abteilung', k)) / 2.0))
    lines(can, t, w('Front', k), [route(ISONZO, m, z, 8)], 0.8, RED, 9)
    dot(can, *kb, RED, 12); label(can, t, w('Front', k) + 0.2, kb[0] + 30, kb[1] + 50, 'ITALIENISCHE FRONT', 60, RED)
    label(can, t, w('Berge', k), kb[0] - 30, kb[1] - 60, 'KARFREIT', 56, WHITE, 'rm')
def ov_sleep(can, t, w0, w1): cap(can, t, w('ohne', 13), 'FAST OHNE SCHLAF', 960, 84)
def s_tactic(t, w0, w1):
    can = plain(); k = 14
    topo = [circ(960 + dx, 520 + dy, r, 60) for dx, dy, r in ((-420, 60, 140), (-420, 60, 90), (380, -80, 180), (380, -80, 120), (380, -80, 60), (0, 260, 110))]
    lines(can, t, w0, topo, 1.2, (70, 78, 90), 3)
    for x, y in ((700, 560), (960, 470), (1220, 520)):
        if t > w0 + 0.4 + (x - 700) / 1000: shape(can, [(x - 45, y - 25), (x + 45, y - 25), (x + 45, y + 25), (x - 45, y + 25)], (60, 20, 20), RED, 5)
    lines(can, t, w('frontal', k) - 0.6, [[(380, 820), (1500, 300)]], 0.6, (110, 110, 110), 4, 0.5)
    pts = [(380, 860), (560, 820), (720, 730), (840, 700), (960, 640), (1080, 640), (1300, 680), (1420, 600), (1500, 470), (1560, 330)]
    dashed(can, pts, eio((t - w('umgehen', k)) / 2.4), YEL, 8)
    if t > w('auf', k): ring(can, t, w('auf', k), 1560, 330, YEL, 46, False)
    cap(can, t, w('umgehen', k), 'UMGEHEN STATT ANGREIFEN', 990, 70); return can
RIDGE = [(0, 900), (220, 820), (400, 760), (520, 790), (700, 640), (860, 560), (1000, 470), (1120, 380), (1200, 340), (1290, 390), (1420, 470), (1560, 560), (1700, 600), (1920, 700)]
def s_matajur(t, w0, w1):
    can = plain(); k = 15; lines(can, t, w0, [RIDGE], 1.6, CREAM, 6)
    lines(can, t, w0 + 0.6, [[(150, 980), (400, 880), (640, 820), (860, 700), (1040, 560), (1200, 400)]], 1.6, YEL, 5)
    tg = w('Gipfel', k)
    if t > tg:
        u = eout((t - tg) / 0.6); lines(can, t, tg, [[(1200, 340), (1200, 340 - 130 * u)]], 0.3, WHITE, 6)
        shape(can, [(1200, 340 - 130 * u), (1290, 340 - 108 * u), (1200, 340 - 86 * u)], RED, RED, 2)
    txt(can, t, w('Monte', k), (1200, 130), 'MONTE MATAJUR', anton(92), WHITE); txt(can, t, w('Matajur', k) + 0.2, (1200, 205), '1.641 M', bebas(60), YEL)
    return can
def s_9000(t, w0, w1):
    can = plain(); k = 16; t0 = w('9.000', k)
    sub(can, t, w('eigener', k), 'NACH EIGENER DARSTELLUNG', 150, 54, GREY)
    n = int(90 * eio((t - t0) / 1.6)) if t > t0 else 0
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(n): x = 420 + (i % 30) * 37; y = 640 + (i // 30) * 50; d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=CREAM + (220,)); d.rectangle((x - 9, y + 13, x + 9, y + 34), fill=CREAM + (220,))
    can.alpha_composite(L)
    counter(can, t, t0, 0, 9000, (W / 2, 420), 230, YEL, 1.6); sub(can, t, t0 + 0.4, 'ITALIENISCHE SOLDATEN GEFANGEN', 870, 62, WHITE); sub(can, t, t0 + 0.8, '1 FIGUR = 100 MANN', 950, 40, GREY)
    return can
def ov_pour(can, t, w0, w1):
    k = 17; t0 = w('Pour', k); x, y = fitpt('r17', t, w0, w1, 1.12, 466, 828); ring(can, t, t0, x, y, YEL, 70, False)
    cap(can, t, t0, 'POUR LE MÉRITE', 940, 84, YEL); sub(can, t, w('höchsten', k), 'HÖCHSTER PREUSSISCHER TAPFERKEITSORDEN', 1025, 48)
GER = Map(9.9, 48.6, 4.5, hi=('Germany',))
def ov_heid(can, t, w0, w1, z):
    k = 18; m = GER
    for nm, ll, c, tt in (('STUTTGART', STU, WHITE, w0 + 0.3), ('ULM', (9.99, 48.40), WHITE, w0 + 0.5)):
        p = m.p(*ll, z); dot(can, *p, c, 9); label(can, t, tt, p[0] + 22, p[1] + 4, nm, 52, c)
    hp = m.p(10.15, 48.68, z); dot(can, *hp, YEL, 14); ring(can, t, w('Heidenheim', k), *hp, YEL, 40, False)
    label(can, t, w('Heidenheim', k), hp[0] + 60, hp[1] - 20, 'HEIDENHEIM AN DER BRENZ', 68, YEL)
    tw(can, t, w('1891', k), '1891', 150, 90); sub(can, t, w('Lehrers', k), 'SOHN EINES LEHRERS', 1000, 64, WHITE)
def s_three(t, w0, w1):
    can = plain(); k = 20
    for i, (wd, lab, col) in enumerate((('schnell', 'SCHNELL', YEL), ('vorne', 'VORNE', WHITE), ('Gegner', 'ÜBERRASCHEN', RED))):
        t0 = w(wd, k) - 0.1; x = 480 + i * 480
        if i == 0: lines(can, t, t0, [[(x - 110, 470), (x + 100, 470)], [(x + 60, 430), (x + 110, 470), (x + 60, 510)], [(x - 90, 520), (x + 40, 520)]], 0.5, col, 9)
        if i == 1:
            person(can, x, 540, 0.9, col, clamp((t - t0) / 0.4)); lines(can, t, t0, [[(x - 140, 560), (x + 140, 560)]], 0.4, col, 5)
            for j in (-1, 1): person(can, x + j * 110, 560, 0.6, GREY, clamp((t - t0) / 0.4) * 0.6)
        if i == 2: lines(can, t, t0, [[(x + 20, 360), (x - 40, 480), (x + 20, 480), (x - 30, 590)]], 0.5, col, 10)
        txt(can, t, t0, (x, 720), lab, anton(86), col)
    return can

# ================= K2 =================
def s_type(t, w0, w1):
    can = plain(); doc(can, t, w0 + 0.05, [('INFANTERIE GREIFT AN', 54, INK), ('Erlebnis und Erfahrung', 34, INK), ('', 16, INK), ('von Erwin Rommel', 32, INK)], W / 2, 500, 900)
    tw(can, t, w('Zwanzig', 21), '1937', 920, 70); return can
def ov_book(can, t, w0, w1): stamp(can, t, w('Bestseller', 22), 'BESTSELLER', (1560, 700), RED, 70, -10)
POL = Map(17.5, 51.8, 20.0, hi=('Poland',))
def ov_pol(can, t, w0, w1, z):
    k = 24; m = POL; tw(can, t, w0 + 0.2, 'SEPTEMBER 1939', 120, 66)
    for i, (a, b) in enumerate((((14.6, 53.6), (18.6, 53.2)), ((15.2, 51.3), (19.4, 51.6)), ((18.8, 49.6), (20.6, 50.6)), ((20.5, 54.3), (21.2, 53.2)))):
        arrow(can, m.p(*a, z), m.p(*b, z), eio((t - w('Angriff', k) - i * 0.25) / 1.0), RED, 18, 48)
    p = m.p(21.0, 52.23, z); label(can, t, w('Polen', k), p[0] + 20, p[1] + 60, 'POLEN', 80, YEL)
def ov_hq(can, t, w0, w1):
    k = 24; cap(can, t, w('Sicherheit', k), 'SICHERHEIT DES HAUPTQUARTIERS', 940, 76); sub(can, t, w('nah', k), 'TÄGLICH NAH AN DER STAATSSPITZE', 1025, 54, YEL)
def ov_pzdiv(can, t, w0, w1): cap(can, t, w('eigenes', 25), 'EIN EIGENES KOMMANDO', 930, 70, WHITE, w('Panzerdivision', 25) - 0.2); cap(can, t, w('Panzerdivision', 25), '7. PANZERDIVISION', 960, 100, YEL)
def s_units(t, w0, w1):
    can = plain(); k = 26
    for x, wd, lab, col in ((620, 'Infanterist', 'INFANTERIST', YEL), (1300, 'Panzer', 'PANZER', GREY)):
        t0 = w(wd, k) - 0.1; box = [(x - 180, 380), (x + 180, 380), (x + 180, 620), (x - 180, 620), (x - 180, 380)]
        inner = [[(x - 180, 380), (x + 180, 620)], [(x + 180, 380), (x - 180, 620)]] if col == YEL else \
                [[(x - 110, 450), (x + 110, 450), (x + 130, 500), (x + 110, 550), (x - 110, 550), (x - 130, 500), (x - 110, 450)]]
        lines(can, t, t0, [box] + inner, 0.8, col, 7); txt(can, t, t0 + 0.2, (x, 720), lab, anton(80), col)
    tn = w('nie', k)
    if t > tn: lines(can, t, tn, [[(1110, 370), (1490, 630)], [(1490, 370), (1110, 630)]], 0.4, RED, 12)
    sub(can, t, tn + 0.3, 'NIE GEFÜHRT', 820, 70, RED); return can

# ================= K3 =================
FR = Map(2.6, 49.9, 10.5, hi=('France', 'Belgium'))
MEUSE = [(5.6, 49.0), (5.25, 49.6), (4.95, 49.95), (4.9, 50.25), (4.85, 50.47), (5.2, 50.85)]
def ov_fr(can, t, w0, w1, z):
    k = 29; m = FR; lines(can, t, w0, [route(MEUSE, m, z, 8)], 1.0, BLUE, 7)
    p = m.p(4.95, 50.0, z); label(can, t, w0 + 0.4, p[0] + 26, p[1] + 40, 'MAAS', 50, BLUE)
    dn = m.p(4.91, 50.26, z); dot(can, *dn, YEL, 12); label(can, t, w('Dinant', k), dn[0] + 26, dn[1] - 30, 'DINANT', 60, YEL)
    tgt = m.p(0.75, 49.87, z); arrow(can, dn, tgt, eio((t - w('Westen', k) + 0.6) / 1.8), RED, 22, 56)
    label(can, t, w('Westen', k) + 0.6, lerp(dn[0], tgt[0], 0.5), lerp(dn[1], tgt[1], 0.5) + 120, '7. PANZERDIVISION', 60, WHITE, 'mm')
    tq = w('weiß', k)
    if t > tq and int((t - tq) * 3) % 2 == 0: txt(can, t, tq, (tgt[0] + 10, tgt[1] - 110), '?', anton(120), YEL)
    sub(can, t, tq, 'SELBST DIE EIGENE FÜHRUNG WEISS NICHT, WO SIE STEHT', 1020, 50, WHITE)
def s_ghost(t, w0, w1):
    base = pan('r19', t, w0, w1, 1); g = base.copy(); ph = (t - w0)
    for k_, dx in enumerate((18, -26)):
        sh_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh_.paste(ImageEnhance.Color(base).enhance(0.2), (int(dx * math.sin(ph * 1.7 + k_)), 0))
        g = Image.blend(g, sh_, 0.22)
    g = ImageEnhance.Color(g).enhance(0.6); shade(g, 205, 0.55)
    cap(g, t, w('Gespensterdivision', 30), 'DIE GESPENSTERDIVISION', 950, 104, WHITE); return g
def ov_front(can, t, w0, w1): cap(can, t, w('vorne', 31), 'FÜHRUNG VON VORNE', 960, 80)
def ov_valery(can, t, w0, w1):
    k = 32; sub(can, t, w('Kanalküste', k), 'ST-VALERY-EN-CAUX, JUNI 1940', 960, 64, WHITE); sub(can, t, w('Cherbourg', k), 'SPÄTER: CHERBOURG', 1030, 54, YEL)
def ov_kehr(can, t, w0, w1): cap(can, t, w('Kehrseite', 33), 'DIE KEHRSEITE', 960, 96, YEL)
def s_bars(t, w0, w1):
    can = plain(); k = 35; base = 820
    txt(can, t, ST[33], (W / 2, 90), 'DIE KEHRSEITE', anton(84), YEL)
    lines(can, t, w0, [[(220, base), (1700, base)]], 0.6, GREY, 4)
    tv = w('Verluste', k); u = eout((t - tv) / 1.0) if t > tv else 0
    if u: shape(can, [(420, base), (620, base), (620, base - 480 * u), (420, base - 480 * u)], (90, 24, 26), RED, 5)
    txt(can, t, tv, (520, base + 60), 'HOHE VERLUSTE', bebas(58), RED); txt(can, t, tv, (520, 230), '7. PANZERDIVISION', bebas(56), WHITE)
    tn = w('Nachbarverbände', k); tk = w('kleinzureden', k)
    for i, x in enumerate((1080, 1300, 1520)):
        if t > tn + i * 0.15:
            hh = 360 * eout((t - tn - i * 0.15) / 0.6) * lerp(1.0, 0.35, eio((t - tk) / 1.0)); shape(can, [(x - 80, base), (x + 80, base), (x + 80, base - hh), (x - 80, base - hh)], (50, 54, 60), GREY, 4)
    txt(can, t, tn, (1300, base + 60), 'LEISTUNG DER NACHBARN', bebas(58), GREY); txt(can, t, tk, (1300, 300), 'KLEINGEREDET', anton(70), YEL); return can
def ov_cam(can, t, w0, w1):
    k = 36; x, y = fitpt('r28', t, w0, w1, 1.06, 950, 1344); ring(can, t, w('Bilder', k), x, y, YEL, 60, False)
    cap(can, t, w('Bilder', k), 'DIE MACHT DER BILDER', 980, 90, YEL)
def ov_report(can, t, w0, w1):
    k = 37; x, y = fitpt('r31', t, w0, w1, 1.05, 154, 317)
    ring(can, t, w('Kameras', k), x, y, YEL, 70, False); sub(can, t, w('Kriegsberichterstatter', k), 'KRIEGSBERICHTERSTATTER', 1000, 66, YEL)
def s_leader(t, w0, w1):
    can = plain(); u = t - w0; L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((0, 0, W, H), fill=(28, 26, 22, 255))
    n = 3 - int(u / 0.4)
    if n >= 1:
        d.line((W / 2, 0, W / 2, H), fill=(90, 86, 78, 255), width=3); d.line((0, H / 2, W, H / 2), fill=(90, 86, 78, 255), width=3)
        for r in (300, 340): d.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), outline=(200, 194, 180, 255), width=5)
        a = (u % 0.4) / 0.4 * 360; d.pieslice((W / 2 - 300, H / 2 - 300, W / 2 + 300, H / 2 + 300), -90, -90 + a, fill=(60, 56, 50, 255))
        d.text((W / 2, H / 2), str(n), font=anton(380), fill=(230, 224, 210, 255), anchor='mm')
    can.alpha_composite(L)
    if n < 1:
        can = plain(); txt(can, t, w0 + 1.2, (W / 2, 470), 'ROMMEL', anton(220), WHITE); sub(can, t, w0 + 1.4, 'IN DER HEIMAT BEKANNT', 640, 70, YEL)
    return can

# ================= K4 =================
def ov_libya(can, t, w0, w1): tw(can, t, w0 + 0.3, 'FEBRUAR 1941 · LIBYEN', 960, 66)
def ov_dak(can, t, w0, w1):
    k = 39; sub(can, t, w('italienischen', k), 'DIE ITALIENISCHEN TRUPPEN STEHEN VOR DEM ZUSAMMENBRUCH', 1020, 50, t1=w('Afrikakorps', k) - 0.6)
    cap(can, t, w('Afrikakorps', k) - 0.3, 'DEUTSCHES AFRIKAKORPS', 980, 92, YEL)
def s_order(t, w0, w1):
    can = dim(pan('r01', t, w0, w1, -1, 0.5), 150); k = 40
    doc(can, t, w('Auftrag', k), [('BEFEHL', 50, INK), ('', 14, INK), ('VERTEIDIGEN', 44, INK), ('UND ABWARTEN', 44, INK)], W / 2, 520, 700); return can
def ov_trotz(can, t, w0, w1): cap(can, t, w('trotzdem', 41), 'TROTZDEM: ANGRIFF', 960, 100, YEL)
LIB = Map(22.0, 31.5, 15.0, hi=('Libya',))
TOB = (23.96, 32.08)
def ov_lib(can, t, w0, w1, z):
    m = LIB; k = 42; a, b = m.p(19.6, 30.4, z), m.p(25.0, 31.4, z)
    for nm, ll in (('LIBYEN', (18.0, 28.8)), ('ÄGYPTEN', (28.0, 29.0))):
        p = m.p(*ll, z); label(can, t, w0, p[0], p[1], nm, 84, GREY, 'mm')
    lines(can, t, w0 + 0.2, [[m.p(25.0, 31.6, z), m.p(25.0, 28.0, z)]], 0.8, (150, 150, 150), 4)
    arrow(can, a, b, eio((t - w('jagt', k)) / 1.6), RED, 22, 56); label(can, t, w('Grenze', k), b[0] + 20, b[1] + 80, 'GRENZE ÄGYPTENS', 54, WHITE)
    tb = m.p(*TOB, z); dot(can, *tb, YEL, 12)
    if t > w('Tobruk', 43): ring(can, t, w('Tobruk', 43), *tb, YEL, 48, False)
    label(can, t, w('Tobruk', 43), tb[0] - 30, tb[1] - 70, 'TOBRUK', 80, YEL, 'rm')
def ov_siege(can, t, w0, w1): cap(can, t, w0 + 0.3, 'BELAGERUNG VON TOBRUK', 960, 84); sub(can, t, w('vergeblich', 44), 'MONATELANG VERGEBLICH', 1035, 54, YEL)
def ov_supply(can, t, w0, w1): cap(can, t, w('Nachschub', 45), 'NACHSCHUB', 960, 120, YEL)
MED = Map(19.0, 35.5, 26.0, hi=('Libya', 'Italy'))
COAST = [(13.19, 32.89), (15.1, 32.3), (17.5, 31.0), (19.4, 30.3), (20.07, 32.12), (21.8, 32.8), (23.96, 32.08), (25.15, 31.57), (27.2, 31.35), (28.95, 30.83)]
def ov_med(can, t, w0, w1, z):
    k = 46; m = MED; sea = route([(14.27, 40.85), (13.5, 38.6), (12.5, 36.5), (13.19, 32.89)], m, z)
    ts = w('Mittelmeer', k) - 0.5; u = eio((t - ts) / 1.8)
    dashed(can, sea, u, WHITE, 6, 20, 0)
    if 0 < u: i = min(len(sea) - 2, int(u * (len(sea) - 1))); p0, p1 = sea[i], sea[i + 1]; ship(can, *p0, math.atan2(p1[1] - p0[1], p1[0] - p0[0]), 50)
    for nm, ll, off in (('NEAPEL', (14.27, 40.85), (24, 0)), ('TRIPOLIS', (13.19, 32.89), (-24, 40)), ('EL ALAMEIN', (28.95, 30.83), (0, 60))):
        p = m.p(*ll, z); dot(can, *p, WHITE, 9); label(can, t, w0 + 0.3, p[0] + off[0], p[1] + off[1], nm, 50, WHITE, 'lm' if off[0] > 0 else ('rm' if off[0] < 0 else 'mm'))
    tk = w('Küstenstraße', k) - 1.2; dashed(can, route(COAST, m, z, 10), eio((t - tk) / 2.2), YEL, 7)
    label(can, t, w('Hunderte', k), m.p(21.5, 30.6, z)[0], m.p(21.5, 30.6, z)[1], 'HUNDERTE KILOMETER', 58, YEL, 'mm')
    for i, (lab, ww) in enumerate((('JEDER LITER TREIBSTOFF', 'Liter'), ('JEDE GRANATE', 'Granate'))):
        sub(can, t, w(ww, k), lab, 150 + i * 70, 56, WHITE)
def ov_plan(can, t, w0, w1): sub(can, t, w('weiter', 47), 'PLANT WEITER, ALS DIE VERSORGUNG REICHT', 1000, 62, WHITE)
def ov_both(can, t, w0, w1): cap(can, t, w('beiden', 48), 'RUF AUF BEIDEN SEITEN', 960, 84)
def s_paper(t, w0, w1):
    can = plain(); u = prog(t, w0, w1); k = 49
    L = Image.new('RGBA', (1100, 760), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.rectangle((0, 0, 1100, 760), fill=(226, 220, 204, 255))
    d.line((40, 120, 1060, 120), fill=INK + (255,), width=4); d.line((40, 128, 1060, 128), fill=INK + (255,), width=1)
    hl = 'THE DESERT FOX'; n = int(clamp((t - w('Spitznamen', k)) / 0.9) * len(hl)) if t > w('Spitznamen', k) else 0
    d.text((550, 230), hl[:n], font=anton(150), fill=INK + (255,), anchor='mm')
    for c in range(3):
        for r_ in range(12): d.rectangle((40 + c * 345, 360 + r_ * 30, 40 + c * 345 + 310 - (r_ % 4 == 3) * 120, 372 + r_ * 30), fill=(150, 144, 130, 255))
    L = L.rotate(lerp(-4, -2, u), expand=True, resample=Image.BICUBIC); sc = lerp(0.92, 1.05, u); L = L.resize((int(L.width * sc), int(L.height * sc)), Image.BICUBIC)
    sh_ = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh_.paste((0, 0, 0, 150), (int(W / 2 - L.width / 2 + 14), int(H / 2 - L.height / 2 + 22)), L.getchannel('A'))
    can.alpha_composite(sh_.filter(ImageFilter.GaussianBlur(16))); can.alpha_composite(L, (int(W / 2 - L.width / 2), int(H / 2 - L.height / 2)))
    txt(can, t, w('britischen', k), (W / 2, 70), 'BRITISCHE PRESSE', bebas(60), YEL)
    cap(can, t, w('beiden', 48), 'SEIN RUF WÄCHST AUF BEIDEN SEITEN', 980, 76, WHITE, w('britischen', k) - 0.3); return can
def ov_fox(can, t, w0, w1): cap(can, t, w0 + 0.2, 'DER WÜSTENFUCHS', 950, 120, YEL)
def ov_auch(can, t, w0, w1):
    k = 50; sub(can, t, w('Oberbefehlshaber', k), 'BRITISCHER OBERBEFEHLSHABER', 950, 50, YEL); cap(can, t, w('Claude', k), 'CLAUDE AUCHINLECK', 1020, 70)
def s_letter(t, w0, w1):
    can = plain(); k = 51
    doc(can, t, w0 + 0.05, [('AN ALLE KOMMANDEURE', 44, INK), ('', 16, INK), ('Rommel wird zu einer Art', 32, INK), ('ZAUBERER', 52, (150, 30, 30)), ('oder', 30, INK), ('SCHRECKGESPENST', 52, (150, 30, 30))], W / 2, 540, 880); return can
def s_strike(t, w0, w1):
    can = plain(); k = 52; txt(can, t, w0 + 0.1, (W / 2, 420), 'ROMMEL', anton(240), WHITE)
    lines(can, t, w('nicht', k), [[(600, 440), (1320, 400)]], 0.5, RED, 22)
    txt(can, t, w('Deutschen', k) - 0.3, (W / 2, 720), 'DIE DEUTSCHEN', anton(150), YEL); return can
def ov_tob42a(can, t, w0, w1): tw(can, t, w0 + 0.3, 'JUNI 1942', 900, 70); cap(can, t, w('Tobruk', 53), 'TOBRUK FÄLLT', 1000, 90, YEL)
def ov_tob42(can, t, w0, w1):
    k = 53; t0 = w('30.000', k); sub(can, t, t0 - 0.3, 'MEHR ALS', 760, 60, WHITE); counter(can, t, t0, 0, 30000, (W / 2, 880), 200, YEL, 1.3); sub(can, t, t0 + 0.6, 'IN GEFANGENSCHAFT', 1020, 60, WHITE)
def ov_gfm(can, t, w0, w1):
    cap(can, t, w('Generalfeldmarschall', 54), 'GENERALFELDMARSCHALL', 900, 92, YEL)
    sub(can, t, w('50', 55), 'MIT 50 JAHREN DER JÜNGSTE IM HEER', 1010, 62, WHITE)

# ================= K5 =================
EGY = Map(28.3, 30.9, 7.0, hi=('Egypt',))
def ov_egy(can, t, w0, w1, z):
    k = 57; m = EGY; ea, al = m.p(28.95, 30.83, z), m.p(29.92, 31.20, z)
    arrow(can, m.p(25.4, 31.4, z), (ea[0] - 30, ea[1]), eio((t - w0 - 0.2) / 1.4), RED, 22, 56)
    dot(can, *ea, YEL, 12); label(can, t, w('El', k), ea[0] - 20, ea[1] - 60, 'EL ALAMEIN', 70, YEL, 'rm')
    dot(can, *al, WHITE, 10); label(can, t, w('Alexandria', k), al[0] + 24, al[1] - 30, 'ALEXANDRIA', 60, WHITE)
    dashed(can, [ea, al], eio((t - w('100', k)) / 0.8), WHITE, 5, 16, 0); label(can, t, w('100', k), (ea[0] + al[0]) / 2 + 10, (ea[1] + al[1]) / 2 + 60, 'RUND 100 KM', 54, WHITE, 'mm')
    lines(can, t, w('stecken', k) - 0.3, [[m.p(29.0, 30.95, z), m.p(28.4, 30.2, z), m.p(27.9, 29.5, z)]], 0.6, RED, 14)
    label(can, t, w('stecken', k), m.p(28.0, 29.4, z)[0] - 30, m.p(28.0, 29.4, z)[1], 'DER VORMARSCH BLEIBT STECKEN', 56, RED, 'rm')
def s_monty(t, w0, w1):
    can = plain(); k = 58; cap(can, t, w('Bernard', k), 'BERNARD MONTGOMERY', 170, 96, WHITE)
    for row, (wd, lab, fn) in enumerate((('Panzer', 'PANZER', tank_icon), ('Flugzeuge', 'FLUGZEUGE', plane_icon), ('Treibstoff', 'TREIBSTOFF', can_icon))):
        t0 = w(wd, k) - 0.2; y = 400 + row * 190; txt(can, t, t0, (330, y), lab, bebas(66), YEL, anchor='rm')
        n = int(clamp((t - t0) / 2.2) * 12) if t > t0 else 0
        for i in range(n): fn(can, 450 + i * 110, y, 1.0, WHITE)
    sub(can, t, w('immer', k), 'IMMER MEHR', 1000, 62, YEL); return can
def ov_battle(can, t, w0, w1):
    k = 59; tw(can, t, w0 + 0.2, 'OKTOBER 1942', 120, 66); cap(can, t, w('nicht', k), 'ROMMEL IST NICHT IN AFRIKA', 960, 84, YEL)
EUA = Map(21.0, 38.5, 52.0, hi=('Austria',))
def ov_kur(can, t, w0, w1, z):
    k = 60; m = EUA; sm, ea = m.p(15.83, 47.63, z), m.p(28.95, 30.83, z)
    dot(can, *sm, YEL, 12); label(can, t, w('krank', k), sm[0] + 26, sm[1] + 10, 'KUR IN ÖSTERREICH', 60, YEL)
    dot(can, *ea, RED, 12); label(can, t, w0 + 0.3, ea[0] - 26, ea[1] - 40, 'EL ALAMEIN', 56, RED, 'rm')
    dashed(can, route([(15.83, 47.63), (17.5, 40.0), (24.0, 34.5), (28.95, 30.83)], m, z), eio((t - w('eilt', k)) / 1.6), WHITE, 6)
def ov_12(can, t, w0, w1):
    k = 61; counter(can, t, w('zwölf', k), 1, 12, (W / 2, 840), 180, YEL, 1.0, '{:,}', ' TAGE'); sub(can, t, w('nicht', k), 'DIE FRONT IST NICHT ZU HALTEN', 1010, 62, WHITE)
def s_order2(t, w0, w1):
    can = plain(); k = 62
    doc(can, t, w0 + 0.05, [('FUNKSPRUCH AUS DEM HAUPTQUARTIER', 34, INK), ('', 16, INK), ('KEIN SCHRITT ZURÜCK', 48, INK), ('', 10, INK), ('SIEG ODER TOD', 58, (150, 30, 30))], W / 2, 520, 960)
    return can
def ov_retreat(can, t, w0, w1): cap(can, t, w('zögert', 63), 'EIN TAG ZÖGERN', 930, 78, WHITE, w('zieht', 63) - 0.2); cap(can, t, w('zieht', 63), 'DANN DER RÜCKZUG', 960, 92, YEL)
NA = Map(19.5, 33.0, 24.0, hi=('Tunisia',))
def ov_tun(can, t, w0, w1, z):
    k = 64; m = NA; path = route(list(reversed(COAST)) + [(11.1, 33.6), (10.2, 36.8)], m, z, 10)
    dashed(can, path, eio((t - w0 - 0.2) / 3.0), RED, 8)
    tn = m.p(10.18, 36.8, z); dot(can, *tn, YEL, 12); label(can, t, w('Tunesien', k), tn[0] + 30, tn[1] - 20, 'TUNESIEN', 70, YEL)
    tw(can, t, w('Mai', k), 'MAI 1943', 120, 70); sub(can, t, w('kapitulieren', k), 'KAPITULATION', 1010, 80, WHITE)
def s_250(t, w0, w1):
    can = plain(); k = 65; t0 = w('250.000', k) - 0.2
    counter(can, t, t0, 0, 250000, (W / 2, 330), 210, YEL, 1.5); sub(can, t, t0 + 0.3, 'SOLDATEN IN GEFANGENSCHAFT', 500, 64, WHITE)
    n = int(clamp((t - t0) / 1.8) * 50) if t > t0 else 0
    for i in range(n): person(can, 330 + (i % 25) * 52, 720 + (i // 25) * 170, 0.45, CREAM, 0.85)
    sub(can, t, t0 + 1.0, '1 FIGUR = 5.000 MANN', 1030, 40, GREY); return can

# ================= K6 =================
def ov_ende43(can, t, w0, w1): tw(can, t, w0 + 0.5, 'ENDE 1943 · ATLANTIKWALL', 960, 62)
def ov_coast(can, t, w0, w1): cap(can, t, w('Küste', 68), 'DIE KÜSTE FRANKREICHS', 960, 90)
WALL = Map(1.5, 49.6, 13.0, hi=('France',))
WALLC = [(4.3, 52.4), (3.6, 51.4), (2.5, 51.05), (1.6, 50.9), (1.6, 50.2), (0.2, 49.7), (-0.2, 49.3), (-1.2, 49.36), (-1.6, 49.65), (-1.85, 49.7), (-1.6, 48.8), (-2.5, 48.6), (-3.5, 48.8)]
def ov_wall(can, t, w0, w1, z):
    lines(can, t, w('Küste', 68) - 0.3, [route(WALLC, WALL, z, 8)], 2.2, YEL, 12)
    cap(can, t, w('Küste', 68), 'DIE KÜSTE FRANKREICHS', 960, 90); sub(can, t, w('Landung', 68), 'GEGEN DIE ERWARTETE LANDUNG', 1035, 56, YEL)
def ov_mines(can, t, w0, w1): cap(can, t, w('Millionen', 69), 'MILLIONEN MINEN', 960, 110, YEL)
def s_obst(t, w0, w1):
    can = plain(); k = 69; gy = 760
    lines(can, t, w0, [[(0, gy), (W, gy)]], 0.6, SAND, 5)
    wave = [(x, 640 + 14 * math.sin(x / 50 + (t - w0) * 2)) for x in range(0, W + 1, 30)]; lines(can, t, w0, [wave], 0.01, BLUE, 4)
    for i, x in enumerate((300, 520, 740)):
        lines(can, t, w('schräge', k) + i * 0.15, [[(x, gy), (x + 120, gy - 170)], [(x + 60, gy), (x + 40, gy - 30)]], 0.4, CREAM, 9)
    for i, x in enumerate((1080, 1300)):
        lines(can, t, w('Stahlkreuze', k) + i * 0.15, [[(x - 70, gy), (x + 70, gy - 140)], [(x + 70, gy), (x - 70, gy - 140)], [(x, gy), (x, gy - 150)]], 0.4, GREY, 10)
    tb = w('Landungsboote', k); u = eout((t - tb) / 1.4) if t > tb else 0
    if u:
        bx = lerp(2000, 1560, u); shape(can, [(bx - 140, 620), (bx + 180, 620), (bx + 200, 560), (bx - 120, 560)], DARK, WHITE, 5)
        if u > 0.95: ring(can, t, tb + 1.3, bx - 120, 600, RED, 40, True)
    txt(can, t, w('schräge', k), (520, 320), 'SCHRÄGE PFÄHLE', bebas(66), CREAM); txt(can, t, w('Stahlkreuze', k), (1190, 320), 'STAHLKREUZE', bebas(66), GREY)
    sub(can, t, tb, 'GEGEN LANDUNGSBOOTE', 1000, 62, YEL); return can
def s_spargel(t, w0, w1):
    can = plain(); k = 70; gy = 820
    lines(can, t, w0, [[(0, gy), (W, gy)]], 0.5, (120, 160, 90), 5)
    for i in range(9):
        x = 200 + i * 190; lines(can, t, w('Holzstämme', k) + i * 0.08, [[(x, gy), (x + (i % 2) * 8, gy - 200 - (i % 3) * 30)]], 0.3, SAND, 10)
    tg = w('Lastensegler', k) - 0.3; u = clamp((t - tg) / 2.0)
    if t > tg: plane(can, lerp(1900, 1080, u), lerp(260, gy - 230, u), 1.6, 0.22 if u < 1 else 0.5, WHITE)
    if u >= 1: ring(can, t, tg + 2.0, 1080, gy - 220, RED, 46, True)
    cap(can, t, w('Rommelspargel', k), '„ROMMELSPARGEL“', 960, 110, YEL); return can
def s_clock(t, w0, w1):
    can = plain(); k = 71; cx, cy, r = W / 2, 470, 280; t0 = w('24', k) - 0.4
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    a = 360 * eio((t - t0) / 2.6) if t > t0 else 0
    if a: d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, -90 + a, fill=RED + (150,))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=CREAM + (255,), width=8)
    for i in range(24):
        an = math.radians(i * 15 - 90); r0 = r - (30 if i % 6 == 0 else 16); d.line((cx + r0 * math.cos(an), cy + r0 * math.sin(an), cx + r * math.cos(an), cy + r * math.sin(an)), fill=CREAM + (255,), width=5)
    can.alpha_composite(L); txt(can, t, t0, (cx, cy), '24', anton(200), WHITE)
    cap(can, t, t0 + 0.3, 'DIE ERSTEN 24 STUNDEN', 860, 84, YEL); sub(can, t, w('Strand', k), 'AM STRAND ENTSCHIEDEN', 960, 62); return can
def s_tanks(t, w0, w1):
    can = plain(); cy = 250
    wave = [(x, cy + 18 * math.sin(x / 90)) for x in range(0, W + 1, 30)]; lines(can, t, w0, [wave], 0.8, BLUE, 6)
    txt(can, t, w0 + 0.3, (W / 2, 130), 'KÜSTE', bebas(60), BLUE)
    tc = w('Küste', 72); tb = w('hinten', 73); tk = w('Kompromiss', 74)
    for i in range(5):
        x = 560 + i * 200
        if t > tc: y = lerp(350, 600, eio((t - tk) / 1.4)) if i % 2 else 350; tank_icon(can, x, y, 1.3, YEL, clamp((t - tc) / 0.4))
        if t > tb: tank_icon(can, x + 40, lerp(880, 640, eio((t - tk) / 1.4)) if i % 2 == 0 else 880, 1.3, GREY, clamp((t - tb) / 0.4))
    txt(can, t, tc, (360, 350), 'ROMMEL', bebas(64), YEL, tk - 0.2, anchor='rm'); txt(can, t, tb, (360, 880), 'ANDERE', bebas(64), GREY, tk - 0.2, anchor='rm')
    cap(can, t, tk, 'KOMPROMISS', 1010, 90, WHITE); return can
NOR = Map(5.0, 48.8, 15.0, hi=('France',))
def ov_dday(can, t, w0, w1, z):
    m = NOR; nb, hr = m.p(-0.6, 49.35, z), m.p(9.89, 48.42, z)
    tw(can, t, w('Morgen', 75), '6. JUNI 1944', 130, 80)
    dot(can, *nb, RED, 13); label(can, t, w('Normandie', 76), nb[0] - 26, nb[1] - 60, 'NORMANDIE', 66, RED, 'mm')
    if t > w('nicht', 76): ring(can, t, w('nicht', 76), *nb, RED, 50, True)
    dashed(can, route([(-0.6, 49.35), (4.5, 49.6), (9.89, 48.42)], m, z), eio((t - w('Herrlingen', 77) + 0.6) / 1.4), YEL, 6)
    dot(can, *hr, YEL, 13); label(can, t, w('Herrlingen', 77), hr[0] + 26, hr[1] - 20, 'HERRLINGEN', 66, YEL)
    sub(can, t, w('Lucie', 77), 'LUCIE ROMMEL HAT GEBURTSTAG', 1010, 64, WHITE)

# ================= K7 =================
def ov_lost(can, t, w0, w1): cap(can, t, w('verloren', 78), 'DER KRIEG IST VERLOREN', 960, 92, YEL)
def s_strafe(t, w0, w1):
    can = plain(); gy = 760; k = 80
    lines(can, t, w0, [[(0, gy + 60), (W, gy + 60)]] + [[(x, gy + 60), (x, gy - 100)] for x in range(140, W, 260)] + [circ(x, gy - 150, 60, 30) for x in range(140, W, 260)], 1.2, (90, 120, 80), 4)
    tw(can, t, w0 + 0.1, '17. JULI 1944', 120, 70); ta = w('greift', k); th = ta + 1.6
    cx_ = lerp(200, 980, eout((t - w0) / (th - w0 + 0.6))) if t < th + 0.6 else 980
    car(can, cx_, gy, 1.1, YEL)
    if t > ta:
        u = clamp((t - ta) / 1.8); plane(can, lerp(2000, 600, u), lerp(260, 380, u), 1.6, 0.12, WHITE)
        if 0.3 < u < 0.95: dashed(can, [(lerp(2000, 600, u) - 60, lerp(260, 380, u) + 20), (cx_ + 180, gy)], 1.0, RED, 5, 14, 0)
    if t > th: ring(can, t, th, cx_ + 150, gy + 10, RED, 70, True)
    cap(can, t, w('schwer', 81), 'SCHWER AM KOPF VERLETZT', 1000, 80, RED); return can
def s_files(t, w0, w1):
    can = plain(); tw(can, t, w0 + 0.1, '20. JULI 1944', 120, 80); sub(can, t, w('scheitert', 82), 'DAS ATTENTAT SCHEITERT', 210, 62, WHITE)
    tv = w('Verhaftungswelle', 83)
    for i in range(7):
        t0 = tv + i * 0.22
        if t < t0: continue
        u = eout((t - t0) / 0.5); x = 360 + i * 200; y = lerp(1300, 560 + (i % 2) * 40, u)
        L = Image.new('RGBA', (300, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.rectangle((0, 0, 300, 400), fill=(214, 200, 166, 255)); d.rectangle((0, 0, 300, 400), outline=(120, 100, 70, 255), width=3)
        for r_ in range(6): d.rectangle((30, 120 + r_ * 40, 270 - (r_ % 3) * 50, 136 + r_ * 40), fill=(150, 136, 110, 255))
        if i == 3 and t > w('Rommels', 84): d.text((150, 60), 'ROMMEL', font=anton(56), fill=(150, 30, 30, 255), anchor='mm')
        else: d.rectangle((40, 44, 260, 76), fill=(120, 104, 80, 255))
        L = L.rotate((i - 3) * 3, expand=True, resample=Image.BICUBIC); can.alpha_composite(L, (int(x - L.width / 2), int(y - L.height / 2)))
    if t > w('Rommels', 84): ring(can, t, w('Rommels', 84), 960, 460, RED, 120, False)
    sub(can, t, tv, 'EINE GROSSE VERHAFTUNGSWELLE', 1010, 62, YEL); return can
def ov_q(can, t, w0, w1): cap(can, t, w('Wie', 85), 'WIE VIEL WUSSTE ER?', 940, 96); sub(can, t, w('umstritten', 85), 'BIS HEUTE UMSTRITTEN', 1030, 56, YEL)
def s_net(t, w0, w1):
    can = plain(); R, S_, V = (420, 560), (960, 560), (1500, 560)
    def node(p, lab, sub_, t0, col):
        lines(can, t, t0, [circ(*p, 120, 48)], 0.6, col, 7); txt(can, t, t0 + 0.2, (p[0], p[1]), lab, anton(54 if len(lab) < 9 else 44), col); txt(can, t, t0 + 0.3, (p[0], p[1] + 170), sub_, bebas(48), GREY)
    node(R, 'ROMMEL', '', w0 + 0.1, YEL); node(S_, 'SPEIDEL', 'STABSCHEF', w('Speidel', 86) - 0.4, WHITE); node(V, 'VERSCHWÖRER', '20. JULI', w('Verschwörern', 86) - 0.4, RED)
    lines(can, t, w('Speidel', 86), [[(R[0] + 120, R[1]), (S_[0] - 120, S_[1])]], 0.5, WHITE, 6)
    lines(can, t, w('Kontakt', 86), [[(S_[0] + 120, S_[1]), (V[0] - 120, V[1])]], 0.5, RED, 6)
    to = w('Ob', 87)
    if t > to:
        dashed(can, [(R[0] + 60, R[1] - 110), (960, 300), (V[0] - 60, V[1] - 110)], eio((t - to) / 1.0), GREY, 5, 16, 0)
        txt(can, t, to + 0.6, (960, 250), '?', anton(130), YEL)
    sub(can, t, w('belegen', 87), 'NICHT BELEGT', 1000, 70, YEL); return can
def s_verdacht(t, w0, w1):
    can = plain(); k = 88
    doc(can, t, w0 + 0.05, [('BERLIN, 1944', 36, INK), ('', 14, INK), ('Betr.: Generalfeldmarschall', 34, INK), ('Erwin Rommel', 40, INK)], W / 2, 500, 820)
    stamp(can, t, w('Verdacht', k), 'VERDACHT', (W / 2 + 60, 620), RED, 120, -10); return can

# ================= K8 =================
GER2 = Map(9.9, 48.5, 2.2, hi=('Germany',))
def ov_back(can, t, w0, w1, z):
    m = GER2; ul, hr = m.p(9.99, 48.40, z), m.p(9.89, 48.42, z)
    dot(can, *ul, WHITE, 9); label(can, t, w0 + 0.3, ul[0] + 24, ul[1] + 30, 'ULM', 54, WHITE)
    dot(can, *hr, YEL, 14); ring(can, t, w('Herrlingen', 89), *hr, YEL, 44, False); label(can, t, w('Herrlingen', 89), hr[0] - 40, hr[1] - 50, 'HERRLINGEN', 72, YEL, 'rm')
    tw(can, t, w('14.', 89), '14. OKTOBER 1944', 140, 80)
def s_generals(t, w0, w1):
    can = plain(); k = 91
    for i, (wd, nm) in enumerate((('Wilhelm', 'WILHELM BURGDORF'), ('Ernst', 'ERNST MAISEL'))):
        t0 = w(wd, k) - 0.3; y = 380 + i * 200
        txt(can, t, t0, (W / 2, y), nm, anton(120), WHITE); txt(can, t, t0 + 0.2, (W / 2, y + 85), 'GENERAL', bebas(50), GREY)
    cap(can, t, w('Wahl', k), 'BRINGEN ROMMEL EINE WAHL', 960, 90, YEL); return can
def s_choice(t, w0, w1):
    can = plain(); k = 92; tg = w('Wählt', 93)
    lines(can, t, w0, [[(W / 2, 150), (W / 2, 930)]], 0.6, GREY, 4)
    dl = 1 - 0.65 * eio((t - tg) / 0.8)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    txt(L, t, w('Prozess', k), (480, 260), 'PROZESS', anton(110), WHITE); txt(L, t, w('Volksgerichtshof', k), (480, 420), 'VOLKSGERICHTSHOF', bebas(68), CREAM)
    txt(L, t, w('Folgen', k), (480, 520), 'FOLGEN FÜR FAMILIE', bebas(58), GREY); txt(L, t, w('Folgen', k) + 0.4, (480, 590), 'UND STAB', bebas(58), GREY)
    if dl < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * dl)))
    can.alpha_composite(L)
    txt(can, t, w('Gift', k), (1440, 260), 'GIFT', anton(130), RED)
    txt(can, t, w('Frau', 93), (1440, 430), 'FRAU UND SOHN GESCHONT', bebas(62), WHITE); txt(can, t, w('Staatsbegräbnis', 93), (1440, 520), 'STAATSBEGRÄBNIS', bebas(62), YEL)
    sub(can, t, w('Entweder', k), 'ENTWEDER', 120, 50, GREY, w('oder', k) - 0.1); return can
def ov_farewell(can, t, w0, w1): sub(can, t, w('Lucie', 94), 'ABSCHIED VON LUCIE', 950, 66, WHITE); sub(can, t, w('Manfred', 94), 'UND SOHN MANFRED (15)', 1025, 60, YEL)
def s_capsule(t, w0, w1):
    can = plain(); gy = 760
    tk = w('Kapsel', 95)
    if t > tk:
        u = eout((t - tk) / 0.5); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); cx, cy = 1240, 470
        d.rounded_rectangle((cx - 110 * u, cy - 40 * u, cx + 110 * u, cy + 40 * u), radius=int(40 * u) + 1, fill=(220, 220, 210, 255), outline=WHITE + (255,), width=4)
        d.line((cx, cy - 40 * u, cx, cy + 40 * u), fill=(150, 150, 140, 255), width=4); can.alpha_composite(L)
    cap(can, t, w('Zyankali', 95), 'ZYANKALI', 650, 110, RED); sub(can, t, w0 + 0.3, 'KURZ HINTER DEM ORT', 140, 60, CREAM); return can
def ov_ulm(can, t, w0, w1):
    k = 96; tw(can, t, w0 + 0.3, 'ULM, 18. OKTOBER 1944', 120, 66)
    sub(can, t, w('Trauerrede', k) - 0.6, 'TRAUERREDE', 940, 56, YEL); cap(can, t, w('Gerd', k), 'GERD VON RUNDSTEDT', 1020, 74)
def s_quote(t, w0, w1):
    can = plain(); k = 97; q = '„EIN HELD, DER SEINEN'; q2 = 'VERWUNDUNGEN ERLEGEN SEI“'
    typewriter(can, t, w('Helden', k) - 0.3, (W / 2, 430), q, typew(76), CREAM, 0.05); typewriter(can, t, w('Verwundungen', k) - 0.2, (W / 2, 540), q2, typew(76), CREAM, 0.05)
    sub(can, t, w0 + 0.2, 'DIE OFFIZIELLE VERSION', 250, 56, GREY)
    lines(can, t, w('erlegen', k) + 0.6, [[(330, 545), (1590, 540)]], 0.5, RED, 10); return can
def ov_mask(can, t, w0, w1): cap(can, t, w('Totenmaske', 98), 'TOTENMASKE', 980, 110, WHITE)
def s_vitrine(t, w0, w1):
    can = plain(); k = 99; cx = 620
    lines(can, t, w0, [[(cx - 230, 720), (cx - 230, 300), (cx + 230, 300), (cx + 230, 720), (cx - 230, 720)], [(cx - 270, 720), (cx + 270, 720), (cx + 270, 800), (cx - 270, 800), (cx - 270, 720)],
                       [(cx - 200, 330), (cx - 150, 380)]], 1.0, CREAM, 5)
    lines(can, t, w0 + 0.6, [circ(cx, 500, 110, 40), [(cx - 45, 480), (cx - 15, 480)], [(cx + 15, 480), (cx + 45, 480)], [(cx, 495), (cx - 8, 545), (cx + 8, 545)], [(cx - 30, 580), (cx + 30, 580)]], 1.0, GREY, 4)
    txt(can, t, w('Rommel-Museums', k), (1340, 330), 'ROMMEL-MUSEUM', anton(76), WHITE); txt(can, t, w('Herrlingen', k), (1340, 410), 'HERRLINGEN', bebas(60), YEL)
    lines(can, t, w('jahrzehntelang', k), [[(1000, 600), (1680, 600)]], 1.2, GREY, 5); txt(can, t, w('jahrzehntelang', k), (1340, 560), 'JAHRZEHNTELANG', bebas(52), GREY)
    stamp(can, t, w('2019', k), '2019 GESCHLOSSEN', (1340, 720), RED, 62, -6)
    sub(can, t, w('überholt', k), 'DIE AUSSTELLUNG GALT ALS ÜBERHOLT', 1000, 56, WHITE); return can
def s_manfred(t, w0, w1):
    can = plain(); k = 100; u = (t - w0) / 3.0 % 1.6
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); x = lerp(-600, 2500, u / 1.6)
    d.polygon([(x, 0), (x + 260, 0), (x - 140, H), (x - 400, H)], fill=(255, 240, 200, 26)); can.alpha_composite(L.filter(ImageFilter.GaussianBlur(30)))
    txt(can, t, w('Wahrheit', k), (W / 2, 240), 'DIE WAHRHEIT KOMMT ANS LICHT', bebas(72), YEL)
    txt(can, t, w('Manfred', k), (W / 2, 470), 'MANFRED ROMMEL', anton(150), WHITE)
    txt(can, t, w('Oberbürgermeister', k), (W / 2, 640), 'SPÄTER OBERBÜRGERMEISTER VON STUTTGART', bebas(66), CREAM); return can

# ================= K9 =================
def ov_1945(can, t, w0, w1): tw(can, t, w0 + 0.5, 'NACH 1945', 960, 70); sub(can, t, w('Gegner', 101), 'RUHM DURCH DIE FRÜHEREN GEGNER', 1035, 54, YEL)
def s_books(t, w0, w1):
    can = plain(); k = 102; tb = w('Bücher', k) - 0.4
    cols = [(150, 40, 40), (40, 70, 110), (200, 170, 90), (60, 90, 60), (120, 100, 80)]
    for i in range(5):
        t0 = tb + i * 0.18
        if t < t0: continue
        y = lerp(-200, 780 - i * 70, eout((t - t0) / 0.5)); shape(can, [(260 + (i % 2) * 20, y), (760 + (i % 2) * 20, y), (760 + (i % 2) * 20, y + 64), (260 + (i % 2) * 20, y + 64)], cols[i], CREAM, 3)
    txt(can, t, tb, (520, 330), 'BÜCHER', anton(96), WHITE); txt(can, t, w('Großbritannien', k), (520, 230), 'GROSSBRITANNIEN', bebas(56), GREY)
    th = w('Hollywood', k)
    if t > th:
        off = ((t - th) * 160) % 150; L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rectangle((1100, 380, 1700, 700), fill=(20, 20, 22, 255))
        for j in range(-1, 6): x = 1100 + j * 150 - off; d.rectangle((x + 15, 420, x + 135, 660), outline=(200, 194, 180, 255), width=3)
        for j in range(-1, 18): x = 1100 + j * 40 - off * 0.8 % 40; d.rectangle((x, 388, x + 18, 404), fill=(200, 194, 180, 255)); d.rectangle((x, 676, x + 18, 692), fill=(200, 194, 180, 255))
        L.putalpha(Image.fromarray((np.asarray(L.getchannel('A')) * clamp((t - th) / 0.4)).astype(np.uint8))); m_ = Image.new('L', (W, H), 0); ImageDraw.Draw(m_).rectangle((1100, 380, 1700, 700), fill=255)
        L.putalpha(Image.fromarray(np.minimum(np.asarray(L.getchannel('A')), np.asarray(m_)))); can.alpha_composite(L)
        txt(can, t, th, (1400, 330), 'HOLLYWOOD', anton(96), YEL)
    return can
def ov_fair(can, t, w0, w1): cap(can, t, w('fairen', 103), '„DER FAIRE KRIEG IN DER WÜSTE“', 960, 84, YEL)
def ov_sand(can, t, w0, w1): sub(can, t, w('keine', 103), '„KEINE IDEOLOGIE,', 940, 70, WHITE); sub(can, t, w('nur', 103), 'NUR ZWEI ARMEEN IM SAND“', 1020, 70, WHITE)
def s_kaserne(t, w0, w1):
    can = plain(); k = 104; gy = 820
    lines(can, t, w0, [[(0, gy), (W, gy)], [(560, gy), (560, 380), (660, 380), (660, gy)], [(1260, gy), (1260, 380), (1360, 380), (1360, gy)], [(660, 760), (1260, 760)], [(660, 640), (1260, 640)]], 1.2, CREAM, 6)
    for x in range(700, 1260, 60): lines(can, t, w0 + 0.8, [[(x, 640), (x, 760)]], 0.4, GREY, 4)
    tk = w('Kasernen', k)
    if t > tk:
        u = eout((t - tk) / 0.5); shape(can, [(640, 300 - 40 * u), (1280, 300 - 40 * u), (1280, 300 + 40 * u), (640, 300 + 40 * u)], (40, 44, 50), WHITE, 4)
        if u > 0.9: txt(can, t, tk + 0.4, (960, 300), 'ROMMEL-KASERNE', anton(62), WHITE)
    cap(can, t, w('Bundeswehr', k), 'DIE NEUE BUNDESWEHR', 140, 78, YEL); sub(can, t, w('Vorbilder', k), 'SUCHT VORBILDER', 210, 56, WHITE); return can
def ov_krit(can, t, w0, w1): cap(can, t, w('Historiker', 105), 'HISTORIKER HEUTE:', 900, 70, WHITE); cap(can, t, w('kritischer', 105), 'DEUTLICH KRITISCHER', 1000, 90, YEL)
RANKS = [('1939', 'GENERALMAJOR'), ('1941', 'GENERALLEUTNANT'), ('1941', 'GENERAL DER PANZERTRUPPE'), ('1942', 'GENERALOBERST'), ('1942', 'GENERALFELDMARSCHALL')]
def s_stairs(t, w0, w1):
    can = plain(); k = 106; t0 = w('steilen', k) - 0.3
    for i, (yr, rk) in enumerate(RANKS):
        ti = t0 + i * 0.55; x = 200 + i * 320; y = 880 - i * 150
        lines(can, t, ti, [[(x, y + 150 if i else 1000), (x, y), (x + 320, y)]], 0.4, YEL if i == 4 else CREAM, 7)
        txt(can, t, ti + 0.1, (x + 160, y - 40), yr, bebas(52), YEL); txt(can, t, ti + 0.2, (x + 160, y + 50), rk, bebas(40 if len(rk) > 16 else 46), WHITE)
    sub(can, t, w('nahe', k), 'UND STAND IHR LANGE NAHE', 140, 66, YEL); return can
def ov_civ(can, t, w0, w1): sub(can, t, w('weniger', 107), 'IN NORDAFRIKA: „WENIGER BRUTAL“ ALS IM OSTEN', 950, 60, WHITE); cap(can, t, w('Zivilisten', 107), 'AUCH DORT LITTEN ZIVILISTEN', 1025, 66, YEL)
TUNM = Map(9.8, 35.3, 9.0, hi=('Tunisia',))
def ov_tunj(can, t, w0, w1, z):
    k = 107; m = TUNM; tn = m.p(10.18, 36.8, z); dot(can, *tn, YEL, 12); label(can, t, w0 + 0.2, tn[0] + 26, tn[1] - 10, 'TUNIS', 60, YEL)
    label(can, t, w0 + 0.3, m.p(9.0, 35.6, z)[0], m.p(9.0, 35.6, z)[1], 'TUNESIEN', 96, GREY, 'mm')
    sub(can, t, w('Juden', k), 'JUDEN UNTER DEUTSCHER BESATZUNG', 940, 62, WHITE); cap(can, t, w('Zwangsarbeit', k), 'ZWANGSARBEIT', 1020, 84, RED)
def ov_resp(can, t, w0, w1): sub(can, t, w('Verantwortlich', 108), 'VERANTWORTLICH: ANDERE DIENSTSTELLEN', 950, 62, WHITE); sub(can, t, w('nicht', 108), 'NICHT ROMMELS STAB', 1025, 58, YEL)
def ov_open(can, t, w0, w1): cap(can, t, w('offen', 109) - 0.3, 'WIE VIEL ER WUSSTE: OFFEN', 980, 80, YEL)
def s_minefield(t, w0, w1):
    can = plain(); k = 110; gy = 470
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.rectangle((0, gy, W, H), fill=(70, 60, 40, int(255 * clamp((t - w0) / 0.6)))); can.alpha_composite(L)
    lines(can, t, w0, [[(x, gy + 6 * math.sin(x / 70)) for x in range(0, W + 1, 30)]], 0.8, SAND, 6)
    tm = w('Minen', k)
    for i, (x, y) in enumerate(((300, 620), (560, 700), (820, 600), (1080, 690), (1340, 610), (1600, 700))):
        if t > tm + i * 0.15:
            a = clamp((t - tm - i * 0.15) / 0.3); shape(can, [(x - 70, y), (x - 50, y - 26), (x + 50, y - 26), (x + 70, y), (x + 50, y + 16), (x - 50, y + 16)], (40, 40, 36), GREY, 4, a)
            lines(can, t, tm + i * 0.15, [[(x, y - 26), (x, gy)]], 0.3, (120, 110, 90), 3)
    cap(can, t, w('Nordafrika', k), 'MINEN IN NORDAFRIKA', 200, 90, WHITE); cap(can, t, w('heute', k), 'TEILWEISE BIS HEUTE IM BODEN', 960, 80, YEL); return can
def s_memorial(t, w0, w1):
    can = plain(); k = 111; gy = 860
    lines(can, t, w0, [[(0, gy), (W, gy)], [(560, gy), (560, 300), (840, 300), (840, gy)], [(530, 300), (870, 300)], [(530, 270), (870, 270), (870, 300)]], 1.2, CREAM, 6)
    txt(can, t, w('Denkmal', k), (700, 580), 'DENKMAL', bebas(56), CREAM)
    tf = w('Figur', k)
    if t > tf:
        a = clamp((t - tf) / 0.6); x = 1220
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = (20, 20, 22, int(255 * a)); o = YEL + (int(255 * a),)
        d.ellipse((x - 40, 470, x + 40, 550), fill=c, outline=o, width=4); d.polygon([(x - 55, 570), (x + 55, 570), (x + 45, 720), (x - 45, 720)], fill=c, outline=o, width=4)
        d.polygon([(x - 40, 720), (x - 8, 720), (x - 14, gy), (x - 40, gy)], fill=c, outline=o, width=4); d.polygon([(x + 8, 720), (x + 40, 720), (x + 36, gy), (x + 14, gy)], fill=c, outline=o, width=4)
        can.alpha_composite(L); txt(can, t, tf + 0.2, (1220, 930), 'FIGUR EINES MINENOPFERS', bebas(56), YEL)
    cap(can, t, w('Heidenheim', k), 'HEIDENHEIM', 130, 90, WHITE); sub(can, t, w('2020', k), 'SEIT 2020', 210, 60, YEL); return can
def ov_officer(can, t, w0, w1): sub(can, t, w('vorne', 112), 'FÜHRTE VON VORNE', 950, 66, WHITE); sub(can, t, w('Gespür', 112), 'GESPÜR FÜR BILDER', 1025, 66, YEL)
def ov_general(can, t, w0, w1): sub(can, t, w('missachtete', 113), 'MISSACHTETE BEFEHLE', 950, 66, WHITE); sub(can, t, w('Tod', 113) - 0.3, 'VON DER EIGENEN FÜHRUNG IN DEN TOD GEZWUNGEN', 1025, 56, YEL)
def s_ask(t, w0, w1):
    can = plain(); k = 114
    txt(can, t, w('Wie', k), (W / 2, 330), 'WIE SEHT IHR', anton(110), WHITE); txt(can, t, w('Erwin', k), (W / 2, 500), 'ERWIN ROMMEL?', anton(150), YEL)
    txt(can, t, w('Schreibt', 115), (W / 2, 760), 'SCHREIBT ES IN DIE KOMMENTARE', bebas(76), CREAM); return can

import importlib.util as _iu
_sp = _iu.spec_from_file_location('anim2', B + '../logo/anim2.py'); _an = _iu.module_from_spec(_sp); _sv = sys.argv; sys.argv = ['x', B + '../logo']; _sp.loader.exec_module(_an); sys.argv = _sv
def s_logo(t, w0, w1): return _an.frame(max(0.0, t - LOGO_T)).convert('RGBA')
# ---------- timeline: (start time, scene) ; each scene starts at the first word of its sentence ----------
def at(k, word=None): return (ST[k] if word is None else w(word, k)) - 0.15
ANCH = [
 (0.0, s_intro),
 (at(5), s_official), (at(7), P('r41', 'pan', 1, ov_lying)),
 (at(9), P('r12', 'fit', ov=ov_name, z1=1.08)), (at(10), P('r43', 'fit', ov=ov_who, z1=1.08)),
 (at(11), P('r11', 'fit', ov=lambda c, t, a, b: tw(c, t, w('1917', 11), 'OKTOBER 1917', 960, 70), z1=1.06)), (at(12), MAP(ISO, ov_iso)), (at(13), P('r04', 'pan', -1, ov_sleep)),
 (at(14), s_tactic), (at(15), s_matajur), (at(16), s_9000), (at(17), P('r17', 'fit', ov=ov_pour, z1=1.12)), (at(18), MAP(GER, ov_heid, 1.05)),
 (at(19), P('r16', 'fit', z1=1.06)), (at(20), s_three), (at(21), s_type), (at(22), P('r42', 'fit', ov=ov_book, z1=1.1)),
 (at(24), MAP(POL, ov_pol)), (at(24, 'Sicherheit'), P('r15', 'pan', 1, ov_hq)), (at(25), P('r13', 'pan', -1, ov_pzdiv)), (at(26), s_units),
 (at(27), P('r23', 'pan', 1, lambda c, t, a, b: tw(c, t, a + 0.5, 'MAI 1940', 960, 70))), (at(28), MAP(FR, ov_fr)), (at(30), s_ghost), (at(31), P('r18', 'pan', 1, ov_front)),
 (at(32), P('r21', 'pan', -1, ov_valery)), (at(33), s_bars), (at(36), P('r28', 'fit', ov=ov_cam, z1=1.06)),
 (at(37), P('r31', 'fit', ov=ov_report)), (at(37, 'Heimat'), s_leader),
 (at(38), C(0.2, 4.1, ov_libya)), (at(39), C(8.3, 13.6, ov_dak)), (at(40), s_order), (at(41), P('r25', 'fit', ov=ov_trotz, z1=1.1)), (at(42), MAP(LIB, ov_lib)),
 (at(44), C(33.0, 35.6, ov_siege)), (at(45), P('r05', 'pan', 1, ov_supply)), (at(46), MAP(MED, ov_med, 1.05)), (at(47), P('r14', 'fit', ov=ov_plan)), 
 (at(48), s_paper), (at(49, 'Wüstenfuchs'), P('r07', 'fit', ov=ov_fox, z1=1.1)), (at(50), C(27.3, 32.4, ov_auch)), (at(51), s_letter), (at(52), s_strike),
 (at(53), C(38.0, 40.9, ov_tob42a)), (at(53, 'mehr'), C(41.0, 43.0, ov_tob42)), (at(54), P('r24', 'fit', ov=ov_gfm, z1=1.08)),
 (at(56), C(22.2, 27.2)), (at(57), MAP(EGY, ov_egy)), (at(58), s_monty), (at(59), C(35.6, 38.0, ov_battle)), (at(60), MAP(EUA, ov_kur, 1.05)),
 (at(61), P('r26', 'fit', ov=ov_12)), (at(62), s_order2), (at(63), P('r30', 'pan', 1, ov_retreat)), (at(64), MAP(NA, ov_tun)), (at(65), s_250), (at(66), P('r27', 'pan', -1, grey=0.8)),
 (at(67), P('r33', 'pan', 1, ov_ende43)), (at(68), MAP(WALL, ov_wall)), (at(69), P('r20', 'pan', 1, ov_mines)), (at(69, 'schräge'), s_obst), (at(70), s_spargel), (at(71), s_clock),
 (at(72), s_tanks), (at(75), MAP(NOR, ov_dday)),
 (at(78), P('r38', 'pan', -1, ov_lost)), (at(79), s_strafe), (at(82), s_files), (at(85), P('r32', 'pan', -1, ov_q)), (at(86), s_net), (at(88), s_verdacht),
 (at(89), MAP(GER2, ov_back, 1.06)), (at(91), s_generals), (at(92), s_choice), (at(94), P('r34', 'fit', ov=ov_farewell, z1=1.08)), (at(95), s_capsule),
 (at(96), P('r29', 'pan', -1, ov_ulm)), (at(97), s_quote), (at(98), P('r40', 'fit', ov=ov_mask, z1=1.1)), (at(99), s_vitrine), (at(100), s_manfred),
 (at(101), C(13.8, 18.4, ov_1945)), (at(102), s_books), (at(103), C(4.2, 8.1, ov_fair)), (at(103, 'Hier'), C(18.7, 22.0, ov_sand)), (at(104), s_kaserne),
 (at(105), P('r22', 'pan', -1, ov_krit, grey=0.5)), (at(106), s_stairs), (at(107), C(55.2, 60.7, ov_civ)), (at(107, 'Tunesien'), MAP(TUNM, ov_tunj)),
 (at(108), P('r06', 'pan', 1, ov_resp)), (at(109), P('r08', 'pan', -1, ov_open)), (at(110), s_minefield), (at(111), s_memorial),
 (at(112), P('r35', 'pan', 1, ov_officer)), (at(113), P('r10', 'fit', ov=ov_general, z1=1.08)), (at(114), s_ask)] + ([(LOGO_T, s_logo)] if LOGO else [])
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
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; P_ = Image.new('RGB', (4 * 480, ((len(ts) + 3) // 4) * 270))
        for i, t in enumerate(ts): P_.paste(frame(t).resize((480, 270)), ((i % 4) * 480, (i // 4) * 270))
        P_.save(B + sys.argv[2], quality=85); sys.exit()
    if sys.argv[1] == 'list':
        for s, e, fn in SC: print(f'{s:7.2f} {e:7.2f} {getattr(fn, "__name__", "")} {getattr(fn, "__qualname__", "")}')
        sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '8M', '-maxrate', '10M', '-bufsize', '16M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
