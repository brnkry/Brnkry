# Heinrich Ehrler (long version, 16:9, German): built like "Der wahre Ursprung" (zoom on photos, 1.2 s crossfades, newsreel labels top left,
# gold serif subtitles), but the colourised photos stay in colour under a light old-film finish (light dust, flicker, grain, vignette).
# Timeline: radio message (Funkspruch) -> narration part 1, 2, 3a -> radio message again -> narration 3b.
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
Image.MAX_IMAGE_PIXELS = None
E = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/ehrler/'
U = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/urs/'
OUT = E + 'build/'; os.makedirs(OUT + 'shots', exist_ok=True)
W, H, FPS, XF = 1920, 1080, 30, 1.2
LS = '/usr/share/fonts/truetype/liberation/'
RADIO = E + 'Telsiz_Final.mp3'; RD = 8.91
def run(c): subprocess.run(c, check=True)
def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)
def norm(w): return re.sub(r'[^a-zäöüßå0-9]', '', w.lower())

# ---------------- timeline ----------------
P = [json.load(open(E + f'p{i}/words.json')) for i in (1, 2, 3)]
iH = next(i for i, w in enumerate(P[2]) if w[0] == 'haben.' and P[2][i - 1][0] == 'zu')      # "...gehört zu haben."
R1 = 0.4; T1 = R1 + RD + 0.4
T2 = T1 + P[0][-1][2] + 0.8
T3 = T2 + P[1][-1][2] + 0.8
CUT_A = P[2][iH][2] + 0.25                       # end of part 3a in the file
R2 = T3 + CUT_A + 0.45                           # second radio message
CUT_B = P[2][iH + 1][1] - 0.12                   # part 3b starts here in the file
T3B = R2 + RD + 0.35 - CUT_B                     # offset so that 3b follows the radio
WD = []                                          # global narration words (word, start, end)
for w in P[0]: WD.append((w[0], w[1] + T1, w[2] + T1))
for w in P[1]: WD.append((w[0], w[1] + T2, w[2] + T2))
for i, w in enumerate(P[2]):
    off = T3 if i <= iH else T3B
    WD.append((w[0], w[1] + off, w[2] + off))
TOTAL = WD[-1][2] + 3.2
TOK = [norm(w[0]) for w in WD]
def K(ph):
    if isinstance(ph, (int, float)): return float(ph)
    p = [norm(x) for x in ph.split()]
    h = [k for k in range(len(TOK) - len(p) + 1) if TOK[k:k + len(p)] == p]
    assert len(h) >= 1, ph
    return WD[h[0]][1] - 0.15

# ---------------- sources ----------------
IMG = {os.path.basename(f).split('.')[0][:18]: f for f in []}
IM = sorted(os.listdir(E + 'img')); IMP = lambda i: E + 'img/' + IM[i]
VID = {'lehr': (E + 'arch/me262_lehrfilm.mkv', (34, 40, 568, 380)), 'dw': (E + 'arch/dw681_1943.mkv', (20, 14, 686, 504)),
       'tir': (E + 'arch/un_tirpitz_1944.mp4', (18, 12, 604, 450)), 'conv': (E + 'arch/un_1942-10-19_Big_Convoy_To_Russia.mp4', (16, 12, 594, 456)),
       'conv2': (E + 'arch/un_1942-07-13_Allied_Convoy_Battles_Axis.mp4', (18, 12, 598, 456)), 'b17': (E + 'arch/b17_flying_fortress.mp4', (10, 10, 698, 460)),
       'tb': (E + 'arch/tallboy.webm', (10, 24, 580, 430)), 'fly': (E + 'arch/me262_lehrfilm.mkv', (34, 40, 568, 380)), 'S': (U + 'vid/1936-09-09_Spain_Air_Raid.mp4', None)}
