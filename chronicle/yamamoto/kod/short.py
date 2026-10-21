# Chronicle of Power: Isoroku Yamamoto short (English, 1080x1920, about 53 s). Look: warm sepia grade, film grain, thin yellow corner marks,
# Oswald titles on yellow plates with a red rule, Playfair dates, word-by-word captions. Mostly archive film, photos always move.
import sys, subprocess, re, os
from lib9 import *
CX = 540            # centred; every text stays inside x 170..910 so it never reaches the like/comment buttons (x > 930)

TXT = open(B + 'code/script.txt').read().strip()
ST = []; _i = 0
for _s in re.split(r'(?<=[.!?])\s+', TXT): ST.append(WORDS[_i][1]); _i += len(_s.split())
def w(word, k): return wt(word, ST[k])
VEND = WORDS[-1][2]; T = VEND + 0.9
INK = (40, 32, 24)

def prog(t, w0, w1): return clamp((t - w0) / (w1 - w0))
def grade(can, warm=0.18, sat=0.75):
    """sepia leaning grade shared by every shot"""
    rgb = can.convert('RGB'); rgb = ImageEnhance.Color(rgb).enhance(sat)
    rgb = Image.blend(rgb, Image.new('RGB', (W, H), (92, 70, 40)), warm * 0.5); rgb = ImageEnhance.Contrast(rgb).enhance(1.08)
    return rgb.convert('RGBA')
_rr = np.random.default_rng(9)
_yy, _xx = np.mgrid[0:H, 0:W]; _rad = np.sqrt(((_xx - CX) / (W * 0.7)) ** 2 + ((_yy - 900) / (H * 0.5)) ** 2)
PLAIN = Image.fromarray((np.ones((H, W, 3)) * np.array((18, 16, 14), float) * (1 + 0.9 * np.clip(1 - _rad, 0, 1))[..., None]).clip(0, 255).astype(np.uint8)).convert('RGBA')
def plain(): return PLAIN.copy()

# ---------- brand text ----------
def fitfont(fn, s, size, maxw):
    f = fn(size)
    while f.getlength(s) > maxw and size > 20: size -= 4; f = fn(size)
    return f
def plate(can, t, t0, s, y, size=104, t1=None, col=DARK, bg=YEL, rule=True):
    """the house title: Oswald on a yellow plate, red rule underneath, slides up"""
    if t < t0: return
    k = eout((t - t0) / 0.35); out = 1.0 if t1 is None else 1 - clamp((t - t1) / 0.3); a = k * out
    if a <= 0.01: return
    f = fitfont(oswald, s, size, 690); tw_ = f.getlength(s); bb = f.getbbox(s); hh = bb[3] - bb[1]; pad = size * 0.18
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); x0 = CX - tw_ / 2; yy = y + (1 - k) * 30
    d.rectangle((x0 - pad, yy - hh / 2 - pad * 0.8, x0 - pad + (tw_ + 2 * pad) * eio((t - t0) / 0.3), yy + hh / 2 + pad * 0.8), fill=bg + (255,))
    d.text((CX, yy), s, font=f, fill=col + (255,), anchor='mm')
    if rule: d.rectangle((x0 - pad, yy + hh / 2 + pad * 0.8 + 10, x0 - pad + min(220, tw_) * eio((t - t0 - 0.2) / 0.3), yy + hh / 2 + pad * 0.8 + 18), fill=RED + (255,))
    if a < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, int(170 * a)), (0, 0), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (5, 10)); can.alpha_composite(L)
def big(can, t, t0, s, y, size=120, col=WHITE, t1=None):
    if t < t0: return
    f = fitfont(oswald, s, size, 720); txt(can, t, t0, (CX, y), s, f, col, t1)
def date(can, t, t0, s, y=YT, size=70, col=CREAM, t1=None):
    if t < t0: return
    f = fitfont(lambda z: playfair(z, 600), s, size, 720); txt(can, t, t0, (CX, y), s, f, col, t1)
# captions: the spoken phrase, current word in yellow (segments from the pause structure)
PHR = []
_cur = [WORDS[0]]
for a_, b_ in zip(WORDS, WORDS[1:]):
    if b_[1] - a_[2] > 0.1 or a_[0][-1] in '.,:?!' or len(_cur) >= 5: PHR.append(_cur); _cur = [b_]
    else: _cur.append(b_)
