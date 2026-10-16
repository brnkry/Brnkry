# Stigler / Brown scenes. Photo, animation, photo, animation ...
import sys, math, subprocess
from base import *
from mapx import *

KIMB = (-0.39, 52.30); BREMEN = (8.80, 53.08); SEETH = (1.42, 52.53); SWE = (13.4, 56.6); VAN = (-123.1, 49.3); GER = (10.4, 51.2)

# ---------------- S1 hook: Stigler portrait ----------------
def s_hook(t):
    c = pcam('p08', t, 0, 6.6, (896, 980, 1180), (896, 1060, 1330)); can = c.frame(); can.alpha_composite(GRAD_SOFT)
    tE = wt('Er') - 0.15
    focus(can, t, wt('deutscher'), 'EIN DEUTSCHER', 'serif', 92, CREAM, 1240, t1=wt('wehrlosen') - 0.1)
    focus(can, t, wt('Jagdflieger'), 'JAGDFLIEGER', 'serif', 92, GOLD, 1350, t1=wt('wehrlosen') - 0.1)
    focus(can, t, wt('wehrlosen'), 'EIN WEHRLOSER', 'serif', 92, CREAM, 1240, t1=tE)
    focus(can, t, wt('amerikanischen'), 'US BOMBER', 'serif', 92, GOLD, 1350, t1=tE)
    reveal(can, t, wt('direkt'), 'DIREKT VOR IHM', 'cond', 54, CREAM, 1450, t1=tE, dur=0.5)
    focus(can, t, wt('schoss') - 0.1, 'ER SCHOSS', 'serif', 132, CREAM, 1250, dur=0.3)
    focus(can, t, wt('nicht.') - 0.05, 'NICHT.', 'serif', 150, (214, 70, 44), 1400, dur=0.3)
    return can

# ---------------- S2 dossier cards ----------------
BG_MANILA = paper((214, 190, 140), 0.09)
def card(name, sub, w=760, h=300):
    im = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((34, 40, 30 + w, 36 + h), fill=(40, 25, 10, 140))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(im); d.rectangle((30, 30, 30 + w, 30 + h), fill=(244, 236, 216, 255))
    d.rectangle((30, 30, 30 + w, 92), fill=(168, 58, 36, 255))
    for y in range(150, h + 20, 52): d.line((60, 30 + y, w, 30 + y), fill=(150, 175, 196, 255), width=2)
    f = FK['cond'](36); d.text((60, 42), sub, font=f, fill=CREAM)
    sz = fit(name, 'serif', 96, w - 80); f2 = FK['serif'](sz); tw = f2.getlength(name)
    d.text((30 + w / 2 - tw / 2, 30 + h / 2 - 10), name, font=f2, fill=INK)
    return im
CARD1 = card('Franz Stigler', 'LUFTWAFFE  ·  JAGDFLIEGER'); CARD2 = card('Charlie Brown', 'USAAF  ·  BOMBERPILOT')
def half_photo(p, cx, cy, w):
    h = w * 960 / 1080; cy = max(cy, h / 2)
    return src(p).resize((W, 960), Image.LANCZOS, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)).convert('RGBA')
HALF1 = half_photo('p08', 896, 712, 1600); HALF2 = half_photo('p06', 896, 1200, 1560)
DARKH = Image.new('RGBA', (W, 960), (16, 11, 6, 255))
def s_dossier(t):
    can = Image.new('RGBA', (W, H), (16, 11, 6, 255))
    for im, t0, y0, side in ((HALF1, wt('Franz'), 0, -1), (HALF2, wt('Charlie'), 960, 1)):
        k = eout((t - t0 + 0.35) / 0.6)
        lit = Image.blend(DARKH, im, 0.28 + 0.72 * k)
        z = lerp(1.0, 1.05, clamp((t - 6.3) / 5.6))
        if z > 1.001:
            lit = lit.resize((int(W * z), int(960 * z)), Image.BILINEAR).crop((int(W * (z - 1) / 2), int(960 * (z - 1) / 2), int(W * (z - 1) / 2) + W, int(960 * (z - 1) / 2) + 960))
        can.paste(lit, (int(side * (1 - eout((t - 6.3) / 0.7)) * 300), y0))
    can.alpha_composite(vgrad(170, 0, 3000, 3001, 520))
    can.alpha_composite(Image.merge('RGBA', [Image.new('L', (W, H), 10)] * 3 + [Image.fromarray(np.repeat((np.clip(1 - np.abs(np.arange(H) - 960) / 120, 0, 1) * 150)[:, None], W, 1).astype(np.uint8))]))
    ImageDraw.Draw(can).line((0, 960, W, 960), fill=GOLD + (255,), width=4)
    cascade(can, t, wt('Geschichte'), 'DIE GESCHICHTE VON', 'cond', 64, CREAM, 360, track=6)
    for cd, t0, y, side, r in ((CARD1, wt('Franz'), 836, -1, -2.0), (CARD2, wt('Charlie'), 1488, 1, 1.6)):
        if t < t0 - 0.3: continue
        k = eout((t - t0 + 0.3) / 0.55)
        im = cd.rotate(r * (1 - k * 0.6), resample=Image.BICUBIC, expand=True)
        put(can, im, 540 + side * (1 - k) * 700, y, 0.66, 1.0)
    if t > wt('Charlie') + 0.2:
        a = ease((t - wt('Charlie') - 0.2) / 0.4)
        d = ImageDraw.Draw(can); d.ellipse((540 - 52 * a, 960 - 52 * a, 540 + 52 * a, 960 + 52 * a), fill=(26, 18, 10, 255), outline=GOLD + (255,), width=4)
        put(can, sprite('&', 'serif', 64, GOLD, False), 540, 958, 1.0, a)
    return can

