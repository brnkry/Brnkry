
# ---------- scenes ----------
TOP = 330
def FV(k, a=0.0, ov=None, z1=1.06, fx=0.5, fy=0.5, sat=0.9):
    """archive film spread over the full 9:16 frame: a vertical slice around fx, slow push-in"""
    def fn(t, w0, w1):
        im = fat(k, a + max(0.0, t - w0)); z = lerp(1.0, z1, prog(t, w0, w1))
        ch = im.height / z; cw = ch * 9 / 16
        x0 = min(max(fx * im.width - cw / 2, 0), im.width - cw); y0 = min(max(fy * im.height - ch / 2, 0), im.height - ch)
        can = grade(im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA'), 0.1, sat); shade(can, 200, 0.55); can.alpha_composite(TOPSH)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
def see(can, fn_, a=0.9):
    """semi-transparent overlay: draw onto an empty layer, then lay it over the running film"""
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn_(L)
    if a < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
    can.alpha_composite(L)
def curl(can, t, t0, cx, cy, r, col=YEL, dur=0.45):
    """a curved arrow turning half way round a point (a sign being turned)"""
    if t < t0: return
    u = eio((t - t0) / dur); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    a0, a1 = -150, -150 + 200 * u; pts = [(cx + r * math.cos(math.radians(a)), cy + r * 0.45 * math.sin(math.radians(a))) for a in np.linspace(a0, a1, 40)]
    d.line(pts, fill=(0, 0, 0, 150), width=22, joint='curve'); d.line(pts, fill=col + (255,), width=14, joint='curve')
    e, q = pts[-1], pts[-4]; ang = math.atan2(e[1] - q[1], e[0] - q[0]); hd = 46
    d.polygon([(e[0] + 14 * math.cos(ang), e[1] + 14 * math.sin(ang)), (e[0] - hd * math.cos(ang - .5), e[1] - hd * math.sin(ang - .5)), (e[0] - hd * math.cos(ang + .5), e[1] - hd * math.sin(ang + .5))], fill=col + (255,))
    can.alpha_composite(L)

# 0: the hook, American generals in colour
def o_hook(can, t, w0, w1):
    title(can, t, ws('Dezember'), 'DEZEMBER 1944', TOP, 120, CREAM)
    hand(can, t, ws('beweisen'), 'Sind Sie Amerikaner?', (CX, 1330), 104, YEL, 0.75)
# 1: German soldiers behind the lines in American uniforms
def o_road(can, t, w0, w1):
    title(can, t, ws('hinter', 6), 'HINTER DEN LINIEN', TOP, 110, CREAM)
    paint(can, t, ws('deutsche'), [(40, 990), (1040, 965), (1050, 1095), (30, 1125)], 'DEUTSCHE SOLDATEN', 120, CREAM, dur=0.5, mod=0.35, t1=w0 + 2.85)
    title(can, t, ws('Uniformen'), 'IN US-UNIFORMEN', 1330, 110, YEL, None, bold=1)
# 2: the name of the plan, the griffin on old paper
def s_griff(t, w0, w1):
    can = BG('gbg', 0.0, 110)(t, w0); im = src('g_griff'); z = lerp(1.0, 1.04, prog(t, w0, w1)); sz = int(820 * z)
    P_ = grade(im.resize((sz, sz), Image.LANCZOS).convert('RGBA'), 0.1, 0.95).rotate(-2, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.75)))
    x, y = int(CX + 20 - P_.width / 2), int(880 - P_.height / 2); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (x + 10, y + 20)); can.alpha_composite(P_, (x, y))
    title(can, t, ws('Plan'), 'DER PLAN', TOP - 20, 90, CREAM)
    stamp(can, t, ws('Unternehmen'), 'UNTERNEHMEN GREIF', (CX + 20, 1235), 88, -5)
    return can
# 3-4: Otto Skorzeny
def s_skp(t, w0, w1):
    can = grade(fit('g_skp', t, w0, w1, 1.06)); shade(can, 230, 0.5)
    title(can, t, ws('Otto'), 'OTTO', 1185, 90, CREAM, None, bold=1)
    title(can, t, ws('Skorzeny'), 'SKORZENY', 1310, 150, YEL, None, bold=2)
    return can
