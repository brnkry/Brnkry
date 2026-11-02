# Bismarck, CDM Short in style A with FULL-SCREEN films:
# every scene is a colour (or b/w) film that fills the screen; it is really a big print lying on the table.
# At each new sentence the camera pulls back so the film turns into a print on the table (blue-toned pile around it, prints moving),
# travels left/right/up/down to the next group while the next film-print scatters in from the direction of travel (big, turning),
# and zooms into it until it fills the screen again. Type, extra prints and the Lütjens cutout sit on the film-print and travel with it.
import sys, os, json, math, subprocess, functools, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, E + '../egon/code')
import eg
from eg import W, H, FPS, CREAM, YEL, eout, eio, lerp, clamp, card, paste, print_im, quote, title, strip, label, tone, DARK, LIGHT, finish
WORDS = json.load(open(E + 'words.json'))
def ws(s, after=0.0):
    for w, a, b in WORDS:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a - 0.04
    raise KeyError(s)

# ---------- footage ----------
CL = E + 'clip/'
@functools.lru_cache(None)
def nfr(k): return len(os.listdir(CL + k))
@functools.lru_cache(maxsize=48)
def _fr(k, i): return Image.open(CL + '%s/%05d.jpg' % (k, i)).convert('RGB')
def raw(k, tt): return _fr(k, min(nfr(k), max(1, int(tt * FPS) + 1)))   # forward only
ROWS = None
@functools.lru_cache(maxsize=24)
def full(k, i):
    """full-screen frame: upscaled crop, a little sharpening, darker bands behind the type"""
    global ROWS
    im = _fr(k, min(nfr(k), max(1, i)))
    if im.size != (W, H): im = im.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    if ROWS is None:
        y = np.arange(H, dtype=np.float32)
        ROWS = (1 - 0.30 * np.exp(-((y - 560) / 260) ** 2) - 0.42 * np.exp(-((y - 1330) / 300) ** 2))[:, None, None]
    return Image.fromarray((np.asarray(im, np.float32) * ROWS).astype(np.uint8))
def film(k, tt): return full(k, min(nfr(k), max(1, int(tt * FPS) + 1)))
def FP(k, tt, wd, seed, cap=None): return print_im(raw(k, tt), wd, True, cap, seed)

@functools.lru_cache(None)
def lutjens():
    im = Image.open(E + 'img/lut_cut.png').convert('RGBA').crop((0, 0, 1632, 2100))
    return im.resize((int(1632 * 1020 / 2100), 1020), Image.LANCZOS)

# ---------- things that lie on a film-print ----------
def sec(can, P_, t, t0, to, r1, frm=(1, 0), drift=(2, 3, 0.06)):
    """an extra print scattering onto the film: from the side, big and turning, then slowly pulling back, always drifting"""
    if t < t0: return
    def pos(tt):
        u = eout(clamp((tt - t0) / 1.2)); d = tt - t0
        sc = 1.0 + 0.30 * (1 - u) + 0.08 * (1 - eout(clamp(d / 3.4))) - 0.008 * d
        return lerp(to[0] + frm[0] * 760, to[0], u) + drift[0] * d, lerp(to[1] + frm[1] * 760, to[1], u) + drift[1] * d, lerp(r1 + 16 * (1 if frm[0] + frm[1] > 0 else -1), r1, u) + drift[2] * d, sc
    x, y, r, sc = pos(t); x2, y2, _, _ = pos(t + 1 / FPS)
    card(can, P_, x, y, r, ((x2 - x) * 1.4, (y2 - y) * 1.4), sc=sc)
def circle_arrow(can, t, t0, cx, cy, rx, ry, dur=1.1):
    if t < t0: return
    u = eio(clamp((t - t0) / dur)); a0 = math.radians(200); a1 = a0 + u * math.radians(320)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pts = [(cx + rx * math.cos(a0 + (a1 - a0) * i / 80), cy + ry * math.sin(a0 + (a1 - a0) * i / 80)) for i in range(81)]
    d.line(pts, fill=YEL + (245,), width=10, joint='curve')
    if u > 0.05:
        (xa, ya), (xb, yb) = pts[-4], pts[-1]; ang = math.atan2(yb - ya, xb - xa)
        d.polygon([(xb + 18 * math.cos(ang), yb + 18 * math.sin(ang)), (xb - 40 * math.cos(ang - .5), yb - 40 * math.sin(ang - .5)), (xb - 40 * math.cos(ang + .5), yb - 40 * math.sin(ang + .5))], fill=YEL + (245,))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.5))); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), (3, 6)); can.alpha_composite(L)

