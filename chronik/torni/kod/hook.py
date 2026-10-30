# Lauri Törni long video: first 30 seconds as a sample (1920x1080, no voice), channel colours and fonts
import sys, math, json, functools, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D = sys.argv[1] + '/'; S = D + '../'; F = S + 'sch/fonts/'
W, H, FPS, T = 1920, 1080, 30, 30.0
YEL, RED, WHITE, DARK, CREAM = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18), (232, 226, 210)
@functools.lru_cache(None)
def anton(s): return ImageFont.truetype(F + 'Anton-Regular.ttf', s)
@functools.lru_cache(None)
def bebas(s): return ImageFont.truetype(F + 'BebasNeue-Regular.ttf', s)
@functools.lru_cache(None)
def typew(s): return ImageFont.truetype(F + 'SpecialElite-Regular.ttf', s)
def clamp(x): return max(0.0, min(1.0, x))
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def lerp(a, b, u): return a + (b - a) * u

# ---------- photos ----------
BLUR = {'t22': [(836, 258, 80), (900, 466, 130), (705, 1735, 240)]}   # cap eagle with swastika, skull, SS collar runes
@functools.lru_cache(None)
def src(n):
    im = Image.open(D + 'img/' + n + '.jpg').convert('RGB')
    for x, y, d in BLUR.get(n, []):
        r = d / 2; box = (int(x - d), int(y - d), int(x + d), int(y + d)); reg = im.crop(box)
        bl = reg.resize((max(1, reg.width // 14), max(1, reg.height // 14)), Image.BILINEAR).resize(reg.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(d * 0.12))
        m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).ellipse((reg.width / 2 - r, reg.height / 2 - r, reg.width / 2 + r, reg.height / 2 + r), fill=255)
        im.paste(Image.composite(bl, reg, m.filter(ImageFilter.GaussianBlur(r * 0.25))), box[:2])
    return im
def cam(n, cx, cy, w, ow=W, oh=H):
    """crop of width w (source px) at centre cx, cy with the output aspect"""
    im = src(n); w = min(w, im.width, im.height * ow / oh); h = w * oh / ow
    x0 = min(max(cx - w / 2, 0), im.width - w); y0 = min(max(cy - h / 2, 0), im.height - h)
    return im.resize((ow, oh), Image.BILINEAR, box=(x0, y0, x0 + w, y0 + h)).convert('RGBA')
def move(n, t, t0, t1, a, b, ow=W, oh=H):
    """constant-speed move from a=(cx, cy, w) to b over the whole time the shot is on screen"""
    u = clamp((t - t0) / (t1 - t0)); return cam(n, lerp(a[0], b[0], u), lerp(a[1], b[1], u), math.exp(lerp(math.log(a[2]), math.log(b[2]), u)), ow, oh)
def grade(im, dark=0.0):
    im = ImageEnhance.Contrast(im).enhance(1.06)
    if dark: im.alpha_composite(Image.new('RGBA', im.size, (6, 7, 9, int(255 * dark))))
    return im
def bottom_shade(im, a=200):
    g = np.clip((np.arange(H) - H * 0.45) / (H * 0.55), 0, 1) ** 1.4 * a
    L = Image.fromarray(np.repeat(g[:, None], W, 1).astype(np.uint8)); S_ = Image.new('RGBA', (W, H), (6, 7, 9, 0)); S_.putalpha(L); im.alpha_composite(S_); return im

# ---------- text ----------
def shadowed(can, draw_fn, blur=12, off=(4, 8), a=200):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(L))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, a), (0, 0), L.getchannel('A'))
    can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), off); can.alpha_composite(L)
def fade_text(can, t, t0, xy, s, font, col, dur=0.45, rise=18, anchor='mm', t1=None):
    if t < t0: return
    k = eout((t - t0) / dur); out = 1.0 if t1 is None else 1 - clamp((t - t1) / 0.35)
    a = int(255 * k * out)
    if a > 2: shadowed(can, lambda d: d.text((xy[0], xy[1] + (1 - k) * rise), s, font=font, fill=col + (a,), anchor=anchor))
def plate(can, t, t0, xy, s, font, bg=YEL, fg=DARK, pad=(26, 12), t1=None, rule=False):
    if t < t0: return
    k = eout((t - t0) / 0.4); out = 1.0 if t1 is None else 1 - clamp((t - t1) / 0.35)
    d0 = ImageDraw.Draw(can); b = d0.textbbox(xy, s, font=font, anchor='mm'); cx = (b[0] + b[2]) / 2; hw = (b[2] - b[0]) / 2 + pad[0]
    def dr(d):
        d.rectangle((cx - hw * k, b[1] - pad[1] - 4, cx + hw * k, b[3] + pad[1]), fill=bg + (int(255 * out),))
        if k > 0.6: d.text(xy, s, font=font, fill=fg + (int(255 * out * clamp((k - 0.6) / 0.4)),), anchor='mm')
        if rule and k > 0.9: d.rectangle((cx - hw, b[3] + pad[1] + 14, cx - hw + (b[3] - b[1]) * 1.2, b[3] + pad[1] + 22), fill=RED + (int(255 * out),))
    shadowed(can, dr, 10, (4, 6), 170)
