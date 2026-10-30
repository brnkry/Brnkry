# Chronicle of Power (English sister channel of Chronik der Macht): avatar, banner and overview
# same colours as CDM, different type: Oswald Bold for the name, Playfair Display for the line underneath
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D = sys.argv[1] + '/'; S = sys.argv[2] + '/'; F = S + 'sch/fonts/'
YEL, RED, WHITE, DARK, CREAM = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18), (226, 218, 198)
def oswald(s, wg=700):
    f = ImageFont.truetype(F + 'Oswald%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
def playfair(s, wg=500):
    f = ImageFont.truetype(F + 'PlayfairDisplay%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
rng = np.random.default_rng(23)
# vehicles, aircraft, U-boats, guns and landscape only, no faces
POOL = [('sb/img/p02.jpg', (0, 0, 0.7, 1)), ('sb/img/p04.jpg', None), ('sb/img/p07.jpg', None), ('luu/img/l12.jpg', None), ('sch/img/s05.jpg', (0, 0, 0.6, 0.55)),
        ('luu/img/l14.jpg', (0.6, 0, 1, 0.5)), ('luu/img/l06.jpg', (0.3, 0.5, 1, 0.85)), ('rommel/img/r05.jpg', (0, 0.3, 1, 1)), ('rommel/img/r23.jpg', (0, 0.15, 0.55, 1)),
        ('rommel/clip/f00045.jpg', None), ('rommel/clip/f01050.jpg', None), ('rommel/clip/f01700.jpg', None), ('rommel/clip/f00960.jpg', (0, 0.2, 1, 1))]
def openp(p):
    path, b = p; im = Image.open(S + path).convert('RGB')
    return im.crop((int(b[0] * im.width), int(b[1] * im.height), int(b[2] * im.width), int(b[3] * im.height))) if b else im
def cover(im, w, h):
    s = max(w / im.width, h / im.height) * rng.uniform(1.0, 1.08); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.BILINEAR)
    x = int((im.width - w) * rng.uniform(0.2, 0.8)); y = int((im.height - h) * rng.uniform(0.1, 0.6)); return im.crop((x, y, x + w, y + h))
def mosaic(w, h, cols, rows, picks, feather):
    out = Image.new('RGB', (w, h), DARK); cw, ch = w / cols, h / rows; k = 0
    cells = [(c, r) for r in range(rows) for c in range(cols)]; rng.shuffle(cells)
    for c, r in cells:
        tw, th = int(cw + 2 * feather), int(ch + 2 * feather); im = cover(openp(picks[k % len(picks)]), tw, th); k += 1
        m = Image.new('L', (tw, th), 0); ImageDraw.Draw(m).rectangle((feather, feather, tw - feather, th - feather), fill=255); m = m.filter(ImageFilter.GaussianBlur(feather / 2))
        out.paste(im, (int(c * cw - feather + rng.uniform(-15, 15)), int(r * ch - feather + rng.uniform(-15, 15))), m)
    return out
def look(im, blur, dark):   # sepia leaning, unlike the cold grey CDM look
    im = im.filter(ImageFilter.GaussianBlur(blur)); im = ImageEnhance.Color(im).enhance(0.25)
    im = Image.blend(im, Image.new('RGB', im.size, (70, 56, 36)), 0.18); im = ImageEnhance.Contrast(im).enhance(1.1)
    return Image.blend(im, Image.new('RGB', im.size, (10, 10, 11)), dark)
def grain(im, amt=5):
    a = np.asarray(im.convert('RGB')).astype(np.int16); a = a + rng.normal(0, amt, a.shape[:2])[..., None].astype(np.int16)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def shadow(can, fn, blur, off=(8, 12), a=200):
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L), (0, 0, 0, a)); can.alpha_composite(L.filter(ImageFilter.GaussianBlur(blur)), off)
def monogram(can, cx, cy, size):
    """white C, P on the yellow plate, red rule: the CDM idea in Oswald"""
    f = oswald(size); d = ImageDraw.Draw(can); wc = d.textlength('C', font=f); wp = d.textlength('P', font=f); gap, pad = size * 0.06, size * 0.09
    x0 = cx - (wc + gap + wp + 2 * pad) / 2; b = d.textbbox((x0 + wc + gap + pad, cy), 'P', font=f, anchor='lm'); plate = (b[0] - pad, b[1] - size * 0.08, b[2] + pad, b[3] + size * 0.07)
    shadow(can, lambda dd, c: (dd.text((x0, cy), 'C', font=f, fill=c, anchor='lm'), dd.rectangle(plate, fill=c)), size * 0.05)
    d = ImageDraw.Draw(can); d.text((x0, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle(plate, fill=YEL); d.text((x0 + wc + gap + pad, cy), 'P', font=f, fill=DARK, anchor='lm')
    d.rectangle((plate[0], plate[3] + size * 0.06, plate[0] + size * 0.32, plate[3] + size * 0.095), fill=RED)
def wordmark(can, cx, cy, size):
    f = oswald(size); d = ImageDraw.Draw(can); t1, t2 = 'CHRONICLE', 'OF POWER'; w1 = d.textlength(t1, font=f); w2 = d.textlength(t2, font=f); gap, pad = size * 0.22, size * 0.14
    x0 = cx - (w1 + gap + w2 + 2 * pad) / 2; b = d.textbbox((x0 + w1 + gap + pad, cy), t2, font=f, anchor='lm'); plate = (b[0] - pad, b[1] - size * 0.1, b[2] + pad, b[3] + size * 0.09)
    shadow(can, lambda dd, c: (dd.text((x0, cy), t1, font=f, fill=c, anchor='lm'), dd.rectangle(plate, fill=c)), size * 0.06)
    d = ImageDraw.Draw(can); d.text((x0, cy), t1, font=f, fill=WHITE, anchor='lm'); d.rectangle(plate, fill=YEL); d.text((x0 + w1 + gap + pad, cy), t2, font=f, fill=DARK, anchor='lm')
    d.rectangle((plate[0], plate[3] + size * 0.09, plate[0] + size * 1.1, plate[3] + size * 0.13), fill=RED)
    return plate[3]

picks = list(POOL); rng.shuffle(picks)
av = look(mosaic(1024, 1024, 3, 3, picks, 60), 4, 0.5).convert('RGBA')
vg = Image.new('L', (1024, 1024), 0); ImageDraw.Draw(vg).ellipse((60, 60, 964, 964), fill=255); vg = vg.filter(ImageFilter.GaussianBlur(120))
av = Image.composite(av, Image.new('RGBA', av.size, (8, 9, 11, 255)), vg); monogram(av, 512, 490, 430)
av = grain(av); av.save(D + 'CoP_Avatar_1024.jpg', quality=95)

W, H = 2560, 1440; rng.shuffle(picks)
bn = look(mosaic(W, H, 5, 3, picks, 90), 5, 0.5).convert('RGBA')
sh = Image.new('RGBA', bn.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((420, 520, 2140, 930), fill=(0, 0, 0, 170)); bn.alpha_composite(sh.filter(ImageFilter.GaussianBlur(90)))
yb = wordmark(bn, W / 2, 668, 148)
d = ImageDraw.Draw(bn); line = 'World War I  ·  World War II  ·  The People Who Shaped Them'
shadow(bn, lambda dd, c: dd.text((W / 2, yb + 98), line, font=playfair(50, 500), fill=c, anchor='mm'), 8, (3, 5))
ImageDraw.Draw(bn).text((W / 2, yb + 98), line, font=playfair(50, 500), fill=CREAM, anchor='mm')
bn = grain(bn); bn.save(D + 'CoP_Banner_2560x1440.jpg', quality=93)

# overview: banner with YouTube safe areas (TV full, desktop 2560x423, mobile/all devices 1546x423), avatar large and tiny
ov = Image.new('RGB', (1920, 1500), (16, 16, 18)); b2 = bn.resize((1920, 1080)); dd = ImageDraw.Draw(b2)
s = 1920 / 2560; dd.rectangle((0, (1440 - 423) / 2 * s, 1920, (1440 + 423) / 2 * s), outline=(90, 200, 255), width=3)
dd.rectangle(((2560 - 1546) / 2 * s, (1440 - 423) / 2 * s, (2560 + 1546) / 2 * s, (1440 + 423) / 2 * s), outline=(255, 90, 90), width=3)
ov.paste(b2, (0, 0))
m = Image.new('L', (300, 300), 0); ImageDraw.Draw(m).ellipse((0, 0, 300, 300), fill=255); ov.paste(av.resize((300, 300)), (700, 1140), m)
m2 = Image.new('L', (48, 48), 0); ImageDraw.Draw(m2).ellipse((0, 0, 48, 48), fill=255); ov.paste(av.resize((48, 48)), (1140, 1266), m2)
ov.save(D + 'CoP_Overview.jpg', quality=90); print('ok')
