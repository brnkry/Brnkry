# Adalbert Schnee Shorts: photo-led, horizontal position moves (CapCut style), Kammhuber palette
import sys, math, subprocess
import base
from base import *

TEND = 114.29

# ---------- blur spots (source px: x, y, diameter) ----------
base.BLUR.clear()
_BL = {

    's01': [(1605, 330, 110), (1549, 640, 110), (1383, 960, 90), (1704, 1064, 90), (1708, 1150, 90)],
    's06': [(347, 720, 90), (227, 1060, 130), (800, 940, 130), (1315, 1140, 130)],
    's08': [(826, 140, 170), (612, 1453, 170), (168, 2205, 130), (1101, 2431, 120), (1101, 2676, 120)],
    's11': [(947, 70, 160)],
    's12': [(605, 1580, 140)],
    's13': [(773, 493, 100)],
    's14': [(520, 1253, 110), (1053, 680, 90), (1640, 720, 80), (1267, 720, 70), (467, 920, 70), (907, 840, 70),
            (1347, 813, 60), (1547, 840, 60), (600, 747, 60), (1067, 933, 70)],
    's15': [(1248, 490, 100), (1257, 815, 110), (1082, 1040, 100), (1389, 1230, 90), (1389, 1310, 80)],
    's16': [(808, 250, 110), (597, 968, 130), (353, 1390, 120), (854, 1537, 90), (843, 1600, 80)],
    's17': [(920, 1240, 160), (520, 1840, 130), (1339, 2133, 120), (1339, 2320, 110)],
    's18': [(779, 170, 140), (867, 2013, 180)],
    's19': [(960, 170, 140), (787, 2133, 210)],
    's21': [(408, 1723, 80), (1467, 830, 110), (2253, 67, 100), (1507, 293, 80), (1107, 493, 80)],
    's03': [(489, 352, 90), (1336, 413, 90), (1890, 428, 80), (2171, 437, 80)],
    's07': [(947, 110, 150)],
    's20': [(960, 125, 120)],
}
base.BLUR.update({k: [(x, y, d * 1.35) for x, y, d in v] for k, v in _BL.items()})

# ---------- photo motion ----------
def pan(p, t, t0, t1, x0, x1, zoom=1.0):
    """full-height photo whose horizontal position moves from x0 to x1 (source px centre), like a CapCut position keyframe"""
    im = src(p); w = min(im.width, im.height * 9 / 16) / zoom
    u = eio((t - t0) / max(0.1, t1 - t0)) * 0.85 + clamp((t - t0) / max(0.1, t1 - t0)) * 0.15
    return PCam(p, lerp(x0, x1, u), im.height / 2, w)
def zoomcam(p, t, t0, t1, cx, cy, z0=1.0, z1=1.06):
    im = src(p); w0 = min(im.width, im.height * 9 / 16)
    u = eio((t - t0) / max(0.1, t1 - t0)); return PCam(p, cx, cy, w0 / lerp(z0, z1, u))
def shot(c, grad=GRAD):
    can = c.frame(); can.alpha_composite(grad); return can

def bigname(can, t, t0, l1, l2, y1=1240, y2=1410, size=170):
    if t < t0: return
    focus(can, t, t0, l1, 'serif', size, CREAM, y1, dur=0.35)
    focus(can, t, t0 + 0.18, l2, 'serif', size + 20, GOLD, y2, dur=0.35)

# ---------- extra overlays ----------
def counter(can, t, t0, n, cy, size=260, col=GOLD, dur=1.2, suffix=''):
    if t < t0: return
    k = eout((t - t0) / dur); v = int(round(n * k))
    put(can, sprite(f'{v}{suffix}', 'serif', size, col), 540, cy, lerp(1.15, 1.0, eout((t - t0) / 0.3)), clamp((t - t0) / 0.15))

