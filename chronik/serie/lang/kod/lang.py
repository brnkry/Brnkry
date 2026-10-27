# "Deutschland im Zweiten Weltkrieg", Teil 1, long version (16:9). Everything happens on the magazine: archive film runs in
# framed photos on the pages and the camera flies into a photo until the film fills the frame, then pulls back to the page.
# The camera always arrives before the word it shows; every page turn ends before the first sentence of the new spread.
import functools
from lcore import *
from lmap import Map, _my
import ldraw as X
from ldraw import counter
from drawings import drawing, tank_m, biplane_m, uboat_m, monoplane_m, loaf_m
P = lambda w_, a=0.0: ws(w_, a)          # global time of a spoken word (start - 0.04)
T_END = VEND + 9.0
CD = 1.0                                 # camera move duration
DARK = (34, 34, 36)

# ---------- framed film on the page ----------
CLIPR = {'tanks': (0.2, 4.2), 'tanksc': (4.3, 6.5), 'street': (0.4, 5.5), 'crowd': (0.3, 4.5), 'ship2': (0.0, 7.9), 'ship1': (0.0, 6.9), 'f1a': (0.0, 7.9), 'f1b': (0.0, 9.9),
         'hit1': (0.3, 12.2), 'hit2': (19.5, 27.7), 'fire': (3.0, 12.8), 'kroll': (0.2, 5.0), 'union': (0.3, 4.6), 'pcrowd': (0.1, 2.7), 'psquare': (0.2, 3.5)}
SRC = {'tanksc': 'tanks', 'hit1': 'hitler_b', 'hit2': 'hitler_b'}
def film_at(key, t, t0, speed=1.0):
    a, b = CLIPR[key]; ct = a + ((t - t0) * speed) % (b - a); return clip_at(SRC.get(key, key), ct)
def framed(pg, t, t0, key, box, cap=None, speed=1.0, still=None):
    """a photo print pasted on the page: soft shadow, thin keyline, four dark photo corners; the film keeps running in it"""
    if t < t0: return
    k = eout((t - t0) / 0.45); x0, y0, bw, bh = [int(v) for v in box]
    g = still if still is not None else film_at(key, t, t0, speed); w, h = g.size
    sc = max(bw / w, bh / h); cw, ch = bw / sc, bh / sc
    fr = tone(g.convert('L').resize((bw, bh), Image.BICUBIC, box=((w - cw) / 2, (h - ch) / 2, (w + cw) / 2, (h + ch) / 2)))
    sh = Image.new('L', (bw + 80, bh + 80), 0); ImageDraw.Draw(sh).rectangle((40 + 8, 40 + 12, 40 + bw + 8, 40 + bh + 12), fill=int(120 * k))
    stamp_ink(pg, sh.filter(ImageFilter.GaussianBlur(12)), (x0 - 40, y0 - 40), (40, 34, 28))
    if k < 1: fr = Image.blend(Image.new('RGB', fr.size, PAPER), fr, k)
    pg.paste(fr, (x0, y0)); d = ImageDraw.Draw(pg); c = fade_col(DARK, k)
    d.rectangle((x0, y0, x0 + bw, y0 + bh), outline=fade_col((60, 60, 60), k), width=2)
    L = 46
    for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x0 + bw, y0, -1, 1), (x0, y0 + bh, 1, -1), (x0 + bw, y0 + bh, -1, -1)):
        d.polygon([(cx - sx * 8, cy - sy * 8), (cx + sx * L, cy - sy * 8), (cx - sx * 8, cy + sy * L)], fill=c)
    if cap:
        d.line((x0, y0 + bh + 30, x0 + 150, y0 + bh + 30), fill=fade_col(ACC, k), width=5)
        d.text((x0, y0 + bh + 48), cap, font=italic(32), fill=fade_col(GREY, k))
def fill(side, box, f=1.09):
    """camera that fills the frame with a photo box of a page"""
    x0, y0, bw, bh = box; return ((0 if side == 'L' else PW) + x0 + bw / 2, y0 + bh / 2, f * max(W / bw, H / bh))
LC, RC, MID = 700, 2100, PW
def fr(side, y0, y1, smax=1.3):
    s = min(smax, 1000 / (y1 - y0), 1840 / PW); return ((LC if side == 'L' else RC), (y0 + y1) / 2, s)
OV = (MID, 905, 0.60)
def head(pg, t, t0, kicker, l1, l2=None, w1=800, w2=400, size=120):
    label(pg, t, t0, kicker, (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, l1, (110, 250), serif(size, w1))
    if l2: label(pg, t, t0 + 0.2, l2, (110, 250 + int(size * 1.17)), serif(size, w2))

# ---------- stills ----------
@functools.lru_cache(None)
def soldier():
    im = Image.open(S + 'teil1/drive/BG2_Bild_4.jpg').convert('RGB'); r = 9; x, y = 113, 84
    reg = im.crop((x - r * 2, y - r * 2, x + r * 2, y + r * 2)); bl = reg.resize((4, 4), Image.BILINEAR).resize(reg.size, Image.BICUBIC)
    m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).ellipse((r * 2 - r - 3, r * 2 - r - 3, r * 2 + r + 3, r * 2 + r + 3), fill=255)
    im.paste(Image.composite(bl, reg, m.filter(ImageFilter.GaussianBlur(2))), (x - r * 2, y - r * 2)); return im.convert('L')

# ================= SP0: masthead and the hook =================
B0 = (110, 600, 1180, 664)
@functools.lru_cache(None)
def masthead():
    pg = base(1, True).copy(); d = ImageDraw.Draw(pg)
    for i, c in enumerate(((24, 24, 26), (196, 30, 34), (236, 186, 32))): d.rectangle((110, 196 + i * 92, 128, 196 + (i + 1) * 92), fill=c)   # the flag as an editorial bar
    d.text((160, 186), 'Deutschland im', font=serif(118, 900), fill=TXT); d.text((160, 326), 'Zweiten Weltkrieg', font=serif(118, 400), fill=TXT)
    for i, c in enumerate(((24, 24, 26), (196, 30, 34), (236, 186, 32))): d.rectangle((110, 490 + i * 9, PW - 110, 490 + (i + 1) * 9), fill=c)
    d.text((110, 545), 'TEIL 1 · DER WEG IN DEN KRIEG', font=sans(38, 800), fill=ACC, anchor='lm')
    d.text((PW - 110, 545), 'EINE SERIE IN MEHREREN TEILEN', font=sans(28, 600), fill=GREY, anchor='rm')
    return pg
def s0L(t):
    pg = masthead().copy()
    framed(pg, t, -1, 'tanks', B0, 'Deutsche Panzer, 1939')
    label(pg, t, P('durfte') - 0.1, '1919', (110, 1350), serif(110, 800), ACC)
    body(pg, t, 420, 1365, 'durfte Deutschland keinen einzigen Panzer besitzen.', P('durfte') - 0.1, accent=('keinen', 'einzigen', 'Panzer'), bold=('Deutschland',), size=56, lh=76, maxw=870)
    return pg
def s0R(t):
    pg = base(2, False).copy()
    drawing(pg, t, P('keinen'), 0.8, lambda ph: tank_m(700, 470, 0.95, ph))
    strike(pg, t, P('Panzer', 4) + 0.15, (260, 240), (1150, 700), 12)
    label(pg, t, P('besitzen'), 'Abb. 1 · Panzer: verboten', (110, 760), italic(34), GREY)
    rule(pg, t, P('Das', 6), 860)
    for i, (a_, b_, w_) in enumerate((('Das Heer:', 'klein', 'klein'), ('Die Wirtschaft:', 'am Boden', 'Boden'), ('Das Land:', 'zerrissen', 'zerrissen'))):
        y = 920 + i * 150; tw = P(w_, 6) if w_ != 'zerrissen' else P('Land', 9)
        label(pg, t, tw - 0.5, a_, (110, y), serif(84, 400)); label(pg, t, tw, b_, (110 + serif(84, 400).getlength(a_ + ' '), y), serif(84, 800), ACC)
    X.flag(pg, t, P('Das', 6) - 0.2, 'de', 130, 1430, 190, 116, 'Weimarer Republik', 'Flagge ab 1919', size=40)
    return pg

