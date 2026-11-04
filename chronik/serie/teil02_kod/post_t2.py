# YouTube community post image (1080x1080) for Teil 2: German infantry crossing a bridge, series title, "Teil 2 ist da"
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(HERE) + '/'; SP = os.path.dirname(B.rstrip('/')) + '/'
sys.path.insert(0, HERE); import story_t2 as S
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
N = 1080; g = Image.open(SP + 't2/c/hoffmann_s49_0.jpg').convert('RGB'); w, h = g.size; c = min(w, h)
im = ImageEnhance.Contrast(g.resize((N, N), Image.LANCZOS, box=((w - c) / 2, (h - c) / 2, (w + c) / 2, (h + c) / 2))).enhance(1.06).convert('RGBA')
sh = np.clip((np.arange(N) - 380) / 520, 0, 1)[:, None] ** 1.2 * 235; Lg = Image.new('RGBA', im.size, (6, 7, 9, 0)); Lg.putalpha(Image.fromarray(np.repeat(sh, N, 1).astype(np.uint8))); im.alpha_composite(Lg)
S.SW_ = N; d = ImageDraw.Draw(im)
S.badge(im, 'TEIL 2 IST DA', 640, 1); S.text(im, 9, 0, 'DER ÜBERFALL AUF POLEN', 770, 92, S.YEL, 980); S.text(im, 9, 0, 'DEUTSCHLAND IM ZWEITEN WELTKRIEG', 880, 56, S.WHITE, 980)
S.flagbar(im, 950, 1); im.convert('RGB').save(B + 'social/YouTube_Post_Teil2_DE.jpg', quality=93); print('ok')
