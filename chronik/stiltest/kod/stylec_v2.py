# Style C test (reference c.mov, "newspaper"): old newsprint pages in layers (some out of focus), photos and film printed onto the paper
# through a ragged ink-brush mask that spreads open, typewriter titles that decode out of random letters, a small framed italic subtitle,
# a box icon and a dotted rule, a small bold year counter, a big serif paragraph; scenes change through a defocus; the camera keeps pushing in.
# Egon Mayer, first 17 s of the recorded voice, 9:16.
import sys, os, math, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance, ImageChops
C = os.path.dirname(os.path.abspath(__file__)) + '/'
EG = C + '../egon/'
sys.path.insert(0, EG + 'code')
import eg
from eg import W, H, FPS, ws, eio, eout, clamp, lerp
F = C + 'fonts/'
@functools.lru_cache(None)
def elite(s): return ImageFont.truetype(F + 'fontsource-special-elite-5.3.0/files/special-elite-latin-400-normal.woff', s)
@functools.lru_cache(None)
def oldst(s, b=False, it=False): return ImageFont.truetype(F + 'fontsource-old-standard-tt-5.3.0/files/old-standard-tt-latin-%s-%s.woff' % ('700' if b else '400', 'italic' if it else 'normal'), s)
@functools.lru_cache(None)
def courier(s, it=False): return ImageFont.truetype(F + 'fontsource-courier-prime-5.3.0/files/courier-prime-latin-400-%s.woff' % ('italic' if it else 'normal'), s)
INK = (34, 31, 28); PAPER = (238, 233, 220); CX = 540; MAXW = 720

# ---------- paper ----------
WORDS_DE = ('der die das und im am ein eine von mit auf für nach bei aus wurde wurden hatte über unter zwischen Bericht Woche Stadt Hafen '
            'Zeitung Ausgabe Montag Dienstag Mittwoch Donnerstag Freitag Wetter Regen Nebel Küste Flugplatz Meldung Leser Bürger Verkehr Markt Preise '
            'Brief Antwort Nachricht heute gestern morgen Abend Morgen Jahr Jahre Monat Seite Spalte Fortsetzung Anzeige Bahnhof Straße Rathaus Schule').split()
@functools.lru_cache(None)
def column_layer(seed, size, bold_heads, wd, ht, alpha):
    """columns of small newspaper type (neutral filler words), a few bold headlines"""
    rng = np.random.default_rng(seed); L = Image.new('L', (wd, ht), 0); d = ImageDraw.Draw(L); f = oldst(size); fh = oldst(int(size * 2.1), True)
    colw = int(size * 13); gap = int(size * 1.2); x = -int(size * 3)
    while x < wd:
        y = -int(size * 2)
        while y < ht:
            if bold_heads and rng.random() < 0.06:
                line = ' '.join(rng.choice(WORDS_DE, 3)).title(); d.text((x, y), line, font=fh, fill=int(255 * alpha)); y += int(size * 2.6); continue
            line = ''
            while f.getlength(line) < colw - size * 2: line += rng.choice(WORDS_DE) + ' '
            d.text((x, y), line.strip(), font=f, fill=int(255 * alpha * rng.uniform(0.7, 1.0))); y += int(size * 1.32)
        x += colw + gap
    return L
