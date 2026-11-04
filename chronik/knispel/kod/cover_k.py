# cover photo for the Knispel short: the opening photo of the short, k04 (smiling in the Tiger's turret) (swastikas already blurred by lib9.src), face between the fixed logo and the text block;
# the plain sky above him are carried upwards as a soft band -> img/cov.jpg (covers4.py job 'knispel' adds the fixed layout)
import sys; sys.path.insert(0, sys.argv[1] + '/code')
from lib9 import *
p = src('k04'); CW = 1350; x0 = 830 - CW // 2; PAD = 380; CH = int(CW * 16 / 9)
body = p.crop((x0, 0, x0 + CW, CH - PAD))
strip = np.asarray(body.crop((0, 0, CW, 60)).filter(ImageFilter.GaussianBlur(40)), np.float32).mean(0)   # colours of the leaves above him, smoothed
g = np.linspace(0.55, 1.0, PAD)[:, None, None] * strip[None]
top = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(8))
can = Image.new('RGB', (CW, CH)); can.paste(top, (0, 0)); can.paste(body, (0, PAD))
seam = body.crop((0, 0, CW, 80)).filter(ImageFilter.GaussianBlur(14)); m = Image.fromarray((np.linspace(255, 0, 80)[:, None] * np.ones((1, CW))).astype(np.uint8))
can.paste(Image.composite(seam, body.crop((0, 0, CW, 80)), m), (0, PAD))
can.save(B + 'img/cov.jpg', quality=95); print('ok', can.size)
