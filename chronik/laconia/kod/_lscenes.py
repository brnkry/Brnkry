
# ================= The Laconia incident (short) scenes =================
def hline(can, t, parts, y, gap=22):
    """one handwritten line whose words appear one by one with the voice: parts = [(word, t0, colour, size)]"""
    ws_ = [caveat(sz, 650).getlength(w_) for w_, _, _, sz in parts]; x = CX - (sum(ws_) + gap * (len(parts) - 1)) / 2
    for (w_, t0, col, sz), wd in zip(parts, ws_):
        hand(can, t, t0, w_, (x + wd / 2, y), sz, col, 0.32); x += wd + gap
def typed(can, t, t0, s_, xy, size, col=CREAM, step=0.045, anchor='mm'):
    """typewriter line with a blinking cursor"""
    if t < t0: return
    n = min(len(s_), int((t - t0) / step) + 1); f = typew(size); cur = '_' if n < len(s_) and int(t * 5) % 2 == 0 else ''
    x = xy[0] - f.getlength(s_) / 2 if anchor == 'mm' else xy[0]
    shadowed(can, lambda d: d.text((x, xy[1]), s_[:n] + cur, font=f, fill=col + (255,), anchor='lm'))
def flag(can, t, t0, xy, size=150):
    """a white flag with a red cross, waving in"""
    if t < t0: return
    k = eout((t - t0) / 0.45); w_, h_ = int(size * 1.4), size; L = Image.new('RGBA', (w_ + 40, h_ + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pts = [(20 + i, 20 + 6 * math.sin(i / 22 + t * 5)) for i in range(0, w_ + 1, 4)]
    poly = pts + [(x, y + h_) for x, y in reversed(pts)]; d.polygon(poly, fill=(245, 245, 240, 255))
    cw = h_ * 0.22; cx, cy = 20 + w_ / 2, 20 + h_ / 2 + 6 * math.sin((w_ / 2) / 22 + t * 5)
    d.rectangle((cx - cw / 2, cy - h_ * 0.38, cx + cw / 2, cy + h_ * 0.38), fill=(200, 30, 36, 255)); d.rectangle((cx - h_ * 0.38, cy - cw / 2, cx + h_ * 0.38, cy + cw / 2), fill=(200, 30, 36, 255))
    L = L.resize((max(1, int(L.width * k)), max(1, int(L.height * k))), Image.BICUBIC)
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.6)))
    x, y = int(xy[0] - L.width / 2), int(xy[1] - L.height / 2); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (x + 6, y + 10)); can.alpha_composite(L, (x, y))
def CARD(k, a=0.0, ov=None, z1=1.06, fx=0.5, fy=0.5, py=PY):
    """a low-resolution archive film in the cream-edged panel over a blurred copy of itself"""
    def fn(t, w0, w1):
        can = card(fat(k, a + max(0.0, t - w0)), t, w0, w1, 1.0, z1, fx, fy, 0.12, py)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
def SIDE(n, sxa, sxb, ov=None, z1=1.04, sh=210):
    def fn(t, w0, w1):
        can, m = side(n, sxa, sxb, t, w0, w1, z1); shade(can, sh, 0.55); can.alpha_composite(TOPSH)
        if ov: ov(can, t, w0, w1, m)
        return can
    return fn

# 0: the hook, written beside Hartenstein as it is spoken (no captions here)
def s_hook(t, w0, w1):
    """Hartenstein on the left, the opening sentence written word by word in the space beside him"""
    im = src('l_8576'); z = lerp(1.0, 1.04, prog(t, w0, w1)); h_ = int(H * 1.08 * z); w_ = int(im.width * h_ / im.height)
    can = Image.new('RGBA', (W, H), (14, 13, 12, 255)); P_ = grade(im.resize((w_, h_), Image.BICUBIC).convert('RGBA'))
    can.alpha_composite(P_, (int(330 - 992 * h_ / im.height), int(-60 * z)))   # his face (source x 992) sits at screen x 330
    g = np.clip((np.arange(W) - 420) / 260, 0, 1) ** 1.2 * 225; L = Image.new('RGBA', (W, H), (10, 10, 12, 0)); L.putalpha(Image.fromarray(np.repeat(g.astype(np.uint8)[None, :], H, 0))); can.alpha_composite(L)
    shade(can, 200, 0.62)
    X = 700   # column 480..910: clear of the like/comment buttons on the right
    for s_, w_t, col, sz, y in (('Er versenkte', ws('Er'), CREAM, 80, 430), ('ein Schiff,', ws('ein', 0.5), CREAM, 80, 530), ('rettete danach', ws('rettete'), CREAM, 70, 650),
                                ('Hunderte', ws('Hunderte'), YEL, 112, 770), ('Schiffbrüchige', ws('Schiffbrüchige', 2.5), CREAM, 66, 885), ('und wurde dafür', ws('und', 3.3), CREAM, 64, 995),
                                ('bombardiert.', ws('bombardiert'), RED, 96, 1110)):
        hand(can, t, w_t, s_, (X, y), sz, col, 0.4 if len(s_) < 12 else 0.55)
    return can
