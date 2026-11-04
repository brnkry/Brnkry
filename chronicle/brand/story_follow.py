# Story 1080x1920 for the Chronik der Macht account: "follow our English channel" (Instagram + Facebook), room left for the mention and link stickers
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D = sys.argv[1] + '/'; S = sys.argv[2] + '/'; F = S + 'sch/fonts/'
YEL, RED, WHITE, DARK, CREAM = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18), (226, 218, 198)
W, H = 1080, 1920
def oswald(s, wg=700):
    f = ImageFont.truetype(F + 'Oswald%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
def playfair(s, wg=500):
    f = ImageFont.truetype(F + 'PlayfairDisplay%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
def anton(s): return ImageFont.truetype(F + 'Anton-Regular.ttf', s)
def shadow(can, fn, blur=12, off=(5, 9), a=210):
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L))
    s = Image.new('RGBA', can.size, (0, 0, 0, 0)); s.paste((0, 0, 0, a), (0, 0), L.getchannel('A'))
    can.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)), off); can.alpha_composite(L)
def T(can, xy, s, f, col=WHITE): shadow(can, lambda d: d.text(xy, s, font=f, fill=col + (255,), anchor='mm'))
def plate(can, cy, s, f, bg=YEL, fg=DARK, rule=True):
    d = ImageDraw.Draw(can); b = d.textbbox((W / 2, cy), s, font=f, anchor='mm'); px, py = 30, 14
    shadow(can, lambda dd: dd.rectangle((b[0] - px, b[1] - py, b[2] + px, b[3] + py), fill=bg + (255,)), 14, (6, 10), 170)
    d = ImageDraw.Draw(can); d.text((W / 2, cy), s, font=f, fill=fg, anchor='mm')
    if rule: d.rectangle((b[0] - px, b[3] + py + 12, b[0] - px + 150, b[3] + py + 20), fill=RED)
# background: the Chronicle of Power banner, vertical crop, blurred and darkened
bn = Image.open(D + 'CoP_Banner_2560x1440.jpg').convert('RGB'); s = H / bn.height; bn = bn.resize((int(bn.width * s), H), Image.LANCZOS)
bg = bn.crop(((bn.width - W) // 2, 0, (bn.width - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(14))
can = Image.blend(ImageEnhance.Color(bg).enhance(0.5), Image.new('RGB', (W, H), (10, 10, 11)), 0.55).convert('RGBA')
# the channel banner as a tilted card (no faces, no symbols: safe for the German account)
cov = Image.open(D + 'CoP_Banner_2560x1440.jpg').convert('RGB'); cov = cov.crop((360, 300, 2200, 1140)).resize((820, 374), Image.LANCZOS).convert('RGBA')
fr = Image.new('RGBA', (844, 398), WHITE + (255,)); fr.alpha_composite(cov, (12, 12)); fr = fr.rotate(-3, expand=True, resample=Image.BICUBIC)
sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (W // 2 - fr.width // 2 + 14, 900 + 22), fr.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
can.alpha_composite(fr, (W // 2 - fr.width // 2, 900))
# avatar
av = Image.open(D + 'CoP_Avatar_1024.jpg').convert('RGBA').resize((190, 190), Image.LANCZOS); m = Image.new('L', (190, 190), 0); ImageDraw.Draw(m).ellipse((0, 0, 190, 190), fill=255)
ring = Image.new('RGBA', (206, 206), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((0, 0, 206, 206), fill=YEL + (255,)); can.alpha_composite(ring, (W // 2 - 103, 292)); can.paste(av, (W // 2 - 95, 300), m)
plate(can, 560, 'NEU: UNSER ENGLISCHER KANAL', oswald(54), rule=False)
f = oswald(96); d = ImageDraw.Draw(can); t1, t2 = 'CHRONICLE', 'OF POWER'; w1 = d.textlength(t1, font=f); w2 = d.textlength(t2, font=f); g = 26; x0 = W / 2 - (w1 + g + w2 + 40) / 2
shadow(can, lambda dd: dd.text((x0, 690), t1, font=f, fill=WHITE + (255,), anchor='lm'))
d = ImageDraw.Draw(can); b = d.textbbox((x0 + w1 + g + 20, 690), t2, font=f, anchor='lm'); d.rectangle((b[0] - 20, b[1] - 12, b[2] + 20, b[3] + 12), fill=YEL); d.text((x0 + w1 + g + 20, 690), t2, font=f, fill=DARK, anchor='lm')
d.rectangle((b[0] - 20, b[3] + 22, b[0] + 130, b[3] + 30), fill=RED)
T(can, (W / 2, 800), 'Weltkriege, Menschen, Wendepunkte, auf Englisch', playfair(38, 500), CREAM)
T(can, (W / 2, 1420), 'JETZT FOLGEN', anton(110), YEL)
T(can, (W / 2, 1515), 'Instagram · Facebook · YouTube', playfair(40, 600), WHITE)
# room for the stickers (@mention and YouTube link): a soft dashed frame marks the spot, the stickers cover it
d = ImageDraw.Draw(can)
for x in range(170, 910, 34): d.line((x, 1600, x + 18, 1600), fill=CREAM + (150,), width=3); d.line((x, 1720, x + 18, 1720), fill=CREAM + (150,), width=3)
a = np.asarray(can.convert('RGB')).astype(np.int16) + np.random.default_rng(3).normal(0, 4, (H, W))[..., None].astype(np.int16)
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(sys.argv[3], quality=93); print('ok')