# ================= SP1: the ship / the question =================
B1 = (110, 470, 1180, 664)
def s1L(t):
    pg = base(3, True).copy(); framed(pg, t, -1, 'ship2', B1, 'Linienschiff Schleswig-Holstein, 1. September 1939')
    label(pg, t, -1, 'DER KRIEG', (110, 300), sans(40, 800), ACC); label(pg, t, -1, 'Zwanzig Jahre später', (110, 350), serif(70, 400))
    return pg
def s1R(t):
    pg = base(4, False).copy(); t0 = P('Wie', 15)
    label(pg, t, t0, 'Wie konnte', (110, 520), serif(140, 800)); label(pg, t, t0 + 0.35, 'das geschehen?', (110, 690), serif(140, 800), ACC)
    rule(pg, t, t0 + 0.6, 920)
    label(pg, t, t0 + 0.7, 'Von Versailles bis zum 1. September 1939.', (110, 960), italic(44), GREY)
    return pg

# ================= SP2: November 1918 / the stab-in-the-back legend =================
B2 = (110, 560, 1180, 664)
def s2L(t):
    pg = base(5, True).copy(); head(pg, t, P('Im', 18) - 0.1, 'NOVEMBER 1918', 'Das Ende des', 'Kaiserreichs', size=100)
    framed(pg, t, P('Im', 18), 'f1b', B2, 'Deutschland, 1918/19')
    label(pg, t, P('Kaiser'), '9. NOVEMBER 1918', (110, 1340), sans(36, 800), ACC)
    label(pg, t, P('Kaiser') + 0.1, 'Der Kaiser dankt ab.', (110, 1390), serif(60, 800)); label(pg, t, P('Republik'), 'Die Republik wird ausgerufen.', (110, 1470), serif(60, 400))
    label(pg, t, P('kein', 27), 'Kein feindlicher Soldat auf deutschem Boden.', (110, 1590), italic(40), GREY)
    return pg
def s2R(t):
    pg = base(6, False).copy(); head(pg, t, P('Bald'), 'DIE LÜGE', 'Die Dolchstoß-', 'legende', w2=800)
    label(pg, t, P('Heer', 33), '„Im Felde', (190, 600), serif(110, 400)); label(pg, t, P('unbesiegt'), 'unbesiegt“', (190, 730), serif(110, 400), ACC)
    if t > P('Heer', 33): drawing(pg, t, P('Heer', 33), 1.0, lambda ph: (*X.helmet(700, 1150, 1.2), []))
    label(pg, t, P('geblieben'), 'Abb. 2 · Stahlhelm M1916', (110, 1420), italic(34), GREY)
    stamp(pg, t, P('Verrätern'), 'LEGENDE', (1000, 1560), 84, -7)
    return pg

# ================= SP3: Versailles / the losses =================
MAP19 = Map('m19', (PW, PH), (110, 330, 1180, 900), 4.5, 24.5, 46.6)
B3 = (110, 640, 1180, 664)
def s3L(t):
    pg = base(7, True).copy(); head(pg, t, P('Am', 38.5) - 0.1, '28. JUNI 1919', 'Der Vertrag', 'von Versailles', w1=400, w2=800)
    framed(pg, t, P('Am', 38.5), 'f1a', B3, 'Archivaufnahme, 1919', speed=0.8)
    label(pg, t, P('unterzeichnete'), 'Unterzeichnet im Spiegelsaal von Versailles', (110, 1420), serif(50, 400))
    return pg
def s3R(t):
    pg = base(8, False).copy(); t0 = P('Es', 44) - 0.1; m = MAP19
    label(pg, t, t0, 'Deutschland 1914 und 1919', (110, 200), serif(78, 800))
    if t >= t0:
        k = eout((t - t0) / 0.8); m.frame(pg, k); m.base_layer(pg, k)
        m.hatch(pg, 'lost1919', clamp((t - P('verlor')) / 0.9), (120, 120, 120), a=0.55, edge=False, step=12)
        m.hatch(pg, 'danzig', clamp((t - P('verlor') - 0.4) / 0.4), (120, 120, 120), a=0.55, edge=False, step=12)
        for s_, ll, t1, f, c in (('Elsass-Lothringen', (6.9, 48.6), P('verlor') + 0.5, sans(26, 700), TXT), ('an Frankreich', (6.9, 48.2), P('verlor') + 0.6, italic(24), TXT),
                                 ('Posen', (17.0, 52.45), P('verlor') + 0.8, sans(26, 700), TXT), ('an Polen', (17.0, 52.05), P('verlor') + 0.9, italic(24), TXT),
                                 ('Polnischer Korridor', (16.2, 53.95), P('Korridor'), sans(28, 800), ACC), ('Danzig', (18.65, 54.62), P('Korridor') + 0.3, sans(26, 700), TXT),
                                 ('Freie Stadt', (18.65, 54.95), P('Korridor') + 0.4, italic(24), TXT), ('Ostpreußen', (21.0, 54.05), P('Ostpreußen'), sans(30, 800), TXT),
                                 ('DEUTSCHES REICH', (11.0, 51.6), t0 + 0.4, sans(34, 700), TXT)):
            m.label(pg, t, t1, s_, ll, f, c)
        m.line(pg, t, P('Korridor') + 0.1, 0.6, [(17.6, 54.75), (17.9, 54.0), (18.3, 53.3), (18.6, 52.9)], ACC, 6, dash=14)
    label(pg, t, P('Achtel'), '1/8', (110, 1290), serif(170, 800), ACC); label(pg, t, P('Achtel') + 0.2, 'des Gebiets verloren', (440, 1365), serif(60, 400))
    label(pg, t, P('Achtel') + 0.4, 'Grau schraffiert: Gebietsverluste 1919', (110, 1540), italic(30), GREY)
    return pg

# ================= SP4: the army / war guilt and reparations =================
def s4L(t):
    pg = base(9, True).copy(); t0 = P('Das', 50) - 0.1
    label(pg, t, t0, 'DAS HEER', (110, 200), sans(40, 800), ACC)
    label(pg, t, P('100.000'), '100.000', (100, 230), serif(250, 800), ACC); label(pg, t, P('Mann', 51), 'Mann, nicht mehr.', (110, 540), serif(70, 400))
    rule(pg, t, P('Panzer', 53) - 0.3, 670)
    for (fn, cx, cy, sc, name, tw) in ((tank_m, 300, 930, 0.42, 'Panzer', P('Panzer', 53)), (biplane_m, 700, 900, 0.5, 'Luftwaffe', P('Luftwaffe', 53.5)), (uboat_m, 1100, 950, 0.48, 'U-Boote', P('U-Boote'))):
        drawing(pg, t, tw, 0.6, lambda ph, fn=fn, cx=cx, cy=cy, sc=sc: fn(cx, cy, sc, ph)); label(pg, t, tw + 0.2, name, (cx, 1060), sans(40, 700), TXT, 'ma')
    stamp(pg, t, P('verboten', 55), 'VERBOTEN', (700, 1215), 96, -5)
    rule(pg, t, P('Rheinland', 56) - 0.3, 1340)
    label(pg, t, P('Rheinland', 56) - 0.2, 'Das Rheinland:', (110, 1380), serif(70, 800)); label(pg, t, P('entmilitarisiert'), 'entmilitarisiert', (110, 1470), serif(70, 400), ACC)
    label(pg, t, P('entmilitarisiert') + 0.3, 'keine Soldaten, keine Festungen', (110, 1575), italic(34), GREY)
    return pg
def s4R(t):
    pg = base(10, False).copy(); t0 = P('Deutschland', 58.4)
    head(pg, t, t0, 'ARTIKEL 231', 'Die Schuld', 'am Krieg', w2=400)
    for i, s_ in enumerate(('„… dass Deutschland und seine Verbündeten', 'als Urheber für alle Verluste und Schäden', 'verantwortlich sind …“')):
        label(pg, t, P('Verantwortung') + 0.2 * i, s_, (110, 580 + i * 56), italic(38), GREY)
    rule(pg, t, P('Sieger') - 0.2, 820)
    label(pg, t, P('Sieger') - 0.2, 'REPARATIONEN · 1921', (110, 860), sans(40, 800), ACC)
    counter(pg, t, P('132') - 0.3, 1.2, 132, (110, 900), serif(230, 800), ACC, expo=False)
    label(pg, t, P('Milliarden', 64.5), 'Milliarden Goldmark', (110, 1200), serif(74, 800))
    drawing(pg, t, P('132') - 0.3, 0.2, lambda ph: X.coins_m(1050, 1560, 1.0, ph * 1.9))
    return pg

