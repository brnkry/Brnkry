
# ---------- graphics over a running film: the film blurred and darkened behind, graphics see-through on top ----------
def BG(k, a, rate=1.0, dimv=120, bl=2.2):
    def fn(t, w0):
        im = fat(k, a + max(0.0, t - w0) * rate)
        sm = im.resize((108, 192), Image.BILINEAR, box=_cover(im.size, 9 / 16)).filter(ImageFilter.GaussianBlur(bl)).resize((W, H), Image.BICUBIC)
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

# ---------- scenes ----------
TOP = 330
def s_hook(t, w0, w1):
    can = grade(fit('k04', t, w0, w1, 1.08)); shade(can, 230, 0.45)
    title(can, t, ws('siebzig'), 'FAST 70 JAHRE', 1180, 120, CREAM, None, bold=1)
    title(can, t, ws('namenlosen'), 'NAMENLOS', 1330, 150, YEL, None, bold=1)
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
    can = BG('ku_sol', 0.3, 0.8, 60, 1.6)(t, w0)
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
def o_ost(can, t, w0, w1, m=None):
    title(can, t, ws('Ostfront'), 'OSTFRONT', TOP, 130, CREAM)
MK = Map(26.0, 52.6, 30.0)
def s_kursk(t, w0, w1):
    can = BG('ku_t34', 0.2, 0.7, 40, 1.6)(t, w0); z = lerp(1.0, 1.08, prog(t, w0, w1)); mp = MK.frame(z); mp.putalpha(130); can.alpha_composite(mp)
    p = lambda lo, la: MK.p(lo, la, z)
    for nm, lo, la in (('BERLIN', 13.4, 52.52), ('MOSKAU', 37.62, 55.75)):
        x, y = p(lo, la); dot(can, x, y, GREY, 9); title(can, t, w0 + 0.25, nm, y + 48, 48, GREY, None, 'bebas', x)
    x, y = p(36.19, 51.73); dot(can, x, y, YEL, 12); ring(can, t, ws('Kursk', 20), x, y, RED, 34, False)
    title(can, t, ws('Kursk', 20), 'KURSK', y - 70, 70, YEL, None, 'bebas', x)
    title(can, t, ws('1943'), '1943', TOP, 140, CREAM)
    return can
def s_count(t, w0, w1):
    can = BG('ti', 12.0, 0.45, 80, 1.8)(t, w0)
    title(can, t, ws('Büchern'), 'IN VIELEN BÜCHERN', TOP, 96, CREAM)
    t0 = ws('168')
    if t >= t0:
        counter(can, t, t0, 0, 168, (CX, 720), 280, YEL, 1.1)
    ta = ws('126'); tb = ws('42', 29)
    for i, (lab, n, ts_) in enumerate((('ALS RICHTSCHÜTZE', 126, ta), ('ALS KOMMANDANT', 42, tb))):
        if t < ts_: continue
        y = 990 + i * 150; u = eio((t - ts_) / 0.6); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((160, y - 30, 920, y + 30), 10, fill=(10, 11, 14, 150)); d.rounded_rectangle((160, y - 30, 160 + 760 * n / 168 * u, y + 30), 10, fill=YEL + (220,))
        can.alpha_composite(L); title(can, t, ts_, f'{n}', y, 52, DARK if n > 60 else WHITE, None, 'anton', 200 + 760 * n / 168 * u - (60 if n > 60 else -50), 300)
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
    can = grade(fit('k09', t, w0, w1, 1.06)); shade(can, 220, 0.5)
    title(can, t, ws('Geschichten'), 'DIE LEGENDE', 1200, 110, CREAM)
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
    can = BG('kt', 7.0, 0.6, 50, 1.6)(t, w0); z = lerp(1.0, 1.06, prog(t, w0, w1)); mp = MS.frame(z); mp.putalpha(130); can.alpha_composite(mp)
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
    can = BG('dig', 19.0, 0.8, 70, 1.6)(t, w0); k = eout((t - w0 - 0.05) / 0.6); u = prog(t, w0, w1)
    if k > 0:
        wd = int(lerp(780, 880, u) * lerp(0.85, 1.0, k)); tg = TAG.resize((wd, int(TAG.height * wd / TAG.width)), Image.LANCZOS).rotate(lerp(-4, 2, u), expand=True, resample=Image.BICUBIC)
        if k < 1: tg.putalpha(tg.getchannel('A').point(lambda v: int(v * k)))
        sh = Image.new('RGBA', tg.size, (0, 0, 0, 0)); sh.putalpha(tg.getchannel('A').point(lambda v: int(v * 0.75)))
        x, y = int(CX - tg.width / 2), int(880 - tg.height / 2 + (1 - k) * 40)
        can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (x + 10, y + 24)); can.alpha_composite(tg, (x, y))
    title(can, t, ws('Erkennungsmarke'), 'ERKENNUNGSMARKE', 1330, 96, YEL)
    return can
