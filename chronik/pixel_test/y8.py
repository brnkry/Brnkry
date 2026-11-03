# Yamamoto 8-bit test (20 s, English voice of the CoP short): everything is drawn at 180 x 320 and scaled up 6x with hard pixels,
# like a 16-bit game cut-scene. Photos of Yamamoto become pixel portraits (downscaled, few colours, no dithering).
import sys, os, json, math, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)) + '/'
Y = D + '../yama/'
LW, LH, K, FPS, T = 180, 320, 6, 30, 20.0
WORDS = json.load(open(Y + 'words.json'))
def wt(s, after=0.0):
    for w, a, b in WORDS:
        if a >= after - 0.01 and w.lower().strip('.,').startswith(s.lower()): return a
    raise KeyError(s)
F8 = ImageFont.truetype(D + 'fonts/PressStart2P.ttf', 8); F16 = ImageFont.truetype(D + 'fonts/PressStart2P.ttf', 16)
PAL = {'k': (12, 12, 20), 'w': (240, 240, 232), 'y': (255, 204, 40), 'r': (220, 48, 48), 'o': (255, 132, 32), 'g': (96, 104, 88), 'G': (150, 160, 140),
       'b': (28, 60, 120), 'B': (40, 96, 170), 'c': (90, 150, 220), 's': (120, 180, 230), 'n': (60, 64, 76), 'N': (110, 114, 126), 'e': (36, 200, 90)}
def sprite(rows, col):
    h, w = len(rows), max(len(r) for r in rows); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); px = im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.': px[x, y] = PAL.get(ch, col) + (255,)
    return im
P38 = sprite(["....N.........N...",
              "...NNN.......NNN..",
              "NNNNNNNNNNNNNNNNNs",
              ".gggggNNNNgggggg..",
              "....N....NN.......",], (0, 0, 0))
SHIP_J = sprite(["..........N..........",
                 ".........NNN...N.....",
                 "....N...NNNNN.NNN....",
                 "..NNNNNNNNNNNNNNNNN..",
                 "nnnnnnnnnnnnnnnnnnnnn",
                 ".nnnnnnnnnnnnnnnnnnn.",], (0, 0, 0))
