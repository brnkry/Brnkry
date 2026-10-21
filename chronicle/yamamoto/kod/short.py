# Chronicle of Power: Isoroku Yamamoto short (English, 1080x1920, about 50 s). Warm sepia grade, film grain, Oswald titles on yellow plates.
# Titles pop in on their word and leave when the next sentence starts; pictures change on sentence starts; a few whip pans follow the motion.
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
def plate(can, t, t0, s, y, size=104, t1=None, col=DARK, bg=YEL, rule=True, x=None):
    """the house title: Oswald on a yellow plate, red rule underneath; pops in (0.15 s), leaves fast"""
    if t < t0: return
    cx = CX if x is None else x
    k = eout((t - t0) / 0.15); out = 1.0 if t1 is None else 1 - clamp((t - t1) / 0.12); a = out
    if a <= 0.01: return
    f = fitfont(oswald, s, size, 690); tw_ = f.getlength(s); bb = f.getbbox(s); hh = bb[3] - bb[1]; pad = size * 0.18
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); x0 = cx - tw_ / 2
    d.rectangle((x0 - pad, y - hh / 2 - pad * 0.8, x0 + tw_ + pad, y + hh / 2 + pad * 0.8), fill=bg + (255,))
    d.text((cx, y), s, font=f, fill=col + (255,), anchor='mm')
    if rule: d.rectangle((x0 - pad, y + hh / 2 + pad * 0.8 + 10, x0 - pad + min(220, tw_), y + hh / 2 + pad * 0.8 + 18), fill=RED + (255,))
    sc = lerp(1.18, 1.0, k)
    if sc != 1.0:
        L = L.resize((int(W * sc), int(H * sc)), Image.BICUBIC); L = L.crop((int((L.width - W) * cx / W), int((L.height - H) * y / H), int((L.width - W) * cx / W) + W, int((L.height - H) * y / H) + H))
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
def C(a, b, ov=None, cx=0.5, z1=1.06, speed=1.0, z0=1.0, cy=0.5):
    def fn(t, w0, w1):
        rate = min(speed, (b - a) / max(0.1, w1 - w0)); s_ = min(a + (t - w0) * rate, b - 0.05)
        im = cframe(int(s_ * FPS) + 1); z = lerp(z0, z1, prog(t, w0, w1)); ch = 1080 / z; cw = ch * W / H
        x0 = min(max(cx * 1920 - cw / 2, 0), 1920 - cw); y0 = min(max(cy * 1080 - ch / 2, 0), 1080 - ch)
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

# ---- helpers for writing on surfaces inside a photo ----
from scipy.ndimage import map_coordinates
def fitpt(n, t, w0, w1, z1, sx, sy):
    """screen position of a source pixel inside fit() (photo fills the frame height, zoom about the centre)"""
    im = src(n); z = lerp(1.0, z1, clamp((t - w0) / (w1 - w0))); pw = im.width * H / im.height
    cw, ch = im.width / z, im.height / z; x0 = (W - pw) / 2
    return (x0 + (sx - (im.width / 2 - cw / 2)) * pw / cw, (sy - (im.height / 2 - ch / 2)) * H / ch)
def ink_text(s_, size, col):
    f = oswald(size); w_ = int(f.getlength(s_)) + 20; L = Image.new('L', (w_, int(size * 1.5)), 0)
    ImageDraw.Draw(L).text((10, size * 0.75), s_, font=f, fill=255, anchor='lm'); return np.asarray(L).astype(np.float32) / 255
