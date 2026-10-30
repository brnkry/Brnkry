
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

def underlined(can, t, t0, s_, y, size, col=CREAM, ucol=RED, x=CX):
    """straight title, a bar wipes in under it"""
    if t < t0: return
    title(can, t, t0, s_, y, size, col, None, 'anton', x, 900, 1)
    w_ = anton(size).getlength(s_); u = eio((t - t0 - 0.15) / 0.35)
    if u > 0:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); y0 = y + size * 0.62
        d.rectangle((x - w_ / 2 + 3, y0 + 4, x - w_ / 2 + w_ * u + 3, y0 + 18), fill=(0, 0, 0, 120)); d.rectangle((x - w_ / 2, y0, x - w_ / 2 + w_ * u, y0 + 14), fill=ucol + (255,)); can.alpha_composite(L)
def sliced(can, t, t0, s_, xy, size, col=CREAM):
    """a straight word that is cut through: a thin red line runs across, then the top half slides off"""
    if t < t0: return
    f = anton(size); bb = f.getbbox(s_); w_, h_ = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    L = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); ImageDraw.Draw(L).text((20 - bb[0], 20 - bb[1]), s_, font=f, fill=col + (255,))
    k = eout((t - t0) / 0.3); L.putalpha(L.getchannel('A').point(lambda v: int(v * k)))
    cy = h_ // 2; top, bot = L.crop((0, 0, w_, cy)), L.crop((0, cy, w_, h_)); sh = eout((t - t0 - 0.45) / 0.3) * 26
    O = Image.new('RGBA', (w_ + 60, h_ + 20), (0, 0, 0, 0)); O.alpha_composite(top, (int(30 + sh), int(10 - sh * 0.25))); O.alpha_composite(bot, (30, cy + 10))
    S = Image.new('RGBA', O.size, (0, 0, 0, 0)); S.paste((0, 0, 0, 200), (0, 0), O.getchannel('A'))
    x, y = int(xy[0] - O.width / 2), int(xy[1] - O.height / 2); can.alpha_composite(S.filter(ImageFilter.GaussianBlur(8)), (x + 3, y + 7)); can.alpha_composite(O, (x, y))
    u = eio((t - t0 - 0.2) / 0.25)
    if u > 0:
        D = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(D).line((x + 10, y + cy + 10, x + 10 + (O.width - 20) * u, y + cy + 10), fill=RED + (255,), width=6); can.alpha_composite(D)
def asks(can, t, t0, s_, y, size, col=CREAM):
    """straight word, a big yellow question mark drops in after it and keeps bouncing"""
    if t < t0: return
    f = anton(size); w_ = f.getlength(s_); q = anton(int(size * 1.35)); wq = q.getlength('?'); x = CX - (w_ + wq + 16) / 2
    title(can, t, t0, s_, y, size, col, None, 'anton', x + w_ / 2, 900, 1)
    tq = t0 + 0.3
    if t > tq:
        k = eout((t - tq) / 0.3); bo = -(1 - k) * 120 - abs(math.sin((t - tq) * 4.0)) * 14 * k
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).text((x + w_ + 16 + wq / 2, y - 6 + bo), '?', font=q, fill=YEL + (int(255 * k),), anchor='mm')
        S = Image.new('RGBA', (W, H), (0, 0, 0, 0)); S.paste((0, 0, 0, 200), (0, 0), L.getchannel('A')); can.alpha_composite(S.filter(ImageFilter.GaussianBlur(8)), (3, 7)); can.alpha_composite(L)
def crossed(can, t, t0, s_, y, size, note, col=CREAM):
    """the word, a red line through it, and the correction written above by hand"""
    if t < t0: return
    title(can, t, t0, s_, y, size, col, None, 'anton', CX, 900, 1)
    w_ = anton(size).getlength(s_); strike(can, t, t0 + 0.2, (CX - w_ / 2, y - size * 0.45, CX + w_ / 2, y + size * 0.35), RED, 12, 0.3)
    hand(can, t, t0 + 0.45, note, (CX - w_ / 2 + 20, y - size * 1.2), 96, RED, 0.4)
