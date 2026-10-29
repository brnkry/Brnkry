
# ---------- full-screen vertical archive film (the old footage is already 9:16) ----------
def V9(k, a, z0=1.0, z1=1.06, ov=None, sh=200, warm=0.06, sat=0.9):
    def fn(t, w0, w1):
        im = fat(k, a + max(0.0, t - w0)); z = lerp(z0, z1, eio(prog(t, w0, w1))); cw, ch = im.width / z, im.height / z
        box = _cover((cw, ch), 9 / 16); x0 = (im.width - cw) / 2 + box[0]; y0 = (im.height - ch) / 2 + box[1]
        can = grade(im.resize((W, H), Image.BICUBIC, box=(max(0, x0), max(0, y0), min(im.width, x0 + box[2] - box[0]), min(im.height, y0 + box[3] - box[1]))).convert('RGBA'), warm, sat); shade(can, sh, 0.55)
        can.alpha_composite(TOPSH)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
def BG(k, a, dimv=70, bl=1.6):
    def fn(t, w0):
        im = fat(k, a + max(0.0, t - w0))
        sm = im.resize((360, 640), Image.BILINEAR, box=_cover(im.size, 9 / 16)).filter(ImageFilter.GaussianBlur(bl)).resize((W, H), Image.BICUBIC)
        can = grade(sm.convert('RGBA'), 0.1, 0.85); dim(can, dimv); return can
    return fn
def arrow_at(can, t, t0, tip, frm, col=YEL, w_=14, head=46, lab=None, lab_xy=None):
    """arrow drawn from frm to tip, label written at its tail"""
    if t < t0: return
    u = eio((t - t0) / 0.35); e = (lerp(frm[0], tip[0], u), lerp(frm[1], tip[1], u)); ang = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line((frm, e), fill=(0, 0, 0, 160), width=w_ + 8); d.line((frm, e), fill=col + (255,), width=w_)
    hp = [(e[0] + 14 * math.cos(ang), e[1] + 14 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))]
    d.polygon(hp, fill=col + (255,)); can.alpha_composite(L)
    if lab: title(can, t, t0 + 0.15, lab, lab_xy[1], 66, col, None, 'anton', lab_xy[0], 900)
def ring_at(can, t, t0, x, y, col=RED, r=44):
    if t < t0: return
    k = eout((t - t0) / 0.35); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for j in range(2):
        uu = ((t - t0) * 0.8 + j / 2) % 1.0; rr = r + 60 * uu; d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=col + (int(170 * (1 - uu) * k),), width=5)
    d.ellipse((x - r * k, y - r * k, x + r * k, y + r * k), outline=col + (255,), width=8); can.alpha_composite(L)
