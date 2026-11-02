# Bismarck, CDM Short in style A, exactly the Egon Mayer v6 way (egon/code/eg.py):
# hook = full-bleed blue-toned Bismarck film with the words typing on; at "Bismarck" two film prints of the ship drop in;
# the hook pulls back and turns out to be a print on one big table of blue-toned prints; the camera travels left/right/up/down
# from group to group, each new group scattering in with the move (from the direction of travel, big and turning).
# Main prints play film (not stills). Type is centred (x = 540) and kept inside the safe area. No fade at the end.
import sys, os, json, math, subprocess, functools, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, E + '../egon/code')
import eg
from eg import W, H, FPS, CREAM, YEL, eout, eio, lerp, clamp, card, paste, print_im, quote, title, strip, label, tone, DARK, LIGHT, finish, dblur
WORDS = json.load(open(E + 'words.json'))
def ws(s, after=0.0):
    for w, a, b in WORDS:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a - 0.04
    raise KeyError(s)

# ---------- footage ----------
CL = E + 'clipL/'
@functools.lru_cache(None)
def nfr(k): return len(os.listdir(CL + k))
@functools.lru_cache(maxsize=64)
def _fr(k, i): return Image.open(CL + '%s/%05d.jpg' % (k, i)).convert('RGB')
def film(k, tt): return _fr(k, min(nfr(k), max(1, int(max(0.0, tt) * 25) + 1)))   # forward only
def FP(k, tt, wd, seed, cap=None, sp=1.0): return print_im(film(k, tt * sp), wd, True, cap, seed)
@functools.lru_cache(maxsize=8)
def lut_print(wd): return print_im(Image.open(E + 'img/lut_blur.jpg').convert('RGB').crop((0, 0, 1632, 2200)), wd, True, 'Günther Lütjens', 51)
# hook background: the portrait 9:16 cut of the Bismarck behind the guns (clip/hook, 30 fps), blue-toned like the Egon hook
HC = E + 'clip/hook/'
@functools.lru_cache(maxsize=16)
def _hk(i): return Image.open(HC + '%05d.jpg' % i).convert('RGB')
def hookbg(tt, dark=0.62):
    n = len(os.listdir(HC)); im = _hk(min(n, max(1, int(tt * 30) + 1))); g = np.asarray(ImageOps.grayscale(im).resize((W, H), Image.BICUBIC), np.float32) / 255
    g = np.clip((g - 0.5) * 1.15 + 0.5, 0, 1); a = DARK + g[..., None] * (LIGHT * 1.25 - DARK)
    yy = np.linspace(0, 1, H)[:, None, None]; a *= (1.0 - (1 - dark) * np.clip((yy - 0.35) / 0.35, 0, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')

# ---------- the table ----------
TW, TH = 2700, 3300
PILE = ['dist', 'esc', 'fire1', 'flash', 'smk', 'bow', 'hor', 'plot', 'sword', 'torp', 'fleet', 'surv', 'hood', 'scut', 'splash', 'wreck', 'wreck2', 'side', 'kgv', 'rod']
def pile_im(i):
    k = PILE[i % len(PILE)]; return _fr(k, max(1, int(nfr(k) * ((i * 0.37) % 0.8 + 0.1))))
@functools.lru_cache(None)
def table():
    cache = E + 'table2.png'
    if os.path.exists(cache): return Image.open(cache).convert('RGB')
    rng = np.random.default_rng(5); can = Image.new('RGBA', (TW, TH), (20, 24, 40, 255))
    for k in range(90):
        P_ = print_im(pile_im(int(rng.integers(1000))), int(rng.uniform(560, 820)), True, None, seed=int(rng.integers(50))).rotate(rng.uniform(-30, 30), expand=True, resample=Image.BICUBIC)
        x, y = int(rng.uniform(0, TW)), int(rng.uniform(0, TH))
        sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.6))); sh = sh.filter(ImageFilter.GaussianBlur(10))
        for dx in (-TW, 0, TW):
            for dy in (-TH, 0, TH): paste(can, sh, x + dx + 8, y + dy + 16); paste(can, P_, x + dx, y + dy)
    T_ = tone(can, DARK, LIGHT * 0.5, 1.2).filter(ImageFilter.GaussianBlur(3.0))
    big = Image.new('RGB', (TW + 1400, TH + 2300))
    for dx in (0, TW):
        for dy in (0, TH): big.paste(T_, (dx, dy))
    big.save(cache); return big
