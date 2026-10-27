# "Deutschland im Zweiten Weltkrieg", Teil 1, long version (16:9): film hook, the magazine cover in the colours of the
# republic's flag, then spreads (moving ink drawings, waving flags, charts, maps from historical borders) cut with archive film.
import functools
from lcore import *
from lmap import Map
import ldraw as X
from ldraw import counter
from drawings import drawing, tank_m, biplane_m, uboat_m, monoplane_m, loaf_m, banknote
T_END = VEND + 7.0
P = lambda w_, a=0.0: ws(w_, a)          # global time of a spoken word (start - 0.04)

# ---------- stills ----------
@functools.lru_cache(None)
def soldier():
    im = Image.open(S + 'teil1/drive/BG2_Bild_4.jpg').convert('RGB'); r = 9; x, y = 113, 84
    reg = im.crop((x - r * 2, y - r * 2, x + r * 2, y + r * 2)); bl = reg.resize((4, 4), Image.BILINEAR).resize(reg.size, Image.BICUBIC)
    m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).ellipse((r * 2 - r - 3, r * 2 - r - 3, r * 2 + r + 3, r * 2 + r + 3), fill=255)
    im.paste(Image.composite(bl, reg, m.filter(ImageFilter.GaussianBlur(2))), (x - r * 2, y - r * 2)); return im.convert('L')

# ---------- the cover: masthead on paper, a duotone photo printed in black, red and gold, the series title on it ----------
@functools.lru_cache(None)
def cover_static():
    pg = M.gloss(40).copy(); d = ImageDraw.Draw(pg)
    d.text((PW / 2, 150), 'CHRONIK DER MACHT', font=serif(118, 900), fill=TXT, anchor='mm')
    d.line((110, 240, PW - 110, 240), fill=TXT, width=3); d.line((110, 250, PW - 110, 250), fill=TXT, width=1)
    d.text((110, 285), 'GESCHICHTSMAGAZIN', font=sans(28, 700), fill=GREY, anchor='lm'); d.text((PW - 110, 285), 'DIE SERIE · TEIL 1', font=sans(28, 700), fill=ACC, anchor='rm')
    g = clip_at('crowd', 2.0); w, h = g.size; bx0, by0, bw, bh = 0, 340, PW, 1170
    sc = max(bw / w, bh / h); cw, ch = bw / sc, bh / sc; ph = np.asarray(g.resize((bw, bh), Image.LANCZOS, box=((w - cw) / 2, (h - ch) / 2, (w + cw) / 2, (h + ch) / 2)), np.float32) / 255
    ph = np.clip((ph - 0.08) * 1.25, 0, 1)
    out = np.zeros((bh, bw, 3), np.float32)
    for i, (c0, c1) in enumerate((((10, 10, 12), (92, 90, 88)), ((70, 10, 12), (200, 46, 40)), ((120, 84, 10), (232, 182, 40)))):
        y0, y1 = int(i * bh / 3), int((i + 1) * bh / 3); p_ = ph[y0:y1][..., None]
        out[y0:y1] = np.array(c0, np.float32) * (1 - p_) + np.array(c1, np.float32) * p_
    r = np.random.default_rng(4); out += r.normal(0, 5, out.shape[:2])[..., None]
    pg.paste(Image.fromarray(out.clip(0, 255).astype(np.uint8)), (bx0, by0))
    L = Image.new('RGBA', pg.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    dl.text((PW / 2, by0 + bh / 6), 'DEUTSCHLAND', font=serif(176, 900), fill=(250, 248, 242, 255), anchor='mm')
    dl.text((PW / 2, by0 + bh / 2 - 10), 'IM ZWEITEN', font=serif(132, 700), fill=(250, 248, 242, 255), anchor='mm')
    dl.text((PW / 2, by0 + bh / 2 + 130), 'WELTKRIEG', font=serif(132, 700), fill=(250, 248, 242, 255), anchor='mm')
    dl.text((PW / 2, by0 + bh * 5 / 6), 'TEIL 1 · DER WEG IN DEN KRIEG', font=sans(54, 800), fill=(24, 20, 14, 255), anchor='mm')
    sh = Image.new('RGBA', pg.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), (0, 0), L.getchannel('A'))
    pgA = pg.convert('RGBA'); pgA.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (4, 7)); pgA.alpha_composite(L); pg = pgA.convert('RGB'); d = ImageDraw.Draw(pg)
    d.text((PW / 2, 1590), '1918 bis 1939', font=serif(74, 700), fill=TXT, anchor='mm')
    d.text((PW / 2, 1680), 'Versailles · Inflation · Machtergreifung · Aufrüstung · München · Polen', font=sans(30, 500), fill=GREY, anchor='mm')
    return pg
def cover(t): return cover_static()

# ---------- the hook page ----------
def hook_page(t):
    pg = base(1, False).copy(); t0 = P('durfte')
    label(pg, t, t0 - 0.2, '1919', (110, 210), serif(190, 800), ACC)
    body(pg, t, 110, 470, 'durfte Deutschland keinen einzigen Panzer besitzen.', t0 - 0.1, accent=('keinen', 'einzigen', 'Panzer'), bold=('Deutschland',), size=70, lh=96)
    X.flag(pg, t, P('Deutschland', 3) - 0.1, 'de', 130, 760, 170, 104, 'Weimarer Republik', 'Flagge ab 1919', size=36)
    drawing(pg, t, P('keinen'), 0.7, lambda ph: tank_m(720, 1230, 0.9, ph))
    strike(pg, t, P('Panzer', 4) + 0.15, (300, 1010), (1150, 1450), 11)
    label(pg, t, P('besitzen') + 0.2, 'Abb. 1 · Panzer: verboten', (110, 1530), italic(34), GREY)
    return pg
HOOK = Book([(None, hook_page)], [], [(0, 2100, 860, 1.05)])

# ---------- spread A1: November 1918 / the stab-in-the-back legend ----------
def a1L(t):
    pg = base(2, True).copy()
    label(pg, t, 0, 'NOVEMBER 1918', (110, 200), sans(40, 800), ACC)
    label(pg, t, 0, 'Das Ende', (110, 250), serif(120, 400)); label(pg, t, 0, 'des Kaiserreichs', (110, 390), serif(120, 800))
    photo(pg, t, P('Kaiser') - 0.6, 'f1b', (110, 600, 1180, 700), 'Deutschland, 1918/19', start=0.0, speed=1.0)
    label(pg, t, P('Kaiser'), '9. November', (110, 1430), sans(36, 700), ACC); label(pg, t, P('Kaiser') + 0.2, 'Der Kaiser dankt ab', (110, 1475), serif(54, 700))
    label(pg, t, P('Republik'), 'Die Republik wird ausgerufen', (110, 1550), serif(54, 400))
    label(pg, t, P('kein', 27), 'Kein feindlicher Soldat auf deutschem Boden.', (110, 1640), italic(36), GREY)
    return pg
def a1R(t):
    pg = base(3, False).copy()
    label(pg, t, P('Bald') - 0.2, 'DIE LÜGE', (110, 200), sans(40, 800), ACC)
    label(pg, t, P('Bald'), 'Die Dolchstoß-', (110, 250), serif(120, 800)); label(pg, t, P('Bald') + 0.1, 'legende', (110, 390), serif(120, 800))
    label(pg, t, P('Heer', 32), '„Im Felde', (190, 600), serif(110, 400), TXT); label(pg, t, P('unbesiegt'), 'unbesiegt“', (190, 730), serif(110, 400), ACC)
    if t > P('Heer', 32): drawing(pg, t, P('Heer', 32), 1.0, lambda ph: (*X.helmet(700, 1150, 1.25), []))
    label(pg, t, P('erdolcht') - 0.4, 'Abb. 2 · Stahlhelm M1916', (110, 1360), italic(34), GREY)
    stamp(pg, t, P('erdolcht'), 'LEGENDE', (980, 1520), 84, -7)
    return pg

