# "Deutschland im Zweiten Weltkrieg", Teil 4: Die Luftschlacht um England (16:9). The Teil 2 v3 magazine engine (t2core): every element
# tied to its spoken word, the camera planned from the page elements, films filling the frame with their caption, slowly moving
# colourised photos, red pen circles, counters, maps drawn on, small running pen drawings. No fade from or to black.
from t2core import *
from t2core import _shadow
from lmap import Map
from drawings import tank_m, monoplane_m, wave_flag, paint_uk, paint_fr
from drawings2 import soldier_m, civilian_m, truck_m, gold_m, radio_m, train_m, enigma_m

# ---------- turns: about 1.4 s before the first word of each new spread (about 1.9 s of silence was put into the voice there) ----------
STARTS = ['Nach dem Sieg über', 'Bereits am 16. Juli', 'Die Kriegsmarine hatte vor', 'Auf der anderen Seite', 'Alle Meldungen liefen', 'Die Kämpfe begannen im', 'Am 13. August folgte', 'Die Bf 109 war', 'Ende August griff die', 'Am 20. August sagte', 'Am 7. September flogen', 'Am 15. September griff', 'Die Luftwaffe griff nun', 'Die Schlacht um England']
TD = Book.TD
TURNS = [K(s) - 1.4 for s in STARTS] + [VEND + 0.6]
def TF(i): return TURNS[i - 1] + TD + 1.05          # a film that opens spread i fills the frame from here
def TS(i): return TURNS[i - 1] + TD + 0.25          # the moment spread i lies open
T_END = VEND + 9.0
def base2(n, left): return base(n, left).copy()
GR = (120, 120, 124)

