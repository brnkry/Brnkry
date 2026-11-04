# Rommel promo (German, Chronik der Macht): Instagram story and reel cut from the vertical video, ending on a "Link in Bio" card; YouTube post image
# usage: promo.py story|reel|post <out>
import sys, subprocess
_argv = list(sys.argv); sys.argv = ['x', 'list']
import full9 as V
from full9 import *
sys.argv = _argv
K = sys.argv[1]
SEG = {'story': (V.at(5) + 0.1, V.ST[9] - 0.12), 'reel': (0.0, V.ST[11] - 0.15)}   # story: "tot" .. "gelogen"; reel: intro .. name reveal
CARD = 4.6

def badge(can, x, y, h=100):
    f = anton(int(h * 0.82)); d = ImageDraw.Draw(can); wc = d.textlength('C', font=f); gap, pad = h * 0.07, h * 0.06; cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'DM', font=f, anchor='lm')
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.06, b[2] + pad, b[3] + h * 0.05), fill=YEL)
    d.text((xd, cy), 'DM', font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.12, b[0] + h * 0.42, b[3] + h * 0.16), fill=RED)
@functools.lru_cache(None)
def _bgcard(kind):
    a, b = SEG[kind]; im = V.frame(b - 0.05).convert('RGBA').filter(ImageFilter.GaussianBlur(26))
    im.alpha_composite(Image.new('RGBA', (W, H), (6, 7, 9, 170))); return im
def card(t, kind):
    """t from 0: last frame blurs away, then NEUES VIDEO / DIE GANZE GESCHICHTE / LINK IN BIO with an arrow up"""
    a, b = SEG[kind]; k = eio(t / 0.6)
    img = Image.blend(V.frame(b - 0.05).convert('RGBA'), _bgcard(kind), k)
    if t > 0.3:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); badge(L, CX - 92, 330, 100); L.putalpha(L.getchannel('A').point(lambda v: int(v * clamp((t - 0.3) / 0.4)))); img.alpha_composite(L)
    stamp(img, t, 0.5, 'NEUES VIDEO', (CX, 640), YEL, 70, -4)
    txt(img, t, 0.8, (CX, 860), 'ERWIN ROMMEL', anton(118), WHITE)
    txt(img, t, 1.0, (CX, 990), 'DIE GANZE GESCHICHTE', bebas(84), CREAM)
    txt(img, t, 1.4, (CX, 1200), 'LINK IN BIO', anton(130), YEL)
    if t > 1.7:   # arrow up towards the profile link
        u = clamp((t - 1.7) / 0.3); bob = 12 * math.sin((t - 1.7) * 6); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.polygon([(CX, 1300 + bob), (CX - 55, 1380 + bob), (CX + 55, 1380 + bob)], fill=YEL + (int(255 * u),)); d.rectangle((CX - 18, 1378 + bob, CX + 18, 1440 + bob), fill=YEL + (int(255 * u),))
        img.alpha_composite(L)
    img.alpha_composite(VIG); return img.convert('RGB')
def render(kind, out):
    a, b = SEG[kind]; n1 = int(round((b - a) * FPS)); n2 = int(CARD * FPS)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', B + K + '_v.mp4'], stdin=subprocess.PIPE)
    for i in range(n1):
        im = V.frame(a + i / FPS)
        if kind == 'story' and i < 9: im = Image.blend(Image.new('RGB', (W, H)), im, i / 9)
        p.stdin.write(np.asarray(im).tobytes())
    for i in range(n2): p.stdin.write(np.asarray(card(i / FPS, kind)).tobytes())
    p.stdin.close(); p.wait()
    L = (n1 + n2) / FPS; F = L - 1.0
    # sound: the video mix for the cut, then the music bed carries the card (swell + whoosh), fade out
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{n1 / FPS:.3f}', '-i', B + 'mix_9x16.wav', '-ss', f'{b:.3f}', '-t', f'{CARD + 0.5:.3f}', '-i', B + 'bed.wav',
                    '-filter_complex', f'[0:a]afade=t=in:d=0.25[x];[1:a]volume=0.5,afade=t=in:d=0.3[y];[x][y]concat=n=2:v=0:a=1,atrim=0:{L:.3f},afade=t=out:st={F:.3f}:d=1.0[o]',
                    '-map', '[o]', '-ar', '48000', B + K + '_a.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', B + K + '_v.mp4', '-i', B + K + '_a.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', B + out], check=True)
    print(out, round(L, 2), 's')
def post(out):
    """YouTube community post image 1080x1080"""
    from thumbs import cover, look, cdm, T as TT, plate as pl
    S2 = 1080; can = look(cover(src('r07'), S2, S2, 0.5, 0.42, 1.0)); sh = Image.new('RGBA', (S2, S2), (0, 0, 0, 0))
    g = (np.clip((np.arange(S2) - S2 * 0.4) / (S2 * 0.6), 0, 1) ** 1.3 * 235).astype(np.uint8); sh.putalpha(Image.fromarray(np.repeat(g[:, None], S2, 1))); can.alpha_composite(sh)
    cdm(can, 60, 50, 80); pl(can, (S2 / 2, 140), 'NEUES VIDEO', anton(64), YEL, DARK, rule=False)
    TT(can, (S2 / 2, 790), 'ERWIN ROMMEL', anton(130)); pl(can, (S2 / 2, 940), 'GIFT ODER PROZESS', anton(78))
    can.convert('RGB').save(B + out, quality=93); print(out)
if K == 'post': post(sys.argv[2])
else: render(K, sys.argv[2])
