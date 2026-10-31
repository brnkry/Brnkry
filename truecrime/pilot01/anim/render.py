"""Pilot 01: 20 saniyelik sessiz animasyon.
Kullanım: python3 render.py <assets_dir> <cut_dir> <out.mp4> [--still t1,t2,...]
"""
import sys, math, subprocess, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from align import ecc, warp_to

AS, CUT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
STILLS = [float(x) for x in sys.argv[sys.argv.index('--still') + 1].split(',')] if '--still' in sys.argv else None
W, H, FPS, DUR = 1920, 1080, 30, 20.0
FONT_SUB = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
FONT_TYPE = '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'
FONT_STAMP = '/usr/share/fonts/opentype/inter/Inter-Black.otf'

def jpg(n): return cv2.imread(f'{AS}/{n}.jpg').astype(np.float32) / 255
def png(n): return cv2.imread(f'{CUT}/{n}.png', cv2.IMREAD_UNCHANGED).astype(np.float32) / 255
def ss(e0, e1, x):
    t = min(max((x - e0) / (e1 - e0), 0.0), 1.0); return t * t * (3 - 2 * t)
def lerp(a, b, t): return a + (b - a) * t

# ---------- yardımcılar ----------
def place(dst, src, M):
    """RGBA src'yi M (src->dst 2x3) ile dst (BGR) üzerine bindirir."""
    h, w = src.shape[:2]
    c = np.array([[0, 0, 1], [w, 0, 1], [0, h, 1], [w, h, 1]], np.float32) @ M.T
    x0, y0 = np.floor(c.min(0)).astype(int); x1, y1 = np.ceil(c.max(0)).astype(int)
    x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, dst.shape[1]), min(y1, dst.shape[0])
    if x1 <= x0 or y1 <= y0: return
    M2 = M.copy(); M2[:, 2] -= (x0, y0)
    p = cv2.warpAffine(src, M2, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    a = p[..., 3:4]
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - a) + p[..., :3] * a

def affine(sx, sy, ang_deg, px, py, tx, ty):
    """(px,py) noktası etrafında ölçek+dönüş, sonra (tx,ty)'ye taşı."""
    a = math.radians(ang_deg); c, s = math.cos(a), math.sin(a)
    R = np.array([[c * sx, -s * sy], [s * sx, c * sy]], np.float32)
    t = np.array([tx, ty], np.float32) - R @ np.array([px, py], np.float32)
    return np.hstack([R, t[:, None]]).astype(np.float32)

