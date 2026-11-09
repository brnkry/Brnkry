# "Deutschland im Zweiten Weltkrieg", Teil 3: Der Krieg im Westen (16:9). The Teil 2 v3 magazine engine (t2core): every element
# tied to its spoken word, the camera planned from the page elements, films filling the frame with their caption, slowly moving
# colourised photos, red pen circles, counters, maps drawn on, small running pen drawings. No fade from or to black.
from t2core import *
from t2core import _shadow
from lmap import Map
from drawings import tank_m, monoplane_m, wave_flag, paint_uk, paint_fr
from drawings2 import soldier_m, civilian_m, truck_m, gold_m, radio_m, train_m, enigma_m

# ---------- turns: about 1.4 s before the first word of each new spread (about 1.9 s of silence was put into the voice there) ----------
STARTS = ['Nach dem Überfall auf', 'Hitler sah das anders.', 'Sicher ist, dass es', 'Zuerst aber schlug', 'Im Oslofjord fuhr', 'Am Morgen des 10.', 'Am 14. Mai, während',
          'Zur selben Zeit schoben', 'Viele deutsche Soldaten schliefen', 'Die eingeschlossenen Truppen wichen', 'Am 26. Mai begann', 'Am 5. Juni begann', 'Hitler bestimmte den Ort', 'Am frühen Morgen des']
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

# ================= SP0: hook =================
B0 = (110, 600, 1180, 664)
@functools.lru_cache(None)
def masthead():
    pg = base(1, True).copy(); d = ImageDraw.Draw(pg)
    for i, c in enumerate(((24, 24, 26), (196, 30, 34), (236, 186, 32))): d.rectangle((110, 196 + i * 92, 128, 196 + (i + 1) * 92), fill=c)
    d.text((160, 186), 'Deutschland im', font=serif(118, 900), fill=TXT); d.text((160, 326), 'Zweiten Weltkrieg', font=serif(118, 400), fill=TXT)
    for i, c in enumerate(((24, 24, 26), (196, 30, 34), (236, 186, 32))): d.rectangle((110, 490 + i * 9, PW - 110, 490 + (i + 1) * 9), fill=c)
    d.text((110, 545), 'TEIL 3 · DER KRIEG IM WESTEN', font=sans(38, 800), fill=ACC, anchor='lm')
    d.text((PW - 110, 545), 'MAI BIS JUNI 1940', font=sans(28, 600), fill=GREY, anchor='rm')
    return pg
def s0L(t):
    pg = masthead().copy(); FILM(pg, t, -1, 'tanks', B0, 'Panzer im Westfeldzug, Mai 1940', 0.8)
    L(pg, t, -1, 'Im Mai 1940 besaß Frankreich', (110, 1400), serif(56, 400)); L(pg, t, -1, 'mehr Panzer als die Wehrmacht.', (110, 1478), serif(56, 800))
    return pg
def s0R(t):
    pg = base2(2, False); t0 = K('die stärkste Festungslinie')
    KICK(pg, t, K('mehr Panzer als die', 1) - 0.6, 'PANZER IM MAI 1940')
    COUNT(pg, t, K('mehr Panzer als die', 1) - 0.4, 0.9, 3384, (110, 250), serif(110, 800), lambda v: de(v), ACC); L(pg, t, K('mehr Panzer als die', 1) - 0.3, 'Frankreich', (520, 290), serif(56, 400))
    COUNT(pg, t, K('als die Wehrmacht,', 2), 0.9, 2445, (110, 400), serif(110, 800), lambda v: de(v), TXT); L(pg, t, K('als die Wehrmacht,', 2), 'Wehrmacht', (520, 440), serif(56, 400))
    PHOTO(pg, t, t0, 'maginot_dome', (110, 600, 560, 420), 'Panzerkuppel der Maginot-Linie', fy=0.45)
    SAY(pg, t, 'Sechs Wochen später musste es einen Waffenstillstand unterschreiben,', (730, 610), 42, maxw=560, accent=('Sechs', 'Wochen'))
    PHOTO(pg, t, K('in demselben Eisenbahnwagen'), 'comp_wagon', (730, 900, 560, 300), 'Der Salonwagen von Compiègne', fy=0.5)
    L(pg, t, K('Deutschland 1918 den', 1), '1918', (730, 1270), serif(90, 800), GREY)
    RULE(pg, t, K('Der Grund lag nicht') - 0.1, 1410)
    SAY(pg, t, 'Der Grund lag nicht in der Zahl der Panzer, sondern in einem Plan, den fast niemand für möglich gehalten hatte.', (110, 1440), 48, accent=('Plan,',))
    return pg

# ================= SP1: Sitzkrieg =================
B1 = (110, 312, 1180, 630)
def s1L(t):
    pg = base2(3, True); t0 = TS(1)
    KICK(pg, t, t0, 'HERBST 1939 BIS FRÜHJAHR 1940'); L(pg, t, t0 + 0.1, 'Der seltsame Krieg', (110, 204), serif(70, 800))
    FILM(pg, t, TF(1) - 1.0, 'westfront', B1, 'Westfront, Winter 1939/40')
    SAY(pg, t, 'Nach dem Überfall auf Polen hatten Großbritannien und Frankreich Deutschland den Krieg erklärt.', (110, 1050), 42)
    SAY(pg, t, 'Doch im Westen wurde kaum gekämpft.', (110, 1200), 56, wg=800, accent=('kaum',))
    for i, (nm, ph_, paint, y) in enumerate((('drôle de guerre', 'drôle de guerre', paint_fr, 1335), ('Phoney War', 'Phoney War', paint_uk, 1440), ('Sitzkrieg', 'vom Sitzkrieg', None, 1545))):
        t1 = K(ph_, 0 if i < 2 else 1)
        if paint: reg((110, y - 10, 210, y + 60), t1); wave_flag(pg, t, t1, 120, y, 90, 56, paint, pole=False)
        L(pg, t, t1, nm, (240, y - 6), italic(56) if i < 2 else serif(56, 800), TXT if i < 2 else ACC)
    return pg
