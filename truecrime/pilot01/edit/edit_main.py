"""Somerton Man: anlatıcılı ana bölüm (yaklaşık 71 sn).
Kullanım: python3 edit_main.py <clips_dir> <vo.wav> <out.mp4> [--still t1,t2,...]
"""
import sys, os, math, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile
from scipy.signal import butter, lfilter

CL, VO, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
STILLS = [float(x) for x in sys.argv[sys.argv.index('--still') + 1].split(',')] if '--still' in sys.argv else None
HERE = os.path.dirname(os.path.abspath(__file__))
F_TYPE = f'{HERE}/fonts/special-elite-latin-400-normal.woff'
F_HAND = f'{HERE}/fonts/caveat-latin-700-normal.woff'
F_HEAD = f'{HERE}/fonts/bebas-neue-latin-400-normal.woff'
F_SERIF = '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
W, H, FPS = 1920, 1080, 24
DUR = 71.0
CREAM = (246, 241, 232); PLUM = (72, 40, 58); RED = (176, 75, 67); INK = (58, 34, 48); PENCIL = (78, 74, 84)

def ss(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0); return t * t * (3 - 2 * t)

# (başlangıç, bitiş, klip, kaynak_başlangıç, hız)
EDL = [
    (0.00, 3.15, 'C1', 4.0, 1.0),
    (3.15, 9.50, 'N1', 0.0, 0.94),
    (9.50, 12.00, 'N2', 0.8, 1.0),
    (12.00, 14.90, 'C2', 1.3, 1.0),
    (14.90, 17.65, 'N3', 0.6, 1.0),
    (17.65, 20.85, 'C5', 0.0, 1.0),
    (20.85, 23.60, 'C4', 5.0, 1.0),
    (23.60, 27.55, 'N4', 0.0, 0.99),
    (27.55, 30.30, 'C3', 7.0, 1.0),
    (30.30, 32.75, 'N5', 0.6, 1.0),
    (32.75, 37.40, 'N6', 0.8, 1.0),
    (37.40, 40.10, 'N7', 1.0, 1.0),
    (40.10, 43.25, 'N8', 0.5, 1.0),
    (43.25, 46.90, 'N9', 0.2, 1.0),
    (46.90, 50.55, 'N10', 0.2, 1.0),
    (50.55, 54.05, 'N11', 0.3, 1.0),
    (54.05, 56.85, 'N12', 0.8, 1.0),
    (56.85, 60.45, 'N13', 0.2, 1.0),
    (60.45, 63.45, 'N14', 1.6, 0.77),
    (63.45, 67.05, 'N15', 0.0, 1.0),
    (67.05, DUR, 'C6', 3.0, 1.0),
]
CUTS = [e[0] for e in EDL[1:]]

# ---------- kare okuyucu ----------
class Reader:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(f'{CL}/{name}.mp4'); self.i = -1; self.f = None
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
    def get(self, idx):
        idx = min(max(idx, 0), self.n - 1)
        if idx < self.i:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx); self.i = idx - 1
        while self.i < idx:
            ok, f = self.cap.read()
            if not ok: break
            self.f = f; self.i += 1
        return self.f
_readers = {}
def frame(seg_key, name, idx):
    if seg_key not in _readers: _readers[seg_key] = Reader(name)
    return _readers[seg_key].get(idx).astype(np.float32) / 255

# ---------- takip (ECC, referans kareden her kareye afin) ----------
def gray_small(f): return cv2.cvtColor(cv2.resize(f, (480, 270)), cv2.COLOR_BGR2GRAY).astype(np.float32)
_track = {}
def track(name, ref_t, idx):
    key = (name, ref_t)
    if key not in _track:
        r = Reader(name); ref = gray_small(r.get(int(ref_t * FPS)))
        Ms = {}; M = np.eye(2, 3, dtype=np.float32)
        r2 = Reader(name)
        for i in range(r2.n):
            g = gray_small(r2.get(i))
            try:
                _, M = cv2.findTransformECC(ref, g, M.copy(), cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5), None, 5)
            except cv2.error:
                pass
            Mf = M.copy(); Mf[:, 2] *= 4; Ms[i] = Mf
        _track[key] = Ms
    Ms = _track[key]; return Ms[min(max(idx, 0), max(Ms))]

def comp_tracked(dst, layer, M, alpha=1.0):
    # layer referans karede çizildi; M: ref -> şimdiki kare (ECC, ters eşleme)
    w = cv2.warpAffine(layer, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    a = w[..., 3:4] * alpha; dst[:] = dst * (1 - a) + w[..., :3] * a

# ---------- yazı yardımcıları ----------
def layer_text(lines, font, size, color, center, rot=0, spacing=1.15, alpha=1.0, stroke=0):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = ImageFont.truetype(font, size)
    cx, cy = center; total = size * spacing * (len(lines) - 1)
    for k, ln in enumerate(lines):
        d.text((cx, cy - total / 2 + k * size * spacing), ln, font=f, fill=color + (int(255 * alpha),), anchor='mm', stroke_width=stroke, stroke_fill=color + (int(255 * alpha),))
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, center=center)
    return np.asarray(im).astype(np.float32)[..., [2, 1, 0, 3]] / 255

