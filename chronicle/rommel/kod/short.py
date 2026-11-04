# Chronicle of Power: Erwin Rommel short (English, 1080x1920, about 53 s). Look: warm sepia grade, film grain, thin yellow corner marks,
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
def frame_marks(can):
    d = ImageDraw.Draw(can); c = YEL + (190,); l = 70; xl, xr = CX - 390, CX + 390
    for (x, y, sx, sy) in ((xl, 300, 1, 1), (xr, 300, -1, 1), (xl, 1560, 1, -1), (xr, 1560, -1, -1)):
        d.line((x, y, x + sx * l, y), fill=c, width=4); d.line((x, y, x, y + sy * l), fill=c, width=4)

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
def hitler_pan(t, w0, w1):
    """cold open: from Hitler on the left to Rommel on the right (crop slides left to right)"""
    im = src('h01'); cw = im.height * W / H; u = eio(prog(t, w0, w1)); cx = lerp(560, 1860, u)
    x0 = min(max(cx - cw / 2, 0), im.width - cw); z = lerp(1.0, 1.06, prog(t, w0, w1)); ch = im.height / z; cw2 = cw / z
    can = grade(im.resize((W, H), Image.BICUBIC, box=(x0 + (cw - cw2) / 2, (im.height - ch) / 2, x0 + (cw + cw2) / 2, (im.height + ch) / 2)).convert('RGBA')); shade(can, 200, 0.55)
    plate(can, t, w('Hitler', 0), 'HITLER', 470, 96, w('marshal', 0))
    big(can, t, w('choice', 0), 'TRIAL', 720, 150, WHITE)
    big(can, t, w('poison', 0), 'OR POISON', 880, 150, RED)
    return can
def ov_name(can, t, w0, w1):
    pass
def ov_ww1(can, t, w0, w1): pass
RIDGE = [(0, 1150), (120, 1080), (230, 1020), (300, 1050), (400, 900), (480, 800), (560, 660), (600, 620), (650, 670), (740, 780), (840, 850), (1080, 980)]
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
def s_matajur(t, w0, w1):
    can = grade(dim(fit('r04', t, w0, w1, 1.08), 175)); k = 2
    lines(can, t, w0, [RIDGE], 1.4, CREAM, 6); lines(can, t, w0 + 0.4, [[(60, 1200), (200, 1120), (330, 1060), (430, 940), (520, 800), (600, 680)]], 1.4, YEL, 6)
    tg = w('Matajur', k)
    if t > tg:
        u = eout((t - tg) / 0.5); lines(can, t, tg, [[(600, 620), (600, 620 - 130 * u)]], 0.2, WHITE, 6)
        shadowed(can, lambda d: d.polygon([(600, 620 - 130 * u), (690, 620 - 108 * u), (600, 620 - 86 * u)], fill=RED + (255,)))
    tc = w('9,000', k)
    if t > tc - 0.3: counter(can, t, tc - 0.3, 0, 9000, (CX, 760), 200, YEL, 1.0, '{:,}')
    return can
def ov_france(can, t, w0, w1): pass
FR = Map(2.6, 50.0, 7.6, hi=('France', 'Belgium'))
def s_frmap(t, w0, w1):
    z = lerp(1.0, 1.06, prog(t, w0, w1)); can = grade(FR.frame(z), 0.2, 1.0); m = FR
    dn, tgt = m.p(4.91, 50.26, z), m.p(0.75, 49.87, z); dot(can, *dn, YEL, 12)
    arrow(can, dn, tgt, eio((t - w0 - 0.1) / 1.0), RED, 24, 60)
    if t > w('lost', 3) and int((t - w('lost', 3)) * 3) % 2 == 0: txt(can, t, w('lost', 3), (tgt[0] + 10, tgt[1] - 110), '?', oswald(130), YEL)
    return can
def s_ghost(t, w0, w1):
    base = grade(pan('r19', t, w0, w1, 1)); g = base.copy(); ph = t - w0
    for k_, dx in enumerate((22, -30)):
        sh_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh_.paste(ImageEnhance.Color(base).enhance(0.1), (int(dx * math.sin(ph * 2.3 + k_)), 0)); g = Image.blend(g, sh_, 0.25)
    shade(g, 200, 0.55); return g
def ov_africa(can, t, w0, w1): pass
def ov_drove(can, t, w0, w1): pass
def ov_feared(can, t, w0, w1): pass
def s_strike(t, w0, w1):
    can = grade(dim(pan('r35', t, w0, w1, 1), 170)); k = 7
    txt(can, t, w0, (CX, 760), 'ROMMEL', oswald(190), WHITE)
    ts = w('stop', k)
    if t > ts: lines(can, t, ts, [[(150, 790), (890, 740)]], 0.35, RED, 22)
    return can
