# debug: screen-space grids of film frames and source-space grids of photos, to place painted words on surfaces
import sys; sys.argv = ['x', 'list']
from gshort import *
out = []
for spec in sys.stdin.read().split():
    k, a, fx = spec.split(':'); im = FV(k, 0.0, None, 1.0, float(fx))(float(a), 0, 10).convert('RGB'); d = ImageDraw.Draw(im)
    for x in range(0, W, 100): d.line((x, 0, x, H), fill=(0, 255, 255)); d.text((x + 3, 3), str(x), fill=(255, 255, 0), font=anton(28))
    for y in range(0, H, 100): d.line((0, y, W, y), fill=(0, 255, 255)); d.text((3, y + 3), str(y), fill=(255, 255, 0), font=anton(28))
    out.append(im.resize((540, 960)))
S = Image.new('RGB', (540 * len(out), 960))
for i, o in enumerate(out): S.paste(o, (i * 540, 0))
S.save(B + 'chk/grid1.jpg')
