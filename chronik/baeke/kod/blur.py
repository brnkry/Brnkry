# swastika blurs, pixel (x, y, r) on the Drive photos; only clearly visible ones
import os
from PIL import Image, ImageDraw, ImageFilter
B = os.path.dirname(os.path.abspath(__file__)) + '/../'
F = sorted(os.listdir(B + 'img'))
BLURPX = {0: [(731, 1409, 26), (1073, 2134, 24)], 15: [(553, 2133, 46)], 21: [(949, 235, 15), (552, 1910, 27)], 22: [(744, 229, 14)]}
def IMP(i): return B + 'img/' + F[i]
def load(i):
    im = Image.open(IMP(i)).convert('RGB'); w, h = im.size
    for x, y, R in BLURPX.get(i, []):
        box = (x - R, y - R, x + R, y + R); patch = im.crop(box).filter(ImageFilter.GaussianBlur(R * 0.35))
        m = Image.new('L', patch.size, 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * R, 2 * R), fill=255)
        im.paste(patch, box[:2], m.filter(ImageFilter.GaussianBlur(R * 0.15)))
    return im
if __name__ == '__main__':
    T = 260; tiles = []
    for i, L in BLURPX.items():
        a = Image.open(IMP(i)).convert('RGB'); b = load(i)
        for x, y, R in L:
            bx = (x - 3 * R, y - 3 * R, x + 3 * R, y + 3 * R)
            tiles += [a.crop(bx).resize((T, T)), b.crop(bx).resize((T, T))]
    S = Image.new('RGB', (T * 4, T * ((len(tiles) + 3) // 4)))
    for k, t in enumerate(tiles): S.paste(t, ((k % 4) * T, (k // 4) * T))
    S.save(B + 'blurchk.jpg', quality=90)
