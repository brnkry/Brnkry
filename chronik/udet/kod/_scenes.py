# ================= Ernst Udet / Ju 87 scenes =================
def ws(word, after=0.0): return wt(word, after) - 0.05
BLUR.update({
    'u03': [(911, 240, 48), (332, 1700, 48), (1160, 1930, 60)],
    'u04': [(850, 832, 42), (1371, 918, 40), (1721, 1088, 48)],
    'u06': [(799, 171, 48), (792, 2255, 48)],
    'u07': [(1222, 1501, 42)],
})
NA = len([f for f in os.listdir(B + 'band') if f.startswith('a')]); NB = len([f for f in os.listdir(B + 'band') if f.startswith('b')])
NV = len(os.listdir(B + 'vfull')); NI = len([f for f in os.listdir(B + 'intro') if f.startswith('c')])
@functools.lru_cache(maxsize=6)
def vf(ct): return Image.open(B + 'vfull/f%05d.jpg' % max(1, min(NV, int(round(ct * FPS)) + 1))).convert('RGB')
@functools.lru_cache(maxsize=6)
def bf(ct):
    if ct >= 186: return Image.open(B + 'band/b%05d.jpg' % max(1, min(NB, int(round((ct - 186) * FPS)) + 1))).convert('RGB')
    return Image.open(B + 'band/a%05d.jpg' % max(1, min(NA, int(round((ct - 79) * FPS)) + 1))).convert('RGB')
