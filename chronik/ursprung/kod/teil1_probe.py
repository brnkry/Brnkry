# Ursprung des 2. Weltkriegs, Teil 1 (Probe): archive photos with slow Ken Burns, Versailles 1919 film, 1.2 s crossfades,
# old-film finish (sepia, grain, dust, scratches, flicker, vignette), gold serif subtitles and typewriter labels like the reference.
import json, os, subprocess, sys, math, random
import numpy as np
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
U = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/urs/'
T = U + 't1/'; S = T + 'shots/'; os.makedirs(S, exist_ok=True)
W, H, FPS, XF = 1920, 1080, 30, 1.2
WD = json.load(open(T + 'words.json')); OFF = 0.4                         # voice starts 0.4 s into the film
END = WD[-1][2] + OFF + 2.5
I = lambda n: U + 'img/' + n + '.jpg'; V = U + 'vid/yt_2BVpuNFFrcE.mp4'
# (start, kind, source, params): photos get (zoom from, zoom to, x from, x to, y from, y to) in 0..1 of the free pan room
SH = [
 (0.0,   'img', I('Polen_1939__Bild_146-1979-056-18A'), (1.00, 1.12, .5, .5, .5, .4)),
 (9.3,   'img', I('Polen_1939__Bild_101I-001-0288-29'), (1.10, 1.00, .3, .6, .5, .5)),
 (14.0,  'img', I('Reichswehr__BildY_1-548-1667-65'), (1.00, 1.10, .5, .5, .5, .5)),
 (18.2,  'img', I('Arbeitslose__Bild_102-10369'), (1.12, 1.02, .5, .5, .3, .6)),
 (22.0,  'img', I('Voelkerbund__Bild_102-00265'), (1.00, 1.10, .2, .6, .5, .5)),
 (27.8,  'img', I('Versailles__KART_756-011'), (1.05, 1.25, .2, .7, .2, .6)),
 (33.3,  'img', I('Reichswehr__BildY_1-548-13388'), (1.10, 1.00, .6, .4, .5, .5)),
 (39.2,  'img', I('Polen_Einmarsch__Bild_183-E10855'), (1.00, 1.12, .5, .5, .5, .5)),
 (45.2,  'img', I('Voelkerbund__Bild_102-00677'), (1.08, 1.00, .5, .5, .5, .5)),
 (50.8,  'img', I('Dawes__Bild_102-00258'), (1.00, 1.10, .5, .5, .3, .5)),
 (53.6,  'img', I('Voelkerbund__Bild_102-00266'), (1.10, 1.00, .4, .6, .5, .5)),
 (59.3,  'img', I('Polen_1939__Bild_183-E10457'), (1.00, 1.12, .5, .5, .5, .5)),
 (67.8,  'img', I('Polen_Einmarsch__Bild_101I-318-0061-33A'), (1.10, 1.00, .5, .5, .4, .6)),
 (72.2,  'vid', V, 10.0),     # Versailles palace front
 (77.8,  'vid', V, 52.0),     # crowds at the fountains
 (82.7,  'img', I('Versailles__Bild_254-10'), (1.00, 1.10, .5, .5, .5, .5)),
 (90.7,  'vid', V, 272.0),    # Hall of Mirrors interior
 (99.8,  'vid', V, 306.0),    # crowd inside
 (108.2, 'vid', V, 168.0),    # arrival of diplomats and officers
 (115.6, 'img', I('Versailles_Spiegelsaal__Bild_183-R02091'), (1.00, 1.14, .5, .5, .5, .45)),
]
LABELS = [(3.3, '1. SEPTEMBER 1939'), (61.2, 'ÜBER 60 MILLIONEN TOTE'), (92.4, '28. JUNI 1919'), (96.0, 'SPIEGELSAAL, VERSAILLES')]
def run(c): subprocess.run(c, check=True)
def shot(i):
    t0, kind, src, p = SH[i]; t1 = SH[i + 1][0] if i + 1 < len(SH) else END; d = t1 - t0 + XF; n = int(round(d * FPS)); out = S + '%02d.mp4' % i
    if os.path.exists(out): return out, d
    if kind == 'img':
        im = Image.open(src).convert('L'); w, h = im.size; r = 16 / 9
        cw, ch = (w, w / r) if w / h < r else (h * r, h); x0, y0 = (w - cw) / 2, (h - ch) / 2
        im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((3840, 2160), Image.LANCZOS)
        z0, z1, xa, xb, ya, yb = p; tmp = S + 'src%02d.png' % i; im.save(tmp)
        # smooth: zoom and pan computed per output frame with sub-pixel precision via a 4K source
        z = f"{z0}+({z1}-{z0})*(on/{n})"
        x = f"({xa}+({xb}-{xa})*(on/{n}))*(iw-iw/zoom)"; y = f"({ya}+({yb}-{ya})*(on/{n}))*(ih-ih/zoom)"
        run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', tmp, '-vf', f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={FPS},format=yuv420p", '-frames:v', str(n), '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', out])
    else:
        run(['ffmpeg', '-v', 'error', '-y', '-ss', str(p), '-i', src, '-t', str(d), '-vf', f"crop=iw:iw*9/16,scale={W}:{H}:flags=lanczos,fps={FPS},format=gray,format=yuv420p", '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', out])
    return out, d
