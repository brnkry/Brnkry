
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
    if label: title(can, t, t0 + 0.2, label, ly if ly is not None else y + r + 50, size, col, None, 'bebas', min(max(x, 170), 910))
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

# --- a bomber formation over France; a crate under a parachute falls away from it (what is inside stays open)
def s_open(t, w0, w1):
    can, m = film(17.5 + (t - w0) * min(1.0, 2.15 / (w1 - w0)), 960, 700, 1.05)
    t1 = ws('dropped') - 0.1
    if t > t1:
        u = clamp((t - t1) / 3.4); x = lerp(560, 600, u) + 14 * math.sin(t * 2.2); y = lerp(660, 1080, eio(u))
        chute(can, x, y, 1.15, clamp((t - t1) / 0.3), 10 * math.sin(t * 2.2), True)
    sky(can, t, ws('occupied'), 'OCCUPIED FRANCE', CX, 430, 104, CREAM, None, 0.5)
    title(can, t, ws('August'), 'AUGUST 1941', 1290, 110, YEL)
    return can
# --- who it was for: the man himself, close up (post-war footage)
def s_name(t, w0, w1):
    can, m = film(0.4 + (t - w0) * 0.9, 960, 520, 1.0, pic=FULL)
    title(can, t, ws('prisoner') - 0.1, 'ONE PRISONER', 430, 96, CREAM, ws('Douglas') - 0.1)
    title(can, t, ws('Douglas'), 'DOUGLAS', 1150, 130, CREAM, None, bold=1)
    title(can, t, ws('Bader'), 'BADER', 1290, 170, YEL, None, bold=1)
    return can
# --- 1931: the wrecked Bulldog; the year in the sky, both legs lost
def s_crash(t, w0, w1):
    can = grade(fit('d06', t, w0, w1, 1.06), 0.1, 0.8); shade(can, 220, 0.5)
    sky(can, t, ws('Ten') - 0.05, '1931', CX, 420, 150, CREAM, None, 0.5)
    t2 = ws('both')
    title(can, t, t2, 'BOTH LEGS', 1250, 120, RED)
    title(can, t, ws('crash'), 'AMPUTATED', 1370, 70, CREAM, None, 'bebas')
    return can
# --- back in a Spitfire (his initials DB on the side): arrow to the legs as he climbs in
def s_fly(t, w0, w1):
    ct = 15.55 + (t - w0) * min(1.0, 1.4 / (w1 - w0)); can, m = film(ct, 1260, 560, 1.1)
    t1 = ws('artificial', 11) - 0.1
    if t > t1:
        lx, ly = m(1330, 720); arrow_to(can, (lx - 330, ly - 420), (lx - 50, ly - 60), eio((t - t1) / 0.35), YEL, 14, 46)
        title(can, t, t1, 'ARTIFICIAL LEGS', 440, 100, YEL)
    return can
# --- the Channel: from England to Saint-Omer, shot down over France
CH = MapNB(1.55, 51.05, 4.4, hi=('United Kingdom',))
def s_map(t, w0, w1):
    z = lerp(1.0, 1.05, prog(t, w0, w1)); can = grade(CH.frame(z), 0.1, 1.0); p = lambda lon, lat: CH.p(lon, lat, z)
    title(can, t, w0 + 0.1, '9 AUGUST 1941', 430, 110, CREAM)
    for nm, lon, lat in (('ENGLAND', 0.2, 51.75), ('FRANCE', 2.7, 49.95)):
        x, y = p(lon, lat); title(can, t, w0 + 0.3, nm, y, 54, (150, 160, 172), None, 'bebas', min(max(x, 170), 820))
    a = p(0.9, 51.25); b = p(1.95, 50.72); t1 = w0 + 0.3; ts_ = ws('shot', 13) - 0.05
    dashed(can, [a, b], eio((t - t1) / max(0.4, ts_ - t1)), YEL, 7, 22, 30)
    x, y = p(2.25, 50.75)
    if t > ts_ - 0.2:
        dot(can, x, y, CREAM, 10); title(can, t, ts_ - 0.2, 'SAINT-OMER', y - 55, 52, CREAM, None, 'bebas', min(x + 40, 880))
    if t > ts_:
        k = eout((t - ts_) / 0.25); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); r = 34 * k
        bx, by = b
        for wd, c in ((18, (0, 0, 0, 160)), (11, RED + (255,))): d.line((bx - r, by - r, bx + r, by + r), fill=c, width=wd); d.line((bx - r, by + r, bx + r, by - r), fill=c, width=wd)
        can.alpha_composite(L); title(can, t, ts_, 'SHOT DOWN', by + 110, 100, RED, None, 'anton', min(max(bx, 260), 820))
    return can
# --- gun camera: a fighter going down; the leg that stayed in the cockpit
def s_bail(t, w0, w1):
    ct = 23.95 + (t - w0) * min(1.0, 3.7 / (w1 - w0)); can, m = film(ct, 960, 540, 1.0)
    title(can, t, ws('right', 17) - 0.05, 'HIS RIGHT LEG', 430, 100, CREAM)
    typed(can, t, ws('torn', 20) - 0.05, 'TORN OFF', 1260, 130, RED)
    return can
