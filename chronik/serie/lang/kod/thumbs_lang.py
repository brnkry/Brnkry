# three 16:9 thumbnails for the long Teil 1: (A) Hitler on the blurred flag, (B) the expansion map, (C) the magazine hook page
import sys, os, math
sys.argv = [sys.argv[0], 'T'] + sys.argv[1:]
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import lang as V
sys.path.insert(0, V.S + 'teil1/covlib'); import lib9 as L
TW, TH = 1280, 720; O = V.LB + 'thumbs/'
YEL, RED, WHITE, DARK = L.YEL, L.RED, L.WHITE, L.DARK
def osw(s): return L.oswald(s)
def txt(can, xy, s, size, col, anchor='la', maxw=700):
    f = osw(size)
    while f.getlength(s) > maxw: size -= 3; f = osw(size)
    La = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(La).text(xy, s, font=f, fill=col + (255,), anchor=anchor)
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 230), (0, 0), La.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)), (4, 6)); can.alpha_composite(La)
    return f
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
def grade(im):
    return ImageEnhance.Contrast(Image.blend(ImageEnhance.Color(im).enhance(0.9), Image.new('RGB', im.size, (92, 70, 40)), 0.06)).enhance(1.08)

# (A) Hitler on the flag
def thumb_a():
    T1 = V.S + 'teil1/'; src = Image.open(T1 + 'cov/raw.png').convert('RGB'); X0, X1, Y0, Y1 = 130, 470, 0, 300
    k = 700 / (X1 - X0); fr = src.crop((X0, Y0, X1, Y1)).resize((700, int((Y1 - Y0) * k)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(3, 80, 2))
    cx, cy, R = (342 - X0) * k, (218 - Y0) * k, 11 * k; m = Image.new('L', fr.size, 0); ImageDraw.Draw(m).ellipse((cx - R, cy - R, cx + R, cy + R), fill=255)
    fr = Image.composite(fr.filter(ImageFilter.GaussianBlur(R * 0.6)), fr, m.filter(ImageFilter.GaussianBlur(R * 0.25)))
    SIL = [(300, 128), (350, 132), (385, 165), (398, 215), (400, 265), (388, 300), (380, 340), (430, 352), (495, 378), (535, 410), (545, 450), (560, 440), (600, 418),
           (640, 425), (650, 470), (615, 500), (580, 500), (560, 520), (560, 600), (130, 600), (120, 540), (105, 500), (92, 455), (100, 415), (140, 405), (170, 415),
           (185, 395), (240, 360), (268, 338), (252, 300), (238, 250), (242, 195), (265, 150)]
    s2 = k / 2; mask = Image.new('L', fr.size, 0); ImageDraw.Draw(mask).polygon([(x * s2, y * s2) for x, y in SIL], fill=255); mask = mask.filter(ImageFilter.GaussianBlur(4))
    yy, xx = np.mgrid[0:TH, 0:TW].astype(np.float32); wave = 40 * np.sin(xx / 200 + yy / 500); band = np.clip(((yy + wave) / (TH / 3)).astype(int), 0, 2)
    cols = np.array([(20, 20, 22), (200, 22, 26), (240, 190, 20)], np.float32); F = cols[band] * (0.78 + 0.22 * np.sin(xx / 140 + yy / 380 + 1.3))[..., None]
    can = ImageEnhance.Brightness(Image.fromarray(F.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).enhance(0.7).convert('RGBA')
    can.paste(fr, (TW - 700 + 60, 70), mask); left_shade(can, 0.55)
    txt(can, (60, 190), 'NIEMAND', 130, WHITE); txt(can, (60, 330), 'HIELT IHN AUF', 112, YEL, maxw=640)
    plate(can, (66, 520), 'DEUTSCHLAND IM 2. WELTKRIEG · TEIL 1', 34); logo(can)
    can.convert('RGB').save(O + 'Teil1_A_Niemand_hielt_ihn_auf.jpg', quality=93)
# (B) the Reich of 1939 as a silhouette filled with the flag colours, on a dark ground
def flagbar(can, x, y, w, h):
    d = ImageDraw.Draw(can)
    for i, c in enumerate(((24, 24, 26), (200, 22, 26), (240, 190, 20))): d.rectangle((x, y + i * h / 3, x + w, y + (i + 1) * h / 3), fill=c)
def thumb_b():
    from PIL import ImageChops
    m = V.MAPE; M_ = None
    for n in ('reich', 'austria', 'sudeten', 'bohemia'): M_ = m.mask(n) if M_ is None else ImageChops.lighter(M_, m.mask(n))
    bb = M_.getbbox(); pad = 30; M_ = M_.crop((bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad))
    sc = min(560 / M_.height, 600 / M_.width); M_ = M_.resize((int(M_.width * sc), int(M_.height * sc)), Image.LANCZOS)
    w, h = M_.size; F = Image.new('RGB', (w, h)); flagbar(F, 0, 0, w, h)
    sh = np.asarray(F, np.float32) * (0.85 + 0.15 * np.sin(np.arange(w) / 60)[None, :, None])
    F = Image.fromarray(sh.clip(0, 255).astype(np.uint8))
    yy, xx = np.mgrid[0:TH, 0:TW].astype(np.float32)
    bg = (22 + 14 * np.exp(-(((xx - 900) / 600) ** 2 + ((yy - 360) / 420) ** 2)))[..., None].repeat(3, 2)
    can = Image.fromarray(bg.astype(np.uint8)).convert('RGBA')
    edge = M_.filter(ImageFilter.MaxFilter(9)); glow = Image.new('RGBA', (w, h), (0, 0, 0, 0)); glow.putalpha(edge.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.8)))
    ox, oy = TW - w - 40, (TH - h) // 2 + 20
    can.alpha_composite(glow, (ox + 10, oy + 14)); can.paste(F, (ox, oy), M_)
    ol = ImageChops.subtract(M_.filter(ImageFilter.MaxFilter(5)), M_); Lo = Image.new('RGBA', (w, h), (245, 240, 230, 0)); Lo.putalpha(ol); can.alpha_composite(Lo, (ox, oy))
    left_shade(can, 0.45, 150)
    txt(can, (60, 170), 'DEUTSCHLAND', 116, WHITE, maxw=560); txt(can, (60, 300), '1919 BIS 1939', 96, YEL, maxw=560)
    txt(can, (62, 420), 'Der Weg in den Krieg', 56, WHITE, maxw=560)
    plate(can, (66, 600), 'IM ZWEITEN WELTKRIEG · TEIL 1', 34); logo(can)
    can.convert('RGB').save(O + 'Teil1_B_Deutschland_1919_bis_1939.jpg', quality=93)