PHR.append(_cur)
def captions(can, t, y=1395):
    ph = [p for p in PHR if p[0][1] - 0.05 <= t <= p[-1][2] + 0.25]
    if not ph: return
    p = ph[-1]; ws = [x[0].upper() for x in p]; f = fitfont(lambda z: oswald(z, 600), ' '.join(ws), 64, 720); sp = f.getlength(' ')
    tot = sum(f.getlength(s) for s in ws) + sp * (len(ws) - 1); x = CX - tot / 2
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    nxt = [x[1] for x in p[1:]] + [p[-1][2] + 0.25]
    for s, (_, a_, b_), n_ in zip(ws, p, nxt):
        on = a_ - 0.03 <= t; col = YEL if a_ - 0.03 <= t < n_ - 0.03 else (WHITE if on else (150, 146, 138))
        d.text((x, y), s, font=f, fill=col + (255,), anchor='lm'); x += f.getlength(s) + sp
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 220), (0, 0), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (3, 6)); can.alpha_composite(L)
# ---------- shots ----------
def P(n, mode='pan', d=1, ov=None, grey=0.0, **kw):
    def fn(t, w0, w1):
        can = pan(n, t, w0, w1, d, **kw) if mode == 'pan' else fit(n, t, w0, w1, **kw)
        can = grade(can)
        if grey: can = Image.blend(can, ImageEnhance.Color(can).enhance(0.0), grey * prog(t, w0, w1))
        shade(can, 200, 0.55)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
CLIPN = len([f for f in os.listdir(B + 'clip') if f.endswith('.jpg')])
@functools.lru_cache(maxsize=6)
def cframe(i): return Image.open(B + 'clip/f%05d.jpg' % max(1, min(CLIPN, i))).convert('RGB')
def C(a, b, ov=None, cx=0.5, z1=1.06, speed=1.0):
    def fn(t, w0, w1):
        rate = min(speed, (b - a) / max(0.1, w1 - w0)); s_ = min(a + (t - w0) * rate, b - 0.05)
        im = cframe(int(s_ * FPS) + 1); z = lerp(1.0, z1, prog(t, w0, w1)); ch = 1080 / z; cw = ch * W / H
        x0 = min(max(cx * 1920 - cw / 2, 0), 1920 - cw); y0 = (1080 - ch) / 2
        can = grade(im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA'), 0.25, 1.0); shade(can, 200, 0.55)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
def lines(can, t, t0, polys, dur=1.0, col=YEL, wd=6):
    if t < t0: return
    lens = [sum(math.dist(p[i], p[i + 1]) for i in range(len(p) - 1)) for p in polys]; goal = sum(lens) * eio((t - t0) / dur); outs = []
    for p, l in zip(polys, lens):
        if goal <= 0: break
        out = [p[0]]; acc = 0
        for i in range(len(p) - 1):
            s_ = math.dist(p[i], p[i + 1])
            if acc + s_ >= goal: f = (goal - acc) / s_ if s_ else 0; out.append((lerp(p[i][0], p[i + 1][0], f), lerp(p[i][1], p[i + 1][1], f))); break
            out.append(p[i + 1]); acc += s_
        outs.append(out); goal -= l
    shadowed(can, lambda d: [d.line(o, fill=col + (255,), width=wd, joint='curve') for o in outs if len(o) > 1], 8, (3, 5), 160)

def doc_card(can, t, t0, rows, cy=820, w=760):
    """intercepted signal on a paper form, typed line by line"""
    if t < t0: return
    k = eout((t - t0) / 0.4); h = 120 + sum(sz * 1.55 for _, sz, _ in rows); L = Image.new('RGBA', (w + 60, int(h + 60)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((30, 30, 30 + w, 30 + h), fill=(226, 216, 192, 255)); d.rectangle((30, 30, 30 + w, 30 + h), outline=(150, 135, 105, 255), width=3)
    y = 80; tt = t - t0 - 0.35
    for s_, sz, col in rows:
        n = max(0, min(len(s_), int(tt / 0.03))); tt -= len(s_) * 0.03 + 0.08
        d.text((30 + w / 2, y + sz * 0.5), s_[:n], font=typew(sz), fill=col + (255,), anchor='mm'); y += sz * 1.55
    L = L.rotate(-2, expand=True, resample=Image.BICUBIC)
    if k < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * k)))
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), (int(CX - L.width / 2 + 14), int(cy - L.height / 2 + 22)), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    can.alpha_composite(L, (int(CX - L.width / 2), int(cy - L.height / 2 + (1 - k) * 60)))
def stampit(can, t, t0, s_, xy, size=80, rot=-10):
    if t < t0: return
    k = eout((t - t0) / 0.25); f = oswald(size); tw_ = f.getlength(s_); bw, bh = tw_ + size * 0.7, size * 1.5
    L = Image.new('RGBA', (int(bw + 40), int(bh + 40)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((20, 20, 20 + bw, 20 + bh), outline=RED + (235,), width=9); d.text((20 + bw / 2, 20 + bh / 2), s_, font=f, fill=RED + (240,), anchor='mm')
    L = L.rotate(rot, expand=True, resample=Image.BICUBIC); sc = lerp(1.5, 1.0, k); L = L.resize((max(1, int(L.width * sc)), max(1, int(L.height * sc))), Image.BICUBIC)
    if k < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * k)))
    can.alpha_composite(L, (int(xy[0] - L.width / 2), int(xy[1] - L.height / 2)))

