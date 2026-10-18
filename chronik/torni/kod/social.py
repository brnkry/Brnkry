# Törni: 3 thumbnails (A/B/C), Instagram/Facebook story image + story video frames, reel overlays and end card
import sys, subprocess
from lib import *
from lib import _bg
OUT = B + 'social/'; import os; os.makedirs(OUT, exist_ok=True)

def badge(can, x, y, h=100):
    f = anton(int(h * 0.82)); d = ImageDraw.Draw(can); wc = d.textlength('C', font=f); gap, pad = h * 0.07, h * 0.06; cy = y + h * 0.48; xd = x + wc + gap + pad
    b = d.textbbox((xd, cy), 'DM', font=f, anchor='lm')
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x - h * 0.22, y - h * 0.16, b[2] + pad + h * 0.22, y + h * 1.12), h * 0.12, fill=(8, 9, 11, 170))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(can)
    d.text((x, cy), 'C', font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.06, b[2] + pad, b[3] + h * 0.05), fill=YEL)
    d.text((xd, cy), 'DM', font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.12, b[0] + h * 0.42, b[3] + h * 0.16), fill=RED)
def shadowed(can, fn, blur=14, off=(5, 9), a=230):
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L))
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, a), (0, 0), L.getchannel('A'))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), off); can.alpha_composite(L)
def T(can, xy, s, font, col=WHITE, anchor='mm'):
    shadowed(can, lambda d: d.text(xy, s, font=font, fill=col + (255,), anchor=anchor))
def arrow(can, a, b, u, col=YEL, w=16, head=46):
    d = ImageDraw.Draw(can); e = (lerp(a[0], b[0], u), lerp(a[1], b[1], u)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
    d.line((a, e), fill=(0, 0, 0, 150), width=w + 8); d.line((a, e), fill=col, width=w)
    d.polygon([(e[0] + 14 * math.cos(ang), e[1] + 14 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))], fill=col)
def plate(can, xy, s, font, bg=YEL, fg=DARK, pad=(28, 12), rule=True):
    d = ImageDraw.Draw(can); b = d.textbbox(xy, s, font=font, anchor='mm')
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((b[0] - pad[0] + 8, b[1] - pad[1] + 10, b[2] + pad[0] + 8, b[3] + pad[1] + 10), fill=(0, 0, 0, 190)); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(can); d.rectangle((b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1]), fill=bg); d.text(xy, s, font=font, fill=fg, anchor='mm')
    if rule: d.rectangle((b[0] - pad[0], b[3] + pad[1] + 14, b[0] - pad[0] + (b[3] - b[1]) * 1.3, b[3] + pad[1] + 24), fill=RED)
def column(n, w, h, cy=0.42, z=1.0):
    im = src(n); cw = min(im.width, im.height * w / h) / z; ch = cw * h / w; c = min(max(im.height * cy, ch / 2), im.height - ch / 2)
    return im.resize((w, h), Image.LANCZOS, box=(im.width / 2 - cw / 2, c - ch / 2, im.width / 2 + cw / 2, c + ch / 2)).convert('RGBA')
def grad(can, a=230, start=0.45):
    hh = can.height; g = (np.clip((np.arange(hh) - hh * start) / (hh * (1 - start)), 0, 1) ** 1.3 * a).astype(np.uint8)
    L = Image.new('RGBA', can.size, (6, 7, 9, 0)); L.putalpha(Image.fromarray(np.repeat(g[:, None], can.width, 1))); can.alpha_composite(L)
def ytlogo(can, cx, cy, s):
    d = ImageDraw.Draw(can); d.rounded_rectangle((cx - s, cy - s * 0.7, cx + s, cy + s * 0.7), s * 0.32, fill=(255, 0, 0))
    d.polygon([(cx - s * 0.3, cy - s * 0.38), (cx - s * 0.3, cy + s * 0.38), (cx + s * 0.42, cy)], fill=WHITE)

