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

# ---------------- scenes ----------------
S = []                                    # (t0, t1, watermark, draw(can, t))
def scene(t0, t1, wm=None):
    def deco(f): S.append((t0, t1, wm, f)); return f
    return deco
T = [K('Zwei Tiger') - 0.15, K('Siebenmal wurde'), K('Sein Name war'), K('Er wurde 1915'), K('Schon 1941'), K('Später kam er'), K('Am 7. April'),
     K('zusammen mit einem'), K('Dafür erhielt er'), K('Im September 1944'), K('Einen Monat zuvor'), K('An die Front'), K('Ihm werden rund'), K('die Angaben schwanken'), K('Johannes Bölter starb'), T_END]
T[0] = 0.0
def st(i): return T[i] - 0.12

@scene(st(0), st(1), 'TIGER')
def s1(c, t):
    card(c, t, 0.0, ('tigroad', 1.0), (110, 900, 860, 700))
    if t < K('und 15 davon'):
        Line(90, 360, [('Zwei Tiger', 'b', 72, K('Zwei Tiger'), {'box': 1})]).draw(c, t)
        Line(90, 450, [('gegen', 'l', 70, K('gegen 22')), ('22', 'h', 210, K('gegen 22', 1))]).draw(c, t)
        Line(90, 690, [('sowjetische', 'b', 66, K('sowjetische Panzer, und')), ('Panzer', 'b', 66, K('Panzer, und 15'))]).draw(c, t)
    else:
        bx = Line(90, 330, [('15', 'o', 330, K('und 15 davon', 1), {'id': 'n'}), ('davon', 'l', 80, K('davon schoss'))]).draw(c, t)
        Line(90, 640, [('schoss er', 'b', 74, K('schoss er selbst')), ('selbst', 'h', 110, K('er selbst ab.', 1)), ('ab.', 'b', 74, K('selbst ab.', 1))]).draw(c, t)
        if 'n' in bx: pen_ellipse(c, t, K('er selbst ab.', 1), bx['n'])
@scene(st(1), st(2), '7×')
def s2(c, t):
    disc(c, t, T[1], 640, 1350, 430)
    Line(90, 330, [('Siebenmal', 'h', 190, K('Siebenmal wurde'))]).draw(c, t)
    b = Line(90, 560, [('wurde er im Krieg', 'l', 64, K('wurde er im Krieg')), ('verwundet', 'b', 76, K('Krieg verwundet,', 1), {'id': 'v'})]).draw(c, t)
    cutout(c, t, T[1], 'a_cut.png', (200, 760, 860, 1160), blur=max(0, 28 * (1 - (t - T[1]) / (K('war Johannes Bölter', 1) - T[1]))))
    Line(990, 700, [('trotzdem', 'l', 62, K('und trotzdem'))], anchor='r').draw(c, t)
    Line(990, 780, [('überlebte er.', 'b', 84, K('trotzdem überlebte', 1), {'col': DARK, 'box': 1})], anchor='r').draw(c, t)
    if 'v' in b: pen_strike(c, t, K('und trotzdem'), (b['v'][0] - 10, b['v'][3] - 40), (b['v'][2] + 10, b['v'][1] + 40))
@scene(st(2), st(3), 'NAME')
def s3(c, t):
    card(c, t, T[2] - 0.05, 'a.jpg', (180, 620, 720, 960), fy=0.2)
    Line(140, 380, [('Sein Name war', 'l', 66, K('Sein Name war'))]).draw(c, t)
    typewriter(c, t, K('war Johannes Bölter', 1), K('war Johannes Bölter', 1) + 0.75, 'Johannes Bölter', 140, 460, 'b', 92)
@scene(st(3), st(4), '1915')
def s4(c, t):
    card(c, t, T[3] - 0.05, 'b.jpg', (300, 860, 640, 900), fy=0.15)
    Line(90, 360, [('Er wurde', 'l', 66, K('Er wurde 1915'))]).draw(c, t)
    b = Line(90, 430, [('1915', 'o', 300, K('Er wurde 1915', 2), {'id': 'y'})]).draw(c, t)
    Line(560, 600, [('geboren.', 'b', 72, K('1915 geboren.', 1))]).draw(c, t)
