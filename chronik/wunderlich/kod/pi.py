# "Pilot im Wrack" (Hans Wunderlich, Birkelse 2017) short, German, CDM. 9:16, real photos and film only, no AI scenes.
# Reuses the Lüth shot renderers (lu.py): photo push-in, video cover crop, Marcellus labels.
import os, sys, json, math, subprocess, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
D = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, D + '../lueth'); import lu
from lu import img_shot, vid_shot, label_png, enc, W, H, FPS, FD, YEL, RED, WHITE, CREAM
VO = 0.4
TOTAL = 88.9 + VO + 1.5
SEG = D + 'segs/'; os.makedirs(SEG, exist_ok=True); os.makedirs(D + 'prep', exist_ok=True)
U1 = D + 'user/177958889_1511140728.jpg_0a28c947_2K.jpg'            # black and white portrait
U2 = D + 'user/182820426_0908a5e4-daf7-42ba-be7c-30c75ad86016.jpeg_fe7da18b_2K.jpg'   # colourised uniform portrait
ING = D + 'ing.mp4'; MAR = D + 'arch/nmesserschmitt-bf-109-in-motion-ww-2-german-fighter-sie-hiess-marie-lc-6y-0-vkzc-a.mp4'
F = D + 'foto/'

def duo(out):
    """hook: the two portraits stacked, gold rule between them"""
    if os.path.exists(out): return out
    can = Image.new('RGB', (int(W * 1.6), int(H * 1.6)), (10, 10, 10)); cw, ch = can.size[0], can.size[1] // 2
    for k, (p, cy) in enumerate([(U1, .38), (U2, .30)]):
        im = Image.open(p).convert('RGB'); w, h = im.size; bw = w; bh = bw * ch / cw
        if bh > h: bh = h; bw = bh * cw / ch
        y0 = min(max(cy * h - bh / 2, 0), h - bh); x0 = (w - bw) / 2
        can.paste(im.resize((cw, ch), Image.LANCZOS, box=(x0, y0, x0 + bw, y0 + bh)), (0, k * ch))
    d = ImageDraw.Draw(can); d.rectangle((0, ch - 4, cw, ch + 4), fill=(214, 178, 100))
    can.save(out); return out

def map_png(out):
    if os.path.exists(out): return out
    MW, MH = int(W * 1.6), int(H * 1.6); LA0, LA1 = 54.4, 58.2; lc = 9.9
    span = (LA1 - LA0) * (MW / MH) / math.cos(math.radians(56.5)); L0, L1 = lc - span / 2, lc + span / 2
    def xy(lo, la): return ((lo - L0) / (L1 - L0) * MW, (LA1 - la) / (LA1 - LA0) * MH)
    rng = np.random.default_rng(5); paper = np.full((MH, MW, 3), (196, 178, 140), np.float32)
    nz = np.array(Image.fromarray((rng.random((MH // 8, MW // 8)) * 255).astype(np.uint8)).resize((MW, MH), Image.BICUBIC), np.float32) / 255
    paper *= (0.85 + 0.22 * nz)[..., None]
    sea = Image.fromarray(np.clip(paper * np.array([0.78, 0.86, 0.92]), 0, 255).astype(np.uint8)); land = Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8))
    mk = Image.new('L', (MW, MH), 0); dm = ImageDraw.Draw(mk); geo = json.load(open(D + '../urs/pak/geo.json')); lines = []
    for f in geo['features']:
        g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            ring = [xy(lo, la) for lo, la in poly[0]]
            if len(ring) > 2: dm.polygon(ring, fill=255); lines.append(ring)
    im = Image.composite(land, sea, mk); d = ImageDraw.Draw(im)
    for r in lines: d.line(r + [r[0]], fill=(110, 86, 58), width=3)
    yy, xx = np.mgrid[0:MH, 0:MW]; e = np.minimum(np.minimum(xx, MW - xx), np.minimum(yy, MH - yy)) / 260.0
    im = Image.fromarray((np.array(im.filter(ImageFilter.GaussianBlur(0.8)), np.float32) * (0.55 + 0.45 * np.clip(e, 0, 1))[..., None]).astype(np.uint8))
    d = ImageDraw.Draw(im); fm = ImageFont.truetype(FD + 'Marcellus-Regular.ttf', 110); fs = ImageFont.truetype(FD + 'Marcellus-Regular.ttf', 66)
    d.text(xy(11.0, 56.75), 'KATTEGAT', font=fs, fill=(70, 80, 92), anchor='mm'); d.text(xy(7.2, 57.3), 'NORDSEE', font=fs, fill=(70, 80, 92), anchor='mm')
    for name, lo, la, big, dx, dy in [('BIRKELSE', 9.67, 57.15, True, -60, -70), ('Aalborg', 9.92, 57.05, False, 60, 40)]:
        x, y = xy(lo, la); r = 30 if big else 18
        d.ellipse((x - r, y - r, x + r, y + r), fill=RED if big else (60, 40, 30), outline=(50, 10, 10), width=4)
        d.text((x + dx, y + dy), name, font=fm if big else fs, fill=(40, 26, 16), anchor='rm' if dx < 0 else 'lm')
    im.save(out); return out

def crop_vid(out, path, ss, dur, cx=.5, top=.03, z=1.25, speed=1.0):
    """16:9 film cut to 9:16 with the window kept clear of the burnt-in captions at the bottom and the logo at the top left"""
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip().split(','))
    ch = int(h / z) // 2 * 2; cw = int(ch * 9 / 16) // 2 * 2; x0 = int(min(max(cx * w - cw / 2, 0), w - cw)); y0 = int(top * h)
    n = int(round(dur * FPS))
    vf = (f"trim=start={ss}:duration={dur * speed + 0.2},setpts=(PTS-STARTPTS)/{speed},tpad=stop_mode=clone:stop_duration=2,fps={FPS},"
          f"crop={cw}:{ch}:{x0}:{y0},scale={W}:{H}:flags=lanczos,setsar=1")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf', vf, '-frames:v', str(n), '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out], check=True)

