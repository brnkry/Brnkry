# ~12 s story (Laidlaw): the hook of the Short, then the photo blurs and a call to watch the full video on the profile
import sys, subprocess
sys.argv_saved = list(sys.argv)
import laid as luu
from laid import *

T_END = 12.0; T_CUT = 8.3
# the portrait keeps moving through the whole story: its window runs to the end
luu.SC[:] = [(0.0, 12.5, luu.SC[0][2], luu.SC[0][3])]

def icon_follow(sz, col):
    L = Image.new('RGBA', (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = sz / 2
    d.ellipse((c - sz * 0.16, sz * 0.12, c + sz * 0.16, sz * 0.44), fill=col)
    d.pieslice((c - sz * 0.32, sz * 0.48, c + sz * 0.32, sz * 1.1), 180, 360, fill=col)
    d.rectangle((sz * 0.74, sz * 0.2, sz * 0.8, sz * 0.5), fill=col); d.rectangle((sz * 0.62, sz * 0.32, sz * 0.92, sz * 0.38), fill=col)
    return L
def icon_heart(sz, col):
    L = Image.new('RGBA', (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(L); r = sz * 0.24
    d.ellipse((sz * 0.12, sz * 0.18, sz * 0.12 + 2 * r, sz * 0.18 + 2 * r), fill=col); d.ellipse((sz * 0.88 - 2 * r, sz * 0.18, sz * 0.88, sz * 0.18 + 2 * r), fill=col)
    d.polygon([(sz * 0.13, sz * 0.46), (sz * 0.87, sz * 0.46), (sz * 0.5, sz * 0.88)], fill=col)
    return L
def icon_share(sz, col):
    L = Image.new('RGBA', (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.polygon([(sz * 0.12, sz * 0.48), (sz * 0.88, sz * 0.14), (sz * 0.6, sz * 0.88), (sz * 0.48, sz * 0.58)], fill=col)
    d.polygon([(sz * 0.48, sz * 0.58), (sz * 0.88, sz * 0.14), (sz * 0.42, sz * 0.52)], fill=(0, 0, 0, 0))
    return L
ICONS = [(icon_follow, 'FOLGEN'), (icon_heart, 'LIKEN'), (icon_share, 'TEILEN')]

def story_frame(t):
    if t < T_CUT: img = frame(t).convert('RGBA')
    else:
        k = eio((t - T_CUT) / 0.8)
        ph = shot(pan_lin('j09', t, 0.0, 12.5, 1150, 1), GRAD_SOFT).filter(ImageFilter.GaussianBlur(4 + 22 * k))
        ph.alpha_composite(Image.new('RGBA', (W, H), (4, 6, 8, int(165 * k))))
        img = Image.blend(frame(t).convert('RGBA'), ph, min(1, k * 1.3))
        tt = T_CUT + 0.4
        plate(img, t, tt, 'NEUES VIDEO', 520, size=64, bg=RUST, fg=CREAM)
        focus(img, t, tt + 0.3, 'DIE GANZE GESCHICHTE', 'serif', 110, CREAM, 720)
        focus(img, t, tt + 0.6, 'JETZT IM PROFIL', 'serif', 130, GOLD, 860)
        if t > tt + 0.9:   # arrow pointing up to the profile
            a = clamp((t - tt - 0.9) / 0.3); bob = 10 * math.sin((t - tt) * 6)
            L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            d.polygon([(540, 300 + bob), (490, 370 + bob), (590, 370 + bob)], fill=GOLD + (int(255 * a),))
            d.rectangle((525, 368 + bob, 555, 430 + bob), fill=GOLD + (int(255 * a),)); img.alpha_composite(L)
        for i, (fn, lab) in enumerate(ICONS):
            ti = tt + 1.4 + i * 0.35
            if t < ti: continue
            k2 = eout((t - ti) / 0.35); x = 270 + i * 270; y = 1260
            L = Image.new('RGBA', (220, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            d.ellipse((10, 10, 210, 210), fill=CREAM + (240,)); L.alpha_composite(fn(120, DEEP + (255,)), (50, 48))
            put(img, L, x, y, lerp(0.4, 1.0, k2), k2)
            put(img, sprite(lab, 'cond', 52, CREAM, True, 3), x, y + 150, 1.0, k2)
    if t >= T_CUT: img.alpha_composite(VIG)
    if t > T_END - 0.4: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * clamp((t - T_END + 0.4) / 0.4)))))
    return img.convert('RGB')

if __name__ == '__main__':
    out = sys.argv_saved[1]; big = len(sys.argv_saved) > 2 and sys.argv_saved[2] == '4k'
    size = '2160x3840' if big else f'{W}x{H}'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', size, '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
    for n in range(int(T_END * FPS)):
        im = story_frame(n / FPS)
        if big: im = im.resize((2160, 3840), Image.LANCZOS)
        p.stdin.write(np.asarray(grain(im, n)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
