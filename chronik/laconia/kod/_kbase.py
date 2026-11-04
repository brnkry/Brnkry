# ---------- scenes ----------
TOP = 330
def FV(k, a=0.0, ov=None, z1=1.06, fx=0.5, fy=0.5, sat=0.9):
    """archive film spread over the full 9:16 frame: a vertical slice around fx, slow push-in"""
    def fn(t, w0, w1):
        im = fat(k, a + max(0.0, t - w0)); z = lerp(1.0, z1, prog(t, w0, w1))
        ch = im.height / z; cw = ch * 9 / 16
        x0 = min(max(fx * im.width - cw / 2, 0), im.width - cw); y0 = min(max(fy * im.height - ch / 2, 0), im.height - ch)
        can = grade(im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA'), 0.1, sat); shade(can, 200, 0.55); can.alpha_composite(TOPSH)
        if ov: ov(can, t, w0, w1)
        return can
    return fn
def see(can, fn_, a=0.9):
    """semi-transparent overlay: draw onto an empty layer, then lay it over the running film"""
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn_(L)
    if a < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
    can.alpha_composite(L)
def curl(can, t, t0, cx, cy, r, col=YEL, dur=0.45):
    """a curved arrow turning half way round a point (a sign being turned)"""
    if t < t0: return
    u = eio((t - t0) / dur); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    a0, a1 = -150, -150 + 200 * u; pts = [(cx + r * math.cos(math.radians(a)), cy + r * 0.45 * math.sin(math.radians(a))) for a in np.linspace(a0, a1, 40)]
    d.line(pts, fill=(0, 0, 0, 150), width=22, joint='curve'); d.line(pts, fill=col + (255,), width=14, joint='curve')
    e, q = pts[-1], pts[-4]; ang = math.atan2(e[1] - q[1], e[0] - q[0]); hd = 46
    d.polygon([(e[0] + 14 * math.cos(ang), e[1] + 14 * math.sin(ang)), (e[0] - hd * math.cos(ang - .5), e[1] - hd * math.sin(ang - .5)), (e[0] - hd * math.cos(ang + .5), e[1] - hd * math.sin(ang + .5))], fill=col + (255,))
    can.alpha_composite(L)

def underlined(can, t, t0, s_, y, size, col=CREAM, ucol=RED, x=CX):
    """straight title, a bar wipes in under it"""
    if t < t0: return
    title(can, t, t0, s_, y, size, col, None, 'anton', x, 900, 1)
    w_ = anton(size).getlength(s_); u = eio((t - t0 - 0.15) / 0.35)
    if u > 0:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); y0 = y + size * 0.62
        d.rectangle((x - w_ / 2 + 3, y0 + 4, x - w_ / 2 + w_ * u + 3, y0 + 18), fill=(0, 0, 0, 120)); d.rectangle((x - w_ / 2, y0, x - w_ / 2 + w_ * u, y0 + 14), fill=ucol + (255,)); can.alpha_composite(L)
def sliced(can, t, t0, s_, xy, size, col=CREAM):
    """a straight word that is cut through: a thin red line runs across, then the top half slides off"""
    if t < t0: return
    f = anton(size); bb = f.getbbox(s_); w_, h_ = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    L = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); ImageDraw.Draw(L).text((20 - bb[0], 20 - bb[1]), s_, font=f, fill=col + (255,))
    k = eout((t - t0) / 0.3); L.putalpha(L.getchannel('A').point(lambda v: int(v * k)))
    cy = h_ // 2; top, bot = L.crop((0, 0, w_, cy)), L.crop((0, cy, w_, h_)); sh = eout((t - t0 - 0.45) / 0.3) * 26
    O = Image.new('RGBA', (w_ + 60, h_ + 20), (0, 0, 0, 0)); O.alpha_composite(top, (int(30 + sh), int(10 - sh * 0.25))); O.alpha_composite(bot, (30, cy + 10))
    S = Image.new('RGBA', O.size, (0, 0, 0, 0)); S.paste((0, 0, 0, 200), (0, 0), O.getchannel('A'))
    x, y = int(xy[0] - O.width / 2), int(xy[1] - O.height / 2); can.alpha_composite(S.filter(ImageFilter.GaussianBlur(8)), (x + 3, y + 7)); can.alpha_composite(O, (x, y))
    u = eio((t - t0 - 0.2) / 0.25)
    if u > 0:
        D = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(D).line((x + 10, y + cy + 10, x + 10 + (O.width - 20) * u, y + cy + 10), fill=RED + (255,), width=6); can.alpha_composite(D)
