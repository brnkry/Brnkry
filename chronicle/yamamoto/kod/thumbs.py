# Yamamoto short covers, 9:16, Chronicle of Power. Everything sits in the middle band (y 330..1450, x 150..930),
# away from the YouTube/Facebook top bar, the right-hand buttons and the bottom title/channel overlay.
import os
from lib9 import *
OUT = B + 'thumbs/'; os.makedirs(OUT, exist_ok=True)
VW, VH = 1080, 1920; MAXW = 760
def sh_(can, fn, blur=14, off=(5, 9), a=230):
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L))
    s = Image.new('RGBA', can.size, (0, 0, 0, 0)); s.paste((0, 0, 0, a), (0, 0), L.getchannel('A'))
    can.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)), off); can.alpha_composite(L)
def fitf(fn, s, size, maxw=MAXW):
    f = fn(size)
    while f.getlength(s) > maxw and size > 20: size -= 4; f = fn(size)
    return f
def T(can, y, s, size, col=WHITE): f = fitf(oswald, s, size); sh_(can, lambda d: d.text((VW / 2, y), s, font=f, fill=col + (255,), anchor='mm'))
def plate(can, y, s, size):
    f = fitf(oswald, s, size, MAXW - 60); d = ImageDraw.Draw(can); b = d.textbbox((VW / 2, y), s, font=f, anchor='mm'); px, py = 28, 14
    s_ = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(s_).rectangle((b[0] - px + 8, b[1] - py + 10, b[2] + px + 8, b[3] + py + 10), fill=(0, 0, 0, 190)); can.alpha_composite(s_.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(can); d.rectangle((b[0] - px, b[1] - py, b[2] + px, b[3] + py), fill=YEL); d.text((VW / 2, y), s, font=f, fill=DARK, anchor='mm')
    d.rectangle((b[0] - px, b[3] + py + 14, b[0] - px + 150, b[3] + py + 24), fill=RED)
def cp(can, x, y, h=84):
    f = oswald(int(h * 0.86)); d = ImageDraw.Draw(can); wc = d.textlength('C', font=f); gap, pad = h * 0.06, h * 0.08; cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'P', font=f, anchor='lm')
    s_ = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(s_).rounded_rectangle((x - h * 0.22, y - h * 0.16, b[2] + pad + h * 0.22, y + h * 1.12), h * 0.12, fill=(8, 9, 11, 170))
    can.alpha_composite(s_.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(can)
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.08, b[2] + pad, b[3] + h * 0.07), fill=YEL)
    d.text((xd, cy), 'P', font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.13, b[0] + h * 0.36, b[3] + h * 0.17), fill=RED)
def raw(n): return Image.open(B + 'img/' + n + '.jpg').convert('RGB')
def cover(im, w, h, cx=0.5, cy=0.42, z=1.0):
    cw = min(im.width, im.height * w / h) / z; ch = cw * h / w
    x0 = min(max(im.width * cx - cw / 2, 0), im.width - cw); y0 = min(max(im.height * cy - ch / 2, 0), im.height - ch)
    return im.resize((w, h), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')
def look(can, sat=0.8, warm=0.12):
    rgb = ImageEnhance.Color(can.convert('RGB')).enhance(sat); rgb = Image.blend(rgb, Image.new('RGB', rgb.size, (92, 70, 40)), warm)
    return ImageEnhance.Contrast(rgb).enhance(1.1).convert('RGBA')
def band(can, y0, y1, a=200):
    """dark soft band behind the text block so it reads on any photo"""
    g = np.zeros(VH, np.float32); yy = np.arange(VH); g = np.clip(np.minimum((yy - y0 + 160) / 160, (y1 + 160 - yy) / 160), 0, 1) * a
    L = Image.new('RGBA', can.size, (6, 7, 9, 0)); L.putalpha(Image.fromarray(np.repeat(g.astype(np.uint8)[:, None], VW, 1))); can.alpha_composite(L)
def save(can, name): can.convert('RGB').save(OUT + name, quality=93); print(name)

def a():   # the man who knew: his face, the warning
    can = look(cover(raw('s3-5'), VW, VH, 0.5, 0.36, 1.12)); band(can, 1050, 1400, 215); cp(can, VW / 2 - 70, 340, 80)
    T(can, 1110, 'HE KNEW JAPAN', 130); T(can, 1250, 'WOULD LOSE', 130, YEL); plate(can, 1400, 'THEN HE PLANNED PEARL HARBOR', 62)
    save(can, 'EN_A_He_Knew.jpg')
def b():   # the hunt: 16 fighters, one target
    can = look(cover(raw('s4-1'), VW, VH, 0.5, 0.45, 1.0)); band(can, 1060, 1380, 215); cp(can, VW / 2 - 70, 340, 80)
    T(can, 1130, '16 FIGHTERS', 150); plate(can, 1320, 'ONE TARGET', 110)
    save(can, 'EN_B_One_Target.jpg')
def c():   # killed by his punctuality
    can = look(cover(raw('s4-3'), VW, VH, 0.35, 0.45, 1.0)); band(can, 1060, 1380, 215); cp(can, VW / 2 - 70, 340, 80)
    T(can, 1120, 'ALWAYS ON TIME', 130); plate(can, 1310, 'IT GOT HIM KILLED', 92)
    save(can, 'EN_C_Always_On_Time.jpg')

if __name__ == '__main__':
    for f in (a, b, c): f()
    ims = [Image.open(OUT + n) for n in ('EN_A_He_Knew.jpg', 'EN_B_One_Target.jpg', 'EN_C_Always_On_Time.jpg')]
    P = Image.new('RGB', (3 * 360, 640)); d = None
    for i, im in enumerate(ims):
        im = im.resize((360, 640)); dd = ImageDraw.Draw(im); s = 360 / VW
        dd.rectangle((0, 0, 360, 290 * s), outline=(0, 255, 255)); dd.rectangle((930 * s, 680 * s, 360, 1580 * s), outline=(0, 255, 255)); dd.rectangle((0, 1580 * s, 360, 640), outline=(0, 255, 255))
        P.paste(im, (i * 360, 0))
    P.save(OUT + '_overview_ui.jpg', quality=85)