def s1R(t):
    pg = base2(4, False); t0 = K('Französische Soldaten warteten')
    PHOTO(pg, t, t0, 'maginot', (110, 200, 560, 400), 'Werk der Maginot-Linie', fy=0.5)
    SAY(pg, t, 'Französische Soldaten warteten in den Bunkern der Maginot-Linie, einer Kette von Festungen entlang der deutschen Grenze.', (720, 200), 38, maxw=570, accent=('Maginot-Linie,',))
    PHOTO(pg, t, K('Gegenüber lagen deutsche'), 'westwall_visit', (720, 640, 570, 330), 'Westwall, 1940', fy=0.5)
    L(pg, t, K('am Westwall.', 1), 'Westwall', (110, 700), serif(80, 800))
    RULE(pg, t, K('Britische Bomber warfen') - 0.1, 1030)
    SAY(pg, t, 'Britische Bomber warfen über Deutschland keine Bomben ab, sondern Millionen Flugblätter.', (110, 1060), 40, maxw=600, accent=('keine', 'Flugblätter.'))
    PHOTO(pg, t, K('Ein britisches Expeditionskorps'), 'banners', (760, 1060, 530, 300), 'Propagandatafeln an der Front', fy=0.5)
    SAY(pg, t, 'Ein britisches Expeditionskorps zog nach Frankreich,', (110, 1310), 36, maxw=600)
    SAY(pg, t, 'Sie glaubten, die Zeit arbeite für sie.', (110, 1470), 56, wg=800, accent=('Zeit',))
    return pg

# ================= SP2: the first plan, Mechelen =================
MW = Map('mw', (PW, PH), (110, 560, 1180, 900), -2.0, 13.0, 46.0)
def s2L(t):
    pg = base2(5, True); t0 = TS(2); m = MW
    KICK(pg, t, t0, 'OKTOBER 1939'); L(pg, t, t0 + 0.1, 'Hitler will angreifen', (110, 212), serif(88, 800))
    SAY(pg, t, 'Seine Generäle hielten das Heer dafür noch nicht für bereit, und der Termin wurde immer wieder verschoben, meist wegen des Wetters.', (110, 360), 36, accent=('verschoben,',))
    t1 = K('Der erste Plan sah'); reg((100, 550, 1300, 1470), t1, kind='pic')
    if t >= t1:
        west_map(pg, t, t1, m, tint=('France',))
        m.label(pg, t, t1 + 0.3, 'FRANKREICH', (2.4, 47.6), sans(40, 800), TXT); m.label(pg, t, t1 + 0.3, 'DEUTSCHES REICH', (10.0, 51.2), sans(32, 800), GREY, sw=4)
        m.label(pg, t, K('Vorstoß durch Belgien', 2), 'BELGIEN', (4.4, 50.25), sans(30, 800), ACC, sw=5)
        arrow(pg, m, t, K('Vorstoß durch Belgien', 2) + 0.1, [(6.8, 51.2), (5.0, 50.9), (3.6, 50.6), (2.7, 49.9)], col=GR)
        dot(pg, m, t, t1 + 0.4, (2.35, 48.86), 'Paris')
    L(pg, t, K('ähnlich wie 1914.', 2), 'wie 1914', (900, 1500), serif(72, 800), GREY)
    return pg
def s2R(t):
    pg = base2(6, False); t0 = K('Am 10. Januar 1940')
    KICK(pg, t, t0, '10. JANUAR 1940'); L(pg, t, t0 + 0.1, 'Notlandung in Belgien', (110, 212), serif(88, 800))
    DRAW(pg, t, K('deutsches Kurierflugzeug im'), 0.9, lambda ph: monoplane_m(1080, 470, 0.4, ph), (900, 380, 1260, 560))
    SAY(pg, t, 'An Bord saß Major Hellmuth Reinberger mit Teilen der Angriffspläne.', (110, 400), 40, maxw=740, accent=('Hellmuth', 'Reinberger'))
    PAPER_DOC(pg, t, K('Teilen der Angriffspläne.', 2), (110, 640, 640, 560), 'GEHEIM', ['Angriff im Westen', 'Luftlandung bei Namur', 'Stoß durch Belgien', '...'], t_burn=K('die Papiere zu verbrennen,', 2))
    SAY(pg, t, 'doch belgische Soldaten stellten sie sicher.', (820, 660), 40, maxw=470, accent=('sicher.',))
    RULE(pg, t, K('Ob dieser Zwischenfall') - 0.1, 1290)
    SAY(pg, t, 'Ob dieser Zwischenfall den deutschen Plan änderte, ist unter Historikern umstritten.', (110, 1320), 46, accent=('umstritten.',))
    return pg

# ================= SP3: Manstein =================
MA = Map('ma', (PW, PH), (110, 600, 1180, 900), -1.0, 11.0, 47.2)
def s3L(t):
    pg = base2(7, True); t0 = TS(3)
    KICK(pg, t, t0, 'EIN ANDERER ENTWURF')
    PHOTO(pg, t, K('Er stammte von Generalleutnant'), 'manstein', (110, 280, 470, 620), 'Erich von Manstein', fy=0.25, zoom=0.05)
    L(pg, t, K('Erich von Manstein,', 0), 'Erich', (650, 300), serif(80, 400)); L(pg, t, K('Erich von Manstein,', 1), 'von Manstein', (650, 400), serif(96, 800))
    SAY(pg, t, 'Stabschef der Heeresgruppe A', (650, 560), 40, col=GREY)
    SAY(pg, t, 'Manstein wollte den Hauptstoß nicht durch Belgien führen, sondern weiter südlich durch die Ardennen,', (110, 1010), 44, accent=('Ardennen,',))
    SAY(pg, t, 'ein bewaldetes Mittelgebirge, das die Franzosen für Panzer als kaum passierbar hielten.', (110, 1150), 42, accent=('kaum', 'passierbar'))
    DRAW(pg, t, K('für Panzer als kaum', 2), 0.9, lambda ph: tank_m(1120, 1400, 0.3, ph), (980, 1330, 1260, 1460))
    return pg
def s3R(t):
    pg = base2(8, False); m = MA; t1 = K('Manstein wollte den Hauptstoß')
    reg((100, 590, 1300, 1510), t1, kind='pic')
    if t >= t1:
        west_map(pg, t, t1, m, tint=('France',))
        m.label(pg, t, t1 + 0.3, 'FRANKREICH', (2.0, 48.2), sans(38, 800), TXT); m.label(pg, t, t1 + 0.3, 'BELGIEN', (4.6, 50.45), sans(26, 800), GREY, sw=4)
        arrow(pg, m, t, t1 + 0.4, [(6.8, 51.3), (5.0, 51.0), (3.7, 50.7)], col=GR)
        STRIKE(pg, t, K('nicht durch Belgien führen,', 2), *[int(v) for v in (m.mp(4.2, 51.3)[0], m.mp(6.2, 51.3)[0], m.mp(5.2, 51.15)[1])], 9)
        m.label(pg, t, K('südlich durch die Ardennen,', 3), 'ARDENNEN', (6.1, 50.25), sans(32, 800), ACC, sw=5)
        arrow(pg, m, t, K('südlich durch die Ardennen,', 3) + 0.1, [(7.2, 50.1), (5.8, 49.85), (4.9, 49.7), (3.3, 49.9), (1.9, 50.1)], dur=1.6)
        dot(pg, m, t, K('südlich durch die Ardennen,', 3) + 0.6, (4.94, 49.70), 'Sedan', dy=44)
    L(pg, t, K('Die Heeresleitung lehnte'), 'abgelehnt', (110, 230), serif(80, 800), GREY); STRIKE(pg, t, K('versetzte Manstein auf', 1), 100, 500, 280, 9)
    KICK(pg, t, K('Am 17. Februar 1940'), '17. FEBRUAR 1940', 380)
    SAY(pg, t, 'Hitler übernahm die Idee.', (110, 430), 64, wg=800, accent=('Idee.',))
    return pg