# 1: the map, U 156 off West Africa
MA = Map(-10.5, 2.5, 34.0)
SINK, FREETOWN, ASC, DAKAR = (-11.63, -5.08), (-13.23, 8.48), (-14.40, -7.93), (-17.45, 14.69)
def s_map1(t, w0, w1):
    can = BG('gl1', 0.0, 60, 1.6)(t, w0); z = lerp(1.0, 1.04, prog(t, w0, w1)); mp = MA.frame(z); mp.putalpha(175); can.alpha_composite(mp)
    p = lambda lo, la: MA.p(lo, la, z)
    title(can, t, w0 + 0.2, 'ATLANTIK', p(-20, 0)[1], 50, (150, 160, 178), None, 'bebas', p(-20, 0)[0])
    title(can, t, ws('Küste') - 0.2, 'WESTAFRIKA', p(2, 9)[1], 54, CREAM, None, 'bebas', min(p(2, 9)[0], 930))
    x, y = p(*FREETOWN); dot(can, x, y, CREAM, 8); title(can, t, w0 + 0.3, 'FREETOWN', y - 42, 42, CREAM, None, 'bebas', max(x, 150))
    x, y = p(*ASC); dot(can, x, y, CREAM, 8); title(can, t, w0 + 0.3, 'ASCENSION', y + 46, 42, CREAM, None, 'bebas', max(x, 150))
    x, y = p(*SINK)
    if t > ws('U', 7.5): ring(can, t, ws('U', 7.5), x, y, YEL, 26, False); title(can, t, ws('U', 7.5), 'U 156', y - 70, 64, YEL, None, 'anton', min(max(x + 60, 200), 900))
    ititle(can, t, ws('September') - 0.1, 'SEPTEMBER 1942', TOP, 96, CREAM)
    return can
# 2: the night attack
def o_torp(can, t, w0, w1):
    ititle(can, t, ws('12.'), '12. SEPTEMBER 1942', TOP, 90, CREAM)
    hand(can, t, ws('Werner'), 'Werner Hartenstein', (CX, 1300), 108, YEL, 0.6)
    title(can, t, ws('Kommandant') , 'KOMMANDANT VON U 156', 1395, 52, CREAM, None, 'bebas')
def s_laconia(t, w0, w1):
    can, m = side('l_img', 600, 800, t, w0, w1, 1.03); shade(can, 200, 0.6); can.alpha_composite(TOPSH)
    paint(can, t, ws('Laconia') - 0.05, [m(860, 1075), m(1560, 1075), m(1600, 1200), m(830, 1200)], 'LACONIA', 160, CREAM, dur=0.5, mod=0.3, op=0.9, glow=((8, 9, 12), 8, 0.5))
    title(can, t, ws('britische', 15.2), 'BRITISCHES TRUPPENTRANSPORTSCHIFF', TOP, 64, CREAM, None, 'bebas', CX, 900)
    return can
# 3: who was on board
def o_pax(can, t, w0, w1):
    popnum(can, t, ws('2.700'), 0, 2700, 280, 170, YEL, 0.9)
    hand(can, t, ws('Menschen', 20), 'Menschen an Bord', (CX, 1340), 100, CREAM, 0.5)