def on_globe(can, cx, cy, r, s_, size, th_c, ph_c, a, col=(28, 38, 70)):
    """write s_ on a sphere (centre cx, cy, radius r on screen) around longitude th_c, latitude ph_c (radians)"""
    if a <= 0.01: return
    A = ink_text(s_, size, col); th_, tw_ = A.shape
    x0, x1 = int(max(0, cx + r * math.sin(th_c - tw_ / r * 0.62))), int(min(W, cx + r))
    y0, y1 = int(max(0, cy + r * math.sin(ph_c) - th_ * 0.9)), int(min(H, cy + r * math.sin(ph_c) + th_ * 0.9))
    if x1 <= x0 or y1 <= y0: return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    ph = np.arcsin(np.clip((yy - cy) / r, -1, 1)); cp = np.cos(ph)
    sth = (xx - cx) / np.maximum(r * cp, 1); ok = np.abs(sth) < 0.995; th = np.arcsin(np.clip(sth, -1, 1))
    u = (th - th_c) * r + tw_ / 2; v = (ph - ph_c) * r + th_ / 2
    al = map_coordinates(A, [v, u], order=1, cval=0) * ok * np.clip(np.cos(th) * 1.4, 0, 1) * a * 0.9
    L = Image.new('RGBA', (x1 - x0, y1 - y0), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8))); can.alpha_composite(L, (x0, y0))
def _coeffs(dst, src_):
    M = []
    for (x, y), (X, Y) in zip(dst, src_): M += [[x, y, 1, 0, 0, 0, -X * x, -X * y], [0, 0, 0, x, y, 1, -Y * x, -Y * y]]
    return np.linalg.solve(np.array(M, float), np.array([c for p in src_ for c in p], float)).tolist()
def on_quad(can, quad, s_, size, a, col=(30, 32, 60)):
    """write s_ into a screen quad (TL, TR, BR, BL), like ink on paper"""
    if a <= 0.01: return
    A = ink_text(s_, size, col); h_, w_ = A.shape; T_ = Image.fromarray((A * 255 * a * 0.88).astype(np.uint8))
    co = _coeffs(quad, [(0, 0), (w_, 0), (w_, h_), (0, h_)])
    M_ = T_.transform((W, H), Image.PERSPECTIVE, co, Image.BICUBIC); L = Image.new('RGBA', (W, H), col + (0,)); L.putalpha(M_); can.alpha_composite(L)

# ---- shots ----
PLANE = [(0.4, (500, 1000)), (1.0, (550, 1050)), (1.3, (575, 1060)), (1.6, (610, 1140)), (1.9, (640, 1190)), (2.2, (675, 1250)), (2.5, (750, 1340)), (2.8, (775, 1440)), (3.1, (825, 1560))]
def s_intro(t, w0, w1):
    """opening film runs through the whole first sentence; '16 FIGHTERS' rides above the plane until it leaves the frame"""
    can = C(0.4, 6.9, None, 0.55, 1.0, 1.0, 1.0)(t, w0, w1); cs = 0.4 + t
    ts = w('sixteen', 0); te = w('kill', 0) - 0.05
    if ts <= t <= te + 0.15:
        c_ = min(cs, 3.05); xs = [p[0] for p in PLANE]
        px = float(np.interp(c_, xs, [p[1][0] for p in PLANE])); py = float(np.interp(c_, xs, [p[1][1] for p in PLANE]))
        plate(can, t, ts, '16 FIGHTERS', py - 190, 92, te, x=min(px - 140, 600))
    return can
