# Bölter sample (first 24 s) in the motion language of the reference: transparent cut-outs placed on the paper,
# text partly behind the subject, a grey panel the subject rises out of before the camera dives in, a narrow strip
# that opens into a taped card, a full-frame blur between scenes, a wipe-up photo montage with white type on top.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edlib import *
T_END = WD[52][2] + OFF + 1.2
def lerp(a, b, u): return a + (b - a) * u

def place(can, img, box, k=1.0, blur=0.0, shadow_a=0.55):
    """a cut-out (RGBA) fitted into box = (x, y, w, h), soft drop shadow, optional blur"""
    x, y, bw, bh = [int(v) for v in box]; im = img
    sc = min(bw / im.width, bh / im.height); w, h = max(1, int(im.width * sc)), max(1, int(im.height * sc))
    g = im.resize((w, h), Image.LANCZOS).convert('LA').convert('RGBA'); a = g.getchannel('A')
    ox, oy = x + (bw - w) // 2, y + bh - h
    if shadow_a > 0:
        sh = Image.new('RGBA', (w, h), (0, 0, 0, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(24)).point(lambda v: int(v * shadow_a * k))); can.alpha_composite(sh, (ox + 16, oy + 22))
    if blur > 0.3: g = g.filter(ImageFilter.GaussianBlur(blur))
    if k < 1: g.putalpha(g.getchannel('A').point(lambda v: int(v * k)))
    can.alpha_composite(g, (ox, oy)); return (ox, oy, ox + w, oy + h)
def panel(can, box, k=1.0, blur=0.0):
    x, y, bw, bh = [int(v) for v in box]
    g = np.linspace(118, 70, bh)[:, None].repeat(bw, 1); P = Image.fromarray(g.astype(np.uint8)).convert('RGB').convert('RGBA'); P.putalpha(int(255 * k))
    if blur > 0.3: P = P.filter(ImageFilter.GaussianBlur(blur))
    can.alpha_composite(P, (x, y))
def bounce_word(can, t, ta, s, kind, size, x, y, col=DARK):
    """letters drop in one after another with a small overshoot"""
    f = font(kind, size); cx = x
    for i, ch in enumerate(s):
        ti = ta + 0.035 * i
        w = f.getlength(ch)
        if t >= ti:
            u = t - ti; dy = -60 * math.exp(-9 * u) * math.cos(14 * u); k = clamp(u / 0.1)
            im = word_img(ch, kind, size, col); im2 = im.copy(); im2.putalpha(im2.getchannel('A').point(lambda v: int(v * k)))
            can.alpha_composite(im2, (int(cx), int(y + dy)))
        cx += w
    return (x, y, cx, y + size * 1.2)
def slide_line(can, t, ta, words, x, y, dist=260):
    """a line of big words that slides in from the right (the reference's 'He was')"""
    u = eout((t - ta) / 0.35); L = Line(int(x + dist * (1 - u)), y, words); return L.draw(can, t)
def wipe_montage(can, t, t0, items, box, step):
    """photos wipe up into a taped frame one after another"""
    x, y, bw, bh = box; n = int((t - t0) / step); u = (t - t0 - n * step) / 0.22
    cur = items[min(n, len(items) - 1)]; prv = items[min(max(n - 1, 0), len(items) - 1)]
    sh = shadow(bw, bh); shl = Image.new('RGBA', sh.size, (0, 0, 0, 0)); shl.putalpha(sh); can.alpha_composite(shl, (x - 62, y - 42))
    pa = grade(fit(load(prv).convert('RGB'), bw, bh)); pb = grade(fit(load(cur).convert('RGB'), bw, bh))
    can.paste(pa, (x, y))
    if n > 0 and u < 1:
        hh = int(bh * eout(u)); can.paste(pb.crop((0, 0, bw, hh)), (x, y + bh - hh))
    else: can.paste(pb, (x, y))
    tape(can, x + 40, y + 6, 38); tape(can, x + bw - 40, y + 6, -38)

S = []
def scene(t0, t1, wm=None):
    def deco(f): S.append((t0, t1, wm, f)); return f
    return deco
T1 = K('und 15 davon') - 0.12; T2 = K('Siebenmal wurde') - 0.12; T3 = K('Sein Name war') - 0.12; T4 = K('Er wurde 1915') - 0.12; T5 = K('Schon 1941') - 0.12; T6 = K('Später kam er') - 0.12

@scene(0.0, T1, 'TIGER')
def c1(c, t):
    z = 1 + 0.05 * clamp(t / T1)
    panel(c, (70, 1010, 640, 600), eout(t / 0.3))
    Line(80, 330, [('Zwei Tiger', 'b', 74, K('Zwei Tiger'), {'box': 1})]).draw(c, t)
    Line(80, 440, [('gegen', 'l', 74, K('gegen 22'))]).draw(c, t)
    bounce_word(c, t, K('gegen 22', 1), '22', 'h', 400, 330, 360)
    tk = load('tabandon_cut.png').crop(load('tabandon_cut.png').getbbox())
    place(c, tk, (int(60 - 120 * z), int(980 - 60 * z), int(1400 * z), int(760 * z)))
    Line(80, 820, [('sowjetische', 'b', 66, K('sowjetische Panzer, und')), ('Panzer', 'h', 96, K('Panzer, und 15'))]).draw(c, t)