# ---------------- S3 tear-off calendar ----------------
BG_DESK = paper((70, 52, 36), 0.12)
def cal_page(num):
    w, h = 600, 700; im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((20, 20, 20 + w, 20 + h), fill=(240, 232, 212, 255)); d.rectangle((20, 20, 20 + w, 150), fill=(150, 46, 30, 255))
    f = FK['serif'](400); tw = f.getlength(num); d.text((20 + w / 2 - tw / 2, 150), num, font=f, fill=INK)
    for x in range(60, w, 60): d.ellipse((x - 7, 34, x + 7, 48), fill=(60, 40, 25, 255))
    return im
PAGES = {n: cal_page(n) for n in ('16', '17', '18', '19', '20')}
def s_calendar(t):
    can = BG_DESK.copy(); cx, cy = 540, 900
    sh = Image.new('RGBA', (720, 820), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((40, 50, 680, 790), fill=(0, 0, 0, 150))
    put(can, sh.filter(ImageFilter.GaussianBlur(18)), cx + 10, cy + 20)
    put(can, PAGES['20'], cx, cy)
    t20 = wt('20.')
    for i, n in enumerate(('19', '18', '17', '16')):
        tf = t20 - 0.08 - i * 0.12          # page leaves at tf
        if t < tf: put(can, PAGES[n], cx, cy); continue
        u = (t - tf) / 0.45
        if u < 1:
            pg = PAGES[n].rotate(18 * u, resample=Image.BICUBIC, expand=True)
            put(can, pg, cx + 240 * u, cy - 500 * u * u, 1.0 - 0.15 * u, 1 - u)
    # header word and year printed on the band and below
    if t > wt('Dezember') - 0.1:
        k = eout((t - wt('Dezember') + 0.1) / 0.35)
        put(can, sprite('DEZEMBER', 'cond', 74, CREAM, False, 8), cx, cy - 280, 1.0, k)
    cascade(can, t, wt('1943'), '1943', 'serif', 150, CREAM, 1420, track=10, step=0.09)
    return can

# ---------------- S4 Brown portrait ----------------
def s_brown(t):
    c = pcam('p06', t, 15.2, 19.9, (896, 1050, 1300), (896, 960, 1100)); can = c.frame(); can.alpha_composite(GRAD)
    focus(can, t, wt('21-j'), '21 JAHRE', 'serif', 120, CREAM, 1260, t1=wt('ersten') - 0.1)
    focus(can, t, wt('ersten'), 'ERSTER EINSATZ', 'serif', 100, CREAM, 1260)
    plate(can, t, wt('Leutnant'), 'LEUTNANT CHARLES BROWN', 1420, size=46)
    return can

# ---------------- S5 crew photo ----------------
def brace(can, t, t0, x0, x1, y, col=CREAM, dur=0.6):
    if t < t0: return
    k = eio((t - t0) / dur); xm = (x0 + x1) / 2
    left = bez((x0, y + 30), (x0, y), (x0 + 40, y)) + [(xm - 30, y)] + bez((xm - 30, y), (xm, y), (xm, y - 30))
    right = bez((x1, y + 30), (x1, y), (x1 - 40, y)) + [(xm + 30, y)] + bez((xm + 30, y), (xm, y), (xm, y - 30))
    stroke(can, partial(left, k), col, 6); stroke(can, partial(right, k), col, 6)
def s_crew(t):
    c = pcam('p05', t, 19.3, 24.2, (760, 950, 1008), (1500, 950, 1008)); can = c.frame(); can.alpha_composite(GRAD)
    can.alpha_composite(vgrad(150, 0, 3000, 3001, 520))
    brace(can, t, wt('Kommandant') - 0.2, 120, 900, 440)
    cascade(can, t, wt('Kommandant') + 0.3, '10 MANN BESATZUNG', 'cond', 56, CREAM, 360, track=5)
    plate(can, t, wt('Kommandant'), 'KOMMANDANT', 1300, size=58)
    reveal(can, t, wt('namens'), 'B-17  „YE OLDE PUB“', 'serif', 74, GOLD, 1430)
    return can

# ---------------- S6 map: Kimbolton to Bremen ----------------
ROUTE_IN = [KIMB, (1.6, 52.9), (4.5, 53.6), (7.2, 53.7), BREMEN]
def s_mapbremen(t):
    t0 = 23.6; u = eio((t - t0) / 4.8)
    c = camlerp((3.8, 53.0, 14.0), (5.4, 53.1, 10.5), u)
    can, cam = draw_map(c, ('Germany',))
    compass(can, 150, 1450, 70, 0.6)
    pts = [cam.p(*p) for p in ROUTE_IN]
    ink_dot(can, *cam.p(*KIMB)); maplabel(can, t, t0, 'KIMBOLTON', *cam.p(*KIMB), size=40, side='r')
    k = eio((t - t0) / 1.6); pp = route(can, pts, k, RUST, 7, dashed=True)
    bx, by = cam.p(*BREMEN)
    if t > wt('Bremen') - 0.2:
        ink_dot(can, bx, by, 11, RUST); maplabel(can, t, wt('Bremen') - 0.2, 'BREMEN', bx, by, size=50, side='l', col=RUST)
    hit = clamp((t - wt('schwer')) / 0.5)
    col = tuple(int(lerp(a, b, hit)) for a, b in zip(NAVY, (150, 40, 28)))
    jx, jy = pp[-1]; jx -= 30 * (1 - k)
    icon(can, 'b17', jx, jy, heading(pp) if k < 1 else -0.05, 54, col)
    rng = np.random.default_rng(4)
    for i in range(10):
        tf = wt('Flak') + i * 0.28; ox, oy = rng.normal(0, 70, 2)
        flak(can, t, tf, jx + ox - 30, jy + oy, 30)
    tj = wt('Jäger')
    for i, (sx, sy) in enumerate(((1000, 640), (1050, 1250))):
        if t < tj: continue
        v = eout((t - tj - i * 0.2) / 1.4)
        x = lerp(sx, jx + 60, v); y = lerp(sy, jy + (-70 if i == 0 else 70), v)
        ang = math.atan2(jy - sy, jx - sx) + (0.9 * v if i == 0 else -0.9 * v)
        icon(can, 'bf', x, y, ang, 30, (58, 52, 46))
    focus(can, t, wt('Ziel'), 'ZIEL: BREMEN', 'serif', 92, INK, 380)
    reveal(can, t, wt('Flak'), 'FLAK UND JÄGER', 'serif', 84, (150, 40, 28), 1400)
    return can

# ---------------- S7 damage on the B-17 photo ----------------
def s_damage(t):
    c = pcam('p11', t, 28.4, 34.3, (420, 770, 700), (240, 790, 500)); can = c.frame(); can.alpha_composite(GRAD)
    eng = c.pt(60, 775); nose = c.pt(6, 795); tail = c.pt(412, 700)
    callout(can, t, wt('Motoren'), (max(80, eng[0] + 40), eng[1]), (540, 1170), 'MOTOREN AUSGEFALLEN', elbow=None)
    callout(can, t, wt('Bugkanzel'), (max(60, nose[0] + 30), nose[1] + 30), (540, 1300), 'BUGKANZEL ZERSTÖRT')
    callout(can, t, wt('Leitwerk'), tail, (540, 1430), 'LEITWERK ZERFETZT')
    return can

# ---------------- S8 crew ledger ----------------
BG_LEDGER = paper((236, 226, 200), 0.06)
def ledger_bg():
    im = BG_LEDGER.copy(); d = ImageDraw.Draw(im)
    for y in range(520, 1480, 120): d.line((110, y + 40, 970, y + 40), fill=(150, 170, 190, 255), width=2)
    d.line((150, 300, 150, 1500), fill=(196, 90, 70, 255), width=3)
    return im
LEDGER = ledger_bg()
def s_ledger(t):
    can = LEDGER.copy()
    cascade(can, t, 34.15, 'BESATZUNG · YE OLDE PUB', 'type', 50, INK, 400, track=2, step=0.02)
    pen_rule(can, t, 34.6, 455, 640, col=INK, th=4)
    rows = [('HUGH ECKENRODE', 'HECKSCHÜTZE', wt('Hugh') - 0.1, 600)]
    reveal(can, t, wt('Hugh') - 0.1, 'HUGH ECKENRODE', 'type', 64, INK, 600, cx=480, dur=0.7)
    reveal(can, t, wt('Heckschütze') + 0.1, 'HECKSCHÜTZE', 'type', 36, SEPIA, 664, cx=480, dur=0.5)
    tt = wt('tot')
    if t > tt:  # ink strike through the name
        k = eio((t - tt) / 0.35); stroke(can, [(190, 604), (190 + 590 * k, 598)], (160, 40, 28), 7, outline=False)
    seal(can, t, tt + 0.1, 'TOT', 820, 630, r=88, col=(160, 40, 28), rot=-14)
    for i, nm in enumerate(('PECHOUT', 'BLACKFORD', 'YELESANKO', 'BROWN')):
        reveal(can, t, wt('mehrere') + i * 0.25, nm, 'type', 60, INK, 840 + i * 120, cx=440, dur=0.45)
    tv = wt('verwundet')
    if t > tv:
        k = eio((t - tv) / 0.5); pts = bez((690, 800), (760, 800), (760, 880)) + [(760, 1100)] + bez((760, 1100), (760, 1180), (690, 1200))
        stroke(can, partial(pts, k), (160, 40, 28), 6, outline=False)
    cascade(can, t, tv + 0.3, 'VERWUNDET', 'cond', 64, (160, 40, 28), 1340, track=6)
    return can

# ---------------- S9 Bf 109 photo ----------------
def s_bf109(t):
    c = pcam('p02', t, 39.4, 46.6, (1560, 900, 1008), (780, 960, 1008)); can = c.frame(); can.alpha_composite(GRAD)
    can.alpha_composite(vgrad(140, 0, 3000, 3001, 560))
    plate(can, t, wt('Oberleutnant'), 'OBERLEUTNANT FRANZ STIGLER', 380, size=46)
    reveal(can, t, wt('Jagdgeschwader'), 'JAGDGESCHWADER 27', 'serif', 66, CREAM, 490)
    ck = c.pt(560, 1000)
    callout(can, t, wt('Bf'), ck, (540, 1400), 'Bf 109 G-6', col=GOLD, size=56)
    return can

# ---------------- S10 tally ----------------
BG_DARK = paper((40, 30, 22), 0.15)
def tally_mark(can, t, t0, x, y, h=260, col=CREAM, ghost=False):
    if t < t0: return
    k = eio((t - t0) / 0.3); pts = [(x - 14, y - h / 2), (x + 14, y + h / 2)]
    p = partial(pts, k)
    if ghost:
        n = 12
        for i in range(int(n * k)):
            if i % 2: continue
            a = (lerp(pts[0][0], pts[1][0], i / n), lerp(pts[0][1], pts[1][1], i / n)); b = (lerp(pts[0][0], pts[1][0], (i + 1) / n), lerp(pts[0][1], pts[1][1], (i + 1) / n))
            stroke(can, [a, b], GOLD, 16, outline=False)
    else: stroke(can, p, col, 22, outline=False)
def s_tally(t):
    can = BG_DARK.copy()
    cascade(can, t, 46.3, 'ABSCHÜSSE AN DIESEM TAG', 'cond', 54, (200, 186, 160), 400, track=5)
    tally_mark(can, t, wt('Ein', 46) - 0.1, 380, 800); tally_mark(can, t, wt('weiterer') - 0.1, 500, 800)
    tally_mark(can, t, wt('Abschuss'), 640, 800, ghost=True)
    if t > wt('Abschuss') + 0.2:
        put(can, sprite('+1', 'serif', 90, GOLD, False), 760, 700, 1.0, ease((t - wt('Abschuss') - 0.2) / 0.3))
    focus(can, t, wt('Ritterkreuz'), '= RITTERKREUZ', 'serif', 104, GOLD, 1150)
    # heartbeat pulse on the edges near the end
    hb = t - wt('gebracht')
    if hb > 0:
        p = max(0, math.sin(hb * 2 * math.pi * 1.1)) ** 8
        can.alpha_composite(Image.new('RGBA', (W, H), (60, 6, 0, int(70 * p))))
    return can

# ---------------- S11 wreck photo ----------------
def s_wreck(t):
    c = pcam('p10', t, 50.0, 54.5, (1000, 1000, 1150), (960, 860, 940)); can = c.frame(); can.alpha_composite(GRAD)
    focus(can, t, wt('neben', 50), 'NEBEN DEM BOMBER', 'serif', 76, CREAM, 1270)
    reveal(can, t, wt('Verwundeten'), 'DIE VERWUNDETEN IM RUMPF', 'cond', 56, GOLD, 1380)
    return can

# ---------------- S12 Rödel ----------------
def s_roedel(t):
    c = pcam('p03', t, 54.0, 58.6, (896, 1000, 1180), (896, 1150, 1350)); can = c.frame(); can.alpha_composite(GRAD)
    cascade(can, t, wt('Kommandeur'), 'SEIN KOMMANDEUR', 'cond', 52, GOLD, 1300, track=6)
    plate(can, t, wt('Gustav'), 'GUSTAV RÖDEL', 1410, size=62, fk='serif', track=2)
    return can

# ---------------- S13 quote card ----------------
BG_QUOTE = paper((233, 222, 196), 0.08)
QLINES = [['„Wer', 'auf', 'einen', 'Mann'], ['am', 'Fallschirm', 'schieße,'], ['den', 'erschieße'], ['er', 'selbst.“']]
QKEYS = ['wer', 'auf', 'einen', 'Mann', 'am', 'Fallschirm', 'schieße', 'den', 'erschieße', 'er', 'selbst']
def s_quote(t):
    can = BG_QUOTE.copy()
    put(can, sprite('“', 'serif', 300, (200, 170, 130), False), 540, 470, 1.0, 0.8)
    times = []; after = 58.3
    for k in QKEYS:
        tk = wt(k, after); times.append(tk); after = tk + 0.01
    size = 78; ys = [700, 820, 940, 1060]; i = 0
    for li, line in enumerate(QLINES):
        txt = ' '.join(line); f = FK['serif'](size); x = 540 - f.getlength(txt) / 2
        for w in line:
            tk = times[i]; i += 1
            if t >= tk - 0.05:
                k = eout((t - tk + 0.05) / 0.3)
                r = int(round((1 - k) * 8 / 2)) * 2
                put(can, sprite(w, 'serif', size, INK, False, 0, r), x + f.getlength(w) / 2, ys[li] - (1 - k) * 14, 1.0, k)
            x += f.getlength(w + ' ')
    pen_rule(can, t, wt('selbst') + 0.2, 1170, 300, col=RUST, th=5)
    cascade(can, t, wt('selbst') + 0.35, 'GUSTAV RÖDEL', 'cond', 46, SEPIA, 1240, track=8)
    return can

# ---------------- S14 map: Sweden? ----------------
def s_sweden(t):
    t0 = 62.2; u = eio((t - t0) / 5.4)
    c = camlerp((8.2, 54.6, 13.0), (9.6, 55.3, 16.0), u)
    can, cam = draw_map(c, ('Sweden',))
    compass(can, 180, 420, 64, 0.55)
    v = (t - t0) / 5.4
    px, py = cam.p(lerp(7.9, 6.9, v), lerp(53.85, 54.05, v))
    wag = 0.35 * math.sin((t - wt('Zeichen')) * 14) * clamp(1 - (t - wt('Zeichen')) / 1.2) if t > wt('Zeichen') else 0
    icon(can, 'b17', px, py + 26, math.pi + 0.15, 54, (150, 40, 28))
    icon(can, 'bf', px + 4, py - 52, math.pi + 0.15 + wag, 32, (58, 52, 46))
    sx, sy = cam.p(*SWE)
    fade = 1 - ease((t - wt('verstand')) / 0.8)
    if t > wt('Zeichen'):
        k = eio((t - wt('Zeichen')) / 0.9)
        pts = bez((px + 20, py - 70), (px + 120, sy - 40), (sx - 30, sy + 30), 50)
        pp = route(can, pts, k, NAVY, 7, dashed=True, alpha=fade)
        if k > 0.95: arrowhead(can, pp[-1], heading(pp), NAVY, 30, fade)
    if t > wt('Schweden'):
        maplabel(can, t, wt('Schweden'), 'SCHWEDEN', sx - 40, sy - 120, size=52, side='c', col=INK)
    if t > wt('Schweden') + 0.4:
        put(can, sprite('?', 'serif', 220, RUST, False), sx - 10, sy + 150, 1.0, ease((t - wt('Schweden') - 0.4) / 0.3) * fade)
    focus(can, t, wt('nach', 63), 'NACH SCHWEDEN?', 'serif', 92, INK, 380, t1=wt('verstand') - 0.2)
    focus(can, t, wt('verstand'), 'BROWN VERSTAND NICHT', 'serif', 80, INK, 380)
    return can

# ---------------- S15 formation photo ----------------
def s_escort(t):
    c = pcam('p07', t, 67.2, 72.7, (1180, 900, 1008), (1420, 860, 1008)); can = c.frame(); can.alpha_composite(GRAD)
    focus(can, t, wt('dicht'), 'DICHT DANEBEN', 'serif', 100, CREAM, 1290)
    reveal(can, t, wt('damit', 69), 'DAMIT DIE FLAK SCHWIEG', 'cond', 56, GOLD, 1410)
    return can

# ---------------- S16 map: salute over the North Sea, landing at Seething ----------------
def s_salute(t):
    t0 = 72.2
    u = eio((t - 75.2) / 2.4)
    c = camlerp((4.3, 53.6, 8.0), (2.6, 53.0, 6.4), u)
    can, cam = draw_map(c, ('United Kingdom',))
    v = eio((t - t0) / 1.6)
    b_lon = lerp(6.2, 4.5, v); b_lat = lerp(53.95, 53.75, v)
    tl = wt('landete')
    if t > 73.8:
        w = eio((t - 73.8) / (tl + 1.0 - 73.8)); pts = [(4.5, 53.75), (3.2, 53.3), SEETH]
        pp = partial([cam.p(*p) for p in pts], w); bx, by = pp[-1]; ang = heading(pp)
    else:
        bx, by = cam.p(b_lon, b_lat); ang = math.pi + 0.12
    route(can, [cam.p(6.6, 54.0), cam.p(b_lon, b_lat)] if t < 73.8 else [cam.p(6.6, 54.0), cam.p(4.5, 53.75)] + [(bx, by)], 1.0, RUST, 5, dashed=True, alpha=0.7)
    icon(can, 'b17', bx, by + 22, ang, 54, (150, 40, 28))
    td = wt('drehte')
    if t < td:
        fx, fy = cam.p(b_lon, b_lat + 0.09); fa = math.pi + 0.12
    else:
        q = eio((t - td) / 1.6)
        pts = bez(cam.p(4.5, 53.84), cam.p(3.6, 54.6), cam.p(6.4, 54.9), 40)
        pp = partial(pts, max(0.02, q)); fx, fy = pp[-1]; fa = heading(pp) if len(pp) > 1 else math.pi
    if t < td + 2.2: icon(can, 'bf', fx, fy - 40, fa, 32, (58, 52, 46), 1 - clamp((t - td - 1.4) / 0.8))
    ts = wt('salutierte')
    if t > ts:
        sx, sy = cam.p(4.5, 53.84)
        for j in range(2):
            uu = clamp((t - ts - j * 0.25) / 1.0); ring(can, sx, sy - 40, 30 + 90 * uu, GOLD, (1 - uu) * 0.9, 4)
    focus(can, t, wt('Über'), 'ÜBER DER NORDSEE', 'serif', 88, INK, 380, t1=ts - 0.1)
    focus(can, t, ts, 'EIN SALUT', 'serif', 108, RUST, 380, t1=tl - 0.2)
    if t > wt('Seething') - 0.1:
        ex, ey = cam.p(*SEETH); ink_dot(can, ex, ey, 12, RUST)
        maplabel(can, t, wt('Seething') - 0.1, 'SEETHING', ex - 60, ey + 90, size=58, side='c', col=RUST)
    focus(can, t, tl, 'GELANDET IN ENGLAND', 'serif', 80, INK, 380)
    return can

# ---------------- S17 report document ----------------
BG_DOC = paper((60, 46, 32), 0.12)
def doc_sheet():
    w, h = 820, 1180; im = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((44, 52, 40 + w, 48 + h), fill=(0, 0, 0, 170))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    pg = paper((238, 230, 210), 0.07, False).crop((0, 0, w, h)); im.alpha_composite(pg, (40, 40))
    d = ImageDraw.Draw(im); f = FK['type'](34)
    d.text((90, 90), 'JAGDGESCHWADER 27', font=f, fill=SEPIA); d.text((90, 140), '20.12.1943', font=f, fill=SEPIA)
    for y in range(470, 1100, 62):
        d.line((90, y, 90 + (w - 120) * (0.6 + 0.4 * ((y * 37) % 11) / 11), y), fill=(150, 140, 120, 255), width=6)
    return im
DOC = doc_sheet()
def s_report(t):
    can = BG_DOC.copy(); t0 = 78.9
    k = eout((t - t0) / 0.6); put(can, DOC.rotate(lerp(6, 1.5, k), resample=Image.BICUBIC, expand=True), 540, 1010 + (1 - k) * 300, 0.84, 1.0)
    cascade(can, t, wt('meldete'), 'MELDUNG', 'type', 110, INK, 740, track=8, step=0.06)
    tn = wt('nie,')
    if t > tn:
        q = eio((t - tn) / 0.3); stroke(can, [(260, 748), (260 + 560 * q, 736)], (170, 36, 24), 12, outline=False)
    seal(can, t, wt('Kriegsgericht'), 'KRIEGSGERICHT', 560, 1130, r=200, col=(170, 36, 24), rot=-10, sub='DROHTE')
    focus(can, t, tn, 'NIE GEMELDET', 'serif', 82, CREAM, 380)
    return can

# ---------------- S18 world map: Canada ----------------
def s_canada(t):
    t0 = 83.6; u = eio((t - t0) / 4.6)
    c = camlerp((-50, 14, 185), (-58, 12, 178), u)
    can, cam = draw_map(c, ('Canada', 'Germany'))
    g = cam.p(*GER); v = cam.p(*VAN)
    ink_dot(can, *g, 9, RUST)
    k = eio((t - t0 - 0.3) / 2.4)
    pts = bez(g, ((g[0] + v[0]) / 2, min(g[1], v[1]) - 330), v, 60)
    pp = route(can, pts, k, RUST, 6)
    if len(pp) > 1 and k < 1: put(can, sprite('•', 'serif', 40, RUST, False), *pp[-1])
    if k >= 1: ink_dot(can, *v, 10, RUST); maplabel(can, t, wt('Kanada') - 0.1, 'VANCOUVER', v[0], v[1] + 50, size=38, side='r')
    maplabel(can, t, wt('Kanada'), 'KANADA', *cam.p(-102, 60), size=64, side='c', col=INK)
    focus(can, t, wt('1953'), '1953', 'serif', 170, INK, 1330)
    reveal(can, t, wt('wanderte'), 'STIGLER WANDERT AUS', 'cond', 56, RUST, 1470)
    return can

# ---------------- S19 newspaper notice ----------------
BG_NEWS = paper((48, 38, 28), 0.12)
def clipping():
    w, h = 780, 980; im = paper((226, 219, 200), 0.10, False).crop((0, 0, w, h)); d = ImageDraw.Draw(im)
    rng = np.random.default_rng(9)
    for y in range(520, 940, 34):
        x = 50
        while x < w - 60:
            ww = rng.integers(30, 120); d.line((x, y, min(x + ww, w - 50), y), fill=(120, 112, 96), width=10); x += ww + 18
    d.line((40, 40, w - 40, 40), fill=INK, width=4); d.line((40, 52, w - 40, 52), fill=INK, width=2)
    m = Image.new('L', (w, h), 255); md = ImageDraw.Draw(m)
    for x in range(0, w, 14): md.polygon([(x, h), (x + 7, h - rng.integers(4, 16)), (x + 14, h)], fill=0)
    im.putalpha(m); out = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0))
    sh = Image.new('RGBA', out.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((46, 52, 40 + w, 46 + h), fill=(0, 0, 0, 160))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); out.alpha_composite(im, (40, 40))
    return out