def s_one(t, w0, w1):
    """s4-1 runs through sentence 1 without a cut; the intercepted signal is laid over it, fast but complete"""
    can = grade(fit('s4-1', t, w0, w1, 1.1)); shade(can, 200, 0.55); t0 = w('because', 1) - 0.4
    if t > t0: dim(can, 125 * clamp((t - t0) / 0.3))
    if t > t0:
        k = eout((t - t0) / 0.2); rows = [('INTERCEPTED SIGNAL', 40), ('', 10), ('C-IN-C COMBINED FLEET', 34), ('18 APRIL', 34), ('RABAUL 0600', 34), ('BALLALE 0800', 34)]
        cw_, h = 700, 120 + sum(sz * 1.55 for _, sz in rows); L = Image.new('RGBA', (cw_ + 60, int(h + 60)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rectangle((30, 30, 30 + cw_, 30 + h), fill=(226, 216, 192, 255)); d.rectangle((30, 30, 30 + cw_, 30 + h), outline=(150, 135, 105, 255), width=3)
        y = 80; tt = t - t0 - 0.15
        for s_, sz in rows:
            n = max(0, min(len(s_), int(tt / 0.012))); tt -= len(s_) * 0.012 + 0.04
            d.text((30 + cw_ / 2, y + sz * 0.5), s_[:n], font=typew(sz), fill=INK + (255,), anchor='mm'); y += sz * 1.55
        L = L.rotate(-2, expand=True, resample=Image.BICUBIC)
        if k < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * k)))
        cy = 800; sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), (int(CX - L.width / 2 + 14), int(cy - L.height / 2 + 22)), L.getchannel('A'))
        can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16))); can.alpha_composite(L, (int(CX - L.width / 2), int(cy - L.height / 2 + (1 - k) * 40)))
        stampit(can, t, t0 + 1.35, 'DECODED', (CX + 150, 990), 74, -9)
    return can
@functools.lru_cache(None)
def _cut():
    im = Image.open(B + 'img/cut_yamamoto.webp').convert('RGBA'); h = 1080; im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    g = np.ones(im.size[::-1], np.float32); g[-260:] = np.linspace(1, 0, 260)[:, None]
    im.putalpha(Image.fromarray((np.asarray(im.getchannel('A')) * g).astype(np.uint8))); return im
def s_cutout(t, w0, w1):
    """the name: archive film keeps running behind, the cut-out portrait large in the middle"""
    can = C(2.3, 5.2, None, 0.55, 1.12, 1.0, 1.04)(t, w0, w1); dim(can, 70)
    k = eout((t - w0 - 0.15) / 0.5); sc = lerp(0.92, 1.0, k) * lerp(1.0, 1.04, prog(t, w0, w1)); im = _cut()
    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.BICUBIC)
    if k < 1: im.putalpha(im.getchannel('A').point(lambda v: int(v * k)))
    x, y = int(CX - im.width / 2), int(1270 - im.height)
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, int(190 * k)), (x + 12, y + 18), im.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
    can.alpha_composite(im, (x, y)); return can
def s_globe(t, w0, w1):
    """'six months, maybe a year' written on the globe behind him, following its curve; framed to the left so the globe is in view"""
    im = src('s3-1'); sc = H / im.height; pw = im.width * sc; z = lerp(1.0, 1.06, prog(t, w0, w1))
    ax, ay = 0.0, H / 2                                      # zoom anchor: left edge, so the globe grows in place
    vw, vh = W / (sc * z), H / (sc * z); sx0 = ax / sc - (ax / sc) / z; sy0 = (ay / sc) - (ay / sc) / z
    can = grade(im.resize((W, H), Image.BICUBIC, box=(sx0, sy0, sx0 + vw, sy0 + vh)).convert('RGBA')); k = 7
    cx, cy, r = (166 - sx0) * sc * z, (700 - sy0) * sc * z, 492 * sc * z
    on_globe(can, cx, cy, r, 'SIX MONTHS', 96, 0.36, -0.22, clamp((t - w('six', k) + 0.05) / 0.12))
    on_globe(can, cx, cy, r, 'MAYBE A YEAR', 80, 0.36, 0.02, clamp((t - w('year', k) + 0.15) / 0.12))
    shade(can, 200, 0.55); return can
def s_paper(t, w0, w1):
    """'no confidence' written on the paper under his hand, readable for us"""
    can = grade(fit('s5', t, w0, w1, 1.06)); k = 7
    q = [fitpt('s5', t, w0, w1, 1.06, *p) for p in ((845, 1792), (1330, 1815), (1345, 1885), (850, 1893))]
    on_quad(can, q, 'NO CONFIDENCE', 90, clamp((t - w('no', k) + 0.05) / 0.12))
    shade(can, 170, 0.62); return can
