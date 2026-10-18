# Lauri Törni long video, complete (voice vcut.wav, 351.5 s) + logo outro appended afterwards
import sys, subprocess
from lib import *
from lib import _bg

T = 352.3
LADOGA = [(30.85, 61.63), (30.45, 61.42), (30.05, 61.05), (29.98, 60.75), (30.45, 60.42), (31.0, 60.08), (31.6, 59.95), (32.4, 60.1), (32.85, 60.5),
          (32.75, 60.9), (32.4, 61.15), (31.9, 61.4), (31.4, 61.62)]
CEDED = [(27.75, 60.52), (28.6, 61.0), (29.3, 61.3), (29.9, 61.55), (30.5, 61.95), (30.75, 62.25), (31.1, 62.55), (31.4, 62.95), (31.9, 63.05), (32.9, 62.55),
         (32.95, 61.85), (32.4, 61.15), (31.9, 61.3), (30.95, 60.55), (30.0, 60.15), (29.4, 60.2), (28.6, 60.45)]
VIIPURI = (28.75, 60.71); LEMETTI = (31.62, 61.78)
KAR = Map(31.4, 61.78, 7.5, hi=('Finland',), extra=((LADOGA, SEA),))
KAR2 = Map(29.6, 61.75, 13.0, hi=('Finland',), extra=((LADOGA, SEA),))
VN = Map(107.6, 15.75, 5.5, hi=('Vietnam',))
EU = Map(19.0, 57.0, 46.0, hi=('Finland',), extra=((LADOGA, SEA),))
EUW = Map(20.0, 55.2, 60.0, hi=('Finland', 'Austria'), extra=((LADOGA, SEA),))
ATL = Map(-30.0, 40.0, 140.0, hi=('United States of America',))
IRN = Map(31.5, 39.5, 48.0, hi=('Iran',))
_OLD = [a for _, a, _ in json.load(open(B + 'words_all.json'))]; _NEW = [a for _, a, _ in WORDS]
def M(t): return float(np.interp(t, _OLD, _NEW))        # scene times were authored on the previous timeline
def w(s, after=0.0): return wt(s, M(after) if after else 0.0)
LOGO0 = None
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

# ================= intro =================
def s_date(t, w0, w1):
    can = shade(dim(pan('t16', t, w0, w1, -1, 0.55), 50), 220)
    typewriter(can, t, 0.25, (W / 2, 820), '18. OKTOBER 1965', typew(88), CREAM, 0.075)
    return can
def s_heli(t, w0, w1):
    z = lerp(1.0, 1.12, clamp((t - w0) / (w1 - w0))); can = VN.frame(z)
    kd, dn, laos, crash = VN.p(107.80, 15.45, z), VN.p(108.22, 16.07, z), VN.p(107.0, 15.62, z), VN.p(107.93, 15.78, z)
    dot(can, *dn, WHITE, 10); label(can, t, w0 + 0.2, dn[0] + 26, dn[1] - 4, 'DA NANG', 62)
    dot(can, *kd, YEL, 12); label(can, t, w0 + 0.3, kd[0] + 28, kd[1] + 6, 'KHAM DUC', 62, YEL)
    label(can, t, w0 + 0.3, laos[0] - 30, laos[1] - 90, 'LAOS', 90, GREY, 'rm')
    dashed(can, [kd, laos], eio((t - w0 - 0.2) / 1.6))
    label(can, t, w('Vietnams'), *VN.p(108.35, 14.9, z), 'VIETNAM', 96, YEL, 'mm')
    ring(can, t, w('Hubschrauber') - 0.2, *crash)
    label(can, t, w('Hubschrauber') + 0.2, crash[0] - 70, crash[1] - 80, 'VERSCHOLLEN', 76, RED, 'rm'); return can
def s_thorne(t, w0, w1):
    can = shade(fit('t18', t, w0, w1, 1.04), 230, 0.45)
    txt(can, t, w('Hauptmann'), (W / 2, 830), 'HAUPTMANN DER US SPECIAL FORCES', bebas(70), CREAM)
    words(can, t, [('LARRY', WHITE, w('Larry')), ('THORNE', YEL, w('Thorne'))], 950, 130); return can
def s_years(t, w0, w1):
    can = dim(pan('t10', t, w0, w1, 1), 165).filter(ImageFilter.GaussianBlur(2))
    counter(can, t, w('34'), 1965, 1999, (W / 2, 470), 300, WHITE, 1.4, '{}')
    txt(can, t, w('Jahre', 11), (W / 2, 690), '34 JAHRE SPÄTER', anton(96), YEL)
    txt(can, t, w('Absturzstelle'), (W / 2, 810), 'DIE ABSTURZSTELLE WIRD GEFUNDEN', bebas(66), CREAM); return can
def triptych(t, items, title=None):
    """three photos side by side, out of focus until each one is named"""
    can = Image.new('RGBA', (W, H), DARK + (255,)); pw = W // 3
    for i, (n, lab, ts) in enumerate(items):
        im = src(n); z = lerp(1.0, 1.04, clamp((t - items[0][2] + 2) / 12)); cw = min(im.width, im.height * pw / H) / z; ch = cw * H / pw
        cy = min(max(im.height * 0.5, ch / 2), im.height - ch / 2)
        ph = im.resize((pw, H), Image.BICUBIC, box=(im.width / 2 - cw / 2, cy - ch / 2, im.width / 2 + cw / 2, cy + ch / 2)).convert('RGBA')
        k = eio((t - ts + 0.15) / 0.8); r = 18 * (1 - k)
        if r > 0.3: ph = ph.filter(ImageFilter.GaussianBlur(r))
        ph.alpha_composite(Image.new('RGBA', ph.size, (6, 7, 9, int(150 * (1 - k)))))
        can.alpha_composite(ph, (i * pw, 0))
        if i: ImageDraw.Draw(can).line((i * pw, 0, i * pw, H), fill=DARK, width=8)
    shade(can, 200, 0.6)
    for i, (n, lab, ts) in enumerate(items): txt(can, t, ts - 0.05, (i * pw + pw / 2, 960), lab, anton(70), YEL if i != 1 else WHITE)
    if title: words(can, t, title, 110, 96)
    return can
