# Teil 2, 6 s test: the magazine (Teil 1 look) mixed with style A. Left page: a normal magazine page (kicker, headline,
# a framed colour photo, body text). Right page: a dark style-A "feature page" inside the magazine: colour prints with
# white borders fly in turning and land on a slate-blue page, a big white grunge number with a yellow two-line title.
# The camera glides onto the right page as the prints land, then dives into the tank print until it fills the frame.
import sys, os, math, functools, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from lcore import *
SP_ = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/'
C = SP_ + 't2/c/'
YEL, CREAM, NAVY = (236, 182, 40), (236, 232, 222), (40, 47, 66)
@functools.lru_cache(None)
def mont(s, wg=900):
    f = ImageFont.truetype(SP_ + 'sch/fonts/Montserrat%5Bwght%5D.ttf', s); f.set_variation_by_axes([wg]); return f
@functools.lru_cache(None)
def img(n): return Image.open(C + n + '.jpg').convert('RGB')

# ---------- style A pieces, sized for a magazine page ----------
@functools.lru_cache(None)
def grunge(w, h, seed=1):
    r = np.random.default_rng(seed); n = np.asarray(Image.fromarray((r.random((h // 8 + 1, w // 8 + 1)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    sp = r.random((h, w)); return Image.fromarray((np.clip(1 - np.clip((0.42 - n) * 4, 0, 1) * 0.55 - (sp > 0.985) * 0.6, 0, 1) * 255).astype(np.uint8))
def gtext(s, font, col, a=1.0, track=-4):
    w = int(sum(font.getlength(c) + track for c in s) + 30); asc, de = font.getmetrics(); L = Image.new('RGBA', (w, asc + de + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(L); x = 12
    for c in s: d.text((x, 8), c, font=font, fill=col + (int(255 * a),)); x += font.getlength(c) + track
    L.putalpha(ImageChops.multiply(L.getchannel('A'), grunge(L.width, L.height, len(s)))); return L
@functools.lru_cache(None)
def a_page():
    """slate-blue page: uneven tone, a faint pile of blurred grey prints, soft vignette (the style-A stage, on paper size)"""
    r = np.random.default_rng(3); yy, xx = np.mgrid[0:PH, 0:PW].astype(np.float32)
    n = np.asarray(Image.fromarray((r.random((PH // 40, PW // 40)) * 255).astype(np.uint8)).resize((PW, PH), Image.BICUBIC), np.float32)[..., None] / 255
    base = np.array(NAVY, np.float32)[None, None] * (0.85 + 0.3 * n)
    pg = Image.fromarray(base.clip(0, 255).astype(np.uint8)).convert('RGBA')
    for k, nm in enumerate(['hoffmann_s30_1', 'hoffmann_s49_1', 'hoffmann_s21_0', 'hoffmann_s35_1', 'hoffmann_s47_1', 'hoffmann_s79_0', 'hoffmann_s28_0']):
        g = img(nm).convert('L').resize((520, 360)); P_ = Image.new('RGBA', (560, 400), (210, 210, 205, 255)); P_.paste(g.convert('RGBA'), (20, 20))
        P_ = P_.rotate(r.uniform(-25, 25), expand=True, resample=Image.BICUBIC); pg.alpha_composite(P_, (int(r.uniform(-150, PW - 250)), int(r.uniform(-120, PH - 250))))
    a = np.asarray(pg.convert('RGB').filter(ImageFilter.GaussianBlur(3)), np.float32)
    a = a * 0.28 + np.array(NAVY, np.float32)[None, None] * 0.72 * (0.85 + 0.3 * n)
    vg = np.clip(1 - 0.5 * np.clip(np.sqrt(((xx - PW / 2) / (PW / 2)) ** 2 + ((yy - PH / 2) / (PH / 2)) ** 2) - 0.5, 0, None), 0, 1)[..., None]
    return Image.fromarray((a * vg).clip(0, 255).astype(np.uint8))
@functools.lru_cache(None)
def a_print(nm, wd, seed):
    """colour print with a white deckled border and a soft drop shadow"""
    g = img(nm); h = int(wd * g.height / g.width); g = g.resize((wd, h), Image.LANCZOS); b = max(14, wd // 26)
    P_ = Image.new('RGBA', (wd + 2 * b, h + 2 * b), (244, 241, 233, 255)); P_.paste(g, (b, b))
    r = np.random.default_rng(seed); m = Image.new('L', P_.size, 255); d = ImageDraw.Draw(m)
    for x in range(0, P_.width, 6): d.rectangle((x, 0, x + 6, int(r.uniform(0, 4))), fill=0); d.rectangle((x, P_.height - int(r.uniform(0, 4)), x + 6, P_.height), fill=0)
    P_.putalpha(m); return P_
def card(pg, P_, cx, cy, rot, sc=1.0, blur=0.0):
    Q = P_.resize((int(P_.width * sc), int(P_.height * sc)), Image.BICUBIC) if abs(sc - 1) > 1e-3 else P_
    Q = Q.rotate(rot, expand=True, resample=Image.BICUBIC)
    if blur > 0.5: Q = Q.filter(ImageFilter.GaussianBlur(blur))
    sh = Image.new('RGBA', Q.size, (0, 0, 0, 0)); sh.putalpha(Q.getchannel('A').point(lambda v: int(v * 0.55)))
    pg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (int(cx - Q.width / 2 + 10), int(cy - Q.height / 2 + 18)))
    pg.alpha_composite(Q, (int(cx - Q.width / 2), int(cy - Q.height / 2)))
def throw(pg, t, t0, P_, to, r1, frm=(1, -1)):
    """a print flies in from off the page, turning, big and blurred, and settles (style A)"""
    if t < t0: return
    u = eout((t - t0) / 0.9); x = lerp(to[0] + frm[0] * 1500, to[0], u); y = lerp(to[1] + frm[1] * 900, to[1], u)
    card(pg, P_, x, y, lerp(r1 + 28 * frm[0], r1, u), lerp(1.35, 1.0, u) - 0.01 * max(0, t - t0 - 0.9), (1 - u) * 10)
def title(pg, t, t0, big, small, cx, cy, size=330, ssize=120):
    if t < t0: return
    fb, fs = mont(size), mont(ssize); k = eout((t - t0) / 0.35)
    B_ = gtext(big, fb, CREAM, k, -10); Ls = [gtext(s, fs, YEL, clamp((t - t0 - 0.25 - 0.15 * i) / 0.3), -4) for i, s in enumerate(small)]
    wsm = max(L.width for L in Ls); x0 = cx - (B_.width + 10 + wsm) / 2
    pg.alpha_composite(B_, (int(x0), int(cy - B_.height / 2)))
    for i, L in enumerate(Ls): pg.alpha_composite(L, (int(x0 + B_.width + 10), int(cy - len(Ls) * ssize * 0.48 + i * ssize * 0.96)))

# ---------- the two pages ----------
FRAME_L = (110, 560, 1180, 760)
TANK = (700, 1000)   # where the tank print lands on the right page (page coords)
def left(t):
    pg = M.gloss(21).copy(); runhead(pg, True, 21)
    d = ImageDraw.Draw(pg); d.text((x0 := 110, 200), '1. SEPTEMBER 1939', font=sans(40, 800), fill=ACC)
    label(pg, t, 0.0, 'Der Überfall', (110, 260), serif(118, 800)); label(pg, t, 0.15, 'auf Polen', (110, 398), serif(118, 400))
    g = img('hoffmann_s09_0'); x0_, y0_, bw, bh = FRAME_L; sc = max(bw / g.width, bh / g.height); cw, ch = bw / sc, bh / sc
    pg.paste(g.resize((bw, bh), Image.LANCZOS, box=((g.width - cw) / 2, (g.height - ch) / 2, (g.width + cw) / 2, (g.height + ch) / 2)), (x0_, y0_))
    d.line((110, 1350, 260, 1350), fill=ACC, width=5); d.text((110, 1368), 'Grenzstein an der deutsch-polnischen Grenze, 1939', font=italic(32), fill=GREY)
    for i, s in enumerate(('Am Morgen des 1. September 1939 standen an der', 'polnischen Grenze rund anderthalb Millionen', 'deutsche Soldaten.')):
        label(pg, t, 0.3 + 0.25 * i, s, (110, 1450 + i * 72), serif(50, 400))
    return pg
def right(t):
    pg = a_page().copy().convert('RGBA')
    throw(pg, t, 0.9, a_print('hoffmann_s36_0', 760, 2), (480, 520), -6, (1, -1))
    throw(pg, t, 1.25, a_print('hoffmann_s23_0', 520, 3), (1040, 600), 7, (1, -1))
    throw(pg, t, 1.6, a_print('hoffmann_s39_0', 900, 4), TANK, -2, (1, 1))
    title(pg, t, 2.3, '1,5', ['MILLIONEN', 'SOLDATEN'], PW / 2, 1530)
    return pg.convert('RGB')
OV = (PW, 905, 0.60)
def fill_r(x, y, wd, f=1.05): return (PW + x, y, f * W / wd)
CAMS = [(0.0, PW, 905, 0.56), (0.9, PW + 700, 905, 0.60, 1.1), (4.0, PW + TANK[0], TANK[1], 2.05, 1.3)]
BOOK = Book([(left, right)], [], CAMS, spine=100)
def frame(t): return BOOK(t)
if __name__ == '__main__':
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[2:]]; Pc = Image.new('RGB', (3 * 640, ((len(ts) + 2) // 3) * 360))
        for i, t in enumerate(ts): Pc.paste(frame(t).resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
        Pc.save(LB + 'chk/mix.jpg', quality=88); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
