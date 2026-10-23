# YouTube community post image (1080x1080) for the Balck short: portrait b27, NEUES VIDEO, name, LEHRER ODER TÄTER? with TÄTER underlined in red
from lib9 import *
from thumb_m import badge, T
S2 = 1080
im = src('b27'); x0, y0, side = 0, 150, 1792
can = im.resize((S2, S2), Image.LANCZOS, box=(x0, y0, x0 + side, y0 + side)).convert('RGBA')
g = (np.clip((np.arange(S2) - S2 * 0.45) / (S2 * 0.45), 0, 1) ** 1.2 * 235).astype(np.uint8)
sh = Image.new('RGBA', (S2, S2), (6, 7, 9, 0)); sh.putalpha(Image.fromarray(np.repeat(g[:, None], S2, 1))); can.alpha_composite(sh)
top = (np.clip((150 - np.arange(S2)) / 150, 0, 1) * 170).astype(np.uint8)
sh = Image.new('RGBA', (S2, S2), (6, 7, 9, 0)); sh.putalpha(Image.fromarray(np.repeat(top[:, None], S2, 1))); can.alpha_composite(sh)
badge(can, 60, 50, 80)
d = ImageDraw.Draw(can); f = anton(60); b = d.textbbox((S2 - 60, 90), 'NEUES VIDEO', font=f, anchor='rm'); d.rectangle((b[0] - 18, b[1] - 10, b[2] + 18, b[3] + 10), fill=YEL); d.text((S2 - 60, 90), 'NEUES VIDEO', font=f, fill=DARK, anchor='rm')
T(can, (S2 / 2, 805), 'HERMANN BALCK', 130, YEL, maxw=980)
s_ = 'LEHRER ODER TÄTER?'; f = anton(84)
T(can, (S2 / 2, 950), s_, 84, WHITE, bold=1)
x0_ = S2 / 2 - f.getlength(s_) / 2 + f.getlength('LEHRER ODER '); x1_ = x0_ + f.getlength('TÄTER')
d = ImageDraw.Draw(can); d.rectangle((x0_, 1000, x1_, 1009), fill=RED)
os.makedirs(B + 'social', exist_ok=True); can.convert('RGB').save(B + 'social/YouTube_Post_Balck.jpg', quality=93); print('ok')