def pwfield(can, t, t0, y, ok_t):
    """a sentry's challenge as an input field: the cursor blinks, the answer stays empty, a red question mark follows"""
    if t < t0: return
    k = eout((t - t0) / 0.3); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, x1 = 150, 930; d.rounded_rectangle((x0, y - 70, x1, y + 70), 18, fill=(10, 11, 14, int(170 * k)), outline=YEL + (int(230 * k),), width=4)
    d.text((x0 + 36, y), 'PASSWORT:', font=bebas(84), fill=CREAM + (int(255 * k),), anchor='lm')
    fx = x0 + 36 + bebas(84).getlength('PASSWORT:') + 26
    for i in range(4): d.rectangle((fx + i * 70, y + 26, fx + i * 70 + 46, y + 32), fill=GREY + (int(220 * k),))
    if t < ok_t and int((t - t0) * 2.6) % 2 == 0: d.rectangle((fx, y - 34, fx + 6, y + 22), fill=YEL + (int(255 * k),))
    if t >= ok_t: d.text((fx + 2 * 70 + 23, y - 2), '?', font=anton(110), fill=RED + (int(255 * eout((t - ok_t) / 0.25)),), anchor='mm')
    can.alpha_composite(L)
def verdict(can, t, t0, s_, y, size, col=YEL):
    """two thin lines open from the middle, the word settles between them"""
    if t < t0: return
    u = eio((t - t0) / 0.4); w_ = anton(size).getlength(s_) + 60; L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for yy in (y - size * 0.72, y + size * 0.62):
        d.rectangle((CX - w_ / 2 * u, yy, CX + w_ / 2 * u, yy + 5), fill=CREAM + (235,))
    can.alpha_composite(L); title(can, t, t0 + 0.2, s_, y, size, col, None, 'anton', CX, 960, 1)

# 0: the hook, American generals in colour
def o_hook(can, t, w0, w1):
    title(can, t, ws('Dezember'), 'DEZEMBER 1944', TOP, 120, CREAM)
    hand(can, t, ws('beweisen'), 'Sind Sie Amerikaner?', (CX, 1330), 104, YEL, 0.75)
# 1: German soldiers behind the lines in American uniforms
def o_road(can, t, w0, w1):
    title(can, t, ws('hinter', 6), 'HINTER DEN LINIEN', TOP, 110, CREAM)
    paint(can, t, ws('deutsche'), [(40, 990), (1040, 965), (1050, 1095), (30, 1125)], 'DEUTSCHE SOLDATEN', 120, CREAM, dur=0.5, mod=0.35, t1=w0 + 2.85)
    title(can, t, ws('Uniformen'), 'IN US-UNIFORMEN', 1330, 110, YEL, None, bold=1)
# 2: the name of the plan, written like the name in the Rommel short: a disguised Panther of Kampfgruppe X behind it
def s_plan(t, w0, w1):
    can, m = side('g_kgx', 900, 1350, t, w0, w1, 1.04); shade(can, 230, 0.5); can.alpha_composite(TOPSH)
    title(can, t, ws('Plan'), 'DER PLAN', TOP, 100, CREAM)
    title(can, t, ws('Unternehmen'), 'UNTERNEHMEN', 1290, 90, CREAM, None, bold=1)
    title(can, t, ws('Greif'), 'GREIF', 1400, 150, YEL, None, bold=2)
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
# 5: Mussolini freed at the Gran Sasso, September 1943 (the colourised photo)
def s_muss(t, w0, w1):
    can, m = side('g_gs', 1080, 1260, t, w0, w1, 1.04); shade(can, 220, 0.5); can.alpha_composite(TOPSH)
    title(can, t, ws('Mussolini'), 'MUSSOLINI', TOP, 120, CREAM)
    title(can, t, ws('befreit'), 'BEFREIT 1943', 1330, 110, YEL, None, bold=1)
    return can
