
# ================= Hermann Balck scenes =================
def ws(word, after=0.0): return wt(word, after) - 0.05
def fr(ct): return cframe(int(round(ct * FPS)) + 1)
PIC = (100, 92, 1820, 990)   # usable film picture inside the rounded 'old film' frame (1920x1080 coords)
def vblur(ct):
    """tiny insignia in the newsreel, blurred anyway (1920 coords: x, y, diameter)"""
    if 0.95 <= ct <= 3.82: return [(540, 470, 90), (1255, 480, 90)]
    if 10.08 <= ct <= 12.35: u = clamp((ct - 10.1) / 2.2); return [(lerp(920, 940, u), lerp(920, 1000, u), 110)]
    return []
def film(ct, cx, cy=540, z=1.25, sat=1.0, warm=0.15):
    im = fr(ct); S = im.width / 1920
    spots = vblur(ct)
    if spots:
        im = im.copy()
        for x, y, d in spots:
            r = d / 2; bx = (int((x - d) * S), int((y - d) * S), int((x + d) * S), int((y + d) * S)); reg = im.crop(bx)
            bl = reg.resize((max(1, reg.width // 12), max(1, reg.height // 12)), Image.BILINEAR).resize(reg.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(d * S * 0.12))
            mk = Image.new('L', reg.size, 0); c = reg.width / 2; rr = r * S; ImageDraw.Draw(mk).ellipse((c - rr, c - rr, c + rr, c + rr), fill=255)
            im.paste(Image.composite(bl, reg, mk.filter(ImageFilter.GaussianBlur(rr * 0.2))), bx[:2])
    ch = min(1080 / z, PIC[3] - PIC[1]); cw = ch * W / H
    x0 = min(max(cx - cw / 2, PIC[0]), PIC[2] - cw); y0 = min(max(cy - ch / 2, PIC[1]), PIC[3] - ch)
    can = grade(im.resize((W, H), Image.BICUBIC, box=(x0 * S, y0 * S, (x0 + cw) * S, (y0 + ch) * S)).convert('RGBA'), warm, sat); shade(can, 200, 0.55)
    return can, (lambda x, y: ((x - x0) * W / cw, (y - y0) * H / ch))
def arrow_to(can, a, b, u, col=YEL, w_=14, head=44):
    if u <= 0: return
    e = (lerp(a[0], b[0], u), lerp(a[1], b[1], u)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line((a, e), fill=(0, 0, 0, 150), width=w_ + 8); d.line((a, e), fill=col + (255,), width=w_)
    d.polygon([(e[0] + 12 * math.cos(ang), e[1] + 12 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))], fill=col + (255,))
    can.alpha_composite(L)
def path_arrow(can, pts, u, col=RED, w_=20, head=56):
    """thick arrow drawn along a polyline (screen coords) up to fraction u"""
    if u <= 0: return
    sm = []
    for i in range(len(pts) - 1):
        for v in np.linspace(0, 1, 14, endpoint=False): sm.append((lerp(pts[i][0], pts[i + 1][0], v), lerp(pts[i][1], pts[i + 1][1], v)))
    sm.append(pts[-1]); n = max(3, int(len(sm) * u))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line(sm[:n], fill=(0, 0, 0, 150), width=w_ + 8, joint='curve'); d.line(sm[:n], fill=col + (255,), width=w_, joint='curve')
    e, q = sm[n - 1], sm[n - 3]; ang = math.atan2(e[1] - q[1], e[0] - q[0])
    d.polygon([(e[0] + 16 * math.cos(ang), e[1] + 16 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))], fill=col + (255,))
    can.alpha_composite(L)
def qbox(cx, cy, s_, size, font=None, tilt=0.0, keyst=0.0):
    """screen quad with the exact aspect of the text (TL, TR, BR, BL); tilt lifts the right end, keyst widens the bottom"""
    f = font or anton(size); bb = f.getbbox(s_); w_, h_ = bb[2] - bb[0] + 20, bb[3] - bb[1] + 20; k = w_ * keyst / 2
    return [(cx - w_ / 2, cy - h_ / 2 + tilt), (cx + w_ / 2, cy - h_ / 2 - tilt), (cx + w_ / 2 + k, cy + h_ / 2 - tilt), (cx - w_ / 2 - k, cy + h_ / 2 + tilt)]
def pin(n, sxa, sxb, w0, w1, z1, tr, quad):
    """screen quad measured on the frame at time tr of a side() shot, back to source pixels (so it moves with the photo)"""
    im = src(n); sc = H / im.height; u = prog(tr, w0, w1); z = lerp(1.0, z1, u); vw, vh = W / (sc * z), H / (sc * z)
    sx0 = lerp(sxa, sxb, u) + (W / sc - vw) / 2; sy0 = (im.height - vh) / 2
    return [(sx0 + x / (sc * z), sy0 + y / (sc * z)) for x, y in quad]
def paint(can, t, t0, quad, s_, size, col, font=None, dur=0.5, mod=0.45, op=0.9, glow=((8, 9, 12), 10, 0.55), t1=None):
    """words painted on a surface of the photo, wiped in left to right"""
    if t <= t0: return
    a = clamp((t - t0) / 0.06) * (1.0 if t1 is None else 1 - clamp((t - t1) / 0.3))
    on_quad(can, quad, s_, size, a, col, font or anton(size), eio((t - t0) / dur), 0.8, mod=mod, op=op, glow=glow)
def pen(can, t, t0, s_, xy, font, col, dur=0.9):
    """elegant writing beside a face, the pen moving left to right, soft shadow"""
    if t < t0: return
    bb = font.getbbox(s_); w_, h_ = bb[2] - bb[0] + 60, bb[3] - bb[1] + 60
    L = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); ImageDraw.Draw(L).text((30 - bb[0], 30 - bb[1]), s_, font=font, fill=col + (255,))
    u = eio((t - t0) / dur); m = np.clip((u * (w_ + 40) - np.arange(w_)) / 40, 0, 1)
    L.putalpha(Image.fromarray((np.asarray(L.getchannel('A'), np.float32) * m[None, :]).astype(np.uint8)))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (0, 0), L.getchannel('A'))
    x, y = int(xy[0] - w_ / 2), int(xy[1] - h_ / 2); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)), (x + 3, y + 5)); can.alpha_composite(L, (x, y))
