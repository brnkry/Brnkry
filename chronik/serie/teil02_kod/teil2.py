# "Deutschland im Zweiten Weltkrieg", Teil 2: Der Überfall auf Polen, long version (16:9), the Teil 1 magazine.
# Everything happens on the magazine: archive film runs in framed prints on the pages and the camera flies into a print until
# the film fills the frame, then pulls back. Boran's colourised photos are printed in colour. Rules of this part:
#  - a word or a picture appears only while the camera shows its place on the page (the camera arrives first, then it appears)
#  - every page turn starts after the last word of the spread has appeared; calm camera moves (1.0 to 1.3 s)
#  - sound: voice, a calm ElevenLabs underscore, and a soft page sound only at the page turns
import functools, math
from lcore import *
from lmap import Map
from drawings import drawing, tank_m, uboat_m
P = lambda w_, a=0.0: ws(w_, a)
CD = 1.1
C = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t2/c/'
DARK = (34, 34, 36)

# ---------- prints on the page ----------
CLIPR = {'tanks': (0.0, 7.8), 'barrier': (0.0, 19.5), 'panzer': (0.0, 16.5), 'stuka': (0.0, 4.8), 'ship': (0.0, 34.5), 'ship2': (0.0, 13.5),
         'moto': (0.0, 11.5), 'pows': (0.0, 19.5), 'bridges': (2.0, 46.0), 'pontoon': (0.0, 20.5), 'officers': (0.0, 27.5), 'brest': (1.5, 39.5),
         'ribbentrop': (0.0, 8.3), 'wfire': (0.0, 36.5), 'wruins': (0.0, 27.5), 'hosp': (0.0, 46.5)}
def film_at(key, t, t0, speed=1.0):
    a, b = CLIPR[key]; ct = a + ((t - t0) * speed) % (b - a); return clip_at(key, ct)
def _corners(pg, x0, y0, bw, bh, k):
    d = ImageDraw.Draw(pg); c = fade_col(DARK, k); d.rectangle((x0, y0, x0 + bw, y0 + bh), outline=fade_col((60, 60, 60), k), width=2); L = 46
    for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x0 + bw, y0, -1, 1), (x0, y0 + bh, 1, -1), (x0 + bw, y0 + bh, -1, -1)):
        d.polygon([(cx - sx * 8, cy - sy * 8), (cx + sx * L, cy - sy * 8), (cx - sx * 8, cy + sy * L)], fill=c)
def _shadow(pg, x0, y0, bw, bh, k):
    sh = Image.new('L', (bw + 80, bh + 80), 0); ImageDraw.Draw(sh).rectangle((48, 52, 40 + bw + 8, 40 + bh + 12), fill=int(120 * k))
    stamp_ink(pg, sh.filter(ImageFilter.GaussianBlur(12)), (x0 - 40, y0 - 40), (40, 34, 28))
def _cap(pg, x0, y, cap, k):
    d = ImageDraw.Draw(pg); d.line((x0, y + 30, x0 + 150, y + 30), fill=fade_col(ACC, k), width=5); d.text((x0, y + 48), cap, font=italic(32), fill=fade_col(GREY, k))
def framed(pg, t, t0, key, box, cap=None, speed=1.0):
    """archive film printed on the page (grey film in the magazine's print tone), the film keeps running in it"""
    if t < t0: return
    k = eout((t - t0) / 0.5); x0, y0, bw, bh = [int(v) for v in box]; g = film_at(key, t, t0, speed); w, h = g.size
    sc = max(bw / w, bh / h); cw, ch = bw / sc, bh / sc
    fr_ = tone(g.convert('L').resize((bw, bh), Image.BICUBIC, box=((w - cw) / 2, (h - ch) / 2, (w + cw) / 2, (h + ch) / 2)))
    _shadow(pg, x0, y0, bw, bh, k)
    if k < 1: fr_ = Image.blend(Image.new('RGB', fr_.size, PAPER), fr_, k)
    pg.paste(fr_, (x0, y0)); _corners(pg, x0, y0, bw, bh, k)
    if cap: _cap(pg, x0, y0 + bh, cap, k)
