# Ursprung des 2. Weltkriegs: montage engine (approved look of Teil 1 v2)
# photos: border trim, full frame, smooth sub-pixel zoom (in / out alternating, always centred), no pan
# films: 16:9 crop, grey; graphics: gfx.py; 1.2 s crossfades; old-film finish (sepia, flicker, grain, dust, vignette);
# newsreel title labels (style C) top left; bold gold serif subtitles bottom centre.
import json, os, subprocess, sys, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
U = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/urs/'
sys.path.insert(0, U + 't1/code'); sys.path.insert(0, U + 'eng')
from look import trim
W, H, FPS, XF, OFF, TAIL = 1920, 1080, 30, 1.2, 0.4, 1.2
LS = '/usr/share/fonts/truetype/liberation/'
VID = {'P': U + 'vid/wwf_prelude_to_war.mp4', 'B': U + 'vid/berlin-symphony-of-a-metropolis-1927-by-walter-ruttmann.mp4', 'V': U + 'vid/yt_2BVpuNFFrcE.mp4',
       'N': U + 'vid/yt_4-y_oz06_cQ.mp4', 'D': U + 'vid/yt_TR1fP8TvM-k.mp4', 'E': U + 'vid/1936-02-12_Ethiopia.mp4', 'S': U + 'vid/1936-09-09_Spain_Air_Raid.mp4',
       'C': U + 'vid/1938-09-19_War_Crisis.mp4', 'U468': U + 'vid/1939-08-23_UfA_468.mp4', 'U470': U + 'vid/1939-09-07_UfA_470.mp4',
       'R': U + 'vid/adolf-hitler-and-the-german-people-remilitarized-the-rhineland-1936-1.mp4', 'A': U + 'vid/german-troops-march-into-austria-1938-color.mp4'}
def run(c): subprocess.run(c, check=True)
def ffpipe(out, n=None):
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)
class Part:
    def __init__(self, d):
        self.d = d if d.endswith('/') else d + '/'; self.wd = json.load(open(self.d + 'words.json'))
        self.tok = [re.sub(r'[^a-zäöüß0-9]', '', w[0].lower()) for w in self.wd]
        self.voice = self.d + 'vcut.wav'
        self.end = self.wd[-1][2] + OFF + TAIL
    def K(self, ph, i=0):
        """start time (film time) of a phrase of the narration"""
        if isinstance(ph, (int, float)): return float(ph)
        p = [re.sub(r'[^a-zäöüß0-9]', '', x.lower()) for x in ph.split()]
        h = [k for k in range(len(self.tok) - len(p) + 1) if self.tok[k:k + len(p)] == p]
        assert len(h) >= 1, ph
        return self.wd[h[0] + i][1] + OFF
# ---------- shots ----------
def img_shot(src, d, out, zin):
    """smooth zoom: per-frame affine transform with sub-pixel precision from a 2x source"""
    im = trim(Image.open(src)).convert('L'); w, h = im.size; r = W / H
    cw, ch = (w, w / r) if w / h < r else (h * r, h); x0, y0 = (w - cw) / 2, (h - ch) / 2
    S = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W * 2, H * 2), Image.LANCZOS).convert('RGB')
    n = int(round(d * FPS)); p = ffpipe(out); z0, z1 = (1.0, 1.10) if zin else (1.10, 1.0)
    for f in range(n):
        z = z0 + (z1 - z0) * (f / max(1, n - 1)); s = 1 / (2 * z)   # source pixels per output pixel = 2/z ... inverse map
        a = 2 / z; cx, cy = W, H   # centre of the 2x source
        data = (a, 0, cx - a * W / 2, 0, a, cy - a * H / 2)
        p.stdin.write(S.transform((W, H), Image.AFFINE, data, resample=Image.BILINEAR).tobytes())
    p.stdin.close(); p.wait()
CROP = {'N': 'crop=944:531:168:94', 'D': 'crop=944:531:168:94'}   # HD copies of the Capra films are pillarboxed 4:3 inside 16:9
def vid_shot(key, ss, d, out, zin):
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', VID[key], '-t', f'{d:.3f}', '-vf',
         f"{CROP.get(key, 'crop=iw:iw*9/16')},scale={W}:{H}:flags=lanczos,fps={FPS},format=gray,format=yuv420p", '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', out])
def build_shots(part, SH, sd):
    os.makedirs(sd, exist_ok=True); clips = []
    starts = [part.K(s[0]) if i else 0.0 for i, s in enumerate(SH)]
    for i, s in enumerate(SH):
        t0 = starts[i]; t1 = starts[i + 1] if i + 1 < len(SH) else part.end; d = t1 - t0 + XF; out = sd + '%03d.mp4' % i
        if not os.path.exists(out):
            kind = s[1]
            if kind == 'img': img_shot(U + 'img/' + s[2] + '.jpg' if not s[2].startswith('/') else s[2], d, out, i % 2 == 0)
            elif kind == 'vid': vid_shot(s[2], s[3], d, out, i % 2 == 0)
            elif kind == 'gfx':
                import gfx; gfx.render(s[2], d, out, [part.K(a) - t0 for a in (s[3] if len(s) > 3 else [])])
        clips.append((out, d)); print('shot', i, flush=True)
    return clips
