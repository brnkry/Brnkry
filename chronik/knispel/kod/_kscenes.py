
# ---------- graphics over a running film: the film blurred and darkened behind, graphics see-through on top ----------
def BG(k, a, rate=1.0, dimv=120, bl=2.2):
    def fn(t, w0):
        im = fat(k, a + max(0.0, t - w0) * rate)
        sm = im.resize((360, 640), Image.BILINEAR, box=_cover(im.size, 9 / 16)).filter(ImageFilter.GaussianBlur(bl)).resize((W, H), Image.BICUBIC)   # soft, but the film stays readable
        can = grade(sm.convert('RGBA'), 0.12, 0.85); dim(can, dimv); return can
    return fn
def plate(can, t, t0, s_, y, size, col, a=1.0, w_=760):
    """a row of the career ladder: dark see-through plate with a cream edge, slides up into place"""
    if t < t0: return
    k = eout((t - t0) / 0.35); f = anton(size); h_ = size + 50; x0 = CX - w_ / 2; yy = y + (1 - k) * 40
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((x0, yy - h_ / 2, x0 + w_, yy + h_ / 2), 14, fill=(10, 11, 14, int(150 * k * a)), outline=CREAM + (int(200 * k * a),), width=3)
    d.text((CX, yy), s_, font=f, fill=col + (int(255 * k * a),), anchor='mm'); can.alpha_composite(L)
def up_arrow(can, t, t0, x, y0, y1, col=YEL):
    if t < t0: return
    u = eio((t - t0) / 0.3); y = lerp(y0, y1, u); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line((x, y0, x, y), fill=col + (230,), width=8); d.polygon([(x - 18, y + 14), (x + 18, y + 14), (x, y - 12)], fill=col + (230,)); can.alpha_composite(L)

from scipy.ndimage import map_coordinates as _mc
TUR = (790, 900)   # turret axis x and radius (source px)
BEND, TILT = 34, 0.02   # the band lines of the turret: ends sag a little, right side a little lower   # k04: turret axis x and its visible half width (source px); the text wraps round the cylinder
def _skel(m):
    """morphological skeleton (Lantuejoul): the centre line of each pen stroke"""
    import cv2
    m = (m > 127).astype(np.uint8); sk = np.zeros_like(m); el = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    while m.any():
        e = cv2.erode(m, el); sk |= m - cv2.dilate(e, el); m = e
    return sk
def _scratch_mask(s_, size, seed):
    """big white capitals scratched into the paint: solid letters with rough, chipped edges and fine scratch lines running through them"""
    import cv2
    f = anton(size); bb = f.getbbox(s_); tw, th = bb[2] - bb[0] + 60, bb[3] - bb[1] + 60
    M = Image.new('L', (tw, th), 0); ImageDraw.Draw(M).text((30 - bb[0], 30 - bb[1]), s_, font=f, fill=255)
    A = np.asarray(M, np.float32) / 255; rng = np.random.default_rng(seed)
    n = cv2.GaussianBlur(rng.random((th, tw)).astype(np.float32), (0, 0), 1.6)
    A = np.clip((cv2.GaussianBlur(A, (0, 0), 1.2) - 0.5 + (n - 0.5) * 0.9) * 6 + 0.5, 0, 1)   # chipped edges
    S = Image.new('L', (tw, th), 0); d = ImageDraw.Draw(S)
    for _ in range(int(tw / 6)):   # tool marks along the letters
        x = rng.uniform(0, tw); y = rng.uniform(0, th); L_ = rng.uniform(10, 50); an = rng.uniform(-0.25, 0.25)
        d.line((x, y, x + L_ * math.cos(an), y + L_ * math.sin(an)), fill=int(rng.uniform(80, 200)), width=1)
    st = np.asarray(S, np.float32) / 255
    return np.clip(A * (0.88 - 0.35 * st) + (rng.random((th, tw)) < 0.004) * 0.6, 0, 1)
