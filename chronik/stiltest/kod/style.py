# Collage style test (Laconia, first 29 s): light grey paper, cut-out figures in black and white with soft shadows, one accent colour,
# big kinetic type layered between the shapes and the figures, motion-blurred entries, accent bands and circles, a slow push on every scene.
import sys, os, json, math, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
LAC = B + '../lac/'
sys.path.insert(0, LAC + 'code')
W, H, FPS = 1080, 1920, 30
ACC = (244, 199, 15); INK = (24, 24, 26); GREY = (120, 120, 124); PAPER0, PAPER1 = (240, 240, 238), (150, 150, 152)
WORDS = json.load(open(LAC + 'words.json'))
def wt(s, after=0.0):
    for w, a, b in WORDS:
        if a >= after - 0.01 and w.lower().startswith(s.lower()): return a
    raise KeyError(s)
def ws(s, after=0.0): return wt(s, after) - 0.04
T = wt('Als') - 0.25   # the test ends after '... italienische Kriegsgefangene.'
def clamp(x): return max(0.0, min(1.0, x))
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def back(x, s=1.7): x = clamp(x); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2   # overshoot
def lerp(a, b, u): return a + (b - a) * u
FD = '/usr/share/fonts/opentype/inter/'
@functools.lru_cache(None)
def black(s): return ImageFont.truetype(FD + 'InterDisplay-Black.otf', s)
@functools.lru_cache(None)
def bold(s): return ImageFont.truetype(FD + 'InterDisplay-Bold.otf', s)
@functools.lru_cache(None)
def slab(s): return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', s)
@functools.lru_cache(None)
def mono(s): return ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', s)
@functools.lru_cache(None)
def hand(s): return ImageFont.truetype(LAC + '../sch/fonts/Caveat.ttf', s)
FX = LAC + '../sch/fonts/'
@functools.lru_cache(None)
def disp(s):
    """condensed display serif with flared ends (closest free match to Historic Mystique); drawn with a thin stroke for weight"""
    f = ImageFont.truetype(FX + 'bigelow-rules.woff', s); f._sw = max(1, s // 45); return f
@functools.lru_cache(None)
def disp2(s): f = ImageFont.truetype(FX + 'rozha-one.woff', s); f._sw = 0; return f

# ---------- paper ----------
@functools.lru_cache(None)
def paper(grid=False, dark=0.0):
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.62)) ** 2)
    k = np.clip(r, 0, 1) ** 1.6
    c = np.array(PAPER0, np.float32)[None, None] * (1 - k[..., None]) + np.array(PAPER1, np.float32)[None, None] * k[..., None]
    c *= 1 - dark
    c += np.random.default_rng(3).normal(0, 2.2, (H, W, 1))
    im = Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).convert('RGBA')
    if grid:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for x in range(0, W, 60): d.line((x, 0, x, H), fill=(110, 140, 190, 60 if x % 300 else 110), width=2)
        for y in range(0, H, 60): d.line((0, y, W, y), fill=(110, 140, 190, 60 if y % 300 else 110), width=2)
        im.alpha_composite(L)
    return im

# ---------- cut-outs ----------
@functools.lru_cache(None)
def cut(name, bw=True, h=None, flat=None):
    im = Image.open(B + 'cut/%s.png' % name).convert('RGBA'); im = im.crop(im.getbbox())
    if h: im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    if flat is not None:   # a flat silhouette
        a = im.getchannel('A'); im = Image.new('RGBA', im.size, flat + (255,)); im.putalpha(a)
    elif bw:
        a = im.getchannel('A'); g = ImageOps.autocontrast(ImageOps.grayscale(im.convert('RGB')), cutoff=1)
        g = ImageEnhance.Contrast(g).enhance(1.15); im = Image.merge('RGBA', (g, g, g, a))
    return im