BGN = 560
@functools.lru_cache(None)
def bg_list():
    rng = np.random.default_rng(11); xs = [a[0] for a in ANC]; ys = [a[1] for a in ANC]
    x0, x1, y0, y1 = min(xs) - 900, max(xs) + W + 900, min(ys) - 900, max(ys) + H + 900
    return [(int(rng.integers(48)), rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(-30, 30), rng.uniform(-7, 7), rng.uniform(-7, 7), rng.uniform(-0.3, 0.3)) for _ in range(BGN)]
@functools.lru_cache(maxsize=64)
def bg_img(i):
    P_ = print_im(pile_im(i * 7 + 3), 520 + (i * 37) % 260, True, None, i)
    T_ = tone(P_.convert('RGB'), DARK, LIGHT * 0.92, 1.1).filter(ImageFilter.GaussianBlur(1.3)).convert('RGBA'); T_.putalpha(P_.getchannel('A'))
    return T_
def bg_layer(can, t, cx, cy):
    for i, x, y, r, vx, vy, vr in bg_list():
        X, Y = x + vx * t - cx, y + vy * t - cy
        if X < -650 or X > W + 650 or Y < -650 or Y > H + 650: continue
        card(can, bg_img(i), X, Y, r + vr * t)
def table_view(cx, cy):
    T_ = table(); x0, y0 = cx % TW, cy % TH
    return T_.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + W, y0 + H))

# ---------- prints scattering in with the camera (eg.enter) ----------
CUR = [0.0]; CNT = [0]; CURJ = [0]
def enter(c, P_, t, to, r1, ox, oy, drift=(0, 0, 0), main=False):
    a = CUR[0]; i = CNT[0]; CNT[0] += 1; j = CURJ[0]
    if j > 0: dx, dy = ANC[j][0] - ANC[j - 1][0], ANC[j][1] - ANC[j - 1][1]
    else: dx, dy = 1.0, 0.0
    n = math.hypot(dx, dy) or 1.0; dx, dy = dx / n, dy / n
    t0 = a - PRE + 0.12 * i
    if t < t0: return
    jit = ((i * 97 + j * 31) % 7 - 3) * 70.0
    def pos(tt):
        u = eout(clamp((tt - t0) / 1.35)); d = tt - a
        fx, fy = to[0] + dx * 680 - dy * jit, to[1] + dy * 680 + dx * jit
        sc = 1.0 + 0.32 * (1 - u) + (0.10 if main else 0.07) * (1 - eout(clamp((tt - t0) / 3.4))) - 0.008 * max(0.0, d)
        return lerp(fx, to[0], u) + drift[0] * d + ox, lerp(fy, to[1], u) + drift[1] * d + oy, lerp(r1 + (16 if i % 2 else -16), r1, u) + drift[2] * d, sc
    x, y, r, sc = pos(t); x2, y2, _, _ = pos(t + 1 / FPS)
    card(c, P_, x, y, r, ((x2 - x) * 1.4, (y2 - y) * 1.4), sc=sc)
