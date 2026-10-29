
# ---------- scenes ----------
TOP = 330
def FV(k, a=0.0, ov=None, z1=1.06, fx=0.5, fy=0.5):
    return FL(k, a, 1.0, 1.0, z1, fx, fy, ov)
def o_hook(can, t, w0, w1, m=None):
    title(can, t, ws('Wüstenfuchs'), 'DER WÜSTENFUCHS', TOP, 120, CREAM)
    title(can, t, ws('Feind'), 'NICHT DER FEIND', 1250, 80, CREAM)
    title(can, t, ws('Regime'), 'SEIN EIGENES REGIME', 1350, 92, RED, None, bold=1)
def o_name(can, t, w0, w1, m=None):
    title(can, t, ws('Erwin'), 'ERWIN', 1295, 90, CREAM, None, bold=1)
    title(can, t, ws('Rommel', 6.8), 'ROMMEL', 1405, 140, YEL, None, bold=2)
def o_port(can, t, w0, w1, m=None):
    title(can, t, ws('12.'), '12. FEBRUAR 1941', TOP, 110, CREAM)
def o_crane(can, t, w0, w1, m=None):
    title(can, t, w0 + 0.05, '12. FEBRUAR 1941', TOP, 110, CREAM)
    title(can, t, ws('Tripolis'), 'TRIPOLIS', 1320, 130, YEL, None, bold=1)
ML = Map(21.5, 31.2, 19.0)
def s_libya(t, w0, w1):
    can = BG('tank1', 0.0, 40)(t, w0); z = lerp(1.0, 1.05, prog(t, w0, w1)); mp = ML.frame(z); mp.putalpha(140); can.alpha_composite(mp)
    p = lambda lo, la: ML.p(lo, la, z)
    for nm, lo, la in (('LIBYEN', 19.0, 28.6), ('ÄGYPTEN', 28.8, 27.6), ('MITTELMEER', 20.0, 34.2)):
        x, y = p(lo, la); title(can, t, w0 + 0.3, nm, y, 56, (150, 160, 178), None, 'bebas', x)
    xt, yt = p(13.19, 32.89); dot(can, xt, yt, YEL, 11); title(can, t, w0 + 0.2, 'TRIPOLIS', yt - 50, 50, CREAM, None, 'bebas', max(xt, 140))
    xa, ya = p(20.2, 30.6); xb, yb = p(25.1, 31.5)
    arrow(can, (xa, ya), (xb, yb), eio((t - ws('griff')) / 1.2), RED, 16, 46)
    if t > ws('Grenze') - 0.1: ring(can, t, ws('Grenze') - 0.1, xb, yb, YEL, 30, False)
    title(can, t, ws('Italiener'), 'NUR VERTEIDIGEN', TOP, 100, CREAM, ws('griff') - 0.2)
    title(can, t, ws('griff'), 'ER GREIFT AN', TOP, 110, YEL)
    return can
def o_storch(can, t, w0, w1, m=None):
    title(can, t, ws('vorne'), 'VON VORNE', TOP, 120, CREAM)
def s_storch(t, w0, w1):
    can, mp = photo_card('r49', (300, 120, 2400, 1700), t, w0, w1, 'walk', 0.0, 1.05, 830, 1000, 752, 70)
    title(can, t, w0 + 0.05, 'FIESELER STORCH', TOP - 40, 100, YEL)
    return can
def o_tob(can, t, w0, w1, m=None):
    title(can, t, ws('Tobruk', 22.3), 'TOBRUK', TOP, 140, CREAM)
    title(can, t, ws('fast', 23.6), 'FAST 8 MONATE', 1320, 100, YEL)
def o_opp(can, t, w0, w1, m=None):
    title(can, t, ws('Gegner'), 'SEINE GEGNER', TOP, 120, CREAM)
def s_auch(t, w0, w1):
    can = grade(fit('r44', t, w0, w1, 1.06)); dim(can, 70)
    title(can, t, ws('Claude'), 'CLAUDE AUCHINLECK', 300, 90, CREAM)
    title(can, t, ws('Claude') + 0.2, 'BRITISCHER OBERBEFEHLSHABER', 385, 50, YEL, None, 'bebas')
    l = [('AN ALLE KOMMANDEURE', 44, INK, ws('Kommandeuren')), ('', 14, INK, 0), ('Nicht mehr von "Rommel" sprechen,', 44, INK, ws('nicht', 31.7)),
         ('sondern von "den Deutschen".', 44, RED, ws('sondern', 33.3))]
    sheet(can, t, ws('schrieb') - 0.3, l, CX, 1180, 920, 0.0)
    return can