def xfade(clips, out, end):
    if os.path.exists(out): return
    # chain in groups to keep the filter graph small
    inp, fl = [], []; acc = clips[0][1] - XF; prev = '[0:v]'
    for c, _ in clips: inp += ['-i', c]
    for i in range(1, len(clips)):
        o = f'[x{i}]'; fl.append(f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={acc:.3f}{o}'); prev = o; acc += clips[i][1] - XF
    run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', prev, '-t', f'{end:.3f}', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', out])
# ---------- text ----------
WEAK = {'der', 'die', 'das', 'den', 'dem', 'des', 'ein', 'eine', 'einen', 'einem', 'einer', 'eines', 'und', 'an', 'in', 'im', 'zu', 'zur', 'zum', 'von', 'vom', 'mit', 'auf', 'aus', 'bei', 'nach', 'vor', 'über', 'um', 'als', 'wie', 'es', 'er', 'sie', 'wurde', 'war'}
def chunks(WD):
    def stop(w): return w[-1] in '.:?!' and not (w[:-1].isdigit() and int(w[:-1]) <= 31) and not w.endswith('J.P.')
    def comma(w): return w[-1] in ',;'
    ph, cur = [], []
    for w in WD:
        cur.append(w)
        if stop(w[0]) or (comma(w[0]) and len(cur) >= 3): ph.append(cur); cur = []
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
    return [(c[0][1] + OFF, c[-1][2] + OFF, ' '.join(x[0] for x in c)) for c in out]
def ass(WD, out):
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
# ---------- finish ----------
def finish(part, cut, labels, out):
    if os.path.exists(out): return
    sub = part.d + 'subs.ass'; ass(part.wd, sub); dz = U + 't1/dust.mp4'
    fc = ("[0:v]format=rgb24,colorchannelmixer=rr=.36:rg=.62:rb=.14:gr=.32:gg=.58:gb=.12:br=.25:bg=.47:bb=.10,"
          "eq=contrast=0.92:brightness=-0.02,eq=brightness='0.012*sin(t*13.1)+0.008*sin(t*29.7)':eval=frame,format=gbrp[a];"
          "[1:v]loop=-1:size=150,setpts=N/30/TB,format=gbrp[d];[a][d]blend=all_mode=screen:all_opacity=0.55,format=yuv420p[b];"
          "[b]noise=alls=9:allf=t,vignette=PI/4.2[n]")
    lab_in = []; prev = '[n]'
    for j, (ph, big, small) in enumerate(labels):
        t0 = part.K(ph); fn = part.d + 'lab%02d.png' % j; label_png(big, small, fn)
        lab_in += ['-loop', '1', '-t', '6.4', '-itsoffset', f'{t0:.2f}', '-i', fn]
        fc += f";[{j + 2}:v]format=rgba,fade=in:st={t0:.2f}:d=0.6:alpha=1,fade=out:st={t0 + 5.6:.2f}:d=0.6:alpha=1[l{j}];{prev}[l{j}]overlay=0:0:eof_action=pass[o{j}]"; prev = f'[o{j}]'
    fc += f";{prev}subtitles={sub}[v]"
    run(['ffmpeg', '-v', 'error', '-y', '-i', cut, '-i', dz, *lab_in, '-filter_complex', fc, '-map', '[v]', '-t', f'{part.end:.3f}',
         '-c:v', 'libx264', '-crf', '21', '-preset', 'medium', '-tune', 'grain', '-pix_fmt', 'yuv420p', out])
def build(pdir, SH, LAB):
    part = Part(pdir); clips = build_shots(part, SH, part.d + 'shots/')
    xfade(clips, part.d + 'cut.mp4', part.end); print('cut ok', flush=True)
    finish(part, part.d + 'cut.mp4', LAB, part.d + 'pic.mp4'); print('pic ok', part.end, flush=True)
def mix(pdir, out, music_ss=20, vol=0.14):
    """voice in front, the calm music lower than in the first test (0.14 instead of 0.22) and ducked under the narration"""
    part = Part(pdir); pic = part.d + 'pic.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-i', pic, '-i', part.voice, '-ss', str(music_ss), '-i', U + 't1/musik.mp3', '-filter_complex',
         f"[1]adelay={int(OFF * 1000)},aformat=channel_layouts=stereo,asplit[v1][v2];[2]atrim=0:{part.end:.2f},volume={vol},afade=t=in:d=2,afade=t=out:st={part.end - 3:.2f}:d=3[m];"
         "[m][v2]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=600[md];[v1][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
         '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-b:v', '5500k', '-maxrate', '7000k', '-bufsize', '14000k', '-preset', 'medium', '-tune', 'grain',
         '-c:a', 'aac', '-b:a', '192k', '-shortest', out])