def later(c, P_, t, t0, to, r1, ox, oy, frm=(1, 0), drift=(2, 3, 0.06)):
    """a print that joins a group later in its scene (on a word): from the side, big and turning, then slowly pulling back"""
    if t < t0: return
    def pos(tt):
        u = eout(clamp((tt - t0) / 1.2)); d = tt - t0
        sc = 1.0 + 0.30 * (1 - u) + 0.08 * (1 - eout(clamp(d / 3.4))) - 0.008 * d
        return lerp(to[0] + frm[0] * 760, to[0], u) + drift[0] * d + ox, lerp(to[1] + frm[1] * 760, to[1], u) + drift[1] * d + oy, lerp(r1 + (16 if frm[0] + frm[1] > 0 else -16), r1, u) + drift[2] * d, sc
    x, y, r, sc = pos(t); x2, y2, _, _ = pos(t + 1 / FPS)
    card(c, P_, x, y, r, ((x2 - x) * 1.4, (y2 - y) * 1.4), sc=sc)
def lt(t, j): return t - (SCN[j][0] - PRE)   # film clock of a scene's prints: they start playing as they scatter in
def circle_arrow(can, t, t0, cx, cy, rx, ry, dur=1.1):
    if t < t0: return
    u = eio(clamp((t - t0) / dur)); a0 = math.radians(200); a1 = a0 + u * math.radians(320)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pts = [(cx + rx * math.cos(a0 + (a1 - a0) * i / 80), cy + ry * math.sin(a0 + (a1 - a0) * i / 80)) for i in range(81)]
    d.line(pts, fill=CREAM + (240,), width=7, joint='curve')
    if u > 0.05:
        (xa, ya), (xb, yb) = pts[-4], pts[-1]; ang = math.atan2(yb - ya, xb - xa)
        for s in (2.6, -2.6): d.line((xb, yb, xb - 30 * math.cos(ang + s * 0.2), yb - 30 * math.sin(ang + s * 0.2)), fill=CREAM + (240,), width=7)
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.5))); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)), (3, 5)); can.alpha_composite(L)

# ---------- scenes on the table ----------
VON1 = ws('Von', 18)
def s_1941(c, t, ox, oy):
    j = 1; enter(c, FP('dist', lt(t, j), 1000, 11), t, (540, 560), -2, ox, oy, (3, 2, 0.08), main=True)
    enter(c, FP('esc', lt(t, j), 620, 12, sp=0.85), t, (760, 930), 5, ox, oy, (-3, 2, -0.1))
    title(c, t, '1941', ['ERSTE UND EINZIGE', 'FEINDFAHRT'], 1390, ws('1941'), [ws('ersten'), ws('Feindfahrt')], ox, oy, True, 200, 62, cps=22)
def s_dk(c, t, ox, oy):
    j = 2; enter(c, FP('fire1', lt(t, j), 1000, 21), t, (540, 560), 3, ox, oy, (-3, 2, -0.08), main=True)
    later(c, FP('hood', (t - ws('Schlachtkreuzer')) * 0.85, 600, 22, cap='HMS Hood'), t, ws('Schlachtkreuzer') - 0.1, (720, 930), -5, ox, oy, (1, 0.2))
    quote(c, t, [[('DÄNEMARKSTRASSE', ws('Dänemarkstraße'))]], 1290, ox, oy, 74, col={0: YEL})
    quote(c, t, [[('SCHLACHTKREUZER', ws('Schlachtkreuzer')), ('HOOD', ws('Hood'))]], 1390, ox, oy, 60)
def s_fire(c, t, ox, oy):
    j = 3; enter(c, FP('flash', lt(t, j), 1000, 31), t, (540, 560), -2, ox, oy, (3, 2, 0.08), main=True)
    title(c, t, '8', ['MINUTEN', 'FEUER'], 1380, ws('acht'), [ws('Minuten'), ws('Feuer')], ox, oy, True, 210, 74, ['DIE HOOD FLOG IN DIE LUFT'], ws('flog') - 0.5, cps=18)