def bars(can, t, t0, cy=1200):
    if t < t0: return
    rows = (('TYP XXI UNTER WASSER', 17, GOLD), ('GELEITZUG', 8, CREAM))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((120, cy - 150, 920, cy + 230), fill=(8, 10, 14, 190))
    for i, (lab, kn, col) in enumerate(rows):
        k = eio((t - t0 - i * 0.35) / 0.8); y = cy - 80 + i * 180
        put(L, sprite(lab, 'cond', 46, col, False, 2), 160, y - 40, anchor='l')
        d.rectangle((160, y, 160 + 700 * kn / 17 * k, y + 50), fill=col + (255,))
        if k > 0.95: put(L, sprite(f'{kn} KN', 'serif', 54, DEEP if kn > 10 else CREAM, False), 160 + 700 * kn / 17 - 80 if kn > 10 else 160 + 700 * kn / 17 + 80, y + 25)
    a = clamp((t - t0) / 0.3); L.putalpha(L.getchannel('A').point(lambda v: int(v * a))); can.alpha_composite(L)

def magnifier(can, t, t0, cam, sx, sy, box=380, R=270, cx=540, cy=820):
    """round loupe that enlarges a detail of the photo, with a leader line to where it sits"""
    if t < t0: return
    k = eout((t - t0) / 0.45)
    reg = src(cam.p).crop((sx - box / 2, sy - box / 2, sx + box / 2, sy + box / 2)).resize((2 * R, 2 * R), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', (2 * R, 2 * R), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * R - 1, 2 * R - 1), fill=255); reg.putalpha(m)
    px, py = cam.pt(sx, sy); py = min(py, H - 40)
    stroke(can, partial([(cx, cy + R), (px, py)], k), GOLD, 5)
    ring_l = Image.new('RGBA', (2 * R + 60, 2 * R + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(ring_l)
    d.ellipse((10, 18, 2 * R + 50, 2 * R + 58), fill=(0, 0, 0, 160)); ring_l = ring_l.filter(ImageFilter.GaussianBlur(12))
    ring_l.alpha_composite(reg, (30, 30)); d = ImageDraw.Draw(ring_l); d.ellipse((24, 24, 2 * R + 36, 2 * R + 36), outline=GOLD + (255,), width=10)
    put(can, ring_l, cx, cy, lerp(0.3, 1.0, k), k)

def typecard(can, t, t0, lines, cy=900, step=0.055):
    if t < t0: return
    k = eout((t - t0) / 0.35)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((110, cy - 230, 970, cy + 230), fill=(222, 211, 186, int(245 * k))); d.rectangle((126, cy - 214, 954, cy + 214), outline=(120, 100, 70, int(255 * k)), width=3)
    can.alpha_composite(L)
    n = int((t - t0 - 0.3) / step); i = 0
    for li, (txt, size, col) in enumerate(lines):
        shown = txt[:max(0, n - i)]; i += len(txt)
        if shown: put(can, sprite(shown, 'type', size, col, False), 540 - (textw(txt, 'type', size) - textw(shown, 'type', size)) / 2, cy - 120 + li * 120)

def sonar(can, t, t0, t1, cy=860):
    """range closing: rings and a falling distance readout ending at 500 m"""
    if t < t0: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse((540 - 380, cy - 380, 540 + 380, cy + 380), fill=(4, 8, 10, 150))
    for j in range(3):
        u = ((t - t0) * 0.6 + j / 3) % 1.0
        r = 40 + 340 * u; d.ellipse((540 - r, cy - r, 540 + r, cy + r), outline=CREAM + (int(170 * (1 - u)),), width=3)
    d.line((540 - 380, cy, 540 + 380, cy), fill=CREAM + (60,), width=2); d.line((540, cy - 380, 540, cy + 380), fill=CREAM + (60,), width=2)
    k = eio((t - t0) / max(0.1, t1 - t0)); dist = int(round(lerp(3000, 500, k) / 50) * 50)
    ang = -math.pi / 2 + 0.6; rr = lerp(330, 70, k); tx, ty = 540 + rr * math.cos(ang), cy + rr * math.sin(ang)
    d.ellipse((tx - 14, ty - 14, tx + 14, ty + 14), fill=RUST + (255,))
    d.ellipse((540 - 12, cy - 12, 540 + 12, cy + 12), fill=GOLD + (255,))
    a = clamp((t - t0) / 0.3); L.putalpha(L.getchannel('A').point(lambda v: int(v * a))); can.alpha_composite(L)
    put(can, sprite(f'{dist} M', 'serif', 150, GOLD if dist > 500 else RUST), 540, cy + 470, 1.0, a)

def desat(can, k):
    if k <= 0: return can
    g = can.convert('L').convert('RGBA'); return Image.blend(can, g, k)

# ---------- scenes (21 photos, each used once; CTA stays on the last one) ----------
def s01(t):   # hook
    c = pan('s09', t, -0.2, 7.2, 820, 980); can = shot(c, GRAD_SOFT)
    tA = wt('Adalbert') - 0.1
    focus(can, t, 0.05, '500 METER', 'serif', 230, GOLD, 1200, t1=tA - 0.15, dur=0.3)
    reveal(can, t, wt('britischen') - 0.1, 'VOR EINEM BRITISCHEN KREUZER', 'cond', 62, CREAM, 1330, t1=tA - 0.15, dur=0.45)
    plate(can, t, wt('Befehl') - 0.05, 'NICHT MEHR SCHIESSEN', 1450, size=56, bg=RUST, fg=CREAM, t1=tA - 0.15)
    bigname(can, t, tA, 'ADALBERT', 'SCHNEE')
    return can
def s02(t):
    c = pan('s12', t, 6.7, 11.1, 1000, 760); can = shot(c)
    plate(can, t, wt('1913'), 'BERLIN · 1913', 1400, size=60)
    return can
def s03(t):
    c = zoomcam('s08', t, 10.7, 14.9, 768, 1376); can = shot(c)
    plate(can, t, wt('1934'), 'MARINE · 1934', 1400, size=60)
    return can
def s04(t):
    c = pan('s18', t, 14.5, 21.1, 760, 1030); can = shot(c)
    plate(can, t, wt('Otto'), 'OTTO KRETSCHMER', 1300, size=64)
    reveal(can, t, wt('U-23'), 'U-23 · WACHOFFIZIER', 'cond', 64, GOLD, 1420)
    return can
def s05(t):
    c = pan('s02', t, 20.7, 26.3, 1100, 760); can = shot(c)
    focus(can, t, wt('1941'), '1941', 'cond', 70, CREAM, 1180)
    focus(can, t, wt('U-201.'), 'U-201', 'serif', 220, GOLD, 1350, dur=0.3)
    return can
def s06(t):
    c = pan('s21', t, 25.9, 31.8, 900, 1500); can = shot(c, GRAD_SOFT)
    magnifier(can, t, wt('Schneemann'), c, 420, 1690)
    focus(can, t, wt('Anspielung'), 'SCHNEE  =  SCHNEEMANN', 'serif', 92, CREAM, 1300)
    return can
def s07(t):
    c = pan('s07', t, 31.4, 36.0, 1500, 950); can = shot(c)
    reveal(can, t, wt('bekanntesten'), 'EINES DER BEKANNTESTEN', 'cond', 62, CREAM, 1300)
    reveal(can, t, wt('Bootswappen'), 'BOOTSWAPPEN', 'serif', 120, GOLD, 1420)
    return can
def s08(t):
    c = pan('s14', t, 35.6, 39.8, 820, 1050); can = shot(c)
    counter(can, t, wt('21', 35), 21, 1230)
    plate(can, t, wt('versenkte'), 'VERSENKTE HANDELSSCHIFFE', 1420, size=52)
    return can
def s09(t):
    c = pan('s06', t, 39.4, 46.6, 1050, 760); can = shot(c)
    callout(can, t, wt('Dönitz'), c.pt(800, 420), (540, 1300), 'KARL DÖNITZ', col=GOLD, size=60)
    plate(can, t, wt('Geleitzüge') - 0.3, 'PLANUNG GEGEN GELEITZÜGE', 1430, size=48, bg=RUST, fg=CREAM)
    return can
def s10(t):
    c = pan('s03', t, 46.2, 51.6, 700, 1800); can = shot(c)
    focus(can, t, wt('völlig'), 'VÖLLIG NEUES BOOT', 'cond', 66, CREAM, 1180, t1=wt('Typ') - 0.2)
    focus(can, t, wt('Typ'), 'TYP XXI', 'serif', 220, GOLD, 1250)
    reveal(can, t, wt('tagelang'), 'TAGELANG GETAUCHT', 'cond', 64, CREAM, 1420)
    return can
def s11(t):
    c = pan('s04', t, 51.2, 56.7, 2200, 1500); can = shot(c, GRAD_SOFT)
    bars(can, t, wt('schneller') - 0.2, 1180)
    return can
def s12(t):
    c = pan('s17', t, 56.3, 62.8, 760, 1030); can = shot(c)
    focus(can, t, wt('U-2511,'), 'U-2511', 'serif', 220, GOLD, 1270, dur=0.3)
    plate(can, t, wt('erste'), 'ERSTE FEINDFAHRT DES TYPS XXI', 1430, size=46)
    return can
def s13(t):
    c = pan('s13', t, 62.4, 67.8, 1050, 760); can = shot(c)
    focus(can, t, wt('Bergen', 62), 'BERGEN', 'serif', 190, CREAM, 1240)
    plate(can, t, wt('April'), '30. APRIL 1945', 1400, size=60, bg=GOLD, fg=DEEP)
    return can
def s14(t):
    c = pan('s20', t, 67.4, 72.9, 760, 1040); can = shot(c, GRAD_SOFT)
    typecard(can, t, wt('Befehl', 67), [('4. MAI 1945', 52, SEPIA), ('ALLE ANGRIFFE', 80, INK), ('EINSTELLEN', 80, RUST)], cy=1180)
    return can
def s15(t):
    c = pan('s16', t, 72.5, 78.5, 1400, 650); can = shot(c)
    reveal(can, t, wt('berichtete'), 'NACH SCHNEES BERICHT', 'cond', 52, CREAM, 1290)
    plate(can, t, wt('Norfolk'), 'KREUZER NORFOLK', 1410, size=64, bg=RUST, fg=CREAM)
    return can
def s16(t):
    c = pan('s11', t, 78.1, 83.5, 760, 1030); can = shot(c, GRAD_SOFT)
    can.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(110 * clamp((t - 78.2) / 0.5)))))
    sonar(can, t, wt('glitt'), wt('Meter', 80) + 0.2)
    return can
