# Teil 2 v2 core: every page element is tied to the spoken words (unique phrase lookup), registers its box, and the camera is
# planned from those boxes: it arrives before an element appears, stays until the element has been readable, films fill the
# frame for at least a few seconds with their caption on screen the whole time. check() lists every element the camera misses,
# every element over the page-number zone and every overlap, before anything is rendered.
import re, math, functools
from lcore import *
from lcore import WORDS as _W
import ldraw as X
from drawings import drawing
C = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t3l/img/'
DARK = (34, 34, 36)
YMAX = PH - 165                      # nothing below this: the page number lives there
def _n(w): return re.sub(r'[^a-zäöüßłńśźżóąęć0-9]', '', w.lower())
_TOK = [_n(w[0]) for w in _W]
@functools.lru_cache(None)
def _find(phrase):
    p = [_n(x) for x in phrase.split()]; L = len(p)
    hits = [i for i in range(len(_TOK) - L + 1) if _TOK[i:i + L] == p]
    assert len(hits) == 1, 'phrase %r found %d times' % (phrase, len(hits))
    return hits[0]
def K(phrase, i=0):
    """start of word i of a phrase that occurs exactly once in the narration (video time)"""
    return _W[_find(phrase) + i][1] + OFF - 0.04
def KE(phrase, i=-1):
    j = _find(phrase) + (i if i >= 0 else len(phrase.split()) + i); return _W[j][2] + OFF

# ---------- registry ----------
REG = []; CUR = [None, None]; REC = [False]
def reg(box, t0, t1=None, kind='text'):
    if REC[0]: REG.append(dict(sp=CUR[0], side=CUR[1], box=tuple(int(v) for v in box), t0=t0, t1=t0 if t1 is None else t1, kind=kind))
def _tb(font, s, xy, anchor='la'):
    d = ImageDraw.Draw(Image.new('L', (8, 8))); return d.textbbox(xy, s, font=font, anchor=anchor)

# ---------- type ----------
def L(pg, t, t0, s, xy, font, col=TXT, anchor='la', kind='text'):
    reg(_tb(font, s, xy, anchor), t0, kind=kind); label(pg, t, t0, s, xy, font, col, anchor)
def KICK(pg, t, t0, s, y=200): L(pg, t, t0, s, (110, y), sans(38, 800), ACC)
def NOTE(pg, t, t0, s, xy, size=32): L(pg, t, t0, s, xy, italic(size), GREY)
def SAY(pg, t, phrase, xy, size=46, lh=None, maxw=1180, accent=(), bold=(), wg=400, col=TXT):
    """the spoken words of `phrase`, each fading in as it is spoken; accent words red and bold"""
    lh = lh or int(size * 1.36); i0 = _find(phrase); toks = phrase.split(); x0, y0 = xy
    acc = {_n(a) for a in accent}; bo = {_n(b) for b in bold}
    fN, fB = serif(size, wg), serif(size, 800); cx, cy = x0, y0; line = []; lines = []
    L_ = Image.new('RGBA', pg.size, (0, 0, 0, 0)) if t > -1e8 else None; d = ImageDraw.Draw(L_)
    for k, w_ in enumerate(toks):
        tw = _W[i0 + k][1] + OFF - 0.04; st = 'a' if _n(w_) in acc else ('b' if _n(w_) in bo else 'n'); f = fB if st != 'n' else fN
        if cx + f.getlength(w_) > x0 + maxw and cx > x0: lines.append(line); line = []; cx = x0; cy += lh
        line.append((cx, cy, w_, tw, f, st)); cx += f.getlength(w_ + ' ')
    lines.append(line)
    for ln in lines:
        x1 = max(c[0] + c[4].getlength(c[2]) for c in ln); reg((ln[0][0], ln[0][1], x1, ln[0][1] + size * 1.15), ln[0][3], ln[-1][3])
        for (x, y, w_, tw, f, st) in ln:
            k = eout((t - tw) / 0.22) if t >= tw else 0
            if k > 0: d.text((x, y + (1 - k) * 12), w_, font=f, fill=(ACC if st == 'a' else col) + (int(255 * k),))
    pg.paste(Image.alpha_composite(pg.convert('RGBA'), L_).convert('RGB')); return cy + lh