# ================= SP4: Weserübung =================
MN = Map('mn', (PW, PH), (110, 315, 1180, 1250), 3.0, 32.7, 54.4)
def s4L(t):
    pg = base2(9, True); m = MN; t0 = TS(4)
    KICK(pg, t, t0, 'APRIL 1940'); L(pg, t, t0 + 0.1, 'Erz aus Schweden', (110, 204), serif(70, 800))
    reg((100, 305, 1300, 1575), t0, kind='pic')
    if t >= t0:
        k = eout((t - t0) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=('reich',), outline=('reich',))
        m.tint(pg, 'Norway', k, ACC, 0.05); m.label(pg, t, t0 + 0.3, 'NORWEGEN', (8.6, 61.6), sans(34, 800), TXT); m.label(pg, t, t0 + 0.3, 'SCHWEDEN', (16.0, 62.3), sans(32, 800), GREY, sw=4)
        dot(pg, m, t, K('lief im Winter das'), (20.22, 67.85), 'Kiruna', dx=10)
        m.line(pg, t, K('das schwedische Eisenerz,', 1), 1.2, [(20.22, 67.85), (19.0, 68.2), (17.43, 68.44)], col=TXT, wd=6, dash=14)
        dot(pg, m, t, K('das schwedische Eisenerz,', 1) + 1.0, (17.43, 68.44), 'Narvik', dx=-20)
        m.label(pg, t, K('die norwegischen Gewässer zu', 3), 'Minen', (5.6, 64.6), italic(40), ACC, sw=5)
        t2 = K('Das Unternehmen Weserübung'); m.label(pg, t, t2, 'WESERÜBUNG', (13.0, 56.6), sans(34, 800), ACC, sw=5)
        for i, (ll, nm) in enumerate((((12.57, 55.68), 'Kopenhagen'), ((10.75, 59.91), 'Oslo'), ((8.0, 58.15), 'Kristiansand'), ((5.32, 60.39), 'Bergen'), ((10.4, 63.43), 'Trondheim'))):
            ti = K('von Oslo bis', 2) - 2.2 + 0.35 * i if i else K('Dänemark wurde innerhalb')
            arrow(pg, m, t, ti, [(9.5, 54.6), ll], dur=0.7, wd=10); dot(pg, m, t, ti + 0.6, ll, nm, dx=(60 if i in (2, 3) else 0))
        arrow(pg, m, t, K('von Oslo bis Narvik.', 3), [(9.5, 54.6), (5.2, 61.0), (12.0, 66.0), (16.9, 68.2)], dur=1.2, wd=10)
    return pg
def s4R(t):
    pg = base2(10, False); t0 = K('Am 9. April 1940')
    KICK(pg, t, t0, '9. APRIL 1940'); L(pg, t, t0 + 0.1, 'Unternehmen Weserübung', (110, 212), serif(84, 800))
    FILM(pg, t, K('Das Unternehmen Weserübung', 2), 'harbour_no', (110, 370, 1180, 560), 'Deutsche Schiffe in einem norwegischen Hafen, April 1940')
    SAY(pg, t, 'Dänemark wurde innerhalb weniger Stunden besetzt und gab noch am selben Tag auf.', (110, 1060), 46, accent=('weniger', 'Stunden'))
    SAY(pg, t, 'In Norwegen landeten deutsche Truppen gleichzeitig in mehreren Häfen, von Oslo bis Narvik.', (110, 1290), 46, accent=('Oslo', 'Narvik.'))
    return pg

# ================= SP5: Blücher, the king, Narvik =================
def s5L(t):
    pg = base2(11, True); t0 = TS(5)
    KICK(pg, t, t0, 'OSLOFJORD, 9. APRIL 1940'); L(pg, t, t0 + 0.1, 'Die Blücher', (110, 212), serif(96, 800))
    PHOTO(pg, t, t0 + 0.3, 'bluecher_col', (110, 380, 1180, 420), 'Der schwere Kreuzer Blücher', fy=0.5)
    PHOTO(pg, t, K('An der Festung Oscarsborg'), 'oscarsborg_gun', (110, 910, 540, 350), 'Geschütz der Festung Oscarsborg', fy=0.5)
    SAY(pg, t, 'Torpedos trafen das Schiff, und die Blücher sank.', (720, 910), 46, maxw=570, accent=('sank.',))
    PHOTO(pg, t, K('und die Blücher sank.', 2), 'bluecher_ria', (720, 1090, 570, 300), 'Die Blücher kentert, 9. April 1940', fy=0.5)
    L(pg, t, K('Hunderte Männer kamen'), 'Hunderte Tote', (110, 1370), serif(64, 800), ACC)
    return pg
def s5R(t):
    pg = base2(12, False); t0 = K('Die Verzögerung reichte aus:')
    SAY(pg, t, 'Die Verzögerung reichte aus:', (110, 200), 50, wg=800)
    L(pg, t, K('König Haakon VII.,', 1), 'König Haakon VII.', (110, 300), serif(60, 800))
    DRAW(pg, t, K('die norwegischen Goldreserven'), 1.0, lambda ph: gold_m(1040, 400, 0.6, ph), (880, 300, 1200, 420))
    SAY(pg, t, 'Der König lehnte es ab, eine von Deutschland eingesetzte Regierung anzuerkennen.', (110, 480), 40, maxw=1180)
    RULE(pg, t, K('Bei Narvik verlor') - 0.1, 640)
    KICK(pg, t, K('Bei Narvik verlor'), 'NARVIK, 10. UND 13. APRIL 1940', 670)
    PHOTO(pg, t, K('Bei Narvik verlor'), 'narvik_destroyer', (110, 720, 560, 380), 'Deutscher Zerstörer, Narvik', fy=0.5)
    SHIPS(pg, t, K('alle zehn Zerstörer,', 1), 10, 780, 760, 50, t_cross=K('alle zehn Zerstörer,', 2) + 0.2)
    L(pg, t, K('alle zehn Zerstörer,', 1), '10 Zerstörer', (740, 830), serif(80, 800), ACC)
    PHOTO(pg, t, K('Britische, französische und polnische'), 'narvik_harbour', (740, 960, 550, 300), 'Hafen von Narvik, April 1940', fy=0.5)
    SAY(pg, t, 'Dann mussten die Alliierten ihre Truppen abziehen, denn in Frankreich stand inzwischen alles auf dem Spiel.', (110, 1390), 42, accent=('Frankreich',))
    return pg

