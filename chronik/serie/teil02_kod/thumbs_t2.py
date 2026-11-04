# three 16:9 thumbnails for Teil 2: (A) Blitzkrieg? with a German tank, (B) Poland attacked from two sides (map), (C) Poland in five weeks (Warsaw burning)
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(os.path.dirname(HERE)) + '/'
sys.path.insert(0, SP + 'teil1/covlib'); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
import lib9 as L
TW, TH = 1280, 720; O = SP + 't2l/thumbs/'; C = SP + 't2/c/'
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
# (A) a German tank in the dust, "BLITZKRIEG?"
def thumb_a():
    im = cover(C + 'hoffmann_s39_0.jpg', 0.85, 0.45, 1.0); left_shade(im, 0.62, 225)
    txt(im, (60, 150), 'DER ERSTE', 92, WHITE, maxw=640); txt(im, (60, 262), 'BLITZKRIEG?', 150, YEL, maxw=640)
    txt(im, (64, 452), 'Der Überfall auf Polen 1939', 50, WHITE, maxw=600)
    plate(im, (70, 612), 'DEUTSCHLAND IM 2. WELTKRIEG · TEIL 2', 32); logo(im)
    im.convert('RGB').save(O + 'Teil2_A_Erster_Blitzkrieg.jpg', quality=93)
# (B) the map: Poland between the Reich and the Soviet Union, red arrows from west, north, south and east
def arrow(d, a, b, col, wd=22):
    ang = math.atan2(b[1] - a[1], b[0] - a[0]); hd = 58; E = (b[0] - 30 * math.cos(ang), b[1] - 30 * math.sin(ang))
    d.line((a, E), fill=col, width=wd)
    d.polygon([(b[0], b[1]), (b[0] - hd * math.cos(ang - 0.55), b[1] - hd * math.sin(ang - 0.55)), (b[0] - hd * math.cos(ang + 0.55), b[1] - hd * math.sin(ang + 0.55))], fill=col)
def thumb_b():
    os.chdir(SP + 't2l/code'); import lmap
    m = lmap.Map('thb', (TW, TH), (610, 10, 690, 700), 12.8, 29.4, 47.8)
    yy, xx = np.mgrid[0:TH, 0:TW].astype(np.float32)
    bg = (20 + 16 * np.exp(-(((xx - 900) / 600) ** 2 + ((yy - 360) / 420) ** 2)))[..., None].repeat(3, 2)
    can = Image.fromarray(bg.astype(np.uint8)).convert('RGBA')
    for n, col in (('reich', (58, 60, 64)), ('danzig', (58, 60, 64)), ('ussr', (58, 60, 64)), ('poland', (232, 226, 214))):
        M = m.mask(n); lay = Image.new('RGBA', can.size, col + (0,)); lay.putalpha(M); can.alpha_composite(lay)
    for n in ('reich', 'ussr', 'poland'):
        o = m.outline(n, 5); lay = Image.new('RGBA', can.size, (14, 14, 16, 0)); lay.putalpha(o); can.alpha_composite(lay)
    d = ImageDraw.Draw(can); P = m.mp
    for a, b in (((14.2, 52.3), (18.6, 52.2)), ((16.6, 54.4), (19.0, 53.0)), ((20.5, 54.6), (20.9, 53.0)), ((17.0, 50.0), (19.6, 50.9)), ((20.6, 48.3), (21.3, 49.9)),
                 ((28.8, 53.6), (25.3, 53.0)), ((28.6, 51.4), (25.0, 51.4)), ((28.2, 49.4), (24.9, 49.9))):
        arrow(d, P(*a), P(*b), RED)
    wx, wy = P(21.01, 52.23); d.ellipse((wx - 9, wy - 9, wx + 9, wy + 9), fill=DARK)
    d.text((wx, wy + 32), 'WARSCHAU', font=osw(30), fill=DARK, anchor='mm')
    for s, ll in (): d.text(P(*ll), s, font=osw(30), fill=(190, 190, 186), anchor='mm')
    left_shade(can, 0.5, 200)
    txt(can, (60, 150), 'VON ZWEI', 128, WHITE, maxw=560); txt(can, (60, 290), 'SEITEN', 128, YEL, maxw=560)
    txt(can, (64, 450), 'Polen, September 1939', 50, WHITE, maxw=520)
    plate(can, (70, 612), 'DEUTSCHLAND IM 2. WELTKRIEG · TEIL 2', 32); logo(can)
    can.convert('RGB').save(O + 'Teil2_B_Von_zwei_Seiten.jpg', quality=93)
# (C) Warsaw burning, "5 WOCHEN"
def thumb_c():
    im = cover(C + 'hoffmann_s86_0.jpg', 0.75, 0.85, 1.35); left_shade(im, 0.6, 220)
    txt(im, (60, 150), 'POLEN FIEL IN', 92, WHITE, maxw=640); txt(im, (60, 262), '5 WOCHEN', 160, YEL, maxw=640)
    txt(im, (64, 460), 'Der Überfall vom September 1939', 50, WHITE, maxw=600)
    plate(im, (70, 612), 'DEUTSCHLAND IM 2. WELTKRIEG · TEIL 2', 32); logo(im)
    im.convert('RGB').save(O + 'Teil2_C_Fuenf_Wochen.jpg', quality=93)
thumb_a(); thumb_b(); thumb_c()
P_ = Image.new('RGB', (TW, TH * 3))
for i, f in enumerate(('Teil2_A_Erster_Blitzkrieg.jpg', 'Teil2_B_Von_zwei_Seiten.jpg', 'Teil2_C_Fuenf_Wochen.jpg')): P_.paste(Image.open(O + f), (0, i * TH))
P_.resize((TW // 2, TH * 3 // 2)).save(SP + 't2l/chk/thumbs.jpg', quality=88); print('ok')
