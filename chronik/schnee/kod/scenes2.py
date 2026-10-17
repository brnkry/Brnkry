# Adalbert Schnee v2: no blur, shortened pauses, continuous photo motion through every transition, more translucent graphics
import sys, math, json, subprocess
import base
from base import *
import scenes as S1
from scenes import counter, bars, magnifier, typecard, sonar, desat, bigname, shot
base.BLUR.clear()                       # Boran blurs the symbols himself
# hook photo: the face sits at the very top, so extend the plain sky upward to bring it below the Shorts top bar
_s20 = Image.open(IMG + 's20.jpg').convert('RGB'); _pad = 520
_top = _s20.crop((0, 0, _s20.width, 60)).resize((_s20.width, _pad), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
_ext = Image.new('RGB', (_s20.width, _s20.height + _pad)); _ext.paste(_top, (0, 0)); _ext.paste(_s20, (0, _pad))
_m = Image.new('L', (_s20.width, 120), 0); [_m.paste(int(255 * (1 - i / 119)), (0, i, _s20.width, i + 1)) for i in range(120)]
_ext.paste(_top.crop((0, _pad - 120, _s20.width, _pad)), (0, _pad), _m)
base.src.cache_clear()
_orig_src = base.src.__wrapped__
@functools.lru_cache(None)
def _src(p): return _ext if p == 's20' else _orig_src(p)
base.src = _src; src = _src
base.WORDS[:] = json.load(open(B + 'words_cut.json'))
import mapx
from mapx import draw_map, Cam, merc, route, ink_dot, maplabel, icon, heading

TMAP = json.load(open(B + 'timemap.json'))
def M(t):
    for s0, s1, n0 in TMAP:
        if t < s1 + 1e-6: return n0 + max(0.0, t - s0)
    s0, s1, n0 = TMAP[-1]; return n0 + t - s0
TEND = round(M(114.29), 2)

# ---------- motion: constant speed over the whole time the photo is on screen ----------
SPEED = 34.0   # screen px per second, slow
def pan_lin(p, t, w0, w1, fx, d):
    im = src(p); scale = H / im.height; w = min(im.width, im.height * 9 / 16)
    span = SPEED * (w1 - w0) / scale
    lo, hi = w / 2, im.width - w / 2
    a, b = fx - d * span / 2, fx + d * span / 2
    if min(a, b) < lo: sh = lo - min(a, b); a += sh; b += sh
    if max(a, b) > hi: sh = max(a, b) - hi; a -= sh; b -= sh
    u = clamp((t - w0) / (w1 - w0))
    return PCam(p, lerp(a, b, u), im.height / 2, w)
def zoom_lin(p, t, w0, w1, cx, cy, z1=1.06):
    im = src(p); w = min(im.width, im.height * 9 / 16); u = clamp((t - w0) / (w1 - w0))
    return PCam(p, cx, cy, w / lerp(1.0, z1, u))

# ---------- new translucent graphics ----------
def panel(can, box, a=170, r=26):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).rounded_rectangle(box, r, fill=(6, 9, 12, a)); can.alpha_composite(L)

YEARS = [1913, 1934, 1941, 1942, 1945, 1982]
def timeline(can, t, t0, year, prev=None, cy=380):
    """translucent life timeline; the marker slides from the previous year to this one"""
    if t < t0 - 0.4: return
    a = clamp((t - t0 + 0.4) / 0.35)
    x0, x1 = 130, 950
    def X(y): return x0 + (x1 - x0) * (y - 1913) / (1982 - 1913)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((90, cy - 70, 990, cy + 70), 22, fill=(6, 9, 12, int(160 * a)))
    d.line((x0, cy, x1, cy), fill=CREAM + (int(130 * a),), width=4)
    for y in YEARS:
        d.ellipse((X(y) - 7, cy - 7, X(y) + 7, cy + 7), fill=CREAM + (int(160 * a),))
    k = eio((t - t0) / 0.7); xm = lerp(X(prev if prev else year), X(year), k)
    d.line((x0, cy, xm, cy), fill=GOLD + (int(255 * a),), width=8)
    d.ellipse((xm - 16, cy - 16, xm + 16, cy + 16), fill=GOLD + (int(255 * a),))
    can.alpha_composite(L)
    put(can, sprite(str(year), 'serif', 54, GOLD), xm, cy - 50 if xm < 900 else cy - 50, 1.0, a)

