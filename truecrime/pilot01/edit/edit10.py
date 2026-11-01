"""10 saniyelik teaser kurgusu.
Kullanım: python3 edit10.py <clips_dir> <out.mp4> [--still t1,t2,...]
"""
import sys, os, math, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile
from scipy.signal import butter, lfilter

CL, OUT = sys.argv[1], sys.argv[2]
STILLS = [float(x) for x in sys.argv[sys.argv.index('--still') + 1].split(',')] if '--still' in sys.argv else None
HERE = os.path.dirname(os.path.abspath(__file__))
F_TYPE = f'{HERE}/fonts/special-elite-latin-400-normal.woff'
F_HAND = f'{HERE}/fonts/caveat-latin-700-normal.woff'
F_HEAD = f'{HERE}/fonts/bebas-neue-latin-400-normal.woff'
W, H, FPS = 1920, 1080, 24
CREAM = (246, 241, 232); PLUM = (72, 40, 58); RED = (176, 75, 67); INK = (58, 34, 48)

def ss(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0); return t * t * (3 - 2 * t)

# ---------- kare okuma ----------
_cache = {}
def frames(name):
    if name not in _cache:
        cap = cv2.VideoCapture(f'{CL}/{name}.mp4'); fs = []
        while True:
            ok, f = cap.read()
            if not ok: break
            fs.append(f)
        _cache[name] = fs
    return _cache[name]

def src_frame(name, t, blur=1):
    fs = frames(name); i = int(round(t * FPS))
    if blur <= 1: return fs[min(max(i, 0), len(fs) - 1)].astype(np.float32) / 255
    acc = sum(fs[min(max(i + k, 0), len(fs) - 1)].astype(np.float32) for k in range(blur))
    return acc / blur / 255

# ---------- kurgu listesi: (başlangıç, bitiş, klip, kaynak_başlangıç, hız, bulanıklık) ----------
EDL = [
    (0.00, 1.70, 'C1', 0.60, 1.0, 1),
    (1.70, 2.95, 'C2', 0.25, 1.0, 1),
    (2.95, 3.75, 'C3', 0.10, 1.0, 1),
    (3.75, 5.05, 'C3', 5.70, 1.0, 1),
    (5.05, 7.25, 'C4', 2.60, 1.0, 1),
    (7.25, 8.45, 'C5', 4.00, 3.0, 3),
    (8.45, 10.0, 'C6', 0.00, 1.0, 1),
]
CUTS = [e[0] for e in EDL[1:]]

