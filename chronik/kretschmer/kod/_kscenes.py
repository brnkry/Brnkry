
# ================= Otto Kretschmer (short) scenes =================
# the archive close-up of Kretschmer (a screen recording): the Knight's Cross centre moves with him and is blurred on every frame,
# his cap badge at the top edge is blurred as a band; the other officers on the right stay outside the 9:16 slice (fx below)
def _kclose_spots(i):
    k = [(1, 490, 980), (23, 490, 1000), (46, 380, 980)]
    for (a, xa, ya), (b, xb, yb) in zip(k, k[1:]):
        if a <= i <= b: u = (i - a) / (b - a); return [(lerp(xa, xb, u), lerp(ya, yb, u), 80), (450, 30, 150), (570, 30, 150)]
    return [(380, 980, 80), (450, 30, 150), (570, 30, 150)]
_ff0 = ff
@functools.lru_cache(maxsize=24)
def ff(k, i):
    im = _ff0(k, i)
    if k == 'kclose':
        im = im.copy(); i = max(1, min(SEG[k], i))
        for x, y, d in _kclose_spots(i): _soft(im, x, y, d)
    return im

def counter(can, t, t0, a, b, y, size, col=YEL, dur=0.9, fmt='{:,}', x=CX):
    """a number counting up, straight, with the channel shadow"""
    if t < t0: return
    v = int(round(lerp(a, b, eout((t - t0) / dur)))); s_ = fmt.format(v).replace(',', '.')
    title(can, t, t0, s_, y, size, col, None, 'anton', x, 900, 1)

# 0-2: the hook (the opening photo of the first Kretschmer short), his name on the archive film, the top tonnage
def s_hook(t, w0, w1):
    can = grade(fit('k_img7', t, w0, w1, 1.06)); shade(can, 230, 0.5)
    title(can, t, ws('Ein'), 'EIN TORPEDO,', 1200, 110, CREAM, None, bold=1)
    title(can, t, ws('ein', 0.6), 'EIN SCHIFF.', 1330, 140, YEL, None, bold=2)
    return can
def o_name(can, t, w0, w1):
    title(can, t, ws('Otto'), 'OTTO', 1270, 90, CREAM, None, bold=1)
    title(can, t, ws('Kretschmer'), 'KRETSCHMER', 1385, 140, YEL, None, bold=2)
def o_bow(can, t, w0, w1):
    title(can, t, ws('erfolgreichsten'), 'DER ERFOLGREICHSTE', TOP, 96, CREAM)
    title(can, t, ws('U-Boot-Kommandanten'), 'U-BOOT-KOMMANDANT', TOP + 110, 96, YEL, None, bold=1)
def s_vorbei(t, w0, w1):
    can = grade(fit('k_img5', t, w0, w1, 1.05)); shade(can, 230, 0.5)
    title(can, t, ws('schon', 10), 'SCHON IM MÄRZ 1941', 1190, 90, CREAM, None, bold=1)
    sliced(can, t, ws('vorbei'), 'VORBEI', (CX, 1330), 140, YEL)
    return can
# 3: U 99 and the night attacks inside the convoy columns
def s_u99(t, w0, w1):
    can = grade(fit('k_u99', t, w0, w1, 1.05)); shade(can, 220, 0.5)
    pt = lambda x, y: fitpt('k_u99', t, w0, w1, 1.05, x, y)
    paint(can, t, ws('99', 13.3), [pt(700, 440), pt(985, 425), pt(985, 640), pt(700, 655)], 'U 99', 120, CREAM, dur=0.35, mod=0.5, op=0.9)
    return can
