# Lauri Törni, vertical 9:16 version of the long video: same voice and timing, layouts rebuilt for 1080x1920,
# text kept clear of the top bar, the right-hand buttons and the caption area; ends after "Schreibt es in die Kommentare."
import sys, subprocess
from lib9 import *
from lib9 import _bg

LADOGA = [(30.85, 61.63), (30.45, 61.42), (30.05, 61.05), (29.98, 60.75), (30.45, 60.42), (31.0, 60.08), (31.6, 59.95), (32.4, 60.1), (32.85, 60.5),
          (32.75, 60.9), (32.4, 61.15), (31.9, 61.4), (31.4, 61.62)]
CEDED = [(27.75, 60.52), (28.6, 61.0), (29.3, 61.3), (29.9, 61.55), (30.5, 61.95), (30.75, 62.25), (31.1, 62.55), (31.4, 62.95), (31.9, 63.05), (32.9, 62.55),
         (32.95, 61.85), (32.4, 61.15), (31.9, 61.3), (30.95, 60.55), (30.0, 60.15), (29.4, 60.2), (28.6, 60.45)]
VIIPURI = (28.75, 60.71); LEMETTI = (31.62, 61.78)
KAR = Map(31.4, 61.78, 5.0, hi=('Finland',), extra=((LADOGA, SEA),))
KAR2 = Map(29.8, 61.75, 9.0, hi=('Finland',), extra=((LADOGA, SEA),))
VN = Map(107.6, 15.75, 3.6, hi=('Vietnam',))
EU = Map(18.5, 57.0, 30.0, hi=('Finland',), extra=((LADOGA, SEA),))
EUW = Map(20.5, 54.0, 36.0, hi=('Finland', 'Austria'), extra=((LADOGA, SEA),))
ATL = Map(-30.0, 40.0, 140.0, hi=('United States of America',))
IRN = Map(31.0, 39.5, 60.0, hi=('Iran',))
_OLD = [a for _, a, _ in json.load(open(B + 'words_all.json'))]; _NEW = [a for _, a, _ in WORDS]
def M(t): return float(np.interp(t, _OLD, _NEW))
def w(s, after=0.0): return wt(s, M(after) if after else 0.0)
def fitpt(n, t, w0, w1, z1, sx, sy):
    """screen position of a source pixel inside fit() (portrait panel, zoom about the centre)"""
    im = src(n); u = clamp((t - w0) / (w1 - w0)); z = lerp(1.0, z1, u); pw = im.width * H / im.height
    cw, ch = im.width / z, im.height / z; x0 = (W - pw) / 2
    return (x0 + (sx - (im.width / 2 - cw / 2)) * pw / cw, (sy - (im.height / 2 - ch / 2)) * H / ch)
def point_at(can, t, t0, tip, lab):
    """yellow arrow from free space below to a person, short name label under its tail"""
    side = -1 if tip[0] > CX else 1
    tail = (min(860, max(200, tip[0] + side * 230)), tip[1] + 300)
    arrow(can, tail, (tip[0] + side * 20, tip[1] + 60), eio((t - t0) / 0.6), YEL, 14, 44)
    label(can, t, t0 + 0.4, tail[0], tail[1] + 50, lab, 64, YEL, 'mm')
INK_ = (40, 32, 24)
_rr = np.random.default_rng(9)
_n = Image.fromarray((_rr.normal(128, 30, (H // 6, W // 6))).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(4))
_yy, _xx = np.mgrid[0:H, 0:W]; _rad = np.sqrt(((_xx - W / 2) / (W * 0.6)) ** 2 + ((_yy - H / 2) / (H * 0.6)) ** 2)
_a = np.ones((H, W, 3)) * np.array(DARK, float) * (1 + 0.9 * np.clip(1 - _rad, 0, 1))[..., None] * (0.92 + 0.08 * np.asarray(_n)[..., None] / 128)
PLAIN = Image.fromarray(_a.clip(0, 255).astype(np.uint8)).convert('RGBA')
def plain(): return PLAIN.copy()
def line_draw(can, t, t0, pts, col=YEL, wd=6, dur=0.8):
    if t < t0: return
    k = eio((t - t0) / dur); tot = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)); goal = tot * k; acc = 0; out = [pts[0]]
    for i in range(len(pts) - 1):
        L_ = math.dist(pts[i], pts[i + 1])
        if acc + L_ >= goal: f = (goal - acc) / L_ if L_ else 0; out.append((lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f))); break
        out.append(pts[i + 1]); acc += L_
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).line(out, fill=col + (255,), width=wd, joint='curve'); can.alpha_composite(L)
def sh(can, a=220, start=0.5): return shade(can, a, start)

# ================= intro =================
def s_date(t, w0, w1):
    can = sh(dim(pan('t16', t, w0, w1, -1, 0.55), 50))
    typewriter(can, t, 0.25, (CX, Y2), '18. OKTOBER 1965', typew(80), CREAM, 0.075)
    return can
def s_heli(t, w0, w1):
    z = lerp(1.0, 1.12, clamp((t - w0) / (w1 - w0))); can = VN.frame(z)
    kd, dn, laos, crash = VN.p(107.80, 15.45, z), VN.p(108.22, 16.07, z), VN.p(107.0, 15.62, z), VN.p(107.93, 15.78, z)
    dot(can, *dn, WHITE, 10); label(can, t, w0 + 0.2, dn[0] + 26, dn[1] - 4, 'DA NANG', 58)
    dot(can, *kd, YEL, 12); label(can, t, w0 + 0.3, kd[0] + 28, kd[1] + 6, 'KHAM DUC', 58, YEL)
    label(can, t, w0 + 0.3, laos[0] - 30, laos[1] - 120, 'LAOS', 86, GREY, 'rm')
    dashed(can, [kd, laos], eio((t - w0 - 0.2) / 1.6))
    label(can, t, w('Vietnams'), CX, Y2, 'VIETNAM', 96, YEL, 'mm')
    ring(can, t, w('Hubschrauber') - 0.2, *crash)
    label(can, t, w('Hubschrauber') + 0.2, crash[0] + 40, crash[1] - 150, 'VERSCHOLLEN', 72, RED, 'mm'); return can