def s17(t):
    c = pan('s01', t, 83.1, 88.6, 1500, 800); can = shot(c)
    focus(can, t, wt('Übungsangriff'), 'ÜBUNGSANGRIFF', 'serif', 130, CREAM, 1260)
    plate(can, t, wt('ohne'), 'KEIN SCHUSS', 1410, size=70, bg=GOLD, fg=DEEP)
    return can
def s18(t):
    c = pan('s19', t, 88.2, 95.6, 1000, 760); can = shot(c)
    can = desat(can, 0.85 * clamp((t - wt('Geschichte', 88)) / 1.2))
    focus(can, t, wt('fast'), 'NUR SEINE EIGENE AUSSAGE', 'cond', 60, CREAM, 1240, t1=wt('Historiker') - 0.2)
    seal(can, t, wt('Historiker'), 'UMSTRITTEN', 540, 1300, r=210, col=RUST, rot=-10)
    return can
def s19(t):
    c = pan('s15', t, 95.2, 100.4, 1300, 750); can = shot(c)
    focus(can, t, wt('9.'), '9. MAI 1945', 'serif', 150, GOLD, 1260)
    plate(can, t, wt('übergab'), 'ÜBERGABE IN BERGEN', 1420, size=58)
    return can
def s20(t):
    c = pan('s05', t, 100.0, 107.1, 1100, 1900); can = shot(c, GRAD_SOFT)
    plate(can, t, wt('Elba'), 'SEGELSCHULE AUF ELBA', 1290, size=56)
    plate(can, t, wt('Verband'), 'VERBAND DER U-BOOT-FAHRER', 1410, size=48, bg=GOLD, fg=DEEP)
    return can