def vshot(ct, z=1.0, cx=0.5, cy=0.5, warm=0.12, sat=0.9):
    """the vertical archive film (1080x1920), zoomed past its black bars"""
    im = vf(ct); cw, ch = 1080 / z, 1920 / z; x0 = min(max(cx * 1080 - cw / 2, 0), 1080 - cw); y0 = min(max(cy * 1920 - ch / 2, 0), 1920 - ch)
    can = grade(im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA'), warm, sat); shade(can, 200, 0.55); return can
def bshot(ct, cx=960, cy=540, z=1.0, warm=0.12, sat=0.9):
    """9:16 window into the letterboxed 16:9 film (1920x1080 coords); returns canvas and film->screen mapper"""
    im = bf(ct); ch = 1080 / z; cw = ch * W / H
    x0 = min(max(cx - cw / 2, 0), 1800 - cw); y0 = min(max(cy - ch / 2, 0), 1080 - ch)   # never reaches the archive mark in the bottom right corner
    can = grade(im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA'), warm, sat); shade(can, 200, 0.55)
    return can, (lambda x, y: ((x - x0) * W / cw, (y - y0) * H / ch))
def track(keys, ct):
    """piecewise-linear camera keys [(ct, cx, cy), ...] -> (cx, cy)"""
    if ct <= keys[0][0]: return keys[0][1:]
    for (a, x0, y0), (b, x1, y1) in zip(keys, keys[1:]):
        if ct <= b: u = eio((ct - a) / (b - a)); return lerp(x0, x1, u), lerp(y0, y1, u)
    return keys[-1][1:]

# ---------- WW2 look for the modern intro footage: colours kept, softer, warmer, film flicker and dust ----------
def ww2(can, t):
    rgb = ImageEnhance.Color(can.convert('RGB')).enhance(0.74)
    rgb = Image.blend(rgb, Image.new('RGB', (W, H), (118, 96, 64)), 0.14); rgb = ImageEnhance.Contrast(rgb).enhance(1.12)
    rgb = ImageEnhance.Brightness(rgb).enhance(1 + 0.03 * math.sin(t * 41) + 0.02 * math.sin(t * 97)).filter(ImageFilter.GaussianBlur(0.9))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); r = np.random.default_rng(int(t * FPS) + 7)
    for _ in range(r.integers(0, 3)):
        x = r.uniform(60, W - 60); d.line((x, 0, x + r.uniform(-8, 8), H), fill=(235, 228, 210, int(r.uniform(18, 45))), width=1)
    for _ in range(r.integers(2, 7)):
        x, y, s = r.uniform(0, W), r.uniform(0, H), r.uniform(1.5, 4); d.ellipse((x - s, y - s, x + s, y + s), fill=(20, 16, 12, int(r.uniform(60, 140))))
    out = rgb.convert('RGBA'); out.alpha_composite(L); return out

# ---------- the Ju 87 B-2 plan (side view traced from the plan sheet) ----------
_BP = Image.open(B + 'pdf/ju87_side.png').getchannel('A')
@functools.lru_cache(None)
def bp_level(k):
    """line art at 1/k size, lines thickened first so they stay a clean 2 px on screen"""
    a = np.asarray(_BP)
    if k > 1: a = np.asarray(Image.fromarray(a).filter(ImageFilter.MaxFilter(2 * k - 1 if k < 4 else 7)))
    im = Image.fromarray(a).resize((_BP.width // k, _BP.height // k), Image.LANCZOS) if k > 1 else Image.fromarray(a)
    return im
GEAR = (1340, 1225, 2060, 1991)        # main gear leg + spat, plan px
SIREN = (1398, 1300)                    # where the siren housing meets the leading edge of the leg fairing
def bp_map(s, th, focus, at):
    c, si = math.cos(math.radians(th)), math.sin(math.radians(th))
    return lambda x, y: (at[0] + s * ((x - focus[0]) * c + (y - focus[1]) * si), at[1] + s * (-(x - focus[0]) * si + (y - focus[1]) * c))
def bp_lines(s, th, focus, at, reveal=1.0, region=None):
    """the traced plan, as an alpha mask on the screen"""
    k = 4 if s < 0.3 else 2 if s < 0.6 else 1; src_ = bp_level(k); sk = s * k; fx, fy = focus[0] / k, focus[1] / k
    c, si = math.cos(math.radians(th)), math.sin(math.radians(th))
    a, b = c / sk, -si / sk; d_, e = si / sk, c / sk
    M = src_.transform((W, H), Image.AFFINE, (a, b, fx - a * at[0] - b * at[1], d_, e, fy - d_ * at[0] - e * at[1]), Image.BICUBIC)
    if region is not None or reveal < 1:
        mk = Image.new('L', _BP.size, 0); dm = ImageDraw.Draw(mk)
        if region is not None: dm.rectangle(region, fill=255)
        else: dm.rectangle((0, 0, _BP.width * reveal, _BP.height), fill=255)
        mk = mk.resize(src_.size).transform((W, H), Image.AFFINE, (a, b, fx - a * at[0] - b * at[1], d_, e, fy - d_ * at[0] - e * at[1]), Image.BILINEAR)
        M = Image.fromarray((np.asarray(M, np.float32) * np.asarray(mk, np.float32) / 255).astype(np.uint8))
    return M
def bp_paint(can, M, col, a=1.0, glow=True, gain=None):
    if glow:
        G = Image.new('RGBA', (W, H), (0, 0, 0, 0)); G.putalpha(M.filter(ImageFilter.GaussianBlur(5)).point(lambda v: int(min(255, v * 2.2) * 0.7 * a))); can.alpha_composite(G)
    L = Image.new('RGBA', (W, H), col + (0,)); g_ = 1.6 if gain is None else gain; L.putalpha(M.point(lambda v: int(min(255, v * g_) * a))); can.alpha_composite(L)
def grid(can, a):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for x in range(-20, W, 60): d.line((x, 0, x, H), fill=CREAM + (int(16 * a),), width=1)
    for y in range(0, H, 60): d.line((0, y, W, y), fill=CREAM + (int(16 * a),), width=1)
    can.alpha_composite(L)
def siren(can, m, s, pop, spin, ang, hl=0.0, a=1.0):
    """siren on the gear leg (plan coords mapped by m): streamlined housing, a two-blade wind propeller at its nose.
    pop 0..1 grows it in, spin 0..1 how fast the propeller turns (1 = a blurred disc), ang its angle"""
    if pop <= 0: return
    sc = eout(pop); cx, cy = SIREN[0] - 95, SIREN[1]
    def P(x, y): return m(cx + (x - cx) * sc, cy + (y - cy) * sc)
    col = tuple(int(lerp(c1, c2, hl)) for c1, c2 in zip(CREAM, YEL)); A = int(255 * a)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    body = [P(SIREN[0] + 6, cy - 52), P(cx + 10, cy - 58), P(cx - 60, cy - 46), P(cx - 92, cy - 22), P(cx - 98, cy), P(cx - 92, cy + 22), P(cx - 60, cy + 46), P(cx + 10, cy + 58), P(SIREN[0] + 6, cy + 52)]
    d.polygon(body, fill=(14, 22, 30, int(200 * a)))
    lw = max(2, int(5 * s / 0.4))
    d.line(body + [body[0]], fill=col + (A,), width=lw, joint='curve')
    for xx in (cx - 30, cx + 20): d.line((P(xx, cy - 54), P(xx, cy + 54)), fill=col + (int(A * 0.6),), width=max(1, lw // 2))
    # air slots
    for k in range(3): d.line((P(cx - 10 + k * 22, cy - 30), P(cx - 10 + k * 22, cy + 30)), fill=col + (int(A * 0.45),), width=max(1, lw // 2))
    hub = P(cx - 104, cy); R = 112 * sc
    d.ellipse(_box(P(cx - 112, cy), 9 * s / 0.4 * sc), fill=col + (A,))
    if spin > 0.05:   # the turning disc, seen edge-on: a thin translucent ellipse along the blades' sweep
        p0, p1 = P(cx - 108, cy - 112), P(cx - 108, cy + 112)
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2; D = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(D)
        dd.line((p0, p1), fill=col + (int(110 * spin * a),), width=int(max(6, 16 * s / 0.4)))
        can.alpha_composite(D.filter(ImageFilter.GaussianBlur(4)))
    if spin < 0.95:
        k_ = math.cos(ang); bl = (1 - spin)
        for sg in (1, -1):
            d.line((P(cx - 108, cy), P(cx - 108 + 6 * math.sin(ang) * sg, cy + sg * 112 * k_)), fill=col + (int(A * bl),), width=max(3, int(9 * s / 0.4)))
    can.alpha_composite(L)
def _box(p, r): return (p[0] - r, p[1] - r, p[0] + r, p[1] + r)
def flow(can, m, t, spd, a, ys=(1200, 1252, 1300, 1350, 1402), x0=250, x1=1800, seg=150, gap=110):
    """relative wind streaming past the siren from ahead (dashes moving nose -> tail in plan coords)"""
    if a <= 0: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); per = seg + gap
    for j, y in enumerate(ys):
        off = (t * spd + j * 61) % per
        for x in np.arange(x0 - per + off, x1, per):
            xa, xb = max(x, x0), min(x + seg, x1)
            if xb <= xa: continue
            yb = y + (0 if abs(y - SIREN[1]) > 140 else 10 * math.sin((xa - SIREN[0]) / 120))
            fa = clamp((xa - x0) / 300) * clamp((x1 - xb) / 300)
            d.line((m(xa, yb), m(xb, yb)), fill=(150, 205, 235, int(200 * a * fa)), width=4)
    can.alpha_composite(L)
def waves(can, c, t, amp, a, ang=0.0):
    """the howl: rings leaving the siren, more and brighter as the dive gets faster"""
    if a <= 0: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); per = lerp(0.5, 0.16, amp)
    for k in range(10):
        ph = ((t / per) + k / 10 * (1 / per) * per / per) % 1.0 if False else ((t + k * per) / (per * 10)) % 1.0
        r = 60 + ph * lerp(260, 520, amp); al = (1 - ph) ** 1.5 * a * lerp(0.35, 1.0, amp)
        if al < 0.02: continue
        d.arc(_box(c, r), ang - 70, ang + 70, fill=YEL + (int(230 * al),), width=int(lerp(3, 8, amp)))
        d.arc(_box(c, r), ang + 110, ang + 250, fill=YEL + (int(150 * al),), width=int(lerp(2, 6, amp)))
    can.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.2)))
def label_line(can, t, t0, s_, p_from, p_to, size=58, col=YEL, t1=None):
    """leader line from a point on the drawing to a label"""
    if t < t0 or (t1 is not None and t > t1 + 0.25): return
    u = eio((t - t0) / 0.35); a = 1.0 if t1 is None else 1 - clamp((t - t1) / 0.25)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); e = (lerp(p_from[0], p_to[0], u), lerp(p_from[1], p_to[1], u))
    d.line((p_from, e), fill=(0, 0, 0, int(150 * a)), width=8); d.line((p_from, e), fill=col + (int(255 * a),), width=4); d.ellipse(_box(p_from, 9), fill=col + (int(255 * a),))
    can.alpha_composite(L)
    if u > 0.6: title(can, t, t0 + 0.25, s_, p_to[1] + (-40 if p_to[1] < p_from[1] else 40), size, col, t1, 'bebas', p_to[0])

def blueprint_bg(ct, t, k=1.0):
    """the Stuka film keeps running, blurred and darkened, under the drawing"""
    bg, _ = bshot(ct, 960, 540, 1.0); bg = bg.filter(ImageFilter.GaussianBlur(lerp(0, 14, k)))
    can = Image.blend(bg, Image.new('RGBA', (W, H), (10, 18, 26, 255)), 0.62 * k); grid(can, k); return can

# camera of the drawing: (time, scale, dive angle, focus x, focus y, screen x, screen y)
def cam(keys, t):
    if t <= keys[0][0]: return keys[0][1:]
    for A_, B_ in zip(keys, keys[1:]):
        if t <= B_[0]: u = eio((t - A_[0]) / (B_[0] - A_[0])); return tuple(lerp(p, q, u) for p, q in zip(A_[1:], B_[1:]))
    return keys[-1][1:]
CTR = (2725, 1000)
def s_anim1(t, w0, w1):
    k = clamp((t - w0) / 0.5); can = blueprint_bg(BG1 + (t - w0), t, k)
    t_gear, t_prop = ws('Fahrwerksbeinen'), ws('kleine', 44)
    t_wind, t_fast, t_loud, t_jer = ws('Fahrtwind'), ws('je', 47), ws('lauter', 49), ws('Jericho')
    keys = [(w0, 0.19, 0, *CTR, 520, 820), (t_gear - 0.1, 0.19, 0, *CTR, 520, 820), (t_gear + 0.9, 0.50, 0, 1560, 1450, 600, 860),
            (t_prop + 0.6, 0.85, 0, 1350, 1330, 620, 860), (t_wind + 0.3, 0.85, 0, 1350, 1330, 620, 860), (t_fast - 0.1, 0.80, 0, 1400, 1340, 620, 860),
            (t_fast + 1.4, 0.2, 72, *CTR, 540, 860), (t_jer - 0.6, 0.21, 72, *CTR, 540, 860), (t_jer + 0.3, 0.36, 72, 1500, 1350, 560, 940), (w1, 0.38, 72, 1480, 1340, 560, 940)]
    s, th, fx, fy, ax, ay = cam(keys, t); m = bp_map(s, th, (fx, fy), (ax, ay))
    M = bp_lines(s, th, (fx, fy), (ax, ay), reveal=eio((t - w0) / 0.9)); bp_paint(can, M, CREAM, 0.95, gain=lerp(3.2, 1.6, clamp((s - 0.2) / 0.3)))
    hl = clamp((t - t_gear) / 0.3) * (1 - 0.6 * clamp((t - t_prop - 0.3) / 0.4))
    if hl > 0: bp_paint(can, bp_lines(s, th, (fx, fy), (ax, ay), region=GEAR), YEL, hl, False)
    # propeller speed: still, then the wind turns it, faster in the dive
    spin = clamp((t - t_wind - 0.3) / 0.9) * lerp(0.55, 1.0, clamp((t - t_fast) / 1.6)); ang = (t - t_wind) * lerp(4, 30, spin) if t > t_wind else 0.0
    vel = lerp(500, 2600, clamp((t - t_fast) / 1.6))
    flow(can, m, t, vel, clamp((t - t_wind) / 0.4))
    siren(can, m, s, clamp((t - t_prop) / 0.45), spin, ang, hl=clamp((t - t_jer) / 0.3))
    c = m(SIREN[0] - 205, SIREN[1]); amp = clamp((t - t_fast - 0.3) / 1.2) * 0.45 + clamp((t - t_loud) / 0.8) * 0.55
    waves(can, c, t, amp, clamp((t - t_fast) / 0.5), ang=180 - th)
    # labels: kept few and to the left of the buttons
    if t < t_fast:
        label_line(can, t, t_prop + 0.3, 'PROPELLER', m(SIREN[0] - 205, SIREN[1] - 100), (300, 520), 60, YEL, t_wind - 0.1)
        label_line(can, t, t_wind + 0.15, 'FAHRTWIND', m(700, 1190), (300, 1180), 60, (150, 205, 235), t_fast - 0.15)
    if t_wind < t < t_fast + 0.3:
        A = m(900, 1305); Bp = m(1150, 1305); arrow_to(can, A, Bp, eio((t - t_wind - 0.1) / 0.4), (150, 205, 235), 12, 38)
    if t >= t_jer - 0.05:
        ringp(can, t, t_jer - 0.05, *m(SIREN[0] - 110, SIREN[1]), 150 * s / 0.42, YEL)
        title(can, t, t_jer - 0.05, 'JERICHO-TROMPETE', 400, 104, YEL)
    return can
def s_anim2(t, w0, w1):
    k = clamp((t - w0) / 0.4); can = blueprint_bg(BG2 + (t - w0), t, k)
    t_br = ws('bremsten')
    s, th, fx, fy, ax, ay = cam([(w0, 0.2, 72, *CTR, 540, 860), (w1, 0.22, 72, *CTR, 540, 860)], t); m = bp_map(s, th, (fx, fy), (ax, ay))
    bp_paint(can, bp_lines(s, th, (fx, fy), (ax, ay), reveal=eio((t - w0) / 0.5)), CREAM, 0.95, gain=3.2)
    siren(can, m, s, clamp((t - w0) / 0.3), 1.0, 0, hl=1.0)
    flow(can, m, t, 2400, clamp((t - w0) / 0.3))
    waves(can, m(SIREN[0] - 205, SIREN[1]), t, 0.8, clamp((t - w0) / 0.4), ang=180 - th)
    if t > t_br:   # drag: arrows pushing back against the dive, along the plane's axis towards the tail
        for dy in (-330, 330):
            arrow_to(can, m(SIREN[0] - 500, SIREN[1] + dy * 1.6), m(SIREN[0] + 450, SIREN[1] + dy * 1.6), eio((t - t_br - abs(dy) / 1500) / 0.45), RED, 14, 44)
        title(can, t, t_br, 'BREMST', 400, 120, RED)
    return can

# ---------- the film and the photos ----------
def s_intro(t, w0, w1):
    # the old film from just below its burned-in headline: a 9:16 window (x 360..1080, y 640..1920 of the 1080x1920 frame)
    k = min(437, int(t * FPS)); im = Image.open(B + 'intro/o%04d.jpg' % (265 + 2 * k)).convert('RGB')
    can = im.resize((W, H), Image.BICUBIC, box=(360, 640, 1080, 1920)).convert('RGBA')
    can = ww2(can, t); shade(can, 170, 0.6); return can
def s_name(t, w0, w1):
    can = vshot(min(2.15, t - w0), 1.06, 0.5, 0.48, 0.1, 0.95)
    title(can, t, ws('Ernst') - 0.05, 'ERNST UDET', 1260, 150, CREAM, None, bold=1)
    return can
def s_ww1(t, w0, w1):
    can, m = side('u02', 700, 820, t, w0, w1, 1.05)
    for s_, cx_, cy_, h_, t0 in (('62', 1080, 660, 230, ws('62') - 0.05), ('ABSCHÜSSE', 1075, 870, 58, ws('Flugzeuge', 15) - 0.05)):   # on the white panel beside his face
        if t > t0: on_quad(can, [m(*v) for v in tquad(cx_, cy_, s_, h_)], s_, 200, clamp((t - t0) / 0.06), INK, anton(200), eio((t - t0) / 0.4), 0.8, mod=0.35, op=0.93)
    return can
def s_richt(t, w0, w1):
    can = grade(fit('u09', t, w0, w1, 1.07)); shade(can, 210, 0.5)
    title(can, t, ws('Manfred') - 0.05, 'MANFRED VON RICHTHOFEN', 1330, 78, CREAM, None, 'bebas')
    return can
def s_show(t, w0, w1):
    can = vshot(9.4 + (t - w0), 1.42, 0.5, 0.5, 0.12, 0.9)
    sky(can, t, ws('Amerika') - 0.05, 'AMERIKA', CX, 420, 120, CREAM, None, 0.5)
    title(can, t, ws('Sturzkampfbomber', 22) - 0.05, 'CURTISS HAWK II', 1240, 110, YEL, None, bold=1)
    return can
def s_dive(t, w0, w1):
    return vshot(28.4 + (t - w0), 1.12, 0.5, 0.5, 0.12, 0.9)
def s_goering(t, w0, w1):
    can, m = side('u04', 900, 1300, t, w0, w1, 1.05)
    gx, gy = m(1530, 520); ringp(can, t, ws('Hermann', 26) - 0.05, gx, gy, 250, YEL, 'HERMANN GÖRING', gy + 305)
    return can
def s_buy(t, w0, w1):
    can, m = side('u01', 450, 600, t, w0, w1, 1.05)
    t0 = ws('1933') - 0.05   # on his jacket, across the chest
    if t > t0: on_quad(can, [m(*v) for v in tquad(1180, 930, '1933', 170, tilt=-6)], '1933', 200, clamp((t - t0) / 0.06), INK, anton(200), eio((t - t0) / 0.4), 0.9, mod=0.45, op=0.9)
    title(can, t, ws('zwei', 29) - 0.05, 'ZWEI MASCHINEN', 1300, 96, CREAM, None, 'bebas')
    return can
def s_germany(t, w0, w1):
    return vshot(17.85 + (t - w0), 1.15, 0.5, 0.5, 0.12, 0.9)
def s_danger(t, w0, w1):
    can = vshot(35.2 + (t - w0), 1.12, 0.5, 0.5, 0.12, 0.9)
    sky(can, t, ws('gefährlich') - 0.05, 'ZU GEFÄHRLICH', CX, 420, 120, CREAM, None, 0.55)
    if t > ws('doch', 36) - 0.05:
        f = anton(120); bb = f.getbbox('ZU GEFÄHRLICH'); w_ = bb[2] - bb[0] + 20; strike(can, t, ws('doch', 36) - 0.05, (CX - w_ / 2, 420 - 50, CX + w_ / 2, 420 + 40), RED, 12, 0.4)
    return can
STK = [(80.0, 760, 560), (81.2, 900, 560), (82.4, 1000, 520), (84.9, 1150, 520)]
def s_stuka(t, w0, w1):
    ct = 80.0 + (t - w0); cx, cy = track(STK, ct); can, m = bshot(ct, cx, cy, 1.0)
    title(can, t, ws('Junkers', 40) - 0.05, 'JUNKERS JU 87', 380, 112, CREAM, None, bold=1)
    title(can, t, ws('Stuka', 42) - 0.05, 'STUKA', 1270, 170, YEL, None, bold=1)
    return can
def s_poland(t, w0, w1):
    ct = 103.0 + (t - w0); cx, cy = track([(103.0, 900, 540), (105.9, 1000, 540)], ct); can, m = bshot(ct, cx, cy, 1.0)
    sky(can, t, ws('Polen', 54) - 0.05, 'POLEN', CX, 380, 110, CREAM, None, 0.4)
    sky(can, t, ws('Frankreich', 54) - 0.05, 'FRANKREICH', CX, 520, 110, CREAM, None, 0.5)
    return can
def s_field(t, w0, w1):
    ct = 117.0 + (t - w0); can, m = bshot(ct, 1000, 540, 1.0); return can
def s_bomb(t, w0, w1):
    ct = 112.0 + (t - w0); cx, cy = track([(112.0, 860, 540), (113.0, 1400, 540)], ct); can, m = bshot(ct, cx, cy, 1.0); return can
def s_d(t, w0, w1):
    can, m = side('u08', 650, 350, t, w0, w1, 1.04)
    t_ab = ws('abgebaut')
    if t > t_ab - 0.05:
        x, y = m(870, 1240); ringp(can, t, t_ab - 0.05, x, y, 95, RED)
        sky(can, t, t_ab - 0.05, 'ABGEBAUT', 300, 650, 96, RED, None, 0.45)   # in the empty sky left of the planes
    return can
def s_glzm(t, w0, w1):
    can = grade(fit('u03', t, w0, w1, 1.08, top=0.4)); shade(can, 220, 0.5)
    typed(can, t, ws('Generalluftzeugmeister') - 0.05, 'GENERALLUFTZEUGMEISTER', 1290, 74, YEL, 0.04)
    return can
def s_prod(t, w0, w1):
    ct = 150.0 + (t - w0); cx, cy = track([(150.0, 700, 540), (152.2, 1100, 540)], ct); can, m = bshot(ct, cx, cy, 1.0)
    return can
def s_kunst(t, w0, w1):
    can = vshot(42.0 + (t - w0), 1.12, 0.5, 0.5, 0.12, 0.9)
    sky(can, t, ws('Kunstflieger') - 0.05, 'KUNSTFLIEGER', CX, 420, 120, CREAM, None, 0.55)
    return can
def s_losses(t, w0, w1):
    ct = 186.4 + (t - w0); cx, cy = track([(186.4, 700, 540), (187.6, 1000, 540)], ct); can, m = bshot(ct, cx, cy, 1.0); return can
def s_blame(t, w0, w1):
    can, q = side('u07', 0, 442, t, w0, w1, 1.03); shade(can, 200, 0.55)
    gx, gy = q(560, 560); ringp(can, t, ws('Göring', 78) - 0.05, gx, gy, 170, YEL, 'GÖRING', gy - 230)
    t2 = ws('Schuld') - 0.05
    if t > t2: on_quad(can, [q(*v) for v in rquad(1310, 1640, 'SCHULD', 130, -4)], 'SCHULD', 150, clamp((t - t2) / 0.06), (190, 40, 36), anton(150), eio((t - t2) / 0.35), 0.8, mod=0.25, op=0.97, glow=((0, 0, 0), 8, 0.5))
    return can
def s_death(t, w0, w1):
    can = fit('u06', t, w0, w1, 1.06, top=0.3); can = night(grade(can, 0.06, 0.55), lerp(0.2, 0.55, prog(t, w0, w1))); shade(can, 220, 0.5)
    title(can, t, ws('17.') - 0.05, '17. NOVEMBER 1941', 1300, 104, CREAM, None, bold=1)
    return can
def s_official(t, w0, w1):
    can = grade(fit('u05', t, w0, w1, 1.06)); shade(can, 200, 0.55)
    title(can, t, ws('Offiziell') - 0.05, 'OFFIZIELL', 255, 96, CREAM, None, bold=1)
    q = lambda x, y: fitpt('u05', t, w0, w1, 1.06, x, y); t0 = ws('verunglückt') - 0.05   # on his jacket
    if t > t0: on_quad(can, [q(*v) for v in rquad(1060, 1460, 'UNFALL', 190, -6)], 'UNFALL', 200, clamp((t - t0) / 0.06), (178, 34, 32), anton(200), eio((t - t0) / 0.35), 0.8, mod=0.35, op=0.95)
    return can

ANCH = [
 (0.0, s_intro, None),
 (ws('Sein', 11) - 0.15, s_name, ('fade',)),
 (ws('Im', 13) - 0.1, s_ww1, ('fade',)),
 (ws('außer') - 0.1, s_richt, ('fade',)),
 (ws('In', 21) - 0.1, s_show, ('fade',)),
 (ws('die', 23.5) - 0.1, s_dive, ('fade',)),
 (ws('Mit', 26) - 0.1, s_goering, ('fade',)),
 (ws('1933') - 0.15, s_buy, ('fade',)),
 (ws('brachte') - 0.1, s_germany, ('fade',)),
 (ws('Viele') - 0.1, s_danger, ('fade',)),
 (ws('Er', 38.5) - 0.1, s_stuka, ('fade',)),
 (ws('An', 43) - 0.1, s_anim1, ('fade',)),
 (ws('In', 54) - 0.1, s_poland, ('fade',)),
 (ws('Soldaten') - 0.1, s_field, ('fade',)),
 (ws('noch', 59) - 0.1, s_bomb, ('fade',)),
 (ws('Doch', 61) - 0.1, s_anim2, ('fade',)),
 (ws('später', 63) - 0.1, s_d, ('fade',)),
 (ws('Udet', 66) - 0.1, s_glzm, ('fade',)),
 (ws('Flugzeugproduktion') - 0.1, s_prod, ('fade',)),
 (ws('Für', 72.5) - 0.1, s_kunst, ('fade',)),
 (ws('Als', 76) - 0.1, s_losses, ('fade',)),
 (ws('gab') - 0.1, s_blame, ('fade',)),
 (ws('Am', 80.5) - 0.1, s_death, ('fade',)),
 (ws('Offiziell') - 0.1, s_official, ('fade',))]
BG1 = 80.0 + ([a for a, fn, tr in ANCH if fn is s_anim1][0] - [a for a, fn, tr in ANCH if fn is s_stuka][0])   # the formation film carries on behind the drawing
BG2 = 112.0 + ([a for a, fn, tr in ANCH if fn is s_anim2][0] - [a for a, fn, tr in ANCH if fn is s_bomb][0])