# blur zones per photo index: (cx, cy, rx) as fractions of the photo width/height; radius in fractions of the width
BLUR = {7: [(0.15, 0.7358, 0.0199), (0.6504, 0.9658, 0.0221)], 12: [(0.5086, 0.1222, 0.0265), (0.1766, 0.945, 0.0205), (0.75, 0.92, 0.0154)], 13: [(0.48, 0.377, 0.0138)], 14: [(0.4267, 0.083, 0.0205), (0.2243, 0.7295, 0.0154), (0.64, 0.989, 0.0231)], 15: [(0.4989, 0.07, 0.0167), (0.29, 0.5929, 0.0143)], 23: [(0.2504, 0.1969, 0.0143), (0.1532, 0.7693, 0.0128), (0.4838, 0.9534, 0.0198)], 24: [(0.5981, 0.7415, 0.0072), (0.73, 0.962, 0.0103)], 5: [(0.29, 0.5697, 0.0167), (0.6736, 0.5848, 0.0092), (0.68, 0.7592, 0.0092)], 6: [(0.6182, 0.1674, 0.0143), (0.48, 0.433, 0.011)], 2: [(0.3287, 0.4182, 0.0088), (0.7643, 0.4506, 0.0082)], 4: [(0.56, 0.3445, 0.0077), (0.4952, 0.5602, 0.0066)], 9: [(0.2995, 0.2775, 0.0066)], 10: [(0.2095, 0.3695, 0.006), (0.5, 0.4026, 0.006), (0.7533, 0.4194, 0.0055), (0.1586, 0.7079, 0.0055), (0.44, 0.7363, 0.0055)], 17: [(0.3726, 0.4759, 0.0191)], 20: [(0.1851, 0.3675, 0.0044), (0.3589, 0.3868, 0.004), (0.5232, 0.3985, 0.004), (0.6987, 0.3685, 0.004), (0.7823, 0.4127, 0.0043)], 1: [(0.5153, 0.1763, 0.022)]}
def load_img(src):
    if isinstance(src, int):
        im = Image.open(IMP(src)).convert('RGB'); w, h = im.size
        for cx, cy, r in BLUR.get(src, []):
            R = int(r * w); box = (int(cx * w - R), int(cy * h - R), int(cx * w + R), int(cy * h + R))
            box = (max(box[0], 0), max(box[1], 0), min(box[2], w), min(box[3], h))
            patch = im.crop(box).filter(ImageFilter.GaussianBlur(R * 0.35))
            m = Image.new('L', patch.size, 0); ImageDraw.Draw(m).ellipse((0, 0, patch.size[0], patch.size[1]), fill=255)
            im.paste(patch, box[:2], m.filter(ImageFilter.GaussianBlur(R * 0.15)))
        return im
    return Image.open(src).convert('RGB')
def frame_src(im):
    """16:9 canvas at 2x: landscape photos fill the frame, portraits sit on a blurred, darkened copy of themselves"""
    w, h = im.size; r = W / H
    if w / h >= 1.25:
        cw, ch = (w, w / r) if w / h < r else (h * r, h); x0, y0 = (w - cw) / 2, (h - ch) / 2
        return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W * 2, H * 2), Image.LANCZOS)
    bg = im.resize((W * 2, int(h * W * 2 / w)), Image.LANCZOS); y0 = (bg.height - H * 2) // 2
    bg = bg.crop((0, y0, W * 2, y0 + H * 2)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new('RGB', bg.size, (0, 0, 0)), 0.55)
    fg = im.resize((int(w * H * 2 / h), H * 2), Image.LANCZOS); bg.paste(fg, ((W * 2 - fg.width) // 2, 0)); return bg
def pipe(out):
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out + '.part.mp4'], stdin=subprocess.PIPE)
def img_shot(src, d, out, zin):
    S = frame_src(load_img(src)); n = int(round(d * FPS)); p = pipe(out); z0, z1 = (1.0, 1.08) if zin else (1.08, 1.0)
    for f in range(n):
        z = z0 + (z1 - z0) * ease(f / max(1, n - 1)) * 0.7 + (z1 - z0) * (f / max(1, n - 1)) * 0.3; a = 2 / z
        p.stdin.write(S.transform((W, H), Image.AFFINE, (a, 0, W - a * W / 2, 0, a, H - a * H / 2), resample=Image.BILINEAR).tobytes())
    p.stdin.close(); p.wait(); os.replace(out + '.part.mp4', out)