def s_convoy(t, w0, w1):
    can = BG('nightbg', 0.0, 90, 2.0)(t, w0)
    def draw(L):
        cols = [190, 380, 700, 890]; sp = 230; off = (t - w0) * 40
        for c in cols:
            for r in range(-1, 9):
                y = 520 + r * sp + off % sp
                if 430 < y < 1230: ship(L, c, y, -math.pi / 2, 72, CREAM)
        u = eio((t - ws('aufgetaucht')) / 2.2)
        if t > ws('aufgetaucht'):
            x = 540; y = lerp(1300, 820, u)
            d = ImageDraw.Draw(L); d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=YEL + (255,))
            for j in range(3):
                uu = ((t - ws('aufgetaucht')) * 0.8 + j / 3) % 1.0; r = 18 + 50 * uu; d.ellipse((x - r, y - r, x + r, y + r), outline=YEL + (int(180 * (1 - uu)),), width=4)
    see(can, draw, 0.85)
    title(can, t, ws('nachts'), 'NACHTS', TOP, 120, CREAM)
    title(can, t, ws('aufgetaucht'), 'AUFGETAUCHT', TOP + 115, 90, YEL, None, bold=1)
    return can
# 4: one torpedo, one ship
def o_peri(can, t, w0, w1):
    pass   # the film speaks for itself here
def o_cross(can, t, w0, w1):
    title(can, t, ws('kam', 23), 'SO NAH WIE MÖGLICH', 1330, 96, YEL, None, bold=1)
def o_flash(can, t, w0, w1):
    underlined(can, t, ws('einziger'), 'EIN SCHUSS', 1330, 130, YEL, RED)
# 5: the silent Otto
def o_radio(can, t, w0, w1):
    pass   # the film speaks for itself here
def s_silent(t, w0, w1):
    can, m = side('k_ba_recolored', 200, 420, t, w0, w1, 1.04); shade(can, 230, 0.5); can.alpha_composite(TOPSH)
    title(can, t, ws('nannte'), 'DER SCHWEIGSAME', 1200, 100, CREAM, None, bold=1)
    title(can, t, ws('Otto', 31), 'OTTO', 1330, 160, YEL, None, bold=2)
    return can
# 6: SC 7, seven ships in one night
def o_sc7(can, t, w0, w1):
    sky(can, t, ws('Geleitzugs', 36), 'GELEITZUG SC 7', CX, 640, 96, CREAM, dur=0.5)
    t0 = ws('sieben', 35.5)
    if t > t0:
        def row(L):
            for i in range(7):
                if t > t0 + i * 0.12:
                    k = eout((t - t0 - i * 0.12) / 0.25); x = 150 + i * 130; ship(L, x, 1180 + (1 - k) * 30, 0, 66, RED if t > t0 + 0.9 + i * 0.08 else CREAM)
        see(can, row, 0.95)
        title(can, t, t0, '7 SCHIFFE IN EINER NACHT', 1330, 84, YEL, None, bold=1)
# 7: the armed merchant cruisers Laurentic and Patroclus
def o_smoke(can, t, w0, w1):
    title(can, t, ws('britischen', 41), 'ZWEI BRITISCHE HILFSKREUZER', 1330, 76, YEL, None, bold=1)
def s_ships(t, w0, w1):
    can = Image.new('RGBA', (W, H), (8, 9, 11, 255)); z = lerp(1.0, 1.04, prog(t, w0, w1))
    for n, y0, box, q, nm, tw in (('k_laurentic', 300, (60, 520, 2340, 1560), [(1000, 1015), (1880, 1015), (1880, 1150), (1000, 1150)], 'LAURENTIC', ws('Laurentic')),
                                  ('k_patroclus', 980, (80, 380, 2460, 1520), [(780, 1110), (1900, 1100), (1900, 1250), (780, 1260)], 'PATROCLUS', ws('Patroclus'))):
        im = src(n); bw, bh = box[2] - box[0], box[3] - box[1]; cw, ch = bw / z, bh / z; x0 = box[0] + (bw - cw) / 2; y0b = box[1] + (bh - ch) / 2
        ph = int(W * bh / bw); P_ = grade(im.resize((W, ph), Image.BICUBIC, box=(x0, y0b, x0 + cw, y0b + ch)).convert('RGBA'), 0.08, 0.95)
        sx, sy = W / cw, ph / ch; mp = lambda X, Y: ((X - x0) * sx, (Y - y0b) * sy)
        paint(P_, t, tw, [mp(*p) for p in q], nm, 120, CREAM, dur=0.4, mod=0.4, op=0.92, glow=None)
        can.alpha_composite(P_, (0, y0))
    title(can, t, w0 + 0.05, 'IN EINER NACHT', 880, 80, YEL, None, bold=1)
    return can