def s_thorne(t, w0, w1):
    can = sh(fit('t18', t, w0, w1, 1.04), 230, 0.45)
    txt(can, t, w('Hauptmann'), (CX, Y1), 'HAUPTMANN DER US SPECIAL FORCES', bebas(66), CREAM)
    words(can, t, [('LARRY', WHITE, w('Larry')), ('THORNE', YEL, w('Thorne'))], Y2 + 20, 130); return can
def s_years(t, w0, w1):
    can = dim(pan('t10', t, w0, w1, 1), 165).filter(ImageFilter.GaussianBlur(2))
    counter(can, t, w('34'), 1965, 1999, (CX, 820), 280, WHITE, 1.4, '{}')
    txt(can, t, w('Jahre', 11), (CX, 1040), '34 JAHRE SPÄTER', anton(96), YEL)
    txt(can, t, w('Absturzstelle'), (CX, 1160), 'DIE ABSTURZSTELLE WIRD GEFUNDEN', bebas(66), CREAM); return can
def triptych(t, items, title=None):
    """three photos stacked as bands, out of focus until each one is named"""
    can = Image.new('RGBA', (W, H), DARK + (255,)); top, bh = 500, 340
    for i, (n, lab, ts) in enumerate(items):
        im = src(n); z = lerp(1.0, 1.04, clamp((t - items[0][2] + 2) / 12)); cw = min(im.width, im.height * W / bh) / z; ch = cw * bh / W
        cy = min(max(im.height * 0.33, ch / 2), im.height - ch / 2)
        ph = im.resize((W, bh), Image.BICUBIC, box=(im.width / 2 - cw / 2, cy - ch / 2, im.width / 2 + cw / 2, cy + ch / 2)).convert('RGBA')
        k = eio((t - ts + 0.15) / 0.8); r = 18 * (1 - k)
        if r > 0.3: ph = ph.filter(ImageFilter.GaussianBlur(r))
        ph.alpha_composite(Image.new('RGBA', ph.size, (6, 7, 9, int(150 * (1 - k)))))
        can.alpha_composite(ph, (0, top + i * bh))
        if i: ImageDraw.Draw(can).line((0, top + i * bh, W, top + i * bh), fill=DARK, width=8)
    for i, (n, lab, ts) in enumerate(items): txt(can, t, ts - 0.05, (CX, top + i * bh + bh - 50), lab, anton(66), YEL if i != 1 else WHITE)
    if title: words(can, t, title, 400, 96)
    return can
def s_three(t, w0, w1):
    return triptych(t, [('t06', 'FINNLAND', w('Finnland', 19)), ('t22', 'WAFFEN-SS', w('Waffen-SS,', 19)), ('t21', 'US ARMY', w('Army.', 19))],
                    [('DREI', WHITE, w('drei', 17)), ('UNIFORMEN', YEL, w('Uniformen'))])
def s_name(t, w0, w1):
    can = sh(pan('t09', t, w0, w1, -1, 0.42, 1.1), 230, 0.45)
    txt(can, t, w('Heimat'), (CX, Y1), 'IN SEINER HEIMAT HIESS ER', bebas(66), CREAM)
    words(can, t, [('LAURI', WHITE, w('Lauri', 30)), ('TÖRNI', YEL, w('Törni', 31))], Y2 + 20, 150); return can

# ================= chapter 1 =================
def s_born(t, w0, w1):
    can = plain()
    chapter(can, t, w0 + 0.3, 1, 'VIIPURI UND DER WINTERKRIEG', w0 + 3.3)
    doc(can, t, w('Lauri', 33) + 0.6, [('GEBURTSREGISTER', 46, INK_), ('LAURI ALLAN TÖRNI', 58, INK_), ('28. MAI 1919', 52, (150, 30, 30)), ('VIIPURI, KARELIEN', 44, INK_)], CX, 960, 820)
    return can
def s_viipuri(t, w0, w1):
    z = lerp(1.0, 1.15, eio((t - w0) / (w1 - w0))); can = KAR2.frame(z)
    vx, vy = KAR2.p(*VIIPURI, z); ced = [KAR2.p(*q, z) for q in CEDED]; k = eio((t - w('heute') - 0.1) / 0.9)
    poly_fill(can, ced, YEL, 90 * (1 - k)); poly_fill(can, ced, RED, 150 * k)
    ImageDraw.Draw(can).polygon([KAR2.p(*q, z) for q in LADOGA], fill=SEA, outline=BORDER)
    dot(can, vx, vy, YEL, 12)
    if t < w('Wyborg'): label(can, t, w0 + 0.2, vx - 34, vy - 6, 'VIIPURI', 64, YEL, 'rm', w('Wyborg') - 0.2)
    label(can, t, w('Wyborg'), vx - 34, vy - 6, 'WYBORG', 64, CREAM, 'rm')
    label(can, t, w0 + 0.4, *KAR2.p(27.0, 63.0, z), 'FINNLAND', 76, CREAM, 'mm')
    label(can, t, w('Russland') - 0.1, *KAR2.p(32.6, 63.6, z), 'RUSSLAND', 76, GREY, 'mm')
    txt(can, t, w('Damals'), (CX, YT), 'DAMALS FINNLAND', anton(76), YEL, w('heute'))
    txt(can, t, w('heute') + 0.1, (CX, YT), 'HEUTE RUSSLAND', anton(76), RED); return can
def s_1938(t, w0, w1):
    can = sh(fit('t23', t, w0, w1, 1.05))
    txt(can, t, w('1938'), (CX, Y1 + 20), '1938', anton(170), YEL)
    txt(can, t, w('Wehrdienst'), (CX, Y3), 'WEHRDIENST', bebas(80), WHITE); return can
def s_attack(t, w0, w1):
    can = sh(pan('t25', t, w0, w1, 1, 0.5, 1.05))
    typewriter(can, t, w('November', 50), (CX, Y1), 'NOVEMBER 1939', typew(80), CREAM, 0.07)
    txt(can, t, w('griff') - 0.05, (CX, Y2 + 20), 'DIE SOWJETUNION GREIFT AN', anton(84), YEL); return can
def s_winter(t, w0, w1):
    can = sh(fit('t04', t, w0, w1, 1.05), 220, 0.55)
    txt(can, t, w('Winterkrieg') + 0.1, (CX, Y2), 'WINTERKRIEG 1939/40', anton(96), WHITE)
    txt(can, t, w('Ladogasees') - 0.2, (CX, Y3), 'NÖRDLICH DES LADOGASEES', bebas(66), YEL); return can
