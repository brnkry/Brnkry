# Bölter Short in the "Edison" reference style: grey typewritten-letter paper, kinetic word-by-word type in mixed weights,
# grey highlight boxes, outlined numbers, hand-drawn circles / arrows / strikes, taped photo cards with soft shadows,
# a cut-out portrait with a disc behind it, blurred-rectangle card transitions, a fast photo montage at the end.
import sys, os, json, math, re, functools, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
W, H, FPS = 1080, 1920, 30
OFF = 0.15
WD = json.load(open(B + 'words.json'))
def _n(w): return re.sub(r'[^a-zäöüß0-9]', '', w.lower())
TOK = [_n(w[0]) for w in WD]
def K(phrase, i=0):
    p = [_n(x) for x in phrase.split()]; hits = [k for k in range(len(TOK) - len(p) + 1) if TOK[k:k + len(p)] == p]
    assert len(hits) == 1, (phrase, hits); return WD[hits[0] + i][1] + OFF
T_END = WD[-1][2] + OFF + 1.3
FD = '/usr/share/fonts/opentype/inter/'
@functools.lru_cache(None)
def font(kind, size):
    f = {'b': 'Inter-ExtraBold.otf', 'h': 'InterDisplay-Black.otf', 'l': 'Inter-Light.otf', 'm': 'Inter-Medium.otf', 'o': 'InterDisplay-Black.otf'}[kind]
    return ImageFont.truetype(FD + f, size)
DARK, MID, LITE, BOXC = (48, 48, 50), (92, 92, 95), (232, 232, 230), (188, 188, 186)
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eout(u): u = clamp(u); return 1 - (1 - u) ** 3
def eio(u): u = clamp(u); return u * u * (3 - 2 * u)

# ---------------- background: a grey typed letter with faint handwriting ----------------
@functools.lru_cache(None)
def paper():
    bw, bh = 1240, 2200; im = Image.new('L', (bw, bh), 0); a = np.zeros((bh, bw), np.float32)
    g = np.linspace(0, 1, bh)[:, None]; base = 196 - 30 * np.clip((g - 0.55) / 0.45, 0, 1) ** 1.2 - 10 * np.clip((0.12 - g) / 0.12, 0, 1)
    img = Image.fromarray(np.repeat(base, bw, 1).astype(np.uint8)).convert('RGB'); d = ImageDraw.Draw(img)
    mono = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 30)
    lines = ['Kommando der schweren Panzer-Abteilung 502', 'Abt. Gef. Std., den 8. April 1944', '', 'Betr.: Gefechtsbericht vom 7.4.1944 südlich Pskow',
             'Am Morgen griffen feindliche Panzer mit aufgesessener Infanterie', 'den Abschnitt der 1. Kompanie an. Zwei Tiger unter Führung', 'des Leutnants hielten die Stellung und wehrten den Angriff ab.',
             'Bei eigenen geringen Verlusten wurden 22 Feindpanzer vernichtet,', 'davon 15 durch den Kompanieführer selbst.', '', 'Die Besatzungen haben sich durch Umsicht und Tapferkeit', 'besonders ausgezeichnet. Es wird gebeten, den Leutnant', 'zur Verleihung des Ritterkreuzes vorzuschlagen.',
             '', 'Munitionslage: ausreichend. Betriebsstoff: knapp.', 'Ausfälle: 1 Tiger kurzfristig, Kettenschaden.', '', 'Für die Richtigkeit:', '', 'Anlagen: 2 Skizzen, 1 Abschußliste']
    y = 330
    for ln in lines * 2:
        d.text((90, y), ln, font=mono, fill=(168, 168, 168)); y += 58
    hand = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf', 96)
    d.text((300, 120), 'Abschußliste', font=hand, fill=(160, 160, 160))
    L = Image.new('L', img.size, 0); dl = ImageDraw.Draw(L)
    rng = np.random.default_rng(7)
    for k in range(5):   # loose handwriting strokes across the page
        x0, y0 = 120 + rng.random() * 500, 700 + k * 260 + rng.random() * 80; pts = []
        for s in range(160):
            x = x0 + s * 4.2; y = y0 + 22 * math.sin(s * 0.55 + k) + 10 * math.sin(s * 1.9) - s * 0.35
            pts.append((x, y))
        dl.line(pts, fill=255, width=4, joint='curve')
    img.paste((95, 95, 95), (0, 0), L.filter(ImageFilter.GaussianBlur(0.8)).point(lambda v: int(v * 0.35)))
    img = img.filter(ImageFilter.GaussianBlur(1.3))
    n = (rng.random((bh // 2, bw // 2)) * 18 - 9).astype(np.float32); n = np.asarray(Image.fromarray(n.astype(np.int8).astype(np.uint8)).resize((bw, bh)), np.float32)
    return img
def background(t, wm=None, wm_a=0.0):
    p = paper(); z = 1.0 + 0.0008 * t; dx = 40 + 10 * math.sin(t * 0.05); dy = 120 + t * 1.2
    cw, ch = W / z, H / z
    bg = p.resize((W, H), Image.BICUBIC, box=(dx, dy, dx + cw, dy + ch))
    if wm and wm_a > 0:
        f = font('h', 560); L = Image.new('L', (W, H), 0); ImageDraw.Draw(L).text((W / 2, 1330), wm, font=f, fill=255, anchor='mm')
        bg.paste((206, 206, 204), (0, 0), L.filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * 0.5 * wm_a)))
    return bg

# ---------------- type ----------------
@functools.lru_cache(maxsize=512)
def word_img(s, kind, size, col, cond=1.0):
    f = font(kind, size); bb = f.getbbox(s); w, h = bb[2] + 12, int(size * 1.3)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == 'o':
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).text((4, int(size * 0.05)), s, font=f, fill=255)
        ring = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(5)), m.filter(ImageFilter.MinFilter(5)))
        im.paste(col + (255,), (0, 0), ring)
    else: d.text((4, int(size * 0.05)), s, font=f, fill=col + (255,))
    if cond != 1.0: im = im.resize((max(1, int(w * cond)), h), Image.LANCZOS)
    return im
