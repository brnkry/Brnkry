# YouTube community post image (1080x1080) for the Manstein short: close-up m14, NEUES VIDEO, name, the legend struck through
from lib9 import *
from thumb_m import badge, T
S2 = 1080
im = src('m14'); x0, y0, side = 780, 0, 1536
can = im.resize((S2, S2), Image.LANCZOS, box=(x0, y0, x0 + side, y0 + side)).convert('RGBA')
g = (np.clip((np.arange(S2) - S2 * 0.42) / (S2 * 0.5), 0, 1) ** 1.2 * 240).astype(np.uint8)
sh = Image.new('RGBA', (S2, S2), (6, 7, 9, 0)); sh.putalpha(Image.fromarray(np.repeat(g[:, None], S2, 1))); can.alpha_composite(sh)
top = (np.clip((150 - np.arange(S2)) / 150, 0, 1) * 170).astype(np.uint8)
sh = Image.new('RGBA', (S2, S2), (6, 7, 9, 0)); sh.putalpha(Image.fromarray(np.repeat(top[:, None], S2, 1))); can.alpha_composite(sh)
badge(can, 60, 50, 80)
d = ImageDraw.Draw(can); f = anton(60); b = d.textbbox((S2 - 60, 90), 'NEUES VIDEO', font=f, anchor='rm'); d.rectangle((b[0] - 18, b[1] - 10, b[2] + 18, b[3] + 10), fill=YEL); d.text((S2 - 60, 90), 'NEUES VIDEO', font=f, fill=DARK, anchor='rm')
T(can, (S2 / 2, 800), 'ERICH VON MANSTEIN', 118, YEL, maxw=980)
s_ = 'DER SAUBERE STRATEGE?'; f = anton(78)
T(can, (S2 / 2, 945), s_, 78, WHITE, bold=1)
x0_ = S2 / 2 - f.getlength(s_) / 2 + f.getlength('DER '); x1_ = x0_ + f.getlength('SAUBERE')
d = ImageDraw.Draw(can); d.line((x0_ - 6, 952, x1_ + 6, 940), fill=RED, width=10)
os.makedirs(B + 'social', exist_ok=True); can.convert('RGB').save(B + 'social/YouTube_Post_Manstein.jpg', quality=93); print('ok')