def s21(t):
    c = zoomcam('s22', t, 106.7, TEND, 896, 1150, 1.0, 1.07); can = shot(c)
    tk = wt('Kanntet')
    focus(can, t, wt('1982') - 0.1, '1913 · 1982', 'serif', 170, CREAM, 1300, t1=tk - 0.2)
    focus(can, t, tk, 'KANNTET IHR', 'serif', 120, CREAM, 1210)
    focus(can, t, wt('diese', 109), 'DIESE GESCHICHTE?', 'serif', 120, GOLD, 1340)
    plate(can, t, wt('Schreibt'), 'SCHREIBT ES IN DIE KOMMENTARE!', 1460, size=46)
    return can

SC = [(0.0, 7.0, s01, 'cut'), (6.8, 11.1, s02, 'fade'), (10.9, 14.9, s03, 'fade'), (14.6, 21.1, s04, 'slide_l'),
      (20.8, 26.3, s05, 'fade'), (25.9, 31.8, s06, 'fade'), (31.5, 36.0, s07, 'slide_r'), (35.7, 39.8, s08, 'fade'),
      (39.5, 46.6, s09, 'fade'), (46.3, 51.6, s10, 'slide_l'), (51.3, 56.7, s11, 'fade'), (56.4, 62.8, s12, 'fade'),
      (62.5, 67.8, s13, 'slide_r'), (67.5, 72.9, s14, 'fade'), (72.6, 78.5, s15, 'fade'), (78.2, 83.5, s16, 'dip'),
      (83.2, 88.6, s17, 'fade'), (88.3, 95.6, s18, 'fade'), (95.3, 100.4, s19, 'slide_l'), (100.1, 107.1, s20, 'fade'),
      (106.8, TEND, s21, 'fade')]