class Line:
    """one line of words: [(text, kind, size, t_appear, opts)], left x or centred; words fade/slide in when spoken"""
    def __init__(self, x, y, words, anchor='l', gap=18, col=DARK):
        if y < 1000: y = int(300 + (y - 330) * 1.28)
        self.x, self.y, self.words, self.anchor, self.gap, self.col = x, y, words, anchor, gap, col
    def layout(self):
        imgs = []
        for w in self.words:
            s, kind, size, ta = w[:4]; o = w[4] if len(w) > 4 else {}; size = int(size * 1.28)
            col = o.get('col', self.col); cond = 0.8 if kind in ('h', 'o') else 1.0
            imgs.append((word_img(s, kind, size, col, cond), ta, o, size))
        tw = sum(i[0].width for i in imgs) + self.gap * (len(imgs) - 1)
        mw = (W - 80 - self.x) if self.anchor == 'l' else ((self.x - 80) if self.anchor == 'r' else W - 160)
        if tw > mw:
            f = mw / tw; imgs = [(im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.LANCZOS), ta, o, int(sz * f)) for im, ta, o, sz in imgs]; tw = mw
        x = self.x - (tw / 2 if self.anchor == 'c' else (tw if self.anchor == 'r' else 0)); out = []
        base = max(i[3] for i in imgs)
        for im, ta, o, size in imgs:
            y = self.y + int((base - size) * 1.0); out.append((im, int(x), y, ta, o)); x += im.width + self.gap
        return out
    def draw(self, can, t):
        boxes = {}
        for im, x, y, ta, o in self.layout():
            if t < ta: continue
            k = eout((t - ta) / 0.18)
            if o.get('box'):
                d = ImageDraw.Draw(can); bw = int(im.width * eout((t - ta) / 0.22)); d.rectangle((x - 8, y + 4, x - 8 + bw + 10, y + im.height - 6), fill=BOXC + (230,))
            w = im
            if k < 1:
                w = im.copy(); w.putalpha(w.getchannel('A').point(lambda v: int(v * k))); w = w.filter(ImageFilter.GaussianBlur(5 * (1 - k)))
            can.alpha_composite(w, (x, int(y + 26 * (1 - k))))
            boxes[o.get('id', '')] = (x, y, x + im.width, y + im.height)
        return boxes