def s_three(c, t, ox, oy):
    j = 4; enter(c, FP('smk', lt(t, j), 1000, 41), t, (540, 560), 2, ox, oy, (-3, 2, -0.08), main=True)
    quote(c, t, [[('VON', VON1), ('ÜBER', ws('über', 18)), ('1.400', ws('1.400')), ('MANN', ws('Mann', 19))]], 1250, ox, oy, 62)
    title(c, t, '3', ['ÜBERLEBENDE'], 1400, ws('drei') - 0.1, ws('überlebten', 19), ox, oy, True, 220, 80, cps=30)
def s_leak(c, t, ox, oy):
    j = 5; enter(c, FP('bow', lt(t, j), 1000, 51), t, (540, 560), 3, ox, oy, (3, 2, 0.08), main=True)
    later(c, FP('splash', t - ws('getroffen'), 600, 52), t, ws('getroffen') - 0.1, (760, 930), 6, ox, oy, (1, 0.2))
    quote(c, t, [[('DOCH', ws('Doch')), ('AUCH', ws('auch', 21)), ('DIE', ws('die', 21.4)), ('BISMARCK', ws('Bismarck', 21.5))], [('WAR', ws('war', 22)), ('GETROFFEN', ws('getroffen'))]], 1260, ox, oy, 60, tout=ws('Aus', 22.7) - 0.1)
    quote(c, t, [[('LECK', ws('Leck')), ('IM', ws('im', 23.5)), ('BUG', ws('Bug'))]], 1300, ox, oy, 86, col={0: YEL})
    quote(c, t, [[('TREIBSTOFF', ws('Treibstoff')), ('LIEF', ws('lief', 24)), ('AUS', ws('aus', 24.5))]], 1410, ox, oy, 58)
def s_lut(c, t, ox, oy):
    j = 6; enter(c, lut_print(620), t, (540, 650), -2, ox, oy, (2, 3, 0.08), main=True)
    quote(c, t, [[('ADMIRAL', ws('Admiral')), ('LÜTJENS', ws('Lütjens'))]], 1330, ox, oy, 70)
    strip(c, t, ws('Kurs') - 0.45, ['KURS AUF FRANKREICH'], 540 + ox, 1430 + oy)
def s_navy(c, t, ox, oy):
    j = 7; enter(c, FP('plot', lt(t, j), 1000, 71), t, (540, 560), 2, ox, oy, (-3, 2, -0.08), main=True)
    quote(c, t, [[('DIE', ws('Die', 27.8)), ('ROYAL', ws('Royal')), ('NAVY', ws('Navy'))]], 1280, ox, oy, 64)
    quote(c, t, [[('DUTZENDE', ws('Dutzenden')), ('SCHIFFE', ws('Schiffen'))]], 1390, ox, oy, 86, col={0: YEL})
def s_sword(c, t, ox, oy):
    j = 8; enter(c, FP('sword', lt(t, j), 1000, 81), t, (540, 560), -3, ox, oy, (3, 2, 0.08), main=True)
    later(c, FP('sw', t - ws('Swordfish'), 520, 82, sp=0.6), t, ws('Swordfish') - 0.1, (330, 930), 5, ox, oy, (-1, 0.2))
    quote(c, t, [[('ZWEI', ws('Zwei')), ('TAGE', ws('Tage')), ('SPÄTER', ws('später'))]], 1210, ox, oy, 56)
    title(c, t, '15', ['SWORDFISH'], 1380, ws('15'), ws('Swordfish'), ox, oy, True, 210, 84, ['VOM FLUGZEUGTRÄGER ARK ROYAL'], ws('vom') - 0.3, cps=20)
def s_torp(c, t, ox, oy):
    j = 9; enter(c, FP('torp', lt(t, j), 1000, 91), t, (540, 560), 2, ox, oy, (-3, 2, -0.08), main=True)
    quote(c, t, [[('EIN', ws('Ein', 36.5)), ('TORPEDO', ws('Torpedo'))]], 1280, ox, oy, 80)
    quote(c, t, [[('RUDER', ws('blockierte')), ('BLOCKIERT', ws('blockierte') + 0.15)]], 1390, ox, oy, 86, col={0: YEL})
