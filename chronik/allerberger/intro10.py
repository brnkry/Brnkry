# 10 s intro demo: style-A hook type on a blue film, then the cut-out portrait steps into the scene, then a push-through
# transition carries the camera to the next cut-out photo. Type always on the left (Shorts buttons on the right, title at the bottom).
import sys, math, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
S = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/'
sys.path.insert(0, S + 'egon/code'); import eg
from eg import mont, gtext_a, put, typed, YEL, CREAM, DARK, LIGHT, eout, eio, clamp, lerp
W, H, FPS, T = 1080, 1920, 30, 10.0
def ease_back(u): u = clamp(u); c = 1.4; return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
@functools.lru_cache(maxsize=40)
def film(i, key):
    im = Image.open(S + 'kittel/clipL/%s/%05d.jpg' % (key, i)).convert('L'); w, h = im.size; cw = h * 9 / 16
    im = im.crop(((w - cw) / 2, 0, (w + cw) / 2, h)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2))
    g = np.asarray(im, np.float32)[..., None] / 255; g = np.clip((g - 0.5) * 1.2 + 0.5, 0, 1)
    a = np.array(DARK, np.float32) + g * (np.array(LIGHT, np.float32) * 1.15 - np.array(DARK, np.float32))
    yy = np.linspace(0, 1, H)[:, None, None]; a *= 1 - 0.5 * np.clip((yy - 0.5) / 0.5, 0, 1)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def bg(t):
    key, n = ('ice', 340) if t < 6.6 else ('front', 300)
    return film(1 + int((t if t < 6.6 else t - 6.6) * 25) % n + (0 if t < 6.6 else 40), key).convert('RGBA')
def soft_top(a, n=90):
    A = np.asarray(a, np.float32); h, w = A.shape
    A *= np.clip(np.arange(h) / n, 0, 1)[:, None]; return Image.fromarray(A.astype(np.uint8))
@functools.lru_cache(None)
def cutout(path, height, blur_pts=()):
    P = Image.open(path).convert('RGBA'); P = P.crop(P.getbbox()); sc = height / P.height; P = P.resize((int(P.width * sc), height), Image.LANCZOS)
    rgb = P.convert('RGB')
    for cx, cy, r in blur_pts:   # symbols, in cut-out pixel coordinates
        m = Image.new('L', P.size, 0); ImageDraw.Draw(m).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255); rgb = Image.composite(rgb.filter(ImageFilter.GaussianBlur(7)), rgb, m.filter(ImageFilter.GaussianBlur(3)))
    a = soft_top(P.getchannel('A')); out = rgb.convert('RGBA'); out.putalpha(a)
    glow = Image.new('RGBA', (P.width + 120, P.height + 120), (0, 0, 0, 0)); gm = Image.new('L', glow.size, 0); gm.paste(a.filter(ImageFilter.MaxFilter(9)), (60, 60))
    glow.paste((235, 220, 190, 255), (0, 0), gm.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.7)))
    sh = Image.new('RGBA', glow.size, (0, 0, 0, 0)); sm = Image.new('L', glow.size, 0); sm.paste(a, (30, 80)); sh.paste((0, 0, 0, 255), (0, 0), sm.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.6)))
    sh.alpha_composite(glow); sh.alpha_composite(out, (60, 60)); return sh
def place(can, im, cx, by, sc=1.0, rot=0.0, alpha=1.0, mblur=0):
    if sc != 1.0: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
    if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    if mblur > 1: im = im.filter(ImageFilter.BoxBlur(mblur))
    if alpha < 1: a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    can.alpha_composite(im, (int(cx - im.width / 2), int(by - im.height)))
def txt(can, s, t, t0, y, size, col, cps=16, x=60, out=None):
    if t < t0: return
    al = typed(s, t, t0, cps, 0.18)
    if out is not None and t > out: k = clamp(1 - (t - out) / 0.25); al = [a * k for a in al]; x -= 80 * (1 - k)
    put(can, gtext_a(s, mont(size, 900), col, al, -2), x, y, 'l')
