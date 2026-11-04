# Laconia, first 29 s, in the collage style of the reference edits
from style import *
import lib9 as L9   # maps (Natural Earth outlines) from the channel kit

# 1: "Er versenkte ein Schiff," : a yellow band grows, the Laconia as a flat black silhouette slides onto it, the words slam in
def s1(t, w0, w1):
    can = paper().copy()
    band(can, t, 0.0, 960, 420, ACC, 0.45)
    word(can, t, ws('Er'), 'ER VERSENKTE', (W / 2, 640), black(92), INK, mode='rise')
    p, mb = mover(t, 0.15, 0.55, (W + 700, 980), (W / 2, 980))
    sink = eio((t - ws('Schiff') - 0.15) / 0.8)   # after the word, the ship tips and sinks a little
    place(can, cut('l_img', flat=INK, h=300), p[0], p[1] + sink * 40, 1.0, -sink * 6, mblur=mb)
    word(can, t, ws('ein', 0.5), 'EIN SCHIFF,', (W / 2, 1290), black(150), INK, mode='slam')
    return push(can, t, w0, w1)

# 2: "rettete danach Hunderte Schiffbrüchige" : yellow disc pops, HUNDERTE behind him, Hartenstein (cut-out) rises in front
def s2(t, w0, w1):
    can = paper().copy()
    disc(can, t, w0 + 0.02, (W / 2 + 40, 900), 380)
    word(can, t, ws('rettete'), 'rettete danach', (150, 470), bold(64), INK, 'lm', mode='wipe')
    word(can, t, ws('Hunderte'), 'HUNDERTE', (W / 2, 760), black(158), INK, mode='slam')   # between the disc and the figure
    p, mb = mover(t, w0 + 0.05, 0.6, (W / 2 + 60, 2400), (W / 2 + 60, 1060), back)
    place(can, cut('l_8576', h=1040), p[0], p[1], mblur=mb)
    word(can, t, ws('Schiffbrüchige', 2.5), 'Schiffbrüchige', (W / 2, 1690), hand(130), INK, mode='wipe', dur=0.5)
    bodylines(can, t, w0 + 0.3, 110, 1800, 3, 220)
    return push(can, t, w0, w1, 1.0, 1.04)

# 3: "und wurde dafür bombardiert." : diagonal stripes, the B-24 dives in with motion blur, slab headline settles letter by letter
def s3(t, w0, w1):
    can = paper().copy()
    stripes(can, t, w0, ACC, 5, 110, 170)
    word(can, t, ws('und', 3.3), 'und wurde dafür', (W / 2, 520), bold(66), INK, mode='rise')
    p, mb = mover(t, w0 + 0.05, 0.7, (W + 600, -400), (W / 2 + 30, 1000))
    place(can, cut('l_b24', h=760), p[0], p[1], 1.0, 8, mblur=mb)
    scramble(can, t, ws('bombardiert'), 'BOMBARDIERT.', (W / 2, 1460), slab(118), INK, 0.45)
    if t > ws('bombardiert'):   # a short shake on the word
        k = max(0.0, 1 - (t - ws('bombardiert')) / 0.3); dx = math.sin(t * 90) * 14 * k
        if abs(dx) > 0.5: can = can.transform(can.size, Image.AFFINE, (1, 0, -dx, 0, 1, 0), Image.BICUBIC)
    return push(can, t, w0, w1)

# 4: "Im September 1942 lag U 156 vor der Küste Westafrikas." : grid paper, the coast as a dark paper cut-out, typed date, a marker with a hand-drawn arrow
MA = L9.Map(-10.5, 2.5, 34.0)
@functools.lru_cache(None)
def land():
    b = np.asarray(MA.base().convert('RGB'), np.int16); sea = np.array(L9.SEA, np.int16)
    m = (np.abs(b - sea).sum(2) > 18).astype(np.uint8) * 255
    for y in range(0, H, 1): pass
    a = Image.fromarray(m).filter(ImageFilter.GaussianBlur(1.2))
    sp = Image.new('RGBA', (W, H), (52, 52, 56, 255)); sp.putalpha(a); return sp
