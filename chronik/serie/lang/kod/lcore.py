# Long version (16:9) engine for "Deutschland im Zweiten Weltkrieg": the magazine of the Shorts, now lying open on a dark walnut
# desk under a lamp. A Book is a run of spreads with page turns and a camera (centre, scale) that glides between details;
# archive film runs full screen in between, graded, with grain, gate weave and a caption in the magazine's style.
import sys, os, math, json, functools, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
LB = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
S = os.path.dirname(LB.rstrip('/')) + '/'
sys.path.insert(0, S + 'serie/code'); sys.path.insert(0, LB + 'code')
import magazine as M
W, H, FPS = 1920, 1080, 30
PW, PH = 1400, 1810; SW = 2 * PW
M.PW, M.PH, M.SW = PW, PH, SW
from magazine import clamp, eio, eout, lerp, serif, sans, italic, stamp_ink, words_in, ink, poly, arc, hatch, strike_red, TXT, GREY, ACC
WORDS = json.load(open(LB + 'words.json')); OFF = 1.0          # one second of film before the narration starts
def wt(word, after=0.0):
    for w_, a, b in WORDS:
        if a + OFF >= after - 0.01 and w_.lower().startswith(word.lower()): return a + OFF
    raise KeyError(word)
def ws(word, after=0.0): return wt(word, after) - 0.04
def we(word, after=0.0):
    for w_, a, b in WORDS:
        if a + OFF >= after - 0.01 and w_.lower().startswith(word.lower()): return b + OFF
    raise KeyError(word)
VEND = WORDS[-1][2] + OFF
LIGHT = (215, 215, 215); PAPER = (249, 248, 245)
def fade_col(c, k, bg=249): return tuple(int(lerp(bg, v, k)) for v in c)

# ---------- page furniture ----------
def runhead(pg, left_side, page_no):
    d = ImageDraw.Draw(pg); x0, x1 = 110, PW - 110
    for k, c in enumerate((ACC, (150, 150, 150), (205, 205, 205))): d.ellipse((x0 + k * 34, 98, x0 + k * 34 + 22, 120), fill=c)
    d.text((x0 + 120, 109), 'CHRONIK DER MACHT', font=sans(28, 600), fill=GREY, anchor='lm')
    d.text((x1, 109), 'TEIL 1 · DER WEG IN DEN KRIEG', font=sans(28, 700), fill=ACC, anchor='rm')
    d.line((x0, 150, x1, 150), fill=LIGHT, width=2)
    d.text((x0 if left_side else x1, PH - 95), str(page_no), font=sans(30, 500), fill=GREY, anchor='lm' if left_side else 'rm')
@functools.lru_cache(None)
def base(n, left=True):
    pg = M.gloss(n).copy(); runhead(pg, left, n); return pg
def label(pg, t, t0, s, xy, font, col=TXT, anchor='la', dur=0.35, rise=14):
    if t < t0: return
    k = eout((t - t0) / dur); ImageDraw.Draw(pg).text((xy[0], xy[1] + (1 - k) * rise), s, font=font, fill=fade_col(col, k), anchor=anchor)
def halo(pg, t, t0, s, xy, font, col=TXT, anchor='mm', sw=6, dur=0.35):
    if t < t0: return
    k = eout((t - t0) / dur)
    ImageDraw.Draw(pg).text(xy, s, font=font, fill=fade_col(col, k), anchor=anchor, stroke_width=sw, stroke_fill=PAPER)
def rule(pg, t, t0, y, x0=110, x1=PW - 110, col=LIGHT, wd=2, dur=0.5):
    if t < t0: return
    ImageDraw.Draw(pg).line((x0, y, lerp(x0, x1, eout((t - t0) / dur)), y), fill=col, width=wd)
def strike(pg, t, t0, a_, b_, wd=9): strike_red(pg, t, t0, a_, b_, wd)
def body(pg, t, x, y, text, after, accent=(), bold=(), size=52, lh=72, maxw=1180):
    """narration words set in the body face, each fading in when spoken"""
    spec = []; a = after
    for w_ in text.split():
        key = w_.strip('.,:;')
        try: tw = wt(key, a); a = tw + 0.01
        except KeyError: tw = wt(key, after)
        st = 'a' if key in accent else 'b' if key in bold else 'n'; spec.append((w_, tw - 0.04, st))
    return words_in(pg, t, x, y, spec, lambda st: serif(size, 700 if st in 'ab' else 400), lh, maxw)
