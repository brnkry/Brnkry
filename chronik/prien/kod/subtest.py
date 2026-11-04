# test: the whole narration as subtitles in the text area of style A (Egon), words appearing with the voice,
# a page of up to 3 lines is cleared when full; numbers and names stand out (yellow, bigger)
import sys, os, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pr, eg
from pr import ws, WORDS, quote, YEL, CREAM, FPS, W, H
KEY = re.compile(r'^(\d[\d.]*|Osterfeld|Calw|Prien|Günther|Segelschiff|Handelsmarine|Reichsmarine|Royal|Oak|Scapa|Flow|U)$')
def pages(maxc=17, nl=3):
    out = []; page = []; line = []
    for w, a, b in WORDS:
        s = w.upper().rstrip('.,')
        if line and len(' '.join(x for x, _, _ in line)) + 1 + len(s) > maxc:
            page.append(line); line = []
            if len(page) == nl: out.append(page); page = []
        line.append((s, a, w)); 
        if w[-1] == '.':   # a sentence end closes the line and the page: every sentence starts on a fresh page
            page.append(line); line = []; out.append(page); page = []
    if line: page.append(line)
    if page: out.append(page)
    return out
PG = pages()
def subs(c, t, ox, oy, y0=1230):
    """words fade in with the voice; only the key words (numbers, names) are yellow and a little bigger"""
    from eg import gtext_a, put, mont, clamp
    for k, pg in enumerate(PG):
        a = pg[0][0][1] - 0.05; e = PG[k + 1][0][0][1] - 0.05 if k + 1 < len(PG) else 1e9
        if not (a <= t < e): continue
        for i, l in enumerate(pg):
            size = eg.fit([' '.join(s for s, _, _ in l)], 70, 900, -2); y = y0 + i * 90
            Ls = []
            for s_, wa, w in l:
                key = bool(KEY.match(w.rstrip('.,'))); f = mont(int(size * (1.12 if key else 1.0)), 900)
                al = clamp((t - wa + 0.04) / 0.3); Ls.append(gtext_a(s_, f, YEL if key else CREAM, [al] * len(s_), -2))
            sp = mont(size, 900).getlength(' ') * 0.8; tot = sum(L.width for L in Ls) + sp * (len(Ls) - 1); x = 540 - tot / 2 + ox
            for L in Ls: put(c, L, x, y + oy, 'l'); x += L.width + sp
def s_born_sub(c, t, ox, oy):
    pr.enter(c, pr.SP(754, 560, 11, cap='Günther Prien'), t, (380, 610), -3, ox, oy, (2, 3, 0.08), main=True)
    pr.later(c, pr.SP(835, 420, 12), t, ws('See') - 0.1, (770, 860), 5, ox, oy, (1, 0.2))
    subs(c, t, ox, oy)
pr.SCN[1] = (pr.SCN[1][0], s_born_sub)
if __name__ == '__main__':
    a, b = float(sys.argv[1]), float(sys.argv[2]); out = sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', out + '_v.mp4'], stdin=subprocess.PIPE)
    for n in range(int(a * FPS), int(b * FPS)): p.stdin.write(np.asarray(pr.frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out + '_v.mp4', '-ss', str(a), '-t', str(b - a), '-i', pr.E + 'vcut.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', out + '.mp4'], check=True)
    print('ok')