def reveal(layer, frac, x0, x1):
    if frac >= 1: return layer
    L = layer.copy(); cut = int(x0 + (x1 - x0) * frac); L[:, cut:, 3] = 0
    e = 30; a0 = max(cut - e, 0); L[:, a0:cut, 3] *= np.linspace(1, 0, cut - a0)[None, :]
    return L

def comp(dst, L, alpha=1.0):
    a = L[..., 3:4] * alpha; dst[:] = dst * (1 - a) + L[..., :3] * a

_tw = {}
def typewriter(dst, text, t, t0, x, y, size=46, cps=26, until=None, fade_from=None):
    n = int(max(0, t - t0) * cps)
    if n <= 0: return
    s = text[:min(n, len(text))]
    key = (s, size, x, y)
    if key not in _tw:
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = ImageFont.truetype(F_TYPE, size)
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
        ds.text((x + 2, y + 3), s, font=f, fill=(30, 14, 24, 230), anchor='ls', stroke_width=6, stroke_fill=(30, 14, 24, 230))
        from PIL import ImageFilter
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(im)
        d.text((x, y), s, font=f, fill=CREAM + (255,), anchor='ls')
        _tw[key] = np.asarray(im).astype(np.float32)[..., [2, 1, 0, 3]] / 255
    al = 1.0 if fade_from is None else 1 - ss(fade_from, fade_from + 0.25, t)
    comp(dst, _tw[key], al)

def note_box(img, search):
    x0, y0, x1, y1 = search; roi = img[y0:y1, x0:x1]
    b, g, r = roi[..., 0], roi[..., 1], roi[..., 2]
    m = ((r > 0.82) & (g > 0.78) & ((r - b) > 0.18)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    if n < 2: return None
    k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); x, y, w, h = st[k, :4]; return (x0 + x, y0 + y, w, h)

def hand_on(dst, text, size, cx, cy, frac, rot=-2):
    L = layer_text([text], F_HAND, size, INK, (cx, cy), rot=rot)
    f = ImageFont.truetype(F_HAND, size); w = f.getlength(text)
    comp(dst, reveal(L, frac, cx - w / 2 - 10, cx + w / 2 + 20))