@functools.lru_cache(maxsize=64)
def _cimg(name, bw, bh, fx, fy):
    g = Image.open(C + name + '.jpg').convert('RGB'); w, h = g.size; sc = max(bw / w, bh / h); cw, ch = bw / sc, bh / sc
    x0 = (w - cw) * fx; y0 = (h - ch) * fy
    im = g.resize((bw, bh), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    a = np.asarray(im, np.float32); a = a * 0.94 + np.array([10, 8, 4], np.float32)   # a touch of print warmth
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def cphoto(pg, t, t0, name, box, cap=None, fx=0.5, fy=0.5):
    """one of the colourised photos, printed in colour"""
    if t < t0: return
    k = eout((t - t0) / 0.5); x0, y0, bw, bh = [int(v) for v in box]; im = _cimg(name, bw, bh, fx, fy)
    _shadow(pg, x0, y0, bw, bh, k)
    if k < 1: im = Image.blend(Image.new('RGB', im.size, PAPER), im, k)
    pg.paste(im, (x0, y0)); _corners(pg, x0, y0, bw, bh, k)
    if cap: _cap(pg, x0, y0 + bh, cap, k)
def fill(side, box, f=1.07):
    x0, y0, bw, bh = box; return ((0 if side == 'L' else PW) + x0 + bw / 2, y0 + bh / 2, f * max(W / bw, H / bh))
LC, RC, MID = 700, 2100, PW
def fr(side, y0, y1, smax=1.3):
    s = min(smax, 1000 / (y1 - y0), 1840 / PW); return ((LC if side == 'L' else RC), (y0 + y1) / 2, s)
OV = (MID, 905, 0.60)
def head(pg, t, t0, kicker, l1, l2=None, w1=800, w2=400, size=110, y=200):
    label(pg, t, t0, kicker, (110, y), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, l1, (110, y + 50), serif(size, w1))
    if l2: label(pg, t, t0 + 0.2, l2, (110, y + 50 + int(size * 1.17)), serif(size, w2))
def big(pg, t, t0, s, xy, size=200, col=ACC): label(pg, t, t0, s, xy, serif(size, 800), col)
def note(pg, t, t0, s, xy, size=34): label(pg, t, t0, s, xy, italic(size), GREY)
def route(pg, t, t0, stops, x, y0, dy=118, dt=0.45, size=54):
    """an itinerary down the page: dots joined by a line, each stop set when it is reached"""
    d = ImageDraw.Draw(pg)
    for i, (s_, tw) in enumerate(stops):
        ti = max(t0, tw)
        if t < ti: continue
        k = eout((t - ti) / 0.35); y = y0 + i * dy
        if i: d.line((x + 14, y - dy + 30, x + 14, lerp(y - dy + 30, y - 6, k)), fill=fade_col(ACC, k), width=5)
        d.ellipse((x, y - 6, x + 28, y + 22), fill=fade_col(ACC if i == len(stops) - 1 else TXT, k))
        d.text((x + 60, y + 8), s_, font=serif(size, 700 if i == len(stops) - 1 else 400), fill=fade_col(TXT, k), anchor='lm')
def strike_through(pg, t, t0, x0, x1, y, wd=10):
    if t < t0: return
    u = eout((t - t0) / 0.45); ImageDraw.Draw(pg).line((x0, y, lerp(x0, x1, u), y), fill=ACC, width=wd)

# ================= SP0: masthead with the opening film / the myth =================
B0 = (110, 600, 1180, 664)
@functools.lru_cache(None)
def masthead():
    pg = base(1, True).copy(); d = ImageDraw.Draw(pg)
    for i, c in enumerate(((24, 24, 26), (196, 30, 34), (236, 186, 32))): d.rectangle((110, 196 + i * 92, 128, 196 + (i + 1) * 92), fill=c)
    d.text((160, 186), 'Deutschland im', font=serif(118, 900), fill=TXT); d.text((160, 326), 'Zweiten Weltkrieg', font=serif(118, 400), fill=TXT)
    for i, c in enumerate(((24, 24, 26), (196, 30, 34), (236, 186, 32))): d.rectangle((110, 490 + i * 9, PW - 110, 490 + (i + 1) * 9), fill=c)
    d.text((110, 545), 'TEIL 2 · DER ÜBERFALL AUF POLEN', font=sans(38, 800), fill=ACC, anchor='lm')
    d.text((PW - 110, 545), 'SEPTEMBER BIS OKTOBER 1939', font=sans(28, 600), fill=GREY, anchor='rm')
    return pg
T_PB = P('Doch', 4) - 0.05                     # the camera leaves the opening film
def s0L(t):
    pg = masthead().copy(); framed(pg, t, -1, 'tanks', B0, 'Deutsche Panzer in Polen, September 1939', 0.8)
    body(pg, t, 110, 1390, 'Der Feldzug gegen Polen gilt bis heute als der erste Blitzkrieg der Geschichte.', -1, accent=('Blitzkrieg',), size=56, lh=78, maxw=1180)
    return pg
def s0R(t):
    pg = base(2, False).copy(); t0 = T_PB + 1.0
    label(pg, t, t0, 'EIN MYTHOS', (110, 200), sans(40, 800), ACC)
    label(pg, t, t0 + 0.1, '„Blitzkrieg“', (110, 250), serif(170, 800))
    strike_through(pg, t, P('Dienstvorschrift') - 0.1, 100, 1040, 360, 12)
    label(pg, t, P('Dienstvorschrift'), 'Das Wort stand in keiner deutschen Dienstvorschrift.', (110, 500), serif(52, 400))
    label(pg, t, P('polnische', 8), 'Die polnische Armee kämpfte länger,', (110, 580), serif(52, 400)); label(pg, t, P('erwartet', 10), 'als viele erwartet hatten.', (110, 650), serif(52, 400))
    t1 = P('Nach', 12)
    cphoto(pg, t, t1, 'eu_warschau', (110, 880, 560, 620), 'Warschau, Herbst 1939', fy=0.4)
    big(pg, t, P('fünf', 12), '5', (760, 840), 300); label(pg, t, P('Wochen', 12), 'Wochen', (950, 1010), serif(90, 400))
    label(pg, t, P('aufgeteilt'), 'Polen, aufgeteilt', (760, 1220), serif(52, 800)); label(pg, t, P('zwischen', 17), 'zwischen zwei', (760, 1290), serif(52, 400)); label(pg, t, P('Diktaturen'), 'Diktaturen.', (760, 1360), serif(52, 400))
    rule(pg, t, P('Und', 18) - 0.1, 1560, 110, PW - 110)
    label(pg, t, P('Front', 19.5), 'Und hinter der Front: ein Krieg', (110, 1600), italic(44), ACC); label(pg, t, P('Zivilbevölkerung') - 0.1, 'gegen die Zivilbevölkerung.', (110, 1660), italic(44), ACC)
    return pg

# ================= SP1: 1 September, three directions =================
B1 = (110, 560, 1180, 680)
MAP39 = Map('m39', (PW, PH), (90, 300, 1220, 1260), 13.0, 26.6, 48.6)
def arrow(pg, m, t, t0, pts, dur=1.0, wd=16):
    """an attack arrow drawn on through lon/lat points, the head at the end"""
    if t < t0: return
    u = eio((t - t0) / dur); Q = [m.mp(*p) for p in pts]; segs = list(zip(Q, Q[1:])); L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs)
    todo = u * L; d = ImageDraw.Draw(pg); E = Q[0]; ang = 0
    for a, b in segs:
        l = math.hypot(b[0] - a[0], b[1] - a[1]); v = min(1, todo / l); E = (lerp(a[0], b[0], v), lerp(a[1], b[1], v)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
        d.line((a, E), fill=ACC, width=wd); todo -= l
        if todo <= 0: break
    hd = 46; d.polygon([(E[0] + 18 * math.cos(ang), E[1] + 18 * math.sin(ang)), (E[0] - hd * math.cos(ang - 0.6), E[1] - hd * math.sin(ang - 0.6)), (E[0] - hd * math.cos(ang + 0.6), E[1] - hd * math.sin(ang + 0.6))], fill=ACC)
def s1L(t):
    pg = base(3, True).copy(); t0 = TURNS[0] + 1.0
    head(pg, t, t0, '1. SEPTEMBER 1939', 'Der Angriff', size=110)
    framed(pg, t, t0 + 0.2, 'barrier', B1, 'Deutsche Soldaten am Schlagbaum der polnischen Grenze')
    label(pg, t, P('anderthalb'), '1,5 Millionen', (110, 1380), serif(150, 800), ACC); label(pg, t, P('Soldaten', 30), 'deutsche Soldaten an der Grenze', (110, 1560), serif(56, 400))
    return pg
def s1R(t):
    pg = base(4, False).copy(); t0 = P('Sie', 32) - 0.2; m = MAP39
    label(pg, t, t0, 'Aus drei Richtungen zugleich', (110, 200), serif(74, 800))
    if t >= t0:
        k = eout((t - t0) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=('reich',), outline=('reich',))
        stamp_ink(pg, m.outline('poland').point(lambda v: int(v * k)), (0, 0), TXT); m.tint(pg, 'poland', k, ACC, 0.05)
        m.label(pg, t, t0 + 0.3, 'POLEN', (21.9, 51.3), sans(44, 800), TXT); m.pin(pg, t, t0 + 0.4, (21.01, 52.23), TXT, 10); m.label(pg, t, t0 + 0.4, 'Warschau', (21.01, 52.55), sans(28, 700), GREY, sw=4)
        m.label(pg, t, t0 + 0.4, 'DEUTSCHES REICH', (14.6, 51.6), sans(32, 700), GREY, sw=4); m.label(pg, t, t0 + 0.5, 'SOWJETUNION', (25.6, 52.9), sans(28, 700), GREY, sw=4)
        m.label(pg, t, t0 + 0.5, 'Ostsee', (17.0, 55.3), italic(34), GREY, sw=4)
        for s_, ll, w_, a_ in (('POMMERN', (16.3, 54.05), 'Pommern', 32), ('OSTPREUSSEN', (21.3, 54.35), 'Ostpreußen', 32), ('SCHLESIEN', (17.1, 50.75), 'Schlesien', 32), ('SLOWAKEI', (19.8, 48.85), 'Slowakei', 32)):
            m.label(pg, t, P(w_, a_), s_, ll, sans(30, 800), ACC, sw=5)
        arrow(pg, m, t, P('Pommern', 32) + 0.1, [(16.4, 53.75), (17.5, 53.35), (18.4, 53.05)])
        arrow(pg, m, t, P('Ostpreußen', 32) + 0.1, [(20.6, 53.75), (20.85, 53.05), (21.0, 52.55)])
        arrow(pg, m, t, P('Schlesien', 32) + 0.1, [(17.9, 51.15), (18.9, 51.55), (19.7, 51.8)])
        arrow(pg, m, t, P('Schlesien', 32) + 0.4, [(18.6, 50.3), (19.2, 50.15), (19.75, 50.08)])
        arrow(pg, m, t, P('Slowakei', 32) + 0.1, [(20.7, 49.2), (21.0, 49.75), (21.5, 50.3)])
        m.label(pg, t, t0 + 0.3, 'Danzig', (18.65, 54.62), sans(26, 700), TXT, sw=4)
    label(pg, t, P('Polen', 42), 'Polen war auf drei Seiten eingeschlossen.', (110, 1640), serif(54, 800))
    return pg

# ================= SP2: the forces / mobilisation postponed / the Peking Plan =================
B2 = (110, 1100, 1180, 560)
def s2L(t):
    pg = base(5, True).copy(); t0 = TURNS[1] + 1.0
    head(pg, t, t0, 'DIE KRÄFTE', 'Ungleiche Gegner', size=100)
    d = ImageDraw.Draw(pg)
    if t >= t0 + 0.3:
        k = eout((t - t0 - 0.3) / 0.4); d.text((430, 520), 'WEHRMACHT', font=sans(36, 800), fill=fade_col(TXT, k), anchor='mm'); d.text((990, 520), 'POLEN', font=sans(36, 800), fill=fade_col(ACC, k), anchor='mm')
        d.line((110, 560, lerp(110, PW - 110, k), 560), fill=LIGHT, width=2)
    rows = (('Panzer', 'über 2.500', 'Panzer', 'einige Hundert', 'Hundert'), ('Flugzeuge', 'über 2.000', 'Flugzeuge', 'rund 400', 'Kampfflugzeuge'), ('Soldaten', '1,5 Millionen', 'Soldaten', 'knapp 1 Million', 'Million'))
    tw_ = [(P('Panzer', 45), P('Hundert', 54)), (P('Flugzeuge', 48), P('Kampfflugzeuge')), (P('verfügte') - 0.2, P('Million', 54))]
    for i, ((nm, a_, _, b_, _), (ta, tb)) in enumerate(zip(rows, tw_)):
        y = 610 + i * 120; label(pg, t, min(ta, tb) - 0.2, nm.upper(), (110, y), sans(28, 700), GREY)
        label(pg, t, ta, a_, (430, y + 40), serif(64, 800), TXT, 'ma'); label(pg, t, tb, b_, (990, y + 40), serif(64, 800), ACC, 'ma')
    note(pg, t, P('leichte'), 'Die meisten deutschen Panzer waren leichte Modelle.', (110, 1000))
    framed(pg, t, P('Panzer', 45) - 0.1, 'panzer', B2, 'Deutsche Panzerverbände, September 1939')
    return pg
B2R = (110, 1060, 560, 500)
def s2R(t):
    pg = base(6, False).copy(); t0 = P('Viele', 62) - 0.2
    label(pg, t, t0, 'Viele Reservisten waren', (110, 200), serif(60, 400)); label(pg, t, t0 + 0.4, 'noch auf dem Weg zu ihren Einheiten.', (110, 270), serif(60, 400))
    cphoto(pg, t, P('Drängen') - 0.2, 'eu_chamberlain', (110, 400, 560, 560), 'Neville Chamberlain (rechts), 1939', fy=0.2)
    label(pg, t, P('Generalmobilmachung') - 0.1, 'Die General-', (740, 440), serif(70, 800)); label(pg, t, P('Generalmobilmachung'), 'mobilmachung', (740, 520), serif(70, 800))
    label(pg, t, P('verschoben'), 'wurde verschoben,', (740, 610), serif(54, 400), ACC); label(pg, t, P('Vorwand') - 0.4, 'um Hitler keinen', (740, 680), serif(54, 400)); label(pg, t, P('Vorwand'), 'Vorwand zu liefern.', (740, 750), serif(54, 400))
    note(pg, t, P('Großbritanniens') + 0.2, 'auf Drängen Großbritanniens', (740, 850), 32); note(pg, t, P('Frankreichs') , 'und Frankreichs', (740, 895), 32)
    t1 = P('Nur', 73) - 0.2
    rule(pg, t, t1, 1000)
    cphoto(pg, t, t1 + 0.1, 'eu_orp_blyskawica', B2R, 'Zerstörer ORP Błyskawica')
    label(pg, t, t1 + 0.1, 'DER PEKING-PLAN', (740, 1060), sans(36, 800), ACC)
    for i, s_ in enumerate(('Burza', 'Błyskawica', 'Grom')): label(pg, t, P(s_.replace('ł', 'ł')) if i else P('Burza'), s_, (740, 1120 + i * 90), serif(70, 800))
    route(pg, t, P('Ostsee', 78), [('Ostsee', P('Ostsee', 78)), ('Großbritannien', P('Großbritannien', 80))], 740, 1430, 90, size=46)
    note(pg, t, P('Royal', 87), 'Sie kämpften an der Seite der Royal Navy weiter.', (110, 1720 - 20), 34)
    return pg

# ================= SP3: Westerplatte and Wieluń / the Polish Post Office, Westerplatte seven days =================
B3 = (110, 330, 1180, 640)
def s3L(t):
    pg = base(7, True).copy(); t0 = TURNS[2] + 1.0
    label(pg, t, t0, 'DANZIG UND WIELUŃ, 1. SEPTEMBER, 4.45 UHR', (110, 200), sans(36, 800), ACC)
    framed(pg, t, t0 + 0.1, 'ship', B3, 'Das Linienschiff Schleswig-Holstein beschießt die Westerplatte')
    cphoto(pg, t, P('Sturzkampfbomber', 95) - 0.2, 'hoffmann_s23_0', (110, 1100, 520, 500), 'Blick aus einem Sturzkampfbomber')
    label(pg, t, P('Wieluń'), 'Wieluń', (700, 1110), serif(110, 800)); label(pg, t, P('Kleinstadt'), 'eine Kleinstadt ohne', (700, 1260), serif(52, 400)); label(pg, t, P('Bedeutung', 100), 'militärische Bedeutung', (700, 1325), serif(52, 400))
    label(pg, t, P('Krankenhaus'), 'Auch das Krankenhaus', (700, 1430), serif(52, 800)); label(pg, t, P('getroffen'), 'wurde getroffen.', (700, 1495), serif(52, 800))
    label(pg, t, P('Hunderte', 106), 'Hunderte Tote.', (700, 1590), serif(52, 400), ACC)
    return pg
def s3R(t):
    pg = base(8, False).copy(); t0 = P('In', 111.5) - 0.2
    label(pg, t, t0, 'DIE POLNISCHE POST IN DANZIG', (110, 200), sans(36, 800), ACC)
    cphoto(pg, t, t0 + 0.1, 'kampf_um_danzig_seite_40-040', (110, 260, 540, 760), 'Danzig, 1. September 1939 (Bildseite 1939)', fy=0.35)
    label(pg, t, P('stundenlang'), 'Stundenlang', (720, 300), serif(64, 800)); label(pg, t, P('Postamt'), 'verteidigten Postbeamte', (720, 380), serif(50, 400)); label(pg, t, P('Postamt') + 0.1, 'ihr Postamt.', (720, 445), serif(50, 400))
    label(pg, t, P('Brand'), 'Erst als das Gebäude', (720, 560), serif(50, 400)); label(pg, t, P('ergaben'), 'brannte, ergaben sie sich.', (720, 625), serif(50, 400))
    label(pg, t, P('Kriegsgericht') - 0.3, 'Später: Kriegsgericht,', (720, 760), serif(50, 800), ACC); label(pg, t, P('erschossen'), 'Todesurteile, erschossen.', (720, 825), serif(50, 800), ACC)
    t1 = P('Auf', 127.5) - 0.2
    rule(pg, t, t1, 1100)
    label(pg, t, t1, 'DIE WESTERPLATTE', (110, 1140), sans(36, 800), ACC)
    cphoto(pg, t, t1 + 0.1, 'eu_westerplatte_collage', (110, 1200, 600, 420), 'Westerplatte, 1. bis 7. September 1939')
    label(pg, t, P('200', 128), 'rund 200 Soldaten', (780, 1200), serif(52, 800)); label(pg, t, P('Sucharski'), 'Major Henryk Sucharski', (780, 1270), serif(46, 400))
    label(pg, t, P('zwölf'), '12 Stunden', (780, 1380), serif(80, 800), GREY); strike_through(pg, t, P('sieben', 141) - 0.1, 770, 1230, 1430, 9)
    label(pg, t, P('sieben', 141), '7 Tage', (780, 1490), serif(110, 800), ACC)
    return pg

# ================= SP4: Krojanty, the myth of lances against tanks =================
def s4L(t):
    pg = base(9, True).copy(); t0 = TURNS[3] + 1.0
    head(pg, t, t0, 'KROJANTY, 1. SEPTEMBER, ABENDS', 'Die Ulanen', size=110)
    cphoto(pg, t, t0 + 0.2, 'hoffmann_s29_0', (110, 520, 1180, 660), 'Pferde und Fahrzeuge auf einer Straße in Polen, September 1939')
    label(pg, t, P('Säbel'), 'Mit gezogenem Säbel gegen', (110, 1320), serif(56, 400)); label(pg, t, P('Infanterieeinheit'), 'eine deutsche Infanterieeinheit.', (110, 1395), serif(56, 400))
    label(pg, t, P('zurück', 150), 'Sie schlugen sie zurück.', (110, 1470), serif(56, 800))
    label(pg, t, P('Panzerspähwagen'), 'Dann: Panzerspähwagen, Feuer.', (110, 1590), serif(56, 800), ACC)
    return pg
def s4R(t):
    pg = base(10, False).copy(); t0 = P('Italienische') - 0.2
    label(pg, t, t0, 'DER MYTHOS', (110, 200), sans(40, 800), ACC)
    label(pg, t, P('Lanzen') - 0.2, 'Mit Lanzen', (110, 250), serif(120, 800)); label(pg, t, P('Panzer', 162), 'gegen Panzer', (110, 390), serif(120, 400))
    drawing(pg, t, P('Panzer', 162) - 0.1, 0.8, lambda ph: tank_m(700, 760, 0.85, ph))
    note(pg, t, P('Kriegsberichterstatter'), 'Erzählt von italienischen Kriegsberichterstattern,', (110, 960), 32); note(pg, t, P('Propaganda', 167), 'verbreitet von der deutschen Propaganda.', (110, 1005), 32)
    strike_through(pg, t, P('falsch'), 100, 1260, 330, 12)
    label(pg, t, P('falsch') + 0.1, 'Falsch.', (110, 1080), serif(110, 800), ACC)
    t1 = P('Die', 174) - 0.2
    label(pg, t, t1, 'DIE WIRKLICHKEIT', (110, 1260), sans(36, 800), ACC)
    cphoto(pg, t, t1 + 0.1, 'hoffmann_s30_1', (740, 1240, 550, 380), 'Pferdebespannte Geschütze, 1939')
    label(pg, t, P('abgesessen'), 'Die Kavallerie kämpfte', (110, 1320), serif(50, 400)); label(pg, t, P('Infanterie', 176), 'meist abgesessen wie', (110, 1385), serif(50, 400)); label(pg, t, P('Infanterie', 176) + 0.1, 'Infanterie.', (110, 1450), serif(50, 400))
    label(pg, t, P('Panzerabwehrkanonen') - 0.3, 'Sie hatte eigene', (110, 1550), serif(50, 800)); label(pg, t, P('Panzerabwehrkanonen'), 'Panzerabwehrkanonen.', (110, 1615), serif(50, 800))
    return pg

# ================= SP5: Bromberg / the Einsatzgruppen =================
def s5L(t):
    pg = base(11, True).copy(); t0 = TURNS[4] + 1.0
    head(pg, t, t0, 'BROMBERG, 3. SEPTEMBER 1939', 'Schüsse in', 'der Stadt', size=110)
    cphoto(pg, t, t0 + 0.3, 'hoffmann_s33_0', (110, 610, 560, 700), 'Eine zerstörte Straße in Polen, 1939')
    label(pg, t, P('hundert', 188), 'mehr als 100', (740, 640), serif(80, 800), ACC); label(pg, t, P('Volksdeutsche'), 'Volksdeutsche getötet', (740, 740), serif(50, 400))
    label(pg, t, P('umstritten'), 'Wie es dazu kam und wie', (740, 880), serif(46, 400)); label(pg, t, P('umstritten') + 0.15, 'viele Opfer es waren,', (740, 940), serif(46, 400)); label(pg, t, P('umstritten') + 0.3, 'ist bis heute umstritten.', (740, 1000), serif(46, 800))
    t1 = P('Die', 197) - 0.2
    rule(pg, t, t1, 1400)
    label(pg, t, P('Bromberger') - 0.1, '„Bromberger Blutsonntag“', (110, 1440), serif(70, 800)); note(pg, t, P('Bromberger') + 0.3, 'So nannte es die nationalsozialistische Propaganda.', (110, 1540))
    label(pg, t, P('vervielfachte'), 'Sie vervielfachte die Opferzahl und rechtfertigte', (110, 1610), serif(44, 400)); label(pg, t, P('Massenerschießungen'), 'damit Massenerschießungen.', (110, 1670), serif(44, 800), ACC)
    return pg
def s5R(t):
    pg = base(12, False).copy(); t0 = P('Nach', 207) - 0.2
    label(pg, t, t0, 'Nach der Einnahme der Stadt:', (110, 200), serif(56, 400)); label(pg, t, P('Hunderte', 208), 'Hunderte polnische Einwohner', (110, 275), serif(56, 800)); label(pg, t, P('hingerichtet'), 'hingerichtet.', (110, 350), serif(56, 800), ACC)
    rule(pg, t, P('Hinter', 211) - 0.2, 470)
    label(pg, t, P('Hinter', 211) - 0.1, 'HINTER DEN TRUPPEN', (110, 510), sans(36, 800), ACC)
    label(pg, t, P('Einsatzgruppen') - 0.1, 'Einsatzgruppen', (110, 560), serif(110, 800)); note(pg, t, P('SD'), 'der Sicherheitspolizei und des SD', (110, 700))
    label(pg, t, P('Listen') - 0.1, 'Auf ihren Listen standen:', (110, 820), serif(54, 400))
    for i, w_ in enumerate(('Lehrer', 'Priester', 'Ärzte', 'Beamte', 'Gutsbesitzer')):
        label(pg, t, P(w_, 217), w_, (160, 910 + i * 92), serif(64, 700))
        if t >= P(w_, 217): ImageDraw.Draw(pg).line((110, 950 + i * 92, 140, 950 + i * 92), fill=ACC, width=5)
    label(pg, t, P('Zehntausende', 224), 'Zehntausende', (110, 1420), serif(130, 800), ACC)
    label(pg, t, P('Zivilisten', 225), 'polnische Zivilisten ermordet,', (110, 1580), serif(56, 400)); label(pg, t, P('Juden', 226), 'darunter viele Juden. Bis Ende 1939.', (110, 1650), serif(56, 400))
    return pg

# ================= SP6: the advance, the Luftwaffe, Warsaw's barricades, the Bzura =================
B6 = (110, 330, 1180, 640)
def s6L(t):
    pg = base(13, True).copy(); t0 = TURNS[5] + 1.0
    label(pg, t, t0, 'DER VORMARSCH', (110, 200), sans(40, 800), ACC)
    framed(pg, t, t0 + 0.1, 'moto', B6, 'Motorisierte Truppen im Vormarsch')
    t1 = P('Die', 236) - 0.2
    cphoto(pg, t, t1, 'hoffmann_s79_0', (110, 1110, 560, 480), 'Zerstörte Bahnanlagen, Luftaufnahme 1939')
    for i, w_ in enumerate(('Flugplätze', 'Brücken', 'Bahnlinien')): label(pg, t, P(w_, 236), w_, (740, 1110 + i * 90), serif(66, 800))
    label(pg, t, P('Kolonnen', 238), 'Angriffe auf Kolonnen,', (740, 1400), serif(48, 400)); label(pg, t, P('Flüchtlingstrecks'), 'auch auf Flüchtlingstrecks.', (740, 1460), serif(48, 800), ACC)
    return pg
def s6R(t):
    pg = base(14, False).copy(); t0 = P('Nach', 244.5) - 0.2
    label(pg, t, t0, 'NACH EINER WOCHE', (110, 200), sans(40, 800), ACC)
    cphoto(pg, t, t0 + 0.1, 'hoffmann_s86_1', (110, 260, 600, 520), 'Verteidiger in Warschau, September 1939')
    label(pg, t, P('Stadtrand'), 'Deutsche Panzer', (780, 280), serif(54, 800)); label(pg, t, P('Stadtrand') + 0.1, 'am Stadtrand', (780, 350), serif(54, 400)); label(pg, t, P('Warschau', 246), 'von Warschau.', (780, 420), serif(54, 400))
    label(pg, t, P('Barrikaden'), 'Der erste Angriff', (780, 560), serif(54, 400)); label(pg, t, P('Barrikaden') + 0.1, 'scheitert an', (780, 630), serif(54, 400)); label(pg, t, P('Verteidiger', 252), 'den Barrikaden.', (780, 700), serif(54, 800), ACC)
    t1 = P('Westlich') - 0.2
    rule(pg, t, t1, 900)
    label(pg, t, t1, 'DIE SCHLACHT AN DER BZURA · AB 9. SEPTEMBER', (110, 940), sans(34, 800), ACC)
    cphoto(pg, t, t1 + 0.1, 'soeldner_karte_s073', (110, 1000, 460, 680), 'Lagekarte von 1939 (Söldner, 1939)', fy=0.3)
    label(pg, t, P('Armeen', 255), 'Zwei polnische Armeen', (640, 1020), serif(50, 800)); label(pg, t, P('Grenze', 257), 'greifen die Flanke der', (640, 1090), serif(50, 400)); label(pg, t, P('Flanke'), 'deutschen 8. Armee an.', (640, 1160), serif(50, 400))
    label(pg, t, P('größte'), 'Die größte Schlacht', (640, 1280), serif(60, 800), ACC); label(pg, t, P('Feldzugs'), 'des Feldzugs.', (640, 1355), serif(60, 400))
    label(pg, t, P('eingekesselt'), 'Die Polen werden', (640, 1470), serif(50, 400)); label(pg, t, P('eingekesselt') + 0.1, 'eingekesselt.', (640, 1535), serif(50, 800))
    return pg

# ================= SP7: the gold / the West waits =================
def s7L(t):
    pg = base(15, True).copy(); t0 = TURNS[6] + 1.0
    head(pg, t, t0, 'DER STAATSSCHATZ', 'Das Gold', 'der Polen', size=110)
    cphoto(pg, t, t0 + 0.3, 'eu_polnische_fluechtlinge_b', (110, 620, 1180, 560), 'Flüchtlinge auf einer Landstraße, September 1939')
    label(pg, t, P('75'), 'rund 75 Tonnen Gold', (110, 1260), serif(72, 800), ACC); note(pg, t, P('Nationalbank'), 'der polnischen Nationalbank', (110, 1360))
    route(pg, t, P('Hauptstadt', 289), [('Warschau', P('Hauptstadt', 289)), ('rumänische Grenze', P('rumänische')), ('Schwarzes Meer', P('Schwarzen')), ('Türkei', P('Türkei')), ('Frankreich', P('Frankreich', 300))],
          110, 1440, 62, size=40)
    label(pg, t, P('nie', 304), 'Die Deutschen bekamen es nie.', (700, 1690), serif(42, 800))
    return pg
def s7R(t):
    pg = base(16, False).copy(); t0 = P('Polen', 306.5) - 0.2
    head(pg, t, t0, 'DER WESTEN', 'Polen wartet', size=100)
    label(pg, t, P('zugesagt'), 'Frankreich hatte eine große Offensive', (110, 470), serif(48, 400)); label(pg, t, P('Mobilmachung', 311), 'binnen zwei Wochen zugesagt.', (110, 530), serif(48, 400))
    cphoto(pg, t, P('Tatsächlich', 317) - 0.2, 'eu_kriegskrise_1939_c', (110, 640, 560, 560), 'Großbritannien, September 1939')
    label(pg, t, P('Saarland'), '7. September:', (740, 660), serif(52, 800)); label(pg, t, P('Saarland') + 0.1, 'Vorstoß ins Saarland,', (740, 730), serif(52, 400)); label(pg, t, P('Dörfer'), 'einige Kilometer weit.', (740, 800), serif(52, 400))
    label(pg, t, P('stehen'), 'Dann Stillstand.', (740, 910), serif(52, 800), ACC); label(pg, t, P('Oktober', 327), 'Im Oktober: Rückzug.', (740, 980), serif(52, 400))
    label(pg, t, P('Flugblätter') - 0.2, 'Britische Bomber werfen vor allem Flugblätter ab.', (110, 1300), serif(48, 400))
    rule(pg, t, P('Franzosen') - 0.2, 1400)
    label(pg, t, P('drôle'), 'drôle de guerre', (110, 1430), italic(84, 400), TXT); note(pg, t, P('seltsamen'), 'der seltsame Krieg', (120, 1540), 36)
    label(pg, t, P('Sitzkrieg'), 'Sitzkrieg', (110, 1590), serif(96, 800), ACC)
    return pg

# ================= SP8: 17 September, the Red Army / Brest-Litowsk =================
B8 = (110, 330, 1180, 640)
def s8L(t):
    pg = base(17, True).copy(); t0 = TURNS[7] + 1.0
    head(pg, t, t0, '17. SEPTEMBER 1939', 'Die Rote Armee', size=110)
    cphoto(pg, t, P('Ostgrenze') - 0.2, 'soeldner_karte_s109', (110, 520, 520, 820), 'Lagekarte zum 17. September (Söldner, 1939)', fy=0.3)
    label(pg, t, P('Moskau', 347), 'Moskau: Der polnische', (700, 540), serif(50, 400)); label(pg, t, P('existiere'), 'Staat existiere nicht mehr.', (700, 605), serif(50, 400))
    label(pg, t, P('Ukrainer'), 'Vorwand: Schutz der Ukrainer', (700, 700), serif(46, 400)); label(pg, t, P('Weißrussen'), 'und Weißrussen.', (700, 760), serif(46, 400))
    label(pg, t, P('Zusatzprotokoll') - 0.4, 'In Wahrheit: das geheime', (700, 880), serif(50, 800), ACC); label(pg, t, P('Zusatzprotokoll'), 'Zusatzprotokoll des', (700, 945), serif(50, 800), ACC); label(pg, t, P('Hitler-Stalin-Pakts'), 'Hitler-Stalin-Pakts.', (700, 1010), serif(50, 800), ACC)
    label(pg, t, P('kaum', 360), 'Im Osten standen kaum', (700, 1120), serif(46, 400)); label(pg, t, P('Truppen', 362), 'noch polnische Truppen.', (700, 1180), serif(46, 400))
    label(pg, t, P('Regierung', 364), 'In der Nacht darauf verlässt', (110, 1500), serif(54, 400)); label(pg, t, P('rumänische', 366), 'die Regierung das Land über Rumänien.', (110, 1570), serif(54, 800))
    return pg
def s8R(t):
    pg = base(18, False).copy(); t0 = P('Wenige', 369) - 0.2
    label(pg, t, t0, 'BREST-LITOWSK, 22. SEPTEMBER 1939', (110, 200), sans(38, 800), ACC)
    framed(pg, t, t0 + 0.1, 'officers', B8, 'Deutsche und sowjetische Offiziere an der Demarkationslinie')
    label(pg, t, P('übergab') + 0.1, 'Die Wehrmacht übergibt die Stadt', (110, 1080), serif(54, 400)); label(pg, t, P('Armee', 371), 'an die Rote Armee.', (110, 1150), serif(54, 800))
    framed(pg, t, P('Guderian') - 0.5, 'brest', (110, 1270, 640, 360), 'Gemeinsamer Vorbeimarsch')
    label(pg, t, P('Guderian'), 'Heinz Guderian', (820, 1290), serif(50, 800)); label(pg, t, P('Semjon'), 'Semjon Kriwoschein', (820, 1360), serif(50, 800), ACC)
    note(pg, t, P('Vorbeimarsch'), 'nehmen gemeinsam', (820, 1440), 32); note(pg, t, P('Vorbeimarsch') + 0.1, 'den Vorbeimarsch ab.', (820, 1485), 32)
    return pg

# ================= SP9: Hela / the escape of the Orzeł =================
B9 = (110, 330, 1180, 600)
def s9L(t):
    pg = base(19, True).copy(); t0 = TURNS[8] + 1.0
    label(pg, t, t0, 'AN DER OSTSEE', (110, 200), sans(40, 800), ACC)
    framed(pg, t, t0 + 0.1, 'ship2', B9, 'Deutsche Schiffsartillerie vor der Küste, September 1939')
    label(pg, t, P('Hela'), 'Die Halbinsel Hela', (110, 1070), serif(96, 800))
    label(pg, t, P('Landstreifen'), 'ein schmaler Landstreifen gegenüber von Gdingen', (110, 1220), serif(46, 400))
    label(pg, t, P('2.800'), 'rund 2.800', (110, 1330), serif(110, 800), ACC); label(pg, t, P('Marineangehörige'), 'Soldaten und Marineangehörige', (110, 1480), serif(50, 400))
    label(pg, t, P('Unrug'), 'unter Konteradmiral Józef Unrug', (110, 1550), serif(50, 800))
    return pg
def s9R(t):
    pg = base(20, False).copy(); t0 = P('Und', 396.5) - 0.2
    label(pg, t, t0, 'DIE FLUCHT DER ORZEŁ', (110, 200), sans(40, 800), ACC)
    drawing(pg, t, t0 + 0.2, 1.0, lambda ph: uboat_m(700, 470, 1.1, ph))
    label(pg, t, P('Tallinn'), 'Im neutralen Tallinn festgesetzt.', (110, 700), serif(52, 400))
    label(pg, t, P('Seekarten'), 'Die Esten nehmen die Seekarten', (110, 780), serif(52, 400)); label(pg, t, P('Munition'), 'und einen Teil der Munition.', (110, 850), serif(52, 400))
    label(pg, t, P('Nacht', 412), 'Nacht zum 18. September: Ausbruch.', (110, 960), serif(52, 800), ACC)
    label(pg, t, P('Leuchttürme') - 0.4, 'Ohne Karten, nur eine selbst', (110, 1080), serif(50, 400)); label(pg, t, P('Leuchttürme'), 'gezeichnete Liste der Leuchttürme', (110, 1145), serif(50, 400))
    route(pg, t, P('Ostsee', 420), [('Tallinn', P('Ostsee', 420)), ('Ostsee', P('Ostsee', 420) + 0.3), ('Meerengen', P('Meerengen')), ('Schottland, Mitte Oktober', P('Schottland'))], 110, 1290, 100, size=48)
    return pg

# ================= SP10: the siege of Warsaw =================
B10 = (110, 330, 1180, 660)
def s10L(t):
    pg = base(21, True).copy(); t0 = TURNS[9] + 1.0
    label(pg, t, t0, 'DIE BELAGERUNG VON WARSCHAU', (110, 200), sans(40, 800), ACC)
    framed(pg, t, t0 + 0.1, 'wfire', B10, 'Warschau brennt, September 1939 (Aufnahme Julien Bryan)')
    label(pg, t, P('Wasserwerke'), 'Wasserwerke und Kraftwerke fallen aus,', (110, 1110), serif(50, 400)); label(pg, t, P('Straßenzüge'), 'ganze Straßenzüge brennen.', (110, 1175), serif(50, 800))
    rule(pg, t, P('Jeden', 436.5) - 0.2, 1300)
    label(pg, t, P('Starzyński') - 0.2, 'Stefan Starzyński', (110, 1325), serif(80, 800)); note(pg, t, P('Stadtpräsident'), 'Stadtpräsident von Warschau', (110, 1435))
    label(pg, t, P('Rundfunk'), 'Jeden Abend im Rundfunk:', (110, 1490), serif(48, 400)); label(pg, t, P('Durchhalten'), 'Aufruf zum Durchhalten.', (110, 1550), serif(48, 800))
    label(pg, t, P('Haft'), 'Er stirbt später in deutscher Haft.', (110, 1620), serif(42, 400), ACC)
    return pg
def s10R(t):
    pg = base(22, False).copy(); t0 = P('Am', 451) - 0.2
    label(pg, t, t0, '25. SEPTEMBER 1939', (110, 200), sans(40, 800), ACC)
    cphoto(pg, t, t0 + 0.1, 'hoffmann_s86_0', (110, 260, 1180, 520), 'Warschau unter Beschuss, September 1939')
    label(pg, t, P('Luftangriff', 453), 'Der schwerste Luftangriff der Belagerung.', (110, 860), serif(52, 800))
    label(pg, t, P('Waffenstillstand'), '27.9. Bitte um Waffenstillstand', (110, 960), serif(46, 400)); label(pg, t, P('Kapitulation', 461), '28.9. Kapitulation', (110, 1025), serif(46, 800), ACC)
    label(pg, t, P('20.000'), 'über 20.000', (110, 1140), serif(80, 800), ACC); label(pg, t, P('Zivilisten', 466), 'tote Zivilisten', (110, 1250), serif(46, 400))
    label(pg, t, P('140.000'), 'rund 140.000', (740, 1140), serif(72, 800)); label(pg, t, P('Gefangenschaft', 468), 'Soldaten gefangen', (740, 1250), serif(46, 400))
    route(pg, t, P('Modlin'), [('29.9. Festung Modlin', P('Modlin')), ('Anfang Oktober: Hela', P('Hela', 475)), ('6.10. letzte Kämpfe bei Kock', P('Kock'))], 110, 1380, 82, size=42)
    cphoto(pg, t, P('Siegesparade') - 0.4, 'hoffmann_s94_0', (900, 1380, 390, 290), '5.10. Siegesparade')
    return pg

# ================= SP11: exile / the balance and the second treaty =================
def s11L(t):
    pg = base(23, True).copy(); t0 = TURNS[10] + 1.0
    head(pg, t, t0, 'IM EXIL', 'Polen hat nicht', 'kapituliert', size=100, w2=800)
    label(pg, t, P('Paris'), 'In Paris: Exilregierung unter', (110, 530), serif(50, 400)); label(pg, t, P('Sikorski'), 'General Władysław Sikorski', (110, 600), serif(56, 800))
    route(pg, t, P('Rumänien', 495), [('Polen', P('Rumänien', 495) - 0.2), ('über Rumänien und Ungarn', P('Ungarn')), ('Frankreich', P('Frankreich', 498))], 110, 760, 100, size=48)
    note(pg, t, P('weiterzukämpfen') - 0.2, 'Zehntausende Soldaten und Piloten fliehen, um weiterzukämpfen.', (110, 1080), 32)
    rule(pg, t, P('Rund', 504) - 0.2, 1200)
    label(pg, t, P('66.000') - 0.1, 'GEFALLEN', (110, 1240), sans(34, 800), GREY)
    label(pg, t, P('66.000'), 'rund 66.000', (110, 1290), serif(90, 800), ACC); note(pg, t, P('Soldaten', 505), 'polnische Soldaten', (110, 1410))
    label(pg, t, P('16.000'), 'etwa 16.000', (720, 1290), serif(90, 800)); note(pg, t, P('Mann', 509), 'Soldaten der Wehrmacht', (720, 1410))
    label(pg, t, P('Hunderttausende'), 'Hunderttausende Polen in deutscher', (110, 1530), serif(48, 400)); label(pg, t, P('sowjetische', 513), 'oder sowjetischer Gefangenschaft.', (110, 1590), serif(48, 400))
    return pg
B11 = (110, 330, 1180, 600)
def s11R(t):
    pg = base(24, False).copy(); t0 = P('Noch', 515.5) - 0.2
    label(pg, t, t0, 'MOSKAU, 28. SEPTEMBER 1939', (110, 200), sans(40, 800), ACC)
    framed(pg, t, t0 + 0.1, 'ribbentrop', B11, 'Ribbentrop fliegt nach Moskau')
    label(pg, t, P('Ribbentrop', 518) + 1.2, 'Ribbentrop und Molotow unterzeichnen', (110, 1010), serif(50, 400)); label(pg, t, max(P('Vertrag', 520), P('Ribbentrop', 518) + 1.3), 'einen weiteren Vertrag.', (110, 1075), serif(50, 800))
    cphoto(pg, t, P('Grenze', 523) - 0.2, 'soeldner_karte_s141', (110, 1180, 420, 520), 'Die neue Grenze (Söldner, 1939)', fy=0.3)
    label(pg, t, P('Bug'), 'Neue Grenze:', (620, 1200), serif(50, 400)); label(pg, t, P('Bug') + 0.1, 'im Wesentlichen der Bug.', (620, 1265), serif(50, 800), ACC)
    label(pg, t, P('Litauen'), 'Litauen fällt dafür in die', (620, 1380), serif(46, 400)); label(pg, t, P('Interessensphäre'), 'sowjetische Interessensphäre.', (620, 1440), serif(46, 400))
    return pg

# ================= SP12: the occupation =================
def s12L(t):
    pg = base(25, True).copy(); t0 = TURNS[11] + 1.0
    head(pg, t, t0, 'DIE BESATZUNG', 'Das General-', 'gouvernement', size=100, w2=800)
    label(pg, t, P('Reich', 530), 'Der Westen Polens wird direkt', (110, 520), serif(50, 400)); label(pg, t, P('Reich', 530) + 0.1, 'in das Reich eingegliedert.', (110, 585), serif(50, 400))
    cphoto(pg, t, P('Generalgouvernement') - 0.2, 'hoffmann_s67_0', (110, 700, 560, 560), 'Eine polnische Stadt, Herbst 1939')
    label(pg, t, P('Frank', 535), 'Hans Frank', (740, 720), serif(76, 800)); note(pg, t, P('Krakau', 538), 'an der Spitze, Sitz in Krakau', (740, 830))
    label(pg, t, P('Arbeitskraft'), 'Polen sollten nur noch', (740, 930), serif(46, 400)); label(pg, t, P('Arbeitskraft') + 0.1, 'als Arbeitskraft dienen.', (740, 990), serif(46, 800), ACC)
    label(pg, t, P('Gymnasien'), 'Hochschulen und Gymnasien geschlossen.', (110, 1360), serif(50, 800))
    label(pg, t, P('November', 548), 'SONDERAKTION KRAKAU · NOVEMBER 1939', (110, 1460), sans(32, 800), ACC)
    label(pg, t, P('180'), 'über 180', (110, 1500), serif(110, 800), ACC); label(pg, t, P('Professoren'), 'Professoren und Mitarbeiter', (600, 1530), serif(46, 400)); label(pg, t, P('Sachsenhausen'), 'ins KZ Sachsenhausen.', (600, 1590), serif(46, 800))
    return pg
def s12R(t):
    pg = base(26, False).copy(); t0 = P('In', 557.5) - 0.2
    label(pg, t, t0, 'PIOTRKÓW, OKTOBER 1939', (110, 200), sans(40, 800), ACC)
    label(pg, t, P('Ghetto'), 'Das erste Ghetto', (110, 250), serif(100, 800)); note(pg, t, P('Ghetto') + 0.2, 'im besetzten Polen', (110, 390))
    rule(pg, t, P('Auch', 563) - 0.2, 500)
    label(pg, t, P('sowjetisch', 563), 'IM SOWJETISCH BESETZTEN OSTEN', (110, 540), sans(36, 800), ACC)
    label(pg, t, P('Verhaftungen'), 'Verhaftungen und', (110, 600), serif(60, 400)); label(pg, t, P('Deportationen'), 'Deportationen.', (110, 680), serif(60, 800))
    rule(pg, t, P('Im', 567.5) - 0.2, 830)
    label(pg, t, P('Katyn') - 0.3, 'KATYN UND ANDERE ORTE · FRÜHJAHR 1940', (110, 870), sans(34, 800), ACC)
    label(pg, t, P('22.000'), 'rund 22.000', (110, 920), serif(150, 800), ACC)
    label(pg, t, P('Offiziere', 572), 'polnische Offiziere, Polizisten', (110, 1120), serif(52, 400)); label(pg, t, P('Intelligenz'), 'und Angehörige der Intelligenz,', (110, 1190), serif(52, 400))
    label(pg, t, P('NKWD'), 'erschossen vom sowjetischen NKWD.', (110, 1260), serif(52, 800))
    return pg

# ================= SP13: the end / Enigma =================
def s13L(t):
    pg = base(27, True).copy(); t0 = TURNS[12] + 1.0
    label(pg, t, t0, 'DIE BILANZ', (110, 200), sans(40, 800), ACC)
    label(pg, t, P('sechs', 581), 'Fast sechs Jahre Besatzung.', (110, 260), serif(66, 800))
    label(pg, t, P('Millionen', 584), '6 Millionen', (110, 420), serif(170, 800), ACC)
    label(pg, t, P('Staatsbürger'), 'polnische Staatsbürger überlebten', (110, 640), serif(56, 400)); label(pg, t, P('überlebten'), 'den Krieg nicht.', (110, 715), serif(56, 400))
    label(pg, t, P('Juden', 588), 'Etwa die Hälfte von ihnen waren Juden.', (110, 830), serif(56, 800))
    cphoto(pg, t, P('Juden', 588) + 0.4, 'eu_polnische_fluechtlinge_a', (110, 980, 1180, 640), 'Polnische Flüchtlinge, 1939')
    return pg
def s13R(t):
    pg = base(28, False).copy(); t0 = P('Doch', 591) - 0.2
    label(pg, t, t0, 'JULI 1939', (110, 200), sans(40, 800), ACC)
    label(pg, t, P('Juli', 595) - 0.3, 'Enigma', (110, 250), serif(170, 800))
    label(pg, t, P('Mathematiker'), 'Polnische Mathematiker zeigen britischen', (110, 470), serif(48, 400)); label(pg, t, P('Kryptologen'), 'und französischen Kryptologen,', (110, 535), serif(48, 400))
    label(pg, t, P('entschlüsseln'), 'wie sich die Enigma entschlüsseln lässt.', (110, 600), serif(48, 800))
    for i, nm in enumerate(('Marian Rejewski', 'Jerzy Różycki', 'Henryk Zygalski')):
        label(pg, t, P('entschlüsseln') + 0.4 + 0.3 * i, nm, (110, 740 + i * 80), serif(58, 700), ACC)
    label(pg, t, P('ahnte'), 'Die Wehrmacht ahnte davon nichts.', (110, 1040), italic(48), GREY)
    rule(pg, t, P('Im', 608) - 0.2, 1170)
    label(pg, t, P('trügerische') - 0.2, 'Im Westen:', (110, 1220), serif(60, 400)); label(pg, t, P('trügerische'), 'eine trügerische Ruhe.', (110, 1300), serif(60, 800))
    label(pg, t, P('nächsten'), 'Hitler plant bereits', (110, 1450), serif(76, 800), ACC); label(pg, t, P('Angriff', 612), 'den nächsten Angriff.', (110, 1550), serif(76, 400), ACC)
    return pg

# ================= SP14: the end page =================
def s14L(t):
    pg = base(29, True).copy(); t0 = VEND + 1.0
    label(pg, t, t0, 'FORTSETZUNG FOLGT', (110, 200), sans(46, 800), ACC)
    label(pg, t, t0 + 0.2, 'TEIL 3', (100, 250), serif(250, 900)); label(pg, t, t0 + 0.5, 'Der Krieg im Westen', (110, 560), serif(84, 400), GREY)
    cphoto(pg, t, t0 + 0.8, 'hoffmann_s77_0', (110, 720, 1180, 760))
    return pg
def s14R(t):
    pg = base(30, False).copy(); t0 = VEND + 1.6
    label(pg, t, t0, 'Gefällt dir die Serie?', (110, 220), serif(96, 800)); d = ImageDraw.Draw(pg)
    for i, nm in enumerate(('Liken', 'Teilen', 'Abonnieren')):
        tt = t0 + 0.5 + i * 0.6
        if t < tt: continue
        u = clamp((t - tt) / 0.45); y = 560 + i * 240
        d.ellipse((150, y - 70, 290, y + 70), outline=fade_col((200, 200, 200), u), width=4); d.ellipse((205, y - 15, 235, y + 15), fill=fade_col(ACC if i == 2 else TXT, u))
        d.text((360, y), nm, font=serif(90, 800 if i == 2 else 700), fill=fade_col(ACC if i == 2 else TXT, u), anchor='lm')
    label(pg, t, t0 + 2.6, 'damit du Teil 3 nicht verpasst.', (110, 1320), serif(60, 400), GREY)
    return pg

# ================= spreads, turns, camera =================
SPREADS = [(s0L, s0R), (s1L, s1R), (s2L, s2R), (s3L, s3R), (s4L, s4R), (s5L, s5R), (s6L, s6R), (s7L, s7R), (s8L, s8R), (s9L, s9R), (s10L, s10R),
           (s11L, s11R), (s12L, s12R), (s13L, s13R), (s14L, s14R)]
def last_word(after_word, a): return P(after_word, a)   # start of the last word of a spread
# each turn starts 0.5 s after the last word of the spread has appeared
TURNS = [P('begonnen', 22.5) + 0.5, P('Kampfflugzeuge') + 3.0, P('weiter', 89) + 0.5, P('Tage', 142) + 0.5, P('Panzerabwehrkanonen') + 0.5, P('Juden', 226) + 0.5,
         P('Gefangenschaft', 277.5) + 0.5, P('Sitzkrieg') + 0.5, P('Truppen', 375) + 0.5, P('Schottland') + 0.5, P('abgenommen', 485) + 0.5,
         P('Interessensphäre') + 0.5, P('Intelligenz') + 0.5, VEND + 0.3]
# the forces spread starts with its own sentence, not in the middle of the 1 September sentence block
TURNS[1] = P('Die', 45) - 1.1
T_END = VEND + 9.0
CAMS = [(0,) + fill('L', B0)]
FILMCAP = []
def cam(t_, c, cd=CD, cap=None):
    CAMS.append((t_ - cd,) + tuple(c) + (cd,))
    if cap: FILMCAP.append((t_, cap))
def turn_cam(i, first): cam(TURNS[i] + 0.35, OV, 0.65); cam(TURNS[i] + 1.15, first, 0.8)
# SP0
cam(T_PB + 1.0, OV, 1.0); cam(P('stand', 5) - 0.05, fr('R', 170, 760)); cam(P('Nach', 12) - 0.1, fr('R', 820, 1720))
# SP1
turn_cam(0, fr('L', 170, 1340)); cam(P('standen', 25) + 0.6, fill('L', B1), 1.2, ('1. September 1939', 'Der Schlagbaum an der polnischen Grenze fällt'))
cam(P('anderthalb') - 0.05, fr('L', 1300, 1700)); cam(P('Sie', 32) - 0.05, fr('R', 170, 1700, 0.62))
# SP2
turn_cam(1, fr('L', 170, 1700)); cam(P('Viele', 62) - 0.05, fr('R', 170, 980)); cam(P('Nur', 73) - 0.05, fr('R', 960, 1740))
# SP3
turn_cam(2, fill('L', B3)); FILMCAP.append((TURNS[2] + 1.15, ('Danzig, 1. September 1939, 4.45 Uhr', 'Die Schleswig-Holstein eröffnet das Feuer auf die Westerplatte')))
cam(P('Sturzkampfbomber', 95) - 0.1, fr('L', 1040, 1720)); cam(P('In', 111.5) - 0.05, fr('R', 170, 1000)); cam(P('Auf', 127.5) - 0.05, fr('R', 1080, 1720))
# SP4
turn_cam(3, fr('L', 170, 1220)); cam(P('Säbel') - 0.1, fr('L', 1240, 1700)); cam(P('Italienische') - 0.05, fr('R', 170, 1220)); cam(P('Die', 174) - 0.05, fr('R', 1220, 1720))
# SP5
turn_cam(4, fr('L', 170, 1320)); cam(P('Die', 197) - 0.05, fr('L', 1360, 1720)); cam(P('Nach', 207) - 0.05, fr('R', 170, 800)); cam(P('Hinter', 211) - 0.05, fr('R', 480, 1720))
# SP6
turn_cam(5, fill('L', B6)); FILMCAP.append((TURNS[5] + 1.15, ('September 1939', 'Deutsche Panzer- und motorisierte Divisionen stoßen vor')))
cam(P('Die', 236) - 0.05, fr('L', 1060, 1700)); cam(P('Nach', 244.5) - 0.05, fr('R', 170, 820)); cam(P('Westlich') - 0.05, fr('R', 900, 1720))
# SP7
turn_cam(6, fr('L', 170, 1220)); cam(P('75') - 0.1, fr('L', 1220, 1720)); cam(P('Polen', 306.5) - 0.05, fr('R', 170, 1240)); cam(P('Flugblätter') - 0.3, fr('R', 1240, 1720))
# SP8
turn_cam(7, fr('L', 170, 1360)); cam(P('Regierung', 364) - 0.1, fr('L', 1000, 1680)); cam(P('Wenige', 369) - 0.05, fill('R', B8), 1.1, ('Brest-Litowsk, September 1939', 'Deutsche und sowjetische Offiziere'))
cam(P('übergab') + 0.1, fr('R', 1040, 1720))
# SP9
turn_cam(8, fill('L', B9)); FILMCAP.append((TURNS[8] + 1.15, ('Danziger Bucht, September 1939', 'Schiffsartillerie beschießt die polnische Küste')))
cam(P('Hela') - 0.1, fr('L', 1040, 1650)); cam(P('Und', 396.5) - 0.05, fr('R', 170, 1000)); cam(P('Nacht', 412) - 0.1, fr('R', 900, 1720))
# SP10
turn_cam(9, fill('L', B10)); FILMCAP.append((TURNS[9] + 1.15, ('Warschau, September 1939', 'Aufnahmen des amerikanischen Kameramanns Julien Bryan')))
cam(P('Wasserwerke') - 0.1, fr('L', 1060, 1720)); cam(P('Am', 451) - 0.05, fr('R', 170, 1300)); cam(P('Modlin') - 0.1, fr('R', 1080, 1720))
# SP11
turn_cam(10, fr('L', 170, 1120)); cam(P('Rund', 504) - 0.05, fr('L', 1180, 1700)); cam(P('Noch', 515.5) - 0.05, fill('R', B11), 1.1, ('28. September 1939', 'Ribbentrop reist nach Moskau'))
cam(P('Ribbentrop', 518) + 1.2, fr('R', 980, 1720))
# SP12
turn_cam(11, fr('L', 170, 1300)); cam(P('Gymnasien') - 0.1, fr('L', 1300, 1720)); cam(P('In', 557.5) - 0.05, fr('R', 170, 820)); cam(P('Im', 567.5) - 0.05, fr('R', 820, 1340))
# SP13
turn_cam(12, fr('L', 170, 960)); cam(P('Juden', 588) + 0.3, fr('L', 900, 1720)); cam(P('Doch', 591) - 0.05, fr('R', 170, 1120)); cam(P('Im', 608) - 0.05, fr('R', 1120, 1720))
# SP14
cam(TURNS[13] + 0.35, OV, 0.65); cam(TURNS[13] + 1.8, (MID, 860, 0.68))
CAMS.sort(key=lambda c: c[0])
MAG = Book(SPREADS, TURNS, CAMS, spine=100)
# captions on screen while a film fills the frame: in when the camera has arrived, out with the next camera move
OVL = []
for ta, (c1, c2) in FILMCAP:
    nxt = min([c[0] for c in CAMS if c[0] > ta + 0.05] or [T_END]); OVL.append((ta + 0.3, nxt + 0.4, c1, c2))
# full-screen archive film laid over the magazine (cross-fades in and out)
FULL = [(P('Zehntausende', 276) - 0.3, TURNS[6] - 0.15, 'pows', 'September 1939', 'Polnische Kriegsgefangene')]
def frame(t):
    img = MAG(t)
    for a, b, nm, c1, c2 in FULL:
        if a - 0.5 <= t <= b + 0.5:
            img = blend(img, film(t, nm, a - 0.5, 0.0, 1.0, cap=c1, cap2=c2, t1=b + 0.3), min((t - a + 0.5) / 0.5, (b + 0.5 - t) / 0.5))
    for a, b, c1, c2 in OVL:
        if a <= t <= b: caption(img, t, a, c1, c2, b)
    if t < 0.6: img = blend(Image.new('RGB', (W, H), (0, 0, 0)), img, t / 0.6)
    if t > T_END - 1.2: img = blend(img, Image.new('RGB', (W, H), (0, 0, 0)), (t - (T_END - 1.2)) / 1.2)
    return img

if __name__ == '__main__':
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[2:]]; n = len(ts); Pc = Image.new('RGB', (3 * 640, ((n + 2) // 3) * 360))
        for i, t in enumerate(ts):
            im = frame(t); ImageDraw.Draw(im).text((20, 20), '%.1f' % t, font=sans(40, 800), fill=(255, 0, 255)); Pc.paste(im.resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
        Pc.save(LB + 'chk/prev.jpg', quality=86); sys.exit()
    if sys.argv[1] == 'pages':
        for i, (L, R) in enumerate(SPREADS):
            te = (TURNS[i] - 0.05) if i < len(TURNS) else T_END - 1.5
            spread_img(L(te), R(te)).convert('RGB').resize((SW // 3, PH // 3)).save(LB + 'chk/sp_%02d.jpg' % i, quality=85)
        sys.exit()
    if sys.argv[1] == 'T': print(round(T_END, 3)); sys.exit()
    if sys.argv[1] == 'turns': print(' '.join('%.2f' % x for x in TURNS)); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
        if n % 300 == 0: print('t', n / FPS, flush=True)
    p.stdin.close(); p.wait(); print('rc', p.returncode)