def s_sk1(t, w0, w1):
    can = grade(fit('g_sk1', t, w0, w1, 1.06)); shade(can, 230, 0.5)
    title(can, t, ws('SS-Offizier'), 'SS-OFFIZIER', 1300, 120, CREAM, None, bold=1)
    return can
# 5: Mussolini freed at the Gran Sasso, September 1943
def o_muss(can, t, w0, w1):
    title(can, t, ws('Mussolini'), 'MUSSOLINI', TOP, 120, CREAM)
    title(can, t, ws('befreit'), 'BEFREIT 1943', 1330, 110, YEL, None, bold=1)
# 6: the Ardennes offensive, on the newsreel map itself
def o_ardmap(can, t, w0, w1):
    paint(can, t, ws('Ardennenoffensive'), [(110, 930), (980, 880), (990, 1010), (120, 1060)], 'ARDENNENOFFENSIVE', 110, RED, dur=0.6, mod=0.3, op=0.95, glow=((250, 240, 225), 10, 0.55))
    title(can, t, ws('Truppe'), 'EINE NEUE TRUPPE', 1330, 100, YEL, None, bold=1)
# 7: looking and talking like Americans
def o_aim(can, t, w0, w1):
    title(can, t, ws('wie', 23.9), 'WIE AMERIKANER', TOP, 120, CREAM)
    hand(can, t, ws('aussah'), 'aussehen', (CX - 120, 1250), 110, YEL, 0.5)
    hand(can, t, ws('sprach'), 'sprechen', (CX + 140, 1360), 110, YEL, 0.5)
# 8: too few volunteers with good English
def s_vol(t, w0, w1):
    can = BG('march', 0.0, 60, 1.4)(t, w0)
    l = [('GESUCHT', 66, RED, w0 + 0.2), ('', 10, INK, 0), ('Freiwillige', 50, INK, ws('Freiwillige')), ('mit gutem Englisch', 50, INK, ws('gutem'))]
    see(can, lambda L: sheet(L, t, w0 + 0.05, l, CX, 900, 820, -1.5), 0.9)
    stamp(can, t, ws('wenige'), 'ZU WENIGE', (CX + 40, 1230), 100, -7)
    title(can, t, w0 + 0.1, 'DIE FREIWILLIGEN', TOP, 100, CREAM)
    return can
# 9: hundreds of vehicles planned
def o_convoy(can, t, w0, w1):
    paint(can, t, ws('Hunderter'), [(120, 1010), (960, 990), (980, 1130), (110, 1160)], 'HUNDERTE FAHRZEUGE', 112, INK, dur=0.5, mod=0.45, op=0.92, glow=((240, 240, 236), 8, 0.4))
    if t > ws('bekam') - 0.25: strike(can, t, ws('bekam') - 0.25, (120, 1010, 980, 1150), RED, 12)
    title(can, t, ws('statt'), 'GEPLANT', TOP, 110, CREAM)
def s_got(t, w0, w1):
    can = BG('roadbg', 0.0, 70, 1.4)(t, w0)
    l = [('BEKOMMEN', 64, RED, w0 + 0.15), ('', 10, INK, 0), ('einige Jeeps', 52, INK, ws('Jeeps', 34)), ('Lastwagen', 52, INK, ws('Lastwagen'))]
    see(can, lambda L: sheet(L, t, w0 + 0.05, l, CX, 900, 760, 1.5), 0.9)
    title(can, t, ws('nur', 33.5), 'NUR', TOP, 120, YEL, None, bold=1)
    return can
# 10: one single Sherman
def o_sherman(can, t, w0, w1):
    title(can, t, ws('einzigen'), 'EIN EINZIGER', TOP - 40, 90, CREAM)
    title(can, t, ws('Sherman'), 'SHERMAN', TOP + 80, 140, YEL, None, bold=2)
