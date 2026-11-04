
# ================= Wainwright scenes =================
def ws(word, after=0.0): return wt(word, after) - 0.05
def fr(ct):   # newsreel frame at newsreel time ct (s)
    return cframe(int(round(ct * FPS)) + 1)
def film(ct, cx, cy=540, z=1.0, sat=1.0, warm=0.18):
    """9:16 window from the 1920x1080 newsreel coordinates, centre (cx, cy), zoom z; returns canvas and a film->screen mapper"""
    im = fr(ct); S = im.width / 1920; ch = 1080 / z; cw = ch * W / H
    x0 = cx - cw / 2; y0 = min(max(cy - ch / 2, 0), 1080 - ch)
    can = grade(im.resize((W, H), Image.BICUBIC, box=(x0 * S, y0 * S, (x0 + cw) * S, (y0 + ch) * S)).convert('RGBA'), warm, sat); shade(can, 200, 0.55)
    return can, (lambda x, y: ((x - x0) * W / cw, (y - y0) * H / ch))
def arrow_to(can, a, b, u, col=YEL, w_=14, head=44):
    if u <= 0: return
    e = (lerp(a[0], b[0], u), lerp(a[1], b[1], u)); ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line((a, e), fill=(0, 0, 0, 150), width=w_ + 8); d.line((a, e), fill=col + (255,), width=w_)
    d.polygon([(e[0] + 12 * math.cos(ang), e[1] + 12 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))], fill=col + (255,))
    can.alpha_composite(L)

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

# Missouri: MacArthur signs (film 0..3.30), the picture freezes on 'signed', the words are written on the open document, then it runs on
# and the frame slides left with him as he turns and hands the pen to Wainwright (film 5.03..5.63)
FREEZE_AT = 3.30; RESUME = None   # set below from the words
DOC1 = [(1045, 724), (1320, 721), (1342, 776), (1063, 780)]   # upper page of the open folder, above the fold (film coords)
DOC2 = [(1075, 798), (1395, 793), (1430, 860), (1103, 866)]   # lower page
def s_sign(t, w0, w1):
    t_res = ws('Dann') + 0.05
    if t < FREEZE_AT: ct = t
    elif t < t_res: ct = FREEZE_AT
    else: ct = FREEZE_AT + (t - t_res)
    cx = 1230; z = 1.0
    if FREEZE_AT <= t < t_res + 0.2: z = lerp(1.0, 1.1, eio((t - FREEZE_AT) / 0.8)) if t < t_res else lerp(1.1, 1.0, eio((t - t_res) / 0.2))
    u = eio((t - ws('drehte') - 0.05) / 1.3) if t > ws('drehte') else 0.0
    fz = eio((t - FREEZE_AT) / 0.8) if FREEZE_AT <= t < t_res else (1 - eio((t - t_res) / 0.3) if t_res <= t < t_res + 0.3 else 0.0)
    cx = lerp(1230, 540, u) + 45 * fz
    can, m = film(ct, cx, 540 + 50 * fz, z)
    if FREEZE_AT <= t < t_res + 0.25:   # frozen frame: a touch of desaturation, the words written on the document, an arrow onto it
        out = 1 - clamp((t - t_res) / 0.25)
        t1 = ws('Japans') - 0.1; t2 = ws('Kapitulation') - 0.05   # German word order: KAPITULATION is spoken first, JAPANS after
        if t > t1: on_quad(can, [m(*p) for p in DOC1], 'JAPANS', 120, out, INK, anton(120), eio((t - t1) / 0.35), 0.7, mod=0.35, op=0.92)
        if t > t2: on_quad(can, [m(*p) for p in DOC2], 'KAPITULATION', 120, out, RED, anton(120), eio((t - t2) / 0.4), 0.7, mod=0.3, op=0.95)
        if t > FREEZE_AT + 0.15:
            tip = m(1180, 718); arrow_to(can, (tip[0] - 160, tip[1] - 330), (tip[0] - 15, tip[1] - 25), eio((t - FREEZE_AT - 0.15) / 0.35) * out)
    if t > ws('abgemagerten') - 0.15:   # a still arrow from the right, stopping short of his head where he bows to take the pen
        tip, tail = (585, 505), (905, 335)
        arrow_to(can, tail, tip, eio((t - ws('abgemagerten') + 0.15) / 0.35) * (1 - clamp((t - ws('hinter') - 0.1) / 0.25)), YEL, 14, 46)
    return can