# ---------- spread A2: Versailles and the losses of 1919 ----------
MAP19 = Map('m19', (PW, PH), (110, 330, 1180, 900), 4.5, 24.5, 46.6)
def a2L(t):
    pg = base(4, True).copy(); t0 = P('Am', 37.5)
    label(pg, t, t0, '28. JUNI 1919', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.2, 'Der Vertrag', (110, 250), serif(120, 400)); label(pg, t, P('Versailles', 40), 'von Versailles', (110, 390), serif(120, 800), ACC)
    photo(pg, t, P('unterzeichnete') - 0.2, 'f1a', (110, 620, 1180, 760), 'Archivaufnahme, 1919', speed=0.8)
    return pg
def a2R(t):
    pg = base(5, False).copy(); t0 = P('Es', 43) - 0.3; m = MAP19
    label(pg, t, t0, 'Deutschland 1914 und 1919', (110, 200), serif(80, 800))
    if t >= t0:
        k = eout((t - t0) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=('reich',), outline=('reich',))
        m.hatch(pg, 'lost1919', clamp((t - P('verlor')) / 0.9), (120, 120, 120), a=0.55, edge=False, step=12)
        m.hatch(pg, 'danzig', clamp((t - P('verlor') - 0.4) / 0.4), (120, 120, 120), a=0.55, edge=False, step=12)
        for s_, ll, t1, f in (('Elsass-Lothringen', (6.9, 48.55), P('verlor') + 0.5, sans(26, 700)), ('an Frankreich', (6.9, 48.2), P('verlor') + 0.6, italic(24)),
                              ('Posen', (17.0, 52.35), P('verlor') + 0.8, sans(26, 700)), ('an Polen', (17.0, 52.05), P('verlor') + 0.9, italic(24)),
                              ('Polnischer Korridor', (17.6, 53.75), P('Korridor'), sans(28, 800)), ('Danzig', (18.65, 54.62), P('Korridor') + 0.3, sans(26, 700)),
                              ('Freie Stadt', (18.65, 54.92), P('Korridor') + 0.4, italic(24)), ('Ostpreußen', (21.0, 54.05), P('Ostpreußen'), sans(30, 800)),
                              ('DEUTSCHES REICH', (11.0, 51.6), t0 + 0.4, sans(34, 700))):
            m.label(pg, t, t1, s_, ll, f, ACC if s_ == 'Polnischer Korridor' else TXT)
        if t > P('Korridor'):   # the corridor itself, in red
            m.line(pg, t, P('Korridor'), 0.6, [(17.6, 54.75), (17.9, 54.0), (18.3, 53.3), (18.6, 52.9)], ACC, 6, dash=14)
    label(pg, t, P('Achtel'), '1/8', (110, 1290), serif(170, 800), ACC); label(pg, t, P('Achtel') + 0.2, 'des Gebiets verloren', (420, 1360), serif(60, 400))
    label(pg, t, P('Achtel') + 0.4, 'Grau schraffiert: Gebietsverluste 1919', (110, 1520), italic(30), GREY)
    return pg

# ---------- spread A3: the army of 100,000; banned weapons; war guilt and reparations ----------
def a3L(t):
    pg = base(6, True).copy(); t0 = P('Heer', 49)
    label(pg, t, t0 - 0.2, 'DAS HEER', (110, 200), sans(40, 800), ACC)
    label(pg, t, P('100.000'), '100.000', (100, 230), serif(250, 800), ACC); label(pg, t, P('Mann', 51), 'Mann, nicht mehr.', (110, 540), serif(70, 400))
    rule(pg, t, P('Panzer', 52), 670)
    for (fn, cx, cy, sc, name, tw) in ((tank_m, 300, 930, 0.42, 'Panzer', P('Panzer', 52)), (biplane_m, 700, 900, 0.5, 'Luftwaffe', P('Luftwaffe', 52.5)), (uboat_m, 1100, 950, 0.48, 'U-Boote', P('U-Boote'))):
        drawing(pg, t, tw, 0.6, lambda ph, fn=fn, cx=cx, cy=cy, sc=sc: fn(cx, cy, sc, ph)); label(pg, t, tw + 0.3, name, (cx, 1060), sans(40, 700), TXT, 'ma')
    stamp(pg, t, P('verboten', 54), 'VERBOTEN', (700, 1215), 96, -5)
    rule(pg, t, P('Rheinland', 55), 1230)
    label(pg, t, P('Rheinland', 55), 'Das Rheinland:', (110, 1280), serif(70, 800)); label(pg, t, P('entmilitarisiert'), 'entmilitarisiert', (110, 1370), serif(70, 400), ACC)
    label(pg, t, P('entmilitarisiert') + 0.3, 'keine Soldaten, keine Festungen', (110, 1470), italic(34), GREY)
    return pg
def a3R(t):
    pg = base(7, False).copy(); t0 = P('Deutschland', 57.5)
    label(pg, t, t0, 'ARTIKEL 231', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.2, 'Die Schuld', (110, 250), serif(120, 800)); label(pg, t, t0 + 0.4, 'am Krieg', (110, 390), serif(120, 400))
    for i, s_ in enumerate(('„… dass Deutschland und seine Verbündeten', 'als Urheber für alle Verluste und Schäden', 'verantwortlich sind …“')):
        label(pg, t, P('Verantwortung') + 0.2 * i, s_, (110, 580 + i * 56), italic(38), GREY)
    rule(pg, t, P('Sieger'), 820)
    label(pg, t, P('Sieger'), 'REPARATIONEN · 1921', (110, 860), sans(40, 800), ACC)
    counter(pg, t, P('132') - 0.6, 1.3, 132, (110, 900), serif(230, 800), ACC, expo=False)
    label(pg, t, P('Milliarden', 63.5), 'Milliarden Goldmark', (110, 1150), serif(74, 800))
    drawing(pg, t, P('Goldmark') - 0.3, 0.3, lambda ph: X.coins_m(1050, 1560, 1.0, ph))
    return pg

# ---------- spread B1: the Ruhr, 1923 / hyperinflation ----------
def b1L(t):
    pg = base(8, True).copy(); t0 = P('Als', 66)
    label(pg, t, t0, 'JANUAR 1923', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.2, 'Die Ruhr-', (110, 250), serif(120, 800)); label(pg, t, t0 + 0.3, 'besetzung', (110, 390), serif(120, 800))
    X.flag(pg, t, P('französische'), 'fr', 130, 610, 190, 116, 'Frankreich', size=40)
    X.flag(pg, t, P('belgische'), 'be', 130, 800, 190, 116, 'Belgien', size=40)
    drawing(pg, t, P('Truppen', 69) - 0.2, 1.0, lambda ph: X.factory_m(860, 1290, 0.62, ph))
    label(pg, t, P('Ruhrgebiet') + 0.3, 'Abb. 3 · Zeche im Ruhrgebiet', (650, 1420), italic(30), GREY)
    label(pg, t, P('Widerstand'), 'Passiver Widerstand', (110, 1530), serif(64, 800)); label(pg, t, P('bezahlen'), 'bezahlt mit frisch gedrucktem Geld', (110, 1620), serif(48, 400), ACC)
    return pg
