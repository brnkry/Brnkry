# Eino Luukkanen Short: photo-led, continuous slow pans, Kammhuber palette; new graphics (plane bands, victory tally, Karelia map, calendar sheet, odds, strike-through)
import sys, math, subprocess
import base
from base import *
base.BLUR.clear()
# Finnish air force swastikas on the aircraft, small blurs only on the symbol
base.BLUR.update({'l23': [(170, 800, 190), (330, 805, 190)], 'l12': [(470, 870, 170), (580, 870, 150)],
                  'l07': [(420, 520, 210), (640, 520, 210)], 'l24': [(160, 645, 220), (370, 645, 220)]})
from PIL import ImageChops
import mapx
from mapx import draw_map, Cam, ink_dot, maplabel, LAND, BORDER

TEND = 128.68

def shot(c, grad=GRAD):
    can = c.frame(); can.alpha_composite(grad); return can
GR = [np.random.default_rng(i).normal(0, 4.0, (H // 2, W // 2)).astype(np.int16) for i in range(6)]
def grain(img, n):
    a = np.asarray(img).astype(np.int16); g = np.kron(GR[n % 6], np.ones((2, 2), np.int16))[..., None]
    return Image.fromarray(np.clip(a + g, 0, 255).astype(np.uint8))
def ui_overlay(im):
    im = im.convert('RGBA'); L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((0, 0, W, 290), fill=(255, 0, 0, 60)); d.rectangle((930, 680, W, 1580), fill=(255, 0, 0, 80)); d.rectangle((0, 1580, W, H), fill=(255, 0, 0, 80))
    im.alpha_composite(L); return im.convert('RGB')

# ---------- motion: constant slow speed for the whole time the photo is on screen ----------
SPEED = 34.0
def pan_lin(p, t, w0, w1, fx, d, cy=None):
    im = src(p); scale = H / im.height; w = min(im.width, im.height * 9 / 16)
    span = SPEED * (w1 - w0) / scale
    lo, hi = w / 2, im.width - w / 2
    a, b = fx - d * span / 2, fx + d * span / 2
    if min(a, b) < lo: sh = lo - min(a, b); a += sh; b += sh
    if max(a, b) > hi: sh = max(a, b) - hi; a -= sh; b -= sh
    u = clamp((t - w0) / (w1 - w0))
    return PCam(p, lerp(a, b, u), im.height / 2 if cy is None else cy, w)
def zoom_lin(p, t, w0, w1, cx, cy, z1=1.06, z0=1.0):
    im = src(p); w = min(im.width, im.height * 9 / 16); u = clamp((t - w0) / (w1 - w0))
    return PCam(p, cx, cy, w / lerp(z0, z1, u))

def dim(can, a):
    if a > 0: can.alpha_composite(Image.new('RGBA', (W, H), (4, 6, 8, int(a))))

# ---------- new graphics ----------
def band(p, cx, cy, w, bw, bh):
    """landscape crop of a photo (source centre cx, cy, width w) scaled to bw x bh"""
    im = src(p); h = w * bh / bw
    x0 = min(max(cx - w / 2, 0), im.width - w); y0 = min(max(cy - h / 2, 0), im.height - h)
    return im.resize((bw, bh), Image.BILINEAR, box=(x0, y0, x0 + w, y0 + h)).convert('RGBA')

def bar_mark(h, col, half=False):
    """one painted victory bar, like the marks on a fighter's tail"""
    L = Image.new('RGBA', (30, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    top = 6 + (h / 2 if half else 0)
    d.rectangle((5, top, 25, 6 + h), fill=(8, 6, 4, 170)); d.rectangle((8, top + 2, 22, 4 + h), fill=col + (255,))
    return L
BAR = bar_mark(64, CREAM); BAR_G = bar_mark(64, GOLD); BAR_R = bar_mark(64, RUST); BAR_H = bar_mark(64, GOLD, True)
def tally(can, t, t0, n, cy, per=14, gap=38, rows_gap=92, dur=1.0, done=0, last_col=None, half_at=None):
    """victory bars stamp in one after another, rows of `per`; `done` bars are already there"""
    if t < t0 and done == 0: return
    step = dur / max(1, n - done)
    for i in range(n):
        ti = t0 + (i - done) * step if i >= done else -1
        if t < ti: break
        k = eout((t - ti) / 0.14) if ti >= 0 else 1.0
        r, c = divmod(i, per); cols = min(per, n - r * per)
        x = 540 + (c - (cols - 1) / 2) * gap; y = cy + r * rows_gap
        spr = BAR_H if half_at == i else (BAR_R if (last_col and i == n - 1) else BAR)
        put(can, spr, x, y - (1 - k) * 26, 1.0, k)

def plane(size, col):
    """small top-down fighter silhouette pointing up"""
    s = size; L = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse((s * 0.44, s * 0.05, s * 0.56, s * 0.9), fill=col)
    d.polygon([(s * 0.04, s * 0.42), (s * 0.96, s * 0.42), (s * 0.92, s * 0.55), (s * 0.08, s * 0.55)], fill=col)
    d.polygon([(s * 0.3, s * 0.82), (s * 0.7, s * 0.82), (s * 0.66, s * 0.9), (s * 0.34, s * 0.9)], fill=col)
    return L
def halo(L, a=170, r=8):
    sh = Image.new('RGBA', (L.width + 40, L.height + 40), (0, 0, 0, 0)); m = L.getchannel('A')
    sh.paste(Image.new('RGBA', L.size, (4, 4, 6, a)), (20, 20), m); sh = sh.filter(ImageFilter.GaussianBlur(r)); sh.alpha_composite(L, (20, 20)); return sh
PL_G = halo(plane(92, GOLD + (255,))); PL_R = halo(plane(62, (196, 70, 64, 255)))
def odds(can, t, t0, cy=1060):
    """one Finnish fighter against a growing enemy formation"""
    if t < t0: return
    k = eout((t - t0) / 0.35)
    put(can, PL_G, 250, cy + 40, lerp(0.6, 1.0, k), k)
    put(can, sprite('1', 'serif', 90, GOLD), 250, cy + 170, 1.0, k)
    n = 0
    for r in range(5):
        for c in range(5 - abs(2 - r) // 2):
            ti = t0 + 0.35 + n * 0.07; n += 1
            if t < ti: continue
            kk = eout((t - ti) / 0.25)
            x = 560 + c * 66 + (r % 2) * 33; y = cy - 130 + r * 72 - (1 - kk) * 40
            put(can, PL_R, x, y, 1.0, kk)
    if t > t0 + 0.35: put(can, sprite('VS', 'cond', 64, CREAM), 420, cy + 40, 1.0, clamp((t - t0 - 0.35) / 0.3))

def calendar(can, t, t0, day, month, year, cx=540, cy=1150):
    """translucent calendar leaf over the photo"""
    if t < t0: return
    k = eout((t - t0) / 0.5); w, h = 320, 330; y = cy + (1 - k) * 40
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); glass(L, (cx - w / 2, y - h / 2, cx + w / 2, y + h / 2), 140)
    d = ImageDraw.Draw(L); d.line((cx - w / 2 + 24, y - h / 2 + 86, cx + w / 2 - 24, y - h / 2 + 86), fill=RUST + (220,), width=3)
    if k < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * k)))
    can.alpha_composite(L)
    put(can, sprite(month, 'cond', 54, RUST, False, 4), cx, y - h / 2 + 50, 1.0, k)
    put(can, sprite(day, 'condl', 170, CREAM), cx, y + 10, 1.0, k)
    put(can, sprite(year, 'cond', 54, GOLD, False, 4), cx, y + h / 2 - 46, 1.0, k)

def strike(can, t, t0, t1, txt, cy, size=130):
    """word appears, then a red pen line crosses it out"""
    if t < t0: return
    focus(can, t, t0, txt, 'serif', size, CREAM, cy, dur=0.35)
    if t >= t1:
        sz = fit(txt, 'serif', size, maxw_at(cy)); tw = textw(txt, 'serif', sz)
        k = eio((t - t1) / 0.35); x0 = 540 - tw / 2 - 20
        stroke(can, [(x0, cy + 18), (x0 + (tw + 40) * k, cy - 8 * k)], RUST, 14)

def shine(can, t, t0, txt, fk, size, col, cy, dur=0.9):
    """text with a light sweep passing across it once"""
    if t < t0: return
    size = fit(txt, fk, size, maxw_at(cy)); spr = sprite(txt, fk, size, col, True)
    k = eout((t - t0) / 0.35); put(can, spr, 540, cy, lerp(0.92, 1.0, k), k)
    u = (t - t0 - 0.25) / dur
    if 0 < u < 1:
        a = np.asarray(sprite(txt, fk, size, col, False).getchannel('A')).astype(np.float32)
        xs = np.arange(a.shape[1]); c = u * (a.shape[1] + 300) - 150
        m = np.clip(1 - np.abs(xs - c) / 90, 0, 1)[None, :] * a * 0.85
        S = Image.new('RGBA', (a.shape[1], a.shape[0]), (255, 250, 225, 0)); S.putalpha(Image.fromarray(m.astype(np.uint8)))
        put(can, S, 540, cy)

def digits(can, t, t0, txt, cy, size=330, col=GOLD, step=0.28, fk='condl'):
    """big italic number, its digits arriving one after another"""
    if t < t0: return
    size = fit(txt, fk, size, maxw_at(cy)); f = FK[fk](size); x = 540 - textw(txt, fk, size) / 2
    for i, ch in enumerate(txt):
        k = eout((t - t0 - i * step) / 0.3); w = f.getlength(ch)
        if k > 0: put(can, sprite(ch, fk, size, col), x + w / 2, cy + (1 - k) * 30, lerp(1.25, 1.0, k), k)
        x += w

def glass(can, box, a=150, r=24):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle(box, r, fill=(6, 9, 12, int(a))); d.rounded_rectangle(box, r, outline=CREAM + (int(a * 0.6),), width=2)
    can.alpha_composite(L)

def lifespan(can, t, t0, a, b, cy=1240):
    """two years joined by a line that draws from birth to death"""
    if t < t0: return
    k = eio((t - t0) / 0.8); x0, x1 = 210, 800
    put(can, sprite(a, 'serif', 110, CREAM), x0, cy, 1.0, clamp((t - t0) / 0.3))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    xa, xb = x0 + 140, x1 - 140
    d.line((xa, cy + 4, lerp(xa, xb, k), cy + 4), fill=(8, 6, 4, 150), width=12); d.line((xa, cy + 4, lerp(xa, xb, k), cy + 4), fill=GOLD + (255,), width=6)
    can.alpha_composite(L)
    if k >= 0.98: put(can, sprite(b, 'serif', 110, GOLD), x1, cy, 1.0, clamp((t - t0 - 0.8) / 0.3))

# ---------- Karelia map ----------
MAPC = (29.4, 62.3, 11.0)
LADOGA = [(30.85, 61.63), (30.45, 61.42), (30.05, 61.05), (29.98, 60.75), (30.45, 60.42), (31.0, 60.08), (31.6, 59.95), (32.4, 60.1), (32.85, 60.5),
          (32.75, 60.9), (32.4, 61.15), (31.9, 61.4), (31.4, 61.62)]
CEDED = [(27.75, 60.52), (28.6, 61.0), (29.3, 61.3), (29.9, 61.55), (30.5, 61.95), (30.75, 62.25), (31.1, 62.55), (31.4, 62.95), (31.9, 63.05), (32.9, 62.55),
         (32.95, 61.85), (32.4, 61.15), (31.9, 61.3), (30.95, 60.55), (30.0, 60.15), (29.4, 60.2), (28.6, 60.45)]
SORT = (30.69, 61.70)
@functools.lru_cache(None)
def base_map():
    mp, cam = draw_map(MAPC, ('Finland',))
    d = ImageDraw.Draw(mp); d.polygon([cam.p(*q) for q in LADOGA], fill=mapx.SEA, outline=BORDER)
    return mp
ICAM = (30.4, 61.3, 11.5); BOX = (150, 1070, 930, 1460)
@functools.lru_cache(None)
def inset_base():
    mp, cam = draw_map(ICAM, ('Finland',)); ImageDraw.Draw(mp).polygon([cam.p(*q) for q in LADOGA], fill=mapx.SEA, outline=BORDER); return mp
def inset(can, t, t0, ceded_t=None, home_t=None, sort_t=None, lad_t=None):
    """translucent map window over the photo; the photo stays in front"""
    if t < t0: return None
    a = clamp((t - t0) / 0.45); cam = Cam(*ICAM); dy = (BOX[1] + BOX[3]) // 2 - H // 2
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); L.paste(inset_base(), (0, dy))
    P = lambda lo, la: (cam.p(lo, la)[0], cam.p(lo, la)[1] + dy)
    if ceded_t is not None and t >= ceded_t:
        k = eio((t - ceded_t) / 1.0); pts = [P(*q) for q in CEDED]
        R = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(R).polygon(pts, fill=RUST + (int(170 * k),)); L.alpha_composite(R)
        stroke(L, partial(pts + [pts[0]], k), RUST, 4); ImageDraw.Draw(L).polygon([P(*q) for q in LADOGA], fill=mapx.SEA + (255,), outline=BORDER)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle(BOX, 24, fill=int(185 * a)); m = m.filter(ImageFilter.GaussianBlur(6))
    L.putalpha(ImageChops.multiply(L.getchannel('A'), m)); can.alpha_composite(L)
    ImageDraw.Draw(can).rounded_rectangle(BOX, 24, outline=CREAM + (int(110 * a),), width=2)
    sx, sy = P(*SORT); lx, ly = P(31.4, 60.55)
    if sort_t is not None: pulse(can, t, sort_t, sx, sy, GOLD if home_t is None else CREAM); maplabel(can, t, sort_t, 'SORTAVALA', sx - 26, sy - 34, size=40, col=GOLD, side='l')
    if lad_t is not None: maplabel(can, t, lad_t, 'LADOGASEE', lx - 100, ly, size=36, col=CREAM)
    if home_t is not None: maplabel(can, t, home_t, 'HEIMAT', sx - 26, sy + 34, size=44, col=GOLD, side='l')
    if ceded_t is not None and t > ceded_t + 0.6: q = P(32.2, 62.3); maplabel(can, t, ceded_t + 0.6, 'ABGETRETEN', q[0] + 10, q[1] + 30, size=38, col=CREAM, side='l')
    f = P(26.5, 62.0); maplabel(can, t, t0 + 0.2, 'FINNLAND', f[0] - 40, f[1], size=40, col=CREAM)
    return sx, sy
def pulse(can, t, t0, x, y, col=GOLD):
    if t < t0: return
    for j in range(2):
        u = ((t - t0) * 0.8 + j * 0.5) % 1.0; ring(can, x, y, 14 + 60 * u, col, (1 - u) * 0.8, 4)
    ink_dot(can, x, y, 11, col)

# ---------- scenes ----------
def sc_hook(t, w0, w1):
    """three aircraft photos in stacked bands, each sliding in on its word"""
    can = Image.new('RGBA', (W, H), DEEP + (255,))
    B3 = [('l23', 1080, 860, 2400, 'FOKKER D.XXI', 0.05, 1), ('l12', 1500, 820, 2000, 'BREWSTER BUFFALO', 0.45, -1), ('l05', 1250, 700, 2200, 'MESSERSCHMITT BF 109', 1.25, 1)]
    for i, (p, cx, cy, w, lab, ti, s) in enumerate(B3):
        if t < ti: continue
        k = eout((t - ti) / 0.4); drift = (t - ti) * 40 * s
        bnd = band(p, cx - drift, cy, w - (t - ti) * 30, 1080, 400)
        y = 300 + i * 410
        x = int(-s * (1 - k) * 1080)
        can.alpha_composite(bnd, (x, y)) if x >= 0 else can.alpha_composite(bnd.crop((-x, 0, 1080, 400)), (0, y))
        plate(can, t, ti + 0.2, lab, y + 330, cx=430, size=40, bg=GOLD if i != 1 else CREAM, fg=DEEP)
    return can
def sc_l01(t, w0, w1):
    can = shot(pan_lin('l01', t, w0, w1, 900, -1)); tE = wt('Eino') - 0.12
    focus(can, t, wt('zwei') - 0.05, 'ZWEI KRIEGE', 'serif', 110, CREAM, 980, t1=tE)
    if t < tE + 0.3:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); digits(L, t, wt('56') - 0.05, '56', 1190, 340)
        if t > tE: a = 1 - ease((t - tE) / 0.3); L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
        can.alpha_composite(L)
    reveal(can, t, wt('bestätigte'), 'BESTÄTIGTE LUFTSIEGE', 'cond', 70, CREAM, 1420, t1=tE)
    if t >= tE:
        focus(can, t, wt('Eino') - 0.04, 'EINO', 'condl', 150, CREAM, 1240, dur=0.3)
        focus(can, t, wt('Luukkanen') - 0.04, 'LUUKKANEN', 'condl', 150, GOLD, 1400, dur=0.3)
    return can
