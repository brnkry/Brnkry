# Kittel short (Wick recipe); Wick short (German, CDM) Instagram/Facebook story (9:16): the hook of the short (bombers in the night sky, the words typing on),
# cut in the silence after "Frankreich.", then a "Neues Video" card over the same film, which keeps running behind it.
# "Schnell ins Profil und ansehen!" on top with an arrow to the profile name. Voice ends with the hook; the music runs on and fades out.
import sys, os, math, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import ws, wk as eg
from wk import W, H, FPS, E, eio, clamp, lerp
import lib9 as L
YEL, WHITE, CREAM, RED = L.YEL, L.WHITE, L.CREAM, L.RED
import json as _j; _W = _j.load(open(E + 'words.json')); A1 = (_W[10][2] + _W[11][1]) / 2   # cut in the silence after 'Wehrmacht.'
CARD = 5.0
CX = 540
def text(img, t, t0, s, y, font, col, maxw=900):
    if t < t0: return
    fn, size = font; font = fn(size)
    while font.getlength(s) > maxw: size -= 4; font = fn(size)
    u = eio((t - t0) / 0.4); La = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(La)
    d.text((CX, y + 30 * (1 - u)), s, font=font, fill=col + (int(255 * u),), anchor='mm')
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(La.getchannel('A').point(lambda v: int(v * 0.8))); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (4, 8)); img.alpha_composite(La)
def badge(img, x, y, h=100):
    f = L.anton(int(h * 0.82)); d = ImageDraw.Draw(img); wc = d.textlength('C', font=f); gap, pad = h * 0.07, h * 0.06; cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'DM', font=f, anchor='lm')
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.06, b[2] + pad, b[3] + h * 0.05), fill=YEL)
    d.text((xd, cy), 'DM', font=f, fill=(14, 15, 18), anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.12, b[0] + h * 0.4, b[3] + h * 0.17), fill=RED)
def card(t):
    img = eg.hookbg(A1 + t)   # the blue-toned hook film keeps running behind the card (as in the Egon story)
    img.alpha_composite(Image.new('RGBA', (W, H), (6, 8, 14, int(115 * eio(t / 0.6)))))
    text(img, t, 0.4, 'SCHNELL INS PROFIL', 400, (L.anton, 116), YEL)
    text(img, t, 0.6, 'UND ANSEHEN!', 525, (L.anton, 96), WHITE)
    if t > 0.8:   # arrow to the profile name
        u = eio((t - 0.8) / 0.35); bob = 8 * math.sin((t - 0.8) * 6); a_, b_ = (250 + bob, 262 + bob * 0.6), (132 + bob, 178 + bob * 0.6)
        La = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(La); ang = math.atan2(b_[1] - a_[1], b_[0] - a_[0]); hd = 50
        d.line((a_, b_), fill=YEL + (int(255 * u),), width=18)
        d.polygon([(b_[0] + 16 * math.cos(ang), b_[1] + 16 * math.sin(ang)), (b_[0] - hd * math.cos(ang - .55), b_[1] - hd * math.sin(ang - .55)), (b_[0] - hd * math.cos(ang + .55), b_[1] - hd * math.sin(ang + .55))], fill=YEL + (int(255 * u),))
        img.alpha_composite(La)
    if t > 1.0:
        La = Image.new('RGBA', (W, H), (0, 0, 0, 0)); badge(La, CX - 92, 760, 100); La.putalpha(La.getchannel('A').point(lambda v: int(v * clamp((t - 1.0) / 0.4)))); img.alpha_composite(La)
    text(img, t, 1.2, 'NEUES VIDEO', 1010, (L.bebas, 80), YEL)
    text(img, t, 1.5, 'SEPP ALLERBERGER', 1200, (L.anton, 140), WHITE)
    s_ = '257 ABSCHÜSSE · OSTFRONT'; text(img, t, 1.75, s_, 1340, (L.bebas, 90), CREAM)
    if t > 2.2:   # red line under VON VORNE
        f = L.bebas(90); x0 = CX - f.getlength(s_) / 2; x1 = x0 + f.getlength('257 ABSCHÜSSE'); u = eio((t - 2.2) / 0.35)
        La = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(La).line((x0, 1386, lerp(x0, x1, u), 1386), fill=RED + (250,), width=8); img.alpha_composite(La)
    return eg.finish(img, 10 + t)
if __name__ == '__main__':
    os.makedirs(E + 'social', exist_ok=True); out = E + 'social/Allerberger_Story_DE.mp4'
    if len(sys.argv) > 1 and sys.argv[1] == 'p':
        P = Image.new('RGB', (4 * 270, 480))
        for i, tt in enumerate((0.5, 1.6, 2.6, 4.8)): P.paste(card(tt).convert('RGB').resize((270, 480)), (i * 270, 0))
        P.save(E + 'chk/story.jpg'); sys.exit()
    n1 = int(round(A1 * FPS)); n2 = int(CARD * FPS)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', E + 'story_v.mp4'], stdin=subprocess.PIPE)
    for i in range(n1): p.stdin.write(np.asarray(eg.frame(i / FPS).convert('RGB')).tobytes())
    for i in range(n2): p.stdin.write(np.asarray(card(i / FPS).convert('RGB')).tobytes())
    p.stdin.close(); p.wait()
    L_ = (n1 + n2) / FPS; h = n1 / FPS
    # voice and effects end with the hook (cut in the silence after a word); the music is one continuous track that rises after the voice and fades out slowly
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', E + 'vcut.wav', '-i', E + 'sfx.wav', '-i', E + 'bed.wav',
                    '-filter_complex', f'[0:a]loudnorm=I=-15:TP=-1.5:LRA=9,aresample=48000,aformat=channel_layouts=stereo,atrim=0:{h:.3f},afade=t=out:st={h - 0.06:.3f}:d=0.06[v];'
                    f'[1:a]atrim=0:{h:.3f},afade=t=out:st={h - 0.3:.3f}:d=0.3[x];'
                    f"[2:a]aresample=48000,atrim=0:{L_:.3f},volume='if(lt(t,{h:.3f}),0.45,0.45+0.4*min(1,(t-{h:.3f})/0.6))':eval=frame,afade=t=out:st={L_ - 3.0:.3f}:d=3.0[b];"
                    f'[v][x][b]amix=inputs=3:normalize=0:duration=longest,atrim=0:{L_:.3f},alimiter=limit=0.93[o]',
                    '-map', '[o]', '-ar', '48000', E + 'story_a.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', E + 'story_v.mp4', '-i', E + 'story_a.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], check=True)
    print(out, round(L_, 2), 's')