def typewriter(can, t, t0, xy, s, font, col, step=0.07, t1=None):
    if t < t0: return
    n = min(len(s), int((t - t0) / step) + 1); out = 1.0 if t1 is None else 1 - clamp((t - t1) / 0.35)
    shown = s[:n]; cur = '_' if n < len(s) and int(t * 4) % 2 == 0 else ''
    x = xy[0] - font.getlength(s) / 2
    shadowed(can, lambda d: d.text((x, xy[1]), shown + cur, font=font, fill=col + (int(255 * out),), anchor='lm'))
def name_title(can, t, t0, cy, white, yellow, size):
    """CHRONIK [DER MACHT] look: white word, then word on a yellow plate, red rule"""
    if t < t0: return
    f = anton(size); k = eout((t - t0) / 0.5)
    w1 = f.getlength(white); w2 = f.getlength(yellow); gap, pad = size * 0.26, size * 0.18; x0 = W / 2 - (w1 + gap + w2 + 2 * pad) / 2
    def dr(d):
        d.text((x0 - (1 - k) * 60, cy), white, font=f, fill=WHITE + (int(255 * k),), anchor='lm')
        b = d.textbbox((x0 + w1 + gap + pad, cy), yellow, font=f, anchor='lm'); kk = eout((t - t0 - 0.15) / 0.45)
        if kk > 0:
            d.rectangle((b[0] - pad, b[1] - size * 0.16, b[0] - pad + (b[2] - b[0] + 2 * pad) * kk, b[3] + size * 0.14), fill=YEL + (255,))
            if kk > 0.7: d.text((x0 + w1 + gap + pad, cy), yellow, font=f, fill=DARK + (int(255 * clamp((kk - 0.7) / 0.3)),), anchor='lm')
            d.rectangle((b[0] - pad, b[3] + size * 0.2, b[0] - pad + size * 1.2 * kk, b[3] + size * 0.27), fill=RED + (255,))
    shadowed(can, dr)

# ---------- map (dark channel style) ----------
GJ = json.load(open(S + 'sch/ne50.geojson'))
def merc(lat): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
POLY = []
for ft in GJ['features']:
    nm = ft['properties'].get('ADMIN') or ft['properties'].get('NAME'); g = ft['geometry']
    for poly in (g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]):
        rg = np.array(poly[0])
        if rg[:, 0].max() < 90 or rg[:, 0].min() > 125 or rg[:, 1].max() < 0 or rg[:, 1].min() > 30: continue
        POLY.append((nm, np.stack([rg[:, 0], [merc(v) for v in rg[:, 1]]], 1)))
SEA, LAND, LAND_HI, BORDER = (9, 12, 17), (34, 40, 50), (60, 54, 26), (88, 100, 116)
MC = (107.5, 15.85); MSPAN = 6.0          # lon span shown at zoom 1
@functools.lru_cache(None)
def map_base():
    s = 2; w, h = W * s, H * s; sc = w / MSPAN; im = Image.new('RGB', (w, h), SEA); d = ImageDraw.Draw(im)
    for lon in range(100, 116): x = (lon - MC[0]) * sc + w / 2; d.line((x, 0, x, h), fill=(15, 20, 27), width=2)
    for lat in range(5, 26): y = h / 2 - (merc(lat) - merc(MC[1])) * sc; d.line((0, y, w, y), fill=(15, 20, 27), width=2)
    for nm, xy in POLY:
        pts = [((x - MC[0]) * sc + w / 2, h / 2 - (y - merc(MC[1])) * sc) for x, y in xy]
        d.polygon(pts, fill=LAND_HI if nm == 'Vietnam' else LAND); d.line(pts + [pts[0]], fill=BORDER, width=3)
    return im.resize((W, H), Image.LANCZOS)
def P(lon, lat, z=1.0):   # map coords -> screen, map zoomed by z around the centre
    sc = W / MSPAN; x = (lon - MC[0]) * sc + W / 2; y = H / 2 - (merc(lat) - merc(MC[1])) * sc
    return (W / 2 + (x - W / 2) * z, H / 2 + (y - H / 2) * z)
def map_frame(z):
    b = map_base(); cw, ch = W / z, H / z
    return b.resize((W, H), Image.BILINEAR, box=(W / 2 - cw / 2, H / 2 - ch / 2, W / 2 + cw / 2, H / 2 + ch / 2)).convert('RGBA')
