# Wolfgang Lüth Short (German, CDM): 9:16, colour photos with a light WW2 film finish, archive film (Real-ESRGAN),
# AI night scenes, Marcellus labels in the channel colours, no subtitles. Thomas Schendel narration.
import os, sys, json, math, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
L = os.path.dirname(os.path.abspath(__file__)) + '/'
W, H, FPS = 1080, 1920, 30
OFF = 0.3
VOICE = L + 'm/voice.mp3'
TOTAL = 174.52 + OFF + 2.6
SEG = L + 'segs/'; os.makedirs(SEG, exist_ok=True); os.makedirs(L + 'prep', exist_ok=True)
UD = L + 'user/'
UF = sorted(f for f in os.listdir(UD) if f.endswith('.jpg'))
def U(i): return UD + UF[i]
G = L + 'gen/'
YEL, RED, WHITE, CREAM, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (232, 226, 210), (14, 15, 18)
FD = '/tmp/claude-0/fonts/'
def run(c): subprocess.run(c, check=True)

# ---------- photo preparation: blur cap and breast eagles (swastika), cache as PNG ----------
BLUR = {3: [(.474, .068, .032)], 4: [(.475, .042, .022), (.34, .509, .028)], 5: [(.307, .593, .032)], 8: [(.487, .118, .032)], 12: [(.496, .207, .032)]}
def prep(i):
    out = L + 'prep/u%02d.png' % i
    if os.path.exists(out): return out
    os.makedirs(L + 'prep', exist_ok=True)
    im = Image.open(U(i)).convert('RGB'); w, h = im.size
    for cx, cy, r in BLUR.get(i, []):
        R = r * w; m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse((cx * w - R, cy * h - R, cx * w + R, cy * h + R), fill=255)
        im = Image.composite(im.filter(ImageFilter.GaussianBlur(R * 0.45)), im, m.filter(ImageFilter.GaussianBlur(R * 0.35)))
    im.save(out); return out

def esr_still(path, box, out):
    if os.path.exists(out): return out
    sys.path.insert(0, L + 'up'); from esr import up
    im = Image.open(path).convert('RGB'); w, h = im.size
    cr = im.crop(box); up(cr).save(out); return out

# ---------- shot renderers ----------
def enc(out, n):
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)

def img_shot(out, path, dur, cx=.5, cy=.5, z0=1.0, z1=1.12, gray=None):
    im = Image.open(path).convert('RGB'); w, h = im.size
    if w / h > W / H: cw, ch = h * W / H, h
    else: cw, ch = w, w * H / W
    x0 = min(max(cx * w - cw / 2, 0), w - cw); y0 = min(max(cy * h - ch / 2, 0), h - ch)
    src = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((int(W * 1.6), int(H * 1.6)), Image.LANCZOS)
    sw, sh = src.size; n = int(round(dur * FPS)); p = enc(out, n)
    for k in range(n):
        u = k / max(n - 1, 1); e = u * u * (3 - 2 * u) * 0.35 + u * 0.65
        z = z0 + (z1 - z0) * e; bw, bh = sw / z, sh / z
        fr = src.resize((W, H), Image.BICUBIC, box=((sw - bw) / 2, (sh - bh) / 2, (sw + bw) / 2, (sh + bh) / 2))
        if gray is not None:
            g = min(max((k / FPS - gray) / 1.2, 0), 1)
            if g > 0: fr = Image.blend(fr, fr.convert('L').convert('RGB'), g)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()

def vid_shot(out, path, ss, dur, speed=1.0, dark=0.0, z0=1.0, z1=1.04):
    # source clip from ss, retimed by speed, cover-cropped to 9:16, slight centred zoom
    src_dur = dur * speed
    n = int(round(dur * FPS))
    vf = (f"trim=start={ss}:duration={src_dur + 0.2},setpts=(PTS-STARTPTS)/{speed},tpad=stop_mode=clone:stop_duration=2,fps={FPS},"
          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"scale=w='trunc({W}*({z0}+({z1}-{z0})*n/{n})/2)*2':h=-2:eval=frame,crop={W}:{H},setsar=1")
    if dark: vf += f",eq=brightness={-dark}:gamma={1 - dark * 1.5}"
    run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf', vf, '-frames:v', str(n), '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out])