# ---------- sarı not takibi ----------
def note_box(img, search):
    x0, y0, x1, y1 = search; roi = img[y0:y1, x0:x1]
    b, g, r = roi[..., 0], roi[..., 1], roi[..., 2]
    m = ((r > 0.82) & (g > 0.78) & ((r - b) > 0.18)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    if n < 2: return None
    k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
    x, y, w, h = st[k, :4]
    return (x0 + x, y0 + y, w, h)

# ---------- yazı katmanları ----------
def rgba_text(text, font, size, fill, rot=0, stroke=0, stroke_fill=None, pad=40):
    f = ImageFont.truetype(font, size)
    w = int(f.getlength(text)) + pad * 2; h = int(size * 1.6) + pad * 2
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((pad, pad), text, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(stroke_fill or fill) + (255,))
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    a = np.asarray(im).astype(np.float32) / 255
    return a[..., [2, 1, 0, 3]]

def paste(dst, L, cx, cy, reveal=1.0, alpha=1.0, scale=1.0):
    if alpha <= 0 or reveal <= 0: return
    if scale != 1.0: L = cv2.resize(L, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    h, w = L.shape[:2]; x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + w, W), min(y0 + h, H)
    if xb <= xa or yb <= ya: return
    s = L[ya - y0:yb - y0, xa - x0:xb - x0].copy()
    if reveal < 1:
        cut = int(w * reveal); s[:, max(cut - (xa - x0), 0):, 3] = 0
        edge = max(cut - (xa - x0), 0)
        s[:, max(edge - 25, 0):edge, 3] *= np.linspace(1, 0, min(25, edge))[None, :] if edge else 1
    a = s[..., 3:4] * alpha
    dst[ya:yb, xa:xb] = dst[ya:yb, xa:xb] * (1 - a) + s[..., :3] * a

def typed(dst, text, font, size, x, y, t0, cps, fill=CREAM, alpha=1.0, anchor='l'):
    n = int(max(0, (T_NOW - t0)) * cps)
    if n <= 0: return
    s = text[:min(n, len(text))]
    L = rgba_text(s, font, size, fill)
    sh = rgba_text(s, font, size, PLUM)
    w = L.shape[1]; cx = x + w / 2 if anchor == 'l' else x
    paste(dst, sh, cx + 4, y + 4, alpha=alpha * 0.85); paste(dst, L, cx, y, alpha=alpha)

HAND_1 = rgba_text('1 Dec 1948', F_HAND, 92, INK, rot=1.5)
HAND_2a = rgba_text('No name.', F_HAND, 86, INK, rot=-3)
HAND_2b = rgba_text('No papers.', F_HAND, 86, INK, rot=-3)
TITLE_S = rgba_text('THE SOMERTON MAN', F_TYPE, 46, CREAM)
TITLE_S_SH = rgba_text('THE SOMERTON MAN', F_TYPE, 46, PLUM)
TITLE_B = rgba_text('WHO WAS HE?', F_HEAD, 230, CREAM)
TITLE_B_SH = rgba_text('WHO WAS HE?', F_HEAD, 230, PLUM)

# ---------- final görünüm ----------
rng = np.random.default_rng(5)
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.30 * (((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2) ** 1.4).clip(0.55, 1)[..., None]
GRAIN = [cv2.resize(rng.normal(0, 0.022, (H // 2, W // 2)).astype(np.float32), (W, H))[..., None] for _ in range(6)]

def punch(img, t, cut):
    k = 1 - ss(cut, cut + 0.22, t)
    s = 1 + 0.045 * k
    if s <= 1.0005: return img
    M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, s)
    return cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)

def render(t):
    global T_NOW; T_NOW = t
    for (a, b, clip, s0, sp, bl) in EDL:
        if a <= t < b or (b == 10.0 and t >= a): break
    st = s0 + (t - a) * sp
    img = src_frame(clip, st, bl)
    img = punch(img, t, a)

    # --- yazılar ---
    if clip == 'C1':
        typed(img, 'SOMERTON BEACH, SOUTH AUSTRALIA', F_TYPE, 50, 110, 930, 0.15, 30, alpha=1 - ss(1.5, 1.7, t))
    if clip == 'C2':
        bx = note_box(img, (60, 650, 700, 1080))
        if bx:
            x, y, w, h = bx
            paste(img, HAND_1, x + w * 0.52, y + 230, reveal=ss(2.05, 2.55, t) * 1.05)
    if clip == 'C3' and s0 > 5:
        bx = note_box(img, (150, 150, 900, 900))
        if bx:
            x, y, w, h = bx
            paste(img, HAND_2a, x + w * 0.46, y + h * 0.60, reveal=ss(3.82, 4.20, t) * 1.05)
            paste(img, HAND_2b, x + w * 0.48, y + h * 0.80, reveal=ss(4.20, 4.62, t) * 1.05)
    if clip == 'C4':
        typed(img, 'ONE TRAIN TICKET. NEVER USED.', F_TYPE, 50, W / 2 - 470, 960, 5.45, 26, alpha=1 - ss(7.05, 7.25, t))
    if clip == 'C6':
        al = ss(8.85, 9.05, t); sc = 1 + 0.25 * (1 - ss(8.85, 9.1, t))
        dim = ss(8.7, 9.1, t) * 0.55
        img = img * (1 - dim)
        paste(img, TITLE_S_SH, W / 2 + 3, 330 + 3, alpha=ss(8.6, 8.85, t))
        paste(img, TITLE_S, W / 2, 330, alpha=ss(8.6, 8.85, t))
        paste(img, TITLE_B_SH, W / 2 + 7, 560 + 7, alpha=al, scale=sc)
        paste(img, TITLE_B, W / 2, 560, alpha=al, scale=sc)
        if t > 9.05:
            ln = ss(9.05, 9.35, t); x0 = W / 2 - 420; x1 = x0 + 840 * ln
            cv2.line(img, (int(x0), 715), (int(x1), 715), tuple(c / 255 for c in RED[::-1]), 10, cv2.LINE_AA)

    # --- görünüm ---
    img = img * VIG
    img = img + GRAIN[int(t * FPS) % len(GRAIN)]
    for c in CUTS:  # kesmede 1 karelik hafif parlama
        if 0 <= t - c < 1 / FPS: img = img * 0.85 + 0.15
    if t > 9.75: img = img * (1 - ss(9.75, 10.0, t))
    return np.clip(img, 0, 1)

# ---------- ses ----------
SR = 48000
def clip_audio(name):
    p = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f'{CL}/{name}.mp4', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True)
    return np.frombuffer(p.stdout, np.float32)

def lp(x, fc):
    b, a = butter(2, fc / (SR / 2)); return lfilter(b, a, x)
def hp(x, fc):
    b, a = butter(2, fc / (SR / 2), 'high'); return lfilter(b, a, x)

def build_audio(path):
    n = int(10 * SR); mix = np.zeros(n)
    t = np.arange(n) / SR
    # klip efektleri
    gains = {'C1': 2.2, 'C2': 2.0, 'C3': 1.4, 'C4': 0.8, 'C5': 2.5, 'C6': 2.0}
    for (a, b, clip, s0, sp, bl) in EDL:
        src = clip_audio(clip)
        i0 = int(s0 * SR); ln = int((b - a) * SR)
        seg = src[i0:i0 + ln] if sp == 1 else src[i0:i0 + int(ln * sp)][::int(sp)][:ln]
        seg = np.pad(seg, (0, max(0, ln - len(seg))))[:ln].astype(np.float64)
        f = int(0.012 * SR); env = np.ones(ln); env[:f] = np.linspace(0, 1, f); env[-f:] = np.linspace(1, 0, f)
        mix[int(a * SR):int(a * SR) + ln] += seg * env * gains[clip]
    # karanlık drone
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t)
    drone = (np.sin(2 * np.pi * 55 * t) * 0.5 + np.sin(2 * np.pi * 55.4 * t) * 0.4 + np.sin(2 * np.pi * 82.4 * t) * 0.25 + np.sin(2 * np.pi * 110.3 * t) * 0.12) * lfo
    air = lp(hp(np.random.default_rng(1).normal(0, 1, n), 300), 2200) * 0.05
    bed = (drone * 0.10 + air) * (np.clip(t / 0.6, 0, 1)) * (1 - np.clip((t - 9.4) / 0.6, 0, 1))
    mix += bed
    # vuruşlar
    def boom(at, amp, dec=0.9, f0=62):
        i = int(at * SR); m = n - i; tt = np.arange(m) / SR
        f = f0 * (1 + 0.8 * np.exp(-tt * 18))
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / dec)
        s += lp(np.random.default_rng(int(at * 100)).normal(0, 1, m), 900) * np.exp(-tt * 25) * 0.4
        mix[i:] += s * amp
    def tick(at, amp):
        i = int(at * SR); m = int(0.08 * SR); tt = np.arange(m) / SR
        s = hp(np.random.default_rng(int(at * 1000)).normal(0, 1, m), 2500) * np.exp(-tt * 70)
        mix[i:i + m] += s * amp
    for c, amp in zip(CUTS, [0.55, 0.3, 0.35, 0.7, 0.35, 0.9]):
        boom(c, amp, dec=0.5 if amp < 0.6 else 1.1)
    # yükselen gerilim (tren kesmesinden önce)
    i0, i1 = int(4.25 * SR), int(5.05 * SR); m = i1 - i0; tt = np.linspace(0, 1, m)
    rs = hp(np.random.default_rng(9).normal(0, 1, m), 1200) * tt ** 2.2 * 0.22
    mix[i0:i1] += rs
    # daktilo tıkları
    for k, ch in enumerate('SOMERTON BEACH, SOUTH AUSTRALIA'):
        if ch != ' ': tick(0.15 + k / 30, 0.25)
    for k, ch in enumerate('ONE TRAIN TICKET. NEVER USED.'):
        if ch != ' ': tick(5.45 + k / 26, 0.22)
    # son vuruşta uzun kuyruk
    boom(8.87, 0.8, dec=1.6, f0=48)
    # limiter
    mix = mix / max(1e-6, np.max(np.abs(mix))) * 0.89
    mix *= 1 - np.clip((t - 9.7) / 0.3, 0, 1)
    wavfile.write(path, SR, (mix * 32767).astype(np.int16))

if STILLS:
    for t in STILLS:
        cv2.imwrite(OUT.replace('.mp4', f'_{t:05.2f}.jpg'), (render(t) * 255).astype(np.uint8))
    sys.exit()

wav = OUT.replace('.mp4', '.wav'); build_audio(wav)
p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', wav,
                      '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for i in range(int(10 * FPS)):
    p.stdin.write((render(i / FPS) * 255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait(); print('done', OUT)