# --- Adolf Galland, the German ace
def s_galland(t, w0, w1):
    can = grade(fit('d05', t, w0, w1, 1.05, 0.15)); shade(can, 230, 0.5)
    title(can, t, ws('Adolf', 21), 'ADOLF', 1150, 120, CREAM, None, bold=1)
    title(can, t, ws('Galland', 21), 'GALLAND', 1290, 160, YEL, None, bold=1)
    title(can, t, ws('German', 21) - 0.05, 'LUFTWAFFE ACE', 430, 80, CREAM, None, 'bebas')
    return can
# --- at Galland's airfield: the two men in one picture, rings on both
def s_airfield(t, w0, w1):
    can, m = side('d03', 0, 560, t, w0, w1, 1.04); shade(can, 200, 0.55)
    gx, gy = m(300, 300); bx, by = m(1260, 420)
    ringp(can, t, ws('invited', 23) - 0.05, gx, gy, 115, CREAM, 'GALLAND')
    ringp(can, t, ws('sit', 25), bx, by, 135, YEL, 'BADER')
    title(can, t, ws('Messerschmitt') - 0.3, 'HIS OWN', 1150, 80, CREAM, None, 'bebas')
    title(can, t, ws('Messerschmitt') - 0.1, 'MESSERSCHMITT', 1260, 110, YEL)
    return can
# --- the Germans with his repaired leg; REPAIRED painted on the brick wall
WALL13 = [(1960, 820), (2330, 790), (2335, 930), (1965, 960)]
def s_leg(t, w0, w1):
    can, m = side('d13', 900, 1250, t, w0, w1, 1.04); shade(can, 200, 0.55)
    t1 = ws('leg', 27.5) - 0.1
    if t > t1:
        lx, ly = m(1400, 980); arrow_to(can, (lx + 300, ly - 380), (lx + 60, ly - 60), eio((t - t1) / 0.35), YEL, 14, 46)
    t2 = ws('repaired', 29) - 0.05
    sky(can, t, t2, 'REPAIRED', CX - 60, 430, 130, CREAM, None, 0.45)
    title(can, t, ws('escape', 30.5) - 0.05, 'ESCAPE', 1290, 140, RED)
    return can
# --- night: knotted sheets down the wall from a window, then CAUGHT
def s_window(t, w0, w1):
    can, m = side('d13', 1392, 1392, t, w0, w1, 1.05); can = night(can, 1.0); shade(can, 210, 0.5)
    t1 = ws('climbed', 31.5) - 0.05; u = eio((t - t1) / 2.2) if t > t1 else 0.0
    if u > 0:
        top = m(2200, 760); bot = m(2215, 1650); bot = (bot[0], min(bot[1], 1440)); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        yb = lerp(top[1], bot[1], u); n = int((yb - top[1]) / 120)
        for wd, c in ((22, (0, 0, 0, 150)), (14, (226, 222, 210, 255))): d.line((top[0], top[1], lerp(top[0], bot[0], u), yb), fill=c, width=wd)
        for i in range(1, n + 1):
            ky = top[1] + i * 120; kx = lerp(top[0], bot[0], (ky - top[1]) / (bot[1] - top[1])); d.ellipse((kx - 17, ky - 13, kx + 17, ky + 13), fill=(240, 236, 224, 255), outline=(0, 0, 0, 160), width=3)
        can.alpha_composite(L)
    title(can, t, ws('knotted', 32) - 0.05, 'KNOTTED BEDSHEETS', 440, 92, CREAM)
    stamp(can, t, ws('caught', 34) - 0.03, 'CAUGHT', (CX, 1210), 130, -6)
    title(can, t, ws('next', 34.5), 'THE NEXT DAY', 1370, 80, CREAM, None, 'bebas')
    return can
# --- Galland's message to England, typed
def s_word(t, w0, w1):
    can = Image.new('RGBA', (W, H), (16, 15, 14, 255))
    paper(can, t, w0, w1, [('FROM: LUFTWAFFE, SAINT-OMER', 28, w0 + 0.2, INK), ('TO: ROYAL AIR FORCE', 28, w0 + 0.6, INK), ('', 0, 0, INK),
                           ('SEND ONE PLANE', 60, ws('send', 37.5) - 0.1, INK), ('WITH A SPARE LEG.', 60, ws('spare', 38.5) - 0.3, INK), ('', 0, 0, INK),
                           ('IT WILL NOT', 60, ws('will', 39.5) - 0.15, RED), ('BE SHOT AT.', 60, ws('shot', 40) - 0.1, RED)])
    return can
# --- the RAF pilots: NO FAVORS written on the Hurricane
FUSE01 = [(1080, 250), (1600, 240), (1605, 360), (1085, 372)]
def s_nofavor(t, w0, w1):
    can, m = side('d01', 650, 820, t, w0, w1, 1.04); shade(can, 200, 0.55)
    t1 = ws('favor', 41.5) - 0.1
    if t > t1: on_quad(can, [m(*q) for q in FUSE01], 'NO FAVORS', 110, clamp((t - t1) / 0.06), CREAM, anton(110), eio((t - t1) / 0.4), 0.8, mod=0.4, op=0.95, glow=((6, 6, 6), 10, 0.55))
    title(can, t, ws('enemy', 42.5) - 0.05, 'FROM THE ENEMY', 1260, 96, YEL)
    return can
