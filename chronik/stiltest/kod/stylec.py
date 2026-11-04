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
def printed(pg, im, box, t, t0, seed):
    """photo printed onto the newsprint: sepia-grey, multiplied with the paper so the page shows through the lights, ragged ink edges"""
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    if t < t0: return pg
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    im = im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1.5); g = np.asarray(g, np.float32) / 255; g = np.clip((g - 0.5) * 1.1 + 0.5, 0, 1)
    tint = np.array((1.0, 0.96, 0.88), np.float32); ph = 255 * (0.07 + 0.93 * g[..., None] ** 0.85) * tint
    region = np.asarray(pg.crop(box), np.float32); mult = region * ph / 255 * 1.16
    m = np.asarray(ink_mask(seed, w, h, (t - t0) / 0.9), np.float32)[..., None] / 255
    out = region * (1 - m) + np.clip(mult, 0, 255) * m
    pg = pg.copy(); pg.paste(Image.fromarray(out.astype(np.uint8)), (x0, y0)); return pg

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
def text_c(d, s, y, font, fill, anchor='mm'): d.text((CX, y), s, font=font, fill=fill, anchor=anchor)
def title_block(img, t, title, t0, sub=None, t_sub=None, year=None, y=1185):
    d = ImageDraw.Draw(img); sz = fitsize(title, elite, 100); f = elite(sz)
    if t >= t0:
        s = decode(title, t, t0); text_c(d, s, y, f, INK + (255,))
        tw = f.getlength(title); bx, by = CX - tw / 2 - 46, y - sz * 0.55   # the small box icon
        a = int(255 * clamp((t - t0) / 0.3)); d.rectangle((bx - 15, by - 15, bx + 15, by + 15), outline=INK + (a,), width=3); d.line((bx - 15, by - 15, bx + 15, by + 15), fill=INK + (a,), width=3); d.line((bx - 15, by + 15, bx + 15, by - 15), fill=INK + (a,), width=3)
    if sub and t >= t_sub:   # framed italic subtitle, the frame draws itself
        k = eout((t - t_sub) / 0.5); fs = courier(40, True); sw = fs.getlength(sub) + 50; x0, y0, x1, y1 = CX - sw / 2, y + 62, CX + sw / 2, y + 118
        per = 2 * (sw + 56) * k; pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]; left = per
        for (ax, ay), (bx_, by_) in zip(pts, pts[1:]):
            L = math.hypot(bx_ - ax, by_ - ay); u = clamp(left / L); d.line((ax, ay, lerp(ax, bx_, u), lerp(ay, by_, u)), fill=INK + (255,), width=3); left -= L
            if left <= 0: break
        d.text((CX, (y0 + y1) / 2), sub, font=fs, fill=(90, 84, 76, int(255 * clamp((t - t_sub - 0.25) / 0.4))), anchor='mm')
        n = int(clamp((t - t_sub - 0.2) / 0.6) * 28)   # dotted rule
        for i in range(n): d.ellipse((CX - 27 * 14 + i * 28 - 4, y1 + 34, CX - 27 * 14 + i * 28 + 4, y1 + 42), fill=INK + (200,))
    if year:
        ys, ty = year; s_ = ys(t) if callable(ys) else ys
        if s_ and t >= ty: d.text((CX, y - 120), s_, font=oldst(46, True), fill=INK + (int(255 * clamp((t - ty) / 0.3)),), anchor='mm')
def paragraph(img, t, lines, y=1470, size=58):
    """the big serif paragraph, words fading in with the voice"""
    d = ImageDraw.Draw(img); f = oldst(fitsize(max((' '.join(w for w, _ in l) for l in lines), key=len), oldst, size))
    for li, l in enumerate(lines):
        sp = f.getlength(' '); tot = sum(f.getlength(w) for w, _ in l) + sp * (len(l) - 1); x = CX - tot / 2
        for w, t0 in l:
            a = clamp((t - t0) / 0.35)
            if a > 0: d.text((x, y + li * size * 1.18), w, font=f, fill=INK + (int(235 * a),), anchor='lm')
            x += f.getlength(w) + sp