def s_motti(t, w0, w1):
    z = lerp(1.0, 1.15, eio((t - w0) / (w1 - w0))); can = KAR.frame(z)
    lx, ly = KAR.p(*LEMETTI, z); label(can, t, w0 + 0.2, *KAR.p(31.7, 61.1, z), 'LADOGASEE', 60, GREY, 'mm')
    k = eout((t - w('Lemetti') + 0.1) / 0.5)
    if k > 0:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for i in range(5): d.rounded_rectangle((lx - 120 + i * 50, ly - 18, lx - 85 + i * 50, ly + 18), 6, fill=RED + (int(230 * k),))
        can.alpha_composite(L)
    te = w('eingekesselte') - 0.1
    for i, ang in enumerate(range(0, 360, 60)):
        a = math.radians(ang); r0, r1 = 300 * z, 165 * z
        arrow(can, (lx + r0 * math.cos(a), ly + r0 * math.sin(a)), (lx + r1 * math.cos(a), ly + r1 * math.sin(a)), eio((t - te - i * 0.08) / 0.7), YEL, 12, 36)
    if t > te + 0.8:
        kk = eio((t - te - 0.8) / 0.8); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); r = 150 * z
        ImageDraw.Draw(L).arc((lx - r, ly - r, lx + r, ly + r), -90, -90 + 360 * kk, fill=YEL + (255,), width=10); can.alpha_composite(L)
    label(can, t, w('Lemetti'), lx, ly - 360 * z, 'LEMETTI', 80, YEL, 'mm')
    txt(can, t, w('zerschlugen') - 0.2, (CX, Y3), 'EINGEKESSELT UND ZERSCHLAGEN', anton(76), WHITE); return can
def s_lt(t, w0, w1):
    can = sh(pan('t03', t, w0, w1, -1, 0.45, 1.05))
    typewriter(can, t, w('März', 65), (CX, Y1), 'MÄRZ 1940', typew(80), CREAM, 0.08)
    txt(can, t, w('Leutnant'), (CX, Y2 + 20), 'LEUTNANT DER RESERVE', anton(90), YEL); return can
def s_lost(t, w0, w1):
    z = 1.15; can = KAR2.frame(z); ced = [KAR2.p(*q, z) for q in CEDED]; vx, vy = KAR2.p(*VIIPURI, z)
    k = eio((t - w('Teile', 70) + 0.2) / 0.9); poly_fill(can, ced, RED, 160 * k)
    ImageDraw.Draw(can).polygon([KAR2.p(*q, z) for q in LADOGA], fill=SEA, outline=BORDER)
    label(can, t, w('Kareliens', 70), *KAR2.p(32.0, 62.4, z), 'KARELIEN', 68, WHITE, 'mm')
    txt(can, t, w('abgeben') - 0.1, (CX, YT), 'AN DIE SOWJETUNION ABGETRETEN', anton(76), RED)
    if t > w('Viipuri', 75) - 0.2: ring(can, t, w('Viipuri', 75) - 0.2, vx, vy, YEL, 30, False)
    dot(can, vx, vy, YEL, 12); label(can, t, w('Viipuri', 75) - 0.1, vx - 40, vy - 6, 'VIIPURI', 68, YEL, 'rm'); return can

# ================= chapter 2 =================
HEL, VIE = (24.94, 60.17), (16.37, 48.21)
def s_wien(t, w0, w1):
    z = lerp(1.0, 1.06, clamp((t - w0) / (w1 - w0))); can = EUW.frame(z)
    chapter(can, t, w0 + 0.3, 2, 'WIEN UND ABTEILUNG TÖRNI', w0 + 3.3)
    hx, hy = EUW.p(*HEL, z); vx, vy = EUW.p(*VIE, z)
    if t > w0 + 0.3:
        dot(can, hx, hy, YEL, 11); label(can, t, w('Juni', 80) - 0.3, hx - 26, hy, 'HELSINKI', 58, YEL, 'rm')
        dashed(can, route([HEL, (21.5, 55.0), VIE], EUW, z), eio((t - w('reiste')) / 1.6))
        if t > w('Wien', 80): dot(can, vx, vy, WHITE, 11); label(can, t, w('Wien', 80), vx + 26, vy, 'WIEN', 68, WHITE)
        typewriter(can, t, w('Juni', 80), (300, 950), 'JUNI 1941', typew(64), CREAM, 0.07)
        txt(can, t, w('mehrwöchige'), (CX, Y3 + 10), 'MEHRWÖCHIGE AUSBILDUNG', anton(76), YEL)
    return can
def s_cont(t, w0, w1):
    can = sh(pan('t29', t, w0, w1, 1, 0.5, 1.05))
    txt(can, t, w('Noch', 88), (CX, Y1), 'ZURÜCK NACH FINNLAND', bebas(72), CREAM)
    txt(can, t, w('dort', 88), (CX, Y2 + 20), 'FORTSETZUNGSKRIEG', anton(100), YEL); return can
def s_abt(t, w0, w1):
    can = sh(pan('t08', t, w0, w1, -1, 0.42, 1.0), 230, 0.45)
    txt(can, t, w('1943'), (CX, Y1), '1943', anton(120), WHITE)
    words(can, t, [('ABTEILUNG', WHITE, w('Abteilung')), ('TÖRNI', YEL, w('Törni', 100))], Y2 + 40, 110); return can