CLIP = clipping()
def s_notice(t):
    can = BG_NEWS.copy(); t0 = 87.8
    k = eout((t - t0) / 0.55); put(can, CLIP.rotate(lerp(-8, -2.5, k), resample=Image.BICUBIC, expand=True), 540, 900, lerp(0.95, 0.85, k), k)
    cascade(can, t, wt('suchte'), 'GESUCHT', 'serif', 120, INK, 590, track=6, step=0.05)
    focus(can, t, wt('1986'), 'SEIT 1986', 'cond', 64, RUST, 720)
    reveal(can, t, wt('unbekannten'), 'DER UNBEKANNTE PILOT', 'serif', 72, CREAM, 1440, dur=0.7)
    return can

# ---------------- S20 reunion print ----------------
def s_reunion(t):
    can, (pcx, pcy, pw, ph) = print_photo('p09', t, 92.4, 99.6, -3.0, -1.0)
    focus(can, t, wt('1990'), '1990', 'serif', 120, CREAM, 300 + 40, t1=None)
    cascade(can, t, wt('meldete', 93), 'STIGLER MELDET SICH', 'cond', 58, GOLD, 1300, t1=wt('enge') - 0.25, track=5)
    if t > wt('beiden'):
        k = eio((t - wt('beiden')) / 0.7)
        a = (pcx - pw * 0.33, pcy - ph * 0.30); b = (pcx + pw * 0.38, pcy - ph * 0.25)
        pts = bez(a, ((a[0] + b[0]) / 2, pcy - ph * 0.62), b, 50)
        stroke(can, partial(pts, k), GOLD, 6)
    focus(can, t, wt('enge'), 'ENGE FREUNDE', 'serif', 110, CREAM, 1330)
    return can

