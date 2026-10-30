# ================= shared helpers =================
def ws(word, after=0.0): return wt(word, after) - 0.05

# ---------- archive films: shown in a framed panel over a blurred copy of themselves ----------
SEG = {k: len(os.listdir(B + 'clip/' + k)) for k in os.listdir(B + 'clip')}
CROP = {}   # the clips were already cut to a 3:4 window around the subject in prep.py
def _soft(im, x, y, d):
    r = d / 2; bx = (int(x - d), int(y - d), int(x + d), int(y + d)); reg = im.crop(bx)
    bl = reg.resize((max(1, reg.width // 8), max(1, reg.height // 8)), Image.BILINEAR).resize(reg.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(d * 0.12))
    mk = Image.new('L', reg.size, 0); c = reg.width / 2; ImageDraw.Draw(mk).ellipse((c - r, c - r, c + r, c + r), fill=255)
    im.paste(Image.composite(bl, reg, mk.filter(ImageFilter.GaussianBlur(r * 0.2))), bx[:2])
@functools.lru_cache(maxsize=24)
def ff(k, i):
    i = max(1, min(SEG[k], i)); im = Image.open(B + 'clip/%s/%05d.jpg' % (k, i)).convert('RGB')
    if k in CROP: return im.crop(CROP[k])
    if k.startswith('o_'):   # some archive shots are a landscape band inside the vertical frame, with a blurred fill above and below: keep only the band
        r = np.asarray(im.convert('L'), np.float32).mean(1); dv = np.abs(np.diff(r))
        top = int(np.argmax(dv[100:960])) + 100; bot = int(np.argmax(dv[960:1820])) + 960
        if dv[top] > 25 and dv[bot] > 25: return im.crop((0, top + 4, im.width, bot - 4))
    return im
def fat(k, ct): return ff(k, int(ct * 25) + 1)   # all clips were extracted at their native 25 fps
PW, PH, PY = 1000, 750, 860
@functools.lru_cache(maxsize=8)
def _panelmask():
    m = Image.new('L', (PW + 120, PH + 120), 0); ImageDraw.Draw(m).rectangle((60, 60, 60 + PW, 60 + PH), fill=255); return m.filter(ImageFilter.GaussianBlur(22))
def card(im, t, w0, w1, z0=1.0, z1=1.06, fx=0.5, fy=0.5, warm=0.12, py=PY):
    """picture in a cream-edged panel, the same picture blurred and darkened behind it, slow push-in"""
    sm = im.resize((54, 96), Image.BILINEAR, box=_cover(im.size, 9 / 16)).filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BICUBIC)
    can = Image.blend(sm, Image.new('RGB', (W, H), (8, 9, 11)), 0.6).convert('RGBA')
    z = lerp(z0, z1, eio(prog(t, w0, w1))); cw, ch = im.width / z, im.width / z * PH / PW
    if ch > im.height / z: ch = im.height / z; cw = ch * PW / PH
    x0 = min(max(fx * im.width - cw / 2, 0), im.width - cw); y0 = min(max(fy * im.height - ch / 2, 0), im.height - ch)
    pn = grade(im.resize((PW, PH), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA'), warm, 0.85)
    pn = pn.filter(ImageFilter.UnsharpMask(2, 60, 2))
    sh = Image.new('RGBA', (PW + 120, PH + 120), (0, 0, 0, 0)); sh.putalpha(_panelmask().point(lambda v: int(v * 0.85)))
    x, y = (W - PW) // 2, py - PH // 2; can.alpha_composite(sh, (x - 60 + 6, y - 60 + 14))
    d = ImageDraw.Draw(can); d.rectangle((x - 8, y - 8, x + PW + 7, y + PH + 7), fill=CREAM + (255,)); can.alpha_composite(pn, (x, y))
    return can
def _cover(sz, asp):
    w, h = sz
    if w / h > asp: cw = h * asp; return ((w - cw) / 2, 0, (w + cw) / 2, h)
    ch = w / asp; return (0, (h - ch) / 2, w, (h + ch) / 2)
def FL(k, a, rate=1.0, z0=1.0, z1=1.06, fx=0.5, fy=0.5, ov=None):
    def fn(t, w0, w1):
        can = card(fat(k, a + max(0.0, t - w0) * rate), t, w0, w1, z0, z1, fx, fy)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
TOPSH = Image.new('RGBA', (W, H), (6, 7, 9, 0)); TOPSH.putalpha(Image.fromarray(np.repeat((np.clip((520 - np.arange(H)) / 400, 0, 1) ** 1.3 * 170).astype(np.uint8)[:, None], W, 1)))
def S_(n, sxa, sxb, z1=1.05, ov=None, sh=200):
    def fn(t, w0, w1):
        can, m = side(n, sxa, sxb, t, w0, w1, z1); shade(can, sh, 0.55); can.alpha_composite(TOPSH)
        if ov: ov(can, t, w0, w1, m)
        return can
    return fn

def paint(can, t, t0, quad, s_, size, col, font=None, dur=0.5, mod=0.45, op=0.9, glow=((8, 9, 12), 10, 0.55), t1=None):
    """words painted on a surface of the photo, wiped in left to right"""
    if t <= t0: return
    a = clamp((t - t0) / 0.06) * (1.0 if t1 is None else 1 - clamp((t - t1) / 0.3))
    on_quad(can, quad, s_, size, a, col, font or anton(size), eio((t - t0) / dur), 0.8, mod=mod, op=op, glow=glow)
# ---------- paper ----------
def newsprint(name, w_=700, sub=None, seed=1):
    """a newspaper front page: masthead, rule, grey column blocks"""
    h_ = int(w_ * 0.62); L = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((0, 0, w_ - 1, h_ - 1), fill=(232, 226, 210, 255), outline=(170, 160, 140, 255), width=2)
    f = playfair(10, 800); sz = 10
    while playfair(sz + 4, 800).getlength(name) < w_ - 90 and sz < 130: sz += 4
    d.text((w_ / 2, 34 + sz * 0.55), name, font=playfair(sz, 800), fill=(22, 20, 18, 255), anchor='mm')
    y = 48 + sz * 1.1; d.line((30, y, w_ - 30, y), fill=(30, 28, 26, 255), width=4); d.line((30, y + 8, w_ - 30, y + 8), fill=(30, 28, 26, 255), width=1)
    if sub: d.text((w_ / 2, y + 30), sub, font=oswald(26, 500), fill=(60, 56, 50, 255), anchor='mm')
    rng = np.random.default_rng(seed); y0 = y + 60; cols = 3; cw = (w_ - 60 - 2 * 24) / cols
    d.rectangle((30, y0, w_ - 30, y0 + 22), fill=(70, 66, 60, 255))
    for c in range(cols):
        x = 30 + c * (cw + 24); yy = y0 + 42
        while yy < h_ - 30:
            d.line((x, yy, x + cw * rng.uniform(0.7, 1.0), yy), fill=(150, 144, 132, 255), width=5); yy += 15
    a = np.asarray(L.getchannel('A')).astype(np.float32) * (0.93 + 0.07 * (rng.random((h_, w_)) > 0.5)); L.putalpha(Image.fromarray(a.astype(np.uint8)))
    return L
@functools.lru_cache(maxsize=16)
def _np(name, w_, sub, seed): return newsprint(name, w_, sub, seed)
def drop(can, t, t0, name, xy, rot=-4, w_=700, sub=None, seed=1):
    """a front page dropped onto the pile: falls in large, settles with a small bounce"""
    if t < t0: return
    k = eout((t - t0) / 0.3); P_ = _np(name, w_, sub, seed).rotate(rot + (1 - k) * 8, expand=True, resample=Image.BICUBIC)
    sc = lerp(1.35, 1.0, k); P_ = P_.resize((int(P_.width * sc), int(P_.height * sc)), Image.BICUBIC)
    if k < 1: P_.putalpha(P_.getchannel('A').point(lambda v: int(v * min(1, k * 1.6))))
    sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.7)))
    x, y = int(xy[0] - P_.width / 2), int(xy[1] - P_.height / 2); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (x + 8, y + 18)); can.alpha_composite(P_, (x, y))