def sc_l13(t, w0, w1):
    can = shot(zoom_lin('l13', t, w0, w1, 768, 1150, 1.06), GRAD_SOFT)
    plate(can, t, wt('Karelien') - 0.05, 'KARELIEN', 1010, size=56, bg=GOLD, fg=DEEP)
    inset(can, t, wt('Karelien') - 0.3, sort_t=wt('Sortavala'), lad_t=wt('Ladogasee')); return can
def sc_l17(t, w0, w1):
    can = shot(zoom_lin('l17', t, w0, w1, 768, 1150, 1.07))
    focus(can, t, wt('1930er'), 'ANFANG DER 1930ER', 'serif', 100, GOLD, 1250)
    plate(can, t, wt('Pilot'), 'PILOT UND OFFIZIER', 1400, size=60); return can
def sc_l10(t, w0, w1):
    can = shot(pan_lin('l10', t, w0, w1, 900, 1))
    strike(can, t, wt('kaum') - 0.1, wt('kaum') + 0.25, 'MODERNE FLUGZEUGE', 1300, 110); return can
def sc_l02(t, w0, w1):
    can = shot(pan_lin('l02', t, w0, w1, 1024, -1), GRAD_SOFT)
    plate(can, t, wt('Sowjetunion'), 'SOWJETISCHER ANGRIFF', 1450, size=60, bg=RUST, fg=CREAM)
    calendar(can, t, wt('30.'), '30', 'NOVEMBER', '1939', cy=1150); return can