# ================= SP6: 10 May, Eben-Emael, the trap =================
MB = Map('mb', (PW, PH), (110, 560, 1180, 700), 1.0, 9.0, 49.1)
def s6L(t):
    pg = base2(13, True); t0 = TS(6); m = MB
    KICK(pg, t, t0, '10. MAI 1940'); L(pg, t, t0 + 0.1, 'Angriff im Westen', (110, 212), serif(88, 800))
    PHOTO(pg, t, K('griff die Wehrmacht die'), 'lux_border', (900, 190, 390, 260), 'Luxemburg, 10. Mai 1940', fy=0.5, zoom=0.04)
    reg((100, 550, 1300, 1270), K('die Niederlande, Belgien', 1), kind='pic')
    if t >= K('die Niederlande, Belgien', 1):
        t1 = K('die Niederlande, Belgien', 1); west_map(pg, t, t1, m)
        for nm, ph_, i, ll, lab in (('Netherlands', 'die Niederlande, Belgien', 1, (5.8, 51.95), 'NIEDERLANDE'), ('Belgium', 'Belgien und Luxemburg', 0, (4.6, 50.7), 'BELGIEN'), ('Luxembourg', 'und Luxemburg an.', 1, (6.1, 49.75), 'LUX.')):
            ti = K(ph_, i); m.hatch(pg, nm, clamp((t - ti) / 0.8)); m.label(pg, t, ti + 0.2, lab, ll, sans(28, 800), TXT, sw=5)
        m.label(pg, t, t1 + 0.3, 'FRANKREICH', (2.6, 49.3), sans(30, 800), GREY, sw=4)
    t2 = K('Am selben Tag trat')
    PHOTO(pg, t, t2, 'chamberlain', (110, 1300, 300, 260), 'Neville Chamberlain', fy=0.3)
    PHOTO(pg, t, K('Sein Nachfolger wurde Winston'), 'churchill', (520, 1300, 380, 260), 'Winston Churchill', fy=0.35)
    SAY(pg, t, 'Sein Nachfolger wurde Winston Churchill.', (960, 1310), 40, maxw=330, accent=('Winston', 'Churchill.'))
    return pg
def s6R(t):
    pg = base2(14, False); t0 = K('Fallschirmjäger sprangen über')
    FILM(pg, t, t0, 'paras', (110, 200, 560, 380), 'Transportflugzeuge Ju 52, Mai 1940')
    SAY(pg, t, 'Fallschirmjäger sprangen über den Niederlanden ab, um Brücken und Flugplätze zu besetzen.', (720, 200), 38, maxw=570)
    KICK(pg, t, K('In Belgien landeten Lastensegler'), 'FESTUNG EBEN-EMAEL', 672)
    PHOTO(pg, t, K('In Belgien landeten Lastensegler'), 'eben_paras', (110, 720, 560, 380), 'Fallschirmpioniere nach dem Angriff', fy=0.4)
    L(pg, t, K('weniger als hundert Fallschirmpionieren', 2), '< 100', (720, 700), serif(110, 800), ACC); L(pg, t, K('weniger als hundert Fallschirmpionieren', 3), 'Fallschirmpioniere', (720, 835), serif(46, 400))
    PHOTO(pg, t, K('Mit Hohlladungen setzten sie'), 'eben_bridge', (720, 910, 570, 300), 'Gesprengte Brücke, Eben-Emael', fy=0.5)
    COUNT(pg, t, K('rund 780 belgische', 1), 0.9, 780, (110, 1200), serif(110, 800), lambda v: '%d' % round(v), TXT); L(pg, t, K('rund 780 belgische', 2), 'belgische Soldaten ergaben sich', (110, 1325), serif(36, 400))
    RULE(pg, t, K('Die Angriffe im Norden') - 0.1, 1385)
    SAY(pg, t, 'Die Angriffe im Norden wirkten genau so, wie die Alliierten es erwartet hatten.', (110, 1410), 38)
    SAY(pg, t, 'Damit liefen sie in die Falle.', (110, 1545), 56, wg=800, accent=('Falle.',))
    return pg

# ================= SP7: Rotterdam =================
B7 = (110, 312, 1180, 630)
def s7L(t):
    pg = base2(15, True); t0 = TS(7)
    t0 = K('Rund 850 Menschen') - 0.2; KICK(pg, t, t0, 'ROTTERDAM, 14. MAI 1940'); L(pg, t, t0 + 0.1, 'Bomben auf die Stadt', (110, 204), serif(70, 800))
    FILM(pg, t, TF(7) - 1.0, 'rotterdam', B7, 'Die zerstörte Innenstadt von Rotterdam')
    COUNT(pg, t, K('Rund 850 Menschen', 1), 0.9, 850, (110, 1060), serif(120, 800), lambda v: 'rund %d' % round(v), ACC); L(pg, t, K('Rund 850 Menschen', 2), 'Tote', (760, 1110), serif(60, 400))
    COUNT(pg, t, K('fast 80.000 wurden', 1), 0.9, 80000, (110, 1260), serif(96, 800), lambda v: 'fast ' + de(v), TXT); L(pg, t, K('wurden obdachlos.', 1), 'obdachlos', (800, 1290), serif(60, 400))
    return pg
def s7R(t):
    pg = base2(16, False)
    PHOTO(pg, t, K('Rund 850 Menschen'), 'laurenskerk', (110, 200, 1180, 560), 'Rotterdam nach dem Bombardement, Laurenskerk', fy=0.5)
    SAY(pg, t, 'Noch am selben Abend legte die niederländische Armee die Waffen nieder.', (110, 870), 46, accent=('Waffen', 'nieder.'))
    PHOTO(pg, t, K('Königin Wilhelmina und die'), 'wilhelmina', (110, 1110, 560, 420), 'Königin Wilhelmina bei Radio Oranje', fy=0.4)
    SAY(pg, t, 'Königin Wilhelmina und die Regierung waren bereits nach London gegangen.', (720, 1120), 42, maxw=570, accent=('London',))
    DRAW(pg, t, K('bereits nach London gegangen.', 2), 0.8, lambda ph: radio_m(1000, 1440, 0.55, ph), (880, 1360, 1150, 1530))
    return pg