def o_jun(can, t, w0, w1, m=None):
    title(can, t, ws('Juni'), 'JUNI 1942', TOP, 120, CREAM)
    title(can, t, ws('fiel', 36.9), 'TOBRUK FÄLLT', 1320, 110, YEL, None, bold=1)
def s_marsch(t, w0, w1):
    can = grade(fit('r09', t, w0, w1, 1.06)); shade(can, 230, 0.5)
    title(can, t, ws('50'), 'MIT 50 JAHREN', 1180, 90, CREAM)
    title(can, t, ws('Generalfeldmarschall'), 'GENERALFELDMARSCHALL', 1320, 96, YEL, None, 'anton', CX, 900)
    return can
def o_ala(can, t, w0, w1, m=None):
    title(can, t, ws('El', 42.9), 'EL ALAMEIN', TOP, 140, CREAM)
    stamp(can, t, ws('scheiterte'), 'GESCHEITERT', (CX, 1320), 100, -6)
def s_hitler(t, w0, w1):
    can, m = side('r51', 0, 600, t, w0, w1, 1.04); shade(can, 210, 0.55); can.alpha_composite(TOPSH)
    title(can, t, ws('Sieg'), 'SIEG ODER TOD', 1320, 130, RED, None, bold=1)
    return can
def o_ret(can, t, w0, w1, m=None):
    title(can, t, w0 + 0.05, 'SIEG ODER TOD', TOP - 50, 90, (170, 160, 150))
    title(can, t, ws('zog'), 'RÜCKZUG', TOP + 60, 140, YEL, None, bold=1)
def s_wall(t, w0, w1):
    can, m = side('r36', 300, 700, t, w0, w1, 1.05); shade(can, 210, 0.55); can.alpha_composite(TOPSH)
    title(can, t, ws('1944', 48), '1944', TOP - 50, 130, CREAM)
    title(can, t, ws('Atlantikwall'), 'ATLANTIKWALL', TOP + 70, 110, YEL)
    if t >= ws('Millionen'): title(can, t, ws('Millionen'), 'MILLIONEN MINEN', 1330, 96, CREAM)
    return can
def s_spargel(t, w0, w1):
    can = BG('map1', 0.0, 80)(t, w0)
    clipping(can, t, w0 + 0.05, 'r45', (0, 0, 2752, 1536), (CX, 760), 960, -2)
    clipping(can, t, ws('Rommelspargel') - 0.1, 'r46', (0, 0, 2752, 1536), (CX + 40, 1060), 900, 4)
    title(can, t, w0 + 0.05, 'PFÄHLE IN DEN STRÄNDEN', TOP - 30, 76, CREAM)
    hand(can, t, ws('Rommelspargel'), 'Rommelspargel', (CX, 1420), 130, YEL, 0.7)
    return can
def o_lost(can, t, w0, w1, m=None):
    title(can, t, ws('Landung'), 'NACH DER LANDUNG', TOP, 100, CREAM)
    title(can, t, ws('verloren'), 'KRIEG VERLOREN', 1320, 120, RED, None, bold=1)
def s_july(t, w0, w1):
    can = grade(fit('r10', t, w0, w1, 1.06)); shade(can, 230, 0.5)
    title(can, t, ws('Attentat'), '20. JULI 1944', 1150, 110, CREAM)
    title(can, t, ws('Attentat') + 0.2, 'ATTENTAT AUF HITLER', 1260, 64, CREAM, None, 'bebas')
    stamp(can, t, ws('Verhören'), 'VERHÖRE', (CX, 1390), 96, -6)
    return can
def o_herr(can, t, w0, w1, m=None):
    title(can, t, ws('14.'), '14. OKTOBER 1944', TOP, 110, CREAM)
    title(can, t, ws('Herrlingen'), 'HERRLINGEN', 1320, 120, YEL, None, bold=1)
def s_choice(t, w0, w1):
    can = BG('pris2', 0.0, 130)(t, w0)
    title(can, t, ws('Wahl'), 'DIE WAHL', TOP, 130, CREAM)
    title(can, t, ws('Volksgerichtshof'), 'VOLKSGERICHTSHOF', 860, 110, CREAM, None, bold=1)
    title(can, t, ws('oder', 72.5), 'ODER', 990, 70, (170, 170, 170), None, 'bebas')
    title(can, t, ws('Gift'), 'GIFT', 1140, 200, RED, None, bold=2)
    return can
def s_family(t, w0, w1):
    can = grade(fit('r48', t, w0, w1, 1.05)); shade(can, 220, 0.5)
    title(can, t, ws('Frau'), 'LUCIE', 1260, 90, CREAM, None, 'anton', 760)
    title(can, t, ws('Sohn', 75.8), 'MANFRED, 15', 1260, 90, CREAM, None, 'anton', 300)
    title(can, t, ws('Wagen'), 'DER LETZTE ABSCHIED', 1380, 70, YEL)
    return can