SINK = (-11.63, -5.08)
def s4(t, w0, w1):
    can = paper(True).copy()
    k = eout((t - w0) / 0.6); L = land()
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.35 * k)))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (14, 26 + int((1 - k) * 120)))
    LL = L.copy(); LL.putalpha(L.getchannel('A').point(lambda v: int(v * k))); can.alpha_composite(LL, (0, int((1 - k) * 120)))
    typed(can, t, ws('September'), 'SEPTEMBER 1942', (W / 2, 330), mono(88), INK, 0.05)
    x, y = MA.p(*SINK)
    if t > ws('U', 7.5):
        u = back((t - ws('U', 7.5)) / 0.4); r = 34 * u; d = ImageDraw.Draw(can)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(196, 38, 40, 255)); d.ellipse((x - r * 0.4, y - r * 0.4, x + r * 0.4, y + r * 0.4), fill=(245, 245, 240, 255))
        v = eout((t - ws('U', 7.5) - 0.2) / 0.6)   # a hand-drawn curly arrow from the label to the marker
        pts = [(x + 260 - 260 * s_ + 40 * math.sin(s_ * 6), y + 220 - 220 * s_ + 30 * math.cos(s_ * 5)) for s_ in np.linspace(0, v, 40)]
        if len(pts) > 2: d.line(pts, fill=INK + (255,), width=6, joint='curve')
        word(can, t, ws('U', 7.5) + 0.25, 'U 156', (x + 300, y + 280), slab(84), INK, mode='slam')
    word(can, t, ws('Küste'), 'Westafrika', (MA.p(-2, 11)[0], MA.p(-2, 11)[1]), hand(96), ACC, mode='wipe', dur=0.5)
    return push(can, t, w0, w1, 1.0, 1.05)

# 5: "Am Abend des 12. September torpedierte Kommandant Werner Hartenstein" : dark stage, a light beam, Hartenstein in it, the name settles
@functools.lru_cache(None)
def beam():
    L = Image.new('L', (W, H), 0); ImageDraw.Draw(L).polygon([(-120, -200), (260, -200), (900, H), (300, H)], fill=150)
    return L.filter(ImageFilter.GaussianBlur(60))
def s5(t, w0, w1):
    can = paper(False, 0.62).copy()
    k = eout((t - w0) / 0.5); B_ = Image.new('RGBA', (W, H), (235, 232, 222, 0)); B_.putalpha(beam().point(lambda v: int(v * k))); can.alpha_composite(B_)
    typed(can, t, ws('12.'), '12. SEPTEMBER, ABENDS', (W / 2, 330), mono(62), (230, 230, 226), 0.04)
    p, mb = mover(t, w0 + 0.1, 0.8, (W / 2 + 500, 1180), (W / 2 + 120, 1180))
    place(can, cut('hart_c', h=1250), p[0], p[1], mblur=mb)
    word(can, t, ws('torpedierte'), 'TORPEDIERTE', (W / 2, 520), black(110), ACC, mode='slam')
    word(can, t, ws('Kommandant'), 'KOMMANDANT', (90, 1420), bold(58), (230, 230, 226), 'lm', mode='wipe')
    scramble(can, t, ws('Werner'), 'HARTENSTEIN', (W / 2 - 20, 1520), slab(108), (245, 245, 240), 0.5)
    return push(can, t, w0, w1, 1.0, 1.04)

# 6: "das britische Truppentransportschiff Laconia." : yellow band wipe, the Laconia cut-out in colour, LACONIA huge behind it, brackets
def s6(t, w0, w1):
    can = paper().copy()
    band(can, t, w0, 980, 560, ACC, 0.35)
    word(can, t, ws('britische', 15.2), 'BRITISCHES TRUPPENTRANSPORTSCHIFF', (W / 2, 560), bold(40), INK, mode='wipe', dur=0.5)
    word(can, t, ws('Laconia'), 'LACONIA', (W / 2, 900), black(230), (255, 255, 255), mode='slam')
    p, mb = mover(t, w0, 0.55, (-700, 1080), (W / 2, 1080))
    place(can, cut('l_img', bw=False, h=430), p[0], p[1], mblur=mb)
    brackets(can, t, w0 + 0.4, (60, 720, W - 60, 1300), INK)
    bodylines(can, t, w0 + 0.6, 90, 1370, 4, 300)
    return push(can, t, w0, w1)

# 7: "An Bord waren rund 2.700 Menschen:" : the number on a floor with its reflection, counting up
def s7(t, w0, w1):
    can = paper().copy(); d = ImageDraw.Draw(can)
    fl = Image.new('RGBA', (W, H - 1080), (0, 0, 0, 0)); g = np.linspace(40, 140, H - 1080).astype(np.uint8)
    fl.putalpha(Image.fromarray(np.repeat(g[:, None], W, 1))); can.alpha_composite(Image.new('RGBA', (W, H - 1080), (70, 70, 74, 255)).copy(), (0, 1080)) if False else can.alpha_composite(fl, (0, 1080))
    word(can, t, ws('An', 17.9), 'AN BORD', (W / 2, 700), mono(64), INK, mode='rise')
    if t > ws('2.700'):
        v = int(round(2700 * eout((t - ws('2.700')) / 0.9))); s_ = '{:,}'.format(v).replace(',', '.')
        f = black(300); L = Image.new('RGBA', (W, 420), (0, 0, 0, 0)); ImageDraw.Draw(L).text((W / 2, 400), s_, font=f, fill=INK + (255,), anchor='ms')
        can.alpha_composite(L, (0, 1080 - 400))
        R = L.transpose(Image.FLIP_TOP_BOTTOM); R.putalpha(R.getchannel('A').point(lambda v: int(v * 0.25))); can.alpha_composite(R.filter(ImageFilter.GaussianBlur(3)), (0, 1085))
    word(can, t, ws('Menschen', 19.5), 'MENSCHEN', (W / 2, 1300), black(110), ACC, mode='slam')
    return push(can, t, w0, w1, 1.0, 1.04)