def stamp(pg, t, t0, s, xy, size=64, ang=-8, col=ACC):
    """a rubber stamp hits the page: framed capitals, uneven ink, slight rotation"""
    if t < t0: return
    u = clamp((t - t0) / 0.18); sc = lerp(1.35, 1.0, eout(u)); f = sans(int(size * sc), 800)
    tw = f.getlength(s); pad = size * 0.35; w_, h_ = int(tw + 2 * pad), int(size * sc * 1.5)
    L = Image.new('L', (w_ + 20, h_ + 20), 0); d = ImageDraw.Draw(L)
    d.rectangle((10, 10, w_ + 10, h_ + 10), outline=255, width=max(4, int(size * 0.09))); d.text(((w_ + 20) / 2, (h_ + 20) / 2), s, font=f, fill=255, anchor='mm')
    r = np.random.default_rng(len(s)); n = np.asarray(Image.fromarray((r.random((h_ // 3 + 8, w_ // 3 + 8)) * 255).astype(np.uint8)).resize(L.size, Image.BICUBIC), np.float32) / 255
    A = (np.asarray(L, np.float32) * (0.55 + 0.45 * n) * min(1, u * 2)).clip(0, 255).astype(np.uint8)
    A = Image.fromarray(A).rotate(ang, expand=True, resample=Image.BICUBIC)
    stamp_ink(pg, A, (xy[0] - A.width / 2, xy[1] - A.height / 2), col, 0.92)

# ---------- archive film ----------
@functools.lru_cache(None)
def clip_n(name): return len(os.listdir(LB + 'clips/' + name))
@functools.lru_cache(maxsize=24)
def clip_frame(name, i):
    i = max(1, min(clip_n(name), i)); im = Image.open(LB + 'clips/%s/f%04d.jpg' % (name, i)).convert('L')
    if name in TRIM: l, t_, r, b = TRIM[name]; im = im.crop((l, t_, im.width - r, im.height - b))
    return im
TRIM = {'hitler_b': (16, 6, 0, 0)}   # a scratch mark at the left edge of the speech film
def clip_at(name, ct): return clip_frame(name, int(ct * FPS) + 1)
def tone(g, warm=True):
    """grey film to a cool-neutral print with a hint of warmth in the highlights"""
    g = ImageEnhance.Contrast(g).enhance(1.12); a = np.asarray(g, np.float32) / 255
    rgb = np.stack([a * 238 + 10, a * 236 + 10, a * 228 + 12], -1) if warm else np.stack([a * 235 + 10] * 3, -1)
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8))
@functools.lru_cache(None)
def _grain_bank():
    r = np.random.default_rng(11); return [r.normal(0, 1, (H // 2, W // 2)).astype(np.float32).repeat(2, 0).repeat(2, 1)[..., None] for _ in range(12)]
def grain(i, amp): return _grain_bank()[i % 12] * amp
@functools.lru_cache(None)
def vignette(w=W, h=H, k=0.55):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    return np.clip(1 - k * np.clip(r - 0.45, 0, None) ** 1.6, 0, 1)[..., None]
def film(t, name, t0, start=0.0, speed=1.0, z0=1.02, z1=1.10, fx=0.5, fy=0.5, cap=None, cap2=None, t1=None):
    """full-screen archive film: slow push in, gate weave, flicker, grain, vignette, a caption bottom left"""
    ct = start + (t - t0) * speed; g = clip_at(name, ct); w, h = g.size
    z = lerp(z0, z1, clamp((t - t0) / 9.0)); cw = min(w, h * W / H) / z; ch = cw * H / W
    r = np.random.default_rng(int(t * FPS) + 7); jx, jy = r.normal(0, 0.35), r.normal(0, 0.35)
    x0 = (w - cw) * fx + jx; y0 = (h - ch) * fy + jy
    im = g.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).filter(ImageFilter.UnsharpMask(2, 60, 2))
    a = np.asarray(tone(im), np.float32) * (1 + 0.03 * math.sin(t * 23) + r.normal(0, 0.012))
    a = a * vignette() + grain(int(t * FPS) + 3, 6.5)
    img = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    if cap: caption(img, t, t0 + 0.5, cap, cap2, t1)
    return img
def caption(img, t, t0, s, s2=None, t1=None):
    """lower-left caption: red rule, place and date in small capitals, a second line in italics"""
    if t < t0: return
    k = eout((t - t0) / 0.5)
    if t1 is not None: k *= clamp((t1 - 0.15 - t) / 0.35)
    if k <= 0: return
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); x, y = 96, 920 - (40 if s2 else 0)
    d.rectangle((x, y, x + int(120 * k), y + 6), fill=ACC + (255,))
    d.text((x, y + 24), s.upper(), font=sans(34, 700), fill=(245, 243, 238, int(255 * k)))
    if s2: d.text((x, y + 72), s2, font=italic(30, 400), fill=(225, 222, 215, int(235 * k)))
    bb = L.getbbox()
    if not bb: return
    bx = (max(0, bb[0] - 20), max(0, bb[1] - 20), min(W, bb[2] + 20), min(H, bb[3] + 20)); Lc = L.crop(bx)
    sh = Image.new('RGBA', Lc.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, int(200 * k)), (0, 0), Lc.getchannel('A'))
    reg = img.crop(bx).convert('RGBA'); reg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), (2, 3)); reg.alpha_composite(Lc); img.paste(reg.convert('RGB'), bx[:2])
def photo(pg, t, t0, name, box, cap=None, start=0.0, speed=1.0, still=None, fx=0.5, fy=0.5):
    """archive film printed on the page: cover-cropped into the box, fades up from the paper, caption below"""
    if t < t0: return
    k = eout((t - t0) / 0.45); x0, y0, bw, bh = box
    g = still if still is not None else clip_at(name, start + (t - t0) * speed); w, h = g.size
    sc = max(bw / w, bh / h); cw, ch = bw / sc, bh / sc; cx0 = (w - cw) * fx; cy0 = (h - ch) * fy
    fr = tone(g.convert('L').resize((bw, bh), Image.LANCZOS, box=(cx0, cy0, cx0 + cw, cy0 + ch)))
    if k < 1: fr = Image.blend(Image.new('RGB', fr.size, PAPER), fr, k)
    pg.paste(fr, (int(x0), int(y0)))
    if cap:
        d = ImageDraw.Draw(pg); d.line((x0, y0 + bh + 26, x0 + 150, y0 + bh + 26), fill=ACC, width=5)
        d.text((x0, y0 + bh + 46), cap, font=italic(32), fill=fade_col(GREY, k))

# ---------- the magazine on the desk ----------
@functools.lru_cache(None)
def desk_tex():
    """dark walnut: long grain streaks, a few slow rings, fine pores"""
    r = np.random.default_rng(5); h, w = H * 2, W * 2
    s1 = np.asarray(Image.fromarray((r.random((h // 6, 24)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    s2 = np.asarray(Image.fromarray((r.random((h // 40, 8)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); ring = 0.5 + 0.5 * np.sin((yy + 60 * np.sin(xx / 700) + 140 * s2) / 23)
    pore = r.random((h, w)).astype(np.float32)
    v = 0.55 * s1 + 0.25 * ring + 0.12 * s2 + 0.08 * pore
    col = np.array([62, 42, 30], np.float32)[None, None] * (0.72 + 0.5 * v[..., None])
    return Image.fromarray(col.clip(0, 255).astype(np.uint8))
@functools.lru_cache(None)
def lamp():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((xx - W * 0.42) / (W * 0.75)) ** 2 + ((yy - H * 0.30) / (H * 0.95)) ** 2)) * 0.35 + 0.72
    return np.clip(g, 0, 1.08)[..., None] * np.array([1.0, 0.985, 0.95], np.float32)[None, None]
@functools.lru_cache(None)
def _spine(spine):
    g = (np.clip(1 - np.abs(np.arange(440) - 220) / 220, 0, 1) ** 2.2 * spine / 255).astype(np.float32); return g[None, :, None]
@functools.lru_cache(None)
def _alpha(hasL, hasR):
    m = Image.new('L', (SW, PH), 0); d = ImageDraw.Draw(m)
    if hasL: d.rectangle((0, 0, PW - 1, PH), fill=255)
    if hasR: d.rectangle((PW, 0, SW, PH), fill=255)
    return m
def spread_img(left, right, spine=110):
    """both pages side by side; the paper darkens where it curves into the spine"""
    can = Image.new('RGB', (SW, PH), (0, 0, 0))
    if left is not None: can.paste(left.convert('RGB'), (0, 0))
    if right is not None: can.paste(right.convert('RGB'), (PW, 0))
    g = _spine(spine); st = np.asarray(can.crop((PW - 220, 0, PW + 220, PH)), np.float32)
    can.paste(Image.fromarray((st * (1 - g) + np.array([20, 20, 24], np.float32) * g).astype(np.uint8)), (PW - 220, 0))
    can.putalpha(_alpha(left is not None, right is not None)); return can
def view(sp, cx, cy, s, ang, t):
    a = math.radians(ang); ca, sa = math.cos(a) / s, math.sin(a) / s
    co = (ca, sa, cx - ca * W / 2 - sa * H / 2, -sa, ca, cy + sa * W / 2 - ca * H / 2)
    # only the part of the spread the camera sees is resampled
    xs = [co[0] * x + co[1] * y + co[2] for x, y in ((0, 0), (W, 0), (0, H), (W, H))]; ys = [co[3] * x + co[4] * y + co[5] for x, y in ((0, 0), (W, 0), (0, H), (W, H))]
    bx0, by0 = max(0, int(min(xs)) - 4), max(0, int(min(ys)) - 4); bx1, by1 = min(sp.width, int(max(xs)) + 5), min(sp.height, int(max(ys)) + 5)
    if bx1 > bx0 and by1 > by0:
        sp = sp.crop((bx0, by0, bx1, by1)); co = (co[0], co[1], co[2] - bx0, co[3], co[4], co[5] - by0)
    v = sp.transform((W, H), Image.AFFINE, co, Image.BILINEAR if s >= 1.0 else Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    ox = int((cx * s * 0.5) % W); oy = int((cy * s * 0.5) % H)
    can = desk_tex().crop((ox, oy, ox + W, oy + H)).convert('RGBA')
    al = v.getchannel('A').resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(2, 7 * s))).resize((W, H), Image.BILINEAR)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((8, 5, 3, 170), (int(18 * s), int(26 * s)), al); can.alpha_composite(sh); can.alpha_composite(v)
    a_ = np.asarray(can.convert('RGB'), np.float32) * lamp() * vignette(k=0.42)
    a_ += grain(int(t * FPS), 2.2)
    return Image.fromarray(a_.clip(0, 255).astype(np.uint8))
class Book:
    """spreads: [(left_fn|None, right_fn|None)], turns: start time of each turn (dur TD), cams: [(t, cx, cy, s)] eased over CD"""
    TD, CD = 0.95, 1.0
    def __init__(self, spreads, turns, cams, ang=-1.2, spine=110):
        self.sp, self.turns, self.cams, self.ang, self.spine = spreads, turns, cams, ang, spine
    def spread(self, t, need=(True, True)):
        k = sum(1 for a in self.turns if t >= a + self.TD)
        for i, a in enumerate(self.turns):
            if a <= t < a + self.TD:
                L0, R0 = self.sp[i]; L1, R1 = self.sp[i + 1]
                base_ = spread_img(L0(t) if L0 else None, R1(t) if R1 else None, self.spine)
                return M.turn(base_, R0(t), L1(t), (t - a) / self.TD)
        L, R = self.sp[k]; return spread_img(L(t) if (L and need[0]) else None, R(t) if (R and need[1]) else None, self.spine)
    def cam(self, t):
        p = self.cams[0][1:4]
        for c in self.cams[1:]:
            if t < c[0]: break
            cd = c[4] if len(c) > 4 else self.CD
            u = eio((t - c[0]) / cd); p = tuple(lerp(x, y, u) for x, y in zip(p, c[1:4]))
        return p
    def __call__(self, t):
        cx, cy, s = self.cam(t); s *= 1 + 0.012 * math.sin(t * 0.11)          # a very slow breathing of the camera
        half = math.hypot(W, H) / 2 / s + 10; need = (cx - half < PW, cx + half > PW)
        return view(self.spread(t, need), cx, cy, s, self.ang + 0.25 * math.sin(t * 0.21), t)
def blend(a, b, u): return Image.blend(a, b, clamp(u))