def reticle(can, t, t0, cx=540, cy=760, R=330):
    """translucent periscope reticle"""
    if t < t0: return
    a = clamp((t - t0) / 0.4); k = eout((t - t0) / 0.6)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); r = R * lerp(1.3, 1.0, k)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=CREAM + (int(200 * a),), width=5)
    d.ellipse((cx - r * 0.12, cy - r * 0.12, cx + r * 0.12, cy + r * 0.12), outline=GOLD + (int(220 * a),), width=4)
    d.line((cx - r, cy, cx - r * 0.18, cy), fill=CREAM + (int(200 * a),), width=4); d.line((cx + r * 0.18, cy, cx + r, cy), fill=CREAM + (int(200 * a),), width=4)
    d.line((cx, cy - r, cx, cy - r * 0.18), fill=CREAM + (int(200 * a),), width=4); d.line((cx, cy + r * 0.18, cx, cy + r), fill=CREAM + (int(200 * a),), width=4)
    for i in range(1, 6):
        x = cx + i * r / 6; d.line((x, cy - 14, x, cy + 14), fill=CREAM + (int(170 * a),), width=3)
        x = cx - i * r / 6; d.line((x, cy - 14, x, cy + 14), fill=CREAM + (int(170 * a),), width=3)
    can.alpha_composite(L)

def ship_icon(size, col):
    L = Image.new('RGBA', (size * 2, size), (0, 0, 0, 0)); d = ImageDraw.Draw(L); w, h = size * 2, size
    d.polygon([(w * 0.04, h * 0.55), (w * 0.96, h * 0.55), (w * 0.86, h * 0.85), (w * 0.12, h * 0.85)], fill=col)
    d.rectangle((w * 0.42, h * 0.3, w * 0.62, h * 0.55), fill=col); d.rectangle((w * 0.5, h * 0.1, w * 0.55, h * 0.3), fill=col)
    d.rectangle((w * 0.2, h * 0.42, w * 0.34, h * 0.55), fill=col)
    return L
SHIP = ship_icon(52, CREAM + (255,))
def ship_tally(can, t, t0, n=21, cy=820):
    if t < t0 - 0.2: return
    panel(can, (110, cy - 230, 970, cy + 230), int(165 * clamp((t - t0 + 0.2) / 0.3)))
    for i in range(n):
        ti = t0 + 0.05 + i * 0.055
        if t < ti: continue
        k = eout((t - ti) / 0.25); r, c = divmod(i, 7)
        put(can, SHIP, 205 + c * 112, cy - 140 + r * 140, lerp(0.5, 1.0, k), k)

def dial(can, t, t0, hours=72, cy=820):
    """translucent clock face counting submerged hours"""
    if t < t0 - 0.2: return
    a = clamp((t - t0 + 0.2) / 0.3); R = 260
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse((540 - R - 30, cy - R - 30, 540 + R + 30, cy + R + 30), fill=(6, 9, 12, int(165 * a)))
    d.ellipse((540 - R, cy - R, 540 + R, cy + R), outline=CREAM + (int(170 * a),), width=4)
    for i in range(12):
        an = i * math.pi / 6; d.line((540 + (R - 26) * math.sin(an), cy - (R - 26) * math.cos(an), 540 + R * math.sin(an), cy - R * math.cos(an)), fill=CREAM + (int(200 * a),), width=4)
    k = eio((t - t0) / 2.4); h = hours * k
    if k > 0.003: d.arc((540 - R + 14, cy - R + 14, 540 + R - 14, cy + R - 14), -90, -90 + 360 * k, fill=GOLD + (int(255 * a),), width=14)
    an = 2 * math.pi * (h % 12) / 12; d.line((540, cy, 540 + (R - 70) * math.sin(an), cy - (R - 70) * math.cos(an)), fill=GOLD + (int(200 * a),), width=8)
    can.alpha_composite(L)
    put(can, sprite(f'{int(h)} STD', 'serif', 110, CREAM), 540, cy + 30, 1.0, a)
    put(can, sprite('GETAUCHT', 'cond', 44, GOLD, False, 3), 540, cy + 120, 1.0, a)