@scene(st(4), st(5), '1941')
def s5(c, t):
    card(c, t, T[4] - 0.05, ('snowtank', 1.0), (110, 980, 860, 640))
    Line(90, 330, [('Schon', 'l', 66, K('Schon 1941')), ('1941', 'h', 170, K('Schon 1941', 1))]).draw(c, t)
    Line(90, 560, [('Ostfront', 'b', 84, K('der Ostfront vor', 1), {'box': 1})]).draw(c, t)
    b = Line(90, 680, [('vor', 'l', 66, K('Ostfront vor Leningrad', 1)), ('Leningrad', 'b', 84, K('vor Leningrad verwundet.', 1), {'id': 'l'})]).draw(c, t)
    Line(990, 860, [('verwundet', 'm', 56, K('Leningrad verwundet.', 1), {'col': MID})], anchor='r').draw(c, t)
    if 'l' in b: pen_ellipse(c, t, K('Leningrad verwundet.', 1), b['l'])
@scene(st(5), st(6), '502')
def s6(c, t):
    card(c, t, T[5] - 0.05, ('tanks697', 1.0), (110, 1020, 860, 600))
    Line(90, 330, [('schwere', 'l', 64, K('zur schweren', 1)), ('Panzer-Abteilung', 'b', 72, K('schweren Panzer-Abteilung', 1), {'box': 1})]).draw(c, t)
    b = Line(90, 440, [('502', 'o', 320, K('Panzer-Abteilung 502', 1), {'id': 'n'})]).draw(c, t)
    Line(990, 860, [('einen', 'l', 60, K('einen Tiger.')), ('Tiger.', 'h', 130, K('einen Tiger.', 1))], anchor='r').draw(c, t)
    if 'n' in b: pen_arrow(c, t, K('erhielt einen Tiger.'), (b['n'][2] - 20, b['n'][1] + 120), (780, 830), 0.3)
@scene(st(6), st(7), '1944')
def s7(c, t):
    card(c, t, T[6] - 0.05, ('smoke', 1.0), (110, 1000, 860, 620))
    Line(90, 330, [('7. April 1944', 'b', 78, K('Am 7. April', 1), {'box': 1})]).draw(c, t)
    Line(90, 450, [('zerstörte er', 'h', 150, K('zerstörte er'))]).draw(c, t)
    b = Line(90, 680, [('südlich von', 'l', 64, K('südlich von Pskow')), ('Pskow', 'b', 84, K('von Pskow zusammen', 1), {'id': 'p'})]).draw(c, t)
    if 'p' in b: pen_arrow(c, t, K('von Pskow zusammen', 1) + 0.2, (b['p'][2] + 10, b['p'][1] + 50), (b['p'][2] + 120, b['p'][3] + 170), -0.4)
@scene(st(7), st(8), '22')
def s8(c, t):
    card(c, t, T[7] - 0.05, ('tigburn', 1.0), (110, 1060, 860, 560))
    if t < K('15 davon selbst.'):
        Line(90, 330, [('mit einem', 'l', 64, K('mit einem zweiten')), ('zweiten Tiger', 'b', 78, K('einem zweiten Tiger', 1), {'box': 1})]).draw(c, t)
        Line(90, 440, [('22', 'h', 250, K('zweiten Tiger 22', 2))]).draw(c, t)
        Line(560, 560, [('sowjetische', 'b', 60, K('Tiger 22 sowjetische', 2))]).draw(c, t)
        Line(560, 650, [('Panzer', 'b', 60, K('sowjetische Panzer, 15', 1))]).draw(c, t)
    else:
        b = Line(90, 330, [('15', 'o', 360, K('15 davon selbst.'), {'id': 'n'})]).draw(c, t)
        Line(470, 520, [('davon', 'l', 72, K('15 davon selbst.', 1)), ('selbst.', 'h', 130, K('15 davon selbst.', 2))]).draw(c, t)
        if 'n' in b: pen_ellipse(c, t, K('15 davon selbst.', 2), b['n'])