def s_three(t, w0, w1):
    return triptych(t, [('t06', 'FINNLAND', w('Finnland', 19)), ('t22', 'WAFFEN-SS', w('Waffen-SS,', 19)), ('t21', 'US ARMY', w('Army.', 19))],
                    [('DREI', WHITE, w('drei', 17)), ('UNIFORMEN', YEL, w('Uniformen'))])
def s_name(t, w0, w1):
    can = shade(pan('t09', t, w0, w1, -1, 0.42, 1.25), 230, 0.45)
    txt(can, t, w('Heimat'), (W / 2, 800), 'IN SEINER HEIMAT HIESS ER', bebas(70), CREAM)
    words(can, t, [('LAURI', WHITE, w('Lauri', 30)), ('TÖRNI', YEL, w('Törni', 31))], 935, 150); return can

# ================= chapter 1 =================
def s_born(t, w0, w1):        # birth register card, no photo
    can = plain()
    chapter(can, t, w0 + 0.3, 1, 'VIIPURI UND DER WINTERKRIEG', w0 + 3.3)
    doc(can, t, w('Lauri', 33) + 0.6, [('GEBURTSREGISTER', 46, INK_), ('LAURI ALLAN TÖRNI', 60, INK_), ('28. MAI 1919', 52, (150, 30, 30)), ('VIIPURI, KARELIEN', 44, INK_)], W / 2, 560, 980)
    return can

def s_viipuri(t, w0, w1):
    z = lerp(1.0, 1.15, eio((t - w0) / (w1 - w0))); can = KAR2.frame(z)
    vx, vy = KAR2.p(*VIIPURI, z); ced = [KAR2.p(*q, z) for q in CEDED]; k = eio((t - w('heute') - 0.1) / 0.9)
    poly_fill(can, ced, YEL, 90 * (1 - k)); poly_fill(can, ced, RED, 150 * k)
    ImageDraw.Draw(can).polygon([KAR2.p(*q, z) for q in LADOGA], fill=SEA, outline=BORDER)
    dot(can, vx, vy, YEL, 12)
    if t < w('Wyborg'): label(can, t, w0 + 0.2, vx - 34, vy - 6, 'VIIPURI', 68, YEL, 'rm', w('Wyborg') - 0.2)
    label(can, t, w('Wyborg'), vx - 34, vy - 6, 'WYBORG', 68, CREAM, 'rm')
    label(can, t, w0 + 0.4, *KAR2.p(26.0, 62.6, z), 'FINNLAND', 80, CREAM, 'mm')
    label(can, t, w('Russland') - 0.1, *KAR2.p(33.6, 63.1, z), 'RUSSLAND', 80, GREY, 'mm')
    txt(can, t, w('Damals'), (W / 2, 110), 'DAMALS FINNLAND', anton(76), YEL, w('heute'))
    txt(can, t, w('heute') + 0.1, (W / 2, 110), 'HEUTE RUSSLAND', anton(76), RED); return can
def s_1938(t, w0, w1):
    can = shade(fit('t23', t, w0, w1, 1.05), 220, 0.5)
    txt(can, t, w('1938'), (W / 2, 840), '1938', anton(170), YEL)
    txt(can, t, w('Wehrdienst'), (W / 2, 975), 'WEHRDIENST', bebas(80), WHITE); return can
def s_attack(t, w0, w1):      # November 1939: machine gun nest in the snow
    can = shade(pan('t25', t, w0, w1, 1, 0.5, 1.12), 220, 0.5)
    typewriter(can, t, w('November', 50), (W / 2, 830), 'NOVEMBER 1939', typew(84), CREAM, 0.07)
    txt(can, t, w('griff') - 0.05, (W / 2, 950), 'DIE SOWJETUNION GREIFT AN', anton(84), YEL); return can
def s_winter(t, w0, w1):
    can = shade(fit('t04', t, w0, w1, 1.05), 220, 0.55)
    txt(can, t, w('Winterkrieg') + 0.1, (W / 2, 900), 'WINTERKRIEG 1939/40', anton(96), WHITE)
    txt(can, t, w('Ladogasees') - 0.2, (W / 2, 1000), 'NÖRDLICH DES LADOGASEES', bebas(66), YEL); return can
def s_motti(t, w0, w1):
    z = lerp(1.0, 1.25, eio((t - w0) / (w1 - w0))); can = KAR.frame(z)
    lx, ly = KAR.p(*LEMETTI, z); label(can, t, w0 + 0.2, *KAR.p(31.7, 61.05, z), 'LADOGASEE', 64, GREY, 'mm')
    k = eout((t - w('Lemetti') + 0.1) / 0.5)
    if k > 0:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for i in range(5): d.rounded_rectangle((lx - 120 + i * 50, ly - 18, lx - 85 + i * 50, ly + 18), 6, fill=RED + (int(230 * k),))
        can.alpha_composite(L)
    te = w('eingekesselte') - 0.1
    for i, ang in enumerate(range(0, 360, 60)):
        a = math.radians(ang); r0, r1 = 330 * z, 165 * z
        arrow(can, (lx + r0 * math.cos(a), ly + r0 * math.sin(a)), (lx + r1 * math.cos(a), ly + r1 * math.sin(a)), eio((t - te - i * 0.08) / 0.7), YEL, 12, 36)
    if t > te + 0.8:
        kk = eio((t - te - 0.8) / 0.8); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); r = 150 * z
        ImageDraw.Draw(L).arc((lx - r, ly - r, lx + r, ly + r), -90, -90 + 360 * kk, fill=YEL + (255,), width=10); can.alpha_composite(L)
    label(can, t, w('Lemetti'), lx + 230 * z, ly - 135 * z, 'LEMETTI', 80, YEL, 'lm')
    txt(can, t, w('zerschlugen') - 0.2, (W / 2, 110), 'EINGEKESSELT UND ZERSCHLAGEN', anton(76), WHITE); return can
