# Manstein Instagram/Facebook story (9:16): the hook of the short (plan rejected, France in six weeks), then a "Neues Video" card
# over the Stuka shot that keeps playing behind it; 'Schnell ins Profil und ansehen!' on top with an arrow to the profile name. Story UI: everything between y 250 and 1670.
import sys, subprocess
sys.argv = ['x', 'list']
import mshort as V
from mshort import *
from thumb_m import badge
A0, A1 = 0.0, V.ST[2] - 0.15
CARD = 5.0
# the Stuka newsreel shot that ends the hook keeps running behind the card (same crop as in the short, so flag and watermark stay out)
_fr = [x for x in V.SC if x[2] is V.s_france][0]
CLIP_T = 0.2 + (A1 - _fr[0])   # newsreel time at the cut (the shot plays at normal speed in the short)
BG = V.C(CLIP_T, CLIP_T + CARD + 0.3, None, 0.15, 1.3, 1.0, 1.3, 0.3)
def card(t):
    img = BG(t, 0.0, CARD + 0.3)
    img.alpha_composite(Image.new('RGBA', (W, H), (6, 7, 9, int(170 * eio(t / 0.6)))))
    # call to action on top, right under the story header, with an arrow to the profile name (top left) that viewers tap
    title(img, t, 0.4, 'SCHNELL INS PROFIL', 400, 116, YEL, maxw=900)
    title(img, t, 0.6, 'UND ANSEHEN!', 525, 96, WHITE)
    if t > 0.8:
        u = eio((t - 0.8) / 0.35); bob = 8 * math.sin((t - 0.8) * 6); a_, b_ = (255, 300), (140, 232)
        a_ = (a_[0] + bob, a_[1] + bob * 0.6); b_ = (b_[0] + bob, b_[1] + bob * 0.6)
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); ang = math.atan2(b_[1] - a_[1], b_[0] - a_[0]); hd = 50
        d.line((a_, b_), fill=YEL + (int(255 * u),), width=18)
        d.polygon([(b_[0] + 16 * math.cos(ang), b_[1] + 16 * math.sin(ang)), (b_[0] - hd * math.cos(ang - .55), b_[1] - hd * math.sin(ang - .55)), (b_[0] - hd * math.cos(ang + .55), b_[1] - hd * math.sin(ang + .55))], fill=YEL + (int(255 * u),))
        img.alpha_composite(L)
    if t > 1.0:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); badge(L, CX - 92, 760, 100); L.putalpha(L.getchannel('A').point(lambda v: int(v * clamp((t - 1.0) / 0.4)))); img.alpha_composite(L)
    stamp(img, t, 1.2, 'NEUES VIDEO', (CX, 1010), 70, -4, None, YEL)
    title(img, t, 1.5, 'ERICH VON MANSTEIN', 1200, 112, WHITE, bold=1, maxw=900)
    title(img, t, 1.75, 'DER SAUBERE STRATEGE?', 1330, 84, CREAM, fname='bebas', maxw=900)
    if t > 1.75:   # red line through SAUBERE once the line has settled
        f = bebas(84); s_ = 'DER SAUBERE STRATEGE?'; x0 = CX - f.getlength(s_) / 2 + f.getlength('DER '); x1 = x0 + f.getlength('SAUBERE'); u = eio((t - 2.2) / 0.35)
        if u > 0: L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).line((x0 - 6, 1342, lerp(x0 - 6, x1 + 6, u), 1330), fill=RED + (250,), width=9); img.alpha_composite(L)
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
