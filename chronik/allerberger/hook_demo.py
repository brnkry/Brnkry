# Allerberger hook mock-up: full-bleed blue film, the person cut out and standing IN the scene (rim light, shadow), name + hook line
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops
S = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/'
sys.path.insert(0, S + 'egon/code'); import eg
from eg import mont, gtext_a, put, YEL, CREAM, DARK, LIGHT
W, H = 1080, 1920
def bluefilm(path):
    im = Image.open(path).convert('L'); w, h = im.size; cw = h * 9 / 16; im = im.crop(((w - cw) / 2, 0, (w + cw) / 2, h)).resize((W, H), Image.BICUBIC)
    g = np.asarray(im, np.float32)[..., None] / 255; g = np.clip((g - 0.5) * 1.15 + 0.5, 0, 1)
    a = np.array(DARK, np.float32) + g * (np.array(LIGHT, np.float32) * 1.15 - np.array(DARK, np.float32))
    yy = np.linspace(0, 1, H)[:, None, None]; a *= 1 - 0.55 * np.clip((yy - 0.45) / 0.55, 0, 1)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
can = bluefilm(S + 'kittel/clipL/ice/00200.jpg').filter(ImageFilter.GaussianBlur(2.5))
# person: cut-out, desaturated to a warm archive tone, scaled to stand from the bottom edge
P = Image.open('cut.png'); bb = P.getbbox(); P = P.crop(bb); sc = 1250 / P.height; P = P.resize((int(P.width * sc), 1250), Image.LANCZOS)
rgb = P.convert('RGB'); a = P.getchannel('A')
top = np.clip(np.arange(P.height) / 90.0, 0, 1)[:, None] * np.clip(np.arange(P.width) / 90.0, 0, 1)[None, :]
a = Image.fromarray((np.asarray(a, np.float32) * top).astype(np.uint8))
x0, y0 = W - P.width + 120, H - P.height + 40
# rim light: a cream edge glow behind the figure
glow = Image.new('RGBA', can.size, (0, 0, 0, 0)); gm = Image.new('L', can.size, 0); gm.paste(a.filter(ImageFilter.MaxFilter(9)), (x0, y0))
glow.paste((235, 220, 190, 255), (0, 0), gm.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.75))); can.alpha_composite(glow)
sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sm = Image.new('L', can.size, 0); sm.paste(a, (x0 - 30, y0 + 20)); sh.paste((0, 0, 0, 255), (0, 0), sm.filter(ImageFilter.GaussianBlur(25)).point(lambda v: int(v * 0.6))); can.alpha_composite(sh)
fig = Image.new('RGBA', can.size, (0, 0, 0, 0)); fig.paste(rgb, (x0, y0)); fm = Image.new('L', can.size, 0); fm.paste(a, (x0, y0)); fig.putalpha(fm); can.alpha_composite(fig)
# bottom fade so the text sits on dark
v = (np.clip((np.arange(H) / H - 0.62) / 0.38, 0, 1) ** 1.4 * 200).astype(np.uint8); L_ = Image.new('RGBA', can.size, (8, 9, 14, 0)); L_.putalpha(Image.fromarray(np.repeat(v[:, None], W, 1))); can.alpha_composite(L_)
# type
def line(s, y, size, col, x=60):
    f = mont(size, 900); put(can, gtext_a(s, f, col, [1] * len(s), -2), x, y, 'l')
line('JOSEF', 300, 90, CREAM); line('„SEPP“', 395, 90, YEL); line('ALLERBERGER', 490, 96, CREAM)
d = ImageDraw.Draw(can); d.rectangle((66, 560, 246, 570), fill=(200, 40, 40))
line('DER ZWEIT-', 1380, 64, CREAM); line('ERFOLGREICHSTE', 1450, 64, YEL); line('SCHARFSCHÜTZE', 1520, 64, YEL); line('DER WEHRMACHT', 1590, 64, CREAM)
d.text((W - 30, H - 30), 'Platzhalter-Foto', font=mont(22, 500), fill=(255, 255, 255, 120), anchor='rs')
for cx, cy, r in ((535, 752, 22), (440, 1668, 24), (686, 1609, 18)):
    m = Image.new('L', can.size, 0); ImageDraw.Draw(m).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    can = Image.composite(can.filter(ImageFilter.GaussianBlur(7)), can, m.filter(ImageFilter.GaussianBlur(3)))
can = eg.finish(can, 1.0)
can.convert('RGB').save('Allerberger_Hook_Beispiel.jpg', quality=92); print('ok')
