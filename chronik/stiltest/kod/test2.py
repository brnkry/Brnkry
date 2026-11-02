# Laconia 0:00-0:57 in the collage style, round 2: display serif (closest free match to Historic Mystique), film inside shapes and letters,
# a filmed grey stage, torn paper, a polaroid, ink circles, hand-drawn arrows, a towing animation, a radio telegram, silhouettes of the boats.
# YouTube Shorts safe area: no text right of x 900 between y 680 and 1580, nothing under y 1560, nothing above y 300.
from style import *
import lib9 as L9
CXS = 480   # text centre, clear of the like/comment column

# 1: "Er versenkte ein Schiff," : yellow band, the Laconia silhouette (larger) with the night film of a burning ship inside it
def s1(t, w0, w1):
    can = paper().copy()
    band(can, t, 0.0, 980, 520, ACC, 0.45)
    word(can, t, ws('Er'), 'ER VERSENKTE', (CXS, 560), disp(120), INK, mode='rise')
    p, mb = mover(t, 0.12, 0.55, (W + 800, 1000), (W / 2, 1000))
    sink = eio((t - ws('Schiff') - 0.15) / 0.8)
    sp = cut('l_img', flat=INK, h=380).rotate(-sink * 5, expand=True, resample=Image.BICUBIC)
    if abs(mb[0]) > 3: place(can, sp, p[0], p[1] + sink * 40, mblur=mb)
    else: filmfill(can, spritemask(sp, p[0], p[1] + sink * 40), 'boom', t, gray=True, contrast=1.5)
    word(can, t, ws('ein', 0.5), 'EIN SCHIFF,', (CXS, 1390), disp(200), INK, mode='slam')
    return push(can, t, w0, w1)

# 2: "rettete danach Hunderte Schiffbrüchige" : yellow disc, HUNDERTE behind him, Hartenstein cut-out rises in front
def s2(t, w0, w1):
    can = paper().copy()
    disc(can, t, w0 + 0.02, (CXS + 40, 880), 360)
    word(can, t, ws('rettete'), 'rettete danach', (CXS, 430), hand(96), INK, mode='wipe', dur=0.4)
    word(can, t, ws('Hunderte'), 'HUNDERTE', (CXS, 640), disp(250), INK, mode='slam')
    p, mb = mover(t, w0 + 0.05, 0.6, (CXS + 60, 2400), (CXS + 60, 1080), back)
    place(can, cut('l_8576', h=820), p[0], p[1], mblur=mb)
    word(can, t, ws('Schiffbrüchige', 2.5), 'SCHIFFBRÜCHIGE', (CXS, 1500), disp(130), INK, mode='rise')
    return push(can, t, w0, w1, 1.0, 1.04)

# 3: "und wurde dafür bombardiert." : the grey stage is a film (B-24s in flight, toned grey), stripes, the B-24 cut-out dives in
def s3(t, w0, w1):
    can = paper().copy()
    full = Image.new('L', (W, H), 255); filmfill(can, full, 'b24up', t - w0, gray=True, contrast=0.9, inner=False)
    can.alpha_composite(Image.new('RGBA', (W, H), (236, 236, 234, 60)))   # paper tone over the film
    stripes(can, t, w0, ACC, 5, 110, 150)
    word(can, t, ws('und', 3.3), 'und wurde dafür', (CXS, 470), hand(100), INK, mode='wipe', dur=0.4)
    p, mb = mover(t, w0 + 0.05, 0.7, (W + 600, -400), (CXS + 40, 960))
    place(can, cut('l_b24', h=720), p[0], p[1], 1.0, 8, mblur=mb)
    scramble(can, t, ws('bombardiert'), 'BOMBARDIERT.', (CXS, 1450), disp(170), INK, 0.45)
    if t > ws('bombardiert'):
        k = max(0.0, 1 - (t - ws('bombardiert')) / 0.3); dx = math.sin(t * 90) * 14 * k
        if abs(dx) > 0.5: can = can.transform(can.size, Image.AFFINE, (1, 0, -dx, 0, 1, 0), Image.BICUBIC)
    return push(can, t, w0, w1)