SHIP_R = SHIP_J.transpose(Image.FLIP_LEFT_RIGHT)
@functools.lru_cache(None)
def P38x2(): return P38.resize((P38.width * 2, P38.height * 2), Image.NEAREST)
@functools.lru_cache(None)
def portrait(name, w, box):
    """photo -> pixel portrait: crop, downscale, 14 colours, no dither"""
    im = Image.open(Y + 'img/' + name).convert('RGB').crop(box)
    im = im.resize((w, int(w * im.height / im.width)), Image.LANCZOS)
    return im.quantize(colors=14, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
def txt(d, xy, s, col='w', f=F8, anchor='la', shadow=True):
    if shadow: d.text((xy[0] + 1, xy[1] + 1), s, font=f, fill=PAL['k'], anchor=anchor)
    d.text(xy, s, font=f, fill=PAL[col], anchor=anchor)
def typed(s, t, t0, cps=18): return s[:max(0, min(len(s), int((t - t0) * cps)))] if t >= t0 else ''
def box(d, x0, y0, x1, y1):
    d.rectangle((x0, y0, x1, y1), fill=PAL['k']); d.rectangle((x0 + 1, y0 + 1, x1 - 1, y1 - 1), outline=PAL['w']); d.rectangle((x0 + 3, y0 + 3, x1 - 3, y1 - 3), outline=PAL['N'])
def sea(c, t, horizon=200, dark=False):
    d = ImageDraw.Draw(c)
    sky = [(20, 30, 70), (30, 50, 100), (50, 80, 140), (80, 120, 180), (120, 160, 210)] if not dark else [(8, 10, 24), (14, 18, 40), (22, 28, 56), (30, 38, 70), (40, 50, 86)]
    for i, col in enumerate(sky): d.rectangle((0, i * horizon // 5, LW, (i + 1) * horizon // 5), fill=col)
    for i, col in enumerate([PAL['s'], PAL['c'], PAL['B'], PAL['b'], (18, 40, 90)]): d.rectangle((0, horizon + i * 24, LW, horizon + (i + 1) * 24), fill=col)
    d.rectangle((0, horizon + 120, LW, LH), fill=(12, 28, 70))
    for k in range(60):   # wave glints scrolling
        y = horizon + 4 + (k * 37) % 150; sp = 6 + (y - horizon) * 0.25; x = int((k * 53 - t * sp) % (LW + 20)) - 10
        d.rectangle((x, y, x + 2 + (y - horizon) // 30, y), fill=PAL['w'] if y < horizon + 40 else PAL['s'])
def hud_top(d, t):
    d.rectangle((0, 0, LW, 13), fill=PAL['k']); txt(d, (4, 3), 'CHRONICLE OF POWER', 'y', shadow=False)
    txt(d, (LW - 4, 3), '%05d' % int(t * 137) if t < 1e9 else '', 'w', anchor='ra', shadow=False)
# ---------- scenes ----------
def s_planes(c, t):
    sea(c, t, 180)
    d = ImageDraw.Draw(c); d.rectangle((140, 40, 152, 52), fill=PAL['y'])   # sun
    n = 16 if t >= wt('sixteen') - 0.1 else 4
    for i in range(n):   # 4 x 4 formation, low over the water, slight bob
        row, col = i // 4, i % 4; x = int(-90 + t * 30 + col * 42 - row * 14) % 300 - 60; y = 112 + row * 16 + int(2 * math.sin(t * 6 + i))
        c.alpha_composite(P38x2(), (x, y))
    box(d, 10, 54, 150, 84)
    txt(d, (16, 61), typed('18 APRIL 1943', t, wt('April')), 'y'); txt(d, (16, 73), typed('P-38 x16', t, wt('sixteen'), 26), 'w')
    if t >= wt('one') - 0.1:   # target reticle on "one man"
        u = min(1, (t - wt('one') + 0.1) / 0.3); r = int(30 - 18 * u); cx, cy = 80, 228
        d.rectangle((cx - r, cy - r, cx + r, cy + r), outline=PAL['r']); d.line((cx - r - 6, cy, cx - r + 4, cy), fill=PAL['r']); d.line((cx + r - 4, cy, cx + r + 6, cy), fill=PAL['r'])
        if int(t * 4) % 2: txt(d, (cx, cy + r + 6), 'TARGET: 1', 'r', anchor='ma')
def s_decode(c, t, t0):
    d = ImageDraw.Draw(c); d.rectangle((0, 0, LW, LH), fill=(6, 12, 8)); rng = np.random.default_rng(3)
    for col in range(22):   # falling cipher
        sp = rng.uniform(30, 70); off = rng.uniform(0, 300)
        for k in range(14):
            y = int((off + (t - t0) * sp + k * 10) % 340) - 10; ch = '0123456789ABCDEF'[(col * 7 + k + int(t * 8)) % 16]
            d.text((col * 8 + 2, y), ch, font=F8, fill=(30, 120 + 9 * k, 60) if k < 13 else (200, 255, 200))
    if t >= wt('decoded') - 0.1:
        box(d, 14, 120, 166, 200); flash = int(t * 6) % 2
        txt(d, (90, 130), 'DECODED', 'e' if flash else 'w', F16, 'ma')
        txt(d, (90, 156), typed('ARRIVAL BALLALE', t, wt('decoded') + 0.2, 24), 'w', anchor='ma'); txt(d, (90, 170), typed('0800 HRS', t, wt('decoded') + 0.8, 24), 'y', anchor='ma')
def s_player(c, t, t0):
    d = ImageDraw.Draw(c); d.rectangle((0, 0, LW, LH), fill=(18, 20, 44))
    for y in range(0, LH, 8): d.line((0, (y + int(t * 20)) % LH, LW, (y + int(t * 20)) % LH), fill=(24, 28, 60))
    P = portrait('s1-2.jpg', 100, (300, 0, 1500, 1500)); x0, y0 = 40, 56
    u = min(1, (t - t0) / 0.5); yy = int(lerp(LH, y0, u))   # slides up
    box(d, x0 - 4, yy - 4, x0 + P.width + 3, yy + P.height + 3); c.paste(P, (x0, yy))
    box(d, 10, 190, 150, 258)
    txt(d, (80, 198), 'PLAYER 1', 'y', anchor='ma')
    txt(d, (80, 212), typed('ISOROKU', t, wt('Isoroku'), 20), 'w', F16, 'ma'); txt(d, (80, 230), typed('YAMAMOTO', t, wt('Yamamoto') - 0.1, 20), 'w', F16, 'ma')
    if t >= wt('planned') - 0.1 and t < wt('never') - 0.2: txt(d, (80, 248), typed('MISSION: PEARL HARBOR', t, wt('planned'), 22)[:21].replace('MISSION: ', ''), 'r', anchor='ma')
    if t >= wt('never') - 0.2:   # "and he never wanted that war"
        box(d, 10, 190, 150, 258)   # the name card turns into a dialogue box
        txt(d, (80, 204), typed('HE NEVER', t, wt('never') - 0.1, 22), 'w', F16, 'ma'); txt(d, (80, 222), typed('WANTED', t, wt('wanted') - 0.1, 22), 'w', F16, 'ma')
        txt(d, (80, 240), typed('THIS WAR.', t, wt('that') - 0.05, 22), 'y', F16, 'ma')
def lerp(a, b, u): return a + (b - a) * u
def s_tsushima(c, t, t0):
    sea(c, t, 170, dark=False)
    d = ImageDraw.Draw(c); bob = int(math.sin(t * 3) * 1.5)
    J = SHIP_J.resize((SHIP_J.width * 3, SHIP_J.height * 3), Image.NEAREST); R = SHIP_R.resize((SHIP_R.width * 2, SHIP_R.height * 2), Image.NEAREST)
    c.alpha_composite(J, (4, 158 + bob)); c.alpha_composite(R, (LW - R.width - 18, 160 - bob))
    for k, tf in enumerate((t0 + 0.4, t0 + 1.3, t0 + 2.2)):   # muzzle flashes and smoke
        if tf <= t < tf + 0.15: d.rectangle((68, 160, 76, 166), fill=PAL['y'])
        if tf <= t < tf + 0.15: d.rectangle((LW - 62, 168, LW - 56, 172), fill=PAL['o'])
    ts = wt('Russian') - 0.5   # the Russian shell arcs over and hits
    if ts <= t < wt('shell') + 0.05:
        u = (t - ts) / (wt('shell') + 0.05 - ts); x = lerp(LW - 60, 36, u); y = 164 - 60 * math.sin(math.pi * u)
        d.rectangle((x - 1, y - 1, x + 1, y + 1), fill=PAL['w'])
    te = wt('shell') + 0.05
    if te <= t < te + 0.6:
        r = int(4 + 22 * (t - te) / 0.6)
        for rr, col in ((r, 'o'), (r * 2 // 3, 'y'), (r // 3, 'w')): d.rectangle((38 - rr, 176 - rr, 38 + rr, 176 + rr), fill=PAL[col])
    box(d, 10, 54, 150, 84); txt(d, (16, 61), 'TSUSHIMA 1905', 'y'); txt(d, (16, 73), typed('YOUNG OFFICER', t, wt('young'), 22), 'w')
    P = portrait('s2-3.jpg', 44, (400, 100, 1400, 1300)); box(d, 16, 200, 64, 200 + P.height + 7); c.paste(P, (20, 204))
    # hand icon: 5 fingers, two vanish on "fingers"
    hx, hy = 96, 204; d.rectangle((hx, hy + 14, hx + 30, hy + 34), fill=(230, 180, 140))
    lost = t >= wt('fingers')
    for f in range(5):
        if lost and f in (1, 2): continue
        d.rectangle((hx + f * 6 + (0 if f < 4 else 2), hy + (4 if f == 4 else 0), hx + f * 6 + 4, hy + 14), fill=(230, 180, 140))
    txt(d, (hx + 15, hy + 40), 'x3' if lost else 'x5', 'r' if lost else 'w', anchor='ma')
SC = [(0.0, lambda c, t: s_planes(c, t)), (wt('They') - 0.1, lambda c, t: s_decode(c, t, wt('They') - 0.1)),
      (wt('His', 10) - 0.1, lambda c, t: s_player(c, t, wt('His', 10) - 0.1)), (wt('As', 15) - 0.1, lambda c, t: s_tsushima(c, t, wt('As', 15) - 0.1))]
def wipe(t):
    """8-bit checker wipe at each cut: blocks close and open over 0.3 s"""
    for a, _ in SC[1:]:
        if a - 0.15 <= t < a + 0.15: return 1 - abs(t - a) / 0.15
    return 0
def frame(t):
    k = max(i for i, (a, _) in enumerate(SC) if a <= t)
    c = Image.new('RGBA', (LW, LH), (0, 0, 0, 255)); SC[k][1](c, t)
    d = ImageDraw.Draw(c)
    w = wipe(t)
    if w > 0:
        n = max(1, int(w * 10))
        for by in range(0, LH, 10):
            for bx in range(0, LW, 10): d.rectangle((bx, by, bx + n - 1, by + n - 1), fill=PAL['k'])
    if wt('shell') + 0.05 <= t < wt('shell') + 0.25:   # hit: screen shake + red flash
        c = Image.blend(c, Image.new('RGBA', (LW, LH), PAL['r'] + (255,)), 0.35); c = c.transform(c.size, Image.AFFINE, (1, 0, (-1) ** int(t * 30) * 2, 0, 1, 0))
    return c.convert('RGB').resize((LW * K, LH * K), Image.NEAREST)
if __name__ == '__main__':
    if sys.argv[1:] and sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[2:]]; P = Image.new('RGB', (270 * len(ts), 480))
        for i, tt in enumerate(ts): P.paste(frame(tt).resize((270, 480), Image.NEAREST), (i * 270, 0))
        P.save(D + 'prev.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (LW * K, LH * K), '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '14', '-preset', 'medium', D + 'v.mp4'], stdin=subprocess.PIPE)
    for n in range(int(T * FPS)): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', D + 'v.mp4', '-i', Y + 'mix.wav', '-map', '0:v', '-map', '1:a', '-af', 'atrim=0:%.2f,afade=t=out:st=%.2f:d=0.6' % (T, T - 0.6),
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', D + 'Yamamoto_8bit_Test_20s.mp4'], check=True)
    print('ok')
