
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

# Missouri: MacArthur signs (film 0..3.30), the picture freezes on 'signed', the words are written on the open document, then it runs on
# and the frame slides left with him as he turns and hands the pen to Wainwright (film 5.03..5.63)
FREEZE_AT = 3.30; RESUME = None   # set below from the words
DOC1 = [(1108, 742), (1392, 738), (1426, 792), (1138, 797)]   # right page of the open folder, line 1 (film coords)
DOC2 = [(1140, 803), (1430, 798), (1466, 852), (1170, 858)]
def s_sign(t, w0, w1):
    t_res = ws('Then') + 0.05
    if t < FREEZE_AT: ct = t
    elif t < t_res: ct = FREEZE_AT
    else: ct = FREEZE_AT + (t - t_res)
    cx = 1230; z = 1.0
    if FREEZE_AT <= t < t_res + 0.2: z = lerp(1.0, 1.1, eio((t - FREEZE_AT) / 0.8)) if t < t_res else lerp(1.1, 1.0, eio((t - t_res) / 0.2))
    u = eio((t - ws('turned') - 0.05) / 1.3) if t > ws('turned') else 0.0
    fz = eio((t - FREEZE_AT) / 0.8) if FREEZE_AT <= t < t_res else (1 - eio((t - t_res) / 0.3) if t_res <= t < t_res + 0.3 else 0.0)
    cx = lerp(1230, 540, u) + 45 * fz
    can, m = film(ct, cx, 540 + 50 * fz, z)
    if FREEZE_AT <= t < t_res + 0.25:   # frozen frame: a touch of desaturation, the words written on the document, an arrow onto it
        out = 1 - clamp((t - t_res) / 0.25)
        t1 = ws("Japan's") - 0.1; t2 = ws('surrender') - 0.05
        if t > t1: on_quad(can, [m(*p) for p in DOC1], "JAPAN'S", 120, out, INK, anton(120), eio((t - t1) / 0.35), 0.7, mod=0.35, op=0.92)
        if t > t2: on_quad(can, [m(*p) for p in DOC2], 'SURRENDER', 120, out, RED, anton(120), eio((t - t2) / 0.4), 0.7, mod=0.3, op=0.95)
        if t > FREEZE_AT + 0.15:
            tip = m(1240, 735); arrow_to(can, (tip[0] - 160, tip[1] - 330), (tip[0] - 15, tip[1] - 25), eio((t - FREEZE_AT - 0.15) / 0.35) * out)
    if t > ws('thin') - 0.1 and t < ws('Three') - 0.1:   # ring on the thin general as he takes the pen
        p = m(400, 260); ring(can, t, ws('thin') - 0.1, p[0], p[1], YEL, 60, False)
    return can
def s_then(t, w0, w1):   # w09, pre-war portrait: 'three years earlier'
    can = grade(fit('w09', t, w0, w1, 1.06)); shade(can, 220, 0.5)
    stamp(can, t, ws('surrendered', 10) - 0.03, 'SURRENDERED 1942', (CX, 1330), 86, -6)
    return can
def s_name(t, w0, w1):   # w08, the name
    can = grade(fit('w08', t, w0, w1, 1.06)); shade(can, 220, 0.5)
    title(can, t, ws('Jonathan'), 'JONATHAN', 1150, 120, CREAM, bold=1)
    title(can, t, ws('Wainwright'), 'WAINWRIGHT', 1290, 150, YEL, bold=1)
    return can
def s_pt(t, w0, w1):   # PT boat (MacArthur leaves), 'MARCH 1942' in the grey sky
    ct = 9.7 + (t - w0) * 0.95; can, m = film(min(ct, 17.4), 960, 540, 1.0, 1.0)
    sky(can, t, ws('March'), 'MARCH 1942', CX, 420, 130, CREAM, None, 0.5)
    return can
def s_command(t, w0, w1):   # w01, the two men in 1941: names on the sky with pointers
    can, m = side('w01', 700, 820, t, w0, w1, 1.04); shade(can, 200, 0.55)
    tt = ws('Wainwright', w0 - 0.5)
    if t > tt: f = m(1030, 260); ring(can, t, tt, f[0], f[1], YEL, 95, False)
    return can
def s_corr(t, w0, w1):   # the island under fire
    ct = 20.85 + (t - w0) * 0.72; can, m = film(min(ct, 22.9), 900, 540, 1.0)
    sky(can, t, ws('Corregidor'), 'CORREGIDOR', CX, 470, 130, CREAM, None, 0.5)
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
    t2 = ws('air', w0)
    if t > t2 - 0.25: on_quad(can, [m(*p) for p in CAB03], 'ON AIR', 130, clamp((t - t2 + 0.25) / 0.06), RED, anton(130), eio((t - t2 + 0.25) / 0.35), 0.8, mod=0.25, op=0.95, glow=((200, 30, 30), 14, 0.55))
    return can