@scene(T1, T2, '15')
def c2(c, t):
    pu = eout((t - T1) / 0.35); s_ = lerp(1.15, 1.0, pu); bw, bh = int(900 * s_), int(620 * s_); x0, y0 = 90 + (900 - bw) // 2, 1090 + (620 - bh) // 2
    ph = grade(fit(load('tprint.jpg'), bw, bh, 0.5, 0.35)).convert('RGBA')
    if pu < 1: ph = ph.filter(ImageFilter.GaussianBlur(14 * (1 - pu)))
    shl = Image.new('RGBA', shadow(bw, bh).size, (0, 0, 0, 0)); shl.putalpha(shadow(bw, bh)); c.alpha_composite(shl, (x0 - 62, y0 - 42)); c.alpha_composite(ph, (x0, y0))
    b = slide_line(c, t, K('und 15 davon', 1), [('15', 'o', 400, K('und 15 davon', 1), {'id': 'n'})], 80, 330)
    slide_line(c, t, K('davon schoss'), [('davon', 'l', 76, K('davon schoss'))], 560, 520)
    slide_line(c, t, K('schoss er selbst'), [('schoss er', 'b', 80, K('schoss er selbst'))], 80, 790)
    slide_line(c, t, K('er selbst ab.', 1), [('selbst ab.', 'h', 130, K('er selbst ab.', 1))], 80, 870)
@scene(T2, T3, '7×')
def c3(c, t):
    a = load('a_cut.png'); a = a.crop(a.getbbox())
    ty = K('Krieg verwundet,', 1)                       # the camera dives into the panel here
    u = eout((t - ty) / 0.5)
    pb = (lerp(220, -200, u), lerp(860, 600, u), lerp(640, 1480, u), lerp(700, 1500, u))
    if u < 1: panel(c, pb, eout((t - T2) / 0.2) * (1 - u), blur=14 * (1 - clamp((t - T2) / 0.2)))
    rise = eout((t - T2 - 0.15) / 0.45); bx = (lerp(260, -40, u), lerp(900 + 620 * (1 - rise), 640, u), lerp(560, 1160, u), lerp(660, 1300, u))
    if t > T2 + 0.15:
        # clip the rising portrait to the panel until the dive
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); place(L, a, bx, shadow_a=0.4)
        if u < 0.05:
            m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((pb[0], pb[1], pb[0] + pb[2], pb[1] + pb[3]), fill=255); L.putalpha(ImageChops.multiply(L.getchannel('A'), m))
        c.alpha_composite(L)
    bounce_word(c, t, K('Siebenmal wurde'), 'Siebenmal', 'h', 190, 80, 300)
    b = Line(80, 560, [('wurde er im Krieg', 'l', 62, K('wurde er im Krieg')), ('verwundet', 'b', 76, K('Krieg verwundet,', 1), {'id': 'v'})]).draw(c, t)
    if 'v' in b: pen_ellipse(c, t, K('Krieg verwundet,', 1) + 0.15, b['v'])
    Line(1000, 1560, [('trotzdem', 'l', 66, K('und trotzdem'), {'col': LITE})], anchor='r').draw(c, t)
    Line(1000, 1650, [('überlebte er.', 'h', 140, K('trotzdem überlebte', 1), {'col': LITE})], anchor='r').draw(c, t)
@scene(T3, T4, 'BÖLTER')
def c4(c, t):
    Line(90, 640, [('Sein Name war', 'l', 76, K('Sein Name war'))]).draw(c, t)
    typewriter(c, t, K('war Johannes Bölter', 1), K('war Johannes Bölter', 1) + 0.7, 'Johannes Bölter', 80, 860, 'b', 132)
@scene(T4, T5, '1915')
def c5(c, t):
    u = eout((t - T4) / 0.35); x0, y0, bw, bh = 200, 820, 680, 860
    cw = int(lerp(90, bw, u)); cx = x0 + (bw - cw) // 2
    card_bg = Image.new('RGBA', (cw, bh), (214, 214, 212, 255))
    if u < 1: card_bg = card_bg.filter(ImageFilter.GaussianBlur(10 * (1 - u)))
    shl = Image.new('RGBA', shadow(cw, bh).size, (0, 0, 0, 0)); shl.putalpha(shadow(cw, bh)); c.alpha_composite(shl, (cx - 62, y0 - 42))
    c.alpha_composite(card_bg, (cx, y0))
    if u > 0.85:
        tape(c, x0 + 40, y0 + 6, 38); tape(c, x0 + bw - 40, y0 + 6, -38)
        bimg = load('b_cut.png'); bimg = bimg.crop(bimg.getbbox()); k = eout((t - T4 - 0.3) / 0.25)
        place(c, bimg, (x0 - 60, y0 + 40 + int(40 * (1 - k)), bw + 120, bh - 40), k=k)
    Line(80, 330, [('Er wurde', 'l', 70, K('Er wurde 1915'))]).draw(c, t)
    bounce_word(c, t, K('Er wurde 1915', 2), '1915', 'h', 300, 80, 410)
    Line(1000, 600, [('geboren.', 'b', 76, K('1915 geboren.', 1))], anchor='r').draw(c, t)
