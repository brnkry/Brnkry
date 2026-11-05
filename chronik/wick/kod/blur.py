import sys
from PIL import Image, ImageDraw, ImageFilter
def blur(f, spots):
    im = Image.open(f).convert('RGB')
    for x, y, r in spots:
        b = im.filter(ImageFilter.GaussianBlur(max(6, r / 3)))
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse((x - r, y - r, x + r, y + r), fill=255); m = m.filter(ImageFilter.GaussianBlur(r / 6))
        im = Image.composite(b, im, m)
    im.save(f, quality=95)
if __name__ == '__main__':
    J = {'fotos/nightriders_2130.jpg': [(410, 15, 50)], 'fotos/nightriders_2730.jpg': [(615, 75, 62)], 'fotos/nightriders_540.jpg': [(35, 165, 58)], 'fotos/nachtgespenst_246.jpg': [(155, 262, 100)]}
    for f, s in J.items(): blur(f, s)
