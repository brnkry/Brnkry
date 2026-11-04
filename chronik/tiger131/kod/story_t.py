# Tiger 131 (German, CDM) Instagram/Facebook story (9:16): the hook of the short (archive film 1943, then Tiger 131 today), then a
# "Neues Video" card over Tiger 131 driving today, the film keeps running behind it; 'Schnell ins Profil und ansehen!' on top with an arrow to the profile name.
import sys, subprocess
sys.argv = ['x', 'list']
import tshort as V
from tshort import *
from thumb_m import badge
A0, A1 = 0.0, V.ws('Sein', 8.5) - 0.12   # the hook: left behind in 1943, still running today; the name comes on the card
CARD = 5.0
def bg(t):
    """Tiger 131 driving in the rain runs behind the card, full frame"""
    im = V.fat('m_close', 0.5 + t); return grade(im.resize((W, H), Image.BICUBIC, box=V._cover(im.size, 9 / 16)).convert('RGBA'), 0.12, 0.85)
def card(t):
    img = bg(t)
    img.alpha_composite(Image.new('RGBA', (W, H), (6, 7, 9, int(170 * eio(t / 0.6)))))
    title(img, t, 0.4, 'SCHNELL INS PROFIL', 400, 116, YEL, maxw=900)
    title(img, t, 0.6, 'UND ANSEHEN!', 525, 96, WHITE)
    if t > 0.8:   # arrow to the profile name, a little higher than in the Manstein story
        u = eio((t - 0.8) / 0.35); bob = 8 * math.sin((t - 0.8) * 6); a_, b_ = (250, 262), (132, 178)
        a_ = (a_[0] + bob, a_[1] + bob * 0.6); b_ = (b_[0] + bob, b_[1] + bob * 0.6)
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); ang = math.atan2(b_[1] - a_[1], b_[0] - a_[0]); hd = 50
        d.line((a_, b_), fill=YEL + (int(255 * u),), width=18)
        d.polygon([(b_[0] + 16 * math.cos(ang), b_[1] + 16 * math.sin(ang)), (b_[0] - hd * math.cos(ang - .55), b_[1] - hd * math.sin(ang - .55)), (b_[0] - hd * math.cos(ang + .55), b_[1] - hd * math.sin(ang + .55))], fill=YEL + (int(255 * u),))
        img.alpha_composite(L)
    if t > 1.0:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); badge(L, CX - 92, 760, 100); L.putalpha(L.getchannel('A').point(lambda v: int(v * clamp((t - 1.0) / 0.4)))); img.alpha_composite(L)
    stamp(img, t, 1.2, 'NEUES VIDEO', (CX, 1010), 70, -4, None, YEL)
    title(img, t, 1.5, 'TIGER 131', 1200, 130, WHITE, bold=1, maxw=900)
    title(img, t, 1.75, 'ER FÄHRT BIS HEUTE', 1330, 84, CREAM, fname='bebas', maxw=900)
    if t > 2.2:   # red line under SIRENE
        f = bebas(84); s_ = 'ER FÄHRT BIS HEUTE'; x0 = CX - f.getlength(s_) / 2 + f.getlength('ER FÄHRT BIS '); x1 = x0 + f.getlength('HEUTE'); u = eio((t - 2.2) / 0.35)
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).line((x0, 1372, lerp(x0, x1, u), 1372), fill=RED + (250,), width=8); img.alpha_composite(L)
    img.alpha_composite(VIG); return img.convert('RGB')
if __name__ == '__main__':
    out = B + 'social/Tiger131_Story_DE.mp4'; os.makedirs(B + 'social', exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == 'p':
        for tt in (2.0, 4.0): V.frame(tt).convert('RGB').resize((540, 960)).save(B + 'chk/st_%s.jpg' % tt)
        for tt in (0.5, 2.5, 4.8): card(tt).resize((540, 960)).save(B + 'chk/st_c%s.jpg' % tt)
        sys.exit()
    n1 = int(round((A1 - A0) * FPS)); n2 = int(CARD * FPS)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', B + 'story_v.mp4'], stdin=subprocess.PIPE)
    for i in range(n1): p.stdin.write(np.asarray(V.frame(A0 + i / FPS)).tobytes())
    for i in range(n2): p.stdin.write(np.asarray(card(i / FPS)).tobytes())
    p.stdin.close(); p.wait()
    L_ = (n1 + n2) / FPS; F_ = L_ - 1.0
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-t', f'{n1 / FPS:.3f}', '-i', B + 'mix.wav', '-ss', f'{A1:.3f}', '-t', f'{CARD + 0.5:.3f}', '-i', B + 'bed_lev.wav',
                    '-filter_complex', f'[1:a]aresample=48000,volume=0.55,afade=t=in:d=0.3[y];[0:a]aresample=48000[x];[x][y]concat=n=2:v=0:a=1,atrim=0:{L_:.3f},afade=t=out:st={F_:.3f}:d=1.0[o]',
                    '-map', '[o]', '-ar', '48000', B + 'story_a.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', B + 'story_v.mp4', '-i', B + 'story_a.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], check=True)
    print(out, round(L_, 2), 's')
