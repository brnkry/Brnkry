# Franz Bäke (long version, 16:9, German): Ehrler engine, one narration file, no radio message
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
Image.MAX_IMAGE_PIXELS = None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blur
E = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/baeke/'
U = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/urs/'
OUT = E + 'build/'; os.makedirs(OUT + 'shots', exist_ok=True)
W, H, FPS, XF = 1920, 1080, 30, 1.2
LS = '/usr/share/fonts/truetype/liberation/'
def run(c): subprocess.run(c, check=True)
def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)
def norm(w): return re.sub(r'[^a-zäöüßå0-9]', '', w.lower())
T1 = 0.6
WD = [(w[0], w[1] + T1, w[2] + T1) for w in json.load(open(E + 'p1/words.json'))]
TOTAL = WD[-1][2] + 3.2
TOK = [norm(w[0]) for w in WD]
def K(ph):
    if isinstance(ph, (int, float)): return float(ph)
    p = [norm(x) for x in ph.split()]
    h = [k for k in range(len(TOK) - len(p) + 1) if TOK[k:k + len(p)] == p]
    assert len(h) >= 1, ph
    return WD[h[0]][1] - 0.15
IMP = blur.IMP
A = E + 'arch/1943-07-21-Die-Deutsche-Wochenschau-'
CR = (12, 10, 696, 516)
VID = {n: (E + 'arch/' + [f for f in sorted(os.listdir(E + 'arch')) if f.endswith(n + '.mkv')][0], CR) for n in ('672', '674', '703', '705', '712')}
VID['tg'] = (E + '../tiger/dl/TIGER.mp4', (0, 280, 720, 720))
COLOR = {'tg'}
def load_img(src):
    if isinstance(src, int): return blur.load(src)
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
         vf + f'scale={W}:{H}:flags=lanczos,fps={FPS},' + ('' if key in COLOR else 'format=gray,') + 'format=yuv420p,setsar=1', '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', out + '.part.mp4'])
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
    return [(c[0][1], c[-1][2], ' '.join(x[0] for x in c)) for c in out]
def ass(out):
    def ts(t): return '%d:%02d:%05.2f' % (t // 3600, t % 3600 // 60, t % 60)
    L = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {W}', f'PlayResY: {H}', '', '[V4+ Styles]',
         'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
         'Style: Sub,Liberation Serif,48,&H2070C3CD,&H000000FF,&H9E000000,&H9E000000,-1,0,0,0,100,100,0,0,3,7,0,2,60,60,72,1',
         '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
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