# 4: the map: the coast as a dark paper cut-out on grid paper, typed date, red marker and a hand-drawn arrow
MA = L9.Map(-10.5, 2.5, 34.0)
@functools.lru_cache(None)
def land():
    b = np.asarray(MA.base().convert('RGB'), np.int16); sea = np.array(L9.SEA, np.int16)
    a = Image.fromarray(((np.abs(b - sea).sum(2) > 18) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    sp = Image.new('RGBA', (W, H), (52, 52, 56, 255)); sp.putalpha(a); return sp
SINK = (-11.63, -5.08)
def s4(t, w0, w1):
    can = paper(True).copy()
    k = eout((t - w0) / 0.6); L = land()
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.35 * k)))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (14, 26 + int((1 - k) * 120)))
    LL = L.copy(); LL.putalpha(L.getchannel('A').point(lambda v: int(v * k))); can.alpha_composite(LL, (0, int((1 - k) * 120)))
    typed(can, t, ws('September'), 'SEPTEMBER 1942', (CXS, 1460), mono(84), INK, 0.05)
    x, y = MA.p(*SINK)
    if t > ws('U', 7.5):
        u = back((t - ws('U', 7.5)) / 0.4); r = 34 * u; d = ImageDraw.Draw(can)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(196, 38, 40, 255)); d.ellipse((x - r * 0.4, y - r * 0.4, x + r * 0.4, y + r * 0.4), fill=(245, 245, 240, 255))
        harrow(can, t, ws('U', 7.5) + 0.2, (x + 230, y + 240), (x + 40, y + 40), INK, 6, 0.3, 0.5)
        word(can, t, ws('U', 7.5) + 0.25, 'U 156', (x + 290, y + 300), disp(130), INK, mode='slam')
    word(can, t, ws('Küste'), 'Westafrika', MA.p(-2, 11), hand(96), ACC, mode='wipe', dur=0.5)
    return push(can, t, w0, w1, 1.0, 1.05)

# 5: dark stage with a light beam, Hartenstein in it
@functools.lru_cache(None)
def beam():
    L = Image.new('L', (W, H), 0); ImageDraw.Draw(L).polygon([(-120, -200), (260, -200), (900, H), (300, H)], fill=150)
    return L.filter(ImageFilter.GaussianBlur(60))
def s5(t, w0, w1):
    can = paper(False, 0.62).copy()
    k = eout((t - w0) / 0.5); B_ = Image.new('RGBA', (W, H), (235, 232, 222, 0)); B_.putalpha(beam().point(lambda v: int(v * k))); can.alpha_composite(B_)
    typed(can, t, ws('12.'), '12. SEPTEMBER, ABENDS', (CXS, 350), mono(58), (230, 230, 226), 0.04)
    p, mb = mover(t, w0 + 0.1, 0.8, (W / 2 + 500, 1150), (W / 2 + 120, 1150))
    place(can, cut('hart_c', h=1200), p[0], p[1], mblur=mb)
    word(can, t, ws('torpedierte'), 'TORPEDIERTE', (CXS, 540), disp(170), ACC, mode='slam')
    word(can, t, ws('Kommandant'), 'Kommandant', (90, 1340), hand(80), (230, 230, 226), 'lm', mode='wipe')
    scramble(can, t, ws('Werner'), 'HARTENSTEIN', (CXS - 30, 1460), disp(150), (245, 245, 240), 0.5)
    return push(can, t, w0, w1, 1.0, 1.04)

# 6: LACONIA in giant letters with the Laconia film inside them, the colour cut-out of the ship below, corner brackets
def s6(t, w0, w1):
    can = paper().copy()
    band(can, t, w0, 1180, 380, ACC, 0.35)
    word(can, t, ws('britische', 15.2), 'BRITISCHES TRUPPENTRANSPORTSCHIFF', (CXS, 470), disp(66), INK, mode='wipe', dur=0.5)
    if t > ws('Laconia') - 0.1:
        k = eout((t - ws('Laconia') + 0.1) / 0.3); m = textmask('LACONIA', disp(330), (CXS, 800)).point(lambda v: int(v * k))
        filmfill(can, m, 'ship', t - w0, gray=True, contrast=2.2, tint=(20, 20, 24))
    p, mb = mover(t, w0, 0.55, (-700, 1190), (CXS + 20, 1190))
    place(can, cut('l_img', bw=False, h=330), p[0], p[1], mblur=mb)
    brackets(can, t, w0 + 0.4, (60, 600, 900, 1420), INK)
    return push(can, t, w0, w1)