# 11: a Panther disguised as an American M10 with sheet metal and paint (Ersatz M10, Malmedy): the words are painted along its sheet-metal side
def s_pm10(t, w0, w1):
    can, m = side('g_pred', 700, 1200, t, w0, w1, 1.03); shade(can, 210, 0.55); can.alpha_composite(TOPSH)
    paint(can, t, ws('Blech'), [m(1190, 672), m(1560, 682), m(1560, 849), m(1190, 845)], 'BLECH', 150, CREAM, dur=0.4, mod=0.55, op=0.9)
    paint(can, t, ws('Farbe'), [m(1585, 683), m(1905, 692), m(1905, 852), m(1585, 849)], 'FARBE', 150, CREAM, dur=0.4, mod=0.55, op=0.9)
    title(can, t, ws('Panzer', 37.5), 'PANTHER ALS US-PANZER', TOP, 96, CREAM)
    title(can, t, ws('getarnt'), 'GETARNT', 1330, 120, YEL, None, bold=1)
    return can
# 12: 16 December, the opening barrage at night
def o_barrage(can, t, w0, w1):
    sky(can, t, ws('16.'), '16. DEZEMBER', CX, 640, 130, CREAM, dur=0.55, skew=-8)
    sky(can, t, ws('Dezember', 41), '1944', CX, 800, 130, YEL, dur=0.4, skew=-8)
    title(can, t, ws('Offensive', 42), 'DIE OFFENSIVE BEGINNT', 1330, 90, CREAM, None, bold=1)
# 13-16: the commandos at work
def o_jeep(can, t, w0, w1):
    title(can, t, ws('Kommandos', 43), 'KLEINE KOMMANDOS', TOP, 110, CREAM)
    title(can, t, ws('erbeuteten'), 'IN ERBEUTETEN JEEPS', 1330, 96, YEL, None, bold=1)
def o_sign(can, t, w0, w1):
    title(can, t, ws('Wegweiser'), 'WEGWEISER', TOP, 120, CREAM)
    curl(can, t, ws('um', 46) - 0.15, 520, 760, 260, YEL, 0.4)
    title(can, t, ws('um', 46), 'UMGEDREHT', 1330, 110, YEL, None, bold=1)
def o_pole(can, t, w0, w1):
    stamp(can, t, ws('kappten') + 0.1, 'GEKAPPT', (560, 760), 110, -8)
    title(can, t, ws('Telefonleitungen'), 'TELEFONLEITUNGEN', 1330, 100, YEL, None, bold=1)
def o_column(can, t, w0, w1):
    title(can, t, ws('Kolonnen'), 'KOLONNEN', TOP, 120, CREAM)
    paint(can, t, ws('falsche'), [(190, 1150), (840, 1118), (930, 1295), (110, 1335)], 'FALSCHE RICHTUNG', 108, RED, dur=0.5, mod=0.35, op=0.95, glow=((245, 245, 240), 8, 0.4))
    if t > ws('schickten'):
        arrow(can, (760, 1000), (330, 860), eio((t - ws('schickten')) / 0.5), YEL, 14, 44)
    if t > ws('falsche') + 0.2:
        arrow(can, (330, 860), (820, 760), eio((t - ws('falsche') - 0.2) / 0.5), RED, 14, 44)