def cta(can, t, t0):
    """small 'Kanntet ihr diese Geschichte?' card in the lower left, while the voice is still running"""
    if t < t0: return
    k = eout((t - t0) / 0.45); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, y0 = 70 - (1 - k) * 60, 1330; f1, f2 = oswald(46, 600), oswald(38, 500)
    s1, s2 = 'Kanntet ihr diese Geschichte?', 'Schreibt es in die Kommentare!'; wd = max(f1.getlength(s1), f2.getlength(s2)) + 140
    d.rounded_rectangle((x0, y0, x0 + wd, y0 + 140), 22, fill=(10, 11, 14, int(185 * k)), outline=YEL + (int(220 * k),), width=3)
    bx, by = x0 + 30, y0 + 38   # speech bubble
    d.rounded_rectangle((bx, by, bx + 66, by + 50), 12, fill=YEL + (int(255 * k),)); d.polygon([(bx + 14, by + 48), (bx + 30, by + 48), (bx + 10, by + 66)], fill=YEL + (int(255 * k),))
    for i in range(3): d.ellipse((bx + 15 + i * 15, by + 21, bx + 23 + i * 15, by + 29), fill=DARK + (int(255 * k),))
    d.text((x0 + 120, y0 + 46), s1, font=f1, fill=WHITE + (int(255 * k),), anchor='lm'); d.text((x0 + 120, y0 + 100), s2, font=f2, fill=YEL + (int(255 * k),), anchor='lm')
    can.alpha_composite(L)
def s_grave(t, w0, w1):
    can = grade(fit('k02', t, w0, w1, 1.06)); shade(can, 200, 0.55); can.alpha_composite(TOPSH)
    title(can, t, ws('2014'), 'NOVEMBER 2014', TOP, 110, CREAM)
    title(can, t, ws('Brünn'), 'SOLDATENFRIEDHOF BRÜNN', TOP + 110, 60, YEL, None, 'bebas')
    cta(can, t, ws('Soldatenfriedhof'))
    return can

ANCH = [
 (0.0, s_hook, None),
 (ws('hinter') - 0.1, FL('dig', 2.0, 1.0, 1.0, 1.08, 0.5, 0.5, o_wall), ('fade',)),
 (ws('Metallmarke') - 0.1, FL('dig', 15.0, 1.0, 1.05, 1.15, 0.5, 0.5, o_lens), ('fade',)),
 (ws('Sein', 7) - 0.1, s_name, ('whip', 1)),
 (ws('Er', 8.5) - 0.05, S_('k01', 1000, 1300, 1.05, o_wm), ('fade',)),
 (ws('erst', 10.5) - 0.1, s_career, ('fade',)),
 (ws('Tigers') - 0.15, FL('ti', 4.0, 1.0, 1.0, 1.08, 0.5, 0.5, o_tiger), ('whip', -1)),
 (ws('Mit', 17) - 0.1, S_('k05', 1050, 1300, 1.05, o_ost), ('fade',)),
 (ws('1943') - 0.1, s_kursk, ('fade',)),
 (ws('In', 21.5) - 0.1, s_count, ('whip', 1)),
 (ws('denn', 33.5) - 0.1, s_crew, ('fade',)),
 (ws('Auch', 37.3) - 0.1, s_legend, ('fade',)),
 (ws('Sicher') - 0.1, S_('k06', 100, 330, 1.05, o_gold), ('whip', -1)),
 (ws('Das', 46.3) - 0.1, FL('ku_tig', 4.8, 0.8, 1.0, 1.08, 0.35, 0.5, o_rk), ('fade',)),
 (ws('Berichten') - 0.1, S_('k07', 950, 1120, 1.05, o_rebel), ('fade',)),
 (ws('Ende', 59) - 0.1, FL('kt', 0.0, 1.0, 1.0, 1.06, 0.5, 0.5, o_kt), ('whip', 1)),
 (ws('Nach', 66) - 0.1, FL('ku_burn', 2.0, 1.0, 1.0, 1.08, 0.5, 0.5, o_burn), ('fade',)),
 (ws('Knispel', 69.5) - 0.1, s_mahren, ('fade',)),
 (ws('Erst', 76) - 0.1, FL('dig', 0.0, 0.9, 1.0, 1.06, 0.5, 0.5, o_2013), ('whip', -1)),
 (ws('Archäologen') - 0.1, FL('dig', 9.5, 1.0, 1.0, 1.08, 0.5, 0.5, o_16), ('fade',)),
 (ws('Bei', 81) - 0.1, s_tag, ('fade',)),
 (ws('Im', 84) - 0.1, s_grave, ('fade',))]