# ---------- map of Riga (aged paper, Baltic) ----------
def map_png(out):
    if os.path.exists(out): return out
    MW, MH = int(W * 1.6), int(H * 1.6); LA0, LA1 = 49.5, 64.5; lc = 24.1; span = (LA1 - LA0) * (MW / MH) / math.cos(math.radians(57))
    L0, L1 = lc - span / 2, lc + span / 2
    def xy(lo, la): return ((lo - L0) / (L1 - L0) * MW, (LA1 - la) / (LA1 - LA0) * MH)
    rng = np.random.default_rng(3)
    paper = np.full((MH, MW, 3), (196, 178, 140), np.float32)
    nz = np.array(Image.fromarray((rng.random((MH // 8, MW // 8)) * 255).astype(np.uint8)).resize((MW, MH), Image.BICUBIC), np.float32) / 255
    paper *= (0.85 + 0.22 * nz)[..., None]
    sea = Image.fromarray(np.clip(paper * np.array([0.78, 0.86, 0.92]), 0, 255).astype(np.uint8))
    land = Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8))
    mk = Image.new('L', (MW, MH), 0); dm = ImageDraw.Draw(mk); geo = json.load(open(L + '../urs/pak/geo.json'))
    lines = []
    for f in geo['features']:
        g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            ring = [xy(lo, la) for lo, la in poly[0]]
            if len(ring) > 2: dm.polygon(ring, fill=255); lines.append(ring)
    im = Image.composite(land, sea, mk); d = ImageDraw.Draw(im)
    for r in lines: d.line(r + [r[0]], fill=(110, 86, 58), width=3)
    im = im.filter(ImageFilter.GaussianBlur(0.8)); d = ImageDraw.Draw(im)
    # graticule
    for lo in range(int(L0) // 5 * 5, int(L1) + 5, 5): d.line([xy(lo, LA0), xy(lo, LA1)], fill=(150, 128, 95), width=2)
    for la in range(50, 65, 5): d.line([xy(L0, la), xy(L1, la)], fill=(150, 128, 95), width=2)
    yy, xx = np.mgrid[0:MH, 0:MW]; e = np.minimum(np.minimum(xx, MW - xx), np.minimum(yy, MH - yy)) / 260.0
    im = Image.fromarray((np.array(im, np.float32) * (0.55 + 0.45 * np.clip(e, 0, 1))[..., None]).astype(np.uint8))
    d = ImageDraw.Draw(im); fm = ImageFont.truetype(FD + 'Marcellus-Regular.ttf', 120); fs = ImageFont.truetype(FD + 'Marcellus-Regular.ttf', 76)
    for name, lo, la in [('OSTSEE', 19.2, 57.8)]: d.text(xy(lo, la), name, font=fs, fill=(70, 80, 92), anchor='mm')
    rx, ry = xy(24.1, 56.95)
    d.ellipse((rx - 34, ry - 34, rx + 34, ry + 34), fill=RED, outline=(60, 10, 10), width=5)
    d.text((rx + 60, ry - 40), 'RIGA', font=fm, fill=(40, 26, 16), anchor='lm'); d.text((rx + 64, ry + 62), '1913', font=fs, fill=(90, 30, 24), anchor='lm')
    im.save(out); return out

# ---------- labels (Marcellus, channel colours) ----------
def label_png(big, small, out):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fb = ImageFont.truetype(FD + 'Marcellus-Regular.ttf', 84); fs = ImageFont.truetype(FD + 'Marcellus-Regular.ttf', 44)
    while fb.getlength(big) > 880: fb = ImageFont.truetype(FD + 'Marcellus-Regular.ttf', fb.size - 4)
    x, y = 92, 1150
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.rectangle((x - 40, y - 40, x + max(fb.getlength(big), fs.getlength(small)) + 60, y + 190), fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(40)))
    d.rectangle((x, y + 4, x + 10, y + 90), fill=RED)
    d.text((x + 34, y), big, font=fb, fill=WHITE, anchor='la')
    lw = fb.getlength(big); d.line((x + 34, y + 112, x + 34 + lw, y + 112), fill=YEL, width=3)
    if small: d.text((x + 34, y + 128), small, font=fs, fill=CREAM, anchor='la')
    im.save(out); return out

# ---------- the shot list (voice time; OFF added on the timeline) ----------
A = L + 'arch/'
def build():
    m = map_png(L + 'prep/map.png')
    iwm1 = esr_still(L + 'stills/iwm_flensburg_mai1945_BU6713.jpg', (230, 0, 530, 534), L + 'prep/iwm6713.png')
    iwm2 = esr_still(L + 'stills/iwm_flensburg_mai1945_BU6711.jpg', (200, 0, 520, 570), L + 'prep/iwm6711.png')
    S = [  # (start, kind, args)
        (0.00, 'img', dict(path=prep(12), cx=.5, z0=1.0, z1=1.14)),
        (3.40, 'vid', dict(path=G + 'nacht1.mp4', ss=0.5, speed=1.0, dark=0.18)),
        (7.00, 'vid', dict(path=UD + 'video2.mp4', ss=0.0, speed=1.0)),
        (12.60, 'vid', dict(path=G + 'nacht2_tunnel.mp4', ss=0.0, speed=1.0)),
        (15.60, 'vid', dict(path=G + 'nacht5_schuss.mp4', ss=0.0, speed=0.55)),
        (19.36, 'img', dict(path=prep(1), cx=.5, z0=1.0, z1=1.12)),
        (25.88, 'img', dict(path=m, cx=.5, z0=1.0, z1=1.25)),
        (31.00, 'img', dict(path=prep(3), cx=.45, z0=1.14, z1=1.0)),
        (35.34, 'vid', dict(path=A + 'A1.mp4', ss=0.0, speed=1.0)),
        (42.50, 'vid', dict(path=A + 'A2.mp4', ss=0.0, speed=1.0)),
        (49.04, 'img', dict(path=prep(2), cx=.5, z0=1.0, z1=1.12)),
        (54.20, 'vid', dict(path=A + 'A3.mp4', ss=0.0, speed=1.0)),
        (58.50, 'vid', dict(path=A + 'A4.mp4', ss=0.0, speed=1.0)),
        (63.06, 'img', dict(path=prep(10), cx=.6, z0=1.0, z1=1.12)),
        (66.70, 'img', dict(path=prep(8), cx=.55, z0=1.12, z1=1.0)),
        (70.40, 'vid', dict(path=A + 'A5.mp4', ss=0.0, speed=1.0)),
        (76.02, 'vid', dict(path=A + 'A6.mp4', ss=0.0, speed=1.0)),
        (80.30, 'img', dict(path=prep(5), cx=.5, z0=1.0, z1=1.12)),
        (84.68, 'img', dict(path=prep(4), cx=.5, z0=1.0, z1=1.14)),
        (88.70, 'img', dict(path=prep(9), cx=.5, z0=1.0, z1=1.12)),
        (93.06, 'vid', dict(path=A + 'A7.mp4', ss=0.0, speed=1.0)),
        (96.52, 'img', dict(path=prep(6), cx=.33, z0=1.0, z1=1.1)),
        (99.42, 'img', dict(path=prep(7), cx=.72, z0=1.1, z1=1.0)),
        (101.42, 'vid', dict(path=A + 'A8.mp4', ss=0.0, speed=1.0)),
        (108.22, 'img', dict(path=iwm1, cx=.5, z0=1.0, z1=1.12)),
        (115.14, 'img', dict(path=iwm2, cx=.5, z0=1.12, z1=1.0)),
        (118.30, 'vid', dict(path=UD + 'video1.mp4', ss=0.0, speed=0.5)),
        (121.54, 'img', dict(path=prep(12), cx=.5, z0=1.25, z1=1.05)),
        (126.82, 'vid', dict(path=UD + 'video2.mp4', ss=5.6, speed=1.0)),
        (130.34, 'vid', dict(path=G + 'nacht4_silhouette.mp4', ss=0.0, speed=0.653)),
        (138.00, 'vid', dict(path=UD + 'video3.mp4', ss=0.0, speed=1.0, z0=1.0, z1=1.0)),
        (143.03, 'vid', dict(path=UD + 'video1.mp4', ss=0.0, speed=1.0, z0=1.0, z1=1.0)),
        (148.07, 'vid', dict(path=G + 'nacht5_schuss.mp4', ss=2.0, speed=1.0)),
        (151.02, 'img', dict(path=prep(1), cx=.5, z0=1.05, z1=1.22, gray=1.0)),
        (154.64, 'vid', dict(path=G + 'nacht2_tunnel.mp4', ss=3.0, speed=0.42)),
        (159.50, 'vid', dict(path=UD + 'video1.mp4', ss=0.0, speed=0.55)),
        (165.06, 'vid', dict(path=A + 'A9.mp4', ss=0.0, speed=1.0)),
        (169.50, 'img', dict(path=prep(12), cx=.5, z0=1.16, z1=1.0)),
    ]
    end = TOTAL - OFF
    segs = []
    for i, (t0, kind, a) in enumerate(S):
        t1 = S[i + 1][0] if i + 1 < len(S) else end
        dur = t1 - t0 + (OFF if i == 0 else 0)
        out = SEG + '%02d.mp4' % i
        if not os.path.exists(out):
            if kind == 'img': img_shot(out, dur=dur, **a)
            else: vid_shot(out, dur=dur, **a)
        segs.append(out); print('seg', i, round(dur, 2), flush=True)
    with open(SEG + 'list.txt', 'w') as f:
        for s in segs: f.write("file '%s'\n" % s)
    cut = L + 'cut.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', SEG + 'list.txt', '-c:v', 'libx264', '-crf', '15', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), cut])
    return cut