def formation(can, t, t0, cy=800):
    """cruiser with a destroyer screen, seen from above, translucent"""
    if t < t0 - 0.2: return
    a = clamp((t - t0 + 0.2) / 0.35); panel(can, (110, cy - 330, 970, cy + 330), int(160 * a))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    k = eout((t - t0) / 0.6)
    def hull(x, y, ln, wd, col):
        d.polygon([(x, y - ln / 2), (x + wd / 2, y - ln / 4), (x + wd / 2, y + ln / 2), (x - wd / 2, y + ln / 2), (x - wd / 2, y - ln / 4)], fill=col)
    hull(540, cy - 20, 230 * k, 46, CREAM + (int(255 * a),))
    for i, (dx, dy) in enumerate(((-230, -170), (230, -170), (-260, 120), (260, 120))):
        kk = eout((t - t0 - 0.3 - i * 0.15) / 0.4)
        if kk > 0: hull(540 + dx, cy - 20 + dy, 110 * kk, 26, (170, 178, 190, int(255 * a * kk)))
    r = 300 * k; d.ellipse((540 - r, cy - 20 - r * 0.75, 540 + r, cy - 20 + r * 0.75), outline=(170, 178, 190, int(120 * a)), width=3)
    can.alpha_composite(L)
    put(can, sprite('NORFOLK', 'cond', 44, GOLD, False, 3), 540, cy + 160, 1.0, a)
    if t > t0 + 0.9: put(can, sprite('ZERSTÖRER', 'cond', 34, (170, 178, 190), False, 2), 540 - 260, cy + 190, 1.0, clamp((t - t0 - 0.9) / 0.3))