def asks(can, t, t0, s_, y, size, col=CREAM):
    """straight word, a big yellow question mark drops in after it and keeps bouncing"""
    if t < t0: return
    f = anton(size); w_ = f.getlength(s_); q = anton(int(size * 1.35)); wq = q.getlength('?'); x = CX - (w_ + wq + 16) / 2
    title(can, t, t0, s_, y, size, col, None, 'anton', x + w_ / 2, 900, 1)
    tq = t0 + 0.3
    if t > tq:
        k = eout((t - tq) / 0.3); bo = -(1 - k) * 120 - abs(math.sin((t - tq) * 4.0)) * 14 * k
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).text((x + w_ + 16 + wq / 2, y - 6 + bo), '?', font=q, fill=YEL + (int(255 * k),), anchor='mm')
        S = Image.new('RGBA', (W, H), (0, 0, 0, 0)); S.paste((0, 0, 0, 200), (0, 0), L.getchannel('A')); can.alpha_composite(S.filter(ImageFilter.GaussianBlur(8)), (3, 7)); can.alpha_composite(L)
def crossed(can, t, t0, s_, y, size, note, col=CREAM):
    """the word, a red line through it, and the correction written above by hand"""
    if t < t0: return
    title(can, t, t0, s_, y, size, col, None, 'anton', CX, 900, 1)
    w_ = anton(size).getlength(s_); strike(can, t, t0 + 0.2, (CX - w_ / 2, y - size * 0.45, CX + w_ / 2, y + size * 0.35), RED, 12, 0.3)
    hand(can, t, t0 + 0.45, note, (CX - w_ / 2 + 20, y - size * 1.2), 96, RED, 0.4)
def pwfield(can, t, t0, y, ok_t):
    """a sentry's challenge as an input field: the cursor blinks, the answer stays empty, a red question mark follows"""
    if t < t0: return
    k = eout((t - t0) / 0.3); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, x1 = 150, 930; d.rounded_rectangle((x0, y - 70, x1, y + 70), 18, fill=(10, 11, 14, int(170 * k)), outline=YEL + (int(230 * k),), width=4)
    d.text((x0 + 36, y), 'PASSWORT:', font=bebas(84), fill=CREAM + (int(255 * k),), anchor='lm')
    fx = x0 + 36 + bebas(84).getlength('PASSWORT:') + 26
    for i in range(4): d.rectangle((fx + i * 70, y + 26, fx + i * 70 + 46, y + 32), fill=GREY + (int(220 * k),))
    if t < ok_t and int((t - t0) * 2.6) % 2 == 0: d.rectangle((fx, y - 34, fx + 6, y + 22), fill=YEL + (int(255 * k),))
    if t >= ok_t: d.text((fx + 2 * 70 + 23, y - 2), '?', font=anton(110), fill=RED + (int(255 * eout((t - ok_t) / 0.25)),), anchor='mm')
    can.alpha_composite(L)
def verdict(can, t, t0, s_, y, size, col=YEL):
    """two thin lines open from the middle, the word settles between them"""
    if t < t0: return
    u = eio((t - t0) / 0.4); w_ = anton(size).getlength(s_) + 60; L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for yy in (y - size * 0.72, y + size * 0.62):
        d.rectangle((CX - w_ / 2 * u, yy, CX + w_ / 2 * u, yy + 5), fill=CREAM + (235,))
    can.alpha_composite(L); title(can, t, t0 + 0.2, s_, y, size, col, None, 'anton', CX, 960, 1)