HEADK = [(5.0, 330, 225), (5.4, 390, 240), (5.75, 480, 330), (6.3, 410, 265), (7.0, 300, 230), (9.6, 295, 230)]   # Wainwright's head centre (film)
def HEAD(ct):
    for (a, x0, y0), (b, x1, y1) in zip(HEADK, HEADK[1:]):
        if ct <= b: u = clamp((ct - a) / (b - a)); return lerp(x0, x1, u), lerp(y0, y1, u)
    return HEADK[-1][1:]
def s_then(t, w0, w1):   # w09, pre-war portrait: 'three years earlier'
    ts = ws('kapituliert', 12); bw = eio((t - ts) / 0.4) if t > ts else 0.0   # the photo turns black and white on 'surrendered'
    can = grade(fit('w09', t, w0, w1, 1.06), 0.12, lerp(0.78, 0.0, bw)); shade(can, 220, 0.5)
    if bw > 0: can.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(70 * bw))))
    title(can, t, ts, 'KAPITULIERT', 900, 104, CREAM, None, 'anton')
    title(can, t, ts + 0.25, '1942', 1035, 150, YEL, None, 'anton')
    return can
def s_name(t, w0, w1):   # w08, the name
    can = grade(fit('w08', t, w0, w1, 1.06)); shade(can, 220, 0.5)
    title(can, t, ws('Jonathan'), 'JONATHAN', 1150, 120, CREAM, bold=1)
    title(can, t, ws('Wainwright'), 'WAINWRIGHT', 1290, 150, YEL, bold=1)
    return can
def s_pt(t, w0, w1):   # PT boat (MacArthur leaves), 'MARCH 1942' in the grey sky
    ct = 9.7 + (t - w0) * 0.95; can, m = film(min(ct, 17.4), 960, 540, 1.0, 1.0)
    sky(can, t, ws('März'), 'MÄRZ 1942', CX, 420, 130, CREAM, None, 0.5)
    return can
def s_command(t, w0, w1):   # w01, the two men in 1941: names on the sky with pointers
    can, m = side('w01', 700, 820, t, w0, w1, 1.04); shade(can, 200, 0.55)
    tt = ws('Wainwright', w0 - 0.5)
    if t > tt: f = m(1030, 235); ring(can, t, tt, f[0], f[1], YEL, 190, False)
    return can
def s_corr(t, w0, w1):   # the island under fire, the ships, the landing craft: one continuous run of the newsreel
    ct = 20.85 + (t - w0) * min(1.0, 8.4 / (w1 - w0)); can, m = film(min(ct, 29.3), 900 if ct < 22.95 else 960, 540, 1.0)
    sky(can, t, ws('Corregidor'), 'CORREGIDOR', CX, 470, 130, CREAM, None, 0.5, 0.0, ws('unter', 27) - 0.1)
    title(can, t, ws('6.', 29), '6. MAI 1942', 450, 120, CREAM, ws('kapitulierte', 31) - 0.35)
    typed(can, t, ws('kapitulierte', 31) - 0.05, 'KAPITULATION', 450, 120, RED)
    return can
def s_ships(t, w0, w1):   # warships firing; the date on the cliff behind
    ct = 22.99 + (t - w0) * 0.55; can, m = film(min(ct, 24.15), 960, 540, 1.0)
    on_quad(can, [(150, 560), (930, 520), (940, 700), (160, 740)], 'MAY 6, 1942', 130, clamp((t - ws('May', w0)) / 0.06) if t > ws('May', w0) else 0, CREAM, anton(130), eio((t - ws('May', w0)) / 0.45), 1.0, mod=0.3, op=0.92, glow=((8, 10, 14), 10, 0.7))
    return can
def s_beach(t, w0, w1):   # men on the beach: the surrender
    ct = 29.4 + (t - w0) * 1.0; can, m = film(min(ct, 32.85), 980, 540, 1.0, 0.9)
    stamp(can, t, ws('surrendered', w0 - 0.5) - 0.03, 'SURRENDER', (CX, 1300), 110, -6)
    return can
def s_radio(t, w0, w1):   # w03, KZRH Manila: across the studio to him at the microphone, ON AIR written on the cabinet
    can, m = side('w03', 150, 1250, t, w0, w1, 1.03); shade(can, 200, 0.55)
    tt = ws('Manila', w0 - 0.5)
    title(can, t, tt, 'MANILA', 1250, 120, CREAM, None)
    t2 = ws('live', w0)
    if t > t2 - 0.25: on_quad(can, [m(*p) for p in CAB03], 'LIVE', 130, clamp((t - t2 + 0.25) / 0.06), RED, anton(130), eio((t - t2 + 0.25) / 0.35), 0.8, mod=0.25, op=0.95, glow=((200, 30, 30), 14, 0.55))
    return can
