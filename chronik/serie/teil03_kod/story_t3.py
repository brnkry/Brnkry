# Teil 3 stories (9:16): (1) video story: tank film with the hook (more tanks than the Wehrmacht, six weeks later an armistice), then a card "Jetzt auf YouTube, Link in Bio";
# (2) still story with a framed empty space for the link sticker.
import sys, os, math, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(HERE) + '/'; SP = os.path.dirname(B.rstrip('/')) + '/'
sys.path.insert(0, SP + 'teil1/covlib'); import lib9 as L
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
SW_, SH_, FPS = 1080, 1920, 30; YEL, RED, WHITE, DARK = L.YEL, L.RED, L.WHITE, L.DARK
W_ = json.load(open(B + 'words.json')); OFF = 1.0
def wt(i): return W_[i][1] + OFF
A = W_[28][2] + OFF + 0.45; CARD = 3.6; T = A + CARD
def osw(s): return L.oswald(s)
def eio(u): u = max(0, min(1, u)); return u * u * (3 - 2 * u)
VIG = None
def vign():
    global VIG
    if VIG is None:
        yy, xx = np.mgrid[0:SH_, 0:SW_].astype(np.float32); r = np.hypot((xx - SW_ / 2) / (SW_ * 0.75), (yy - SH_ / 2) / (SH_ * 0.62)); VIG = np.clip(1.08 - 0.55 * r ** 2, 0.25, 1)[..., None]
    return VIG
def film(t):
    if t < 7.6: name, n = 'tanks', int(t * FPS) % 290 + 1; dx = 0
    else: name, n = 'column', int((t - 7.6) * FPS + 40) % 440 + 1; dx = 0
    g = Image.open(B + 'clips/%s/f%04d.jpg' % (name, n)).convert('RGB'); w, h = g.size; z = 1 + 0.01 * t; cw = h * SW_ / SH_ / z; ch = h / z
    im = g.resize((SW_, SH_), Image.BICUBIC, box=((w - cw) / 2 + dx, (h - ch) / 2, (w + cw) / 2 + dx, (h + ch) / 2))
    im = Image.blend(im, Image.new('RGB', im.size, (92, 70, 40)), 0.08)
    return Image.fromarray((np.asarray(im, np.float32) * vign()).clip(0, 255).astype(np.uint8)).convert('RGBA')
def text(img, t, t0, s, y, size, col, maxw=960):
    if t < t0: return None
    k = eio((t - t0) / 0.35); f = osw(size)
    while f.getlength(s) > maxw: size -= 4; f = osw(size)
    La = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(La).text((SW_ / 2, y + (1 - k) * 30), s, font=f, fill=col + (int(255 * k),), anchor='mm')
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, int(220 * k)), (0, 0), La.getchannel('A')); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (4, 8)); img.alpha_composite(La)
    return ImageDraw.Draw(img).textbbox((SW_ / 2, y), s, font=f, anchor='mm')
def flagbar(img, y, k):
    d = ImageDraw.Draw(img); w = 600 * k
    for i, c in enumerate(((24, 24, 26), (200, 22, 26), (240, 190, 20))): d.rectangle((SW_ / 2 - w / 2, y + i * 12, SW_ / 2 + w / 2, y + (i + 1) * 12), fill=c + (255,))
def badge(img, s, y, k):
    d = ImageDraw.Draw(img); f = osw(62); b = d.textbbox((SW_ / 2, y), s, font=f, anchor='mm')
    d.rectangle((b[0] - 26, b[1] - 14, b[2] + 26, b[3] + 14), fill=YEL + (int(255 * k),)); d.text((SW_ / 2, y), s, font=f, fill=DARK + (int(255 * k),), anchor='mm')
def series(img, u, y0=560):
    text(img, u, 0.15, 'DEUTSCHLAND IM', y0, 118, WHITE); text(img, u, 0.25, 'ZWEITEN WELTKRIEG', y0 + 130, 118, WHITE)
    if u > 0.35: flagbar(img, y0 + 215, eio((u - 0.35) / 0.3))
    text(img, u, 0.45, 'TEIL 3 · DER KRIEG IM WESTEN', y0 + 310, 60, YEL)