_SM = {}
def engrave(can, t, t0, s_, sp, y0, span, size):
    """text scratched into the curved turret steel: wraps round the cylinder, bright bare-metal lines with a dark lip, scratched in left to right"""
    if t < t0: return
    if (s_, size) not in _SM: _SM[(s_, size)] = _scratch_mask(s_, size, len(s_))
    A0 = _SM[(s_, size)]; th, tw = A0.shape; rev = eio((t - t0) / 0.9); A = A0 * np.clip((rev * (tw + 60) - np.arange(tw)) / 60, 0, 1)[None, :]
    cx, R = TUR; a = math.asin(min(0.95, tw * 0.5 / R))
    hsrc = th * (2 * R * math.sin(a)) / tw
    (X0, Y0), (X1, Y1) = sp(0, 0), sp(1000, 1000); kx, ky = (X1 - X0) / 1000, (Y1 - Y0) / 1000
    xs0, xs1 = cx - R * math.sin(a), cx + R * math.sin(a); ys0 = y0 - hsrc / 2
    bx0, bx1 = int(X0 + kx * xs0) - 4, int(X0 + kx * xs1) + 4; by0, by1 = int(Y0 + ky * (ys0 - 60)) - 4, int(Y0 + ky * (ys0 + hsrc + BEND + 60)) + 4
    bx0, by0 = max(0, bx0), max(0, by0); bx1, by1 = min(W, bx1), min(H, by1)
    if bx1 <= bx0 or by1 <= by0: return
    yy, xx = np.mgrid[by0:by1, bx0:bx1].astype(np.float32); sx = (xx - X0) / kx; sy = (yy - Y0) / ky
    th_ = np.arcsin(np.clip((sx - cx) / R, -1, 1)); u = (th_ + a) / (2 * a) * tw
    v = (sy - ys0 - BEND * (1 - np.cos(th_)) / (1 - math.cos(a)) * 0.5 - TILT * (sx - cx)) / hsrc * th   # letters follow the curve of the steel band
    G = _mc(A, [v, u], order=1, cval=0.0); G[(th_ < -a) | (th_ > a)] = 0
    shade_ = np.cos(th_) ** 1.2
    base = np.asarray(can.crop((bx0, by0, bx1, by1)).convert('RGB'), np.float32)
    lip = np.clip(np.roll(G, 2, 0) - G, 0, 1)        # thin dark wall beside each scratch
    cut = (G * shade_)[..., None]; metal = np.clip(base * 0.12 + np.array([226, 224, 218], np.float32), 0, 255)   # bare steel, still tinted by the dirt around it
    out = base * (1 - cut) + metal * cut; out = out * (1 - (lip * 0.45 * shade_)[..., None])
    can.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA'), (bx0, by0))
HELM = (1380, 640, 610, 560)   # k09: helmet dome centre and radii (source px)
def arc_text(can, t, t0, s_, sp, r0, r1, a0, a1, size, col, dur=0.6, mod=0.5):
    """words painted round the dome of the helmet: letters stand on an arc of the oval, painted in left to right, taking the texture of the steel"""
    if t < t0: return
    f = anton(size); bb = f.getbbox(s_); tw, th = bb[2] - bb[0] + 20, bb[3] - bb[1] + 20
    M = Image.new('L', (tw, th), 0); ImageDraw.Draw(M).text((10 - bb[0], 10 - bb[1]), s_, font=f, fill=255)
    A = np.asarray(M, np.float32) / 255 * np.clip((eio((t - t0) / dur) * (tw + 60) - np.arange(tw)) / 60, 0, 1)[None, :]
    cx, cy, rx, ry = HELM; (X0, Y0), (X1, Y1) = sp(0, 0), sp(1000, 1000); kx, ky = (X1 - X0) / 1000, (Y1 - Y0) / 1000
    bx0, bx1 = int(X0 + kx * (cx - rx * r1)), int(X0 + kx * (cx + rx * r1)); by0, by1 = int(Y0 + ky * (cy - ry * r1)), int(Y0 + ky * cy)
    bx0, by0 = max(0, bx0), max(0, by0); bx1, by1 = min(W, bx1), min(H, by1)
    if bx1 <= bx0 or by1 <= by0: return
    yy, xx = np.mgrid[by0:by1, bx0:bx1].astype(np.float32); ex = ((xx - X0) / kx - cx) / rx; ey = ((yy - Y0) / ky - cy) / ry
    r = np.sqrt(ex ** 2 + ey ** 2); ph = np.degrees(np.arctan2(ey, ex))
    u = (ph - a0) / (a1 - a0) * tw; v = (r1 - r) / (r1 - r0) * th
    G = _mc(A, [v, u], order=1, cval=0.0); G[(ph < a0) | (ph > a1) | (r < r0) | (r > r1)] = 0
    base = np.asarray(can.crop((bx0, by0, bx1, by1)).convert('RGB'), np.float32); lum = base.mean(2) / 255
    al = np.clip(G * (1 - mod + mod * np.clip(lum / max(lum.mean(), 0.05), 0.4, 1.6)), 0, 1) * 0.92
    glow = np.clip(np.asarray(Image.fromarray((G * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5)), np.float32) / 255, 0, 1) * 0.45
    out = base * (1 - glow[..., None]) ; out = out * (1 - al[..., None]) + np.array(col, np.float32) * al[..., None]
    can.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA'), (bx0, by0))

