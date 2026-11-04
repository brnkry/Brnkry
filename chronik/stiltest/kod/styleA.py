# Style A (reference a.mov): dark slate-blue textured stage, a pile of old black-and-white prints with white deckled borders, tilted and flying in
# with motion blur, the camera drifting slowly over them; extra-bold grunge sans type (a white year + a two-line yellow title + a torn white
# paper strip with small dark caps), quotes in white caps with a small yellow line, grain, dust and vignette. Laconia, first 28.6 s, 9:16.
import sys, os, json, math, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
LAC = B + '../lac/'; sys.path.insert(0, LAC + 'code')
import lib9 as L9
W, H, FPS = 1080, 1920, 30
NAVY = (40, 47, 66); CREAM = (236, 232, 222); YEL = (236, 182, 40); INK = (36, 38, 46)
WORDS = json.load(open(LAC + 'words.json'))
def wt(s, after=0.0):
    for w, a, b in WORDS:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a
    raise KeyError(s)
def ws(s, after=0.0): return wt(s, after) - 0.04
def clamp(x): return max(0.0, min(1.0, x))
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def lerp(a, b, u): return a + (b - a) * u
CX = 480   # text centre, clear of the Shorts buttons on the right

@functools.lru_cache(None)
def mont(s, wg=800):
    f = ImageFont.truetype(LAC + '../sch/fonts/Montserrat%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
@functools.lru_cache(None)
def script(s): return ImageFont.truetype(LAC + '../sch/fonts/Caveat.ttf', s)

# ---------- textures ----------
@functools.lru_cache(None)
def grunge(seed=1):
    """worn print texture: blotchy low-frequency noise with fine specks, used to eat into type and paper"""
    rng = np.random.default_rng(seed); n = rng.random((H // 8, W // 8)); n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6)), np.float32) / 255
    sp = rng.random((H, W)); m = np.clip(1.0 - np.clip((0.42 - n) * 4, 0, 1) * 0.55 - (sp > 0.985) * 0.6, 0, 1)
    return Image.fromarray((m * 255).astype(np.uint8))
@functools.lru_cache(None)
def stage():
    """the slate-blue stage: uneven tone, scratches, vignette"""
    rng = np.random.default_rng(7); yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H * 0.45) / (H * 0.6)) ** 2)
    base = np.array(NAVY, np.float32)[None, None] * (1.12 - 0.5 * np.clip(r, 0, 1.3)[..., None] ** 1.6)
    n = np.asarray(Image.fromarray((rng.random((H // 16, W // 16)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(20)), np.float32) / 255
    base *= (0.88 + 0.24 * n)[..., None]
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(im)
    for _ in range(140):   # fine scratches
        x, y = rng.uniform(0, W), rng.uniform(0, H); a = rng.uniform(0, math.pi); l = rng.uniform(20, 160)
        d.line((x, y, x + l * math.cos(a), y + l * math.sin(a)), fill=(150, 160, 185, int(rng.uniform(10, 35))), width=1)
    return im
def finish(img, t):
    """grain, drifting dust, a soft blue grade and vignette over the whole frame"""
    rng = np.random.default_rng(int(t * 30)); a = np.asarray(img.convert('RGB')).astype(np.int16)
    a += rng.normal(0, 6, (H, W))[..., None].astype(np.int16)
    for _ in range(18):
        x, y = int(rng.uniform(0, W)), int(rng.uniform(0, H)); a[max(0, y - 1):y + 2, max(0, x - 1):x + 2] += int(rng.choice([-50, 60]))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

# ---------- prints ----------
def print_(name, wd, src=None, crop=None, tone=True, cap=None, seed=1):
    if src is None: return _print(name, wd, crop, tone, cap, seed)
    return _print_im(src, wd, crop, tone, cap, seed)
@functools.lru_cache(maxsize=64)
def _print(name, wd, crop, tone, cap, seed): return _print_im(L9.src(name), wd, crop, tone, cap, seed)
def _print_im(src, wd, crop=None, tone=True, cap=None, seed=1):
    """an old print: black and white, slightly blue, a white deckled border, faint wear, optional handwriting on the border"""
    im = src.convert('RGB')
    if crop: im = im.crop(crop)
    ph = int(wd * im.height / im.width); im = im.resize((wd, ph), Image.LANCZOS)
    g = ImageOps.grayscale(im); g = ImageEnhance.Contrast(g).enhance(1.15)
    im = Image.merge('RGB', (g.point(lambda v: int(v * 0.93)), g.point(lambda v: int(v * 0.96)), g)) if tone else im
    bw = max(14, wd // 26); bb = bw * (3 if cap else 1); P_ = Image.new('RGBA', (wd + 2 * bw, ph + bw + bb), (238, 236, 230, 255)); P_.paste(im, (bw, bw))
    rng = np.random.default_rng(seed); a = np.asarray(P_.getchannel('A')).copy()   # deckled edge: nibble the outline
    for x in range(0, P_.width, 6):
        a[:int(rng.uniform(0, 4)), x:x + 6] = 0; a[P_.height - int(rng.uniform(0, 4)):, x:x + 6] = 0
    for y in range(0, P_.height, 6):
        a[y:y + 6, :int(rng.uniform(0, 4))] = 0; a[y:y + 6, P_.width - int(rng.uniform(0, 4)):] = 0
    P_.putalpha(Image.fromarray(a))
    gm = grunge(seed).resize(P_.size); P_ = Image.composite(P_, Image.new('RGBA', P_.size, (205, 205, 200, 255)), gm.point(lambda v: 255 if v > 120 else 200))
    P_.putalpha(Image.fromarray(a))
    if cap: ImageDraw.Draw(P_).text((bw + 10, ph + bw + bb * 0.45), cap, font=script(int(bb * 0.75)), fill=(70, 70, 80, 230), anchor='lm')
    return P_
def card(can, P_, cx, cy, rot, sc=1.0, alpha=1.0, mb=(0, 0)):
    """lay a print with its shadow; mb = motion (dx, dy) this frame for a smear"""
    if sc != 1: P_ = P_.resize((max(1, int(P_.width * sc)), max(1, int(P_.height * sc))), Image.BICUBIC)
    P_ = P_.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 1: P_ = P_.copy(); P_.putalpha(P_.getchannel('A').point(lambda v: int(v * alpha)))
    x, y = int(cx - P_.width / 2), int(cy - P_.height / 2)
    sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.55 * alpha)))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (x + 10, y + 22))
    if abs(mb[0]) + abs(mb[1]) > 3:
        acc = Image.new('RGBA', can.size, (0, 0, 0, 0))
        for k in range(7):
            f = (k - 3) / 6; L = Image.new('RGBA', can.size, (0, 0, 0, 0)); L.alpha_composite(P_, (int(x + mb[0] * f), int(y + mb[1] * f))); L.putalpha(L.getchannel('A').point(lambda v: v // 3)); acc.alpha_composite(L)
        can.alpha_composite(acc); return
    can.alpha_composite(P_, (x, y))
def fly(t, t0, dur, frm, to, r0, r1):
    """position, rotation and per-frame motion of a print flying in"""
    u = eout((t - t0) / dur); u2 = eout((t + 1 / FPS - t0) / dur)
    p = (lerp(frm[0], to[0], u), lerp(frm[1], to[1], u)); q = (lerp(frm[0], to[0], u2), lerp(frm[1], to[1], u2))
    return p, lerp(r0, r1, u), ((q[0] - p[0]) * 3, (q[1] - p[1]) * 3)
CLIPS = LAC + 'clip/'
@functools.lru_cache(maxsize=48)
def _fr(k, i): return Image.open(CLIPS + '%s/%05d.jpg' % (k, i)).convert('RGB')
def film(k, tt): n = len(os.listdir(CLIPS + k)); return _fr(k, max(1, min(n, int(tt * 25) + 1)))

# ---------- type ----------
def gtext(s, font, col, track=-2):
    """one line of extra-bold type with tight tracking and worn ink"""
    xs = []; x = 0
    for ch in s: xs.append(x); x += font.getlength(ch) + track
    asc, desc = font.getmetrics(); L = Image.new('RGBA', (int(x) + 20, asc + desc + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for ch, xx in zip(s, xs): d.text((10 + xx, 10), ch, font=font, fill=col + (255,))
    gm = grunge(len(s)).crop((0, 0, L.width, L.height)); L.putalpha(ImageChops.multiply(L.getchannel('A'), gm.point(lambda v: min(255, int(v * 1.05)))))
    return L
def reveal(L, k, mode='up'):
    """letters rise out of a mask (the reference's title animation)"""
    if k >= 1: return L
    out = Image.new('RGBA', L.size, (0, 0, 0, 0)); dy = int((1 - k) * L.height * 0.9); out.alpha_composite(L.crop((0, 0, L.width, L.height - dy)), (0, dy)); return out
def put(can, L, cx, cy, anchor='m', alpha=1.0):
    if alpha < 1: L = L.copy(); L.putalpha(L.getchannel('A').point(lambda v: int(v * alpha)))
    x = cx - L.width / 2 if anchor == 'm' else (cx if anchor == 'l' else cx - L.width)
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.45)))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (int(x + 4), int(cy - L.height / 2 + 8))); can.alpha_composite(L, (int(x), int(cy - L.height / 2)))
def titleblock(can, t, t0, big, small, cy, big_first=True, size=230, ssize=96, strip=None, t_strip=None, col_small=YEL):
    """the reference's title: a big white number/word beside a two-line yellow title, a torn white strip with small dark caps underneath"""
    if t < t0: return
    while True:   # fit the block into the safe width
        Lb = gtext(big, mont(size, 900), CREAM, -6); ls = [gtext(s, mont(ssize, 900), col_small, -3) for s in small]
        sw_ = max(l.width for l in ls); gap = 18; tot = Lb.width + gap + sw_
        if tot <= 800 or size < 60: break
        size = int(size * 0.92); ssize = int(ssize * 0.92)
    x0 = CX - tot / 2
    kb = eout((t - t0) / 0.45); ks = eout((t - t0 - 0.15) / 0.45)
    xb, xs = (x0, x0 + Lb.width + gap) if big_first else (x0 + sw_ + gap, x0)
    put(can, reveal(Lb, kb), xb, cy, 'l', min(1, kb * 2))
    for i, l in enumerate(ls):
        yy = cy - (len(ls) - 1) * ssize * 0.46 + i * ssize * 0.92
        put(can, reveal(l, ks), xs if big_first else xs + sw_ - l.width, yy, 'l', min(1, ks * 2))
    if strip and t > (t_strip or t0 + 0.5):
        k = eout((t - (t_strip or t0 + 0.5)) / 0.35); f = mont(34, 800); lines = strip
        w_ = int(max(f.getlength(s) for s in lines) + 70); h_ = 26 + 44 * len(lines)
        P_ = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); rng = np.random.default_rng(len(lines[0]))
        top = [(x, rng.uniform(0, 7)) for x in range(0, w_ + 1, 10)]; bot = [(x, h_ - rng.uniform(0, 7)) for x in range(w_, -1, -10)]
        ImageDraw.Draw(P_).polygon(top + bot, fill=(234, 232, 226, 255))
        for i, s_ in enumerate(lines): ImageDraw.Draw(P_).text((35, 16 + i * 44), s_, font=f, fill=INK + (255,))
        gm = grunge(9).crop((0, 0, w_, h_)); P_.putalpha(ImageChops.multiply(P_.getchannel('A'), gm))
        m = np.clip((k * (w_ + 60) - np.arange(w_)) / 60, 0, 1); P_.putalpha(Image.fromarray((np.asarray(P_.getchannel('A'), np.float32) * m[None, :]).astype(np.uint8)))
        put(can, P_, CX, cy + size * 0.5 + 30 + h_ / 2)
def quote(can, t, parts, cy, size=74, line_h=1.02):
    """a quote in white caps, words appearing with the voice: parts = [(line, [(word, t0, colour)])]"""
    f = mont(size, 900)
    while size > 30 and max(sum(f.getlength(w_) for w_, _, _ in ws_) + f.getlength(' ') * 0.8 * (len(ws_) - 1) for _, ws_ in parts) > 800: size -= 4; f = mont(size, 900)
    for li, (_, words) in enumerate(parts):
        Ls = [(gtext(w_, f, col, -2), t0) for w_, t0, col in words]; sp = f.getlength(' ') * 0.8
        tot = sum(l.width for l, _ in Ls) + sp * (len(Ls) - 1); x = CX - tot / 2; y = cy + li * size * line_h
        for l, t0 in Ls:
            if t >= t0: k = eout((t - t0) / 0.3); put(can, reveal(l, k), x, y, 'l', min(1, k * 2))
            x += l.width + sp

# ---------- the 28.6 s ----------
# props laid on the stage (kept between scenes so the pile grows, like the reference)
PR = {
 'hart': lambda: print_('l_8576', 640, cap='Werner Hartenstein', seed=2),
 'uboat': lambda: print_('l_img1', 760, seed=3),
 'deck': lambda: print_('l_hss', 820, crop=(150, 0, 2750, 1536), seed=4),
 'raft': lambda: print_('l_16794967', 600, seed=5),
 'b24': lambda: print_('l_b24', 700, seed=6),
 'hart2': lambda: print_('l_hart2', 760, crop=(400, 200, 1600, 1500), cap='12. September 1942', seed=7),
 'ship': lambda: print_('l_img', 820, crop=(0, 250, 2654, 1500), cap='RMS Laconia', seed=8),
 'surv': lambda: print_('l_survivors', 760, seed=9),
 'sen': lambda: print_('l_sen', 700, seed=10),
 'deck2': lambda: print_('l_220963', 700, seed=13)}
def P(k): return PR[k]()
def s_hook(t, w0, w1):
    can = stage().copy()
    bg = film('women', t * 0.8); bg = ImageOps.grayscale(bg.resize((W, int(W * bg.height / bg.width)))).convert('RGBA'); bg = bg.resize((W, H), Image.BICUBIC, box=(bg.width * 0.2, 0, bg.width * 0.8, bg.height))
    bg.putalpha(60); can.alpha_composite(Image.merge('RGBA', (*[c.point(lambda v: int(v * 0.7)) for c in bg.convert('RGB').split()], bg.getchannel('A'))))
    for k_, t0, frm, to, r0, r1 in (('deck', 0.0, (-900, 300), (300, 420), -40, -12), ('raft', 0.15, (W + 700, 200), (800, 330), 30, 9), ('b24', 0.3, (W + 800, 1300), (820, 1000), -30, -8),
                                    ('hart', 0.45, (CX, H + 900), (CX - 60, 740), 14, 3)):
        if t > t0: p, r, mb = fly(t, t0, 0.6, frm, to, r0, r1); card(can, P(k_), p[0], p[1], r, 1.0, mb=mb)
    quote(can, t, [('ER VERSENKTE EIN SCHIFF,', [('ER', ws('Er'), CREAM), ('VERSENKTE', ws('versenkte'), CREAM), ('EIN', ws('ein', 0.5), CREAM), ('SCHIFF,', ws('Schiff'), CREAM)]),
                   ('', [('RETTETE', ws('rettete'), CREAM), ('HUNDERTE', ws('Hunderte'), YEL)]), ('', [('SCHIFFBRÜCHIGE', ws('Schiffbrüchige', 2.5), CREAM)]),
                   ('', [('UND', ws('und', 3.3), CREAM), ('WURDE', ws('wurde', 3.6), CREAM), ('BOMBARDIERT.', ws('bombardiert'), YEL)])], 1300, 66)
    return drift(can, t, w0, w1, 1.0, 1.05, 0, -1.2)
def s_1942(t, w0, w1):
    can = stage().copy()
    for k_, t0, frm, to, r0, r1 in (('uboat', w0, (-900, 700), (420, 760), -30, -7), ('sen', w0 + 0.12, (W + 900, 300), (720, 470), 25, 10), ('raft', w0 + 0.25, (W + 700, 1300), (760, 1180), -20, 6)):
        p, r, mb = fly(t, t0, 0.6, frm, to, r0, r1); card(can, P(k_), p[0], p[1], r, 0.85, mb=mb)
    titleblock(can, t, ws('September') - 0.1, '1942', ['U 156 VOR', 'WESTAFRIKA'], 1440, True, 210, 84,
               ['IM SEPTEMBER 1942 LAG U 156', 'VOR DER KÜSTE WESTAFRIKAS.'], ws('U', 7.5))
    return drift(can, t, w0, w1, 1.03, 1.0, 1.0, 0)
def s_attack(t, w0, w1):
    can = stage().copy()
    p, r, mb = fly(t, w0, 0.7, (CX, -900), (CX + 40, 760), -25, -4); card(can, P('hart2'), p[0], p[1], r, 1.05, mb=mb)
    titleblock(can, t, ws('torpedierte'), '12.9.', ['DER', 'ANGRIFF'], 1420, False, 200, 84,
               ['KOMMANDANT WERNER HARTENSTEIN', 'TORPEDIERT DIE LACONIA.'], ws('Werner'))
    return drift(can, t, w0, w1, 1.0, 1.06, 0, 0)
def s_ship(t, w0, w1):
    can = stage().copy()
    p, r, mb = fly(t, w0, 0.6, (W + 1000, 800), (CX + 20, 820), 30, -3); card(can, P('ship'), p[0], p[1], r, 1.05, mb=mb)
    titleblock(can, t, ws('Laconia') - 0.15, 'LACONIA', ['BRITISCHES', 'TRUPPEN-', 'TRANSPORTSCHIFF'], 1430, True, 150, 54, None)
    return drift(can, t, w0, w1, 1.05, 1.0, -0.8, 0)
def s_people(t, w0, w1):
    """two prints with the archive film of the passengers inside them; with the list, two new prints are dealt on top"""
    can = stage().copy(); tl = ws('britische', 20.7)
    for k_, frm, to, r0, r1, wd, d0 in (('pax', (-900, 500), (380, 560), -25, -6, 620, 0.0), ('women', (W + 900, 800), (700, 820), 25, 7, 560, 0.15)):
        tt = t - w0; P_ = print_(None, wd, src=film(k_, min(tt, 4.9 if k_ == 'pax' else 9.4)), seed=11 if k_ == 'pax' else 12)
        p, r, mb = fly(t, w0 + d0, 0.6, frm, to, r0, r1); card(can, P_, p[0], p[1], r, 1.0, mb=mb)
        if t > tl - 0.1: break
    if t > tl - 0.1:
        for k_, t0, frm, to, r0, r1 in (('surv', tl - 0.1, (-900, 700), (420, 640), -20, -5), ('deck2', tl + 0.1, (W + 900, 900), (680, 900), 22, 6)):
            p, r, mb = fly(t, t0, 0.6, frm, to, r0, r1); card(can, P(k_), p[0], p[1], r, 0.9, mb=mb)
    if t < tl - 0.05:
        titleblock(can, t, ws('2.700'), '2.700', ['MENSCHEN', 'AN BORD'], 1380, True, 210, 84)
    else:
        f = mont(44, 800); y = 1180
        for s_, t0 in (('BRITISCHE SOLDATEN', tl), ('ZIVILISTEN, FRAUEN UND KINDER', ws('Zivilisten')), ('POLNISCHE WACHSOLDATEN', ws('polnische'))):
            if t >= t0: k = eout((t - t0) / 0.3); put(can, reveal(gtext(s_, f, CREAM, -1), k), CX, y, 'm', min(1, k * 2))
            y += 60
        titleblock(can, t, ws('1.800'), '1.800', ['ITALIENISCHE', 'GEFANGENE'], 1440, True, 170, 66)
    return drift(can, t, w0, w1, 1.0, 1.05, 0.8, 0)
def drift(can, t, w0, w1, z0, z1, rot_per_s, dy_per_s):
    """the slow camera move over the table: zoom, a little rotation, a little travel"""
    u = clamp((t - w0) / max(0.01, w1 - w0)); z = lerp(z0, z1, eio(u)); a = rot_per_s * (t - w0) * 0.4
    big = can.rotate(a, resample=Image.BICUBIC, center=(W / 2, H / 2), fillcolor=NAVY + (255,)) if abs(a) > 0.01 else can
    z = max(z, 1.0) + 0.03; cw, ch = W / z, H / z; oy = max(-(H - ch) / 2, min((H - ch) / 2, dy_per_s * (t - w0) * 10))
    return big.resize((W, H), Image.BICUBIC, box=((W - cw) / 2, (H - ch) / 2 + oy, (W + cw) / 2, (H + ch) / 2 + oy))
SC = [(0.0, s_hook), (ws('Im'), s_1942), (ws('Am', 10.9), s_attack), (ws('das', 15.2), s_ship), (ws('An', 17.9), s_people)]
TEND = wt('Als') - 0.08
def frame(t):
    i = max(j for j, (a, _) in enumerate(SC) if a <= t); a, fn = SC[i]; b = SC[i + 1][0] if i + 1 < len(SC) else TEND
    img = fn(t, a, b)
    if i + 1 < len(SC) and t > b - 0.2:   # the reference cuts through a quick blur
        u = (t - (b - 0.2)) / 0.2; img = img.filter(ImageFilter.GaussianBlur(14 * eio(u)))
    if i > 0 and t < a + 0.2:
        u = (t - a) / 0.2; img = img.filter(ImageFilter.GaussianBlur(14 * (1 - eio(u))))
    if t < 0.35: img = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), img, eio(t / 0.35))
    return finish(img, t)

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); P_ = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = frame(t).convert('RGBA'); d = ImageDraw.Draw(f)
            if os.environ.get('UI'):
                d.rectangle((0, 0, W, 290), outline=(0, 255, 255, 255), width=4); d.rectangle((930, 680, W, 1580), outline=(0, 255, 255, 255), width=4); d.rectangle((0, 1580, W, H), outline=(0, 255, 255, 255), width=4)
            d.text((10, 300), '%.2f' % t, fill=(255, 0, 255, 255)); P_.paste(f.convert('RGB').resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P_.save(B + sys.argv[2], quality=85); sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
        if n % 30 == 0: print('t', n / FPS, flush=True)
    p.stdin.close(); p.wait(); print('rc', p.returncode)
