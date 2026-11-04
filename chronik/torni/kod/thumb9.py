# Törni: 3 thumbnails (A/B/C), Instagram/Facebook story image + story video frames, reel overlays and end card
import sys, subprocess
from lib import *
from lib import _bg
OUT = B + 'social/'; import os; os.makedirs(OUT, exist_ok=True)

def badge(can, x, y, h=100):
    f = anton(int(h * 0.82)); d = ImageDraw.Draw(can); wc = d.textlength('C', font=f); gap, pad = h * 0.07, h * 0.06; cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'DM', font=f, anchor='lm')
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x - h * 0.22, y - h * 0.16, b[2] + pad + h * 0.22, y + h * 1.12), h * 0.12, fill=(8, 9, 11, 170))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(can)
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.06, b[2] + pad, b[3] + h * 0.05), fill=YEL)
    d.text((xd, cy), 'DM', font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.12, b[0] + h * 0.42, b[3] + h * 0.16), fill=RED)
def shadowed(can, fn, blur=14, off=(5, 9), a=230):
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L))
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, a), (0, 0), L.getchannel('A'))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), off); can.alpha_composite(L)
def T(can, xy, s, font, col=WHITE, anchor='mm'):
    shadowed(can, lambda d: d.text(xy, s, font=font, fill=col + (255,), anchor=anchor))
def arrow(can, a, b, u, col=YEL, w=16, head=46):
    d = ImageDraw.Draw(can); e = (lerp(a[0], b[0], u), lerp(a[1], b[1], u)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
    d.line((a, e), fill=(0, 0, 0, 150), width=w + 8); d.line((a, e), fill=col, width=w)
    d.polygon([(e[0] + 14 * math.cos(ang), e[1] + 14 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))], fill=col)
def plate(can, xy, s, font, bg=YEL, fg=DARK, pad=(28, 12), rule=True):
    d = ImageDraw.Draw(can); b = d.textbbox(xy, s, font=font, anchor='mm')
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((b[0] - pad[0] + 8, b[1] - pad[1] + 10, b[2] + pad[0] + 8, b[3] + pad[1] + 10), fill=(0, 0, 0, 190)); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(can); d.rectangle((b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1]), fill=bg); d.text(xy, s, font=font, fill=fg, anchor='mm')
    if rule: d.rectangle((b[0] - pad[0], b[3] + pad[1] + 14, b[0] - pad[0] + (b[3] - b[1]) * 1.3, b[3] + pad[1] + 24), fill=RED)
def column(n, w, h, cy=0.42, z=1.0):
    im = src(n); cw = min(im.width, im.height * w / h) / z; ch = cw * h / w; c = min(max(im.height * cy, ch / 2), im.height - ch / 2)
    return im.resize((w, h), Image.LANCZOS, box=(im.width / 2 - cw / 2, c - ch / 2, im.width / 2 + cw / 2, c + ch / 2)).convert('RGBA')
def grad(can, a=230, start=0.45):
    hh = can.height; g = (np.clip((np.arange(hh) - hh * start) / (hh * (1 - start)), 0, 1) ** 1.3 * a).astype(np.uint8)
    L = Image.new('RGBA', can.size, (6, 7, 9, 0)); L.putalpha(Image.fromarray(np.repeat(g[:, None], can.width, 1))); can.alpha_composite(L)
def ytlogo(can, cx, cy, s):
    d = ImageDraw.Draw(can); d.rounded_rectangle((cx - s, cy - s * 0.7, cx + s, cy + s * 0.7), s * 0.32, fill=(255, 0, 0))
    d.polygon([(cx - s * 0.3, cy - s * 0.38), (cx - s * 0.3, cy + s * 0.38), (cx + s * 0.42, cy)], fill=WHITE)


# 9:16 cover for the vertical full version (Facebook Reel): three uniforms stacked as bands, title underneath
def thumb9():
    SW, SH = 1080, 1920; can = Image.new('RGBA', (SW, SH), DARK + (255,)); top, bh = 250, 400
    for i, (n, cy, lab, bg) in enumerate([('t06', 0.30, 'FINNLAND', YEL), ('t22', 0.37, 'WAFFEN-SS', WHITE), ('t18', 0.25, 'US ARMY', YEL)]):
        can.alpha_composite(column(n, SW, bh, cy, 1.0), (0, top + i * bh))
        d = ImageDraw.Draw(can); d.line((0, top + i * bh, SW, top + i * bh), fill=YEL, width=8)
        plate(can, (210, top + i * bh + bh - 60), lab, anton(58), bg, DARK, rule=False)
    ImageDraw.Draw(can).line((0, top + 3 * bh, SW, top + 3 * bh), fill=YEL, width=8)
    g = Image.new('RGBA', (SW, SH), (0, 0, 0, 0)); gg = (np.clip((np.arange(SH) - (top + 3 * bh - 160)) / 300, 0, 1) * 235).astype(np.uint8)
    g.putalpha(Image.fromarray(np.repeat(gg[:, None], SW, 1))); can.alpha_composite(g)
    badge(can, SW / 2 - 75, 80, 96)
    T(can, (SW / 2, 1530), '3 UNIFORMEN, 1 MANN', anton(118))
    T(can, (SW / 2, 1690), 'LAURI TÖRNI', anton(150), YEL)
    can.convert('RGB').save(OUT + 'Thumbnail_9x16_Facebook.jpg', quality=93)
thumb9()