def bund():
    out = D + 'prep/bf109.png'
    if os.path.exists(out): return out
    im = Image.open(F + 'a01_bf109_bundesarchiv.jpg').convert('RGB'); w, h = im.size
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse((0.75 * w, 0.33 * h, 0.89 * w, 0.60 * h), fill=255)   # tail swastika
    im = Image.composite(im.filter(ImageFilter.GaussianBlur(10)), im, m.filter(ImageFilter.GaussianBlur(8))); im.save(out); return out

def shots():
    duo_p = duo(D + 'prep/duo.png'); mp = map_png(D + 'prep/map.png'); bf = bund()
    return [
        (0.00, 'img', dict(path=duo_p, z0=1.0, z1=1.08)),
        (5.74, 'img', dict(path=F + 'n04_historynet.jpg', cx=.66, z0=1.0, z1=1.10)),
        (10.20, 'crop', dict(path=ING, ss=3.2, cx=.55)),
        (13.30, 'img', dict(path=mp, z0=1.0, z1=1.22)),
        (18.58, 'crop', dict(path=ING, ss=18.2, cx=.45)),
        (21.16, 'crop', dict(path=ING, ss=48.2, cx=.40, speed=0.8)),
        (25.20, 'crop', dict(path=ING, ss=43.6, cx=.45, speed=0.8)),
        (28.90, 'vid', dict(path=MAR, ss=55.0, speed=1.0)),
        (32.10, 'vid', dict(path=MAR, ss=78.5, speed=1.0)),
        (35.52, 'img', dict(path=F + 'n03_globalnews2.jpg', cx=.45, z0=1.0, z1=1.10)),
        (38.02, 'vid', dict(path=MAR, ss=90.0, speed=0.8)),
        (41.12, 'crop', dict(path=ING, ss=16.6, cx=.42)),
        (44.10, 'crop', dict(path=ING, ss=24.1, cx=.50, speed=0.7)),
        (46.60, 'img', dict(path=F + 'n02_globalnews1.jpg', cx=.40, z0=1.0, z1=1.10)),
        (49.40, 'crop', dict(path=ING, ss=79.6, cx=.42, speed=0.8)),
        (52.24, 'vid', dict(path=MAR, ss=102.5, speed=1.0)),
        (55.00, 'vid', dict(path=MAR, ss=108.5, speed=1.0)),
        (57.68, 'img', dict(path=U2, cx=.5, z0=1.0, z1=1.10)),
        (63.60, 'img', dict(path=U1, cx=.5, z0=1.12, z1=1.0)),
        (66.60, 'vid', dict(path=MAR, ss=87.0, speed=0.8)),
        (69.00, 'vid', dict(path=MAR, ss=150.0, speed=1.0)),
        (71.30, 'vid', dict(path=MAR, ss=61.0, speed=1.0)),
        (74.00, 'vid', dict(path=MAR, ss=126.5, speed=1.0)),
        (77.20, 'crop', dict(path=ING, ss=30.0, cx=.50, speed=0.5)),
        (80.20, 'crop', dict(path=ING, ss=54.2, cx=.45, speed=0.8)),
        (83.30, 'img', dict(path=bf, cx=.45, z0=1.0, z1=1.12)),
        (86.40, 'img', dict(path=duo_p, z0=1.10, z1=1.0)),
    ]