# ---------- scenes ----------
TOP = 330
def s_hook(t, w0, w1):
    can = grade(fit('k04', t, w0, w1, 1.08)); shade(can, 230, 0.45)
    sp = lambda x, y: fitpt('k04', t, w0, w1, 1.08, x, y)
    engrave(can, t, ws('siebzig') - 0.1, 'FAST 70 JAHRE', sp, 1232, 0.62, 128)
    engrave(can, t, ws('namenlosen'), 'NAMENLOS', sp, 1560, 0.62, 180)
    return can
def o_wall(can, t, w0, w1, m=None):
    title(can, t, ws('hinter'), 'HINTER EINER KIRCHENMAUER', TOP, 80, CREAM)
def o_lens(can, t, w0, w1, m=None):
    title(can, t, w0 + 0.05, 'EINE METALLMARKE', TOP, 100, YEL)
def s_name(t, w0, w1):
    can = grade(fit('k03', t, w0, w1, 1.07)); shade(can, 230, 0.5)
    title(can, t, ws('Kurt', 7.5), 'KURT', 1150, 120, CREAM, None, bold=1)
    title(can, t, ws('Knispel', 8), 'KNISPEL', 1310, 200, YEL, None, bold=2)
    return can
def o_wm(can, t, w0, w1, m=None):
    title(can, t, ws('Wehrmacht'), 'PANZERSOLDAT', TOP, 110, CREAM)
def s_career(t, w0, w1):
    can = BG('ku_sol', 0.3, 1.0, 60, 1.6)(t, w0)
    t1, t2, t3 = ws('Ladeschütze', 10.5), ws('Richtschütze', 11.5), ws('Kommandant', 13)
    plate(can, t, t1, 'LADESCHÜTZE', 1180, 84, CREAM if t >= t2 else YEL, 0.75 if t >= t2 else 1.0)
    up_arrow(can, t, t2 - 0.15, CX, 1110, 1040)
    plate(can, t, t2, 'RICHTSCHÜTZE', 960, 84, CREAM if t >= t3 else YEL, 0.75 if t >= t3 else 1.0)
    up_arrow(can, t, t3 - 0.15, CX, 890, 820)
    plate(can, t, t3, 'KOMMANDANT', 740, 96, YEL)
    return can
def o_tiger(can, t, w0, w1, m=None):
    title(can, t, ws('Tigers'), 'TIGER', TOP, 140, CREAM)
    title(can, t, ws('schweren'), 'SCHWERE PANZERABTEILUNG 503', 1330, 66, YEL, None, 'bebas')
SKIRT5 = [(1500, 730), (2120, 700), (2120, 880), (1500, 950)]   # k05: the side skirt plates of the Panzer IV (source px)
def o_ost(can, t, w0, w1, m):
    paint(can, t, ws('Ostfront'), [m(*q) for q in SKIRT5], 'OSTFRONT', 160, (236, 232, 220), None, 0.55, 0.55, 0.9)
MK = Map(26.0, 52.6, 30.0)
def s_kursk(t, w0, w1):
    can = BG('ku_t34', 0.2, 1.0, 40, 1.6)(t, w0); z = lerp(1.0, 1.08, prog(t, w0, w1)); mp = MK.frame(z); mp.putalpha(130); can.alpha_composite(mp)
    p = lambda lo, la: MK.p(lo, la, z)
    for nm, lo, la in (('BERLIN', 13.4, 52.52), ('MOSKAU', 37.62, 55.75)):
        x, y = p(lo, la); dot(can, x, y, GREY, 9); title(can, t, w0 + 0.25, nm, y + 48, 48, GREY, None, 'bebas', x)
    x, y = p(36.19, 51.73); dot(can, x, y, YEL, 12); ring(can, t, ws('Kursk', 20), x, y, RED, 34, False)
    title(can, t, ws('Kursk', 20), 'KURSK', y - 70, 70, YEL, None, 'bebas', x)
    title(can, t, ws('1943'), '1943', TOP, 140, CREAM)
    return can
