# "Deutschland im Zweiten Weltkrieg", Teil 2: Der Überfall auf Polen, long version v2 (16:9). The Teil 1 magazine;
# text tied to the spoken words, a camera planned from the page elements (t2core), films filling the frame with their caption,
# slowly moving photos, red pen circles, counters, maps drawn on and small running pen drawings.
from t2core import *
from lmap import Map
from drawings import tank_m, uboat_m, monoplane_m
from drawings2 import soldier_m, civilian_m, truck_m, gold_m, radio_m, train_m, enigma_m
import drawings2

# ---------- turns: 2.5 s before the first word of each new spread (3 s of breathing room was put into the voice there) ----------
STARTS = ['Am Morgen des 1.', 'Die Wehrmacht verfügte', 'In denselben Minuten', 'Am Abend des ersten', 'Zwei Tage später kam', 'An der Front stießen',
          'Während die Armee kämpfte', 'Am frühen Morgen', 'An der Ostsee hielt', 'Warschau wurde nun', 'Doch Polen hatte nicht', 'Den Westen Polens', 'Für Polen begann']
TD = Book.TD
TURNS = [K(s) - 2.55 for s in STARTS] + [VEND + 0.6]
def TF(i): return TURNS[i - 1] + TD + 1.05          # a film that opens spread i fills the frame from here
FE = {1: K('rund anderthalb Millionen', 1) - 1.3, 3: K('warfen deutsche Sturzkampfbomber') - 1.3, 6: K('Die Luftwaffe zerstörte') - 1.3, 10: K('Jeden Abend sprach') - 1.3}
def TS(i): return TURNS[i - 1] + TD + 1.15          # the moment spread i lies open
T_END = VEND + 10.0

def base2(n, left): return base(n, left).copy()

# ================= SP0 =================
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
def s0L(t):
    pg = masthead().copy(); FILM(pg, t, -1, 'tanks', B0, 'Deutsche Panzer in Polen, September 1939', 0.8)
    L(pg, t, -1, 'Der Feldzug gegen Polen gilt bis heute', (110, 1400), serif(56, 400)); L(pg, t, -1, 'als der erste Blitzkrieg der Geschichte.', (110, 1478), serif(56, 400))
    UNDER(pg, t, -1, 520, 790, 1546)
    return pg
def s0R(t):
    pg = base2(2, False); t0 = K('Doch dieses Wort')
    KICK(pg, t, t0, 'EIN MYTHOS'); L(pg, t, t0 + 0.1, '„Blitzkrieg“', (110, 250), serif(150, 800))
    STRIKE(pg, t, K('keiner deutschen Dienstvorschrift', 2), 100, 900, 355, 12)
    SAY(pg, t, 'Doch dieses Wort stand in keiner deutschen Dienstvorschrift, und die polnische Armee kämpfte länger, als viele erwartet hatten.', (110, 470), 48, accent=('Dienstvorschrift',))
    PHOTO(pg, t, K('Nach fünf Wochen'), 'eu_warschau', (110, 760, 520, 560), 'Warschau, Herbst 1939', fy=0.4)
    COUNT(pg, t, K('Nach fünf Wochen', 1), 0.6, 5, (700, 730), serif(250, 800), lambda v: '%d' % round(v))
    L(pg, t, K('Nach fünf Wochen', 2), 'Wochen', (880, 860), serif(90, 400))
    CIRCLE(pg, t, K('Nach fünf Wochen', 2) + 0.5, (700, 790, 1190, 975))
    SAY(pg, t, 'war Polen trotzdem von der Landkarte verschwunden, aufgeteilt zwischen zwei Diktaturen.', (700, 1040), 44, maxw=590, accent=('zwei', 'Diktaturen.'))
    RULE(pg, t, K('Und hinter der Front') - 0.1, 1430)
    SAY(pg, t, 'Und hinter der Front hatte bereits ein Krieg gegen die Zivilbevölkerung begonnen.', (110, 1460), 46, maxw=840, accent=('Zivilbevölkerung',))
    DRAW(pg, t, K('gegen die Zivilbevölkerung'), 0.8, lambda ph: civilian_m(1150, 1620, 0.55, ph), (1110, 1440, 1210, 1630))
    return pg

