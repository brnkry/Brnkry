# Series thumbnails v2: one huge word over a full-bleed photo, small part badge
import sys, os
SP = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/'
sys.path.insert(0, SP + 'teil1/covlib'); import lib9 as L
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
TW, TH = 1280, 720; YEL, RED, WHITE, DARK = L.YEL, L.RED, L.WHITE, L.DARK
def osw(s): return L.oswald(s)
def cover(path, fx, fy, zoom, gray=False):
    g = Image.open(path).convert('RGB'); w, h = g.size; sc = max(TW / w, TH / h) * zoom; cw, ch = TW / sc, TH / sc
    x0 = (w - cw) * fx; y0 = (h - ch) * fy
    im = g.resize((TW, TH), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).filter(ImageFilter.UnsharpMask(2, 80, 2))
    im = ImageEnhance.Contrast(im).enhance(1.18)
    return im.convert('RGBA')
def shade(can, side='L', a=235, w0=0.55):
    x = np.arange(TW) / TW; g = np.clip(1 - (x if side == 'L' else 1 - x) / w0, 0, 1) ** 1.3 * a
    v = np.clip((np.arange(TH) / TH - 0.55) / 0.45, 0, 1) ** 1.5 * 170
    A = np.maximum(g[None, :], v[:, None]).astype(np.uint8)
    lay = Image.new('RGBA', can.size, (5, 6, 8, 0)); lay.putalpha(Image.fromarray(A)); can.alpha_composite(lay)
    yy, xx = np.mgrid[0:TH, 0:TW].astype(np.float32); r = np.hypot((xx - TW / 2) / TW, (yy - TH / 2) / TH)
    lay = Image.new('RGBA', can.size, (0, 0, 0, 0)); lay.putalpha(Image.fromarray((np.clip(r - 0.35, 0, 1) * 300).clip(0, 160).astype(np.uint8))); can.alpha_composite(lay)
def word(can, s, x, y, size, col, maxw, anchor='ls'):
    f = osw(size)
    while f.getlength(s) > maxw: size -= 4; f = osw(size)
    La = Image.new('RGBA', can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(La); d.text((x, y), s, font=f, fill=col + (255,), anchor=anchor)
    st = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(st).text((x, y), s, font=f, fill=(0, 0, 0, 255), anchor=anchor, stroke_width=7, stroke_fill=(0, 0, 0, 255))
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 240), (0, 0), st.getchannel('A'))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (6, 10)); can.alpha_composite(st); can.alpha_composite(La)
    return ImageDraw.Draw(can).textbbox((x, y), s, font=f, anchor=anchor)
def badge(can, n, x, y):
    d = ImageDraw.Draw(can); f = osw(60); s = 'TEIL %d' % n; b = d.textbbox((x, y), s, font=f, anchor='la')
    d.rectangle((b[0] - 18, b[1] - 12, b[2] + 18, b[3] + 12), fill=RED + (255,)); d.text((x, y), s, font=f, fill=WHITE, anchor='la')
def logo(can):
    d = ImageDraw.Draw(can); f = osw(40); x, y = TW - 150, 30
    d.rounded_rectangle((x - 10, y - 6, x + 106, y + 52), 6, fill=(8, 9, 11, 200)); d.text((x, y + 23), 'C', font=f, fill=WHITE, anchor='lm')
    b = d.textbbox((x + 30, y + 23), 'DM', font=f, anchor='lm'); d.rectangle((b[0] - 4, b[1] - 4, b[2] + 4, b[3] + 4), fill=YEL); d.text((x + 30, y + 23), 'DM', font=f, fill=DARK, anchor='lm')
def right_photo(path, zoom=1.0, dy=0):
    g = Image.open(path).convert('RGB'); w, h = g.size; sc = TH / h * zoom; g = g.resize((int(w * sc), int(h * sc)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
    g = ImageEnhance.Contrast(g).enhance(1.18)
    can = Image.new('RGBA', (TW, TH), (6, 7, 9, 255)); x0 = TW - g.width + int(g.width * 0.08)
    m = np.clip(np.arange(g.width) / (g.width * 0.35), 0, 1) ** 1.2; M = Image.fromarray(np.repeat((m * 255)[None, :], g.height, 0).astype(np.uint8))
    can.paste(g, (x0, dy), M); return can
def make(src, n, w, out, fx=0.5, fy=0.5, zoom=1.0, side='L', col=None, sub=None, top=False, right=False):
    can = right_photo(src, zoom) if right else cover(src, fx, fy, zoom)
    if top:
        v = np.clip(1 - np.arange(TH) / (TH * 0.5), 0, 1) ** 1.2 * 150; lay = Image.new('RGBA', can.size, (5, 6, 8, 0)); lay.putalpha(Image.fromarray(np.repeat(v[:, None], TW, 1).astype(np.uint8))); can.alpha_composite(lay)
    else: shade(can, side)
    x = 56 if side == 'L' else TW - 56; anc = 'ls' if side == 'L' else 'rs'
    b = word(can, w, x, 390 if top else 650, 220, col or YEL, 900, anc)
    d = ImageDraw.Draw(can); d.rectangle((b[0], b[3] + 14, b[0] + 160, b[3] + 24), fill=RED)
    word(can, sub or 'DEUTSCHLAND IM ZWEITEN WELTKRIEG', x, b[1] - 26, 66, WHITE, 1160, anc)
    badge(can, n, 56, 38); logo(can)
    can.convert('RGB').save(out, quality=93)
if __name__ == '__main__':
    O = SP + 'thn/v4/'; os.makedirs(O, exist_ok=True); K = SP + 'thn/kaynak2/'; T3 = SP + 't3l/img/'; T2 = SP + 't2/c/'
    U = SP + 'thn/up/'
    J = [(U + 'Teil1_Hitler_Rede.jpg', 1, 'AUFSTIEG', 'T1_A', dict(right=True)),
         (U + 'Teil1_B_Reichstagsbrand_1933.jpg', 1, 'BRAND', 'T1_B', dict(fx=0.5, fy=0.2)),
         (U + 'Teil1_C_Chamberlain_Muenchen_1938.jpg', 1, 'MÜNCHEN', 'T1_C', dict(fx=0.62, fy=0.55, zoom=1.6)),
         (U + 'Teil2_Warschau_Soldaten.jpg', 2, 'ÜBERFALL', 'T2_A', dict(fy=0.4)),
         (U + 'Teil2_B_Brand.jpg', 2, 'FEUER', 'T2_B', dict(fy=0.55)),
         (U + 'Teil2_C_Panzer.jpg', 2, 'BLITZKRIEG', 'T2_C', dict(fx=0.6, fy=0.5)),
         (U + 'Teil3_Hitler_Eiffelturm.jpg', 3, 'PARIS', 'T3_A', dict(fy=1.0)),
         (U + 'Teil3_B_Hitler_Salonwagen.jpg', 3, 'RACHE', 'T3_B', dict(fx=0.8, fy=0.3)),
         (U + 'Teil3_C_Duenkirchen.jpg', 3, 'DÜNKIRCHEN', 'T3_C', dict(fy=0.65))]
    for src, n, w, name, kw in J: make(src, n, w, O + name + '.jpg', **kw)
    print('ok')