# ---------- thumbnails ----------
def thumb_a():   # three uniforms, one man
    can = Image.new('RGBA', (W, H), DARK + (255,)); pw = W // 3
    for i, n in enumerate(['t06', 't22', 't18']):
        can.alpha_composite(column(n, pw, H, 0.40, 1.08), (i * pw, 0))
        if i: ImageDraw.Draw(can).line((i * pw, 0, i * pw, H), fill=YEL, width=10)
    grad(can, 235, 0.42); badge(can, W / 2 - 75, 36, 92)
    for i, lab in enumerate(['FINNLAND', 'WAFFEN-SS', 'USA']): plate(can, (i * pw + pw / 2, 640), lab, anton(66), YEL if i != 1 else WHITE, DARK, rule=False)
    T(can, (W / 2, 800), '3 UNIFORMEN, 1 MANN', anton(150))
    T(can, (W / 2, 965), 'LAURI TÖRNI', anton(130), YEL)
    can.convert('RGB').save(OUT + 'Thumbnail_A_Drei_Uniformen.jpg', quality=93)
def thumb_b():   # two names
    can = Image.new('RGBA', (W, H), DARK + (255,))
    L = column('t09', 1000, H, 0.38, 1.0); R = column('t18', 1000, H, 0.38, 1.05)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(0, 0), (1010, 0), (900, H), (0, H)], fill=255)
    can.paste(R, (W - 1000, 0)); can.paste(L, (-40, 0), m.crop((40, 0, 1040, H)))
    Lr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(Lr).line([(960, -10), (850, H + 10)], fill=YEL + (255,), width=14); can.alpha_composite(Lr)
    grad(can, 240, 0.40); badge(can, 70, 40, 92)
    T(can, (480, 780), 'LAURI TÖRNI', anton(120)); T(can, (1450, 780), 'LARRY THORNE', anton(120), YEL)
    arrow(can, (760, 900), (1180, 900), 1.0, YEL, 18, 54)
    plate(can, (W / 2, 990), 'DERSELBE MANN', anton(84), RED, WHITE, rule=False)
    can.convert('RGB').save(OUT + 'Thumbnail_B_Zwei_Namen.jpg', quality=93)
def thumb_c():   # missing in Vietnam
    can = shade(dim(pan('t16', 0, 0, 1, 1, 0.55, 1.0), 70), 235, 0.35)
    P = column('t18', 760, H, 0.36, 1.0); m = Image.new('L', P.size, 255); dm = ImageDraw.Draw(m)
    for i in range(110): dm.line((i, 0, i, H), fill=int(255 * i / 110))
    can.paste(P, (W - 760, 0), m); grad(can, 200, 0.6); badge(can, 70, 40, 92)
    ImageDraw.Draw(can).ellipse((1524 - 300, 420 - 300, 1524 + 300, 420 + 300), outline=RED, width=10)
    T(can, (560, 360), 'VERSCHOLLEN', anton(170), WHITE)
    plate(can, (560, 560), 'VIETNAM 1965', anton(110), YEL, DARK)
    T(can, (560, 790), '34 JAHRE SPÄTER', anton(110), WHITE)
    T(can, (560, 945), 'GEFUNDEN', anton(110), YEL)
    can.convert('RGB').save(OUT + 'Thumbnail_C_Verschollen.jpg', quality=93)

# ---------- story image (1080x1920) ----------
SW, SH = 1080, 1920
def story_bg(n, cy=0.4, z=1.0):
    can = column(n, SW, SH, cy, z); grad(can, 240, 0.35)
    top = Image.new('RGBA', (SW, SH), (0, 0, 0, 0)); g = (np.clip((420 - np.arange(SH)) / 420, 0, 1) * 170).astype(np.uint8); top.putalpha(Image.fromarray(np.repeat(g[:, None], SW, 1))); can.alpha_composite(top)
    return can
def story_text(can, k=1.0):
    badge(can, SW / 2 - 70, 300, 84)
    plate(can, (SW / 2, 1010), 'NEUE DOKUMENTATION', anton(64), RED, WHITE, rule=False)
    T(can, (SW / 2, 1150), 'LAURI TÖRNI', anton(140), YEL)
    T(can, (SW / 2, 1275), 'DREI UNIFORMEN, ZWEI NAMEN', bebas(70), WHITE)
def story_cta(can, y=1450):
    ytlogo(can, SW / 2 - 230, y, 62); T(can, (SW / 2 + 70, y + 4), 'JETZT AUF YOUTUBE', anton(66), WHITE)
    T(can, (SW / 2, y + 150), 'LINK ANTIPPEN', bebas(70), YEL)
    arrow(can, (SW / 2, y + 210), (SW / 2, y + 330), 1.0, YEL, 14, 44)