# 7: 2.700 on a floor with its reflection
def s7(t, w0, w1):
    can = paper().copy()
    fl = Image.new('RGBA', (W, H - 1080), (0, 0, 0, 0)); g = np.linspace(40, 140, H - 1080).astype(np.uint8)
    fl.putalpha(Image.fromarray(np.repeat(g[:, None], W, 1))); can.alpha_composite(fl, (0, 1080))
    word(can, t, ws('An', 17.9), 'AN BORD', (CXS, 640), mono(64), INK, mode='rise')
    if t > ws('2.700'):
        v = int(round(2700 * eout((t - ws('2.700')) / 0.9))); s_ = '{:,}'.format(v).replace(',', '.')
        f = disp(360); L = Image.new('RGBA', (W, 460), (0, 0, 0, 0)); ImageDraw.Draw(L).text((CXS, 440), s_, font=f, fill=INK + (255,), anchor='ms', stroke_width=f._sw, stroke_fill=INK + (255,))
        can.alpha_composite(L, (0, 1080 - 440))
        R = L.transpose(Image.FLIP_TOP_BOTTOM); R.putalpha(R.getchannel('A').point(lambda v: int(v * 0.25))); can.alpha_composite(R.filter(ImageFilter.GaussianBlur(3)), (0, 1085))
    word(can, t, ws('Menschen', 19.5), 'MENSCHEN', (CXS, 1330), disp(150), ACC, mode='slam')
    return push(can, t, w0, w1, 1.0, 1.04)

# 8: 54 figures (one for every 50 people); 36 turn yellow for the 1,800 Italian prisoners
def figure(d, x, y, s, col):
    d.ellipse((x - s * 0.22, y - s * 0.95, x + s * 0.22, y - s * 0.51), fill=col + (255,))
    d.rounded_rectangle((x - s * 0.3, y - s * 0.45, x + s * 0.3, y + s * 0.35), s * 0.14, fill=col + (255,))
    d.rectangle((x - s * 0.22, y + s * 0.3, x - s * 0.04, y + s * 0.75), fill=col + (255,)); d.rectangle((x + s * 0.04, y + s * 0.3, x + s * 0.22, y + s * 0.75), fill=col + (255,))
def s8(t, w0, w1):
    can = paper(True).copy()
    cols, rows, s = 9, 6, 74; x0, y0 = CXS - (cols - 1) * 92 / 2, 760
    tp = ws('1.800'); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(cols * rows):
        r, c = divmod(i, cols); ti = w0 + 0.02 * i
        if t < ti: continue
        k = back((t - ti) / 0.3); yy = y0 + r * 112 + (1 - k) * 40
        yel = i >= cols * rows - 36 and t > tp + 0.018 * (i - (cols * rows - 36))
        figure(d, x0 + c * 92, yy, s * min(1, k), ACC if yel else (70, 70, 74))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.3)))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (6, 12)); can.alpha_composite(L)
    for s_, t0, y in (('britische Soldaten', ws('britische', 20.7), 360), ('Zivilisten, Frauen und Kinder', ws('Zivilisten'), 460), ('polnische Wachsoldaten', ws('polnische'), 560)):
        word(can, t, t0, s_, (CXS, y), hand(78), INK, mode='wipe', dur=0.4)
    if t > tp:
        word(can, t, tp, '1.800', (CXS, 1420), disp(200), INK, mode='slam')
        word(can, t, ws('italienische', 26.5), 'ITALIENISCHE KRIEGSGEFANGENE', (CXS, 1530), disp(70), INK, mode='wipe', dur=0.5)
    return push(can, t, w0, w1, 1.0, 1.03)