# ================= SP8: Ardennes, Sedan, Pervitin =================
MS = Map('ms', (PW, PH), (110, 315, 1180, 760), 3.4, 7.0, 49.0)
def s8L(t):
    pg = base2(17, True); t0 = TS(8)
    t0 = K('Über enge Waldstraßen') - 0.2; KICK(pg, t, t0, 'ARDENNEN, MAI 1940'); L(pg, t, t0 + 0.1, 'Durch den Wald', (110, 204), serif(70, 800))
    FILM(pg, t, TF(8) - 1.0, 'column', (110, 312, 1180, 590), 'Deutsche Kolonnen auf dem Vormarsch, Mai 1940')
    PHOTO(pg, t, K('Über enge Waldstraßen'), 'panzer_wood', (110, 980, 560, 380), 'Leichte Panzer in einem Wald im Westen', fy=0.5)
    SAY(pg, t, 'Über enge Waldstraßen rollten Zehntausende Fahrzeuge, und es kam zu kilometerlangen Staus.', (720, 990), 38, maxw=570, accent=('Zehntausende', 'kilometerlangen'))
    DRAW(pg, t, K('rollten Zehntausende Fahrzeuge,', 1), 0.8, lambda ph: truck_m(900, 1460, 0.45, ph), (740, 1360, 1060, 1480))
    SAY(pg, t, 'doch die französische Führung erkannte nicht, wo der Hauptstoß lag.', (110, 1475), 38, maxw=1180, accent=('Hauptstoß',))
    return pg
def s8R(t):
    pg = base2(18, False); m = MS; t0 = K('Am 13. Mai erreichten')
    KICK(pg, t, t0, '13. MAI 1940'); L(pg, t, t0 + 0.1, 'Sedan', (110, 204), serif(70, 800))
    reg((100, 305, 1300, 1085), t0, kind='pic')
    if t >= t0:
        k = eout((t - t0) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=('reich',), outline=('reich',)); m.tint(pg, 'France', k, ACC, 0.05)
        m.line(pg, t, t0 + 0.3, 1.2, [(5.38, 49.16), (5.1, 49.5), (4.94, 49.70), (4.72, 49.77), (4.83, 50.14), (4.91, 50.26), (4.86, 50.47)], col=(60, 110, 180), wd=8)
        m.label(pg, t, K('die Maas bei Sedan.', 1), 'Maas', (4.55, 50.25), italic(40), (60, 110, 180), sw=5)
        dot(pg, m, t, K('die Maas bei Sedan.', 3), (4.94, 49.70), 'Sedan', dx=60, dy=10)
        m.label(pg, t, t0 + 0.4, 'BELGIEN', (5.2, 50.35), sans(28, 800), GREY, sw=4); m.label(pg, t, t0 + 0.4, 'FRANKREICH', (4.2, 49.35), sans(30, 800), TXT, sw=4)
        arrow(pg, m, t, K('Gruppe von Generalleutnant Heinz', 1), [(6.4, 49.95), (5.6, 49.8), (5.05, 49.72)], dur=1.0)
        arrow(pg, m, t, K('über den Fluss.', 1), [(4.95, 49.70), (4.5, 49.62), (3.9, 49.6)], dur=0.9)
    PHOTO(pg, t, K('Panzer der Gruppe von', 1), 'guderian_enigma', (110, 1110, 380, 450), 'Heinz Guderian im Funkpanzerwagen', fy=0.25)
    SAY(pg, t, 'Stundenlang griff die Luftwaffe die französischen Stellungen an,', (540, 1110), 36, maxw=750)
    PHOTO(pg, t, K('dann setzten Infanterie und'), 'floing', (540, 1220, 470, 280), 'Pontonbrücke über die Maas bei Floing', fy=0.5)
    L(pg, t, K('Die französische Front brach'), 'Die Front', (1040, 1250), serif(46, 400)); L(pg, t, K('Front brach auf.', 1), 'bricht.', (1040, 1320), serif(60, 800), ACC)
    return pg

# ================= SP9: Pervitin, Rommel, Abbeville, Reynaud =================
MC = Map('mc', (PW, PH), (110, 880, 1180, 680), -0.5, 7.0, 48.6)
def s9L(t):
    pg = base2(19, True); t0 = TS(9)
    KICK(pg, t, t0, 'APRIL BIS JULI 1940'); L(pg, t, t0 + 0.1, 'Pervitin', (110, 212), serif(96, 800))
    PHOTO(pg, t, t0 + 0.3, 'pervitin', (110, 380, 560, 380), 'Pervitin, Deutschlandmuseum Berlin', fy=0.5, zoom=0.04)
    COUNT(pg, t, K('mehr als 35 Millionen', 2), 1.0, 35, (720, 390), serif(130, 800), lambda v: '%d Mio.' % round(v), ACC); L(pg, t, K('Millionen Tabletten Pervitin', 1), 'Tabletten', (720, 560), serif(56, 400))
    SAY(pg, t, 'ein Aufputschmittel auf der Grundlage von Methamphetamin.', (720, 650), 34, maxw=570, accent=('Methamphetamin.',))
    RULE(pg, t, K('Die Panzer fuhren nun') - 0.1, 858)
    m = MC; t1 = K('Die Panzer fuhren nun')
    reg((100, 870, 1300, 1570), t1, kind='pic')
    if t >= t1:
        k = eout((t - t1) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=('reich',), outline=('reich',)); m.tint(pg, 'France', k, ACC, 0.05)
        dot(pg, m, t, t1 + 0.2, (2.35, 48.86), 'Paris', dy=-30); dot(pg, m, t, t1 + 0.3, (4.94, 49.70), 'Sedan', dy=36)
        arrow(pg, m, t, K('nach Westen, zum Ärmelkanal.', 0), [(4.85, 49.75), (3.8, 49.9), (2.6, 50.05), (1.95, 50.1)], dur=1.6); dot(pg, m, t, K('Am 20. Mai erreichte'), (1.83, 50.10), 'Abbeville', dy=-34)
        m.label(pg, t, K('zum Ärmelkanal.', 1), 'Ärmelkanal', (0.6, 50.6), italic(34), GREY, sw=4)
    return pg