# ---------- scenes: (start, film parts, rotation on the table, overlay) ----------
def o_hook(c, t):
    sec(c, FP('sw', 1.0, 600, 3), t, ws('Doppeldecker') - 0.15, (540, 560), -4, (1, -0.3))
    quote(c, t, [[('EINES', ws('Eines')), ('DER', ws('der')), ('GRÖSSTEN', ws('größten'))], [('SCHLACHTSCHIFFE', ws('Schlachtschiffe'))], [('EUROPAS', ws('Europas'))]],
          1180, size=84, lh=1.04, tout=ws('wurde') - 0.05, col={1: YEL})
    quote(c, t, [[('WURDE', ws('wurde')), ('VON', ws('von')), ('EINEM', ws('einem'))], [('LANGSAMEN', ws('langsamen'))], [('DOPPELDECKER', ws('Doppeldecker'))], [('GESTOPPT.', ws('gestoppt'))]],
          1110, size=84, lh=1.04, tout=ws('Ihr') - 0.15, col={2: YEL})
    quote(c, t, [[('BISMARCK', ws('Bismarck'))]], 1290, size=170)
    quote(c, t, [[('IHR', ws('Ihr')), ('NAME', ws('Name')), ('WAR', ws('war'))]], 1170, size=58, tout=ws('Bismarck') - 0.05)
def o_1941(c, t):
    title(c, t, '1941', ['ERSTE UND EINZIGE', 'FEINDFAHRT'], 1330, ws('1941'), [ws('ersten'), ws('Feindfahrt')], 0, 0, True, 200, 70, cps=18)
    quote(c, t, [[('IM', ws('Im', 7)), ('MAI', ws('Mai'))]], 1150, size=60)
def o_dk(c, t):
    sec(c, FP('hood', t - ws('Schlachtkreuzer') + 0.1, 640, 21, cap='HMS Hood'), t, ws('Schlachtkreuzer') - 0.1, (540, 560), 4, (-1, 0))
    quote(c, t, [[('DÄNEMARKSTRASSE', ws('Dänemarkstraße'))]], 1250, size=76, col={0: YEL})
    quote(c, t, [[('SCHLACHTKREUZER', ws('Schlachtkreuzer')), ('HOOD', ws('Hood'))]], 1350, size=58)
VON1 = ws('Von', 18)
def o_fire(c, t):
    if t < VON1:
        title(c, t, '8', ['MINUTEN', 'FEUER'], 1280, ws('acht'), [ws('Minuten'), ws('Feuer')], 0, 0, True, 210, 74, cps=18)
        quote(c, t, [[('DIE', ws('die', 16.9)), ('HOOD', ws('Hood', 17)), ('EXPLODIERT', ws('Luft'))]], 1450, size=62)
    else:
        quote(c, t, [[('VON', VON1), ('ÜBER', ws('über', 18)), ('1.400', ws('1.400')), ('MANN', ws('Mann', 19))]], 1160, size=62)
        title(c, t, '3', ['ÜBERLEBENDE'], 1330, ws('drei'), ws('drei') + 0.15, 0, 0, True, 230, 80, cps=24)
def o_leak(c, t):
    quote(c, t, [[('LECK', ws('Leck')), ('IM', ws('im', 23.5)), ('BUG', ws('Bug'))]], 1250, size=86, col={0: YEL}, tout=ws('Admiral') - 0.25)
    quote(c, t, [[('TREIBSTOFF', ws('Treibstoff')), ('LIEF', ws('lief', 24)), ('AUS', ws('aus', 24.5))]], 1360, size=58, tout=ws('Admiral') - 0.25)
    a = ws('Admiral') - 0.1
    if t >= a:   # the admiral, cut out, rises into the picture and pulls back slowly
        u = eout(clamp((t - a) / 1.1)); d = t - a; sc = 1.0 + 0.12 * (1 - u) + 0.05 * (1 - eout(clamp(d / 3))) - 0.006 * d
        card(c, lutjens(), 540 + 2 * d, lerp(1990, 1420, u) + 2 * d, lerp(4, 0, u))
    quote(c, t, [[('ADMIRAL', ws('Admiral'))]], 470, size=56, col={0: YEL})
    quote(c, t, [[('GÜNTHER', ws('Lütjens')), ('LÜTJENS', ws('Lütjens') + 0.12)]], 560, size=88)
    strip(c, t, ws('Kurs') - 0.45, ['KURS AUF FRANKREICH'], 540, 680)