MONT = ['m660.jpg', 'm676.jpg', 'm648.jpg', 'm672.jpg', 'm594.jpg', 'm676.jpg', 'm660.jpg', 'm648.jpg']
@scene(T5, T6, '1941')
def c6(c, t):
    box = (60, 420, 960, 1180)
    if t < T5 + 0.3:
        u = eout((t - T5) / 0.3); slab = Image.new('RGBA', (box[2], box[3]), (112, 112, 114, int(255 * u))).filter(ImageFilter.GaussianBlur(16 * (1 - u))); c.alpha_composite(slab, (box[0], box[1]))
    else: wipe_montage(c, t, T5 + 0.3, MONT, box, 0.55)
    Line(120, 1080, [('Schon', 'l', 70, K('Schon 1941'), {'col': LITE}), ('1941', 'h', 160, K('Schon 1941', 1), {'col': LITE})]).draw(c, t)
    Line(120, 1290, [('Ostfront', 'b', 82, K('der Ostfront vor', 1), {'col': LITE})]).draw(c, t)
    b = Line(120, 1400, [('vor', 'l', 70, K('Ostfront vor Leningrad', 1), {'col': LITE}), ('Leningrad', 'b', 82, K('vor Leningrad verwundet.', 1), {'col': LITE, 'id': 'l'})]).draw(c, t)
    if 'l' in b: pen_ellipse(c, t, K('vor Leningrad verwundet.', 1) + 0.1, b['l'], col=LITE)
@scene(T6, T_END + 1, '502')
def c7(c, t):
    u = eout((t - T6) / 0.4); x0, y0, bw, bh = 110, 1060, 860, 560
    s_ = lerp(1.12, 1.0, u); cw, ch = int(bw * s_), int(bh * s_); cx, cy = x0 + (bw - cw) // 2, y0 + (bh - ch) // 2
    ph = grade(fit(load('t505.jpg'), cw, ch, 0.5, 0.4)).convert('RGBA')
    if u < 1: ph = ph.filter(ImageFilter.GaussianBlur(14 * (1 - u)))
    if t < K('einen Tiger.'):
        shl = Image.new('RGBA', shadow(cw, ch).size, (0, 0, 0, 0)); shl.putalpha(shadow(cw, ch)); c.alpha_composite(shl, (cx - 62, cy - 42))
    tt = K('einen Tiger.'); ko = 1 - clamp((t - tt) / 0.25)
    if ko > 0:
        if ko < 1: ph = ph.filter(ImageFilter.GaussianBlur(16 * (1 - ko))); ph.putalpha(int(255 * ko))
        c.alpha_composite(ph, (cx, cy))
    if t > tt:   # the Tiger cut-out rolls in on the paper
        k = eout((t - tt - 0.1) / 0.5); tk = load('tabandon_cut.png'); tk = tk.crop(tk.getbbox())
        place(c, tk, (int(lerp(1200, -40, k)), 1020, 1260, 700))
    Line(80, 330, [('schwere', 'l', 64, K('zur schweren', 1)), ('Panzer-Abteilung', 'b', 72, K('schweren Panzer-Abteilung', 1), {'box': 1})]).draw(c, t)
    bounce_word(c, t, K('Panzer-Abteilung 502', 1), '502', 'h', 330, 80, 430)
    Line(1000, 700, [('einen', 'l', 66, K('einen Tiger.'))], anchor='r').draw(c, t)
    slide_line(c, t, K('einen Tiger.', 1), [('Tiger.', 'h', 170, K('einen Tiger.', 1))], 520, 760, 300)

def frame(t):
    sc = [s for s in S if s[0] <= t < s[1]][-1]; t0, t1, wm, f = sc
    wa = eout((t - t0) / 0.4) * (1 - eout((t - (t1 - 0.25)) / 0.25))
    bg = background(t, wm, wa).convert('RGBA')
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); f(fg, t)
    ex = (t - (t1 - 0.2)) / 0.2
    if 0 < ex < 1 and t1 < T_END:
        fg = fg.filter(ImageFilter.GaussianBlur(18 * ex)); fg.putalpha(fg.getchannel('A').point(lambda v: int(v * (1 - 0.7 * ex))))
    en = (t - t0) / 0.15
    if 0 <= en < 1 and t0 > 0: fg = fg.filter(ImageFilter.GaussianBlur(10 * (1 - en)))
    bg.alpha_composite(fg); return bg.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'T': print(round(T_END, 3)); sys.exit()
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[3:]]; P = Image.new('RGB', (270 * len(ts), 480))
        for i, tt in enumerate(ts):
            im = frame(tt); ImageDraw.Draw(im).text((20, 20), '%.2f' % tt, font=font('b', 60), fill=(255, 0, 255)); P.paste(im.resize((270, 480)), (i * 270, 0))
        P.save(B + 'sh/' + sys.argv[2], quality=85); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