def tank(can, x, y, s=1.0, col=YEL, flip=False, a=1.0):
    """small tank symbol for the maps (hull, tracks, turret, gun)"""
    if a <= 0: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); g = -1 if flip else 1; A = int(255 * a)
    def P(px, py): return (x + g * px * s, y + py * s)
    for off, c in ((5, (0, 0, 0, int(160 * a))), (0, col + (A,))):
        o = off * s
        d.rounded_rectangle((x - 34 * s - o, y + 4 * s - o, x + 34 * s + o, y + 20 * s + o), 8 * s, fill=c)
        d.polygon([P(-30 - off, 4 + off), P(30 + off, 4 + off), P(24 + off, -8 - off), P(-26 - off, -8 - off)], fill=c)
        d.rounded_rectangle((x - 14 * s - o, y - 22 * s - o, x + 12 * s + o, y - 6 * s + o), 5 * s, fill=c)
        d.line((P(10, -15), P(46, -17)), fill=c, width=int(6 * s + 2 * o))
    can.alpha_composite(L)
def river(can, pts, col=(110, 140, 170), w_=7):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).line(pts, fill=col + (230,), width=w_, joint='curve'); can.alpha_composite(L)

# --- 1980 / the Red Army: a Soviet tank column with rocket launchers (end of the newsreel)
def s_open(t, w0, w1):
    can, m = film(min(26.0 + t * 0.8, 31.2), 400, 700, lerp(1.22, 1.3, prog(t, w0, w1)))
    title(can, t, 0.25, '1980', 420, 140, CREAM, ws('Rote') - 0.25)
    sky(can, t, ws('Rote'), 'ROTE ARMEE', CX, 470, 140, CREAM, None, 0.5)
    return can
# --- his own footage: summer tunic, the Knight's Cross (S2 then the close-up S5)
def s_film2(t, w0, w1):
    can, m = film(min(1.0 + (t - w0), 3.78), 1250, 560, 1.25); return can
def s_film5(t, w0, w1):
    can, m = film(min(10.12 + (t - w0) * 0.6, 12.3), 980, 600, 1.28)   # S5 is only 2.2 s: slowed down so it never stops
    title(can, t, ws('1948', 8.5), '1948', 1240, 110, CREAM)
    title(can, t, ws('verurteilt', 9), 'VERURTEILT', 1360, 104, RED)
    return can
