# cover photo for the Rommel short: the sharp colour portrait r09 (cap eagle and breast eagle blurred by lib9.src),
# face between the fixed logo and the text block; the background above is carried up as a soft band -> img/cov.jpg
import sys; sys.path.insert(0, sys.argv[1] + '/code')
from lib9 import *
p = src('r09'); TOPB = int(sys.argv[2]) if len(sys.argv) > 2 else 200
row = np.asarray(p.crop((0, 0, p.width, 40)).filter(ImageFilter.GaussianBlur(30)), np.float32).mean(0)
band = Image.fromarray(np.clip(np.linspace(0.8, 1.0, TOPB)[:, None, None] * row[None], 0, 255).astype(np.uint8))
can = Image.new('RGB', (p.width, p.height + TOPB)); can.paste(band, (0, 0)); can.paste(p, (0, TOPB))
can.save(B + 'img/cov.jpg', quality=95); print('ok', can.size)
