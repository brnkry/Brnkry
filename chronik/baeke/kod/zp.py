# zp.py out.jpg "i,x,y,r" ... absolute pixel centre, half-size r; grid every r/5 px with labels
import sys, os
from PIL import Image, ImageDraw, ImageFont
F = sorted(os.listdir('img')); T = int(os.environ.get('T', 300)); tiles = []
fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
for a in sys.argv[2:]:
    i, x, y, r = map(int, a.split(',')); im = Image.open('img/' + F[i]).convert('RGB')
    box = (x - r, y - r, x + r, y + r); c = im.crop(box).resize((T, T), Image.LANCZOS); d = ImageDraw.Draw(c)
    for k in range(1, 10):
        p = k * T / 10; col = (255, 0, 0) if k != 5 else (0, 255, 255)
        d.line((p, 0, p, 4), fill=col, width=2); d.line((0, p, 4, p), fill=col, width=2); d.line((p, T - 4, p, T), fill=col, width=2); d.line((T - 4, p, T, p), fill=col, width=2)
    d.text((4, T - 16), a, font=fnt, fill=(0, 255, 0)); tiles.append(c)
n = len(tiles); cols = min(n, 6); rows = (n + cols - 1) // cols; S = Image.new('RGB', (cols * T, rows * T))
for k, t in enumerate(tiles): S.paste(t, ((k % cols) * T, (k // cols) * T))
S.save(sys.argv[1], quality=90); print(S.size)
