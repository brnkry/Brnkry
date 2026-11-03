# "Jungen 1945" CDM short: Boran's colourised footage full screen (9:16 cut per shot, keeping the boy in frame),
# subtitles in the hook type of the style-A videos (Montserrat 900 with the worn texture), words appearing with the voice,
# small enough that the film stays in front; nothing else on screen.
import sys, os, json, subprocess
import numpy as np
from PIL import Image
J = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, J + '../egon/code')
import eg
from eg import W, H, CREAM, YEL, clamp, put, gtext_a, mont
FPS = 30; SRC = J + 'dl/1103 (2).mov'
WORDS = json.load(open(J + 'words.json'))
# shots of the colourised file: (start, end, crop x of a 1215 x 2160 window in the 3840 x 2160 frame)
SHOTS = [(0.0, 7.467, 1250), (7.467, 11.133, 1658), (11.133, 14.333, 1169), (14.333, 19.067, 1169), (19.067, 24.1, 1313), (24.1, 30.133, 1658)]
END = 30.133
YELW = {'1945', 'jungen.', 'flakhelfer', 'volkssturm', '16', '60', 'tausenden', 'erhobenen', 'händen.'}
def chunks():
    out = []; cur = []
    for i, (w, a, b) in enumerate(WORDS):
        cur.append((w, a, b))
        n = sum(len(x[0]) + 1 for x in cur)
        nxt = WORDS[i + 1][0] if i + 1 < len(WORDS) else None
        if w[-1] in '.,' or len(cur) >= 3 or n >= 16 or (nxt and n + len(nxt) > 20):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out
CH = chunks()
def subs(can, t):
    for k, c in enumerate(CH):
        a = c[0][1] - 0.05; e = CH[k + 1][0][1] - 0.05 if k + 1 < len(CH) else END
        if not (a <= t < e): continue
        ws = [w.upper().rstrip('.,') if w not in ('1945', '16', '60') else w for w, _, _ in c]
        size = eg.fit([' '.join(ws)], 84, 900, -2); f = mont(size, 900)
        Ls = [gtext_a(s, f, YEL if c[i][0].lower() in YELW else CREAM, [clamp((t - c[i][1] + 0.05) / 0.18)] * len(s), -2) for i, s in enumerate(ws)]
        sp = f.getlength(' ') * 0.8; tot = sum(L.width for L in Ls) + sp * (len(Ls) - 1); x = 540 - tot / 2
        for L in Ls:
            put(can, L, x, 1400, 'l'); x += L.width + sp
def frames():
    for a, b, x0 in SHOTS:
        n = int(round(b * FPS)) - int(round(a * FPS))
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', '%.4f' % a, '-i', SRC, '-frames:v', str(n), '-vf', 'crop=1215:2160:%d:0,scale=1080:1920:flags=lanczos' % x0,
                              '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
        for i in range(n):
            buf = p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3: break
            yield Image.frombuffer('RGB', (W, H), buf)
        p.wait()
if __name__ == '__main__':
    prev = sys.argv[1:] and sys.argv[1] == 'preview'
    out = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '12M', '-preset', 'medium', J + 'jv.mp4'], stdin=subprocess.PIPE) if not prev else None
    picks = [float(x) for x in sys.argv[2:]] if prev else []; got = []
    for n, im in enumerate(frames()):
        t = n / FPS
        if prev and not any(abs(t - q) < 0.5 / FPS for q in picks): continue
        c = im.convert('RGBA'); subs(c, t)
        if prev: got.append(c.convert('RGB').resize((270, 480)))
        else: out.stdin.write(np.asarray(c.convert('RGB')).tobytes())
    if prev:
        P = Image.new('RGB', (270 * len(got), 480)); [P.paste(g, (i * 270, 0)) for i, g in enumerate(got)]; P.save(J + 'prev.jpg')
    else: out.stdin.close(); out.wait(); print('frames', n + 1)