def place(can, sp, cx, cy, sc=1.0, rot=0.0, alpha=1.0, blur=0.0, shadow=True, mblur=(0, 0)):
    """put a sprite with a soft drop shadow; mblur = (dx, dy) of the motion this frame, smeared over 7 copies"""
    if sc != 1.0: sp = sp.resize((max(1, int(sp.width * sc)), max(1, int(sp.height * sc))), Image.BICUBIC)
    if rot: sp = sp.rotate(rot, expand=True, resample=Image.BICUBIC)
    if blur > 0.3: sp = sp.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 1: sp = sp.copy(); sp.putalpha(sp.getchannel('A').point(lambda v: int(v * alpha)))
    x, y = int(cx - sp.width / 2), int(cy - sp.height / 2)
    if shadow:
        sh = Image.new('RGBA', sp.size, (0, 0, 0, 0)); sh.putalpha(sp.getchannel('A').point(lambda v: int(v * 0.42 * alpha)))
        can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (x + 14, y + 26))
    if abs(mblur[0]) + abs(mblur[1]) > 2:
        acc = Image.new('RGBA', can.size, (0, 0, 0, 0))
        for k in range(7):
            f = (k - 3) / 6; L = Image.new('RGBA', can.size, (0, 0, 0, 0)); L.alpha_composite(sp, (int(x + mblur[0] * f), int(y + mblur[1] * f)))
            L.putalpha(L.getchannel('A').point(lambda v: v // 3)); acc.alpha_composite(L)
        can.alpha_composite(acc); return
    can.alpha_composite(sp, (x, y))
def mover(t, t0, dur, a, b, ease=eout):
    """position at t moving from a to b, and the per-frame motion for motion blur"""
    u = ease((t - t0) / dur); u2 = ease((t + 1 / FPS - t0) / dur)
    p = (lerp(a[0], b[0], u), lerp(a[1], b[1], u)); q = (lerp(a[0], b[0], u2), lerp(a[1], b[1], u2))
    return p, ((q[0] - p[0]) * 3, (q[1] - p[1]) * 3)

# ---------- type ----------
def word(can, t, t0, s, xy, font, col=INK, anchor='mm', dur=0.28, mode='rise', rot=0.0):
    """one word: rises and sharpens in (mode 'rise'), scales down from big and blurred ('slam'), or wipes in ('wipe')"""
    if t < t0: return
    k = eout((t - t0) / dur); bb = font.getbbox(s); w_, h_ = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    sw = getattr(font, '_sw', 0); w_ += 2 * sw; h_ += 2 * sw
    L = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); ImageDraw.Draw(L).text((20 + sw - bb[0], 20 + sw - bb[1]), s, font=font, fill=col + (255,), stroke_width=sw, stroke_fill=col + (255,))
    if mode == 'wipe':
        m = np.clip((k * (w_ + 60) - np.arange(w_)) / 60, 0, 1); L.putalpha(Image.fromarray((np.asarray(L.getchannel('A'), np.float32) * m[None, :]).astype(np.uint8))); sc, dy, bl = 1.0, 0, 0
    elif mode == 'slam':
        sc = lerp(1.9, 1.0, k); dy = 0; bl = (1 - k) * 10
    else:
        sc = 1.0; dy = (1 - k) * 40; bl = (1 - k) * 6
    if rot: L = L.rotate(rot, expand=True, resample=Image.BICUBIC)
    if sc != 1.0: L = L.resize((int(L.width * sc), int(L.height * sc)), Image.BICUBIC)
    if bl > 0.3: L = L.filter(ImageFilter.GaussianBlur(bl))
    L.putalpha(L.getchannel('A').point(lambda v: int(v * min(1, k * 1.5))))
    x, y = xy; ax = {'l': 0, 'm': 0.5, 'r': 1}[anchor[0]]; ay = 0.5
    can.alpha_composite(L, (int(x - L.width * ax), int(y + dy - L.height * ay)))
def scramble(can, t, t0, s, xy, font, col=INK, dur=0.5):
    """letters settle one after another out of random characters (the slab headlines of the reference)"""
    if t < t0: return
    rng = np.random.default_rng(int(t * 30)); n = len(s); u = clamp((t - t0) / dur)
    out = ''.join(c if (i / n < u or c == ' ') else (chr(rng.integers(65, 91)) if u > i / n - 0.35 else ' ') for i, c in enumerate(s))
    sw = getattr(font, '_sw', 0); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).text(xy, out, font=font, fill=col + (255,), anchor='mm', stroke_width=sw, stroke_fill=col + (255,))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.25)))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), (4, 8)); can.alpha_composite(L)
def typed(can, t, t0, s, xy, font, col=INK, step=0.035, anchor='mm'):
    if t < t0: return
    n = min(len(s), int((t - t0) / step) + 1); d = ImageDraw.Draw(can)
    x = xy[0] - font.getlength(s) / 2 if anchor == 'mm' else xy[0]
    d.text((x, xy[1]), s[:n], font=font, fill=col + (255,), anchor='lm')