# ================= SP5: the Ruhr / hyperinflation =================
def s5L(t):
    pg = base(11, True).copy(); head(pg, t, P('Als', 67) - 0.1, 'JANUAR 1923', 'Die Ruhr-', 'besetzung', w2=800)
    X.flag(pg, t, P('französische'), 'fr', 130, 610, 190, 116, 'Frankreich', size=40)
    X.flag(pg, t, P('belgische'), 'be', 130, 800, 190, 116, 'Belgien', size=40)
    drawing(pg, t, P('Truppen', 70) - 0.2, 1.0, lambda ph: X.factory_m(860, 1290, 0.62, ph))
    label(pg, t, P('Ruhrgebiet'), 'Abb. 3 · Zeche im Ruhrgebiet', (650, 1420), italic(30), GREY)
    label(pg, t, P('Ruhrgebiet') + 0.2, 'Frankreich und Belgien holen sich Kohle', (110, 1530), serif(48, 400)); label(pg, t, P('Ruhrgebiet') + 0.4, 'als Pfand für die Reparationen.', (110, 1600), serif(48, 400))
    return pg
def s5R(t):
    pg = base(12, False).copy(); t0 = P('Regierung', 74)
    if t > P('druckte'):
        notes = X.notes_m(140, 470, 1120, 420, t - P('druckte'))
        ink(pg, t, -1, 0.001, notes, wd=3, a=0.5 * clamp((t - P('druckte')) / 0.5) * clamp((P('Dollar') - t) / 0.8))
    head(pg, t, t0, '1923', 'Hyperinflation', size=120)
    label(pg, t, P('druckte'), 'Der Staat bezahlt den Widerstand', (110, 410), italic(42), GREY); label(pg, t, P('bezahlen'), 'mit frisch gedrucktem Geld.', (110, 462), italic(42), GREY)
    label(pg, t, P('Im', 79.5), 'November 1923: 1 Dollar =', (110, 920), serif(64, 400))
    counter(pg, t, P('Dollar'), 1.3, 4.2e12, (110, 1000), serif(110, 800), ACC)
    label(pg, t, P('Billionen'), 'Mark', (110, 1140), serif(60, 400))
    rule(pg, t, P('Brot', 84) - 0.2, 1240)
    drawing(pg, t, P('Brot', 84), 0.6, lambda ph: loaf_m(1080, 1360, 0.8, ph))
    label(pg, t, P('Brot', 84) - 0.1, 'Ein Brot in Berlin:', (110, 1280), serif(56, 400)); label(pg, t, P('Hunderte', 85), 'Hunderte', (110, 1350), serif(80, 800), ACC)
    label(pg, t, P('Milliarden', 86), 'Milliarden Mark', (110, 1450), serif(80, 800), ACC)
    label(pg, t, P('Wer'), 'Ersparnisse eines ganzen Lebens:', (110, 1590), italic(40), GREY)
    stamp(pg, t, P('plötzlich'), 'WERTLOS', (1120, 1600), 80, -8)
    return pg

# ================= SP6: the Munich putsch / Landsberg / the golden twenties =================
B6 = (110, 600, 1180, 664)
def s6L(t):
    pg = base(13, True).copy(); head(pg, t, P('Im', 91) - 0.1, 'MÜNCHEN, 9. NOVEMBER 1923', 'Der Hitler-', 'Putsch', w2=800)
    framed(pg, t, P('Im', 91), 'hit2', B6, 'Adolf Hitler, Aufnahme Anfang der 1930er Jahre')
    stamp(pg, t, P('scheiterte'), 'GESCHEITERT', (700, 1500), 100, -6)
    return pg
def s6R(t):
    pg = base(14, False).copy(); t0 = P('Haft', 98) - 0.2
    label(pg, t, t0, 'FESTUNGSHAFT', (110, 200), sans(40, 800), ACC); label(pg, t, t0 + 0.1, 'Landsberg', (110, 250), serif(110, 800))
    if t > t0: drawing(pg, t, t0, 0.7, lambda ph: (*X.prison(330, 640, 0.62), []))
    if t > P('Buch'): drawing(pg, t, P('Buch'), 0.6, lambda ph: (*X.book(880, 640, 0.62), []))
    label(pg, t, P('Mein'), '„Mein Kampf“, 1925', (880, 820), italic(34), GREY, 'ma')
    rule(pg, t, P('Dann', 101.5) - 0.2, 930)
    label(pg, t, P('Dann', 101.5) - 0.2, 'DIE GOLDENEN ZWANZIGER', (110, 970), sans(40, 800), ACC)
    label(pg, t, P('Währung'), 'Rentenmark', (110, 1020), serif(80, 800)); label(pg, t, P('Inflation', 104) - 0.2, 'beendet die Inflation, November 1923', (110, 1120), serif(44, 400), GREY)
    label(pg, t, P('amerikanische', 104), 'US-Kredite', (110, 1190), serif(80, 800)); label(pg, t, P('Kredite', 106) + 0.2, 'Dawes-Plan, 1924', (110, 1290), serif(44, 400), GREY)
    X.axes(pg, t, P('Wirtschaft', 107), (110, 1370, 1180, 250))
    X.stock(pg, t, P('Wirtschaft', 107), 2.2, (110, 1370, 1180, 250), [(0, 0.1), (0.15, 0.22), (0.3, 0.3), (0.45, 0.42), (0.6, 0.5), (0.75, 0.62), (0.9, 0.7), (1.0, 0.75)], crash_at=2)
    label(pg, t, P('geliehenem'), 'auf Kredit gebaut', (1290, 1640), italic(36), ACC, 'ra')
    return pg

# ================= SP7: the crash, unemployment / the radicals =================
B7 = (110, 200, 1180, 664)
def s7L(t):
    pg = base(15, True).copy(); t0 = P('Im', 111) - 0.1
    label(pg, t, t0, 'NEW YORK, OKTOBER 1929', (110, 200), sans(40, 800), ACC); label(pg, t, t0 + 0.1, 'Der Börsenkrach', (110, 250), serif(100, 800))
    X.axes(pg, t, t0 + 0.2, (110, 420, 1180, 400))
    pts = [(0, 0.35), (0.1, 0.42), (0.2, 0.5), (0.3, 0.58), (0.4, 0.66), (0.5, 0.76), (0.58, 0.86), (0.62, 0.9), (0.68, 0.55), (0.74, 0.62), (0.8, 0.38), (0.88, 0.3), (1.0, 0.12)]
    X.stock(pg, t, t0 + 0.3, P('zusammen', 114) - t0 + 0.3, (110, 420, 1180, 400), pts, crash_at=0.55, wd=7)
    label(pg, t, P('zusammen', 114), 'Schwarzer Donnerstag, 24. Oktober 1929', (110, 850), italic(36), GREY)
    label(pg, t, P('forderten', 116), 'US-Banken fordern ihre Kredite zurück.', (110, 920), serif(56, 800))
    rule(pg, t, P('Fabriken') - 0.3, 1030)
    label(pg, t, P('Fabriken') - 0.3, 'ARBEITSLOSE IN DEUTSCHLAND (MIO.)', (110, 1070), sans(34, 800), GREY)
    t1 = P('Fabriken')
    X.barchart(pg, t, 160, 1470, 190, 80, 300, 6.0, [('1929', 1.9, t1, False), ('1930', 3.1, t1 + 0.4, False), ('1931', 4.5, t1 + 0.8, False), ('1932', 6.0, P('sechs', 121), True)],
               lambda v: ('%.1f' % v).replace('.', ','))
    label(pg, t, P('Millionen', 121.5), '6 Millionen Arbeitslose', (110, 1580), serif(70, 800), ACC)
    return pg