def s9R(t):
    pg = base2(20, False); t0 = K('Eine der schnellsten war')
    PHOTO(pg, t, t0, 'rommel_maps', (110, 200, 560, 420), 'Erwin Rommel (vorn) mit Offizieren, Mai 1940', fy=0.3)
    L(pg, t, K('Generalmajor Erwin Rommel.', 1), 'Erwin Rommel', (720, 210), serif(64, 800)); NOTE(pg, t, K('Generalmajor Erwin Rommel.', 1), '7. Panzerdivision', (720, 300))
    L(pg, t, K('bald die Gespensterdivision.', 2), '„Gespensterdivision“', (720, 420), italic(52), ACC)
    RULE(pg, t, K('Am 20. Mai erreichte') - 0.1, 730)
    KICK(pg, t, K('Am 20. Mai erreichte'), '20. MAI 1940, ABBEVILLE', 755)
    SAY(pg, t, 'Die alliierten Armeen in Belgien und Nordfrankreich waren vom Rest Frankreichs abgeschnitten.', (110, 805), 44, accent=('abgeschnitten.',))
    RULE(pg, t, K('Am 15. Mai hatte') - 0.1, 1030)
    PHOTO(pg, t, K('Am 15. Mai hatte'), 'reynaud_petain', (110, 1060, 520, 500), 'Paul Reynaud (Mitte) mit Pétain und Weygand, Mai 1940', fy=0.3)
    NOTE(pg, t, K('Am 15. Mai hatte'), 'Reynaud an Churchill, 15. Mai:', (690, 1060))
    QUOTE(pg, t, K('„Wir sind geschlagen.“'), 'Wir sind', (690, 1150), 84); L(pg, t, K('„Wir sind geschlagen.“', 2), 'geschlagen.“', (690, 1260), italic(84), ACC)
    return pg

# ================= SP10: the halt order =================
MD = Map('md', (PW, PH), (110, 315, 1180, 820), 0.6, 5.6, 49.6)
def s10L(t):
    pg = base2(21, True); m = MD; t0 = TS(10)
    KICK(pg, t, t0, 'ENDE MAI 1940'); L(pg, t, t0 + 0.1, 'Der Kessel', (110, 204), serif(70, 800))
    reg((100, 305, 1300, 1145), t0, kind='pic')
    if t >= t0:
        k = eout((t - t0) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=('reich',), outline=('reich',)); m.tint(pg, 'France', k, ACC, 0.04)
        m.label(pg, t, t0 + 0.3, 'BELGIEN', (4.3, 50.9), sans(28, 800), GREY, sw=4); m.label(pg, t, t0 + 0.3, 'FRANKREICH', (4.6, 49.75), sans(28, 800), GREY, sw=4)
        pocket = [(1.9, 51.0), (2.55, 51.12), (3.2, 51.25), (3.6, 51.0), (3.3, 50.7), (2.6, 50.62), (2.0, 50.8)]
        hatch_mask(pg, m, polymask(m, pocket), clamp((t - K('zur Küste zurück, nach', 3)) / 0.8), col=(60, 110, 180), a=0.6)
        dot(pg, m, t, K('zur Küste zurück, nach', 3), (2.38, 51.03), 'Dünkirchen', dy=-38)
        for i, p in enumerate(((1.6, 50.3), (2.4, 50.25), (3.4, 50.35))):
            arrow(pg, m, t, K('hielten die deutschen Panzer', 1) + 0.2 * i, [p, (p[0] + 0.25, p[1] + 0.33)], dur=0.6, wd=12)
        if t >= K('hielten die deutschen Panzer', 3):
            u = eout((t - K('hielten die deutschen Panzer', 3)) / 0.3); x, y = m.mp(2.5, 50.02); d = ImageDraw.Draw(pg)
            d.text((x, y), 'HALT', font=sans(int(90 * (1.4 - 0.4 * u)), 900), fill=fade_col(ACC, u), anchor='mm')
    SAY(pg, t, 'Der Befehl kam von Generaloberst Gerd von Rundstedt, und Hitler bestätigte ihn.', (110, 1180), 42, accent=('Rundstedt,',))
    SAY(pg, t, 'Die Luftwaffe sollte den Kessel allein zerschlagen.', (110, 1400), 46, wg=800)
    return pg
def s10R(t):
    pg = base2(22, False); t0 = K('Erst zwei Tage später')
    PHOTO(pg, t, K('Die Luftwaffe sollte den'), 'dunkirk_dunes', (110, 200, 1180, 700), 'Britische Soldaten in den Dünen bei Dünkirchen', fy=0.4)
    SAY(pg, t, 'Erst zwei Tage später durften die Panzer weiterfahren.', (110, 1010), 48, accent=('zwei', 'Tage'))
    RULE(pg, t, K('Warum dieser Haltbefehl gegeben') - 0.1, 1190)
    L(pg, t, K('Warum dieser Haltbefehl gegeben', 2), 'Der Haltbefehl', (110, 1230), serif(84, 800))
    SAY(pg, t, 'beschäftigt Historiker bis heute.', (110, 1360), 52, accent=('bis', 'heute.'))
    return pg

# ================= SP11: Dynamo, Bletchley =================
B11 = (110, 312, 1180, 630)
def s11L(t):
    pg = base2(23, True); t0 = TS(11)
    t0 = K('und holten Soldaten von') + 0.1; KICK(pg, t, t0, '26. MAI BIS 4. JUNI 1940'); L(pg, t, t0 + 0.1, 'Operation Dynamo', (110, 204), serif(70, 800))
    FILM(pg, t, TF(11) - 1.0, 'dunkirk', B11, 'Britische Schiffe vor Dünkirchen')
    PHOTO(pg, t, K('holten Soldaten von den'), 'dunkirk_beach', (110, 1050, 560, 360), 'Soldaten warten am Strand auf die Schiffe', fy=0.5)
    SAY(pg, t, 'und holten Soldaten von den Stränden und der Mole.', (720, 1050), 40, maxw=570, accent=('Stränden',))
    SAY(pg, t, 'Am 28. Mai kapitulierte die belgische Armee.', (720, 1290), 38, maxw=570)
    return pg