# ---------------- S21 2008 month strip ----------------
MON = ['JAN', 'FEB', 'MÄR', 'APR', 'MAI', 'JUN', 'JUL', 'AUG', 'SEP', 'OKT', 'NOV', 'DEZ']
def s_2008(t):
    can = BG_DARK.copy(); t0 = 99.2
    x0, x1, y = 170, 910, 960; cw = (x1 - x0) / 12
    k = eio((t - t0) / 0.9); d = ImageDraw.Draw(can)
    for i, m in enumerate(MON):
        a = clamp((t - t0 - i * 0.05) / 0.3)
        if a <= 0: continue
        xa = x0 + i * cw
        d.rectangle((xa + 3, y - 40, xa + cw - 3, y + 40), outline=(200, 186, 160, int(200 * a)), width=2)
        put(can, sprite(m, 'cond', 26, (200, 186, 160), False, 1), xa + cw / 2, y, 1.0, a)
    focus(can, t, wt('2008'), '2008', 'serif', 150, CREAM, 380)
    for idx, t1, name, sub, yy in ((2, wt('März'), 'FRANZ STIGLER', '92 JAHRE', 680), (10, wt('November'), 'CHARLIE BROWN', '86 JAHRE', 1250)):
        if t < t1: continue
        xm = x0 + (idx + 0.5) * cw; q = eout((t - t1) / 0.4)
        d = ImageDraw.Draw(can); d.rectangle((xm - cw / 2 + 3, y - 40, xm + cw / 2 - 3, y + 40), fill=GOLD + (int(230 * q),))
        put(can, sprite(MON[idx], 'cond', 26, DEEP, False, 1), xm, y, 1.0, q)
        ya = y - 50 if yy < y else y + 50; yb = yy + (60 if yy < y else -60)
        stroke(can, partial([(xm, ya), (xm, yb)], q), GOLD, 4, outline=False)
        cx = min(max(xm, 300), 660)
        cascade(can, t, t1 + 0.1, name, 'serif', 64, CREAM, yy, cx=cx, track=1)
        tsub = wt('92') if idx == 2 else wt('86.')
        reveal(can, t, tsub, sub, 'cond', 52, GOLD, yy + (-80 if yy < y else 80), cx=cx)
    return can