CAB03 = [(1560, 340), (1890, 335), (1892, 470), (1562, 476)]   # back wall right of his head
def s_pow(t, w0, w1):   # w05, the gaunt general: POW on the wall behind him
    can = grade(fit('w05', t, w0, w1, 1.05)); shade(can, 210, 0.5)
    q = lambda x, y: fitpt('w05', t, w0, w1, 1.05, x, y); t1 = ws('Kriegsgefangene', w0 - 0.5)
    if t > t1 - 0.2: on_quad(can, [q(*p) for p in WALL05], 'GEFANGEN', 150, clamp((t - t1 + 0.2) / 0.06), CREAM, anton(150), eio((t - t1 + 0.2) / 0.4), 1.0, mod=0.35, op=0.9, glow=((8, 8, 8), 10, 0.6))
    return can
WALL05 = [(250, 478), (690, 467), (692, 582), (252, 593)]   # wider: GEFANGEN is longer than P.O.W.
PAC = MapNB(124.5, 29.6, 38, hi=('Philippines',))
def s_map(t, w0, w1):   # camp to camp: Corregidor, Tarlac, Formosa, Manchuria
    z = lerp(1.0, 1.04, prog(t, w0, w1)); can = grade(PAC.frame(z), 0.1, 1.0); p = lambda lon, lat: PAC.p(lon, lat, z)
    for nm, lon, lat in (('MANDSCHUKUO', 126.5, 46.0), ('KOREA', 127.8, 37.0), ('CHINA', 113.5, 31.0), ('JAPAN', 138.0, 37.5)):
        x, y = p(lon, lat); title(can, t, w0 + 0.2, nm, y, 46, (150, 160, 170), None, 'bebas', min(max(x, 140), 900))
    stops = [('CORREGIDOR', 120.57, 14.38, ws('Über', w0 - 0.5)), ('FORMOSA', 121.6, 23.97, ws('Lager', w0 - 0.5)), ('MANDSCHUREI', 125.1, 42.9, ws('Mandschurei', w0 - 0.5))]
    pts = [p(lon, lat) for _, lon, lat, _ in stops]
    for i, (nm, lon, lat, tt) in enumerate(stops):
        if t > tt:
            x, y = pts[i]; dot(can, x, y, YEL if i == 2 else CREAM, 11); title(can, t, tt, nm, y - 60, 60, YEL if i == 2 else CREAM, None, 'bebas', min(max(x, 220), 860))
        if i and t > stops[i - 1][3]:
            u = eio((t - stops[i - 1][3]) / max(0.4, tt - stops[i - 1][3]))
            dashed(can, [pts[i - 1], pts[i]], u, YEL, 7, 22, 30 if u < 1 else 0)
    return can
def s_fear(t, w0, w1):   # w07, the cup: GAVE UP? on the wall
    can = grade(fit('w07', t, w0, w1, 1.05)); shade(can, 210, 0.5)
    q = lambda x, y: fitpt('w07', t, w0, w1, 1.05, x, y); t1 = ws('aufgegeben', w0)
    if t > t1 - 0.1: on_quad(can, [q(*p) for p in WALL07], 'AUFGEGEBEN?', 120, clamp((t - t1 + 0.1) / 0.06), INK, anton(120), eio((t - t1 + 0.1) / 0.35), 0.8, mod=0.35, op=0.92)
    return can
WALL07 = [(1150, 480), (1460, 468), (1464, 600), (1153, 612)]
def s_free(t, w0, w1):   # the general saluting at the aircraft, August 1945
    ct = 36.0 + (t - w0) * min(0.85, 2.85 / (w1 - w0)); can, m = film(min(ct, 38.9), 1050, 560, 1.0, 1.0)
    title(can, t, ws('August', w0 - 0.5), 'AUGUST 1945', 420, 110, CREAM)
    t1 = ws('befreiten', w0) - 0.1
    if t > t1: on_quad(can, [m(*q) for q in PLANE11], 'BEFREIT', 120, clamp((t - t1) / 0.06), INK, anton(120), eio((t - t1) / 0.35), 0.8, mod=0.35, op=0.92)
    return can
