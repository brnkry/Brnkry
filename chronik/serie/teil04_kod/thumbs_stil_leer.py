# Teil 4 thumbnails in four reference styles (Power of Politics / Alexander 1917 / Three Emperors 1888 / Berlin Wall)
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops, ImageOps
D = os.path.dirname(os.path.abspath(__file__)) + '/'; S = D + 'd/'; O = D + 'out/'; F = '/tmp/claude-0/fonts/'
TW, TH = 1280, 720
PEOPLE = False
RED, DARK, YEL, WHITE = (178, 22, 26), (52, 52, 54), (244, 196, 48), (250, 250, 248)
def font(n, s): return ImageFont.truetype(F + n + '.ttf', s)
def rng(k=1): return np.random.default_rng(k)
def noise(w, h, amp, k=1, blur=0.8):
    n = (rng(k).random((h, w)) * 255).astype(np.uint8); im = Image.fromarray(n).filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(im, np.float32) / 255 - 0.5
def cover(path, w, h, fx=0.5, fy=0.5, z=1.0):
    g = Image.open(path).convert('RGB'); sc = max(w / g.width, h / g.height) * z; cw, ch = w / sc, h / sc
    return g.resize((w, h), Image.LANCZOS, box=((g.width - cw) * fx, (g.height - ch) * fy, (g.width - cw) * fx + cw, (g.height - ch) * fy + ch))
def cut(name, h=None, w=None):
    im = Image.open(S + name + '_cut.png').convert('RGBA')
    if h: im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    if w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    return im
def shadow_paste(can, im, xy, blur=18, a=0.6, off=(10, 14)):
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * a)))
    can.alpha_composite(sh, (xy[0] + off[0], xy[1] + off[1])); can.alpha_composite(im, xy)
def outline(im, wd=5, col=(255, 255, 255)):
    a = im.getchannel('A'); ring = a.filter(ImageFilter.MaxFilter(wd * 2 + 1))
    base = Image.new('RGBA', im.size, col + (0,)); base.putalpha(ring); base.alpha_composite(im); return base
def text(can, xy, s, f, col, anchor='la', stroke=0, sc=None, shadow=0):
    d = ImageDraw.Draw(can)
    if shadow:
        L = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(L).text(xy, s, font=f, fill=(0, 0, 0, 200), anchor=anchor); can.alpha_composite(L.filter(ImageFilter.GaussianBlur(shadow)), (4, 6))
    d.text(xy, s, font=f, fill=col, anchor=anchor, stroke_width=stroke, stroke_fill=sc); return d.textbbox(xy, s, font=f, anchor=anchor)
def fit_font(n, s, maxw, size):
    f = font(n, size)
    while f.getlength(s) > maxw: size -= 2; f = font(n, size)
    return f
def logo(can, x=1132, y=26, dark=False):
    d = ImageDraw.Draw(can); f = font('Oswald', 40)
    d.rounded_rectangle((x - 10, y - 6, x + 106, y + 52), 6, fill=(8, 9, 11, 220)); d.text((x, y + 23), 'C', font=f, fill=WHITE, anchor='lm')
    b = d.textbbox((x + 30, y + 23), 'DM', font=f, anchor='lm'); d.rectangle((b[0] - 4, b[1] - 4, b[2] + 4, b[3] + 4), fill=YEL); d.text((x + 30, y + 23), 'DM', font=f, fill=(20, 20, 20), anchor='lm')
def badge(can, x, y, s='TEIL 4'):
    d = ImageDraw.Draw(can); f = font('Oswald', 46); b = d.textbbox((x, y), s, font=f)
    d.rectangle((b[0] - 14, b[1] - 9, b[2] + 14, b[3] + 9), fill=RED); d.text((x, y), s, font=f, fill=WHITE)