def s_lt(t, w0, w1):
    can = shade(pan('t03', t, w0, w1, -1, 0.45, 1.15), 220, 0.5)
    typewriter(can, t, w('März', 65), (W / 2, 850), 'MÄRZ 1940', typew(84), CREAM, 0.08)
    txt(can, t, w('Leutnant'), (W / 2, 975), 'LEUTNANT DER RESERVE', anton(90), YEL); return can
def s_lost(t, w0, w1):
    z = 1.15; can = KAR2.frame(z); ced = [KAR2.p(*q, z) for q in CEDED]; vx, vy = KAR2.p(*VIIPURI, z)
    k = eio((t - w('Teile', 70) + 0.2) / 0.9); poly_fill(can, ced, RED, 160 * k)
    ImageDraw.Draw(can).polygon([KAR2.p(*q, z) for q in LADOGA], fill=SEA, outline=BORDER)
    label(can, t, w('Kareliens', 70), *KAR2.p(32.0, 62.2, z), 'KARELIEN', 70, WHITE, 'mm')
    txt(can, t, w('abgeben') - 0.1, (W / 2, 110), 'AN DIE SOWJETUNION ABGETRETEN', anton(76), RED)
    if t > w('Viipuri', 75) - 0.2: ring(can, t, w('Viipuri', 75) - 0.2, vx, vy, YEL, 30, False)
    dot(can, vx, vy, YEL, 12); label(can, t, w('Viipuri', 75) - 0.1, vx - 40, vy - 6, 'VIIPURI', 72, YEL, 'rm'); return can

# ================= chapter 2: Wien und Abteilung Törni =================
HEL, VIE = (24.94, 60.17), (16.37, 48.21)
def s_wien(t, w0, w1):
    z = lerp(1.0, 1.08, clamp((t - w0) / (w1 - w0))); can = EUW.frame(z)
    chapter(can, t, w0 + 0.3, 2, 'WIEN UND ABTEILUNG TÖRNI', w0 + 3.3)
    hx, hy = EUW.p(*HEL, z); vx, vy = EUW.p(*VIE, z)
    if t > w0 + 0.3:
        dot(can, hx, vy * 0 + hy, YEL, 11); label(can, t, w('Juni', 80) - 0.3, hx + 26, hy, 'HELSINKI', 60, YEL)
        dashed(can, route([HEL, (21.0, 55.0), VIE], EUW, z), eio((t - w('reiste')) / 1.6))
        if t > w('Wien', 80): dot(can, vx, vy, WHITE, 11); label(can, t, w('Wien', 80), vx + 26, vy, 'WIEN', 70, WHITE)
        typewriter(can, t, w('Juni', 80), (W / 2, 920), 'JUNI 1941', typew(70), CREAM, 0.07)
        txt(can, t, w('mehrwöchige'), (W / 2, 1015), 'MEHRWÖCHIGE AUSBILDUNG', anton(76), YEL)
    return can
def s_cont(t, w0, w1):
    can = shade(pan('t29', t, w0, w1, 1, 0.5, 1.15), 220, 0.5)
    txt(can, t, w('kehrte', 88), (W / 2, 850), 'ZURÜCK NACH FINNLAND', bebas(72), CREAM)
    txt(can, t, w('Fortsetzungskrieg'), (W / 2, 965), 'FORTSETZUNGSKRIEG', anton(100), YEL); return can
def s_abt(t, w0, w1):
    can = shade(pan('t08', t, w0, w1, -1, 0.42, 1.0), 230, 0.45)
    txt(can, t, w('1943'), (W / 2, 820), '1943', anton(120), WHITE)
    words(can, t, [('ABTEILUNG', WHITE, w('Abteilung')), ('TÖRNI', YEL, w('Törni', 100))], 960, 120); return can
def s_raid(t, w0, w1):        # behind the lines: schematic over a dark photo
    can = plain()
    fx = W * 0.5; L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pts = [(fx + 40 * math.sin(y / 90), y) for y in range(160, 960, 8)]
    d.line(pts, fill=RED + (230,), width=8)
    can.alpha_composite(L)
    label(can, t, w0 + 0.2, fx - 300, 200, 'FINNLAND', 64, YEL, 'mm'); label(can, t, w0 + 0.2, fx + 320, 200, 'SOWJETISCHE SEITE', 64, RED, 'mm')
    label(can, t, w0 + 0.4, fx, 1000, 'FRONTLINIE', 54, GREY, 'mm')
    path = [(fx - 420, 700), (fx - 120, 640), (fx + 140, 560), (fx + 420, 470), (fx + 640, 520)]
    dashed(can, path, eio((t - w('operierten')) / 2.2), YEL, 8)
    for i, (x, y) in enumerate([(fx + 300, 500), (fx + 560, 470)]):
        if t > w('Hinterhalte') + i * 0.35:
            k = eout((t - w('Hinterhalte') - i * 0.35) / 0.3); q = 26 * k; L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            d.line((x - q, y - q, x + q, y + q), fill=YEL + (255,), width=10); d.line((x - q, y + q, x + q, y - q), fill=YEL + (255,), width=10); can.alpha_composite(L)
    if t > w('kehrten', 105): dashed(can, [(fx + 640, 560), (fx + 300, 680), (fx - 80, 760), (fx - 420, 780)], eio((t - w('kehrten', 105)) / 1.6), WHITE, 6)
    txt(can, t, w('weit', 103), (W / 2, 110), 'WEIT HINTER DEN LINIEN', anton(84), WHITE)
    txt(can, t, w('Tagen'), (fx - 420, 860), 'NACH TAGEN ZURÜCK', bebas(56), CREAM); return can