def dot(can, x, y, col=YEL, r=11, a=1.0):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse((x - r * 2.4, y - r * 2.4, x + r * 2.4, y + r * 2.4), fill=col + (int(60 * a),)); L = L.filter(ImageFilter.GaussianBlur(r)); d = ImageDraw.Draw(L)
    d.ellipse((x - r, y - r, x + r, y + r), fill=col + (int(255 * a),)); can.alpha_composite(L)
def label(can, t, t0, x, y, s, size=46, col=WHITE, anchor='lm'):
    fade_text(can, t, t0, (x, y), s, bebas(size), col, 0.35, 8, anchor)
def dashed(can, pts, u, col=YEL, w=7, seg=22):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    tot = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)); goal = tot * u; acc = 0; on = True; run = 0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]; L_ = math.dist(a, b); s = 0
        while s < L_ and acc + s < goal:
            e = min(L_, s + seg, goal - acc); p0 = (lerp(a[0], b[0], s / L_), lerp(a[1], b[1], s / L_)); p1 = (lerp(a[0], b[0], e / L_), lerp(a[1], b[1], e / L_))
            if on: d.line((p0, p1), fill=col + (255,), width=w)
            on = not on; s = e
        acc += L_
    can.alpha_composite(L)
    if goal > 0 and len(pts) > 1:   # arrow head at the current tip
        ang = math.atan2(pts[-1][1] - pts[0][1], pts[-1][0] - pts[0][0]); tip = (lerp(pts[0][0], pts[-1][0], u), lerp(pts[0][1], pts[-1][1], u)); s = 30
        ImageDraw.Draw(can).polygon([tip, (tip[0] - s * math.cos(ang - .45), tip[1] - s * math.sin(ang - .45)), (tip[0] - s * math.cos(ang + .45), tip[1] - s * math.sin(ang + .45))], fill=col)
def pulse_ring(can, t, t0, x, y, col=RED, r=40):
    if t < t0: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); k = eout((t - t0) / 0.4)
    for j in range(3):
        u = ((t - t0) * 0.7 + j / 3) % 1.0; rr = r + 90 * u; d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=col + (int(200 * (1 - u) * k),), width=5)
    d.ellipse((x - r * k, y - r * k, x + r * k, y + r * k), outline=col + (255,), width=8)
    d.line((x - r * 0.45 * k, y - r * 0.45 * k, x + r * 0.45 * k, y + r * 0.45 * k), fill=col + (255,), width=8); d.line((x - r * 0.45 * k, y + r * 0.45 * k, x + r * 0.45 * k, y - r * 0.45 * k), fill=col + (255,), width=8)
    can.alpha_composite(L)

# ---------- scenes ----------
def sc_jungle(t, w0, w1):    # 18. Oktober 1965, Vietnam
    can = bottom_shade(grade(move('t16', t, w0, w1, (1300, 900, 2300), (1150, 860, 1900)), 0.25), 220)
    typewriter(can, t, 0.7, (W / 2, 800), '18. OKTOBER 1965', typew(84), CREAM, 0.08)
    plate(can, t, 2.3, (W / 2, 925), 'VIETNAM', anton(70), rule=True)
    return can
def sc_map(t, w0, w1):       # the helicopter disappears
    z = lerp(1.0, 1.25, eio((t - w0) / (w1 - w0))); can = map_frame(z)
    kd, dn, laos, crash = P(107.80, 15.45, z), P(108.22, 16.07, z), P(107.05, 15.62, z), P(107.93, 15.78, z)
    dot(can, *dn, WHITE, 9); label(can, t, w0 + 0.3, dn[0] + 24, dn[1] - 4, 'DA NANG', 60)
    if t > 5.7: dot(can, *kd, YEL, 11, clamp((t - 5.7) / 0.3)); label(can, t, 5.7, kd[0] + 28, kd[1] + 4, 'KHAM DUC', 62, YEL)
    if t > 6.4: dashed(can, [kd, laos], eio((t - 6.4) / 1.2))
    label(can, t, 6.2, laos[0] - 30, laos[1] - 80, 'LAOS', 84, (190, 196, 204), 'rm')
    pulse_ring(can, t, 7.7, *crash)
    if t > 8.0: label(can, t, 8.0, crash[0] - 70, crash[1] - 80, 'VERSCHOLLEN', 72, RED, 'rm')
    plate(can, t, w0 + 0.4, (W / 2, 130), 'EIN HUBSCHRAUBER VERSCHWINDET', bebas(84), DARK, WHITE)
    label(can, t, w0 + 0.8, *P(108.0, 14.6, z), 'VIETNAM', 70, (150, 140, 90), 'mm')
    return can