def s_list(t, w0, w1):
    can = BG('women', 0.0, 130, 1.8)(t, w0)
    title(can, t, w0 + 0.05, '2.700 MENSCHEN', TOP, 96, YEL)
    for (s_, w_, y) in (('britische Soldaten', ws('Soldaten', 21), 560), ('Zivilisten, Frauen und Kinder', ws('Zivilisten'), 680), ('polnische Wachsoldaten', ws('polnische'), 800)):
        hand(can, t, w_, s_, (CX, y), 86, CREAM, 0.5)
    popnum(can, t, ws('1.800'), 0, 1800, 1020, 200, YEL, 0.9)
    ititle(can, t, ws('italienische', 26.5), 'ITALIENISCHE KRIEGSGEFANGENE', 1170, 70, YEL)
    return can
# 4: surfacing, the cries for help
def o_esurf(can, t, w0, w1):
    ititle(can, t, ws('auftauchte') - 0.1, 'U 156 TAUCHT AUF', TOP, 96, CREAM)
def o_side(can, t, w0, w1):
    title(can, t, ws('Wasser', 32), 'AUS DEM WASSER', 300, 90, CREAM)
def o_water(can, t, w0, w1):
    title(can, t, w0 + 0.05, 'AUS DEM WASSER', 300, 90, CREAM)
    hand(can, t, ws('Hilferufe'), '„Aiuto! Aiuto!“', (CX, 1330), 130, YEL, 0.6)
    title(can, t, ws('Italienisch') - 0.1, 'HILFERUFE AUF ITALIENISCH', 1440, 52, CREAM, None, 'bebas')
# 5: the decision to rescue
def s_hart(t, w0, w1):
    can, m = side('l_hart2', 500, 760, t, w0, w1, 1.04); shade(can, 230, 0.5); can.alpha_composite(TOPSH)
    x, y = m(860, 700)
    if t > ws('Hartenstein', 34.5): arrow_at(can, t, ws('Hartenstein', 34.5), (x, y - 40), (x + 40, y - 260), YEL, 10, 36)
    hand(can, t, ws('Hartenstein', 34.5), 'Hartenstein', (min(x + 120, 860), y - 320), 92, YEL, 0.45)
    hand(can, t, ws('Verbündeten'), 'Verbündete!', (CX, 1290), 110, CREAM, 0.45)
    underlined(can, t, ws('Rettung'), 'DIE RETTUNG', 1410, 100, YEL, RED)
    return can
def o_climb(can, t, w0, w1, m):
    pass
def o_deck(can, t, w0, w1, m):
    x, y = m(1500, 1000)
    hand(can, t, ws('voller') - 0.1, 'voller Menschen', (CX, 760), 116, YEL, 0.5)
    if t > ws('voller'): arrow_at(can, t, ws('voller'), (x, y), (CX + 60, 830), YEL, 12, 40)
def o_sen(can, t, w0, w1, m):
    x, y = m(1820, 560)
    if t > ws('Rettungsboote', 44.2): arrow_at(can, t, ws('Rettungsboote', 44.2), (x, y + 20), (x + 60, y + 360), YEL, 12, 40)
    hand(can, t, ws('Schlepptau') - 0.2, 'im Schlepptau', (min(x + 40, 800), y + 450), 104, YEL, 0.5)
# 6: the open radio message in English (the wording from Hartenstein's signal of 13 September 1942)
def s_radio(t, w0, w1):
    can = BG('radiobg', 0.0, 100, 1.6)(t, w0)
    ititle(can, t, ws('offen'), 'OFFEN AUF ENGLISCH', TOP, 96, CREAM)
    k = eout((t - w0) / 0.35); P_ = Image.new('RGBA', (900, 640), (232, 226, 210, int(235 * k))); d = ImageDraw.Draw(P_)
    d.rectangle((0, 0, 899, 639), outline=(150, 135, 105, int(255 * k)), width=3); d.text((30, 30), 'FUNKSPRUCH  U 156  13.9.1942', font=typew(30), fill=(120, 40, 40, int(255 * k)))
    can.alpha_composite(P_, (90, 560))
    lines = [('IF ANY SHIP WILL ASSIST THE', ws('Er', 47.7)), ('SHIP-WRECKED LACONIA CREW,', ws('Schiff', 48.4)), ('I WILL NOT ATTACK HER', ws('angreifen')),
             ('PROVIDING I AM NOT BEING', ws('solange')), ('ATTACKED BY SHIP OR AIR FORCES.', ws('angegriffen'))]
    for i, (s_, t0) in enumerate(lines):
        if t < t0: continue
        n = min(len(s_), int((t - t0) / 0.02) + 1); f = typew(44); col = RED if 'NOT ATTACK' in s_ else INK
        ImageDraw.Draw(can).text((130, 680 + i * 92), s_[:n], font=f, fill=col + (255,))
    return can