def s_count(t, w0, w1):
    can = BG('ku_ht', 3.0, 1.0, 80, 1.6)(t, w0)
    title(can, t, ws('Büchern'), 'IN VIELEN BÜCHERN', TOP, 96, CREAM, ws('nicht', 33) - 0.15)
    t0 = ws('168')
    if t >= t0:
        counter(can, t, t0, 0, 168, (CX, 720), 280, YEL, 1.1)
    ta = ws('126'); tb = ws('42', 29)
    for i, (lab, n, ts_) in enumerate((('ALS RICHTSCHÜTZE', 126, ta), ('ALS KOMMANDANT', 42, tb))):
        if t < ts_: continue
        y = 990 + i * 150; u = eio((t - ts_) / 0.6); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((160, y - 30, 920, y + 30), 10, fill=(10, 11, 14, 150)); d.rounded_rectangle((160, y - 30, 160 + 760 * n / 168 * u, y + 30), 10, fill=YEL + (220,))
        can.alpha_composite(L); title(can, t, ts_, f'{n}', y, 52, WHITE, None, 'anton', 840, 300)
        title(can, t, ts_ + 0.1, lab, y + 62, 40, CREAM, None, 'bebas', 340)
    tn = ws('nicht', 33)
    if t >= tn:
        u = eio((t - tn) / 0.3); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).line((270, 760, lerp(270, 810, u), 690), fill=RED + (240,), width=16); can.alpha_composite(L)
        title(can, t, tn + 0.1, 'NICHT BELEGT', TOP, 120, RED)
    return can
def s_crew(t, w0, w1):
    can = grade(fit('k08', t, w0, w1, 1.06)); shade(can, 220, 0.5)
    title(can, t, ws('keine', 35), 'KEINE ZÄHLUNG PRO BESATZUNG', 1330, 70, CREAM, None, 'anton', CX, 840)
    return can
def s_legend(t, w0, w1):
    can, m = side('k09', 840, 920, t, w0, w1, 1.04); shade(can, 200, 0.6)
    arc_text(can, t, ws('Geschichten'), 'DIE LEGENDE', m, 0.80, 0.92, -122, -58, 75, CREAM)
    hand(can, t, ws('ausgeschmückt'), 'ausgeschmückt?', (CX, 1350), 120, YEL, 0.6)
    return can
def o_gold(can, t, w0, w1, m=None):
    title(can, t, ws('1944'), '1944', TOP, 140, CREAM)
    title(can, t, ws('Deutsche', 44), 'DEUTSCHES KREUZ IN GOLD', 1330, 74, YEL)
def o_rk(can, t, w0, w1, m=None):
    b = hand(can, t, ws('Ritterkreuz'), 'Ritterkreuz', (CX, 1240), 130, CREAM, 0.6)
    if b: strike(can, t, ws('nie', 47.5), b)
    title(can, t, ws('Feldwebels'), 'FELDWEBEL', TOP, 130, YEL)
def o_rebel(can, t, w0, w1, m=None):
    hand(can, t, ws('unbequem'), 'unbequem', (CX, 1200), 120, CREAM, 0.6)
    title(can, t, ws('Haare'), 'HAARE UND BART: ZU LANG', 1350, 64, YEL)
def o_kt(can, t, w0, w1, m=None):
    title(can, t, ws('Ende', 59), 'APRIL 1945', TOP, 130, CREAM)
    title(can, t, ws('Königstiger'), 'KÖNIGSTIGER', 1330, 100, YEL)
def o_burn(can, t, w0, w1, m=None):
    title(can, t, ws('Granatsplitter'), 'GRANATSPLITTER', TOP, 110, RED)