# 6: the Ardennes offensive, on the newsreel map itself
def o_ardmap(can, t, w0, w1):
    paint(can, t, ws('Ardennenoffensive'), [(110, 930), (980, 880), (990, 1010), (120, 1060)], 'ARDENNENOFFENSIVE', 110, RED, dur=0.6, mod=0.3, op=0.95, glow=((250, 240, 225), 10, 0.55))
def s_skt(t, w0, w1):
    can = grade(fit('g_skt', t, w0, w1, 1.05)); shade(can, 230, 0.5)
    title(can, t, ws('Truppe'), 'EINE NEUE TRUPPE', 1330, 100, YEL, None, bold=1)
    return can
# 7: looking and talking like Americans
def o_aim(can, t, w0, w1):
    title(can, t, ws('wie', 23.9), 'WIE AMERIKANER', TOP, 120, CREAM)
    hand(can, t, ws('aussah'), 'aussehen', (CX - 120, 1250), 110, YEL, 0.5)
    hand(can, t, ws('sprach'), 'sprechen', (CX + 140, 1360), 110, YEL, 0.5)
# 8: too few volunteers with good English
def s_vol(t, w0, w1):
    can = BG('march', 0.0, 60, 1.4)(t, w0)
    l = [('GESUCHT', 66, RED, w0 + 0.2), ('', 10, INK, 0), ('Freiwillige', 50, INK, ws('Freiwillige')), ('mit gutem Englisch', 50, INK, ws('gutem'))]
    see(can, lambda L: sheet(L, t, w0 + 0.05, l, CX, 860, 820, 0.0), 0.9)
    underlined(can, t, ws('wenige'), 'ZU WENIGE', 1250, 120, YEL, RED)
    title(can, t, w0 + 0.1, 'DIE FREIWILLIGEN', TOP, 100, CREAM)
    return can
# 9: hundreds of vehicles planned
def o_convoy(can, t, w0, w1):
    paint(can, t, ws('Hunderter'), [(120, 1010), (960, 990), (980, 1130), (110, 1160)], 'HUNDERTE FAHRZEUGE', 112, INK, dur=0.5, mod=0.45, op=0.92, glow=((240, 240, 236), 8, 0.4))
    if t > ws('Fahrzeuge') + 0.15: strike(can, t, ws('Fahrzeuge') + 0.15, (120, 1010, 980, 1150), RED, 12)
    title(can, t, ws('statt'), 'GEPLANT', TOP, 110, CREAM)
def s_got(t, w0, w1):
    can = BG('roadbg', 0.0, 70, 1.4)(t, w0)
    l = [('BEKOMMEN', 64, RED, w0 + 0.15), ('', 10, INK, 0), ('einige Jeeps', 52, INK, ws('Jeeps', 34)), ('Lastwagen', 52, INK, ws('Lastwagen'))]
    see(can, lambda L: sheet(L, t, w0 + 0.05, l, CX, 900, 760, 0.0), 0.9)
    title(can, t, ws('nur', 33.5), 'NUR', TOP, 120, YEL, None, bold=1)
    return can
# 10: one single Sherman
def o_sherman(can, t, w0, w1):
    title(can, t, ws('einzigen'), 'EIN EINZIGER', TOP - 40, 90, CREAM)
    title(can, t, ws('Sherman'), 'SHERMAN', TOP + 80, 140, YEL, None, bold=2)
# 11: a Panther disguised as an American M10 with sheet metal and paint (Ersatz M10, Malmedy): the words are painted along its sheet-metal side
def s_cafe(t, w0, w1):
    can, m = side('g_pm10', 300, 560, t, w0, w1, 1.04); shade(can, 210, 0.55); can.alpha_composite(TOPSH)
    title(can, t, w0 + 0.1, 'DIE ANDEREN PANZER', TOP, 100, CREAM)
    k = eout((t - w0 - 0.25) / 0.35)
    if k > 0:
        im = src('g_m10').resize((330, 330), Image.LANCZOS).convert('RGBA'); P_ = Image.new('RGBA', (350, 410), CREAM + (255,)); P_.alpha_composite(grade(im, 0.08, 0.9), (10, 10))
        ImageDraw.Draw(P_).text((175, 375), 'ECHTER US-M10', font=bebas(40), fill=INK + (255,), anchor='mm'); P_.putalpha(P_.getchannel('A').point(lambda v: int(v * k)))
        sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.6)))
        x, y = 690, int(450 + (1 - k) * 40); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (x + 6, y + 12)); can.alpha_composite(P_, (x, y))
    return can