# --- the raid: fighters over France, the crate falls again
def s_raid(t, w0, w1):
    can, m = film(21.3 + (t - w0) * min(1.0, 2.6 / (w1 - w0)), 960, 540, 1.05)
    title(can, t, w0 + 0.1, '19 AUGUST 1941', 430, 100, CREAM)
    t1 = ws('dropped', 44) - 0.1
    if t > t1:
        u = clamp((t - t1) / 2.4); x = lerp(640, 600, u) + 12 * math.sin(t * 2.4); y = lerp(560, 1060, eio(u))
        chute(can, x, y, 1.15, clamp((t - t1) / 0.3), 9 * math.sin(t * 2.4), True)
    title(can, t, ws('raid', 45) - 0.1, 'DURING A RAID', 1290, 100, YEL)
    return can
# --- what was inside: the crate with the leg
def s_reveal(t, w0, w1):
    can, m = side('d14', 1000, 900, t, w0, w1, 1.06); shade(can, 200, 0.55)
    title(can, t, ws('new', 46.5) - 0.05, 'A NEW LEG', 1290, 140, YEL, None, bold=1)
    return can
# --- with two legs again: escape after escape, then the threat at night
def s_again(t, w0, w1):
    tn = ws('night', 53); k = eio((t - tn + 0.6) / 0.6) if t > tn - 0.6 else 0.0
    can = night(fit('d08', t, w0, w1, 1.06), 0.3 + 0.7 * k); shade(can, 210, 0.5)
    t1 = ws('escape', 49.5) - 0.1; tt = ws('threatened', 51.5) - 0.3; out = 1 - clamp((t - tt) / 0.25)
    title(can, t, t1, 'ESCAPE', 1150, 120, CREAM, tt)
    if t1 < t and out > 0:   # tally of attempts drawn under the word
        n = min(5, int((t - t1) / 0.4) + 1); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); A = int(255 * out)
        for i in range(n):
            if i < 4: x = 450 + i * 60; d.line((x, 1250, x - 10, 1370), fill=(0, 0, 0, int(150 * out)), width=18); d.line((x, 1250, x - 10, 1370), fill=CREAM + (A,), width=11)
            else: d.line((425, 1340, 655, 1270), fill=(0, 0, 0, int(150 * out)), width=18); d.line((425, 1340, 655, 1270), fill=RED + (A,), width=11)
        can.alpha_composite(L)
    title(can, t, ws('threatened', 51.5) - 0.05, 'TAKE HIS LEGS', 1180, 100, RED)
    title(can, t, tn - 0.05, 'AT NIGHT', 1300, 120, (190, 205, 235))
    return can
# --- Colditz
def s_colditz(t, w0, w1):
    can = grade(fit('d16', t, w0, w1, 1.06, 0.1)); shade(can, 210, 0.5)
    sky(can, t, ws('Colditz') - 0.15, 'COLDITZ', CX, 430, 150, CREAM, None, 0.5)
    return can
# --- after the war: Galland and Bader laughing together
def s_end(t, w0, w1):
    can, m = side('d12', 430, 530, t, w0, w1, 1.04); shade(can, 210, 0.5)
    title(can, t, ws('enemy', 57) - 0.05, 'THE ENEMY', 1150, 100, CREAM)
    title(can, t, ws('friend', 59.5) - 0.05, 'FRIENDS', 1280, 150, YEL, None, bold=1)
    title(can, t, ws('forty', 60) - 0.05, 'FOR 40 YEARS', 1400, 80, CREAM, None, 'bebas')
    return can

ANCH = [
 (0.0, s_open, None),
 (ws('It', 5) - 0.1, s_name, ('fade',)),
 (ws('Ten', 7.5) - 0.1, s_crash, ('fade',)),
 (ws('but', 11) - 0.1, s_fly, ('fade',)),
 (ws('Earlier', 13) - 0.1, s_map, ('whip', 1)),
 (ws('As', 16.8) - 0.1, s_bail, ('fade',)),
 (ws('The', 21.5) - 0.1, s_galland, ('fade',)),
 (ws('invited', 23.4) - 0.1, s_airfield, ('fade',)),
 (ws('The', 27) - 0.1, s_leg, ('fade',)),
 (ws('He', 31.6) - 0.1, s_window, ('fade',)),
 (ws('Galland', 36) - 0.1, s_word, ('fade',)),
 (ws('The', 41.2) - 0.1, s_nofavor, ('fade',)),
 (ws('One', 43.6) - 0.1, s_raid, ('whip', -1)),
 (ws('Inside', 46) - 0.1, s_reveal, ('fade',)),
 (ws('With', 48.2) - 0.1, s_again, ('fade',)),
 (ws('In', 54.2) - 0.1, s_colditz, ('fade',)),
 (ws('And', 56.6) - 0.1, s_end, ('fade',))]