def o_plot(c, t):
    quote(c, t, [[('DIE', ws('Die', 27.8)), ('ROYAL', ws('Royal')), ('NAVY', ws('Navy'))]], 1240, size=64)
    quote(c, t, [[('DUTZENDE', ws('Dutzenden')), ('SCHIFFE', ws('Schiffen'))]], 1350, size=86, col={0: YEL})
def o_sword(c, t):
    title(c, t, '15', ['SWORDFISH'], 1290, ws('15'), ws('Swordfish'), 0, 0, True, 220, 84, ['VOM FLUGZEUGTRÄGER ARK ROYAL'], ws('vom') - 0.3, cps=20)
    quote(c, t, [[('ZWEI', ws('Zwei')), ('TAGE', ws('Tage')), ('SPÄTER', ws('später'))]], 1110, size=56)
def o_torp(c, t):
    quote(c, t, [[('EIN', ws('Ein', 36.5)), ('TORPEDO', ws('Torpedo'))]], 1230, size=80)
    quote(c, t, [[('RUDER', ws('blockierte')), ('BLOCKIERT', ws('blockierte') + 0.15)]], 1340, size=86, col={0: YEL})
def o_circ(c, t):
    circle_arrow(c, t, ws('nur', 40) - 0.1, 560, 860, 400, 150)
    quote(c, t, [[('NUR', ws('nur', 40)), ('NOCH', ws('noch', 40)), ('IM', ws('im', 40.6)), ('KREIS', ws('Kreis'))]], 1260, size=84, col={0: YEL})
    quote(c, t, [[('KEIN', ws('nicht', 42)), ('ENTKOMMEN', ws('entkommen'))]], 1370, size=58)
def o_fleet(c, t):
    quote(c, t, [[('AM', ws('Am', 43)), ('NÄCHSTEN', ws('nächsten')), ('MORGEN', ws('Morgen'))]], 1330, size=66)
    sec(c, FP('kgv', t - ws('King') + 0.15, 560, 31, cap='King George V'), t, ws('King') - 0.15, (330, 540), -5, (-1, -0.2))
    sec(c, FP('rod', t - ws('Rodney') + 0.25, 500, 32, cap='Rodney'), t, ws('Rodney') - 0.25, (760, 880), 5, (1, 0.2))
def o_hit(c, t):
    quote(c, t, [[('EIN', ws('Ein', 47.6)), ('TREFFER', ws('Treffer'))]], 1220, size=62)
    quote(c, t, [[('BRÜCKE', ws('Brücke')), ('ZERSTÖRT', ws('Brücke') + 0.15)]], 1330, size=86, col={0: YEL})
def o_scut(c, t):
    quote(c, t, [[('DER', ws('Der', 51.6)), ('ERSTE', ws('Erste')), ('OFFIZIER', ws('Offizier'))]], 1220, size=60)
    quote(c, t, [[('SELBST', ws('selbst')), ('VERSENKT', ws('versenken'))]], 1330, size=86, col={0: YEL})
def o_surv(c, t):
    quote(c, t, [[('VON', ws('Von', 56)), ('ÜBER', ws('über', 56)), ('2.200', ws('2.200')), ('MANN', ws('Mann', 57))]], 1160, size=62)
    title(c, t, '114', ['ÜBERLEBENDE'], 1330, ws('114'), ws('114') + 0.25, 0, 0, True, 220, 80, cps=24)
def o_wreck(c, t):
    quote(c, t, [[('ROBERT', ws('Robert')), ('BALLARD', ws('Ballard'))]], 470, size=84)
    strip(c, t, ws('fünfzig') - 0.3, ['1989'], 540, 380)
    strip(c, t, ws('auch', 63) - 0.5, ['ENTDECKTE AUCH DIE TITANIC'], 540, 570)
    title(c, t, '4.791', ['METER', 'TIEFE'], 1320, ws('fünf', 65), [ws('Kilometern'), ws('Tiefe')], 0, 0, True, 190, 70, cps=18)
