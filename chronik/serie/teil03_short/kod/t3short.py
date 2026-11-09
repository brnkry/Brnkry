# Teil 3 as a 30 s Short (9:16) in the magazine style of the long video: the same pages, maps, counters, photos and page turns,
# the camera framing one page at a time in portrait. New narration (Robert Ranger, [quickly reads]), words.json +1 s.
from t2core import *
from t2core import _shadow
from lmap import Map
from drawings import tank_m
TD = Book.TD
GR = (120, 120, 124)
def base2(n, left): return base(n, left).copy()
def arrow(pg, m, t, t0, pts, dur=1.0, wd=16, col=ACC):
    if t < t0: return
    u = eio((t - t0) / dur); Q = [m.mp(*p) for p in pts]; segs = list(zip(Q, Q[1:])); Ln = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs)
    todo = u * Ln; d = ImageDraw.Draw(pg); E = Q[0]; ang = 0
    for a, b in segs:
        l = math.hypot(b[0] - a[0], b[1] - a[1]); v = min(1, todo / l); E = (lerp(a[0], b[0], v), lerp(a[1], b[1], v)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
        d.line((a, E), fill=col, width=wd); todo -= l
        if todo <= 0: break
    hd = 46; d.polygon([(E[0] + 18 * math.cos(ang), E[1] + 18 * math.sin(ang)), (E[0] - hd * math.cos(ang - 0.6), E[1] - hd * math.sin(ang - 0.6)), (E[0] - hd * math.cos(ang + 0.6), E[1] - hd * math.sin(ang + 0.6))], fill=col)
def west_map(pg, t, t0, m, tint=()):
    k = eout((t - t0) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=('reich',), outline=('reich',))
    for n in tint: m.tint(pg, n, k, ACC, 0.06)
def dot(pg, m, t, t0, ll, name, dx=0, dy=-34, size=28, col=TXT):
    m.pin(pg, t, t0, ll, col, 9); m.label(pg, t, t0 + 0.1, name, (ll[0], ll[1]), sans(size, 700), col, sw=5, dy=dy, dx=dx)
def KICK(pg, t, t0, s, y=165): L(pg, t, t0, s, (110, y), sans(34, 800), ACC)

TURNS = [K('Der Grund war') - 1.05, K('Am 13. Mai erreichten') - 1.05, K('Die ganze Geschichte') - 1.05]
VLAST = VEND
T_END = VLAST + 2.2

# ===== SP0: hook =====
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
    SAY(pg, t, 'Im Mai 1940 hatte Frankreich', (110, 1400), 60)
    SAY(pg, t, 'mehr Panzer als die Wehrmacht', (110, 1480), 60, wg=800, accent=('Panzer',))
    return pg
def s0R(t):
    pg = base2(2, False); tc = K('mehr Panzer als die', 1)
    KICK(pg, t, tc - 0.3, 'PANZER IM MAI 1940')
    COUNT(pg, t, tc - 0.2, 0.9, 3384, (110, 250), serif(120, 800), lambda v: de(v), ACC); L(pg, t, tc - 0.1, 'Frankreich', (560, 292), serif(60, 400))
    COUNT(pg, t, K('als die Wehrmacht', 2), 0.9, 2445, (110, 410), serif(120, 800), lambda v: de(v), TXT); L(pg, t, K('als die Wehrmacht', 2), 'Wehrmacht', (560, 452), serif(60, 400))
    PHOTO(pg, t, K('die stärkste Festungslinie'), 'maginot_dome', (110, 620, 560, 400), 'Panzerkuppel der Maginot-Linie', fy=0.45)
    SAY(pg, t, 'und die stärkste Festungslinie Europas.', (730, 640), 50, maxw=560, accent=('Festungslinie',))
    RULE(pg, t, K('Trotzdem stand die') - 0.1, 1100)
    SAY(pg, t, 'Trotzdem stand die deutsche Armee nur sechs Wochen später in Paris.', (110, 1130), 50, accent=('sechs', 'Wochen', 'Paris.'))
    PHOTO(pg, t, K('später in Paris.'), 'paris_parade', (110, 1290, 560, 270), 'Paris, Juni 1940', fy=0.5)
    L(pg, t, K('nur sechs Wochen', 1), '6 Wochen', (730, 1300), serif(110, 800), ACC)
    return pg

# ===== SP1: the plan, the Ardennes =====
MA = Map('ma', (PW, PH), (110, 640, 1180, 900), -1.0, 11.0, 47.2)
def s1L(t):
    pg = base2(3, True); t0 = K('Der Grund war')
    KICK(pg, t, t0, 'DER PLAN')
    PHOTO(pg, t, t0 + 0.1, 'manstein', (110, 230, 520, 680), 'Erich von Manstein', fy=0.25, zoom=0.05)
    SAY(pg, t, 'Der Grund war ein Plan, den fast niemand für möglich hielt.', (700, 250), 66, maxw=590, wg=400, accent=('Plan,',))
    L(pg, t, K('für möglich hielt', 2), 'Mansteins Entwurf', (700, 820), italic(40), GREY)
    return pg
def s1R(t):
    pg = base2(4, False); m = MA; t1 = K('Die Panzer fuhren nicht')
    SAY(pg, t, 'Die Panzer fuhren nicht durch Belgien, sondern durch die Ardennen.', (110, 230), 58, accent=('Ardennen.',))
    reg((100, 630, 1300, 1550), t1, kind='pic')
    if t >= t1:
        west_map(pg, t, t1, m, tint=('France',))
        m.label(pg, t, t1 + 0.3, 'FRANKREICH', (2.0, 48.2), sans(38, 800), TXT); m.label(pg, t, t1 + 0.3, 'BELGIEN', (4.6, 50.45), sans(26, 800), GREY, sw=4)
        arrow(pg, m, t, t1 + 0.3, [(6.8, 51.3), (5.0, 51.0), (3.7, 50.7)], col=GR)
        STRIKE(pg, t, K('nicht durch Belgien', 2) + 0.2, *[int(v) for v in (m.mp(4.2, 51.3)[0], m.mp(6.2, 51.3)[0], m.mp(5.2, 51.15)[1])], 9)
        ta = K('sondern durch die Ardennen', 3)
        m.label(pg, t, ta, 'ARDENNEN', (6.1, 50.25), sans(34, 800), ACC, sw=5)
        arrow(pg, m, t, ta + 0.1, [(7.2, 50.1), (5.8, 49.85), (4.9, 49.7), (3.3, 49.9), (1.9, 50.1)], dur=1.8)
    DRAW(pg, t, K('dicht bewaldetes Mittelgebirge', 2), 0.9, lambda ph: tank_m(1120, 1580, 0.3, ph), (980, 1510, 1260, 1640))
    return pg

# ===== SP2: Sedan, the Channel; the railway carriage =====
MC = Map('mc', (PW, PH), (110, 640, 1180, 820), -0.5, 7.0, 48.6)
def s2L(t):
    pg = base2(5, True); t0 = K('Am 13. Mai erreichten')
    KICK(pg, t, t0, 'MAI 1940'); L(pg, t, t0, '13. Mai', (110, 210), serif(120, 800), ACC)
    SAY(pg, t, 'erreichten sie die Maas bei Sedan,', (110, 380), 54, accent=('Sedan,',))
    SAY(pg, t, 'eine Woche später den Ärmelkanal.', (110, 470), 54, accent=('Ärmelkanal.',))
    m = MC; t1 = K('die Maas bei Sedan'); reg((100, 630, 1300, 1470), t1, kind='pic')
    if t >= t1:
        k = eout((t - t1) / 0.8); m.frame(pg, k); m.base_layer(pg, k, fill=('reich',), outline=('reich',)); m.tint(pg, 'France', k, ACC, 0.05)
        dot(pg, m, t, t1 + 0.2, (2.35, 48.86), 'Paris', dy=-30); dot(pg, m, t, K('die Maas bei Sedan', 3), (4.94, 49.70), 'Sedan', dy=36)
        arrow(pg, m, t, K('eine Woche später'), [(4.85, 49.75), (3.8, 49.9), (2.6, 50.05), (1.95, 50.1)], dur=1.5)
        dot(pg, m, t, K('den Ärmelkanal.', 1), (1.83, 50.10), 'Abbeville', dy=-34)
        m.label(pg, t, K('den Ärmelkanal.', 1), 'Ärmelkanal', (0.6, 50.6), italic(36), GREY, sw=4)
    return pg
def s2R(t):
    pg = base2(6, False); t0 = K('Den Waffenstillstand ließ')
    KICK(pg, t, t0, 'COMPIÈGNE, 22. JUNI 1940'); L(pg, t, t0, 'Derselbe Wagen', (110, 210), serif(84, 800))
    FILM(pg, t, t0, 'wagon', (110, 340, 1180, 560), 'Der Salonwagen von 1918')
    SAY(pg, t, 'Den Waffenstillstand ließ Hitler im selben Eisenbahnwagen unterschreiben wie 1918.', (110, 990), 50, accent=('Hitler', 'Eisenbahnwagen'))
    PHOTO(pg, t, K('ließ Hitler im', 1), 'salonwagen_c', (110, 1200, 560, 380), 'Hitler vor dem Wagen, Juni 1940', fy=0.35)
    L(pg, t, K('im selben Eisenbahnwagen', 2), '1918', (730, 1230), serif(120, 800), GREY); L(pg, t, K('wie 1918.', 1), '1940', (730, 1390), serif(120, 800), ACC)
    return pg

# ===== SP3: the call to watch the whole film =====
def s3L(t):
    pg = base2(7, True); t0 = K('Die ganze Geschichte')
    KICK(pg, t, t0, 'JETZT AUF DEM KANAL')
    L(pg, t, t0, 'TEIL 3', (100, 220), serif(230, 900)); L(pg, t, t0 + 0.2, 'Der Krieg im Westen', (110, 500), serif(80, 400), GREY)
    PHOTO(pg, t, t0 + 0.3, 'eiffel_c', (110, 640, 1180, 760), 'Paris, 23. Juni 1940', fy=0.75)
    SAY(pg, t, 'Die ganze Geschichte jetzt auf dem Kanal.', (110, 1490), 54, wg=800, accent=('Kanal.',))
    return pg
def s3R(t): return base2(8, False)

SPREADS = [(s0L, s0R), (s1L, s1R), (s2L, s2R), (s3L, s3R)]
FILLS = []
REC[0] = True
for i, (Lf, Rf) in enumerate(SPREADS):
    for side, fn in (('L', Lf), ('R', Rf)): CUR[0], CUR[1] = i, side; fn(1e5)
REC[0] = False
# portrait camera: a page fits the frame almost exactly, so the camera frames the whole page the voice is on and pushes in slowly
SP_ = 0.80
OVP = (PW, PH / 2, 0.36)
CAMS = [(0.0, PW / 2, PH / 2 + 30, SP_)]   # v2: no full-frame film at the start, the page is seen from the first frame
for i in range(len(SPREADS)):
    a = 0.0 if i == 0 else TURNS[i - 1] + TD; b = TURNS[i] if i < len(TURNS) else T_END
    for side, cx in (('L', PW / 2), ('R', PW * 1.5)):
        ts_ = [e['t0'] for e in REG if e['sp'] == i and e['side'] == side and e['t0'] > 0.5 and e['kind'] != 'mark']
        if not ts_: continue
        t0 = max(a, min(ts_) - 0.45) if not (i == 0 and side == 'L') else 0.0
        CAMS.append((t0, cx, PH / 2 + 30, SP_, 0.6))
    if i < len(TURNS): CAMS.append((TURNS[i],) + OVP + (0.5,))
CAMS.sort(key=lambda c: c[0])
MAG = Book(SPREADS, TURNS, CAMS, spine=100)
def frame(t):
    img = MAG(t)
    for f in FILLS:
        c0 = f[3] + 0.35
        if c0 <= t <= f[4] + 0.15: caption(img, t, c0, f[5], f[6], f[4] + 0.15)
    return img

if __name__ == '__main__':
    if sys.argv[1] == 'check':
        FG = [(f[0], f[3] - 1.1, f[4] + 0.3, (f[2][0] + (PW if f[1] == 'R' else 0), f[2][1], f[2][0] + f[2][2] + (PW if f[1] == 'R' else 0), f[2][1] + f[2][3])) for f in FILLS]
        bad = check(MAG, T_END, fills=FG)
        for b in bad:
            e = b[1]; print(b[0], 'sp%d%s' % (e['sp'], e['side']), e['box'], '%.2f-%.2f' % (e['t0'], e['t1']), e['kind'], ('<-> %s' % (b[2]['box'],)) if len(b) > 2 else '')
        print(len(bad), 'problems', 'T_END %.2f' % T_END); sys.exit()
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); Pc = Image.new('RGB', (6 * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            im = frame(t); ImageDraw.Draw(im).text((20, 20), '%.1f' % t, font=sans(60, 800), fill=(255, 0, 255)); Pc.paste(im.resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        Pc.save(LB + 'chk/' + sys.argv[2], quality=86); sys.exit()
    if sys.argv[1] == 'T': print(round(T_END, 3)); sys.exit()
    if sys.argv[1] == 'turns': print(' '.join('%.2f' % x for x in TURNS)); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
        if n % 150 == 0: print('t', n / FPS, flush=True)
    p.stdin.close(); p.wait(); print('rc', p.returncode)