# 8: the total, and the dead
def s_total(t, w0, w1):
    can = grade(fit('k_43816', t, w0, w1, 1.05)); shade(can, 240, 0.45)
    counter(can, t, ws('47', 45.5), 0, 47, 1120, 170, YEL)
    title(can, t, ws('versenkte', 46.5), 'VERSENKTE SCHIFFE', 1240, 70, CREAM, None, bold=1)
    counter(can, t, ws('274.000'), 0, 274333, 1350, 110, CREAM, 1.4)
    title(can, t, ws('Bruttoregistertonnen'), 'BRUTTOREGISTERTONNEN', 1440, 52, CREAM, None, 'bebas')
    return can
def o_seaburn(can, t, w0, w1):
    title(can, t, ws('Hunderte'), 'HUNDERTE SEELEUTE', 1240, 100, CREAM, None, bold=1)
# 9: HX 112, Schepke and U 100
def s_hx(t, w0, w1):
    can, m = side('k_hx112', 400, 900, t, w0, w1, 1.04); shade(can, 220, 0.5)
    x, y = m(1150, 330); sky(can, t, ws('HX'), 'HX 112', CX, y, 170, CREAM, dur=0.5, skew=-6)
    title(can, t, ws('Geleitzug', 57), 'GELEITZUG', y - 150, 70, CREAM, None, 'bebas')
    return can
def s_schepke(t, w0, w1):
    can = grade(fit('k_schepke', t, w0, w1, 1.05)); shade(can, 230, 0.5)
    title(can, t, ws('Joachim'), 'JOACHIM SCHEPKE', 1330, 110, YEL, None, bold=1)
    return can
def s_u100(t, w0, w1):
    can = grade(fit('k_u100', t, w0, w1, 1.05)); shade(can, 220, 0.5)
    title(can, t, w0 + 0.1, 'U 100', 1330, 150, YEL, None, bold=2)
    return can
# 10: depth charges, surfaced, scuttled
def s_dc(t, w0, w1):
    can = BG('dcbg', 0.0, 100, 2.2)(t, w0)
    def draw(L):
        d = ImageDraw.Draw(L); sea = 760
        d.rectangle((0, sea, W, sea + 4), fill=CREAM + (150,))
        dx = lerp(820, 300, eio(prog(t, w0, w1)))   # the destroyer passes over the boat
        d.polygon([(dx - 230, sea), (dx + 230, sea), (dx + 260, sea - 40), (dx - 200, sea - 40)], fill=CREAM + (255,))
        d.rectangle((dx - 60, sea - 110, dx + 40, sea - 40), fill=CREAM + (255,)); d.rectangle((dx - 10, sea - 170, dx + 10, sea - 110), fill=CREAM + (255,))
        ux, uy = 540, 1130; d.rounded_rectangle((ux - 220, uy - 26, ux + 220, uy + 26), 26, fill=YEL + (255,)); d.rectangle((ux - 40, uy - 70, ux + 40, uy - 26), fill=YEL + (255,))
        for i in range(5):
            t0 = ws('Wasserbomben') + i * 0.45
            if t < t0: continue
            u = (t - t0) / 1.0; x = lerp(dx + 120, dx - 120, i / 4)
            if u < 1: y = lerp(sea + 10, uy - 60 + (i % 2) * 90, u); d.rounded_rectangle((x - 14, y - 20, x + 14, y + 20), 6, fill=CREAM + (255,))
            else:
                y = uy - 60 + (i % 2) * 90; uu = min(1, (u - 1) / 0.6); r = 30 + 150 * uu
                d.ellipse((x - r, y - r, x + r, y + r), outline=CREAM + (int(220 * (1 - uu)),), width=8)
    see(can, draw, 0.88)
    title(can, t, ws('Walker'), 'ZERSTÖRER HMS WALKER', 1330, 84, YEL, None, bold=1)
    return can
def o_surface(can, t, w0, w1):
    pass   # the film speaks for itself here