def s_circ(c, t, ox, oy):
    j = 10; enter(c, FP('hor', lt(t, j), 1000, 101), t, (540, 600), -2, ox, oy, (3, 2, 0.08), main=True)
    circle_arrow(c, t, ws('nur', 40) - 0.1, 540 + ox, 600 + oy, 380, 150)
    quote(c, t, [[('NUR', ws('nur', 40)), ('NOCH', ws('noch', 40)), ('IM', ws('im', 40.6)), ('KREIS', ws('Kreis'))]], 1290, ox, oy, 84, col={0: YEL})
    quote(c, t, [[('KEIN', ws('nicht', 42) - 0.1), ('ENTKOMMEN', ws('entkommen') - 0.15)]], 1400, ox, oy, 58)
def s_fleet(c, t, ox, oy):   # the final battle stays in one group up to the bridge hit, so both battleships stay in view
    j = 11; enter(c, FP('fleet', lt(t, j), 1000, 111), t, (540, 520), 2, ox, oy, (-3, 2, -0.08), main=True)
    later(c, FP('kgv', (t - ws('Schlachtschiffe', 44)) * 0.9, 540, 112, cap='King George V'), t, ws('Schlachtschiffe', 44) - 0.1, (300, 900), -5, ox, oy, (-1, -0.2))
    later(c, FP('rod', t - ws('Rodney'), 500, 113, cap='Rodney'), t, ws('Rodney') - 0.3, (780, 960), 5, ox, oy, (1, 0.2))
    quote(c, t, [[('AM', ws('Am', 43)), ('NÄCHSTEN', ws('nächsten')), ('MORGEN', ws('Morgen'))]], 1330, ox, oy, 66, tout=ws('Ein', 47.6) - 0.1)
    quote(c, t, [[('EIN', ws('Ein', 47.6)), ('TREFFER', ws('Treffer'))]], 1300, ox, oy, 62)
    quote(c, t, [[('BRÜCKE', ws('Brücke')), ('ZERSTÖRT', ws('Brücke') + 0.15)]], 1410, ox, oy, 86, col={0: YEL})
def s_scut(c, t, ox, oy):
    j = 12; enter(c, FP('scut', lt(t, j), 1000, 121), t, (540, 560), -2, ox, oy, (3, 2, 0.08), main=True)
    quote(c, t, [[('DER', ws('Der', 51.6)), ('ERSTE', ws('Erste')), ('OFFIZIER', ws('Offizier'))]], 1280, ox, oy, 60)
    quote(c, t, [[('SELBST', ws('selbst')), ('VERSENKT', ws('versenken'))]], 1390, ox, oy, 86, col={0: YEL})
def s_surv(c, t, ox, oy):
    j = 13; enter(c, FP('surv', lt(t, j), 1000, 131), t, (540, 560), 2, ox, oy, (-3, 2, -0.08), main=True)
    quote(c, t, [[('VON', ws('Von', 56)), ('ÜBER', ws('über', 56)), ('2.200', ws('2.200')), ('MANN', ws('Mann', 57))]], 1150, ox, oy, 62)
    title(c, t, '114', ['ÜBERLEBENDE'], 1400, ws('114'), ws('überlebten', 58), ox, oy, True, 210, 80, cps=30)
def s_wreck(c, t, ox, oy):
    j = 14; enter(c, FP('wreck', lt(t, j), 1000, 141), t, (540, 540), -2, ox, oy, (-2, 3, -0.08), main=True)
    later(c, FP('wreck2', t - ws('Robert'), 600, 142), t, ws('Robert') - 0.1, (740, 920), 5, ox, oy, (1, 0.2))
    quote(c, t, [[('ROBERT', ws('Robert')), ('BALLARD', ws('Ballard'))]], 1250, ox, oy, 70)
    strip(c, t, ws('fünfzig') - 0.4, ['1989'], 540 + ox, 1325 + oy)
    title(c, t, '4.791', ['METER', 'TIEFE'], 1450, ws('fünf', 65), [ws('Kilometern'), ws('Tiefe')], ox, oy, True, 180, 66, cps=18)