# ---- shots ----
def s_decoded(t, w0, w1):
    can = grade(dim(fit('s4-1', t, w0, w1, 1.06), 175)); t0 = w('decoded', 1) - 0.25
    doc_card(can, t, t0, [('INTERCEPTED SIGNAL', 40, INK), ('', 10, INK), ('C-IN-C COMBINED FLEET', 34, INK), ('18 APRIL', 34, INK), ('RABAUL 0600', 34, INK), ('BALLALE 0800', 34, INK)], 800, 700)
    stampit(can, t, t0 + 1.2, 'DECODED', (CX + 150, 1010), 74, -9); return can
def s_factories(t, w0, w1):
    can = grade(fit('s3-3', t, w0, w1, 1.1)); shade(can, 200, 0.55); return can
def s_sixmonths(t, w0, w1):
    can = plain(); k = 9; tc = w('carriers', k)
    for i, (dt, y) in enumerate((('DEC 7, 1941', 560), ('JUNE 4, 1942', 760))):
        t0 = w0 + 0.1 + i * 0.5; txt(can, t, t0, (CX, y), dt, oswald(84, 600), WHITE if i == 0 else YEL)
    if t > w0 + 0.35: lines(can, t, w0 + 0.35, [[(CX, 615), (CX, 700)]], 0.3, CREAM, 5)
    for i in range(4):
        x = CX - 300 + i * 200; y = 1000; t0 = tc - 0.3 + i * 0.12
        if t < t0: continue
        a = clamp((t - t0) / 0.3); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.polygon([(x - 85, y), (x + 85, y), (x + 70, y + 26), (x - 70, y + 26)], fill=(40, 42, 46, int(255 * a)), outline=CREAM + (int(255 * a),))
        d.rectangle((x - 85, y - 8, x + 85, y), fill=(60, 62, 66, int(255 * a))); d.rectangle((x + 30, y - 34, x + 48, y - 8), fill=CREAM + (int(255 * a),))
        can.alpha_composite(L)
        if t > t0 + 0.35: lines(can, t, t0 + 0.35, [[(x - 70, y - 50), (x + 70, y + 50)], [(x + 70, y - 50), (x - 70, y + 50)]], 0.25, RED, 10)
    return can
RAB = Map(156.1, -7.3, 12.0)
def s_route(t, w0, w1):
    z = lerp(1.0, 1.05, prog(t, w0, w1)); can = grade(RAB.frame(z), 0.15, 1.0); m = RAB
    rb, bl, gc = m.p(152.2, -4.2, z), m.p(155.88, -6.87, z), m.p(160.0, -9.43, z)
    for p_, nm, col, off in ((rb, 'RABAUL', WHITE, (0, -46)), (bl, 'BALLALE', YEL, (-20, 44)), (gc, 'GUADALCANAL', CREAM, (-150, -44))):
        dot(can, *p_, col, 10); txt(can, t, w0 + 0.2, (p_[0] + off[0], p_[1] + off[1]), nm, oswald(44, 600), col)
    dashed(can, [rb, bl], eio((t - w0 - 0.2) / 1.4), YEL, 6)
    if t > w('travel', 10): dashed(can, [gc, (lerp(gc[0], bl[0], 0.85), lerp(gc[1], bl[1], 0.85))], eio((t - w('travel', 10)) / 1.2), RED, 6)
    return can