def sc_l20(t, w0, w1):
    can = shot(pan_lin('l20', t, w0, w1, 1024, 1))
    reveal(can, t, wt('führte'), 'FÜHRT EINE EINHEIT DER', 'cond', 60, CREAM, 1260)
    focus(can, t, wt('Jagdstaffel'), 'JAGDSTAFFEL 24', 'serif', 130, GOLD, 1390); return can
def wide(p, t, w0, w1, fx, d, hh=1240, cy=None, yc=860):
    """landscape photo shown wider than full height: sharp band of height hh over a blurred, darkened copy"""
    im = src(p); scale = hh / im.height; sw = W / scale
    span = SPEED * (w1 - w0) / scale; lo, hi = sw / 2, im.width - sw / 2
    a, b = fx - d * span / 2, fx + d * span / 2
    if min(a, b) < lo: sh = lo - min(a, b); a += sh; b += sh
    if max(a, b) > hi: sh = max(a, b) - hi; a -= sh; b -= sh
    x = lerp(a, b, clamp((t - w0) / (w1 - w0)))
    bg = PCam(p, x, im.height / 2, 99999).frame().filter(ImageFilter.GaussianBlur(28))
    bg = Image.blend(bg, Image.new('RGBA', (W, H), (8, 10, 12, 255)), 0.5)
    bd = im.resize((W, hh), Image.BILINEAR, box=(x - sw / 2, 0, x + sw / 2, im.height)).convert('RGBA')
    m = Image.new('L', (W, hh), 255); dm = ImageDraw.Draw(m)
    for i in range(40): dm.line((0, i, W, i), fill=int(255 * i / 40)); dm.line((0, hh - 1 - i, W, hh - 1 - i), fill=int(255 * i / 40))
    bg.paste(bd, (0, yc - hh // 2), m); bx = x - sw / 2
    return bg, (lambda sx, sy: ((sx - bx) * scale, (sy) * scale + yc - hh / 2))
def sc_l23(t, w0, w1):
    can, pt = wide('l23', t, w0, w1, 900, -1); can.alpha_composite(GRAD_SOFT)
    callout(can, t, wt('Fokker'), pt(1150, 560), (480, 1330), 'FOKKER D.XXI', col=GOLD, size=70)
    reveal(can, t, wt('niederländisches'), 'NIEDERLÄNDISCHES MODELL', 'cond', 62, CREAM, 1450); return can
def sc_l06(t, w0, w1):
    can = shot(pan_lin('l06', t, w0, w1, 1000, -1)); dim(can, 120 * clamp((t - wt('Gegner') + 0.3) / 0.4))
    odds(can, t, wt('Gegner'), 1000)
    plate(can, t, wt('weit'), 'ZAHLENMÄSSIG WEIT ÜBERLEGEN', 1400, size=52, bg=RUST, fg=CREAM); return can
def sc_l22(t, w0, w1):
    can = shot(pan_lin('l22', t, w0, w1, 896, -1))
    focus(can, t, wt('nächsten'), '1. DEZEMBER 1939', 'serif', 110, CREAM, 1250)
    plate(can, t, wt('SB-Bomber'), 'ERSTER LUFTSIEG: SB-BOMBER', 1400, size=54, bg=GOLD, fg=DEEP); return can
def sc_l18m(t, w0, w1):
    can = shot(pan_lin('l18', t, w0, w1, 1100, 1), GRAD_SOFT)
    plate(can, t, wt('Winterkrieg') - 0.05, 'ENDE DES WINTERKRIEGS · MÄRZ 1940', 1010, size=48, bg=RUST, fg=CREAM)
    inset(can, t, wt('Winterkrieg') - 0.3, ceded_t=wt('große', 45), home_t=wt('Heimat') - 0.1, sort_t=wt('Luukkanens', 50)); return can
def sc_l12(t, w0, w1):
    c = pan_lin('l12', t, w0, w1, 1500, 1); can = shot(c)
    reveal(can, t, wt('kaufte'), 'GEKAUFT IN DEN USA', 'cond', 64, CREAM, 1200)
    callout(can, t, wt('Brewster'), c.pt(1640, 760), (520, 1380), 'BREWSTER BUFFALO', col=GOLD, size=66); return can
def sc_l14(t, w0, w1):
    can = shot(pan_lin('l14', t, w0, w1, 900, -1))
    strike(can, t, wt('veraltet') - 0.05, wt('doch', 61), 'VERALTET', 1220, 150)
    plate(can, t, wt('Fortsetzungskrieg'), 'FORTSETZUNGSKRIEG AB 1941', 1420, size=54, bg=RUST, fg=CREAM); return can
def sc_l16(t, w0, w1):
    can = shot(pan_lin('l16', t, w0, w1, 1500, -1))
    reveal(can, t, wt('finnische'), 'FINNISCHE PILOTEN', 'cond', 64, CREAM, 1260)
    focus(can, t, wt('überraschend'), 'ÜBERRASCHEND VIELE ERFOLGE', 'serif', 90, GOLD, 1390); return can
def sc_l08(t, w0, w1):
    can = shot(pan_lin('l08', t, w0, w1, 1100, 1))
    digits(can, t, wt('14,5'), '14,5', 1150, 300, step=0.18)
    focus(can, t, wt('Abschüsse'), 'ABSCHÜSSE MIT DER BREWSTER', 'cond', 60, CREAM, 1320)
    plate(can, t, wt('geteilte'), 'GETEILTE ZÄHLTEN ANTEILIG', 1440, size=52, bg=GOLD, fg=DEEP); return can
def sc_l03(t, w0, w1):
    can = shot(pan_lin('l03', t, w0, w1, 1500, -1)); tj = wt('Major') - 0.2
    focus(can, t, wt('März', 77), 'MÄRZ 1943', 'serif', 140, GOLD, 1300, t1=tj)
    plate(can, t, wt('Major'), 'MAJOR', 1250, size=70, bg=CREAM, fg=DEEP)
    focus(can, t, wt('Jagdstaffel', 80), 'JAGDSTAFFEL 34', 'serif', 130, GOLD, 1400); return can
def sc_l07(t, w0, w1):
    c = pan_lin('l07', t, w0, w1, 1000, 1); can = shot(c)
    callout(can, t, wt('deutsche') - 0.05, c.pt(800, 470), (480, 1320), 'DEUTSCHE MESSERSCHMITT BF 109 G', col=GOLD, size=56); return can
def sc_l04(t, w0, w1):
    can = shot(pan_lin('l04', t, w0, w1, 2400, -1))
    focus(can, t, wt('Sommer'), 'SOMMER 1944', 'serif', 140, CREAM, 1200)
    plate(can, t, wt('Großoffensive'), 'SOWJETISCHE GROSSOFFENSIVE', 1340, size=54, bg=RUST, fg=CREAM)
    reveal(can, t, wt('Karelischen'), 'KARELISCHE LANDENGE', 'cond', 62, GOLD, 1450); return can
def sc_l09(t, w0, w1):
    can = shot(pan_lin('l09', t, w0, w1, 896, 1))
    focus(can, t, wt('18.'), '18. JUNI 1944', 'serif', 110, CREAM, 1170)
    shine(can, t, wt('Mannerheim-Kreuz,'), 'MANNERHEIM-KREUZ', 'serif', 120, GOLD, 1310)
    reveal(can, t, wt('Finnlands', 98), 'FINNLANDS HÖCHSTE MILITÄRISCHE AUSZEICHNUNG', 'cond', 48, CREAM, 1430); return can
def sc_l05(t, w0, w1):
    can = shot(pan_lin('l05', t, w0, w1, 1350, 1), GRAD_SOFT); t56 = wt('56.')
    focus(can, t, wt('5.', 100), '5. AUGUST 1944', 'serif', 120, CREAM, 1250, t1=t56 - 0.25)
    digits(can, t, t56, '56.', 1170, 320, step=0.22)
    plate(can, t, wt('letzten'), 'LETZTER LUFTSIEG', 1380, size=66, bg=RUST, fg=CREAM); return can
def sc_l24(t, w0, w1):
    can = shot(pan_lin('l24', t, w0, w1, 1100, -1))
    focus(can, t, wt('schwiegen'), 'WAFFENSTILLSTAND', 'serif', 120, CREAM, 1260)
    plate(can, t, wt('Karelien', 110), 'KARELIEN BLIEB VERLOREN', 1410, size=58, bg=RUST, fg=CREAM); return can
def sc_l11(t, w0, w1):
    can = shot(pan_lin('l11', t, w0, w1, 896, 1))
    plate(can, t, wt('diente'), 'IN DER LUFTWAFFE', 1180, size=54)
    focus(can, t, wt('1951'), 'BIS 1951', 'serif', 130, GOLD, 1300)
    reveal(can, t, wt('Erinnerungen') - 0.15, 'SEINE ERINNERUNGEN', 'type', 80, CREAM, 1440, dur=0.9); return can
def sc_l19(t, w0, w1):
    can = shot(pan_lin('l19', t, w0, w1, 1792, -1))
    lifespan(can, t, wt('1964') - 0.3, '1909', '1964', 1250)
    plate(can, t, wt('54'), '54 JAHRE', 1410, size=64, bg=GOLD, fg=DEEP); return can
def sc_end(t, w0, w1):
    can = shot(pan_lin('l21', t, w0, w1, 1100, 1)); tk = wt('Kanntet')
    focus(can, t, tk, 'KANNTET IHR', 'serif', 120, CREAM, 1210)
    focus(can, t, wt('diese', 120), 'DIESE GESCHICHTE?', 'serif', 120, GOLD, 1340)
    plate(can, t, wt('Schreibt'), 'SCHREIBT ES IN DIE KOMMENTARE!', 1460, size=46); return can

SCN = [(0.0, sc_hook, 'cut'), (2.30, sc_l01, 'flash'), (8.85, sc_l13, 'dip'), (13.75, sc_l17, 'fade'), (19.55, sc_l10, 'slide_l'),
       (22.70, sc_l02, 'fade'), (28.85, sc_l20, 'fade'), (32.55, sc_l23, 'slide_r'), (36.60, sc_l06, 'fade'), (40.15, sc_l22, 'fade'),
       (44.80, sc_l18m, 'dip'), (54.15, sc_l12, 'flash'), (60.00, sc_l14, 'fade'), (64.50, sc_l16, 'slide_l'), (69.60, sc_l08, 'fade'),
       (77.60, sc_l03, 'dip'), (84.00, sc_l07, 'slide_r'), (88.60, sc_l04, 'fade'), (95.35, sc_l09, 'fade'),
       (102.25, sc_l05, 'slide_l'), (108.55, sc_l24, 'dip'), (113.80, sc_l11, 'fade'),
       (119.40, sc_l19, 'fade'), (124.10, sc_end, 'fade')]
OV = 0.22
SC = []
for i, (t0, fn, tr) in enumerate(SCN):
    s = 0.0 if i == 0 else t0 - OV
    e = TEND if i == len(SCN) - 1 else SCN[i + 1][0] + OV
    SC.append((s, e, fn, tr))

DIPC = Image.new('RGBA', (W, H), (4, 6, 8, 255)); FLASHC = Image.new('RGBA', (W, H), (250, 244, 225, 255))
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
        elif tr == 'flash':
            img = Image.blend(run(a, t), FLASHC, min(1, u * 2) * 0.75) if u < 0.5 else Image.blend(FLASHC, run(b, t), 0.25 + 0.75 * (u - 0.5) * 2)
        else: img = Image.blend(run(a, t), run(b, t), u)
    img.alpha_composite(VIG)
    if t > TEND - 0.6: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * clamp((t - TEND + 0.6) / 0.5)))))
    return img.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; ims = [ui_overlay(frame(t)).resize((270, 480)) for t in ts]
        cols = 6; rows = (len(ims) + cols - 1) // cols; Sh = Image.new('RGB', (270 * cols, 480 * rows))
        for i, im in enumerate(ims):
            Sh.paste(im, ((i % cols) * 270, (i // cols) * 480)); ImageDraw.Draw(Sh).text(((i % cols) * 270 + 4, (i // cols) * 480 + 4), f'{ts[i]}', fill=(0, 255, 0))
        Sh.save(B + sys.argv[2], quality=90)
    else:
        out = sys.argv[2]; a, b = float(sys.argv[3]), float(sys.argv[4])
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
        for n in range(int(round(a * FPS)), int(round(b * FPS))):
            p.stdin.write(grain(frame(n / FPS), n).tobytes())
        p.stdin.close(); p.wait(); print('rc', p.returncode)