def s_bounty(t, w0, w1):      # bounty notice, no photo
    can = plain()
    txt(can, t, w('Berichten'), (W / 2, 110), 'BERICHTEN ZUFOLGE', bebas(64), CREAM)
    doc(can, t, w('Berichten') + 0.3, [('KOPFGELD', 80, (150, 30, 30)), ('LAURI TÖRNI', 56, INK_), ('', 30, INK_), ('', 30, INK_)], W / 2, 560, 900)
    counter(can, t, w('drei', 112) - 0.2, 0, 3000000, (W / 2, 660), 120, INK_, 1.6, '{:,}', ' FMK')
    stamp(can, t, w('Finnmark') + 0.2, 'SOWJETISCHE SEITE', (1450, 820), RED, 54, -10); return can

def s_ilom(t, w0, w1):
    can = shade(fit('t19', t, w0, w1, 1.05), 220, 0.5)
    txt(can, t, w('Sommer', 115), (W / 2, 830), 'SOMMER 1944', typew(80), CREAM)
    txt(can, t, w('Ilomantsi'), (W / 2, 960), 'ILOMANTSI', anton(110), YEL); return can
def s_koiv(t, w0, w1):
    can = shade(fit('t28', t, w0, w1, 1.05), 230, 0.45)
    txt(can, t, w('Soldaten', 123), (W / 2, 790), 'UNTER SEINEM KOMMANDO', bebas(64), CREAM)
    words(can, t, [('MAUNO', WHITE, w('Mauno')), ('KOIVISTO', YEL, w('Koivisto'))], 905, 120)
    txt(can, t, w('Präsident'), (W / 2, 1015), 'SPÄTER PRÄSIDENT FINNLANDS', bebas(64), WHITE); return can
def s_mhk(t, w0, w1):         # Mannerheim Cross drawn as a graphic
    can = plain(); cx, cy, r = W / 2, 430, 210
    pts = [(cx - r * 0.28, cy - r), (cx + r * 0.28, cy - r), (cx + r * 0.16, cy - r * 0.16), (cx + r, cy - r * 0.28), (cx + r, cy + r * 0.28), (cx + r * 0.16, cy + r * 0.16),
           (cx + r * 0.28, cy + r), (cx - r * 0.28, cy + r), (cx - r * 0.16, cy + r * 0.16), (cx - r, cy + r * 0.28), (cx - r, cy - r * 0.28), (cx - r * 0.16, cy - r * 0.16), (cx - r * 0.28, cy - r)]
    line_draw(can, t, w('Juli') - 0.2, pts, YEL, 8, 1.4)
    if t > w('Mannerheim-Kreuz,') - 0.1:
        k = eio((t - w('Mannerheim-Kreuz,') + 0.1) / 0.6); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).polygon(pts, fill=YEL + (int(80 * k),)); can.alpha_composite(L)
        for ang in (45, 135):   # crossed swords
            a = math.radians(ang); line_draw(can, t, w('Mannerheim-Kreuz,'), [(cx - 1.25 * r * math.cos(a), cy - 1.25 * r * math.sin(a)), (cx + 1.25 * r * math.cos(a), cy + 1.25 * r * math.sin(a))], WHITE, 7, 0.6)
    typewriter(can, t, w('Juli'), (W / 2, 790), 'JULI 1944', typew(76), CREAM, 0.08)
    txt(can, t, w('Mannerheim-Kreuz,') - 0.05, (W / 2, 905), 'MANNERHEIM-KREUZ', anton(120), YEL)
    txt(can, t, w('höchste'), (W / 2, 1015), 'FINNLANDS HÖCHSTE MILITÄRISCHE AUSZEICHNUNG', bebas(54), WHITE); return can

def s_armist(t, w0, w1):
    can = plain()
    chapter(can, t, w0 + 0.3, 3, 'VERRAT UND FLUCHT', w0 + 3.3)
    doc(can, t, w('September'), [('WAFFENSTILLSTAND', 64, INK_), ('FINNLAND / SOWJETUNION', 40, INK_), ('SEPTEMBER 1944', 46, (150, 30, 30))], W / 2, 560, 900)
    return can
def s_notover(t, w0, w1):     # typographic: VORBEI crossed out
    can = plain()
    txt(can, t, w('Für', 145), (W / 2, 380), 'FÜR TÖRNI WAR DER KRIEG', anton(90), WHITE)
    txt(can, t, w('Krieg', 146), (W / 2, 520), 'VORBEI', anton(150), GREY)
    line_draw(can, t, w('nicht', 146), [(W / 2 - 280, 540), (W / 2 + 280, 500)], RED, 16, 0.4)
    txt(can, t, w('Gruppe'), (W / 2, 760), 'EINE GEHEIME GRUPPE', bebas(76), CREAM)
    txt(can, t, w('Widerstand'), (W / 2, 870), 'WIDERSTAND GEGEN EINE BESETZUNG', anton(84), YEL); return can

NEU, LUE = (13.06, 53.36), (10.69, 53.87)
def s_germ(t, w0, w1):
    z = lerp(1.0, 1.1, clamp((t - w0) / (w1 - w0))); can = EU.frame(z)
    hx, hy = EU.p(*HEL, z); nx, ny = EU.p(*NEU, z)
    dot(can, hx, hy, YEL, 11); label(can, t, w0 + 0.2, hx + 26, hy, 'FINNLAND', 60, YEL)
    dashed(can, route([HEL, (19.5, 58.0), NEU], EU, z), eio((t - w('ging', 152)) / 1.6), YEL)
    if t > w('Deutschland', 152): dot(can, nx, ny, WHITE, 11); label(can, t, w('Deutschland', 152), nx + 26, ny, 'NEUSTRELITZ', 60, WHITE)
    typewriter(can, t, w('Januar'), (W / 2, 110), 'JANUAR 1945', typew(76), CREAM, 0.07)
    txt(can, t, w('Saboteur'), (W / 2, 975), 'AUSBILDUNG ZUM SABOTEUR', anton(84), YEL); return can