# 7: the other boats, the Italian submarine
def s_doen(t, w0, w1):
    can = grade(fit('l_doenitz', t, w0, w1, 1.05)); shade(can, 230, 0.5)
    title(can, t, w0 + 0.05, 'KARL DÖNITZ', 1190, 100, CREAM, None, bold=1)
    ititle(can, t, ws('weitere'), 'SCHICKT U 506 UND U 507', 1310, 70, YEL)
    return can
def o_surv(can, t, w0, w1, m):
    x, y = m(1040, 400); arrow_at(can, t, w0 + 0.2, (x, y - 30), (x, y - 230), YEL, 10, 34); hand(can, t, w0 + 0.3, 'U 507', (x, y - 290), 96, YEL, 0.4)
    ititle(can, t, ws('italienisches'), '+ CAPPELLINI (ITALIEN)', 1330, 72, CREAM)
# 8: 16 September, the red cross flag, the way to the French ships
def o_tow(can, t, w0, w1):
    ititle(can, t, ws('16.'), '16. SEPTEMBER', TOP, 100, CREAM)
def s_flag(t, w0, w1):
    can = BG('gl1', 12.0, 90, 1.8)(t, w0)
    flag(can, t, w0 + 0.05, (CX, 820), 220)
    hand(can, t, ws('Rotkreuzflagge') + 0.1, 'Rotkreuzflagge', (CX, 1130), 120, CREAM, 0.5)
    hand(can, t, ws('Brücke'), 'auf der Brücke', (CX, 1250), 96, YEL, 0.4)
    return can
def s_map2(t, w0, w1):
    can = BG('gl1', 6.0, 60, 1.6)(t, w0); z = lerp(1.0, 1.03, prog(t, w0, w1)); mp = MA.frame(z); mp.putalpha(175); can.alpha_composite(mp)
    p = lambda lo, la: MA.p(lo, la, z)
    x, y = p(*DAKAR); dot(can, x, y, CREAM, 8); title(can, t, w0 + 0.2, 'DAKAR', y - 42, 42, CREAM, None, 'bebas', max(x, 150))
    meet = p(-12.0, 0.5); us = p(*SINK)
    dashed(can, [p(*DAKAR), p(-15.5, 8.0), meet], eio((t - w0) / 2.4), CREAM, 7, 20, 30)
    dashed(can, [us, meet], eio((t - w0 - 0.4) / 1.6), YEL, 7, 20, 30)
    flag(can, t, w0 + 0.2, (us[0] + 70, us[1] + 40), 56)
    title(can, t, ws('französischen'), 'FRANZÖSISCHE SCHIFFE', p(-21, 11)[1], 54, CREAM, None, 'bebas', 300)
    ititle(can, t, ws('Überlebenden', 65.5), 'ÜBERGABE DER ÜBERLEBENDEN', TOP, 70, YEL)
    return can
# 9: the B-24, the order from Ascension, the bomb
def o_b24fly(can, t, w0, w1):
    ititle(can, t, ws('amerikanischer'), 'AMERIKANISCHER BOMBER', TOP, 84, CREAM)
def o_b24(can, t, w0, w1, m):
    ititle(can, t, ws('B-24'), 'B-24 LIBERATOR', 1330, 110, YEL)
def o_asc(can, t, w0, w1, m):
    paint(can, t, ws('Ascension') - 0.05, [m(780, 1120), m(1480, 1100), m(1520, 1250), m(750, 1275)], 'ASCENSION', 130, CREAM, dur=0.5, mod=0.4, op=0.9)
    if t > ws('Befehl', 74.8):
        u = eout((t - ws('Befehl', 74.8)) / 0.25); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((160, 600 - 90 * u, 920, 600 + 90 * u), 14, fill=(232, 226, 210, int(235 * u))); can.alpha_composite(L)
        typed(can, t, ws('Befehl', 74.8) + 0.2, 'BEFEHL: "SINK SUB"', (CX, 600), 62, RED, 0.05)