@functools.lru_cache(None)
def paper_base():
    rng = np.random.default_rng(3); n = rng.random((H // 24, W // 24)); n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W + 400, H + 400), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30)), np.float32) / 255
    a = np.array(PAPER, np.float32)[None, None] * (0.86 + 0.2 * n[..., None]); g = rng.normal(0, 7, a.shape[:2])[..., None]; a = np.clip(a + g, 0, 255)
    return Image.fromarray(a.astype(np.uint8))
GX, GY = 1300, 2050
PATH = [(0, 0), (1, 0), (1, 1), (0, 1)]
ANC = [(420 + p[0] * GX, 360 + p[1] * GY) for p in PATH]
WW, WH = 420 * 2 + GX + W + 200, 360 * 2 + GY + H + 200
@functools.lru_cache(None)
def world():
    cache = C + 'world.npz'
    if os.path.exists(cache):
        z = np.load(cache); return Image.fromarray(z['base']), Image.fromarray(z['far']), Image.fromarray(z['near'])
    rng = np.random.default_rng(3); n = rng.random((WH // 24, WW // 24)); n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((WW, WH), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30)), np.float32) / 255
    a = np.array(PAPER, np.float32)[None, None] * (0.86 + 0.2 * n[..., None]); a = np.clip(a + rng.normal(0, 7, a.shape[:2])[..., None], 0, 255)
    base = Image.fromarray(a.astype(np.uint8))
    far = column_layer(11, 34, True, WW, WH, 0.34).rotate(-1.2, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(3.6))
    near = column_layer(21, 24, False, WW, WH, 0.36).rotate(0.7, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8))
    np.savez(cache, base=np.asarray(base), far=np.asarray(far), near=np.asarray(near)); return base, far, near
def paper_at(cx, cy):
    """the page under the camera (top-left cx, cy); the far, out-of-focus layer moves slower (depth)"""
    base, far, near = world()
    pg = base.resize((W, H), Image.BICUBIC, box=(cx, cy, cx + W, cy + H))
    fx, fy = 420 + (cx - 420) * 0.7, 360 + (cy - 360) * 0.7
    for L, (x, y) in ((far, (fx, fy)), (near, (cx, cy))):
        Lc = L.resize((W, H), Image.BICUBIC, box=(x, y, x + W, y + H)); pg = Image.composite(Image.new('RGB', (W, H), INK), pg, Lc.point(lambda v: int(v * 0.8)))
    return Image.blend(pg, Image.new('RGB', (W, H), (246, 242, 232)), 0.18)
def paper(t, k):
    """three layers of newsprint at different depths; each scene shows another part of the page, the layers drift at different speeds"""
    base = paper_base().copy().convert('RGBA'); ox = 60 + 25 * t; oy = 80 + 12 * t
    pg = base.crop((int(ox) % 300, int(oy) % 300, int(ox) % 300 + W, int(oy) % 300 + H)).convert('RGB')
    for seed, size, heads, alpha, blur, speed, rot in ((11 + k, 34, True, 0.34, 3.6, 0.6, -1.5), (21 + k, 24, False, 0.36, 0.8, 1.0, 0.8)):
        Lr = column_layer(seed, size, heads, W + 500, H + 500, alpha)
        sx, sy = 120 + speed * 18 * t, 160 + speed * 9 * t
        Lc = Lr.rotate(rot, resample=Image.BICUBIC).resize((W, H), Image.BICUBIC, box=(sx, sy, sx + W, sy + H))
        if blur: Lc = Lc.filter(ImageFilter.GaussianBlur(blur))
        pg = Image.composite(Image.new('RGB', (W, H), INK), pg, Lc.point(lambda v: int(v * 0.8)))
    return Image.blend(pg, Image.new('RGB', (W, H), (246, 242, 232)), 0.18)

# ---------- ink-brush printed photo ----------
@functools.lru_cache(None)
def ink_noise(seed, w, h):
    rng = np.random.default_rng(seed)
    def octave(sc, ax=1.0):
        n = rng.random((max(2, int(h / sc)), max(2, int(w / sc / ax)))); return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    streak = octave(10, 6.0)   # dry-brush streaks, long sideways
    return 0.5 * octave(160) + 0.32 * octave(45) + 0.18 * streak
@functools.lru_cache(None)
def ink_field(seed, w, h):
    """signed distance-like field: 1 deep inside the box, 0 at the edge, plus noise"""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); dx = np.minimum(xx, w - 1 - xx) / (w * 0.5); dy = np.minimum(yy, h - 1 - yy) / (h * 0.5)
    return np.minimum(dx, dy) * 1.6 + (ink_noise(seed, w, h) - 0.5) * 0.75
def ink_mask(seed, w, h, k):
    """k 0..1: the ink spreads from the middle outwards"""
    th = lerp(1.6, 0.16, eout(k)); a = np.clip((ink_field(seed, w, h) - th) / 0.2, 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5))
def printed(pg, im, box, t, t0, seed, colour=True):
    """photo printed onto the newsprint: sepia-grey, multiplied with the paper so the page shows through the lights, ragged ink edges"""
    pg = pg.convert('RGB')
    x0, y0, x1, y1 = [int(round(v)) for v in box]; w, h = x1 - x0, y1 - y0
    if t < t0 or x1 <= 0 or y1 <= 0 or x0 >= W or y0 >= H: return pg
    k = (t - t0) / 1.0; z = 1.0 + 0.10 * (1 - eout(clamp(k / 1.6))) + 0.006 * max(0.0, t - t0)   # arrives a little big, settles, keeps pushing in slowly
    s = max(w / im.width, h / im.height) * z; im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    im = im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
    if colour:   # the colour stays, muted, so it still reads as printed on newsprint
        im = ImageEnhance.Color(ImageOps.autocontrast(im, cutoff=1.0)).enhance(0.72); ph = np.asarray(im, np.float32)
        ph = 255 * (0.06 + 0.94 * (ph / 255) ** 0.9) * np.array((1.0, 0.97, 0.92), np.float32)
    else:
        g = np.asarray(ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1.5), np.float32) / 255
        ph = 255 * (0.07 + 0.93 * g[..., None] ** 0.85) * np.array((1.0, 0.96, 0.88), np.float32)
    cx0, cy0, cx1, cy1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    region = np.asarray(pg.crop((cx0, cy0, cx1, cy1)), np.float32); ph = ph[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0]
    mult = region * ph / 255 * 1.14
    m = np.asarray(ink_mask(seed, w, h, k), np.float32)[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0, None] / 255
    out = region * (1 - m) + np.clip(mult, 0, 255) * m
    pg = pg.copy(); pg.paste(Image.fromarray(out.astype(np.uint8)), (cx0, cy0)); return pg

