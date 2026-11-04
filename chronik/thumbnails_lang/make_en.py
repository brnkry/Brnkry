# long-video thumbnails v2 in the channel's logo style: Anton white + yellow plate with dark text + red rule, CDM badge, no script font
import sys
exec(open(sys.argv[1] + '/make.py').read().split('# ---------- Hartmann A')[0])
from PIL import ImageEnhance

def badge(can, x, y, h=110):
    """CDM logo: white C, DM on a yellow plate, red rule; (x, y) is the top-left corner"""
    f = anton(int(h * 0.82)); d = ImageDraw.Draw(can)
    wc = d.textlength('C', font=f); wd = d.textlength('DM', font=f); gap, pad = h * 0.07, h * 0.06
    cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'DM', font=f, anchor='lm')
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.rounded_rectangle((x - h * 0.22, y - h * 0.16, b[2] + pad + h * 0.22, y + h * 1.12), h * 0.12, fill=(8, 9, 11, 170))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(can)
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm')
    d.rectangle((b[0] - pad, b[1] - h * 0.06, b[2] + pad, b[3] + h * 0.05), fill=YEL)
    d.text((xd, cy), 'DM', font=f, fill=DARK, anchor='lm')
    d.rectangle((b[0] - pad, b[3] + h * 0.12, b[0] + h * 0.42, b[3] + h * 0.16), fill=RED)
def title2(can, cy, white, yellow, size, gap=36, pad=30, rule=True):
    """one line: white word(s), then word(s) on a yellow plate, red rule under the plate (the logo/banner look)"""
    d = ImageDraw.Draw(can); f = anton(size)
    w1 = d.textlength(white, font=f) if white else 0; w2 = d.textlength(yellow, font=f); g = gap if white else 0
    x0 = W / 2 - (w1 + g + w2 + 2 * pad) / 2
    if white: text(can, (x0, cy), white, f, WHITE, anchor='lm')
    d = ImageDraw.Draw(can); b = d.textbbox((x0 + w1 + g + pad, cy), yellow, font=f, anchor='lm')
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((b[0] - pad + 8, b[1] - size * 0.08 + 12, b[2] + pad + 8, b[3] + size * 0.07 + 12), fill=(0, 0, 0, 190)); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(can); d.rectangle((b[0] - pad, b[1] - size * 0.08, b[2] + pad, b[3] + size * 0.07), fill=YEL)
    d.text((x0 + w1 + g + pad, cy), yellow, font=f, fill=DARK, anchor='lm')
    if rule: d.rectangle((b[0] - pad, b[3] + size * 0.13, b[0] - pad + size * 1.1, b[3] + size * 0.17), fill=RED)