def photo_card(n, box, t, w0, w1, bgk, bga, z1=1.06, py=PY, pw=PW, ph=PH, dimbg=80):
    """a photo in a cream-edged panel over the blurred running film; returns the canvas and a source -> screen mapper"""
    can = BG(bgk, bga, dimbg)(t, w0); im = src(n).crop(box); z = lerp(1.0, z1, eio(prog(t, w0, w1)))
    cw, ch = im.width / z, im.height / z; x0, y0 = (im.width - cw) / 2, (im.height - ch) / 2
    pn = grade(im.resize((pw, ph), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA'), 0.08, 0.95)
    x, y = (W - pw) // 2, py - ph // 2
    sh = Image.new('RGBA', (pw + 60, ph + 60), (0, 0, 0, 0)); sh.putalpha(Image.new('L', (pw + 60, ph + 60), 150).filter(ImageFilter.GaussianBlur(20)))
    can.alpha_composite(sh, (x - 24, y - 14)); ImageDraw.Draw(can).rectangle((x - 8, y - 8, x + pw + 7, y + ph + 7), fill=CREAM + (255,)); can.alpha_composite(pn, (x, y))
    sx, sy = pw / cw, ph / ch
    return can, (lambda X, Y: (x + (X - box[0] - x0) * sx, y + (Y - box[1] - y0) * sy))

# ---------- scenes ----------
TOP = 330
def o_hook(can, t, w0, w1):
    title(can, t, ws('April') - 0.1, 'APRIL 1943', TOP, 130, CREAM)
    title(can, t, ws('Tunesien'), 'TUNESIEN', 1300, 120, YEL, None, bold=1)
def o_today(can, t, w0, w1, m=None):
    title(can, t, ws('fährt', 7) - 0.05, 'FÄHRT BIS HEUTE', TOP, 110, YEL)
D131 = [(860, 352, 952, 612), (955, 348, 1092, 612), (1098, 352, 1202, 612)]   # t02: the three painted digits (source px)
@functools.lru_cache(None)
def _t02():
    im = src('t02').crop((260, 40, 1790, 1000)); return im
def s_131(t, w0, w1):
    """the turret number: the photo dimmed, each digit lights up in yellow as it is explained"""
    can = BG('o_grass', 0.0, 90)(t, w0); im = _t02(); z = lerp(1.0, 1.08, eio(prog(t, w0, w1)))
    pw, ph = 1000, int(1000 * im.height / im.width); cw, ch = im.width / z, im.height / z; x0, y0 = (im.width - cw) / 2, (im.height - ch) / 2
    pn = im.resize((pw, ph), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)); sx = pw / cw
    base = ImageEnhance.Brightness(pn).enhance(0.55).convert('RGBA'); a = np.asarray(pn.convert('L'), np.float32)
    for (bx0, by0, bx1, by1), ts_ in zip(D131, (ws('erste', 12.3), ws('dritter'), ws('erster', 14.3))):
        k = eout((t - ts_) / 0.35)
        if k <= 0: continue
        X0, Y0 = int((bx0 - 260 - x0) * sx), int((by0 - 40 - y0) * sx); X1, Y1 = int((bx1 - 260 - x0) * sx), int((by1 - 40 - y0) * sx)
        sub = a[Y0:Y1, X0:X1]; m = np.clip((sub - 120) / 50, 0, 1) * k   # only the white paint of the digit
        L = Image.new('RGBA', (X1 - X0, Y1 - Y0), YEL + (0,)); L.putalpha(Image.fromarray((m * 255).astype(np.uint8)))
        G = Image.new('RGBA', (X1 - X0 + 80, Y1 - Y0 + 80), (0, 0, 0, 0)); G.alpha_composite(L, (40, 40))
        gl = Image.new('RGBA', G.size, YEL + (0,)); gl.putalpha(G.getchannel('A').filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.8)))
        base.alpha_composite(gl, (X0 - 40, Y0 - 40)); base.alpha_composite(L, (X0, Y0))
    x, y = (W - pw) // 2, 820 - ph // 2; ImageDraw.Draw(can).rectangle((x - 8, y - 8, x + pw + 7, y + ph + 7), fill=CREAM + (255,)); can.alpha_composite(base, (x, y))
    title(can, t, ws('Tiger', 9.3), 'TIGER 131', TOP - 60, 120, CREAM, None, bold=1)
    for i, (lab, ts_) in enumerate((('1. KOMPANIE', ws('erste', 12.3)), ('3. ZUG', ws('dritter')), ('1. PANZER', ws('erster', 14.3)))):
        title(can, t, ts_, lab, 1190 + i * 92, 70, YEL, None, 'bebas')
    return can
def o_504(can, t, w0, w1, m=None):
    title(can, t, ws('schweren', 15.8), 'SCHWERE PANZERABTEILUNG 504', 1330, 62, YEL, None, 'bebas')