# ---------- shared drawing helpers ----------
def arrow(pg, m, t, t0, pts, dur=1.0, wd=16, col=ACC):
    if t < t0: return
    u = eio((t - t0) / dur); Q = [m.mp(*p) for p in pts]; segs = list(zip(Q, Q[1:])); Ln = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs)
    todo = u * Ln; d = ImageDraw.Draw(pg); E = Q[0]; ang = 0
    for a, b in segs:
        l = math.hypot(b[0] - a[0], b[1] - a[1]); v = min(1, todo / l); E = (lerp(a[0], b[0], v), lerp(a[1], b[1], v)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
        d.line((a, E), fill=col, width=wd); todo -= l
        if todo <= 0: break
    hd = 46; d.polygon([(E[0] + 18 * math.cos(ang), E[1] + 18 * math.sin(ang)), (E[0] - hd * math.cos(ang - 0.6), E[1] - hd * math.sin(ang - 0.6)), (E[0] - hd * math.cos(ang + 0.6), E[1] - hd * math.sin(ang + 0.6))], fill=col)
def polymask(m, pts):
    im = Image.new('L', m.size, 0); ImageDraw.Draw(im).polygon([m.mp(*p) for p in pts], fill=255); return ImageChops.multiply(im, m.clip())
def hatch_mask(pg, m, msk, k, col=ACC, a=0.7, step=15):
    """red hatching of an arbitrary mask, swept in from the left"""
    if k <= 0: return
    bb = msk.getbbox()
    if not bb: return
    x0, y0, x1, y1 = bb; xe = int(lerp(x0, x1, eout(k)))
    if xe <= x0: return
    P = m.pattern(step, 45)[y0:y1, x0:xe]; M_ = np.asarray(msk)[y0:y1, x0:xe] > 0
    A = (M_ & P).astype(np.float32) * 255 * a; stamp_ink(pg, Image.fromarray(A.astype(np.uint8)), (x0, y0), col)
def west_map(pg, t, t0, m, tint=(), labels=True):
    k = eout((t - t0) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=('reich',), outline=('reich',))
    for n in tint: m.tint(pg, n, k, ACC, 0.06)
def dot(pg, m, t, t0, ll, name, dx=0, dy=-34, size=28, col=TXT):
    m.pin(pg, t, t0, ll, col, 9); m.label(pg, t, t0 + 0.1, name, (ll[0], ll[1]), sans(size, 700), col, sw=5, dy=dy, dx=dx)
def ship_icon(d, x, y, s, col):
    d.polygon([(x - 60 * s, y), (x + 60 * s, y), (x + 46 * s, y + 18 * s), (x - 52 * s, y + 18 * s)], fill=col)
    d.rectangle((x - 18 * s, y - 16 * s, x + 14 * s, y), fill=col); d.rectangle((x - 4 * s, y - 34 * s, x + 2 * s, y - 16 * s), fill=col)
def SHIPS(pg, t, t0, n, x, y, gap, t_cross=None):
    reg((x - 60, y - 40, x + gap * (n - 1) + 60, y + 24), t0)
    d = ImageDraw.Draw(pg)
    for i in range(n):
        ti = t0 + 0.08 * i
        if t < ti: continue
        k = eout((t - ti) / 0.3); cx = x + gap * i; ship_icon(d, cx, y, 0.62, fade_col(TXT, k))
        if t_cross is not None and t >= t_cross + 0.06 * i:
            u = eout((t - t_cross - 0.06 * i) / 0.25); d.line((cx - 40, y - 34, lerp(cx - 40, cx + 40, u), lerp(y - 34, y + 22, u)), fill=ACC, width=7)
def PAPER_DOC(pg, t, t0, box, title, lines, t_burn=None):
    """a typed secret order; from t_burn its corner chars and burns away"""
    x0, y0, w, h = box; reg((x0, y0, x0 + w, y0 + h), t0, kind='pic')
    if t < t0: return
    k = eout((t - t0) / 0.5); d = ImageDraw.Draw(pg)
    _shadow(pg, x0, y0, w, h, k); d.rectangle((x0, y0, x0 + w, y0 + h), fill=fade_col((244, 238, 222), k), outline=fade_col((180, 170, 150), k), width=2)
    d.text((x0 + 40, y0 + 40), title, font=sans(40, 800), fill=fade_col(ACC, k))
    for i, l in enumerate(lines): d.text((x0 + 40, y0 + 120 + i * 52), l, font=italic(32), fill=fade_col(TXT, k))
    if t_burn is not None and t > t_burn:
        u = clamp((t - t_burn) / 2.2); r = u * w * 0.42; cx, cy = x0 + w, y0 + h
        pts = [(cx + r * 1.15 * math.cos(a) * (1 + 0.1 * math.sin(a * 13)), cy + r * math.sin(a) * (1 + 0.12 * math.cos(a * 11))) for a in np.linspace(math.pi, 1.5 * math.pi, 40)]
        burnt = [(cx, cy)] + pts; d.polygon(burnt, fill=(28, 22, 18))
        edge = [(cx + (r + 10) * 1.15 * math.cos(a) * (1 + 0.1 * math.sin(a * 13)), cy + (r + 10) * math.sin(a) * (1 + 0.12 * math.cos(a * 11))) for a in np.linspace(math.pi, 1.5 * math.pi, 40)]
        d.line(edge, fill=(200, 120, 40), width=6)
def KICK(pg, t, t0, s, y=165): L(pg, t, t0, s, (110, y), sans(34, 800), ACC)
def QUOTE(pg, t, t0, s, xy, size=72):
    L(pg, t, t0, '„' + s + '“', xy, italic(size), TXT)

def FLOWBOX(pg, t, t0, s, box, col=TXT):
    """a ruled box with a label, drawn on (the reporting chain of the Dowding system)"""
    x0, y0, x1, y1 = box; reg(box, t0)
    if t < t0: return
    k = eout((t - t0) / 0.4); d = ImageDraw.Draw(pg)
    d.rectangle(box, outline=fade_col(col, k), width=4, fill=fade_col((240, 238, 232), k))
    d.text(((x0 + x1) / 2, (y0 + y1) / 2), s, font=sans(34, 800), fill=fade_col(col, k), anchor='mm')
def ARROW_V(pg, t, t0, x, y0, y1, col=ACC):
    if t < t0: return
    u = eout((t - t0) / 0.4); ye = lerp(y0, y1, u); d = ImageDraw.Draw(pg)
    d.line((x, y0, x, ye), fill=col, width=8)
    if u > 0.6: d.polygon([(x - 18, ye - 22), (x + 18, ye - 22), (x, ye + 4)], fill=col)
RADAR = [(1.3, 51.13), (0.75, 50.95), (0.33, 50.8), (-0.5, 50.83), (-1.2, 50.6), (1.0, 51.28), (0.75, 51.6), (1.4, 52.0)]

# ================= SP0: hook =================
B0 = (110, 600, 1180, 664)
@functools.lru_cache(None)
def masthead():
    pg = base(1, True).copy(); d = ImageDraw.Draw(pg)
    for i, c in enumerate(((24, 24, 26), (196, 30, 34), (236, 186, 32))): d.rectangle((110, 196 + i * 92, 128, 196 + (i + 1) * 92), fill=c)
    d.text((160, 186), 'Deutschland im', font=serif(118, 900), fill=TXT); d.text((160, 326), 'Zweiten Weltkrieg', font=serif(118, 400), fill=TXT)
    for i, c in enumerate(((24, 24, 26), (196, 30, 34), (236, 186, 32))): d.rectangle((110, 490 + i * 9, PW - 110, 490 + (i + 1) * 9), fill=c)
    d.text((110, 545), 'TEIL 4 · DIE LUFTSCHLACHT UM ENGLAND', font=sans(36, 800), fill=ACC, anchor='lm')
    d.text((PW - 110, 545), 'JULI BIS OKTOBER 1940', font=sans(28, 600), fill=GREY, anchor='rm')
    return pg
def s0L(t):
    pg = masthead().copy(); FILM(pg, t, -1, 'bombers2', B0, 'Aus einem deutschen Bomber, 1940', 0.8)
    L(pg, t, -1, 'Im Sommer 1940 hatte die Luftwaffe', (110, 1400), serif(56, 400)); L(pg, t, -1, 'mehr als dreimal so viele Flugzeuge.', (110, 1478), serif(56, 800))
    return pg
def s0R(t):
    pg = base2(2, False); t0 = K('mehr als dreimal')
    KICK(pg, t, t0 - 0.2, 'EINSATZBEREIT IM AUGUST 1940')
    COUNT(pg, t, t0 - 0.1, 0.9, 2500, (110, 250), serif(110, 800), lambda v: de(v), ACC); L(pg, t, t0, 'Flugzeuge der Luftwaffe', (520, 290), serif(52, 400))
    COUNT(pg, t, K('wie das britische Jagdkommando.', 2), 0.9, 600, (110, 400), serif(110, 800), lambda v: '%d' % round(v), TXT); L(pg, t, K('wie das britische Jagdkommando.', 2), 'britische Jäger', (520, 440), serif(52, 400))
    PHOTO(pg, t, K('Sie sollte den Himmel'), 'he111_form', (110, 600, 560, 420), 'Bomber He 111 im Verband, 1940', fy=0.3)
    SAY(pg, t, 'Sie sollte den Himmel über England freikämpfen, damit die Wehrmacht über den Ärmelkanal setzen konnte.', (730, 610), 40, maxw=560, accent=('England',))
    RULE(pg, t, K('Doch nach vier Monaten') - 0.1, 1140)
    SAY(pg, t, 'Doch nach vier Monaten war die Invasion abgesagt,', (110, 1170), 50, accent=('abgesagt,',))
    SAY(pg, t, 'und Deutschland hatte zum ersten Mal in diesem Krieg sein Ziel nicht erreicht.', (110, 1320), 50, wg=800, accent=('nicht', 'erreicht.'))
    return pg

# ================= SP1: peace offer, Reichsmarschall, London refuses =================
def s1L(t):
    pg = base2(3, True); t0 = TS(1)
    KICK(pg, t, t0, '19. JULI 1940'); L(pg, t, t0 + 0.1, 'Ein Angebot an London', (110, 204), serif(76, 800))
    PHOTO(pg, t, t0 + 0.3, 'reichstag', (110, 340, 560, 760), 'Reichstagssitzung am 19. Juli 1940', fy=0.45, zoom=0.05)
    SAY(pg, t, 'Nach dem Sieg über Frankreich rechnete Hitler damit, dass Großbritannien einlenken würde.', (720, 340), 42, maxw=570, accent=('einlenken',))
    SAY(pg, t, 'Am 19. Juli 1940 bot er im Reichstag einen Frieden an', (720, 720), 40, maxw=570, accent=('Frieden',))
    QUOTE(pg, t, K('Appell an die Vernunft.', 1), 'Appell an die Vernunft', (110, 1260), 64)
    return pg
def s1R(t):
    pg = base2(4, False); t0 = K('An diesem Tag ernannte')
    PHOTO(pg, t, t0, 'goering_kess', (110, 200, 1180, 540), 'Hermann Göring bei einer Luftwaffeneinheit, 1940', fy=0.25)
    COUNT(pg, t, K('zwölf Generäle zu', 0), 0.8, 12, (110, 850), serif(110, 800), lambda v: '%d' % round(v), TXT); L(pg, t, K('zu Generalfeldmarschällen,', 1), 'Generalfeldmarschälle', (300, 890), serif(52, 400))
    L(pg, t, K('wurde sogar Reichsmarschall.', 2), 'Göring: Reichsmarschall', (110, 1000), serif(56, 800), ACC)
    RULE(pg, t, K('Drei Tage später lehnte') - 0.1, 1110)
    SAY(pg, t, 'Drei Tage später lehnte London ab.', (110, 1140), 60, wg=800, accent=('ab.',))
    PHOTO(pg, t, K('Premierminister Winston Churchill hatte'), 'churchill', (110, 1270, 360, 280), 'Winston Churchill', fy=0.3)
    SAY(pg, t, 'Großbritannien werde weiterkämpfen, notfalls allein.', (530, 1290), 44, maxw=760, accent=('allein.',))
    return pg

# ================= SP2: Seelöwe =================
def s2L(t):
    pg = base2(5, True); t0 = TS(2)
    KICK(pg, t, t0, 'WEISUNG NR. 16, 16. JULI 1940'); L(pg, t, t0 + 0.1, 'Unternehmen Seelöwe', (110, 204), serif(84, 800))
    PHOTO(pg, t, K('Sie befahl, eine Landung'), 'seel_tank', (110, 360, 1180, 600), 'Ein Panzer wird an der Kanalküste verladen, 1940', fy=0.5)
    SAY(pg, t, 'Die Wehrmacht hatte jedoch keine Landungsflotte.', (110, 1110), 56, wg=800, accent=('keine', 'Landungsflotte.'))
    return pg
def s2R(t):
    pg = base2(6, False); t0 = K('Die Marine ließ deshalb')
    PHOTO(pg, t, t0, 'barges', (110, 200, 1180, 520), 'Flusskähne für das Unternehmen Seelöwe, Wilhelmshaven 1940', fy=0.5)
    COUNT(pg, t, K('mehr als 2.000 Flusskähne', 2), 0.9, 2000, (110, 830), serif(110, 800), lambda v: 'über ' + de(v), ACC); L(pg, t, K('mehr als 2.000 Flusskähne', 3), 'Flusskähne', (720, 870), serif(56, 400))
    SAY(pg, t, 'aus Deutschland, Belgien und den Niederlanden an die Kanalküste bringen.', (110, 990), 40, accent=('Kanalküste',))
    PHOTO(pg, t, K('Viele hatten keinen eigenen'), 'seel_boats', (110, 1150, 560, 360), 'Landungsübung mit Schleppern', fy=0.5)
    SAY(pg, t, 'Viele hatten keinen eigenen Motor und mussten von Schleppern gezogen werden.', (720, 1150), 40, maxw=570, accent=('Motor',))
    return pg

# ================= SP3: why the air war, the Luftflotten =================
MC = Map('mc', (PW, PH), (110, 300, 1180, 720), -6.5, 9.5, 47.0)
def s3L(t):
    pg = base2(7, True); t0 = TS(3)
    KICK(pg, t, t0, 'DER PLAN')
    SAY(pg, t, 'Die Kriegsmarine hatte vor Norwegen viele Schiffe verloren und war der britischen Flotte weit unterlegen.', (110, 260), 42, accent=('unterlegen.',))
    SAY(pg, t, 'Eine Landung war nur möglich, wenn die Royal Air Force sie nicht mehr angreifen konnte.', (110, 470), 42, accent=('Royal', 'Air', 'Force'))
    SAY(pg, t, 'Deshalb sollte zuerst die Luftwaffe die britischen Jäger vernichten.', (110, 680), 54, wg=800, accent=('Jäger',))
    PHOTO(pg, t, K('Göring versprach, das werde'), 'goering_galland', (110, 920, 640, 470), 'Bruno Loerzer, Hermann Göring und Adolf Galland, 1940', fy=0.3)
    SAY(pg, t, 'Göring versprach, das werde nur wenige Wochen dauern.', (810, 930), 42, maxw=480, accent=('wenige', 'Wochen'))
    return pg
AIR = [('he111_form', 'He 111', 'Heinkel He 111,', 1), ('do17_form', 'Do 17', 'Dornier Do 17', 1), ('ju88_crew', 'Ju 88', 'Junkers Ju 88,', 1),
       ('ju87', 'Ju 87', 'Sturzkampfbomber Ju 87,', 1), ('bf109_beach', 'Bf 109', 'Messerschmitt Bf 109', 1)]
def s3R(t):
    pg = base2(8, False); m = MC; t1 = K('Dafür standen drei Luftflotten')
    KICK(pg, t, t1, 'DREI LUFTFLOTTEN', 250)
    reg((100, 290, 1300, 1030), t1, kind='pic')
    if t >= t1:
        k = eout((t - t1) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=(), outline=('UK', 'France'))
        m.tint(pg, 'UK', k, (60, 110, 180), 0.08)
        m.label(pg, t, t1 + 0.3, 'GROSSBRITANNIEN', (-2.2, 52.7), sans(30, 800), TXT); m.label(pg, t, t1 + 0.3, 'FRANKREICH', (1.6, 47.8), sans(30, 800), GREY, sw=4)
        t2 = K('Die Luftflotte 2 unter'); m.pin(pg, t, t2, (4.35, 50.85)); m.label(pg, t, t2, 'LUFTFLOTTE 2', (5.3, 51.45), sans(28, 800), ACC, sw=5)
        m.label(pg, t, K('Albert Kesselring lag in', 1), 'Kesselring', (5.3, 50.3), italic(28), TXT, sw=5)
        t3 = K('die Luftflotte 3 unter'); m.pin(pg, t, t3, (2.35, 48.86)); m.label(pg, t, t3, 'LUFTFLOTTE 3', (3.9, 49.3), sans(28, 800), ACC, sw=5)
        m.label(pg, t, K('Hugo Sperrle weiter westlich', 1), 'Sperrle', (3.9, 48.75), italic(28), TXT, sw=5)
        t5 = K('die Luftflotte 5 in'); m.label(pg, t, t5, 'LUFTFLOTTE 5', (5.6, 53.75), sans(28, 800), ACC, sw=5)
        m.label(pg, t, t5 + 0.2, 'aus Norwegen und Dänemark', (5.6, 53.3), italic(26), TXT, sw=5)
        arrow(pg, m, t, t5 + 0.3, [(8.8, 53.95), (4.0, 54.15), (0.2, 54.2)], dur=1.0, wd=10)
    COUNT(pg, t, K('rund 2.500 einsatzbereite Flugzeuge:', 1), 0.9, 2500, (110, 1060), serif(84, 800), lambda v: 'rund ' + de(v), ACC)
    L(pg, t, K('rund 2.500 einsatzbereite Flugzeuge:', 2), 'einsatzbereite Flugzeuge', (640, 1090), serif(44, 400))
    for i, (img, nm, ph_, wi) in enumerate(AIR):
        x = 110 + i * 240; ti = K(ph_, wi)
        PHOTO(pg, t, ti, img, (x, 1200, 220, 170), None, fy=0.4, zoom=0.04)
        L(pg, t, ti, nm, (x, 1385), sans(30, 800), TXT)
    return pg

# ================= SP4: Fighter Command, radar, observers =================
MR = Map('mr', (PW, PH), (720, 420, 570, 430), -3.2, 3.2, 49.4)
def s4L(t):
    pg = base2(9, True); t0 = TS(4)
    KICK(pg, t, t0, 'FIGHTER COMMAND')
    PHOTO(pg, t, K('unter Luftmarschall Hugh Dowding'), 'dowding', (110, 260, 470, 620), 'Hugh Dowding', fy=0.25, zoom=0.05)
    L(pg, t, K('Luftmarschall Hugh Dowding', 1), 'Hugh', (650, 280), serif(80, 400)); L(pg, t, K('Luftmarschall Hugh Dowding', 2), 'Dowding', (650, 380), serif(96, 800))
    COUNT(pg, t, K('mit gut 600 einsatzbereiten', 2), 0.8, 600, (650, 540), serif(100, 800), lambda v: 'gut %d' % round(v), ACC)
    L(pg, t, K('einsatzbereiten Jägern,', 1), 'einsatzbereite Jäger', (650, 680), serif(44, 400))
    SAY(pg, t, 'vor allem Hurricanes und Spitfires.', (650, 770), 40, maxw=640, accent=('Hurricanes', 'Spitfires.'))
    PHOTO(pg, t, K('vor allem Hurricanes und', 2), 'spitfire_refuel', (110, 990, 1180, 520), 'Eine Spitfire wird betankt, Fowlmere, September 1940', fy=0.5)
    return pg
def s4R(t):
    pg = base2(10, False); m = MR
    SAY(pg, t, 'Dowding hatte schon vor dem Krieg ein System aufgebaut, das es so nirgendwo sonst gab.', (110, 200), 44, accent=('System',))
    t1 = K('An der Küste standen')
    PHOTO(pg, t, t1, 'radar', (110, 420, 560, 430), 'Radarmasten der Kette Chain Home', fy=0.5)
    reg((710, 410, 1300, 860), t1, kind='pic')
    if t >= t1:
        k = eout((t - t1) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=(), outline=('UK', 'France', 'Belgium'))
        tr = K('Radarstationen der Kette Chain', 0)
        for i, ll in enumerate(RADAR): m.pin(pg, t, tr + 0.12 * i, ll, ACC, 9)
        m.label(pg, t, tr + 0.4, 'Chain Home', (-1.6, 51.75), sans(28, 800), ACC, sw=5)
        m.label(pg, t, t1 + 0.3, 'FRANKREICH', (2.0, 49.85), sans(24, 800), GREY, sw=4)
        if t >= K('schon über Frankreich erkennen', 2):
            u = eout((t - K('schon über Frankreich erkennen', 2)) / 1.2); d = ImageDraw.Draw(pg)
            for ll in RADAR[:5]:
                x, y = m.mp(*ll); r = 40 + 160 * u
                d.arc((x - r, y - r, x + r, y + r), 20, 160, fill=fade_col(ACC, 1 - 0.6 * u), width=3)
    SAY(pg, t, 'Im Landesinneren meldeten Tausende Beobachter des Royal Observer Corps jedes Flugzeug, das sie sahen oder hörten.', (110, 980), 40, maxw=600, accent=('Royal', 'Observer', 'Corps'))
    PHOTO(pg, t, K('Im Landesinneren meldeten Tausende'), 'k4_beobachter_stpauls', (760, 980, 530, 380), 'Luftraumbeobachter über London', fy=0.4)
    return pg

# ================= SP5: Bentley Priory =================
def s5L(t):
    pg = base2(11, True); t0 = TS(5)
    KICK(pg, t, t0, 'BENTLEY PRIORY'); L(pg, t, t0 + 0.1, 'Das Lagebild', (110, 204), serif(84, 800))
    SAY(pg, t, 'Alle Meldungen liefen in Bentley Priory bei London zusammen.', (110, 340), 44, accent=('Bentley', 'Priory'))
    PHOTO(pg, t, K('Auf großen Kartentischen schoben'), 'opsroom', (110, 500, 1180, 840), 'Kartentisch in einer Leitstelle des Fighter Command', fy=0.55, zoom=0.05)
    return pg
def s5R(t):
    pg = base2(12, False); t0 = K('Dort wurden sie geprüft')
    SAY(pg, t, 'Dort wurden sie geprüft und an die Leitstellen weitergegeben.', (110, 200), 44)
    FLOWBOX(pg, t, K('Alle Meldungen liefen in') + 0.3, 'RADAR', (110, 380, 650, 470)); FLOWBOX(pg, t, K('Alle Meldungen liefen in') + 0.5, 'BEOBACHTER', (750, 380, 1290, 470))
    ARROW_V(pg, t, t0 - 0.2, 380, 480, 560); ARROW_V(pg, t, t0 - 0.2, 1020, 480, 560)
    FLOWBOX(pg, t, t0, 'BENTLEY PRIORY', (110, 570, 1290, 660), ACC)
    ARROW_V(pg, t, K('an die Leitstellen weitergegeben.', 1), 700, 670, 750)
    FLOWBOX(pg, t, K('an die Leitstellen weitergegeben.', 1), 'LEITSTELLEN', (110, 760, 1290, 850))
    ARROW_V(pg, t, K('ihre Staffeln genau dorthin', 1), 700, 860, 940)
    FLOWBOX(pg, t, K('ihre Staffeln genau dorthin', 1), 'STAFFELN', (110, 950, 1290, 1040), ACC)
    SAY(pg, t, 'So konnten sie ihre Staffeln genau dorthin schicken.', (110, 1110), 44)
    SAY(pg, t, 'Die britischen Jäger mussten nicht auf Patrouille warten, sie starteten erst, wenn der Angriff kam.', (110, 1260), 50, wg=800, accent=('erst,',))
    return pg

# ================= SP6: Kanalkampf, radar attacks =================
B6 = (110, 312, 1180, 630)
MV = Map('mv', (PW, PH), (110, 610, 1180, 600), -3.8, 2.4, 49.9)
def s6L(t):
    pg = base2(13, True); t0 = TS(6)
    t2 = K('um die Jäger der') + 0.2; KICK(pg, t, t2, 'JULI 1940'); L(pg, t, t2 + 0.1, 'Über dem Ärmelkanal', (110, 204), serif(76, 800))
    FILM(pg, t, TF(6) - 1.0, 'stuka_att', B6, 'Sturzkampfbomber Ju 87 über dem Kanal, 1940')
    SAY(pg, t, 'um die Jäger der RAF herauszulocken.', (110, 1060), 46, accent=('RAF',))
    L(pg, t, K('diese Wochen den Kanalkampf.', 3), 'Kanalkampf', (110, 1250), serif(84, 800), ACC)
    SAY(pg, t, 'Beide Seiten verloren Flugzeuge, doch eine Entscheidung brachte das nicht.', (110, 1400), 42)
    return pg
def s6R(t):
    pg = base2(14, False); t0 = K('Am 1. August befahl')
    KICK(pg, t, t0, 'WEISUNG NR. 17, 1. AUGUST 1940')
    SAY(pg, t, 'die britische Luftwaffe so schnell wie möglich niederzukämpfen.', (110, 260), 46, accent=('niederzukämpfen.',))
    t1 = K('Am 12. August griffen'); m = MV
    KICK(pg, t, t1, '12. AUGUST 1940', 520)
    reg((100, 600, 1300, 1220), t1, kind='pic')
    if t >= t1:
        k = eout((t - t1) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=(), outline=('UK', 'France'))
        for i, ll in enumerate(RADAR[:6]): m.pin(pg, t, t1 + 0.3 + 0.1 * i, ll, TXT, 9)
        m.label(pg, t, t1 + 0.4, 'ENGLAND', (-1.6, 51.6), sans(30, 800), GREY, sw=4)
        tv = K('Die Station Ventnor auf', 2); m.pin(pg, t, tv, (-1.2, 50.6), ACC, 14)
        m.label(pg, t, tv, 'Ventnor', (-1.2, 50.35), sans(32, 800), ACC, sw=5)
        if t >= K('fiel für Tage aus,', 0): stamp(pg, t, K('fiel für Tage aus,', 0), 'AUSGEFALLEN', m.mp(-2.6, 50.1), 40, -6)
    SAY(pg, t, 'Die deutsche Führung unterschätzte das Radar und stellte die Angriffe darauf bald ein.', (110, 1300), 46, accent=('unterschätzte',))
    return pg

# ================= SP7: Adlertag, Black Thursday, 18 August =================
def s7L(t):
    pg = base2(15, True); t0 = TS(7)
    KICK(pg, t, t0, '13. AUGUST 1940'); L(pg, t, t0 + 0.1, 'Der Adlertag', (110, 204), serif(84, 800))
    PHOTO(pg, t, t0 + 0.3, 'he111_kg1', (110, 360, 1180, 520), 'Bomber He 111 im Anflug, 1940', fy=0.5)
    SAY(pg, t, 'Am 15. August flog die Luftwaffe so viele Einsätze wie an keinem anderen Tag der Schlacht.', (110, 960), 42, accent=('15.', 'August'))
    SAY(pg, t, 'Doch das Radar hatte sie früh erfasst,', (110, 1130), 42, accent=('Radar',))
    L(pg, t, K('der Schwarze Donnerstag.', 1), 'Schwarzer Donnerstag', (110, 1300), serif(84, 800), ACC)
    return pg
def s7R(t):
    pg = base2(16, False); t0 = K('Am 18. August erlitten')
    KICK(pg, t, t0, '18. AUGUST 1940')
    PHOTO(pg, t, t0, 'do17_low', (110, 250, 1180, 520), 'Do 17 im Tiefflug über Südengland, 18. August 1940', fy=0.5)
    SAY(pg, t, 'Am 18. August erlitten die Stukas so schwere Verluste, dass sie aus der Schlacht genommen wurden.', (110, 880), 42, accent=('Stukas',))
    PHOTO(pg, t, K('Gegen moderne Jäger waren'), 'ju87', (110, 1100, 560, 360), 'Sturzkampfbomber Ju 87', fy=0.5)
    SAY(pg, t, 'Auch die zweimotorige Bf 110 war den Hurricanes und Spitfires im Kurvenkampf unterlegen.', (720, 1100), 36, maxw=570, accent=('Bf', '110'))
    SAY(pg, t, 'Bald mussten selbst die Zerstörer von Bf 109 begleitet werden.', (720, 1340), 36, maxw=570)
    return pg

# ================= SP8: the Bf 109, Galland =================
def s8L(t):
    pg = base2(17, True); t0 = TS(8)
    KICK(pg, t, t0, 'DIE MESSERSCHMITT BF 109')
    PHOTO(pg, t, t0 + 0.3, 'bf109_beach', (110, 280, 1180, 640), 'Notgelandete Bf 109 an der Kanalküste, 1940', fy=0.55)
    SAY(pg, t, 'Die Bf 109 war den britischen Jägern ebenbürtig, doch sie hatte ein anderes Problem.', (110, 1030), 44, accent=('Problem.',))
    COUNT(pg, t, K('etwa zehn Minuten Luftkampf.', 1), 0.8, 10, (110, 1230), serif(130, 800), lambda v: '%d Min.' % round(v), ACC)
    L(pg, t, K('etwa zehn Minuten Luftkampf.', 2), 'Luftkampf über London', (600, 1290), serif(48, 400))
    return pg
def s8R(t):
    pg = base2(18, False)
    SAY(pg, t, 'Göring verlangte, dass die Jäger dicht bei den Bombern blieben.', (110, 200), 46, accent=('dicht',))
    SAY(pg, t, 'Die Piloten verloren so ihren größten Vorteil, die Höhe und den Überraschungsangriff.', (110, 380), 42)
    PHOTO(pg, t, K('Als Göring den Jagdflieger'), 'galland', (110, 600, 470, 740), 'Adolf Galland', fy=0.25, zoom=0.05)
    SAY(pg, t, 'Als Göring den Jagdflieger Adolf Galland fragte, was er brauche, soll dieser geantwortet haben:', (640, 610), 40, maxw=650, accent=('Adolf', 'Galland'))
    QUOTE(pg, t, K('eine Staffel Spitfires.', 1), 'Eine Staffel Spitfires.', (640, 900), 54)
    PHOTO(pg, t, K('eine Staffel Spitfires.', 2), 'spitfire_new', (640, 1020, 650, 330), 'Supermarine Spitfire, 1940', fy=0.5)
    return pg

# ================= SP9: airfields, pilots, 303 =================
ME = Map('me', (PW, PH), (110, 330, 1180, 600), -1.6, 2.2, 50.65)
AIRFIELDS = [('Biggin Hill', (0.03, 51.33), 'etwa Biggin Hill,', 1, 0, -40), ('Kenley', (-0.09, 51.30), 'Kenley und Manston.', 0, -90, 34), ('Manston', (1.35, 51.34), 'Kenley und Manston.', 2, 0, -40)]
def s9L(t):
    pg = base2(19, True); t0 = TS(9); m = ME
    KICK(pg, t, t0, 'ENDE AUGUST 1940'); L(pg, t, t0 + 0.1, 'Angriff auf die Flugplätze', (110, 204), serif(72, 800))
    reg((100, 320, 1300, 940), t0 + 0.3, kind='pic')
    if t >= t0 + 0.3:
        k = eout((t - t0 - 0.3) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=(), outline=('UK', 'France'))
        m.pin(pg, t, t0 + 0.5, (-0.12, 51.5), TXT, 12); m.label(pg, t, t0 + 0.5, 'London', (-0.12, 51.5), sans(32, 800), TXT, sw=5, dy=-36)
        m.label(pg, t, t0 + 0.5, 'Ärmelkanal', (0.2, 50.85), italic(30), GREY, sw=4)
        for nm, ll, ph_, wi, dx, dy in AIRFIELDS:
            ti = K(ph_, wi); m.pin(pg, t, ti, ll, ACC, 13); m.label(pg, t, ti, nm, ll, sans(30, 800), ACC, sw=5, dx=dx, dy=dy)
    PHOTO(pg, t, K('Für das Fighter Command wurde'), 'rochester', (110, 1000, 560, 380), 'Luftangriff auf den Flugplatz Rochester', fy=0.5)
    SAY(pg, t, 'Für das Fighter Command wurde es gefährlich.', (720, 1010), 50, maxw=570, wg=800, accent=('gefährlich.',))
    return pg
def s9R(t):
    pg = base2(20, False)
    SAY(pg, t, 'Flugzeuge konnten die britischen Fabriken schnell ersetzen, sie bauten im Sommer 1940 mehr Jäger als die deutschen.', (110, 200), 42)
    SAY(pg, t, 'Erfahrene Piloten aber fehlten.', (110, 420), 62, wg=800, accent=('Piloten',))
    PHOTO(pg, t, K('Unter ihnen waren auch'), 'do17_spit', (110, 560, 1180, 520), 'Eine Spitfire neben einer Do 17', fy=0.5)
    SAY(pg, t, 'Unter ihnen waren auch Polen, Tschechen, Kanadier und Neuseeländer.', (110, 1180), 40, accent=('Polen,',))
    L(pg, t, K('Die polnische Staffel 303', 3), '303', (110, 1300), serif(140, 800), ACC)
    SAY(pg, t, 'meldete mehr Abschüsse als jede andere Staffel des Fighter Command.', (420, 1330), 40, maxw=870)
    return pg

# ================= SP10: The Few, London and Berlin =================
def s10L(t):
    pg = base2(21, True); t0 = TS(10)
    KICK(pg, t, t0, '20. AUGUST 1940'); L(pg, t, t0 + 0.1, 'Churchill im Unterhaus', (110, 204), serif(72, 800))
    PHOTO(pg, t, t0 + 0.3, 'he111_spit', (110, 340, 1180, 480), 'Luftkampf über England, 1940', fy=0.45)
    SAY(pg, t, 'Nie zuvor in der Geschichte menschlicher Konflikte haben so viele so wenigen so viel zu verdanken gehabt.', (110, 930), 54, accent=('wenigen',))
    L(pg, t, K('in Großbritannien „The Few“', 2), '„The Few“', (110, 1280), serif(90, 800), ACC)
    COUNT(pg, t, K('die rund 3.000 Männer,', 2), 0.8, 3000, (640, 1280), serif(90, 800), lambda v: 'rund ' + de(v), TXT)
    L(pg, t, K('genannt, die Wenigen.', 2), 'die Wenigen', (110, 1410), italic(52), GREY)
    L(pg, t, K('die rund 3.000 Männer,', 3), 'Männer im Fighter Command', (640, 1400), serif(40, 400))
    return pg
def s10R(t):
    pg = base2(22, False); t0 = K('In der Nacht zum 25.')
    KICK(pg, t, t0, '24. AUF 25. AUGUST 1940')
    SAY(pg, t, 'In der Nacht zum 25. August warfen deutsche Bomber, offenbar aus Versehen, Bomben auf London.', (110, 250), 42, accent=('Versehen,',))
    PHOTO(pg, t, K('Bomben auf London.', 0), 'tanklager', (110, 470, 560, 420), 'Brennendes Tanklager bei London, 1940', fy=0.5)
    SAY(pg, t, 'Churchill ließ in der folgenden Nacht Berlin bombardieren.', (720, 470), 42, maxw=570, accent=('Berlin',))
    SAY(pg, t, 'Die Schäden waren gering, doch Göring hatte versprochen, kein feindlicher Bomber werde das Reichsgebiet erreichen.', (720, 690), 32, maxw=570)
    RULE(pg, t, K('Am 4. September drohte') - 0.1, 1010)
    KICK(pg, t, K('Am 4. September drohte'), '4. SEPTEMBER 1940, SPORTPALAST', 1040)
    SAY(pg, t, 'Am 4. September drohte Hitler im Berliner Sportpalast, man werde die britischen Städte ausradieren.', (110, 1100), 44)
    L(pg, t, K('britischen Städte ausradieren.', 2), '„ausradieren“', (110, 1360), italic(84), ACC)
    return pg

# ================= SP11: 7 September =================
B11 = (110, 312, 1180, 630)
def s11L(t):
    pg = base2(23, True); t0 = TS(11)
    t2 = K('Göring sah ihnen von') - 0.3; KICK(pg, t, t2, '7. SEPTEMBER 1940'); L(pg, t, t2 + 0.1, 'Angriff auf London', (110, 204), serif(84, 800))
    FILM(pg, t, TF(11) - 1.0, 'london_air', B11, 'Deutsche Luftaufnahme von London und der Themse')
    t1 = K('Göring sah ihnen von')
    COUNT(pg, t, t1 - 0.6, 0.8, 350, (110, 1040), serif(110, 800), lambda v: 'rund %d' % round(v), ACC); L(pg, t, t1 - 0.5, 'Bomber', (110, 1170), serif(48, 400))
    COUNT(pg, t, t1 - 0.3, 0.8, 600, (720, 1040), serif(110, 800), lambda v: 'über %d' % round(v), TXT); L(pg, t, t1 - 0.2, 'Jäger als Begleitschutz', (720, 1170), serif(48, 400))
    SAY(pg, t, 'Göring sah ihnen von der französischen Küste aus nach.', (110, 1320), 46)
    return pg
def s11R(t):
    pg = base2(24, False); t0 = K('Die Bomben trafen vor')
    PHOTO(pg, t, t0, 'docks_he111', (110, 200, 560, 560), 'He 111 über der Themse, 7.9.1940', fy=0.4)
    SAY(pg, t, 'Die Bomben trafen vor allem die Docks und die Wohnviertel im Osten der Stadt.', (720, 200), 40, maxw=570, accent=('Docks',))
    PHOTO(pg, t, K('Die Brände waren bis'), 'london_fire', (720, 520, 570, 300), 'Brände an der Themse, 1940', fy=0.5)
    L(pg, t, K('mehr als 400 Menschen', 2), 'mehr als 400 Tote', (110, 880), serif(64, 800), ACC)
    COUNT(pg, t, K('London 57 Nächte in', 1), 0.8, 57, (110, 980), serif(150, 800), lambda v: '%d' % round(v), ACC)
    L(pg, t, K('London 57 Nächte in', 2), 'Nächte in Folge', (110, 1150), serif(44, 400))
    FILM(pg, t, K('London 57 Nächte in', 1), 'night_raid', (720, 900, 570, 300), 'Nachtangriff auf London, 1940')
    SAY(pg, t, 'Für die erschöpften Jagdflieger aber bedeutete der Wechsel eine Atempause, denn ihre Flugplätze wurden kaum noch angegriffen.', (110, 1330), 40, accent=('Atempause,',))
    return pg

# ================= SP12: 15 September, Seelöwe postponed =================
def s12L(t):
    pg = base2(25, True); t0 = TS(12)
    KICK(pg, t, t0, '15. SEPTEMBER 1940'); L(pg, t, t0 + 0.1, 'Battle of Britain Day', (110, 204), serif(80, 800))
    SAY(pg, t, 'Am 15. September griff die Luftwaffe London zweimal mit großen Verbänden an.', (110, 340), 42, accent=('zweimal',))
    PHOTO(pg, t, K('Er fragte Luftvizemarschall Keith'), 'park', (110, 540, 420, 540), 'Keith Park', fy=0.3, zoom=0.05)
    SAY(pg, t, 'Churchill war an diesem Tag in der Leitstelle der 11. Jagdgruppe in Uxbridge.', (590, 540), 38, maxw=700)
    SAY(pg, t, 'Er fragte Luftvizemarschall Keith Park, welche Reserven noch blieben.', (590, 740), 38, maxw=700, accent=('Keith', 'Park,'))
    SAY(pg, t, 'Park antwortete, es gebe keine mehr.', (590, 930), 52, maxw=700, wg=800, accent=('keine',))
    FILM(pg, t, K('Trotzdem wurden die Verbände'), 'crash', (110, 1200, 560, 320), 'Abschuss über England, 1940')
    COUNT(pg, t, K('verloren etwa 60 Flugzeuge.', 2), 0.8, 60, (720, 1200), serif(110, 800), lambda v: 'etwa %d' % round(v), ACC)
    L(pg, t, K('verloren etwa 60 Flugzeuge.', 3), 'deutsche Flugzeuge verloren', (720, 1330), serif(40, 400))
    return pg
def s12R(t):
    pg = base2(26, False); t0 = K('Zwei Tage später verschob')
    KICK(pg, t, t0, '17. SEPTEMBER 1940')
    SAY(pg, t, 'Zwei Tage später verschob Hitler das Unternehmen Seelöwe auf unbestimmte Zeit.', (110, 250), 48, accent=('Seelöwe',))
    FILM(pg, t, K('Britische Bomber hatten in'), 'balloons', (110, 470, 1180, 520), 'Britische Bomber auf dem Weg zu den Invasionshäfen')
    SAY(pg, t, 'Britische Bomber hatten in den Häfen viele der gesammelten Kähne zerstört, und die Herbststürme rückten näher.', (110, 1100), 40)
    stamp(pg, t, K('auf das Frühjahr 1941', 3), 'VERTAGT', (1050, 1340), 60, -8)
    reg((900, 1270, 1200, 1410), K('auf das Frühjahr 1941', 3))
    L(pg, t, K('auf das Frühjahr 1941', 3), 'auf Frühjahr 1941', (110, 1310), serif(60, 800))
    SAY(pg, t, 'Danach kam sie nie wieder ernsthaft zur Sprache.', (110, 1450), 42)
    return pg

# ================= SP13: Coventry, London burns, the Blitz =================
def s13L(t):
    pg = base2(27, True); t0 = TS(13)
    KICK(pg, t, t0, '14. NOVEMBER 1940'); L(pg, t, t0 + 0.1, 'Coventry', (110, 204), serif(96, 800))
    SAY(pg, t, 'Die Luftwaffe griff nun vor allem nachts an, als Ziel dienten Städte und Industrie.', (110, 340), 40, accent=('nachts',))
    PHOTO(pg, t, K('In der Nacht zum 15.'), 'coventry_before', (110, 500, 470, 600), 'Coventry, deutsche Luftaufnahme', fy=0.5)
    PHOTO(pg, t, K('Rund 500 Bomber legten'), 'coventry_cath', (640, 500, 650, 420), 'Die zerstörte Kathedrale von Coventry', fy=0.5)
    L(pg, t, K('mehr als 500 Menschen', 2), 'mehr als 500 Tote', (640, 1010), serif(64, 800), ACC)
    PHOTO(pg, t, K('Die deutsche Propaganda prägte'), 'coventry_ruins', (640, 1120, 650, 380), 'Coventry nach dem Angriff', fy=0.5)
    L(pg, t, K('das Wort coventrieren.', 2), '„coventrieren“', (110, 1260), italic(66), ACC)
    return pg
def s13R(t):
    pg = base2(28, False); t0 = K('Am 29. Dezember brannte')
    KICK(pg, t, t0, '29. DEZEMBER 1940')
    SAY(pg, t, 'Am 29. Dezember brannte die Londoner City.', (110, 250), 46, accent=('City.',))
    PHOTO(pg, t, K('Ein Foto der Kuppel'), 'stpauls', (110, 350, 560, 560), 'St Paul’s Cathedral, 29. Dezember 1940', fy=0.5)
    FILM(pg, t, K('Ein Foto der Kuppel', 3), 'firehose', (720, 350, 570, 300), 'London, 1940')
    SAY(pg, t, 'Die nächtlichen Angriffe dauerten bis Mai 1941.', (720, 770), 38, maxw=570)
    COUNT(pg, t, K('über 40.000 Zivilisten.', 1), 0.9, 40000, (720, 880), serif(84, 800), lambda v: 'über ' + de(v), ACC)
    L(pg, t, K('über 40.000 Zivilisten.', 2), 'tote Zivilisten', (720, 990), serif(40, 400))
    PHOTO(pg, t, K('Die Moral der Bevölkerung'), 'underground', (110, 1070, 560, 330), 'Schutz in der Londoner U-Bahn', fy=0.5)
    PHOTO(pg, t, K('brach jedoch nicht,'), 'shelter_woman', (720, 1070, 570, 330), 'In einem Schutztunnel unter London', fy=0.6)
    SAY(pg, t, 'Die Moral der Bevölkerung brach jedoch nicht, und die Rüstungsproduktion lief weiter.', (110, 1500), 34)
    return pg

# ================= SP14: the balance, the turn east =================
def s14L(t):
    pg = base2(29, True); t0 = TS(14)
    KICK(pg, t, t0, 'BILANZ'); L(pg, t, t0 + 0.1, 'Eine Schlacht in der Luft', (110, 204), serif(76, 800))
    SAY(pg, t, 'Die Schlacht um England gilt heute als die erste große Schlacht, die allein in der Luft entschieden wurde.', (110, 330), 42, accent=('allein',))
    KICK(pg, t, K('Bis Ende Oktober 1940'), 'BIS ENDE OKTOBER 1940', 560)
    COUNT(pg, t, K('rund 1.900 Flugzeuge,', 1), 0.9, 1900, (110, 610), serif(96, 800), lambda v: 'rund ' + de(v), ACC); L(pg, t, K('rund 1.900 Flugzeuge,', 2), 'Flugzeuge der Luftwaffe', (110, 730), serif(38, 400))
    COUNT(pg, t, K('rund 1.000 Jäger.', 1), 0.9, 1000, (720, 610), serif(96, 800), lambda v: 'rund ' + de(v), TXT); L(pg, t, K('rund 1.000 Jäger.', 2), 'Jäger des Fighter Command', (720, 730), serif(38, 400))
    COUNT(pg, t, K('544 Piloten und Besatzungsmitglieder'), 0.9, 544, (720, 820), serif(84, 800), lambda v: '%d' % round(v), TXT); L(pg, t, K('544 Piloten und Besatzungsmitglieder', 1), 'britische Flieger tot', (720, 930), serif(38, 400))
    COUNT(pg, t, K('mehr als 2.500 Flieger.', 2), 0.9, 2500, (110, 820), serif(84, 800), lambda v: 'über ' + de(v), ACC); L(pg, t, K('mehr als 2.500 Flieger.', 3), 'deutsche Flieger tot', (110, 930), serif(38, 400))
    SAY(pg, t, 'Die Luftwaffe hatte ihre Gegner unterschätzt, ihre Ziele mehrmals gewechselt und ihre Bomber zu schwach bewaffnet.', (110, 1030), 38)
    PHOTO(pg, t, K('Die Luftwaffe hatte ihre'), 'he111_cockpit', (110, 1180, 1180, 340), 'Blick aus einer He 111 auf einen zweiten Bomber', fy=0.45)
    return pg
def s14R(t):
    pg = base2(30, False); t0 = K('Großbritannien blieb im Krieg')
    PHOTO(pg, t, t0, 'k6_churchill_coventry', (110, 200, 760, 540), 'Churchill in den Ruinen von Coventry', fy=0.5)
    PHOTO(pg, t, t0 + 0.4, 'k8_truemmer_strasse', (930, 200, 360, 540), 'Zerstörte Straße', fy=0.5)
    SAY(pg, t, 'Großbritannien blieb im Krieg und wurde später zum Sprungbrett für die Landung der Alliierten in Frankreich.', (110, 880), 44, accent=('Sprungbrett',))
    SAY(pg, t, 'Hitler aber wandte sich einem anderen Ziel zu.', (110, 1100), 58, wg=800, accent=('anderen',))
    SAY(pg, t, 'Schon im Sommer 1940 ließ er Pläne für einen Krieg gegen die Sowjetunion ausarbeiten, und im Dezember unterschrieb er die Weisung dafür.', (110, 1250), 42, accent=('Sowjetunion',))
    return pg

# ================= SP15: end page =================
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
END0 = TURNS[14] + TD + 1.3
CLICKS = [END0 + 1.0 + i * 1.1 for i in range(3)]
def s15L(t):
    pg = base2(31, True); t0 = TURNS[14] + TD + 0.2
    KICK(pg, t, t0, 'FORTSETZUNG FOLGT'); L(pg, t, t0 + 0.2, 'TEIL 5', (100, 250), serif(230, 900)); L(pg, t, t0 + 0.5, 'Afrika und der Balkan', (110, 530), serif(76, 400), GREY)
    FILM(pg, t, t0 + 0.8, 'searchlights', (110, 680, 1180, 720))
    return pg
def s15R(t):
    pg = base2(32, False); t0 = END0 - 0.2
    L(pg, t, t0, 'Gefällt dir die Serie?', (110, 220), serif(96, 800)); d = ImageDraw.Draw(pg)
    for i, (nm, ic) in enumerate((('Liken', icon_thumb), ('Teilen', icon_share), ('Abonnieren', icon_bell))):
        y = 560 + i * 280; tc = CLICKS[i]; reg((110, y - 120, 1100, y + 130), tc - 0.6)
        if t < tc - 0.6: continue
        u = clamp((t - tc + 0.6) / 0.45); press = math.exp(-((t - tc) / 0.12) ** 2) if t > tc - 0.3 else 0
        on = t >= tc; col = ACC if on else TXT; sc = (1.0 - 0.18 * press)
        d.rounded_rectangle((120, y - 110, 1020, y + 110), 110, outline=fade_col((200, 200, 200), u), width=5, fill=fade_col(((250, 232, 230) if on else (244, 243, 240)), u))
        if i == 2: ic(d, 240, y + 10, 0.9 * sc, fade_col(col, u), 18 * math.sin((t - tc) * 9) * math.exp(-max(0, t - tc) * 1.5) if on else 0)
        else: ic(d, 240, y + 10, 0.9 * sc, fade_col(col, u))
        d.text((380, y), nm, font=serif(84, 800), fill=fade_col(col, u), anchor='lm')
        if t > tc - 0.35:
            v = eout(clamp((t - tc + 0.35) / 0.3)); px, py = lerp(1250, 900, v), lerp(y + 150, y + 30, v); r_ = 1 - 0.25 * press
            d.polygon([(px, py), (px + 40 * r_, py + 100 * r_), (px + 58 * r_, py + 62 * r_), (px + 100 * r_, py + 56 * r_)], fill=TXT)
    L(pg, t, CLICKS[2] + 0.6, 'damit du Teil 5 nicht verpasst.', (110, 1440), serif(56, 400), GREY)
    return pg

SPREADS = [(s0L, s0R), (s1L, s1R), (s2L, s2R), (s3L, s3R), (s4L, s4R), (s5L, s5R), (s6L, s6R), (s7L, s7R), (s8L, s8R), (s9L, s9R), (s10L, s10R),
           (s11L, s11R), (s12L, s12R), (s13L, s13R), (s14L, s14R), (s15L, s15R)]
FILLS = [(0, 'L', B0, 0.0, K('mehr als dreimal') - 1.5, 'Luftschlacht um England, 1940', 'Aus einem deutschen Bomber'),
         (6, 'L', B6, TF(6), K('um die Jäger der') - 1.0, 'Ärmelkanal, Juli 1940', 'Stukas greifen einen Geleitzug an'),
         (11, 'L', B11, TF(11), K('Göring sah ihnen von') - 1.6, 'London, 7. September 1940', 'Deutsche Luftaufnahme der Themse')]
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
CAMS.sort(key=lambda c: c[0])
MAG = Book(SPREADS, TURNS, CAMS, spine=100)
def frame(t):
    img = MAG(t)
    for f in FILLS:
        c0 = f[3] + (0.35 if f[3] < 0.5 else 0.25)
        if c0 <= t <= f[4] + 0.15: caption(img, t, c0, f[5], f[6], f[4] + 0.15)
    return img                                                  # no fade from or to black (Boran)

if __name__ == '__main__':
    if sys.argv[1] == 'check':
        FG = [(f[0], f[3] - 1.1, f[4] + 0.3, (f[2][0] + (PW if f[1] == 'R' else 0), f[2][1], f[2][0] + f[2][2] + (PW if f[1] == 'R' else 0), f[2][1] + f[2][3])) for f in FILLS]
        for f in FILLS: print('fill sp%d %.1f-%.1f  %.1fs' % (f[0], f[3], f[4], f[4] - f[3]))
        bad = check(MAG, T_END, fills=FG)
        for b in bad:
            e = b[1]; print(b[0], 'sp%d%s' % (e['sp'], e['side']), e['box'], '%.2f-%.2f' % (e['t0'], e['t1']), e['kind'], ('<-> %s' % (b[2]['box'],)) if len(b) > 2 else '')
        print(len(bad), 'problems'); sys.exit()
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); Pc = Image.new('RGB', (3 * 640, ((n + 2) // 3) * 360))
        for i, t in enumerate(ts):
            im = frame(t); ImageDraw.Draw(im).text((20, 20), '%.1f' % t, font=sans(40, 800), fill=(255, 0, 255)); Pc.paste(im.resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
        Pc.save(LB + 'chk/' + sys.argv[2], quality=86); sys.exit()
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