def typewriter(can, t, t0, t1, s, x, y, kind='b', size=84, col=DARK, cursor_until=None):
    if t < t0: return
    n = int(len(s) * clamp((t - t0) / max(0.05, t1 - t0)) + 0.999); sub = s[:n]
    if sub: can.alpha_composite(word_img(sub, kind, size, col), (x, y))
    cu = cursor_until if cursor_until is not None else t1 + 0.8
    if t < cu and int(t * 3) % 2 == 0:
        cx = x + (word_img(sub, kind, size, col).width if sub else 6); ImageDraw.Draw(can).rectangle((cx, y + 10, cx + 6, y + int(size * 1.15)), fill=col + (255,))

# ---------------- pen marks ----------------
def pen_ellipse(can, t, t0, box, dur=0.45, wd=7, col=DARK):
    if t < t0: return
    u = eout((t - t0) / dur); x0, y0, x1, y1 = box; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 26, (y1 - y0) / 2 + 16
    n = int(110 * u) + 2; pts = []
    for i in range(n):
        a = -2.4 + i / 100 * 2 * math.pi * 1.08; r = 1 + 0.035 * math.sin(i * 0.21)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    ImageDraw.Draw(can).line(pts, fill=col + (255,), width=wd, joint='curve')
def pen_arrow(can, t, t0, p0, p1, bend=0.25, dur=0.35, wd=6, col=DARK):
    if t < t0: return
    u = eout((t - t0) / dur); mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2; nx, ny = -(p1[1] - p0[1]) * bend, (p1[0] - p0[0]) * bend
    c = (mx + nx, my + ny); pts = []
    for i in range(int(40 * u) + 2):
        s = i / 40; pts.append(((1 - s) ** 2 * p0[0] + 2 * (1 - s) * s * c[0] + s * s * p1[0], (1 - s) ** 2 * p0[1] + 2 * (1 - s) * s * c[1] + s * s * p1[1]))
    d = ImageDraw.Draw(can); d.line(pts, fill=col + (255,), width=wd, joint='curve')
    if u > 0.9 and len(pts) > 2:
        (ax, ay), (bx, by) = pts[-3], pts[-1]; ang = math.atan2(by - ay, bx - ax)
        for s in (2.6, -2.6): d.line((bx, by, bx + 30 * math.cos(ang + s), by + 30 * math.sin(ang + s)), fill=col + (255,), width=wd)
def pen_strike(can, t, t0, p0, p1, dur=0.25, wd=8, col=DARK):
    if t < t0: return
    u = eout((t - t0) / dur); ImageDraw.Draw(can).line((p0, (p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u)), fill=col + (255,), width=wd)
def tally(can, t, ts, x, y, col=DARK):
    d = ImageDraw.Draw(can)
    for i, ti in enumerate(ts):
        if t < ti: continue
        u = eout((t - ti) / 0.12)
        if i < 4 or i >= 5: xx = x + (i if i < 5 else i + 1) * 46; d.line((xx, y, xx + 6, y + 150 * u), fill=col + (255,), width=10)
        else: d.line((x - 20, y + 120, x - 20 + 230 * u, y + 30 - 10 * u), fill=col + (255,), width=10)

# ---------------- pictures ----------------
@functools.lru_cache(maxsize=64)
def load(name):
    p = B + 'img/' + name
    im = Image.open(p).convert('RGBA' if p.endswith('.png') else 'RGB')
    return im
def clip_frame(name, i):
    d = B + 'clip/' + name + '/'; n = len(os.listdir(d)); return Image.open(d + 'f%04d.jpg' % (i % n + 1)).convert('RGB')
def grade(im):
    g = ImageEnhance.Contrast(im.convert('L')).enhance(1.12).convert('RGB'); return g
def fit(im, bw, bh, fx=0.5, fy=0.5, z=1.0):
    w, h = im.size; sc = max(bw / w, bh / h) * z; cw, ch = bw / sc, bh / sc
    return im.resize((bw, bh), Image.LANCZOS, box=((w - cw) * fx, (h - ch) * fy, (w - cw) * fx + cw, (h - ch) * fy + ch))