def s_map(t, w0, w1):
    can, mp = photo_card('t18', (0, 120, 2048, 1900), t, w0, w1, 'o_land', 0.0, 1.05, 820, 900, 782, 60)
    x, y = mp(1025, 560); ring_at(can, t, ws('Medjez'), x, y, YEL, 34)
    x2, y2 = mp(1088, 1584); ring_at(can, t, ws('Churchill-Panzer'), x2, y2, RED, 40)
    title(can, t, ws('Hügeln'), 'MEDJEZ EL BAB', TOP - 60, 110, CREAM)
    title(can, t, ws('Churchill-Panzer'), 'GEGEN CHURCHILL-PANZER', 1300, 70, YEL)
    return can
def s_dmg(t, w0, w1):
    can, mp = photo_card('t16', (500, 0, 2400, 1425), t, w0, w1, 'o_sil', 0.0, 1.04, 820, 1000, 750, 70)
    a = mp(1360, 1110); arrow_at(can, t, ws('Drehkranz'), a, (a[0] - 260, a[1] + 300), RED, lab='DREHKRANZ', lab_xy=(a[0] - 260, a[1] + 360))
    b = mp(1470, 860); arrow_at(can, t, ws('zweiter', 25.4), b, (b[0] + 220, b[1] - 330), YEL, lab='HÖHENRICHTUNG', lab_xy=(min(b[0] + 220, 760), b[1] - 400))
    title(can, t, ws('Treffer'), 'ZWEI TREFFER', TOP - 60, 110, CREAM)
    return can
def s_hatch(t, w0, w1):
    can, m = side('t13', 760, 880, t, w0, w1, 1.05); shade(can, 200, 0.55); can.alpha_composite(TOPSH)
    p = m(1270, 470); arrow_at(can, t, ws('stieg'), (p[0], p[1] - 10), (p[0] + 160, p[1] - 280), YEL, lab='LUKE OFFEN', lab_xy=(min(p[0] + 170, 780), p[1] - 340))
    title(can, t, ws('auf', 30.5), 'AUFGEGEBEN', 1330, 120, RED, None, bold=1)
    return can
def o_luck(can, t, w0, w1, m=None):
    hand(can, t, ws('Glücksfall'), 'Glücksfall', (CX, 1300), 140, YEL, 0.7)
CLIP = {}
def clipping(can, t, t0, n, box, xy, wd, rot):
    """a newspaper cutting dropped onto the pile"""
    if t < t0: return
    if n not in CLIP: CLIP[n] = src(n).crop(box).convert('RGBA')
    k = eout((t - t0) / 0.32); P_ = CLIP[n]; P_ = P_.resize((int(wd), int(wd * P_.height / P_.width)), Image.LANCZOS).rotate(rot + (1 - k) * 7, expand=True, resample=Image.BICUBIC)
    sc = lerp(1.3, 1.0, k); P_ = P_.resize((int(P_.width * sc), int(P_.height * sc)), Image.BICUBIC)
    if k < 1: P_.putalpha(P_.getchannel('A').point(lambda v: int(v * min(1, k * 1.6))))
    sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.7)))
    x, y = int(xy[0] - P_.width / 2), int(xy[1] - P_.height / 2); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (x + 10, y + 20)); can.alpha_composite(P_, (x, y))
def s_press(t, w0, w1):
    can = BG('o_dust', 0.5, 90)(t, w0)
    clipping(can, t, ws('denn', 33), 't07', (0, 0, 2400, 1792), (CX, 700), 900, -3)
    clipping(can, t, ws('Nähe') - 0.2, 't06', (0, 0, 2400, 1792), (CX, 1080), 860, 4)
    title(can, t, ws('denn', 33), 'MAI 1943', TOP - 60, 110, CREAM)
    return can
def o_parts(can, t, w0, w1, m=None):
    title(can, t, ws('Luken'), 'LUKEN UND TEILE', TOP, 100, CREAM)
    title(can, t, ws('zerstörten'), 'AUS ZERSTÖRTEN TIGERN', 1330, 66, YEL)
