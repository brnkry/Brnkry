# channel logo proposals for "Chronik der Macht": avatar (1024, circle-safe) + wordmark (1800x600) per option
import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = sys.argv[1] + '/'; F = D + '../sch/fonts/'
YEL, RED, WHITE, DARK, PAPER, INK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18), (232, 224, 205), (30, 28, 26)
def anton(s): return ImageFont.truetype(F + 'Anton-Regular.ttf', s)
def bebas(s): return ImageFont.truetype(F + 'BebasNeue-Regular.ttf', s)
def typew(s): return ImageFont.truetype(F + 'SpecialElite-Regular.ttf', s)
rng = np.random.default_rng(4)

def grain(im, amt=10, scale=1):
    a = np.asarray(im.convert('RGB')).astype(np.int16); h, w = a.shape[:2]
    n = rng.normal(0, amt, (h // scale + 1, w // scale + 1)); n = np.kron(n, np.ones((scale, scale)))[:h, :w]
    return Image.fromarray(np.clip(a + n[..., None], 0, 255).astype(np.uint8))
def paper(w, h, col=PAPER):
    a = np.ones((h, w, 3)) * np.array(col, float)
    n = Image.fromarray((rng.normal(128, 40, (h // 6, w // 6))).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(4))
    a *= (0.93 + 0.07 * np.asarray(n)[..., None] / 128)
    y, x = np.mgrid[0:h, 0:w]; r = np.sqrt(((x - w / 2) / (w * 0.6)) ** 2 + ((y - h / 2) / (h * 0.6)) ** 2)
    a *= (1 - 0.25 * np.clip(r - 0.5, 0, 1))[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
def worn(L, keep=0.82, blot=3):
    """rubber-stamp wear: random ink dropout"""
    a = np.asarray(L.getchannel('A')).astype(np.float32); h, w = a.shape
    n = Image.fromarray((rng.random((h // blot, w // blot)) * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.2))
    m = (np.asarray(n) / 255.0 < keep) * 0.85 + 0.15
    L.putalpha(Image.fromarray((a * m).astype(np.uint8))); return L
def arc_text(d, cx, cy, r, txt, font, fill, start, span, inward=False):
    """text along a circle, centred on angle start (degrees, 0 = top), spread over span degrees"""
    n = len(txt); ws = [font.getlength(c) for c in txt]; tot = sum(ws); sg = -1 if inward else 1; a = start - sg * span / 2
    for c, w in zip(txt, ws):
        ang = a + sg * span * (w / 2) / tot; a += sg * span * w / tot
        th = math.radians(ang); x = cx + r * math.sin(th); y = cy - r * math.cos(th)
        G = Image.new('RGBA', (int(w) + 40, font.size + 40), (0, 0, 0, 0)); ImageDraw.Draw(G).text((20, 10), c, font=font, fill=fill)
        G = G.rotate(-ang + (180 if inward else 0), resample=Image.BICUBIC, expand=True)
        d.alpha_composite(G, (int(x - G.width / 2), int(y - G.height / 2)))
def save(im, name): im.convert('RGB').save(D + name, quality=95); print(name)

# ---------- A: archive stamp ----------
def stamp(size, col=RED):
    L = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = size / 2; R = size * 0.46
    d.ellipse((c - R, c - R, c + R, c + R), outline=col + (255,), width=int(size * 0.028))
    d.ellipse((c - R * 0.74, c - R * 0.74, c + R * 0.74, c + R * 0.74), outline=col + (255,), width=int(size * 0.012))
    f = bebas(int(size * 0.105))
    arc_text(L, c, c, R * 0.865, 'CHRONIK DER MACHT', f, col + (255,), 0, 200)
    arc_text(L, c, c, R * 0.865, '•  ARCHIV  •', bebas(int(size * 0.085)), col + (255,), 180, 70, inward=True)
    d.text((c, c + size * 0.01), 'CdM', font=anton(int(size * 0.26)), fill=col + (255,), anchor='mm')
    d.line((c - R * 0.5, c + R * 0.36, c + R * 0.5, c + R * 0.36), fill=col + (255,), width=int(size * 0.01))
    return worn(L)
def opt_a():
    av = paper(1024, 1024); s = stamp(900).rotate(-8, resample=Image.BICUBIC); av.alpha_composite(s, (62, 62)); save(grain(av, 6), 'A_Stempel_avatar.jpg')
    wm = Image.new('RGBA', (1800, 600), DARK + (255,)); s = stamp(470, RED).rotate(-8, resample=Image.BICUBIC); wm.alpha_composite(s, (60, 65))
    d = ImageDraw.Draw(wm); d.text((600, 220), 'CHRONIK DER MACHT', font=anton(150), fill=WHITE, anchor='lm')
    d.text((606, 370), 'Geschichte. Quellen. Originalaufnahmen.', font=typew(52), fill=(200, 196, 186), anchor='lm')
    save(grain(wm, 5), 'A_Stempel_wordmark.jpg')

# ---------- B: yellow bar (the thumbnail look) ----------
def opt_b():
    av = Image.new('RGBA', (1024, 1024), DARK + (255,)); d = ImageDraw.Draw(av)
    d.text((512, 430), 'C', font=anton(660), fill=WHITE, anchor='mm')
    d.rectangle((300, 760, 724, 818), fill=YEL)
    d.rectangle((300, 836, 470, 852), fill=RED)
    save(grain(av, 5), 'B_Balken_avatar.jpg')
    wm = Image.new('RGBA', (1800, 600), DARK + (255,)); d = ImageDraw.Draw(wm)
    d.text((900, 210), 'CHRONIK', font=anton(230), fill=WHITE, anchor='mm')
    b = d.textbbox((900, 440), 'DER MACHT', font=anton(110), anchor='mm'); d.rectangle((b[0] - 34, b[1] - 22, b[2] + 34, b[3] + 18), fill=YEL)
    d.text((900, 440), 'DER MACHT', font=anton(110), fill=DARK, anchor='mm')
    d.rectangle((b[0] - 34, b[3] + 34, b[0] + 160, b[3] + 44), fill=RED)
    save(grain(wm, 4), 'B_Balken_wordmark.jpg')

# ---------- C: typewriter key ----------
def key(size, ch='C'):
    L = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = size / 2; R = size * 0.44
    sh = Image.new('RGBA', (size, size), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((c - R, c - R + size * 0.03, c + R, c + R + size * 0.03), fill=(0, 0, 0, 200)); L.alpha_composite(sh.filter(ImageFilter.GaussianBlur(size * 0.03)))
    for i in range(30):   # brushed metal rim, light from top left
        u = i / 29; r = R - i * size * 0.002; v = int(150 + 80 * (1 - u))
        d.ellipse((c - r, c - r, c + r, c + r), fill=(v, v - 4, v - 10, 255))
    r2 = R * 0.84; d.ellipse((c - r2, c - r2, c + r2, c + r2), fill=(22, 22, 24, 255))
    hl = Image.new('RGBA', (size, size), (0, 0, 0, 0)); ImageDraw.Draw(hl).ellipse((c - r2 * 0.9, c - r2 * 0.95, c + r2 * 0.5, c - r2 * 0.1), fill=(255, 255, 255, 26)); L.alpha_composite(hl.filter(ImageFilter.GaussianBlur(size * 0.04)))
    d.text((c, c + size * 0.02), ch, font=typew(int(size * 0.5)), fill=PAPER + (255,), anchor='mm')
    return L
def opt_c():
    av = Image.new('RGBA', (1024, 1024), (24, 23, 22, 255)); av.alpha_composite(key(960), (32, 32)); save(grain(av, 5), 'C_Taste_avatar.jpg')
    wm = paper(1800, 600, (40, 38, 35)); wm.alpha_composite(key(470), (70, 65))
    d = ImageDraw.Draw(wm); d.text((600, 250), 'Chronik der Macht', font=typew(120), fill=PAPER, anchor='lm')
    d.line((606, 345, 1690, 345), fill=YEL, width=6)
    d.text((606, 410), 'WAS WIRKLICH GESCHAH', font=bebas(70), fill=(190, 184, 172), anchor='lm')
    save(grain(wm, 5), 'C_Taste_wordmark.jpg')

# ---------- D: film frame ----------
def frame(size):
    L = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(L); w = size * 0.62; x0 = (size - w) / 2
    d.rectangle((x0, size * 0.06, x0 + w, size * 0.94), fill=(18, 18, 20, 255))
    for i in range(7):   # perforations on both edges
        y = size * 0.1 + i * size * 0.12; ph = size * 0.06
        for xx in (x0 + w * 0.05, x0 + w * 0.85):
            d.rounded_rectangle((xx, y, xx + w * 0.1, y + ph), size * 0.01, fill=(232, 224, 205, 255))
    fx0, fx1 = x0 + w * 0.22, x0 + w * 0.78
    d.rectangle((fx0, size * 0.2, fx1, size * 0.8), fill=(36, 36, 38, 255))
    d.text((size / 2, size * 0.47), 'C', font=anton(int(size * 0.42)), fill=YEL + (255,), anchor='mm')
    d.rectangle((fx0 + 20, size * 0.72, fx1 - 20, size * 0.735), fill=RED + (255,))
    return L
def opt_d():
    av = Image.new('RGBA', (1024, 1024), (205, 198, 182, 255)); av.alpha_composite(frame(1024).rotate(-6, resample=Image.BICUBIC)); save(grain(av, 7), 'D_Film_avatar.jpg')
    wm = Image.new('RGBA', (1800, 600), DARK + (255,)); wm.alpha_composite(frame(560).rotate(-6, resample=Image.BICUBIC), (30, 20))
    d = ImageDraw.Draw(wm); d.text((600, 230), 'CHRONIK DER MACHT', font=anton(150), fill=WHITE, anchor='lm')
    d.text((604, 385), 'DOKUMENTATIONEN AUS ORIGINALAUFNAHMEN', font=bebas(64), fill=YEL, anchor='lm')
    save(grain(wm, 5), 'D_Film_wordmark.jpg')

for f in (opt_a, opt_b, opt_c, opt_d): f()
# preview: avatars as YouTube circles, large and at real size
P = Image.new('RGB', (4 * 300, 420), (15, 15, 15)); dd = ImageDraw.Draw(P)
for i, n in enumerate(['A_Stempel', 'B_Balken', 'C_Taste', 'D_Film']):
    im = Image.open(D + n + '_avatar.jpg').resize((240, 240), Image.LANCZOS); m = Image.new('L', (240, 240), 0); ImageDraw.Draw(m).ellipse((0, 0, 239, 239), fill=255)
    P.paste(im, (i * 300 + 30, 20), m); sm = im.resize((48, 48), Image.LANCZOS); m2 = m.resize((48, 48)); P.paste(sm, (i * 300 + 126, 290), m2)
    dd.text((i * 300 + 150, 380), n, fill=(230, 230, 230), anchor='mm', font=bebas(36))
P.save(D + 'preview_avatars.jpg', quality=92)