def COUNT(pg, t, t0, dur, v, xy, font, fmt, col=ACC):
    reg(_tb(font, fmt(v), xy), t0)
    if t < t0: return
    u = eio((t - t0) / dur); ImageDraw.Draw(pg).text(xy, fmt(v * u if u < 1 else v), font=font, fill=fade_col(col, eout((t - t0) / 0.3)))
def de(v): return '{:,.0f}'.format(v).replace(',', '.')
def RULE(pg, t, t0, y, x0=110, x1=PW - 110): reg((x0, y - 2, x1, y + 2), t0, kind='mark'); rule(pg, t, t0, y, x0, x1)
def STRIKE(pg, t, t0, x0, x1, y, wd=10):
    reg((x0, y - 6, x1, y + 6), t0, kind='mark')
    if t >= t0: u = eout((t - t0) / 0.45); ImageDraw.Draw(pg).line((x0, y, lerp(x0, x1, u), y), fill=ACC, width=wd)
def CIRCLE(pg, t, t0, box, dur=0.7, wd=6, pad=26):
    """a red pen circle drawn round an element"""
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; rx, ry = (x1 - x0) / 2 + pad, (y1 - y0) / 2 + pad * 0.8
    reg((cx - rx, cy - ry, cx + rx, cy + ry), t0, kind='mark')
    if t < t0: return
    u = eout((t - t0) / dur); n = 64; a0 = math.radians(200)
    pts = [(cx + rx * (1 + 0.03 * math.sin(i * 0.5)) * math.cos(a0 + 2.15 * math.pi * u * i / n), cy + ry * (1 + 0.03 * math.cos(i * 0.4)) * math.sin(a0 + 2.15 * math.pi * u * i / n)) for i in range(n + 1)]
    ImageDraw.Draw(pg).line(pts, fill=ACC, width=wd, joint='curve')
def UNDER(pg, t, t0, x0, x1, y, wd=6):
    reg((x0, y - 4, x1, y + 4), t0, kind='mark')
    if t >= t0: u = eout((t - t0) / 0.4); ImageDraw.Draw(pg).line((x0, y, lerp(x0, x1, u), y), fill=ACC, width=wd)
def DRAW(pg, t, t0, dur, make, box):
    reg(box, t0, kind='draw'); drawing(pg, t, t0, dur, make)
def ROUTE(pg, t, stops, x, y0, dy=74, size=42):
    """stops [(text, t)]: dots joined by a red line, each stop set when it is said"""
    d = ImageDraw.Draw(pg)
    for i, (s_, ti) in enumerate(stops):
        y = y0 + i * dy; f = serif(size, 700 if i == len(stops) - 1 else 400); reg((x, y - 8, x + 60 + f.getlength(s_), y + size), ti)
        if t < ti: continue
        k = eout((t - ti) / 0.35)
        if i: d.line((x + 14, y - dy + 30, x + 14, lerp(y - dy + 30, y - 6, k)), fill=fade_col(ACC, k), width=5)
        d.ellipse((x, y - 6, x + 28, y + 22), fill=fade_col(ACC if i == len(stops) - 1 else TXT, k))
        d.text((x + 60, y + 8), s_, font=f, fill=fade_col(TXT, k), anchor='lm')

# ---------- pictures ----------
CLIPR = {}
def film_at(key, t, t0, speed=1.0):
    a, b = CLIPR.get(key, (0.0, clip_n(key) / FPS - 0.2)); ct = a + ((t - t0) * speed) % (b - a); return clip_at(key, ct)
def _corners(pg, x0, y0, bw, bh, k):
    d = ImageDraw.Draw(pg); c = fade_col(DARK, k); d.rectangle((x0, y0, x0 + bw, y0 + bh), outline=fade_col((60, 60, 60), k), width=2); L_ = 46
    for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x0 + bw, y0, -1, 1), (x0, y0 + bh, 1, -1), (x0 + bw, y0 + bh, -1, -1)):
        d.polygon([(cx - sx * 8, cy - sy * 8), (cx + sx * L_, cy - sy * 8), (cx - sx * 8, cy + sy * L_)], fill=c)