MS = Map(16.32, 48.96, 1.45)
def s_mahren(t, w0, w1):
    can = BG('ku_ex', 0.0, 1.0, 50, 1.6)(t, w0); z = lerp(1.0, 1.06, prog(t, w0, w1)); mp = MS.frame(z); mp.putalpha(130); can.alpha_composite(mp)
    p = lambda lo, la: MS.p(lo, la, z); fade_ = 1 - 0.55 * eio((t - ws('Spur', 75)) / 0.8)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    xb, yb = p(16.61, 49.19); dot(L, xb, yb, GREY, 9); title(L, t, w0 + 0.3, 'BRÜNN', yb - 50, 52, GREY, None, 'bebas', xb)
    xw, yw = p(16.49, 48.93); ring(L, t, w0 + 0.2, xw, yw, RED, 30, True); title(L, t, w0 + 0.2, 'WOSTITZ', yw + 62, 56, CREAM, None, 'bebas', xw)
    xu, yu = p(16.10, 48.80)
    dashed(L, [(xw, yw), (lerp(xw, xu, 0.5), lerp(yw, yu, 0.5) - 40), (xu, yu)], eio((t - ws('Feldlazarett')) / 0.9), YEL, 7, 22, 30)
    if t > ws('Urbau'): dot(L, xu, yu, YEL, 12)
    title(L, t, ws('Urbau'), 'URBAU', yu - 66, 70, YEL, None, 'bebas', xu)
    title(L, t, ws('Vrbovec'), 'HEUTE VRBOVEC', yu + 58, 48, CREAM, None, 'bebas', xu)
    x, y = p(16.3, 48.68); title(L, t, w0 + 0.4, 'ÖSTERREICH', y, 46, (150, 160, 178), None, 'bebas', x)
    title(L, t, w0 + 0.1, 'SÜDMÄHREN', TOP, 120, CREAM)
    if fade_ < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * fade_)))
    can.alpha_composite(L); return can
def o_2013(can, t, w0, w1, m=None):
    title(can, t, ws('2013'), '2013', TOP, 150, CREAM)
def o_16(can, t, w0, w1, m=None):
    title(can, t, w0 + 0.05, '2013', TOP, 150, CREAM)
    title(can, t, ws('sechzehn'), '16 DEUTSCHE SOLDATEN', 1330, 80, YEL)
TAG = Image.open(B + 'img/tag.png').convert('RGBA')
def s_tag(t, w0, w1):
    """the dog tag cut out of its photo, floating over the cleaning footage"""
    can = BG('dig', 16.0, 1.0, 70, 1.6)(t, w0); k = eout((t - w0 - 0.05) / 0.6); u = prog(t, w0, w1)
    if k > 0:
        wd = int(lerp(780, 880, u) * lerp(0.85, 1.0, k)); tg = TAG.resize((wd, int(TAG.height * wd / TAG.width)), Image.LANCZOS).rotate(lerp(-4, 2, u), expand=True, resample=Image.BICUBIC)
        if k < 1: tg.putalpha(tg.getchannel('A').point(lambda v: int(v * k)))
        sh = Image.new('RGBA', tg.size, (0, 0, 0, 0)); sh.putalpha(tg.getchannel('A').point(lambda v: int(v * 0.75)))
        x, y = int(CX - tg.width / 2), int(880 - tg.height / 2 + (1 - k) * 40)
        can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (x + 10, y + 24)); can.alpha_composite(tg, (x, y))
    title(can, t, ws('Erkennungsmarke'), 'ERKENNUNGSMARKE', 1330, 96, YEL)
    return can
def cta(can, t, t0):
    """small comment card in the lower left while the voice still runs: the bubble rocks, the question mark bounces, both lines wipe in left to right"""
    if t < t0: return
    k = eout((t - t0) / 0.45); A = int(255 * k); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, y0 = 70 - (1 - k) * 60, 1330; f1, f2 = oswald(46, 600), oswald(38, 500)
    s1, s2 = 'Kanntet ihr diese Geschichte', 'Schreibt es in die Kommentare!'; w1_ = f1.getlength(s1); wq = f1.getlength('?')
    wd = max(w1_ + wq, f2.getlength(s2)) + 150
    d.rounded_rectangle((x0, y0, x0 + wd, y0 + 140), 22, fill=(10, 11, 14, int(185 * k)), outline=YEL + (int(220 * k),), width=3)
    can.alpha_composite(L)
    B_ = Image.new('RGBA', (90, 90), (0, 0, 0, 0)); db = ImageDraw.Draw(B_)   # the bubble, rocking left and right
    db.rounded_rectangle((12, 14, 78, 64), 12, fill=YEL + (A,)); db.polygon([(26, 62), (42, 62), (22, 80)], fill=YEL + (A,))
    for i in range(3): db.ellipse((27 + i * 15, 35, 35 + i * 15, 43), fill=DARK + (A,))
    B_ = B_.rotate(9 * math.sin((t - t0) * 4.2), resample=Image.BICUBIC); can.alpha_composite(B_, (int(x0 + 18), int(y0 + 22)))
    def wipe(s_, f, col, xy, ts_, dur=0.7):
        if t < ts_: return
        bb = f.getbbox(s_); T_ = Image.new('RGBA', (bb[2] + 20, bb[3] + 20), (0, 0, 0, 0)); ImageDraw.Draw(T_).text((0, 0), s_, font=f, fill=col + (255,))
        u = eio((t - ts_) / dur); m = np.clip((u * (T_.width + 40) - np.arange(T_.width)) / 40, 0, 1)
        T_.putalpha(Image.fromarray((np.asarray(T_.getchannel('A'), np.float32) * m[None, :] * k).astype(np.uint8))); can.alpha_composite(T_, (int(xy[0]), int(xy[1])))
    tx = x0 + 125; wipe(s1, f1, WHITE, (tx, y0 + 20), t0 + 0.25); wipe(s2, f2, YEL, (tx, y0 + 82), t0 + 0.9)
    tq = t0 + 0.9
    if t > tq:   # the question mark drops in and keeps bouncing
        bo = -abs(math.sin((t - tq) * 5.0)) * 10 * min(1, (t - tq) / 0.3); Q = Image.new('RGBA', (60, 80), (0, 0, 0, 0)); ImageDraw.Draw(Q).text((4, 0), '?', font=f1, fill=YEL + (A,))
        Q = Q.rotate(12 * math.sin((t - tq) * 3.0), resample=Image.BICUBIC); can.alpha_composite(Q, (int(tx + w1_ + 2), int(y0 + 20 + bo)))
