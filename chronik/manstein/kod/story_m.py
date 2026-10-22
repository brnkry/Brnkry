# Manstein Instagram/Facebook story (9:16): the hook of the short (plan rejected, France in six weeks), then a "Neues Video" card
# with an empty space marked for the link sticker. Story UI: everything between y 250 and 1670.
import sys, subprocess
sys.argv = ['x', 'list']
import mshort as V
from mshort import *
from thumb_m import badge
A0, A1 = 0.0, V.ST[2] - 0.15
CARD = 5.0
@functools.lru_cache(None)
def _bg():
    im = V.frame(A1 - 0.05).convert('RGBA').filter(ImageFilter.GaussianBlur(26)); im.alpha_composite(Image.new('RGBA', (W, H), (6, 7, 9, 175))); return im
def card(t):
    img = Image.blend(V.frame(A1 - 0.05).convert('RGBA'), _bg(), eio(t / 0.6))
    if t > 0.3:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); badge(L, CX - 92, 330, 100); L.putalpha(L.getchannel('A').point(lambda v: int(v * clamp((t - 0.3) / 0.4)))); img.alpha_composite(L)
    stamp(img, t, 0.5, 'NEUES VIDEO', (CX, 610), 70, -4, None, YEL)
    title(img, t, 0.8, 'ERICH VON MANSTEIN', 820, 112, WHITE, bold=1, maxw=900)
    title(img, t, 1.05, 'DER SAUBERE STRATEGE?', 950, 84, CREAM, fname='bebas', maxw=900)
    if t > 1.05:   # red line through SAUBERE once the line has settled
        f = bebas(84); s_ = 'DER SAUBERE STRATEGE?'; x0 = CX - f.getlength(s_) / 2 + f.getlength('DER '); x1 = x0 + f.getlength('SAUBERE'); u = eio((t - 1.5) / 0.35)
        if u > 0: L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).line((x0 - 6, 962, lerp(x0 - 6, x1 + 6, u), 950), fill=RED + (250,), width=9); img.alpha_composite(L)
    title(img, t, 1.9, 'JETZT ANSEHEN', 1150, 120, YEL)
    if t > 2.2:   # arrow down to where the link sticker goes
        u = clamp((t - 2.2) / 0.3); bob = 12 * math.sin((t - 2.2) * 6); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rectangle((CX - 18, 1235 + bob, CX + 18, 1295 + bob), fill=YEL + (int(255 * u),)); d.polygon([(CX, 1370 + bob), (CX - 55, 1290 + bob), (CX + 55, 1290 + bob)], fill=YEL + (int(255 * u),))
        img.alpha_composite(L)
    img.alpha_composite(VIG); return img.convert('RGB')
if __name__ == '__main__':
    out = B + 'social/Manstein_Story_DE.mp4'; os.makedirs(B + 'social', exist_ok=True)
    n1 = int(round((A1 - A0) * FPS)); n2 = int(CARD * FPS)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', B + 'story_v.mp4'], stdin=subprocess.PIPE)
    for i in range(n1): p.stdin.write(np.asarray(V.frame(A0 + i / FPS)).tobytes())
    for i in range(n2): p.stdin.write(np.asarray(card(i / FPS)).tobytes())
    p.stdin.close(); p.wait()
    L_ = (n1 + n2) / FPS; F_ = L_ - 1.0
    # sound: the short's mix for the hook, then the music bed under the card with a stamp hit, fade out
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-t', f'{n1 / FPS:.3f}', '-i', B + 'mix.wav', '-ss', f'{A1:.3f}', '-t', f'{CARD + 0.5:.3f}', '-i', B + 'bed_lev.wav',
                    '-filter_complex', f'[1:a]aresample=48000,volume=0.55,afade=t=in:d=0.3[y];[0:a]aresample=48000[x];[x][y]concat=n=2:v=0:a=1,atrim=0:{L_:.3f},afade=t=out:st={F_:.3f}:d=1.0[o]',
                    '-map', '[o]', '-ar', '48000', B + 'story_a.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', B + 'story_v.mp4', '-i', B + 'story_a.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], check=True)
    print(out, round(L_, 2), 's')
