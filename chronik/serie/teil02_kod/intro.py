# Teil 2, opening (first paragraph, about 20 s), magazine mixed with style A.
# Spread 1  left: masthead (series title, Teil 2), a framed colour photo, the first sentence set on the page as it is spoken.
#           right: a dark style-A feature page: prints fly in and settle (soft), BLITZKRIEG in big grunge capitals, then a red pen
#           crosses it out at "Dienstvorschrift" (no stamps, no boxes); a yellow line "stand in keiner Dienstvorschrift".
# At "Nach fünf Wochen" the camera moves to the right page's lower half: "5 WOCHEN" and the 1939 map of Poland from the book.
import sys, os, functools, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lcore import *
from mixtest import mont, img, gtext, a_page, a_print, card, title, YEL, CREAM
P = lambda w_, a=0.0: ws(w_, a)
def soft_throw(pg, t, t0, P_, to, r1, frm=(1, -1), dur=1.1):
    """calmer than the shorts: the print glides in from just outside the page, a small turn, settles; no big scale jump"""
    if t < t0: return
    u = eout((t - t0) / dur); x = lerp(to[0] + frm[0] * 900, to[0], u); y = lerp(to[1] + frm[1] * 500, to[1], u)
    card(pg, P_, x, y, lerp(r1 + 12 * frm[0], r1, u), lerp(1.12, 1.0, u) - 0.006 * max(0, t - t0 - dur), (1 - u) * 5)
def pen_strike(pg, t, t0, a_, b_, wd=16, dur=0.45):
    if t < t0: return
    u = eout((t - t0) / dur); d = ImageDraw.Draw(pg); x = lerp(a_[0], b_[0], u); y = lerp(a_[1], b_[1], u)
    d.line((a_[0], a_[1], x, y), fill=(196, 40, 36), width=wd)
def masthead_l(t):
    pg = M.gloss(1).copy(); runhead(pg, True, 1); d = ImageDraw.Draw(pg)
    for i, c in enumerate(((24, 24, 26), (196, 30, 34), (236, 186, 32))): d.rectangle((110, 196 + i * 92, 128, 196 + (i + 1) * 92), fill=c)
    d.text((160, 186), 'Deutschland im', font=serif(118, 900), fill=TXT); d.text((160, 326), 'Zweiten Weltkrieg', font=serif(118, 400), fill=TXT)
    for i, c in enumerate(((24, 24, 26), (196, 30, 34), (236, 186, 32))): d.rectangle((110, 490 + i * 9, PW - 110, 490 + (i + 1) * 9), fill=c)
    d.text((110, 545), 'TEIL 2 · DER ÜBERFALL AUF POLEN', font=sans(38, 800), fill=ACC, anchor='lm')
    d.text((PW - 110, 545), 'SEPTEMBER BIS OKTOBER 1939', font=sans(28, 600), fill=GREY, anchor='rm')
    g = img('hoffmann_s49_0'); x0, y0, bw, bh = 110, 620, 1180, 720; sc = max(bw / g.width, bh / g.height); cw, ch = bw / sc, bh / sc
    pg.paste(g.resize((bw, bh), Image.LANCZOS, box=((g.width - cw) / 2, (g.height - ch) / 2, (g.width + cw) / 2, (g.height + ch) / 2)), (x0, y0))
    d.line((110, 1370, 260, 1370), fill=ACC, width=5); d.text((110, 1388), 'Deutsche Infanterie überquert eine Brücke, September 1939', font=italic(32), fill=GREY)
    body(pg, t, 110, 1470, 'Der Feldzug gegen Polen gilt bis heute als der erste Blitzkrieg der Geschichte.', P('Der') - 0.3, accent=('Blitzkrieg',), size=54, lh=74, maxw=1180)
    return pg
def feature_r(t):
    pg = a_page().copy().convert('RGBA')
    soft_throw(pg, t, P('Feldzug') - 0.2, a_print('hoffmann_s23_0', 560, 3), (420, 470), -7, (-1, -1))
    soft_throw(pg, t, P('Polen') - 0.1, a_print('hoffmann_s39_0', 720, 4), (930, 560), 5, (1, -1))
    soft_throw(pg, t, P('heute') - 0.1, a_print('hoffmann_s36_0', 600, 5), (640, 900), -2, (1, 1))
    t_b = P('Blitzkrieg')
    if t >= t_b:
        k = eout((t - t_b) / 0.35); L = gtext('BLITZKRIEG', mont(190), CREAM, k, -8)
        pg.alpha_composite(L, (int(PW / 2 - L.width / 2), 1180))
        pen_strike(pg, t, P('Dienstvorschrift') - 0.2, (PW / 2 - L.width / 2 + 10, 1180 + 130), (PW / 2 + L.width / 2 - 10, 1180 + 100), 18)
    if t >= P('stand'):
        for i, s in enumerate(('STAND IN KEINER', 'DIENSTVORSCHRIFT')):
            tw = P('keiner') if i == 0 else P('Dienstvorschrift')
            if t >= tw - 0.1:
                L = gtext(s, mont(74), YEL, clamp((t - tw + 0.1) / 0.3), -3); pg.alpha_composite(L, (int(PW / 2 - L.width / 2), 1420 + i * 82))
    return pg.convert('RGB')
def map_r(t):
    """right page, second state: the prints slide away, 5 WOCHEN and the period map of Poland"""
    pg = feature_r(t).convert('RGBA'); t0 = P('Nach', 9)
    if t < t0: return pg.convert('RGB')
    u = eout((t - t0) / 0.7); cover = a_page().copy().convert('RGBA'); cover.putalpha(int(255 * u)); pg.alpha_composite(cover)
    soft_throw(pg, t, t0 + 0.1, a_print('soeldner_karte_s162', 560, 9), (PW / 2, 700), -2, (-1, 1))
    title(pg, t, P('fünf', 9), '5', ['WOCHEN'], PW / 2, 1330, 260, 110)
    if t >= P('aufgeteilt'):
        for i, s in enumerate(('AUFGETEILT ZWISCHEN', 'ZWEI DIKTATUREN')):
            tw = P('aufgeteilt') if i == 0 else P('Diktaturen')
            L = gtext(s, mont(64), CREAM, clamp((t - tw + 0.1) / 0.3), -3); pg.alpha_composite(L, (int(PW / 2 - L.width / 2), 1500 + i * 72))
    return pg.convert('RGB')
OVV = (PW, 905, 0.56)
CAMS = [(0.0, PW, 905, 0.53), (P('Blitzkrieg') - 0.9, PW + 700, 1000, 0.62, 1.0),       # the whole spread while the first sentence is set; then onto the feature page
        (P('Doch') - 0.4, PW + 700, 1300, 0.95, 1.0),                                # close on BLITZKRIEG for the strike
        (P('Nach', 9) - 0.2, PW + 700, 1050, 0.64, 1.0)]
BOOK = Book([(masthead_l, map_r)], [], CAMS, spine=100)
T_END = P('Und', 15) - 0.2
def frame(t): return BOOK(t)
if __name__ == '__main__':
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[2:]]; Pc = Image.new('RGB', (3 * 640, ((len(ts) + 2) // 3) * 360))
        for i, t in enumerate(ts): Pc.paste(frame(t).resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
        Pc.save(LB + 'chk/intro.jpg', quality=88); sys.exit()
    if sys.argv[1] == 'T': print(round(T_END, 2)); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