SC = [(0.0, [('hook', 0.0)], -3, o_hook), (ws('Im', 6.9), [('s1941', None)], 3, o_1941), (ws('In', 11.7), [('dk', None)], -3, o_dk),
      (ws('Nach'), [('fire', None), ('smoke', VON1)], 3, o_fire), (ws('Doch'), [('leak', None)], -3, o_leak), (ws('Die', 27.8), [('plot', None)], 3, o_plot),
      (ws('Zwei'), [('sword', None)], -3, o_sword), (ws('Ein', 36.5), [('torp', None)], 3, o_torp), (ws('Die', 39.4), [('circ', None)], -3, o_circ),
      (ws('Am', 43), [('fleet', None)], 3, o_fleet), (ws('Ein', 47.6), [('hit', None)], -3, o_hit), (ws('Der', 51.6), [('scut', None)], 3, o_scut),
      (ws('Von', 56), [('surv', None)], -3, o_surv), (ws('Ihr', 60), [('wreck', None)], 3, o_wreck)]
TEND = WORDS[-1][2] + 1.4
PRE, POST = 0.35, 1.0; D = PRE + POST
ZT = 0.5
GX, GY = 1500, 2300
PATH = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (2, 3)]
ANC = [(p[0] * GX, p[1] * GY) for p in PATH]
def t_in(j): return 0.0 if j == 0 else SC[j][0] - PRE    # when scene j's film-print arrives (and its film starts)

def layer(j, t):
    """scene j's film frame with everything that lies on it (screen coordinates at full zoom)"""
    parts = SC[j][1]; lt = t_in(j)
    k, a = parts[0][0], lt
    for kk, aa in parts[1:]:
        if t >= aa: k, a = kk, aa
    c = film(k, t - a).convert('RGBA'); SC[j][3](c, t); return c
def msc(j, t): return 1.0 + 0.06 * (1 - eout(clamp((t - t_in(j) - 0.8) / 5.0)))   # arrives a little big, pulls back slowly (never below full screen)
BW = 16
def as_print(L):
    P_ = Image.new('RGBA', (W + 2 * BW, H + 2 * BW), (236, 234, 228, 255)); P_.paste(L.convert('RGB'), (BW, BW)); return P_

# ---------- the table (blue-toned pile, half resolution of world units) ----------
TW, TH = 2400, 3000
PILE = ['hook', 's1941', 'dk', 'fire', 'smoke', 'leak', 'plot', 'sword', 'torp', 'circ', 'fleet', 'hit', 'scut', 'surv', 'wreck', 'sw', 'hood', 'kgv', 'rod']
def pile_im(i):
    k = PILE[i % len(PILE)]; im = _fr(k, max(1, int(nfr(k) * ((i * 0.37) % 0.8 + 0.1))))
    if im.width < im.height: im = im.crop((0, int(im.height * 0.2), im.width, int(im.height * 0.2) + int(im.width * 0.8)))
    return im
@functools.lru_cache(None)
def table():
    cache = E + 'table.png'
    if os.path.exists(cache): return Image.open(cache).convert('RGB')
    rng = np.random.default_rng(5); can = Image.new('RGBA', (TW, TH), (20, 24, 40, 255))
    for k in range(70):
        P_ = print_im(pile_im(int(rng.integers(1000))), int(rng.uniform(420, 640)), True, None, seed=int(rng.integers(50))).rotate(rng.uniform(-30, 30), expand=True, resample=Image.BICUBIC)
        x, y = int(rng.uniform(0, TW)), int(rng.uniform(0, TH))
        sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.6))); sh = sh.filter(ImageFilter.GaussianBlur(8))
        for dx in (-TW, 0, TW):
            for dy in (-TH, 0, TH): paste(can, sh, x + dx + 6, y + dy + 12); paste(can, P_, x + dx, y + dy)
    T_ = tone(can, DARK, LIGHT * 0.5, 1.2).filter(ImageFilter.GaussianBlur(2.0))
    big = Image.new('RGB', (2 * TW, 2 * TH))
    for dx in (0, TW):
        for dy in (0, TH): big.paste(T_, (dx, dy))
    big.save(cache); return big
def table_view(cx, cy, z):
    """screen window around world point (cx, cy) at zoom z (table stored at half resolution)"""
    T_ = table(); bw, bh = W / z / 2, H / z / 2; x0, y0 = (cx / 2 - bw / 2) % TW, (cy / 2 - bh / 2) % TH
    return T_.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + bw, y0 + bh))