# 9: "Als U 156 auftauchte," : a U-boat silhouette rises through a waterline, the film of a surfacing boat inside it
def s9(t, w0, w1):
    can = paper().copy(); wl = 1060
    u = back((t - w0) / 0.9, 1.2); sp = uboat(980); y = lerp(wl + 260, wl - 20, u)
    m = spritemask(sp, CXS + 30, y); cutm = Image.new('L', (W, H), 0); ImageDraw.Draw(cutm).rectangle((0, 0, W, wl + 40), fill=255)
    m = ImageChops.multiply(m, cutm); filmfill(can, m, 'esurf', t - w0, gray=True, contrast=1.25)
    d = ImageDraw.Draw(can)
    for i in range(3):   # waterline strokes
        ph = (t * 1.6 + i * 0.33) % 1.0; d.line((60 + i * 40, wl + 40 + i * 22, 860 - i * 60, wl + 40 + i * 22), fill=INK + (int(200 * (1 - ph * 0.5)),), width=5 - i)
    word(can, t, ws('Als'), 'ALS', (CXS, 560), disp(110), INK, mode='rise')
    word(can, t, ws('U', 28.9), 'U 156', (CXS, 700), disp(190), INK, mode='slam')
    word(can, t, ws('auftauchte'), 'auftauchte', (CXS, 1320), hand(120), INK, mode='wipe', dur=0.5)
    return push(can, t, w0, w1)

# 10: "hörte die Besatzung aus dem Wasser Hilferufe auf Italienisch." : HILFERUFE in huge letters with the film of people in the water inside, sound rings
def s10(t, w0, w1):
    can = paper().copy()
    word(can, t, ws('hörte'), 'aus dem Wasser', (CXS, 560), hand(110), INK, mode='wipe', dur=0.5)
    if t > ws('Hilferufe') - 0.1:
        k = eout((t - ws('Hilferufe') + 0.1) / 0.3); f = disp(250)
        m = textmask('HILFE', f, (CXS, 860)).point(lambda v: int(v * k)); m2 = textmask('RUFE', f, (CXS, 1110)).point(lambda v: int(v * k))
        filmfill(can, ImageChops.lighter(m, m2), 'water', t - w0, gray=True, contrast=2.2, tint=(20, 20, 24))
        d = ImageDraw.Draw(can)
        for j in range(3):
            ph = ((t - ws('Hilferufe')) * 0.9 + j / 3) % 1.0; r = 120 + 420 * ph
            d.arc((CXS - r, 980 - r, CXS + r, 980 + r), 200, 340, fill=ACC + (int(220 * (1 - ph)),), width=8)
    word(can, t, ws('Italienisch'), 'AUF ITALIENISCH', (CXS, 1400), disp(110), ACC, mode='slam')
    return push(can, t, w0, w1)

# 11: "Hartenstein begriff ... des eigenen Verbündeten getroffen hatte, und begann eine Rettung." : torn yellow strip, Hartenstein, ink circle, RETTUNG
def s11(t, w0, w1):
    can = paper().copy()
    k = eout((t - w0) / 0.4); strip = torn(1300, 700, ACC, 4)
    can.alpha_composite(strip, (int(-110 - (1 - k) * 1400), 520))
    p, mb = mover(t, w0 + 0.1, 0.7, (-500, 1080), (300, 1080))
    place(can, cut('hart_c', h=1060), p[0], p[1], mblur=mb)
    word(can, t, ws('begriff'), 'begriff:', (690, 420), hand(100), INK, mode='wipe', dur=0.4)
    word(can, t, ws('eigenen'), 'der eigene', (690, 640), disp(90), INK, mode='rise')
    word(can, t, ws('Verbündeten'), 'VERBÜNDETE', (640, 780), disp(150), INK, mode='slam')
    inkcircle(can, t, ws('getroffen'), (420, 690, 870, 870), (196, 38, 40), 8, 0.5)
    word(can, t, ws('getroffen'), 'getroffen', (640, 940), hand(96), (196, 38, 40), mode='wipe', dur=0.4)
    if t > ws('begann'):
        disc(can, t, ws('begann'), (680, 1240), 170, INK, 0.35)
        scramble(can, t, ws('Rettung') - 0.2, 'RETTUNG', (680, 1240), disp(120), ACC, 0.45)
    return push(can, t, w0, w1, 1.0, 1.04)

