# cover photo for the Rommel short: the colour portrait r32 (Rommel at the Atlantic Wall, 1943; cap eagle blurred by lib9.src),
# full photo height, the uniform carried down as a soft band so the face sits between the fixed logo and the text block -> img/cov.jpg
import sys; sys.path.insert(0, sys.argv[1] + '/code')
from lib9 import *
p = src('r32'); CW = 1008; x0 = 1050 - CW // 2; BOT = 520
body = p.crop((x0, 0, x0 + CW, p.height))
row = np.asarray(body.crop((0, p.height - 60, CW, p.height)).filter(ImageFilter.GaussianBlur(25)), np.float32).mean(0)
band = Image.fromarray(np.clip(np.linspace(1.0, 0.35, BOT)[:, None, None] * row[None], 0, 255).astype(np.uint8))
can = Image.new('RGB', (CW, p.height + BOT)); can.paste(body, (0, 0)); can.paste(band, (0, p.height))
can.save(B + 'img/cov.jpg', quality=95); print('ok', can.size)
