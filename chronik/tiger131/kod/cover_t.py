# cover photo for the Tiger 131 short: the colour photo t20 (Tiger 131 in Tunisia, 1943) with the tank in the upper middle,
# sky carried up and ground carried down as soft bands -> img/cov.jpg (covers4.py job 'tiger131' adds the fixed layout)
import sys; sys.path.insert(0, sys.argv[1] + '/code')
from lib9 import *
CW, CH = 1350, 2400; p = src('t20').crop((230, 0, 2030, 1792)); s = CW / p.width; ph = int(p.height * s); p = p.resize((CW, ph), Image.LANCZOS)
Y = 330; can = Image.new('RGB', (CW, CH))
top = np.asarray(p.crop((0, 0, CW, 40)).filter(ImageFilter.GaussianBlur(30)), np.float32).mean(0)
can.paste(Image.fromarray(np.clip(np.linspace(0.75, 1.0, Y)[:, None, None] * top[None], 0, 255).astype(np.uint8)), (0, 0))
bot = np.asarray(p.crop((0, ph - 60, CW, ph)).filter(ImageFilter.GaussianBlur(30)), np.float32).mean(0); rest = CH - Y - ph
can.paste(Image.fromarray(np.clip(np.linspace(1.0, 0.45, rest)[:, None, None] * bot[None], 0, 255).astype(np.uint8)), (0, Y + ph))
can.paste(p, (0, Y)); can.save(B + 'img/cov.jpg', quality=95); print('ok', Y, ph)
