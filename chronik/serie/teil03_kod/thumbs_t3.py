# three 16:9 thumbnails for Teil 3 (same layout as Teil 2): (A) Blitzkrieg? with a German tank, (B) Poland attacked from two sides (map), (C) Poland in five weeks (Warsaw burning)
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(os.path.dirname(HERE)) + '/'
sys.path.insert(0, SP + 'teil1/covlib'); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
import lib9 as L
TW, TH = 1280, 720; O = SP + 't3l/thumbs/'; C = SP + 't3l/img/'
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
PL = 'DEUTSCHLAND IM 2. WELTKRIEG · TEIL 3'
# (A) German troops at the Arc de Triomphe, "6 WOCHEN"
def thumb_a():
    im = cover(C + 'paris_parade.jpg', 0.9, 0.6, 1.0); left_shade(im, 0.62, 225)
    txt(im, (60, 150), 'FRANKREICH FIEL IN', 84, WHITE, maxw=640); txt(im, (60, 262), '6 WOCHEN', 160, YEL, maxw=640)
    txt(im, (64, 460), 'Der Westfeldzug, Mai bis Juni 1940', 50, WHITE, maxw=600)
    plate(im, (70, 612), PL, 32); logo(im)
    im.convert('RGB').save(O + 'Teil3_A_Sechs_Wochen.jpg', quality=93)
def arrow(d, a, b, col, wd=22):
    ang = math.atan2(b[1] - a[1], b[0] - a[0]); hd = 58; E = (b[0] - 30 * math.cos(ang), b[1] - 30 * math.sin(ang))
    d.line((a, E), fill=col, width=wd)
    d.polygon([(b[0], b[1]), (b[0] - hd * math.cos(ang - 0.55), b[1] - hd * math.sin(ang - 0.55)), (b[0] - hd * math.cos(ang + 0.55), b[1] - hd * math.sin(ang + 0.55))], fill=col)
# (B) the map: the cut through the Ardennes from Sedan to the Channel
def thumb_b():
    os.chdir(SP + 't3l/code'); import lmap
    m = lmap.Map('thb3', (TW, TH), (560, 10, 720, 700), -2.0, 8.8, 47.2)
    yy, xx = np.mgrid[0:TH, 0:TW].astype(np.float32)
    bg = (20 + 16 * np.exp(-(((xx - 900) / 600) ** 2 + ((yy - 360) / 420) ** 2)))[..., None].repeat(3, 2)
    can = Image.fromarray(bg.astype(np.uint8)).convert('RGBA')
    for n, col in (('Germany', (58, 60, 64)), ('UK', (58, 60, 64)), ('Belgium', (150, 148, 142)), ('Netherlands', (150, 148, 142)), ('Luxembourg', (150, 148, 142)), ('France', (232, 226, 214))):
        M = m.mask(n); lay = Image.new('RGBA', can.size, col + (0,)); lay.putalpha(M); can.alpha_composite(lay)
    for n in ('Germany', 'France', 'Belgium', 'Netherlands'):
        o = m.outline(n, 5); lay = Image.new('RGBA', can.size, (14, 14, 16, 0)); lay.putalpha(o); can.alpha_composite(lay)
    d = ImageDraw.Draw(can); P = m.mp
    arrow(d, P(7.2, 50.0), P(4.95, 49.7), RED, 26); arrow(d, P(4.95, 49.7), P(1.9, 50.15), RED, 26)
    for nm, ll in (('SEDAN', (4.95, 49.7)), ('ABBEVILLE', (1.83, 50.1)), ('PARIS', (2.35, 48.86))):
        x, y = P(*ll); d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=DARK); d.text((x, y + 32), nm, font=osw(28), fill=DARK, anchor='mm')
    left_shade(can, 0.5, 200)
    txt(can, (60, 150), 'DURCH DIE', 110, WHITE, maxw=520); txt(can, (60, 280), 'ARDENNEN', 128, YEL, maxw=520)
    txt(can, (64, 450), 'Der Plan, den keiner erwartete', 46, WHITE, maxw=500)
    plate(can, (70, 612), PL, 32); logo(can)
    can.convert('RGB').save(O + 'Teil3_B_Ardennen.jpg', quality=93)
# (C) Hitler and his entourage at the 1918 railway carriage, "DERSELBE WAGEN"
def thumb_c():
    im = cover(C + 'comp_hitler.jpg', 0.8, 0.4, 1.15); left_shade(im, 0.6, 225)
    txt(im, (60, 150), 'COMPIÈGNE 1940', 84, WHITE, maxw=600); txt(im, (60, 262), 'DERSELBE WAGEN', 130, YEL, maxw=620)
    txt(im, (64, 452), 'Wie 1918, nur umgekehrt', 50, WHITE, maxw=600)
    plate(im, (70, 612), PL, 32); logo(im)
    im.convert('RGB').save(O + 'Teil3_C_Derselbe_Wagen.jpg', quality=93)
os.makedirs(O, exist_ok=True)
thumb_a(); thumb_b(); thumb_c()
P_ = Image.new('RGB', (TW, TH * 3))
for i, f in enumerate(('Teil3_A_Sechs_Wochen.jpg', 'Teil3_B_Ardennen.jpg', 'Teil3_C_Derselbe_Wagen.jpg')): P_.paste(Image.open(O + f), (0, i * TH))
P_.resize((TW // 2, TH * 3 // 2)).save(SP + 't3l/chk/thumbs.jpg', quality=88); print('ok')