DIPC = Image.new('RGBA', (W, H), (4, 6, 8, 255))
def frame(t):
    act = [s for s in SC if s[0] <= t < s[1]] or [SC[-1]]
    if len(act) == 1: img = act[0][2](t)
    else:
        a, b = act[0], act[1]; u = ease((t - b[0]) / (a[1] - b[0])); tr = b[3]
        if tr in ('slide_l', 'slide_r'):
            A = a[2](t); B_ = b[2](t); s = 1 if tr == 'slide_l' else -1; off = int(W * u)
            img = Image.new('RGBA', (W, H), (0, 0, 0, 255)); img.paste(A, (-s * off, 0)); img.paste(B_, (s * (W - off), 0))
        elif tr == 'cut': img = b[2](t) if u > 0.5 else a[2](t)
        elif tr == 'dip':
            img = Image.blend(a[2](t), DIPC, min(1, u * 2)) if u < 0.5 else Image.blend(DIPC, b[2](t), (u - 0.5) * 2)
        else: img = Image.blend(a[2](t), b[2](t), u)
    img.alpha_composite(VIG)
    if t > TEND - 0.6: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * clamp((t - TEND + 0.6) / 0.5)))))
    return img.convert('RGB')

GR = [np.random.default_rng(i).normal(0, 4.0, (H // 2, W // 2)).astype(np.int16) for i in range(6)]
def grain(img, n):
    a = np.asarray(img).astype(np.int16); g = np.kron(GR[n % 6], np.ones((2, 2), np.int16))[..., None]
    return Image.fromarray(np.clip(a + g, 0, 255).astype(np.uint8))
def ui_overlay(im):
    im = im.convert('RGBA'); L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((0, 0, W, 290), fill=(255, 0, 0, 60)); d.rectangle((930, 680, W, 1580), fill=(255, 0, 0, 80)); d.rectangle((0, 1580, W, H), fill=(255, 0, 0, 80))
    im.alpha_composite(L); return im.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; ims = [ui_overlay(frame(t)).resize((270, 480)) for t in ts]
        cols = 6; rows = (len(ims) + cols - 1) // cols; S = Image.new('RGB', (270 * cols, 480 * rows))
        for i, im in enumerate(ims):
            S.paste(im, ((i % cols) * 270, (i // cols) * 480)); ImageDraw.Draw(S).text(((i % cols) * 270 + 4, (i // cols) * 480 + 4), f'{ts[i]}', fill=(0, 255, 0))
        S.save(B + sys.argv[2], quality=90)
    elif sys.argv[1] == 'still':
        frame(float(sys.argv[3])).save(B + sys.argv[2], quality=92)
    else:
        out = sys.argv[2]; a, b = float(sys.argv[3]), float(sys.argv[4]); big = len(sys.argv) > 5 and sys.argv[5] == '4k'
        size = '2160x3840' if big else f'{W}x{H}'
        G4 = [np.random.default_rng(i).normal(0, 4.0, (1920, 1080)).astype(np.int16) for i in range(6)] if big else None
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', size, '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
        for n in range(int(round(a * FPS)), int(round(b * FPS))):
            if big:
                im = frame(n / FPS).resize((2160, 3840), Image.LANCZOS)
                arr = np.asarray(im).astype(np.int16) + np.kron(G4[n % 6], np.ones((2, 2), np.int16))[..., None]
                p.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
            else: p.stdin.write(grain(frame(n / FPS), n).tobytes())
        p.stdin.close(); p.wait(); print('rc', p.returncode)