def o_tunis(can, t, w0, w1):
    title(can, t, ws('Tunis'), 'TUNIS', TOP, 140, CREAM)
def o_king(can, t, w0, w1, m=None):
    title(can, t, ws('König'), 'KÖNIG GEORG VI.', TOP, 110, CREAM)
    title(can, t, ws('besichtigte'), 'JUNI 1943', 1330, 90, YEL)
ME = Map(3.5, 44.5, 34.0)
def s_route(t, w0, w1):
    can = BG('o_sil', 0.5, 50)(t, w0); z = lerp(1.0, 1.05, prog(t, w0, w1)); mp = ME.frame(z); mp.putalpha(140); can.alpha_composite(mp)
    p = lambda lo, la: ME.p(lo, la, z)
    pts = route([(10.18, 36.80), (9.0, 37.6), (3.0, 37.4), (-5.6, 36.0), (-10.5, 38.5), (-10.5, 44.0), (-6.0, 48.8), (-2.0, 50.6)], ME, z)
    dashed(can, pts, eio((t - ws('Oktober')) / 2.0), YEL, 7, 22, 34)
    xa, ya = p(10.18, 36.80); dot(can, xa, ya, YEL, 11); title(can, t, w0 + 0.2, 'TUNIS', ya + 55, 52, CREAM, None, 'bebas', xa)
    xb, yb = p(-2.0, 50.6); title(can, t, ws('England'), 'ENGLAND', yb - 60, 64, YEL, None, 'bebas', xb + 30)
    if t > ws('England'): dot(can, xb, yb, YEL, 12)
    title(can, t, ws('Oktober'), 'OKTOBER 1943', TOP, 120, CREAM)
    return can
def o_test(can, t, w0, w1):
    title(can, t, ws('Schule'), 'SCHULE FÜR PANZERTECHNIK', TOP, 76, CREAM)
    title(can, t, ws('Panzerung'), 'PANZERUNG', 1180, 80, YEL)
    title(can, t, ws('Motor', 52), 'MOTOR', 1270, 70, CREAM, None, 'bebas')
    title(can, t, ws('Kanone', 53), 'KANONE', 1350, 70, CREAM, None, 'bebas')
def s_report(t, w0, w1):
    can = BG('o_mov', 0.5, 80)(t, w0); t0 = ws('schrieb')
    l = [('BERICHT', 60, INK, t0 + 0.2), ('PANZERKAMPFWAGEN TIGER', 42, INK, t0 + 0.5), ('', 20, INK, 0), ('Panzerung vorn: 100 mm', 36, (90, 80, 70), t0 + 1.0),
         ('Motor: Maybach HL 210', 36, (90, 80, 70), t0 + 1.4), ('Kanone: 8,8 cm KwK 36', 36, (90, 80, 70), t0 + 1.8)]
    sheet(can, t, t0 - 0.1, l, CX, 860, 880, 0.0)
    return can
def o_bov(can, t, w0, w1, m=None):
    title(can, t, ws('1951'), '1951', TOP, 140, CREAM)
    title(can, t, ws('Bovington'), 'PANZERMUSEUM BOVINGTON', 1330, 66, YEL)