# --- the name: colour portrait
def s_name(t, w0, w1):
    can = grade(fit('b27', t, w0, w1, 1.07)); shade(can, 230, 0.5)
    title(can, t, ws('Hermann'), 'HERMANN', 1120, 120, CREAM, None, bold=1)
    title(can, t, ws('Balck', 11), 'BALCK', 1270, 200, YEL, None, bold=2)
    title(can, t, ws('1893'), '1893  ·  DANZIG', 1410, 70, CREAM, None, 'bebas')
    return can
def s_ww1(t, w0, w1):   # b16: seven red strokes on the curtain, one for each wound
    can = grade(fit('b16', t, w0, w1, 1.05)); shade(can, 220, 0.5)
    q = lambda x, y: fitpt('b16', t, w0, w1, 1.05, x, y); t0 = ws('siebenmal')
    sky(can, t, ws('Ersten') - 0.1, '1914', 160, 470, 120, CREAM, None, 0.4)
    if t > t0:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); n = int(clamp((t - t0) / 0.6) * 7 + 0.999)
        for i in range(min(n, 7)):
            a = q(60 + i * 46, 1050); b = q(70 + i * 46, 1300); d.line((a, b), fill=RED + (235,), width=11)
        a = q(40, 1260); b = q(380, 1110)
        if n >= 7: d.line((a, b), fill=RED + (235,), width=9)
        can.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.0)))
        title(can, t, t0 + 0.6, '7× VERWUNDET', 1330, 96, RED)
    return can
# --- Sedan, 13 May 1940
class Map1940(Map):
    """borders of 13 May 1940 (here the same lines as today: Eupen-Malmedy was still Belgian), the Reich in its own tone"""
    @functools.lru_cache(None)
    def base(s):
        k = 2; im = Image.new('RGB', (W * k, H * k), SEA); d = ImageDraw.Draw(im); span = W / s.sc
        lon0, lon1 = s.c[0] - span, s.c[0] + span
        for nm, xs, ys, a, b_, c, e in ALLP:
            if b_ < lon0 - 5 or a > lon1 + 5: continue
            pts = [(((x - s.c[0]) * s.sc + W / 2) * k, (H / 2 - (y - s.c[1]) * s.sc) * k) for x, y in zip(xs, ys)]
            if len(pts) < 3: continue
            d.polygon(pts, fill=LAND_HI if nm in s.hi else ((58, 44, 44) if nm == 'Germany' else LAND)); d.line(pts + [pts[0]], fill=BORDER, width=3)
        return im.resize((W, H), Image.LANCZOS)
MS = Map1940(5.0, 49.9, 4.6, hi=('France',))
LAB40 = [('BELGIEN', 4.5, 50.72), ('LUX.', 6.08, 49.68), ('DEUTSCHES', 6.95, 50.55), ('REICH', 6.95, 50.33)]
MAAS = [(4.87, 50.47), (4.91, 50.26), (4.82, 50.14), (4.72, 49.90), (4.72, 49.77), (4.94, 49.70), (5.10, 49.55), (5.38, 49.16)]
def s_sedan(t, w0, w1):
    z = lerp(1.0, 1.05, prog(t, w0, w1)); can = grade(MS.frame(z), 0.1, 1.0); p = lambda lon, lat: MS.p(lon, lat, z)
    river(can, [p(*q) for q in MAAS]); title(can, t, w0 + 0.15, '13. MAI 1940', 420, 120, CREAM)
    for i, (nm, lo, la) in enumerate(LAB40):
        x, y = p(lo, la); title(can, t, w0 + 0.4 + 0.08 * i, nm, y, 46, (150, 160, 178), None, 'bebas', min(max(x, 120), 820))
    x, y = p(4.94, 49.70); dot(can, x, y, CREAM, 10); title(can, t, ws('Sedan', 18) - 0.05, 'SEDAN', y + 55, 54, CREAM, None, 'bebas', x)
    xm, ym = p(4.80, 50.05); title(can, t, ws('Maas', 18), 'MAAS', ym, 58, (150, 185, 215), None, 'bebas', xm + 70)
    a1 = [p(*q) for q in ((5.9, 49.80), (5.5, 49.74), (5.15, 49.72), (4.85, 49.70))]
    a2 = a1 + [p(*q) for q in ((4.4, 49.78), (3.8, 49.92), (3.0, 50.05), (2.5, 50.10))]
    t1 = ws('führte', 18) - 0.05; t2 = ws('Durchbruch', 18) - 0.1
    if t < t2: path_arrow(can, a1, eio((t - t1) / 1.6))
    else: path_arrow(can, a2, lerp(0.42, 1.0, eio((t - t2) / 1.2)))
    if t > t2: x, y = p(2.9, 49.65); title(can, t, t2 + 0.4, 'FRANKREICH', y, 70, YEL, None, 'bebas', max(x, 230))
    return can
