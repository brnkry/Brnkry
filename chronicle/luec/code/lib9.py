# minimal cover lib for the Wolfgang Lüth short (covers4.py job 'lueth'); photo: Lüth with white cap (colourised by Boran)
import os
from PIL import Image, ImageFont, ImageFilter, ImageDraw
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
def oswald(s):
    f = ImageFont.truetype('/tmp/claude-0/fonts/Oswald.ttf', s)
    try: f.set_variation_by_name('Bold')
    except Exception: pass
    return f
BLUR = [(873, 283, 62, 62), (1275, 1725, 70, 70)]   # cap eagle swastika, Knight's Cross centre (German channel)
def src(name):
    im = Image.open(B + 'img/' + name + '.jpg').convert('RGB')
    for x, y, rx, ry in BLUR:
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse((x - rx, y - ry, x + rx, y + ry), fill=255); m = m.filter(ImageFilter.GaussianBlur(12))
        im = Image.composite(im.filter(ImageFilter.GaussianBlur(22)), im, m)
    return im