# ---------- hook (Egon: film full-bleed, words typing on, the name brings prints, then it pulls back onto the table) ----------
H1 = ws('Bismarck', 6)
ZS = ws('Im', 6.9) - 0.25; ZE = ZS + 0.55
T2b = ZE + 0.15
ZH = 1.8
HOOKP = [('side', 780, 520, 520, -4, 0.0), ('dist', 470, 730, 880, 6, 0.3)]   # film prints of the ship at "Bismarck": (clip, width, x, y, rotation, delay)
def hookcard_print(tt): return print_im(hookbg(tt).convert('RGB').resize((600, 1067), Image.LANCZOS), 600, False, None, 7)
def hook_prints(c, t, f=1.0, ox=0.0, oy=0.0, blur=True):
    for i, (k, wd, x1, y1, r1, dl) in enumerate(HOOKP):
        t0 = H1 + dl
        if t < t0: continue
        def pos(tt):
            u = eout((tt - t0) / (1.0 * eg.SLOW)); return x1 + 2 * (tt - t0), lerp(-800, y1, u) + 3 * (tt - t0), lerp(r1 + 9, r1, u)
        x, y, r = pos(t); x2, y2, _ = pos(t + 1 / FPS); d = t - t0; sc = 1.0 + 0.25 * (1 - eout(d / 2.8)) - 0.01 * d
        P_ = FP(k, (t - t0) * (0.75 if k == 'side' else 1.0) + (0.0 if k == 'side' else 3.5), wd, 30 + i)
        card(c, P_, 540 + (x - 540) * f + ox, 960 + (y - 960) * f + oy, r, ((x2 - x) * 1.6 * f, (y2 - y) * 1.6 * f) if blur else (0, 0), sc=sc * f)
def s_hookcard(c, t, ox, oy):
    card(c, hookcard_print(t), 540 + ox, 960 + oy, 0)
    hook_prints(c, t, 1 / ZH, ox, oy, False)
def qlines(can, t, lines, y0, size, tout, cols=None, lh=1.04):
    """hook type: one line per call so short lines stay big and only long words shrink to the 700 px width"""
    y = y0
    for i, l in enumerate(lines):
        sz = eg.fit([' '.join(w_ for w_, _ in l)], size, 900, -2)
        quote(can, t, [l], y + sz * 0.5, size=sz, tout=tout, col={0: (cols or {}).get(i, CREAM)}); y += sz * lh
def hook_frame(t):
    can = hookbg(t)
    qlines(can, t, [[('EINES', ws('Eines')), ('DER', ws('der'))], [('GRÖSSTEN', ws('größten'))], [('SCHLACHTSCHIFFE', ws('Schlachtschiffe'))], [('EUROPAS', ws('Europas'))]],
           760, 120, ws('wurde') - 0.08, {2: YEL})
    qlines(can, t, [[('WURDE', ws('wurde')), ('VON', ws('von')), ('EINEM', ws('einem'))], [('LANGSAMEN', ws('langsamen'))], [('DOPPELDECKER', ws('Doppeldecker'))],
                    [('MIT', ws('mit'))], [('STOFFBESPANNUNG', ws('Stoffbespannung'))], [('GESTOPPT.', ws('gestoppt'))]], 640, 110, ws('Ihr') - 0.12, {2: YEL})
    hook_prints(can, t)
    qlines(can, t, [[('IHR', ws('Ihr')), ('NAME', ws('Name')), ('WAR', ws('war'))], [('BISMARCK', ws('Bismarck', 6))]], 1150, 120, ZS - 0.12, {1: YEL})
    return can