def _smoke(t, w0, w1):
    """Pearl Harbor smoke (clip 23.0 to 31.0) behind the Midway dates, dark and soft"""
    s_ = lerp(23.0, 31.0, prog(t, w0, w1)); im = cframe(int(s_ * FPS) + 1); ch = 1080; cw = ch * W / H; x0 = 960 - cw / 2
    can = grade(im.resize((W, H), Image.BICUBIC, box=(x0, 0, x0 + cw, ch)).convert('RGBA'), 0.25, 1.0).filter(ImageFilter.GaussianBlur(3)); dim(can, 165); return can
def s_sixmonths(t, w0, w1):
    can = _smoke(t, w0, w1)
    for i, (dt, y) in enumerate((('DEC 7, 1941', 620), ('JUNE 4, 1942', 820))):
        t0 = w0 + 0.1 + i * 0.5; txt(can, t, t0, (CX, y), dt, oswald(84, 600), WHITE if i == 0 else YEL)
    if t > w0 + 0.35: lines(can, t, w0 + 0.35, [[(CX, 675), (CX, 760)]], 0.3, CREAM, 5)
    return can
RAB = Map(156.1, -7.3, 12.0)
@functools.lru_cache(None)
def _mapcard():
    return grade(RAB.frame(1.0), 0.15, 1.0).crop((60, 520, 1020, 1290))
def s_code(t, w0, w1):
    """the flag film keeps running; the route map comes in as a card at the start of the sentence and finishes its animation"""
    can = C(32.9, 34.9, None, 0.6, 1.1)(t, w0, w1); dim(can, 90); ts = ST[10] + 0.05
    k = eout((t - ts) / 0.3)
    if k <= 0: return can
    card = _mapcard().copy(); ox, oy = 60, 520
    def P_(lon, lat): q = RAB.p(lon, lat); return (q[0] - ox, q[1] - oy)
    rb, bl, gc = P_(152.2, -4.2), P_(155.88, -6.87), P_(160.0, -9.43)
    for p_, nm, col, off in ((rb, 'RABAUL', WHITE, (0, -46)), (bl, 'BALLALE', YEL, (-20, 44)), (gc, 'GUADALCANAL', CREAM, (-150, -44))):
        d = ImageDraw.Draw(card); d.ellipse((p_[0] - 10, p_[1] - 10, p_[0] + 10, p_[1] + 10), fill=col + (255,)); d.text((p_[0] + off[0], p_[1] + off[1]), nm, font=oswald(44, 600), fill=col + (255,), anchor='mm')
    def dash(pts, u, col):
        if u <= 0: return
        d = ImageDraw.Draw(card); (ax, ay), (bx, by) = pts; L_ = math.dist(pts[0], pts[1]); n = int(L_ / 22)
        for i in range(int(n * u)):
            if i % 2 == 0: d.line((lerp(ax, bx, i / n), lerp(ay, by, i / n), lerp(ax, bx, (i + 1) / n), lerp(ay, by, (i + 1) / n)), fill=col + (255,), width=7)
    dash((rb, bl), eio((t - ts - 0.3) / 0.9), YEL)
    tg = ts + 1.3; dash((gc, (lerp(gc[0], bl[0], 0.9), lerp(gc[1], bl[1], 0.9))), eio((t - tg) / 0.9), RED)
    if t > tg + 0.9: d = ImageDraw.Draw(card); d.ellipse((bl[0] - 34, bl[1] - 34, bl[0] + 34, bl[1] + 34), outline=RED + (255,), width=6)
    bord = Image.new('RGBA', (card.width + 16, card.height + 16), CREAM + (255,)); bord.alpha_composite(card, (8, 8))
    sc = lerp(0.9, 1.0, k); bord = bord.resize((int(bord.width * sc), int(bord.height * sc)), Image.BICUBIC)
    if k < 1: bord.putalpha(bord.getchannel('A').point(lambda v: int(v * k)))
    x, y = int(CX - bord.width / 2), int(900 - bord.height / 2)
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, int(170 * k)), (x + 14, y + 20), bord.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    can.alpha_composite(bord, (x, y)); return can
def s_calendar(t, w0, w1):
    can = grade(dim(pan('s4-6', t, w0, w1, 1), 170)); k = 12
    for i, (yr, t0) in enumerate((('1942', w('Doolittle', k) - 0.3), ('1943', w('Doolittle', k) + 0.9))):
        if t < t0: continue
        u = eout((t - t0) / 0.3); x = CX - 190 + i * 380; y = 760 + (1 - u) * 60
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); a = int(255 * u)
        d.rectangle((x - 160, y - 190, x + 160, y + 190), fill=(236, 230, 214, a)); d.rectangle((x - 160, y - 190, x + 160, y - 110), fill=RED + (a,))
        d.text((x, y - 150), 'APRIL', font=oswald(56), fill=WHITE + (a,), anchor='mm'); d.text((x, y + 10), '18', font=oswald(170), fill=INK + (a,), anchor='mm')
        d.text((x, y + 140), yr, font=oswald(56, 600), fill=INK + (a,), anchor='mm')
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, int(150 * u)), (0, 0), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (8, 14)); can.alpha_composite(L)
    return can