@scene(st(8), st(9), 'RK')
def s9(c, t):
    card(c, t, T[8] - 0.05, 'a.jpg', (180, 760, 720, 860), fy=0.85, zoom=0.08)
    Line(90, 360, [('Dafür erhielt er das', 'l', 62, K('Dafür erhielt er'))]).draw(c, t)
    Line(90, 450, [('Ritterkreuz', 'h', 170, K('das Ritterkreuz.', 1))]).draw(c, t)
@scene(st(9), st(10), '1944')
def s10(c, t):
    card(c, t, T[9] - 0.05, 'b.jpg', (330, 900, 620, 760), fy=0.2)
    Line(90, 330, [('September 1944', 'b', 78, K('Im September 1944', 1), {'box': 1})]).draw(c, t)
    Line(90, 450, [('als', 'l', 64, K('als Leutnant')), ('Leutnant', 'b', 78, K('als Leutnant', 1))]).draw(c, t)
    b = Line(90, 580, [('das', 'l', 64, K('das Eichenlaub.')), ('Eichenlaub', 'h', 150, K('das Eichenlaub.', 1), {'id': 'e'})]).draw(c, t)
    if 'e' in b: pen_ellipse(c, t, K('das Eichenlaub.', 1) + 0.3, b['e'])
@scene(st(10), st(11), 'VII')
def s11(c, t):
    card(c, t, T[10] - 0.05, ('tigroad', 0.6), (110, 1180, 860, 460))
    Line(90, 330, [('Einen Monat zuvor', 'l', 64, K('Einen Monat zuvor'))]).draw(c, t)
    Line(90, 420, [('zum', 'l', 70, K('zum siebten Mal')), ('siebten Mal', 'h', 160, K('zum siebten Mal', 1))]).draw(c, t)
    b = Line(90, 650, [('verwundet', 'b', 84, K('Mal verwundet worden.', 1), {'id': 'v'})]).draw(c, t)
    ts = [K('zum siebten Mal', 1) + 0.12 * i for i in range(7)]; tally(c, t, ts, 740, 690)
@scene(st(11), st(12), 'FRONT')
def s12(c, t):
    card(c, t, T[11] - 0.05, ('snowtank', 0.7), (110, 1060, 860, 560))
    b = Line(90, 330, [('An die Front', 'b', 80, K('An die Front')), ('nicht mehr zurück', 'b', 80, K('nicht mehr zurück'), {'id': 'z'})]).draw(c, t) if False else None
    Line(90, 330, [('An die', 'l', 66, K('An die Front')), ('Front', 'h', 150, K('die Front kehrte', 1))]).draw(c, t)
    b = Line(90, 540, [('zurück', 'b', 84, K('mehr zurück und', 1), {'id': 'z'})]).draw(c, t)
    if 'z' in b: pen_strike(c, t, K('mehr zurück und', 1) + 0.15, (b['z'][0] - 10, (b['z'][1] + b['z'][3]) / 2 + 6), (b['z'][2] + 14, (b['z'][1] + b['z'][3]) / 2 - 4))
    Line(90, 680, [('bis Kriegsende', 'l', 62, K('bis Kriegsende'), {'box': 1})]).draw(c, t)
    Line(90, 780, [('Panzerunteroffiziere', 'b', 74, K('Kriegsende Panzerunteroffiziere', 1))]).draw(c, t)
@scene(st(12), st(13), '139')
def s13(c, t):
    card(c, t, T[12] - 0.05, ('tigroad', 1.0), (110, 1100, 860, 520), fx=0.5)
    Line(90, 330, [('rund', 'l', 66, K('rund 139'))]).draw(c, t)
    b = Line(90, 400, [('139', 'o', 360, K('rund 139', 1), {'id': 'n'})]).draw(c, t)
    Line(90, 800, [('abgeschossene', 'b', 70, K('abgeschossene Panzer')), ('Panzer', 'b', 70, K('abgeschossene Panzer', 1))]).draw(c, t)
    Line(90, 900, [('zugeschrieben', 'l', 60, K('Panzer zugeschrieben,', 1), {'col': MID})]).draw(c, t)
