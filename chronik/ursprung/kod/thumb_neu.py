# three new covers for "Der wahre Ursprung des Zweiten Weltkriegs": (A) timeline collage, statement; (B) 1939? question; (C) the true origin, 1919
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance
W, H = 1280, 720; FD = '/tmp/claude-0/fonts/'
U = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/urs/'; IMG = U + 'img/'
OUT = '/home/user/Brnkry/chronik/ursprung/thumbnails/'
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
osw = lambda z: ImageFont.truetype(FD + 'Oswald.ttf', z); anton = lambda z: ImageFont.truetype(FD + 'Anton.ttf', z)
rng = np.random.default_rng(3)
def sepia(im, k=1.0, dark=1.0):
    g = np.asarray(ImageOps.autocontrast(im.convert('L'), cutoff=1), np.float32) * dark
    return Image.fromarray(np.stack([g * 1.06 + 12, g * 0.94 + 5, g * 0.76], -1).clip(0, 255).astype(np.uint8))
def cover(path, w, h, fx=0.5, fy=0.5):
    im = Image.open(path); s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
def grain(c, a=7):
    arr = np.asarray(c.convert('RGB'), np.float32) + rng.normal(0, a, (H, W, 1)); return Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert('RGBA')
def shade(c, top=0, bottom=0):
    y = np.arange(H)[:, None].repeat(W, 1).astype(np.float32); a = np.zeros((H, W), np.float32)
    if bottom: a = np.maximum(a, np.clip((y - H * (1 - bottom)) / (H * bottom), 0, 1) * 235)
    if top: a = np.maximum(a, np.clip((H * top - y) / (H * top), 0, 1) * 220)
    L = Image.new('RGBA', (W, H), (8, 8, 10, 0)); L.putalpha(Image.fromarray(a.astype(np.uint8))); c.alpha_composite(L)
def stext(c, xy, s, f, col, anchor='la', sh=10):
    L = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(L).text(xy, s, font=f, fill=col + (255,), anchor=anchor)
    S = Image.new('RGBA', c.size, (0, 0, 0, 0)); S.paste((0, 0, 0, 235), (0, 0), L.getchannel('A')); c.alpha_composite(S.filter(ImageFilter.GaussianBlur(sh)), (4, 6)); c.alpha_composite(L)
def fit(fn, s, w, z):
    while fn(z).getlength(s) > w: z -= 2
    return fn(z)
def logo(c):
    d = ImageDraw.Draw(c); f = osw(44); x, y = W - 150, 30
    d.rounded_rectangle((x - 12, y - 8, x + 120, y + 58), 6, fill=(8, 9, 11, 210)); d.text((x, y + 25), 'C', font=f, fill=WHITE, anchor='lm')
    b = d.textbbox((x + 34, y + 25), 'DM', font=f, anchor='lm'); d.rectangle((b[0] - 4, b[1] - 4, b[2] + 4, b[3] + 4), fill=YEL); d.text((x + 34, y + 25), 'DM', font=f, fill=DARK, anchor='lm')
def tag(c, x, y, s, z=40, bg=YEL, fg=DARK):
    d = ImageDraw.Draw(c); f = osw(z); b = d.textbbox((x, y), s, font=f); d.rectangle((b[0] - 14, b[1] - 8, b[2] + 14, b[3] + 8), fill=bg); d.text((x, y), s, font=f, fill=fg)