def o_b24top(can, t, w0, w1):
    hand(can, t, ws('Bombe', 76), 'eine Bombe', (CX, 1330), 116, CREAM, 0.45)
def o_boom(can, t, w0, w1):
    hand(can, t, ws('Dutzende'), 'Dutzende starben', (CX, 1330), 116, RED, 0.6)
def o_uair(can, t, w0, w1):
    hand(can, t, ws('Wasser', 82.8) - 0.2, 'zurück ins Wasser', (CX, 1330), 108, YEL, 0.55)
def o_wdive(can, t, w0, w1):
    ititle(can, t, w0 + 0.02, 'ABGETAUCHT', 1330, 110, CREAM)
# 10: the French ships, the dead
def o_gl2(can, t, w0, w1):
    ititle(can, t, ws('nächsten'), '17. SEPTEMBER', TOP, 100, CREAM)
    hand(can, t, ws('Kriegsschiffe') - 0.2, 'französische Kriegsschiffe', (CX, 1330), 96, YEL, 0.6)
def o_gloire(can, t, w0, w1, m):
    ititle(can, t, w0 + 0.05, 'KREUZER GLOIRE', TOP, 100, CREAM)
    hand(can, t, ws('Überlebenden', 88), 'die meisten Überlebenden', (CX, 1330), 92, YEL, 0.6)
def s_dead(t, w0, w1):
    can = BG('sea', 0.0, 110, 1.6)(t, w0)
    hand(can, t, ws('mehr', 90.5), 'mehr als', (CX, 720), 100, CREAM, 0.4)
    popnum(can, t, ws('1.600'), 0, 1600, 900, 230, RED, 1.0)
    title(can, t, ws('Menschen', 92), 'TOTE', 1060, 90, CREAM, None, bold=1)
    hand(can, t, ws('italienische', 94.3), 'die meisten: italienische Gefangene', (CX, 1230), 82, YEL, 0.7)
    return can
# 11: the Laconia order, Nuremberg
def s_order(t, w0, w1):
    can = grade(fit('l_2279', t, w0, w1, 1.05)); shade(can, 250, 0.4)
    ititle(can, t, ws('Laconia-Befehl'), 'LACONIA-BEFEHL', 1000, 110, YEL)
    typed(can, t, ws('Laconia-Befehl') + 0.3, '17. SEPTEMBER 1942', (CX, 1100), 44, CREAM, 0.04)
    hand(can, t, ws('Schiffbrüchige', 99.9), 'Schiffbrüchige', (CX, 1215), 96, CREAM, 0.45)
    sliced(can, t, ws('retten', 100.6), 'RETTEN', (CX, 1350), 120, RED)
    return can
def o_nbg(can, t, w0, w1, m):
    ititle(can, t, ws('Nürnberg'), 'NÜRNBERG 1946', TOP, 100, CREAM)
    verdict(can, t, ws('erwiesen'), 'NICHT ERWIESEN', 1400, 110, YEL)
# 12: the end of U 156
def o_crew(can, t, w0, w1):
    hand(can, t, w0 + 0.05, 'Werner Hartenstein', (CX, 1310), 108, YEL, 0.55)
    ititle(can, t, w0 + 0.45, '1908 - 1943', 1410, 64, CREAM)
def o_hit(can, t, w0, w1, m):
    ititle(can, t, ws('März', 112.5), '8. MÄRZ 1943', TOP, 100, CREAM)
    hand(can, t, ws('Flugzeug'), 'ein amerikanisches Flugzeug', (CX, 1330), 92, YEL, 0.6)
def o_swirl(can, t, w0, w1, m):
    title(can, t, w0 + 0.1, 'U 156', 1330, 130, YEL, None, bold=2)
def o_raft(can, t, w0, w1, m):
    hand(can, t, ws('östlich'), 'östlich von Barbados', (CX, 1330), 100, CREAM, 0.6)