# ---- title track: pops on its word, leaves when the next sentence starts ----
def nxt(t0): n_ = [x for x in ST if x > t0 + 0.05]; return (n_[0] - 0.24) if n_ else None   # gone before the next picture fades in
TR = [('date', 0.25, 'April 18, 1943', YT, 74, CREAM, w('sixteen', 0) - 0.15),
      ('plate', w('one', 0) + 0.12, 'ONE TARGET', 1150, 110, None, w('knew', 1)),
      ('plate', w('Isoroku', 2) - 0.1, 'ISOROKU YAMAMOTO', 1150, 96, None, w('who', 2) - 0.12),
      ('plate', w('Pearl', 2) - 0.22, 'PEARL HARBOR', 520, 110, None, nxt(w('Pearl', 2))),
      ('plate', w('never', 3) - 0.1, 'HE NEVER WANTED THIS WAR', 1150, 84, None, nxt(w('never', 3))),
      ('date', ST[4], 'Tsushima, 1905', 1010, 74, CREAM, nxt(ST[4])), ('plate', w('fingers', 4) - 0.1, 'LOST TWO FINGERS', 1150, 100, None, nxt(ST[4])),
      ('plate', w('Harvard', 5) - 0.08, 'HARVARD', 860, 64, None, nxt(ST[5])), ('plate', w('Washington', 5) - 0.08, 'WASHINGTON', 960, 64, None, nxt(ST[5])),
      ('date', w('strike', 8) - 0.1, 'December 7, 1941', YT, 74, CREAM, nxt(ST[8])), ('plate', w('Pearl', 8) - 0.15, 'PEARL HARBOR', 560, 110, None, nxt(ST[8])),
      ('date', ST[9], 'Midway, June 1942', YT, 74, CREAM, nxt(ST[9])), ('plate', w('carriers', 9) - 0.1, '4 CARRIERS LOST', 1150, 104, None, nxt(ST[9])),
      ('plate', w('codebreakers', 10) - 0.1, 'CODE CRACKED', 400, 100, None, nxt(ST[10])),
      ('date', ST[11], 'Bougainville', YT, 74, CREAM, nxt(ST[11])), ('plate', w('shot', 11) - 0.1, 'SHOT DOWN', 1150, 120, None, nxt(ST[11])),
      ('plate', w('Doolittle', 12) - 0.1, 'ONE YEAR AFTER DOOLITTLE', 1150, 88, None, None)]
def titles(can, t):
    for k, t0, s_, y, sz, col, t1 in TR:
        if t < t0 or (t1 is not None and t > t1 + 0.15): continue
        if k == 'date': date(can, t, t0, s_, y, sz, col, t1)
        else: plate(can, t, t0, s_, y, sz, t1)