def hartmann_a():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    L = grade(cover(load('i7'), 1100, H, 0.5, 0.15, 1.12)).convert('RGBA')
    R = ImageEnhance.Contrast(ImageOps.grayscale(cover(load('i6'), 1100, H, 0.5, 0.2, 1.18)).convert('RGB')).enhance(1.15).convert('RGBA')
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(0, 0), (1010, 0), (900, H), (0, H)], fill=255)
    can.paste(R, (W - 1100, 0)); can.paste(L.crop((0, 0, 1100, H)), (-60, 0), m.crop((60, 0, 1160, H)))
    Lr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(Lr).line([(950, -10), (840, H + 10)], fill=YEL + (255,), width=14); can.alpha_composite(Lr)
    vgrad(can, 90, 240, 0.40); vignette(can, 120)
    plate(can, (200, 120), '1944', bebas(84), YEL, DARK, rot=3)
    plate(can, (1720, 120), '1955', bebas(84), WHITE, DARK, rot=-3)
    badge(can, 820, 50, 104)
    text(can, (W // 2, 700), 'ERICH HARTMANN', anton(190), WHITE)
    title2(can, 930, '', '10 YEARS IN PRISON', 150)
    save(can, 'Hartmann_A_EN.jpg')

def hartmann_b():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    bg = cover(load('i5'), W, H, 0.6, 0.3, 1.3).filter(ImageFilter.GaussianBlur(30)).convert('RGBA'); can.alpha_composite(bg)
    can.alpha_composite(Image.new('RGBA', (W, H), (6, 7, 9, 150)))
    P = grade(load('i5').crop((790, 0, 1790, 1438)).resize((751, H), Image.LANCZOS)).convert('RGBA')
    m = Image.new('L', P.size, 255); dm = ImageDraw.Draw(m)
    for i in range(120): dm.line((i, 0, i, H), fill=int(255 * i / 120)); dm.line((P.width - 1 - i, 0, P.width - 1 - i, H), fill=int(255 * i / 120))
    can.paste(P, (W - P.width - 70, 0), m)
    hgrad(can, 0, 1000, 210, 0); vignette(can, 110)
    badge(can, 90, 60, 100)
    text(can, (540, 360), '352', anton(360), WHITE)
    d = ImageDraw.Draw(can); f = anton(150); b = d.textbbox((540, 610), 'WIRKLICH?', font=f, anchor='mm')
    d.rectangle((b[0] - 32, b[1] - 14, b[2] + 32, b[3] + 12), fill=YEL); d.text((540, 610), 'WIRKLICH?', font=f, fill=DARK, anchor='mm')
    d.rectangle((b[0] - 32, b[3] + 26, b[0] + 130, b[3] + 34), fill=RED)
    text(can, (540, 805), 'ERICH', anton(150), WHITE)
    text(can, (540, 945), 'HARTMANN', anton(150), WHITE)
    save(can, 'Hartmann_B.jpg')

def lw_a():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    A = grade(cover(load('i2'), 1000, H, 0.5, 0.05, 1.1)).convert('RGBA')
    B = grade(cover(load('i3'), 1000, H, 0.5, 0.1, 1.1), 1.05, 1.0).convert('RGBA')
    can.paste(B, (W - 1000, 0))
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(0, 0), (1020, 0), (900, H), (0, H)], fill=255)
    can.paste(A, (-20, 0), m.crop((20, 0, 1020, H)))
    Lr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(Lr).line([(1000, -10), (880, H + 10)], fill=YEL + (255,), width=14); can.alpha_composite(Lr)
    vgrad(can, 80, 245, 0.40); vignette(can, 110)
    plate(can, (200, 110), 'REAL', bebas(100), YEL, DARK, rot=3)
    plate(can, (1730, 110), 'FILM', bebas(100), RED, WHITE, rot=-3)
    badge(can, 820, 50, 104)
    title2(can, 740, 'THE REAL', 'DAS BOOT CAPTAIN', 150)
    text(can, (W // 2, 970), 'HEINRICH LEHMANN-WILLENBROCK', anton(122), WHITE)
    save(can, 'LehmannWillenbrock_A_EN.jpg')

def lw_b():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    bg = cover(load('i4'), W, H, 0.5, 0.4, 1.5).filter(ImageFilter.GaussianBlur(30)).convert('RGBA'); can.alpha_composite(bg)
    can.alpha_composite(Image.new('RGBA', (W, H), (6, 7, 9, 150)))
    P = grade(cover(load('i4'), 1200, H, 0.5, 0.15, 1.05)).convert('RGBA')
    m = Image.new('L', (1200, H), 255); dm = ImageDraw.Draw(m)
    for i in range(200): dm.line((i, 0, i, H), fill=int(255 * i / 200))
    can.paste(P, (W - 1200 + 40, 0), m)
    hgrad(can, 0, 1000, 215, 0); vignette(can, 100)
    st = grade(cover(load('i3'), 620, 360, 0.5, 0.3, 1.05)).convert('RGBA')
    card = Image.new('RGBA', (640, 380), WHITE + (255,)); card.paste(st, (10, 10)); card = card.rotate(-5, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', card.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (0, 0), card.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (110, 175)); can.alpha_composite(card, (90, 155))
    plate(can, (560, 540), 'FILM', bebas(70), RED, WHITE, rot=-5)
    arrow(can, [(720, 360), (960, 280), (1150, 450)], YEL, 16)
    badge(can, 90, 40, 96)
    text(can, (540, 665), 'DAS BOOT', anton(170), WHITE)
    d = ImageDraw.Draw(can); f = anton(120); bb = d.textbbox((540, 805), 'WAR ECHT', font=f, anchor='mm')
    d.rectangle((bb[0] - 30, bb[1] - 12, bb[2] + 30, bb[3] + 10), fill=YEL); d.text((540, 805), 'WAR ECHT', font=f, fill=DARK, anchor='mm')
    text(can, (540, 925), 'HEINRICH', anton(100), WHITE)
    text(can, (540, 1025), 'LEHMANN-WILLENBROCK', anton(100), WHITE)
    save(can, 'LehmannWillenbrock_B.jpg')


hartmann_a(); lw_a()