# ---------- type ----------
GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def decode(s, t, t0, per=0.07, lead=0.35):
    """typewriter title decoding out of random letters, left to right"""
    out = []; rng = np.random.default_rng(int(t * 15))
    for i, ch in enumerate(s):
        ti = t0 + lead + i * per
        if t < t0 + i * per * 0.5: out.append(' ')
        elif t < ti and ch != ' ': out.append(GLYPHS[rng.integers(len(GLYPHS))])
        else: out.append(ch)
    return ''.join(out)
def fitsize(s, font_fn, size, maxw=MAXW):
    while font_fn(size).getlength(s) > maxw and size > 20: size -= 2
    return size
def text_c(d, s, y, font, fill, anchor='mm'): d.text((CX + OFF[0], y + OFF[1]), s, font=font, fill=fill, anchor=anchor)
OFF = [0, 0]
def title_block(img, t, title, t0, sub=None, t_sub=None, year=None, y=1240):
    d = ImageDraw.Draw(img); sz = fitsize(title, elite, 100); f = elite(sz); ox, oy = OFF
    if t >= t0:
        s = decode(title, t, t0); text_c(d, s, y, f, INK + (255,))
        tw = f.getlength(title); bx, by = CX - tw / 2 - 46 + ox, y - sz * 0.55 + oy   # the small box icon
        a = int(255 * clamp((t - t0) / 0.3)); d.rectangle((bx - 15, by - 15, bx + 15, by + 15), outline=INK + (a,), width=3); d.line((bx - 15, by - 15, bx + 15, by + 15), fill=INK + (a,), width=3); d.line((bx - 15, by + 15, bx + 15, by - 15), fill=INK + (a,), width=3)
    if sub and t >= t_sub:   # framed italic subtitle, the frame draws itself
        k = eout((t - t_sub) / 0.5); fs = courier(40, True); sw = fs.getlength(sub) + 50; x0, y0, x1, y1 = CX - sw / 2 + ox, y + 62 + oy, CX + sw / 2 + ox, y + 118 + oy
        per = 2 * (sw + 56) * k; pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]; left = per
        for (ax, ay), (bx_, by_) in zip(pts, pts[1:]):
            L = math.hypot(bx_ - ax, by_ - ay); u = clamp(left / L); d.line((ax, ay, lerp(ax, bx_, u), lerp(ay, by_, u)), fill=INK + (255,), width=3); left -= L
            if left <= 0: break
        d.text((CX, (y0 + y1) / 2), sub, font=fs, fill=(90, 84, 76, int(255 * clamp((t - t_sub - 0.25) / 0.4))), anchor='mm')
    if year or sub:   # dotted rule, the year counter in its middle
        t_r = min([v for v in (t_sub, year[1] if year else None) if v is not None])
        n = int(clamp((t - t_r) / 0.6) * 12)
        for i in range(n):
            for sg in (-1, 1): xx = CX + ox + sg * (80 + i * 26); d.ellipse((xx - 4, y + 156 + oy, xx + 4, y + 164 + oy), fill=INK + (200,))
    if year:
        ys, ty = year; s_ = ys(t) if callable(ys) else ys
        if s_ and t >= ty: d.text((CX + ox, y + 160 + oy), s_, font=oldst(46, True), fill=INK + (int(255 * clamp((t - ty) / 0.3)),), anchor='mm')