def sc_thorne(t, w0, w1):    # Hauptmann Larry Thorne
    can = bottom_shade(grade(move('t18', t, w0, w1, (896, 640, 1792), (896, 600, 1560))), 230)
    name_title(can, t, 10.8, 830, 'LARRY', 'THORNE', 150)
    fade_text(can, t, 11.6, (W / 2, 990), 'HAUPTMANN DER US SPECIAL FORCES', bebas(64), CREAM)
    return can
def sc_years(t, w0, w1):     # 34 Jahre später
    can = grade(move('t10', t, w0, w1, (1400, 768, 2752), (1300, 760, 2300)), 0.62).filter(ImageFilter.GaussianBlur(3))
    k = eio((t - 15.2) / 1.8); year = int(round(lerp(1965, 1999, k)))
    shadowed(can, lambda d: d.text((W / 2, 470), str(year), font=anton(300), fill=WHITE + (255,), anchor='mm'))
    plate(can, t, 17.1, (W / 2, 720), '34 JAHRE SPÄTER', anton(80), rule=True)
    fade_text(can, t, 17.7, (W / 2, 850), 'WIRD DIE ABSTURZSTELLE GEFUNDEN', bebas(60), CREAM)
    return can
TRI = [('t06', 'FINNLAND', 19.4, (896, 900, 1792)), ('t22', 'WAFFEN-SS', 20.5, (896, 1150, 1792)), ('t21', 'USA', 21.6, (896, 900, 1792))]
def sc_three(t, w0, w1):     # three uniforms
    can = Image.new('RGBA', (W, H), DARK + (255,)); pw = W // 3
    for i, (n, lab, ti, c) in enumerate(TRI):
        if t < ti: continue
        k = eout((t - ti) / 0.5); drift = (t - ti) * 12
        ph = cam(n, c[0], c[1] - drift, c[2], pw, H)
        can.alpha_composite(ph, (i * pw, int((1 - k) * H * 0.6)))
        if i: ImageDraw.Draw(can).line((i * pw, 0, i * pw, H), fill=DARK, width=8)
        plate(can, t, ti + 0.35, (i * pw + pw / 2, 930), lab, anton(64), YEL if i != 1 else WHITE, DARK)
    bottom_shade(can, 120)
    plate(can, t, 23.0, (W / 2, 120), 'DREI UNIFORMEN', anton(84), DARK, WHITE)
    return can
def sc_name(t, w0, w1):      # Lauri Törni
    can = bottom_shade(grade(move('t09', t, w0, w1, (1250, 760, 1900), (1220, 700, 1350))), 230)
    fade_text(can, t, 25.9, (W / 2, 745), 'IN SEINER HEIMAT HIESS ER', bebas(66), CREAM, t1=None)
    name_title(can, t, 26.7, 890, 'LAURI', 'TÖRNI', 160)
    return can

SCN = [(0.0, sc_jungle), (5.0, sc_map), (10.2, sc_thorne), (14.6, sc_years), (19.0, sc_three), (25.2, sc_name)]
OV = 0.4
SC = [(0 if i == 0 else s - OV, T if i == len(SCN) - 1 else SCN[i + 1][0] + OV, fn) for i, (s, fn) in enumerate(SCN)]
y_, x_ = np.mgrid[0:H, 0:W]; rr = np.sqrt(((x_ - W / 2) / (W * 0.62)) ** 2 + ((y_ - H / 2) / (H * 0.62)) ** 2)
VIG = Image.new('RGBA', (W, H), (0, 0, 0, 0)); VIG.putalpha(Image.fromarray((np.clip(rr - 0.6, 0, 1) * 1.5 ** 1 * 170).clip(0, 255).astype(np.uint8)))
rng = np.random.default_rng(3)
def frame(t):
    act = [s for s in SC if s[0] <= t < s[1]] or [SC[-1]]
    img = act[0][2](t, act[0][0], act[0][1])
    if len(act) > 1: img = Image.blend(img, act[1][2](t, act[1][0], act[1][1]), eio((t - act[1][0]) / (act[0][1] - act[1][0])))
    img.alpha_composite(VIG)
    fade = clamp(1 - t / 0.5) if t < 0.5 else clamp((t - (T - 0.8)) / 0.8)
    if fade > 0: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * fade))))
    a = np.asarray(img.convert('RGB')).astype(np.int16) + rng.normal(0, 4, (H, W))[..., None].astype(np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

if __name__ == '__main__':
    if sys.argv[2] == 'preview':
        ts = [float(x) for x in sys.argv[4:]]; P_ = Image.new('RGB', (4 * 480, ((len(ts) + 3) // 4) * 270))
        for i, t in enumerate(ts): P_.paste(frame(t).resize((480, 270)), ((i % 4) * 480, (i // 4) * 270))
        P_.save(D + sys.argv[3], quality=85); sys.exit()
    a, b = float(sys.argv[3]), float(sys.argv[4])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', D + sys.argv[2]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