# 17: few teams got through, the rumour spread faster
MA = Map(5.95, 50.25, 2.7)
FRONT = [(6.25, 50.62), (6.27, 50.40), (6.14, 50.20), (6.04, 50.05), (6.13, 49.92), (6.42, 49.81)]
def s_rumor(t, w0, w1):
    can = BG('rumor', 0.0, 50, 1.6)(t, w0); z = lerp(1.0, 1.04, prog(t, w0, w1)); mp = MA.frame(z); mp.putalpha(165); can.alpha_composite(mp)
    p = lambda lo, la: MA.p(lo, la, z)
    see(can, lambda L: ImageDraw.Draw(L).line([p(*q) for q in FRONT], fill=RED + (255,), width=10, joint='curve'), 0.85)
    title(can, t, w0 + 0.2, 'FRONT 16.12.', p(6.55, 50.52)[1], 40, RED, None, 'bebas', min(p(6.55, 50.52)[0], 960))
    for nm, lo, la in (('LÜTTICH', 5.57, 50.63), ('MALMEDY', 6.03, 50.43), ('ST. VITH', 6.13, 50.28), ('BASTOGNE', 5.72, 50.0)):
        x, y = p(lo, la); dot(can, x, y, CREAM, 8); title(can, t, w0 + 0.2, nm, y - 42, 42, CREAM, None, 'bebas', min(max(x, 120), 960))
    t0 = ws('wenige', 50.6)
    for i, (a_, b_) in enumerate((((6.30, 50.50), (5.80, 50.48)), ((6.25, 50.30), (5.70, 50.28)), ((6.10, 50.10), (5.55, 50.12)), ((6.30, 49.95), (5.80, 49.92)))):
        ok = i == 1; u = eio((t - t0 - i * 0.12) / 0.8) * (1.0 if ok else 0.55)
        if u > 0:
            A, Bp = p(*a_), p(*b_); e = (lerp(A[0], Bp[0], u), lerp(A[1], Bp[1], u))
            dashed(can, [A, e], 1.0, YEL, 6, 18, 26)
            if not ok and t > ws('durch'): ring(can, t, ws('durch') + i * 0.08, e[0], e[1], RED, 22, True)
    if t > ws('Gerücht'):
        x, y = p(5.70, 50.28); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for j in range(5):
            u = ((t - ws('Gerücht')) * 0.55 + j / 5) % 1.0; r = 40 + 760 * u; d.ellipse((x - r, y - r, x + r, y + r), outline=YEL + (int(190 * (1 - u)),), width=6)
        can.alpha_composite(L)
    title(can, t, ws('Nur', 50.4), 'NUR WENIGE KAMEN DURCH', TOP, 92, CREAM, ws('Gerücht') - 0.2)
    title(can, t, ws('Gerücht'), 'DAS GERÜCHT', TOP, 120, YEL, None, bold=1)
    title(can, t, ws('schneller'), 'SCHNELLER ALS SIE', 1330, 96, CREAM, None, bold=1)
    return can
# 18-19: trick questions at every crossing
def o_post(can, t, w0, w1):
    title(can, t, ws('Kreuzung'), 'AN JEDER KREUZUNG', TOP, 110, CREAM)
    stamp(can, t, ws('Fangfragen'), 'FANGFRAGEN', (CX, 1300), 110, -5)
def o_gis(can, t, w0, w1):
    def pad(L):
        k = eout((t - w0) / 0.35); P_ = Image.new('RGBA', (840, 470), (236, 230, 212, 255)); d = ImageDraw.Draw(P_)
        for yy in range(70, 470, 58): d.line((30, yy, 810, yy), fill=(150, 170, 200, 255), width=2)
        d.line((90, 0, 90, 470), fill=(200, 90, 90, 255), width=2)
        P_ = P_.rotate(-2, expand=True, resample=Image.BICUBIC)
        if k < 1: P_.putalpha(P_.getchannel('A').point(lambda v: int(v * k)))
        L.alpha_composite(P_, (int(CX - P_.width / 2), int(1010 - P_.height / 2 + (1 - k) * 60)))
    see(can, pad, 0.92)
    hand(can, t, ws('Wer', 59), 'Wer spielt bei den Yankees?', (CX + 20, 880), 76, INK, 0.7)
    hand(can, t, ws('Wie', 60.5), 'Wie heißt die Freundin', (CX + 20, 1000), 76, INK, 0.6)
    hand(can, t, ws('Micky'), 'von Micky Maus?', (CX + 20, 1110), 76, INK, 0.45)
    title(can, t, w0 + 0.1, 'DIE FRAGEN', TOP, 110, CREAM)
# 20: Omar Bradley
def s_brad(t, w0, w1):
    can = grade(fit('g_brad', t, w0, w1, 1.06)); shade(can, 230, 0.5)
    title(can, t, ws('Omar'), 'OMAR BRADLEY', 1190, 110, CREAM, None, bold=1)
    hand(can, t, ws('Hauptstadt'), 'Hauptstadt von Illinois?', (CX, 1330), 96, YEL, 0.7)
    return can
