# new covers (fact + question) for Rommel, Törni, Hartmann, Lehmann-Willenbrock: text top left, bottom right kept clear for the duration badge.
# Portraits are cropped from the earlier covers (Boran's colourised photos, symbols already blurred).
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H = 1280, 720; FD = '/tmp/claude-0/fonts/'; R = '/home/user/Brnkry/chronik/'; O = R + 'thumbnails_lang/neu/'
YEL, RED, WHITE, DARK = (244, 196, 22), (200, 22, 26), (246, 244, 238), (14, 14, 16)
anton = lambda z: ImageFont.truetype(FD + 'Anton.ttf', z)
def crop(path, box, w, h):
    im = Image.open(path).convert('RGB').crop(box); s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS); x = (im.width - w) // 2; y = (im.height - h) // 2; return im.crop((x, y, x + w, y + h))
def topshade(c, h0=0.55, a=235, left=None):
    y = np.arange(H, dtype=np.float32)[:, None]; x = np.arange(W, dtype=np.float32)[None, :]
    g = np.clip((H * h0 - y) / (H * h0), 0, 1) ** 1.2 * a
    g = np.broadcast_to(g, (H, W)).copy()
    if left: g = np.maximum(g, np.clip((W * left - x) / (W * left), 0, 1) * a)
    L = Image.new('RGBA', (W, H), (8, 8, 10, 0)); L.putalpha(Image.fromarray(g.astype(np.uint8))); c.alpha_composite(L)
def stext(c, xy, s, f, col, anchor='la'):
    L = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(L).text(xy, s, font=f, fill=col + (255,), anchor=anchor)
    S = Image.new('RGBA', c.size, (0, 0, 0, 0)); S.paste((0, 0, 0, 240), (0, 0), L.getchannel('A')); c.alpha_composite(S.filter(ImageFilter.GaussianBlur(10)), (4, 6)); c.alpha_composite(L)
def fit(s, w, z):
    while anton(z).getlength(s) > w: z -= 2
    return anton(z)
def plate(c, x, y, s, z, maxw):
    f = fit(s, maxw, z); d = ImageDraw.Draw(c); b = d.textbbox((x, y), s, font=f); px, py = 20, 10
    sh = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((b[0] - px + 8, b[1] - py + 10, b[2] + px + 8, b[3] + py + 10), fill=(0, 0, 0, 190)); c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(c); d.rectangle((b[0] - px, b[1] - py, b[2] + px, b[3] + py), fill=YEL); d.text((x, y), s, font=f, fill=DARK)
    d.rectangle((b[0] - px, b[3] + py + 8, b[0] - px + 150, b[3] + py + 16), fill=RED)
def logo(c):
    d = ImageDraw.Draw(c); f = anton(44); x, y = W - 150, 28
    d.rounded_rectangle((x - 12, y - 8, x + 120, y + 58), 6, fill=(8, 9, 11, 210)); d.text((x, y + 25), 'C', font=f, fill=WHITE, anchor='lm')
    b = d.textbbox((x + 34, y + 25), 'DM', font=f, anchor='lm'); d.rectangle((b[0] - 4, b[1] - 4, b[2] + 4, b[3] + 4), fill=YEL); d.text((x + 34, y + 25), 'DM', font=f, fill=DARK, anchor='lm')
def head(c, l1, q, maxw=780, z1=118):
    f1 = fit(l1, maxw, z1); qy = 590; stext(c, (44, qy - 24), l1, f1, WHITE, 'ls'); plate(c, 52, qy, q, 70, maxw - 20)
def botshade(c, a=245):
    y = np.arange(H, dtype=np.float32)[:, None]; g = np.clip((y - H * 0.42) / (H * 0.58), 0, 1) ** 1.1 * a
    L = Image.new('RGBA', (W, H), (8, 8, 10, 0)); L.putalpha(Image.fromarray(np.broadcast_to(g, (H, W)).astype(np.uint8))); c.alpha_composite(L)
def save(c, n): logo(c); c.convert('RGB').save(O + n, quality=94); print(n)
# Rommel: face (A) and the portrait in the field cap (C), only areas without the old text
c = Image.new('RGBA', (W, H), (10, 10, 12, 255))
c.paste(crop(R + 'rommel/thumbnails/DE_YT_A_Gift_oder_Prozess.jpg', (930, 0, 1890, 1080), 680, H), (0, 0))
c.paste(crop(R + 'rommel/thumbnails/DE_YT_C_Held_oder_Mythos.jpg', (1160, 90, 1920, 1005), 600, H), (680, 0))
ImageDraw.Draw(c).rectangle((677, 0, 683, H), fill=YEL)
bx = (926, 620, 950, 644); c.paste(c.crop(bx).filter(ImageFilter.GaussianBlur(5)), bx[:2])   # Knight's Cross centre
botshade(c); head(c, 'GIFT ODER PROZESS', 'WARUM MUSSTE ROMMEL STERBEN?'); save(c, 'Rommel_D_Gift_oder_Prozess.jpg')
# Törni: the three portraits above the old labels
c = Image.new('RGBA', (W, H), (10, 10, 12, 255)); S = R + 'torni/social/Thumbnail_A_Drei_Uniformen.jpg'
for i, b in enumerate(((90, 0, 440, 590), (790, 120, 1080, 590), (1430, 0, 1780, 590))): c.paste(crop(S, b, 427, H), (i * 427, 0))
for x in (424, 851): ImageDraw.Draw(c).rectangle((x, 0, x + 5, H), fill=YEL)
botshade(c); head(c, 'IN 3 ARMEEN GEKÄMPFT', 'WIE WAR DAS MÖGLICH?', maxw=860, z1=124); save(c, 'Toerni_D_Drei_Armeen.jpg')
# Hartmann: the colour portrait and the 1955 photo
c = Image.new('RGBA', (W, H), (10, 10, 12, 255))
c.paste(crop(R + 'thumbnails_lang/Hartmann_B.jpg', (1100, 40, 1880, 920), 640, H), (0, 0)); c.paste(crop(R + 'thumbnails_lang/Hartmann_A.jpg', (960, 110, 1500, 610), 640, H), (640, 0))
ImageDraw.Draw(c).rectangle((637, 0, 643, H), fill=YEL)
botshade(c); head(c, '352 ABSCHÜSSE', 'WARUM 10 JAHRE HAFT?', maxw=820, z1=130); save(c, 'Hartmann_D_352_Haft.jpg')
# Lehmann-Willenbrock: the real Kaleu and the film
c = Image.new('RGBA', (W, H), (10, 10, 12, 255)); S = R + 'thumbnails_lang/LehmannWillenbrock_A.jpg'
c.paste(crop(S, (330, 160, 820, 630), 640, H), (0, 0)); c.paste(crop(S, (1150, 180, 1550, 630), 640, H), (640, 0))
ImageDraw.Draw(c).rectangle((637, 0, 643, H), fill=YEL)
botshade(c); head(c, 'DAS BOOT WAR ECHT', 'WER WAR DER KALEU?', maxw=860, z1=124); save(c, 'LehmannWillenbrock_D_Das_Boot_echt.jpg')