LABELS = [(7.35, '14. MAI 1945', 'Flensburg-Mürwik'), (19.6, 'WOLFGANG LÜTH', 'Kapitän zur See'), (63.3, 'U 181', 'Höhepunkt seines Ruhms'),
          (76.3, 'ÜBER 200 TAGE', 'auf Feindfahrt, 1943'), (85.0, 'BRILLANTEN', '9. August 1943'), (101.7, 'MARINESCHULE MÜRWIK', 'Flensburg, September 1944'),
          (130.6, 'MATHIAS GOTTLOB', 'Matrosengefreiter, 18 Jahre')]
FLASH = 138.0 + 5.04 - 0.22      # lightning at the end of the tunnel clip, into the sentry scene (voice time)
SHOT = 143.03 + 76 / 24          # muzzle flash frame of video1

def sound():
    mix = L + 'mix.m4a'
    if os.path.exists(mix): return mix
    T = TOTAL
    rain = f"anoisesrc=d={T}:c=pink:a=0.5,highpass=f=900,lowpass=f=9000,volume=0.35,"
    # rain under the night sections only
    rain += ("volume='if(between(t,3.6,19.7)+between(t,115.4,165.4),1,0)':eval=frame,"
             "afade=t=in:st=3.6:d=0.6,afade=t=out:st=165.0:d=0.6")
    music = L + '../urs/t1/musik.mp3'
    fl = (f"[0:a]adelay={int(OFF * 1000)}:all=1,apad,atrim=0:{T}[v];"
          f"[1:a]atrim=0:{T},asetpts=PTS-STARTPTS,volume=0.16,afade=t=in:d=2,afade=t=out:st={T - 3}:d=3[m];"
          f"{rain}[r0];[r0]aformat=channel_layouts=stereo[r];"
          f"[2:a]adelay={int((FLASH + OFF) * 1000)}:all=1,volume=0.9[th];"
          f"[3:a]adelay={int((SHOT + OFF) * 1000)}:all=1,volume=1.1[sh];"
          f"[v]asplit[v1][v2];[m][v2]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=800[md];"
          f"[v1][md][r][th][sh]amix=inputs=5:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    run(['ffmpeg', '-v', 'error', '-y', '-i', VOICE, '-ss', '30', '-i', music, '-i', L + 'm/thunder.mp3', '-i', L + 'm/shot.mp3',
         '-filter_complex', fl, '-map', '[a]', '-t', f'{T:.3f}', '-c:a', 'aac', '-b:a', '192k', mix])
    return mix