def vid_shot(key, ss, d, out):
    src, cr = VID[key]
    if cr: x, y, w, h = cr; h2 = w * 9 / 16; vf = f'crop={w}:{int(h2)}:{x}:{int(y + (h - h2) / 2)},'
    else: vf = 'crop=iw:iw*9/16,'
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', src, '-t', f'{d:.3f}', '-vf',
         vf + f'scale={W}:{H}:flags=lanczos,fps={FPS},format=gray,format=yuv420p,setsar=1', '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', out + '.part.mp4'])
    os.replace(out + '.part.mp4', out)

# ---------------- text ----------------
WEAK = {'der', 'die', 'das', 'den', 'dem', 'des', 'ein', 'eine', 'einen', 'einem', 'einer', 'eines', 'und', 'an', 'in', 'im', 'zu', 'zur', 'zum', 'von', 'vom', 'mit', 'auf', 'aus', 'bei', 'nach', 'vor', 'über', 'um', 'als', 'wie', 'es', 'er', 'sie', 'wurde', 'war'}
def chunks(WDL):
    def stop(w): return w[-1] in '.:?!' and not (w[:-1].isdigit() and int(w[:-1]) <= 31)
    ph, cur = [], []
    for w in WDL:
        cur.append(w)
        if stop(w[0]) or (w[0][-1] in ',;' and len(cur) >= 3): ph.append(cur); cur = []
    if cur: ph.append(cur)
    out = []
    def split(c):
        txt = ' '.join(x[0] for x in c)
        if len(txt) <= 58 or len(c) < 4: out.append(c); return
        best, bk = 1e9, None
        for k in range(2, len(c) - 1):
            a = len(' '.join(x[0] for x in c[:k])); pen = abs(a - len(txt) / 2) + (40 if c[k - 1][0].lower() in WEAK else 0)
            if pen < best: best, bk = pen, k
        split(c[:bk]); split(c[bk:])
    for c in ph: split(c)
    return [(c[0][1], c[-1][2], ' '.join(x[0] for x in c).replace('Me zweihundertzweiundsechzig', 'Me 262')) for c in out]