def story_image():
    can = story_bg('t09', 0.36); story_text(can); story_cta(can)
    can.convert('RGB').save(OUT + 'Story_Bild.jpg', quality=93)

# ---------- story video frames (12 s) ----------
SEQ = [('t06', 0.0, 'FINNLAND'), ('t22', 1.6, 'WAFFEN-SS'), ('t18', 3.2, 'US ARMY')]
def story_frame(t):
    can = Image.new('RGBA', (SW, SH), DARK + (255,))
    if t < 5.0:
        for i, (n, t0, lab) in enumerate(SEQ):
            if t < t0: break
            k = eout((t - t0) / 0.5); ph = column(n, SW, SH, 0.40, lerp(1.0, 1.06, clamp((t - t0) / 3)))
            if k < 1: ph.putalpha(int(255 * k))
            can.alpha_composite(ph)
        grad(can, 230, 0.5); idx = max(i for i, (_, t0, _) in enumerate(SEQ) if t >= t0)
        T(can, (SW / 2, 1450), SEQ[idx][2], anton(120), YEL if idx != 1 else WHITE)
        T(can, (SW / 2, 380), 'DREI UNIFORMEN', anton(110), WHITE)
        T(can, (SW / 2, 500), 'EIN MANN', anton(110), YEL)
    else:
        k = eio((t - 5.0) / 0.8); bg = story_bg('t09', 0.36, lerp(1.08, 1.0, k))
        bg = bg.filter(ImageFilter.GaussianBlur(10 * (1 - k))) if k < 1 else bg
        can.alpha_composite(bg); can.alpha_composite(Image.new('RGBA', (SW, SH), (0, 0, 0, int(255 * (1 - k)))))
        if t > 5.6: story_text(can)
        if t > 6.6:
            kk = eout((t - 6.6) / 0.4); L = Image.new('RGBA', (SW, SH), (0, 0, 0, 0)); story_cta(L, 1450 + int(math.sin(t * 5) * 6))
            if kk < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * kk)))
            can.alpha_composite(L)
    if t > 11.5: can.alpha_composite(Image.new('RGBA', (SW, SH), (0, 0, 0, int(255 * clamp((t - 11.5) / 0.5)))))
    return can.convert('RGB')

# ---------- reel overlay (static PNG over the 16:9 video) and end card ----------
def reel_overlay():
    L = Image.new('RGBA', (SW, SH), (0, 0, 0, 0)); badge(L, SW / 2 - 70, 230, 84)
    T(L, (SW / 2, 470), 'DREI UNIFORMEN.', anton(96), WHITE); T(L, (SW / 2, 580), 'EIN MANN.', anton(96), YEL)
    T(L, (SW / 2, 1420), 'GANZE DOKU AUF YOUTUBE', anton(70), WHITE); T(L, (SW / 2, 1510), 'LINK IN BIO', bebas(70), YEL)
    L.save(OUT + 'reel_overlay.png')
def reel_end(t):
    can = story_bg('t09', 0.36, lerp(1.05, 1.0, clamp(t / 4))); story_text(can)
    ytlogo(can, SW / 2 - 230, 1450, 62); T(can, (SW / 2 + 70, 1454), 'GANZE DOKU AUF YOUTUBE', anton(56), WHITE)
    T(can, (SW / 2, 1600), 'LINK IN BIO', anton(90), YEL)
    if t > 3.5: can.alpha_composite(Image.new('RGBA', (SW, SH), (0, 0, 0, int(255 * clamp((t - 3.5) / 0.5)))))
    return can.convert('RGB')
def render(fn, dur, out):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{SW}x{SH}', '-r', '30', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
    for n in range(int(dur * 30)): p.stdin.write(np.asarray(fn(n / 30)).tobytes())
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'stills': thumb_a(); thumb_b(); thumb_c(); story_image(); reel_overlay(); print('stills ok')
    if what == 'story': render(story_frame, 12.0, OUT + 'story_v.mp4'); print('story ok')
    if what == 'end': render(reel_end, 4.0, OUT + 'reel_end_v.mp4'); print('end ok')