BGN = 120
@functools.lru_cache(None)
def bg_list():
    rng = np.random.default_rng(11); xs = [a[0] for a in ANC]; ys = [a[1] for a in ANC]
    x0, x1, y0, y1 = min(xs) - 2200, max(xs) + 2200, min(ys) - 2600, max(ys) + 2600
    return [(int(rng.integers(1000)), rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(-30, 30), rng.uniform(-14, 14), rng.uniform(-14, 14), rng.uniform(-0.4, 0.4), rng.uniform(950, 1350)) for _ in range(BGN)]
@functools.lru_cache(maxsize=64)
def bg_img(i):
    P_ = print_im(pile_im(i), 520, True, None, i % 50)
    T_ = tone(P_.convert('RGB'), DARK, LIGHT * 0.92, 1.1).filter(ImageFilter.GaussianBlur(1.0)).convert('RGBA'); T_.putalpha(P_.getchannel('A'))
    return T_
def S(wx, wy, cx, cy, z): return (wx - cx) * z + W / 2, (wy - cy) * z + H / 2

# ---------- camera ----------
def cam(t):
    """(cx, cy, z, k, moving) : world point in the middle of the screen, zoom, current scene"""
    k = max(i for i, s in enumerate(SC) if s[0] - PRE <= t) if t >= 0 else 0
    if k == 0 or t >= SC[k][0] + POST: return ANC[k][0], ANC[k][1], 1.0, k, None
    u = clamp((t - (SC[k][0] - PRE)) / D); p = eio(clamp((u - 0.06) / 0.82))
    z = 1.0 - (1.0 - ZT) * math.sin(math.pi * u) ** 0.8
    return lerp(ANC[k - 1][0], ANC[k][0], p), lerp(ANC[k - 1][1], ANC[k][1], p), z, k, u
def main_pose(j, t, z, k):
    """world position, rotation and scale of scene j's film-print; the print in focus straightens out as the camera closes in"""
    r = SC[j][2] * (1 - z) / (1 - ZT); x, y = ANC[j]; sc = msc(j, t)
    if j == k and j > 0:   # arriving with the camera move, from the direction of travel
        dx, dy = ANC[j][0] - ANC[j - 1][0], ANC[j][1] - ANC[j - 1][1]; n = math.hypot(dx, dy); dx, dy = dx / n, dy / n
        t0 = t_in(j); v = eout(clamp((t - t0) / (0.8 * D)))
        x, y = lerp(x + dx * 1500 - dy * 160, x, v), lerp(y + dy * 1500 + dx * 160, y, v)
        r = lerp(r + (14 if j % 2 else -14), r, v); sc *= 1.0 + 0.32 * (1 - v)
    return x, y, r, sc
def frame(t):
    cx, cy, z, k, u = cam(t)
    if u is None:   # full screen: the film-print fills the frame (straight, slowly pulling back)
        L = layer(k, t); s = msc(k, t); bw, bh = W / s, H / s
        img = L.resize((W, H), Image.BICUBIC, box=(W / 2 - bw / 2, H / 2 - bh / 2, W / 2 + bw / 2, H / 2 + bh / 2))
    else:
        img = table_view(cx, cy, z).convert('RGBA')
        for i, x, y, r, vx, vy, vr, ww in bg_list():
            X, Y = S(x + vx * t, y + vy * t, cx, cy, z)
            if -700 < X < W + 700 and -700 < Y < H + 700: card(img, bg_img(i), X, Y, r + vr * t, sc=z * ww / 520)
        for j in (k - 1, k):
            if j < 0 or t < t_in(j): continue
            x, y, r, sc = main_pose(j, t, z, k); X, Y = S(x, y, cx, cy, z)
            card(img, as_print(layer(j, t)), X, Y, r, sc=z * sc)
        (cx2, cy2, z2, _, _) = cam(t + 1 / FPS)
        img = eg.dblur(img, (cx - cx2) * z * 0.6, (cy - cy2) * z * 0.6)
    if t > TEND - 0.6: img = Image.blend(img.convert('RGBA'), Image.new('RGBA', (W, H), (0, 0, 0, 255)), eio((t - (TEND - 0.6)) / 0.6))
    return finish(img, t)

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
