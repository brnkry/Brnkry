# Törni long video, intro + chapter 1 (voice 12.mp3, 82 s)
import sys, subprocess
from lib import *

T = 81.95
LADOGA = [(30.85, 61.63), (30.45, 61.42), (30.05, 61.05), (29.98, 60.75), (30.45, 60.42), (31.0, 60.08), (31.6, 59.95), (32.4, 60.1), (32.85, 60.5),
          (32.75, 60.9), (32.4, 61.15), (31.9, 61.4), (31.4, 61.62)]
CEDED = [(27.75, 60.52), (28.6, 61.0), (29.3, 61.3), (29.9, 61.55), (30.5, 61.95), (30.75, 62.25), (31.1, 62.55), (31.4, 62.95), (31.9, 63.05), (32.9, 62.55),
         (32.95, 61.85), (32.4, 61.15), (31.9, 61.3), (30.95, 60.55), (30.0, 60.15), (29.4, 60.2), (28.6, 60.45)]
VIIPURI = (28.75, 60.71); LEMETTI = (31.62, 61.78)
FIN = Map(28.5, 63.9, 34.0, hi=('Finland',), extra=((LADOGA, SEA),))
KAR = Map(31.4, 61.78, 7.5, hi=('Finland',), extra=((LADOGA, SEA),))
KAR2 = Map(29.6, 61.75, 13.0, hi=('Finland',), extra=((LADOGA, SEA),))
VN = Map(107.6, 15.75, 5.5, hi=('Vietnam',))

# ---------- intro ----------
def s_date(t, w0, w1):        # Am 18. Oktober 1965 ... Vietnam
    can = shade(dim(pan('t16', t, w0, w1, -1, 0.55), 50), 220)
    typewriter(can, t, 0.25, (W / 2, 820), '18. OKTOBER 1965', typew(88), CREAM, 0.075)
    txt(can, t, wt('Vietnams'), (W / 2, 940), 'VIETNAM', anton(84), YEL)
    return can
def s_heli(t, w0, w1):        # the helicopter disappears
    z = lerp(1.0, 1.12, clamp((t - w0) / (w1 - w0))); can = VN.frame(z)
    kd, dn, laos, crash = VN.p(107.80, 15.45, z), VN.p(108.22, 16.07, z), VN.p(107.0, 15.62, z), VN.p(107.93, 15.78, z)
    dot(can, *dn, WHITE, 10); label(can, t, w0 + 0.2, dn[0] + 26, dn[1] - 4, 'DA NANG', 62)
    dot(can, *kd, YEL, 12); label(can, t, w0 + 0.3, kd[0] + 28, kd[1] + 6, 'KHAM DUC', 62, YEL)
    label(can, t, w0 + 0.3, laos[0] - 30, laos[1] - 90, 'LAOS', 90, GREY, 'rm')
    dashed(can, [kd, laos], eio((t - w0 - 0.2) / 1.6))
    ring(can, t, wt('Hubschrauber') - 0.2, *crash)
    label(can, t, wt('Hubschrauber') + 0.2, crash[0] - 70, crash[1] - 80, 'VERSCHOLLEN', 76, RED, 'rm')
    return can
def s_thorne(t, w0, w1):      # Hauptmann der Special Forces: Larry Thorne
    can = shade(fit('t18', t, w0, w1, 1.04, 0.0), 230, 0.45)
    txt(can, t, wt('Hauptmann'), (W / 2, 830), 'HAUPTMANN DER US SPECIAL FORCES', bebas(70), CREAM)
    words(can, t, [('LARRY', WHITE, wt('Larry')), ('THORNE', YEL, wt('Thorne'))], 950, 130)
    return can
def s_years(t, w0, w1):       # 34 Jahre später
    can = dim(pan('t10', t, w0, w1, 1), 165).filter(ImageFilter.GaussianBlur(2))
    k = eio((t - wt('34')) / 1.4); y = int(round(lerp(1965, 1999, k)))
    shadowed(can, lambda d: d.text((W / 2, 470), str(y), font=anton(300), fill=WHITE + (255,), anchor='mm'))
    txt(can, t, wt('Jahre', 12), (W / 2, 690), '34 JAHRE SPÄTER', anton(96), YEL)
    txt(can, t, wt('Absturzstelle'), (W / 2, 810), 'DIE ABSTURZSTELLE WIRD GEFUNDEN', bebas(66), CREAM)
    return can