TURRET20 = [(300, 330), (1960, 330), (1960, 640), (1440, 680), (300, 600)]   # t20: turret and gun above the hull line (source px)
@functools.lru_cache(None)
def _t20parts():
    """turret and gun cut out along their outline (the bright sky is not part of them); the hull keeps a filled-in deck where the turret stood"""
    import cv2
    im = src('t20').crop((200, 120, 2200, 1400)); A = np.asarray(im); hsv = cv2.cvtColor(A, cv2.COLOR_RGB2HSV)
    sky = (hsv[..., 2] > 150) & (hsv[..., 1] < 70); sky = cv2.morphologyEx(sky.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    poly = np.zeros(A.shape[:2], np.uint8); cv2.fillPoly(poly, [np.array([(x - 200, y - 120) for x, y in TURRET20], np.int32)], 1)
    tur = (poly & (1 - sky)).astype(np.uint8); tur = cv2.morphologyEx(tur, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    hull = cv2.inpaint(A, cv2.dilate(tur, np.ones((7, 7), np.uint8)) * 255, 9, cv2.INPAINT_TELEA)
    hull = cv2.addWeighted(hull, 1.0, np.zeros_like(hull), 0, 0) * (1 - 0.35 * cv2.GaussianBlur(tur.astype(np.float32), (0, 0), 6))[..., None]   # a shadow where the turret sat
    top = im.convert('RGBA'); top.putalpha(Image.fromarray((cv2.GaussianBlur(tur.astype(np.float32), (0, 0), 1.2) * 255).astype(np.uint8)))
    return im, top, Image.fromarray(np.clip(hull, 0, 255).astype(np.uint8)).convert('RGBA')
def s_restore(t, w0, w1):
    """1990: the tank comes apart (turret lifts off the hull), then goes back together when it is restored"""
    can = BG('o_flat', 0.3, 70)(t, w0); im, top, hull = _t20parts(); pw = 1000; ph = int(pw * im.height / im.width); sc = pw / im.width
    lift = 170 * eio((t - ws('zerlegt')) / 0.7) * (1 - eio((t - ws('restauriert')) / 0.8))
    x, y = (W - pw) // 2, 900 - ph // 2
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); L.alpha_composite(hull.resize((pw, ph), Image.BICUBIC), (x, y)); L.alpha_composite(top.resize((pw, ph), Image.BICUBIC), (x, int(y - lift)))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.6)).filter(ImageFilter.GaussianBlur(14))); can.alpha_composite(sh, (8, 18)); can.alpha_composite(L)
    title(can, t, ws('1990'), 'AB 1990', TOP - 60, 130, CREAM)
    title(can, t, ws('zerlegt'), 'ZERLEGT', 1320, 110, RED, ws('restauriert') - 0.25)
    title(can, t, ws('restauriert'), 'RESTAURIERT', 1320, 110, YEL)
    return can
def s_engine(t, w0, w1):
    can, mp = photo_card('t21', (0, 0, 1920, 1280), t, w0, w1, 'm_close', 0.5, 1.05, 820, 1000, 667, 60)
    title(can, t, ws('Maybach-Motor'), 'MAYBACH-MOTOR', TOP - 60, 120, CREAM)
    title(can, t, ws('Königstiger'), 'AUS DEM KÖNIGSTIGER', 1250, 70, YEL)
    title(can, t, ws('2003'), 'SEIT 2003', 1350, 90, CREAM)
    return can
def o_run(can, t, w0, w1, m=None):
    title(can, t, ws('eigener'), 'AUS EIGENER KRAFT', TOP, 100, YEL)
def o_plans(can, t, w0, w1, m=None):
    title(can, t, ws('zweiten', 75.8), 'ZWEITE ÜBERHOLUNG', TOP, 96, CREAM)
    hand(can, t, ws('Originalplänen'), 'nach Originalplänen', (CX, 1330), 110, YEL, 0.7)
def o_fury(can, t, w0, w1, m=None):
    title(can, t, ws('2014'), '2014', TOP - 70, 120, CREAM)
    if t >= ws('Fury'):
        k = eout((t - ws('Fury')) / 0.3); sz = int(lerp(330, 250, k))
        title(can, t, ws('Fury'), 'FURY', 1250, sz, YEL, None, bold=3)