# 21: the claimed plan to kill Eisenhower in Paris
MP = Map(4.25, 49.55, 6.6)
def s_paris(t, w0, w1):
    can = BG('paris', 0.0, 50, 1.6)(t, w0); z = lerp(1.0, 1.04, prog(t, w0, w1)); mp = MP.frame(z); mp.putalpha(165); can.alpha_composite(mp)
    p = lambda lo, la: MP.p(lo, la, z)
    for nm, lo, la in (('BELGIEN', 4.6, 50.75), ('FRANKREICH', 3.3, 48.35), ('DEUTSCHLAND', 7.2, 50.15)):
        x, y = p(lo, la); title(can, t, w0 + 0.2, nm, y, 46, (150, 160, 178), None, 'bebas', min(max(x, 130), 950))
    xa, ya = p(5.95, 50.25); xp, yp = p(2.35, 48.86)
    poly_fill(can, [p(5.4, 50.55), p(6.3, 50.6), p(6.4, 49.85), p(5.6, 49.8)], RED, 70)
    title(can, t, w0 + 0.2, 'ARDENNEN', ya - 120, 50, RED, None, 'bebas', xa)
    dashed(can, [(xa, ya), (lerp(xa, xp, 0.5), lerp(ya, yp, 0.5) - 60), (xp + 30, yp - 10)], eio((t - ws('unterwegs')) / 1.0), YEL, 8, 22, 34)
    dot(can, xp, yp, CREAM, 10); title(can, t, w0 + 0.2, 'PARIS', yp + 50, 52, CREAM, None, 'bebas', xp + 30)
    if t > ws('Eisenhower'): ring(can, t, ws('Eisenhower'), xp, yp, RED, 40, False)
    hand(can, t, ws('töten') - 0.1, 'Eisenhower töten?', (CX, 1330), 104, YEL, 0.6)
    title(can, t, ws('behaupteten'), 'DIE BEHAUPTUNG', TOP, 110, CREAM)
    return can
# 22-23: Eisenhower, Christmas under guard
def s_ike(t, w0, w1):
    can = grade(fit('g_ike', t, w0, w1, 1.05)); shade(can, 230, 0.5)
    stamp(can, t, ws('Belegt'), 'NICHT BELEGT', (CX, 1270), 96, -6)
    title(can, t, ws('Oberbefehlshaber'), 'DWIGHT D. EISENHOWER', TOP, 84, CREAM)
    title(can, t, ws('Oberbefehlshaber') + 0.2, 'ALLIIERTER OBERBEFEHLSHABER', TOP + 80, 52, YEL, None, 'bebas')
    return can
def o_ikefilm(can, t, w0, w1):
    title(can, t, ws('Weihnachten', 75), 'WEIHNACHTEN 1944', TOP, 110, CREAM)
    title(can, t, ws('strenger'), 'UNTER BEWACHUNG', 1330, 110, YEL, None, bold=1)
# 24-27: three men caught at Aywaille, tried and shot
def o_ayw(can, t, w0, w1):
    title(can, t, ws('Drei'), 'DREI MÄNNER', TOP, 120, CREAM)
    title(can, t, ws('Aywaille'), 'AYWAILLE', 1310, 130, YEL, None, bold=1)
def o_pw(can, t, w0, w1):
    stamp(can, t, ws('Passwort'), 'PASSWORT?', (CX, 1260), 120, -6)
def s_court(t, w0, w1):
    can = BG('court', 0.0, 70, 1.4)(t, w0)
    l = [('MILITÄRGERICHT', 60, INK, ws('Militärgericht')), ('', 10, INK, 0), ('Urteil: Spionage', 48, INK, ws('verurteilte')), ('Tod durch Erschießen', 48, RED, ws('Spione'))]
    see(can, lambda L: sheet(L, t, w0 + 0.05, l, CX, 920, 860, -1.2), 0.9)
    return can
def s_com(t, w0, w1):
    can, m = side('g_com', 500, 760, t, w0, w1, 1.04); shade(can, 210, 0.55); can.alpha_composite(TOPSH)
    paint(can, t, ws('Weihnachten', 85), [m(880, 610), m(1370, 705), m(1370, 805), m(880, 715)], '23. DEZEMBER', 110, INK, dur=0.5, mod=0.55, op=0.85, glow=None)
    paint(can, t, ws('Weihnachten', 85) + 0.35, [m(950, 760), m(1310, 830), m(1310, 950), m(950, 880)], '1944', 120, INK, dur=0.35, mod=0.55, op=0.85, glow=None)
    title(can, t, ws('erschossen'), 'ERSCHOSSEN', 1330, 120, RED, None, bold=1)
    return can