# ---------- scenes ----------
B1, B2, B3 = ws('Egon'), ws('Er'), ws('Ab', 12)
TEND = eg.WORDS[[w for w, a, b in eg.WORDS].index('„Richthofen“.')][2] + 1.3
BOX = (60, 230, 1020, 1030)
def s0(t, k):
    pg = paper(t, k); pg = printed(pg, eg.film('form', t + 0.5).convert('RGB'), BOX, t, 0.0, 5).convert('RGBA')
    title_block(pg, t, 'Abwehrfeuer', ws('Bomber'), 'von hinten', ws('hinten'))
    paragraph(pg, t, [[('Wer', ws('Wer')), ('amerikanische', ws('amerikanische')), ('Bomber', ws('Bomber'))], [('von', ws('von')), ('hinten', ws('hinten')), ('angriff,', ws('angriff')), ('flog', ws('flog'))],
                      [('direkt', ws('direkt')), ('in', ws('in')), ('ihr', ws('ihr')), ('Abwehrfeuer.', ws('Abwehrfeuer'))]], 1440)
    return pg
def s1(t, k):
    pg = paper(t, k); pg = printed(pg, eg.src('16').crop((0, 0, 1696, 2000)), BOX, t, B1 - 0.2, 6).convert('RGBA')
    title_block(pg, t, 'Egon Mayer', ws('Egon'), 'Jagdflieger', ws('griff'))
    paragraph(pg, t, [[('Egon', ws('Egon')), ('Mayer', ws('Mayer')), ('griff', ws('griff')), ('sie', ws('sie', 5))], [('deshalb', ws('deshalb')), ('von', ws('von', 5.5)), ('vorne', ws('vorne')), ('an.', ws('an', 6))]], 1470)
    return pg
def yr2(t):
    if t < ws('1937'): return '1917'
    u = clamp((t - ws('1937')) / 0.7); return str(int(round(lerp(1917, 1937, eio(u)))))
def s2(t, k):
    pg = paper(t, k); pg = printed(pg, eg.src('19'), BOX, t, B2 - 0.2, 7).convert('RGBA')
    title_block(pg, t, 'Konstanz', ws('Konstanz') - 0.3, 'Luftwaffe', ws('Luftwaffe'), (yr2, ws('1917')))
    paragraph(pg, t, [[('Er', ws('Er')), ('wurde', ws('wurde', 6.9)), ('1917', ws('1917')), ('in', ws('in', 8)), ('Konstanz', ws('Konstanz'))], [('geboren', ws('geboren')), ('und', ws('und', 9.4)), ('ging', ws('ging')), ('1937', ws('1937'))],
                      [('zur', ws('zur')), ('Luftwaffe.', ws('Luftwaffe'))]], 1440)
    return pg
def s3(t, k):
    pg = paper(t, k); pg = printed(pg, eg.src('24'), BOX, t, B3 - 0.2, 8).convert('RGBA')
    title_block(pg, t, 'Jagdgeschwader 2', ws('Jagdgeschwader') - 0.3, '„Richthofen“', ws('„Richthofen'), ('1939', ws('1939')))
    paragraph(pg, t, [[('Ab', ws('Ab', 12)), ('Dezember', ws('Dezember')), ('1939', ws('1939'))], [('flog', ws('flog', 14)), ('er', ws('er', 14.5)), ('im', ws('im', 14.7))], [('Jagdgeschwader', ws('Jagdgeschwader')), ('2', ws('2', 15.5)), ('„Richthofen“.', ws('„Richthofen'))]], 1440)
    return pg
SC = [(0.0, s0), (B1, s1), (B2, s2), (B3, s3)]
def cam(img, t, a):
    """the slow push-in of the reference"""
    d_ = max(0.0, t - a) + 0.4; z = 1.0 + 0.012 * d_; bw, bh = W / z, H / z
    return img.resize((W, H), Image.BICUBIC, box=(CX - bw / 2, 960 - bh / 2 + 4 * d_, CX + bw / 2, 960 + bh / 2 + 4 * d_))
def scene(i, t): a, fn = SC[i]; return cam(fn(t, i), t, a)
def vign(img):
    a = np.asarray(img.convert('RGB'), np.float32); yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * 0.72)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    a *= (1 - 0.34 * np.clip(r - 0.4, 0, 1) ** 1.4)[..., None]; return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
D0, D1 = 0.35, 0.4
def frame(t):
    i = max(j for j, (a, _) in enumerate(SC) if a <= t)
    for j in (i, i + 1):
        if 0 < j < len(SC) and SC[j][0] - D0 <= t < SC[j][0] + D1:   # defocus into the next scene
            b = SC[j][0]; u = (t - (b - D0)) / (D0 + D1)
            A_ = scene(j - 1, t).filter(ImageFilter.GaussianBlur(26 * eio(clamp(u * 1.6))))
            B_ = scene(j, t).filter(ImageFilter.GaussianBlur(26 * (1 - eio(clamp((u - 0.35) / 0.65)))))
            img = Image.blend(A_.convert('RGB'), B_.convert('RGB'), eio(clamp((u - 0.25) / 0.5))); break
    else: img = scene(i, t)
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