def paragraph(img, t, lines, y=1470, size=52):
    """the big serif paragraph, words fading in with the voice"""
    d = ImageDraw.Draw(img); f = oldst(fitsize(max((' '.join(w for w, _ in l) for l in lines), key=len), oldst, size))
    for li, l in enumerate(lines):
        sp = f.getlength(' '); tot = sum(f.getlength(w) for w, _ in l) + sp * (len(l) - 1); x = CX - tot / 2 + OFF[0]
        for w, t0 in l:
            a = clamp((t - t0) / 0.35)
            if a > 0: d.text((x, y + li * size * 1.16 + OFF[1]), w, font=f, fill=INK + (int(235 * a),), anchor='lm')
            x += f.getlength(w) + sp

# ---------- scenes ----------
B1, B2, B3 = ws('Egon'), ws('Er'), ws('Ab', 12)
TEND = eg.WORDS[[w for w, a, b in eg.WORDS].index('„Richthofen“.')][2] + 1.3
BOX = (-30, 140, 1110, 1120)
def bx(ox, oy): return (BOX[0] + ox, BOX[1] + oy, BOX[2] + ox, BOX[3] + oy)
def s0(pg, t, ox, oy):
    pg = printed(pg, eg.film('form', t + 0.5).convert('RGB'), bx(ox, oy), t, -0.6, 5).convert('RGBA')
    title_block(pg, t, 'Abwehrfeuer', ws('Bomber'), 'von hinten', ws('hinten'))
    paragraph(pg, t, [[('Wer', ws('Wer')), ('amerikanische', ws('amerikanische')), ('Bomber', ws('Bomber'))], [('von', ws('von')), ('hinten', ws('hinten')), ('angriff,', ws('angriff')), ('flog', ws('flog'))],
                      [('direkt', ws('direkt')), ('in', ws('in')), ('ihr', ws('ihr')), ('Abwehrfeuer.', ws('Abwehrfeuer'))]], 1452)
    return pg
def s1(pg, t, ox, oy):
    pg = printed(pg, eg.src('16').crop((0, 120, 1696, 1600)), bx(ox, oy), t, B1 - 0.3, 6).convert('RGBA')
    title_block(pg, t, 'Egon Mayer', ws('Egon'), 'Jagdflieger', ws('griff'))
    paragraph(pg, t, [[('Egon', ws('Egon')), ('Mayer', ws('Mayer')), ('griff', ws('griff')), ('sie', ws('sie', 5))], [('deshalb', ws('deshalb')), ('von', ws('von', 5.5)), ('vorne', ws('vorne')), ('an.', ws('an', 6))]], 1470)
    return pg
def yr2(t):
    if t < ws('1937'): return '1917'
    u = clamp((t - ws('1937')) / 0.7); return str(int(round(lerp(1917, 1937, eio(u)))))
def s2(pg, t, ox, oy):
    pg = printed(pg, eg.src('19'), bx(ox, oy), t, B2 - 0.3, 7).convert('RGBA')
    title_block(pg, t, 'Konstanz', ws('Konstanz') - 0.3, 'Luftwaffe', ws('Luftwaffe'), (yr2, ws('1917')))
    paragraph(pg, t, [[('Er', ws('Er')), ('wurde', ws('wurde', 6.9)), ('1917', ws('1917')), ('in', ws('in', 8)), ('Konstanz', ws('Konstanz'))], [('geboren', ws('geboren')), ('und', ws('und', 9.4)), ('ging', ws('ging')), ('1937', ws('1937'))],
                      [('zur', ws('zur')), ('Luftwaffe.', ws('Luftwaffe'))]], 1452)
    return pg
def s3(pg, t, ox, oy):
    pg = printed(pg, eg.src('24'), bx(ox, oy), t, B3 - 0.3, 8).convert('RGBA')
    title_block(pg, t, 'Jagdgeschwader 2', ws('Jagdgeschwader') - 0.3, '„Richthofen“', ws('„Richthofen'), ('1939', ws('1939')))
    paragraph(pg, t, [[('Ab', ws('Ab', 12)), ('Dezember', ws('Dezember')), ('1939', ws('1939'))], [('flog', ws('flog', 14)), ('er', ws('er', 14.5)), ('im', ws('im', 14.7))], [('Jagdgeschwader', ws('Jagdgeschwader')), ('2', ws('2', 15.5)), ('„Richthofen“.', ws('„Richthofen'))]], 1452)
    return pg