def s7R(t):
    pg = base(16, False).copy()
    framed(pg, t, P('Davon') - 1.5, 'crowd', B7, 'Kundgebung in Berlin, 1933')
    rule(pg, t, P('1928') - 0.3, 960)
    label(pg, t, P('1928') - 0.3, 'NSDAP BEI REICHSTAGSWAHLEN (%)', (110, 1000), sans(34, 800), GREY)
    X.barchart(pg, t, 230, 1470, 230, 140, 330, 37.3, [('1928', 2.6, P('1928'), False), ('1930', 18.3, P('erhalten'), False), ('Juli 1932', 37.3, P('Juli', 131), True)],
               lambda v: ('%.1f' % v).replace('.', ','))
    label(pg, t, P('stärkste'), 'Stärkste Partei im Reichstag', (110, 1580), serif(70, 800), ACC)
    return pg

# ================= SP8: 30 January 1933 / Papen / the Reichstag fire =================
B8L = (110, 600, 1180, 664); B8R = (110, 1000, 1180, 664)
def s8L(t):
    pg = base(17, True).copy(); head(pg, t, P('Am', 138) - 0.1, '30. JANUAR 1933', 'Reichskanzler', 'Adolf Hitler')
    framed(pg, t, P('Am', 138), 'hit1', B8L, 'Adolf Hitler, 1933')
    return pg
def s8R(t):
    pg = base(18, False).copy(); t0 = P('Konservative') - 0.1
    label(pg, t, t0, 'DIE ILLUSION', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, '„Wir haben ihn', (110, 250), serif(100, 400)); label(pg, t, t0 + 0.3, 'uns engagiert.“', (110, 370), serif(100, 800))
    label(pg, t, t0 + 0.6, 'Franz von Papen, Vizekanzler, 1933', (110, 510), italic(38), GREY)
    label(pg, t, P('irrten') - 0.1, 'Sie irrten sich.', (110, 600), serif(110, 800), ACC)
    rule(pg, t, P('Vier') - 1.0, 800)
    label(pg, t, P('Vier') - 1.0, 'BERLIN, 27. FEBRUAR 1933', (110, 840), sans(40, 800), ACC); label(pg, t, P('Vier') - 0.9, 'Der Reichstag brennt', (110, 890), serif(64, 800))
    framed(pg, t, P('Vier') - 1.0, 'fire', B8R, 'Der Reichstag in Flammen')
    return pg

# ================= SP9: Ermächtigungsgesetz, Gleichschaltung / persecution, the oath =================
B9 = (110, 200, 1180, 664); B9U = (780, 1080, 510, 287)
def s9L(t):
    pg = base(19, True).copy()
    framed(pg, t, -1, 'kroll', B9, 'Krolloper, 23. März 1933: Abstimmung über das Ermächtigungsgesetz')
    label(pg, t, -1, 'Gleichschaltung', (110, 950), serif(90, 800))
    for i, (s_, date, tw) in enumerate((('Gewerkschaften', '2. Mai 1933', P('zerschlagen')), ('Parteien', '14. Juli 1933', P('verboten', 163)), ('Freie Presse', '1933', P('gleichgeschaltet')))):
        y = 1090 + i * 190; f = serif(76, 400); label(pg, t, -1, s_, (110, y), f); label(pg, t, -1, date, (110, y + 98), sans(30, 600), GREY)
        strike(pg, t, tw, (100, y + 52), (130 + f.getlength(s_), y + 44), 9)
    framed(pg, t, P('Gewerkschaften') - 0.3, 'union', B9U, 'Gewerkschaftshaus, 2. Mai 1933')
    return pg
def s9R(t):
    pg = base(20, False).copy(); t0 = P('Jüdische') - 0.2
    head(pg, t, t0, '1. APRIL 1933', 'Boykott jüdischer', 'Geschäfte', w2=800, size=96)
    label(pg, t, P('jüdische', 169), '7. APRIL 1933', (110, 540), sans(40, 800), ACC)
    label(pg, t, P('Beamte'), 'Jüdische Beamte', (110, 590), serif(80, 400)); label(pg, t, P('entlassen'), 'werden entlassen', (110, 690), serif(80, 400))
    rule(pg, t, P('Als', 172) - 0.2, 860)
    label(pg, t, P('Als', 172), '2. AUGUST 1934', (110, 900), sans(40, 800), ACC)
    label(pg, t, P('Hindenburg', 172.5), 'Hindenburg stirbt', (110, 950), serif(96, 800))
    label(pg, t, P('Staatsoberhaupt') - 0.2, 'Hitler wird', (110, 1090), serif(70, 400)); label(pg, t, P('Staatsoberhaupt'), '„Führer und Reichskanzler“', (110, 1180), serif(70, 800), ACC)
    label(pg, t, P('Eid'), 'Der Eid der Soldaten:', (110, 1340), serif(56, 400))
    label(pg, t, P('persönlich') - 0.1, 'auf Hitler persönlich', (110, 1420), serif(70, 800))
    rule(pg, t, P('schwören'), 1520, 110, 840, ACC, 6)
    return pg

# ================= SP10: secret and open rearmament =================
def s10L(t):
    pg = base(21, True).copy(); t0 = P('Heimlich') - 0.1
    head(pg, t, t0, '1925 BIS 1933', 'Heimlich', 'aufgerüstet')
    label(pg, t, P('Sowjetunion', 185), 'In der Sowjetunion, fern der Kontrolleure:', (110, 600), italic(40), GREY)
    X.flag(pg, t, P('Sowjetunion', 185), 'su', 1060, 560, 150, 92, pole=False)
    drawing(pg, t, P('Panzern'), 0.6, lambda ph: tank_m(380, 930, 0.42, ph))
    label(pg, t, P('Panzern') + 0.2, 'Panzerschule Kama', (380, 1080), sans(38, 700), TXT, 'ma'); label(pg, t, P('Panzern') + 0.3, 'bei Kasan', (380, 1130), italic(32), GREY, 'ma')
    drawing(pg, t, P('Flugzeugen'), 0.6, lambda ph: biplane_m(1000, 900, 0.48, ph))
    label(pg, t, P('Flugzeugen') + 0.2, 'Fliegerschule', (1000, 1080), sans(38, 700), TXT, 'ma'); label(pg, t, P('Flugzeugen') + 0.3, 'Lipezk', (1000, 1130), italic(32), GREY, 'ma')
    rule(pg, t, P('Nun', 191) - 0.2, 1280)
    label(pg, t, P('offen', 192), 'Ab 1935: offen.', (110, 1330), serif(100, 800), ACC)
    return pg
def s10R(t):
    pg = base(22, False).copy(); t0 = P('Im', 193)
    head(pg, t, t0, '16. MÄRZ 1935', 'Allgemeine', 'Wehrpflicht', w1=400, w2=800)
    framed(pg, t, P('Wehrpflicht') + 0.1, None, (110, 600, 560, 560), 'Soldat der Wehrmacht', still=soldier())
    label(pg, t, P('Luftwaffe', 197), 'Luftwaffe', (740, 620), serif(90, 800)); label(pg, t, P('offiziell', 198), 'offiziell', (740, 730), serif(70, 400), ACC); label(pg, t, P('offiziell', 198) + 0.2, 'vorgestellt', (740, 810), serif(70, 400), ACC)
    drawing(pg, t, P('Luftwaffe', 197), 0.8, lambda ph: monoplane_m(960, 1060, 0.6, ph))
    stamp(pg, t, P('Bruch'), 'VERTRAGSBRUCH', (700, 1420), 96, -6)
    label(pg, t, P('Protesten'), 'Die Reaktion: Proteste. Sonst nichts.', (110, 1600), italic(40), GREY)
    return pg

# ================= the big map, 1936 to 1939 =================
MAPE = Map('E', (SW, PH), (110, 230, SW - 220, 1470), 2.0, 30.0, 46.0)
@functools.lru_cache(None)
def map_paper():
    a = np.concatenate([np.asarray(M.gloss(31)), np.asarray(M.gloss(32))], 1); pg = Image.fromarray(a); d = ImageDraw.Draw(pg)
    for k, c in enumerate((ACC, (150, 150, 150), (205, 205, 205))): d.ellipse((110 + k * 34, 98, 132 + k * 34, 120), fill=c)
    d.text((230, 109), 'CHRONIK DER MACHT', font=sans(28, 600), fill=GREY, anchor='lm'); d.text((SW - 110, 109), 'TEIL 1 · DER WEG IN DEN KRIEG', font=sans(28, 700), fill=ACC, anchor='rm')
    d.text((110, 182), 'Schritt für Schritt', font=serif(60, 800), fill=TXT, anchor='lm'); d.text((640, 186), 'Die Expansion des Deutschen Reiches, 1936 bis 1939', font=italic(34), fill=GREY, anchor='lm')
    return pg