def s11R(t):
    pg = base2(24, False)
    PHOTO(pg, t, K('Französische Truppen verteidigten'), 'dunkirk_ship', (110, 200, 400, 520), 'Gerettete Soldaten an Bord, Mai 1940', fy=0.3)
    COUNT(pg, t, K('Bis zum 4. Juni'), 1.4, 338226, (560, 220), serif(120, 800), lambda v: de(v), ACC); L(pg, t, K('Soldaten nach England gebracht,', 0), 'Soldaten gerettet', (560, 370), serif(52, 400))
    L(pg, t, K('darunter mehr als 100.000', 2), 'darunter über 100.000 Franzosen', (560, 460), serif(40, 400), GREY)
    SAY(pg, t, 'Fast ihre gesamte schwere Ausrüstung blieb am Strand zurück.', (560, 560), 38, maxw=730)
    QUOTE(pg, t, K('Churchill sagte vor dem'), 'Kriege werden nicht durch', (110, 830), 56); L(pg, t, K('nicht durch Evakuierungen gewonnen.', 2), 'Evakuierungen gewonnen.“', (110, 910), italic(56), ACC)
    NOTE(pg, t, K('Churchill sagte vor dem'), 'Churchill vor dem Unterhaus, 4. Juni 1940', (110, 1000))
    RULE(pg, t, K('Und in Bletchley Park') - 0.1, 1060)
    KICK(pg, t, K('Und in Bletchley Park'), 'BLETCHLEY PARK, ENDE MAI 1940', 1085)
    PHOTO(pg, t, K('Und in Bletchley Park'), 'bletchley', (110, 1140, 420, 270), 'Bletchley Park', fy=0.5)
    PHOTO(pg, t, K('die Funksprüche der Luftwaffe'), 'enigma', (560, 1140, 260, 340), 'Eine Enigma der Wehrmacht', fy=0.4)
    SAY(pg, t, 'Die Arbeit der polnischen Mathematiker zahlte sich aus.', (860, 1150), 38, maxw=430, accent=('polnischen', 'Mathematiker'))
    return pg

# ================= SP12: Fall Rot, Paris, Pétain, de Gaulle =================
MF = Map('mf', (PW, PH), (110, 315, 1180, 1100), -5.0, 9.0, 42.2)
def s12L(t):
    pg = base2(25, True); t0 = TS(12); m = MF
    KICK(pg, t, t0, '5. JUNI 1940'); L(pg, t, t0 + 0.1, 'Nach Süden', (110, 204), serif(70, 800))
    reg((100, 305, 1300, 1425), t0, kind='pic')
    if t >= t0:
        k = eout((t - t0) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=('reich',), outline=('reich',)); m.tint(pg, 'France', k, ACC, 0.05)
        dot(pg, m, t, t0 + 0.3, (2.35, 48.86), 'Paris', dy=-34)
        for i, (a, b) in enumerate((((1.0, 49.9), (0.3, 47.3)), ((3.1, 49.5), (2.9, 46.6)), ((4.6, 49.5), (5.0, 46.8)))):
            arrow(pg, m, t, K('zweite Phase der Offensive,', 1) + 0.3 * i, [a, b], dur=1.1, wd=14)
        m.label(pg, t, K('Am 10. Juni erklärte', 3), 'ITALIEN', (8.0, 44.3), sans(30, 800), ACC, sw=5); m.hatch(pg, 'Italy', clamp((t - K('Am 10. Juni erklärte', 3)) / 0.8))
        dot(pg, m, t, K('wich nach Bordeaux aus.', 2), (-0.58, 44.84), 'Bordeaux', dy=34)
    return pg
def s12R(t):
    pg = base2(26, False)
    FILM(pg, t, K('Millionen Franzosen flohen vor'), 'refugees', (110, 200, 560, 380), 'Flüchtlinge auf der Straße, Juni 1940')
    SAY(pg, t, 'Millionen Franzosen flohen vor der Front nach Süden, die Straßen waren verstopft.', (720, 210), 38, maxw=570, accent=('Millionen',))
    PHOTO(pg, t, K('am 14. Juni marschierten'), 'paris_parade', (110, 680, 560, 360), 'Deutsche Truppen in Paris, Juni 1940', fy=0.4)
    SAY(pg, t, 'Paris wurde zur offenen Stadt erklärt, und am 14. Juni marschierten deutsche Truppen ein.', (720, 690), 38, maxw=570, accent=('Paris',))
    RULE(pg, t, K('Reynaud trat zurück.') - 0.1, 1140)
    PHOTO(pg, t, K('Marschall Philippe Pétain,', 0), 'petain', (110, 1170, 330, 380), 'Philippe Pétain, 1940', fy=0.3)
    L(pg, t, K('bat am 17. Juni', 0), '17. Juni', (470, 1180), serif(56, 800), ACC); L(pg, t, K('um Waffenstillstand.', 1), 'Bitte um Waffenstillstand', (470, 1260), serif(34, 400))
    PHOTO(pg, t, K('Charles de Gaulle rief'), 'degaulle_bbc', (870, 1170, 420, 290), 'De Gaulle bei der BBC', fy=0.3)
    L(pg, t, K('Am nächsten Tag sprach'), '18. Juni', (470, 1350), serif(56, 800), (60, 110, 180)); L(pg, t, K('den Kampf fortzusetzen.', 1), 'Weiterkämpfen', (470, 1430), serif(34, 400))
    return pg

# ================= SP13: Compiègne =================
MV = Map('mv', (PW, PH), (110, 300, 700, 650), -5.0, 9.0, 42.2)
VICHY = [(6.0, 46.2), (5.49, 47.09), (4.85, 46.78), (4.12, 46.45), (3.33, 46.57), (2.07, 47.22), (1.0, 47.13), (0.55, 46.6), (0.16, 45.65), (-0.24, 44.92), (-0.5, 43.89), (-0.77, 43.49), (-1.24, 43.16),
         (3.2, 42.3), (7.7, 43.7), (7.2, 45.9)]
def s13L(t):
    pg = base2(27, True); t0 = TS(13)
    t0 = K('im November 1918 der') + 0.1; KICK(pg, t, t0, 'COMPIÈGNE, 21. UND 22. JUNI 1940'); L(pg, t, t0 + 0.1, 'Derselbe Wagen', (110, 204), serif(70, 800))
    FILM(pg, t, TF(13) - 1.0, 'wagon', (110, 312, 1180, 590), 'Der Salonwagen von 1918 auf der Lichtung von Compiègne')
    L(pg, t, K('im November 1918 der', 1), 'November 1918', (110, 990), serif(64, 800), GREY); L(pg, t, K('Am 22. Juni 1940'), 'Juni 1940', (700, 990), serif(64, 800), ACC)
    PHOTO(pg, t, K('Er setzte sich auf'), 'comp_hitler', (110, 1110, 560, 400), 'Hitler und seine Begleitung vor dem Wagen', fy=0.4)
    SAY(pg, t, 'Er setzte sich auf den Platz, auf dem damals Marschall Foch gesessen hatte.', (720, 1120), 40, maxw=570, accent=('Foch',))
    return pg