def s_raid(t, w0, w1):        # behind the lines: Finland below, the front across, the Soviet side above
    can = plain(); fy = 1000
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line([(x, fy + 34 * math.sin(x / 90)) for x in range(40, W - 39, 8)], fill=RED + (230,), width=8); can.alpha_composite(L)
    label(can, t, w0 + 0.2, CX, 560, 'SOWJETISCHE SEITE', 62, RED, 'mm'); label(can, t, w0 + 0.2, CX, 1470, 'FINNLAND', 64, YEL, 'mm')
    label(can, t, w0 + 0.4, 880, fy + 90, 'FRONTLINIE', 50, GREY, 'rm')
    path = [(300, 1330), (340, 1150), (420, 960), (520, 840), (640, 760)]
    dashed(can, path, eio((t - w('operierten')) / 2.2), YEL, 8)
    for i, (x, y) in enumerate([(540, 850), (670, 770)]):
        if t > w('Hinterhalte') + i * 0.35:
            k = eout((t - w('Hinterhalte') - i * 0.35) / 0.3); q = 26 * k; L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            d.line((x - q, y - q, x + q, y + q), fill=YEL + (255,), width=10); d.line((x - q, y + q, x + q, y - q), fill=YEL + (255,), width=10); can.alpha_composite(L)
    if t > w('kehrten', 105): dashed(can, [(720, 800), (780, 950), (770, 1120), (720, 1290)], eio((t - w('kehrten', 105)) / 1.6), WHITE, 6)
    txt(can, t, w('weit', 103), (CX, YT), 'WEIT HINTER DEN LINIEN', anton(84), WHITE)
    txt(can, t, w('Tagen'), (760, 1370), 'NACH TAGEN ZURÜCK', bebas(52), CREAM); return can
def s_bounty(t, w0, w1):
    can = plain()
    txt(can, t, w('Berichten'), (CX, YT), 'BERICHTEN ZUFOLGE', bebas(64), CREAM)
    doc(can, t, w('Berichten') + 0.3, [('KOPFGELD', 80, (150, 30, 30)), ('LAURI TÖRNI', 56, INK_), ('', 30, INK_), ('', 30, INK_)], CX, 900, 820)
    counter(can, t, w('drei', 112) - 0.2, 0, 3000000, (CX, 1000), 100, INK_, 1.6, '{:,}', ' FMK')
    stamp(can, t, w('Finnmark') + 0.2, 'SOWJETISCHE SEITE', (CX + 60, 1250), RED, 50, -10); return can
def s_ilom(t, w0, w1):
    can = sh(fit('t19', t, w0, w1, 1.05))
    txt(can, t, w('Sommer', 115), (CX, Y1), 'SOMMER 1944', typew(80), CREAM)
    txt(can, t, w('Ilomantsi'), (CX, Y2 + 20), 'ILOMANTSI', anton(110), YEL); return can
def s_koiv(t, w0, w1):
    can = sh(fit('t28', t, w0, w1, 1.05), 230, 0.5)
    point_at(can, t, w('Mauno'), fitpt('t28', t, w0, w1, 1.05, 520, 400), 'KOIVISTO')
    txt(can, t, w('Soldaten', 123), (CX, Y1), 'UNTER SEINEM KOMMANDO', bebas(64), CREAM)
    words(can, t, [('MAUNO', WHITE, w('Mauno')), ('KOIVISTO', YEL, w('Koivisto'))], Y2, 110)
    txt(can, t, w('Präsident'), (CX, Y3 + 10), 'SPÄTER PRÄSIDENT FINNLANDS', bebas(64), WHITE); return can
def s_mhk(t, w0, w1):
    can = plain(); cx, cy, r = CX, 760, 230
    pts = [(cx - r * 0.28, cy - r), (cx + r * 0.28, cy - r), (cx + r * 0.16, cy - r * 0.16), (cx + r, cy - r * 0.28), (cx + r, cy + r * 0.28), (cx + r * 0.16, cy + r * 0.16),
           (cx + r * 0.28, cy + r), (cx - r * 0.28, cy + r), (cx - r * 0.16, cy + r * 0.16), (cx - r, cy + r * 0.28), (cx - r, cy - r * 0.28), (cx - r * 0.16, cy - r * 0.16), (cx - r * 0.28, cy - r)]
    line_draw(can, t, w('Juli') - 0.2, pts, YEL, 8, 1.4)
    if t > w('Mannerheim-Kreuz,') - 0.1:
        k = eio((t - w('Mannerheim-Kreuz,') + 0.1) / 0.6); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).polygon(pts, fill=YEL + (int(80 * k),)); can.alpha_composite(L)
        for ang in (45, 135):
            a = math.radians(ang); line_draw(can, t, w('Mannerheim-Kreuz,'), [(cx - 1.25 * r * math.cos(a), cy - 1.25 * r * math.sin(a)), (cx + 1.25 * r * math.cos(a), cy + 1.25 * r * math.sin(a))], WHITE, 7, 0.6)
    typewriter(can, t, w('Juli'), (CX, Y1 + 20), 'JULI 1944', typew(76), CREAM, 0.08)
    txt(can, t, w('Mannerheim-Kreuz,') - 0.05, (CX, Y2 + 30), 'MANNERHEIM-KREUZ', anton(110), YEL)
    txt(can, t, w('höchste'), (CX, Y3 + 30), 'FINNLANDS HÖCHSTE MILITÄRISCHE AUSZEICHNUNG', bebas(54), WHITE); return can
def s_armist(t, w0, w1):
    can = plain()
    chapter(can, t, w0 + 0.3, 3, 'VERRAT UND FLUCHT', w0 + 3.3)
    doc(can, t, w('September'), [('WAFFENSTILLSTAND', 64, INK_), ('FINNLAND / SOWJETUNION', 40, INK_), ('SEPTEMBER 1944', 46, (150, 30, 30))], CX, 960, 820)
    return can
def s_notover(t, w0, w1):
    can = plain()
    txt(can, t, w('Für', 145), (CX, 600), 'FÜR TÖRNI WAR DER KRIEG', anton(84), WHITE)
    txt(can, t, w('Krieg', 146), (CX, 760), 'VORBEI', anton(150), GREY)
    line_draw(can, t, w('nicht', 146), [(CX - 260, 780), (CX + 260, 740)], RED, 16, 0.4)
    txt(can, t, w('Gruppe'), (CX, 1020), 'EINE GEHEIME GRUPPE', bebas(76), CREAM)
    txt(can, t, w('Widerstand'), (CX, 1140), 'WIDERSTAND GEGEN EINE BESETZUNG', anton(84), YEL); return can