def o_dive(can, t, w0, w1):
    title(can, t, ws('ließ'), 'BOOT VERSENKT', 1330, 110, CREAM, None, bold=1)
def s_tally(t, w0, w1):
    can = BG('tallybg', 0.0, 120, 2.2)(t, w0)
    counter(can, t, ws('Drei'), 0, 3, 800, 220, RED, 0.4)
    title(can, t, ws('starben'), 'TOTE', 940, 80, CREAM, None, bold=1)
    counter(can, t, ws('40', 73.5), 0, 40, 1160, 220, YEL, 0.6)
    title(can, t, ws('gerettet'), 'GERETTET', 1300, 80, CREAM, None, bold=1)
    return can
def s_ace(t, w0, w1):
    can = grade(fit('k_ace', t, w0, w1, 1.05)); shade(can, 230, 0.5)
    title(can, t, ws('kamen', 75.3), 'IN GEFANGENSCHAFT', 1330, 100, YEL, None, bold=1)
    return can
# 11: Macintyre keeps the binoculars
def s_mac(t, w0, w1):
    can = grade(fit('k_macintyre', t, w0, w1, 1.05)); shade(can, 230, 0.5)
    title(can, t, ws('Donald'), 'DONALD MACINTYRE', 1200, 100, CREAM, None, bold=1)
    title(can, t, ws('Kommandant', 77.4), 'KOMMANDANT DER HMS WALKER', 1310, 60, YEL, None, 'bebas')
    return can
def s_glass(t, w0, w1):
    """the whole bridge photo across the width, shifted up so the binoculars on his chest sit well above the captions"""
    im = src('k_img1'); z = lerp(1.0, 1.04, prog(t, w0, w1)); sw = W * z; sc = sw / im.width; sh = int(im.height * sc)
    can = __import__('lib9')._bg('k_img1').copy(); x0, y0 = (W - sw) / 2, -80 - (sh - im.height * W / im.width) * 0.5
    can.alpha_composite(grade(im.resize((int(sw), sh), Image.BICUBIC).convert('RGBA')), (int(x0), int(y0))); shade(can, 230, 0.62); can.alpha_composite(TOPSH)
    x, y = x0 + 920 * sc, y0 + 2120 * sc   # centre of the binoculars on his chest (source 740..1100 x 1940..2290)
    ring(can, t, ws('Fernglas'), x, y, YEL, 125, False)
    hand(can, t, ws('als', 80.9), 'als Andenken', (CX + 150, y - 250), 110, YEL, 0.55)
    return can
# 12: the escape plan from Canada (map), the intercepted letters, the trap
MC = Map(-71.5, 46.0, 17.0)
BOW, PM = (-78.69, 43.91), (-65.02, 47.82)   # Camp 30 Bowmanville, Ontario; Pointe de Maisonnette, Chaleur Bay, New Brunswick
def s_canada(t, w0, w1):
    can = BG('mapbg', 0.0, 50, 1.6)(t, w0); z = lerp(1.0, 1.04, prog(t, w0, w1)); mp = MC.frame(z); mp.putalpha(170); can.alpha_composite(mp)
    p = lambda lo, la: MC.p(lo, la, z)
    for nm, lo, la in (('KANADA', -74.5, 49.3), ('USA', -76.0, 42.4), ('NEW BRUNSWICK', -66.3, 46.4)):
        x, y = p(lo, la); title(can, t, w0 + 0.2, nm, y, 46, (150, 160, 178), None, 'bebas', min(max(x, 140), 940))
    bx, by = p(*BOW); dot(can, bx, by, YEL, 10)
    if t > ws('Kanada'): title(can, t, ws('Kanada'), 'LAGER BOWMANVILLE', by + 55, 48, YEL, None, 'bebas', max(bx + 60, 220))
    if t > ws('Tunnel'):
        u = eio((t - ws('Tunnel')) / 0.6); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).line((bx, by, bx + 70 * u, by + 30 * u), fill=CREAM + (255,), width=6); can.alpha_composite(L)
        title(can, t, ws('Tunnel'), 'TUNNEL', by - 60, 46, CREAM, None, 'bebas', max(bx + 30, 160))
    px, py = p(*PM)
    route_ = [(bx, by), p(-74.0, 46.6), p(-69.5, 47.8), (px, py)]
    dashed(can, route_, eio((t - ws('Küste')) / 1.4), YEL, 7, 20, 30)
    if t > ws('U-Boot', 92.5):
        dot(can, px + 60, py - 20, RED, 12); title(can, t, ws('U-Boot', 92.5), 'U-BOOT', py - 80, 52, RED, None, 'bebas', min(px + 40, 950))
    return can