T_RH, T_AT, T_SU = P('marschierten', 208), P('rollten', 228), P('Sudetenland', 236)
T_BM, T_DZ, T_GA, T_PA, T_PL = P('Nun', 273) - 0.2, P('Danzig', 279), P('garantierten'), P('Doch', 287), P('teilten')
PACT = [(21.95, 53.45), (21.7, 53.15), (21.2, 52.75), (21.0, 52.25), (21.35, 51.75), (21.75, 51.2), (21.8, 50.65), (22.3, 50.4), (22.75, 49.95), (22.8, 49.6), (22.6, 49.15)]
@functools.lru_cache(maxsize=2)
def map_spread(tq):
    t = tq / 1000; pg = map_paper().copy(); m = MAPE; k = eout((t - T_RH + 2.4) / 0.8); d = ImageDraw.Draw(pg)
    m.frame(pg, k); m.base_layer(pg, k)
    m.tint(pg, 'ussr', clamp((t - T_PA) / 0.8), (120, 30, 30), 0.10)
    m.hatch(pg, 'rhineland', clamp((t - T_RH) / 0.9)); m.hatch(pg, 'austria', clamp((t - T_AT) / 0.8)); m.hatch(pg, 'sudeten', clamp((t - T_SU) / 0.8))
    m.hatch(pg, 'bohemia', clamp((t - T_BM) / 0.8)); m.hatch(pg, 'danzig', clamp((t - T_DZ) / 0.5), (40, 40, 40), 0.6)
    F = lambda s: sans(s, 700)
    for s_, ll in (('FRANKREICH', (4.2, 47.4)), ('POLEN', (19.6, 52.3)), ('UNGARN', (19.3, 47.0)), ('ITALIEN', (10.5, 46.25)), ('SCHWEIZ', (7.9, 46.75)), ('BELGIEN', (4.6, 50.6)),
                   ('NIEDERLANDE', (5.4, 52.75)), ('DÄNEMARK', (9.3, 55.6)), ('LITAUEN', (23.9, 55.4)), ('RUMÄNIEN', (26.0, 47.3)), ('SOWJETUNION', (28.0, 53.6))):
        m.label(pg, t, T_RH - 2.0, s_, ll, F(26), (150, 150, 150), sw=4)
    m.label(pg, t, T_RH - 1.8, 'DEUTSCHES REICH', (10.6, 52.6), F(40), GREY)
    for s_, ll in (('Nordsee', (5.6, 55.35)), ('Ostsee', (15.6, 55.2))): m.label(pg, t, T_RH - 1.6, s_, ll, italic(30), GREY, sw=0)
    yr, nm = serif(52, 800), sans(32, 800)
    def step(t0, year, name, ll, lead=None):
        x, y = m.mp(*ll)
        if lead is not None and t >= t0 + 0.3:
            b_ = m.mp(*lead); d.line(((x, y + 44), b_), fill=TXT, width=2); d.ellipse((b_[0] - 5, b_[1] - 5, b_[0] + 5, b_[1] + 5), fill=TXT)
        halo(pg, t, t0 + 0.2, year, (x, y - 30), yr, ACC, sw=7); halo(pg, t, t0 + 0.3, name, (x, y + 24), nm, TXT, sw=7)
    step(T_RH, 'März 1936', 'Rheinland', (3.9, 51.9), (6.9, 50.6))
    step(T_AT, 'März 1938', 'Österreich', (13.4, 46.55))
    step(T_SU, 'Okt. 1938', 'Sudetenland', (11.2, 51.45), (12.6, 50.25))
    step(T_BM, 'März 1939', 'Böhmen und Mähren', (17.9, 48.45), (15.6, 49.6))
    if t >= T_DZ:
        m.pin(pg, t, T_DZ, (18.65, 54.35)); m.label(pg, t, T_DZ + 0.1, 'Danzig', (18.65, 54.8), sans(34, 800), ACC, sw=6)
        m.line(pg, t, T_DZ + 0.3, 0.6, [(17.6, 54.75), (17.9, 54.0), (18.3, 53.3), (18.6, 52.9)], ACC, 6, dash=16); m.label(pg, t, T_DZ + 0.7, 'Korridor', (16.6, 53.5), sans(30, 800), ACC, sw=6)
    if P('sagte', 220) <= t < T_AT - 0.2:   # Hitler's line about the Rhineland, on a card in the North Sea corner
        q = clamp((t - P('sagte', 220)) / 0.4) * clamp((T_AT - 0.2 - t) / 0.4)
        d.rectangle((130, 270, 880, 540), fill=fade_col(PAPER, q), outline=fade_col((190, 190, 190), q), width=2)
        for i, s_ in enumerate(('„Die 48 Stunden nach dem Einmarsch', 'ins Rheinland waren die aufregendsten', 'meines Lebens.“')):
            d.text((160, 295 + i * 52), s_, font=italic(38, 500), fill=fade_col(TXT, q))
        d.text((160, 470), 'Adolf Hitler', font=sans(30, 700), fill=fade_col(GREY, q))
    if T_RH + 6 <= t < T_AT:
        x, y = m.mp(3.0, 48.9); X.flag(pg, t, P('Frankreich', 218), 'fr', int(x), int(y), 120, 74, pole=False)
    if t >= T_GA:   # the guarantee, on a card in the North Sea corner
        d.rectangle((130, 270, 760, 640), fill=PAPER, outline=(190, 190, 190), width=2)
        X.flag(pg, t, T_GA, 'uk', 160, 300, 130, 80, 'Großbritannien', pole=False, size=30); X.flag(pg, t, T_GA + 0.3, 'fr', 160, 410, 130, 80, 'Frankreich', pole=False, size=30)
        label(pg, t, T_GA + 0.5, 'garantieren Polens Grenzen', (160, 525), italic(32), GREY); label(pg, t, T_GA + 0.6, '31. März 1939', (160, 575), sans(30, 700), ACC)
        x, y = m.mp(19.6, 51.75); X.flag(pg, t, T_GA + 0.6, 'pl', int(x - 60), int(y + 30), 120, 74, pole=False)
    if t >= T_PA:
        x, y = m.mp(27.2, 54.9); X.flag(pg, t, T_PA + 0.3, 'su', int(x), int(y), 150, 92, pole=False)
        x, y = m.mp(25.6, 48.55); halo(pg, t, T_PA + 0.4, '23. August 1939', (x, y - 34), sans(34, 800), ACC, sw=7); halo(pg, t, T_PA + 0.5, 'Hitler-Stalin-Pakt', (x, y + 14), serif(44, 800), TXT, sw=7)
        m.line(pg, t, T_PL, 1.6, PACT, ACC, 7, dash=18)
        m.label(pg, t, T_PL + 1.2, 'deutsche Interessensphäre', (18.2, 50.75), italic(30), TXT, sw=6); m.label(pg, t, T_PL + 1.4, 'sowjetische Interessensphäre', (25.4, 51.6), italic(30), TXT, sw=6)
        m.label(pg, t, T_PL + 1.6, 'geheimes Zusatzprotokoll', (24.9, 50.3), sans(26, 700), ACC, sw=6)
    return pg
def mapL(t): return map_spread(int(t * 1000)).crop((0, 0, PW, PH))
def mapR(t): return map_spread(int(t * 1000)).crop((PW, 0, SW, PH))

