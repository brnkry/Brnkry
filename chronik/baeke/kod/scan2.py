# empty/low-quality check of every archive shot window; prints a frame strip per shot
import sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bb
mod = __import__(sys.argv[1]); st = mod.starts() if hasattr(mod, 'starts') else None
SH = mod.SH; TOT = mod.TOTAL
if st is None: st = [mod.K(s[0]) for s in SH]; st[0] = 0
fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12); rows = []
for i, s in enumerate(SH):
    if s[1] != 'vid': continue
    d = (st[i + 1] if i + 1 < len(SH) else TOT) - st[i] + bb.XF; src, cr = bb.VID[s[2]]
    vf = f'crop={cr[2]}:{cr[3]}:{cr[0]}:{cr[1]},fps={6 / d},scale=160:120'
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(s[3]), '-i', src, '-t', f'{d:.2f}', '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    n = len(raw) // (160 * 120 * 3); row = Image.new('RGB', (160 * 7, 120))
    lab = Image.new('RGB', (160, 120)); ImageDraw.Draw(lab).text((4, 4), f'#{i} {s[2]}\n{s[3]:.0f}s d={d:.1f}\n{s[0][:22]}', font=fnt, fill=(255, 255, 0)); row.paste(lab, (0, 0))
    for k in range(min(n, 6)): row.paste(Image.frombytes('RGB', (160, 120), raw[k * 57600:(k + 1) * 57600]), (160 * (k + 1), 0))
    rows.append(row)
S = Image.new('RGB', (160 * 7 * 2, 120 * ((len(rows) + 1) // 2)))
for k, r in enumerate(rows): S.paste(r, ((k % 2) * 1120, (k // 2) * 120))
S.save(bb.E + 'sheets/scan_' + sys.argv[1] + '.jpg', quality=85); print(len(rows))