SC = [(0.0, s0), (B1, s1), (B2, s2), (B3, s3)]
PRE, POST = 0.3, 1.0
def campos(t):
    k = max(i for i, (a, _) in enumerate(SC) if a <= t)
    if k + 1 < len(SC) and t >= SC[k + 1][0] - PRE: k += 1
    b = SC[k][0]
    if k == 0 or t >= b + POST: return ANC[k], (0.0, 0.0), k, None
    f = lambda tt: eio(clamp((tt - (b - PRE)) / (PRE + POST))); u, u2 = f(t), f(t + 1 / FPS); (ax, ay), (bx_, by_) = ANC[k - 1], ANC[k]
    return (lerp(ax, bx_, u), lerp(ay, by_, u)), ((bx_ - ax) * (u2 - u), (by_ - ay) * (u2 - u)), k, u
def dblur(img, vx, vy):
    L = math.hypot(vx, vy) * 0.8
    if L < 2: return img
    a = np.asarray(img.convert('RGB'), np.float32); n = 9; pd = int(L / 2) + 2; ap = np.pad(a, ((pd, pd), (pd, pd), (0, 0)), mode='edge'); acc = np.zeros_like(a)
    for i in range(n):
        f = (i - (n - 1) / 2) / (n - 1); dx, dy = int(round(vx / math.hypot(vx, vy) * L * f)), int(round(vy / math.hypot(vx, vy) * L * f))
        acc += ap[pd + dy:pd + dy + H, pd + dx:pd + dx + W]
    return Image.fromarray((acc / n).astype(np.uint8))
def vign(img):
    a = np.asarray(img.convert('RGB'), np.float32); yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * 0.72)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    a *= (1 - 0.34 * np.clip(r - 0.4, 0, 1) ** 1.4)[..., None]; return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def frame(t):
    (cx, cy), (vx, vy), k, u = campos(t)
    pg = paper_at(cx, cy)
    for j in range(max(0, k - 1), min(len(SC), k + 2)):   # the scenes lie on the same page; the camera sees the next one coming
        OFF[0], OFF[1] = ANC[j][0] - cx, ANC[j][1] - cy
        if abs(OFF[0]) > W + 200 or abs(OFF[1]) > H + 200: continue
        pg = SC[j][1](pg, t, OFF[0], OFF[1])
    img = pg.convert('RGB')
    if u is not None:   # the move: motion blur and a light defocus in the middle of it
        img = dblur(img, vx, vy); bl = 5 * math.sin(math.pi * u)
        if bl > 0.5: img = img.filter(ImageFilter.GaussianBlur(bl))
    a0 = SC[k][0] + (POST if k > 0 else 0); z = 1.0 + 0.010 * max(0.0, t - a0)   # the slow push-in
    if z > 1.0005:
        bw, bh = W / z, H / z; img = img.resize((W, H), Image.BICUBIC, box=(CX - bw / 2, 960 - bh / 2, CX + bw / 2, 960 + bh / 2))
    img = vign(img)
    if t > TEND - 0.6: img = Image.blend(img, Image.new('RGB', (W, H), (0, 0, 0)), eio((t - (TEND - 0.6)) / 0.6))
    return eg.finish(img.convert('RGBA'), t)
if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); P_ = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = frame(t).convert('RGBA'); d = ImageDraw.Draw(f)
            if os.environ.get('UI'):
                d.rectangle((0, 0, W, 290), outline=(0, 255, 255, 255), width=4); d.rectangle((930, 680, W, 1580), outline=(0, 255, 255, 255), width=4); d.rectangle((0, 1580, W, H), outline=(0, 255, 255, 255), width=4)
            d.text((10, 300), '%.2f' % t, fill=(255, 0, 255, 255)); P_.paste(f.convert('RGB').resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P_.save(C + sys.argv[2], quality=85); sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', C + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(np.asarray(frame(n / FPS).convert('RGB')).tobytes())
        if n % 30 == 0: print('t', n / FPS, flush=True)
    p.stdin.close(); p.wait(); print('rc', p.returncode)