def bergen_map(can, t, t0, box=(110, 300, 970, 700)):
    """translucent map strip: Bergen and the course out into the North Sea"""
    if t < t0 - 0.2: return
    a = clamp((t - t0 + 0.2) / 0.35)
    mp, cam = draw_map((5.5, 58.9, 26.0), ('Norway',))
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle(box, 26, fill=int(235 * a))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); L.paste(mp, (0, (box[1] + box[3]) // 2 - H // 2)); L.putalpha(m); can.alpha_composite(L)
    dy = (box[1] + box[3]) // 2 - H // 2
    P = lambda lo, la: (cam.p(lo, la)[0], cam.p(lo, la)[1] + dy)
    bx, by = P(5.32, 60.39); pts = [(bx, by), P(4.4, 60.2), P(3.0, 59.6), P(1.5, 58.8)]
    k = eio((t - t0 - 0.3) / 1.6); pp = route(can, pts, k, GOLD, 6, dashed=True, alpha=a)
    ink_dot(can, bx, by, 12, GOLD)
    if a > 0.6: maplabel(can, t, t0 + 0.2, 'BERGEN', bx + 6, by - 36, size=50, col=CREAM, side='r')
    if len(pp) > 1 and k > 0.05: ink_dot(can, pp[-1][0], pp[-1][1], 8, CREAM)

# ---------- scenes: (old start, photo function) ----------
def sc_hook(t, w0, w1):
    u = clamp((t - w0) / (w1 - w0)); c = PCam('s20', lerp(1060, 650, u), 1230, 1300); can = shot(c, GRAD_SOFT)
    tA = wt('Adalbert') - 0.1
    focus(can, t, 0.05, '500 METER', 'serif', 230, GOLD, 1200, t1=tA - 0.15, dur=0.3)
    reveal(can, t, wt('britischen') - 0.1, 'VOR EINEM BRITISCHEN KREUZER', 'cond', 62, CREAM, 1330, t1=tA - 0.15, dur=0.45)
    plate(can, t, wt('Befehl') - 0.05, 'NICHT MEHR SCHIESSEN', 1450, size=56, bg=RUST, fg=CREAM, t1=tA - 0.15)
    if t >= tA:   # each name appears exactly when it is spoken
        focus(can, t, 5.40, 'ADALBERT', 'serif', 170, CREAM, 1240, dur=0.3)
        focus(can, t, 5.98, 'SCHNEE', 'serif', 190, GOLD, 1410, dur=0.3)
    return can
def sc_1913(t, w0, w1):
    can = shot(pan_lin('s12', t, w0, w1, 880, -1))
    focus(can, t, wt('1913'), '1913', 'serif', 170, GOLD, 1250)
    plate(can, t, wt('Berlin'), 'BERLIN', 1420, size=64); return can
def sc_1934(t, w0, w1):
    can = shot(zoom_lin('s08', t, w0, w1, 768, 1376))
    plate(can, t, wt('1934'), 'MARINE · 1934', 1400, size=60); return can
def sc_kretschmer(t, w0, w1):
    c = pan_lin('s18', t, w0, w1, 880, 1); can = shot(c)
    callout(can, t, wt('Otto'), c.pt(560, 1060), (540, 1300), 'OTTO KRETSCHMER', col=GOLD, size=60)
    reveal(can, t, wt('U-23'), 'U-23 · WACHOFFIZIER', 'cond', 64, GOLD, 1420); return can
def sc_u201(t, w0, w1):
    can = shot(pan_lin('s02', t, w0, w1, 900, -1))
    focus(can, t, wt('1941'), '1941', 'cond', 70, CREAM, 1200)
    c = pan_lin('s02', t, w0, w1, 900, -1)
    callout(can, t, wt('U-201.') + 0.1, c.pt(1250, 650), (540, 1350), 'U-201', col=GOLD, size=110); return can
def sc_snow(t, w0, w1):
    c = pan_lin('s21', t, w0, w1, 1200, 1); can = shot(c, GRAD_SOFT)
    magnifier(can, t, wt('Schneemann'), c, 420, 1690)
    focus(can, t, wt('Anspielung'), 'SCHNEE  =  SCHNEEMANN', 'serif', 92, CREAM, 1300); return can
def sc_wappen(t, w0, w1):
    can = shot(pan_lin('s07', t, w0, w1, 1200, -1))
    reveal(can, t, wt('bekanntesten'), 'EINES DER BEKANNTESTEN', 'cond', 62, CREAM, 1300)
    reveal(can, t, wt('Bootswappen'), 'BOOTSWAPPEN', 'serif', 120, GOLD, 1420); return can
def sc_21(t, w0, w1):
    can = shot(pan_lin('s14', t, w0, w1, 950, 1))
    counter(can, t, wt('21', 25), 21, 1230)
    plate(can, t, wt('versenkte'), 'VERSENKTE HANDELSSCHIFFE', 1420, size=52); return can
def sc_doenitz(t, w0, w1):
    c = pan_lin('s06', t, w0, w1, 900, -1); can = shot(c)
    callout(can, t, wt('Dönitz'), c.pt(800, 420), (540, 1300), 'KARL DÖNITZ', col=GOLD, size=60)
    plate(can, t, wt('Geleitzüge') - 0.3, 'PLANUNG GEGEN GELEITZÜGE', 1430, size=48, bg=RUST, fg=CREAM); return can
def sc_xxi(t, w0, w1):
    can = shot(pan_lin('s03', t, w0, w1, 1250, 1))
    focus(can, t, wt('völlig'), 'VÖLLIG NEUES BOOT', 'cond', 66, CREAM, 1180, t1=wt('Typ') - 0.2)
    focus(can, t, wt('Typ'), 'TYP XXI', 'serif', 220, GOLD, 1250)
    reveal(can, t, wt('tagelang'), 'TAGELANG GETAUCHT', 'cond', 64, CREAM, 1420); return can
def sc_speed(t, w0, w1):
    can = shot(pan_lin('s04', t, w0, w1, 1800, -1), GRAD_SOFT); bars(can, t, wt('schneller') - 0.2, 1180); return can
def sc_u2511(t, w0, w1):
    can = shot(pan_lin('s17', t, w0, w1, 900, 1))
    focus(can, t, wt('U-2511,'), 'U-2511', 'serif', 220, GOLD, 1270, dur=0.3)
    plate(can, t, wt('erste'), 'ERSTE FEINDFAHRT DES TYPS XXI', 1430, size=46); return can
def sc_bergen(t, w0, w1):
    can = shot(pan_lin('s13', t, w0, w1, 900, -1))
    focus(can, t, wt('Bergen', 50), 'BERGEN', 'serif', 190, CREAM, 1240)
    plate(can, t, wt('April'), '30. APRIL 1945', 1400, size=60, bg=GOLD, fg=DEEP); return can
def sc_order(t, w0, w1):
    can = shot(pan_lin('s09', t, w0, w1, 900, 1), GRAD_SOFT)
    typecard(can, t, wt('Befehl', 50), [('4. MAI 1945', 52, SEPIA), ('ALLE ANGRIFFE', 80, INK), ('EINSTELLEN', 80, RUST)], cy=1180); return can
def sc_norfolk(t, w0, w1):
    can = shot(pan_lin('s16', t, w0, w1, 1000, -1), GRAD_SOFT)
    reveal(can, t, wt('berichtete'), 'NACH SCHNEES BERICHT', 'cond', 52, CREAM, 1290)
    plate(can, t, wt('Norfolk'), 'KREUZER NORFOLK', 1410, size=64, bg=RUST, fg=CREAM); return can
def sc_sonar(t, w0, w1):
    can = shot(pan_lin('s11', t, w0, w1, 880, 1), GRAD_SOFT)
    can.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(110 * clamp((t - w0) / 0.5)))))
    sonar(can, t, wt('glitt'), wt('Meter', 60) + 0.2); return can
