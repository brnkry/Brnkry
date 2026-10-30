# YouTube community post image for Teil 1 (1080x1080): the flag cover background, a headline and the series plate
import sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
D = sys.argv[1]; sys.path.insert(0, D + '/covlib'); import lib9 as L
im = Image.open(D + '/cov/cov_flag.jpg').crop((0, 300, 1080, 1380)).convert('RGBA')
g = np.clip((np.arange(1080) - 560) / 300, 0, 1) * 225; B_ = Image.new('RGBA', im.size, (6, 7, 9, 0)); B_.putalpha(Image.fromarray(np.repeat(g.astype(np.uint8)[:, None], 1080, 1))); im.alpha_composite(B_)
def T(y, s, size, col):
    f = L.oswald(size)
    while f.getlength(s) > 960: size -= 4; f = L.oswald(size)
    La = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(La).text((540, y), s, font=f, fill=col + (255,), anchor='mm')
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 230), (0, 0), La.getchannel('A')); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (4, 8)); im.alpha_composite(La)
T(790, 'VON VERSAILLES BIS POLEN', 104, L.WHITE); T(895, 'WIE ES ZUM KRIEG KAM', 96, L.YEL)
d = ImageDraw.Draw(im); f = L.oswald(52); s = 'NEUE SERIE · TEIL 1'; b = d.textbbox((540, 1000), s, font=f, anchor='mm')
d.rectangle((b[0] - 24, b[1] - 12, b[2] + 24, b[3] + 12), fill=L.YEL); d.text((540, 1000), s, font=f, fill=L.DARK, anchor='mm'); d.rectangle((b[0] - 24, b[3] + 22, b[0] + 110, b[3] + 30), fill=L.RED)
import os; os.makedirs(D + '/social', exist_ok=True); im.convert('RGB').save(D + '/social/YouTube_Post_Teil1_DE.jpg', quality=93); print('ok')
