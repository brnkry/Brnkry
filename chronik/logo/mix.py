# style B "CDM" logo and banner over a blurred mosaic of many archive photos
import sys, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D = sys.argv[1] + '/'; S = D + '../'; F = S + 'sch/fonts/'
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
anton = lambda s: ImageFont.truetype(F + 'Anton-Regular.ttf', s); bebas = lambda s: ImageFont.truetype(F + 'BebasNeue-Regular.ttf', s)
rng = np.random.default_rng(11)
POOL = sorted(glob.glob(S + 'luu/img/l*.jpg')) + sorted(glob.glob(S + 'sch/img/s*.jpg')) + sorted(glob.glob(S + 'sb/img/p*.jpg')) + sorted(glob.glob(S + 'thumb/src/i*.jpg'))
def cover(im, w, h):
    s = max(w / im.width, h / im.height) * rng.uniform(1.0, 1.25); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.BILINEAR)
    x = int((im.width - w) * rng.uniform(0.2, 0.8)); y = int((im.height - h) * rng.uniform(0.1, 0.6)); return im.crop((x, y, x + w, y + h))
def mosaic(w, h, cols, rows, picks, feather):
    """photos in a loose grid, each tile larger than its cell and feathered so they melt into each other"""
    out = Image.new('RGB', (w, h), DARK); cw, ch = w / cols, h / rows; k = 0
    cells = [(c, r) for r in range(rows) for c in range(cols)]; rng.shuffle(cells)
    for c, r in cells:
        tw, th = int(cw + 2 * feather), int(ch + 2 * feather)
        im = cover(Image.open(picks[k % len(picks)]).convert('RGB'), tw, th); k += 1
        m = Image.new('L', (tw, th), 0); ImageDraw.Draw(m).rectangle((feather, feather, tw - feather, th - feather), fill=255); m = m.filter(ImageFilter.GaussianBlur(feather / 2))
        out.paste(im, (int(c * cw - feather + rng.uniform(-15, 15)), int(r * ch - feather + rng.uniform(-15, 15))), m)
    return out
def look(im, blur, dark):
    im = im.filter(ImageFilter.GaussianBlur(blur)); im = ImageEnhance.Color(im).enhance(0.5); im = ImageEnhance.Contrast(im).enhance(1.1)
    return Image.blend(im, Image.new('RGB', im.size, (10, 11, 13)), dark)
def grain(im, amt=5):
    a = np.asarray(im.convert('RGB')).astype(np.int16); a = a + rng.normal(0, amt, a.shape[:2])[..., None].astype(np.int16)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def cdm(can, cx, cy, size, shadow=True):
    """white C, then DM on a yellow plate, red rule under the plate"""
    d = ImageDraw.Draw(can); f = anton(size); wc = d.textlength('C', font=f); wd = d.textlength('DM', font=f); gap, pad = size * 0.08, size * 0.07
    x0 = cx - (wc + gap + wd + 2 * pad) / 2
    b = d.textbbox((x0 + wc + gap + pad, cy), 'DM', font=f, anchor='lm')
    if shadow:
        sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
        ds.text((x0 + 8, cy + 12), 'C', font=f, fill=(0, 0, 0, 210), anchor='lm'); ds.rectangle((b[0] - pad + 8, b[1] - size * 0.07 + 12, b[2] + pad + 8, b[3] + size * 0.06 + 12), fill=(0, 0, 0, 190))
        can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(size * 0.05))); d = ImageDraw.Draw(can)
    d.text((x0, cy), 'C', font=f, fill=WHITE, anchor='lm')
    d.rectangle((b[0] - pad, b[1] - size * 0.07, b[2] + pad, b[3] + size * 0.06), fill=YEL)
    d.text((x0 + wc + gap + pad, cy), 'DM', font=f, fill=DARK, anchor='lm')
    d.rectangle((b[0] - pad, b[3] + size * 0.12, b[0] + size * 0.37, b[3] + size * 0.155), fill=RED)

# avatar 1024: 4x4 mosaic
picks = list(POOL); rng.shuffle(picks)
av = look(mosaic(1024, 1024, 4, 4, picks, 60), 5, 0.5).convert('RGBA')
vg = Image.new('L', (1024, 1024), 0); ImageDraw.Draw(vg).ellipse((60, 60, 964, 964), fill=255); vg = vg.filter(ImageFilter.GaussianBlur(120))
av = Image.composite(av, Image.new('RGBA', av.size, (8, 9, 11, 255)), vg); cdm(av, 512, 500, 380)
grain(av).save(D + 'CDM_Avatar_Mix.jpg', quality=95)
# banner 2560x1440: 9x5 mosaic, title in the safe area
W, H = 2560, 1440; rng.shuffle(picks)
bn = look(mosaic(W, H, 9, 5, picks, 70), 7, 0.55).convert('RGBA'); d = ImageDraw.Draw(bn)
sh = Image.new('RGBA', bn.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((420, 520, 2140, 930), fill=(0, 0, 0, 160)); bn.alpha_composite(sh.filter(ImageFilter.GaussianBlur(90)))
d = ImageDraw.Draw(bn); cy = 680; f1 = anton(186); t1, t2 = 'CHRONIK', 'DER MACHT'
w1 = d.textlength(t1, font=f1); w2 = d.textlength(t2, font=f1); gap, pad = 48, 34; x0 = W / 2 - (w1 + gap + w2 + 2 * pad) / 2
d.text((x0, cy), t1, font=f1, fill=WHITE, anchor='lm')
b = d.textbbox((x0 + w1 + gap + pad, cy), t2, font=f1, anchor='lm'); d.rectangle((b[0] - pad, b[1] - 30, b[2] + pad, b[3] + 26), fill=YEL)
d.text((x0 + w1 + gap + pad, cy), t2, font=f1, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + 38, b[0] + 220, b[3] + 50), fill=RED)
d.text((W / 2, 888), 'GESCHICHTE  ·  QUELLEN  ·  ORIGINALAUFNAHMEN', font=bebas(80), fill=(215, 210, 200), anchor='mm')
grain(bn).save(D + 'CDM_Banner_Mix.jpg', quality=93)
# overview: banner, avatar big and at real size
O = Image.new('RGB', (1920, 1440), (12, 12, 12)); O.paste(bn.convert('RGB').resize((1920, 1080)), (0, 0))
a = av.convert('RGB').resize((300, 300), Image.LANCZOS); m = Image.new('L', (300, 300), 0); ImageDraw.Draw(m).ellipse((0, 0, 299, 299), fill=255)
O.paste(a, (700, 1110), m); O.paste(a.resize((56, 56), Image.LANCZOS), (1140, 1232), m.resize((56, 56)))
O.save(D + 'CDM_Mix_Uebersicht.jpg', quality=88); print(len(POOL))