POR = cutout(S + 'allb/cut.png', 1250, ((415, 52, 22), (322, 968, 24), (566, 905, 18)))
TNK = cutout(S + 'allb/cut_b22.png', 760)
def frame(t):
    can = bg(t)
    # --- 0 to 3.3: the hook, type only
    o1 = 3.25
    txt(can, 'ER WAR DER ZWEIT-', t, 0.15, 640, 82, CREAM, out=o1); txt(can, 'ERFOLGREICHSTE', t, 0.75, 740, 96, YEL, out=o1)
    txt(can, 'SCHARFSCHÜTZE', t, 1.45, 850, 96, YEL, out=o1); txt(can, 'DER WEHRMACHT.', t, 2.2, 950, 82, CREAM, out=o1)
    # --- 3.4 to 6.4: his name, the portrait steps in from below and keeps a slow push
    t1 = 3.45
    if t >= t1:
        u = ease_back((t - t1) / 0.9); push = 1 + 0.025 * max(0, t - t1 - 0.9)
        if t < 6.35: place(can, POR, 700, lerp(H + 900, H + 40, u), push)
    txt(can, 'SEIN NAME:', t, t1 + 0.05, 330, 56, CREAM, out=6.2)
    txt(can, 'JOSEF', t, t1 + 0.45, 420, 104, CREAM, out=6.2); txt(can, '„SEPP“', t, t1 + 0.8, 525, 104, YEL, out=6.2); txt(can, 'ALLERBERGER', t, t1 + 1.15, 630, 104, CREAM, out=6.2)
    # --- 6.35 to 7.1: push-through: the portrait rushes past the camera (scale up, out to the left), the film whips, the next photo flies in
    tt = 6.35
    if tt <= t < tt + 0.45:
        u = eio((t - tt) / 0.45); place(can, POR, lerp(700, -500, u), H + 40 + 900 * u * u, 1.08 + 1.4 * u, 0, 1.0, int(30 * u))
    if t >= tt + 0.15:
        u = ease_back((t - tt - 0.15) / 0.75); drift = max(0, t - tt - 0.9)
        place(can, TNK, lerp(1700, 640 - 8 * drift, u), 1480, lerp(1.35, 1.0, eout(clamp((t - tt - 0.15) / 0.75))) * (1 + 0.012 * drift), lerp(-12, -2, u), 1.0, int(max(0, 26 * (1 - (t - tt - 0.15) / 0.4))))
    # whip flash between the two films
    if tt - 0.1 <= t < tt + 0.5:
        k = math.sin(math.pi * clamp((t - tt + 0.1) / 0.6)); fl = Image.new('RGBA', can.size, (235, 225, 205, int(70 * k))); can.alpha_composite(fl)
    txt(can, '1942', t, tt + 0.7, 360, 150, CREAM, cps=10); txt(can, 'OSTFRONT', t, tt + 1.05, 480, 84, YEL)
    txt(can, 'ERST MG-SCHÜTZE,', t, tt + 1.6, 1560 - 980, 50, CREAM, cps=22); txt(can, 'DANN SCHARFSCHÜTZE.', t, tt + 2.3, 1640 - 980, 50, CREAM, cps=22)
    # the old film kept moving under the whip: horizontal smear during the cut
    if tt - 0.05 <= t < tt + 0.35:
        k = math.sin(math.pi * clamp((t - tt + 0.05) / 0.4)); a_ = np.asarray(can).astype(np.float32); n_ = max(1, int(18 * k)); can = Image.fromarray((sum(np.roll(a_, s_, axis=1) for s_ in range(-n_, n_ + 1, max(1, n_ // 4))) / len(range(-n_, n_ + 1, max(1, n_ // 4)))).astype(np.uint8)) if k > 0.05 else can
    return eg.finish(can, t)
if __name__ == '__main__':
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[3:]]; P_ = Image.new('RGB', (len(ts) * 270, 480))
        for i, t in enumerate(ts): P_.paste(frame(t).convert('RGB').resize((270, 480)), (i * 270, 0))
        P_.save(sys.argv[2]); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
    for n in range(int(a * FPS), int(b * FPS)): p.stdin.write(np.asarray(frame(n / FPS).convert('RGB')).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