NEU, LUE = (13.06, 53.36), (10.69, 53.87)
def s_germ(t, w0, w1):
    z = lerp(1.0, 1.08, clamp((t - w0) / (w1 - w0))); can = EU.frame(z)
    hx, hy = EU.p(*HEL, z); nx, ny = EU.p(*NEU, z)
    dot(can, hx, hy, YEL, 11); label(can, t, w0 + 0.2, hx - 26, hy - 50, 'FINNLAND', 58, YEL, 'rm')
    dashed(can, route([HEL, (19.5, 58.0), NEU], EU, z), eio((t - w('ging', 152)) / 1.6), YEL)
    if t > w('Deutschland', 152): dot(can, nx, ny, WHITE, 11); label(can, t, w('Deutschland', 152), nx + 26, ny + 40, 'NEUSTRELITZ', 58, WHITE)
    typewriter(can, t, w('Januar'), (CX, YT), 'JANUAR 1945', typew(76), CREAM, 0.07)
    txt(can, t, w('Saboteur'), (CX, Y3 + 10), 'AUSBILDUNG ZUM SABOTEUR', anton(84), YEL); return can
def s_ss45(t, w0, w1):
    can = sh(pan('t27', t, w0, w1, 1, 0.45, 1.05))
    txt(can, t, w('Kriegswochen'), (CX, Y1), 'NORDDEUTSCHLAND 1945', bebas(72), CREAM)
    txt(can, t, w('Mai', 165), (CX, Y2 + 20), 'MAI 1945: KAPITULATION', anton(96), YEL); return can
def s_escape(t, w0, w1):
    z = lerp(1.0, 1.06, clamp((t - w0) / (w1 - w0))); can = EU.frame(z)
    lx, ly = EU.p(*LUE, z); hx, hy = EU.p(*HEL, z)
    dot(can, lx, ly, RED, 11); label(can, t, w0 + 0.2, lx - 26, ly, 'LÜBECK', 58, RED, 'rm')
    if t > w('Gefangenenlager'): stamp(can, t, w('Gefangenenlager'), 'POW', (lx + 40, ly + 170), RED, 54, -8)
    dashed(can, route([LUE, (14.0, 57.5), (18.5, 60.5), HEL], EU, z), eio((t - w('floh', 170)) / 2.4), YEL)
    if t > w('Finnland', 172): dot(can, hx, hy, YEL, 11); label(can, t, w('Finnland', 172), hx - 26, hy - 50, 'FINNLAND', 58, YEL, 'rm')
    txt(can, t, w('floh', 170), (CX, YT), 'FLUCHT AUS DEM LAGER', anton(84), WHITE); return can
def s_akte(t, w0, w1):        # police photos: the three views of the file photo, one after another, each full screen
    ts = [w('verhaftete'), w('Diese', 177), w('Aufnahmen')]; im = src('t12'); pw = im.width / 3
    i = 2 if t >= ts[2] else 1 if t >= ts[1] else 0
    def part(j):
        cw = min(pw, im.height * W / H); ch = cw * H / W; x0 = j * pw + (pw - cw) / 2
        return im.resize((W, H), Image.BICUBIC, box=(x0, (im.height - ch) / 2, x0 + cw, (im.height + ch) / 2)).convert('RGBA')
    can = part(i)
    if i > 0 and t < ts[i] + 0.35:   # the next photo slides in from the right
        k = eio((t - ts[i]) / 0.35); prev = part(i - 1); off = int(W * k)
        can = Image.new('RGBA', (W, H), DARK + (255,)); can.paste(prev, (-off, 0)); can.paste(part(i), (W - off, 0))
    sh(can, 220, 0.55)
    stamp(can, t, w('Akte') + 0.3, 'VALPO 1946', (CX + 120, 560), RED, 66, -8)
    txt(can, t, w('Staatspolizei'), (CX, Y3), 'VERHAFTET VON DER STAATSPOLIZEI', anton(70), YEL); return can
def s_verdict(t, w0, w1):
    can = plain()
    doc(can, t, w('Wegen', 180) - 0.2, [('URTEIL', 70, INK_), ('LANDESVERRAT', 52, INK_), ('6 JAHRE HAFT', 60, (150, 30, 30))], CX, 860, 780)
    stamp(can, t, w('verurteilt') + 0.2, 'VERURTEILT', (CX + 80, 1190), RED, 70, -12)
    return can
def s_prison(t, w0, w1):
    can = plain()
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    op = eio((t - w('Zweimal')) / 0.8) * (1 - eio((t - w('zweimal', 188)) / 0.6))
    for i in range(6):
        x = 90 + i * 180 + (op * 70 if i % 2 else -op * 70); d.rectangle((x - 14, 0, x + 14, H), fill=(40, 42, 46, 235)); d.rectangle((x - 4, 0, x + 4, H), fill=(90, 92, 98, 255))
    can.alpha_composite(L)
    txt(can, t, w('Zweimal'), (CX, 800), '2 × GEFLOHEN', anton(120), YEL)
    txt(can, t, w('zweimal', 188), (CX, 1000), '2 × GEFASST', anton(120), RED); return can
def s_paasi(t, w0, w1):
    can = sh(fit('t26', t, w0, w1, 1.05), 230, 0.45)
    typewriter(can, t, w('Dezember'), (CX, Y1), 'DEZEMBER 1948', typew(76), CREAM, 0.07)
    txt(can, t, w('begnadigte'), (CX, Y2 + 10), 'BEGNADIGT', anton(120), YEL)
    txt(can, t, w('Juho'), (CX, Y3 + 20), 'PRÄSIDENT JUHO PAASIKIVI', bebas(62), WHITE); return can

# ================= chapter 4 =================
def lowfit(n, t, w0, w1):
    """portrait photo a little wider than the screen, sitting at the bottom; the top stays free for the chapter card"""
    im = src(n); k = W / im.width * lerp(1.15, 1.2, clamp((t - w0) / (w1 - w0))); pw, ph = int(im.width * k), int(im.height * k)
    x0, y0 = (W - pw) // 2, H - ph; can = _bg(n).copy(); P = im.resize((pw, ph), Image.BICUBIC).convert('RGBA')
    m = Image.new('L', (pw, ph), 255); dm = ImageDraw.Draw(m)
    for i in range(140): dm.line((0, i, pw, i), fill=int(255 * i / 140))
    can.paste(P, (x0, y0), m); return can, (lambda sx, sy: (x0 + sx * k, y0 + sy * k))
