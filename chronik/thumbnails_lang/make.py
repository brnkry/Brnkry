# long-video thumbnails (1920x1080): Erich Hartmann and Heinrich Lehmann-Willenbrock, two options each
import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
D = sys.argv[1] + '/'
F = D + '../sch/fonts/'
W, H = 1920, 1080
YEL, RED, WHITE, DARK = (244, 199, 15), (205, 35, 40), (245, 245, 240), (12, 14, 18)
def anton(s): return ImageFont.truetype(F + 'Anton-Regular.ttf', s)
def bebas(s): return ImageFont.truetype(F + 'BebasNeue-Regular.ttf', s)
def brush(s): return ImageFont.truetype(D + 'fontsource-caveat-brush-5.3.0/files/caveat-brush-latin-400-normal.woff2', s)

# swastika spots (source px x, y, diameter): cap eagles, Knight's Cross centres, breast eagles
BLUR = {'i1': [(1134, 150, 80), (1296, 1390, 70)], 'i2': [(1345, 158, 64), (1972, 1272, 60)],
        'i4': [(1382, 1237, 62)], 'i5': [(1209, 1154, 62), (902, 1400, 66)], 'i7': [(1248, 1117, 60), (934, 1388, 66)]}
def load(n):
    im = Image.open(D + 'src/' + n + '.jpg').convert('RGB')
    for x, y, d in BLUR.get(n, []):
        r = d / 2; box = (int(x - d), int(y - d), int(x + d), int(y + d)); reg = im.crop(box)
        bl = reg.resize((max(1, reg.width // 8), max(1, reg.height // 8)), Image.BILINEAR).resize(reg.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(d * 0.12))
        m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).ellipse((reg.width / 2 - r, reg.height / 2 - r, reg.width / 2 + r, reg.height / 2 + r), fill=255)
        im.paste(Image.composite(bl, reg, m.filter(ImageFilter.GaussianBlur(r * 0.25))), box[:2])
    return im
def cover(im, w, h, cx=0.5, cy=0.5, zoom=1.0):
    s = max(w / im.width, h / im.height) * zoom; iw, ih = int(im.width * s), int(im.height * s)
    im = im.resize((iw, ih), Image.LANCZOS); x = int((iw - w) * cx); y = int((ih - h) * cy)
    return im.crop((x, y, x + w, y + h))
def grade(im, amt=1.12, sat=1.08):
    from PIL import ImageEnhance
    return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(amt)).enhance(sat)

def text(can, xy, s, font, fill, anchor='mm', stroke=0, shadow=True, rot=0):
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    if shadow:
        S = Image.new('RGBA', can.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(S)
        ds.text((xy[0] + 6, xy[1] + 10), s, font=font, fill=(0, 0, 0, 230), anchor=anchor, stroke_width=stroke + 6, stroke_fill=(0, 0, 0, 230))
        L.alpha_composite(S.filter(ImageFilter.GaussianBlur(14)))
    d.text(xy, s, font=font, fill=fill + (255,), anchor=anchor, stroke_width=stroke, stroke_fill=(10, 10, 10, 255))
    if rot: L = L.rotate(rot, center=xy, resample=Image.BICUBIC)
    can.alpha_composite(L)
def plate(can, xy, s, font, bg, fg, pad=(26, 10), rot=0):
    d0 = ImageDraw.Draw(can); b = d0.textbbox(xy, s, font=font, anchor='mm')
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((b[0] - pad[0], b[1] - pad[1] - 6, b[2] + pad[0], b[3] + pad[1]), fill=bg + (255,))
    d.text(xy, s, font=font, fill=fg + (255,), anchor='mm')
    if rot: L = L.rotate(rot, center=xy, resample=Image.BICUBIC)
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 160), (0, 0), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (6, 8)); can.alpha_composite(L)
def arrow(can, pts, col, w=16, head=46):
    """hand-drawn style curved arrow through the given points (quadratic bezier)"""
    p0, p1, p2 = pts; P = [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in [i / 40 for i in range(41)]]
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line(P, fill=(0, 0, 0, 200), width=w + 10, joint='curve'); d.line(P, fill=col + (255,), width=w, joint='curve')
    a = math.atan2(P[-1][1] - P[-4][1], P[-1][0] - P[-4][0]); e = P[-1]
    tri = [(e[0] + 10 * math.cos(a), e[1] + 10 * math.sin(a)), (e[0] - head * math.cos(a - 0.5), e[1] - head * math.sin(a - 0.5)), (e[0] - head * math.cos(a + 0.5), e[1] - head * math.sin(a + 0.5))]
    d.polygon(tri, fill=col + (255,), outline=(0, 0, 0, 200)); can.alpha_composite(L)