# --- the Chir, December 1942
MT = Map(43.2, 48.95, 4.4)
CHIR = [(40.9, 49.65), (41.5, 49.40), (42.1, 49.05), (42.6, 48.70), (43.08, 48.36)]
DON = [(42.4, 49.75), (42.9, 49.30), (43.25, 48.85), (43.08, 48.36), (42.7, 47.95), (42.3, 47.6)]
def s_tschir(t, w0, w1):
    z = lerp(1.0, 1.05, prog(t, w0, w1)); can = grade(MT.frame(z), 0.1, 1.0); p = lambda lon, lat: MT.p(lon, lat, z)
    river(can, [p(*q) for q in DON], (110, 140, 170), 9); title(can, t, w0 + 0.15, 'DEZEMBER 1942', 420, 116, CREAM)
    t1 = ws('Tschir', 26) - 0.1
    if t > t1:
        u = eio((t - t1) / 0.6); pts = [p(*q) for q in CHIR]; n = max(2, int(len(pts) * u + 0.999)); river(can, pts[:n], (150, 190, 225), 9)
        x, y = p(42.0, 49.15); title(can, t, t1, 'TSCHIR', y - 50, 66, (150, 190, 225), None, 'bebas', x)
    x, y = p(44.52, 48.71); t2 = ws('Stalingrad', 26)
    if t > t2 - 0.1: dot(can, x, y, RED, 12); title(can, t, t2 - 0.1, 'STALINGRAD', y + 60, 60, CREAM, None, 'bebas', min(x, 720))
    t3 = ws('11.', 26)
    if t > t3:
        x, y = p(42.4, 48.6); title(can, t, t3, '11. PANZERDIVISION', y + 75, 54, YEL, None, 'bebas', x)
        for i, (dx, dy) in enumerate(((-70, 0), (0, -30), (70, 0))): tank(can, x + dx, y + dy, 1.0, YEL, False, eout((t - t3 - 0.12 * i) / 0.3))
    t4 = ws('sowjetische', 33) - 0.05
    if t > t4:   # the Soviet tank army comes down over the Chir
        for i, (lo, la) in enumerate(((41.7, 49.75), (42.2, 49.85), (42.7, 49.7), (43.1, 49.55))):
            u = eio((t - t4 - 0.08 * i) / 0.9); x, y = p(lo + 0.25 * u, la - 0.45 * u); tank(can, x, y, 1.0, RED, True, clamp((t - t4 - 0.08 * i) / 0.2))
        arrow(can, p(41.6, 49.45), p(42.0, 48.95), eio((t - t4 - 0.2) / 0.6)); arrow(can, p(42.6, 49.45), p(42.55, 48.85), eio((t - t4 - 0.3) / 0.6))
        title(can, t, t4 + 0.1, 'SOWJETISCHE PANZERARMEE', 530, 64, RED, None, 'bebas')
    return can
def s_soviet(t, w0, w1):   # b13: Soviet tanks and infantry
    can, m = side('b13', 500, 640, t, w0, w1, 1.04); shade(can, 200, 0.55)
    sky(can, t, ws('Panzerarmee', 33), 'PANZERARMEE', CX, 450, 120, CREAM, None, 0.5)
    return can