def brackets(can, t, t0, box, col=INK, w=4, L_=46):
    """thin corner brackets drawn around a box (the frame marks of the reference)"""
    if t < t0: return
    u = eout((t - t0) / 0.35); x0, y0, x1, y1 = box; l = L_ * u; d = ImageDraw.Draw(can); c = col + (220,)
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line((x, y, x + sx * l, y), fill=c, width=w); d.line((x, y, x, y + sy * l), fill=c, width=w)
def bodylines(can, t, t0, x, y, n=5, w_=300, col=GREY):
    """small grey 'body text' lines, the decorative paragraph of the reference"""
    if t < t0: return
    d = ImageDraw.Draw(can); rng = np.random.default_rng(int(x + y))
    for i in range(n):
        u = eout((t - t0 - i * 0.05) / 0.3); d.line((x, y + i * 14, x + w_ * rng.uniform(0.6, 1.0) * u, y + i * 14), fill=col + (200,), width=4)

# ---------- shapes ----------
def band(can, t, t0, y, h_, col=ACC, dur=0.35, rot=0.0, grow=True):
    """an accent band: grows from a thin line to its height"""
    if t < t0: return
    k = eout((t - t0) / dur); hh = lerp(10, h_, k) if grow else h_
    L = Image.new('RGBA', (W + 600, int(hh) + 4), col + (255,))
    if rot: L = L.rotate(rot, expand=True, resample=Image.BICUBIC)
    can.alpha_composite(L, (int(W / 2 - L.width / 2), int(y - L.height / 2)))
def disc(can, t, t0, c, r, col=ACC, dur=0.45):
    if t < t0: return
    k = back((t - t0) / dur); rr = max(1, r * k)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.ellipse((c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr), fill=col + (255,))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.35)))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)), (10, 22)); can.alpha_composite(L)
def stripes(can, t, t0, col=ACC, n=5, wd=120, a=150):
    """diagonal accent stripes sliding in (the blue stripes of the reference)"""
    if t < t0: return
    u = eout((t - t0) / 0.5); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(n):
        x = -400 + i * 330 + (1 - u) * 900
        d.polygon([(x, H * 0.62), (x + wd, H * 0.62), (x + wd + 700, -100), (x + 700, -100)], fill=col + (a,))
    can.alpha_composite(L)
def push(img, t, w0, w1, z0=1.0, z1=1.05):
    """slow push-in on the whole composed frame"""
    z = lerp(z0, z1, clamp((t - w0) / max(0.01, w1 - w0)))
    if z == 1: return img
    cw, ch = W / z, H / z; return img.resize((W, H), Image.BICUBIC, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))

# ---------- film inside shapes ----------
CLIPS = LAC + 'clip/'
@functools.lru_cache(maxsize=48)
def _fr(k, i): return Image.open(CLIPS + '%s/%05d.jpg' % (k, i)).convert('RGB')
@functools.lru_cache(None)
def _n(k): return len(os.listdir(CLIPS + k))
def film(k, tt): return _fr(k, max(1, min(_n(k), int(tt * 25) + 1)))
def filmfill(can, alpha, k, tt, gray=True, tint=None, contrast=1.15, inner=True):
    """the running film shows only inside alpha (a full-frame L mask): ship and letter shapes filled with footage"""
    bb = alpha.getbbox()
    if not bb: return
    im = film(k, tt); bw, bh = bb[2] - bb[0], bb[3] - bb[1]; s = max(bw / im.width, bh / im.height)
    cw, ch = min(im.width, bw / s), min(im.height, bh / s); x0, y0 = max(0.0, (im.width - cw) / 2), max(0.0, (im.height - ch) / 2)
    f = im.resize((bw, bh), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))
    if gray: f = ImageOps.grayscale(f).convert('RGB')
    f = ImageEnhance.Contrast(f).enhance(contrast)
    if tint: f = Image.blend(f, Image.new('RGB', f.size, tint), 0.35)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); L.paste(f, bb[:2]); L.putalpha(alpha)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(alpha.point(lambda v: int(v * 0.4)))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (14, 26)); can.alpha_composite(L)
    if inner:   # a thin dark inner edge so the shape reads as a cut-out
        e = alpha.filter(ImageFilter.MaxFilter(5)); edge = ImageChops.subtract(e, alpha)
        E = Image.new('RGBA', (W, H), INK + (0,)); E.putalpha(edge.point(lambda v: int(v * 0.8))); can.alpha_composite(E)
def textmask(s, font, xy, anchor='mm'):
    sw = getattr(font, '_sw', 0); m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).text(xy, s, font=font, fill=255, anchor=anchor, stroke_width=sw, stroke_fill=255); return m
def spritemask(sp, cx, cy):
    m = Image.new('L', (W, H), 0); m.paste(sp.getchannel('A'), (int(cx - sp.width / 2), int(cy - sp.height / 2))); return m