def ring(can, box, col, w=12):
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse(box, outline=(0, 0, 0, 180), width=w + 8); d.ellipse(box, outline=col + (255,), width=w); can.alpha_composite(L)
def vgrad(can, top=0, bot=200, start=0.45):
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for y in range(H):
        u = max(0, (y / H - start) / (1 - start)); a = int(bot * u ** 1.4 + top * max(0, 1 - y / (H * 0.3)))
        d.line((0, y, W, y), fill=(6, 7, 9, min(255, a)))
    can.alpha_composite(L)
def hgrad(can, x0, x1, a0, a1):
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for x in range(min(x0, x1), max(x0, x1)):
        u = (x - x0) / (x1 - x0); d.line((x, 0, x, H), fill=(6, 7, 9, int(a0 + (a1 - a0) * u)))
    can.alpha_composite(L)
def vignette(can, k=150):
    L = Image.new('L', (W // 4, H // 4), 0); d = ImageDraw.Draw(L); d.ellipse((-W // 10, -H // 8, W // 4 + W // 10, H // 4 + H // 8), fill=255)
    m = ImageOps.invert(L.filter(ImageFilter.GaussianBlur(40))).resize((W, H)); V = Image.new('RGBA', (W, H), (0, 0, 0, 0)); V.putalpha(m.point(lambda v: int(v * k / 255))); can.alpha_composite(V)
def save(can, name): can.convert('RGB').save(D + name, quality=92); print(name)

# ---------- Hartmann A: the same man, 1944 and 1955 ----------
def hartmann_a():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    L = grade(cover(load('i7'), 1100, H, 0.5, 0.15, 1.12)).convert('RGBA')
    R = ImageOps.grayscale(cover(load('i6'), 1100, H, 0.5, 0.2, 1.18)).convert('RGB')
    from PIL import ImageEnhance; R = ImageEnhance.Contrast(R).enhance(1.15).convert('RGBA')
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(0, 0), (1010, 0), (900, H), (0, H)], fill=255)
    can.paste(R, (W - 1100, 0)); can.paste(L.crop((0, 0, 1100, H)), (-60, 0), m.crop((60, 0, 1160, H)))
    Lr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(Lr).line([(950, -10), (840, H + 10)], fill=YEL + (255,), width=14); can.alpha_composite(Lr)
    vgrad(can, 90, 235, 0.42); vignette(can, 120)
    plate(can, (230, 110), '1944', bebas(80), YEL, DARK, rot=3)
    plate(can, (1700, 110), '1955', bebas(80), WHITE, DARK, rot=-3)
    text(can, (W // 2, 790), '10 JAHRE HAFT', anton(250), YEL)
    text(can, (W // 2, 975), 'ERICH HARTMANN', anton(108), WHITE)
    text(can, (W // 2 - 20, 150), 'derselbe Mann', brush(120), WHITE)
    arrow(can, [(700, 200), (600, 230), (560, 330)], WHITE, 13, 40)
    arrow(can, [(1220, 200), (1330, 230), (1370, 330)], WHITE, 13, 40)
    save(can, 'Hartmann_A.jpg')

# ---------- Hartmann B: 352, checked ----------
def hartmann_b():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    P = grade(load('i5').crop((790, 0, 1790, 1438)).resize((751, H), Image.LANCZOS)).convert('RGBA')
    m = Image.new('L', P.size, 255); dm = ImageDraw.Draw(m)
    for i in range(120): dm.line((i, 0, i, H), fill=int(255 * i / 120)); dm.line((P.width - 1 - i, 0, P.width - 1 - i, H), fill=int(255 * i / 120))
    can.paste(P, (W - P.width - 70, 0), m)
    hgrad(can, 0, 1000, 210, 0); vignette(can, 110)
    text(can, (470, 430), '352', anton(420), YEL)
    text(can, (470, 690), 'ABSCHÜSSE', anton(140), WHITE)
    text(can, (500, 860), 'wirklich?', brush(190), RED, rot=4, stroke=3)
    text(can, (470, 990), 'ERICH HARTMANN', bebas(92), WHITE)
    save(can, 'Hartmann_B.jpg')

# ---------- Lehmann-Willenbrock A: real vs film ----------
def lw_a():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    A = grade(cover(load('i2'), 1000, H, 0.5, 0.05, 1.1)).convert('RGBA')
    B = grade(cover(load('i3'), 1000, H, 0.5, 0.1, 1.1), 1.05, 1.0).convert('RGBA')
    can.paste(B, (W - 1000, 0))
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(0, 0), (1020, 0), (900, H), (0, H)], fill=255)
    can.paste(A.crop((0, 0, 1000, H)).resize((1000, H)), (-20, 0), m.crop((20, 0, 1020, H)))
    Lr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(Lr).line([(1000, -10), (880, H + 10)], fill=YEL + (255,), width=14); can.alpha_composite(Lr)
    vgrad(can, 80, 240, 0.42); vignette(can, 110)
    plate(can, (220, 100), 'ECHT', bebas(96), YEL, DARK, rot=3)
    plate(can, (1710, 100), 'FILM', bebas(96), RED, WHITE, rot=-3)
    text(can, (W // 2, 790), 'DER ECHTE KALEU', anton(220), YEL)
    text(can, (W // 2, 960), 'aus "Das Boot"', brush(150), WHITE, rot=-2)
    save(can, 'LehmannWillenbrock_A.jpg')

# ---------- Lehmann-Willenbrock B: "Das Boot" existed ----------
def lw_b():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    bg = cover(load('i4'), W, H, 0.5, 0.4, 1.5).filter(ImageFilter.GaussianBlur(30)).convert('RGBA'); can.alpha_composite(bg)
    can.alpha_composite(Image.new('RGBA', (W, H), (6, 7, 9, 150)))
    P = grade(cover(load('i4'), 1200, H, 0.5, 0.15, 1.05)).convert('RGBA')
    m = Image.new('L', (1200, H), 255); dm = ImageDraw.Draw(m)
    for i in range(200): dm.line((i, 0, i, H), fill=int(255 * i / 200))
    can.paste(P, (W - 1200 + 40, 0), m)
    hgrad(can, 0, 1000, 215, 0); vignette(can, 100)
    # film still as a tilted inset photo
    st = grade(cover(load('i3'), 620, 360, 0.5, 0.3, 1.05)).convert('RGBA')
    card = Image.new('RGBA', (640, 380), WHITE + (255,)); card.paste(st, (10, 10)); card = card.rotate(-5, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', card.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (0, 0), card.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (110, 90)); can.alpha_composite(card, (90, 70))
    plate(can, (330, 470), 'FILM, 1981', bebas(54), RED, WHITE, rot=-5)
    arrow(can, [(720, 280), (960, 200), (1150, 380)], YEL, 16)
    text(can, (520, 690), 'DAS BOOT', anton(230), YEL)
    text(can, (540, 880), 'gab es wirklich', brush(150), WHITE, rot=-3)
    text(can, (520, 1010), 'HEINRICH LEHMANN-WILLENBROCK', bebas(70), WHITE)
    save(can, 'LehmannWillenbrock_B.jpg')

for f in (hartmann_a, hartmann_b, lw_a, lw_b): f()