# ================= SP1: 1 September =================
B1 = (110, 430, 1180, 600)
MAP39 = Map('m39', (PW, PH), (90, 300, 1220, 1160), 13.0, 26.6, 48.6)
def arrow(pg, m, t, t0, pts, dur=1.0, wd=16):
    if t < t0: return
    u = eio((t - t0) / dur); Q = [m.mp(*p) for p in pts]; segs = list(zip(Q, Q[1:])); Ln = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs)
    todo = u * Ln; d = ImageDraw.Draw(pg); E = Q[0]; ang = 0
    for a, b in segs:
        l = math.hypot(b[0] - a[0], b[1] - a[1]); v = min(1, todo / l); E = (lerp(a[0], b[0], v), lerp(a[1], b[1], v)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
        d.line((a, E), fill=ACC, width=wd); todo -= l
        if todo <= 0: break
    hd = 46; d.polygon([(E[0] + 18 * math.cos(ang), E[1] + 18 * math.sin(ang)), (E[0] - hd * math.cos(ang - 0.6), E[1] - hd * math.sin(ang - 0.6)), (E[0] - hd * math.cos(ang + 0.6), E[1] - hd * math.sin(ang + 0.6))], fill=ACC)
def poland_map(pg, t, t0, m, extra=()):
    k = eout((t - t0) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=('reich',), outline=('reich',))
    stamp_ink(pg, m.outline('poland').point(lambda v: int(v * k)), (0, 0), TXT); m.tint(pg, 'poland', k, ACC, 0.05)
    m.label(pg, t, t0 + 0.3, 'POLEN', (21.9, 51.3), sans(44, 800), TXT); m.pin(pg, t, t0 + 0.4, (21.01, 52.23), TXT, 10); m.label(pg, t, t0 + 0.4, 'Warschau', (21.01, 52.55), sans(28, 700), GREY, sw=4)
    m.label(pg, t, t0 + 0.4, 'DEUTSCHES REICH', (14.8 if m is MAP39 else 16.2, 51.6), sans(30, 700), GREY, sw=4); m.label(pg, t, t0 + 0.5, 'Ostsee', (17.0, 55.3) if m is MAP39 else (16.2, 54.75), italic(34), GREY, sw=4)
    m.label(pg, t, t0 + 0.3, 'Danzig', (18.65, 54.62), sans(26, 700), TXT, sw=4)
def s1L(t):
    pg = base2(3, True); t0 = FE[1] + 1.0
    KICK(pg, t, t0, '1. SEPTEMBER 1939'); L(pg, t, t0 + 0.1, 'Der Angriff', (110, 250), serif(110, 800))
    FILM(pg, t, TF(1) - 1.0, 'barrier', B1, 'Deutsche Soldaten am Schlagbaum der polnischen Grenze')
    COUNT(pg, t, K('rund anderthalb Millionen', 1), 1.0, 1.5, (110, 1150), serif(140, 800), lambda v: ('%.1f Millionen' % v).replace('.', ','))
    L(pg, t, K('Millionen deutsche Soldaten', 1), 'deutsche Soldaten', (110, 1330), serif(60, 400))
    DRAW(pg, t, K('Millionen deutsche Soldaten', 2), 0.8, lambda ph: soldier_m(1080, 1520, 0.62, ph), (1030, 1300, 1150, 1530))
    DRAW(pg, t, K('Millionen deutsche Soldaten', 2) + 0.3, 0.8, lambda ph: soldier_m(1200, 1520, 0.62, ph + 0.4), (1150, 1300, 1270, 1530))
    return pg
def s1R(t):
    pg = base2(4, False); t0 = K('Sie griffen aus drei'); m = MAP39
    L(pg, t, t0, 'Aus drei Richtungen zugleich', (110, 200), serif(74, 800))
    reg((100, 300, 1300, 1460), t0, kind='pic')
    if t >= t0:
        poland_map(pg, t, t0, m)
        for s_, ll, ph_, i in (('POMMERN', (16.3, 54.05), 'aus Pommern und', 1), ('OSTPREUSSEN', (21.3, 54.35), 'und Ostpreußen im', 1), ('SCHLESIEN', (17.1, 50.75), 'aus Schlesien im', 1), ('SLOWAKEI', (19.8, 48.85), 'aus der Slowakei', 2)):
            m.label(pg, t, K(ph_, i), s_, ll, sans(30, 800), ACC, sw=5)
        arrow(pg, m, t, K('aus Pommern und', 1) + 0.1, [(16.4, 53.75), (17.5, 53.35), (18.4, 53.05)])
        arrow(pg, m, t, K('und Ostpreußen im', 1) + 0.1, [(20.6, 53.75), (20.85, 53.05), (21.0, 52.55)])
        arrow(pg, m, t, K('aus Schlesien im', 1) + 0.1, [(17.9, 51.15), (18.9, 51.55), (19.7, 51.8)])
        arrow(pg, m, t, K('aus Schlesien im', 1) + 0.4, [(18.6, 50.3), (19.2, 50.15), (19.75, 50.08)])
        arrow(pg, m, t, K('aus der Slowakei', 2) + 0.1, [(20.7, 49.2), (21.0, 49.75), (21.5, 50.3)])
    SAY(pg, t, 'Polen war auf drei Seiten eingeschlossen.', (110, 1520), 54, wg=800)
    return pg

# ================= SP2: the forces / mobilisation / Peking Plan =================
def s2L(t):
    pg = base2(5, True); t0 = TS(2)
    KICK(pg, t, t0, 'DIE KRÄFTE'); L(pg, t, t0 + 0.1, 'Ungleiche Gegner', (110, 250), serif(100, 800))
    L(pg, t, t0 + 0.3, 'WEHRMACHT', (430, 450), sans(36, 800), TXT, 'mm'); L(pg, t, t0 + 0.3, 'POLEN', (990, 450), sans(36, 800), ACC, 'mm'); RULE(pg, t, t0 + 0.3, 490)
    rows = (('PANZER', K('mehr als 2.500 Panzer', 2), 2500, 'über %s', K('einige Hundert Panzer'), 'einige Hundert'),
            ('FLUGZEUGE', K('mehr als 2.000 Flugzeuge', 2), 2000, 'über %s', K('rund 400 einsatzbereite', 1), 'rund 400'),
            ('SOLDATEN', K('knapp eine Million'), None, '1,5 Millionen', K('knapp eine Million'), 'knapp 1 Million'))
    for i, (nm, ta, v, f, tb, sb) in enumerate(rows):
        y = 530 + i * 125; L(pg, t, min(ta, tb) - 0.2, nm, (110, y), sans(26, 700), GREY)
        if v: COUNT(pg, t, ta, 0.9, v, (300, y + 30), serif(60, 800), lambda x, f=f: f % de(x), TXT)
        else: L(pg, t, ta, f, (300, y + 30), serif(60, 800))
        L(pg, t, tb, sb, (800, y + 30), serif(60, 800), ACC)
    NOTE(pg, t, K('die meisten davon leichte'), 'Die meisten deutschen Panzer waren leichte Modelle.', (110, 920))
    FILM(pg, t, K('mehr als 2.500 Panzer', 2), 'panzer', (110, 990, 1180, 520), 'Deutsche Panzerverbände, September 1939')
    return pg
def s2R(t):
    pg = base2(6, False)
    SAY(pg, t, 'Viele Reservisten waren noch auf dem Weg zu ihren Einheiten.', (110, 200), 54, maxw=860)
    DRAW(pg, t, K('Viele Reservisten waren', 1), 0.8, lambda ph: soldier_m(1150, 400, 0.6, ph), (1100, 190, 1220, 410))
    PHOTO(pg, t, K('Auf Drängen Großbritanniens'), 'eu_chamberlain', (110, 470, 520, 500), 'Neville Chamberlain (rechts), 1939', fy=0.2)
    SAY(pg, t, 'Auf Drängen Großbritanniens und Frankreichs hatte Warschau die Generalmobilmachung verschoben, um Hitler keinen Vorwand zu liefern.', (690, 480), 44, maxw=600, accent=('Generalmobilmachung', 'verschoben,'))
    RULE(pg, t, K('Nur die kleine polnische') - 0.1, 1080)
    KICK(pg, t, K('Nur die kleine polnische'), 'DER PEKING-PLAN', 1110)
    SAY(pg, t, 'Nur die kleine polnische Marine hatte einen Teil ihrer Schiffe in Sicherheit gebracht.', (110, 1160), 42, maxw=1180)
    PHOTO(pg, t, K('Zwei Tage vor Kriegsbeginn'), 'eu_orp_blyskawica', (110, 1290, 460, 290))
    for i, (nm, ph_) in enumerate((('Burza', 'Zerstörer Burza,'), ('Błyskawica', 'Burza, Błyskawica und'), ('Grom', 'und Grom aus'))):
        L(pg, t, K(ph_, 1), nm, (630, 1290 + i * 66), serif(52, 800))
    ROUTE(pg, t, [('Ostsee', K('aus der Ostsee', 2)), ('Großbritannien', K('erreichten Großbritannien', 1))], 920, 1310, 80, 40)
    NOTE(pg, t, K('an der Seite der Royal'), 'an der Seite der Royal Navy', (630, 1500))
    return pg

# ================= SP3: Westerplatte, Wieluń / Post Office, Westerplatte =================
B3 = (110, 260, 1180, 620)
def s3L(t):
    pg = base2(7, True); t0 = FE[3] + 1.0
    KICK(pg, t, t0, 'DANZIG UND WIELUŃ, 1. SEPTEMBER 1939')
    FILM(pg, t, TF(3) - 1.0, 'ship', B3, 'Das Linienschiff Schleswig-Holstein beschießt die Westerplatte')
    PHOTO(pg, t, K('warfen deutsche Sturzkampfbomber'), 'hoffmann_s23_0', (110, 1010, 500, 470), 'Blick aus einem Sturzkampfbomber')
    DRAW(pg, t, K('warfen deutsche Sturzkampfbomber', 2), 0.7, lambda ph: monoplane_m(1110, 1040, 0.26, ph), (980, 990, 1240, 1090))
    L(pg, t, K('Bomben auf Wieluń', 2), 'Wieluń', (660, 1100), serif(96, 800))
    SAY(pg, t, 'eine Kleinstadt ohne militärische Bedeutung.', (660, 1230), 42, maxw=630)
    SAY(pg, t, 'Auch das Krankenhaus wurde getroffen.', (660, 1340), 42, maxw=630, accent=('Krankenhaus',))
    SAY(pg, t, 'Hunderte Einwohner starben, der größte Teil der Innenstadt lag in Trümmern.', (660, 1470), 36, maxw=630)
    return pg
def s3R(t):
    pg = base2(8, False); t0 = K('In Danzig verteidigten')
    KICK(pg, t, t0, 'DIE POLNISCHE POST IN DANZIG')
    PHOTO(pg, t, t0, 'kampf_um_danzig_seite_40-040', (110, 260, 500, 700), '„Kampf um Danzig“, 1939', fy=0.3, zoom=0.05)
    SAY(pg, t, 'In Danzig verteidigten polnische Postbeamte stundenlang ihr Postamt. Erst als das Gebäude in Brand gesetzt wurde, ergaben sie sich.', (660, 270), 42, maxw=630, accent=('stundenlang',))
    SAY(pg, t, 'Die meisten Überlebenden wurden einige Wochen später von einem deutschen Kriegsgericht zum Tode verurteilt und erschossen.', (660, 720), 40, maxw=630, accent=('Kriegsgericht', 'Tode', 'verurteilt', 'erschossen.'))
    RULE(pg, t, K('Auf der Westerplatte hielten') - 0.1, 1110)
    KICK(pg, t, K('Auf der Westerplatte hielten'), 'DIE WESTERPLATTE', 1140)
    PHOTO(pg, t, K('Auf der Westerplatte hielten'), 'eu_westerplatte_collage', (110, 1190, 560, 400), zoom=0.04)
    COUNT(pg, t, K('rund 200 polnische', 1), 0.8, 200, (720, 1190), serif(56, 800), lambda v: 'rund %d Soldaten' % round(v), TXT)
    L(pg, t, K('Major Henryk Sucharski', 1), 'Major Henryk Sucharski', (720, 1260), serif(40, 400))
    L(pg, t, K('dass sie zwölf Stunden', 2), '12 Stunden', (720, 1340), serif(70, 800), GREY)
    STRIKE(pg, t, K('Es wurden sieben'), 710, 1110, 1390, 9)
    L(pg, t, K('wurden sieben Tage', 1), '7 Tage', (720, 1440), serif(100, 800), ACC)
    CIRCLE(pg, t, K('wurden sieben Tage', 2) + 0.4, (720, 1455, 1050, 1555), pad=18)
    return pg

# ================= SP4: Krojanty =================
def s4L(t):
    pg = base2(9, True); t0 = TS(4)
    KICK(pg, t, t0, 'KROJANTY, 1. SEPTEMBER 1939, ABENDS'); L(pg, t, t0 + 0.1, 'Die Ulanen', (110, 250), serif(110, 800))
    PHOTO(pg, t, t0 + 0.2, 'hoffmann_s29_0', (110, 430, 1180, 600), 'Pferde und Fahrzeuge auf einer Straße in Polen, September 1939')
    SAY(pg, t, 'Am Abend des ersten Kriegstages griffen bei Krojanty polnische Ulanen mit gezogenem Säbel eine deutsche Infanterieeinheit an und schlugen sie zurück.', (110, 1140), 46, accent=('Krojanty',))
    SAY(pg, t, 'Dann tauchten deutsche Panzerspähwagen auf und eröffneten das Feuer.', (110, 1400), 46, wg=800, accent=('Panzerspähwagen',))
    return pg
def s4R(t):
    pg = base2(10, False); t0 = K('Italienische Kriegsberichterstatter, die')
    KICK(pg, t, t0, 'DER MYTHOS')
    L(pg, t, K('mit Lanzen gegen Panzer'), 'Mit Lanzen', (110, 250), serif(110, 800)); L(pg, t, K('mit Lanzen gegen Panzer', 2), 'gegen Panzer', (110, 380), serif(110, 400))
    DRAW(pg, t, K('gegen Panzer anritten', 1), 0.8, lambda ph: tank_m(1030, 470, 0.34, ph), (860, 380, 1220, 520))
    SAY(pg, t, 'Italienische Kriegsberichterstatter, die das Schlachtfeld kurz darauf besuchten, machten daraus eine Geschichte von Reitern, die mit Lanzen gegen Panzer anritten.', (110, 560), 40)
    SAY(pg, t, 'Die deutsche Propaganda verbreitete sie weiter.', (110, 790), 40)
    STRIKE(pg, t, K('aber sie ist falsch', 3), 100, 760, 320, 12)
    L(pg, t, K('aber sie ist falsch', 3), 'Falsch.', (110, 880), serif(100, 800), ACC)
    KICK(pg, t, K('Die polnische Kavallerie kämpfte'), 'DIE WIRKLICHKEIT', 1060)
    SAY(pg, t, 'Die polnische Kavallerie kämpfte meist abgesessen wie Infanterie und besaß eigene Panzerabwehrkanonen.', (110, 1110), 44, maxw=600, accent=('Panzerabwehrkanonen.',))
    PHOTO(pg, t, K('Die polnische Kavallerie kämpfte'), 'hoffmann_s30_1', (760, 1100, 530, 400), 'Bespannte Geschütze, 1939')
    return pg

# ================= SP5: Bromberg / Einsatzgruppen =================
def s5L(t):
    pg = base2(11, True); t0 = TS(5)
    KICK(pg, t, t0, 'BROMBERG, 3. SEPTEMBER 1939'); L(pg, t, t0 + 0.1, 'Schüsse in der Stadt', (110, 250), serif(96, 800))
    PHOTO(pg, t, t0 + 0.2, 'hoffmann_s33_0', (110, 410, 540, 620), 'Eine zerstörte Straße in Polen, 1939')
    SAY(pg, t, 'Zwei Tage später kam es in Bromberg zu Schusswechseln zwischen polnischen Soldaten und Angehörigen der deutschen Minderheit.', (700, 420), 42, maxw=590, accent=('Bromberg',))
    COUNT(pg, t, K('Mehr als hundert Volksdeutsche'), 0.8, 100, (700, 850), serif(72, 800), lambda v: 'mehr als %d' % round(v))
    L(pg, t, K('hundert Volksdeutsche wurden', 1), 'Volksdeutsche getötet', (700, 950), serif(44, 400))
    SAY(pg, t, 'Wie es dazu kam und wie viele Opfer es genau waren, ist bis heute umstritten.', (110, 1140), 44, accent=('umstritten.',))
    RULE(pg, t, K('Die nationalsozialistische Propaganda sprach') - 0.1, 1290)
    SAY(pg, t, 'Die nationalsozialistische Propaganda sprach vom Bromberger Blutsonntag, vervielfachte die Zahl der Opfer und rechtfertigte damit Massenerschießungen.', (110, 1320), 42, accent=('Bromberger', 'Blutsonntag,', 'Massenerschießungen.'))
    return pg
def s5R(t):
    pg = base2(12, False)
    SAY(pg, t, 'Nach der Einnahme der Stadt wurden Hunderte polnische Einwohner hingerichtet.', (110, 200), 50, accent=('hingerichtet.',))
    RULE(pg, t, K('Hinter den Truppen folgten') - 0.1, 380)
    KICK(pg, t, K('Hinter den Truppen folgten'), 'HINTER DEN TRUPPEN', 410)
    L(pg, t, K('folgten Einsatzgruppen der', 1), 'Einsatzgruppen', (110, 460), serif(100, 800))
    NOTE(pg, t, K('der Sicherheitspolizei und'), 'der Sicherheitspolizei und des SD', (110, 590))
    L(pg, t, K('Sie führten Listen'), 'Auf ihren Listen standen:', (110, 670), serif(50, 400))
    for i, (w_, ph_) in enumerate((('Lehrer', 'denen Lehrer,'), ('Priester', 'Lehrer, Priester,'), ('Ärzte', 'Priester, Ärzte,'), ('Beamte', 'Ärzte, Beamte und'), ('Gutsbesitzer', 'und Gutsbesitzer standen'))):
        tw = K(ph_, 1 if i else 1); L(pg, t, tw, w_, (170, 750 + i * 76), serif(56, 700)); UNDER(pg, t, tw, 110, 145, 785 + i * 76, 5)
    DRAW(pg, t, K('Sie führten Listen'), 1.0, lambda ph: X.paper_m(1000, 960, 0.9, ph), (880, 800, 1130, 1130))
    SAY(pg, t, 'Bis zum Jahresende ermordeten deutsche Einheiten Zehntausende polnische Zivilisten, darunter viele Juden.', (110, 1200), 48, accent=('Zehntausende',))
    return pg

# ================= SP6: advance, Warsaw's barricades, Bzura =================
def s6L(t):
    pg = base2(13, True); t0 = FE[6] + 1.0
    KICK(pg, t, t0, 'DER VORMARSCH')
    FILM(pg, t, TF(6) - 1.0, 'moto', (110, 260, 1180, 600), 'Motorisierte Truppen im Vormarsch, September 1939')
    FILM(pg, t, K('Die Luftwaffe zerstörte'), 'bridges', (110, 990, 540, 470), 'Zerstörte Brücken, September 1939')
    DRAW(pg, t, K('Die Luftwaffe zerstörte'), 0.7, lambda ph: monoplane_m(1100, 1020, 0.26, ph), (970, 970, 1230, 1070))
    for i, (w_, ph_) in enumerate((('Flugplätze', 'zerstörte Flugplätze,'), ('Brücken', 'Flugplätze, Brücken und'), ('Bahnlinien', 'und Bahnlinien und'))):
        L(pg, t, K(ph_, 1), w_, (700, 1090 + i * 80), serif(58, 800))
    SAY(pg, t, 'und griff Kolonnen auf den Straßen an, auch Flüchtlingstrecks.', (700, 1350), 42, maxw=590, accent=('Flüchtlingstrecks.',))
    return pg
def s6R(t):
    pg = base2(14, False); t0 = K('Nach einer Woche erreichten')
    KICK(pg, t, t0, 'NACH EINER WOCHE')
    FILM(pg, t, t0, 'pows', (110, 250, 560, 470), 'Polnische Kriegsgefangene, September 1939')
    SAY(pg, t, 'Nach einer Woche erreichten die ersten deutschen Panzer den Stadtrand von Warschau. Ein erster Angriff auf die Stadt scheiterte an den Barrikaden der Verteidiger.', (720, 260), 42, maxw=570, accent=('Barrikaden',))
    RULE(pg, t, K('Westlich der Hauptstadt') - 0.1, 850)
    KICK(pg, t, K('Westlich der Hauptstadt'), 'DIE SCHLACHT AN DER BZURA', 880)
    PHOTO(pg, t, K('Westlich der Hauptstadt'), 'soeldner_karte_s073', (110, 930, 440, 640), fy=0.3, zoom=0.05)
    SAY(pg, t, 'Westlich der Hauptstadt hatten sich inzwischen zwei polnische Armeen gesammelt, die von der Grenze zurückgewichen waren.', (600, 940), 40, maxw=690)
    L(pg, t, K('Am 9. September griffen'), '9. September', (600, 1150), serif(50, 800), ACC)
    SAY(pg, t, 'Daraus wurde die größte Schlacht des Feldzugs.', (600, 1220), 44, maxw=690, accent=('größte', 'Schlacht'))
    SAY(pg, t, 'Einige Tage lang gerieten deutsche Divisionen in Bedrängnis, dann wurden die polnischen Verbände eingekesselt.', (600, 1350), 38, maxw=690, accent=('eingekesselt.',))
    return pg

# ================= SP7: the gold / the West =================
def s7L(t):
    pg = base2(15, True); t0 = TS(7)
    KICK(pg, t, t0, 'DER STAATSSCHATZ'); L(pg, t, t0 + 0.1, 'Das Gold der Polen', (110, 250), serif(96, 800))
    PHOTO(pg, t, t0 + 0.2, 'eu_polnische_fluechtlinge_b', (110, 400, 1180, 520), 'Flüchtlinge auf einer Landstraße, September 1939')
    COUNT(pg, t, K('rund 75 Tonnen', 1), 0.8, 75, (110, 1010), serif(72, 800), lambda v: 'rund %d Tonnen Gold' % round(v))
    NOTE(pg, t, K('der polnischen Nationalbank'), 'der polnischen Nationalbank', (110, 1110))
    DRAW(pg, t, K('rund 75 Tonnen', 1), 0.8, lambda ph: gold_m(1080, 1130, 0.62, ph), (930, 1020, 1230, 1140))
    ROUTE(pg, t, [('Warschau', K('Nationalbank die Hauptstadt', 2)), ('rumänische Grenze', K('Konvoi die rumänische', 2)), ('Schwarzes Meer', K('zum Schwarzen Meer', 1)),
                  ('Türkei', K('über die Türkei', 2)), ('Frankreich', K('Türkei nach Frankreich', 2))], 110, 1200, 72, 40)
    DRAW(pg, t, K('erreichte der Konvoi'), 0.8, lambda ph: truck_m(960, 1460, 0.62, ph), (830, 1340, 1080, 1470))
    L(pg, t, K('Die deutsche Seite bekam'), 'Die Deutschen bekamen es nie.', (700, 1530), serif(40, 800))
    return pg
def s7R(t):
    pg = base2(16, False); t0 = K('Polen wartete auf Hilfe')
    KICK(pg, t, t0, 'DER WESTEN'); L(pg, t, t0 + 0.1, 'Polen wartet', (110, 250), serif(96, 800))
    SAY(pg, t, 'Frankreich hatte zugesagt, spätestens zwei Wochen nach der Mobilmachung mit einer großen Offensive gegen Deutschland zu beginnen.', (110, 400), 42)
    PHOTO(pg, t, K('Tatsächlich rückten französische'), 'eu_kriegskrise_1939_c', (110, 620, 480, 480), 'Großbritannien, September 1939')
    SAY(pg, t, 'Tatsächlich rückten französische Truppen am 7. September ins Saarland vor, einige Kilometer weit, durch geräumte Dörfer. Dann blieben sie stehen, und im Oktober zogen sie sich wieder zurück.', (640, 630), 40, maxw=650, accent=('Saarland',))
    SAY(pg, t, 'Britische Bomber warfen über Deutschland vor allem Flugblätter ab.', (110, 1240), 42, maxw=700, accent=('Flugblätter',))
    DRAW(pg, t, K('vor allem Flugblätter', 2), 0.3, lambda ph: ([], [], [(X.notes_m(860, 1200, 420, 160, ph, 10, 5), 0.7)]), (860, 1200, 1280, 1360))
    RULE(pg, t, K('Die Franzosen nannten') - 0.1, 1390)
    L(pg, t, K('Zeit drôle de guerre', 1), 'drôle de guerre', (110, 1410), italic(76, 400))
    NOTE(pg, t, K('den seltsamen Krieg', 1), 'der seltsame Krieg', (120, 1510))
    L(pg, t, K('hieß sie Sitzkrieg', 2), 'Sitzkrieg', (760, 1420), serif(90, 800), ACC)
    return pg

# ================= SP8: the Red Army / Brest =================
MAP17 = Map('m17', (PW, PH), (110, 400, 1180, 880), 14.0, 29.0, 48.2)
def s8L(t):
    pg = base2(17, True); t0 = TS(8); m = MAP17
    KICK(pg, t, t0, '17. SEPTEMBER 1939'); L(pg, t, t0 + 0.1, 'Die Rote Armee', (110, 250), serif(110, 800))
    reg((110, 400, 1290, 1280), t0, kind='pic')
    if t >= t0:
        poland_map(pg, t, t0, m); m.label(pg, t, t0 + 0.5, 'SOWJETUNION', (26.9, 54.75), sans(30, 800), GREY, sw=4)
        ta = K('überschritt die Rote Armee', 1)
        for i, pts in enumerate(([(28.6, 54.4), (26.7, 53.8)], [(28.4, 52.7), (26.3, 52.4)], [(28.2, 51.2), (26.0, 51.1)], [(27.9, 49.8), (25.8, 49.9)])):
            arrow(pg, m, t, ta + 0.15 * i, pts, 0.9)
        m.label(pg, t, K('Im Osten standen kaum'), 'kaum noch polnische Truppen', (24.6, 50.6), italic(28), ACC, sw=5)
        m.pin(pg, t, K('Land über die rumänische', 3), (25.18, 48.4), TXT, 9); m.label(pg, t, K('Land über die rumänische', 3), 'Regierung nach Rumänien', (22.8, 48.6), sans(26, 700), TXT, sw=4)
    SAY(pg, t, 'Moskau erklärte, der polnische Staat existiere nicht mehr und man komme, um Ukrainer und Weißrussen zu schützen.', (110, 1320), 40)
    SAY(pg, t, 'Tatsächlich setzte die Sowjetunion das geheime Zusatzprotokoll des Hitler-Stalin-Pakts um.', (110, 1450), 40, accent=('Zusatzprotokoll', 'Hitler-Stalin-Pakts'))
    return pg
def s8R(t):
    pg = base2(18, False); t0 = K('Wenige Tage später übergab')
    KICK(pg, t, K('General Heinz Guderian') + 0.5, 'BREST-LITOWSK, 22. SEPTEMBER 1939')
    FILM(pg, t, t0, 'officers', (110, 260, 1180, 600), 'Deutsche und sowjetische Offiziere an der Demarkationslinie')
    FILM(pg, t, K('General Heinz Guderian') + 0.9, 'brest', (110, 1090, 640, 400), 'Gemeinsamer Vorbeimarsch')
    L(pg, t, K('General Heinz Guderian', 1), 'Heinz Guderian', (800, 1100), serif(48, 800))
    L(pg, t, K('Semjon Kriwoschein nahmen'), 'Semjon Kriwoschein', (800, 1170), serif(48, 800), ACC)
    return pg

# ================= SP9: Hela / Orzeł =================
MAPB = Map('balt', (PW, PH), (110, 470, 1180, 620), -5.0, 30.0, 53.4)
ORZ = [(24.75, 59.47), (23.0, 59.3), (20.6, 58.3), (19.3, 56.7), (16.6, 55.62), (14.2, 55.3), (12.8, 55.6), (12.65, 56.05), (11.8, 56.9), (11.0, 57.85), (9.0, 58.1),
       (5.0, 57.6), (0.0, 56.8), (-2.3, 56.2), (-3.35, 56.03)]
def s9L(t):
    pg = base2(19, True); t0 = TS(9)
    KICK(pg, t, t0, 'AN DER OSTSEE')
    L(pg, t, K('hielt sich die Halbinsel Hela', 4), 'Die Halbinsel Hela', (110, 250), serif(96, 800))
    SAY(pg, t, 'ein schmaler Landstreifen gegenüber von Gdingen, auf dem sich rund 2.800 polnische Soldaten und Marineangehörige unter Konteradmiral Józef Unrug verschanzt hatten.', (110, 390), 42, accent=('Józef', 'Unrug'))
    COUNT(pg, t, K('rund 2.800 polnische', 1), 1.0, 2800, (110, 600), serif(110, 800), lambda v: de(v))
    FILM(pg, t, t0 + 0.1, 'ship2', (110, 800, 1180, 560), 'Deutsche Schiffsartillerie vor der Danziger Bucht, September 1939')
    return pg
def s9R(t):
    pg = base2(20, False); t0 = K('Und weiter nördlich gelang'); m = MAPB
    KICK(pg, t, t0, 'DIE FLUCHT DER ORZEŁ')
    DRAW(pg, t, t0, 0.9, lambda ph: uboat_m(820, 330, 0.62, ph), (480, 250, 1170, 420))
    reg((110, 470, 1290, 1090), t0, kind='pic')
    if t >= t0:
        k = eout((t - t0) / 0.8); m.frame(pg, k); stamp_ink(pg, m.ground().point(lambda v: int(v * 0.55 * k)), (0, 0), (150, 150, 150))
        m.label(pg, t, t0 + 0.3, 'Ostsee', (19.0, 56.0), italic(30), GREY, sw=4); m.label(pg, t, t0 + 0.3, 'Nordsee', (3.0, 56.2), italic(30), GREY, sw=4)
        m.pin(pg, t, K('Hafen von Tallinn', 2), (24.75, 59.44), TXT, 9); m.label(pg, t, K('Hafen von Tallinn', 2), 'Tallinn', (24.75, 59.95), sans(26, 800), TXT, sw=4)
        m.line(pg, t, K('brach die Besatzung aus'), KE('erreichte Mitte Oktober Schottland') - K('brach die Besatzung aus'), ORZ, ACC, 6, dash=12)
        m.pin(pg, t, K('Oktober Schottland.', 1), (-3.35, 56.03), ACC, 10); m.label(pg, t, K('Oktober Schottland.', 1), 'Schottland', (-2.6, 56.6), sans(26, 800), ACC, sw=4)
    SAY(pg, t, 'Die Orzeł war in den neutralen Hafen von Tallinn eingelaufen und dort festgesetzt worden. Die Esten nahmen ihr die Seekarten ab und einen Teil der Munition.', (110, 1130), 40)
    SAY(pg, t, 'In der Nacht zum 18. September brach die Besatzung aus dem Hafen aus.', (110, 1330), 40, wg=800)
    SAY(pg, t, 'Ohne Karten, nur mit einer selbst gezeichneten Liste der Leuchttürme, schlich sie wochenlang durch die Ostsee und durch die Meerengen und erreichte Mitte Oktober Schottland.', (110, 1445), 36, accent=('Leuchttürme,', 'Schottland.'))
    return pg

# ================= SP10: the siege of Warsaw =================
def s10L(t):
    pg = base2(21, True); t0 = FE[10] + 1.0
    KICK(pg, t, t0, 'DIE BELAGERUNG VON WARSCHAU')
    FILM(pg, t, TF(10) - 1.0, 'wfire', (110, 260, 1180, 620), 'Warschau brennt, September 1939 (Aufnahme: Julien Bryan)')
    PHOTO(pg, t, K('Jeden Abend sprach'), 'hoffmann_s86_1', (110, 990, 480, 420), 'Verteidiger in Warschau, 1939')
    L(pg, t, K('Stadtpräsident Stefan Starzyński', 1), 'Stefan Starzyński', (640, 990), serif(62, 800))
    NOTE(pg, t, K('Stadtpräsident Stefan Starzyński'), 'Stadtpräsident von Warschau', (640, 1080))
    L(pg, t, K('im Rundfunk zu'), 'Jeden Abend im Rundfunk:', (640, 1140), serif(42, 400))
    L(pg, t, K('zum Durchhalten auf'), 'Aufruf zum Durchhalten.', (640, 1200), serif(42, 800), ACC)
    DRAW(pg, t, K('im Rundfunk zu'), 0.8, lambda ph: radio_m(1180, 1440, 0.55, ph), (1080, 1340, 1280, 1500))
    SAY(pg, t, 'Nach der Kapitulation blieb er in der Stadt. Die Deutschen verhafteten ihn, und er kam später in deutscher Haft ums Leben.', (640, 1290), 36, maxw=420, accent=('Haft',))
    return pg
def s10R(t):
    pg = base2(22, False); t0 = K('Am 25. September erlebte')
    KICK(pg, t, t0, '25. SEPTEMBER 1939')
    PHOTO(pg, t, t0, 'hoffmann_s86_0', (110, 250, 1180, 460), 'Warschau unter Beschuss, September 1939')
    SAY(pg, t, 'Am 25. September erlebte die Stadt den schwersten Luftangriff der Belagerung.', (110, 810), 44, accent=('schwersten', 'Luftangriff'))
    ROUTE(pg, t, [('27.9. Bitte um Waffenstillstand', K('bat die Stadt um', 3)), ('28.9. Kapitulation', K('wurde die Kapitulation unterzeichnet', 2))], 110, 960, 64, 38)
    COUNT(pg, t, K('Mehr als 20.000 Zivilisten', 2), 1.0, 20000, (110, 1110), serif(70, 800), lambda v: 'über ' + de(v))
    NOTE(pg, t, K('Zivilisten waren in Warschau'), 'tote Zivilisten', (110, 1200))
    COUNT(pg, t, K('rund 140.000 Soldaten', 1), 1.0, 140000, (720, 1110), serif(70, 800), lambda v: de(v), TXT)
    NOTE(pg, t, K('Soldaten gingen in Gefangenschaft. Die'), 'Soldaten in Gefangenschaft', (720, 1200))
    ROUTE(pg, t, [('29.9. Festung Modlin', K('Die Festung Modlin', 2)), ('Anfang Oktober: Hela', K('die Halbinsel Hela Anfang', 2)), ('6.10. letzte Kämpfe bei Kock', K('Oktober bei Kock', 2))], 110, 1290, 64, 36)
    PHOTO(pg, t, K('eine Siegesparade abgenommen'), 'hoffmann_s94_0', (900, 1290, 390, 260))
    NOTE(pg, t, K('eine Siegesparade abgenommen'), '5.10.: Siegesparade', (900, 1570), 28)
    return pg

# ================= SP11: exile, balance / the treaty =================
def s11L(t):
    pg = base2(23, True); t0 = TS(11)
    KICK(pg, t, t0, 'IM EXIL'); L(pg, t, t0 + 0.1, 'Polen hat nicht kapituliert', (110, 250), serif(84, 800))
    PHOTO(pg, t, K('In Paris bildete'), 'eu_exil_portrait', (110, 400, 420, 520), 'General Władysław Sikorski', fy=0.2, zoom=0.05)
    SAY(pg, t, 'In Paris bildete sich eine Exilregierung unter General Władysław Sikorski.', (580, 410), 44, maxw=710, accent=('Exilregierung',))
    SAY(pg, t, 'Zehntausende polnische Soldaten und Piloten waren über Rumänien und Ungarn geflohen und schlugen sich nach Frankreich durch, um dort weiterzukämpfen.', (580, 600), 38, maxw=500)
    DRAW(pg, t, K('Zehntausende polnische Soldaten und'), 0.8, lambda ph: soldier_m(1200, 990, 0.5, ph), (1155, 820, 1250, 1000))
    RULE(pg, t, K('Rund 66.000 polnische') - 0.1, 1080)
    KICK(pg, t, K('Rund 66.000 polnische'), 'DIE BILANZ', 1110)
    COUNT(pg, t, K('Rund 66.000 polnische', 1), 1.0, 66000, (110, 1160), serif(80, 800), lambda v: 'rund ' + de(v))
    NOTE(pg, t, K('polnische Soldaten waren gefallen', 2), 'gefallene polnische Soldaten', (110, 1260))
    COUNT(pg, t, K('etwa 16.000 Mann', 1), 1.0, 16000, (720, 1160), serif(80, 800), lambda v: 'etwa ' + de(v), TXT)
    NOTE(pg, t, K('etwa 16.000 Mann', 2), 'Soldaten der Wehrmacht', (720, 1260))
    SAY(pg, t, 'Hunderttausende Polen gerieten in deutsche oder sowjetische Gefangenschaft.', (110, 1340), 44)
    return pg
def s11R(t):
    pg = base2(24, False); t0 = K('Noch am Tag der')
    KICK(pg, t, K('Die neue Grenze folgte') - 0.2, 'MOSKAU, 28. SEPTEMBER 1939')
    FILM(pg, t, t0, 'ribbentrop', (110, 260, 1180, 560), 'Ribbentrop fliegt nach Moskau')
    PHOTO(pg, t, K('Die neue Grenze folgte'), 'soeldner_karte_s141', (110, 920, 440, 640), fy=0.3, zoom=0.05)
    SAY(pg, t, 'Die neue Grenze folgte im Wesentlichen dem Fluss Bug, und Litauen fiel dafür in die sowjetische Interessensphäre.', (600, 930), 44, maxw=690, accent=('Bug,', 'Litauen'))
    NOTE(pg, t, K('Die neue Grenze folgte'), 'Karte aus einem Buch von 1939', (600, 1250))
    return pg

# ================= SP12: occupation =================
def s12L(t):
    pg = base2(25, True); t0 = TS(12)
    KICK(pg, t, t0, 'DIE BESATZUNG'); L(pg, t, t0 + 0.1, 'Das Generalgouvernement', (110, 250), serif(84, 800))
    SAY(pg, t, 'Den Westen Polens gliederte Deutschland direkt in das Reich ein.', (110, 390), 44)
    PHOTO(pg, t, K('Aus dem übrigen besetzten'), 'hoffmann_s67_0', (110, 520, 540, 520), 'Eine polnische Stadt, Herbst 1939')
    SAY(pg, t, 'Aus dem übrigen besetzten Gebiet wurde das Generalgouvernement, mit Hans Frank an der Spitze und Sitz in Krakau.', (700, 530), 40, maxw=590, accent=('Hans', 'Frank', 'Krakau.'))
    SAY(pg, t, 'Die polnische Bevölkerung sollte dort nur noch als Arbeitskraft dienen.', (700, 870), 40, maxw=590, accent=('Arbeitskraft',))
    SAY(pg, t, 'Hochschulen und Gymnasien wurden geschlossen.', (110, 1130), 46, wg=800)
    KICK(pg, t, K('Im November verhaftete'), 'SONDERAKTION KRAKAU, NOVEMBER 1939', 1230)
    COUNT(pg, t, K('über 180 Professoren', 1), 0.8, 180, (110, 1280), serif(96, 800), lambda v: 'über %d' % round(v))
    SAY(pg, t, 'Professoren und Mitarbeiter der Universität und brachte sie in das Konzentrationslager Sachsenhausen.', (540, 1290), 36, maxw=750, accent=('Sachsenhausen.',))
    return pg
def s12R(t):
    pg = base2(26, False); t0 = K('In Piotrków war')
    KICK(pg, t, t0, 'PIOTRKÓW, OKTOBER 1939'); L(pg, t, K('das erste Ghetto', 1), 'Das erste Ghetto', (110, 250), serif(96, 800)); NOTE(pg, t, K('das erste Ghetto', 2), 'im besetzten Polen', (110, 380))
    RULE(pg, t, K('Auch im sowjetisch') - 0.1, 450)
    SAY(pg, t, 'Auch im sowjetisch besetzten Osten begannen Verhaftungen und Deportationen.', (110, 480), 48, accent=('Verhaftungen', 'Deportationen.'))
    DRAW(pg, t, K('und Deportationen.', 1), 0.9, lambda ph: train_m(700, 850, 0.75, ph), (370, 690, 1000, 855))
    RULE(pg, t, K('Im folgenden Frühjahr') - 0.1, 930)
    KICK(pg, t, K('Im folgenden Frühjahr'), 'KATYN UND ANDERE ORTE, FRÜHJAHR 1940', 960)
    COUNT(pg, t, K('rund 22.000 polnische', 1), 1.0, 22000, (110, 1010), serif(130, 800), lambda v: 'rund ' + de(v))
    SAY(pg, t, 'Im folgenden Frühjahr erschoss der sowjetische Geheimdienst NKWD in Katyn und an anderen Orten rund 22.000 polnische Offiziere, Polizisten und Angehörige der Intelligenz.', (110, 1200), 42, accent=('NKWD', 'Katyn'))
    return pg

# ================= SP13: the end / Enigma =================
def s13L(t):
    pg = base2(27, True); t0 = TS(13)
    KICK(pg, t, t0, 'DIE BILANZ')
    SAY(pg, t, 'Für Polen begann eine Besatzung, die fast sechs Jahre dauern sollte.', (110, 250), 58, accent=('sechs', 'Jahre'))
    COUNT(pg, t, K('Rund sechs Millionen polnische', 1), 1.0, 6, (110, 450), serif(160, 800), lambda v: '%d Millionen' % round(v))
    SAY(pg, t, 'Rund sechs Millionen polnische Staatsbürger überlebten den Krieg nicht, etwa die Hälfte von ihnen waren Juden.', (110, 660), 46)
    PHOTO(pg, t, K('Rund sechs Millionen polnische'), 'eu_polnische_fluechtlinge_a', (110, 870, 1180, 620), 'Polnische Flüchtlinge, 1939')
    return pg
def s13R(t):
    pg = base2(28, False); t0 = K('Doch etwas hatte Polen')
    KICK(pg, t, t0, 'JULI 1939'); L(pg, t, t0 + 0.2, 'Enigma', (110, 250), serif(170, 800))
    DRAW(pg, t, t0 + 0.2, 1.0, lambda ph: enigma_m(1010, 380, 0.6, ph), (870, 280, 1150, 480))
    SAY(pg, t, 'Doch etwas hatte Polen schon vor dem Krieg weitergegeben.', (110, 560), 44)
    SAY(pg, t, 'Im Juli 1939 hatten polnische Mathematiker britischen und französischen Kryptologen gezeigt, wie sich die deutsche Verschlüsselungsmaschine Enigma entschlüsseln ließ.', (110, 690), 42, accent=('Mathematiker', 'Enigma'))
    for i, nm in enumerate(('Marian Rejewski', 'Jerzy Różycki', 'Henryk Zygalski')): L(pg, t, K('polnische Mathematiker britischen', 1) + 0.35 * i, nm, (110 + i * 400, 950), serif(40, 800), ACC)
    SAY(pg, t, 'Die Wehrmacht ahnte davon nichts.', (110, 1040), 46)
    RULE(pg, t, K('Im Westen herrschte') - 0.1, 1140)
    SAY(pg, t, 'Im Westen herrschte nun eine trügerische Ruhe.', (110, 1180), 56, accent=('trügerische', 'Ruhe.'))
    SAY(pg, t, 'Doch Hitler plante bereits den nächsten Angriff.', (110, 1320), 64, wg=800, accent=('nächsten', 'Angriff.'))
    return pg

# ================= SP14: end page =================
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
END0 = TURNS[13] + TD + 1.3
CLICKS = [END0 + 1.0 + i * 1.1 for i in range(3)]          # the moment each button is pressed (click sound)
def s14L(t):
    pg = base2(29, True); t0 = TURNS[13] + TD + 0.2
    KICK(pg, t, t0, 'FORTSETZUNG FOLGT'); L(pg, t, t0 + 0.2, 'TEIL 3', (100, 250), serif(230, 900)); L(pg, t, t0 + 0.5, 'Der Krieg im Westen', (110, 530), serif(80, 400), GREY)
    PHOTO(pg, t, t0 + 0.8, 'hoffmann_s77_0', (110, 680, 1180, 760))
    return pg
def s14R(t):
    pg = base2(30, False); t0 = END0 - 0.2
    L(pg, t, t0, 'Gefällt dir die Serie?', (110, 220), serif(96, 800)); d = ImageDraw.Draw(pg)
    for i, (nm, ic) in enumerate((('Liken', icon_thumb), ('Teilen', icon_share), ('Abonnieren', icon_bell))):
        y = 560 + i * 280; tc = CLICKS[i]; reg((110, y - 120, 1100, y + 130), tc - 0.6)
        if t < tc - 0.6: continue
        u = clamp((t - tc + 0.6) / 0.45); press = math.exp(-((t - tc) / 0.12) ** 2) if t > tc - 0.3 else 0
        on = t >= tc; col = ACC if on else TXT; sc = (1.0 - 0.18 * press)
        bx0, by0, bx1, by1 = 120, y - 110, 1020, y + 110
        d.rounded_rectangle((bx0, by0, bx1, by1), 110, outline=fade_col((200, 200, 200), u), width=5, fill=fade_col(((250, 232, 230) if on else (244, 243, 240)), u))
        if i == 2: ic(d, 240, y + 10, 0.9 * sc, fade_col(col, u), 18 * math.sin((t - tc) * 9) * math.exp(-max(0, t - tc) * 1.5) if on else 0)
        else: ic(d, 240, y + 10, 0.9 * sc, fade_col(col, u))
        d.text((380, y), nm, font=serif(84, 800), fill=fade_col(col, u), anchor='lm')
        if t > tc - 0.35:   # the cursor comes in and clicks
            v = eout(clamp((t - tc + 0.35) / 0.3)); px, py = lerp(1250, 900, v), lerp(y + 150, y + 30, v); r_ = 1 - 0.25 * press
            d.polygon([(px, py), (px + 40 * r_, py + 100 * r_), (px + 58 * r_, py + 62 * r_), (px + 100 * r_, py + 56 * r_)], fill=TXT)
    L(pg, t, CLICKS[2] + 0.6, 'damit du Teil 3 nicht verpasst.', (110, 1440), serif(56, 400), GREY)
    return pg

SPREADS = [(s0L, s0R), (s1L, s1R), (s2L, s2R), (s3L, s3R), (s4L, s4R), (s5L, s5R), (s6L, s6R), (s7L, s7R), (s8L, s8R), (s9L, s9R), (s10L, s10R),
           (s11L, s11R), (s12L, s12R), (s13L, s13R), (s14L, s14R)]
# films that fill the frame: (spread, side, box, from, to, caption 1, caption 2)
FILLS = [(0, 'L', B0, 0.0, K('Doch dieses Wort') - 0.9, 'Polen, September 1939', 'Deutsche Panzer beim Vormarsch'),
         (1, 'L', B1, TF(1), FE[1], '1. September 1939', 'Deutsche Soldaten öffnen den Schlagbaum an der polnischen Grenze'),
         (3, 'L', B3, TF(3), FE[3], 'Danzig, 1. September 1939, 4.45 Uhr', 'Die Schleswig-Holstein eröffnet das Feuer auf die Westerplatte'),
         (6, 'L', (110, 260, 1180, 600), TF(6), FE[6], 'September 1939', 'Deutsche Panzer- und motorisierte Divisionen stoßen schnell vor'),
         (6, 'R', (110, 250, 560, 470), K('Zehntausende Soldaten gingen') + 0.8, TURNS[6] - 0.1, 'Bzura, September 1939', 'Zehntausende polnische Soldaten gehen in Gefangenschaft'),
         (8, 'R', (110, 260, 1180, 600), K('Wenige Tage später übergab') - 0.2, K('General Heinz Guderian') - 0.4, 'Brest-Litowsk, September 1939', 'Die Wehrmacht übergibt die Stadt an die Rote Armee'),
         (8, 'R', (110, 1090, 640, 400), K('nahmen gemeinsam den') + 0.6, TURNS[8] - 0.1, 'Brest-Litowsk, 22. September 1939', 'Guderian und Kriwoschein nehmen den Vorbeimarsch ab'),
         (10, 'L', (110, 260, 1180, 620), TF(10), FE[10], 'Warschau, September 1939', 'Wasserwerke und Kraftwerke fallen aus, ganze Straßenzüge brennen'),
         (11, 'R', (110, 260, 1180, 560), K('Noch am Tag der') + 0.7, K('Die neue Grenze folgte') - 1.3, 'Moskau, 28. September 1939', 'Ribbentrop und Molotow unterzeichnen einen weiteren Vertrag')]
REC[0] = True
for i, (Lf, Rf) in enumerate(SPREADS):
    for side, fn in (('L', Lf), ('R', Rf)): CUR[0], CUR[1] = i, side; fn(1e5)
REC[0] = False
CAMS = [(0.0,) + fill_frame(B0)]
for i in range(len(SPREADS)):
    a = 0.0 if i == 0 else TURNS[i - 1] + TD; b = TURNS[i] if i < len(TURNS) else T_END
    fl = [((f[2][0] + (PW if f[1] == 'R' else 0), f[2][1], f[2][0] + f[2][2] + (PW if f[1] == 'R' else 0), f[2][1] + f[2][3]), f[3], f[4]) for f in FILLS if f[0] == i]
    its = [e for e in REG if e['sp'] == i and not (i == 0 and e['t0'] < 0.5)]
    keys, _ = plan(its, fl, (a, b))
    CAMS += keys
    if i < len(TURNS): CAMS.append((TURNS[i],) + OV + (0.65,))
CAMS[-1] = CAMS[-1] if CAMS[-1][0] < T_END else CAMS[-1]
CAMS.sort(key=lambda c: c[0])
MAG = Book(SPREADS, TURNS, CAMS, spine=100)
def frame(t):
    img = MAG(t)
    for f in FILLS:
        c0 = f[3] + (0.35 if f[3] < 0.5 else 0.25)
        if c0 <= t <= f[4] + 0.15: caption(img, t, c0, f[5], f[6], f[4] + 0.15)
    if t < 0.6: img = blend(Image.new('RGB', (W, H), (0, 0, 0)), img, t / 0.6)
    if t > T_END - 1.2: img = blend(img, Image.new('RGB', (W, H), (0, 0, 0)), (t - (T_END - 1.2)) / 1.2)
    return img

if __name__ == '__main__':
    if sys.argv[1] == 'check':
        FG = [(f[0], f[3] - 1.1, f[4] + 0.3, (f[2][0] + (PW if f[1] == 'R' else 0), f[2][1], f[2][0] + f[2][2] + (PW if f[1] == 'R' else 0), f[2][1] + f[2][3])) for f in FILLS]
        for f in FILLS: print('fill sp%d %.1f-%.1f  %.1fs' % (f[0], f[3], f[4], f[4] - f[3]))
        bad = check(MAG, T_END, fills=FG)
        for b in bad:
            e = b[1]; print(b[0], 'sp%d%s' % (e['sp'], e['side']), e['box'], '%.2f-%.2f' % (e['t0'], e['t1']), e['kind'], ('<-> %s' % (b[2]['box'],)) if len(b) > 2 else '')
        print(len(bad), 'problems'); sys.exit()
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[2:]]; n = len(ts); Pc = Image.new('RGB', (3 * 640, ((n + 2) // 3) * 360))
        for i, t in enumerate(ts):
            im = frame(t); ImageDraw.Draw(im).text((20, 20), '%.1f' % t, font=sans(40, 800), fill=(255, 0, 255)); Pc.paste(im.resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
        Pc.save(LB + 'chk/prev.jpg', quality=86); sys.exit()
    if sys.argv[1] == 'pages':
        for i, (Lf, Rf) in enumerate(SPREADS):
            spread_img(Lf(1e5), Rf(1e5)).convert('RGB').resize((SW // 3, PH // 3)).save(LB + 'chk/sp_%02d.jpg' % i, quality=85)
        sys.exit()
    if sys.argv[1] == 'T': print(round(T_END, 3)); sys.exit()
    if sys.argv[1] == 'turns': print(' '.join('%.2f' % x for x in TURNS)); print('clicks', ' '.join('%.2f' % x for x in CLICKS)); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
        if n % 300 == 0: print('t', n / FPS, flush=True)
    p.stdin.close(); p.wait(); print('rc', p.returncode)
