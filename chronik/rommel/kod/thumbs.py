# Rommel thumbnails: German long video (YouTube 16:9 A/B/C, Facebook 9:16 A/B/C, symbols blurred) and English short (9:16 A/B/C, Chronicle of Power, no blur)
import sys, os
from lib import *
OUT = B + 'thumbs/'; os.makedirs(OUT, exist_ok=True)

def oswald(s, wg=700):
    f = ImageFont.truetype(F + 'Oswald%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
def sh_(can, fn, blur=14, off=(5, 9), a=230):
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L))
    s = Image.new('RGBA', can.size, (0, 0, 0, 0)); s.paste((0, 0, 0, a), (0, 0), L.getchannel('A'))
    can.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)), off); can.alpha_composite(L)
def T(can, xy, s, font, col=WHITE, anchor='mm'): sh_(can, lambda d: d.text(xy, s, font=font, fill=col + (255,), anchor=anchor))
def fitf(fn, s, size, maxw):
    f = fn(size)
    while f.getlength(s) > maxw and size > 20: size -= 4; f = fn(size)
    return f
def plate(can, xy, s, font, bg=YEL, fg=DARK, pad=(28, 12), rule=True):
    d = ImageDraw.Draw(can); b = d.textbbox(xy, s, font=font, anchor='mm')
    s_ = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(s_).rectangle((b[0] - pad[0] + 8, b[1] - pad[1] + 10, b[2] + pad[0] + 8, b[3] + pad[1] + 10), fill=(0, 0, 0, 190)); can.alpha_composite(s_.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(can); d.rectangle((b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1]), fill=bg); d.text(xy, s, font=font, fill=fg, anchor='mm')
    if rule: d.rectangle((b[0] - pad[0], b[3] + pad[1] + 14, b[0] - pad[0] + (b[3] - b[1]) * 1.3, b[3] + pad[1] + 24), fill=RED)
def grad(can, a=230, start=0.45, top=0):
    hh = can.height; g = (np.clip((np.arange(hh) - hh * start) / (hh * (1 - start)), 0, 1) ** 1.3 * a)
    if top: g = np.maximum(g, np.clip(1 - np.arange(hh) / (hh * 0.22), 0, 1) * top)
    L = Image.new('RGBA', can.size, (6, 7, 9, 0)); L.putalpha(Image.fromarray(np.repeat(g.astype(np.uint8)[:, None], can.width, 1))); can.alpha_composite(L)
def side(can, a=230, right=False, w=0.6):
    ww = can.width; g = np.clip(1 - np.arange(ww) / (ww * w), 0, 1) ** 1.2 * a
    if right: g = g[::-1]
    L = Image.new('RGBA', can.size, (6, 7, 9, 0)); L.putalpha(Image.fromarray(np.tile(g.astype(np.uint8), (can.height, 1)))); can.alpha_composite(L)
def raw(n): return Image.open(B + 'img/' + n + '.jpg').convert('RGB') if n != 'h01' else Image.open(B + '../en/img/h01.jpg').convert('RGB')
def cover(im, w, h, cx=0.5, cy=0.42, z=1.0):
    cw = min(im.width, im.height * w / h) / z; ch = cw * h / w
    x0 = min(max(im.width * cx - cw / 2, 0), im.width - cw); y0 = min(max(im.height * cy - ch / 2, 0), im.height - ch)
    return im.resize((w, h), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')
def clipframe(sec): return Image.open(B + 'clip/f%05d.jpg' % (int(sec * 30) + 1)).convert('RGB')
def look(can, sat=0.85, warm=0.0):
    rgb = ImageEnhance.Color(can.convert('RGB')).enhance(sat)
    if warm: rgb = Image.blend(rgb, Image.new('RGB', rgb.size, (92, 70, 40)), warm)
    return ImageEnhance.Contrast(rgb).enhance(1.1).convert('RGBA')
def cdm(can, x, y, h=100):
    f = anton(int(h * 0.82)); d = ImageDraw.Draw(can); wc = d.textlength('C', font=f); gap, pad = h * 0.07, h * 0.06; cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'DM', font=f, anchor='lm')
    s_ = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(s_).rounded_rectangle((x - h * 0.22, y - h * 0.16, b[2] + pad + h * 0.22, y + h * 1.12), h * 0.12, fill=(8, 9, 11, 170))
    can.alpha_composite(s_.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(can)
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.06, b[2] + pad, b[3] + h * 0.05), fill=YEL)
    d.text((xd, cy), 'DM', font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.12, b[0] + h * 0.42, b[3] + h * 0.16), fill=RED)