LABELS = [(13.5, 'BIRKELSE', 'Nordjütland, März 2017'), (26.74, 'MESSERSCHMITT BF 109', 'über 33.000 gebaut'),
          (57.9, 'HANS WUNDERLICH', 'geboren am 22. Juli 1925'), (67.0, '10. OKTOBER 1944', 'Absturz bei Aalborg')]

def main():
    S = shots(); end = TOTAL - VO; segs = []
    for i, (t0, kind, a) in enumerate(S):
        t1 = S[i + 1][0] if i + 1 < len(S) else end
        dur = t1 - t0 + (VO if i == 0 else 0)
        out = SEG + hashlib.md5(repr((kind, sorted(a.items()), round(dur, 3))).encode()).hexdigest()[:12] + '.mp4'
        if not os.path.exists(out):
            tmp = out[:-4] + '.part.mp4'
            if kind == 'img': img_shot(tmp, dur=dur, **a)
            elif kind == 'crop': crop_vid(tmp, dur=dur, **a)
            else: vid_shot(tmp, dur=dur, **a)
            os.rename(tmp, out)
        segs.append(out); print('seg', i, round(dur, 2), flush=True)
    with open(SEG + 'list.txt', 'w') as f:
        for s in segs: f.write("file '%s'\n" % s)
    cut = D + 'cut.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', SEG + 'list.txt', '-c:v', 'libx264', '-crf', '15', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), cut], check=True)
    T = TOTAL
    fl = (f"[0:a]adelay={int(VO * 1000)}:all=1,aformat=sample_rates=48000:channel_layouts=stereo[v];"
          f"[1:a]atrim=0:{T},aformat=sample_rates=48000:channel_layouts=stereo,dynaudnorm=f=400:g=41:m=12,loudnorm=I=-30:LRA=4:TP=-5,"
          f"afade=t=out:st={T - 1.2}:d=1.2[m];"
          f"[v][m]amix=inputs=2:normalize=0:duration=longest,atrim=0:{T},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', D + 'voice.mp3', '-i', D + 'music.mp3', '-filter_complex', fl, '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', D + 'mix.m4a'], check=True)
    labs = [(t + VO, label_png(b, s, D + 'prep/lab%02d.png' % j)) for j, (t, b, s) in enumerate(LABELS)]
    fc = "[0:v]eq=contrast=1.03:saturation=0.95,noise=alls=5:allf=t,vignette=PI/5[n]"; inp = []; prev = '[n]'
    for j, (t0, fn) in enumerate(labs):
        inp += ['-loop', '1', '-t', '4.6', '-itsoffset', f'{t0:.2f}', '-i', fn]
        fc += f";[{j + 2}:v]format=rgba,fade=in:st={t0:.2f}:d=0.5:alpha=1,fade=out:st={t0 + 4.0:.2f}:d=0.5:alpha=1[l{j}];{prev}[l{j}]overlay=0:0:eof_action=pass[o{j}]"; prev = f'[o{j}]'
    fc += f";{prev}fade=t=out:st={T - 0.6:.2f}:d=0.6[v]"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cut, '-i', D + 'mix.m4a', *inp, '-filter_complex', fc, '-map', '[v]', '-map', '1:a', '-t', f'{T:.3f}',
                    '-c:v', 'libx264', '-b:v', '10M', '-maxrate', '14M', '-bufsize', '20M', '-preset', 'faster', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart',
                    D + 'Pilot_Shorts_DE_v3.mp4'], check=True)
    print('DONE', flush=True)

if __name__ == '__main__':
    main()