PLANE11 = [(1080, 393), (1265, 393), (1265, 457), (1080, 457)]   # white fuselage right of his head (film coords)
def s_missouri_date(t, w0, w1):   # w10, the reunion with MacArthur, two days before the ceremony
    can, m = side('w10', 500, 380, t, w0, w1, 1.04); shade(can, 200, 0.55)
    title(can, t, ws('Zwei', w0 - 0.5), '2. SEPTEMBER 1945', 1180, 92, CREAM)
    title(can, t, ws('USS', w0 - 0.5), 'USS MISSOURI', 1310, 120, YEL)
    return can
def s_medal(t, w0, w1):   # w02, Truman pins the medal; then BLOCKED 1942
    can, m = side('w02', 760, 760, t, w0, w1, 1.03); shade(can, 200, 0.55)
    tm = ws('Medal', w0 - 0.5); tb = ws('blockiert', w0) - 0.05; te = tb - 0.12   # MEDAL OF HONOR and the arrow stay until 'blocked'
    for i, (s_, q) in enumerate(zip(('MEDAL', 'OF', 'HONOR'), TREES02)):
        tt = tm + i * 0.15; out = 1 - clamp((t - te) / 0.12)
        if tm <= t and out > 0: on_quad(can, [m(*p) for p in q], s_, 120, clamp((t - tt) / 0.06) * out, YEL, anton(120), eio((t - tt) / 0.3), 0.8, op=0.95, glow=((6, 8, 6), 10, 0.7))
    if tm + 0.5 < t < te + 0.12:
        a = m(1080, 560); b = m(1505, 930); arrow_to(can, a, b, eio((t - tm - 0.5) / 0.4) * (1 - clamp((t - te) / 0.12)), YEL, 12, 40)
    for i, (s_, q) in enumerate(zip(('1942', 'BLOCKIERT'), TREES02[::2])):
        tt = tb + i * 0.1
        if t > tt: on_quad(can, [m(*p) for p in q], s_, 120, clamp((t - tt) / 0.06), RED, anton(120), eio((t - tt) / 0.3), 0.8, op=0.95, glow=((6, 8, 6), 10, 0.7))
    return can
TREES02 = [[(840, 200), (1300, 200), (1300, 310), (840, 310)], [(980, 320), (1160, 320), (1160, 400), (980, 400)], [(840, 410), (1300, 410), (1300, 520), (840, 520)]]   # foliage left of his head
def s_end(t, w0, w1):   # back on the Missouri, MacArthur signing again: Japan does the same
    ct = 7.35 + (t - w0) * min(0.5, 2.05 / (w1 - w0)); can, m = film(min(ct, 9.45), 520, 540, lerp(1.0, 1.05, prog(t, w0, w1)))
    t1 = ws('zur', w0 - 0.5); t2 = ws('sah', w0 - 0.5)
    title(can, t, t1, 'ZUR KAPITULATION', 470, 96, CREAM, None, 'anton', 650, 520)
    title(can, t, ws('gezwungen', w0 - 0.5), 'GEZWUNGEN', 580, 110, CREAM, None, 'anton', 650, 520)
    title(can, t, t2, 'SAH JAPAN', 760, 90, YEL, None, 'anton', 650, 520)
    title(can, t, ws('kapitulieren', w0 - 0.5), 'KAPITULIEREN', 870, 110, YEL, None, 'anton', 650, 520)
    return can

ANCH = [
 (0.0, s_sign, None),
 (ws('Drei') - 0.1, s_then, ('fade',)),
 (ws('Sein', 14.5) - 0.1, s_name, ('fade',)),
 (ws('Im', 17) - 0.1, s_pt, ('whip', 1)),
 (ws('und', 21) - 0.1, s_command, ('fade',)),
 (ws('Auf', 25) - 0.1, s_corr, ('whip', -1)),
 (ws('Die', 34.5) - 0.1, s_radio, ('fade',)),
 (ws('Er', 41.5) - 0.1, s_pow, ('fade',)),
 (ws('Über', 45.5) - 0.1, s_map, ('fade',)),
 (ws('in', 50.5) - 0.1, s_fear, ('fade',)),
 (ws('Im', 56) - 0.1, s_free, ('whip', 1)),
 (ws('Zwei', 60) - 0.1, s_missouri_date, ('fade',)),
 (ws('Wochen', 63.5) - 0.1, s_medal, ('fade',)),
 (ws('Der', 71) - 0.1, s_end, ('fade',))]