# 12: "Er nahm Schiffbrüchige an Bord, bis das Deck voller Menschen war," : a polaroid of the crowded deck drops in, taped, arrow to the people
def s12(t, w0, w1):
    can = paper(True).copy()
    k = back((t - w0) / 0.5, 1.2); P_ = polaroid(L9.src('l_hss').crop((150, 0, 2750, 1536)), 820)
    y = lerp(-900, 900, k); place(can, P_, CXS, y)
    if t > w0 + 0.45: tape(can, CXS - 330, 900 - P_.height / 2 + 6, 160, -10); tape(can, CXS + 330, 900 - P_.height / 2 + 6, 160, 9)
    word(can, t, ws('Schiffbrüchige', 40.5), 'an Bord genommen', (CXS, 420), hand(96), INK, mode='wipe', dur=0.5)
    harrow(can, t, ws('Deck'), (CXS - 260, 1430), (CXS - 60, 1050), INK, 6, -0.25, 0.45)
    word(can, t, ws('voller'), 'DECK VOLLER MENSCHEN', (CXS, 1480), disp(96), INK, mode='slam')
    return push(can, t, w0, w1)

# 13: "und nahm Rettungsboote ins Schlepptau." : the U-boat silhouette crosses the grid, a rope with lifeboats trailing behind it
def s13(t, w0, w1):
    can = paper(True).copy(); u = clamp((t - w0) / (w1 - w0)); bx = lerp(900, 740, u); by = 860
    sp = uboat(440); place(can, sp, bx, by)
    d = ImageDraw.Draw(can); px = bx - 220; py = by + 30
    for i in range(3):
        tt = (t - w0) * 3 - i * 0.4
        if tt < 0: break
        lx = px - 120; ly = by + 70 + 10 * math.sin(t * 3 + i)
        d.line((px, py, lx + 60, ly), fill=INK + (220,), width=4); px, py = lx - 60, ly
        place(can, lifeboat(120, ACC), lx, ly + 14)
    word(can, t, ws('Rettungsboote', 44), 'RETTUNGSBOOTE', (CXS, 560), disp(150), INK, mode='slam')
    word(can, t, ws('Schlepptau'), 'im Schlepptau', (CXS, 1280), hand(120), INK, mode='wipe', dur=0.5)
    return push(can, t, w0, w1)

# 14: the radio message: dark stage, rings from the mast, the telegram typed on a torn strip as it is spoken, morse dots
def s14(t, w0, w1):
    can = paper(False, 0.66).copy(); d = ImageDraw.Draw(can)
    for j in range(4):
        ph = ((t - w0) * 0.7 + j / 4) % 1.0; r = 60 + 600 * ph
        d.ellipse((CXS - r, 330 - r * 0.6, CXS + r, 330 + r * 0.6), outline=ACC + (int(200 * (1 - ph)),), width=5)
    place(can, uboat(420, (230, 230, 226)), CXS, 360, shadow=False)
    word(can, t, ws('offen'), 'OFFEN AUF ENGLISCH', (CXS, 520), disp(110), ACC, mode='slam')
    k = eout((t - ws('Er', 47.7) + 0.2) / 0.4)
    if k > 0:
        strip = torn(860, 640, (236, 232, 220), 7); can.alpha_composite(strip, (int(CXS - 430), int(700 + (1 - k) * 900)))
        lines = [('IF ANY SHIP WILL ASSIST', ws('Er', 47.7)), ('THE SHIP-WRECKED LACONIA', ws('Schiff', 48.4)), ('CREW, I WILL NOT ATTACK', ws('angreifen')),
                 ('HER PROVIDING I AM NOT', ws('solange')), ('BEING ATTACKED.', ws('angegriffen'))]
        for i, (s_, t0) in enumerate(lines):
            typed(can, t, t0, s_, (CXS - 380, 790 + i * 100), mono(52), (196, 38, 40) if 'NOT ATTACK' in s_ else INK, 0.022, anchor='lm')
        for i in range(int((t - ws('Er', 47.7)) * 8)):   # morse dots and dashes along the bottom of the strip
            if i > 38: break
            x = CXS - 380 + i * 20; ImageDraw.Draw(can).rectangle((x, 1270, x + (14 if i % 3 else 6), 1276), fill=INK + (200,))
    return push(can, t, w0, w1, 1.0, 1.03)