# ---------- timeline: (start, scene, transition into it) ----------
def at(k, word=None): return (ST[k] if word is None else w(word, k)) - 0.05
ANCH = [
 (0.0, s_intro, None),
 (w('one', 0) - 0.02, s_one, ('whip', 1)),
 (at(2), s_cutout, ('fade',)), (at(2, 'who'), C(10.4, 15.2, None, 0.6, 1.32, 1.0, 1.25, 0.7), ('whip', -1)),
 (at(3), P('s3-5', 'fit', z1=1.08), ('fade',)),
 (at(4), P('s2-3', 'fit', z1=1.1), ('fade',)),
 (at(5), P('s2-5', 'fit', z1=1.08), ('fade',)), (at(5, 'Washington'), P('s2-1', 'fit', z1=1.08), ('fade',)),
 (at(6), P('s3-3', 'fit', z1=1.1), ('fade',)),
 (at(7), s_globe, ('fade',)), (at(7, 'and'), s_paper, ('fade',)),
 (at(8), P('s1-1', 'fit', z1=1.08), ('fade',)), (at(8, 'and'), C(5.2, 9.9, None, 0.55, 1.06), ('whip', 1)), (at(8, 'Pearl'), C(17.0, 23.0, None, 0.5, 1.06, 1.0), ('fade',)),
 (at(9), s_sixmonths, ('fade',)),
 (at(10), s_code, ('fade',)),
 (at(11), P('s4-3', 'fit', z1=1.08), ('whip', -1)), (at(11, 'and'), P('s4-5', 'pan', 1), ('fade',)),
 (at(12), s_calendar, ('fade',))]
DUR = {'fade': 0.2, 'whip': 0.34}
SC = []
for i, (s0, fn, tr) in enumerate(ANCH):
    d_in = DUR[tr[0]] if tr else 0.0; nx = ANCH[i + 1] if i + 1 < len(ANCH) else None
    d_out = DUR[nx[2][0]] if nx else 0.0
    SC.append((s0 - d_in / 2, (nx[0] + d_out / 2) if nx else T, fn, tr))
def _shift(img, dx):
    out = Image.new('RGBA', (W, H), (0, 0, 0, 255)); out.alpha_composite(img, (int(dx), 0)) if -W < dx < W else None; return out
def whip(a, b, u, d):
    """camera swings in direction d: a leaves, b arrives, both smeared along the move"""
    e = eio(u); amt = 90 * math.sin(math.pi * u)
    def smear(im, dx):
        acc = np.zeros((H, W, 4), np.float32)
        for k in range(-3, 4): acc += np.asarray(_shift(im, dx + k * amt / 3), np.float32)
        return acc / 7
    A = smear(a, -d * e * W); B_ = smear(b, d * (1 - e) * W)
    mask = np.zeros((1, W, 1), np.float32); edge = W / 2 - d * (e - 0.5) * W
    xs = np.arange(W)[None, :, None]; mask = ((xs - edge) * d > 0).astype(np.float32) if True else mask
    return Image.fromarray((A * (1 - mask) + B_ * mask).clip(0, 255).astype(np.uint8), 'RGBA')
def frame(t):
    act = [s for s in SC if s[0] <= t < s[1]] or [SC[-1]]
    img = act[0][2](t, act[0][0], act[0][1])
    if len(act) > 1:
        b = act[1]; u = clamp((t - b[0]) / (act[0][1] - b[0])); nimg = b[2](t, b[0], b[1])
        img = whip(img, nimg, u, b[3][1]) if b[3] and b[3][0] == 'whip' else Image.blend(img, nimg, eio(u))
    img.alpha_composite(VIG); titles(img, t)
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
        for s, e, fn, tr in SC: print(f'{s:6.2f} {e:6.2f} {getattr(fn, "__qualname__", "")} {tr}')
        sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-maxrate', '12M', '-bufsize', '20M', '-preset', 'medium', B + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