def frame(t):
    if t < A:
        img = film(t)
        text(img, t, wt(4), 'FRANKREICH HATTE', 600, 100, WHITE); text(img, t, wt(5), 'MEHR PANZER', 730, 150, YEL)
        text(img, t, wt(21), 'SECHS WOCHEN SPÄTER:', 1080, 84, WHITE); text(img, t, wt(27), 'WAFFENSTILLSTAND', 1190, 104, YEL)
        return img.convert('RGB')
    u = t - A; img = film(t).filter(ImageFilter.GaussianBlur(8 * eio(u / 0.3)))
    img.alpha_composite(Image.new('RGBA', (SW_, SH_), (6, 7, 9, int(190 * eio(u / 0.3)))))
    if u > 0.05: badge(img, 'NEUE DOKU · 10 MINUTEN', 420, eio((u - 0.05) / 0.25))
    series(img, u)
    text(img, u, 0.7, 'JETZT AUF YOUTUBE', 1110, 96, WHITE); text(img, u, 0.85, 'LINK IN BIO', 1230, 120, YEL)
    if u > 1.0:   # an arrow up to the profile name
        k = eio((u - 1.0) / 0.3); d = ImageDraw.Draw(img); bob = 12 * math.sin(u * 6); ax, ay = SW_ / 2, 250 + bob
        d.polygon([(ax, ay - 60), (ax - 56, ay), (ax + 56, ay)], fill=YEL + (int(255 * k),)); d.rectangle((ax - 18, ay, ax + 18, ay + 90), fill=YEL + (int(255 * k),))
    return img.convert('RGB')
def still():
    g = Image.open(B + 'img/paris_parade.jpg').convert('RGB'); w, h = g.size; cw = h * SW_ / SH_
    im = ImageEnhance.Contrast(g.resize((SW_, SH_), Image.LANCZOS, box=(w * 0.72 - cw / 2, 0, w * 0.72 + cw / 2, h))).enhance(1.06)
    im = Image.fromarray((np.asarray(im, np.float32) * vign()).clip(0, 255).astype(np.uint8)).convert('RGBA')
    sh = np.clip((np.arange(SH_) - 200) / 900, 0, 1)[:, None] * 0 + 0.42; Lg = Image.new('RGBA', im.size, (6, 7, 9, 0)); Lg.putalpha(Image.fromarray((np.repeat(sh, SW_, 1) * 255).astype(np.uint8))); im.alpha_composite(Lg)
    badge(im, 'NEUE DOKU · 10 MINUTEN', 300, 1)
    text(im, 9, 0, 'FRANKREICH FIEL IN', 470, 100, WHITE); b = text(im, 9, 0, '6 WOCHEN', 620, 160, YEL)
    series(im, 9, 840)
    text(im, 9, 0, 'Jetzt ansehen:', 1330, 70, WHITE); text(im, 9, 0, 'HIER KLICKEN', 1430, 104, YEL)
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = 190, 1560, 890, 1740   # dashed frame for the link sticker
    per = 2 * (x1 - x0) + 2 * (y1 - y0)
    def pt(q):
        q %= per
        if q < x1 - x0: return (x0 + q, y0)
        q -= x1 - x0
        if q < y1 - y0: return (x1, y0 + q)
        q -= y1 - y0
        if q < x1 - x0: return (x1 - q, y1)
        return (x0, y1 - (q - (x1 - x0)))
    for i in range(0, per, 36): d.line([pt(i), pt(i + 20)], fill=WHITE + (210,), width=5)
    ax = SW_ / 2; d.polygon([(ax - 34, 1492), (ax + 34, 1492), (ax, 1538)], fill=YEL)
    os.makedirs(B + 'social', exist_ok=True); im.convert('RGB').save(B + 'social/Teil3_Story_Bild.jpg', quality=93)
if __name__ == '__main__':
    still()
    out = B + 'social/Teil3_Story_Video.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{SW_}x{SH_}', '-r', str(FPS), '-i', '-', '-i', B + 'mix3.wav', '-stream_loop', '-1', '-i', B + 'el/bed2.mp3',
                          '-filter_complex', f'[1:a]atrim=0:{A},asetpts=PTS-STARTPTS,afade=t=out:st={A - 0.1}:d=0.1[x];[2:a]atrim=20:{20 + CARD},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=0.35,afade=t=in:d=0.4,afade=t=out:st={CARD - 0.7}:d=0.7[y];[x][y]concat=n=2:v=0:a=1[a]',
                          '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for n in range(int(T * FPS)): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait()
    C = Image.new('RGB', (360 * 5, 640))
    for i, tt in enumerate((4.5, 8.0, 12.5, T - 0.3)): C.paste(frame(tt).resize((360, 640)), (i * 360, 0))
    C.paste(Image.open(B + 'social/Teil3_Story_Bild.jpg').resize((360, 640)), (4 * 360, 0)); C.save(B + 'chk/story.jpg', quality=86); print(out, T)
