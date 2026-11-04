# Teil 1 Instagram/Facebook story (9:16): the hook of the video (1919, not a single tank), then a "Neue Serie" card over the
# map page that keeps animating behind it; 'Schnell ins Profil und ansehen!' on top with an arrow to the profile name.
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.argv = [sys.argv[0], 'x'] + sys.argv[1:]
import teil1 as V
from magazine import W, H, FPS, eio, clamp, lerp
sys.path.insert(0, V.T1 + 'covlib'); import lib9 as L
YEL, RED, WHITE, DARK = L.YEL, L.RED, L.WHITE, L.DARK; osw = L.oswald; CX = W / 2
A1 = V.ws('Der', 5) - 0.1; CARD = 5.5
def text(img, t, t0, s, y, size, col, maxw=900):
    if t < t0: return
    k = eio((t - t0) / 0.35); f = osw(size)
    while f.getlength(s) > maxw: size -= 4; f = osw(size)
    La = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(La).text((CX, y + (1 - k) * 30), s, font=f, fill=col + (int(255 * k),), anchor='mm')
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, int(220 * k)), (0, 0), La.getchannel('A')); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (4, 8)); img.alpha_composite(La)
def plate(img, t, t0, s, y, size):
    if t < t0: return
    k = eio((t - t0) / 0.3); f = osw(size); d = ImageDraw.Draw(img); b = d.textbbox((CX, y), s, font=f, anchor='mm'); px, py = 30, 14
    sc = lerp(1.3, 1.0, k); w_, h_ = (b[2] - b[0]) / 2 + px, (b[3] - b[1]) / 2 + py
    Lp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(Lp); dl.rectangle((CX - w_ * sc, y - h_ * sc, CX + w_ * sc, y + h_ * sc), fill=YEL + (int(255 * k),))
    dl.text((CX, y), s, font=osw(int(size * sc)), fill=DARK + (int(255 * k),), anchor='mm'); dl.rectangle((CX - w_ * sc, y + h_ * sc + 12, CX - w_ * sc + 150, y + h_ * sc + 22), fill=RED + (int(255 * k),))
    img.alpha_composite(Lp)
def card(t):
    k = eio(t / 0.6); img = V.frame(66.5 + t * 1.4)   # the map page, steps hatching in behind the card
    img = Image.blend(img, img.filter(ImageFilter.GaussianBlur(5)), k).convert('RGBA')
    img.alpha_composite(Image.new('RGBA', (W, H), (6, 7, 9, int(212 * k))))
    text(img, t, 0.4, 'SCHNELL INS PROFIL', 400, 116, YEL); text(img, t, 0.6, 'UND ANSEHEN!', 525, 96, WHITE)
    if t > 0.8:
        u = eio((t - 0.8) / 0.35); bob = 8 * math.sin((t - 0.8) * 6); a_, b_ = (250 + bob, 262 + bob * 0.6), (132 + bob, 178 + bob * 0.6)
        La = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(La); ang = math.atan2(b_[1] - a_[1], b_[0] - a_[0]); hd = 50
        d.line((a_, b_), fill=YEL + (int(255 * u),), width=18)
        d.polygon([(b_[0] + 16 * math.cos(ang), b_[1] + 16 * math.sin(ang)), (b_[0] - hd * math.cos(ang - .55), b_[1] - hd * math.sin(ang - .55)), (b_[0] - hd * math.cos(ang + .55), b_[1] - hd * math.sin(ang + .55))], fill=YEL + (int(255 * u),))
        img.alpha_composite(La)
    plate(img, t, 1.1, 'NEUE SERIE', 820, 76)
    text(img, t, 1.4, 'DEUTSCHLAND IM', 1000, 120, WHITE); text(img, t, 1.6, 'ZWEITEN WELTKRIEG', 1130, 120, WHITE)
    text(img, t, 1.9, 'TEIL 1 · DER WEG IN DEN KRIEG', 1270, 70, YEL)
    return img.convert('RGB')
if __name__ == '__main__':
    B = V.T1; out = B + 'social/Teil1_Story_DE.mp4'; os.makedirs(B + 'social', exist_ok=True)
    if sys.argv[2:] and sys.argv[2] == 'p':
        for tt in (0.5, 2.5, 5.0): card(tt).resize((540, 960)).save(B + 'chk/st_c%s.jpg' % tt)
        sys.exit()
    n1 = int(round(A1 * FPS)); n2 = int(CARD * FPS)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', B + 'story_v.mp4'], stdin=subprocess.PIPE)
    for i in range(n1): p.stdin.write(np.asarray(V.frame(i / FPS)).tobytes())
    for i in range(n2): p.stdin.write(np.asarray(card(i / FPS)).tobytes())
    p.stdin.close(); p.wait()
    L_ = (n1 + n2) / FPS; F_ = L_ - 1.0
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-t', f'{n1 / FPS:.3f}', '-i', B + 'mix.wav', '-ss', f'{A1:.3f}', '-t', f'{CARD + 0.5:.3f}', '-i', B + 'bed_lev.wav',
                    '-filter_complex', f'[1:a]aresample=48000,volume=0.55,afade=t=in:d=0.3[y];[0:a]aresample=48000[x];[x][y]concat=n=2:v=0:a=1,atrim=0:{L_:.3f},afade=t=out:st={F_:.3f}:d=1.0[o]',
                    '-map', '[o]', '-ar', '48000', B + 'story_a.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', B + 'story_v.mp4', '-i', B + 'story_a.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], check=True)
    print(out, round(L_, 2), 's')