# 15: "Dönitz schickte weitere U-Boote, und auch ein italienisches U-Boot kam zu Hilfe." : Dönitz cut-out, three boat silhouettes slide in with labels
def s15(t, w0, w1):
    can = paper().copy()
    p, mb = mover(t, w0, 0.6, (-500, 1250), (230, 1250))
    place(can, cut('l_doenitz', h=980), p[0], p[1], mblur=mb)
    word(can, t, ws('Dönitz', 53), 'DÖNITZ', (CXS, 420), disp(170), INK, mode='slam')
    for i, (lab, t0, col, y) in enumerate((('U 506', ws('weitere'), INK, 700), ('U 507', ws('weitere') + 0.25, INK, 900), ('CAPPELLINI', ws('italienisches'), (40, 110, 60), 1100))):
        q, mb2 = mover(t, t0, 0.55, (W + 500, y), (640, y))
        place(can, uboat(420, col), q[0], q[1], mblur=mb2)
        word(can, t, t0 + 0.3, lab, (640, y + 95), disp(70), col, mode='rise')
    word(can, t, ws('Hilfe'), 'zu Hilfe', (640, 1380), hand(110), ACC, mode='wipe', dur=0.4)
    return push(can, t, w0, w1)

SC = [(0.0, s1), (ws('rettete'), s2), (ws('und', 3.3), s3), (ws('Im'), s4), (ws('Am', 10.9), s5), (ws('das', 15.2), s6), (ws('An', 17.9), s7), (ws('britische', 20.7), s8),
      (ws('Als'), s9), (ws('hörte'), s10), (ws('Hartenstein', 34.5), s11), (ws('Er', 40.2), s12), (ws('und', 43.7), s13), (ws('Dann'), s14), (ws('Dönitz', 53), s15)]
TEND = wt('Am', 57.7) - 0.08
def frame(t):
    i = max(j for j, (a, _) in enumerate(SC) if a <= t); a, fn = SC[i]; b = SC[i + 1][0] if i + 1 < len(SC) else TEND
    img = fn(t, a, b)
    for lim, sign in (((b - 0.12, b), -1), ((a, a + 0.12), 1)):
        if (sign < 0 and i + 1 < len(SC) and t > lim[0]) or (sign > 0 and i > 0 and t < lim[1]):
            u = (t - lim[0]) / 0.12; dx = (-W * 0.18 * eio(u)) if sign < 0 else (W * 0.18 * (1 - eio(u)))
            acc = np.zeros((H, W, 4), np.float32)
            for k in range(6): acc += np.asarray(img.transform(img.size, Image.AFFINE, (1, 0, -(dx * k / 5), 0, 1, 0), Image.BILINEAR), np.float32)
            img = Image.fromarray((acc / 6).astype(np.uint8))
    a_ = np.asarray(img.convert('RGB')).astype(np.int16) + np.random.default_rng(int(t * 30)).normal(0, 3, (H, W))[..., None].astype(np.int16)
    return Image.fromarray(np.clip(a_, 0, 255).astype(np.uint8))

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); P_ = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = frame(t).convert('RGBA'); d = ImageDraw.Draw(f)
            if os.environ.get('UI'):
                d.rectangle((0, 0, W, 290), outline=(0, 255, 255, 255), width=4); d.rectangle((930, 680, W, 1580), outline=(0, 255, 255, 255), width=4); d.rectangle((0, 1580, W, H), outline=(0, 255, 255, 255), width=4)
            d.text((10, 300), '%.2f' % t, fill=(255, 0, 255, 255)); P_.paste(f.convert('RGB').resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P_.save(B + sys.argv[2], quality=85); sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
        if n % 30 == 0: print('t', n / FPS, flush=True)
    p.stdin.close(); p.wait(); print('rc', p.returncode)