# sabit katmanlar (referans karelerde)
L_TAMAM = layer_text(['TAMÁM SHUD'], F_SERIF, 66, INK, (1005, 668), rot=13.5)
CODE = ['WRGOABABD', 'MLIAOI', 'WTBIMPANETP', 'MLIABOAIAQC', 'ITTMTSAMSTGAB']
L_CODE = [layer_text([c], F_HAND, 74, PENCIL, (990, 250 + k * 118), rot=4) for k, c in enumerate(CODE)]
L_STRIKE = np.zeros((H, W, 4), np.float32)
cv2.line(L_STRIKE, (875, 372), (1105, 360), (PENCIL[2] / 255, PENCIL[1] / 255, PENCIL[0] / 255, 1), 5, cv2.LINE_AA)
L_STONE = layer_text(['HERE LIES', 'THE UNKNOWN', 'MAN', '1948'], F_TYPE, 38, (120, 100, 108), (970, 640), spacing=1.35)
L_WEBB = layer_text(['CARL WEBB'], F_TYPE, 120, INK, (1030, 700))
L_WEBB2 = layer_text(['ELECTRICAL ENGINEER, MELBOURNE'], F_TYPE, 44, INK, (1030, 815))
L_T1 = layer_text(['THE SOMERTON MAN'], F_TYPE, 46, CREAM, (W // 2, 330))
L_T1s = layer_text(['THE SOMERTON MAN'], F_TYPE, 46, PLUM, (W // 2 + 3, 333))
L_T2 = layer_text(['WHO WAS HE?'], F_HEAD, 230, CREAM, (W // 2, 560))
L_T2s = layer_text(['WHO WAS HE?'], F_HEAD, 230, PLUM, (W // 2 + 7, 567))

# ---------- görünüm ----------
rng = np.random.default_rng(5)
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.30 * (((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2) ** 1.4).clip(0.55, 1)[..., None]
GRAIN = [cv2.resize(rng.normal(0, 0.02, (H // 2, W // 2)).astype(np.float32), (W, H))[..., None] for _ in range(6)]
BIG = {37.40, 46.90, 56.85, 67.05}

def punch(img, t, cut, amt):
    k = 1 - ss(cut, cut + 0.3, t); s = 1 + amt * k
    if s <= 1.0005: return img
    return cv2.warpAffine(img, cv2.getRotationMatrix2D((W / 2, H / 2), 0, s), (W, H), borderMode=cv2.BORDER_REFLECT)

def render(t):
    for si, (a, b, clip, s0, sp) in enumerate(EDL):
        if a <= t < b or (si == len(EDL) - 1 and t >= a): break
    idx = int(round((s0 + (t - a) * sp) * FPS))
    img = frame(si, clip, idx)
    img = punch(img, t, a, 0.035 if a in BIG else 0.015)

    # --- yazılar ---
    if clip == 'C1': typewriter(img, '1 DECEMBER 1948', t, 0.5, 110, 960, cps=20, fade_from=2.85)
    if clip == 'N1': typewriter(img, 'SOMERTON BEACH, SOUTH AUSTRALIA', t, 3.4, 110, 960, cps=26, fade_from=9.2)
    if clip == 'C2':
        bx = note_box(img, (60, 600, 760, 1080))
        if bx: x, y, w, h = bx; hand_on(img, 'No name.', 96, x + w * 0.5, y + min(210, h * 0.55), ss(13.85, 14.45, t))
    if clip == 'C3':
        bx = note_box(img, (150, 150, 1000, 1000))
        if bx: x, y, w, h = bx; hand_on(img, 'Labels cut.', 92, x + w * 0.5, y + h * 0.66, ss(28.4, 29.2, t), rot=-4)
    if clip == 'C4':
        typewriter(img, 'ADELAIDE RAILWAY STATION', t, 21.1, 110, 930, cps=26, fade_from=23.3)
        typewriter(img, 'JANUARY 1949', t, 22.1, 110, 990, cps=20, fade_from=23.3)
    if clip == 'N7' and t > 37.7:
        comp_tracked(img, L_TAMAM, track('N7', 3.5, idx), alpha=ss(37.7, 38.0, t) * 0.92)
    if clip == 'N10':
        M = track('N10', 0.2, idx)
        for k, L in enumerate(L_CODE):
            t0 = 47.25 + k * 0.42
            if t > t0:
                Lr = reveal(L, ss(t0, t0 + 0.38, t), 650, 1350)
                comp_tracked(img, Lr, M, alpha=0.85)
        if t > 47.75: comp_tracked(img, reveal(L_STRIKE, ss(47.75, 47.95, t), 870, 1110), M, alpha=0.8)
    if clip == 'N12' and t > 54.3:
        comp_tracked(img, L_STONE, track('N12', 0.2, idx), alpha=ss(54.3, 54.9, t) * 0.85)
    if clip == 'N13': typewriter(img, '2022', t, 57.1, 110, 960, cps=12, fade_from=60.2)
    if clip == 'N14':
        M = track('N14', 3.0, idx)
        comp_tracked(img, L_WEBB, M, alpha=ss(60.6, 60.9, t))
        comp_tracked(img, L_WEBB2, M, alpha=ss(61.3, 61.6, t))
    if clip == 'C6':
        img = img * (1 - ss(67.4, 67.9, t) * 0.55)
        al1 = ss(67.4, 67.7, t); al2 = ss(67.95, 68.15, t)
        comp(img, L_T1s, al1); comp(img, L_T1, al1)
        if al2 > 0:
            sc = 1 + 0.25 * (1 - ss(67.95, 68.2, t))
            for L in (L_T2s, L_T2):
                Ls = cv2.warpAffine(L, cv2.getRotationMatrix2D((W / 2, 560), 0, sc), (W, H))
                comp(img, Ls, al2)
        if t > 68.2:
            ln = ss(68.2, 68.5, t); x0 = W / 2 - 420
            cv2.line(img, (int(x0), 715), (int(x0 + 840 * ln), 715), tuple(c / 255 for c in RED[::-1]), 10, cv2.LINE_AA)

    img = img * VIG + GRAIN[int(t * FPS) % len(GRAIN)]
    if t < 0.35: img = img * ss(0, 0.35, t)
    if t > DUR - 0.6: img = img * (1 - ss(DUR - 0.6, DUR, t))
    return np.clip(img, 0, 1)

# ---------- ses ----------
SR = 48000
def clip_audio(name):
    p = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f'{CL}/{name}.mp4', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True)
    return np.frombuffer(p.stdout, np.float32)
def lp(x, fc): b, a = butter(2, fc / (SR / 2)); return lfilter(b, a, x)
def hp(x, fc): b, a = butter(2, fc / (SR / 2), 'high'); return lfilter(b, a, x)

def build_audio(path):
    n = int(DUR * SR); t = np.arange(n) / SR
    sfx = np.zeros(n)
    for (a, b, clip, s0, sp) in EDL:
        src = clip_audio(clip).astype(np.float64)
        if not len(src): continue
        src = src / max(1e-4, np.percentile(np.abs(src), 99.5))
        ln = int((b - a) * SR); pos = (s0 + np.arange(ln) / SR * sp) * SR
        seg = np.interp(pos, np.arange(len(src)), src, right=0)
        f = int(0.03 * SR); env = np.ones(ln); env[:f] = np.linspace(0, 1, f); env[-f:] = np.linspace(1, 0, f)
        sfx[int(a * SR):int(a * SR) + ln] += seg[:n - int(a * SR)] * env[:n - int(a * SR)]
    sr0, vo = wavfile.read(VO); vo = vo.astype(np.float64)
    if vo.ndim > 1: vo = vo.mean(1)
    vo = vo / 32768 if vo.max() > 2 else vo
    if sr0 != SR: vo = np.interp(np.arange(0, len(vo), sr0 / SR), np.arange(len(vo)), vo)
    vo = np.pad(vo, (0, max(0, n - len(vo))))[:n]
    vo = vo / max(1e-4, np.max(np.abs(vo))) * 0.8
    # anlatım varken efektleri kıs
    envv = np.convolve(np.abs(vo), np.ones(int(0.25 * SR)) / int(0.25 * SR), 'same')
    duck = 1 - 0.6 * np.clip(envv / 0.05, 0, 1)
    mix = vo + sfx * 0.16 * duck
    # müzik yatağı
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.2 * t)
    drone = (np.sin(2 * np.pi * 55 * t) * 0.5 + np.sin(2 * np.pi * 55.4 * t) * 0.4 + np.sin(2 * np.pi * 82.4 * t) * 0.22 + np.sin(2 * np.pi * 110.3 * t) * 0.1) * lfo
    air = lp(hp(np.random.default_rng(1).normal(0, 1, n), 300), 1800) * 0.04
    pulse = np.zeros(n)
    for k in np.arange(30.3, 66.5, 1.2):  # gizem bölümünde yavaş nabız
        i = int(k * SR); m = int(0.5 * SR); tt = np.arange(m) / SR
        pulse[i:i + m] += np.sin(2 * np.pi * 48 * tt) * np.exp(-tt * 9) * 0.5
    bed = (drone * 0.07 + air + pulse * 0.12) * np.clip(t / 1.0, 0, 1) * (1 - np.clip((t - (DUR - 1.0)) / 1.0, 0, 1))
    mix += bed
    def boom(at, amp, dec=1.0, f0=58):
        i = int(at * SR); m = n - i; tt = np.arange(m) / SR
        f = f0 * (1 + 0.8 * np.exp(-tt * 18)); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / dec)
        s += lp(np.random.default_rng(int(at * 100)).normal(0, 1, m), 900) * np.exp(-tt * 25) * 0.4
        mix[i:] += s * amp
    def tick(at, amp):
        i = int(at * SR); m = int(0.07 * SR); tt = np.arange(m) / SR
        mix[i:i + m] += hp(np.random.default_rng(int(at * 1000)).normal(0, 1, m), 2500) * np.exp(-tt * 70) * amp
    for c in (20.85, 30.30): boom(c, 0.22, 0.6)
    for c in (37.40, 46.90, 56.85): boom(c, 0.38, 1.2)
    boom(67.95, 0.5, 1.8, 46)
    i0, i1 = int(35.9 * SR), int(37.4 * SR); tt = np.linspace(0, 1, i1 - i0)
    mix[i0:i1] += hp(np.random.default_rng(9).normal(0, 1, i1 - i0), 1200) * tt ** 2.4 * 0.12
    for text, t0, cps in (('1 DECEMBER 1948', 0.5, 20), ('SOMERTON BEACH, SOUTH AUSTRALIA', 3.4, 26), ('ADELAIDE RAILWAY STATION', 21.1, 26), ('JANUARY 1949', 22.1, 20), ('2022', 57.1, 12)):
        for k, ch in enumerate(text):
            if ch != ' ': tick(t0 + k / cps, 0.10)
    mix = mix / max(1e-6, np.max(np.abs(mix))) * 0.9
    wavfile.write(path, SR, (mix * 32767).astype(np.int16))

if STILLS:
    for t in STILLS: cv2.imwrite(OUT.replace('.mp4', f'_{t:05.2f}.jpg'), (render(t) * 255).astype(np.uint8))
    sys.exit()

wav = OUT.replace('.mp4', '.wav'); build_audio(wav)
p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', wav,
                      '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for i in range(int(DUR * FPS)):
    p.stdin.write((render(i / FPS) * 255).astype(np.uint8).tobytes())
    if i % 240 == 0: print('frame', i, flush=True)
p.stdin.close(); p.wait(); print('done', OUT)