# 8: the list: 54 figures (one for every 50 people); labels appear as they are spoken; 36 turn yellow for the 1,800 Italian prisoners
def figure(d, x, y, s, col):
    d.ellipse((x - s * 0.22, y - s * 0.95, x + s * 0.22, y - s * 0.51), fill=col + (255,))
    d.rounded_rectangle((x - s * 0.3, y - s * 0.45, x + s * 0.3, y + s * 0.35), s * 0.14, fill=col + (255,))
    d.rectangle((x - s * 0.22, y + s * 0.3, x - s * 0.04, y + s * 0.75), fill=col + (255,)); d.rectangle((x + s * 0.04, y + s * 0.3, x + s * 0.22, y + s * 0.75), fill=col + (255,))
def s8(t, w0, w1):
    can = paper(True).copy()
    cols, rows, s = 9, 6, 82; x0, y0 = W / 2 - (cols - 1) * 105 / 2, 760
    tp = ws('1.800')
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(cols * rows):
        r, c = divmod(i, cols); ti = w0 + 0.02 * i
        if t < ti: continue
        k = back((t - ti) / 0.3); yy = y0 + r * 125 + (1 - k) * 40
        yel = i >= cols * rows - 36 and t > tp + 0.03 * (i - (cols * rows - 36)) * 0.6
        figure(d, x0 + c * 105, yy, s * min(1, k), ACC if yel else (70, 70, 74))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.3)))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (6, 12)); can.alpha_composite(L)
    for s_, t0, y in (('britische Soldaten', ws('britische', 20.7), 330), ('Zivilisten, Frauen und Kinder', ws('Zivilisten'), 420), ('polnische Wachsoldaten', ws('polnische'), 510)):
        word(can, t, t0, s_, (W / 2, y), bold(64), INK, mode='wipe', dur=0.4)
    if t > tp:
        word(can, t, tp, '1.800', (W / 2, 1600), black(200), INK, mode='slam')
        word(can, t, ws('italienische', 26.5), 'ITALIENISCHE KRIEGSGEFANGENE', (W / 2, 1760), slab(50), INK, mode='wipe', dur=0.5)
    return push(can, t, w0, w1, 1.0, 1.03)

SC = [(0.0, s1), (ws('rettete'), s2), (ws('und', 3.3), s3), (ws('Im'), s4), (ws('Am', 10.9), s5), (ws('das', 15.2), s6), (ws('An', 17.9), s7), (ws('britische', 20.7), s8)]
TEND = wt('Als') - 0.08
def frame(t):
    i = max(j for j, (a, _) in enumerate(SC) if a <= t); a, fn = SC[i]; b = SC[i + 1][0] if i + 1 < len(SC) else TEND
    img = fn(t, a, b)
    if i + 1 < len(SC) and t > b - 0.12:   # quick smear into the next scene (the reference cuts on motion)
        u = (t - (b - 0.12)) / 0.12; dx = -W * 0.18 * eio(u)
        acc = np.zeros((H, W, 4), np.float32)
        for k in range(6): acc += np.asarray(img.transform(img.size, Image.AFFINE, (1, 0, -(dx * k / 5), 0, 1, 0), Image.BILINEAR), np.float32)
        img = Image.fromarray((acc / 6).astype(np.uint8))
    if i > 0 and t < a + 0.12:
        u = (t - a) / 0.12; dx = W * 0.18 * (1 - eio(u))
        acc = np.zeros((H, W, 4), np.float32)
        for k in range(6): acc += np.asarray(img.transform(img.size, Image.AFFINE, (1, 0, -(dx * k / 5), 0, 1, 0), Image.BILINEAR), np.float32)
        img = Image.fromarray((acc / 6).astype(np.uint8))
    a_ = np.asarray(img.convert('RGB')).astype(np.int16) + np.random.default_rng(int(t * 30)).normal(0, 3, (H, W))[..., None].astype(np.int16)
    return Image.fromarray(np.clip(a_, 0, 255).astype(np.uint8))

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); P_ = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = frame(t); ImageDraw.Draw(f).text((10, 10), '%.2f' % t, fill=(255, 0, 255)); P_.paste(f.resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P_.save(B + sys.argv[2], quality=85); sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
        if n % 30 == 0: print('t', n / FPS, flush=True)
    p.stdin.close(); p.wait(); print('rc', p.returncode)