def b1R(t):
    pg = base(9, False).copy(); t0 = P('Regierung', 72.5) + 0.2
    if t > P('druckte'):
        notes = X.notes_m(140, 160, 1120, 520, t - P('druckte'))
        ink(pg, t, -1, 0.001, notes, wd=3, a=0.55 * clamp((t - P('druckte')) / 0.5) * clamp((P('Dollar') + 1.0 - t) / 0.8))
    label(pg, t, t0, 'NOVEMBER 1923', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, 'Hyper-', (110, 250), serif(120, 800)); label(pg, t, t0 + 0.2, 'inflation', (110, 390), serif(120, 800))
    label(pg, t, P('Dollar') - 0.2, '1 Dollar =', (110, 620), serif(70, 400))
    counter(pg, t, P('Dollar'), 1.3, 4.2e12, (110, 700), serif(110, 800), ACC)
    label(pg, t, P('Billionen') + 0.2, 'Mark', (110, 840), serif(60, 400))
    rule(pg, t, P('Brot', 84), 960)
    drawing(pg, t, P('Brot', 84), 0.6, lambda ph: loaf_m(1040, 1100, 0.8, ph))
    label(pg, t, P('Brot', 84), 'Ein Brot in Berlin:', (110, 1010), serif(56, 400)); label(pg, t, P('Hunderte', 85), 'Hunderte', (110, 1090), serif(80, 800), ACC)
    label(pg, t, P('Milliarden', 85.5), 'Milliarden Mark', (110, 1190), serif(80, 800), ACC)
    if t > P('Wer'):
        L, sh = banknote(700, 1480, 880, 300); ink(pg, t, P('Wer'), 0.7, L, wd=3); ink(pg, t, P('Wer') + 0.7, 0.3, sh, wd=2, a=0.35)
        label(pg, t, P('Wer') + 0.5, 'REICHSBANKNOTE', (700, 1400), sans(32, 700), TXT, 'mm'); label(pg, t, P('Wer') + 0.6, '100 Billionen Mark', (700, 1480), serif(60, 800), TXT, 'mm')
    stamp(pg, t, P('nichts', 88), 'WERTLOS', (720, 1500), 110, -9)
    return pg

# ---------- spread B2: the Munich putsch / the golden twenties ----------
def b2L(t):
    pg = base(10, True).copy(); t0 = P('Im', 90)
    label(pg, t, t0, 'MÜNCHEN, 9. NOVEMBER 1923', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.2, 'Der Hitler-', (110, 250), serif(120, 800)); label(pg, t, t0 + 0.3, 'Putsch', (110, 390), serif(120, 800))
    photo(pg, t, P('Adolf', 92), 'hitler_b', (110, 600, 1180, 700), 'Adolf Hitler, Aufnahme Anfang der 1930er Jahre', start=13.4, speed=0.5)
    stamp(pg, t, P('scheiterte'), 'GESCHEITERT', (700, 1520), 100, -6)
    return pg
def b2R(t):
    pg = base(11, False).copy(); t0 = P('Haft', 97)
    label(pg, t, t0, 'FESTUNGSHAFT', (110, 200), sans(40, 800), ACC); label(pg, t, t0 + 0.1, 'Landsberg', (110, 250), serif(110, 800))
    if t > t0: drawing(pg, t, t0, 0.7, lambda ph: (*X.prison(330, 620, 0.62), []))
    if t > P('Buch'): drawing(pg, t, P('Buch'), 0.6, lambda ph: (*X.book(880, 620, 0.62), []))
    label(pg, t, P('Mein') , '„Mein Kampf“, 1925', (880, 800), italic(34), GREY, 'ma')
    rule(pg, t, P('Dann', 100.5), 930)
    label(pg, t, P('Dann', 100.5), 'DIE GOLDENEN ZWANZIGER', (110, 970), sans(40, 800), ACC)
    label(pg, t, P('Währung'), 'Rentenmark', (110, 1030), serif(80, 800)); label(pg, t, P('Währung') + 0.3, 'stoppt die Inflation', (560, 1055), serif(50, 400))
    label(pg, t, P('amerikanische'), 'US-Kredite', (110, 1150), serif(80, 800)); label(pg, t, P('amerikanische') + 0.3, 'Dawes-Plan, 1924', (560, 1175), serif(50, 400))
    X.axes(pg, t, P('Wirtschaft', 107), (110, 1300, 1180, 330))
    X.stock(pg, t, P('Wirtschaft', 107), 2.2, (110, 1300, 1180, 330), [(0, 0.1), (0.15, 0.22), (0.3, 0.3), (0.45, 0.42), (0.6, 0.5), (0.75, 0.62), (0.9, 0.7), (1.0, 0.75)], crash_at=2)
    label(pg, t, P('geliehenem') , 'auf Kredit gebaut', (1290, 1650), italic(36), ACC, 'ra')
    return pg

# ---------- spread B3: the crash of 1929 / unemployment and the rise of the NSDAP ----------
def b3L(t):
    pg = base(12, True).copy(); t0 = P('Im', 110.5)
    label(pg, t, t0, 'NEW YORK, OKTOBER 1929', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.2, 'Der Börsen-', (110, 250), serif(120, 800)); label(pg, t, t0 + 0.3, 'krach', (110, 390), serif(120, 800))
    X.axes(pg, t, t0 + 0.3, (110, 600, 1180, 620))
    pts = [(0, 0.35), (0.1, 0.42), (0.2, 0.5), (0.3, 0.58), (0.4, 0.66), (0.5, 0.76), (0.58, 0.86), (0.62, 0.9), (0.68, 0.55), (0.74, 0.62), (0.8, 0.38), (0.88, 0.3), (1.0, 0.12)]
    X.stock(pg, t, t0 + 0.4, P('zusammen', 113) - t0 + 0.2, (110, 600, 1180, 620), pts, crash_at=0.55, wd=7)
    label(pg, t, P('zusammen', 113), 'Schwarzer Donnerstag, 24. Oktober 1929', (110, 1250), italic(36), GREY)
    label(pg, t, P('forderten', 115), 'US-Banken fordern', (110, 1380), serif(70, 800)); label(pg, t, P('Kredite', 116), 'ihre Kredite zurück', (110, 1470), serif(70, 400), ACC)
    return pg
def b3R(t):
    pg = base(13, False).copy(); t0 = P('Fabriken')
    label(pg, t, t0 - 0.2, 'ARBEITSLOSE IN DEUTSCHLAND (MIO.)', (110, 200), sans(36, 800), GREY)
    X.barchart(pg, t, 160, 720, 200, 90, 440, 6.0, [('1929', 1.9, t0, False), ('1930', 3.1, t0 + 0.4, False), ('1931', 4.5, t0 + 0.8, False), ('1932', 6.0, P('sechs', 120), True)],
               lambda v: ('%.1f' % v).replace('.', ','))
    label(pg, t, P('Millionen', 120.5), '6 Millionen', (1290, 260), serif(90, 800), ACC, 'ra')
    rule(pg, t, P('1928') - 0.3, 860)
    label(pg, t, P('1928') - 0.3, 'NSDAP BEI REICHSTAGSWAHLEN (%)', (110, 900), sans(36, 800), GREY)
    X.barchart(pg, t, 230, 1560, 230, 140, 520, 37.3, [('1928', 2.6, P('1928'), False), ('1930', 18.3, P('erhalten'), False), ('Juli 1932', 37.3, P('Juli', 130), True)],
               lambda v: ('%.1f' % v).replace('.', ','))
    label(pg, t, P('stärkste'), 'stärkste Partei', (1290, 960), serif(70, 800), ACC, 'ra')
    return pg