def cp(can, x, y, h=100):
    f = oswald(int(h * 0.86)); d = ImageDraw.Draw(can); wc = d.textlength('C', font=f); gap, pad = h * 0.06, h * 0.08; cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'P', font=f, anchor='lm')
    s_ = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(s_).rounded_rectangle((x - h * 0.22, y - h * 0.16, b[2] + pad + h * 0.22, y + h * 1.12), h * 0.12, fill=(8, 9, 11, 170))
    can.alpha_composite(s_.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(can)
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.08, b[2] + pad, b[3] + h * 0.07), fill=YEL)
    d.text((xd, cy), 'P', font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.13, b[0] + h * 0.36, b[3] + h * 0.17), fill=RED)
def save(can, name): can.convert('RGB').save(OUT + name, quality=93); print(name)

# ---------------- German YouTube 16:9 (1920x1080) ----------------
TW, TH = 1920, 1080
def de_a():   # the face of the legend, the choice
    can = Image.new('RGBA', (TW, TH), DARK + (255,)); can.alpha_composite(look(cover(src('r07'), 1150, TH, 0.5, 0.40, 1.05)), (770, 0))
    side(can, 255, False, 0.62); grad(can, 120, 0.7); cdm(can, 70, 50, 92)
    T(can, (90, 470), 'ROMMEL', anton(250), WHITE, 'lm'); plate(can, (440, 700), 'GIFT ODER PROZESS', anton(96))
    save(can, 'DE_YT_A_Gift_oder_Prozess.jpg')
def de_b():   # lying in state vs death mask: the lie
    can = Image.new('RGBA', (TW, TH), DARK + (255,)); can.alpha_composite(look(cover(src('r12'), 960, TH, 0.5, 0.36, 1.05)), (0, 0)); can.alpha_composite(look(cover(src('r40'), 960, TH, 0.5, 0.45, 1.0), 0.6), (960, 0))
    ImageDraw.Draw(can).line((960, 0, 960, TH), fill=YEL, width=10); grad(can, 235, 0.45); cdm(can, TW / 2 - 85, 40, 92)
    T(can, (TW / 2, 780), 'DIE LÜGE', anton(190), WHITE); plate(can, (TW / 2, 955), 'UM SEINEN TOD', anton(92))
    save(can, 'DE_YT_B_Die_Luege.jpg')
def de_c():   # desert fox: archive film + portrait
    can = look(cover(clipframe(20.5), TW, TH, 0.5, 0.5, 1.05).convert('RGBA'), 0.6); can.alpha_composite(look(cover(src('r43'), 760, TH, 0.5, 0.42, 1.08)), (1160, 0))
    side(can, 220, False, 0.6); grad(can, 200, 0.55); cdm(can, 70, 50, 92)
    T(can, (90, 430), 'WÜSTENFUCHS', anton(190), YEL, 'lm'); plate(can, (420, 650), 'HELD ODER MYTHOS?', anton(84))
    save(can, 'DE_YT_C_Held_oder_Mythos.jpg')

# ---------------- German Facebook 9:16 (1080x1920) ----------------
VW, VH = 1080, 1920
def de_fb_a():
    can = look(cover(src('r07'), VW, VH, 0.5, 0.42, 1.0)); grad(can, 245, 0.5, 120); cdm(can, VW / 2 - 85, 120, 92)
    T(can, (VW / 2, 1300), 'ROMMEL', anton(230)); plate(can, (VW / 2, 1500), 'GIFT ODER PROZESS', anton(88))
    save(can, 'DE_FB_A_Gift_oder_Prozess.jpg')
