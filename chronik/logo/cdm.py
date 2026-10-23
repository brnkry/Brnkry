# style-B avatar variants with the letters CDM
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
D = sys.argv[1] + '/'; F = D + '../sch/fonts/'
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
anton = lambda s: ImageFont.truetype(F + 'Anton-Regular.ttf', s)
rng = np.random.default_rng(5)
def grain(im):
    a = np.asarray(im.convert('RGB')).astype(np.int16) + rng.normal(0, 5, (1024, 1024))[..., None].astype(np.int16)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
# 1: white CDM with the yellow and red bars
im = Image.new('RGB', (1024, 1024), DARK); d = ImageDraw.Draw(im)
f = anton(400); b = d.textbbox((512, 470), 'CDM', font=f, anchor='mm'); d.text((512, 470), 'CDM', font=f, fill=WHITE, anchor='mm')
d.rectangle((b[0], 700, b[2], 752), fill=YEL); d.rectangle((b[0], 770, b[0] + 160, 784), fill=RED)
grain(im).save(D + 'B_CDM_1_avatar.jpg', quality=95)
# 2: C in white, DM on a yellow plate, like the wordmark
im = Image.new('RGB', (1024, 1024), DARK); d = ImageDraw.Draw(im)
f = anton(380); wc = d.textlength('C', font=f); wd = d.textlength('DM', font=f); gap, pad = 30, 26
x0 = 512 - (wc + gap + wd + 2 * pad) / 2
d.text((x0, 500), 'C', font=f, fill=WHITE, anchor='lm')
b = d.textbbox((x0 + wc + gap + pad, 500), 'DM', font=f, anchor='lm'); d.rectangle((b[0] - pad, b[1] - 26, b[2] + pad, b[3] + 22), fill=YEL)
d.text((x0 + wc + gap + pad, 500), 'DM', font=f, fill=DARK, anchor='lm')
d.rectangle((b[0] - pad, b[3] + 44, b[0] + 140, b[3] + 58), fill=RED)
grain(im).save(D + 'B_CDM_2_avatar.jpg', quality=95)
# preview as YouTube circles (big and real size), next to the plain C
P = Image.new('RGB', (900, 400), (15, 15, 15))
for i, n in enumerate(['B_Balken_avatar', 'B_CDM_1_avatar', 'B_CDM_2_avatar']):
    a = Image.open(D + n + '.jpg').resize((240, 240), Image.LANCZOS); m = Image.new('L', (240, 240), 0); ImageDraw.Draw(m).ellipse((0, 0, 239, 239), fill=255)
    P.paste(a, (i * 300 + 30, 20), m); P.paste(a.resize((48, 48), Image.LANCZOS), (i * 300 + 126, 300), m.resize((48, 48)))
P.save(D + 'B_CDM_vergleich.jpg', quality=92)