def s13R(t):
    pg = base2(28, False); m = MV
    PHOTO(pg, t, K('unterschrieb die französische Delegation.', 0), 'huntziger', (110, 200, 560, 380), 'Huntziger unterschreibt', fy=0.4)
    PHOTO(pg, t, K('unterschrieb die französische Delegation.', 2), 'comp_keitel', (720, 200, 570, 380), 'Keitel, die Bedingungen', fy=0.4)
    t1 = K('Frankreich wurde geteilt:'); reg((100, 690, 830, 1320), t1, kind='pic')
    if t >= t1:
        k = eout((t - t1) / 0.8); m.box = (110, 700, 700, 610); m.frame(pg, k); m.base_layer(pg, k, fill=(), outline=())
        fr = m.mask('France'); vm = polymask(m, VICHY); occ = ImageChops.subtract(fr, vm); vi = ImageChops.multiply(fr, vm)
        hatch_mask(pg, m, occ, clamp((t - K('und die Atlantikküste wurden', 2)) / 0.9)); stamp_ink(pg, vi.point(lambda v: int(v * 0.08 * k)), (0, 0), (60, 110, 180))
        m.label(pg, t, K('und die Atlantikküste wurden', 2), 'BESETZT', (1.5, 48.8), sans(30, 800), ACC, sw=5)
        m.label(pg, t, K('von Vichy aus.', 1), 'VICHY', (3.6, 45.3), sans(30, 800), (60, 110, 180), sw=5)
    L(pg, t, K('Fast zwei Millionen französische', 1), 'fast 2 Mio.', (860, 700), serif(90, 800), ACC); L(pg, t, K('in Gefangenschaft,', 1), 'Kriegsgefangene', (860, 815), serif(44, 400))
    PHOTO(pg, t, K('die meisten blieben jahrelang'), 'pows_column', (860, 890, 430, 280), 'Gefangene alliierte Soldaten', fy=0.5)
    COUNT(pg, t, K('rund 27.000 Tote.', 1), 0.9, 27000, (860, 1260), serif(70, 800), lambda v: 'rund ' + de(v), TXT); L(pg, t, K('rund 27.000 Tote.', 2), 'deutsche Tote', (860, 1350), serif(40, 400))
    SAY(pg, t, 'Der Wagen wurde nach Berlin gebracht und ausgestellt.', (110, 1470), 44)
    return pg

# ================= SP14: Paris, the bells, the end =================
def s14L(t):
    pg = base2(29, True); t0 = TS(14)
    KICK(pg, t, t0, 'PARIS, 23. JUNI 1940')
    PHOTO(pg, t, t0 + 0.2, 'hitler_eiffel', (110, 260, 600, 830), 'Hitler vor dem Eiffelturm, 23. Juni 1940', fy=0.4, zoom=0.05)
    for i, (nm, ph_) in enumerate((('Oper', 'zur Oper,'), ('Eiffelturm', 'zum Eiffelturm und'), ('Grab Napoleons', 'Grab Napoleons.'))):
        ROUTE(pg, t, [('Oper', K('zur Oper,', 1)), ('Eiffelturm', K('zum Eiffelturm und', 1)), ('Grab Napoleons', K('Grab Napoleons.', 1))], 780, 320, 100, 46) if i == 0 else None
    SAY(pg, t, 'In Deutschland ließ das Regime eine Woche lang die Glocken läuten.', (110, 1180), 46, accent=('Glocken',))
    return pg
def s14R(t):
    pg = base2(30, False); t0 = K('In nur sechs Wochen')
    L(pg, t, K('In nur sechs Wochen', 2), '6 Wochen', (110, 220), serif(130, 800), ACC); L(pg, t, K('in vier Jahren nicht', 1), '4 Jahre', (780, 220), serif(130, 800), GREY)
    NOTE(pg, t, K('in vier Jahren nicht', 1), 'Erster Weltkrieg', (780, 390))
    PHOTO(pg, t, K('Doch ein Gegner blieb.'), 'dunkirk_dover', (110, 480, 1180, 560), 'Zurückgekehrte Soldaten in einem englischen Hafen, 1940', fy=0.45)
    SAY(pg, t, 'Großbritannien lehnte jedes Friedensangebot ab.', (110, 1150), 48, wg=800, accent=('Großbritannien',))
    SAY(pg, t, 'Über den Ärmelkanal hinweg konnte das Heer nicht angreifen.', (110, 1290), 42)
    SAY(pg, t, 'Nun sollte die Luftwaffe den Weg freikämpfen.', (110, 1420), 58, wg=800, accent=('Luftwaffe',))
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
    KICK(pg, t, t0, 'FORTSETZUNG FOLGT'); L(pg, t, t0 + 0.2, 'TEIL 4', (100, 250), serif(230, 900)); L(pg, t, t0 + 0.5, 'Die Luftschlacht um England', (110, 530), serif(76, 400), GREY)
    FILM(pg, t, t0 + 0.8, 'sea', (110, 680, 1180, 720))
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
    L(pg, t, CLICKS[2] + 0.6, 'damit du Teil 4 nicht verpasst.', (110, 1440), serif(56, 400), GREY)
    return pg

SPREADS = [(s0L, s0R), (s1L, s1R), (s2L, s2R), (s3L, s3R), (s4L, s4R), (s5L, s5R), (s6L, s6R), (s7L, s7R), (s8L, s8R), (s9L, s9R), (s10L, s10R),
           (s11L, s11R), (s12L, s12R), (s13L, s13R), (s14L, s14R), (s15L, s15R)]
# films that fill the frame: (spread, side, box, from, to, caption 1, caption 2)
FILLS = [(0, 'L', B0, 0.0, K('mehr Panzer als die') - 1.0, 'Westfeldzug, Mai 1940', 'Deutsche Panzer beim Vormarsch'),
         (7, 'L', B7, TF(7), K('Rund 850 Menschen') - 1.3, 'Rotterdam, Mai 1940', 'Die zerstörte Innenstadt'),
         (8, 'L', (110, 312, 1180, 590), TF(8), K('Über enge Waldstraßen') - 1.3, 'Ardennen, Mai 1940', 'Deutsche Kolonnen auf dem Weg nach Westen'),
         (11, 'L', B11, TF(11), K('und holten Soldaten von') - 1.0, 'Dünkirchen, Mai 1940', 'Britische Schiffe unter Beschuss'),
         (13, 'L', (110, 312, 1180, 590), TF(13), K('im November 1918 der') - 1.0, 'Compiègne, 21. Juni 1940', 'Der Salonwagen von 1918 steht wieder auf der Lichtung')]
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