def s_night(t, w0, w1):   # b23 at night: the staff car in the pine forest
    can, m = side('b23', 560, 700, t, w0, w1, 1.05)
    rgb = ImageEnhance.Brightness(ImageEnhance.Color(can.convert('RGB')).enhance(0.35)).enhance(0.55)
    can = Image.blend(rgb, Image.new('RGB', (W, H), (20, 34, 60)), 0.3).convert('RGBA'); shade(can, 200, 0.55)
    title(can, t, ws('nachts', 35), 'NACHTS', 470, 140, (190, 205, 235), None)
    return can
def s_day(t, w0, w1):   # Panther moving in daylight
    can, m = film(min(16.9 + (t - w0) * 1.0, 19.85), 820, 560, 1.22)
    title(can, t, ws('tagsüber', 36), 'TAGSÜBER', 470, 140, CREAM, None)
    return can
def s_25(t, w0, w1):   # b22: Panzer III column, '25' painted on the turret side, then the arrow round behind
    can, m = side('b22', 760, 860, t, w0, w1, 1.04); shade(can, 200, 0.55)
    t1 = ws('25', 39)
    paint(can, t, t1, [m(*q) for q in pin('b22', 760, 860, w0, w1, 1.04, 41.0, qbox(585, 990, 'NUR 25', 96, tilt=4))], 'NUR 25', 96, CREAM, dur=0.4, mod=0.4, op=0.92)
    t2 = ws('Angreifern', 39) - 0.1
    if t > t2: path_arrow(can, [(140, 700), (400, 520), (760, 560), (900, 700), (830, 860)], eio((t - t2) / 1.0), YEL, 16, 50)
    return can
TURRET22 = [(1040, 980), (1560, 990), (1560, 1120), (1040, 1115)]
def s_hq(t, w0, w1):   # b24: at the map table, the army group written on the map
    can, m = side('b24', 700, 760, t, w0, w1, 1.04); shade(can, 200, 0.5)
    t1 = ws('Heeresgruppe', 44)
    pen(can, t, t1 - 0.05, 'Heeresgruppe', (800, 470), playfair(84, 700), (236, 210, 150), 0.8)
    return can
MAP24 = [(720, 1440), (1620, 1430), (1700, 1600), (680, 1612)]
def s_lorraine(t, w0, w1):   # b25: Panthers under foliage in a French village, autumn 1944
    can, m = side('b25', 900, 1150, t, w0, w1, 1.04); shade(can, 200, 0.55)
    pq = lambda tr, q: [m(*v) for v in pin('b25', 900, 1150, w0, w1, 1.04, tr, q)]
    paint(can, t, ws('Herbst', 47.5), pq(50.0, qbox(660, 628, 'HERBST 1944', 74, tilt=-5)), 'HERBST 1944', 74, (236, 230, 214), dur=0.6, mod=0.5, op=0.92)
    sky(can, t, ws('Lothringen', 49), 'LOTHRINGEN', CX, 420, 120, CREAM, None, 0.5)
    paint(can, t, ws('George', 51), pq(52.9, qbox(600, 1370, 'GEORGE PATTON', 84, keyst=0.06)), 'GEORGE PATTON', 84, YEL, dur=0.45, mod=0.35, op=0.95)
    return can
def s_guns(t, w0, w1):   # newsreel: a howitzer firing
    can, m = film(min(15.62 + (t - w0) * 0.45, 16.85), 960, 560, 1.25)
    title(can, t, ws('November', 53) + 0.45, 'NOVEMBER 1944', 440, 110, CREAM)
    return can
def s_exec(t, w0, w1):   # b12: a gun crew; the stamp
    can, m = side('b12', 1000, 1200, t, w0, w1, 1.04); shade(can, 200, 0.55); can = grade(can, 0.1, 0.5)
    pq = lambda q: [m(*v) for v in pin('b12', 1000, 1200, w0, w1, 1.04, 58.0, q)]
    paint(can, t, ws('ohne', 55) - 0.03, pq(qbox(CX, 255, 'OHNE GERICHTSVERFAHREN', 62)), 'OHNE GERICHTSVERFAHREN', 62, (232, 224, 205), dur=0.6, mod=0.45, op=0.92)
    paint(can, t, ws('erschießen', 55) - 0.03, pq(qbox(CX, 375, 'ERSCHOSSEN', 116)), 'ERSCHOSSEN', 116, (214, 58, 50), dur=0.45, mod=0.35, op=0.95, glow=((0, 0, 0), 12, 0.7))
    return can
