# Otto Kretschmer short (German, CDM) Instagram/Facebook story (9:16): the hook of the short (one torpedo, one ship, then his name), then a
# "Neues Video" card over the night convoy film (ships burning) that keeps running behind it; 'Schnell ins Profil und ansehen!' on top with an arrow to the profile name.
import sys, subprocess
sys.argv = ['x', 'list']
import kshort as V
from kshort import *
from thumb_m import badge
A0, A1 = 0.0, 3.88   # the hook ends in the pause after 'Kretschmer' (the word ends at 3.86 s, 'gemessen' starts at 3.94 s)
CARD = 5.0
def bg(t):
    """the night convoy film with burning ships (6.8 s, longer than the card) runs behind the card, full frame"""
    im = V.fat('sc7', 0.0 + t); return grade(im.resize((W, H), Image.BICUBIC, box=V._cover(im.size, 9 / 16)).convert('RGBA'), 0.12, 0.85)
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
    title(img, t, 1.2, 'NEUES VIDEO', 1010, 80, YEL, None, 'bebas')
    title(img, t, 1.5, 'OTTO KRETSCHMER', 1200, 120, WHITE, bold=1, maxw=900)
    title(img, t, 1.75, 'EIN TORPEDO, EIN SCHIFF', 1330, 84, CREAM, fname='bebas', maxw=900)
    if t > 2.2:   # red line under EIN SCHIFF
        f = bebas(84); s_ = 'EIN TORPEDO, EIN SCHIFF'; x0 = CX - f.getlength(s_) / 2 + f.getlength('EIN TORPEDO, '); x1 = x0 + f.getlength('EIN SCHIFF'); u = eio((t - 2.2) / 0.35)
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).line((x0, 1372, lerp(x0, x1, u), 1372), fill=RED + (250,), width=8); img.alpha_composite(L)
    img.alpha_composite(VIG); return img.convert('RGB')
if __name__ == '__main__':
    out = B + 'social/Kretschmer_Story_DE.mp4'; os.makedirs(B + 'social', exist_ok=True)
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
    # voice and effects end with the hook; the music runs on as one continuous track, rises from under the voice and fades out slowly to the end
    h = n1 / FPS
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', B + 'vcut.wav', '-i', B + 'sfx.wav', '-i', B + 'bed_lev.wav',
                    '-filter_complex', f'[0:a]loudnorm=I=-15:TP=-1.5:LRA=9,aresample=48000,aformat=channel_layouts=stereo,atrim=0:{h:.3f},afade=t=out:st={h - 0.08:.3f}:d=0.08[v];'
                    f'[1:a]atrim=0:{h:.3f},afade=t=out:st={h - 0.3:.3f}:d=0.3[x];'
                    f"[2:a]aresample=48000,atrim=0:{L_:.3f},volume='if(lt(t,{h:.3f}),0.2,0.2+0.35*min(1,(t-{h:.3f})/0.6))':eval=frame,afade=t=out:st={L_ - 3.0:.3f}:d=3.0[b];"
                    f'[v][x][b]amix=inputs=3:normalize=0:duration=longest,atrim=0:{L_:.3f},alimiter=limit=0.93[o]',
                    '-map', '[o]', '-ar', '48000', B + 'story_a.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', B + 'story_v.mp4', '-i', B + 'story_a.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], check=True)
    print(out, round(L_, 2), 's')