@scene(st(13), st(14), '?')
def s14(c, t):
    card(c, t, T[13] - 0.05, 'a.jpg', (240, 980, 600, 640), fy=0.25)
    Line(90, 330, [('die Angaben', 'l', 64, K('die Angaben schwanken')), ('schwanken', 'b', 84, K('Angaben schwanken', 1), {'box': 1})]).draw(c, t)
    b1 = Line(90, 500, [('89', 'o', 260, K('zwischen 89', 1), {'id': 'a'})]).draw(c, t)
    b2 = Line(990, 500, [('144', 'h', 260, K('und 144.', 1), {'id': 'b'})], anchor='r').draw(c, t)
    if 'a' in b1: pen_arrow(c, t, K('und 144.'), (b1['a'][2] + 20, b1['a'][1] + 140), (650, b1['a'][1] + 140), 0.15)
MONT = ['a.jpg', ('tigroad', 1), 'b.jpg', ('tanks697', 1), ('snowtank', 1), 'a.jpg', ('tigburn', 1), 'b.jpg']
@scene(st(14), T_END + 1, 'BÖLTER')
def s15(c, t):
    t0 = T[14]; k = int((t - t0) / 0.26)
    box = (200, 900, 680, 760)
    if k < len(MONT) - 1 and t < K('starb 1987'):
        src = MONT[k % len(MONT)]; x, y, bw, bh = box
        im = clip_frame(src[0], int((t - t0) * FPS)) if isinstance(src, tuple) else load(src)
        ph = grade(fit(im.convert('RGB'), bw, bh, 0.5, 0.25)).convert('RGBA')
        shl = Image.new('RGBA', shadow(bw, bh).size, (0, 0, 0, 0)); shl.putalpha(shadow(bw, bh)); c.alpha_composite(shl, (x - 62, y - 42))
        c.alpha_composite(ph, (x, y)); tape(c, x + 30, y + 8, 38); tape(c, x + bw - 30, y + 8, -38)
    else:
        card(c, t, K('starb 1987') - 0.05, 'a.jpg', box, fy=0.2)
    typewriter(c, t, t0, t0 + 0.7, 'Johannes Bölter', 110, 330, 'b', 84)
    Line(110, 450, [('starb', 'l', 66, K('starb 1987')), ('1987', 'h', 150, K('starb 1987', 1))]).draw(c, t)
    Line(990, 610, [('mit', 'l', 62, K('mit 72 Jahren.')), ('72 Jahren', 'b', 84, K('mit 72 Jahren.', 1), {'box': 1})], anchor='r').draw(c, t)

def frame(t):
    act = [s for s in S if s[0] <= t < s[1]]; sc = act[-1]
    t0, t1, wm, f = sc
    wa = eout((t - t0) / 0.4) * (1 - eout((t - (t1 - 0.25)) / 0.25))
    bg = background(t, wm, wa).convert('RGBA')
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); f(fg, t)
    z = 1.0 + 0.035 * clamp((t - t0) / max(1, t1 - t0))
    if abs(z - 1) > 0.002:
        cw, ch = W / z, H / z; fg = fg.resize((W, H), Image.BICUBIC, box=((W - cw) / 2, (H - ch) * 0.45, (W - cw) / 2 + cw, (H - ch) * 0.45 + ch))
    ex = (t - (t1 - 0.2)) / 0.2                                  # scene exit: a quick blur-out
    if 0 < ex < 1 and t1 < T_END:
        fg = fg.filter(ImageFilter.GaussianBlur(16 * ex)); fg.putalpha(fg.getchannel('A').point(lambda v: int(v * (1 - ex))))
    bg.alpha_composite(fg)
    if t > T_END - 0.6: bg = Image.blend(bg, Image.new('RGBA', (W, H), (40, 40, 42, 255)), clamp((t - T_END + 0.6) / 0.6) * 0.0)
    return bg.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'T': print(round(T_END, 3)); sys.exit()
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[3:]]; P = Image.new('RGB', (270 * len(ts), 480))
        for i, tt in enumerate(ts):
            im = frame(tt); ImageDraw.Draw(im).text((20, 20), '%.2f' % tt, font=font('b', 60), fill=(255, 0, 255)); P.paste(im.resize((270, 480)), (i * 270, 0))
        P.save(B + 'sh/' + sys.argv[2], quality=85); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
