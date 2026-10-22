
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
    can, m = film(min(10.12 + (t - w0) * 0.8, 12.3), 980, 600, 1.28)
    stamp(can, t, ws('verurteilt', 9) - 0.03, '1948 VERURTEILT', (CX, 1320), 92, -6)
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
MS = Map(4.4, 49.9, 4.6, hi=('France',))
MAAS = [(4.87, 50.47), (4.91, 50.26), (4.82, 50.14), (4.72, 49.90), (4.72, 49.77), (4.94, 49.70), (5.10, 49.55), (5.38, 49.16)]
def s_sedan(t, w0, w1):
    z = lerp(1.0, 1.05, prog(t, w0, w1)); can = grade(MS.frame(z), 0.1, 1.0); p = lambda lon, lat: MS.p(lon, lat, z)
    river(can, [p(*q) for q in MAAS]); title(can, t, w0 + 0.15, '13. MAI 1940', 420, 120, CREAM)
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
MT = Map(43.2, 48.7, 4.4)
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
    if t > t3: x, y = p(42.4, 48.6); dot(can, x, y, YEL, 10); title(can, t, t3, '11. PANZERDIVISION', y + 60, 54, YEL, None, 'bebas', x)
    return can
def s_soviet(t, w0, w1):   # b13: Soviet tanks and infantry
    can, m = side('b13', 500, 640, t, w0, w1, 1.04); shade(can, 200, 0.55)
    sky(can, t, ws('Panzerarmee', 32), 'PANZERARMEE', CX, 450, 120, CREAM, None, 0.5)
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
    if t > t1: on_quad(can, [m(*q) for q in TURRET22], 'NUR 25', 120, clamp((t - t1) / 0.06), CREAM, anton(120), eio((t - t1) / 0.4), 0.8, mod=0.4, op=0.92)
    t2 = ws('Angreifern', 39) - 0.1
    if t > t2: path_arrow(can, [(140, 760), (420, 560), (820, 640), (930, 880), (720, 1060)], eio((t - t2) / 1.0), YEL, 16, 50)
    return can
TURRET22 = [(1040, 980), (1560, 990), (1560, 1120), (1040, 1115)]
def s_hq(t, w0, w1):   # b24: at the map table, the army group written on the map
    can, m = side('b24', 700, 760, t, w0, w1, 1.04); shade(can, 200, 0.5)
    t1 = ws('Heeresgruppe', 44)
    title(can, t, t1 - 0.05, 'HEERESGRUPPE', 1300, 120, YEL)
    return can
MAP24 = [(720, 1440), (1620, 1430), (1700, 1600), (680, 1612)]
def s_lorraine(t, w0, w1):   # b25: Panthers under foliage in a French village, autumn 1944
    can, m = side('b25', 900, 1150, t, w0, w1, 1.04); shade(can, 200, 0.55)
    title(can, t, ws('Herbst', 47.5), 'HERBST 1944', 1180, 100, CREAM, ws('gegen', 50) - 0.2)
    sky(can, t, ws('Lothringen', 49), 'LOTHRINGEN', CX, 440, 120, CREAM, None, 0.5)
    title(can, t, ws('Patton', 51), 'GEGEN PATTON', 1220, 110, YEL)
    return can
def s_guns(t, w0, w1):   # newsreel: a howitzer firing
    can, m = film(min(15.62 + (t - w0) * 0.45, 16.85), 960, 560, 1.25)
    title(can, t, ws('November', 53), 'NOVEMBER 1944', 440, 110, CREAM)
    return can
def s_exec(t, w0, w1):   # b12: a gun crew; the stamp
    can, m = side('b12', 1000, 1200, t, w0, w1, 1.04); shade(can, 200, 0.55); can = grade(can, 0.1, 0.5)
    stamp(can, t, ws('ohne', 55) - 0.03, 'OHNE GERICHTSVERFAHREN', (CX, 1180), 74, -5)
    stamp(can, t, ws('erschießen', 55) - 0.03, 'ERSCHOSSEN', (CX, 1340), 110, -7)
    return can
def s_relieved(t, w0, w1):   # b20: with Major Walter, summer
    can = grade(fit('b20', t, w0, w1, 1.05)); shade(can, 210, 0.5)
    stamp(can, t, ws('abgelöst', 60) - 0.03, 'ABGELÖST', (CX, 1250), 110, -6)
    title(can, t, ws('Ungarn', 60), 'UNGARN', 1390, 100, YEL)
    return can
def s_captive(t, w0, w1):   # b10: German soldiers surrendering, 1945; the word on the white wall
    can, m = side('b10', 300, 500, t, w0, w1, 1.04); shade(can, 200, 0.55)
    t1 = ws('Gefangenschaft', 63)
    title(can, t, t1 - 0.05, 'GEFANGENSCHAFT', 1380, 96, YEL)
    title(can, t, ws('Kriegsende', 63), 'KRIEGSENDE', 1250, 104, CREAM)
    return can
WALL10 = [(330, 330), (560, 320), (560, 480), (330, 488)]
def s_court(t, w0, w1):   # b14, profile: Stuttgart 1948
    can, m = side('b14', 620, 760, t, w0, w1, 1.04); shade(can, 210, 0.5)
    title(can, t, ws('1948', 66), 'STUTTGART 1948', 1120, 96, CREAM)
    stamp(can, t, ws('drei', 70) - 0.03, '3 JAHRE HAFT', (CX, 1270), 104, -6)
    title(can, t, ws('18', 72), '18 MONATE', 1410, 84, YEL)
    return can
def s_quiet(t, w0, w1):   # b18, close-up: no interviews
    can = grade(fit('b18', t, w0, w1, 1.06), 0.12, 0.6); shade(can, 220, 0.5)
    stamp(can, t, ws('Interviews', 76) - 0.03, 'KEINE INTERVIEWS', (CX, 1320), 92, -6)
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
    stamp(can, t, ws('Sowjets', 84) - 0.05, 'GEGEN DIE SOWJETS', (CX - 20, 1300), 64, -5)
    return can
def s_nazi(t, w0, w1):   # b08: the army historian's verdict
    can = grade(fit('b08', t, w0, w1, 1.05)); shade(can, 220, 0.5)
    title(can, t, ws('US', 86) - 0.1, 'US ARMY HISTORIKER:', 1120, 70, CREAM, None, 'bebas')
    title(can, t, ws('überzeugten', 90), 'ÜBERZEUGTER', 1230, 104, CREAM)
    title(can, t, ws('Nationalsozialisten', 90), 'NATIONALSOZIALIST', 1350, 104, RED)
    return can
def s_death(t, w0, w1):   # b04, days before his death
    can = grade(fit('b04', t, w0, w1, 1.05), 0.1, 0.7); shade(can, 220, 0.5)
    title(can, t, ws('1982', 94), '1982', 1280, 170, CREAM)
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
 (ws('Eine', 32.5) - 0.1, s_soviet, ('whip', -1)),
 (ws('Eine', 35) - 0.1, s_night, ('fade',)),
 (ws('und', 37.5) - 0.1, s_day, ('fade',)),
 (ws('Mit', 39) - 0.1, s_25, ('whip', 1)),
 (ws('Er', 44) - 0.1, s_hq, ('fade',)),
 (ws('Im', 47.5) - 0.1, s_lorraine, ('fade',)),
 (ws('Im', 53) - 0.1, s_guns, ('whip', -1)),
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
