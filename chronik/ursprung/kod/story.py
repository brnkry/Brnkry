# Instagram/Facebook story (9:16) for the long video: its first two sentences (16:9 picture over a blurred copy), then a 5 s "Neues Video" card
import sys, os, math, subprocess, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont
U = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/urs/'
SRC = U + 'Der_wahre_Ursprung_des_Zweiten_Weltkriegs.mp4'; OUT = U + 'pak/Ursprung_Story_DE.mp4'
S = json.load(open(U + 'pak/sents.json')); A1 = (S[1][2] + S[2][1]) / 2
W, H, FPS = 1080, 1920, 30; CARD = 5.0
YEL, WHITE, CREAM, RED, DARK = (244, 199, 15), (245, 245, 240), (232, 226, 210), (196, 38, 40), (14, 15, 18)
F = '/tmp/claude-0/fonts/'
def anton(s): return ImageFont.truetype(F + 'Anton.ttf', s)
def bebas(s): return ImageFont.truetype(F + 'BebasNeue.ttf', s)
def eio(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def text(img, t, t0, s, y, fn, size, col, maxw=900):
    if t < t0: return
    f = fn(size)
    while f.getlength(s) > maxw: size -= 4; f = fn(size)
    u = eio((t - t0) / 0.4); La = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(La).text((540, y + 30 * (1 - u)), s, font=f, fill=col + (int(255 * u),), anchor='mm')
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(La.getchannel('A').point(lambda v: int(v * 0.8))); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (4, 8)); img.alpha_composite(La)
def badge(img, x, y, h=100):
    f = anton(int(h * 0.82)); d = ImageDraw.Draw(img); wc = d.textlength('C', font=f); gap, pad = h * 0.07, h * 0.06; cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'DM', font=f, anchor='lm')
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.06, b[2] + pad, b[3] + h * 0.05), fill=YEL)
    d.text((xd, cy), 'DM', font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.12, b[0] + h * 0.4, b[3] + h * 0.17), fill=RED)
def overlay(t):
    img = Image.new('RGBA', (W, H), (6, 8, 14, int(222 * eio(t / 0.6))))
    text(img, t, 0.4, 'SCHNELL INS PROFIL', 400, anton, 116, YEL)
    text(img, t, 0.6, 'UND ANSEHEN!', 525, anton, 96, WHITE)
    if t > 0.8:
        u = eio((t - 0.8) / 0.35); bob = 8 * math.sin((t - 0.8) * 6); a_, b_ = (250 + bob, 262 + bob * 0.6), (132 + bob, 178 + bob * 0.6)
        d = ImageDraw.Draw(img); ang = math.atan2(b_[1] - a_[1], b_[0] - a_[0]); hd = 50
        d.line((a_, b_), fill=YEL + (int(255 * u),), width=18)
        d.polygon([(b_[0] + 16 * math.cos(ang), b_[1] + 16 * math.sin(ang)), (b_[0] - hd * math.cos(ang - .55), b_[1] - hd * math.sin(ang - .55)), (b_[0] - hd * math.cos(ang + .55), b_[1] - hd * math.sin(ang + .55))], fill=YEL + (int(255 * u),))
    if t > 1.0:
        La = Image.new('RGBA', (W, H), (0, 0, 0, 0)); badge(La, 540 - 92, 760, 100); La.putalpha(La.getchannel('A').point(lambda v: int(v * min(1, (t - 1.0) / 0.4)))); img.alpha_composite(La)
    text(img, t, 1.2, 'NEUE DOKU · 40 MINUTEN', 1010, bebas, 80, YEL)
    text(img, t, 1.5, 'DER WAHRE URSPRUNG', 1180, anton, 120, WHITE)
    text(img, t, 1.65, 'DES 2. WELTKRIEGS', 1310, anton, 120, WHITE)
    s_ = 'ER BEGANN NICHT 1939'; text(img, t, 1.9, s_, 1450, bebas, 96, CREAM)
    if t > 2.3:
        f = bebas(96); x0 = 540 - f.getlength(s_) / 2; x1 = x0 + f.getlength(s_); u = eio((t - 2.3) / 0.35)
        ImageDraw.Draw(img).line((x0, 1500, x0 + (x1 - x0) * u, 1500), fill=RED + (250,), width=8)
    return img
tmp = U + 'pak/story_ov.mov'; n = int(CARD * FPS)
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'qtrle', tmp], stdin=subprocess.PIPE)
for i in range(n): p.stdin.write(overlay(i / FPS).tobytes())
p.stdin.close(); p.wait()
L = A1 + CARD
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-t', f'{L + 0.5:.3f}', '-i', SRC, '-itsoffset', f'{A1:.3f}', '-i', tmp, '-i', U + 'final/music.wav', '-filter_complex',
    f'[0:v]trim=0:{L:.3f},setpts=PTS-STARTPTS,split[s1][s2];[s1]scale=-2:1920,crop=1080:1920,boxblur=30:2,eq=brightness=-0.12[bg];'
    f'[s2]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2[base];[base][1:v]overlay=0:0:eof_action=pass,format=yuv420p[v];'
    f'[0:a]atrim=0:{A1:.3f},afade=t=out:st={A1 - 0.25:.3f}:d=0.25[h];[2:a]atrim={A1:.3f}:{L:.3f},asetpts=PTS-STARTPTS,volume=0.5,adelay={int(A1 * 1000)}:all=1,afade=t=in:st={A1:.3f}:d=0.3,afade=t=out:st={L - 1.6:.3f}:d=1.6[m];'
    '[h][m]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5[a]',
    '-map', '[v]', '-map', '[a]', '-t', f'{L:.3f}', '-r', '30', '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', OUT], check=True)
os.remove(tmp); print('ok', round(L, 2))
