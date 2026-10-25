# YouTube community post image (1080x1080) for the English Udet short: the cover picture (Udet behind the lead Stuka), NEW VIDEO, the hook
from lib9 import *
from thumb_m import T
S2 = 1080
im = Image.open(B + 'img/cov_en.jpg').convert('RGB'); x0, y0, side = 0, 110, 1080
can = im.resize((S2, S2), Image.LANCZOS, box=(x0, y0, x0 + side, y0 + side)).convert('RGBA')
g = (np.clip((np.arange(S2) - S2 * 0.62) / (S2 * 0.3), 0, 1) ** 1.2 * 235).astype(np.uint8)
sh = Image.new('RGBA', (S2, S2), (6, 7, 9, 0)); sh.putalpha(Image.fromarray(np.repeat(g[:, None], S2, 1))); can.alpha_composite(sh)
d = ImageDraw.Draw(can); f = anton(66); d.text((60, 90), 'C', font=f, fill=WHITE, anchor='lm'); b = d.textbbox((60 + f.getlength('C') + 10, 90), 'P', font=f, anchor='lm')
d.rectangle((b[0] - 6, b[1] - 6, b[2] + 6, b[3] + 6), fill=YEL); d.text((b[0], 90), 'P', font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - 6, b[3] + 12, b[0] + 30, b[3] + 16), fill=RED)
f = anton(60); b = d.textbbox((S2 - 60, 90), 'NEW VIDEO', font=f, anchor='rm'); d.rectangle((b[0] - 18, b[1] - 10, b[2] + 18, b[3] + 10), fill=YEL); d.text((S2 - 60, 90), 'NEW VIDEO', font=f, fill=DARK, anchor='rm')
T(can, (S2 / 2, 930), 'ERNST UDET', 112, YEL, maxw=980)
T(can, (S2 / 2, 1030), 'THE MAN BEHIND THE SIREN', 58, WHITE, maxw=980, bold=1)
os.makedirs(B + 'social', exist_ok=True); can.convert('RGB').save(B + 'social/YouTube_Post_Udet.jpg', quality=93); print('ok')