def _shadow(pg, x0, y0, bw, bh, k):
    sh = Image.new('L', (bw + 80, bh + 80), 0); ImageDraw.Draw(sh).rectangle((48, 52, 40 + bw + 8, 40 + bh + 12), fill=int(120 * k))
    stamp_ink(pg, sh.filter(ImageFilter.GaussianBlur(12)), (x0 - 40, y0 - 40), (40, 34, 28))
def _cap(pg, t0, x0, y, cap, k):
    reg((x0, y + 26, x0 + italic(30).getlength(cap), y + 84), t0, kind='cap')
    d = ImageDraw.Draw(pg); d.line((x0, y + 30, x0 + 150, y + 30), fill=fade_col(ACC, k), width=5); d.text((x0, y + 44), cap, font=italic(30), fill=fade_col(GREY, k))
def FILM(pg, t, t0, key, box, cap=None, speed=1.0):
    x0, y0, bw, bh = [int(v) for v in box]; reg((x0, y0, x0 + bw, y0 + bh), t0, kind='pic')
    if cap and t < t0: reg((x0, y0 + bh + 26, x0 + italic(30).getlength(cap), y0 + bh + 84), t0, kind='cap')
    if t < t0: return
    k = eout((t - t0) / 0.5); g = film_at(key, t, t0, speed); w, h = g.size
    sc = max(bw / w, bh / h); cw, ch = bw / sc, bh / sc
    fr_ = tone(g.convert('L').resize((bw, bh), Image.BICUBIC, box=((w - cw) / 2, (h - ch) / 2, (w + cw) / 2, (h + ch) / 2)))
    _shadow(pg, x0, y0, bw, bh, k)
    if k < 1: fr_ = Image.blend(Image.new('RGB', fr_.size, PAPER), fr_, k)
    pg.paste(fr_, (x0, y0)); _corners(pg, x0, y0, bw, bh, k)
    if cap: _cap(pg, t0, x0, y0 + bh, cap, k)
@functools.lru_cache(maxsize=8)
def _src(name): return Image.open(C + name + '.jpg').convert('RGB')
def PHOTO(pg, t, t0, name, box, cap=None, fx=0.5, fy=0.5, zoom=0.07, drift=(0.03, 0.0)):
    """a colourised photo printed in colour; it slowly moves (zoom in and drift) as long as it is on the page"""
    x0, y0, bw, bh = [int(v) for v in box]; reg((x0, y0, x0 + bw, y0 + bh), t0, kind='pic')
    if cap and t < t0: reg((x0, y0 + bh + 26, x0 + italic(30).getlength(cap), y0 + bh + 84), t0, kind='cap')
    if t < t0: return
    k = eout((t - t0) / 0.5); u = clamp((t - t0) / 14.0); z = 1 + zoom * eio(u)
    g = _src(name); w, h = g.size; sc = max(bw / w, bh / h) * z; cw, ch = bw / sc, bh / sc
    cx = (w - cw) * clamp(fx + drift[0] * (u - 0.5)); cy = (h - ch) * clamp(fy + drift[1] * (u - 0.5))
    im = g.resize((bw, bh), Image.BICUBIC, box=(cx, cy, cx + cw, cy + ch))
    a = np.asarray(im, np.float32) * 0.94 + np.array([10, 8, 4], np.float32); im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    _shadow(pg, x0, y0, bw, bh, k)
    if k < 1: im = Image.blend(Image.new('RGB', im.size, PAPER), im, k)
    pg.paste(im, (x0, y0)); _corners(pg, x0, y0, bw, bh, k)
    if cap: _cap(pg, t0, x0, y0 + bh, cap, k)

# ---------- the camera, planned from the registry ----------
SMAX = 1.22
def frame_for(box, pad=60, smax=SMAX):
    x0, y0, x1, y1 = box; w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    s = min(smax, W / w, H / h); return ((x0 + x1) / 2, (y0 + y1) / 2, s)
def fill_frame(gbox, f=1.07):
    x0, y0, x1, y1 = gbox; bw, bh = x1 - x0, y1 - y0; return ((x0 + x1) / 2, (y0 + y1) / 2, f * max(W / bw, H / bh))