def s_letters(t, w0, w1):
    can = BG('mapbg2', 0.0, 80, 1.8)(t, w0)
    def page(L):
        k = eout((t - w0) / 0.35); P_ = Image.new('RGBA', (820, 640), (236, 230, 212, 255)); d = ImageDraw.Draw(P_); rng = np.random.default_rng(3)
        for i, yy in enumerate(range(80, 600, 56)):   # handwriting as wavy strokes, not readable words
            x = 60; pts = []
            while x < 760 - rng.integers(0, 160) * (i == 8):
                pts.append((x, yy + 8 * math.sin(x * 0.09 + i))); x += 6
            d.line(pts, fill=(60, 60, 80, 255), width=4)
        if t > ws('verschlüsselten'):
            u = eio((t - ws('verschlüsselten')) / 0.5)
            for yy in (136, 304, 472): d.line((60, yy + 22, 60 + 640 * u, yy + 22), fill=RED + (255,), width=6)
        if k < 1: P_.putalpha(P_.getchannel('A').point(lambda v: int(v * k)))
        L.alpha_composite(P_, (int(CX - 410), int(560 + (1 - k) * 60)))
    see(can, page, 0.92)
    title(can, t, ws('verschlüsselten'), 'VERSCHLÜSSELTE BRIEFE', 1330, 84, YEL, None, bold=1)
    return can
MB = Map(-65.4, 47.9, 3.2)   # Chaleur Bay
def s_trap(t, w0, w1):
    can = BG('mapbg', 2.0, 50, 1.6)(t, w0); z = lerp(1.0, 1.04, prog(t, w0, w1)); mp = MB.frame(z); mp.putalpha(170); can.alpha_composite(mp)
    p = lambda lo, la: MB.p(lo, la, z)
    px, py = p(*PM); dot(can, px, py, YEL, 10); title(can, t, w0 + 0.2, 'POINTE DE MAISONNETTE', py + 60, 44, YEL, None, 'bebas', min(max(px, 300), 780))
    for i, (lo, la) in enumerate(((-64.75, 47.95), (-64.55, 48.05), (-64.9, 48.08))):
        if t > w0 + 0.2 + i * 0.25: x, y = p(lo, la); ship(can, x, y, math.pi, 46, RED)
    t0 = ws('entkam')
    ux, uy = p(-64.6, 47.9); u = eio((t - t0) / 1.2) if t > t0 else 0.0
    x, y = lerp(ux, ux + 340, u), lerp(uy, uy - 80, u); dot(can, x, y, CREAM, 12)
    title(can, t, ws('scheiterte'), 'FLUCHT GESCHEITERT', 1330, 96, RED, None, bold=1)
    title(can, t, ws('entkam'), 'DAS U-BOOT ENTKAM KNAPP', 1440, 64, CREAM, None, 'bebas')
    return can
def s_years(t, w0, w1):
    can = BG('yearsbg', 0.0, 110, 2.0)(t, w0)
    counter(can, t, w0 + 0.1, 1941, 1947, 900, 220, YEL, 1.6, '{}')
    title(can, t, ws('Gefangenschaft', 104), 'IN GEFANGENSCHAFT', 1060, 90, CREAM, None, bold=1)
    return can
# 13: Bundesmarine and NATO (the 1970s interview, in colour)
def o_interview(can, t, w0, w1):
    title(can, t, ws('Flottillenadmiral') - 0.2, 'FLOTTILLENADMIRAL', 1330, 100, YEL, None, bold=1)