def s_ss45(t, w0, w1):
    can = shade(pan('t27', t, w0, w1, 1, 0.45, 1.12), 220, 0.5)
    txt(can, t, w('Kriegswochen'), (W / 2, 850), 'NORDDEUTSCHLAND 1945', bebas(72), CREAM)
    txt(can, t, w('Mai', 165), (W / 2, 965), 'MAI 1945: KAPITULATION', anton(96), YEL); return can
def s_escape(t, w0, w1):
    z = lerp(1.0, 1.08, clamp((t - w0) / (w1 - w0))); can = EU.frame(z)
    lx, ly = EU.p(*LUE, z); hx, hy = EU.p(*HEL, z)
    dot(can, lx, ly, RED, 11); label(can, t, w0 + 0.2, lx - 26, ly, 'LÜBECK', 62, RED, 'rm')
    if t > w('Gefangenenlager'): stamp(can, t, w('Gefangenenlager'), 'POW', (lx - 120, ly + 120), RED, 54, -8)
    dashed(can, route([LUE, (14.0, 57.5), (18.5, 60.5), HEL], EU, z), eio((t - w('floh', 170)) / 2.4), YEL)
    if t > w('Finnland', 172): dot(can, hx, hy, YEL, 11); label(can, t, w('Finnland', 172), hx + 26, hy, 'FINNLAND', 62, YEL)
    txt(can, t, w('floh', 170), (W / 2, 110), 'FLUCHT AUS DEM LAGER', anton(84), WHITE); return can