def s_pm10(t, w0, w1):
    can, m = side('g_pred', 900, 1250, t, w0, w1, 1.03); shade(can, 210, 0.55); can.alpha_composite(TOPSH)
    paint(can, t, ws('Blech'), [m(1190, 672), m(1560, 682), m(1560, 849), m(1190, 845)], 'BLECH', 150, CREAM, dur=0.4, mod=0.55, op=0.9)
    paint(can, t, ws('Farbe'), [m(1585, 683), m(1905, 692), m(1905, 852), m(1585, 849)], 'FARBE', 150, CREAM, dur=0.4, mod=0.55, op=0.9)
    title(can, t, w0 + 0.1, 'PANTHER ALS M10', TOP, 100, CREAM)
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
    sliced(can, t, ws('Telefonleitungen'), 'GEKAPPT', (CX, 760), 140)
    title(can, t, ws('kappten') + 0.05, 'TELEFONLEITUNGEN', 1330, 100, YEL, None, bold=1)
def o_column(can, t, w0, w1):
    title(can, t, ws('Kolonnen'), 'KOLONNEN', TOP, 120, CREAM)
    paint(can, t, ws('falsche'), [(190, 1150), (840, 1118), (930, 1295), (110, 1335)], 'FALSCHE RICHTUNG', 108, RED, dur=0.5, mod=0.35, op=0.95, glow=((245, 245, 240), 8, 0.4))
    if t > ws('schickten'):
        arrow(can, (760, 1000), (330, 860), eio((t - ws('schickten')) / 0.5), YEL, 14, 44)
    if t > ws('falsche') + 0.2:
        arrow(can, (330, 860), (820, 760), eio((t - ws('falsche') - 0.2) / 0.5), RED, 14, 44)
# 17: few got through: the disguised Panthers ended as wrecks in the snow; then the rumour on the map
def s_fb(t, w0, w1):
    can, m = side('g_fb', 700, 900, t, w0, w1, 1.04); shade(can, 220, 0.5); can.alpha_composite(TOPSH)
    title(can, t, ws('Nur', 50.4), 'NUR WENIGE', TOP, 120, CREAM)
    return can
def s_td(t, w0, w1):
    can, m = side('g_td', 500, 760, t, w0, w1, 1.04); shade(can, 220, 0.5); can.alpha_composite(TOPSH)
    title(can, t, w0 + 0.05, 'NUR WENIGE', TOP, 120, CREAM)
    title(can, t, ws('kamen', 51.3), 'KAMEN DURCH', 1330, 120, YEL, None, bold=1)
    return can
