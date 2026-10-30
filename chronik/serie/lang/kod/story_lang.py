# Instagram/Facebook story (9:16) for the long Teil 1: the tank film with the hook (1919: no tank / 1939: war), then a card for the
# series with an empty, framed space where the link sticker goes ("Hier klicken").
import sys, math, subprocess
sys.argv = [sys.argv[0], 'T']
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import lang as V
sys.path.insert(0, V.S + 'teil1/covlib'); import lib9 as L
SW_, SH_, FPS = 1080, 1920, 30; YEL, RED, WHITE, DARK = L.YEL, L.RED, L.WHITE, L.DARK
A = V.wt('Das', 5.5) - 0.03; CARD = 3.2; T = A + CARD   # the voice is cut right where the next sentence begins
def osw(s): return L.oswald(s)
def bg(t, blur=0):
    g = V.clip_at('tanks', 0.2 + t * 0.55); w, h = g.size; cw = h * SW_ / SH_   # the film keeps running behind the card
    im = V.tone(g.resize((SW_, SH_), Image.BICUBIC, box=((w - cw) / 2 + 30, 0, (w + cw) / 2 + 30, h)))
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im, np.float32) * V.vignette(SW_, SH_, 0.6) + V.grain(int(t * FPS), 5)[:SH_ // 2 * 2, :SW_][:SH_, :SW_] if False else np.asarray(im, np.float32) * V.vignette(SW_, SH_, 0.6)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
def text(img, t, t0, s, y, size, col, maxw=940):
    if t < t0: return
    k = V.eio(min(1, (t - t0) / 0.35)); f = osw(size)
    while f.getlength(s) > maxw: size -= 4; f = osw(size)
    La = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(La).text((SW_ / 2, y + (1 - k) * 30), s, font=f, fill=col + (int(255 * k),), anchor='mm')
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, int(220 * k)), (0, 0), La.getchannel('A')); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (4, 8)); img.alpha_composite(La)
def flagbar(img, y, k):
    d = ImageDraw.Draw(img); w = 600 * k
    for i, c in enumerate(((24, 24, 26), (200, 22, 26), (240, 190, 20))): d.rectangle((SW_ / 2 - w / 2, y + i * 12, SW_ / 2 + w / 2, y + (i + 1) * 12), fill=c + (255,))
def frame(t):
    if t < A:
        img = bg(t)
        text(img, t, V.P('Zwanzig') , '1939:', 560, 110, YEL); text(img, t, V.P('Panzer'), 'PANZER ROLLEN', 690, 104, YEL); text(img, t, V.P('Polen'), 'NACH POLEN', 810, 104, YEL)
        text(img, t, V.P('durfte') , '1919:', 1040, 110, WHITE); text(img, t, V.P('keinen'), 'KEIN EINZIGER', 1170, 104, WHITE); text(img, t, V.P('Panzer', 4), 'PANZER ERLAUBT', 1290, 104, WHITE)
        return img.convert('RGB')
    u = t - A; img = bg(t, 8 * V.eio(min(1, u / 0.3)))
    img.alpha_composite(Image.new('RGBA', (SW_, SH_), (6, 7, 9, int(185 * V.eio(min(1, u / 0.3))))))
    if u > 0.05:
        d = ImageDraw.Draw(img); f = osw(64); s = 'NEUE DOKU'; b = d.textbbox((SW_ / 2, 430), s, font=f, anchor='mm'); k = V.eio(min(1, (u - 0.05) / 0.25))
        d.rectangle((b[0] - 26, b[1] - 14, b[2] + 26, b[3] + 14), fill=YEL + (int(255 * k),)); d.text((SW_ / 2, 430), s, font=f, fill=DARK + (int(255 * k),), anchor='mm')
    text(img, u, 0.15, 'DEUTSCHLAND IM', 590, 118, WHITE); text(img, u, 0.25, 'ZWEITEN WELTKRIEG', 720, 118, WHITE)
    if u > 0.35: flagbar(img, 805, V.eio(min(1, (u - 0.35) / 0.3)))
    text(img, u, 0.45, 'TEIL 1 · DER WEG IN DEN KRIEG', 900, 62, YEL)
    text(img, u, 0.6, 'Die ganze Geschichte:', 1080, 64, WHITE); text(img, u, 0.7, 'HIER KLICKEN', 1170, 96, YEL)
    if u > 0.8:   # the empty space for the link sticker, with a pulsing arrow pointing at it
        k = V.eio(min(1, (u - 0.8) / 0.3)); d = ImageDraw.Draw(img); x0, y0, x1, y1 = 190, 1290, 890, 1470
        for i in range(0, 2 * (x1 - x0) + 2 * (y1 - y0), 36):   # dashed frame
            p = i; seg = []
            for q in (p, p + 20):
                if q < x1 - x0: seg.append((x0 + q, y0))
                elif q < (x1 - x0) + (y1 - y0): seg.append((x1, y0 + q - (x1 - x0)))
                elif q < 2 * (x1 - x0) + (y1 - y0): seg.append((x1 - (q - (x1 - x0) - (y1 - y0)), y1))
                else: seg.append((x0, y1 - (q - 2 * (x1 - x0) - (y1 - y0))))
            d.line(seg, fill=WHITE + (int(200 * k),), width=5)
        bob = 10 * math.sin(u * 6); ax = SW_ / 2
        d.polygon([(ax - 34, 1222 + bob), (ax + 34, 1222 + bob), (ax, 1268 + bob)], fill=YEL + (int(255 * k),))
    return img.convert('RGB')
if __name__ == '__main__':
    out = V.LB + 'social/Teil1_Lang_Story.mp4'; import os; os.makedirs(V.LB + 'social', exist_ok=True)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{SW_}x{SH_}', '-r', str(FPS), '-i', '-', '-i', V.LB + 'mix2.wav', '-i', V.LB + 'bed_lev.wav',
                          '-filter_complex', f'[1:a]atrim=0:{A},asetpts=PTS-STARTPTS,afade=t=out:st={A - 0.08}:d=0.08[x];[2:a]atrim=30:{30 + CARD},asetpts=PTS-STARTPTS,volume=0.5,afade=t=in:d=0.4,afade=t=out:st={CARD - 0.6}:d=0.6[y];[x][y]concat=n=2:v=0:a=1[a]',
                          '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for n in range(int(T * FPS)): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait()
    for tt in (2.5, 5.9, A + 0.4, T - 0.3): frame(tt).resize((360, 640)).save(V.LB + 'chk/story_%.1f.jpg' % tt)
    print(out, T)