def s_paper(t, w0, w1):
    can = plain(); u = prog(t, w0, w1); k = 8
    L = Image.new('RGBA', (860, 1000), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.rectangle((0, 0, 860, 1000), fill=(226, 220, 204, 255))
    d.line((40, 110, 820, 110), fill=INK + (255,), width=4); d.line((40, 118, 820, 118), fill=INK + (255,), width=1)
    hl = 'THE DESERT FOX'; t0 = w('press', k); n = int(clamp((t - t0) / 0.8) * len(hl)) if t > t0 else 0
    d.text((430, 230), hl[:n], font=oswald(120), fill=INK + (255,), anchor='mm')
    for c in range(2):
        for r_ in range(18): d.rectangle((40 + c * 400, 360 + r_ * 32, 40 + c * 400 + 360 - (r_ % 4 == 3) * 130, 374 + r_ * 32), fill=(150, 144, 130, 255))
    L = L.rotate(lerp(-5, -2, u), expand=True, resample=Image.BICUBIC); sc = lerp(0.85, 1.0, eout(u * 1.5)); L = L.resize((int(L.width * sc), int(L.height * sc)), Image.BICUBIC)
    cy = 860; sh_ = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh_.paste((0, 0, 0, 150), (int(CX - L.width / 2 + 14), int(cy - L.height / 2 + 22)), L.getchannel('A'))
    can.alpha_composite(sh_.filter(ImageFilter.GaussianBlur(16))); can.alpha_composite(L, (int(CX - L.width / 2), int(cy - L.height / 2)))
    return can
def ov_fox(can, t, w0, w1): pass
def ov_youngest(can, t, w0, w1): pass
def ov_lost(can, t, w0, w1): pass
def s_files(t, w0, w1):
    can = grade(dim(pan('r38', t, w0, w1, -1), 185)); tv = w0 + 0.15
    tn = w('name', 10)
    for i in (0, 1, 3, 4, 2):
        t0 = tv + i * 0.12
        if t < t0: continue
        u = eout((t - t0) / 0.4); x = 190 + i * 175; y = lerp(1700, 760 + (i % 2) * 40, u)
        if i == 2 and t > tn: g = eout((t - tn) / 0.4); x = lerp(x, CX, g); y = lerp(y, 720, g)
        L = Image.new('RGBA', (260, 350), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.rectangle((0, 0, 260, 350), fill=(214, 200, 166, 255)); d.rectangle((0, 0, 260, 350), outline=(120, 100, 70, 255), width=3)
        for r_ in range(6): d.rectangle((26, 110 + r_ * 36, 234 - (r_ % 3) * 44, 124 + r_ * 36), fill=(150, 136, 110, 255))
        if i == 2 and t > w('name', 10): d.text((130, 54), 'ROMMEL', font=oswald(48), fill=(150, 30, 30, 255), anchor='mm')
        else: d.rectangle((36, 40, 224, 68), fill=(120, 104, 80, 255))
        L = L.rotate((i - 2) * 3, expand=True, resample=Image.BICUBIC)
        if i == 2 and t > tn: sc = lerp(1.0, 1.5, eout((t - tn) / 0.4)); L = L.resize((int(L.width * sc), int(L.height * sc)), Image.BICUBIC)
        can.alpha_composite(L, (int(x - L.width / 2), int(y - L.height / 2)))
    if t > tn: ring(can, t, tn + 0.3, CX, 532, RED, 150, False)
    return can
def ov_oct(can, t, w0, w1): pass
def ov_car(can, t, w0, w1): pass
def s_cyanide(t, w0, w1):
    can = grade(dim(fit('r40', t, w0, w1, 1.12), 120)); tk = w('cyanide', 11)
    if t > tk - 0.3:
        u = eout((t - tk + 0.3) / 0.4); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); cx, cy = CX, 560
        d.rounded_rectangle((cx - 120 * u, cy - 44 * u, cx + 120 * u, cy + 44 * u), radius=int(44 * u) + 1, fill=(220, 220, 210, 255), outline=WHITE + (255,), width=4)
        d.line((cx, cy - 44 * u, cx, cy + 44 * u), fill=(150, 150, 140, 255), width=4); can.alpha_composite(L)
    return can
def ov_hero(can, t, w0, w1):
    pass

# ---------- title track: the titles of the first cut, same places; each comes in on its word and leaves when the next sentence starts ----------
# (kind, t0, text, y, size, colour, forced end)
TR = [('date', ST[1], 'Field Marshal', 1010, 64, CREAM, None), ('plate', w('Erwin', 1), 'ERWIN ROMMEL', 1150, 120, None, None),
      ('date', ST[2], 'World War One', YT, 72, CREAM, w('stormed', 2) - 0.1), ('plate', w('lieutenant', 2), 'A YOUNG LIEUTENANT', 1150, 90, None, w('stormed', 2) - 0.1),
      ('plate', w('stormed', 2), 'MONTE MATAJUR', 470, 96, None, w('captured', 2) - 0.2),
      ('date', ST[3], '1940', YT, 90, CREAM, None), ('plate', w('France', 3), 'FRANCE', 1150, 110, None, w('even', 3) - 0.1),
      ('big', w('German', 3), 'GERMAN COMMAND', 1060, 76, CREAM, None), ('plate', w('lost', 3), 'LOST TRACK OF HIM', 1180, 84, None, None),
      ('plate', w('Ghost', 4), 'THE GHOST DIVISION', 1150, 96, None, None),
      ('date', ST[5], 'North Africa, 1941', YT, 70, CREAM, None), ('plate', w('Africa', 5), 'AFRICA', 1150, 120, None, None),
      ('big', w('small', 6), 'A SMALL FORCE', 1060, 90, CREAM, w('British', 6) - 0.2), ('plate', w('Egypt', 6) - 0.3, 'BACK TO EGYPT', 1150, 100, None, None),
      ('big', w('feared', 7), 'THE BRITISH FEARED HIM', 1100, 84, WHITE, w('commander', 7) - 0.1), ('date', w('commander', 7), 'Their commander ordered:', 520, 60, CREAM, None),
      ('plate', w('stop', 7), 'STOP SAYING HIS NAME', 1150, 92, None, None),
      ('date', ST[8], 'The British press', YT, 66, CREAM, None), ('plate', w('Desert', 8), 'THE DESERT FOX', 1150, 120, None, None),
      ('date', ST[9], 'At fifty', 1010, 70, CREAM, None), ('plate', w('youngest', 9), 'YOUNGEST FIELD MARSHAL', 1150, 92, None, None),
      ('date', ST[10], '1944', YT, 90, CREAM, w('July', 10) - 0.1), ('big', w('Hitler', 10), 'HE TOLD HITLER', 1060, 80, CREAM, w('July', 10) - 0.1),
      ('plate', w('lost', 10), 'THE WAR IS LOST', 1170, 100, None, w('July', 10) - 0.1),
      ('date', w('July', 10), 'July 20, 1944', YT, 70, CREAM, None), ('plate', w('July', 10), 'THE PLOT FAILED', 1150, 100, None, w('name', 10) - 0.1),
      ('plate', w('name', 10), 'HIS NAME CAME UP', 1150, 100, None, None),
      ('date', ST[11], 'October 14, 1944', YT, 74, CREAM, None), ('plate', w('goodbye', 11), 'GOODBYE', 1150, 120, None, w('got', 11) - 0.1),
      ('big', w('got', 11), 'HE GOT INTO THE CAR', 1150, 84, WHITE, w('took', 11) - 0.1), ('red', w('cyanide', 11), 'CYANIDE', 1150, 130, None, None),
      ('date', ST[12], 'Ulm, October 18, 1944', YT, 62, CREAM, None), ('plate', w('hero', 12) - 0.15, 'BURIED AS A HERO', 1150, 104, None, None)]
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
 (0.0, hitler_pan),
 (at(1), P('r43', 'fit', ov=ov_name, z1=1.1)),
 (at(2), P('r11', 'fit', ov=ov_ww1, z1=1.1)), (at(2, 'stormed'), s_matajur),
 (at(3), P('r23', 'pan', 1, ov_france, zoom=1.0)), (at(3, 'even'), s_frmap),
 (at(4), s_ghost),
 (at(5), C(0.2, 4.1, ov_africa, 0.5, 1.08)), (at(6), C(18.7, 22.0, None, 0.5)), (at(6, 'drove'), C(33.0, 37.5, ov_drove, 0.45)),
 (at(7), C(29.4, 32.4, ov_feared, 0.5, 1.12)), (at(7, 'ordered'), s_strike),
 (at(8), s_paper), (at(8, 'Desert'), P('r07', 'fit', ov=ov_fox, z1=1.12)),
 (at(9), P('r09', 'fit', ov=ov_youngest, z1=1.08)),
 (at(10), C(56.2, 60.7, ov_lost, 0.5)), (at(10, 'July'), s_files),
 (at(11), P('r34', 'fit', ov=ov_oct, z1=1.08)), (at(11, 'got'), P('r36', 'pan', 1, ov_car)), (at(11, 'took'), s_cyanide),
 (at(12), P('r29', 'pan', -1, ov_hero))]
OV = 0.25
SC = [(0 if i == 0 else s - OV, T if i == len(ANCH) - 1 else ANCH[i + 1][0] + OV, fn) for i, (s, fn) in enumerate(ANCH)]
def frame(t):
    act = [s for s in SC if s[0] <= t < s[1]] or [SC[-1]]
    img = act[0][2](t, act[0][0], act[0][1])
    if len(act) > 1: img = Image.blend(img, act[1][2](t, act[1][0], act[1][1]), eio((t - act[1][0]) / (act[0][1] - act[1][0])))
    img.alpha_composite(VIG); frame_marks(img); titles(img, t); captions(img, t)
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