def s_relieved(t, w0, w1):   # b20: with Major Walter, summer
    can = grade(fit('b20', t, w0, w1, 1.05)); shade(can, 210, 0.5)
    sky(can, t, ws('abgelöst', 60) - 0.03, 'ABGELÖST', CX, 300, 124, (222, 62, 54), None, 0.45)
    title(can, t, ws('Ungarn', 60), 'UNGARN', 1390, 100, YEL)
    return can
def s_captive(t, w0, w1):   # b10: German soldiers surrendering, 1945; the word on the white wall
    can, m = side('b10', 300, 500, t, w0, w1, 1.04); shade(can, 200, 0.55)
    pq = lambda q: [m(*v) for v in pin('b10', 300, 500, w0, w1, 1.04, 64.5, q)]; chalk = (238, 234, 224)
    paint(can, t, ws('Kriegsende', 63), pq(qbox(590, 240, 'KRIEGSENDE', 88)), 'KRIEGSENDE', 92, chalk, dur=0.5, mod=0.45)
    paint(can, t, ws('Gefangenschaft', 63) - 0.05, pq(qbox(590, 326, 'GEFANGENSCHAFT', 60)), 'GEFANGENSCHAFT', 62, YEL, dur=0.6, mod=0.4)
    return can
WALL10 = [(330, 330), (560, 320), (560, 480), (330, 488)]
def s_court(t, w0, w1):   # b14, profile: Stuttgart 1948
    can, m = side('b14', 620, 760, t, w0, w1, 1.04); shade(can, 210, 0.5)
    title(can, t, ws('1948', 66), 'STUTTGART 1948', 1060, 96, CREAM)
    title(can, t, ws('drei', 70) - 0.03, '3 JAHRE HAFT', 1185, 104, RED)
    t2 = ws('18', 72); arrow_to(can, (CX, 1250), (CX, 1312), eio((t - t2 + 0.1) / 0.3), YEL, 10, 30)
    title(can, t, t2 + 0.1, '18 MONATE', 1375, 84, YEL)
    return can
def s_quiet(t, w0, w1):   # b18, close-up: no interviews
    can = grade(fit('b18', t, w0, w1, 1.06), 0.12, 0.6); shade(can, 220, 0.5)
    return can
def s_doc(t, w0, w1):   # the 1980 report
    can = Image.new('RGBA', (W, H), (16, 15, 14, 255))
    k0 = eout((t - w0 - 0.1) / 0.5); pw, ph = 760, 900; L = Image.new('RGBA', (pw + 60, ph + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((30, 30, 30 + pw, 30 + ph), fill=(232, 228, 214, 255)); d.rectangle((30, 30, 30 + pw, 30 + ph), outline=(150, 140, 120, 255), width=3)
    lines_ = [('OFFICE OF NET ASSESSMENT', 30, w0 + 0.2), ('DEPARTMENT OF DEFENSE', 30, w0 + 0.5), ('', 0, 0), ('GENERALS BALCK AND', 48, ws('Mellenthin', 79) - 0.6),
              ('VON MELLENTHIN', 48, ws('Mellenthin', 79) - 0.2), ('ON TACTICS', 48, ws('Mellenthin', 79) + 0.2), ('', 0, 0), ('Implications for NATO', 32, ws('amerikanischen', 82)),
              ('Military Doctrine', 32, ws('amerikanischen', 82) + 0.4), ('', 0, 0), ('19 December 1980', 30, ws('erklärte', 83))]
    y = 110
    for s_, sz, ts in lines_:
        if sz:
            n = max(0, min(len(s_), int((t - ts) / 0.02))); d.text((30 + pw / 2, y), s_[:n], font=typew(sz), fill=INK + (255,), anchor='mm')
        y += (sz or 26) * 1.7
    L = L.rotate(-1.5, expand=True, resample=Image.BICUBIC)
    if k0 < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * k0)))
    sc = lerp(1.0, 1.04, prog(t, w0, w1)); L = L.resize((int(L.width * sc), int(L.height * sc)), Image.BICUBIC)
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (int(CX - L.width / 2 + 14), int(300 + 22)), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    can.alpha_composite(L, (int(CX - L.width / 2), int(300 + (1 - k0) * 40)))
    return can