TRI = [('t06', 'FINNLAND', 'Finnland'), ('t22', 'WAFFEN-SS', 'Waffen-SS,'), ('t21', 'US ARMY', 'Army.')]
def s_three(t, w0, w1):       # drei Uniformen
    can = Image.new('RGBA', (W, H), DARK + (255,)); pw = W // 3
    for i, (n, lab, word) in enumerate(TRI):
        ti = wt(word, 20) - 0.25
        if t < ti: continue
        k = eout((t - ti) / 0.55); im = src(n)
        z = lerp(1.0, 1.04, clamp((t - ti) / 9)); w = min(im.width, im.height * pw / H) / z; h = w * H / pw; cy = min(max(im.height * 0.5, h / 2), im.height - h / 2)
        ph = im.resize((pw, H), Image.BILINEAR, box=(im.width / 2 - w / 2, cy - h / 2, im.width / 2 + w / 2, cy + h / 2)).convert('RGBA')
        ph.putalpha(int(255 * k)); can.alpha_composite(ph, (i * pw, int((1 - k) * 60)))
        if i: ImageDraw.Draw(can).line((i * pw, 0, i * pw, H), fill=DARK, width=8)
    shade(can, 200, 0.6)
    for i, (n, lab, word) in enumerate(TRI): txt(can, t, wt(word, 20) - 0.05, (i * pw + pw / 2, 960), lab, anton(70), YEL if i != 1 else WHITE)
    words(can, t, [('DREI', WHITE, wt('drei', 18)), ('UNIFORMEN', YEL, wt('Uniformen'))], 110, 96)
    return can
def s_name(t, w0, w1):        # in seiner Heimat: Lauri Törni
    can = shade(pan('t09', t, w0, w1, -1, 0.42, 1.25), 230, 0.45)
    txt(can, t, wt('Heimat'), (W / 2, 800), 'IN SEINER HEIMAT HIESS ER', bebas(70), CREAM)
    words(can, t, [('LAURI', WHITE, wt('Lauri', 32)), ('TÖRNI', YEL, wt('Törni', 33))], 935, 150)
    return can

# ---------- chapter 1: Viipuri und der Winterkrieg ----------
def s_born(t, w0, w1):        # chapter card, born 28 May 1919
    can = dim(fit('t06', t, w0, w1, 1.05, 0.0), 150 * (1 - clamp((t - w0 - 2.4) / 0.6)))
    chapter(can, t, w0 + 0.3, 1, 'VIIPURI UND DER WINTERKRIEG', wt('wurde', 36) - 0.3)
    shade(can, int(220 * clamp((t - wt('28.') + 0.5) / 0.5)), 0.5)
    typewriter(can, t, wt('28.'), (W / 2, 860), '28. MAI 1919', typew(84), CREAM, 0.08)
    txt(can, t, wt('Viipuri', 40), (W / 2, 970), 'VIIPURI, KARELIEN', anton(80), YEL)
    return can
def s_viipuri(t, w0, w1):     # then Finland, today Russia
    z = lerp(1.0, 1.15, eio((t - w0) / (w1 - w0))); can = KAR2.frame(z)
    vx, vy = KAR2.p(*VIIPURI, z); ced = [KAR2.p(*q, z) for q in CEDED]
    k = eio((t - wt('heute') - 0.1) / 0.9)
    poly_fill(can, ced, YEL, 90 * (1 - k)); poly_fill(can, ced, RED, 150 * k)
    ImageDraw.Draw(can).polygon([KAR2.p(*q, z) for q in LADOGA], fill=SEA, outline=BORDER)
    dot(can, vx, vy, YEL, 12)
    old = 1 - clamp((t - wt('Wyborg') + 0.2) / 0.3)
    if old > 0: label(can, t, w0 + 0.2, vx - 34, vy - 6, 'VIIPURI', 68, YEL, 'rm', wt('Wyborg') - 0.2)
    label(can, t, wt('Wyborg'), vx - 34, vy - 6, 'WYBORG', 68, CREAM, 'rm')
    label(can, t, w0 + 0.4, *KAR2.p(26.0, 62.6, z), 'FINNLAND', 80, CREAM, 'mm')
    label(can, t, wt('Russland') - 0.1, *KAR2.p(34.6, 62.6, z), 'RUSSLAND', 80, GREY, 'mm')
    txt(can, t, wt('Damals'), (W / 2, 110), 'DAMALS FINNLAND', anton(76), YEL, wt('heute'))
    txt(can, t, wt('heute') + 0.1, (W / 2, 110), 'HEUTE RUSSLAND', anton(76), RED)
    return can
def s_1938(t, w0, w1):        # 1938 Wehrdienst
    can = shade(fit('t23', t, w0, w1, 1.05), 220, 0.5)
    txt(can, t, wt('1938'), (W / 2, 840), '1938', anton(170), YEL)
    txt(can, t, wt('Wehrdienst'), (W / 2, 975), 'WEHRDIENST', bebas(80), WHITE)
    return can
ATT = [((31.6, 60.0), (29.4, 60.7)), ((35.0, 61.9), (32.0, 61.9)), ((34.0, 65.0), (29.6, 64.9)), ((33.0, 67.0), (29.2, 66.9)), ((33.5, 69.6), (30.4, 69.3))]
def s_attack(t, w0, w1):      # November 1939: the Soviet Union attacks
    can = FIN.frame(1.0)
    label(can, t, w0 + 0.3, *FIN.p(25.5, 63.5), 'FINNLAND', 80, CREAM, 'mm')
    label(can, t, w0 + 0.3, *FIN.p(36.5, 63.5), 'SOWJETUNION', 80, GREY, 'mm')
    ta = wt('griff') - 0.2
    for i, (a, b) in enumerate(ATT): arrow(can, FIN.p(*a), FIN.p(*b), eio((t - ta - i * 0.18) / 0.8), RED, 22, 60)
    typewriter(can, t, wt('November'), (400, 110), 'NOVEMBER 1939', typew(76), CREAM, 0.07)
    txt(can, t, wt('Sowjetunion', 57) + 0.3, (W / 2, 960), 'WINTERKRIEG', anton(110), YEL)
    return can