def sc_feint(t, w0, w1):
    can = shot(pan_lin('s01', t, w0, w1, 1200, -1))
    focus(can, t, wt('Übungsangriff'), 'ÜBUNGSANGRIFF', 'serif', 130, CREAM, 1260)
    plate(can, t, wt('ohne'), 'KEIN SCHUSS', 1410, size=70, bg=GOLD, fg=DEEP); return can
def sc_doubt(t, w0, w1):
    can = shot(pan_lin('s19', t, w0, w1, 880, 1))
    can = desat(can, 0.85 * clamp((t - wt('Geschichte', 60)) / 1.2))
    focus(can, t, wt('fast'), 'NUR SEINE EIGENE AUSSAGE', 'cond', 60, CREAM, 1240, t1=wt('Historiker') - 0.2)
    seal(can, t, wt('Historiker'), 'UMSTRITTEN', 540, 1300, r=210, col=RUST, rot=-10); return can
def sc_surrender(t, w0, w1):
    can = shot(pan_lin('s15', t, w0, w1, 1000, -1))
    focus(can, t, wt('9.'), '9. MAI 1945', 'serif', 150, GOLD, 1260)
    plate(can, t, wt('übergab'), 'ÜBERGABE IN BERGEN', 1420, size=58); return can
def sc_after(t, w0, w1):
    can = shot(pan_lin('s05', t, w0, w1, 1500, 1), GRAD_SOFT)
    plate(can, t, wt('Elba'), 'SEGELSCHULE AUF ELBA', 780, size=56)
    plate(can, t, wt('Verband'), 'VERBAND DER U-BOOT-FAHRER', 900, size=48, bg=GOLD, fg=DEEP); return can
def sc_end(t, w0, w1):
    can = shot(zoom_lin('s22', t, w0, w1, 896, 1150, 1.07)); tk = wt('Kanntet')
    focus(can, t, wt('1982') - 0.1, '1913 · 1982', 'serif', 170, CREAM, 1260, t1=tk - 0.2)
    plate(can, t, wt('Hamburg'), 'HAMBURG', 1420, size=70, bg=GOLD, fg=DEEP, t1=tk - 0.2)
    focus(can, t, tk, 'KANNTET IHR', 'serif', 120, CREAM, 1210)
    focus(can, t, wt('diese', 90), 'DIESE GESCHICHTE?', 'serif', 120, GOLD, 1340)
    plate(can, t, wt('Schreibt'), 'SCHREIBT ES IN DIE KOMMENTARE!', 1460, size=46); return can

