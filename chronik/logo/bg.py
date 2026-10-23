# banner and avatar (style B) over blurred archive photos: aircraft, U-boats, airfields
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D = sys.argv[1] + '/'; S = D + '../'; F = S + 'sch/fonts/'
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
anton = lambda s: ImageFont.truetype(F + 'Anton-Regular.ttf', s); bebas = lambda s: ImageFont.truetype(F + 'BebasNeue-Regular.ttf', s)
W, H = 2560, 1440
def cover(im, w, h, cx=0.5, cy=0.5):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = int((im.width - w) * cx); y = int((im.height - h) * cy); return im.crop((x, y, x + w, y + h))
def look(im, blur, dark):
    """blur, mute the colours toward a cold-warm archive tone, darken"""
    im = im.filter(ImageFilter.GaussianBlur(blur)); im = ImageEnhance.Color(im).enhance(0.55)
    return Image.blend(im, Image.new('RGB', im.size, (10, 11, 13)), dark)
def strip(paths, w, h, feather=140):
    """photos side by side with soft seams"""
    n = len(paths); pw = w // n + feather; out = Image.new('RGB', (w, h))
    for i, (p, cx, cy) in enumerate(paths):
        im = cover(Image.open(p).convert('RGB'), pw, h, cx, cy); x = i * (w // n) - feather // 2
        m = Image.new('L', (pw, h), 255); dm = ImageDraw.Draw(m)
        for k in range(feather): v = int(255 * k / feather); dm.line((k, 0, k, h), fill=v) if i else None; dm.line((pw - 1 - k, 0, pw - 1 - k, h), fill=v) if i < n - 1 else None
        out.paste(im, (x, 0), m)
    return out
def title(can):
    d = ImageDraw.Draw(can); cy = 680; f1 = anton(186); t1, t2 = 'CHRONIK', 'DER MACHT'
    w1 = d.textlength(t1, font=f1); w2 = d.textlength(t2, font=f1); gap, pad = 48, 34; x0 = W / 2 - (w1 + gap + w2 + 2 * pad) / 2
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((x0 - 120, 520, x0 + w1 + gap + w2 + 2 * pad + 120, 930), fill=(0, 0, 0, 150)); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(80)))
    d = ImageDraw.Draw(can); d.text((x0, cy), t1, font=f1, fill=WHITE, anchor='lm')
    b = d.textbbox((x0 + w1 + gap + pad, cy), t2, font=f1, anchor='lm'); d.rectangle((b[0] - pad, b[1] - 30, b[2] + pad, b[3] + 26), fill=YEL)
    d.text((x0 + w1 + gap + pad, cy), t2, font=f1, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + 38, b[0] + 220, b[3] + 50), fill=RED)
    d.text((W / 2, 888), 'GESCHICHTE  ·  QUELLEN  ·  ORIGINALAUFNAHMEN', font=bebas(80), fill=(215, 210, 200), anchor='mm')
def grain(im, amt=5):
    a = np.asarray(im.convert('RGB')).astype(np.int16); a = a + np.random.default_rng(2).normal(0, amt, a.shape[:2])[..., None].astype(np.int16)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
# banner 1: five-photo strip
bg = strip([(S + 'sb/img/p11.jpg', 0.5, 0.5), (S + 'sch/img/s03.jpg', 0.5, 0.5), (S + 'luu/img/l12.jpg', 0.55, 0.5), (S + 'sb/img/p04.jpg', 0.45, 0.5), (S + 'sch/img/s05.jpg', 0.5, 0.5)], W, H)
can = look(bg, 9, 0.55).convert('RGBA'); title(can); grain(can).save(D + 'B_Banner_Collage.jpg', quality=93)
# banner 2: one wide aircraft photo
can = look(cover(Image.open(S + 'sb/img/p04.jpg').convert('RGB'), W, H, 0.5, 0.5), 10, 0.52).convert('RGBA'); title(can); grain(can).save(D + 'B_Banner_Flugzeuge.jpg', quality=93)
# banner 3: U-boats at the pier
can = look(cover(Image.open(S + 'sch/img/s03.jpg').convert('RGB'), W, H, 0.5, 0.5), 10, 0.52).convert('RGBA'); title(can); grain(can).save(D + 'B_Banner_UBoote.jpg', quality=93)
# avatars: the C over a blurred photo
for name, p, cx in (('Flugzeug', S + 'luu/img/l12.jpg', 0.6), ('UBoot', S + 'sch/img/s03.jpg', 0.5)):
    a = look(cover(Image.open(p).convert('RGB'), 1024, 1024, cx, 0.5), 7, 0.5).convert('RGBA'); d = ImageDraw.Draw(a)
    sh = Image.new('RGBA', a.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((518, 444), 'C', font=anton(660), fill=(0, 0, 0, 200), anchor='mm'); a.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    d.text((512, 430), 'C', font=anton(660), fill=WHITE, anchor='mm'); d.rectangle((300, 760, 724, 818), fill=YEL); d.rectangle((300, 836, 470, 852), fill=RED)
    grain(a).save(D + f'B_Avatar_{name}.jpg', quality=95)
# overview
O = Image.new('RGB', (1920, 1240), (12, 12, 12)); dd = ImageDraw.Draw(O)
for i, n in enumerate(['B_Banner_Collage', 'B_Banner_Flugzeuge', 'B_Banner_UBoote']): O.paste(Image.open(D + n + '.jpg').resize((960, 540)), ((i % 2) * 960, (i // 2) * 540))
for i, n in enumerate(['B_Avatar_Flugzeug', 'B_Avatar_UBoot']):
    a = Image.open(D + n + '.jpg').resize((300, 300), Image.LANCZOS); m = Image.new('L', (300, 300), 0); ImageDraw.Draw(m).ellipse((0, 0, 299, 299), fill=255)
    O.paste(a, (1000 + i * 420, 600), m); O.paste(a.resize((56, 56), Image.LANCZOS), (1122 + i * 420, 940), m.resize((56, 56)))
O.save(D + 'B_Hintergrund_Uebersicht.jpg', quality=88)