# ---------- spread C0: 30 January 1933 / Papen's illusion ----------
def c0L(t):
    pg = base(14, True).copy(); t0 = 0
    label(pg, t, t0, '30. JANUAR 1933', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0, 'Reichskanzler', (110, 250), serif(120, 800)); label(pg, t, t0, 'Adolf Hitler', (110, 390), serif(120, 400))
    photo(pg, t, t0, 'hitler_b', (110, 600, 1180, 700), 'Adolf Hitler, 1933', start=20.0, speed=0.5)
    return pg
def c0R(t):
    pg = base(15, False).copy(); t0 = P('Konservative') - 0.2
    label(pg, t, t0, 'DIE ILLUSION', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.2, '“', (90, 230), serif(300, 800), ACC)
    label(pg, t, t0 + 0.4, 'Wir haben ihn', (110, 470), serif(110, 400)); label(pg, t, t0 + 0.6, 'uns engagiert.', (110, 600), serif(110, 800))
    label(pg, t, t0 + 1.0, 'Franz von Papen, Vizekanzler, 1933', (110, 760), italic(38), GREY)
    rule(pg, t, P('Sie', 148), 900)
    label(pg, t, P('irrten'), 'Sie irrten sich.', (110, 960), serif(100, 800), ACC)
    return pg

# ---------- spread C1: Gleichschaltung / persecution / the oath ----------
def c1L(t):
    pg = base(16, True).copy()
    label(pg, t, 0, 'FRÜHJAHR UND SOMMER 1933', (110, 200), sans(40, 800), ACC)
    label(pg, t, 0, 'Gleich-', (110, 250), serif(120, 800)); label(pg, t, 0, 'schaltung', (110, 390), serif(120, 800))
    for i, (s_, date, tw) in enumerate((('Gewerkschaften', '2. Mai 1933', P('zerschlagen')), ('Parteien', '14. Juli 1933', P('verboten', 164)), ('Freie Presse', '1933', P('gleichgeschaltet')))):
        y = 640 + i * 260; label(pg, t, 0, s_, (110, y), serif(100, 400)); label(pg, t, 0, date, (110, y + 140), sans(32, 600), GREY)
        f = serif(100, 400); w_ = f.getlength(s_); strike(pg, t, tw, (100, y + 70), (130 + w_, y + 58), 10)
    stamp(pg, t, P('gleichgeschaltet') + 0.4, 'VERBOTEN', (1000, 1520), 96, -8)
    return pg
def c1R(t):
    pg = base(17, False).copy(); t0 = P('Jüdische') - 0.2
    label(pg, t, t0, '1. APRIL 1933', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, 'Boykott jüdischer', (110, 250), serif(96, 800)); label(pg, t, t0 + 0.2, 'Geschäfte', (110, 365), serif(96, 800))
    label(pg, t, P('jüdische', 168.5), '7. APRIL 1933', (110, 540), sans(40, 800), ACC)
    label(pg, t, P('Beamte'), 'Jüdische Beamte', (110, 590), serif(80, 400)); label(pg, t, P('entlassen'), 'werden entlassen', (110, 690), serif(80, 400))
    rule(pg, t, P('Als', 171), 860)
    label(pg, t, P('Als', 171), '2. AUGUST 1934', (110, 900), sans(40, 800), ACC)
    label(pg, t, P('Hindenburg', 171.5), 'Hindenburg stirbt', (110, 950), serif(96, 800))
    label(pg, t, P('Staatsoberhaupt') - 0.2, 'Hitler wird', (110, 1090), serif(70, 400)); label(pg, t, P('Staatsoberhaupt'), '„Führer und Reichskanzler“', (110, 1180), serif(70, 800), ACC)
    label(pg, t, P('Eid'), 'Der Eid der Soldaten:', (110, 1340), serif(56, 400))
    label(pg, t, P('persönlich') - 0.1, 'auf Hitler persönlich', (110, 1420), serif(70, 800))
    rule(pg, t, P('schwören'), 1520, 110, 840, ACC, 6)
    return pg

# ---------- spread C2: secret and open rearmament ----------
def c2L(t):
    pg = base(18, True).copy(); t0 = P('Heimlich') - 0.1
    label(pg, t, t0, '1925 BIS 1933', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, 'Heimlich', (110, 250), serif(120, 800)); label(pg, t, t0 + 0.2, 'aufgerüstet', (110, 390), serif(120, 400))
    label(pg, t, P('Sowjetunion', 184), 'In der Sowjetunion, fern der Kontrolleure:', (110, 600), italic(40), GREY)
    X.flag(pg, t, P('Sowjetunion', 184), 'su', 1060, 560, 150, 92, pole=False)
    drawing(pg, t, P('Panzern'), 0.6, lambda ph: tank_m(380, 930, 0.42, ph))
    label(pg, t, P('Panzern') + 0.3, 'Panzerschule Kama', (380, 1080), sans(38, 700), TXT, 'ma'); label(pg, t, P('Panzern') + 0.4, 'bei Kasan', (380, 1130), italic(32), GREY, 'ma')
    drawing(pg, t, P('Flugzeugen'), 0.6, lambda ph: biplane_m(1000, 900, 0.48, ph))
    label(pg, t, P('Flugzeugen') + 0.3, 'Fliegerschule', (1000, 1080), sans(38, 700), TXT, 'ma'); label(pg, t, P('Flugzeugen') + 0.4, 'Lipezk', (1000, 1130), italic(32), GREY, 'ma')
    rule(pg, t, P('Nun', 190), 1280)
    label(pg, t, P('offen', 191), 'Ab 1935: offen.', (110, 1330), serif(100, 800), ACC)
    return pg
def c2R(t):
    pg = base(19, False).copy(); t0 = P('Im', 192)
    label(pg, t, t0, '16. MÄRZ 1935', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, 'Allgemeine', (110, 250), serif(120, 400)); label(pg, t, P('Wehrpflicht'), 'Wehrpflicht', (110, 390), serif(120, 800))
    photo(pg, t, P('Wehrpflicht') + 0.2, None, (110, 600, 560, 620), 'Soldat der Wehrmacht', still=soldier())
    label(pg, t, P('Luftwaffe', 197), 'Luftwaffe', (740, 640), serif(90, 800)); label(pg, t, P('offiziell', 198), 'offiziell', (740, 750), serif(70, 400), ACC); label(pg, t, P('offiziell', 198) + 0.2, 'vorgestellt', (740, 830), serif(70, 400), ACC)
    drawing(pg, t, P('Luftwaffe', 197), 0.8, lambda ph: monoplane_m(900, 1080, 0.68, ph))
    stamp(pg, t, P('Bruch'), 'VERTRAGSBRUCH', (700, 1440), 96, -6)
    label(pg, t, P('Protesten') , 'Die Reaktion: Proteste. Sonst nichts.', (110, 1620), italic(40), GREY)
    return pg

# ---------- the big map spread, 1936 to 1939 ----------
MAPE = Map('E', (SW, PH), (110, 230, SW - 220, 1470), 2.0, 30.0, 46.0)
@functools.lru_cache(None)
def map_paper():
    a = np.concatenate([np.asarray(M.gloss(31)), np.asarray(M.gloss(32))], 1); pg = Image.fromarray(a); d = ImageDraw.Draw(pg)
    for k, c in enumerate((ACC, (150, 150, 150), (205, 205, 205))): d.ellipse((110 + k * 34, 98, 132 + k * 34, 120), fill=c)
    d.text((230, 109), 'CHRONIK DER MACHT', font=sans(28, 600), fill=GREY, anchor='lm'); d.text((SW - 110, 109), 'TEIL 1 · DER WEG IN DEN KRIEG', font=sans(28, 700), fill=ACC, anchor='rm')
    d.text((110, 192), 'Schritt für Schritt', font=serif(60, 800), fill=TXT, anchor='lm'); d.text((640, 196), 'Die Expansion des Deutschen Reiches, 1936 bis 1939', font=italic(34), fill=GREY, anchor='lm')
    return pg
