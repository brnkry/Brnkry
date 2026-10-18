# banner variants with the social icons row: YouTube banner 2560x1440 and Facebook cover 1640x624, same design
import sys
src = open(sys.argv[1] + '/bg.py').read(); exec(src[:src.index('def title(can):')]); exec(src[src.index('def grain'):src.index('# banner 1')])
def icons(can, cx, cy, s, label):
    """white YouTube, Instagram and Facebook marks in a row, then the account name"""
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); w = int(s * 0.08)
    f = bebas(int(s * 0.95)); tw = d.textlength(label, font=f); gap = s * 0.35
    tot = 3 * s + 2 * gap + gap * 1.3 + tw; x = cx - tot / 2; y0 = cy - s / 2
    # YouTube: rounded rect with play triangle cut out
    d.rounded_rectangle((x, y0 + s * 0.15, x + s, y0 + s * 0.85), s * 0.2, fill=WHITE)
    d.polygon([(x + s * 0.40, y0 + s * 0.32), (x + s * 0.40, y0 + s * 0.68), (x + s * 0.70, y0 + s * 0.5)], fill=DARK); x += s + gap
    # Instagram: rounded square outline, ring, dot
    d.rounded_rectangle((x, y0, x + s, y0 + s), s * 0.28, outline=WHITE, width=w)
    d.ellipse((x + s * 0.27, y0 + s * 0.27, x + s * 0.73, y0 + s * 0.73), outline=WHITE, width=w)
    d.ellipse((x + s * 0.70, y0 + s * 0.17, x + s * 0.82, y0 + s * 0.29), fill=WHITE); x += s + gap
    # Facebook: filled circle with an f
    d.ellipse((x, y0, x + s, y0 + s), fill=WHITE)
    d.text((x + s * 0.54, y0 + s * 0.56), 'f', font=ImageFont.truetype(F + 'Anton-Regular.ttf', int(s * 0.95)), fill=DARK, anchor='mm'); x += s + gap * 1.3
    d.text((x, cy + s * 0.04), label, font=f, fill=WHITE, anchor='lm')
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (0, 0), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (3, 5)); can.alpha_composite(L)
def layout(can, w, h, cy, size, tag, ic):
    d = ImageDraw.Draw(can); f1 = anton(size); t1, t2 = 'CHRONIK', 'DER MACHT'
    w1 = d.textlength(t1, font=f1); w2 = d.textlength(t2, font=f1); gap, pad = size * 0.26, size * 0.18; x0 = w / 2 - (w1 + gap + w2 + 2 * pad) / 2
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((x0 - size * 0.6, cy - size * 0.9, x0 + w1 + gap + w2 + 2 * pad + size * 0.6, cy + size * 1.9), fill=(0, 0, 0, 150)); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(size * 0.4)))
    d = ImageDraw.Draw(can); d.text((x0, cy), t1, font=f1, fill=WHITE, anchor='lm')
    b = d.textbbox((x0 + w1 + gap + pad, cy), t2, font=f1, anchor='lm'); d.rectangle((b[0] - pad, b[1] - size * 0.16, b[2] + pad, b[3] + size * 0.14), fill=YEL)
    d.text((x0 + w1 + gap + pad, cy), t2, font=f1, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + size * 0.2, b[0] + size * 1.2, b[3] + size * 0.27), fill=RED)
    d.text((w / 2, cy + size * 0.95), 'GESCHICHTE  ·  QUELLEN  ·  ORIGINALAUFNAHMEN', font=bebas(int(size * 0.4)), fill=(215, 210, 200), anchor='mm')
    icons(can, w / 2, cy + size * 1.5, int(size * 0.4), 'CHRONIK DER MACHT') if ic else None
photo = Image.open(S + 'sb/img/p04.jpg').convert('RGB')
# YouTube banner: everything inside the 1546x423 area at y 508..931
yt = look(cover(photo, 2560, 1440, 0.5, 0.5), 10, 0.52).convert('RGBA'); layout(yt, 2560, 1440, 615, 172, True, True)
grain(yt).save(D + 'Banner_YouTube_Social.jpg', quality=93)
# Facebook cover 1640x624: phones crop the sides, so keep it in the middle 1100 px
fb = look(cover(photo, 1640, 624, 0.5, 0.45), 8, 0.52).convert('RGBA'); layout(fb, 1640, 624, 230, 112, True, True)
grain(fb).save(D + 'Cover_Facebook_Social.jpg', quality=93)
# previews with the visible areas marked
p = yt.copy(); dp = ImageDraw.Draw(p); dp.rectangle((507, 508, 2053, 931), outline=(255, 60, 60), width=6); p.convert('RGB').resize((1280, 720)).save(D + 'Banner_YouTube_Social_preview.jpg', quality=88)
q = fb.copy(); dq = ImageDraw.Draw(q); dq.rectangle((270, 0, 1370, 624), outline=(255, 60, 60), width=4); q.convert('RGB').save(D + 'Cover_Facebook_Social_preview.jpg', quality=88)