def dust():
    """5 s loop of dust, hairs and vertical scratches on black (screen-blended later)"""
    out = T + 'dust.mp4'
    if os.path.exists(out): return out
    rng = random.Random(7); p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    sx = [rng.uniform(100, W - 100) for _ in range(2)]
    for f in range(5 * FPS):
        im = Image.new('L', (W, H), 0); d = ImageDraw.Draw(im)
        for _ in range(rng.randint(2, 9)):
            x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1, 3.5); d.ellipse((x - r, y - r, x + r, y + r), fill=rng.randint(120, 230))
        if rng.random() < 0.12:
            x, y = rng.uniform(0, W), rng.uniform(0, H); d.line([(x, y), (x + rng.uniform(-30, 30), y + rng.uniform(10, 40)), (x + rng.uniform(-30, 30), y + rng.uniform(30, 70))], fill=170, width=1)
        for k in range(2):
            sx[k] += rng.uniform(-3, 3)
            if rng.random() < 0.55: d.line([(sx[k], 0), (sx[k] + rng.uniform(-2, 2), H)], fill=rng.randint(60, 120), width=1)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait(); return out
def chunks():
    """subtitle parts like the reference: one phrase per line, cut after a comma or full stop; a phrase over
    ~58 characters is cut into balanced halves, never right after an article or preposition.
    A day number with a dot (28., 1.) is an ordinal, a year with a dot (1919.) ends the sentence."""
    def stop(w): return w[-1] in '.:?!' and not (w[:-1].isdigit() and int(w[:-1]) <= 31)
    def comma(w): return w[-1] in ',;'
    WEAK = {'der', 'die', 'das', 'den', 'dem', 'des', 'ein', 'eine', 'einen', 'einem', 'einer', 'eines', 'und', 'an', 'in', 'im', 'zu', 'zur', 'zum', 'von', 'vom', 'mit', 'auf', 'aus', 'bei', 'nach', 'vor', 'über', 'um', 'als', 'wie', 'es', 'er', 'sie'}
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
def ass():
    def ts(t): return '%d:%02d:%05.2f' % (t // 3600, t % 3600 // 60, t % 60)
    L = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {W}', f'PlayResY: {H}', '', '[V4+ Styles]',
         'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
         'Style: Sub,Liberation Serif,46,&H2070C3CD,&H000000FF,&H9E000000,&H9E000000,0,0,0,0,100,100,0,0,3,7,0,2,60,60,72,1',
         'Style: Lab,Liberation Mono,30,&H00283228,&H000000FF,&H00C8DCE8,&H00000000,1,0,0,0,100,100,1,0,3,9,0,1,95,60,175,1',
         '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    cs = chunks()
    for i, (a, b, t) in enumerate(cs):
        b2 = cs[i + 1][0] - 0.05 if i + 1 < len(cs) and cs[i + 1][0] - b < 0.7 else b + 0.45
        L.append(f'Dialogue: 0,{ts(a)},{ts(b2)},Sub,,0,0,0,,{{\\fad(380,150)}}{t}')
    for t0, s in LABELS:   # typewriter: one more letter every 55 ms, then holds for 4.5 s
        full = '{\\c&H2828C8&}■ {\\c&H283228&}'
        for k in range(1, len(s) + 1):
            a = t0 + (k - 1) * 0.055; b = t0 + k * 0.055 if k < len(s) else t0 + len(s) * 0.055 + 4.5
            fade = '{\\fad(0,300)}' if k == len(s) else ''
            L.append(f'Dialogue: 1,{ts(a)},{ts(b)},Lab,,0,0,0,,{fade}{full}{s[:k]}')
    open(T + 'subs.ass', 'w').write('\n'.join(L) + '\n'); return T + 'subs.ass'
if __name__ == '__main__':
    clips = [shot(i) for i in range(len(SH))]; print('shots ok', flush=True)
    # crossfade chain
    inp, fl = [], []; acc = clips[0][1] - XF
    for c, _ in clips: inp += ['-i', c]
    prev = '[0:v]'
    for i in range(1, len(clips)):
        o = f'[x{i}]'; fl.append(f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={acc:.3f}{o}'); prev = o; acc += clips[i][1] - XF
    if not os.path.exists(T + 'cut.mp4'): run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', prev, '-t', f'{END:.3f}', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', T + 'cut.mp4'])
    print('cut ok', flush=True)
    dz = dust(); sub = ass()
    # old-film finish: sepia tone (warm, low contrast like the reference), flicker, grain, dust and scratches, vignette, gate weave
    fc = ("[0:v]format=rgb24,colorchannelmixer=rr=.36:rg=.62:rb=.14:gr=.32:gg=.58:gb=.12:br=.25:bg=.47:bb=.10,"
          "eq=contrast=0.92:brightness=-0.02:saturation=1.0,eq=brightness='0.018*sin(t*13.1)+0.012*sin(t*29.7)':eval=frame,"
          "crop=iw-12:ih-12:6+3*sin(t*2.3):6+3*cos(t*1.7),scale=1920:1080,format=gbrp[a];"
          "[1:v]loop=-1:size=150,setpts=N/30/TB,format=gbrp[d];[a][d]blend=all_mode=screen:all_opacity=0.55,format=yuv420p[b];"
          f"[b]noise=alls=9:allf=t,vignette=PI/4.2,subtitles={sub}[v]")
    run(['ffmpeg', '-v', 'error', '-y', '-i', T + 'cut.mp4', '-i', dz, '-filter_complex', fc, '-map', '[v]', '-t', f'{END:.3f}', '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-tune', 'grain', '-pix_fmt', 'yuv420p', T + 'pic.mp4'])
    print('pic ok', flush=True)
    # sound: voice + calm music under it (ducks under the voice), fade out
    run(['ffmpeg', '-v', 'error', '-y', '-i', T + 'pic.mp4', '-i', T + 'vcut.wav', '-ss', '20', '-i', T + 'musik.mp3', '-filter_complex',
         f"[1]adelay={int(OFF * 1000)},aformat=channel_layouts=stereo,asplit[v1][v2];[2]atrim=0:{END:.2f},volume=0.22,afade=t=in:d=2,afade=t=out:st={END - 3:.2f}:d=3[m];"
         "[m][v2]sidechaincompress=threshold=0.04:ratio=4:attack=30:release=500[md];[v1][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
         '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', T + 'Ursprung_Teil1_Probe.mp4'])
    print('done', END)