def sheet(can, t, t0, lines, cx=CX, cy=900, w_=900, rot=-2.0):
    """typed sheet; lines = [(text, size, colour, t_start)], each line typed fast from its own time"""
    if t < t0: return
    k = eout((t - t0) / 0.45); h_ = 110 + sum(sz * 1.55 for _, sz, _, _ in lines)
    L = Image.new('RGBA', (int(w_), int(h_)), (226, 216, 192, 255)); d = ImageDraw.Draw(L); d.rectangle((0, 0, w_ - 1, h_ - 1), outline=(150, 135, 105, 255), width=3)
    y = 60
    for s_, sz, col, ts in lines:
        n = 0 if t < ts else min(len(s_), int((t - ts) / 0.022) + 1)
        f = shrink(typew(sz), s_, w_ - 80); d.text((w_ / 2, y + sz * 0.5), s_[:n], font=f, fill=col + (255,), anchor='mm'); y += sz * 1.55
    L = L.rotate(rot, expand=True, resample=Image.BICUBIC)
    if k < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * k)))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); sh.putalpha(L.getchannel('A').point(lambda v: int(v * 0.6)))
    x, y = int(cx - L.width / 2), int(cy - L.height / 2 + (1 - k) * 90); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (x + 6, y + 16)); can.alpha_composite(L, (x, y))
    return (x, y)