def gbox(e): x0, y0, x1, y1 = e['box']; o = PW if e['side'] == 'R' else 0; return (x0 + o, y0, x1 + o, y1)
def union(a, b): return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))
OV = (PW, 905, 0.60)
def plan(items, fills, win, CD=1.05, DWELL=1.5, LEAD=0.35, SMIN=0.64):
    """items: registry entries of one spread; fills: [(gbox, ta, tb)]; win = (spread visible from, turn starts)"""
    ev = [dict(box=gbox(e), a=e['t0'], b=e['t1'], fill=False) for e in items if e['kind'] != 'mark' and e['t0'] > win[0] - 5]
    ev += [dict(box=b, a=ta, b=tb, fill=True) for b, ta, tb in fills]
    ev.sort(key=lambda e: e['a'])
    cl = []
    for e in ev:
        if cl and not e['fill'] and not cl[-1]['fill']:
            u = union(cl[-1]['box'], e['box']); s = frame_for(u)[2]
            if s >= SMIN and e['a'] - cl[-1]['a'] < 16: cl[-1]['box'] = u; cl[-1]['b'] = max(cl[-1]['b'], e['b']); continue
        cl.append(dict(box=e['box'], a=e['a'], b=e['b'], fill=e['fill']))
    # resolve clusters that come too soon after the previous one: merge (zoom out) when possible
    i = 1
    while i < len(cl):
        p, c = cl[i - 1], cl[i]; need = c['a'] - LEAD - CD; free = p['b'] + (0.2 if p['fill'] else DWELL)
        if need < free and not p['fill'] and not c['fill']:
            u = union(p['box'], c['box'])
            if frame_for(u)[2] >= SMIN: p['box'] = u; p['b'] = max(p['b'], c['b']); cl.pop(i); continue
        i += 1
    keys = []; prev_free = win[0]
    for c in cl:
        tgt = fill_frame(c['box']) if c['fill'] else frame_for(c['box'])
        arr = (c['a'] if c['fill'] else c['a'] - LEAD); st = max(arr - CD, win[0]) if c['fill'] else max(arr - CD, prev_free); cd = CD if st + CD <= arr + 1.0 else CD
        keys.append((st,) + tgt + (cd,)); prev_free = max(st + cd, c['b'] + (0.15 if c['fill'] else DWELL))
    return keys, cl
def check(MAG, T_END, step=0.25, fills=()):
    """elements the camera does not show while they appear, elements over the page number, overlaps"""
    bad = []
    for e in REG:
        x0, y0, x1, y1 = e['box']
        if e['kind'] != 'mark' and (y1 > YMAX or x1 > PW - 100 or x0 < 100): bad.append(('RAND', e))
    by = {}
    for e in REG:
        if e['kind'] in ('mark', 'draw'): continue
        by.setdefault((e['sp'], e['side']), []).append(e)
    for k, es in by.items():
        for i in range(len(es)):
            for j in range(i + 1, len(es)):
                a, b = es[i]['box'], es[j]['box']
                if min(a[2], b[2]) - max(a[0], b[0]) > 6 and min(a[3], b[3]) - max(a[1], b[1]) > 6: bad.append(('OVERLAP', es[i], es[j]))
    for e in REG:
        if e['kind'] == 'mark' or e['t0'] < 0.5: continue
        if e['kind'] == 'cap' and any(f[0] == e['sp'] and abs(gbox(e)[1] - f[3][3]) < 40 for f in fills): continue   # caption of a film that fills the frame: shown on screen
        gb = gbox(e); miss = 0; n = 0; t = e['t0'] + 0.1
        while t <= e['t1'] + 1.0:
            n += 1; cx, cy, s = MAG.cam(t); hw, hh = W / 2 / s, H / 2 / s
            sp = sum(1 for a in MAG.turns if t >= a + MAG.TD)
            infill = any(f[0] == e['sp'] and f[1] <= t <= f[2] and min(gb[2], f[3][2]) > max(gb[0], f[3][0]) and min(gb[3], f[3][3]) > max(gb[1], f[3][1]) for f in fills)
            if not infill and (sp != e['sp'] or any(a <= t < a + MAG.TD for a in MAG.turns) or gb[0] < cx - hw - 8 or gb[2] > cx + hw + 8 or gb[1] < cy - hh - 8 or gb[3] > cy + hh + 8): miss += 1
            t += step
        if miss: bad.append(('UNSEEN %d/%d' % (miss, n), e))
    return bad