# ---------- paper pieces ----------
def torn(w_, h_, col=(236, 232, 220), seed=1, edges='tb'):
    """a strip of paper with torn edges"""
    rng = np.random.default_rng(seed); top = [(x, rng.uniform(0, 14)) for x in range(0, w_ + 1, 12)]; bot = [(x, h_ - rng.uniform(0, 14)) for x in range(w_, -1, -12)]
    if 't' not in edges: top = [(0, 0), (w_, 0)]
    if 'b' not in edges: bot = [(w_, h_), (0, h_)]
    L = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); ImageDraw.Draw(L).polygon(top + bot, fill=col + (255,))
    n = (rng.random((h_, w_)) * 10).astype(np.int16); a = np.asarray(L, np.int16).copy(); a[..., :3] = np.clip(a[..., :3] - n[..., None], 0, 255)
    return Image.fromarray(a.astype(np.uint8))
def tape(can, cx, cy, w_=150, rot=-8):
    T_ = Image.new('RGBA', (w_, 46), (235, 228, 200, 170)); T_ = T_.rotate(rot, expand=True, resample=Image.BICUBIC); can.alpha_composite(T_, (int(cx - T_.width / 2), int(cy - T_.height / 2)))
def polaroid(im, wd):
    """a photo in a white instant-print frame"""
    ph = int(wd * im.height / im.width); P_ = Image.new('RGBA', (wd + 40, ph + 120), (246, 244, 238, 255))
    P_.paste(im.convert('RGB').resize((wd, ph), Image.LANCZOS), (20, 20)); return P_
def inkcircle(can, t, t0, box, col=(196, 38, 40), w=7, dur=0.5):
    """a hand-drawn ellipse around something, drawn in one stroke"""
    if t < t0: return
    u = eout((t - t0) / dur); x0, y0, x1, y1 = box; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    pts = [(cx + rx * (1 + 0.04 * math.sin(a * 3)) * math.cos(a), cy + ry * (1 + 0.05 * math.cos(a * 2)) * math.sin(a)) for a in np.linspace(-2.6, -2.6 + 2 * math.pi * 1.08 * u, 80)]
    if len(pts) > 2: ImageDraw.Draw(can).line(pts, fill=col + (235,), width=w, joint='curve')
def harrow(can, t, t0, a, b, col=INK, w=6, bend=0.25, dur=0.5):
    """a hand-drawn curved arrow from a to b"""
    if t < t0: return
    u = eout((t - t0) / dur); mx, my = (a[0] + b[0]) / 2 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2 + (b[0] - a[0]) * bend
    pts = [((1 - v) ** 2 * a[0] + 2 * (1 - v) * v * mx + v * v * b[0], (1 - v) ** 2 * a[1] + 2 * (1 - v) * v * my + v * v * b[1]) for v in np.linspace(0, u, 40)]
    d = ImageDraw.Draw(can); d.line(pts, fill=col + (255,), width=w, joint='curve')
    if u > 0.95:
        e, q = pts[-1], pts[-5]; ang = math.atan2(e[1] - q[1], e[0] - q[0])
        for da in (2.6, -2.6): d.line((e, (e[0] + 34 * math.cos(ang + da), e[1] + 34 * math.sin(ang + da))), fill=col + (255,), width=w)
def uboat(w_, col=INK):
    """a side-view silhouette of a large U-boat (hull, conning tower, deck gun), as an RGBA sprite"""
    h_ = int(w_ * 0.26); L = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = col + (255,); y = h_ * 0.62
    d.polygon([(0, y), (w_ * 0.08, y - h_ * 0.1), (w_ * 0.92, y - h_ * 0.1), (w_, y - h_ * 0.02), (w_ * 0.9, y + h_ * 0.16), (w_ * 0.1, y + h_ * 0.16)], fill=c)
    d.polygon([(w_ * 0.42, y - h_ * 0.1), (w_ * 0.44, y - h_ * 0.42), (w_ * 0.56, y - h_ * 0.42), (w_ * 0.6, y - h_ * 0.1)], fill=c)
    d.rectangle((w_ * 0.47, y - h_ * 0.62, w_ * 0.48, y - h_ * 0.42), fill=c); d.rectangle((w_ * 0.52, y - h_ * 0.56, w_ * 0.53, y - h_ * 0.42), fill=c)
    d.rectangle((w_ * 0.3, y - h_ * 0.2, w_ * 0.36, y - h_ * 0.1), fill=c); d.line((w_ * 0.33, y - h_ * 0.17, w_ * 0.24, y - h_ * 0.24), fill=c, width=max(2, w_ // 120))
    return L
def lifeboat(w_, col=INK):
    h_ = int(w_ * 0.32); L = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); ImageDraw.Draw(L).polygon([(0, h_ * 0.2), (w_, h_ * 0.2), (w_ * 0.82, h_), (w_ * 0.18, h_)], fill=col + (255,)); return L
