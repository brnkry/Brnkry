# 9:16 covers in the layout Boran picked (the Yamamoto CoP cover): full-bleed portrait, channel logo centred on top,
# two big lines (white, then yellow) in the lower middle, a yellow plate with dark text and a red rule under it
from lib9 import *
from thumb_m import T
def logo(can, cx, cy, h, a, b):
    """white letter(s) a, then b on a yellow plate, short red rule under the plate (CDM / CP)"""
    d = ImageDraw.Draw(can); f = anton(int(h * 0.82)); wa = d.textlength(a, font=f); wb = d.textlength(b, font=f); pad = h * 0.08
    x = cx - (wa + wb + 3 * pad) / 2; d.text((x, cy), a, font=f, fill=WHITE, anchor='lm'); xb = x + wa + 2 * pad
    bb = d.textbbox((xb, cy), b, font=f, anchor='lm'); d.rectangle((bb[0] - pad, bb[1] - h * 0.07, bb[2] + pad, bb[3] + h * 0.06), fill=YEL)
    d.text((xb, cy), b, font=f, fill=DARK, anchor='lm'); d.rectangle((bb[0] - pad, bb[3] + h * 0.13, bb[0] + h * 0.45, bb[3] + h * 0.18), fill=RED)
def fullbleed(n, x0, y0, s):
    im = src(n); return im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + W / s, y0 + H / s)).convert('RGBA')
def shadeband(can):
    """dark top edge behind the logo and a long dark ramp under the text, the photo stays full screen"""
    y = np.arange(H, dtype=np.float32); g = np.clip((180 - y) / 180, 0, 1) * 120 + np.clip((y - 720) / 520, 0, 1) ** 1.3 * 215
    L = Image.new('RGBA', (W, H), (6, 7, 9, 0)); L.putalpha(Image.fromarray(np.repeat(np.clip(g, 0, 255)[:, None], W, 1).astype(np.uint8))); can.alpha_composite(L)
def plate(can, s_, y, size=46):
    d = ImageDraw.Draw(can); f = anton(size); b = d.textbbox((CX, y), s_, font=f, anchor='mm'); x0, x1 = b[0] - 22, b[2] + 22
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((x0 + 4, b[1] - 10, x1 + 4, b[3] + 16), fill=(0, 0, 0, 160)); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(can); d.rectangle((x0, b[1] - 12, x1, b[3] + 12), fill=YEL); d.text((CX, y), s_, font=f, fill=DARK, anchor='mm')
    d.rectangle((x0 + 4, b[3] + 26, x0 + 150, b[3] + 33), fill=RED)
def cover(n, x0, y0, s, mark, l1, l2, sub, out):
    can = fullbleed(n, x0, y0, s); shadeband(can); logo(can, CX, 250, 80, *mark)
    T(can, (CX, 985), l1, 150, WHITE, maxw=960); T(can, (CX, 1135), l2, 170, YEL, maxw=960); plate(can, sub, 1290)
    can.convert('RGB').save(out, quality=93); return can
