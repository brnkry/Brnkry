
# ---------- full-screen vertical archive film (the old footage is already 9:16) ----------
def V9(k, a, z0=1.0, z1=1.06, ov=None, sh=200, warm=0.06, sat=0.9, k2=None, d1=None):   # k2: a second archive shot that follows after d1 s
    def fn(t, w0, w1):
        tt = a + max(0.0, t - w0); im = fat(k2, tt - d1) if k2 and tt >= d1 else fat(k, tt); z = lerp(z0, z1, eio(prog(t, w0, w1))); cw, ch = im.width / z, im.height / z
        box = _cover((cw, ch), 9 / 16); x0 = (im.width - cw) / 2 + box[0]; y0 = (im.height - ch) / 2 + box[1]
        can = grade(im.resize((W, H), Image.BICUBIC, box=(max(0, x0), max(0, y0), min(im.width, x0 + box[2] - box[0]), min(im.height, y0 + box[3] - box[1]))).convert('RGBA'), warm, sat); shade(can, sh, 0.55)
        can.alpha_composite(TOPSH)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
def BG(k, a, dimv=70, bl=1.6):
    def fn(t, w0):
        im = fat(k, a + max(0.0, t - w0))
        sm = im.resize((360, 640), Image.BILINEAR, box=_cover(im.size, 9 / 16)).filter(ImageFilter.GaussianBlur(bl)).resize((W, H), Image.BICUBIC)
        can = grade(sm.convert('RGBA'), 0.1, 0.85); dim(can, dimv); return can
    return fn
def arrow_at(can, t, t0, tip, frm, col=YEL, w_=14, head=46, lab=None, lab_xy=None):
    """arrow drawn from frm to tip, label written at its tail"""
    if t < t0: return
    u = eio((t - t0) / 0.35); e = (lerp(frm[0], tip[0], u), lerp(frm[1], tip[1], u)); ang = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line((frm, e), fill=(0, 0, 0, 160), width=w_ + 8); d.line((frm, e), fill=col + (255,), width=w_)
    hp = [(e[0] + 14 * math.cos(ang), e[1] + 14 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))]
    d.polygon(hp, fill=col + (255,)); can.alpha_composite(L)
    if lab: title(can, t, t0 + 0.15, lab, lab_xy[1], 66, col, None, 'anton', lab_xy[0], 900)
def ring_at(can, t, t0, x, y, col=RED, r=44):
    if t < t0: return
    k = eout((t - t0) / 0.35); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for j in range(2):
        uu = ((t - t0) * 0.8 + j / 2) % 1.0; rr = r + 60 * uu; d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=col + (int(170 * (1 - uu) * k),), width=5)
    d.ellipse((x - r * k, y - r * k, x + r * k, y + r * k), outline=col + (255,), width=8); can.alpha_composite(L)
def photo_card(n, box, t, w0, w1, bgk, bga, z1=1.06, py=PY, pw=PW, ph=PH, dimbg=80):
    """a photo in a cream-edged panel over the blurred running film; returns the canvas and a source -> screen mapper"""
    can = BG(bgk, bga, dimbg)(t, w0); im = src(n).crop(box); z = lerp(1.0, z1, prog(t, w0, w1))
    cw, ch = im.width / z, im.height / z; x0, y0 = (im.width - cw) / 2, (im.height - ch) / 2
    pn = grade(im.resize((pw, ph), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA'), 0.08, 0.95)
    x, y = (W - pw) // 2, py - ph // 2
    sh = Image.new('RGBA', (pw + 60, ph + 60), (0, 0, 0, 0)); sh.putalpha(Image.new('L', (pw + 60, ph + 60), 150).filter(ImageFilter.GaussianBlur(20)))
    can.alpha_composite(sh, (x - 24, y - 14)); ImageDraw.Draw(can).rectangle((x - 8, y - 8, x + pw + 7, y + ph + 7), fill=CREAM + (255,)); can.alpha_composite(pn, (x, y))
    sx, sy = pw / cw, ph / ch
    return can, (lambda X, Y: (x + (X - box[0] - x0) * sx, y + (Y - box[1] - y0) * sy))

