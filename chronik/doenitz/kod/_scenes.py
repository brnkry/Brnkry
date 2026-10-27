# ================= Karl Dönitz scenes =================
def ws(word, after=0.0): return wt(word, after) - 0.05

# ---------- archive films: 640x480 newsreels shown in a framed panel over a blurred copy of themselves ----------
SEG = {'adm_d': 81, 'adm_p': 104, 'adm_s': 259, 'fr_sp': 183, 'fr_a': 241, 'fr_rel': 180, 'nu': 1531}
CROP = {'adm_d': (40, 0, 560, 390), 'adm_p': (0, 0, 620, 465), 'adm_s': (10, 0, 630, 465), 'fr_sp': (12, 8, 555, 415), 'fr_a': (12, 8, 555, 415), 'fr_rel': (12, 8, 555, 415), 'nu': (0, 0, 640, 480)}   # Pathé logo, name supers and black edges stay outside
TRK = {int(k): v for k, v in json.load(open(B + 'clip/adm_d_track.json')).items()}
def _soft(im, x, y, d):
    r = d / 2; bx = (int(x - d), int(y - d), int(x + d), int(y + d)); reg = im.crop(bx)
    bl = reg.resize((max(1, reg.width // 8), max(1, reg.height // 8)), Image.BILINEAR).resize(reg.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(d * 0.12))
    mk = Image.new('L', reg.size, 0); c = reg.width / 2; ImageDraw.Draw(mk).ellipse((c - r, c - r, c + r, c + r), fill=255)
    im.paste(Image.composite(bl, reg, mk.filter(ImageFilter.GaussianBlur(r * 0.2))), bx[:2])
@functools.lru_cache(maxsize=24)
def ff(k, i):
    i = max(1, min(SEG[k], i)); im = Image.open(B + 'clip/%s/%05d.jpg' % (k, i)).convert('RGB')
    if k == 'adm_d': x, y, _ = TRK[i]; _soft(im, x, y - 16, 56)   # Dönitz's cap eagle, tracked
    return im.crop(CROP[k])
def fat(k, ct): return ff(k, int(round(ct * FPS)) + 1)
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
        if ov: ov(can, t, w0, w1)
        return can
    return fn

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

# ---------- scenes ----------
TOP = 330
def o_hook(can, t, w0, w1):
    title(can, t, ws('Hitlers'), 'HITLERS', 1190, 120, CREAM, None, bold=1)
    title(can, t, ws('Nachfolger'), 'NACHFOLGER', 1335, 150, YEL, None, bold=1)
def o_school(can, t, w0, w1):
    title(can, t, ws('achtzehn'), '18 JAHRE SPÄTER', TOP, 104, CREAM)
    stamp(can, t, ws('Schulklasse'), '1963', (790, 1330), 92, -8)
def s_school(t, w0, w1):
    can = card(src('p01'), t, w0, w1, 1.0, 1.12, 0.62, 0.45, 0.1); o_school(can, t, w0, w1); return can
def s_name(t, w0, w1):
    can = grade(fit('p08', t, w0, w1, 1.07)); shade(can, 230, 0.5)
    title(can, t, ws('Karl', 4.5), 'KARL', 1150, 120, CREAM, None, bold=1)
    title(can, t, ws('Dönitz', 5), 'DÖNITZ', 1310, 210, YEL, None, bold=2)
    return can
def o_cmd(can, t, w0, w1):
    title(can, t, ws('Befehlshaber'), 'BEFEHLSHABER', TOP - 40, 100, CREAM)
    title(can, t, ws('U-Boote'), 'DER U-BOOTE', TOP + 70, 100, YEL)
def o_crew(can, t, w0, w1):
    z = ws('Zehntausende')
    title(can, t, w0 + 0.05, 'BEFEHLSHABER', TOP - 40, 100, CREAM, z - 0.1)
    title(can, t, w0 + 0.05, 'DER U-BOOTE', TOP + 70, 100, YEL, z - 0.1)
    title(can, t, z, 'ZEHNTAUSENDE', TOP - 40, 110, YEL)
    title(can, t, ws('junge', 9), 'JUNGE MÄNNER', TOP + 70, 100, CREAM)
def o_sink(can, t, w0, w1):
    title(can, t, w0 + 0.05, 'ATLANTIK', TOP, 120, CREAM)
    stamp(can, t, ws('nie', 11), '3 VON 4 STARBEN', (CX, 1330), 74, -6)
def s_test(t, w0, w1):
    can = grade(fit('p05', t, w0, w1, 1.05, blur=10)); dim(can, 120)
    l = [('POLITISCHES TESTAMENT', 52, INK, w0 + 0.25), ('Berlin, 29. April 1945', 34, (90, 80, 70), w0 + 0.6), ('', 20, INK, 0),
         ('Ich ernenne daher', 42, INK, ws('ernannte')), ('Großadmiral Dönitz', 54, INK, ws('Hitler', 13.5)), ('zum Reichspräsidenten', 50, RED, ws('Reichspräsidenten'))]
    p = sheet(can, t, w0 + 0.05, l, CX, 900, 900)
    if p and t > ws('Reichspräsidenten') + 0.5:
        u = eio((t - ws('Reichspräsidenten') - 0.5) / 0.35); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x0, x1, y = 250, 830, 1140
        ImageDraw.Draw(L).line((x0, y, lerp(x0, x1, u), y - 8 * u), fill=RED + (230,), width=8); can.alpha_composite(L)
    return can
MP = Map(11.2, 53.9, 7.4)
def s_map(t, w0, w1):
    z = lerp(1.0, 1.06, prog(t, w0, w1)); can = grade(MP.frame(z), 0.08, 1.0); p = lambda lo, la: MP.p(lo, la, z)
    for nm, lo, la in (('DÄNEMARK', 9.6, 55.9), ('NORDSEE', 8.2, 54.15), ('OSTSEE', 12.9, 54.9)):
        x, y = p(lo, la); title(can, t, w0 + 0.3, nm, y, 46, (140, 150, 168), None, 'bebas', x)
    xb, yb = p(13.4, 52.52); dot(can, xb, yb, GREY, 9); title(can, t, w0 + 0.4, 'BERLIN', yb + 50, 50, GREY, None, 'bebas', xb)
    xf, yf = p(9.45, 54.80); dot(can, xf, yf, YEL, 12); ring(can, t, ws('Flensburg'), xf, yf, YEL, 34, False)
    title(can, t, ws('Flensburg'), 'FLENSBURG-MÜRWIK', yf - 70, 64, YEL, None, 'bebas', max(xf, 250))
    ring(can, t, ws('kaum'), xb, yb, RED, 30, True)
    title(can, t, ws('drei', 17.5), '3 WOCHEN', TOP, 130, CREAM)
    title(can, t, ws('regierte'), 'REGIERUNG DÖNITZ', yf + 64, 56, CREAM, None, 'bebas', max(xf, 250))
    return can
def o_arrest(can, t, w0, w1):
    title(can, t, ws('Am', 20.5), '23. MAI 1945', TOP, 120, CREAM)
    title(can, t, ws('britische'), 'BRITISCHE SOLDATEN', 1330, 70, CREAM, None, 'bebas')
def o_p13(can, t, w0, w1):
    stamp(can, t, ws('verhaftet'), 'VERHAFTET', (CX, 1300), 110, -7)
def o_nu(can, t, w0, w1):
    title(can, t, ws('Nürnberg'), 'NÜRNBERG 1946', TOP, 120, CREAM)
    stamp(can, t, ws('zehn', 29), '10 JAHRE HAFT', (CX, 1330), 88, -6)
def o_sp(can, t, w0, w1):
    title(can, t, w0 + 0.05, 'SPANDAU', TOP, 130, CREAM)
def o_rel(can, t, w0, w1):
    title(can, t, w0 + 0.05, 'SPANDAU', TOP, 130, CREAM, ws('Tag', 32) - 0.1)
    title(can, t, ws('Tag', 32), 'FREI: OKTOBER 1956', TOP, 100, YEL)
def o_63(can, t, w0, w1):
    title(can, t, ws('Januar'), 'JANUAR 1963', TOP, 120, CREAM)
    title(can, t, ws('Gymnasium'), 'GYMNASIUM', 1240, 70, CREAM, None, 'bebas')
    title(can, t, ws('Geesthacht'), 'GEESTHACHT', 1330, 110, YEL)
def o_bar(can, t, w0, w1):
    title(can, t, ws('Schülersprecher'), 'SCHÜLERSPRECHER', TOP, 100, CREAM)
    hand(can, t, ws('Uwe'), 'Uwe Barschel', (CX, 1180), 120, CREAM, 0.7)
    title(can, t, ws('später', 41), 'SPÄTER MINISTERPRÄSIDENT', 1330, 64, YEL, None, 'anton', CX, 820)
    title(can, t, ws('Schleswig-Holstein'), 'VON SCHLESWIG-HOLSTEIN', 1410, 54, CREAM, None, 'bebas')
def o_talk(can, t, w0, w1):
    title(can, t, ws('Krieg', 46), 'ÜBER DEN KRIEG', TOP, 110, CREAM)
    b1 = hand(can, t, ws('Kritik'), 'Kritik?', (330, 1270), 120, CREAM, 0.5)
    if b1: strike(can, t, ws('Kritik') + 0.5, b1)
    b2 = hand(can, t, ws('Reue'), 'Reue?', (760, 1270), 120, CREAM, 0.5)
    if b2: strike(can, t, ws('Reue') + 0.45, b2)
def o_clap(can, t, w0, w1):
    title(can, t, ws('applaudierten'), 'APPLAUS', TOP, 140, YEL)
    drop(can, t, ws('Lokalzeitung'), 'LOKALZEITUNG', (CX, 1150), -3, 760, 'JANUAR 1963', 2)
def s_press(t, w0, w1, dark=0.0):
    can = grade(fit('p11c', t, w0, w1, 1.04, 0.0, 9)); dim(can, 110 + 120 * dark)
    drop(can, t, ws('Spiegel'), 'DER SPIEGEL', (450, 640), -6, 720, None, 3)
    drop(can, t, ws('Zeit', 54.5), 'DIE ZEIT', (640, 910), 5, 720, None, 4)
    drop(can, t, ws('Monde'), 'LE MONDE', (450, 1180), -3, 720, None, 5)
    if dark == 0: stamp(can, t, ws('empört'), 'EMPÖRUNG', (CX, 1300), 130, -8)
    return can
def s_head(t, w0, w1):
    can = s_press(t, w0 - 5, w1, 1.0)
    title(can, t, ws('Schulleiter'), 'DER SCHULLEITER', TOP, 110, CREAM)
    title(can, t, ws('Druck', 59.5), 'UNTER DRUCK', 1300, 120, RED)
    k = eio((t - ws('Leben', 61)) / 0.8)
    if k > 0: dim(can, 170 * k)
    return can
def o_end(can, t, w0, w1):
    title(can, t, ws('Dönitz', 62), 'KARL DÖNITZ', 1090, 110, CREAM, None, bold=1)
    title(can, t, ws('1980'), 'GESTORBEN 1980', 1220, 96, YEL)
    stamp(can, t, ws('Rolle', 65), 'OHNE REUE', (CX, 1375), 100, -6)

ANCH = [
 (0.0, S_('p06', 160, 420, 1.06, o_hook), None),
 (ws('achtzehn') - 0.1, s_school, ('whip', 1)),
 (ws('Sein') - 0.1, s_name, ('fade',)),
 (ws('Als', 6) - 0.1, FL('adm_d', 0.9, 0.9, 1.15, 1.25, 0.45, 0.4, o_cmd), ('whip', -1)),
 (ws('U-Boote') - 0.15, FL('adm_p', 0.1, 1.0, 1.0, 1.08, 0.5, 0.45, o_crew), ('fade',)),
 (ws('Atlantik') - 0.15, FL('adm_s', 1.0, 1.0, 1.0, 1.1, 0.5, 0.55, o_sink), ('fade',)),
 (ws('In', 12.3) - 0.1, s_test, ('fade',)),
 (ws('Von', 15.4) - 0.1, s_map, ('whip', 1)),
 (ws('Am', 20.5) - 0.1, FL('fr_a', 0.0, 1.0, 1.0, 1.06, 0.55, 0.5, o_arrest), ('fade',)),
 (ws('Dönitz', 25) - 0.1, S_('p13', 700, 830, 1.05, o_p13), ('fade',)),
 (ws('In', 28) - 0.1, FL('nu', 37.6, 1.0, 1.55, 1.75, 0.53, 0.3, o_nu), ('whip', -1)),
 (ws('Spandau') - 0.1, FL('fr_sp', 4.55, 1.0, 1.0, 1.08, 0.5, 0.55, o_sp), ('fade',)),
 (ws('letzten', 32) - 0.15, FL('fr_rel', 4.0, 1.0, 1.15, 1.25, 0.6, 0.35, o_rel), ('fade',)),
 (ws('Im', 33.5) - 0.1, S_('p01', 1820, 1880, 1.05, o_63), ('whip', 1)),
 (ws('Organisiert') - 0.1, S_('p01', 60, 160, 1.06, o_bar), ('fade',)),
 (ws('Dönitz', 44) - 0.1, S_('p01', 1300, 900, 1.04, o_talk), ('fade',)),
 (ws('Lehrer', 49.5) - 0.1, S_('p01', 900, 650, 1.04, o_clap), ('fade',)),
 (ws('Dann', 53.3) - 0.1, s_press, ('whip', -1)),
 (ws('Der', 58.6) - 0.1, s_head, ('fade',)),
 (ws('Dönitz', 62) - 0.15, S_('p10', 40, 260, 1.06, o_end), ('fade',))]
