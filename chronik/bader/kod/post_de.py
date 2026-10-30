# YouTube community post image (1080x1080) for the German Bader short (CDM): Galland and Bader after the war, NEW VIDEO, the hook
from lib9 import *
from thumb_m import T, badge
S2 = 1080
im = src('d12'); x0, y0, side = 0, 0, 1792
can = im.resize((S2, S2), Image.LANCZOS, box=(x0, y0, x0 + side, y0 + side)).convert('RGBA')
g = (np.clip((np.arange(S2) - S2 * 0.45) / (S2 * 0.45), 0, 1) ** 1.2 * 235).astype(np.uint8)
sh = Image.new('RGBA', (S2, S2), (6, 7, 9, 0)); sh.putalpha(Image.fromarray(np.repeat(g[:, None], S2, 1))); can.alpha_composite(sh)
badge(can, 60, 50, 80); d = ImageDraw.Draw(can)
f = anton(60); b = d.textbbox((S2 - 60, 90), 'NEUES VIDEO', font=f, anchor='rm'); d.rectangle((b[0] - 18, b[1] - 10, b[2] + 18, b[3] + 10), fill=YEL); d.text((S2 - 60, 90), 'NEUES VIDEO', font=f, fill=DARK, anchor='rm')
T(can, (S2 / 2, 805), 'DOUGLAS BADER', 130, YEL, maxw=980)
T(can, (S2 / 2, 950), 'SEIN FEIND WURDE SEIN FREUND', 70, WHITE, maxw=980, bold=1)
os.makedirs(B + 'social', exist_ok=True); can.convert('RGB').save(B + 'social/YouTube_Post_Bader_DE.jpg', quality=93); print('ok')