def camera(stage, cx, cy, cw, shake=(0, 0)):
    s = W / cw
    M = np.array([[s, 0, W / 2 - s * (cx + shake[0])], [0, s, H / 2 - s * (cy + shake[1])]], np.float32)
    return cv2.warpAffine(stage, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def handheld(t, amp=6):
    return (amp * (math.sin(t * 0.9) * 0.6 + math.sin(t * 2.3 + 1) * 0.4), amp * 0.7 * (math.sin(t * 1.3 + 2) * 0.6 + math.sin(t * 2.9) * 0.4))

def feather_mask(shape, box, blur=25):
    m = np.zeros(shape[:2], np.float32); x0, y0, x1, y1 = box
    cv2.ellipse(m, ((x0 + x1) // 2, (y0 + y1) // 2), ((x1 - x0) // 2, (y1 - y0) // 2), 0, 0, 360, 1, -1)
    return cv2.GaussianBlur(m, (0, 0), blur)[..., None]

def diff_mask(A, B, box, thr=0.12, grow=25, blur=18):
    d = cv2.GaussianBlur(np.abs(A - B).sum(2), (0, 0), 4)
    m = np.zeros(d.shape, np.float32); x0, y0, x1, y1 = box
    m[y0:y1, x0:x1] = (d[y0:y1, x0:x1] > thr).astype(np.float32)
    m = cv2.dilate(m, np.ones((grow, grow), np.uint8))
    return cv2.GaussianBlur(m, (0, 0), blur)[..., None]

def aligned(A8, nameB):
    B = cv2.imread(f'{AS}/{nameB}.jpg'); M = ecc(A8, B)
    return warp_to(A8, B, M).astype(np.float32) / 255

def water(img, region_mask, t, amp=3.0, speed=1.0, depth=None):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    k = depth if depth is not None else 1.0
    dx = amp * k * (np.sin(yy * 0.045 + t * 2.1 * speed) * 0.6 + np.sin(yy * 0.13 - t * 3.3 * speed + xx * 0.004) * 0.4)
    dy = amp * 0.45 * k * np.sin(xx * 0.011 + yy * 0.03 - t * 1.7 * speed)
    wv = cv2.remap(img, xx + dx, yy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return img * (1 - region_mask) + wv * region_mask

def sway_field(h, w, boxes, t):
    """Ağaç/ot sallanması için yer değiştirme alanı."""
    dx = np.zeros((h, w), np.float32)
    for (x0, y0, x1, y1, amp, freq, ph) in boxes:
        yy = np.arange(y0, y1, dtype=np.float32)[:, None]
        k = np.clip((y1 - yy) / (y1 - y0), 0, 1) ** 1.7
        xs = np.arange(x0, x1, dtype=np.float32)[None, :]
        edge = np.clip(np.minimum(xs - x0, x1 - xs) / 40.0, 0, 1)
        wave = amp * (math.sin(t * freq * 2 * math.pi + ph) + 0.35 * math.sin(t * freq * 5.1 + ph * 2)) \
            + amp * 0.18 * np.sin(yy * 0.09 + t * 9 + ph)
        dx[y0:y1, x0:x1] += k * wave * edge
    return dx

def remap_x(img, dx):
    h, w = img.shape[:2]; yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return cv2.remap(img, xx - dx, yy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

def flow_morph_setup(A, B, region):
    g = lambda I: cv2.cvtColor((cv2.resize(I, None, fx=.5, fy=.5) * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_ULTRAFAST + 2)
    fab = cv2.resize(dis.calc(g(A), g(B), None), (A.shape[1], A.shape[0])) * 2
    fba = cv2.resize(dis.calc(g(B), g(A), None), (A.shape[1], A.shape[0])) * 2
    return dict(A=A, B=B, fab=fab, fba=fba, region=region)

def flow_morph(m, t):
    t = float(t)
    A, B = m['A'], m['B']; h, w = A.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    f1, f2 = m['fba'].astype(np.float32), m['fab'].astype(np.float32)
    wa = cv2.remap(A, (xx + f1[..., 0] * t).astype(np.float32), (yy + f1[..., 1] * t).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    wb = cv2.remap(B, (xx + f2[..., 0] * (1 - t)).astype(np.float32), (yy + f2[..., 1] * (1 - t)).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    mid = wa * (1 - t) + wb * t
    r = m['region']
    base = A * (1 - t) + B * t if t not in (0, 1) else (A if t == 0 else B)
    out = A * (1 - r) + mid * r
    return out if t < 1 else B

def talking(t, spans, rate=6.5):
    for (a, b) in spans:
        if a <= t <= b:
            v = math.sin(2 * math.pi * rate * (t - a) + 1.4 * math.sin(2 * math.pi * 1.9 * (t - a)))
            return 1.0 if v > -0.15 else 0.0
    return 0.0

# ---------- yazı ----------
def text_layer(lines, font_path, size, pos, fill=(255, 255, 255), anchor='la', shadow=True, spacing=12, alpha=1.0):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = ImageFont.truetype(font_path, size)
    x, y = pos
    for ln in lines:
        if shadow:
            for o in (3, 2):
                d.text((x + o, y + o), ln, font=f, fill=(0, 0, 0, int(160 * alpha)), anchor=anchor)
        d.text((x, y), ln, font=f, fill=fill + (int(255 * alpha),), anchor=anchor)
        y += size + spacing
    a = np.asarray(im).astype(np.float32) / 255
    if shadow: a = np.dstack([a[..., :3], a[..., 3]])
    return a[..., [2, 1, 0, 3]]

def comp_text(frame, layer):
    a = layer[..., 3:4]; frame[:] = frame * (1 - a) + layer[..., :3] * a

_sub_cache = {}
def subtitle(frame, txt, alpha):
    if not txt or alpha <= 0: return
    key = txt
    if key not in _sub_cache:
        f = ImageFont.truetype(FONT_SUB, 44)
        words, lines, cur = txt.split(), [], ''
        for wd in words:
            if f.getlength((cur + ' ' + wd).strip()) > 1600: lines.append(cur); cur = wd
            else: cur = (cur + ' ' + wd).strip()
        lines.append(cur)
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        y = H - 70 - (len(lines) - 1) * 58
        for ln in lines:
            d.text((W // 2, y), ln, font=f, fill=(255, 255, 255, 255), anchor='ms', stroke_width=5, stroke_fill=(0, 0, 0, 200))
            y += 58
        _sub_cache[key] = np.asarray(im).astype(np.float32)[..., [2, 1, 0, 3]] / 255
    L = _sub_cache[key].copy(); L[..., 3] *= alpha; comp_text(frame, L)

SUBS = [
    (3.3, 5.7, 'Found him like this, sir. Couple of blokes on the beach saw him.'),
    (6.3, 7.8, 'Anyone know who he is?'),
    (11.7, 13.8, 'No papers. Nothing with a name on it.'),
    (14.3, 15.7, 'Just a train ticket. Never used.'),
    (16.9, 18.3, 'So who are you, mate?'),
]

# ---------- partiküller ----------
rng = np.random.default_rng(3)
SAND = [dict(x=rng.uniform(0, W * 1.3), y=rng.uniform(H * 0.55, H), v=rng.uniform(250, 650), r=rng.uniform(1, 2.6), a=rng.uniform(.25, .6), ph=rng.uniform(0, 6)) for _ in range(160)]
def sand(frame, t, strength=1.0):
    ov = np.zeros_like(frame); al = np.zeros(frame.shape[:2], np.float32)
    for p in SAND:
        x = (p['x'] - p['v'] * t) % (W * 1.3) - W * 0.15
        y = p['y'] + 14 * math.sin(t * 2 + p['ph']) - 0.02 * (p['v'] * t % 400)
        cv2.circle(ov, (int(x), int(y)), int(round(p['r'])), (0.72, 0.84, 0.91), -1, cv2.LINE_AA)
        cv2.circle(al, (int(x), int(y)), int(round(p['r'])), p['a'] * strength, -1, cv2.LINE_AA)
    al = cv2.GaussianBlur(al, (0, 0), 0.8)[..., None]
    frame[:] = frame * (1 - al) + ov * al

def gull(frame, x, y, size, t, ph=0):
    flap = math.sin(t * 9 + ph)
    wy = size * 0.45 * flap
    pts_l = np.array([[x, y], [x - size * 0.5, y - size * 0.25 - wy], [x - size, y + wy * 0.4]], np.int32)
    pts_r = np.array([[x, y], [x + size * 0.5, y - size * 0.25 - wy], [x + size, y + wy * 0.4]], np.int32)
    col = (0.22, 0.22, 0.25)
    for pts in (pts_l, pts_r):
        cv2.polylines(frame, [pts.reshape(-1, 1, 2)], False, col, max(2, int(size * 0.09)), cv2.LINE_AA)
    cv2.circle(frame, (int(x), int(y)), max(2, int(size * 0.08)), col, -1, cv2.LINE_AA)

# ---------- final görünüm ----------
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.38 * (((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2) ** 1.3).clip(0.45, 1)[..., None]
def finish(frame, t):
    f = frame * VIG
    f = f * np.array([0.97, 1.0, 1.04], np.float32)  # hafif sıcak ton (BGR)
    f = (f - 0.5) * 1.05 + 0.5
    n = rng.normal(0, 0.018, (H // 2, W // 2)).astype(np.float32)
    f = f + cv2.resize(n, (W, H))[..., None]
    return np.clip(f, 0, 1)

# =====================================================================
# SAHNE A: deniz (0 - 2.6)
# =====================================================================
BG = jpg('S1_bg')
HZ = 815
bh, bw = BG.shape[:2]
depthA = np.clip((np.arange(bh, dtype=np.float32) - HZ) / (bh - HZ), 0, 1)[:, None] ** 1.2
seaA = (np.arange(bh)[:, None] > HZ + 3).astype(np.float32) * np.ones((1, bw), np.float32)
seaA = cv2.GaussianBlur(seaA, (0, 0), 3)[..., None]
GLINT = [(rng.uniform(1300, 2752), rng.uniform(HZ + 10, HZ + 260), rng.uniform(0, 6)) for _ in range(120)]

def sky_drift(img, t, speed, hz):
    top = img[:hz]
    M = np.float32([[1, 0, -speed * t], [0, 1, 0]])
    top2 = cv2.warpAffine(top, M, (top.shape[1], top.shape[0]), borderMode=cv2.BORDER_REFLECT)
    out = img.copy(); out[:hz] = top2
    return out

def shotA(t):
    st = sky_drift(BG, t, 14, HZ)
    st = water(st, seaA, t, amp=5.0, depth=depthA)
    # parıltılar
    ov = np.zeros(st.shape[:2], np.float32)
    for (x, y, ph) in GLINT:
        v = max(0, math.sin(t * 5 + ph)) ** 6
        if v > 0.05: cv2.circle(ov, (int(x), int(y)), 2, v, -1, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 1.5)[..., None]
    st = st + ov * np.array([0.75, 0.9, 1.0], np.float32)
    k = ss(0, 2.6, t)
    fr = camera(st, lerp(1300, 1420, k), lerp(770, 790, k), lerp(2700, 2380, k), handheld(t, 3))
    gull(fr, 300 + 420 * t, 300 - 30 * t + 8 * math.sin(t * 2), 34, t)
    gull(fr, 120 + 380 * t, 360 - 22 * t, 24, t, 1.7)
    # başlık (daktilo)
    l1, l2 = 'SOMERTON BEACH, SOUTH AUSTRALIA', '1 DECEMBER 1948'
    n1 = int(np.clip((t - 0.25) / 1.1, 0, 1) * len(l1)); n2 = int(np.clip((t - 1.35) / 0.6, 0, 1) * len(l2))
    al = 1 - ss(2.25, 2.6, t)
    comp_text(fr, text_layer([l1[:n1], l2[:n2]], FONT_TYPE, 46, (110, 860), fill=(240, 236, 226), alpha=al))
    return fr

# =====================================================================
# SAHNE B: geniş plan (2.6 - 8.6)
# =====================================================================
FG = png('S1_fg') if os.path.exists(f'{CUT}/S1_fg.png') else None
VIC = png('S1_vic'); CON_A = png('S1_con_a'); DET_A = png('S1_det_a')

# Gökyüzü: BG büyütülüp ufuk duvarın arkasına saklanır
SKY = cv2.resize(BG, None, fx=1.2, fy=1.2)[:, 275:275 + 2752][:1536]
TREES = [(330, 180, 660, 860, 7, 0.32, 0.0), (1540, 0, 2080, 800, 9, 0.27, 1.3)]
GRASS = [(30, 1040, 150, 1130, 5, 0.9, 0.3), (190, 980, 330, 1065, 5, 0.8, 1.1), (1230, 960, 1330, 1075, 6, 1.0, 2.0),
         (1540, 990, 1610, 1075, 5, 0.9, 0.7), (2560, 1080, 2730, 1310, 8, 0.8, 1.6), (2450, 1170, 2510, 1265, 5, 1.1, 2.4)]

# Konuşan memur: con_b ağzı con_a'ya yamanır
def build_talk_variant(nameA, nameB, crop_off, size, mouth_box_full):
    A8 = cv2.imread(f'{AS}/{nameA}.jpg'); Bw = aligned(A8, nameB); A = A8.astype(np.float32) / 255
    m = feather_mask(A.shape, mouth_box_full, 10)
    T = A * (1 - m) + Bw * m
    x0, y0 = crop_off; h, w = size
    return T[y0:y0 + h, x0:x0 + w]

CON_TALK = CON_A.copy()
CON_TALK[..., :3] = build_talk_variant('S1_con_a', 'S1_con_b', (950, 124), CON_A.shape[:2], (1405, 300, 1515, 440))
DET_TALK = DET_A.copy()
DET_TALK[..., :3] = build_talk_variant('S1_det_a', 'S1_det_c', (1076, 70), DET_A.shape[:2], (1385, 150, 1495, 300))

# Yürüyen dedektif rig'i (S1_det_a, yerel koordinatlar 604x1400)
HIP_Y = 800
def build_rig(src):
    h, w = src.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    book = (xx >= 195) & (xx <= 378) & (yy >= 785) & (yy <= 945)
    hand = (xx >= 395) & (yy <= 860)
    torso_m = ((yy < HIP_Y) | book | hand).astype(np.float32)
    torso_m = cv2.GaussianBlur(torso_m, (0, 0), 1.2)
    torso = src.copy(); torso[..., 3] *= torso_m
    # bacak kaynağı: defter bölgesi pantolonla doldurulur
    legsrc = src.copy()
    bgr8 = (legsrc[..., :3] * 255).astype(np.uint8)
    inp = cv2.inpaint(bgr8, book.astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA).astype(np.float32) / 255
    legsrc[..., :3] = inp
    fill = book & (xx > 190) & (xx < 395)
    legsrc[..., 3] = np.where(fill, 1.0, legsrc[..., 3])
    lower = (yy >= HIP_Y - 25)
    far = legsrc.copy(); far[..., 3] *= (lower & (xx < 288)).astype(np.float32)
    near = legsrc.copy(); near[..., 3] *= (lower & (xx >= 280)).astype(np.float32)
    hip = legsrc.copy(); hip[..., 3] *= ((yy >= HIP_Y - 25) & (yy < HIP_Y + 110)).astype(np.float32)
    return dict(torso=torso, far=far, near=near, hip=hip)
RIG = build_rig(DET_A); RIG_T = build_rig(DET_TALK)
L_LEG = 530.0; TH_N0, TH_F0 = 16.8, -17.4
PIV_F, PIV_N = (250, 830), (322, 830)

def det_pose(s, talk=False):
    """s: 0..1 adım fazı. Yerel tuvalde figürü çizer (600x1500 + kenar)."""
    r = RIG_T if talk else RIG
    thn = TH_N0 - 34.2 * s; thf = TH_F0 + 34.2 * s
    lift = L_LEG * (max(math.cos(math.radians(thn)), math.cos(math.radians(thf))) - math.cos(math.radians(TH_N0)))
    can = np.zeros((1560, 760, 4), np.float32)
    off = (80, 90 - lift)
    def put(piece, ang, piv):
        M = affine(1, 1, -ang, piv[0], piv[1], piv[0] + off[0], piv[1] + off[1])
        h, w = piece.shape[:2]
        p = cv2.warpAffine(piece, M, (can.shape[1], can.shape[0]), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        a = p[..., 3:4]; can[..., :3] = can[..., :3] * (1 - a) + p[..., :3] * a; can[..., 3:4] = can[..., 3:4] * (1 - a) + a
    put(r['hip'], 0, (300, 830))
    put(r['far'], thf - TH_F0, PIV_F)
    put(r['near'], thn - TH_N0, PIV_N)
    lean = 1.2 * math.sin(math.pi * s * 2)
    put(r['torso'], lean, (300, 830))
    return can, off

# Sahne yerleşimi (sahne koordinatları 2752x1536)
VIC_S, VIC_X, VIC_Y = 0.15, 300, 1052      # sol üst köşe x, alt kenar y
CON_S, CON_X, CON_Y = 0.19, 700, 1085
DET_S, DET_FOOT_Y = 0.40, 1262
DET_START, DET_STOP = 2280, 1330            # ayak orta noktası x
B0 = 2.6
HALF = 0.46                                  # yarım adım süresi
N_HALF = 7
WALK_T0 = B0 + 0.5
STRIDE = 313 * DET_S

def det_state(t):
    """(x, s, walking)"""
    u = (t - WALK_T0) / HALF
    if u <= 0: return DET_START, 0.0, True
    if u >= N_HALF: return DET_STOP, 0.0, False
    k = int(u); f = u - k
    s = (1 - math.cos(math.pi * f)) / 2 if k % 2 == 0 else (1 + math.cos(math.pi * f)) / 2
    # duruş bacağı sabit kalsın diye hız adım fazına bağlı
    x = DET_START - (DET_START - DET_STOP) * (k + (1 - math.cos(math.pi * f)) / 2) / N_HALF
    return x, s, True

def shotB(t):
    lt = t - B0
    sky = sky_drift(SKY, t, 10, 1200)
    st = sky.copy()
    fg = FG.copy()
    dx = sway_field(1536, 2752, TREES + GRASS, t)
    fg = remap_x(fg, dx)
    a = fg[..., 3:4]; st = st * (1 - a) + fg[..., :3] * a
    # kurban (hareketsiz)
    place(st, VIC, affine(VIC_S, VIC_S, 0, 0, VIC.shape[0], VIC_X, VIC_Y))
    # memur: nefes + konuşma
    br = 1 + 0.007 * math.sin(t * 2 * math.pi * 0.35)
    tk = talking(t, [(3.35, 5.65)])
    con = CON_TALK if tk else CON_A
    hx, hy = CON_A.shape[1] / 2, CON_A.shape[0]
    place(st, con, affine(CON_S, CON_S * br, 0, hx, hy, CON_X + hx * CON_S, CON_Y))
    # dedektif: yürüyüş + konuşma (sola bakar: yatay çevrilir)
    x, s, walking = det_state(t)
    dtk = talking(t, [(6.35, 7.7)]) > 0
    fig, off = det_pose(s, talk=dtk)
    foot_local = (off[0] + 300, off[1] + 1400)
    bob = 0.0 if walking else 0.004 * math.sin(t * 2 * math.pi * 0.3)
    M = affine(-DET_S, DET_S * (1 + bob), 0, foot_local[0], foot_local[1] + 0, x, DET_FOOT_Y)
    # kumda gölge
    sh = np.zeros_like(st[..., :1])
    place(st, np.dstack([np.zeros((60, 300, 3), np.float32), cv2.GaussianBlur(np.pad(np.ones((20, 220), np.float32), ((20, 20), (40, 40))), (0, 0), 9)[..., None] * 0.28]),
          affine(DET_S * 1.25, DET_S * 1.25, 0, 150, 30, x + 10, DET_FOOT_Y - 2))
    place(st, fig, M)
    k = ss(0, 6.0, lt)
    fr = camera(st, lerp(1180, 1130, k), lerp(955, 985, k), lerp(1800, 1640, k), handheld(t, 4))
    if lt < 3.0: gull(fr, 1500 - 160 * lt, 170 + 10 * math.sin(t * 1.5), 18, t, 0.5)
    sand(fr, t, 0.8)
    return fr

# =====================================================================
# SAHNE C: cep (8.6 - 14.0)
# =====================================================================
C0, C2 = 8.6, 11.4
S2K1_8 = cv2.imread(f'{AS}/S2_k1.jpg'); S2K1 = S2K1_8.astype(np.float32) / 255
S2BL = aligned(S2K1_8, 'S2_k1_blink'); S2K2 = aligned(S2K1_8, 'S2_k2')
S2K3_8 = cv2.imread(f'{AS}/S2_k3.jpg'); S2K3 = S2K3_8.astype(np.float32) / 255; S2K3T = aligned(S2K3_8, 'S2_k3_talk')
m_blink2 = diff_mask(S2K1, S2BL, (1580, 260, 1860, 520))
m_arm = diff_mask(S2K1, S2K2, (900, 350, 2300, 1500), thr=0.10, grow=45, blur=20)
MORPH2 = flow_morph_setup(S2K1, S2K2, m_arm)
m_talk3 = diff_mask(S2K3, S2K3T, (1620, 420, 1900, 660))
def sea_mask(img, box):
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    m = ((b - r) > 0.08).astype(np.float32); x0, y0, x1, y1 = box
    z = np.zeros_like(m); z[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    return cv2.GaussianBlur(cv2.erode(z, np.ones((5, 5), np.uint8)), (0, 0), 2)[..., None]
SEA2 = sea_mask(S2K1, (2300, 250, 2752, 700))
SEA3 = sea_mask(S2K3, (2300, 250, 2752, 700))

def blink_amt(t, times):
    return max([1.0 if abs(t - b) < 0.06 else (0.5 if abs(t - b) < 0.1 else 0.0) for b in times] + [0.0])

def shotC(t):
    lt = t - C0
    if t < C2:
        mt = ss(1.4, 2.25, lt)
        img = flow_morph(MORPH2, mt) if 0 < mt < 1 else (S2K1 if mt == 0 else S2K2)
        if mt == 0:
            b = blink_amt(t, [9.25]); img = img * (1 - m_blink2 * b) + S2BL * m_blink2 * b
        img = water(img, SEA2, t, amp=2.5)
        k = ss(0, 2.8, lt)
        fr = camera(img, lerp(1500, 1440, k), lerp(800, 830, k), lerp(2700, 2450, k), handheld(t, 5))
    else:
        k = ss(0, 2.6, t - C2)
        img = S2K3
        tk = talking(t, [(11.75, 13.7)])
        img = img * (1 - m_talk3 * tk) + S2K3T * m_talk3 * tk
        img = water(img, SEA3, t, amp=2.5)
        fr = camera(img, lerp(1560, 1580, k), lerp(600, 610, k), lerp(1750, 1600, k), handheld(t, 5))
    sand(fr, t, 0.6)
    return fr

# =====================================================================
# SAHNE D: yakın plan (14.0 - 18.6)
# =====================================================================
D0 = 14.0
S3K1_8 = cv2.imread(f'{AS}/S3_k1.jpg'); S3K1 = S3K1_8.astype(np.float32) / 255
S3BL = aligned(S3K1_8, 'S3_k1_blink'); S3T1 = aligned(S3K1_8, 'S3_k1_talk')
S3K2 = aligned(S3K1_8, 'S3_k2'); S3T2 = aligned(S3K1_8, 'S3_k2_talk')
m_bl3 = diff_mask(S3K1, S3BL, (1550, 470, 1950, 680))
m_t3a = diff_mask(S3K1, S3T1, (1650, 680, 2000, 1000))
m_t3b = diff_mask(S3K2, S3T2, (1650, 680, 2000, 1000))
m_eye = diff_mask(S3K1, S3K2, (1500, 420, 2050, 1000), thr=0.10, grow=31)
MORPH3 = flow_morph_setup(S3K1, S3K2, m_eye)
SEA_D = sea_mask(S3K1, (0, 380, 1450, 640))

def shotD(t):
    lt = t - D0
    mt = ss(2.25, 2.6, lt)
    if mt <= 0:
        img = S3K1
        tk = talking(t, [(14.35, 15.65)]); img = img * (1 - m_t3a * tk) + S3T1 * m_t3a * tk
        b = blink_amt(t, [15.95]); img = img * (1 - m_bl3 * b) + S3BL * m_bl3 * b
    elif mt < 1:
        img = flow_morph(MORPH3, mt)
    else:
        img = S3K2
        tk = talking(t, [(16.95, 18.25)]); img = img * (1 - m_t3b * tk) + S3T2 * m_t3b * tk
    img = water(img, SEA_D, t, amp=2.0)
    k = ss(0, 4.6, lt)
    fr = camera(img, lerp(1450, 1640, k), lerp(760, 700, k), lerp(2650, 2050, k), handheld(t, 3))
    sand(fr, t, 0.35)
    return fr

# =====================================================================
# SAHNE E: kapanış (18.6 - 20)
# =====================================================================
E0 = 18.6
def shotE(t):
    lt = t - E0
    fr = np.zeros((H, W, 3), np.float32) + 0.03
    if lt > 0.25:
        p = ss(0.25, 0.42, lt); sc = lerp(1.6, 1.0, p)
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        f = ImageFont.truetype(FONT_STAMP, int(118 * sc))
        tw = f.getlength('UNIDENTIFIED'); x0, y0 = W / 2 - tw / 2 - 40 * sc, H / 2 - 95 * sc
        d.rectangle([x0, y0, W / 2 + tw / 2 + 40 * sc, H / 2 + 95 * sc - 50 * sc], outline=(179, 38, 46, int(255 * p)), width=int(10 * sc))
        d.text((W / 2, H / 2 - 22 * sc), 'UNIDENTIFIED', font=f, fill=(179, 38, 46, int(255 * p)), anchor='mm')
        im = im.rotate(-6, center=(W / 2, H / 2))
        L = np.asarray(im).astype(np.float32)[..., [2, 1, 0, 3]] / 255
        comp_text(fr, L)
        if lt > 0.7:
            comp_text(fr, text_layer(['SOMERTON BEACH  ·  1948'], FONT_TYPE, 38, (W // 2, H // 2 + 150), fill=(200, 196, 188), anchor='ma', alpha=ss(0.7, 1.0, lt)))
    return fr

def render(t):
    if t < B0: fr = shotA(t)
    elif t < C0: fr = shotB(t)
    elif t < D0: fr = shotC(t)
    elif t < E0: fr = shotD(t)
    else: fr = shotE(t)
    for (a, b, s) in SUBS:
        if a <= t <= b: subtitle(fr, s, ss(a, a + 0.12, t) * (1 - ss(b - 0.12, b, t)))
    fr = finish(fr, t)
    if t < 0.4: fr = fr * ss(0, 0.4, t)
    return fr

if STILLS:
    for t in STILLS:
        cv2.imwrite(OUT.replace('.mp4', f'_{t:05.2f}.jpg'), (render(t) * 255).astype(np.uint8))
    sys.exit()

p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
N = int(DUR * FPS)
for i in range(N):
    p.stdin.write((render(i / FPS) * 255).astype(np.uint8).tobytes())
    if i % 60 == 0: print('frame', i, flush=True)
p.stdin.close(); p.wait()
print('done', OUT)