T_RH, T_AT, T_SU = P('marschierten', 207), P('rollten', 227), P('Sudetenland', 235)
T_BM, T_DZ, T_GA, T_PA, T_PL = P('Nun', 272), P('Danzig', 278), P('garantierten'), P('Doch', 286), P('teilten')
PACT = [(21.95, 53.45), (21.7, 53.15), (21.2, 52.75), (21.0, 52.25), (21.35, 51.75), (21.75, 51.2), (21.8, 50.65), (22.3, 50.4), (22.75, 49.95), (22.8, 49.6), (22.6, 49.15)]
@functools.lru_cache(maxsize=2)
def map_spread(tq):
    t = tq / 1000; pg = map_paper().copy(); m = MAPE; k = eout((t - T_RH + 2.6) / 0.8)
    m.frame(pg, k); m.base_layer(pg, k)
    m.tint(pg, 'ussr', clamp((t - T_PA) / 0.8), (120, 30, 30), 0.10)
    m.hatch(pg, 'rhineland', clamp((t - T_RH) / 0.9)); m.hatch(pg, 'austria', clamp((t - T_AT) / 0.8)); m.hatch(pg, 'sudeten', clamp((t - T_SU) / 0.8))
    m.hatch(pg, 'bohemia', clamp((t - T_BM) / 0.8))
    m.hatch(pg, 'danzig', clamp((t - T_DZ) / 0.5), (40, 40, 40), 0.6)
    F = lambda s: sans(s, 700)
    for s_, ll in (('FRANKREICH', (4.2, 47.4)), ('POLEN', (20.2, 52.2)), ('UNGARN', (19.3, 47.0)), ('ITALIEN', (10.5, 46.25)), ('SCHWEIZ', (7.9, 46.75)), ('BELGIEN', (4.6, 50.6)),
                   ('NIEDERLANDE', (5.6, 52.5)), ('DÄNEMARK', (9.3, 55.6)), ('LITAUEN', (23.9, 55.4)), ('RUMÄNIEN', (26.0, 47.3)), ('SOWJETUNION', (28.0, 53.0))):
        m.label(pg, t, T_RH - 2.0, s_, ll, F(26), (150, 150, 150), sw=4)
    m.label(pg, t, T_RH - 1.8, 'DEUTSCHES REICH', (10.6, 52.6), F(40), GREY)
    for s_, ll in (('Nordsee', (5.8, 54.9)), ('Ostsee', (15.6, 55.2))): m.label(pg, t, T_RH - 1.6, s_, ll, italic(30), GREY, sw=0)
    yr, nm = serif(54, 800), sans(32, 800)
    def step(t0, year, name, ll, lead=None):
        x, y = m.mp(*ll)
        if lead is not None and t >= t0 + 0.3:
            b_ = m.mp(*lead); ImageDraw.Draw(pg).line(((x, y + 34), b_), fill=TXT, width=2); ImageDraw.Draw(pg).ellipse((b_[0] - 5, b_[1] - 5, b_[0] + 5, b_[1] + 5), fill=TXT)
        halo(pg, t, t0 + 0.2, year, (x, y - 26), yr, ACC); halo(pg, t, t0 + 0.3, name, (x, y + 16), nm, TXT)
    step(T_RH, 'März 1936', 'Rheinland', (3.9, 52.1), (6.9, 50.6))
    step(T_AT, 'März 1938', 'Österreich', (13.4, 46.62))
    step(T_SU, 'Okt. 1938', 'Sudetenland', (11.4, 51.35), (12.6, 50.2))
    step(T_BM, 'März 1939', 'Böhmen und Mähren', (17.6, 48.55), (15.6, 49.6))
    if t >= T_DZ:
        m.pin(pg, t, T_DZ, (18.65, 54.35)); m.label(pg, t, T_DZ + 0.1, 'Danzig', (18.65, 54.75), sans(34, 800), ACC)
        m.line(pg, t, T_DZ + 0.3, 0.6, [(17.6, 54.75), (17.9, 54.0), (18.3, 53.3), (18.6, 52.9)], ACC, 6, dash=16); m.label(pg, t, T_DZ + 0.7, 'Korridor', (16.9, 53.6), sans(28, 700), ACC)
    # Hitler's line about the Rhineland, in the North Sea corner while the zone is on screen
    if P('sagte', 219) <= t < T_AT - 0.2:
        q = clamp((t - P('sagte', 219)) / 0.4) * clamp((T_AT - 0.2 - t) / 0.4); d = ImageDraw.Draw(pg)
        d.rectangle((130, 280, 860, 300 + 3 * 52 + 60), fill=fade_col(PAPER, q, 249), outline=fade_col((200, 200, 200), q), width=2)
        for i, s_ in enumerate(('„Die 48 Stunden nach dem Einmarsch', 'ins Rheinland waren die aufregendsten', 'meines Lebens.“')):
            d.text((150, 300 + i * 52), s_, font=italic(38, 500), fill=fade_col(TXT, q), stroke_width=5, stroke_fill=PAPER)
        d.text((150, 300 + 3 * 52 + 10), 'Adolf Hitler', font=sans(30, 700), fill=fade_col(GREY, q), stroke_width=5, stroke_fill=PAPER)
    # France stood by
    if T_RH + 6 <= t < T_AT:
        x, y = m.mp(3.0, 48.6); X.flag(pg, t, P('Frankreich', 217), 'fr', int(x), int(y), 120, 74, pole=False)
    # the guarantee and the pact, in the North Sea corner
    if t >= T_GA:
        X.flag(pg, t, T_GA, 'uk', 150, 290, 130, 80, 'Großbritannien', pole=False, size=30); X.flag(pg, t, T_GA + 0.3, 'fr', 150, 400, 130, 80, 'Frankreich', pole=False, size=30)
        halo(pg, t, T_GA + 0.5, 'garantieren Polens Grenzen', (150, 540), italic(32), GREY, 'lm', 4); halo(pg, t, T_GA + 0.5, '31. März 1939', (150, 585), sans(30, 700), ACC, 'lm', 4)
        x, y = m.mp(20.2, 51.6); X.flag(pg, t, T_GA + 0.6, 'pl', int(x - 60), int(y + 30), 120, 74, pole=False)
    if t >= T_PA:
        x, y = m.mp(26.6, 54.6); X.flag(pg, t, T_PA + 0.3, 'su', int(x), int(y), 150, 92, pole=False)
        x, y = m.mp(24.0, 49.4); halo(pg, t, T_PA + 0.4, '23. August 1939', (x, y - 30), sans(34, 800), ACC); halo(pg, t, T_PA + 0.5, 'Hitler-Stalin-Pakt', (x, y + 14), serif(44, 800), TXT)
        m.line(pg, t, T_PL, 1.6, PACT, ACC, 7, dash=18)
        m.label(pg, t, T_PL + 1.2, 'deutsche Interessensphäre', (18.4, 51.0), italic(30), TXT, sw=5); m.label(pg, t, T_PL + 1.4, 'sowjetische Interessensphäre', (25.2, 51.5), italic(30), TXT, sw=5)
        m.label(pg, t, T_PL + 1.6, 'geheimes Zusatzprotokoll', (21.0, 50.1), sans(26, 700), ACC, sw=5)
    return pg
