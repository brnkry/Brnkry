# minimal cover lib for the Tiger I short (covers4.py job 'tiger_short'); frame from Boran's colour footage (Tiger 132)
import os
from PIL import Image, ImageFont
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
def oswald(s):
    f = ImageFont.truetype('/tmp/claude-0/fonts/Oswald.ttf', s)
    try: f.set_variation_by_name('Bold')
    except Exception: pass
    return f
def src(name): return Image.open(B + 'img/' + name + '.jpg').convert('RGB')