# (C) German tanks rolling, the flag down the left edge
def thumb_c():
    g = V.clip_at('tanks', 1.6); w, h = g.size; cw = h * TW / TH; c = V.tone(g.resize((TW, TH), Image.LANCZOS, box=((w - cw) / 2, 0, (w + cw) / 2, h)))
    im = grade(c.filter(ImageFilter.UnsharpMask(2, 70, 2))).convert('RGBA'); left_shade(im, 0.7, 225)
    flagbar(im, 0, 0, 26, TH)
    txt(im, (66, 140), '1919: KEIN', 104, WHITE, maxw=700); txt(im, (66, 260), 'EINZIGER PANZER', 104, WHITE, maxw=700); txt(im, (66, 390), '1939: KRIEG', 132, YEL, maxw=700)
    plate(im, (72, 620), 'DEUTSCHLAND IM 2. WELTKRIEG · TEIL 1', 32); logo(im)
    im.convert('RGB').save(O + 'Teil1_C_Kein_Panzer_Krieg.jpg', quality=93)
thumb_a(); thumb_b(); thumb_c()
P = Image.new('RGB', (TW, TH * 3))
for i, f in enumerate(('Teil1_A_Niemand_hielt_ihn_auf.jpg', 'Teil1_B_Deutschland_1919_bis_1939.jpg', 'Teil1_C_Kein_Panzer_Krieg.jpg')): P.paste(Image.open(O + f), (0, i * TH))
P.resize((TW // 2, TH * 3 // 2)).save(V.LB + 'chk/thumbs.jpg', quality=88); print('ok')