# ================= SP12: Munich / Chamberlain, November pogroms =================
def s12L(t):
    pg = base(25, True).copy(); t0 = P('Im', 241.5) - 0.1
    head(pg, t, t0, 'MÜNCHEN, 29. SEPTEMBER 1938', 'Das Münchner', 'Abkommen')
    if t > t0 + 0.3: drawing(pg, t, t0 + 0.3, 1.2, lambda ph: (*X.table(700, 900, 1.25), []))
    for (x, nm, cc, tw, sub) in ((325, 'Hitler', 'de', P('Hitler', 244), 'Deutsches Reich'), (575, 'Mussolini', 'it', P('Mussolini'), 'Italien'),
                                 (825, 'Chamberlain', 'uk', P('Chamberlain', 247), 'Großbritannien'), (1075, 'Daladier', 'fr', P('Daladier'), 'Frankreich')):
        X.flag(pg, t, tw, cc, x - 55, 560, 110, 68, pole=False)
        label(pg, t, tw + 0.1, nm, (x, 1060), sans(32, 800), TXT, 'ma'); label(pg, t, tw + 0.2, sub, (x, 1104), italic(24), GREY, 'ma')
    X.flag(pg, t, P('Tschechoslowakei', 251.5), 'cs', 820, 1190, 130, 80, pole=False)
    label(pg, t, P('Tschechoslowakei', 251.5) + 0.2, 'Die Tschechoslowakei:', (110, 1340), serif(60, 800)); label(pg, t, P('Tisch'), 'nicht eingeladen', (110, 1420), serif(60, 400), ACC)
    label(pg, t, P('Tisch') + 0.3, 'Abb. · Der leere Stuhl', (110, 1510), italic(30), GREY)
    return pg
def s12R(t):
    pg = base(26, False).copy(); t0 = P('Man', 255) - 0.1
    head(pg, t, t0, 'LONDON, 30. SEPTEMBER 1938', '„Peace for', 'our time.“', w1=400, w2=800, size=110)
    label(pg, t, P('Frieden', 259), 'Frieden für unsere Zeit. Neville Chamberlain', (110, 540), italic(38), GREY)
    drawing(pg, t, P('verkündete'), 0.5, lambda ph: X.paper_m(1050, 800, 0.9, ph))
    if t > P('Wenige', 261):
        k = eout((t - P('Wenige', 261)) / 0.5); d = ImageDraw.Draw(pg); d.rectangle((0, 1040, PW, PH - 160), fill=fade_col((28, 26, 26), k))
        d.text((110, 1100), '9. UND 10. NOVEMBER 1938', font=sans(40, 800), fill=fade_col((214, 72, 64), k, 28))
        d.text((110, 1150), 'Novemberpogrome', font=serif(110, 800), fill=fade_col((246, 243, 236), k, 28))
        if t > P('Synagogen') - 0.3:
            k2 = eout((t - P('Synagogen') + 0.3) / 0.4)
            d.text((110, 1320), 'Synagogen brennen, jüdische Geschäfte werden zerstört,', font=serif(46, 400), fill=fade_col((226, 222, 214), k2, 28))
            d.text((110, 1385), 'rund 30.000 jüdische Männer verschleppt.', font=serif(46, 400), fill=fade_col((226, 222, 214), k2, 28))
    return pg

# ================= SP13: Prague, March 1939 =================
B13L = (110, 600, 1180, 664); B13R = (110, 200, 1180, 664)
def s13L(t):
    pg = base(27, True).copy(); head(pg, t, P('Im', 265.5) - 0.1, 'PRAG, 15. MÄRZ 1939', 'Die Wehrmacht', 'in Prag', w2=400)
    framed(pg, t, P('Im', 265.5), 'tanksc', B13L, 'Deutsche Panzer in Prag, 15. März 1939')
    return pg
def s13R(t):
    pg = base(28, False).copy()
    framed(pg, t, P('Im', 265.5), 'pcrowd', B13R, 'Prager Bürger am Straßenrand')
    label(pg, t, P('Protektorat') - 0.6, 'Protektorat', (110, 980), serif(110, 400)); label(pg, t, P('Protektorat') - 0.4, 'Böhmen und Mähren', (110, 1110), serif(110, 800), ACC)
    label(pg, t, P('erklärt', 272), 'Die Tschechoslowakei hört auf zu bestehen.', (110, 1290), italic(42), GREY)
    return pg

# ================= SP15: Gleiwitz / 4:45 =================
B15S = (110, 560, 1180, 664); B15T = (110, 1330, 620, 349)
def s15L(t):
    pg = base(31, True).copy(); t0 = P('Am', 300) - 0.1
    head(pg, t, t0, '31. AUGUST 1939, ABENDS', 'Sender', 'Gleiwitz', w1=400, w2=800)
    drawing(pg, t, t0 + 0.3, 1.2, lambda ph: X.tower_m(940, 1560, 1.0, ph))
    label(pg, t, P('verkleidete'), 'SS-Männer in Zivil', (110, 700), serif(60, 800)); label(pg, t, P('verkleidete') + 0.3, 'überfallen den eigenen Sender', (110, 780), serif(50, 400))
    stamp(pg, t, P('inszeniert'), 'INSZENIERT', (420, 1080), 100, -8)
    label(pg, t, P('Vorwand'), 'Der Vorwand für den Krieg', (110, 1300), italic(40), GREY)
    return pg
def s15R(t):
    pg = base(32, False).copy(); t0 = P('Am', 310) - 0.1
    label(pg, t, t0, '1. SEPTEMBER 1939', (110, 200), sans(40, 800), ACC)
    label(pg, t, P('um', 311) - 0.1, '4:45 Uhr', (100, 230), serif(220, 800), ACC)
    framed(pg, t, P('Uhr', 312), 'ship2', B15S, 'Die Schleswig-Holstein vor der Westerplatte')
    framed(pg, t, P('Uhr', 312) + 0.3, 'tanks', B15T)
    label(pg, t, P('Uhr', 312) + 0.4, 'Deutsche Truppen', (780, 1360), serif(52, 800)); label(pg, t, P('Uhr', 312) + 0.5, 'überschreiten', (780, 1430), serif(52, 400)); label(pg, t, P('Uhr', 312) + 0.6, 'die Grenze.', (780, 1500), serif(52, 400))
    return pg

# ================= SP16: the declarations of war, the toll =================
def s16L(t):
    pg = base(33, True).copy(); t0 = P('Zwei', 323) - 0.1
    head(pg, t, t0, '3. SEPTEMBER 1939', 'Kriegs-', 'erklärung', w2=800)
    X.flag(pg, t, P('Großbritannien', 324), 'uk', 140, 640, 330, 200, 'Großbritannien', size=54)
    X.flag(pg, t, P('Frankreich', 325), 'fr', 140, 1000, 330, 200, 'Frankreich', size=54)
    label(pg, t, P('Krieg', 327), 'erklären Deutschland den Krieg.', (140, 1340), serif(60, 400))
    return pg
def s16R(t):
    pg = base(34, False).copy(); t0 = P('Zwanzig', 328)
    label(pg, t, t0, '1919', (110, 210), serif(190, 800), GREY); label(pg, t, t0 + 0.3, '1939', (720, 210), serif(190, 800), ACC)
    if t > t0 + 0.2:
        u = eout((t - t0 - 0.2) / 0.3); d = ImageDraw.Draw(pg); xe = lerp(560, 680, u); d.line((560, 330, xe, 330), fill=TXT, width=6)
        if u > 0.9: d.polygon([(xe + 8, 330), (xe - 18, 314), (xe - 18, 346)], fill=TXT)
    label(pg, t, P('Weltkrieg', 330), 'Der Zweite Weltkrieg beginnt.', (110, 470), serif(66, 800))
    rule(pg, t, P('sechs', 333) - 0.2, 640)
    label(pg, t, P('sechs', 333), '6', (100, 650), serif(300, 800), ACC); label(pg, t, P('Jahre', 333.5), 'Jahre Krieg', (330, 800), serif(80, 400))
    label(pg, t, P('sechzig'), 'über 60 Millionen', (110, 1060), serif(130, 800), ACC); label(pg, t, P('Menschen', 336), 'Tote', (110, 1220), serif(100, 400))
    return pg