def s_winter(t, w0, w1):      # fought north of Lake Ladoga
    can = shade(fit('t04', t, w0, w1, 1.05), 220, 0.55)
    txt(can, t, wt('Winterkrieg') + 0.1, (W / 2, 900), 'WINTERKRIEG 1939/40', anton(96), WHITE)
    txt(can, t, wt('Ladogasees') - 0.2, (W / 2, 1000), 'NÖRDLICH DES LADOGASEES', bebas(66), YEL)
    return can
def s_motti(t, w0, w1):       # the encirclement at Lemetti
    z = lerp(1.0, 1.25, eio((t - w0) / (w1 - w0))); can = KAR.frame(z)
    lx, ly = KAR.p(*LEMETTI, z); lad = KAR.p(31.7, 61.05, z)
    label(can, t, w0 + 0.2, *lad, 'LADOGASEE', 64, GREY, 'mm')
    k = eout((t - wt('Lemetti') + 0.1) / 0.5)
    if k > 0:   # Soviet column inside the pocket
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for i in range(5): d.rounded_rectangle((lx - 120 + i * 50, ly - 18, lx - 85 + i * 50, ly + 18), 6, fill=RED + (int(230 * k),))
        can.alpha_composite(L)
    te = wt('eingekesselte') - 0.1
    for i, ang in enumerate(range(0, 360, 60)):   # Finnish arrows closing the ring
        a = math.radians(ang); r0, r1 = 330 * z, 165 * z
        arrow(can, (lx + r0 * math.cos(a), ly + r0 * math.sin(a)), (lx + r1 * math.cos(a), ly + r1 * math.sin(a)), eio((t - te - i * 0.08) / 0.7), YEL, 12, 36)
    if t > te + 0.8:
        kk = eio((t - te - 0.8) / 0.8); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); r = 150 * z
        ImageDraw.Draw(L).arc((lx - r, ly - r, lx + r, ly + r), -90, -90 + 360 * kk, fill=YEL + (255,), width=10); can.alpha_composite(L)
    label(can, t, wt('Lemetti'), lx + 230 * z, ly - 135 * z, 'LEMETTI', 80, YEL, 'lm')
    txt(can, t, wt('zerschlugen') - 0.2, (W / 2, 110), 'EINGEKESSELT UND ZERSCHLAGEN', anton(76), WHITE)
    return can
def s_lt(t, w0, w1):          # March 1940, lieutenant of the reserve
    can = shade(pan('t03', t, w0, w1, -1, 0.45, 1.15), 220, 0.5)
    typewriter(can, t, wt('März', 70), (W / 2, 850), 'MÄRZ 1940', typew(84), CREAM, 0.08)
    txt(can, t, wt('Leutnant'), (W / 2, 975), 'LEUTNANT DER RESERVE', anton(90), YEL)
    return can
def s_lost(t, w0, w1):        # Karelia lost, Viipuri too
    z = 1.15; can = KAR2.frame(z); ced = [KAR2.p(*q, z) for q in CEDED]; vx, vy = KAR2.p(*VIIPURI, z)
    k = eio((t - wt('Teile', 77) + 0.2) / 0.9); poly_fill(can, ced, RED, 160 * k)
    ImageDraw.Draw(can).polygon([KAR2.p(*q, z) for q in LADOGA], fill=SEA, outline=BORDER)
    label(can, t, wt('Kareliens', 77), *KAR2.p(32.0, 62.2, z), 'KARELIEN', 70, WHITE, 'mm')
    txt(can, t, wt('abgeben') - 0.1, (W / 2, 110), 'AN DIE SOWJETUNION ABGETRETEN', anton(76), RED)
    if t > wt('Viipuri', 79) - 0.2: ring(can, t, wt('Viipuri', 79) - 0.2, vx, vy, YEL, 30, False)
    dot(can, vx, vy, YEL, 12); label(can, t, wt('Viipuri', 79) - 0.1, vx - 40, vy - 6, 'VIIPURI', 72, YEL, 'rm')
    return can

SCN = [(0.0, s_date), (3.3, s_heli), (6.9, s_thorne), (12.4, s_years), (16.8, s_three), (29.0, s_name),
       (35.0, s_born), (43.8, s_viipuri), (49.9, s_1938), (53.5, s_attack), (60.4, s_winter), (64.5, s_motti), (69.9, s_lt), (75.9, s_lost)]
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
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '16M', '-maxrate', '20M', '-bufsize', '30M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
