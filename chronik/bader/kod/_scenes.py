
# ================= Douglas Bader scenes =================
def ws(word, after=0.0): return wt(word, after) - 0.05
def fr(ct): return cframe(int(round(ct * FPS)) + 1)
FULL, BOX = (0, 1920), (250, 1665)   # picture width of the full-frame shots and of the 4:3 newsreel shots (1920 coords)
def film(ct, cx, cy=540, z=1.0, sat=1.0, warm=0.14, pic=BOX, night=0.0):
    """9:16 window into the archive film (1920x1080 coords) kept inside the picture (no black side bars); returns canvas and a film->screen mapper"""
    im = fr(ct); S = im.width / 1920; ch = 1080 / z; cw = ch * W / H
    x0 = min(max(cx - cw / 2, pic[0] + 4), pic[1] - 4 - cw); y0 = min(max(cy - ch / 2, 0), 1080 - ch)
    can = grade(im.resize((W, H), Image.BICUBIC, box=(x0 * S, y0 * S, (x0 + cw) * S, (y0 + ch) * S)).convert('RGBA'), warm, sat); shade(can, 200, 0.55)
    return can, (lambda x, y: ((x - x0) * W / cw, (y - y0) * H / ch))
def arrow_to(can, a, b, u, col=YEL, w_=14, head=44):
    if u <= 0: return
    e = (lerp(a[0], b[0], u), lerp(a[1], b[1], u)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line((a, e), fill=(0, 0, 0, 150), width=w_ + 8); d.line((a, e), fill=col + (255,), width=w_)
    d.polygon([(e[0] + 12 * math.cos(ang), e[1] + 12 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))], fill=col + (255,))
    can.alpha_composite(L)
def chute(can, x, y, s=1.0, a=1.0, sway=0.0, q=False):
    """a small crate under a parachute, drawn in cream with a dark edge; q puts a question mark on the crate"""
    if a <= 0: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); A = int(255 * a); r = 70 * s; cy = y - 150 * s
    for wd, c in ((7, (10, 10, 12, int(170 * a))), (3, CREAM + (A,))):
        d.pieslice((x - r + sway, cy - r * 0.8, x + r + sway, cy + r * 0.8), 180, 360, fill=None if wd == 3 else c, outline=c, width=wd)
        for k in (-1, -0.35, 0.35, 1):
            d.line((x + sway + k * r, cy, x + k * 14 * s, y - 22 * s), fill=c, width=max(2, wd - 4))
    d.pieslice((x - r + sway + 3, cy - r * 0.8 + 3, x + r + sway - 3, cy + r * 0.8 - 3), 180, 360, fill=CREAM + (int(215 * a),))
    d.rectangle((x - 26 * s, y - 24 * s, x + 26 * s, y + 24 * s), fill=(150, 116, 70, A), outline=(10, 10, 12, A), width=4)
    if q: d.text((x, y + 2), '?', font=anton(int(40 * s)), fill=CREAM + (A,), anchor='mm')
    can.alpha_composite(L)
def ringp(can, t, t0, x, y, r, col=YEL, label=None, ly=None, size=58):
    """a circle drawn round a face, with its name under or over it"""
    if t < t0: return
    u = eio((t - t0) / 0.45); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for wd, c in ((14, (0, 0, 0, 140)), (8, col + (255,))): d.arc((x - r, y - r, x + r, y + r), -90, -90 + 360 * u, fill=c, width=wd)
    can.alpha_composite(L)
    if label and 120 < x < 960: title(can, t, t0 + 0.2, label, ly if ly is not None else y + r + 50, size, col, None, 'bebas', x)   # the name stays with the face