def s_dead(t, w0, w1):
    can, m = side('r41', 700, 1000, t, w0, w1, 1.05); shade(can, 220, 0.55); can.alpha_composite(TOPSH)
    title(can, t, ws('tot'), 'TOT', TOP, 150, CREAM)
    stamp(can, t, ws('Verwundungen'), 'OFFIZIELL: VERWUNDUNG', (CX, 1320), 70, -5)
    return can
def s_wreath(t, w0, w1):
    can, m = side('r29', 900, 1100, t, w0, w1, 1.04); shade(can, 210, 0.55); can.alpha_composite(TOPSH)
    title(can, t, ws('Kranz'), 'HITLERS KRANZ', TOP, 120, CREAM)
    title(can, t, ws('Trauerfeier'), 'TRAUERFEIER IN ULM', 1320, 90, YEL)
    return can
def s_rund(t, w0, w1):
    can = grade(fit('r47', t, w0, w1, 1.05)); shade(can, 230, 0.45)
    title(can, t, w0 + 0.05, 'GERD VON RUNDSTEDT', 1120, 80, CREAM)
    hand(can, t, ws('Sein', 87), '"Sein Herz gehörte', (CX, 1260), 100, YEL, 0.7)
    hand(can, t, ws('Führer'), 'dem Führer."', (CX, 1370), 100, YEL, 0.5)
    return can
def s_end(t, w0, w1):
    can = grade(fit('r50', t, w0, w1, 1.05)); shade(can, 220, 0.5)
    title(can, t, ws('Wahrheit'), 'DIE WAHRHEIT', TOP, 120, YEL)
    title(can, t, ws('Manfred'), 'MANFRED ROMMEL', 1110, 100, CREAM)
    title(can, t, ws('Wahrheit') + 0.4, 'GANZE DOKU AUF DEM KANAL', 1250, 56, YEL, None, 'bebas')
    cta(can, t, ws('Wahrheit') + 0.6)
    return can

ANCH = [
 (0.0, FV('jeep', 0.0, o_hook), None),
 (ws('Sein', 5.8) - 0.1, FV('cam', 0.0, o_name, 1.08, 0.5, 0.4), ('whip', 1)),
 (ws('Am', 7.5) - 0.1, FV('port', 0.0, o_port), ('fade',)),
 (ws('landete') - 0.1, FV('crane', 2.0, o_crane), ('fade',)),
 (ws('Er', 11.6) - 0.1, s_libya, ('whip', -1)),
 (ws('Er', 18.8) - 0.1, FV('storch', 0.0, o_storch), ('fade',)),
 (ws('kleinen') - 0.1, s_storch, ('fade',)),
 (ws('Nur', 22.2) - 0.1, FV('gun', 0.0, o_tob), ('whip', 1)),
 (ws('Seine', 25.2) - 0.1, FV('rom1', 0.0, o_opp), ('fade',)),
 (ws('britische', 27.5) - 0.1, s_auch, ('fade',)),
 (ws('Im', 35) - 0.1, FV('pris', 0.0, o_jun), ('whip', -1)),
 (ws('Rommel', 38) - 0.1, s_marsch, ('fade',)),
 (ws('Wenige', 40.9) - 0.1, FV('dust', 0.0, o_ala), ('whip', 1)),
 (ws('Hitler', 43.9) - 0.1, s_hitler, ('fade',)),
 (ws('Rommel', 46.0) - 0.1, FV('cars', 0.0, o_ret), ('fade',)),
 (ws('1944', 48) - 0.1, s_wall, ('whip', -1)),
 (ws('und', 52.2) - 0.1, s_spargel, ('fade',)),
 (ws('Doch', 55.2) - 0.1, FV('car', 0.0, o_lost), ('fade',)),
 (ws('Nach', 59.8) - 0.1, s_july, ('fade',)),
 (ws('Am', 64.3) - 0.1, FV('meet', 0.0, o_herr), ('whip', 1)),
 (ws('Sie', 69.9) - 0.1, s_choice, ('fade',)),
 (ws('Rommel', 73.4) - 0.1, s_family, ('fade',)),
 (ws('Wenig', 77.6) - 0.1, s_dead, ('fade',)),
 (ws('Hitler', 81.7) - 0.1, s_wreath, ('fade',)),
 (ws('Generalfeldmarschall', 85) - 0.1, s_rund, ('fade',)),
 (ws('Die', 89.2) - 0.1, s_end, ('fade',))]