def mapL(t): return map_spread(int(t * 1000)).crop((0, 0, PW, PH))
def mapR(t): return map_spread(int(t * 1000)).crop((PW, 0, SW, PH))

# ---------- spread E2: Munich / Chamberlain / November pogroms ----------
def e2L(t):
    pg = base(22, True).copy(); t0 = P('Im', 240)
    label(pg, t, t0, 'MÜNCHEN, 29. SEPTEMBER 1938', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, 'Das Münchner', (110, 250), serif(120, 800)); label(pg, t, t0 + 0.2, 'Abkommen', (110, 390), serif(120, 400))
    if t > t0 + 0.3: drawing(pg, t, t0 + 0.3, 1.2, lambda ph: (*X.table(700, 900, 1.25), []))
    for (x, nm, cc, tw) in ((325, 'Hitler', None, P('Hitler', 244)), (575, 'Mussolini', 'it', P('Mussolini')), (825, 'Chamberlain', 'uk', P('Chamberlain', 246)), (1075, 'Daladier', 'fr', P('Daladier'))):
        if cc: X.flag(pg, t, tw, cc, x - 55, 560, 110, 68, pole=False)
        else: label(pg, t, tw, 'Deutsches Reich', (x, 594), italic(28), GREY, 'mm')
        label(pg, t, tw + 0.1, nm, (x, 1060), sans(32, 800), TXT, 'ma')
    X.flag(pg, t, P('Tschechoslowakei', 250), 'cs', 820, 1190, 130, 80, pole=False)
    label(pg, t, P('Tschechoslowakei', 250) + 0.2, 'Die Tschechoslowakei:', (110, 1330), serif(60, 800)); label(pg, t, P('Tisch'), 'nicht eingeladen', (110, 1410), serif(60, 400), ACC)
    label(pg, t, P('Tisch') + 0.3, 'Abb. · Der leere Stuhl', (110, 1500), italic(30), GREY)
    return pg
def e2R(t):
    pg = base(23, False).copy(); t0 = P('verkündete') - 0.4
    label(pg, t, t0, 'LONDON, 30. SEPTEMBER 1938', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, '„Peace for', (110, 250), serif(110, 400)); label(pg, t, t0 + 0.2, 'our time.“', (110, 380), serif(110, 800), ACC)
    label(pg, t, P('Frieden', 258), 'Frieden für unsere Zeit. Neville Chamberlain', (110, 540), italic(38), GREY)
    drawing(pg, t, P('verkündete'), 0.5, lambda ph: X.paper_m(1050, 790, 0.9, ph))
    if t > P('Wenige', 260):
        k = eout((t - P('Wenige', 260)) / 0.5); d = ImageDraw.Draw(pg); d.rectangle((0, 1040, PW, PH - 160), fill=fade_col((28, 26, 26), k))
        d.text((110, 1100), '9. UND 10. NOVEMBER 1938', font=sans(40, 800), fill=fade_col((214, 72, 64), k, 28))
        d.text((110, 1150), 'Novemberpogrome', font=serif(110, 800), fill=fade_col((246, 243, 236), k, 28))
        if t > P('Synagogen'):
            k2 = eout((t - P('Synagogen')) / 0.4)
            d.text((110, 1320), 'Synagogen brennen, jüdische Geschäfte werden zerstört,', font=serif(46, 400), fill=fade_col((226, 222, 214), k2, 28))
            d.text((110, 1385), 'rund 30.000 jüdische Männer verschleppt.', font=serif(46, 400), fill=fade_col((226, 222, 214), k2, 28))
    return pg

# ---------- spread F: Gleiwitz / 4:45 ----------
def f1L(t):
    pg = base(24, True).copy(); t0 = P('Am', 299)
    label(pg, t, t0, '31. AUGUST 1939, ABENDS', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, 'Sender', (110, 250), serif(120, 400)); label(pg, t, t0 + 0.2, 'Gleiwitz', (110, 390), serif(120, 800))
    drawing(pg, t, t0 + 0.3, 1.2, lambda ph: X.tower_m(900, 1560, 1.0, ph))
    label(pg, t, P('verkleidete'), 'SS-Männer in Zivil', (110, 700), serif(60, 800)); label(pg, t, P('verkleidete') + 0.3, 'überfallen den eigenen Sender', (110, 780), serif(50, 400))
    stamp(pg, t, P('inszeniert'), 'INSZENIERT', (420, 1080), 100, -8)
    label(pg, t, P('Vorwand'), 'Der Vorwand für den Krieg', (110, 1300), italic(40), GREY)
    return pg
def f1R(t):
    pg = base(25, False).copy(); t0 = P('Am', 308.5)
    label(pg, t, t0, '1. SEPTEMBER 1939', (110, 200), sans(40, 800), ACC)
    label(pg, t, P('um', 311) - 0.1, '4:45', (100, 220), serif(300, 800), ACC); label(pg, t, P('Uhr', 311), 'Uhr', (760, 420), serif(90, 400))
    drawing(pg, t, P('Uhr', 311) + 0.3, 0.8, lambda ph: X.ship_m(680, 1050, 1.15, ph))
    label(pg, t, P('Linienschiff') , 'Linienschiff Schleswig-Holstein', (110, 1260), serif(60, 800)); label(pg, t, P('Feuer', 315), 'eröffnet das Feuer auf die Westerplatte', (110, 1340), serif(50, 400), ACC)
    return pg

# ---------- spread G: the declarations of war / the toll; end page ----------
def g1L(t):
    pg = base(26, True).copy(); t0 = P('Zwei', 322)
    label(pg, t, t0, '3. SEPTEMBER 1939', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, 'Kriegs-', (110, 250), serif(120, 800)); label(pg, t, t0 + 0.2, 'erklärung', (110, 390), serif(120, 800))
    X.flag(pg, t, P('Großbritannien', 324), 'uk', 140, 640, 330, 200, 'Großbritannien', size=54)
    X.flag(pg, t, P('Frankreich', 325), 'fr', 140, 1000, 330, 200, 'Frankreich', size=54)
    label(pg, t, P('Krieg', 326.5), 'erklären Deutschland den Krieg.', (140, 1340), serif(60, 400))
    return pg
def g1R(t):
    pg = base(27, False).copy(); t0 = P('Zwanzig', 327)
    label(pg, t, t0, '1919', (110, 210), serif(190, 800), GREY); label(pg, t, t0 + 0.3, '1939', (700, 210), serif(190, 800), ACC)
    if t > t0 + 0.2:   # an arrow from 1919 to 1939
        u = eout((t - t0 - 0.2) / 0.3); d = ImageDraw.Draw(pg); xe = lerp(545, 670, u); d.line((545, 330, xe, 330), fill=TXT, width=6)
        if u > 0.9: d.polygon([(xe + 8, 330), (xe - 18, 314), (xe - 18, 346)], fill=TXT)
    label(pg, t, P('Weltkrieg', 330), 'Der Zweite Weltkrieg beginnt.', (110, 470), serif(66, 800))
    rule(pg, t, P('sechs', 332), 640)
    label(pg, t, P('sechs', 332), '6', (100, 650), serif(300, 800), ACC); label(pg, t, P('Jahre', 332.5), 'Jahre Krieg', (330, 800), serif(80, 400))
    label(pg, t, P('sechzig'), 'über 60 Millionen', (110, 1060), serif(130, 800), ACC); label(pg, t, P('Menschen', 335), 'Tote', (110, 1220), serif(100, 400))
    return pg