def cta(can, t, t0):
    """small comment card in the lower left: the bubble rocks, the question mark bounces, both lines wipe in"""
    if t < t0: return
    k = eout((t - t0) / 0.45); A = int(255 * k); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, y0 = 70 - (1 - k) * 60, 1330; f1, f2 = oswald(46, 600), oswald(38, 500)
    s1, s2 = 'Kanntet ihr diese Geschichte', 'Schreibt es in die Kommentare!'; w1_ = f1.getlength(s1); wq = f1.getlength('?')
    wd = max(w1_ + wq, f2.getlength(s2)) + 150
    d.rounded_rectangle((x0, y0, x0 + wd, y0 + 140), 22, fill=(10, 11, 14, int(185 * k)), outline=YEL + (int(220 * k),), width=3); can.alpha_composite(L)
    B_ = Image.new('RGBA', (90, 90), (0, 0, 0, 0)); db = ImageDraw.Draw(B_)
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
    if t > tq:
        bo = -abs(math.sin((t - tq) * 5.0)) * 10 * min(1, (t - tq) / 0.3); Q = Image.new('RGBA', (60, 80), (0, 0, 0, 0)); ImageDraw.Draw(Q).text((4, 0), '?', font=f1, fill=YEL + (A,))
        Q = Q.rotate(12 * math.sin((t - tq) * 3.0), resample=Image.BICUBIC); can.alpha_composite(Q, (int(tx + w1_ + 2), int(y0 + 20 + bo)))
def o_end(can, t, w0, w1, m=None):
    title(can, t, ws('einzige'), 'DER EINZIGE', TOP - 40, 110, CREAM)
    title(can, t, ws('fahrbereite'), 'FAHRBEREITE TIGER I', TOP + 70, 90, YEL)
    cta(can, t, ws('Tiger', 86))

ANCH = [
 (0.0, V9('o_dust', 0.0, 1.0, 1.06, o_hook), None),
 (ws('und', 6.2) - 0.1, FL('n_a', 0.0, 1.0, 1.0, 1.06, 0.5, 0.5, o_today), ('whip', 1)),
 (ws('Sein', 8.5) - 0.1, s_131, ('fade',)),
 (ws('Er', 15.3) - 0.1, S_('t03', 900, 1300, 1.05, o_504), ('fade',)),
 (ws('und', 18.3) - 0.1, s_map, ('whip', -1)),
 (ws('Ein', 22.7) - 0.1, s_dmg, ('fade',)),
 (ws('Die', 28.4) - 0.1, s_hatch, ('fade',)),
 (ws('Für', 31.2) - 0.1, S_('t19', 900, 1200, 1.05, o_luck), ('whip', 1)),
 (ws('denn', 33) - 0.1, s_press, ('fade',)),
 (ws('Mit', 36.8) - 0.1, S_('t08', 700, 1000, 1.05, o_parts), ('fade',)),
 (ws('und', 40.8) - 0.1, V9('o_tunis', 0.0, 1.0, 1.05, o_tunis), ('fade',)),
 (ws('auch', 43.1) - 0.1, S_('t17', 500, 700, 1.05, o_king), ('fade',)),
 (ws('Im', 45.3) - 0.1, s_route, ('whip', -1)),
 (ws('Die', 48.5) - 0.1, V9('o_deck', 0.0, 1.0, 1.06, o_test), ('fade',)),
 (ws('schrieb') - 0.15, s_report, ('fade',)),
 (ws('1951') - 0.1, S_('t12', 600, 900, 1.05, o_bov), ('whip', 1)),
 (ws('Ab', 60.2) - 0.1, s_restore, ('fade',)),
 (ws('Als', 66) - 0.1, s_engine, ('fade',)),
 (ws('fährt', 71.5) - 0.1, FL('m_rain', 0.0, 1.0, 1.0, 1.06, 0.5, 0.5, o_run), ('fade',)),
 (ws('Bei', 75.5) - 0.1, S_('t11', 300, 650, 1.05, o_plans), ('fade',)),
 (ws('2014') - 0.1, S_('t04', 500, 800, 1.05, o_fury), ('whip', -1)),
 (ws('Heute', 85.3) - 0.1, FL('n_b', 0.0, 1.0, 1.0, 1.06, 0.5, 0.5, o_end), ('fade',))]