def s_nofut(t, w0, w1):
    can, pt = lowfit('t15', t, w0, w1); sh(can, 230, 0.5)
    chapter(can, t, w0 + 0.3, 4, 'EIN NEUER NAME', w0 + 3.3)
    txt(can, t, w('Doch', 200) + 0.2, (CX, Y3), 'KEINE ZUKUNFT IN FINNLAND', anton(84), WHITE)
    point_at(can, t, w('Törni', 200), pt(560, 600), 'TÖRNI'); return can
STO, CCS, MOB = (18.07, 59.33), (-66.9, 10.5), (-88.04, 30.69)
def s_sea(t, w0, w1):
    z = 1.0; can = ATL.frame(z)
    pts = route([STO, (5.0, 56.0), (-10.0, 45.0), (-35.0, 25.0), CCS], ATL)
    pts2 = route([CCS, (-75.0, 16.0), (-84.0, 21.5), (-86.5, 26.0), MOB], ATL)
    sx, sy = ATL.p(*STO); cx_, cy_ = ATL.p(*CCS); mx, my = ATL.p(*MOB)
    dot(can, sx, sy, YEL, 10); label(can, t, w('1949', 200), sx - 20, sy - 40, '1949', 52, YEL, 'rm')
    label(can, t, w('Schweden'), sx - 20 - bebas(52).getlength('1949') - 14, sy - 40, 'SCHWEDEN', 52, YEL, 'rm')
    u1 = eio((t - w('Schiff', 205)) / 3.0); dashed(can, pts, u1, YEL, 6, 18, 0)
    if 0 < u1 < 1: i = int(u1 * (len(pts) - 2)); ship(can, *pts[i + 1], math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0]), 40)
    if t > w('Venezuela'): dot(can, cx_, cy_, WHITE, 10); label(can, t, w('Venezuela'), cx_ + 20, cy_ + 34, 'CARACAS', 50, WHITE)
    label(can, t, w('falschem'), sx - 20, sy + 30, 'UNTER FALSCHEM NAMEN', 38, CREAM, 'rm')
    u2 = eio((t - w('fuhr', 208)) / 3.4); dashed(can, pts2, u2, WHITE, 6, 18, 0)
    if 0 < u2 < 1: i = int(u2 * (len(pts2) - 2)); ship(can, *pts2[i + 1], math.atan2(pts2[i + 1][1] - pts2[i][1], pts2[i + 1][0] - pts2[i][0]), 40)
    if t > w('sprang'): ring(can, t, w('sprang'), mx + 10, my + 40, YEL, 22, False); label(can, t, w('sprang'), mx + 40, my + 90, 'ÜBER BORD', 50, YEL, 'lm')
    if u2 >= 0.99: dot(can, mx, my, WHITE, 10)
    if t > w('Alabamas'): label(can, t, w('Alabamas'), mx + 10, my - 60, 'MOBILE, ALABAMA', 50, WHITE)
    txt(can, t, w('Golf'), (CX, Y3), 'GOLF VON MEXIKO', anton(76), WHITE); return can
def s_lodge(t, w0, w1):
    can = dim(fit('t07', t, w0, w1, 1.03), 180).filter(ImageFilter.GaussianBlur(4))
    doc(can, t, w('Gesetz') - 0.1, [('LODGE ACT', 72, INK_), ('DIENST IN DER US ARMY', 42, INK_), ('= STAATSBÜRGERSCHAFT', 42, (150, 30, 30))], CX, 900, 820)
    return can
def s_rename(t, w0, w1):
    can = sh(fit('t01', t, w0, w1, 1.05), 235, 0.45)
    txt(can, t, w('1954'), (CX, 1040), '1954', typew(80), CREAM)
    t_old, t_new = w('Lauri', 230), w('Larry', 230)
    f = anton(112); tw = f.getlength('LAURI TÖRNI')
    if t > t_old:
        a_ = 1 - 0.45 * clamp((t - t_new) / 0.4)
        shadowed(can, lambda d: d.text((CX, 1190), 'LAURI TÖRNI', font=f, fill=WHITE + (int(255 * a_ * eout((t - t_old) / 0.35)),), anchor='mm'))
        if t > t_new - 0.25:
            k = eio((t - t_new + 0.25) / 0.4); L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(L).line((CX - tw / 2 - 20, 1200, CX - tw / 2 - 20 + (tw + 40) * k, 1180), fill=RED + (255,), width=14); can.alpha_composite(L)
    if t > t_new:
        s_ = 'LARRY THORNE'; f2 = anton(116); n = min(len(s_), int((t - t_new) / 0.06) + 1)
        shadowed(can, lambda d: d.text((CX - f2.getlength(s_) / 2, 1360), s_[:n], font=f2, fill=YEL + (255,), anchor='lm'))
    return can
def s_sf(t, w0, w1):
    can = sh(pan('t24', t, w0, w1, -1, 0.45, 1.05))
    txt(can, t, w('Special', 238), (CX, Y1), 'SPECIAL FORCES', anton(100), WHITE)
    txt(can, t, w('Green'), (CX, Y2 + 10), 'GREEN BERETS', anton(84), YEL)
    txt(can, t, w('Staatsbürger', 240), (CX, Y3 + 20), 'STAATSBÜRGER UND OFFIZIER', bebas(62), CREAM); return can
TOL, ZAG = (11.56, 47.76), (49.2, 32.6)
def s_iran(t, w0, w1):
    z = lerp(1.0, 1.06, clamp((t - w0) / (w1 - w0))); can = IRN.frame(z)
    bx, by = IRN.p(*TOL, z); zx, zy = IRN.p(*ZAG, z)
    dot(can, bx, by, YEL, 11); label(can, t, w('Tölz'), bx + 24, by - 40, 'BAD TÖLZ', 56, YEL)
    dashed(can, route([TOL, (25.0, 42.0), (38.0, 37.0), ZAG], IRN, z), eio((t - w('Tölz')) / 1.8), YEL)
    if t > w('Iran', 245): dot(can, zx, zy, RED, 11); label(can, t, w('Iran', 245), zx - 24, zy + 50, 'IRAN', 70, WHITE, 'rm')
    typewriter(can, t, w('1962'), (CX, YT), '1962', typew(80), CREAM, 0.1)
    txt(can, t, w('Bergungsmission'), (CX, Y3 + 10), 'BERGUNGSMISSION', anton(90), YEL); return can