def s_akte(t, w0, w1):        # police photos: three portraits revealed one by one
    im = src('t12'); can = _bg('t12').copy(); dim(can, 120)
    full = crop('t12', im.width / 2, im.height / 2, im.width, W, int(W * im.height / im.width))
    ph = full.resize((W - 160, int((W - 160) * full.height / full.width)), Image.BICUBIC); x0, y0 = 80, (H - ph.height) // 2 - 30
    ts = [w('verhaftete'), w('Aufnahmen'), w('Akte')]
    for i in range(3):
        k = eout((t - ts[i]) / 0.35)
        if k <= 0: continue
        part = ph.crop((i * ph.width // 3, 0, (i + 1) * ph.width // 3, ph.height)); part.putalpha(int(255 * k))
        can.alpha_composite(part, (x0 + i * ph.width // 3, y0))
    stamp(can, t, w('Akte') + 0.3, 'VALPO 1946', (W - 330, 170), RED, 70, -8)
    txt(can, t, w('Staatspolizei'), (W / 2, 1000), 'VERHAFTET VON DER STAATSPOLIZEI', anton(70), YEL); return can
def s_verdict(t, w0, w1):
    can = plain()
    doc(can, t, w('Wegen', 180) - 0.2, [('URTEIL', 70, INK_), ('LANDESVERRAT', 52, INK_), ('6 JAHRE HAFT', 60, (150, 30, 30))], W / 2, 520, 820)
    stamp(can, t, w('verurteilt') + 0.2, 'VERURTEILT', (1400, 760), RED, 70, -12)
    return can
def s_prison(t, w0, w1):      # twice escaped, twice caught
    can = plain()
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    op = eio((t - w('Zweimal')) / 0.8) * (1 - eio((t - w('zweimal', 188)) / 0.6))
    for i in range(9):   # prison bars sliding open and shut
        x = 160 + i * 200 + (op * 90 if i % 2 else -op * 90); d.rectangle((x - 14, 0, x + 14, H), fill=(40, 42, 46, 235)); d.rectangle((x - 4, 0, x + 4, H), fill=(90, 92, 98, 255))
    can.alpha_composite(L)
    txt(can, t, w('Zweimal'), (W / 2, 420), '2 × GEFLOHEN', anton(120), YEL)
    txt(can, t, w('zweimal', 188), (W / 2, 620), '2 × GEFASST', anton(120), RED); return can
def s_paasi(t, w0, w1):
    can = shade(fit('t26', t, w0, w1, 1.05), 230, 0.45)
    typewriter(can, t, w('Dezember'), (W / 2, 800), 'DEZEMBER 1948', typew(76), CREAM, 0.07)
    txt(can, t, w('begnadigte'), (W / 2, 920), 'BEGNADIGT', anton(120), YEL)
    txt(can, t, w('Juho'), (W / 2, 1025), 'PRÄSIDENT JUHO PAASIKIVI', bebas(62), WHITE); return can

# ================= chapter 4: Ein neuer Name =================
def s_nofut(t, w0, w1):
    can = shade(fit('t15', t, w0, w1, 1.05), 230, 0.45)
    chapter(can, t, w0 + 0.3, 4, 'EIN NEUER NAME', w0 + 3.3)
    txt(can, t, w('Zukunft') + 0.1, (W / 2, 960), 'KEINE ZUKUNFT IN FINNLAND', anton(90), WHITE); return can
STO, CCS, MOB = (18.07, 59.33), (-66.9, 10.5), (-88.04, 30.69)
def s_sea(t, w0, w1):
    z = 1.0; can = ATL.frame(z)
    pts = route([STO, (5.0, 56.0), (-10.0, 45.0), (-35.0, 25.0), CCS], ATL)
    pts2 = route([CCS, (-75.0, 16.0), (-84.0, 21.5), (-86.5, 26.0), MOB], ATL)
    sx, sy = ATL.p(*STO); cx_, cy_ = ATL.p(*CCS); mx, my = ATL.p(*MOB)
    dot(can, sx, sy, YEL, 10); label(can, t, w('Schweden'), sx - 20, sy - 30, 'SCHWEDEN 1949', 52, YEL, 'rm')
    u1 = eio((t - w('Schiff', 205)) / 3.0); dashed(can, pts, u1, YEL, 6, 18, 0)
    if 0 < u1 < 1: i = int(u1 * (len(pts) - 2)); ship(can, *pts[i + 1], math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0]), 44)
    if t > w('Venezuela'): dot(can, cx_, cy_, WHITE, 10); label(can, t, w('Venezuela'), cx_ + 20, cy_ + 30, 'CARACAS', 52, WHITE)
    label(can, t, w('falschem'), sx - 20, sy + 30, 'UNTER FALSCHEM NAMEN', 40, CREAM, 'rm')
    u2 = eio((t - w('fuhr', 208)) / 3.4); dashed(can, pts2, u2, WHITE, 6, 18, 0)
    if 0 < u2 < 1: i = int(u2 * (len(pts2) - 2)); ship(can, *pts2[i + 1], math.atan2(pts2[i + 1][1] - pts2[i][1], pts2[i + 1][0] - pts2[i][0]), 44)
    if t > w('sprang'): ring(can, t, w('sprang'), mx + 10, my + 40, YEL, 22, False); label(can, t, w('sprang'), mx - 30, my + 80, 'ÜBER BORD', 52, YEL, 'rm')
    if t > w('Alabamas'): label(can, t, w('Alabamas'), mx + 30, my - 40, 'MOBILE, ALABAMA', 54, WHITE)
    txt(can, t, w('Golf'), (W / 2, 1000), 'GOLF VON MEXIKO', anton(76), WHITE); return can
def s_lodge(t, w0, w1):
    can = dim(fit('t07', t, w0, w1, 1.03), 180).filter(ImageFilter.GaussianBlur(4))
    doc(can, t, w('Gesetz') - 0.1, [('LODGE ACT', 72, INK_), ('DIENST IN DER US ARMY', 42, INK_), ('= STAATSBÜRGERSCHAFT', 42, (150, 30, 30))], W / 2, 540, 860)
    return can
def s_rename(t, w0, w1):      # old name crossed out, new name typed beneath
    can = shade(fit('t01', t, w0, w1, 1.05), 235, 0.4)
    txt(can, t, w('1954'), (W / 2, 640), '1954', typew(80), CREAM)
    t_old, t_new = w('Lauri', 230), w('Larry', 230)
    if t > t_old:
        a_ = 1 - 0.45 * clamp((t - t_new) / 0.4)
        f = anton(120); tw = f.getlength('LAURI TÖRNI')
        shadowed(can, lambda d: d.text((W / 2, 790), 'LAURI TÖRNI', font=f, fill=WHITE + (int(255 * a_ * eout((t - t_old) / 0.35)),), anchor='mm'))
        if t > t_new - 0.25:
            k = eio((t - t_new + 0.25) / 0.4); L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(L).line((W / 2 - tw / 2 - 20, 800, W / 2 - tw / 2 - 20 + (tw + 40) * k, 780), fill=RED + (255,), width=14); can.alpha_composite(L)
    if t > t_new:
        s_ = 'LARRY THORNE'; n = min(len(s_), int((t - t_new) / 0.06) + 1)
        shadowed(can, lambda d: d.text((W / 2 - anton(130).getlength(s_) / 2, 950), s_[:n], font=anton(130), fill=YEL + (255,), anchor='lm'))
    return can
def s_sf(t, w0, w1):
    can = shade(pan('t24', t, w0, w1, -1, 0.45, 1.12), 220, 0.5)
    txt(can, t, w('Special', 238), (W / 2, 850), 'SPECIAL FORCES', anton(100), WHITE)
    txt(can, t, w('Green'), (W / 2, 965), 'GREEN BERETS', anton(84), YEL)
    txt(can, t, w('Staatsbürger', 240), (W / 2, 110), 'STAATSBÜRGER UND OFFIZIER', bebas(66), CREAM); return can
TOL, ZAG = (11.56, 47.76), (49.2, 32.6)
def s_iran(t, w0, w1):
    z = lerp(1.0, 1.08, clamp((t - w0) / (w1 - w0))); can = IRN.frame(z)
    bx, by = IRN.p(*TOL, z); zx, zy = IRN.p(*ZAG, z)
    dot(can, bx, by, YEL, 11); label(can, t, w('Tölz'), bx + 24, by - 26, 'BAD TÖLZ', 58, YEL)
    dashed(can, route([TOL, (25.0, 42.0), (38.0, 37.0), ZAG], IRN, z), eio((t - w('Tölz')) / 1.8), YEL)
    if t > w('Iran', 245): dot(can, zx, zy, RED, 11); label(can, t, w('Iran', 245), zx + 24, zy, 'IRAN', 70, WHITE)
    typewriter(can, t, w('1962'), (W / 2, 110), '1962', typew(80), CREAM, 0.1)
    txt(can, t, w('Bergungsmission'), (W / 2, 990), 'BERGUNGSMISSION', anton(90), YEL); return can
def s_zagros(t, w0, w1):      # altitude line over the mountain photo
    can = shade(pan('t17', t, w0, w1, 1, 0.5, 1.12), 200, 0.55)
    k = eio((t - w('3.800') + 0.2) / 1.4); y = lerp(900, 330, k)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for x in range(120, W - 120, 36): d.line((x, y, x + 20, y), fill=YEL + (255,), width=5)
    can.alpha_composite(L)
    if k > 0: counter(can, t, w('3.800') - 0.2, 0, 3800, (W - 300, y - 70), 110, YEL, 1.4, '{:,}', ' M')
    txt(can, t, w('Zagros-Gebirge'), (W / 2, 110), 'ZAGROS-GEBIRGE', anton(84), WHITE)
    txt(can, t, w('geheimes'), (W / 2, 975), 'TOTE GEBORGEN, GEHEIMES MATERIAL GESICHERT', bebas(62), CREAM); return can

# ================= chapter 5: Vietnam =================
def s_vn(t, w0, w1):
    can = shade(pan('t05', t, w0, w1, 1, 0.5, 1.12), 220, 0.5)
    chapter(can, t, w0 + 0.3, 5, 'VIETNAM', w0 + 3.3)
    txt(can, t, w('1963'), (W / 2, 960), 'VIETNAM AB 1963', anton(96), YEL); return can
def s_secret(t, w0, w1):
    can = shade(pan('t11', t, w0, w1, -1, 0.45, 1.1), 220, 0.5)
    stamp(can, t, w('geheimen'), 'GEHEIM', (W / 2, 420), RED, 110, -8)
    txt(can, t, w('Laos', 270), (W / 2, 965), 'EINSÄTZE ÜBER DIE GRENZE NACH LAOS', anton(76), WHITE); return can
def s_crash(t, w0, w1):
    z = lerp(1.0, 1.15, clamp((t - w0) / (w1 - w0))); can = VN.frame(z)
    kd, dn, crash = VN.p(107.80, 15.45, z), VN.p(108.22, 16.07, z), VN.p(107.93, 15.78, z)
    dot(can, *dn, WHITE, 10); label(can, t, w0 + 0.2, dn[0] + 26, dn[1] - 4, 'DA NANG', 62)
    dot(can, *kd, YEL, 12); label(can, t, w('Kham', 280), kd[0] + 28, kd[1] + 6, 'KHAM DUC', 62, YEL)
    typewriter(can, t, w('18.', 270), (W / 2, 110), '18. OKTOBER 1965', typew(76), CREAM, 0.07)
    # rain streaks
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rr = np.random.default_rng(int(t * 30))
    if t > w('Wetter'):
        for _ in range(160): x, y = rr.uniform(0, W), rr.uniform(0, H); d.line((x, y, x - 14, y + 44), fill=(170, 180, 195, 90), width=2)
    can.alpha_composite(L)
    dashed(can, [kd, crash], eio((t - w('startete')) / 2.0), YEL)
    ring(can, t, w('stürzte'), *crash)
    label(can, t, w('stürzte') + 0.3, crash[0] - 70, crash[1] - 80, 'ABSTURZ', 76, RED, 'rm')
    txt(can, t, w('Hubschrauber', 280), (W / 2, 990), 'HUBSCHRAUBER DER SÜDVIETNAMESISCHEN LUFTWAFFE', bebas(56), WHITE, w('Wetter')); return can
def s_missing(t, w0, w1):
    can = shade(pan('t20', t, w0, w1, -1, 0.5, 1.1), 220, 0.5)
    txt(can, t, w('Suche', 290), (W / 2, 110), 'DIE SUCHE BLEIBT OHNE ERFOLG', anton(76), WHITE)
    stamp(can, t, w('vermisst'), 'VERMISST', (W / 2, 520), RED, 110, -6)
    txt(can, t, w('Major'), (W / 2, 965), 'SPÄTER ZUM MAJOR BEFÖRDERT', anton(80), YEL); return can
def s_found(t, w0, w1):
    can = dim(pan('t13', t, w0, w1, 1, 0.5, 1.05), 165).filter(ImageFilter.GaussianBlur(2))
    counter(can, t, w('1999') - 0.6, 1965, 1999, (W / 2, 470), 280, WHITE, 1.2, '{}')
    txt(can, t, w('Absturzstelle', 300), (W / 2, 690), 'ABSTURZSTELLE GEFUNDEN', anton(90), YEL)
    txt(can, t, w('amerikanisch-vietnamesisches'), (W / 2, 810), 'AMERIKANISCH-VIETNAMESISCHES TEAM', bebas(62), CREAM); return can
def s_arl(t, w0, w1):         # Arlington: rows of white headstones rising
    can = plain(); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for row in range(4):
        y = 560 + row * 95; sc = 0.6 + row * 0.18; n = 9 - row
        for i in range(n):
            ti = w('Nationalfriedhof') - 0.4 + (row * 9 + i) * 0.05; k = eout((t - ti) / 0.4)
            if k <= 0: continue
            x = W / 2 + (i - (n - 1) / 2) * 190 * sc; hw, hh = 34 * sc, 80 * sc * k
            d.rounded_rectangle((x - hw, y - hh, x + hw, y), int(18 * sc), fill=(225, 225, 218, int(235 * k)))
    can.alpha_composite(L)
    typewriter(can, t, w('26.'), (W / 2, 200), '26. JUNI 2003', typew(76), CREAM, 0.07)
    txt(can, t, w('Nationalfriedhof'), (W / 2, 330), 'ARLINGTON', anton(130), WHITE)
    txt(can, t, w('Larry', 312), (W / 2, 1000), 'BEIGESETZT ALS LARRY THORNE', anton(76), YEL); return can

def s_outro3(t, w0, w1):      # three uniforms as a timeline, no photos
    can = plain(); x0, x1, y = 260, 1660, 560
    line_draw(can, t, w('Uniformen', 315) - 0.3, [(x0, y), (x1, y)], GREY, 5, 1.2)
    items = [(x0 + 120, '1939-1944', 'FINNLAND', YEL, w('Uniformen', 315)), (W / 2, '1945', 'WAFFEN-SS', WHITE, w('Namen', 316)), (x1 - 120, '1954-1965', 'US ARMY', YEL, w('Leben', 318))]
    for x, yrs, lab, col, ti in items:
        if t > ti: dot(can, x, y, col, 16, clamp((t - ti) / 0.3))
        txt(can, t, ti, (x, y - 90), yrs, typew(56), CREAM); txt(can, t, ti + 0.1, (x, y + 100), lab, anton(84), col)
    txt(can, t, w('zwei', 316), (W / 2, 200), 'DREI UNIFORMEN, ZWEI NAMEN', anton(84), WHITE)
    words(can, t, [('ZWISCHEN', WHITE, w('zwischen', 318)), ('DEN FRONTEN', YEL, w('Fronten', 318))], 870, 110); return can

def s_view(t, w0, w1):
    can = shade(pan('t14', t, w0, w1, 1, 0.30, 1.0), 220, 0.62)
    txt(can, t, w('Kriegsheld'), (W / 2, 850), 'FÜR VIELE EIN KRIEGSHELD', anton(84), YEL)
    txt(can, t, w('erinnern'), (W / 2, 965), 'ANDERE ERINNERN AN DEN DIENST IN DER WAFFEN-SS', bebas(58), WHITE); return can
def s_story(t, w0, w1):       # team photo, arrow to Captain Thorne (standing, second from left)
    u = clamp((t - w0) / (w1 - w0)); im = src('t02'); cw = lerp(2400, 2150, u); cx = lerp(1200, 1075, u); cy = 700
    can = shade(crop('t02', cx, cy, cw), 220, 0.62); ch = cw * H / W; x0, y0 = min(max(cx - cw / 2, 0), im.width - cw), min(max(cy - ch / 2, 0), im.height - ch)
    fx, fy = (600 - x0) * W / cw, (520 - y0) * W / cw
    ta = w0 + 0.6
    arrow(can, (fx + 330, fy - 150), (fx + 70, fy - 40), eio((t - ta) / 0.6), YEL, 14, 44)
    label(can, t, ta + 0.4, fx + 350, fy - 160, 'CAPT. LARRY THORNE', 64, YEL)
    txt(can, t, w('Schicksale'), (W / 2, 990), 'EINZELNE SCHICKSALE IN GROSSEN KONFLIKTEN', anton(70), WHITE); return can
def s_ask(t, w0, w1):         # big question, both names
    can = plain()
    txt(can, t, w('Wie', 335), (W / 2, 330), 'WIE SEHT IHR', anton(110), WHITE)
    txt(can, t, w('Lauri', 336), (W / 2 - 360, 520), 'LAURI TÖRNI', anton(100), YEL)
    txt(can, t, w('Lauri', 336) + 0.3, (W / 2, 520), '/', anton(100), GREY)
    txt(can, t, w('Lauri', 336) + 0.5, (W / 2 + 380, 520), 'LARRY THORNE', anton(100), YEL)
    txt(can, t, w('Lauri', 336) + 0.9, (W / 2, 680), '?', anton(200), WHITE)
    txt(can, t, w('Schreibt', 336), (W / 2, 900), 'SCHREIBT ES IN DIE KOMMENTARE', bebas(70), CREAM); return can

sys.path.insert(0, B + '../logo'); sys.argv_ = list(sys.argv)
import importlib.util as _iu
_sp = _iu.spec_from_file_location('anim2', B + '../logo/anim2.py'); _an = _iu.module_from_spec(_sp); _sv = sys.argv; sys.argv = ['x', B + '../logo']; _sp.loader.exec_module(_an); sys.argv = _sv
def s_sub(t, w0, w1):         # channel logo animation, starts with "abonniert Chronik der Macht"
    return _an.frame(max(0.0, t - LOGO_T)).convert('RGBA')
SCN = [(0.0, s_date), (3.25, s_heli), (6.6, s_thorne), (11.8, s_years), (15.75, s_three), (27.9, s_name),
       (33.3, s_born), (42.0, s_viipuri), (47.65, s_1938), (51.2, s_attack), (57.9, s_winter), (62.0, s_motti), (66.9, s_lt), (72.7, s_lost),
       (78.85, s_wien), (90.4, s_cont), (95.7, s_abt), (103.5, s_raid), (110.9, s_bounty), (117.7, s_ilom), (125.4, s_koiv), (132.9, s_mhk),
       (140.7, s_armist), (146.6, s_notover), (154.6, s_germ), (161.6, s_ss45), (172.1, s_escape), (177.4, s_akte), (182.4, s_verdict),
       (186.1, s_prison), (193.6, s_paasi),
       (200.2, s_nofut), (203.0, s_sea), (221.4, s_lodge), (231.0, s_rename), (239.2, s_sf), (245.8, s_iran), (250.1, s_zagros),
       (263.7, s_vn), (268.2, s_secret), (276.8, s_crash), (292.2, s_missing), (299.1, s_found), (305.9, s_arl),
       (317.1, s_outro3), (322.3, s_view), (331.0, s_story), (340.1, s_ask), (344.4, s_sub)]
LOGO_T = w('abonniert', 340) - 0.25
SCN = [((LOGO_T if fn is s_sub else (0.0 if s == 0 else M(s) - 0.05)), fn) for s, fn in SCN]
T = LOGO_T + 6.0
OV = 0.4
SC = [(0 if i == 0 else s - OV, T if i == len(SCN) - 1 else SCN[i + 1][0] + OV, fn) for i, (s, fn) in enumerate(SCN)]
def frame(t): return assemble(SC, t, T)

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; P_ = Image.new('RGB', (4 * 480, ((len(ts) + 3) // 4) * 270))
        for i, t in enumerate(ts): P_.paste(frame(t).resize((480, 270)), ((i % 4) * 480, (i // 4) * 270))
        P_.save(B + sys.argv[2], quality=85); sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '8M', '-maxrate', '10M', '-bufsize', '16M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