# 14: 1998
def s_old(t, w0, w1):
    can = grade(fit('k_img12', t, w0, w1, 1.05)); shade(can, 230, 0.5)
    title(can, t, ws('1998'), '1998', TOP, 130, CREAM)
    title(can, t, ws('Donau'), 'AUF DER DONAU', 1330, 100, YEL, None, bold=1)
    return can
def s_end(t, w0, w1):
    can = grade(fit('k_h0579', t, w0, w1, 1.04)); shade(can, 230, 0.5)
    title(can, t, w0 + 0.05, 'OTTO KRETSCHMER', TOP, 100, CREAM)
    title(can, t, w0 + 0.25, '1912 · 1998', TOP + 95, 64, YEL, None, 'bebas')
    hand(can, t, ws('goldene'), 'Goldene Hochzeit', (CX, 1180), 104, YEL, 0.6)
    cta(can, t, ws('während') - 0.6)
    return can

NOCAP = [(0.0, ws('Nach') - 0.02)]   # the opening words are already on screen in big letters
ANCH = [
 (0.0, s_hook, None),
 (ws('Otto') + 0.08, FV('kclose', 0.0, o_name, 1.03, 0.375), ('fade',)),
 (ws('versenkten') - 0.03 - 0.0, FV('bow', 0.0, o_bow, 1.04, 0.5), ('whip', 1)),
 (ws('und', 9) - 0.12, s_vorbei, ('fade',)),
 (ws('99', 13.3) - 0.15, s_u99, ('whip', -1)),
 (ws('Geleitzüge') - 0.1, s_convoy, ('fade',)),
 (ws('Statt') + 0.02, FV('peri', 0.0, o_peri, 1.03, 0.5), ('fade',)),
 (ws('Statt') + 1.92, FV('cross', 0.0, o_cross, 1.03, 0.5), ('cut',)),
 (ws('Statt') + 3.92, FV('flash', 0.0, o_flash, 1.03, 0.5), ('cut',)),
 (ws('Weil') - 0.1, FV('radio', 0.0, o_radio, 1.03, 0.5), ('whip', 1)),
 (ws('absetzte') + 0.3, s_silent, ('fade',)),
 (ws('In', 32) + 0.04, FV('sc7', 0.0, o_sc7, 1.03, 0.5), ('whip', -1)),
 (ws('Gut', 38.5) - 0.1, FV('smoke', 0.0, o_smoke, 1.03, 0.55), ('fade',)),
 (ws('Laurentic') - 0.1, s_ships, ('fade',)),
 (ws('Insgesamt') - 0.1, s_total, ('whip', 1)),
 (ws('Auf', 52) - 0.1, FV('seaburn', 0.0, o_seaburn, 1.03, 0.5), ('fade',)),
 (ws('Im', 55) - 0.1, s_hx, ('whip', -1)),
 (ws('In', 60) - 0.1, s_schepke, ('fade',)),
 (ws('U', 64.2) - 0.1, s_u100, ('fade',)),
 (ws('Wasserbomben') - 0.1, s_dc, ('whip', 1)),
 (ws('U', 68.4) - 0.1, FV('surface', 0.0, o_surface, 1.03, 0.5), ('fade',)),
 (ws('Kretschmer', 70.6) - 0.1, FV('dive', 0.0, o_dive, 1.03, 0.5), ('fade',)),
 (ws('Drei', 72.8) - 0.1, s_tally, ('fade',)),
 (ws('kamen', 75.3) - 0.1, s_ace, ('fade',)),
 (ws('Der', 76.9) - 0.1, s_mac, ('whip', 1)),
 (ws('Kretschmers') - 0.1, s_glass, ('fade',)),
 (ws('Kretschmer', 82) - 0.1, s_canada, ('whip', -1)),
 (ws('Doch', 94) - 0.1, s_letters, ('fade',)),
 (ws('warteten') - 0.1, s_trap, ('fade',)),
 (ws('Kretschmer', 102) - 0.1, s_years, ('fade',)),
 (ws('Später', 105.5) - 0.1, FV('interview', 0.0, o_interview, 1.03, 0.5), ('whip', 1)),
 (ws('Er', 110.9) - 0.1, s_old, ('fade',)),
 (ws('während') - 0.1, s_end, ('fade',))]