# (A) four years side by side, statement
def A():
    c = Image.new('RGBA', (W, H), (10, 10, 12, 255)); P = [('Versailles__Bild_254-10.jpg', '1919', .5, .4), ('Rentenmark__Bild_102-11823.jpg', '1923', .45, .5),
                                                        ('Arbeitslose__Bild_183-81526-0005.jpg', '1932', .5, .4), ('Polen_1939__Bild_146-1979-056-18A.jpg', '1939', .45, .5)]
    sw = W // 4
    for i, (f, y, fx, fy) in enumerate(P):
        im = sepia(cover(IMG + f, sw - 6, H, fx, fy), dark=0.9 if y != '1939' else 0.75); c.paste(im.convert('RGBA'), (i * sw + 3, 0))
        tag(c, i * sw + 24, 110, y, 46, RED if y == '1939' else YEL, WHITE if y == '1939' else DARK)
    shade(c, top=0.25, bottom=0.55); c = grain(c)
    f1 = fit(anton, 'DER 2. WELTKRIEG', 1180, 150); stext(c, (W / 2, 522), 'DER 2. WELTKRIEG', f1, WHITE, 'ms')
    f2 = fit(anton, 'BEGANN VOR 1939', 1180, 150); w2 = f2.getlength('BEGANN VOR 1939'); x0 = W / 2 - w2 / 2
    YB = 662; stext(c, (x0, YB), 'BEGANN ', f2, YEL, 'ls'); x1 = x0 + f2.getlength('BEGANN ')
    # VOR in italics (Anton has no italic: the word is sheared like a slanted cut)
    L = Image.new('RGBA', c.size, (0, 0, 0, 0)); stext(L, (x1 - 16, YB), 'VOR', f2, YEL, 'ls'); k = 0.2
    L = L.transform(c.size, Image.AFFINE, (1, k, -k * YB, 0, 1, 0), resample=Image.BICUBIC); c.alpha_composite(L)
    stext(c, (x1 + f2.getlength('VOR ') + 4, YB), '1939', f2, YEL, 'ls')
    logo(c); c.convert('RGB').save(OUT + 'DE_Ursprung_A_Begann_vor_1939.jpg', quality=94)
# (B) the barrier of 1 September 1939, the year as a question
def B():
    c = sepia(cover(IMG + 'Polen_1939__Bild_146-1979-056-18A.jpg', W, H, .45, .45), dark=0.7).convert('RGBA'); shade(c, top=0.45, bottom=0.35); c = grain(c)
    f = fit(anton, 'BEGANN DER 2. WELTKRIEG', 960, 118); stext(c, (W / 2 - 40, 175), 'BEGANN DER 2. WELTKRIEG', f, WHITE, 'ms')
    fy = anton(330); wy = fy.getlength('1939'); fq = anton(330); wq = fq.getlength('?'); x0 = W / 2 - (wy + wq) / 2
    stext(c, (x0, 560), '1939', fy, YEL, 'ls', sh=14); stext(c, (x0 + wy, 560), '?', fq, RED, 'ls', sh=14)
    tag(c, W / 2 - 205, 610, 'DER WAHRE URSPRUNG', 50, WHITE, DARK)
    logo(c); c.convert('RGB').save(OUT + 'DE_Ursprung_B_1939_Frage.jpg', quality=94)
# (C) portrait and the Hall of Mirrors: the true origin, 1919
def C():
    c = sepia(cover(IMG + 'Versailles_Spiegelsaal__Bild_183-R02091.jpg', W, H, .5, .4), dark=0.6).convert('RGBA')
    h = Image.open(U + 'pak/hitler.jpg').convert('L'); bm = Image.new('L', h.size, 0); ImageDraw.Draw(bm).ellipse((380, 400, 485, 590), fill=255)
    h = Image.composite(h.filter(ImageFilter.GaussianBlur(16)), h, bm.filter(ImageFilter.GaussianBlur(14))).crop((0, 0, 505, 590)); s = H / 590
    h = sepia(h.resize((int(505 * s), H), Image.LANCZOS), dark=1.0); m = Image.new('L', h.size, 255)
    g = np.clip(np.arange(h.width)[None, :].repeat(H, 0) / (h.width * 0.25), 0, 1) * np.clip((h.width - np.arange(h.width)[None, :].repeat(H, 0)) / (h.width * 0.3), 0, 1)
    c.paste(h.convert('RGBA'), (W - h.width + 60, 0), Image.fromarray((g * 255).astype(np.uint8)))
    shade(c, bottom=0.5); c = grain(c)
    f1 = fit(anton, 'DER WAHRE URSPRUNG', 820, 140); stext(c, (50, 420), 'DER WAHRE URSPRUNG', f1, WHITE, 'ls')
    f2 = fit(anton, 'DES 2. WELTKRIEGS', 820, 110); stext(c, (50, 545), 'DES 2. WELTKRIEGS', f2, WHITE, 'ls')
    tag(c, 64, 600, 'ER BEGANN NICHT 1939', 62, YEL, DARK)
    logo(c); c.convert('RGB').save(OUT + 'DE_Ursprung_C_Wahrer_Ursprung.jpg', quality=94)
A(); B(); C(); print('ok')