# ---------- camera (eg.campos / table_frame) ----------
GX, GY = 1380, 2160
PATH = [(-1, 0), (0, 0), (1, 0), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (2, 3)]
SCN = [(ZS, s_hookcard), (T2b, s_1941), (ws('In', 11.7), s_dk), (ws('Nach'), s_fire), (VON1, s_three), (ws('Doch'), s_leak), (ws('Admiral') - 0.3, s_lut),
       (ws('Die', 27.8), s_navy), (ws('Zwei'), s_sword), (ws('Ein', 36.5), s_torp), (ws('Die', 39.4), s_circ), (ws('Am', 43), s_fleet), (ws('Der', 51.6), s_scut),
       (ws('Von', 56), s_surv), (ws('Ihr', 60), s_wreck)]
ANC = [(p[0] * GX, p[1] * GY) for p in PATH]
PRE, POST = 0.25, 1.25
TEND = WORDS[-1][2] + 1.3
def campos(t):
    k = max(i for i, (a, _) in enumerate(SCN) if a <= t) if t >= SCN[0][0] else 0
    nxt = k + 1 if k + 1 < len(SCN) and t >= SCN[k + 1][0] - PRE else None
    if nxt is not None: k, prev = nxt, k
    else: prev = k - 1 if k > 0 and t < SCN[k][0] + POST else None
    if prev is None: return ANC[k], (0.0, 0.0), k, None
    b = SCN[k][0]; f = lambda tt: eio(clamp((tt - (b - PRE)) / (PRE + POST)))
    u, u2 = f(t), f(t + 1 / FPS); (ax, ay), (bx, by) = ANC[prev], ANC[k]
    return (lerp(ax, bx, u), lerp(ay, by, u)), ((bx - ax) * (u2 - u), (by - ay) * (u2 - u)), k, (prev, u)
def zoom_at(t):
    k = max([i for i, (a, _) in enumerate(SCN) if a <= t] or [0]); a = SCN[k][0] + POST
    if k == 0: return lerp(ZH, 1.0, eio((t - ZS) / (ZE - ZS)))
    return 1.0 + 0.006 * max(0.0, t - a)
def table_frame(t):
    (cx, cy), (vx, vy), k, tr = campos(t)
    can = table_view(cx, cy).convert('RGBA')
    bg_layer(can, t, cx, cy)
    for j in range(max(0, k - 1), min(len(SCN), k + 2)):
        CUR[0] = SCN[j][0]; CNT[0] = 0; CURJ[0] = j; SCN[j][1](can, t, ANC[j][0] - cx, ANC[j][1] - cy)
    if tr is not None:
        prev, u = tr; can = dblur(can, vx * 0.6, vy * 0.6)
        z = lerp(zoom_at(SCN[k][0] - PRE), 1.0, u)
    else: z = zoom_at(t)
    if z > 1.0005:
        bw, bh = W / z, H / z; can = can.resize((W, H), Image.BICUBIC, box=(540 - 540 / z, 960 - 960 / z, 540 - 540 / z + bw, 960 - 960 / z + bh))
    return can
def frame(t):
    if t < ZS: img = hook_frame(t)
    elif t < ZS + 0.15: img = Image.blend(hook_frame(t), table_frame(t), (t - ZS) / 0.15)
    else: img = table_frame(t)
    return finish(img, t)   # no fade at the end

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); P_ = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = frame(t).convert('RGBA'); d = ImageDraw.Draw(f)
            if os.environ.get('UI'):
                d.rectangle((0, 0, W, 290), outline=(0, 255, 255, 255), width=4); d.rectangle((930, 680, W, 1580), outline=(0, 255, 255, 255), width=4); d.rectangle((0, 1580, W, H), outline=(0, 255, 255, 255), width=4)
            d.text((10, 300), '%.2f' % t, fill=(255, 0, 255, 255)); P_.paste(f.convert('RGB').resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P_.save(E + sys.argv[2], quality=85); sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', E + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
        if n % 30 == 0: print('t', n / FPS, flush=True)
    p.stdin.close(); p.wait(); print('rc', p.returncode)