CAB03 = [(1560, 340), (1890, 335), (1892, 470), (1562, 476)]   # back wall right of his head
def s_pow(t, w0, w1):   # w05, the gaunt general: POW on the wall behind him
    can = grade(fit('w05', t, w0, w1, 1.05)); shade(can, 210, 0.5)
    q = lambda x, y: fitpt('w05', t, w0, w1, 1.05, x, y); t1 = ws('prisoner', w0 - 0.5)
    if t > t1 - 0.2: on_quad(can, [q(*p) for p in WALL05], 'P.O.W.', 150, clamp((t - t1 + 0.2) / 0.06), CREAM, anton(150), eio((t - t1 + 0.2) / 0.4), 1.0, mod=0.35, op=0.9, glow=((8, 8, 8), 10, 0.6))
    return can
WALL05 = [(260, 430), (660, 420), (665, 640), (262, 655)]
PAC = Map(124.5, 29.6, 38, hi=('Philippines',))
def s_map(t, w0, w1):   # camp to camp: Corregidor, Tarlac, Formosa, Manchuria
    z = lerp(1.0, 1.04, prog(t, w0, w1)); can = grade(PAC.frame(z), 0.1, 1.0); p = lambda lon, lat: PAC.p(lon, lat, z)
    stops = [('CORREGIDOR', 120.57, 14.38, ws('more', w0 - 0.5)), ('FORMOSA', 121.6, 23.97, ws('camp', w0 - 0.5)), ('MANCHURIA', 125.1, 42.9, ws('Manchuria', w0 - 0.5))]
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
    q = lambda x, y: fitpt('w07', t, w0, w1, 1.05, x, y); t1 = ws('gave', w0)
    if t > t1 - 0.1: on_quad(can, [q(*p) for p in WALL07], 'GAVE UP?', 120, clamp((t - t1 + 0.1) / 0.06), INK, anton(120), eio((t - t1 + 0.1) / 0.35), 0.8, mod=0.35, op=0.92)
    return can
WALL07 = [(1150, 480), (1460, 468), (1464, 600), (1153, 612)]
def s_free(t, w0, w1):   # the general saluting at the aircraft, August 1945
    ct = 36.0 + (t - w0) * 0.85; can, m = film(min(ct, 38.9), 1000, 560, 1.0, 1.0)
    title(can, t, ws('August', w0 - 0.5), 'AUGUST 1945', 420, 110, CREAM)
    stamp(can, t, ws('freed', w0) - 0.03, 'FREED', (CX, 1300), 120, -6, None, YEL)
    return can
def s_missouri_date(t, w0, w1):   # w10, the reunion with MacArthur, two days before the ceremony
    can, m = side('w10', 500, 380, t, w0, w1, 1.04); shade(can, 200, 0.55)
    title(can, t, ws('Two', w0 - 0.5), 'SEPTEMBER 2, 1945', 1180, 92, CREAM)
    title(can, t, ws('USS', w0 - 0.5), 'USS MISSOURI', 1310, 120, YEL)
    return can
def s_medal(t, w0, w1):   # w02, Truman pins the medal; then BLOCKED 1942
    can, m = side('w02', 1100, 700, t, w0, w1, 1.04); shade(can, 200, 0.55)
    title(can, t, ws('Medal', w0 - 0.5), 'MEDAL OF HONOR', 1180, 104, YEL, ws('award', w0) - 0.15)
    stamp(can, t, ws('blocked', w0) - 0.03, 'BLOCKED IN 1942', (CX, 1300), 92, -6)
    return can
def s_end(t, w0, w1):   # back on the Missouri, MacArthur signing again: Japan does the same
    ct = 7.35 + (t - w0) * 0.5; can, m = film(min(ct, 9.45), 1150, 560, lerp(1.0, 1.08, prog(t, w0, w1)))
    title(can, t, ws('watched', w0 - 0.5), 'JAPAN SURRENDERS', 1300, 110, YEL)
    return can

ANCH = [
 (0.0, s_sign, None),
 (ws('Three') - 0.1, s_then, ('fade',)),
 (ws('His', 11) - 0.1, s_name, ('fade',)),
 (ws('In', 13.5) - 0.1, s_pt, ('whip', 1)),
 (ws('and', 17) - 0.1, s_command, ('fade',)),
 (ws('On', 19.5) - 0.1, s_corr, ('whip', -1)),
 (ws('under', 22) - 0.1, s_ships, ('fade',)),
 (ws('Then', 24.5) - 0.1, s_beach, ('fade',)),
 (ws('The', 28) - 0.1, s_radio, ('fade',)),
 (ws('He', 33) - 0.1, s_pow, ('fade',)),
 (ws('For', 36) - 0.1, s_map, ('fade',)),
 (ws('afraid', 40) - 0.1, s_fear, ('fade',)),
 (ws('In', 44) - 0.1, s_free, ('whip', 1)),
 (ws('Two', 47.5) - 0.1, s_missouri_date, ('fade',)),
 (ws('Weeks', 51) - 0.1, s_medal, ('fade',)),
 (ws('The', 56.5) - 0.1, s_end, ('fade',))]