# 28-29: Skorzeny in Dachau, acquitted
def o_skint(can, t, w0, w1):
    paint(can, t, ws('Dachau'), [(712, 560), (1030, 553), (1032, 668), (714, 675)], 'DACHAU', 110, INK, dur=0.5, mod=0.5, op=0.85, glow=None)
    paint(can, t, ws('1947'), [(745, 700), (1020, 694), (1022, 812), (747, 818)], '1947', 110, INK, dur=0.4, mod=0.5, op=0.85, glow=None)
    title(can, t, ws('Gericht', 91), 'VOR GERICHT', 1180, 110, CREAM, None, bold=1)
    cta(can, t, ws('1947') + 0.8)
def o_mug(can, t, w0, w1):
    stamp(can, t, ws('freigesprochen'), 'FREIGESPROCHEN', (CX, 1150), 100, -6)
    cta(can, t, ws('1947') + 0.8)

ANCH = [
 (0.0, FV('hook', 0.0, o_hook, 1.05, 0.5), None),
 (ws('denn', 5.5) - 0.1, FV('road', 0.0, o_road, 1.05, 0.5), ('fade',)),
 (ws('Der', 10) - 0.1, s_griff, ('whip', 1)),
 (ws('Geführt') - 0.1, s_skp, ('fade',)),
 (ws('dem', 14.9) - 0.1, s_sk1, ('fade',)),
 (ws('Mussolini') - 0.1, FV('muss', 0.0, o_muss, 1.04, 0.45), ('whip', -1)),
 (ws('Für', 20.3) - 0.1, FV('ardmap', 0.0, o_ardmap, 1.05, 0.5), ('fade',)),
 (ws('die', 23.4) - 0.1, FV('aim', 0.0, o_aim, 1.05, 0.5), ('whip', 1)),
 (ws('Doch', 26.3) - 0.1, s_vol, ('fade',)),
 (ws('und', 29.9) - 0.1, FV('convoy', 0.0, o_convoy, 1.04, 0.5), ('fade',)),
 (ws('Skorzeny', 32.9) - 0.4, s_got, ('fade',)),
 (ws('und', 35.6) - 0.1, FV('sherman', 0.0, o_sherman, 1.04, 0.5), ('whip', 1)),
 (ws('Die', 37.3) - 0.1, s_pm10, ('fade',)),
 (ws('Am', 40.3) - 0.1, FV('barrage', 0.0, o_barrage, 1.03, 0.5), ('whip', -1)),
 (ws('Kleine') - 0.1, FV('jeep', 0.0, o_jeep, 1.04, 0.5), ('fade',)),
 (ws('drehten') - 0.1, FV('sign', 0.0, o_sign, 1.03, 0.5), ('fade',)),
 (ws('kappten') - 0.05, FV('pole', 0.0, o_pole, 1.03, 0.62), ('fade',)),
 (ws('und', 47.9) - 0.15, FV('column', 0.0, o_column, 1.04, 0.5), ('fade',)),
 (ws('Nur', 50.4) - 0.1, s_rumor, ('whip', 1)),
 (ws('An', 55.2) - 0.1, FV('post', 0.0, o_post, 1.04, 0.5), ('whip', -1)),
 (ws('Wer', 59) - 0.1, FV('gis', 0.0, o_gis, 1.04, 0.5), ('fade',)),
 (ws('General', 62.6) - 0.1, s_brad, ('fade',)),
 (ws('Gefangene') - 0.1, s_paris, ('whip', 1)),
 (ws('Belegt') - 0.1, s_ike, ('fade',)),
 (ws('Weihnachten', 75) - 0.1, FV('ikefilm', 0.0, o_ikefilm, 1.04, 0.5), ('fade',)),
 (ws('Drei') - 0.1, FV('ayw', 0.0, o_ayw, 1.04, 0.5), ('whip', -1)),
 (ws('Sie', 80.5) - 0.1, FV('pw', 0.0, o_pw, 1.03, 0.5), ('fade',)),
 (ws('ein', 82.3) - 0.1, s_court, ('fade',)),
 (ws('und', 85) - 0.1, s_com, ('fade',)),
 (ws('Skorzeny', 87.4) - 0.1, FV('skint', 0.0, o_skint, 1.04, 0.5), ('whip', 1)),
 (ws('und', 91.6) - 0.1, FV('mug', 0.0, o_mug, 1.03, 0.5), ('fade',))]