def s_grave(t, w0, w1):
    can = grade(fit('k02', t, w0, w1, 1.06)); shade(can, 200, 0.55); can.alpha_composite(TOPSH)
    title(can, t, ws('2014'), 'NOVEMBER 2014', TOP, 110, CREAM)
    title(can, t, ws('Brünn'), 'SOLDATENFRIEDHOF BRÜNN', TOP + 110, 60, YEL, None, 'bebas')
    cta(can, t, ws('Soldatenfriedhof'))
    return can

ANCH = [
 (0.0, s_hook, None),
 (ws('erkannte') - 0.1, FL('dig', 12.3, 1.0, 1.05, 1.15, 0.5, 0.5, o_lens), ('fade',)),
 (ws('Sein', 7) - 0.1, s_name, ('whip', 1)),
 (ws('Er', 8.5) - 0.05, S_('k01', 400, 470, 1.05, o_wm), ('fade',)),
 (ws('erst', 10.5) - 0.1, s_career, ('fade',)),
 (ws('Tigers') - 0.15, FL('ti', 4.0, 1.0, 1.0, 1.08, 0.5, 0.5, o_tiger), ('whip', -1)),
 (ws('Mit', 17) - 0.1, S_('k05', 1350, 1480, 1.05, o_ost), ('fade',)),
 (ws('1943') - 0.1, s_kursk, ('fade',)),
 (ws('In', 21.5) - 0.1, s_count, ('whip', 1)),
 (ws('denn', 33.5) - 0.1, s_crew, ('fade',)),
 (ws('Auch', 37.3) - 0.1, s_legend, ('fade',)),
 (ws('dass', 42.3) - 0.1, S_('k06', 100, 330, 1.05, o_gold), ('whip', -1)),
 (ws('Das', 46.3) - 0.1, FL('ku_tig', 4.8, 1.0, 1.0, 1.08, 0.35, 0.5, o_rk), ('fade',)),
 (ws('Berichten') - 0.1, S_('k07', 950, 1120, 1.05, o_rebel), ('fade',)),
 (ws('Ende', 59) - 0.1, FL('kt', 0.0, 1.0, 1.0, 1.06, 0.5, 0.5, o_kt), ('whip', 1)),
 (ws('Nach', 66) - 0.1, FL('ku_burn', 2.0, 1.0, 1.0, 1.08, 0.5, 0.5, o_burn), ('fade',)),
 (ws('Knispel', 69.5) - 0.1, s_mahren, ('fade',)),
 (ws('Erst', 76) - 0.1, FL('dig', 0.0, 1.0, 1.0, 1.06, 0.5, 0.5, o_2013), ('fade',)),
 (ws('Archäologen') - 0.1, FL('dig', 4.8, 1.0, 1.0, 1.08, 0.5, 0.5, o_16), ('fade',)),
 (ws('Bei', 81) - 0.1, s_tag, ('fade',)),
 (ws('Im', 84) - 0.1, s_grave, ('fade',))]