# ---------------- S22 CTA ----------------
def s_cta(t):
    can, _ = print_photo('p01', t, 109.0, 112.8, 2.5, 1.0, wmax=900)
    focus(can, t, wt('Kanntet'), 'KANNTET IHR', 'serif', 100, CREAM, 1210)
    focus(can, t, wt('diese', 109), 'DIESE GESCHICHTE?', 'serif', 100, GOLD, 1330)
    plate(can, t, wt('Schreibt'), 'SCHREIBT ES IN DIE KOMMENTARE!', 1460, size=44)
    return can

# (start, end, fn, transition into this scene)
SC = [(0.0, 6.55, s_hook, 'cut'), (6.35, 11.95, s_dossier, 'dip'), (11.7, 15.6, s_calendar, 'slide_l'),
      (15.35, 19.75, s_brown, 'fade'), (19.5, 23.85, s_crew, 'slide_r'), (23.6, 28.75, s_mapbremen, 'fade'),
      (28.5, 34.3, s_damage, 'fade'), (34.0, 39.85, s_ledger, 'slide_l'), (39.6, 46.55, s_bf109, 'fade'),
      (46.3, 50.35, s_tally, 'dip'), (50.1, 54.45, s_wreck, 'fade'), (54.2, 58.5, s_roedel, 'slide_r'),
      (58.25, 62.55, s_quote, 'fade'), (62.2, 67.65, s_sweden, 'fade'), (67.4, 72.55, s_escort, 'slide_l'),
      (72.2, 79.1, s_salute, 'fade'), (78.85, 83.9, s_report, 'slide_r'), (83.6, 88.0, s_canada, 'dip'),
      (87.75, 92.75, s_notice, 'fade'), (92.4, 99.45, s_reunion, 'fade'), (99.2, 109.3, s_2008, 'dip'),
      (109.0, TEND, s_cta, 'fade')]

DIPC = Image.new('RGBA', (W, H), (20, 14, 8, 255))
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
    if t > TEND - 0.7: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * clamp((t - TEND + 0.7) / 0.6)))))
    return img.convert('RGB')

GR = [np.random.default_rng(i).normal(0, 4.5, (H // 2, W // 2)).astype(np.int16) for i in range(6)]
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
        out = sys.argv[2]; a, b = float(sys.argv[3]), float(sys.argv[4])
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'fast', out], stdin=subprocess.PIPE)
        for n in range(int(round(a * FPS)), int(round(b * FPS))):
            p.stdin.write(grain(frame(n / FPS), n).tobytes())
        p.stdin.close(); p.wait(); print('rc', p.returncode)