def s_end(t, w0, w1):
    can, m = side('l_16794972', 700, 900, t, w0, w1, 1.04); shade(can, 200, 0.55); can.alpha_composite(TOPSH)
    verdict(can, t, ws('gesamte') - 0.1, 'KEINE ÜBERLEBENDEN', 820, 100, CREAM)
    cta(can, t, ws('gesamte') + 0.3)
    return can

NOCAP = [(0.0, ws('Im') - 0.06)]
ANCH = [
 (0.0, s_hook, None),
 (ws('Im') - 0.1, s_map1, ('fade',)),
 (ws('Am', 10.9) - 0.1, FV('torp', 0.6, o_torp, 1.04, 0.5), ('whip', 1)),
 (ws('das', 15.2) - 0.1, s_laconia, ('fade',)),
 (ws('An', 17.9) - 0.1, CARD('pax', 0.0, o_pax), ('fade',)),
 (ws('britische', 20.7) - 0.1, s_list, ('fade',)),
 (ws('Als') - 0.1, FV('esurf', 0.0, o_esurf, 1.04, 0.5), ('whip', -1)),
 (ws('hörte') - 0.1, CARD('side', 0.0, o_side), ('fade',)),
 (ws('Hilferufe') - 0.3, CARD('water', 0.0, o_water), ('fade',)),
 (ws('Hartenstein', 34.5) - 0.1, s_hart, ('fade',)),
 (ws('Er', 40.2) - 0.1, SIDE('l_220963', 900, 1150, o_climb), ('fade',)),
 (ws('bis', 41.9) - 0.1, SIDE('l_hss', 800, 1200, o_deck), ('fade',)),
 (ws('und', 43.7) - 0.1, SIDE('l_sen', 900, 1150, o_sen), ('fade',)),
 (ws('Dann') - 0.1, s_radio, ('whip', 1)),
 (ws('Dönitz', 53) - 0.1, s_doen, ('fade',)),
 (ws('und', 55) - 0.1, SIDE('l_survivors', 500, 800, o_surv), ('fade',)),
 (ws('Am', 57.7) - 0.1, CARD('tow', 0.0, o_tow), ('whip', -1)),
 (ws('großen') - 0.3, s_flag, ('fade',)),
 (ws('französischen', 63.5) - 0.1, s_map2, ('fade',)),
 (ws('Da', 67) - 0.1, CARD('b24fly', 0.0, o_b24fly), ('whip', 1)),
 (ws('vom') - 0.1, SIDE('l_b24', 500, 800, o_b24), ('fade',)),
 (ws('Die', 71.4) - 0.1, SIDE('l_ascension', 640, 720, o_asc), ('fade',)),
 (ws('Eine', 76) - 0.1, CARD('b24top', 0.0, o_b24top), ('whip', -1)),
 (ws('Dutzende') - 0.1, CARD('boom', 0.0, o_boom), ('fade',)),
 (ws('Hartenstein', 80.6) - 0.1, CARD('uair', 0.0, o_uair), ('fade',)),
 (ws('und', 83.9) - 0.1, CARD('wdive', 0.0, o_wdive), ('fade',)),
 (ws('Am', 84.9) - 0.1, CARD('gl2', 0.0, o_gl2), ('whip', 1)),
 (ws('meisten', 87.5) - 0.1, SIDE('l_img2', 500, 800, o_gloire), ('fade',)),
 (ws('Trotzdem') - 0.1, s_dead, ('fade',)),
 (ws('Dönitz', 95.9) - 0.1, s_order, ('whip', -1)),
 (ws('Nach', 101.2) - 0.1, SIDE('l_nuremberg', 400, 900, o_nbg, 1.03, 245), ('fade',)),
 (ws('Hartenstein', 110.2) - 0.1, CARD('crew', 0.0, o_crew), ('fade',)),
 (ws('Im', 112.3) - 0.1, SIDE('l_u156hit', 500, 900, o_hit), ('whip', 1)),
 (ws('U', 116.4) - 0.1, SIDE('l_16794965', 600, 800, o_swirl), ('fade',)),
 (ws('östlich') - 0.1, SIDE('l_16794967', 700, 900, o_raft), ('fade',)),
 (ws('und', 119.6) - 0.1, s_end, ('fade',))]
