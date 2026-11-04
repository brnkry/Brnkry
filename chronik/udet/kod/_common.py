# helpers shared with the Bader shorts
def arrow_to(can, a, b, u, col=YEL, w_=14, head=44):
    if u <= 0: return
    e = (lerp(a[0], b[0], u), lerp(a[1], b[1], u)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line((a, e), fill=(0, 0, 0, 150), width=w_ + 8); d.line((a, e), fill=col + (255,), width=w_)
    d.polygon([(e[0] + 12 * math.cos(ang), e[1] + 12 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))], fill=col + (255,))
    can.alpha_composite(L)
def ringp(can, t, t0, x, y, r, col=YEL, label=None, ly=None, size=58):
    """a circle drawn round a face, with its name under or over it"""
    if t < t0: return
    u = eio((t - t0) / 0.45); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for wd, c in ((14, (0, 0, 0, 140)), (8, col + (255,))): d.arc((x - r, y - r, x + r, y + r), -90, -90 + 360 * u, fill=c, width=wd)
    can.alpha_composite(L)
    if label and 120 < x < 960: title(can, t, t0 + 0.2, label, ly if ly is not None else y + r + 50, size, col, None, 'bebas', x)   # the name stays with the face
def rquad(cx, cy, s_, h, ang, font=None):
    """quad (source coords) for s_ with its true aspect, h high, centred on (cx, cy), turned by ang degrees (along a slanted surface)"""
    f = font or anton(200); bb = f.getbbox(s_); w = h * (bb[2] - bb[0] + 20) / (bb[3] - bb[1] + 20); a = math.radians(ang)
    ux, uy, vx, vy = math.cos(a) * w / 2, math.sin(a) * w / 2, -math.sin(a) * h / 2, math.cos(a) * h / 2
    return [(cx - ux - vx, cy - uy - vy), (cx + ux - vx, cy + uy - vy), (cx + ux + vx, cy + uy + vy), (cx - ux + vx, cy - uy + vy)]
def tquad(cx, cy, s_, h, font=None, tilt=0.0):
    """quad (source coords) for s_ with its true aspect, h high, centred on (cx, cy); tilt lifts the right end"""
    f = font or anton(200); bb = f.getbbox(s_); w = h * (bb[2] - bb[0] + 20) / (bb[3] - bb[1] + 20)
    return [(cx - w / 2, cy - h / 2 + tilt), (cx + w / 2, cy - h / 2 - tilt), (cx + w / 2, cy + h / 2 - tilt), (cx - w / 2, cy + h / 2 + tilt)]
def night(can, k=1.0):
    rgb = can.convert('RGB'); n = Image.blend(rgb, ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(0.3)).enhance(0.45), k)
    return Image.blend(n, Image.new('RGB', (W, H), (18, 30, 58)), 0.28 * k).convert('RGBA')
def typed(can, t, t0, s_, y, size=120, col=CREAM, step=0.075, x=CX, t1=None, font=None):
    """letters arrive one by one (flat, centred)"""
    if t < t0 or (t1 is not None and t > t1 + 0.25): return
    f = font or anton(size); a = 1.0 if t1 is None else 1 - clamp((t - t1) / 0.25)
    tw_ = f.getlength(s_); xx = x - tw_ / 2
    for i, ch in enumerate(s_):
        k = eout((t - t0 - i * step) / 0.18)
        if k > 0 and ch != ' ':
            sp = _spr(ch, 'anton', f.size, col) if font is None else None
            if sp is not None:
                sp = sp.copy(); sp.putalpha(sp.getchannel('A').point(lambda v: int(v * k * a)))
                can.alpha_composite(sp, (int(xx - 40 + f.getbbox(ch)[0]), int(y - sp.height / 2 + (1 - k) * 18)))
        xx += f.getlength(ch)