# rumour
MA = Map(5.95, 50.25, 2.7)
FRONT = [(6.25, 50.62), (6.27, 50.40), (6.14, 50.20), (6.04, 50.05), (6.13, 49.92), (6.42, 49.81)]
def s_rumor(t, w0, w1):
    can = BG('rumor', 0.0, 50, 1.6)(t, w0); z = lerp(1.0, 1.04, prog(t, w0, w1)); mp = MA.frame(z); mp.putalpha(165); can.alpha_composite(mp)
    p = lambda lo, la: MA.p(lo, la, z)
    see(can, lambda L: ImageDraw.Draw(L).line([p(*q) for q in FRONT], fill=RED + (255,), width=10, joint='curve'), 0.85)
    title(can, t, w0 + 0.2, 'FRONT 16.12.', p(6.55, 50.52)[1], 40, RED, None, 'bebas', min(p(6.55, 50.52)[0], 960))
    for nm, lo, la in (('LÜTTICH', 5.57, 50.63), ('MALMEDY', 6.03, 50.43), ('ST. VITH', 6.13, 50.28), ('BASTOGNE', 5.72, 50.0)):
        x, y = p(lo, la); dot(can, x, y, CREAM, 8); title(can, t, w0 + 0.2, nm, y - 42, 42, CREAM, None, 'bebas', min(max(x, 120), 960))
    t0 = w0 - 0.4
    for i, (a_, b_) in enumerate((((6.30, 50.50), (5.80, 50.48)), ((6.25, 50.30), (5.70, 50.28)), ((6.10, 50.10), (5.55, 50.12)), ((6.30, 49.95), (5.80, 49.92)))):
        ok = i == 1; u = eio((t - t0 - i * 0.12) / 0.8) * (1.0 if ok else 0.55)
        if u > 0:
            A, Bp = p(*a_), p(*b_); e = (lerp(A[0], Bp[0], u), lerp(A[1], Bp[1], u))
            dashed(can, [A, e], 1.0, YEL, 6, 18, 26)
            if not ok: ring(can, t, w0 + 0.15 + i * 0.08, e[0], e[1], RED, 22, True)
    if t > ws('Gerücht'):
        x, y = p(5.70, 50.28); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for j in range(5):
            u = ((t - ws('Gerücht')) * 0.55 + j / 5) % 1.0; r = 40 + 760 * u; d.ellipse((x - r, y - r, x + r, y + r), outline=YEL + (int(190 * (1 - u)),), width=6)
        can.alpha_composite(L)
    title(can, t, ws('Gerücht'), 'DAS GERÜCHT', TOP, 120, YEL, None, bold=1)
    title(can, t, ws('schneller'), 'SCHNELLER ALS SIE', 1330, 96, CREAM, None, bold=1)
    return can
# 18-19: trick questions at every crossing
def o_post(can, t, w0, w1):
    title(can, t, ws('Kreuzung'), 'AN JEDER KREUZUNG', TOP, 110, CREAM)
    asks(can, t, ws('Fangfragen'), 'FANGFRAGEN', 1300, 120, CREAM)
def o_gis(can, t, w0, w1):
    def pad(L):
        k = eout((t - w0) / 0.35); P_ = Image.new('RGBA', (840, 470), (236, 230, 212, 255)); d = ImageDraw.Draw(P_)
        for yy in range(70, 470, 58): d.line((30, yy, 810, yy), fill=(150, 170, 200, 255), width=2)
        d.line((90, 0, 90, 470), fill=(200, 90, 90, 255), width=2)
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
MP = Map(4.55, 49.8, 5.6)
ARD = [(5.25, 50.45), (5.95, 50.55), (6.35, 50.35), (6.45, 49.85), (5.95, 49.75), (5.35, 49.85)]   # Ardennes uplands across Belgium and Luxembourg
def s_paris(t, w0, w1):
    can = BG('paris', 0.0, 50, 1.6)(t, w0); z = lerp(1.0, 1.03, prog(t, w0, w1)); mp = MP.frame(z); mp.putalpha(170); can.alpha_composite(mp)
    p = lambda lo, la: MP.p(lo, la, z)
    for nm, lo, la in (('BELGIEN', 4.45, 50.62), ('FRANKREICH', 3.4, 49.35), ('DEUTSCHLAND', 6.75, 51.0), ('LUX.', 6.12, 49.55)):
        x, y = p(lo, la); title(can, t, w0 + 0.2, nm, y, 44 if nm != 'LUX.' else 36, (150, 160, 178), None, 'bebas', x)
    see(can, lambda L: poly_fill(L, [p(*q) for q in ARD], RED, 90), 1.0)
    xa, ya = p(5.9, 50.15); xp, yp = p(2.35, 48.86)
    title(can, t, w0 + 0.2, 'ARDENNEN', p(5.85, 50.62)[1] - 30, 50, RED, None, 'bebas', xa)
    dashed(can, [(xa, ya), (lerp(xa, xp, 0.5), lerp(ya, yp, 0.5) - 50), (xp + 22, yp - 8)], eio((t - ws('unterwegs')) / 1.0), YEL, 8, 22, 34)
    dot(can, xp, yp, CREAM, 10); title(can, t, w0 + 0.2, 'PARIS', yp + 50, 52, CREAM, None, 'bebas', max(xp, 110))
    if t > ws('Eisenhower'): ring(can, t, ws('Eisenhower'), xp, yp, RED, 40, False)
    hand(can, t, ws('töten') - 0.1, 'Eisenhower töten?', (CX, 1330), 104, YEL, 0.6)
    title(can, t, ws('behaupteten'), 'DIE BEHAUPTUNG', TOP, 110, CREAM)
    return can
