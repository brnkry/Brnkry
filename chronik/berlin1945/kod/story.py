# Berlin 1945 short (German, CDM) Instagram/Facebook story: the hook of the short up to "Dann hielten sie an.", then a 5 s "Neues Video" card
# over the short's own picture running on (darkened). Voice ends with the hook; the music runs on and fades out.
import sys, os, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
S = sys.argv[1] + '/'; OUT = sys.argv[2]; SHORT = S + 'out/Berlin1945_Shorts_DE_v1.mp4'
W, H, FPS = 1080, 1920, 30; CARD = 5.0
Wd = json.load(open(S + 'words.json')); A1 = (Wd[14][2] + Wd[15][1]) / 2 + 0.2      # silence after "Dann hielten sie an."
assert Wd[14][0] == 'an.', Wd[14]
YEL, WHITE, CREAM, RED, DARK = (244, 199, 15), (245, 245, 240), (232, 226, 210), (196, 38, 40), (14, 15, 18)
F = '/tmp/claude-0/fonts/'
def anton(s): return ImageFont.truetype(F + 'Anton.ttf', s)
def bebas(s): return ImageFont.truetype(F + 'BebasNeue.ttf', s)
def eio(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def text(img, t, t0, s, y, fn, size, col, maxw=860):
    if t < t0: return
    f = fn(size)
    while f.getlength(s) > maxw: size -= 4; f = fn(size)
    u = eio((t - t0) / 0.4); La = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(La).text((520, y + 30 * (1 - u)), s, font=f, fill=col + (int(255 * u),), anchor='mm')
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(La.getchannel('A').point(lambda v: int(v * 0.8))); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (4, 8)); img.alpha_composite(La)
def badge(img, x, y, h=100):
    f = anton(int(h * 0.82)); d = ImageDraw.Draw(img); wc = d.textlength('C', font=f); gap, pad = h * 0.07, h * 0.06; cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'DM', font=f, anchor='lm')
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.06, b[2] + pad, b[3] + h * 0.05), fill=YEL)
    d.text((xd, cy), 'DM', font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.12, b[0] + h * 0.4, b[3] + h * 0.17), fill=RED)
def overlay(t):
    img = Image.new('RGBA', (W, H), (6, 8, 14, int(150 * eio(t / 0.6))))
    text(img, t, 0.4, 'SCHNELL INS PROFIL', 400, anton, 116, YEL)
    text(img, t, 0.6, 'UND ANSEHEN!', 525, anton, 96, WHITE)
    if t > 0.8:   # arrow to the profile name
        u = eio((t - 0.8) / 0.35); bob = 8 * math.sin((t - 0.8) * 6); a_, b_ = (250 + bob, 262 + bob * 0.6), (132 + bob, 178 + bob * 0.6)
        d = ImageDraw.Draw(img); ang = math.atan2(b_[1] - a_[1], b_[0] - a_[0]); hd = 50
        d.line((a_, b_), fill=YEL + (int(255 * u),), width=18)
        d.polygon([(b_[0] + 16 * math.cos(ang), b_[1] + 16 * math.sin(ang)), (b_[0] - hd * math.cos(ang - .55), b_[1] - hd * math.sin(ang - .55)), (b_[0] - hd * math.cos(ang + .55), b_[1] - hd * math.sin(ang + .55))], fill=YEL + (int(255 * u),))
    if t > 1.0:
        La = Image.new('RGBA', (W, H), (0, 0, 0, 0)); badge(La, 520 - 92, 760, 100); La.putalpha(La.getchannel('A').point(lambda v: int(v * min(1, (t - 1.0) / 0.4)))); img.alpha_composite(La)
    text(img, t, 1.2, 'NEUES VIDEO', 1010, bebas, 80, YEL)
    text(img, t, 1.5, 'BERLIN 1945', 1200, anton, 150, WHITE)
    s_ = 'IN 17 TAGEN · DIE ROTE ARMEE'; text(img, t, 1.75, s_, 1340, bebas, 90, CREAM)
    if t > 2.2:
        f = bebas(90); x0 = 520 - f.getlength(s_) / 2; x1 = x0 + f.getlength('IN 17 TAGEN'); u = eio((t - 2.2) / 0.35)
        ImageDraw.Draw(img).line((x0, 1386, x0 + (x1 - x0) * u, 1386), fill=RED + (250,), width=8)
    return img
if __name__ == '__main__':
    tmp = S + 'story_ov.mov'; n = int(CARD * FPS)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'qtrle', tmp], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(overlay(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    L = A1 + CARD
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SHORT, '-itsoffset', str(A1), '-i', tmp, '-ss', '30', '-i', S + 'music.mp3', '-filter_complex',
        f'[0:v]trim=0:{L:.3f},setpts=PTS-STARTPTS[v0];[v0][1:v]overlay=0:0:eof_action=pass[v];'
        f'[0:a]atrim=0:{A1:.3f},afade=t=out:st={A1 - 0.25:.3f}:d=0.25[h];[2:a]atrim=0:{L:.3f},volume=0.35,afade=t=in:st=0:d=0.3,afade=t=out:st={L - 1.6:.3f}:d=1.6[m];'
        '[h][m]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5[a]',
        '-map', '[v]', '-map', '[a]', '-t', f'{L:.3f}', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', OUT], check=True)
    os.remove(tmp); print('ok', round(L, 2))