@functools.lru_cache(maxsize=32)
def shadow(bw, bh, r=34, a=150):
    s = Image.new('L', (bw + 4 * r, bh + 4 * r), 0); ImageDraw.Draw(s).rectangle((2 * r, 2 * r, 2 * r + bw, 2 * r + bh), fill=a); return s.filter(ImageFilter.GaussianBlur(r))
def tape(can, x, y, ang, k=1.0):
    t = Image.new('RGBA', (190, 56), (38, 38, 40, int(235 * k))); t = t.rotate(ang, expand=True, resample=Image.BICUBIC); can.alpha_composite(t, (int(x - t.width / 2), int(y - t.height / 2)))
def card(can, t, t0, src, box, t1=None, tapes=True, fx=0.5, fy=0.4, zoom=0.05, out=0.22):
    """a photo or film card: a blurred grey slab grows in, the picture sharpens into it, tape on the top corners"""
    if t < t0 or (t1 is not None and t > t1 + out): return
    x, y, bw, bh = box; y = min(y + 70, 1650 - bh) if y < 1300 else y; u = (t - t0) / 0.36; ko = 1.0 if t1 is None or t < t1 else 1 - (t - t1) / out
    if isinstance(src, tuple): im = clip_frame(src[0], int((t - t0) * FPS * src[1]))
    else: im = load(src)
    if callable(src): im = src(t)
    z = 1 + zoom * clamp((t - t0) / 6.0); ph = grade(fit(im.convert('RGB'), bw, bh, fx, fy, z))
    s = 0.9 + 0.1 * eout(u); cw, ch = int(bw * s), int(bh * s); cx, cy = x + (bw - cw) // 2, y + (bh - ch) // 2
    sh = shadow(bw, bh); can.paste((0, 0, 0), (x - 2 * 34 + 6, y - 2 * 34 + 26), Image.eval(sh, lambda v: int(v * clamp(u) * ko)).convert('L')) if False else None
    shl = Image.new('RGBA', sh.size, (0, 0, 0, 0)); shl.putalpha(sh.point(lambda v: int(v * clamp(u) * ko))); can.alpha_composite(shl, (x - 68 + 6, y - 68 + 26))
    if u < 0.55:
        slab = Image.new('RGBA', (cw, ch), (112, 112, 114, int(255 * clamp(u / 0.3) * ko))); slab = slab.filter(ImageFilter.GaussianBlur(18 * (1 - u / 0.55)))
        can.alpha_composite(slab, (cx, cy)); return
    k = eout((u - 0.55) / 0.45); p = ph.resize((cw, ch)) if (cw, ch) != (bw, bh) else ph
    if k < 1: p = Image.blend(Image.new('RGB', p.size, (112, 112, 114)), p.filter(ImageFilter.GaussianBlur(10 * (1 - k))), k)
    pa = p.convert('RGBA'); pa.putalpha(int(255 * ko)); can.alpha_composite(pa, (cx, cy))
    if tapes and k > 0.3: tape(can, cx + 30, cy + 8, 38, ko); tape(can, cx + cw - 30, cy + 8, -38, ko)
def cutout(can, t, t0, name, box, blur=0.0, k=1.0):
    if t < t0: return
    x, y, bw, bh = box; y += 60; im = load(name); im = fit(im, bw, bh, 0.5, 0.0)
    g = im.convert('LA').convert('RGBA'); a = im.getchannel('A')
    sh = Image.new('RGBA', g.size, (0, 0, 0, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.55 * k)))
    can.alpha_composite(sh, (x + 14, y + 24))
    if blur > 0.3: g = g.filter(ImageFilter.GaussianBlur(blur))
    if k < 1: g.putalpha(g.getchannel('A').point(lambda v: int(v * k)))
    can.alpha_composite(g, (x, y))
def disc(can, t, t0, cx, cy, r, k=1.0):
    if t < t0: return
    u = eout((t - t0) / 0.5) * k; L = Image.new('L', (W, H), 0); ImageDraw.Draw(L).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255); L = L.filter(ImageFilter.GaussianBlur(30))
    can.alpha_composite(Image.merge('RGBA', (Image.new('L', (W, H), 70),) * 3 + (L.point(lambda v: int(v * 0.55 * u)),)))