def finish(cut, mix, out):
    labs = []
    for j, (t, big, small) in enumerate(LABELS):
        labs.append((t + OFF, label_png(big, small, L + 'prep/lab%02d.png' % j)))
    fc = ("[0:v]eq=saturation=0.82:contrast=1.04,colorbalance=rs=0.04:gs=0.01:bs=-0.05:rm=0.03:bm=-0.03,"
          "eq=brightness='0.010*sin(t*13.1)+0.007*sin(t*29.7)':eval=frame,format=gbrp[a];"
          "[1:v]loop=-1:size=150,setpts=N/30/TB,scale=1080:1920,format=gbrp[d];[a][d]blend=all_mode=screen:all_opacity=0.30,format=yuv420p[b];"
          "[b]noise=alls=7:allf=t,vignette=PI/4.6[n]")
    inp, prev = [], '[n]'
    for j, (t0, fn) in enumerate(labs):
        inp += ['-loop', '1', '-t', '4.6', '-itsoffset', f'{t0:.2f}', '-i', fn]
        fc += f";[{j + 3}:v]format=rgba,fade=in:st={t0:.2f}:d=0.5:alpha=1,fade=out:st={t0 + 4.0:.2f}:d=0.5:alpha=1[l{j}];{prev}[l{j}]overlay=0:0:eof_action=pass[o{j}]"; prev = f'[o{j}]'
    ft = FLASH + OFF
    fc += (f";color=c=white:s={W}x{H}:d=1.2,format=rgba,fade=in:st=0:d=0.18:alpha=1,fade=out:st=0.22:d=0.7:alpha=1,setpts=PTS+{ft - 0.18:.3f}/TB[fl];"
           f"{prev}[fl]overlay=0:0:eof_action=pass,fade=t=in:st=0:d=0.4,fade=t=out:st={TOTAL - 1.6:.2f}:d=1.6[v]")
    run(['ffmpeg', '-v', 'error', '-stats', '-y', '-i', cut, '-i', L + '../urs/t1/dust.mp4', '-i', mix, *inp, '-filter_complex', fc, '-map', '[v]', '-map', '2:a',
         '-t', f'{TOTAL:.3f}', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy', '-movflags', '+faststart', out])

if __name__ == '__main__':
    cut = build(); mix = sound()
    finish(cut, mix, L + 'Lueth_Shorts_DE.mp4'); print('DONE', flush=True)