def s_zagros(t, w0, w1):
    can = sh(pan('t17', t, w0, w1, 1, 0.5, 1.05), 200, 0.55)
    k = eio((t - w('3.800') + 0.2) / 1.4); y = lerp(1250, 720, k)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for x in range(60, W - 60, 36): d.line((x, y, x + 20, y), fill=YEL + (255,), width=5)
    can.alpha_composite(L)
    if k > 0: counter(can, t, w('3.800') - 0.2, 0, 3800, (CX + 160, y - 70), 100, YEL, 1.4, '{:,}', ' M')
    txt(can, t, w('Zagros-Gebirge'), (CX, YT), 'ZAGROS-GEBIRGE', anton(84), WHITE)
    txt(can, t, w('geheimes'), (CX, Y3), 'TOTE GEBORGEN, GEHEIMES MATERIAL GESICHERT', bebas(60), CREAM); return can

# ================= chapter 5 =================
def s_vn(t, w0, w1):
    can = sh(pan('t05', t, w0, w1, 1, 0.5, 1.05))
    chapter(can, t, w0 + 0.3, 5, 'VIETNAM', w0 + 3.3)
    txt(can, t, w('1963'), (CX, Y3), 'VIETNAM AB 1963', anton(96), YEL); return can
def s_secret(t, w0, w1):
    can = sh(pan('t11', t, w0, w1, -1, 0.45, 1.05))
    stamp(can, t, w('geheimen'), 'GEHEIM', (CX, 760), RED, 110, -8)
    txt(can, t, w('Laos', 270), (CX, Y3), 'EINSÄTZE ÜBER DIE GRENZE NACH LAOS', anton(76), WHITE); return can
def s_crash(t, w0, w1):
    z = lerp(1.0, 1.12, clamp((t - w0) / (w1 - w0))); can = VN.frame(z)
    kd, dn, crash = VN.p(107.80, 15.45, z), VN.p(108.22, 16.07, z), VN.p(107.93, 15.78, z)
    dot(can, *dn, WHITE, 10); label(can, t, w0 + 0.2, dn[0] + 26, dn[1] - 4, 'DA NANG', 58)
    dot(can, *kd, YEL, 12); label(can, t, w('Kham', 280), kd[0] + 28, kd[1] + 6, 'KHAM DUC', 58, YEL)
    typewriter(can, t, w('18.', 270), (CX, YT), '18. OKTOBER 1965', typew(72), CREAM, 0.07)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rr = np.random.default_rng(int(t * 30))
    if t > w('Wetter'):
        for _ in range(170): x, y = rr.uniform(0, W), rr.uniform(0, H); d.line((x, y, x - 14, y + 44), fill=(170, 180, 195, 90), width=2)
    can.alpha_composite(L)
    dashed(can, [kd, crash], eio((t - w('startete')) / 2.0), YEL)
    ring(can, t, w('stürzte'), *crash)
    label(can, t, w('stürzte') + 0.3, crash[0] - 60, crash[1] - 90, 'ABSTURZ', 72, RED, 'rm')
    txt(can, t, w('Hubschrauber', 280), (CX, Y3), 'HUBSCHRAUBER DER SÜDVIETNAMESISCHEN LUFTWAFFE', bebas(56), WHITE, w('Wetter')); return can
def s_missing(t, w0, w1):
    can = sh(pan('t20', t, w0, w1, -1, 0.5, 1.05))
    txt(can, t, w('Suche', 290), (CX, YT), 'DIE SUCHE BLEIBT OHNE ERFOLG', anton(76), WHITE)
    stamp(can, t, w('vermisst'), 'VERMISST', (CX, 900), RED, 110, -6)
    txt(can, t, w('Major'), (CX, Y3), 'SPÄTER ZUM MAJOR BEFÖRDERT', anton(80), YEL); return can
def s_found(t, w0, w1):
    can = dim(pan('t13', t, w0, w1, 1, 0.5, 1.05), 165).filter(ImageFilter.GaussianBlur(2))
    counter(can, t, w('1999') - 0.6, 1965, 1999, (CX, 820), 260, WHITE, 1.2, '{}')
    txt(can, t, w('Absturzstelle', 300), (CX, 1040), 'ABSTURZSTELLE GEFUNDEN', anton(90), YEL)
    txt(can, t, w('amerikanisch-vietnamesisches'), (CX, 1160), 'AMERIKANISCH-VIETNAMESISCHES TEAM', bebas(62), CREAM); return can
def s_arl(t, w0, w1):
    can = plain(); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for row in range(4):
        y = 960 + row * 120; sc = 0.6 + row * 0.18; n = 7 - row
        for i in range(n):
            ti = w('Nationalfriedhof') - 0.4 + (row * 7 + i) * 0.05; k = eout((t - ti) / 0.4)
            if k <= 0: continue
            x = CX + (i - (n - 1) / 2) * 190 * sc; hw, hh = 34 * sc, 80 * sc * k
            d.rounded_rectangle((x - hw, y - hh, x + hw, y), int(18 * sc), fill=(225, 225, 218, int(235 * k)))
    can.alpha_composite(L)
    typewriter(can, t, w('26.'), (CX, 520), '26. JUNI 2003', typew(72), CREAM, 0.07)
    txt(can, t, w('Nationalfriedhof'), (CX, 680), 'ARLINGTON', anton(130), WHITE)
    txt(can, t, w('Larry', 312), (CX, Y3 + 10), 'BEIGESETZT ALS LARRY THORNE', anton(76), YEL); return can
def s_outro3(t, w0, w1):      # three uniforms as a vertical timeline
    can = plain(); x, y0, y1 = 230, 640, 1300
    line_draw(can, t, w('Uniformen', 315) - 0.3, [(x, y0), (x, y1)], GREY, 5, 1.2)
    items = [(y0 + 60, '1939-1944', 'FINNLAND', YEL, w('Uniformen', 315)), ((y0 + y1) / 2, '1945', 'WAFFEN-SS', WHITE, w('Namen', 316)), (y1 - 60, '1954-1965', 'US ARMY', YEL, w('Leben', 318))]
    for y, yrs, lab, col, ti in items:
        if t > ti: dot(can, x, y, col, 16, clamp((t - ti) / 0.3))
        txt(can, t, ti, (x + 60, y - 50), yrs, typew(50), CREAM, anchor='lm'); txt(can, t, ti + 0.1, (x + 60, y + 30), lab, anton(84), col, anchor='lm')
    txt(can, t, w('zwei', 316), (CX, YT), 'DREI UNIFORMEN, ZWEI NAMEN', anton(80), WHITE)
    words(can, t, [('ZWISCHEN', WHITE, w('zwischen', 318)), ('DEN FRONTEN', YEL, w('Fronten', 318))], Y3 + 10, 100); return can