# ================= SP17: the end page: part 2 and the call to subscribe =================
MAPP = Map('pl', (PW, PH), (180, 820, 1040, 760), 13.0, 26.0, 48.6)
def arrow(pg, m, t, t0, a_, b_, dur=0.8):
    if t < t0: return
    u = eio((t - t0) / dur); A = m.mp(*a_); B = m.mp(*b_); E = (lerp(A[0], B[0], u), lerp(A[1], B[1], u)); d = ImageDraw.Draw(pg)
    d.line((A, E), fill=ACC, width=16); ang = math.atan2(E[1] - A[1], E[0] - A[0]); hd = 46
    d.polygon([(E[0] + 20 * math.cos(ang), E[1] + 20 * math.sin(ang)), (E[0] - hd * math.cos(ang - 0.6), E[1] - hd * math.sin(ang - 0.6)), (E[0] - hd * math.cos(ang + 0.6), E[1] - hd * math.sin(ang + 0.6))], fill=ACC)
def s17L(t):
    pg = base(35, True).copy(); t0 = VEND + 1.0; m = MAPP
    label(pg, t, t0, 'FORTSETZUNG FOLGT', (110, 200), sans(46, 800), ACC)
    label(pg, t, t0 + 0.2, 'TEIL 2', (100, 250), serif(250, 900))
    label(pg, t, t0 + 0.5, 'Der Überfall auf Polen', (110, 560), serif(84, 400), GREY)
    if t >= t0 + 0.7:   # Poland and the three thrusts of September 1939
        k = eout((t - t0 - 0.7) / 0.6); m.frame(pg, k); stamp_ink(pg, m.ground().point(lambda v: int(v * 0.45 * k)), (0, 0), (150, 150, 150))
        stamp_ink(pg, m.outline('poland').point(lambda v: int(v * k)), (0, 0), TXT); m.tint(pg, 'poland', k, ACC, 0.06)
        m.label(pg, t, t0 + 0.9, 'POLEN', (20.0, 52.0), sans(40, 800), TXT); m.label(pg, t, t0 + 1.0, 'Warschau', (21.0, 52.55), sans(26, 700), GREY, sw=4)
        m.pin(pg, t, t0 + 1.0, (21.0, 52.23), TXT, 9)
        for i, (a_, b_) in enumerate((((14.6, 52.6), (19.0, 52.3)), ((19.6, 54.4), (20.6, 52.9)), ((19.2, 49.4), (20.3, 50.9)))):
            arrow(pg, m, t, t0 + 1.2 + i * 0.35, a_, b_)
        m.label(pg, t, t0 + 2.4, '1. September 1939', (16.0, 49.25), sans(30, 800), ACC, sw=5)
    return pg
def icon_thumb(d, cx, cy, s, col):
    d.rounded_rectangle((cx - 60 * s, cy - 10 * s, cx - 30 * s, cy + 70 * s), int(6 * s), fill=col)
    d.rounded_rectangle((cx - 22 * s, cy - 10 * s, cx + 62 * s, cy + 70 * s), int(14 * s), fill=col)
    d.polygon([(cx - 22 * s, cy - 6 * s), (cx + 2 * s, cy - 70 * s), (cx + 22 * s, cy - 72 * s), (cx + 24 * s, cy - 40 * s), (cx + 14 * s, cy - 6 * s)], fill=col)
def icon_share(d, cx, cy, s, col):
    d.polygon([(cx + 10 * s, cy - 60 * s), (cx + 70 * s, cy - 5 * s), (cx + 10 * s, cy + 50 * s), (cx + 10 * s, cy + 22 * s), (cx - 30 * s, cy + 20 * s), (cx - 62 * s, cy + 60 * s),
               (cx - 56 * s, cy + 10 * s), (cx - 20 * s, cy - 28 * s), (cx + 10 * s, cy - 30 * s)], fill=col)
def icon_bell(d, cx, cy, s, col, swing=0.0):
    a = math.radians(swing); R = lambda x, y: (cx + (x * math.cos(a) - y * math.sin(a)) * s, cy - 60 * s + (x * math.sin(a) + y * math.cos(a)) * s)
    d.polygon([R(-12, 0), R(-36, 20), R(-44, 70), R(-58, 100), R(58, 100), R(44, 70), R(36, 20), R(12, 0)], fill=col)
    c = R(0, 116); d.ellipse((c[0] - 14 * s, c[1] - 14 * s, c[0] + 14 * s, c[1] + 14 * s), fill=col); c = R(0, -6); d.ellipse((c[0] - 10 * s, c[1] - 10 * s, c[0] + 10 * s, c[1] + 10 * s), fill=col)
def s17R(t):
    pg = base(36, False).copy(); t0 = VEND + 1.6
    label(pg, t, t0, 'Gefällt dir die Serie?', (110, 220), serif(96, 800))
    d = ImageDraw.Draw(pg)
    for i, (nm, ic) in enumerate((('Liken', icon_thumb), ('Teilen', icon_share), ('Abonnieren', icon_bell))):
        tt = t0 + 0.5 + i * 0.6
        if t < tt: continue
        u = clamp((t - tt) / 0.45); sc = 1.0 + 0.35 * math.sin(math.pi * u) * (1 - u)
        y = 520 + i * 260; cx = 230; col = ACC if (i == 2 or t > tt + 0.5) else TXT
        d.ellipse((cx - 95 * sc, y - 95 * sc + 40, cx + 95 * sc, y + 95 * sc + 40), outline=fade_col((200, 200, 200), u), width=4)
        if i == 2: ic(d, cx, y + 40, 0.95 * sc, fade_col(col, u), 18 * math.sin((t - tt) * 9) * math.exp(-(t - tt) * 1.5))
        else: ic(d, cx, y + 40, 0.95 * sc, fade_col(col, u))
        d.text((400, y + 40), nm, font=serif(90, 800 if i == 2 else 700), fill=fade_col(ACC if i == 2 else TXT, u), anchor='lm')
    label(pg, t, t0 + 2.6, 'damit du Teil 2 nicht verpasst.', (110, 1320), serif(60, 400), GREY)
    return pg

# ================= the magazine: spreads, turns, camera =================
SPREADS = [(s0L, s0R), (s1L, s1R), (s2L, s2R), (s3L, s3R), (s4L, s4R), (s5L, s5R), (s6L, s6R), (s7L, s7R), (s8L, s8R), (s9L, s9R), (s10L, s10R),
           (mapL, mapR), (s12L, s12R), (s13L, s13R), (mapL, mapR), (s15L, s15R), (s16L, s16R), (s17L, s17R)]
def TS(word_t): return word_t - 1.0          # a turn that ends just before the first word of the new spread
TURNS = [TS(P('Und', 10.5)) + 0.25, P('Im', 18) - 0.6, TS(P('Am', 38.5)), TS(P('Das', 50)), TS(P('Als', 67)), TS(P('Im', 91)), TS(P('Im', 111)), TS(P('Am', 138)),
         P('Mit', 156.5) - 1.2, TS(P('Heimlich')), TS(P('Am', 206.5)), TS(P('Im', 241.5)), TS(P('Im', 265.5)), TS(P('Nun', 273)), TS(P('Am', 300)),
         P('Zwei', 323) - 1.05, VEND + 0.3]