def s_calendar(t, w0, w1):
    can = grade(dim(pan('s4-6', t, w0, w1, 1), 170)); k = 12
    for i, (yr, t0) in enumerate((('1942', w('Doolittle', k) - 0.3), ('1943', w('Doolittle', k) + 0.9))):
        if t < t0: continue
        u = eout((t - t0) / 0.4); x = CX - 190 + i * 380; y = 760 + (1 - u) * 60
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); a = int(255 * u)
        d.rectangle((x - 160, y - 190, x + 160, y + 190), fill=(236, 230, 214, a)); d.rectangle((x - 160, y - 190, x + 160, y - 110), fill=RED + (a,))
        d.text((x, y - 150), 'APRIL', font=oswald(56), fill=WHITE + (a,), anchor='mm'); d.text((x, y + 10), '18', font=oswald(170), fill=INK + (a,), anchor='mm')
        d.text((x, y + 140), yr, font=oswald(56, 600), fill=INK + (a,), anchor='mm')
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, int(150 * u)), (0, 0), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (8, 14)); can.alpha_composite(L)
    return can

# ---- title track (voice synced; each leaves when the next sentence starts) ----
TR = [('date', ST[0], 'April 18, 1943', YT, 74, CREAM, w('one', 0)), ('plate', w('sixteen', 0), '16 FIGHTERS', 1150, 110, None, w('kill', 0) - 0.1),
      ('plate', w('one', 0), 'ONE TARGET', 1150, 110, None, None),
      ('plate', w('Isoroku', 2), 'ISOROKU YAMAMOTO', 1150, 96, None, w('who', 2) - 0.1), ('plate', w('Pearl', 2), 'PEARL HARBOR', 1150, 110, None, None),
      ('plate', w('never', 3), 'HE NEVER WANTED THIS WAR', 1150, 84, None, None),
      ('date', ST[4], 'Tsushima, 1905', 1010, 74, CREAM, None), ('plate', w('fingers', 4), 'LOST TWO FINGERS', 1150, 100, None, None),
      ('plate', w('Harvard', 5), 'HARVARD', 1150, 120, None, w('Washington', 5) - 0.1), ('plate', w('Washington', 5), 'WASHINGTON', 1150, 120, None, None),
      ('plate', w('factories', 6), 'FACTORIES', 1150, 110, None, w('oil', 6) - 0.1), ('plate', w('oil', 6), 'OIL FIELDS', 1150, 110, None, None),
      ('plate', w('six', 7), 'SIX MONTHS', 1150, 110, None, w('year', 7) - 0.1), ('plate', w('year', 7), 'MAYBE A YEAR', 1150, 110, None, w('after', 7) - 0.1),
      ('plate', w('confidence', 7), 'THEN: NO CONFIDENCE', 1150, 96, None, None),
      ('date', w('Pearl', 8), 'December 7, 1941', YT, 74, CREAM, None), ('plate', w('strike', 8), 'PEARL HARBOR', 1150, 110, None, None),
      ('date', ST[9], 'Midway, June 1942', YT, 74, CREAM, None), ('plate', w('carriers', 9), '4 CARRIERS LOST', 1150, 104, None, None),
      ('plate', w('codebreakers', 10), 'CODE CRACKED', 430, 110, None, None),
      ('date', ST[11], 'Bougainville', YT, 74, CREAM, None), ('plate', w('shot', 11), 'SHOT DOWN', 1150, 120, None, None),
      ('plate', w('Doolittle', 12), 'ONE YEAR AFTER DOOLITTLE', 1150, 88, None, None)]
def _end(t0, forced):
    nxt = [x for x in ST if x > t0 + 0.05]; e = (nxt[0] - 0.08) if nxt else None
    return forced if forced is not None and (e is None or forced < e) else e