OLD = [(0.0, sc_hook, 'cut'), (6.9, sc_1913, 'fade'), (('n', 11.05), sc_1934, 'fade'), (('n', 14.6), sc_kretschmer, 'slide_l'), (20.9, sc_u201, 'fade'),
       (26.1, sc_snow, 'fade'), (31.6, sc_wappen, 'slide_r'), (35.8, sc_21, 'fade'), (39.6, sc_doenitz, 'fade'), (46.4, sc_xxi, 'slide_l'),
       (51.4, sc_speed, 'fade'), (56.5, sc_u2511, 'fade'), (62.6, sc_bergen, 'slide_r'), (67.6, sc_order, 'fade'), (72.7, sc_norfolk, 'fade'),
       (78.3, sc_sonar, 'dip'), (83.3, sc_feint, 'fade'), (88.4, sc_doubt, 'fade'), (95.4, sc_surrender, 'slide_l'), (100.2, sc_after, 'fade'),
       (106.9, sc_end, 'fade')]
OV = 0.22
SC = []
for i, (t0, fn, tr) in enumerate(OLD):
    N = lambda x: x[1] if isinstance(x, tuple) else M(x)
    s = 0.0 if i == 0 else N(t0) - OV
    e = TEND if i == len(OLD) - 1 else N(OLD[i + 1][0]) + OV
    SC.append((s, e, fn, tr))

DIPC = Image.new('RGBA', (W, H), (4, 6, 8, 255))
def run(sc, t): return sc[2](t, sc[0], sc[1])
def frame(t):
    act = [s for s in SC if s[0] <= t < s[1]] or [SC[-1]]
    if len(act) == 1: img = run(act[0], t)
    else:
        a, b = act[0], act[1]; u = ease((t - b[0]) / (a[1] - b[0])); tr = b[3]
        if tr in ('slide_l', 'slide_r'):
            A = run(a, t); B_ = run(b, t); s = 1 if tr == 'slide_l' else -1; off = int(W * u)
            img = Image.new('RGBA', (W, H), (0, 0, 0, 255)); img.paste(A, (-s * off, 0)); img.paste(B_, (s * (W - off), 0))
        elif tr == 'dip':
            img = Image.blend(run(a, t), DIPC, min(1, u * 2)) if u < 0.5 else Image.blend(DIPC, run(b, t), (u - 0.5) * 2)
        else: img = Image.blend(run(a, t), run(b, t), u)
    img.alpha_composite(VIG)
    if t > TEND - 0.6: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * clamp((t - TEND + 0.6) / 0.5)))))
    return img.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; ims = [S1.ui_overlay(frame(t)).resize((270, 480)) for t in ts]
        cols = 6; rows = (len(ims) + cols - 1) // cols; Sh = Image.new('RGB', (270 * cols, 480 * rows))
        for i, im in enumerate(ims):
            Sh.paste(im, ((i % cols) * 270, (i // cols) * 480)); ImageDraw.Draw(Sh).text(((i % cols) * 270 + 4, (i // cols) * 480 + 4), f'{ts[i]}', fill=(0, 255, 0))
        Sh.save(B + sys.argv[2], quality=90)
    elif sys.argv[1] == 'info':
        print('TEND', TEND); [print(round(s, 2), round(e, 2), f.__name__) for s, e, f, _ in SC]
    else:
        out = sys.argv[2]; a, b = float(sys.argv[3]), float(sys.argv[4])
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
        for n in range(int(round(a * FPS)), int(round(b * FPS))):
            p.stdin.write(S1.grain(frame(n / FPS), n).tobytes())
        p.stdin.close(); p.wait(); print('rc', p.returncode)
