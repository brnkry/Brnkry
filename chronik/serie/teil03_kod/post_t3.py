# three 16:9 thumbnails for Teil 3 (same layout as Teil 2): (A) Blitzkrieg? with a German tank, (B) Poland attacked from two sides (map), (C) Poland in five weeks (Warsaw burning)
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(os.path.dirname(HERE)) + '/'
sys.path.insert(0, SP + 'teil1/covlib'); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
import lib9 as L
TW, TH = 1080, 1080; O = SP + 't3l/thumbs/'; C = SP + 't3l/img/'
YEL, RED, WHITE, DARK = L.YEL, L.RED, L.WHITE, L.DARK
def osw(s): return L.oswald(s)
def txt(can, xy, s, size, col, anchor='la', maxw=700):
    f = osw(size)
    while f.getlength(s) > maxw: size -= 3; f = osw(size)
    La = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(La).text(xy, s, font=f, fill=col + (255,), anchor=anchor)
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 235), (0, 0), La.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)), (4, 6)); can.alpha_composite(La)
    return ImageDraw.Draw(can).textbbox(xy, s, font=f, anchor=anchor)
def plate(can, xy, s, size=34):
    d = ImageDraw.Draw(can); f = osw(size); b = d.textbbox(xy, s, font=f, anchor='la'); px, py = 18, 8
    d.rectangle((b[0] - px, b[1] - py, b[2] + px, b[3] + py), fill=YEL); d.text(xy, s, font=f, fill=DARK, anchor='la'); d.rectangle((b[0] - px, b[3] + py + 8, b[0] - px + 110, b[3] + py + 15), fill=RED)
def logo(can):
    d = ImageDraw.Draw(can); f = osw(46); x, y = 52, 34
    d.rounded_rectangle((x - 12, y - 8, x + 120, y + 58), 6, fill=(8, 9, 11, 200)); d.text((x, y + 25), 'C', font=f, fill=WHITE, anchor='lm')
    b = d.textbbox((x + 34, y + 25), 'DM', font=f, anchor='lm'); d.rectangle((b[0] - 4, b[1] - 4, b[2] + 4, b[3] + 4), fill=YEL); d.text((x + 34, y + 25), 'DM', font=f, fill=DARK, anchor='lm')
def left_shade(can, w0=0.62, a=210):
    g = np.clip(1 - np.arange(TW) / (TW * w0), 0, 1) ** 0.8 * a
    Lg = Image.new('RGBA', can.size, (6, 7, 9, 0)); Lg.putalpha(Image.fromarray(np.repeat(g[None, :].astype(np.uint8), TH, 0))); can.alpha_composite(Lg)
def cover(path, fx=0.5, fy=0.5, zoom=1.0):
    g = Image.open(path).convert('RGB'); w, h = g.size; sc = max(TW / w, TH / h) * zoom; cw, ch = TW / sc, TH / sc
    x0 = (w - cw) * fx; y0 = (h - ch) * fy
    im = g.resize((TW, TH), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).filter(ImageFilter.UnsharpMask(2, 60, 2))
    return ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.05)).enhance(1.08).convert('RGBA')
def strike(can, b, wd=14):
    d = ImageDraw.Draw(can); y0 = (b[1] + b[3]) / 2 + 8
    d.line((b[0] - 10, y0 + 10, b[2] + 10, y0 - 12), fill=RED, width=wd)

im = cover(C + 'paris_parade.jpg', 0.85, 0.5, 1.0); left_shade(im, 0.75, 215)
g = np.clip((np.arange(TH) - 560) / 520, 0, 1) * 200; Lg = Image.new('RGBA', im.size, (6, 7, 9, 0)); Lg.putalpha(Image.fromarray(np.repeat(g[:, None], TW, 1).astype(np.uint8))); im.alpha_composite(Lg)
plate(im, (70, 150), 'TEIL 3 IST DA', 44)
txt(im, (60, 270), 'FRANKREICH FIEL IN', 92, WHITE, maxw=900); txt(im, (60, 390), '6 WOCHEN', 190, YEL, maxw=900)
txt(im, (64, 640), 'Der Krieg im Westen, Mai bis Juni 1940', 52, WHITE, maxw=900)
txt(im, (64, 880), 'DEUTSCHLAND IM ZWEITEN WELTKRIEG', 50, WHITE, maxw=900); txt(im, (64, 950), 'Jetzt auf dem Kanal', 44, YEL, maxw=900)
logo(im); im.convert('RGB').save(SP + 't3l/social/YouTube_Post_Teil3_DE.jpg', quality=93); print('ok')
