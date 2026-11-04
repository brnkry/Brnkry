# zoom crops with a source-pixel grid: zoom.py out.jpg img:cx:cy:half ...
import sys, glob
from PIL import Image, ImageDraw
tiles = []
for a in sys.argv[2:]:
    f, cx, cy, h = a.split(':'); cx, cy, h = int(cx), int(cy), int(h)
    im = Image.open(glob.glob('/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/egon/drive/' + f + '_*.jpg')[0]).convert('RGB')
    c = im.crop((cx - h, cy - h, cx + h, cy + h)).resize((400, 400), Image.LANCZOS); d = ImageDraw.Draw(c); s = 400 / (2 * h)
    st = 20 if h <= 120 else 50
    for v in range((cx - h) // st * st, cx + h, st):
        X = (v - cx + h) * s; d.line((X, 0, X, 400), fill=(255, 0, 255), width=1); d.text((X + 1, 1), str(v), fill=(255, 255, 0))
    for v in range((cy - h) // st * st, cy + h, st):
        Y = (v - cy + h) * s; d.line((0, Y, 400, Y), fill=(255, 0, 255), width=1); d.text((1, Y + 1), str(v), fill=(255, 255, 0))
    d.text((5, 385), a, fill=(0, 255, 0)); tiles.append(c)
T = Image.new('RGB', (min(4, len(tiles)) * 405, ((len(tiles) + 3) // 4) * 405))
for i, c in enumerate(tiles): T.paste(c, ((i % 4) * 405, (i // 4) * 405))
T.save(sys.argv[1], quality=85)
