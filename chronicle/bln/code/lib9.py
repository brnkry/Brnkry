# minimal cover lib for the Berlin 1945 short (covers4.py job 'berlin')
import os
from PIL import Image, ImageFont, ImageFilter
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
def oswald(s):
    f = ImageFont.truetype('/tmp/claude-0/fonts/Oswald.ttf', s)
    try: f.set_variation_by_name('Bold')
    except Exception: pass
    return f
def src(name):
    im = Image.open(B + 'img/' + name + '.jpg').convert('RGB')
    return im.crop((170, 110, 2810, 2560)) if name == 'reichstag' else im   # Bild 204-009 without the white print border
