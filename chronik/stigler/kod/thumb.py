# channel-style thumbnail: close portraits, big Anton names, surname in yellow
import sys
from base import *
from PIL import ImageEnhance
OUT = B + 'thumb/'

def half(p, cx, cy, w, hgt=960):
    h = w * hgt / 1080
    im = src(p).resize((1080, hgt), Image.LANCZOS, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))
    im = ImageEnhance.Contrast(im).enhance(1.08); im = ImageEnhance.Color(im).enhance(1.06)
    return im.convert('RGBA')

def shadow_text(can, txt, size, col, cx, cy, maxw=1000, track=0):
    size = fit(txt, 'serif', size, maxw, track)
    f = FK['serif'](size); w = textw(txt, 'serif', size, track); asc, desc = f.getmetrics()
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0 = cx - w / 2; y0 = cy - (asc + desc) / 2
    for off, a, r in (((0, 10), 230, 18), ((0, 4), 255, 4)):
        S = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(S)
        ds.text((x0 + off[0], y0 + off[1]), txt, font=f, fill=(0, 0, 0, a)); L.alpha_composite(S.filter(ImageFilter.GaussianBlur(r)))
    d = ImageDraw.Draw(L); d.text((x0, y0), txt, font=f, fill=col + (255,), stroke_width=3, stroke_fill=(10, 10, 12, 255))
    can.alpha_composite(L); return w

def variant_split():
    can = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    can.paste(half('p08', 896, 840, 1340), (0, 0)); can.paste(half('p06', 896, 1010, 1300), (0, 960))
    can.alpha_composite(vgrad(0, 0)); 
    # darken around the seam so the names read clearly
    y = np.arange(H); a = np.clip(1 - np.abs(y - 960) / 330, 0, 1) ** 1.4 * 150
    can.alpha_composite(Image.merge('RGBA', [Image.new('L', (W, H), 0)] * 3 + [Image.fromarray(np.repeat(a[:, None], W, 1).astype(np.uint8))]))
    ImageDraw.Draw(can).line((0, 960, W, 960), fill=GOLD + (255,), width=6)
    shadow_text(can, 'STIGLER', 230, CREAM, 540, 820)
    shadow_text(can, 'BROWN', 230, GOLD, 540, 1105)
    d = ImageDraw.Draw(can); d.ellipse((540 - 58, 960 - 58, 540 + 58, 960 + 58), fill=DEEP + (255,), outline=GOLD + (255,), width=6)
    f = FK['serif'](80); d.text((540 - f.getlength('&') / 2, 960 - 52), '&', font=f, fill=GOLD + (255,))
    can.alpha_composite(VIG)
    return can.convert('RGB')

def variant_hook():
    can = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    can.paste(half('p08', 896, 820, 1500, 1920).resize((1080, 1920)) if False else PCam('p08', 896, 1050, 1250).frame(), (0, 0))
    can.alpha_composite(vgrad(60, 230, 900, 1700))
    shadow_text(can, 'ER SCHOSS', 210, CREAM, 540, 1180)
    shadow_text(can, 'NICHT', 260, GOLD, 540, 1420)
    d = ImageDraw.Draw(can); d.rectangle((300, 1575, 780, 1585), fill=CREAM + (255,))
    can.alpha_composite(VIG)
    return can.convert('RGB')

if __name__ == '__main__':
    a = variant_split(); a.save(OUT + 'thumb_stigler_brown.jpg', quality=93)
    b = variant_hook(); b.save(OUT + 'thumb_er_schoss_nicht.jpg', quality=93)
    S = Image.new('RGB', (540 * 2 + 20, 960), (255, 255, 255)); S.paste(a.resize((540, 960)), (0, 0)); S.paste(b.resize((540, 960)), (560, 0)); S.save(OUT + 'preview.jpg', quality=85)