def halftone(im, cell=6):
    g = ImageOps.grayscale(im); w, h = g.size; small = g.resize((w // cell, h // cell), Image.BILINEAR); a = np.asarray(small, np.float32) / 255
    out = Image.new('L', (w, h), 255); d = ImageDraw.Draw(out)
    for j in range(a.shape[0]):
        for i in range(a.shape[1]):
            r = (1 - a[j, i]) * cell * 0.72
            if r > 0.4: cx, cy = i * cell + cell / 2, j * cell + cell / 2; d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=0)
    return out
def splatter(can, k, n, box, col=RED):
    r = rng(k); d = ImageDraw.Draw(can)
    for _ in range(n):
        x, y = r.uniform(box[0], box[2]), r.uniform(box[1], box[3]); s = r.choice([2, 3, 4, 6, 9]); d.ellipse((x - s, y - s, x + s, y + s), fill=col + (230,))
def skyline_mask(w, h):
    """a London roofline with St Paul's dome as a flat silhouette mask"""
    m = Image.new('L', (w, h), 0); d = ImageDraw.Draw(m); r = rng(5); x = 0
    while x < w:
        bw = r.integers(30, 90); bh = r.integers(int(h * 0.25), int(h * 0.6)); d.rectangle((x, h - bh, x + bw, h), fill=255)
        if r.random() < 0.3: d.rectangle((x + bw // 2 - 4, h - bh - r.integers(20, 60), x + bw // 2 + 4, h - bh), fill=255)
        x += bw
    cx = int(w * 0.62); base = int(h * 0.38)   # St Paul's
    d.rectangle((cx - 110, base, cx + 110, h), fill=255); d.rectangle((cx - 70, base - 50, cx + 70, base), fill=255)
    d.pieslice((cx - 70, base - 125, cx + 70, base + 15), 180, 360, fill=255); d.rectangle((cx - 9, base - 175, cx + 9, base - 110), fill=255)
    d.polygon([(cx, base - 205), (cx - 10, base - 175), (cx + 10, base - 175)], fill=255)
    for tx in (cx - 150, cx + 150): d.rectangle((tx - 18, base - 30, tx + 18, h), fill=255); d.polygon([(tx - 18, base - 30), (tx, base - 90), (tx + 18, base - 30)], fill=255)
    return m

# ================= A: "The Power of Politics" =================
def thumb_A():
    bg = np.ones((TH, TW, 3), np.float32) * np.array([232, 220, 196], np.float32); bg += noise(TW, TH, 1, 2, 1.2)[..., None] * 26
    can = Image.fromarray(bg.clip(0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(can)
    # faint aerial of London bottom left (like the faint Colosseum)
    ae = ImageOps.grayscale(cover(S + 'wapping.jpg', 520, 360, 0.5, 0.6)).point(lambda v: int(v * 0.6 + 90))
    ae_rgba = Image.new('RGBA', ae.size, (150, 130, 100, 0)); ae_rgba.putalpha(ImageOps.invert(ae).point(lambda v: int(v * 0.32))); can.alpha_composite(ae_rgba, (0, 360))
    for x in range(40, 640, 22): d.line((x, 150, x, 600), fill=(196, 186, 166, 255), width=1)       # graph paper
    for y in range(150, 600, 22): d.line((40, y, 640, y), fill=(196, 186, 166, 255), width=1)
    # orange panel with the He 111 over Wapping in duotone
    pw, ph = 330, 430; P = ImageOps.grayscale(cover(S + 'wapping.jpg', pw, ph, 0.25, 0.25, 1.6)); P = ImageOps.autocontrast(P)
    duo = ImageOps.colorize(P, (150, 40, 0), (255, 196, 70)).convert('RGBA'); can.alpha_composite(duo, (870, 40))
    # the Spitfire cut-out in the panel corner
    sp = cut('spitfire_air', w=230); sp = ImageOps.grayscale(sp.convert('RGB')).convert('RGBA'); sp.putalpha(cut('spitfire_air', w=230).getchannel('A'))
    shadow_paste(can, sp, (1010, 330), 8, 0.5, (5, 8))
    # Churchill as an engraving: high contrast grey, his dark suit in red, white sticker outline
    ch = cut('churchill_c', h=640); g = ImageEnhance.Contrast(ImageOps.grayscale(ch.convert('RGB'))).enhance(1.5).filter(ImageFilter.UnsharpMask(2, 120, 2))
    ga = np.asarray(g, np.float32); hh = ga.shape[0]; yy = np.arange(hh)[:, None] / hh
    dark = np.clip((150 - ga) / 50, 0, 1) * np.clip((yy - 0.36) / 0.06, 0, 1)
    dark = np.asarray(Image.fromarray((dark * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), np.float32) / 255
    rgb = np.stack([ga, ga, ga], -1); red = np.stack([ga * 0.65 + 118, ga * 0.18 + 16, ga * 0.18 + 18], -1)
    rgb = rgb * (1 - dark[..., None]) + red * dark[..., None]
    chc = Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).convert('RGBA'); chc.putalpha(ch.getchannel('A')); chc = outline(chc, 5)
    shadow_paste(can, chc, (640, TH - chc.height + 40), 16, 0.45)
    # halftone London skyline across the bottom
    sk = skyline_mask(900, 200); dots = Image.new('L', (900, 200), 205); dd_ = ImageDraw.Draw(dots)
    for j in range(0, 200, 6):
        for i in range(0, 900, 6):
            rr = 1.0 + 1.6 * (j / 200); dd_.ellipse((i + 3 - rr, j + 3 - rr, i + 3 + rr, j + 3 + rr), fill=95)
    ht = Image.blend(Image.new('L', (900, 200), 150), dots, 0.75)
    sk = sk.resize((900, 200)); ht = ht.resize((900, 200))
    lay = Image.merge('RGBA', (ht, ht, ht, sk)); can.alpha_composite(lay, (380, TH - 190))
    # title in two colours, condensed heavy
    f1 = fit_font('Anton', 'LUFTSCHLACHT', 590, 130); f2 = fit_font('Anton', 'UM ENGLAND', 590, 150)
    b = text(can, (52, 225), 'LUFT', f1, RED); text(can, (b[2] + 4, 225), 'SCHLACHT', f1, DARK)
    b = text(can, (52, 395), 'UM', f2, DARK); text(can, (b[2] + 22, 395), 'ENGLAND', f2, RED)
    splatter(can, 4, 14, (60, 560, 640, 700)); splatter(can, 7, 6, (560, 120, 700, 200))
    logo(can, 40, 30); badge(can, 52, 640)
    return can
# ================= B: "Alexander 1917" =================
def thumb_B():
    sky = cover(S + 'spitfire_air.jpg', TW, TH, 0.5, 0.2, 1.0).filter(ImageFilter.GaussianBlur(1.5)); sky = ImageEnhance.Color(sky).enhance(0.25); sky = ImageEnhance.Brightness(sky).enhance(1.15)
    can = sky.convert('RGBA'); can.alpha_composite(Image.new('RGBA', (TW, TH), (235, 238, 240, 110)))
    # giant year, filled with the burning docks, steel-blue and half transparent
    f = font('Anton', 480); M = Image.new('L', (TW, TH), 0); ImageDraw.Draw(M).text((TW / 2, 475), '1940', font=f, fill=255, anchor='mm')
    fill = ImageOps.colorize(ImageOps.grayscale(cover(S + 'london_fire.jpg', TW, TH, 0.5, 0.5)), (40, 60, 72), (190, 205, 212)).convert('RGBA')
    fill.putalpha(M.point(lambda v: int(v * 0.78))); can.alpha_composite(fill)
    # foreground: the firemen in warm, painterly colour, rising from the bottom
    k5 = cut('k5_feuerwehr', h=470); g = np.asarray(ImageOps.grayscale(k5.convert('RGB')), np.float32)
    warm = np.stack([g * 1.05 + 18, g * 0.92 + 8, g * 0.75], -1).clip(0, 255).astype(np.uint8); k5w = Image.fromarray(warm).convert('RGBA'); k5w.putalpha(k5.getchannel('A'))
    k5w = k5w.filter(ImageFilter.UnsharpMask(2, 90, 2))
    if PEOPLE: shadow_paste(can, k5w, ((TW - k5w.width) // 2 + 40, TH - k5w.height + 10), 20, 0.6)
    # red smoke glow at the bottom like the flags
    gl = np.zeros((TH, TW), np.float32); yy = np.arange(TH)[:, None] / TH; gl += np.clip((yy - 0.7) / 0.3, 0, 1) * 0.55
    glow = Image.new('RGBA', (TW, TH), (170, 30, 20, 0)); glow.putalpha(Image.fromarray((gl * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30))); can.alpha_composite(glow)
    text(can, (TW / 2, 60), 'LUFTSCHLACHT', font('Anton', 92), RED, 'mt', shadow=6)
    text(can, (TW / 2, 160), 'UM ENGLAND', font('Anton', 84), (30, 30, 32), 'mt', shadow=4)
    logo(can); badge(can, 36, 28)
    return can
# ================= C: "The Three Emperors 1888" =================
def thumb_C():
    base = np.ones((TH, TW, 3), np.float32) * 38; base += noise(TW, TH, 1, 3, 2.5)[..., None] * 34 + noise(TW, TH, 1, 9, 0.7)[..., None] * 16
    can = Image.fromarray(base.clip(0, 255).astype(np.uint8)).convert('RGBA')
    sk = ImageOps.grayscale(cover(S + 'stpauls.jpg', TW, TH, 0.5, 0.45)); sk_l = Image.new('RGBA', (TW, TH), (20, 20, 22, 0)); sk_l.putalpha(sk.point(lambda v: int(v * 0.22))); can.alpha_composite(sk_l)
    # giant warm year with a grungy surface
    f = font('Anton', 520); M = Image.new('L', (TW, TH), 0); ImageDraw.Draw(M).text((TW / 2, 395), '1940', font=f, fill=255, anchor='mm')
    yx = np.linspace(0, 1, TW)[None, :]; col = np.stack([248 + 0 * yx, 178 + 40 * yx, 92 + 0 * yx], -1).repeat(TH, 0)
    col = col * (1 + noise(TW, TH, 1, 11, 1.5)[..., None] * 0.18); spk = rng(12).random((TH, TW)) < 0.004
    col[spk] *= 0.6
    Y = Image.fromarray(col.clip(0, 255).astype(np.uint8)).convert('RGBA'); Y.putalpha(M); can.alpha_composite(Y)
    title = 'LUFTSCHLACHT UM ENGLAND'; text(can, (TW / 2, 30), title, fit_font('Anton', title, 890, 96), (240, 240, 240), 'mt', shadow=5)
    # three men: Dowding, Churchill, Galland
    for name, h, cx, front in () if not PEOPLE else (('dowding', 470, 250, False), ('galland', 470, 1030, False), ('churchill_c', 560, 640, True)):
        im = cut(name, h=h)
        if name == 'churchill_c': im = ImageEnhance.Contrast(im).enhance(1.15)
        im = im.filter(ImageFilter.UnsharpMask(2, 80, 2)); shadow_paste(can, im, (cx - im.width // 2, TH - im.height + 6), 24, 0.75, (0, 10))
    vig = np.clip(np.hypot((np.arange(TW)[None, :] - TW / 2) / TW, (np.arange(TH)[:, None] - TH / 2) / TH) - 0.32, 0, 1) * 300
    v = Image.new('RGBA', (TW, TH), (0, 0, 0, 0)); v.putalpha(Image.fromarray(vig.clip(0, 150).astype(np.uint8))); can.alpha_composite(v)
    logo(can); badge(can, 36, 28)
    return can
# ================= D: "The Berlin Wall" =================
def thumb_D():
    base = np.ones((TH, TW, 3), np.float32) * np.array([238, 236, 230], np.float32); base += noise(TW, TH, 1, 4, 1.0)[..., None] * 18
    can = Image.fromarray(base.clip(0, 255).astype(np.uint8)).convert('RGBA')
    # map: the London aerial turned into thin grey line work, the Thames inked red
    ae = ImageOps.grayscale(cover(S + 'wapping.jpg', 760, 560, 0.55, 0.55, 1.1)); ed = ae.filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 38 else 0)
    ml = Image.new('RGBA', ae.size, (120, 120, 120, 0)); ml.putalpha(ed.point(lambda v: int(v * 0.5))); can.alpha_composite(ml, (0, 0))
    d = ImageDraw.Draw(can); r = rng(8); pts = [(560 + 40 * math.sin(i * 0.5), i * 12) for i in range(0, 52)]
    d.line(pts, fill=RED + (255,), width=5, joint='curve')
    text(can, (420, 70), 'LONDON', font('Oswald', 34), (40, 40, 40)); text(can, (470, 470), 'THEMSE', font('Oswald', 26), (70, 70, 70))
    # red paint splash top right
    sp = Image.new('L', (TW, TH), 0); ds = ImageDraw.Draw(sp)
    for k in range(60):
        a = r.uniform(0, 2 * math.pi); rr = r.uniform(80, 260); x, y = 1080 + rr * math.cos(a), 120 + rr * 0.7 * math.sin(a); s = r.uniform(30, 110); ds.ellipse((x - s, y - s, x + s, y + s), fill=255)
    sp = sp.filter(ImageFilter.GaussianBlur(3)).point(lambda v: 255 if v > 128 else 0)
    spl = Image.new('RGBA', (TW, TH), (150, 14, 18, 0)); spl.putalpha(sp); can.alpha_composite(spl); splatter(can, 21, 30, (820, 0, 1280, 360), (150, 14, 18))
    # black-and-white people
    def bw(n, h):
        im = cut(n, h=h); g = ImageEnhance.Contrast(ImageOps.grayscale(im.convert('RGB'))).enhance(1.25).convert('RGBA'); g.putalpha(im.getchannel('A')); return g.filter(ImageFilter.UnsharpMask(2, 90, 2))
    ob = bw('k4_observer', 470); shadow_paste(can, ob, (1050, 60), 14, 0.5)
    fw = bw('k5_feuerwehr', 500); shadow_paste(can, fw, (640, TH - fw.height + 20), 18, 0.55)
    spf = bw('spitfire_air', 150); shadow_paste(can, spf, (820, 30), 8, 0.4)
    # newspaper clipping
    npw, nph = 330, 250; N = Image.new('RGBA', (npw, nph), (232, 226, 210, 255)); dn = ImageDraw.Draw(N)
    dn.text((14, 10), 'DAILY NEWS, SEPT. 9, 1940', font=font('Oswald', 18), fill=(40, 40, 40)); dn.line((14, 38, npw - 14, 38), fill=(40, 40, 40), width=2)
    dn.text((14, 44), 'LONDON CAN', font=font('Anton', 56), fill=(25, 25, 25)); dn.text((14, 112), 'TAKE IT!', font=font('Anton', 56), fill=(25, 25, 25))
    for i in range(6): dn.line((14, 186 + i * 10, npw - 14 - (i * 23) % 70, 186 + i * 10), fill=(120, 120, 120), width=3)
    N = N.rotate(-5, expand=True, resample=Image.BICUBIC)
    # skyline silhouette and a Chain Home mast bottom left
    sk = skyline_mask(520, 140).filter(ImageFilter.GaussianBlur(0.6)); skl = Image.new('RGBA', sk.size, (70, 70, 72, 0)); skl.putalpha(sk.point(lambda v: int(v * 0.85))); can.alpha_composite(skl, (0, TH - 140))
    dd = ImageDraw.Draw(can)
    for mx in (40,):
        dd.line((mx, TH, mx + 25, TH - 300), fill=(50, 50, 52), width=4); dd.line((mx + 50, TH, mx + 25, TH - 300), fill=(50, 50, 52), width=4)
        for k in range(10): y = TH - 30 * k; dd.line((mx + 2.5 * k, y, mx + 50 - 2.5 * k, y - 30), fill=(50, 50, 52), width=2)
    shadow_paste(can, N, (300, 470), 10, 0.5)
    # title stacked, black and dark red, red ribbon
    f = fit_font('Anton', 'LUFTSCHLACHT', 520, 132)
    text(can, (40, 40), 'DIE', font('Anton', 110), (15, 15, 15)); text(can, (40, 168), 'LUFTSCHLACHT', f, (120, 10, 14)); text(can, (40, 310), 'UM ENGLAND', fit_font('Anton', 'UM ENGLAND', 520, 132), (15, 15, 15))
    rib = Image.new('RGBA', (560, 64), (150, 14, 18, 255)); rd = ImageDraw.Draw(rib)
    for x in range(0, 560, 6): rd.line((x, 0, x, r.integers(0, 6)), fill=(0, 0, 0, 0)); rd.line((x, 64, x, 64 - r.integers(0, 6)), fill=(0, 0, 0, 0))
    rd.text((280, 32), 'LONDON BRANNTE 57 NÄCHTE', font=font('Oswald', 34), fill=WHITE, anchor='mm'); can.alpha_composite(rib, (36, 452))
    logo(can); badge(can, 1125, 650)
    return can

if __name__ == '__main__':
    os.makedirs(O, exist_ok=True)
    for k, fn in (('B_1940_leer', thumb_B), ('C_1940_leer', thumb_C)):
        fn().convert('RGB').save(O + 'Teil4_Stil_%s.jpg' % k, quality=95); print(k)