def g2L(t):
    pg = base(28, True).copy(); t0 = VEND + 0.9
    label(pg, t, t0, 'FORTSETZUNG FOLGT', (110, 260), sans(46, 800), ACC)
    label(pg, t, t0 + 0.2, 'TEIL 2', (100, 310), serif(260, 900))
    label(pg, t, t0 + 0.5, 'Der Überfall auf Polen', (110, 640), serif(84, 400), GREY)
    return pg
def g2R(t):
    pg = base(29, False).copy(); t0 = VEND + 1.3
    label(pg, t, t0, 'Gefällt dir die Serie?', (110, 300), serif(90, 800))
    for i, s_ in enumerate(('Abonnieren', 'Liken', 'Teilen')): label(pg, t, t0 + 0.4 + i * 0.3, s_, (110, 460 + i * 120), serif(90, 700), ACC if i == 0 else TXT)
    label(pg, t, t0 + 1.5, 'damit du Teil 2 nicht verpasst.', (110, 860), serif(56, 400), GREY)
    return pg

# ---------- the books and their cameras (spread coords: left page centre x 700, right page centre x 2100) ----------
def mc(lon, lat): return MAPE.mp(lon, lat)
LC, RC, MID = 700, 2100, PW
def fr(side, y0, y1, smax=1.3):
    """camera on a band of a page: side 'L' / 'R', page rows y0..y1 fill the frame height (with a margin)"""
    s = min(smax, 1000 / (y1 - y0), 1840 / PW); return ((LC if side == 'L' else RC), (y0 + y1) / 2, s)
OV = (MID, 905, 0.60)   # the whole spread on the desk
def K(t, c): return (t,) + tuple(c)
HOOK = Book([(None, hook_page)], [], [K(0, fr('R', 170, 1100)), K(P('keinen') + 0.2, fr('R', 700, 1600))])
BOOK_A = Book([(None, cover), (a1L, a1R), (a2L, a2R), (a3L, a3R), (b1L, b1R), (b2L, b2R), (b3L, b3R)],
              [P('Im', 17.5) - 0.35, P('Am', 37.5) - 0.5, P('Heer', 49) - 0.75, P('Als', 66) - 0.6, P('Im', 90) - 0.55, P('Im', 110.5) - 0.55],
              [K(0, (RC, 905, 0.58)), K(P('Wie', 15) + 0.1, (RC, 905, 0.66)), K(P('Im', 17.5) - 0.3, OV), K(P('Im', 17.5) + 0.8, fr('L', 170, 1350)),
               K(P('Viele'), fr('L', 560, 1720)), K(P('Bald') - 0.2, fr('R', 170, 900)), K(P('Heer', 32), fr('R', 520, 1600)),
               K(P('Am', 37.5) - 0.6, OV), K(P('Am', 37.5) + 0.5, fr('L', 170, 1420)), K(P('Es', 43) - 0.4, fr('R', 170, 1300)),
               K(P('Korridor') - 0.3, (PW + 920, 620, 1.55)), K(P('Ostpreußen') + 0.6, fr('R', 400, 1600)),
               K(P('Heer', 49) - 0.85, OV), K(P('Heer', 49) + 0.3, fr('L', 170, 700)), K(P('Panzer', 52) - 0.2, fr('L', 640, 1250)), K(P('Rheinland', 55) - 0.1, fr('L', 1000, 1560)),
               K(P('Deutschland', 57.5) - 0.3, fr('R', 170, 800)), K(P('Sieger') - 0.3, fr('R', 820, 1720)),
               K(P('Als', 66) - 0.7, OV), K(P('Als', 66) + 0.4, fr('L', 170, 950)), K(P('Truppen', 69), fr('L', 560, 1700)), K(P('Regierung', 72.5) - 0.3, fr('R', 140, 900)),
               K(P('Dollar') - 0.6, fr('R', 560, 1300)), K(P('Wer') - 0.3, fr('R', 940, 1700)),
               K(P('Im', 90) - 0.65, OV), K(P('Im', 90) + 0.4, fr('L', 170, 1400)), K(P('Hitler', 96.5) - 0.3, fr('R', 170, 900)), K(P('Dann', 100.5) - 0.2, fr('R', 930, 1700)),
               K(P('Im', 110.5) - 0.65, OV), K(P('Im', 110.5) + 0.4, fr('L', 170, 1300)), K(P('forderten', 115) - 0.2, fr('L', 700, 1560)), K(P('Fabriken') - 0.4, fr('R', 170, 850)),
               K(P('1928') - 0.6, fr('R', 860, 1680)), K(P('stärkste') + 0.4, OV)])
BOOK_C = Book([(c0L, c0R), (c1L, c1R), (c2L, c2R)], [P('Mit', 155.5), P('Heimlich') - 0.6],
              [K(0, fr('R', 170, 1100)), K(P('Mit', 155.5) + 1.2, fr('L', 170, 1500)), K(P('Jüdische') - 0.3, fr('R', 170, 800)), K(P('Als', 171) - 0.2, fr('R', 850, 1560)),
               K(P('Heimlich') - 0.7, OV), K(P('Heimlich') + 0.4, fr('L', 170, 700)), K(P('Sowjetunion', 184) - 0.2, fr('L', 540, 1460)), K(P('Im', 192) - 0.3, fr('R', 170, 1250)),
               K(P('Bruch') - 0.4, fr('R', 900, 1700))])
rx, ry = mc(7.2, 50.6); ax_, ay_ = mc(13.6, 48.8); sx, sy = mc(14.0, 50.6); dx_, dy_ = mc(19.0, 53.6); px_, py_ = mc(21.5, 51.6)
BOOK_E = Book([(mapL, mapR), (e2L, e2R), (mapL, mapR)], [P('Im', 240) - 0.6, P('Im', 264.5) + 0.3],
              [K(0, OV), (T_RH - 0.5, rx + 120, ry - 120, 1.25), (P('sagte', 219) - 0.3, rx, ry - 330, 1.05), (T_AT - 0.5, ax_, ay_, 1.15), (T_SU - 0.4, sx, sy, 1.15),
               K(P('Im', 240) - 0.7, OV), K(P('Im', 240) + 0.4, fr('L', 170, 1560)), K(P('verkündete') - 0.6, fr('R', 170, 1000)), K(P('Wenige', 260) - 0.2, fr('R', 1000, 1680)),
               K(P('Im', 264.5), OV), (T_DZ - 0.3, dx_, dy_, 1.35), (T_GA - 0.4, MID - 300, 700, 0.85), (T_PA, px_, py_ + 40, 1.0), (T_PL + 2.2, px_ - 100, py_, 0.9)],
              spine=60)
BOOK_F = Book([(f1L, f1R)], [], [K(0, fr('L', 170, 1660)), K(P('Am', 308.5) - 0.2, fr('R', 170, 1420))])
BOOK_G = Book([(g1L, g1R), (g2L, g2R)], [VEND + 0.5],
              [K(0, fr('L', 170, 1420)), K(P('Zwanzig', 327) - 0.3, fr('R', 170, 1360)), K(VEND + 0.4, OV), K(VEND + 1.6, (MID, 760, 0.70))])

# ---------- the timeline: (start, kind, fn) ----------
def F(name, t0, start=0.0, speed=1.0, cap=None, cap2=None, t1=None, **kw):
    return lambda t: film(t, name, t0, start, speed, cap=cap, cap2=cap2, t1=t1, **kw)