RADIO_LINES = [(0.25, 3.45, 'Theo, Heinrich hier. Habe zwei Bomber abgeschossen.'), (3.5, 5.7, 'Munition ist alle. Ich ramme jetzt.'), (5.85, 8.7, 'Auf Wiedersehen, wir sehen uns in Walhalla.')]
def ass(out):
    def ts(t): return '%d:%02d:%05.2f' % (t // 3600, t % 3600 // 60, t % 60)
    L = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {W}', f'PlayResY: {H}', '', '[V4+ Styles]',
         'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
         'Style: Sub,Liberation Serif,48,&H2070C3CD,&H000000FF,&H9E000000,&H9E000000,-1,0,0,0,100,100,0,0,3,7,0,2,60,60,72,1',
         '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    for r0 in (R1, R2):
        for a, b, t in RADIO_LINES:
            L.append(f'Dialogue: 0,{ts(r0 + a)},{ts(r0 + b)},Sub,,0,0,0,,{{\\fad(250,150)}}{{\\i1}}Funkspruch:{{\\i0}} „{t}“')
    cs = chunks(WD)
    for i, (a, b, t) in enumerate(cs):
        b2 = cs[i + 1][0] - 0.05 if i + 1 < len(cs) and cs[i + 1][0] - b < 0.7 else b + 0.45
        L.append(f'Dialogue: 0,{ts(a)},{ts(b2)},Sub,,0,0,0,,{{\\fad(380,150)}}{t}')
    open(out, 'w').write('\n'.join(L) + '\n')
def label_png(big, small, out):
    GOLD, CREAM = (214, 190, 120), (236, 226, 204)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fb = ImageFont.truetype(LS + 'LiberationSerif-Bold.ttf', 44); fs = ImageFont.truetype(LS + 'LiberationSerif-Italic.ttf', 30)
    x, y = 90, 90; bs = ' '.join(big); wb = max(d.textlength(bs, font=fb), d.textlength(small, font=fs))
    d.rectangle((x - 30, y - 24, x + wb + 30, y + 122), fill=(0, 0, 0, 80))
    d.line((x, y - 8, x + wb, y - 8), fill=GOLD + (255,), width=2); d.text((x, y), bs, font=fb, fill=CREAM + (255,))
    d.text((x, y + 60), small, font=fs, fill=GOLD + (255,)); d.line((x, y + 106, x + wb, y + 106), fill=GOLD + (255,), width=2)
    im.save(out)

FLY_TRACK = [(0, 104, 450), (1, 106, 400), (2, 100, 300), (3, 100, 230), (4, 50, 250), (5, 110, 230), (6, 130, 220), (7, 110, 210), (8, 110, 210), (9, 130, 370), (10, 100, 310), (11, 110, 270)]
def _frames(ss, d):
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', VID['fly'][0], '-t', f'{d + 0.2:.3f}', '-vf',
                           f'crop=568:319:34:70,scale={W}:{H}:flags=lanczos,fps={FPS},format=gray,format=rgb24', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    while True:
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3: break
        yield raw
    dec.kill()
def _match(g, tpl, cx, cy, rad):
    """normalised cross-correlation of tpl around (cx, cy) on half-resolution grey image g"""
    th, tw = tpl.shape; t0 = (tpl - tpl.mean()) / (tpl.std() + 1e-6)
    x0, y0 = max(int(cx - rad - tw // 2), 0), max(int(cy - rad - th // 2), 0)
    win = g[y0:int(cy + rad + th // 2) + 1, x0:int(cx + rad + tw // 2) + 1]
    from numpy.lib.stride_tricks import sliding_window_view
    v = sliding_window_view(win, (th, tw))[::2, ::2]
    m = v.mean(axis=(2, 3), keepdims=True); sd = v.std(axis=(2, 3), keepdims=True) + 1e-6
    sc = (((v - m) / sd) * t0).mean(axis=(2, 3)); j, i = np.unravel_index(np.argmax(sc), sc.shape)
    return x0 + i * 2 + tw // 2, y0 + j * 2 + th // 2, sc.max()
def fly_shot(ss, d, out):
    """flying Me 262 (training film): the tail swastika is found in every frame by template matching and covered by a small blur"""
    n = int(round(d * FPS))
    # template from the frame 3 s in, where the swastika sits near (100, 230) in full resolution
    ref = None
    for k, raw in enumerate(_frames(ss + 3.0, 0.1)):
        ref = np.asarray(Image.frombytes('RGB', (W, H), raw).convert('L').resize((W // 2, H // 2)), np.float32); break
    x, y, _ = _match(ref, ref[115 - 24:115 + 24, 50 - 24:50 + 24], 50, 115, 20)
    tpl = ref[y - 18:y + 18, x - 18:x + 18].copy()
    cx, cy = 52, 225; p = pipe(out)
    for f, raw in enumerate(_frames(ss, d)):
        if f >= n: break
        im = Image.frombytes('RGB', (W, H), raw); g = np.asarray(im.convert('L').resize((W // 2, H // 2)), np.float32)
        cx, cy, sc = _match(g, tpl, cx, cy, 40 if f else 70)
        X, Y, R = cx * 2, cy * 2, 46; box = (int(X - R), int(Y - R), int(X + R), int(Y + R))
        pt = im.crop(box).filter(ImageFilter.GaussianBlur(12)); m = Image.new('L', pt.size, 0); ImageDraw.Draw(m).ellipse((0, 0) + pt.size, fill=255)
        im.paste(pt, box[:2], m.filter(ImageFilter.GaussianBlur(5))); p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait(); os.replace(out + '.part.mp4', out)
