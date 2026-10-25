# cover composite for the Udet short: the Stuka formation photo (u08), the lead plane large in front,
# Udet's portrait (u03) in the sky behind it like a double exposure -> img/cov.jpg (covers4.py job 'udet_de' adds the fixed layout)
import sys; sys.path.insert(0, sys.argv[1] + '/code')
from lib9 import *
import cv2
VW, VH = 1080, 1920
p = src('u08'); s = 1.22; x0 = 852; PY = 670; y0 = 150 - PY / s       # the lead plane (src y 150..480) lands at screen y PY..PY+380
top = int(-y0 * s) + 2
pic = p.resize((VW, VH - top), Image.LANCZOS, box=(x0, 0, x0 + VW / s, (VH - top) / s)).convert('RGB')
can = Image.new('RGB', (VW, VH)); row = np.asarray(pic.crop((0, 0, VW, 6))).astype(np.float32).mean(0)
g = np.linspace(0.6, 1.0, top)[:, None, None] * row[None]          # the sky carried up, deeper towards the top
can.paste(Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)), (0, 0)); can.paste(pic, (0, top))
# what is not sky (the planes) stays in front of the portrait
hsv = cv2.cvtColor(np.asarray(can), cv2.COLOR_RGB2HSV).astype(int)
sky = (hsv[..., 0] > 95) & (hsv[..., 0] < 120) & (hsv[..., 2] > 150) & (hsv[..., 1] < 140)
sky = cv2.morphologyEx(sky.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)); front = 1 - cv2.GaussianBlur(sky.astype(np.float32), (0, 0), 2)
front[:top] = 0
# Udet in the sky: warm, slightly muted, soft edges
u = src('u03').crop((150, 110, 1390, 1250)); u = u.resize((1080, 993), Image.LANCZOS)
u = ImageEnhance.Contrast(ImageEnhance.Color(u).enhance(0.7)).enhance(1.05)
yy, xx = np.mgrid[0:VH, 0:VW]; fade = np.clip((1060 - yy) / 160, 0, 1) * np.clip(1 - (np.abs(xx - 540) - 300) / 240, 0, 1) * (1 - front)
U = np.zeros((VH, VW, 3), np.float32); U[:993] = np.asarray(u, np.float32)
a = (fade * 0.92)[..., None]; out = np.asarray(can, np.float32) * (1 - a) + U * a
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(B + 'img/cov.jpg', quality=95); print('ok')