def de_fb_b():
    can = Image.new('RGBA', (VW, VH), DARK + (255,)); can.alpha_composite(look(cover(src('r12'), VW, VH // 2, 0.5, 0.33, 1.0)), (0, 0)); can.alpha_composite(look(cover(src('r40'), VW, VH // 2, 0.5, 0.45, 1.0), 0.6), (0, VH // 2))
    ImageDraw.Draw(can).line((0, VH // 2, VW, VH // 2), fill=YEL, width=10); grad(can, 235, 0.55, 120); cdm(can, VW / 2 - 85, 120, 92)
    T(can, (VW / 2, 1420), 'DIE LÜGE', anton(200)); plate(can, (VW / 2, 1610), 'UM SEINEN TOD', anton(90))
    save(can, 'DE_FB_B_Die_Luege.jpg')
def de_fb_c():
    can = look(cover(src('r43'), VW, VH, 0.45, 0.42, 1.0)); grad(can, 240, 0.5, 120); cdm(can, VW / 2 - 85, 120, 92)
    T(can, (VW / 2, 1300), 'WÜSTENFUCHS', anton(170), YEL); plate(can, (VW / 2, 1490), 'HELD ODER MYTHOS?', anton(80))
    save(can, 'DE_FB_C_Held_oder_Mythos.jpg')

# ---------------- English short 9:16, Chronicle of Power (no blur, sepia, Oswald) ----------------
def en_a():   # Hitler and Rommel: the choice
    can = Image.new('RGBA', (VW, VH), DARK + (255,)); h = raw('h01')
    can.alpha_composite(look(cover(h, VW, 900, 0.5, 0.40, 1.0), 0.8, 0.12), (0, 0)); can.alpha_composite(look(cover(raw('r09'), VW, 1020, 0.5, 0.30, 1.0), 0.8, 0.12), (0, 900))
    ImageDraw.Draw(can).line((0, 900, VW, 900), fill=YEL, width=10); grad(can, 250, 0.72, 120); cp(can, VW / 2 - 70, 120, 92)
    T(can, (VW / 2, 1610), "HITLER'S CHOICE", fitf(oswald, "HITLER'S CHOICE", 150, 900)); plate(can, (VW / 2, 1790), 'TRIAL OR POISON', oswald(90))
    save(can, 'EN_A_Hitlers_Choice.jpg')
def en_b():   # the Desert Fox
    can = look(cover(raw('r07'), VW, VH, 0.5, 0.42, 1.0), 0.8, 0.12); grad(can, 245, 0.5, 120); cp(can, VW / 2 - 70, 120, 92)
    T(can, (VW / 2, 1290), 'THE DESERT FOX', fitf(oswald, 'THE DESERT FOX', 150, 900), YEL); plate(can, (VW / 2, 1490), 'WHY HE TOOK POISON', oswald(84))
    save(can, 'EN_B_Desert_Fox.jpg')
def en_c():   # buried as a hero
    can = Image.new('RGBA', (VW, VH), DARK + (255,)); can.alpha_composite(look(cover(raw('r43'), VW, 1100, 0.45, 0.4, 1.0), 0.8, 0.12), (0, 0))
    can.alpha_composite(look(cover(raw('r29'), VW, 820, 0.45, 0.5, 1.0), 0.8, 0.12), (0, 1100)); ImageDraw.Draw(can).line((0, 1100, VW, 1100), fill=YEL, width=10)
    grad(can, 235, 0.5, 120); cp(can, VW / 2 - 70, 120, 92)
    T(can, (VW / 2, 1360), 'BURIED AS A HERO', fitf(oswald, 'BURIED AS A HERO', 140, 900)); plate(can, (VW / 2, 1560), 'BUT IT WAS A LIE', oswald(88))
    save(can, 'EN_C_Buried_as_a_Hero.jpg')

for f in (de_a, de_b, de_c, de_fb_a, de_fb_b, de_fb_c, en_a, en_b, en_c): f()
# overview sheets
ims = [Image.open(OUT + n) for n in ('DE_YT_A_Gift_oder_Prozess.jpg', 'DE_YT_B_Die_Luege.jpg', 'DE_YT_C_Held_oder_Mythos.jpg')]
P = Image.new('RGB', (1920, 360)); [P.paste(im.resize((640, 360)), (i * 640, 0)) for i, im in enumerate(ims)]; P.save(OUT + '_overview_DE_YT.jpg', quality=85)
ims = [Image.open(OUT + n) for n in sorted(os.listdir(OUT)) if n.startswith(('DE_FB', 'EN_'))]
P = Image.new('RGB', (len(ims) * 300, 533)); [P.paste(im.resize((300, 533)), (i * 300, 0)) for i, im in enumerate(ims)]; P.save(OUT + '_overview_9x16.jpg', quality=85)