# 22-23: Eisenhower, Christmas under guard
def s_ike(t, w0, w1):
    can = grade(fit('g_ike', t, w0, w1, 1.05)); shade(can, 230, 0.5)
    crossed(can, t, ws('Belegt'), 'BELEGT', 1290, 130, 'nicht')
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
    pwfield(can, t, ws('kannten'), 1250, ws('nicht', 81.8))
def s_court(t, w0, w1):
    can = BG('court', 0.0, 70, 1.4)(t, w0)
    l = [('MILITÄRGERICHT', 60, INK, ws('Militärgericht')), ('', 10, INK, 0), ('Urteil: Spionage', 48, INK, ws('verurteilte')), ('Tod durch Erschießen', 48, RED, ws('Spione'))]
    see(can, lambda L: sheet(L, t, w0 + 0.05, l, CX, 920, 860, 0.0), 0.9)
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
    verdict(can, t, ws('freigesprochen'), 'FREIGESPROCHEN', 1150, 110, YEL)
    cta(can, t, ws('1947') + 0.8)

ANCH = [
 (0.0, FV('hook', 0.0, o_hook, 1.05, 0.5), None),
 (ws('denn', 5.5) - 0.1, FV('road', 0.0, o_road, 1.05, 0.5), ('fade',)),
 (ws('Der', 10) - 0.1, s_plan, ('whip', 1)),
 (ws('Geführt') - 0.1, s_skp, ('fade',)),
 (ws('dem', 14.9) - 0.1, s_sk1, ('fade',)),
 (ws('Mussolini') - 0.1, s_muss, ('whip', -1)),
 (ws('Für', 20.3) - 0.1, FV('ardmap', 0.0, o_ardmap, 1.05, 0.5), ('fade',)),
 (ws('eine', 22.3) - 0.1, s_skt, ('fade',)),
 (ws('die', 23.4) - 0.1, FV('aim', 0.0, o_aim, 1.05, 0.5), ('whip', 1)),
 (ws('Doch', 26.3) - 0.1, s_vol, ('fade',)),
 (ws('und', 29.9) - 0.1, FV('convoy', 0.0, o_convoy, 1.04, 0.5), ('fade',)),
 (ws('Skorzeny', 32.9) - 0.4, s_got, ('fade',)),
 (ws('und', 35.6) - 0.1, FV('sherman', 0.0, o_sherman, 1.04, 0.5), ('whip', 1)),
 (ws('Die', 37.3) - 0.1, s_cafe, ('fade',)),
 (ws('mit', 38.5) - 0.1, s_pm10, ('fade',)),
 (ws('Am', 40.3) - 0.1, FV('barrage', 0.0, o_barrage, 1.03, 0.5), ('whip', -1)),
 (ws('Kleine') - 0.1, FV('jeep', 0.0, o_jeep, 1.04, 0.5), ('fade',)),
 (ws('drehten') - 0.1, FV('sign', 0.0, o_sign, 1.03, 0.5), ('fade',)),
 (ws('kappten') + 0.2, FV('pole', 0.0, o_pole, 1.03, 0.62), ('fade',)),
 (ws('und', 47.9) - 0.15, FV('column', 0.0, o_column, 1.04, 0.5), ('fade',)),
 (ws('Nur', 50.4) - 0.1, s_fb, ('whip', 1)),
 (ws('kamen', 51.3) - 0.15, s_td, ('fade',)),
 (ws('doch', 52.2) - 0.1, s_rumor, ('fade',)),
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