SEG = []
def seg(a, fn): SEG.append((a, fn))
seg(0.0, F('tanks', 0.0, 0.2))
seg(P('durfte') - 0.12, HOOK)
seg(P('Das', 5) - 0.1, F('street', P('Das', 5) - 0.1, 0.4))
seg(P('das', 8) - 0.1, F('crowd', P('das', 8) - 0.1, 0.3))
seg(P('Und', 10) - 0.15, F('ship2', P('Und', 10) - 0.15, 1.5, fy=0.4))
seg(P('Wie', 15) - 0.15, BOOK_A)
seg(P('Davon') - 0.1, F('crowd', P('Davon') - 0.1, 2.0, 0.9))
seg(P('1928') - 0.25, BOOK_A)
seg(P('Am', 136.5) - 0.1, F('hitler_b', P('Am', 136.5) - 0.1, 0.4, cap='Berlin, 30. Januar 1933', cap2='Adolf Hitler wird Reichskanzler', t1=P('Konservative') - 0.15))
seg(P('Konservative') - 0.15, BOOK_C)
seg(P('Vier') - 0.15, F('fire', P('Vier') - 0.15, 3.6, 0.95, cap='Berlin, 27. Februar 1933', cap2='Der Reichstag brennt', t1=P('Mit', 155.5) - 0.1))
seg(P('Mit', 155.5) - 0.1, F('kroll', P('Mit', 155.5) - 0.1, 0.2, 0.9, cap='Berlin, 23. März 1933', cap2='Die Krolloper: Abstimmung über das Ermächtigungsgesetz', t1=P('Gewerkschaften') - 0.1))
seg(P('Gewerkschaften') - 0.1, F('union', P('Gewerkschaften') - 0.1, 0.3, 0.9, cap='2. Mai 1933', cap2='Ein besetztes Gewerkschaftshaus', t1=P('alle', 163) - 0.1))
seg(P('alle', 163) - 0.1, BOOK_C)
seg(P('Am', 205) - 0.25, BOOK_E)
seg(P('Im', 264.5) - 0.1, F('tanks', P('Im', 264.5) - 0.1, 4.3, 0.9, cap='Prag, 15. März 1939', cap2='Die Wehrmacht marschiert ein', t1=P('Böhmen') - 0.1))
seg(P('Böhmen') - 0.1, F('pcrowd', P('Böhmen') - 0.1, 0.1, 0.95))
seg(P('erklärt', 271) - 0.2, F('psquare', P('erklärt', 271) - 0.2, 0.2, 0.9))
seg(P('Nun', 272) - 0.15, BOOK_E)
seg(P('Am', 299) - 0.15, BOOK_F)
seg(P('eröffnete') - 0.1, F('ship2', P('eröffnete') - 0.1, 2.5, 0.9, cap='Danzig, 1. September 1939', cap2='Die Schleswig-Holstein beschießt die Westerplatte', t1=P('und', 318.5) - 0.1))
seg(P('und', 318.5) - 0.1, F('tanks', P('und', 318.5) - 0.1, 0.4, 1.0))
seg(P('Zwei', 322) - 0.15, BOOK_G)
XF = 0.22   # half the crossfade between two films or two books
BOX = (460, 259, 1000, 562)   # where a film sits as a photo on the page before the camera flies into it
def photo_zoom(bg, fimg, u, a=1.0):
    """u 0: the film is a photo (BOX) on the page; u 1: the camera has flown in and the film fills the frame"""
    e = eio(u); bx, by, bw, bh = BOX; rx0, ry0 = lerp(bx, 0, e), lerp(by, 0, e); rw = lerp(bw, W, e); rh = rw * H / W; z = rw / bw
    if e > 0: bg = bg.transform((W, H), Image.AFFINE, (1 / z, 0, bx - rx0 / z, 0, 1 / z, by - ry0 / z), Image.BILINEAR)
    else: bg = bg.copy()
    if a <= 0: return bg
    fi = fimg.resize((max(1, int(rw)), max(1, int(rh))), Image.BILINEAR)
    if e < 0.98:   # a soft print shadow while it is still a photo on paper
        sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).rectangle((rx0 + 6, ry0 + 10, rx0 + rw + 6, ry0 + rh + 10), fill=int(110 * a * (1 - e)))
        bg = Image.composite(Image.new('RGB', (W, H), (20, 16, 12)), bg, sh.filter(ImageFilter.GaussianBlur(10)))
    if a < 1: fi = Image.blend(bg.crop((int(rx0), int(ry0), int(rx0) + fi.width, int(ry0) + fi.height)), fi, a)
    bg.paste(fi, (int(rx0), int(ry0))); return bg
def isbook(fn): return isinstance(fn, Book)
ZI0, ZI1 = 0.55, 0.75     # into a film: the photo appears ZI0 before the cut, the flight in ends ZI1 after it
ZO0, ZO1 = 0.75, 0.5      # out of a film: the flight out starts ZO0 before the book, the photo fades from the page ZO1 after
def frame(t):
    i = max(j for j, (a, _) in enumerate(SEG) if a <= t or j == 0); a_i, fn = SEG[i]
    nxt = SEG[i + 1] if i + 1 < len(SEG) else None; prv = SEG[i - 1] if i > 0 else None
    if isbook(fn):
        img = fn(t)
        if nxt and not isbook(nxt[1]) and t > nxt[0] - ZI0:                     # a film is about to come out of this page
            u = (t - (nxt[0] - ZI0 + 0.3)) / (ZI0 - 0.3 + ZI1); img = photo_zoom(img, nxt[1](t), clamp(u), clamp((t - (nxt[0] - ZI0)) / 0.3))
        elif prv and not isbook(prv[1]) and t < a_i + ZO1:                     # we have just flown back out of a film
            u = 1 - (t - (a_i - ZO0)) / (ZO0 + ZO1 - 0.3); img = photo_zoom(img, prv[1](t), clamp(u), clamp((a_i + ZO1 - t) / 0.3))
        elif nxt and isbook(nxt[1]) and nxt[1] is not fn and t > nxt[0] - XF: img = blend(img, nxt[1](t), (t - (nxt[0] - XF)) / (2 * XF))
        elif prv and isbook(prv[1]) and prv[1] is not fn and t < a_i + XF: img = blend(prv[1](t), img, (t - (a_i - XF)) / (2 * XF))
    else:
        img = fn(t)
        if prv and isbook(prv[1]) and t < a_i + ZI1:
            u = (t - (a_i - ZI0 + 0.3)) / (ZI0 - 0.3 + ZI1); img = photo_zoom(prv[1](t), img, clamp(u))
        elif nxt and isbook(nxt[1]) and t > nxt[0] - ZO0:
            u = 1 - (t - (nxt[0] - ZO0)) / (ZO0 + ZO1 - 0.3); img = photo_zoom(nxt[1](t), img, clamp(u))
        elif nxt and not isbook(nxt[1]) and t > nxt[0] - XF: img = blend(img, nxt[1](t), (t - (nxt[0] - XF)) / (2 * XF))
        elif prv and not isbook(prv[1]) and t < a_i + XF: img = blend(prv[1](t), img, (t - (a_i - XF)) / (2 * XF))
    if t > T_END - 1.2: img = blend(img, Image.new('RGB', (W, H), (0, 0, 0)), (t - (T_END - 1.2)) / 1.2)
    return img

if __name__ == '__main__':
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[2:]]
        for t in ts: frame(t).save(LB + 'chk/p_%06.2f.jpg' % t, quality=86)
        n = len(ts); Pc = Image.new('RGB', (3 * 640, ((n + 2) // 3) * 360))
        for i, t in enumerate(ts): Pc.paste(Image.open(LB + 'chk/p_%06.2f.jpg' % t).resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
        Pc.save(LB + 'chk/prev.jpg', quality=88); sys.exit()
    if sys.argv[1] == 'T': print(round(T_END, 3)); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
