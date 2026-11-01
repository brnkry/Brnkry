
# ---------- text helpers shared with the Kretschmer short: italic Anton, popping and sliding numbers ----------
def _ital(s_, size, col, bold=1, shear=0.22):
    sp = _spr(s_, 'anton', size, col, bold); w_, h_ = sp.size
    return sp.transform((int(w_ + h_ * shear), h_), Image.AFFINE, (1, shear, -h_ * shear, 0, 1, 0), Image.BICUBIC)
def ititle(can, t, t0, s_, y, size, col=CREAM, x=CX, maxw=900, slide=80):
    """the same Anton, set in italics, sliding in from the left"""
    if t < t0: return
    while anton(size).getlength(s_) > maxw and size > 24: size -= 4
    k = eout((t - t0) / 0.4); sp = _ital(s_, size, col)
    if k < 1: sp = sp.copy(); sp.putalpha(sp.getchannel('A').point(lambda v: int(v * k)))
    can.alpha_composite(sp, (int(x - sp.width / 2 - (1 - k) * slide), int(y - sp.height / 2)))
def popnum(can, t, t0, a, b, y, size, col=YEL, dur=0.8, x=CX):
    """a number counting up while it drops in large and settles with a small bounce"""
    if t < t0: return
    u = clamp((t - t0) / dur); v = int(round(lerp(a, b, eout(u)))); sc = 1.0 + 0.7 * (1 - eout(clamp((t - t0) / 0.45))) - 0.08 * math.sin(math.pi * clamp((t - t0 - 0.3) / 0.35))
    sp = _spr('{:,}'.format(v).replace(',', '.'), 'anton', size, col, 2); sp = sp.resize((max(1, int(sp.width * sc)), max(1, int(sp.height * sc))), Image.BICUBIC)
    k = clamp((t - t0) / 0.2)
    if k < 1: sp.putalpha(sp.getchannel('A').point(lambda q: int(q * k)))
    can.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height / 2)))
def inum(can, t, t0, a, b, y, size, col=CREAM, dur=1.4, x=CX):
    """a number counting up in italics, sliding in"""
    if t < t0: return
    v = int(round(lerp(a, b, eout((t - t0) / dur)))); s_ = '{:,}'.format(v).replace(',', '.')
    k = eout((t - t0) / 0.35); sp = _ital(s_, size, col, 2)
    if k < 1: sp = sp.copy(); sp.putalpha(sp.getchannel('A').point(lambda q: int(q * k)))
    can.alpha_composite(sp, (int(x - sp.width / 2 + (1 - k) * 120), int(y - sp.height / 2)))
def counter(can, t, t0, a, b, y, size, col=YEL, dur=0.9, fmt='{:,}', x=CX):
    """a number counting up, straight, with the channel shadow"""
    if t < t0: return
    v = int(round(lerp(a, b, eout((t - t0) / dur)))); s_ = fmt.format(v).replace(',', '.')
    title(can, t, t0, s_, y, size, col, None, 'anton', x, 900, 1)