def mc(lon, lat): return MAPE.mp(lon, lat)
CAMS = [(0,) + fill('L', B0)]
def cam(t_, c, cd=CD): CAMS.append((t_ - cd,) + tuple(c) + (cd,))
cam(P('durfte') - 0.05, OV, 1.1)                                                   # out of the tank film onto the magazine
cam(P('Das', 6) + 0.1, fr('R', 820, 1600))
cam(TURNS[0] + 0.3, OV, 0.7); cam(TURNS[0] + 2.0, fill('L', B1))                   # into the ship film
cam(P('Wie', 15) - 0.05, (MID, 820, 0.66))
cam(TURNS[1] + 0.3, OV, 0.6); cam(P('Im', 18) + 1.0, fr('L', 170, 1300))
cam(P('Kaiser') + 0.1, fill('L', B2)); cam(P('Viele') + 0.3, fr('L', 1250, 1700))
cam(P('Bald') - 0.05, fr('R', 170, 900)); cam(P('Heer', 33) - 0.05, fr('R', 520, 1650))
cam(TURNS[2] + 0.3, OV, 0.6); cam(P('Am', 38.5) + 1.0, fr('L', 170, 1500))
cam(P('Es', 44) - 0.05, fr('R', 170, 1600)); cam(P('Korridor') - 0.1, (PW + 900, 600, 1.5)); cam(P('Ostpreußen') + 0.9, fr('R', 170, 1600))
cam(TURNS[3] + 0.3, OV, 0.6); cam(P('Das', 50) + 0.9, fr('L', 170, 700))
cam(P('Panzer', 53) - 0.05, fr('L', 640, 1300)); cam(P('Rheinland', 56) - 0.25, fr('L', 1300, 1700))
cam(P('Deutschland', 58.4) - 0.05, fr('R', 170, 800)); cam(P('Sieger') - 0.25, fr('R', 820, 1720))
cam(TURNS[4] + 0.3, OV, 0.6); cam(P('Als', 67) + 0.9, fr('L', 170, 950)); cam(P('Truppen', 70) - 0.25, fr('L', 560, 1700))
cam(P('Regierung', 74) - 0.05, fr('R', 140, 920)); cam(P('Im', 79.5) - 0.05, fr('R', 880, 1560)); cam(P('Brot', 84) - 0.1, fr('R', 1220, 1700))
cam(TURNS[5] + 0.3, OV, 0.6); cam(P('Im', 91) + 0.9, fr('L', 170, 1340)); cam(P('Adolf', 93) - 0.1, fill('L', B6)); cam(P('Der', 96) + 0.2, fr('L', 1000, 1650))
cam(P('Haft', 98) - 0.25, fr('R', 170, 900)); cam(P('Dann', 101.5) - 0.05, fr('R', 920, 1700))
cam(TURNS[6] + 0.3, OV, 0.6); cam(P('Im', 111) + 0.9, fr('L', 170, 1010)); cam(P('Fabriken') - 0.3, fr('L', 1030, 1700))
cam(P('Davon') - 0.05, fill('R', B7)); cam(P('1928') - 0.1, fr('R', 940, 1700))
cam(TURNS[7] + 0.3, OV, 0.6); cam(P('Am', 138) + 1.2, fill('L', B8L)); cam(P('Konservative') - 0.05, fr('R', 170, 760))
cam(P('Vier') - 0.05, fill('R', B8R))
cam(TURNS[8] - 0.05, OV, 0.9); cam(TURNS[8] + 1.9, fill('L', B9)); cam(P('Gewerkschaften') - 0.05, fr('L', 930, 1700))
cam(P('Jüdische') - 0.1, fr('R', 170, 800)); cam(P('Als', 172) - 0.1, fr('R', 850, 1560))
cam(TURNS[9] + 0.3, OV, 0.6); cam(P('Heimlich') + 0.9, fr('L', 170, 700)); cam(P('Sowjetunion', 185) - 0.05, fr('L', 540, 1460))
cam(P('Im', 193) - 0.05, fr('R', 170, 1250)); cam(P('Bruch') - 0.1, fr('R', 1000, 1700))
rx, ry = mc(6.6, 51.0); ax_, ay_ = mc(13.6, 48.6); sx, sy = mc(13.6, 50.6); dx_, dy_ = mc(18.6, 53.6); px_, py_ = mc(22.0, 51.6)
cam(TURNS[10] + 0.3, OV, 0.6); cam(T_RH - 0.1, (rx + 120, ry - 120, 1.2)); cam(P('sagte', 220) - 0.1, (rx + 60, ry - 300, 1.0))
cam(T_AT - 0.1, (ax_, ay_, 1.1)); cam(T_SU - 0.1, (sx, sy, 1.1))
cam(TURNS[11] + 0.3, OV, 0.6); cam(P('Im', 241.5) + 0.9, fr('L', 170, 1560)); cam(P('Man', 255) - 0.05, fr('R', 170, 1000)); cam(P('Wenige', 261) - 0.05, fr('R', 1040, 1650))
cam(TURNS[12] + 0.3, OV, 0.6); cam(P('Im', 265.5) + 1.2, fill('L', B13L)); cam(P('Böhmen') - 0.6, fill('R', B13R)); cam(P('Protektorat') - 0.5, fr('R', 940, 1360))
cam(TURNS[13] + 0.3, OV, 0.6); cam(T_DZ - 0.1, (dx_, dy_, 1.3)); cam(T_GA - 0.1, (MID - 250, 760, 0.82)); cam(T_PA - 0.05, (px_, py_ + 40, 0.95))
cam(TURNS[14] + 0.3, OV, 0.6); cam(P('Am', 300) + 0.9, fr('L', 170, 1660))
cam(P('Am', 310) - 0.05, fr('R', 170, 1700)); cam(P('eröffnete') - 0.4, fill('R', B15S)); cam(P('und', 319) - 0.05, fill('R', B15T))
cam(TURNS[15] + 0.05, OV, 0.9); cam(P('Zwei', 323) + 0.9, fr('L', 170, 1420)); cam(P('Zwanzig', 328) - 0.05, fr('R', 170, 1360))
cam(TURNS[16] + 0.3, OV, 0.6); cam(TURNS[16] + 2.0, (MID, 860, 0.68))
MAG = Book(SPREADS, TURNS, CAMS, spine=100)
# captions on screen while a film fills the frame: in when the camera has arrived, out together with the pull-back
CAPS = [('Deutsche Panzer, 1939', None), ('1. September 1939', 'Linienschiff Schleswig-Holstein'), ('Deutschland, 1918/19', 'Das Kaiserreich ist am Ende'),
        ('München, November 1923', 'Adolf Hitler, Aufnahme Anfang der 1930er Jahre'), ('Berlin, 1933', 'Kundgebung'), ('Berlin, 30. Januar 1933', 'Adolf Hitler wird Reichskanzler'),
        ('Berlin, 27. Februar 1933', 'Der Reichstag brennt'), ('Berlin, 23. März 1933', 'Krolloper: Abstimmung über das Ermächtigungsgesetz'),
        ('Prag, 15. März 1939', 'Die Wehrmacht marschiert ein'), ('Prag, 15. März 1939', 'Prager Bürger am Straßenrand'),
        ('Danzig, 1. September 1939', 'Die Schleswig-Holstein beschießt die Westerplatte'), ('1. September 1939', 'Deutsche Truppen überschreiten die Grenze')]
OVL = []; _fills = [i for i, c in enumerate(CAMS) if c[3] > 1.5]
for (i, (c1, c2)) in zip(_fills, CAPS):
    c = CAMS[i]; arr = c[0] + (c[4] if len(c) > 4 else 0) if i else 0.0; nxt = CAMS[i + 1][0] if i + 1 < len(CAMS) else T_END
    OVL.append((max(0.0, arr - 0.5), nxt + 0.5, c1, c2))
for j in range(len(OVL) - 1):   # back-to-back films: the first caption gives way to the next
    if OVL[j][1] > OVL[j + 1][0]: OVL[j] = (OVL[j][0], OVL[j + 1][0] + 0.15, OVL[j][2], OVL[j][3])
def frame(t):
    img = MAG(t)
    for a, b, c1, c2 in OVL:
        if a <= t <= b: caption(img, t, a, c1, c2, b)
    if t > T_END - 1.2: img = blend(img, Image.new('RGB', (W, H), (0, 0, 0)), (t - (T_END - 1.2)) / 1.2)
    return img
SEG = [(0.0, MAG)]
def isbook(fn): return True

if __name__ == '__main__':
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[2:]]
        for t in ts: frame(t).save(LB + 'chk/p_%06.2f.jpg' % t, quality=86)
        n = len(ts); Pc = Image.new('RGB', (3 * 640, ((n + 2) // 3) * 360))
        for i, t in enumerate(ts): Pc.paste(Image.open(LB + 'chk/p_%06.2f.jpg' % t).resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
        Pc.save(LB + 'chk/prev.jpg', quality=88); sys.exit()
    if sys.argv[1] == 'pages':   # every spread in its final state, for layout checks
        for i, (L, R) in enumerate(SPREADS):
            te = (TURNS[i] - 0.05) if i < len(TURNS) else T_END - 1.5
            spread_img(L(te), R(te)).convert('RGB').resize((SW // 3, PH // 3)).save(LB + 'chk/sp_%02d.jpg' % i, quality=85)
        sys.exit()
    if sys.argv[1] == 'T': print(round(T_END, 3)); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