TRACK = [(k, t0, s_, y, sz, col, (max(_end(t0, fe), t0 + 1.1) if _end(t0, fe) is not None else None)) for k, t0, s_, y, sz, col, fe in TR]   # at least 1.1 s on screen
for i, (k, t0, s_, y, sz, col, t1) in enumerate(TRACK):     # a title never fades over the next one in the same place
    for k2, u0, *_r in [(x[0], x[1], x[3]) for x in TRACK[i + 1:]]:
        if (k2 == 'date') == (k == 'date') and abs(_r[0] - y) < 100 and u0 > t0 and (t1 is None or u0 < t1 + 0.3):
            TRACK[i] = (k, t0, s_, y, sz, col, u0 - 0.32); break
def titles(can, t):
    for k, t0, s_, y, sz, col, t1 in TRACK:
        if t < t0 or (t1 is not None and t > t1 + 0.3): continue
        if k == 'date': date(can, t, t0, s_, y, sz, col, t1)
        elif k == 'big': big(can, t, t0, s_, y, sz, col, t1)
        elif k == 'red': plate(can, t, t0, s_, y, sz, t1, WHITE, RED, False)
        else: plate(can, t, t0, s_, y, sz, t1)

# ---------- timeline ----------

def at(k, word=None): return (ST[k] if word is None else w(word, k)) - 0.12
ANCH = [
 (0.0, P('s4-4', 'pan', 1)),
 (at(1), P('s4-1', 'fit', z1=1.08)), (at(1, 'because'), s_decoded),
 (at(2), P('s1-1', 'fit', z1=1.1)), (at(2, 'who'), C(0.5, 9.8, None, 0.5, 1.05)),
 (at(3), P('s3-5', 'fit', z1=1.08)),
 (at(4), P('s2-3', 'fit', z1=1.1)),
 (at(5), P('s2-5', 'fit', z1=1.08)), (at(5, 'Washington'), P('s2-1', 'fit', z1=1.08)),
 (at(6), s_factories),
 (at(7), P('s3-1', 'fit', z1=1.08)), (at(7, 'after'), P('s5', 'fit', z1=1.08)),
 (at(8), P('s1-2', 'fit', z1=1.08)), (at(8, 'strike'), C(17.2, 25.0, None, 0.5, 1.06, 1.0)),
 (at(9), s_sixmonths),
 (at(10), s_route),
 (at(11), P('s4-3', 'fit', z1=1.08)), (at(11, 'shot'), P('s4-5', 'pan', 1)),
 (at(12), s_calendar)]
OV = 0.25
SC = [(0 if i == 0 else s - OV, T if i == len(ANCH) - 1 else ANCH[i + 1][0] + OV, fn) for i, (s, fn) in enumerate(ANCH)]
def frame(t):
    act = [s for s in SC if s[0] <= t < s[1]] or [SC[-1]]
    img = act[0][2](t, act[0][0], act[0][1])
    if len(act) > 1: img = Image.blend(img, act[1][2](t, act[1][0], act[1][1]), eio((t - act[1][0]) / (act[0][1] - act[1][0])))
    img.alpha_composite(VIG); titles(img, t); captions(img, t)
    fade = clamp(1 - t / 0.3)
    if fade > 0: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * fade))))
    a = np.asarray(img.convert('RGB')).astype(np.int16) + np.random.default_rng(int(t * 30)).normal(0, 5, (H, W))[..., None].astype(np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); P_ = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = frame(t).convert('RGBA'); d = ImageDraw.Draw(f)
            if os.environ.get('UI'):
                d.rectangle((0, 0, W, 290), outline=(0, 255, 255, 255), width=4); d.rectangle((930, 680, W, 1580), outline=(0, 255, 255, 255), width=4); d.rectangle((0, 1580, W, H), outline=(0, 255, 255, 255), width=4)
            P_.paste(f.convert('RGB').resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P_.save(B + sys.argv[2], quality=85); sys.exit()
    if sys.argv[1] == 'list':
        for s, e, fn in SC: print(f'{s:6.2f} {e:6.2f} {getattr(fn, "__qualname__", "")}')
        sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-maxrate', '12M', '-bufsize', '20M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
