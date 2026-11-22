"""Two faces into one: left half from A, right half from B, eyes and mouth on the same points, misty dark seam."""
import sys, numpy as np
from PIL import Image, ImageFilter
W, H = 1280, 720
DST = np.array([(740, 360), (1020, 360), (880, 612)], float)
def warp(path, pts):
    S = np.array(pts, float)
    im = Image.open(path).convert('RGB')
    # only the picture inside the 2.35 letterbox is valid; feather its edge so no hard line shows
    v = Image.new('L', im.size, 0); v.paste(255, (40, 134 + 90, im.width - 40, im.height - 134 - 90) if im.height == 1080 else (0, 0, im.width, im.height))
    # affine from canvas -> source: [x y 1] @ M = src
    A = np.c_[DST, np.ones(3)]; M = np.linalg.solve(A, S)
    a, d = M[0]; b, e = M[1]; c, f = M[2]
    T = (a, b, c, d, e, f)
    rgb = np.asarray(im.transform((W, H), Image.AFFINE, T, resample=Image.BICUBIC)).astype(float)
    val = np.asarray(v.transform((W, H), Image.AFFINE, T, resample=Image.BILINEAR).filter(ImageFilter.GaussianBlur(110))).astype(float) / 255
    val = np.clip(val * 1.5 - 0.25, 0, 1) ** 1.3
    return np.dstack([rgb, val])
def compose(a, pa, b, pb, out):
    A = warp(a, pa); B = warp(b, pb); va = A[..., 3:]; vb = B[..., 3:]; A = A[..., :3]; B = B[..., :3]
    x = np.arange(W)[None, :, None]; c = 880; w = 60
    t = np.clip((x - (c - w)) / (2 * w), 0, 1); t = t * t * (3 - 2 * t)
    o = A * (1 - t) + B * t; val = va * (1 - t) + vb * t
    n = np.random.default_rng(3).random((H // 8, W // 8))
    n = np.asarray(Image.fromarray((n * 255).astype('uint8')).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(18))).astype(float) / 255
    band = np.exp(-((x[..., 0] - c) / 50.0) ** 2)[..., None] * (0.55 + 0.45 * n[..., None])
    o = o * (1 - 0.7 * band)
    yy, xx = np.mgrid[0:H, 0:W]
    dd = ((xx - 900) / 520.0) ** 2 + ((yy - 420) / 440.0) ** 2
    m = np.clip((1.15 - dd) / 0.55, 0, 1); m = m * m * (3 - 2 * m)
    al = m[..., None] * val
    Image.fromarray(np.clip(o * al + np.array([7, 6, 10.]) * (1 - al), 0, 255).astype('uint8')).save(out, quality=95)
    Image.fromarray(np.dstack([np.clip(o, 0, 255), al[..., 0] * 255]).astype('uint8'), 'RGBA').save(out.replace('.jpg', '.png'))
YONE_H = [(400, 386), (820, 300), (720, 820)]
YONE_M = [(816, 492), (1104, 492), (960, 740)]
YASUO = [(1290, 270), (1580, 220), (1500, 535)]
compose('yone_insan.jpg', YONE_H, 'yone_maske.jpg', YONE_M, 'yone_ikiyuz_v.jpg')
compose('yasuo_yuz.jpg', YASUO, 'yone_insan.jpg', YONE_H, 'yasuo_yone_yuz.jpg')