def s_view(t, w0, w1):
    can = sh(pan('t14', t, w0, w1, 1, 0.5, 1.0), 220, 0.55)
    txt(can, t, w('Kriegsheld'), (CX, Y2), 'FÜR VIELE EIN KRIEGSHELD', anton(84), YEL)
    txt(can, t, w('erinnern'), (CX, Y3 + 10), 'ANDERE ERINNERN AN DEN DIENST IN DER WAFFEN-SS', bebas(56), WHITE); return can
def s_story(t, w0, w1):       # team photo, arrow to Captain Thorne (standing, second from left)
    u = clamp((t - w0) / (w1 - w0)); im = src('t02'); cw = im.height * W / H / lerp(1.0, 1.06, u); cx = lerp(820, 780, u); cy = im.height / 2
    can = sh(crop('t02', cx, cy, cw), 220, 0.6); ch = cw * H / W; x0, y0 = min(max(cx - cw / 2, 0), im.width - cw), min(max(cy - ch / 2, 0), im.height - ch)
    fx, fy = (600 - x0) * W / cw, (520 - y0) * W / cw
    ta = w0 + 0.6
    arrow(can, (fx + 260, fy + 330), (fx + 50, fy + 60), eio((t - ta) / 0.6), YEL, 14, 44)
    label(can, t, ta + 0.4, fx + 260, fy + 390, 'CAPT. LARRY THORNE', 60, YEL, 'mm')
    txt(can, t, w('Schicksale'), (CX, Y3), 'EINZELNE SCHICKSALE IN GROSSEN KONFLIKTEN', anton(66), WHITE); return can
def s_ask(t, w0, w1):
    can = plain(); tl = w('Lauri', 336)
    txt(can, t, w('Wie', 335), (CX, 600), 'WIE SEHT IHR', anton(110), WHITE)
    txt(can, t, tl, (CX, 780), 'LAURI TÖRNI', anton(100), YEL)
    txt(can, t, tl + 0.3, (CX, 880), '/', anton(80), GREY)
    txt(can, t, tl + 0.5, (CX, 980), 'LARRY THORNE', anton(100), YEL)
    txt(can, t, tl + 0.9, (CX, 1160), '?', anton(180), WHITE)
    txt(can, t, w('Schreibt', 336), (CX, Y3 + 10), 'SCHREIBT ES IN DIE KOMMENTARE', bebas(70), CREAM); return can

ANCH = [(None, s_date), (('verschwindet', 0), s_heli), (('An', 6), s_thorne), (('Erst', 11), s_years), (('Doch', 15), s_three), (('In', 27), s_name),
        (('Lauri', 33), s_born), (('Damals', 0), s_viipuri), (('1938', 0), s_1938), (('Ein', 51), s_attack), (('Im', 57), s_winter), (('wo', 62), s_motti),
        (('Als', 66), s_lt), (('Finnland', 72), s_lost), (('Finnland', 78), s_wien), (('Noch', 88), s_cont), (('1943', 0), s_abt), (('Seine', 103), s_raid),
        (('Berichten', 0), s_bounty), (('Im', 117), s_ilom), (('Einer', 124), s_koiv), (('Im', 132), s_mhk), (('Im', 140), s_armist), (('Für', 146), s_notover),
        (('und', 154), s_germ), (('In', 161), s_ss45), (('Aus', 172), s_escape), (('Dort', 177), s_akte), (('Wegen', 180), s_verdict), (('Zweimal', 0), s_prison),
        (('Im', 193), s_paasi), (('Doch', 200), s_nofut), (('1949', 0), s_sea), (('Ein', 221), s_lodge), (('1954', 0), s_rename), (('Er', 239), s_sf),
        (('1962', 0), s_iran), (('In', 250), s_zagros), (('Ab', 263), s_vn), (('1965', 268), s_secret), (('Am', 276), s_crash), (('Die', 292), s_missing),
        (('Erst', 299), s_found), (('Am', 305), s_arl), (('Drei', 316), s_outro3), (('In', 322), s_view), (('Seine', 330), s_story), (('Wie', 339), s_ask)]
HOLD = {s_view: 1.0, s_verdict: 0.7}
SCN = [((0.0 if fn is s_date else w(*an) - 0.15 + HOLD.get(fn, 0.0)), fn) for an, fn in ANCH]
T_VOICE = wt('Kommentare.', 340) + 0.85          # voice is cut here, before "Wenn euch diese Geschichte gefallen hat ..."
T = T_VOICE + 1.4
OV = 0.4
SC = [(0 if i == 0 else s - OV, T if i == len(SCN) - 1 else SCN[i + 1][0] + OV, fn) for i, (s, fn) in enumerate(SCN)]
def frame(t): return assemble(SC, t, T)
def ui(im):
    im = im.convert('RGBA'); L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((0, 0, W, 290), fill=(255, 0, 0, 60)); d.rectangle((930, 680, W, 1580), fill=(255, 0, 0, 80)); d.rectangle((0, 1580, W, H), fill=(255, 0, 0, 80))
    im.alpha_composite(L); return im.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; cols = 8; P_ = Image.new('RGB', (cols * 240, ((len(ts) + cols - 1) // cols) * 427))
        for i, t in enumerate(ts):
            P_.paste(ui(frame(t)).resize((240, 427)), ((i % cols) * 240, (i // cols) * 427)); ImageDraw.Draw(P_).text(((i % cols) * 240 + 4, (i // cols) * 427 + 4), str(t), fill=(0, 255, 0))
        P_.save(B + sys.argv[2], quality=85); sys.exit()
    if sys.argv[1] == 'T': print(T, T_VOICE); sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '8M', '-maxrate', '10M', '-bufsize', '16M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