def paper(can, t, w0, w1, lines_, top=360, pw=780, ph=760, rot=-1.2):
    """a typed message on a sheet of paper, lines typed in at their own times"""
    k0 = eout((t - w0 - 0.05) / 0.45); L = Image.new('RGBA', (pw + 60, ph + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((30, 30, 30 + pw, 30 + ph), fill=(232, 227, 212, 255)); d.rectangle((30, 30, 30 + pw, 30 + ph), outline=(150, 140, 120, 255), width=3)
    y = 110
    for s_, sz, ts, col in lines_:
        if sz:
            n = max(0, min(len(s_), int((t - ts) / 0.025))); d.text((30 + pw / 2, y), s_[:n], font=typew(sz), fill=col + (255,), anchor='mm')
        y += (sz or 24) * 1.75
    L = L.rotate(rot, expand=True, resample=Image.BICUBIC)
    if k0 < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * k0)))
    sc = lerp(1.0, 1.04, prog(t, w0, w1)); L = L.resize((int(L.width * sc), int(L.height * sc)), Image.BICUBIC)
    sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (int(CX - L.width / 2 + 14), int(top + 22)), L.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    can.alpha_composite(L, (int(CX - L.width / 2), int(top + (1 - k0) * 40)))
def film_fit(ct, cy=760, wscale=1.0):
    """the whole 16:9 frame across the screen (no crop into the face), the empty space above and below filled with a blurred copy"""
    im = fr(ct).convert('RGB'); bg = im.resize((int(H * 16 / 9), H), Image.BILINEAR); x0 = (bg.width - W) // 2
    bg = bg.crop((x0, 0, x0 + W, H)).filter(ImageFilter.GaussianBlur(28)); bg = ImageEnhance.Brightness(bg).enhance(0.55)
    fw = int(W * wscale); fh = int(fw * 9 / 16); fg = im.resize((fw, fh), Image.BICUBIC)
    bg.paste(fg, ((W - fw) // 2, int(cy - fh / 2))); return grade(bg.convert('RGBA'), 0.14, 1.0)
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
class MapNB(Map):
    """coastlines only: no modern borders on a 1940s map"""
    @functools.lru_cache(None)
    def base(s):
        k = 2; im = Image.new('RGB', (W * k, H * k), SEA); d = ImageDraw.Draw(im); span = W / s.sc
        lon0, lon1 = s.c[0] - span, s.c[0] + span
        for nm, xs, ys, a, b_, c, e in ALLP:
            if b_ < lon0 - 5 or a > lon1 + 5: continue
            pts = [(((x - s.c[0]) * s.sc + W / 2) * k, (H / 2 - (y - s.c[1]) * s.sc) * k) for x, y in zip(xs, ys)]
            if len(pts) >= 3: d.polygon(pts, fill=LAND_HI if nm in s.hi else LAND, outline=LAND_HI if nm in s.hi else LAND)
        return im.resize((W, H), Image.LANCZOS)

# --- planes over occupied France (what was in the box stays open until the end)
def s_open(t, w0, w1):
    can, m = film(17.0 + (t - w0), 960, 620, 1.05)   # the formation, the bomber, the fighters: the film at its own speed
    title(can, t, ws('August'), 'AUGUST 1941', 430, 110, CREAM)
    sky(can, t, ws('besetzten'), 'BESETZTES FRANKREICH', CX, 1250, 92, CREAM, None, 0.5)
    return can
# --- who it was for: the man himself, close up (post-war footage)
def s_name(t, w0, w1):
    n = int((t - w0) * FPS * min(1.0, 3.55 / (w1 - w0))) + 1; can = grade(Image.open(B + 'clip2/f%04d.jpg' % max(1, min(108, n))).convert('RGB').resize((W, H)).convert('RGBA'), 0.14, 1.0); shade(can, 200, 0.55)   # the portrait film, already 9:16
    title(can, t, ws('Gefangenen') - 0.1, 'EIN GEFANGENER', 300, 96, CREAM, ws('Douglas') - 0.1)
    title(can, t, ws('Douglas'), 'DOUGLAS', 1150, 130, CREAM, None, bold=1)
    title(can, t, ws('Bader'), 'BADER', 1290, 170, YEL, None, bold=1)
    return can
# --- 1931: the wrecked Bulldog; the year in the sky, both legs lost
def s_crash(t, w0, w1):
    can = grade(fit('d06', t, w0, w1, 1.06), 0.1, 0.8); shade(can, 220, 0.5)
    sky(can, t, ws('Zehn') - 0.05, '1931', CX, 320, 150, CREAM, None, 0.5)
    t2 = ws('beide') - 0.05; q = lambda x, y: fitpt('d06', t, w0, w1, 1.06, x, y)
    if t > t2: on_quad(can, [q(*v) for v in tquad(990, 1255, 'BEIDE BEINE', 128, tilt=20)], 'BEIDE BEINE', 150, clamp((t - t2) / 0.06), (178, 62, 40), anton(150), eio((t - t2) / 0.4), 0.9, mod=0.45, op=0.95, glow=((10, 6, 4), 8, 0.45))
    t3 = ws('verloren') - 0.05
    if t > t3: on_quad(can, [q(*v) for v in tquad(1000, 1385, 'AMPUTIERT', 100, tilt=20)], 'AMPUTIERT', 150, clamp((t - t3) / 0.06), (178, 62, 40), anton(150), eio((t - t3) / 0.4), 0.9, mod=0.45, op=0.95, glow=((10, 6, 4), 8, 0.45))
    return can
# --- back in a Spitfire (his initials DB on the side): arrow to the legs as he climbs in
FLY0 = None   # set after ANCH (start of s_fly): the map keeps this film running behind it
CANOPY = [(14.4, 1370, 598), (15.0, 1410, 615), (15.6, 1420, 620), (16.2, 1520, 622), (16.8, 1540, 628)]   # centre of the canopy glass (film coords)
def canopy(ct):
    for (a, x0, y0), (b, x1, y1) in zip(CANOPY, CANOPY[1:]):
        if ct <= b: u = clamp((ct - a) / (b - a)); return lerp(x0, x1, u), lerp(y0, y1, u)
    return CANOPY[-1][1:]
def s_fly(t, w0, w1):
    ct = 14.4 + (t - w0); gx, gy = canopy(ct); can, m = film(ct, gx - 150, 560, 1.0)   # the window follows the glass, so the words stay put on it
    t1 = ws('Prothesen', 15) - 0.1
    if t > t1:
        a = clamp((t - t1) / 0.06)
        on_quad(can, [m(*v) for v in tquad(gx - 60, gy, 'PROTHESEN', 42, tilt=2)], 'PROTHESEN', 120, a, YEL, anton(120), eio((t - t1) / 0.35), 0.7, mod=0.25, op=0.95, glow=((0, 0, 0), 8, 0.6))
    return can
# --- the Channel: from England to Saint-Omer, shot down over France
CH = MapNB(1.55, 51.05, 4.4, hi=('United Kingdom',))
def s_map(t, w0, w1):
    z = lerp(1.0, 1.05, prog(t, w0, w1)); p = lambda lon, lat: CH.p(lon, lat, z)
    bg, _ = film(14.4 + (t - FLY0), 1500, 560, 1.1); bg = bg.filter(ImageFilter.GaussianBlur(9))   # the film keeps running behind the map
    can = Image.blend(bg, grade(CH.frame(z), 0.1, 1.0), 0.5)
    title(can, t, w0 + 0.1, '9. AUGUST 1941', 430, 110, CREAM)
    for nm, lon, lat in (('ENGLAND', 0.2, 51.75), ('FRANKREICH', 2.7, 49.95)):
        x, y = p(lon, lat); title(can, t, w0 + 0.3, nm, y, 54, (150, 160, 172), None, 'bebas', min(max(x, 170), 820))
    a = p(0.9, 51.25); b = p(1.95, 50.72); t1 = w0 + 0.3; ts_ = ws('abgeschossen', 17) - 0.05
    dashed(can, [a, b], eio((t - t1) / max(0.4, ts_ - t1)), YEL, 7, 22, 30)
    x, y = p(2.25, 50.75)
    if t > ts_ - 0.2:
        dot(can, x, y, CREAM, 10); title(can, t, ts_ - 0.2, 'SAINT-OMER', y - 55, 52, CREAM, None, 'bebas', min(x + 40, 880))
    if t > ts_:
        k = eout((t - ts_) / 0.25); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); r = 34 * k
        bx, by = b
        for wd, c in ((18, (0, 0, 0, 160)), (11, RED + (255,))): d.line((bx - r, by - r, bx + r, by + r), fill=c, width=wd); d.line((bx - r, by + r, bx + r, by - r), fill=c, width=wd)
        can.alpha_composite(L); title(can, t, ts_, 'ABGESCHOSSEN', by + 110, 90, RED, None, 'anton', min(max(bx, 260), 820))
    return can
# --- gun camera: a fighter going down; the leg that stayed in the cockpit
def s_bail(t, w0, w1):
    ct = 22.55 + (t - w0) * min(1.0, 5.1 / (w1 - w0)); can, m = film(ct, 960, 540, 1.0)   # the fighters, then the gun camera, at their own speed
    title(can, t, ws('rechte', 21) - 0.05, 'DAS RECHTE BEIN', 430, 100, CREAM)
    typed(can, t, ws('riss', 24) - 0.05, 'ABGERISSEN', 1260, 120, RED)
    return can
# --- Adolf Galland, the German ace
def s_galland(t, w0, w1):
    can = grade(fit('d05', t, w0, w1, 1.05, 0.15)); shade(can, 230, 0.5)
    title(can, t, ws('Adolf', 25), 'ADOLF', 1150, 120, CREAM, None, bold=1)
    title(can, t, ws('Galland', 25), 'GALLAND', 1290, 160, YEL, None, bold=1)
    title(can, t, ws('Fliegerass', 25) - 0.05, 'FLIEGERASS', 430, 80, CREAM, None, 'bebas')
    return can
# --- at Galland's airfield: the two men in one picture, rings on both
def s_airfield(t, w0, w1):
    ti, tsit = ws('lud', 27.5) - 0.05, ws('ließ', 29.5)   # hold on Galland, then glide to Bader
    can, m = side('d03', 0, 800, t, w0, w1, 1.04, eio((t - ti - 0.9) / max(0.3, tsit - ti - 1.0)) if t > ti + 0.9 else 0.0); shade(can, 200, 0.55)
    gx, gy = m(345, 360); bx, by = m(1275, 500); k = m(1, 0)[0] - m(0, 0)[0]   # head centres and screen scale
    ringp(can, t, ws('lud', 27.5) - 0.05, gx, gy, 185 * k, CREAM, 'GALLAND')
    ringp(can, t, ws('ließ', 29.5), bx, by, 195 * k, YEL, 'BADER')
    title(can, t, ws('eigenen', 30) - 0.1, 'SEINE EIGENE', 1150, 80, CREAM, None, 'bebas')
    title(can, t, ws('Messerschmitt') - 0.1, 'MESSERSCHMITT', 1260, 110, YEL)
    return can
# --- the Germans with his repaired leg; REPAIRED painted on the brick wall
WALL13 = [(1960, 820), (2330, 790), (2335, 930), (1965, 960)]
def s_leg(t, w0, w1):
    tw = ws('Er', 38.4) - 0.1; tc = ws('kletterte', 38.4) - 0.05
    u = 0.25 * clamp((t - w0) / (tw - w0)) + 0.75 * eio((t - tw) / 0.9) if t > tw else 0.25 * clamp((t - w0) / (tw - w0))
    can, m = side('d13', 900, 1392, t, w0, w1, 1.06, u); nk = eio((t - tw) / 0.9) if t > tw else 0.0
    if nk > 0: can = night(can, nk)
    shade(can, 200, 0.55)
    if t < tw + 0.4: can = leg_marks(can, m, t, 1 - clamp((t - tw) / 0.4))
    window_rope(can, m, t, tc)
    title(can, t, ws('Bettlaken', 39) - 0.05, 'BETTLAKEN', 440, 110, CREAM)
    stamp(can, t, ws('gefasst', 43) - 0.03, 'GEFASST', (CX, 1210), 130, 0)
    title(can, t, ws('nächsten', 43), 'AM NÄCHSTEN TAG', 1370, 80, CREAM, None, 'bebas')
    return can
def leg_marks(can, m, t, a):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    t1 = ws('Bein', 33.5) - 0.1
    if t > t1:
        lx, ly = m(1400, 980); arrow_to(L, (lx + 300, ly - 380), (lx + 60, ly - 60), eio((t - t1) / 0.35), YEL, 14, 46)
    sky(L, t, ws('reparierten', 34.5) - 0.05, 'REPARIERT', CX - 60, 430, 130, CREAM, None, 0.45)
    title(L, t, ws('Flucht', 37) - 0.05, 'FLUCHT', 1290, 140, RED)
    if a < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
    can.alpha_composite(L); return can
def window_rope(can, m, t, t1):
    """knotted sheets let down from the window, growing as he climbs"""
    u = eio((t - t1) / 2.2) if t > t1 else 0.0
    if u <= 0: return
    top = m(2200, 760); bot = m(2215, 1650); bot = (bot[0], min(bot[1], 1440)); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    yb = lerp(top[1], bot[1], u); n = int((yb - top[1]) / 120)
    for wd, c in ((22, (0, 0, 0, 150)), (14, (226, 222, 210, 255))): d.line((top[0], top[1], lerp(top[0], bot[0], u), yb), fill=c, width=wd)
    for i in range(1, n + 1):
        ky = top[1] + i * 120; kx = lerp(top[0], bot[0], (ky - top[1]) / (bot[1] - top[1])); d.ellipse((kx - 17, ky - 13, kx + 17, ky + 13), fill=(240, 236, 224, 255), outline=(0, 0, 0, 160), width=3)
    can.alpha_composite(L)
# --- Galland's message to England, typed
def s_word(t, w0, w1):
    can, _ = film(0.3 + (t - w0), 960, 540, 1.0, pic=FULL); can = ImageEnhance.Brightness(can.filter(ImageFilter.GaussianBlur(10))).enhance(0.55)   # unused newsreel keeps running behind the sheet
    paper(can, t, w0, w1, [('VON: LUFTWAFFE, SAINT-OMER', 28, w0 + 0.2, INK), ('AN: ROYAL AIR FORCE', 28, w0 + 0.6, INK), ('', 0, 0, INK),
                           ('SCHICKT EIN FLUGZEUG', 52, ws('Schickt', 46) - 0.1, INK), ('MIT EINEM ERSATZBEIN.', 52, ws('Ersatzbein', 47.5) - 0.3, INK), ('', 0, 0, INK),
                           ('ES WIRD NICHT', 58, ws('wird', 49) - 0.15, RED), ('BESCHOSSEN.', 58, ws('beschossen', 49.5) - 0.1, RED)])
    return can
# --- the RAF pilots: NO FAVORS written on the Hurricane
FUSE01 = tquad(1470, 300, 'KEIN GEFALLEN', 105, tilt=14)   # on the Hurricane's fuselage, tilted with it
def s_nofavor(t, w0, w1):
    can, m = side('d01', 820, 900, t, w0, w1, 1.04); shade(can, 200, 0.55)
    t1 = ws('Gefallen', 52) - 0.1
    if t > t1: on_quad(can, [m(*q) for q in FUSE01], 'KEIN GEFALLEN', 110, clamp((t - t1) / 0.06), CREAM, anton(110), eio((t - t1) / 0.4), 0.8, mod=0.4, op=0.95, glow=((6, 6, 6), 10, 0.55))
    title(can, t, ws('Feind', 51) - 0.05, 'VOM FEIND', 1260, 110, YEL)
    return can
# --- the raid: a Spitfire over France at its own speed
def s_raid(t, w0, w1):
    can, m = film(5.25 + (t - w0), 1000, 560, 1.0, pic=FULL) if t - w0 < 2.75 else film(19.75 + (t - w0 - 2.75), 960, 540, 1.0)   # the colour Spitfire, then the bomber
    title(can, t, w0 + 0.1, '19. AUGUST 1941', 430, 100, CREAM)
    title(can, t, ws('während', 55) - 0.1, 'MITTEN IM ANGRIFF', 1290, 100, YEL)
    return can
# --- what was inside: the crate with the leg
def s_reveal(t, w0, w1):
    can, m = side('d14', 230, 330, t, w0, w1, 1.06); shade(can, 200, 0.55)
    t1 = ws('neues', 57) - 0.1
    if t > t1: on_quad(can, [m(*v) for v in rquad(905, 785, 'EIN NEUES BEIN', 82, -31)], 'EIN NEUES BEIN', 120, clamp((t - t1) / 0.06), (165, 38, 30), anton(120), eio((t - t1) / 0.4), 0.8, mod=0.5, op=0.95)
    return can
# --- with two legs again: escape after escape, then the threat at night
def s_again(t, w0, w1):
    tn = ws('nachts', 64); k = eio((t - tn + 0.6) / 0.6) if t > tn - 0.6 else 0.0
    can = night(fit('d08', t, w0, w1, 1.06), 0.3 + 0.7 * k); shade(can, 210, 0.5)
    q = lambda x, y: fitpt('d08', t, w0, w1, 1.06, x, y)
    t1 = ws('versuchte', 60) - 0.1; ex, ey = q(548, 950)
    title(can, t, t1, 'FLUCHT', ey, 96, CREAM, None, 'anton', ex)   # right above the raised thumb
    if t > t1:   # one stroke per attempt, in the gap between thumb and index finger
        n = min(4, int((t - t1) / 0.35) + 1); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for i in range(n):
            a, b = q(645 + i * 40, 1075), q(635 + i * 40, 1215)
            d.line((a, b), fill=(0, 0, 0, 150), width=16); d.line((a, b), fill=CREAM + (255,), width=9)
        tr = ws('drohten', 63.5) - 0.1; u = eio((t - tr) / 0.35)
        if u > 0:   # the fifth, red stroke across the four
            a, b = q(620, 1185), q(790, 1105); e = (lerp(a[0], b[0], u), lerp(a[1], b[1], u))
            d.line((a, e), fill=(0, 0, 0, 150), width=18); d.line((a, e), fill=RED + (255,), width=11)
        can.alpha_composite(L)
    lx, ly = q(1010, 1330)
    title(can, t, ws('drohten', 63.5) - 0.05, 'DIE BEINE', ly - 60, 80, RED, None, 'anton', lx)   # right of the four fingers
    title(can, t, ws('wegzunehmen', 64.5) - 0.1, 'WEG', ly + 30, 100, RED, None, 'anton', lx)
    title(can, t, tn - 0.05, 'NACHTS', ly + 140, 80, (190, 205, 235), None, 'anton', lx)
    return can
# --- Colditz
def s_colditz(t, w0, w1):
    can = grade(crop('d16', 900, 900, lerp(1300, 1180, prog(t, w0, w1)))); shade(can, 210, 0.5)   # closer on the tower
    sky(can, t, ws('Colditz', 66) - 0.15, 'COLDITZ', 200, 330, 86, CREAM, None, 0.5)
    return can
# --- April 1945: Bader among RAF officers, the newsreel running on
def s_freed(t, w0, w1):
    can, m = film(11.25 + (t - w0), 960, 540, 1.0)
    title(can, t, ws('befreiten', 69.5) - 0.05, 'BEFREIT', 430, 140, YEL)
    title(can, t, ws('April', 70.5) - 0.05, 'APRIL 1945', 1270, 100, CREAM)
    return can
# --- home: Bader and his wife Thelma
def s_thelma(t, w0, w1):
    can, m = film(8.05 + (t - w0), 980, 540, 1.0)
    title(can, t, ws('Thelma') - 0.1, 'THELMA', 1250, 130, CREAM)
    return can
# --- the victory flypast over London
def s_flypast(t, w0, w1):
    can, m = film(17.0 + (t - w0), 1100, 600, 1.0)
    sky(can, t, ws('Siegesüberflug') - 0.05, 'SIEGESÜBERFLUG', CX, 430, 100, CREAM, None, 0.5)
    title(can, t, ws('London', 77.5) - 0.05, 'LONDON, JUNI 1945', 1260, 90, YEL)
    return can
# --- after the war: Galland in a cockpit, Bader leaning on it; the frame moves from Bader to Galland
def s_cockpit(t, w0, w1):
    """the whole photo across the screen (both men in it), a blurred copy fills above and below; rings on Bader, then on Galland"""
    im = src('d02').convert('RGB'); z = lerp(1.0, 1.06, prog(t, w0, w1)); fw = int(W * z); fh = int(fw * im.height / im.width); y0 = 980 - fh / 2; x0 = (W - fw) / 2 - 110   # a little to the left: Bader's ring stays clear of the buttons
    bg = im.resize((int(H * im.width / im.height), H), Image.BILINEAR); bx0 = (bg.width - W) // 2
    can = ImageEnhance.Brightness(bg.crop((bx0, 0, bx0 + W, H)).filter(ImageFilter.GaussianBlur(28))).enhance(0.5)
    can.paste(im.resize((fw, fh), Image.BICUBIC), (int(x0), int(y0))); can = grade(can.convert('RGBA')); shade(can, 200, 0.55)
    m = lambda x, y: (x0 + x * fw / im.width, y0 + y * fh / im.height); k = fw / im.width
    bx, by = m(2040, 600); gx, gy = m(560, 1330); tg = ws('Galland', 79.4) - 0.05
    ringp(can, t, w0 + 0.1, bx, by, 260 * k, YEL, 'BADER', by - 260 * k - 45)
    ringp(can, t, tg, gx, gy, 220 * k, CREAM, 'GALLAND', gy - 220 * k - 45)
    title(can, t, ws('Feind', 80) - 0.05, 'DER FEIND', 430, 120, RED)
    return can
# --- after the war: Galland and Bader laughing together
def s_end(t, w0, w1):
    can, m = side('d12', 430, 530, t, w0, w1, 1.04); shade(can, 210, 0.5)
    for s_, cy, h, col, t0 in (('MEHR ALS', 280, 36, INK, ws('mehr', 83) - 0.05), ('40 JAHRE', 334, 58, INK, ws('vierzig', 83.5) - 0.05), ('FREUNDE', 392, 46, (150, 30, 28), ws('Freund', 84.5) - 0.05)):
        if t > t0: on_quad(can, [m(*v) for v in tquad(1095, cy, s_, h)], s_, 120, clamp((t - t0) / 0.06), col, anton(120), eio((t - t0) / 0.4), 0.7, mod=0.4, op=0.93)
    return can

ANCH = [
 (0.0, s_open, None),
 (ws('Sie', 7) - 0.1, s_name, ('fade',)),
 (ws('Zehn', 10.8) - 0.1, s_crash, ('fade',)),
 (ws('doch', 14.8) - 0.1, s_fly, ('fade',)),
 (ws('Anfang', 16.9) - 0.1, s_map, ('fade',)),
 (ws('Als', 20.6) - 0.1, s_bail, ('fade',)),
 (ws('Das', 25.6) - 0.1, s_galland, ('fade',)),
 (ws('lud', 27.8) - 0.1, s_airfield, ('fade',)),
 (ws('Die', 32.3) - 0.1, s_leg, ('fade',)),
 (ws('Galland', 44.8) - 0.1, s_word, ('fade',)),
 (ws('Die', 50.3) - 0.1, s_nofavor, ('fade',)),
 (ws('Einer', 53.3) - 0.1, s_raid, ('fade',)),
 (ws('Darin', 56.8) - 0.1, s_reveal, ('fade',)),
 (ws('Wieder', 59) - 0.1, s_again, ('fade',)),
 (ws('Am', 66.1) - 0.1, s_colditz, ('fade',)),
 (ws('Amerikanische', 68.5) - 0.1, s_freed, ('fade',)),
 (ws('Zu', 73) - 0.1, s_thelma, ('fade',)),
 (ws('im', 75.6) - 0.1, s_flypast, ('fade',)),
 (ws('Und', 78.8) - 0.1, s_cockpit, ('fade',)),
 (ws('blieb', 83) - 0.1, s_end, ('fade',))]
FLY0 = [a for a, fn, tr in ANCH if fn is s_fly][0]