def s_old(t, w0, w1):   # b03, post-war, in a suit
    can = grade(fit('b03', t, w0, w1, 1.06)); shade(can, 210, 0.5)
    title(can, t, ws('gegen', 85) - 0.05, 'GEGEN DIE', 330, 84, CREAM, None, 'anton', 765)
    title(can, t, ws('Sowjets', 85) - 0.05, 'SOWJETS', 445, 116, RED, None, 'anton', 765)
    return can
def s_nazi(t, w0, w1):   # b08: the army historian's verdict
    can = grade(fit('b08', t, w0, w1, 1.05)); shade(can, 220, 0.5)
    title(can, t, ws('US', 86) - 0.1, 'US ARMY HISTORIKER:', 1120, 70, CREAM, None, 'bebas')
    title(can, t, ws('überzeugten', 90), 'ÜBERZEUGTER', 1230, 104, CREAM)
    title(can, t, ws('Nationalsozialisten', 90), 'NATIONALSOZIALIST', 1350, 104, RED)
    return can
def s_death(t, w0, w1):   # b04, days before his death
    can = grade(fit('b04', t, w0, w1, 1.05), 0.1, 0.7); shade(can, 220, 0.5)
    title(can, t, ws('1982', 94), '1982', 280, 92, CREAM, None, 'anton', 850)
    return can
def s_final(t, w0, w1):   # b09: asked as a teacher, convicted as a perpetrator
    can = grade(fit('b09', t, w0, w1, 1.06)); shade(can, 220, 0.5)
    t1 = ws('Lehrer', 97); t2 = ws('Täter', 99)
    title(can, t, t1, 'LEHRER', 1150, 130, CREAM)
    if t > t2:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); f = anton(130); wl = f.getlength('LEHRER'); u = eio((t - t2) / 0.3)
        ImageDraw.Draw(L).line((CX - wl / 2 - 10, 1160, lerp(CX - wl / 2 - 10, CX + wl / 2 + 10, u), 1150), fill=RED + (240,), width=12); can.alpha_composite(L)
    title(can, t, t2 + 0.1, 'TÄTER', 1320, 170, RED)
    return can
def s_end(t, w0, w1):   # b07: the closing question
    can = grade(fit('b07', t, w0, w1, 1.06)); shade(can, 220, 0.5); return can

ANCH = [
 (0.0, s_open, None),
 (ws('Es', 6) - 0.05, s_film2, ('fade',)),
 (ws('deutsches', 7) - 0.05, s_film5, ('fade',)),
 (ws('Hermann', 11) - 0.1, s_name, ('fade',)),
 (ws('im', 15) - 0.1, s_ww1, ('fade',)),
 (ws('Am', 17.5) - 0.1, s_sedan, ('whip', 1)),
 (ws('Im', 25.5) - 0.1, s_tschir, ('fade',)),
 (ws('Panzerarmee', 33) - 0.08, s_soviet, ('whip', -1)),
 (ws('Eine', 35) - 0.1, s_night, ('fade',)),
 (ws('und', 37.5) - 0.1, s_day, ('fade',)),
 (ws('Mit', 39) - 0.1, s_25, ('whip', 1)),
 (ws('Er', 44) - 0.1, s_hq, ('fade',)),
 (ws('Im', 47.5) - 0.1, s_lorraine, ('fade',)),
 (ws('November', 53) + 0.2, s_guns, ('whip', -1)),
 (ws('ohne', 55.5) - 0.3, s_exec, ('fade',)),
 (ws('Im', 60) - 0.1, s_relieved, ('fade',)),
 (ws('Bei', 63.5) - 0.1, s_captive, ('fade',)),
 (ws('1948', 66.5) - 0.1, s_court, ('fade',)),
 (ws('Danach', 74.5) - 0.1, s_quiet, ('fade',)),
 (ws('Erst', 79) - 0.1, s_doc, ('fade',)),
 (ws('wie', 84.5) - 0.1, s_old, ('fade',)),
 (ws('Der', 86.8) - 0.1, s_nazi, ('fade',)),
 (ws('Hermann', 94.5) - 0.1, s_death, ('fade',)),
 (ws('Gefragt', 97.5) - 0.1, s_final, ('fade',)),
 (ws('Kanntet', 102.5) - 0.1, s_end, ('fade',))]
