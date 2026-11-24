# minimal cover lib for the Wunderlich short (covers4.py job 'wunderlich'); colourised portrait from Boran
import os
from PIL import Image, ImageFont
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
def oswald(s):
    f = ImageFont.truetype('/tmp/claude-0/fonts/Oswald.ttf', s)
    try: f.set_variation_by_name('Bold')
    except Exception: pass
    return f
def src(name):
    # the portrait fills the frame, so the fixed logo would sit on the forehead: extend the plain grey wall upwards a little, feathered
    from PIL import ImageFilter
    import numpy as np
    im = Image.open(B + 'img/' + name + '.jpg').convert('RGB'); w, h = im.size; add = int(h * 0.10); feather = 260
    wall = np.array(im.crop((0, 0, w, 60)), np.float32).mean(axis=(0, 1))
    top = np.tile(wall, (add + feather, w, 1)) + np.random.default_rng(1).normal(0, 6, (add + feather, w, 1))
    out = np.zeros((h + add, w, 3), np.float32); out[add:] = np.array(im, np.float32); a = np.clip(np.arange(add + feather) - add, 0, feather) / feather
    out[:add + feather] = top * (1 - a)[:, None, None] + out[:add + feather] * a[:, None, None]
    return Image.fromarray(np.clip(out, 0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))
