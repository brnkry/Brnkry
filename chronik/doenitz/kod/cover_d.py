# cover photo for the Dönitz short: the colour portrait p08 (swastikas already blurred by lib9.src), face large and below the fixed logo;
# the plain studio background is carried upwards -> img/cov.jpg (covers4.py job 'doenitz' adds the fixed layout)
import sys; sys.path.insert(0, sys.argv[1] + '/code')
from lib9 import *
p = src('p08'); CW = 1200; x0 = 896 - CW // 2; PAD = 520; CH = int(CW * 16 / 9)
body = p.crop((x0, 0, x0 + CW, CH - PAD))
row = np.asarray(body.crop((0, 0, CW, 40)).filter(ImageFilter.GaussianBlur(20))).astype(np.float32).mean(0)
g = np.linspace(0.7, 1.0, PAD)[:, None, None] * row[None]
top = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
can = Image.new('RGB', (CW, CH)); can.paste(top, (0, 0)); m = np.clip(np.arange(CH - PAD) / 60, 0, 1)[:, None] * np.ones((1, CW))
can.paste(body, (0, PAD)); can.paste(top.crop((0, PAD - 60, CW, PAD)), (0, PAD), Image.fromarray(((1 - m[:60]) * 255).astype(np.uint8)))
can.save(B + 'img/cov.jpg', quality=95); print('ok', can.size)
