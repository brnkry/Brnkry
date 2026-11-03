# Heinz-Wolfgang Schnaufer, subtitle mode (as prien/code/ps.py): the whole narration stays on screen as subtitles (centred, words appear with the voice,
# punctuation kept); at key moments some words become a style-A title (big number left, yellow words right, like 19 MINUTEN)
# with the rest of the sentence above/below; some sentences come on a torn white paper strip. Pictures/camera = sc.py.
import sys, os, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageChops
import sc as pr, eg
from sc import WORDS, YEL, CREAM, FPS, W, H, E
from eg import gtext_a, put, mont, clamp, typed, grunge, INK

KEY = re.compile(r'^(\d[\d.]*|Schnaufer|Heinz-Wolfgang|Calw|Weinkellerei|Nachtjagd|Messerschmitt|Bf|Royal|Air|Force|Halifax|Köln|Rumpelhardt|Gänsler|Ritterkreuz|Gespenst|St|Trond|Kommodore|Nachtjagdgeschwaders|Lancaster-Bomber|Hyde|Park|Imperial|War|Museum|Bordeaux|Lastwagen|Gasflaschen)$')
def bare(w): return w.rstrip('.,:')
def wi(w, after=0.0): return next(i for i, (x, a, _) in enumerate(WORDS) if a >= after - 0.05 and bare(x) == w)
# style-A moments: (first, last, [big word idxs], big text override or None, [[yellow word idxs] per line])
EM = [
    (wi('Er', 11), wi('geboren', 11), [wi('1922')], None, [[wi('in', 12)], [wi('Calw')]]),
    (wi('Mit', 16), wi('Abitur'), [wi('17')], None, [[wi('Jahren', 17)]]),
    (wi('und', 22), wi('110', 23), [wi('110', 23)], None, [[wi('Messerschmitt')], [wi('Bf', 23)]]),
    (wi('Seinen', 29.9), wi('1942'), [wi('1942')], None, [[wi('Juni')]]),
    (wi('Im', 50), wi('Abschuss', 53), [wi('1944')], None, [[wi('Oktober')]]),
    (wi('Wenig'), wi('Jahren', 56), [wi('22')], None, [[wi('Jahren', 56)]]),
    (wi('Am', 61), wi('1945'), [wi('1945')], None, [[wi('21')], [wi('Februar')]]),
    (wi('sieben', 68), wi('Minuten'), [wi('19')], None, [[wi('Minuten')]]),
    (wi('Insgesamt'), wi('Abschüsse'), [wi('121')], None, [[wi('Abschüsse')]]),
    (wi('Im', 94.9), wi('1950'), [wi('1950')], None, [[wi('Juli')]]),
    (wi('Heinz-Wolfgang', 108), wi('alt'), [wi('28')], None, [[wi('Jahre', 109)]]),
]
# paper strips (first, last)
ST = [(wi('Am', 42), wi('Ritterkreuz')), (wi('Bei', 44.9), wi('Trond')), (wi('Ein', 83.5), wi('Museum'))]

def tok(i): return (WORDS[i][0].upper(), WORDS[i][1], WORDS[i][0])
CY = 1335   # vertical centre of every subtitle page / title block (photos above, YouTube title below)
PAIRS = {('Royal', 'Air'), ('Air', 'Force'), ('St', 'Trond'), ('Hyde', 'Park'), ('Imperial', 'War'), ('War', 'Museum'), ('Heinz-Wolfgang', 'Schnaufer'), ('Bf', '110'), ('Fritz', 'Rumpelhardt'), ('Wilhelm', 'Gänsler'), ('21', 'Februar'), ('Messerschmitt', 'Bf')}
def glued(a, b): return (bare(a), bare(b)) in PAIRS
def wrap(idx, maxc):
    out = []; line = []
    for i in idx:
        s = WORDS[i][0].upper()
        if line and len(' '.join(x for x, _, _ in line)) + 1 + len(s) > maxc:
            carry = [line.pop()] if len(line) > 1 and glued(line[-1][2], WORDS[i][0]) else []   # names stay on one line
            out.append(line); line = carry
        line.append(tok(i))
    if line: out.append(line)
    return out
def pages(maxc=19, nl=2):
    out = []; page = []; line = []; i = 0
    def flush():
        nonlocal page, line
        if line: page.append(line); line = []
        if page: out.append(('P', page, page[-1][-1][1])); page = []
    while i < len(WORDS):
        em = next((e for e in EM if e[0] == i), None); st = next((s for s in ST if s[0] == i), None)
        if em: flush(); out.append(('EM', em, WORDS[em[1]][1])); i = em[1] + 1; continue
        if st: flush(); out.append(('ST', st, WORDS[st[1]][1])); i = st[1] + 1; continue
        w, a, b = WORDS[i]; s = w.upper()
        if line and len(' '.join(x for x, _, _ in line)) + 1 + len(s) > maxc:
            carry = [line.pop()] if len(line) > 1 and glued(line[-1][2], w) else []
            page.append(line); line = carry
            if len(page) == nl: out.append(('P', page, page[-1][-1][1])); page = []
        line.append((s, a, w))
        if w[-1] == '.': flush()   # every sentence starts on a fresh page
        i += 1
    flush()
    return out
PG = pages()
def pfirst(pg): return pg[1][0][0][1] if pg[0] == 'P' else WORDS[pg[1][0]][1]
# a page shows from its first word, but never leaves before its last word has been visible for 0.45 s
VS = []
for k, pg in enumerate(PG):
    a = pfirst(pg) - 0.05
    if k: a = max(a, PG[k - 1][2] + 0.45)
    VS.append(a)

def sline(c, t, l, y, size0=58):
    size = eg.fit([' '.join(s for s, _, _ in l)], size0, 900, -2); Ls = []
    for s_, wa, w in l:
        key = bool(KEY.match(bare(w))); f = mont(int(size * (1.12 if key else 1.0)), 900)
        al = clamp((t - wa + 0.04) / 0.2); Ls.append(gtext_a(s_, f, YEL if key else CREAM, [al] * len(s_), -2))
    sp = mont(size, 900).getlength(' ') * 0.55 - 13   # gtext_a pads each word by 20 px; a little more air than v2
    gaps = [sp + (4 if KEY.match(bare(l[k][2])) or KEY.match(bare(l[k + 1][2])) else 0) for k in range(len(l) - 1)]
    tot = sum(L.width for L in Ls) + sum(gaps); x = 540 - tot / 2
    for k, L in enumerate(Ls): put(c, L, x, y, 'l'); x += L.width + (gaps[k] if k < len(gaps) else 0)
def emph(c, t, em):
    """the big number and its yellow words in reading order (number left or right, whichever is said first),
    the rest of the sentence as subtitle lines above and below; the whole block centred on CY"""
    i0, i1, ib, btxt, iys = em
    T = lambda i: WORDS[i][1] - 0.04
    smallk = [i for l in iys for i in l]; allk = ib + smallk
    pre = wrap(range(i0, min(allk)), 21); post = wrap(range(max(allk) + 1, i1 + 1), 21)
    big = btxt or ' '.join(WORDS[i][0].upper() for i in ib)
    small = [' '.join(WORDS[i][0].upper() for i in l) for l in iys]
    bigfirst = ib[0] < min(smallk)
    B, s_ = 150, 58
    while True:
        fb, fs = mont(B, 900), mont(s_, 900)
        wb = sum(fb.getlength(ch) - 6 for ch in big) + 20; wsm = max(sum(fs.getlength(ch) - 3 for ch in x) + 20 for x in small)
        if wb + 16 + wsm <= 700: break
        B = int(B * 0.96); s_ = int(s_ * 0.96)
    LH, G = 72, 28
    Htot = len(pre) * LH + B + len(post) * LH + G * (bool(pre) + bool(post)); top = CY - Htot / 2
    cy = top + len(pre) * LH + G * bool(pre) + B / 2
    x0 = 540 - (wb + 16 + wsm) / 2
    xb, xs = (x0, x0 + wb + 16) if bigfirst else (x0 + wsm + 16, x0)
    if t >= T(ib[0]): put(c, gtext_a(big, fb, CREAM, typed(big, t, T(ib[0]), 8, 0.2), -6), xb, cy, 'l')
    lh = s_ * 0.95
    for k, (l, x) in enumerate(zip(iys, small)):
        if t >= T(l[0]):
            L = gtext_a(x, fs, YEL, typed(x, t, T(l[0]), 24, 0.15), -3)
            put(c, L, xs if bigfirst else xs + wsm - L.width, cy - (len(small) - 1) * lh / 2 + k * lh, 'l')
    for k, l in enumerate(pre): sline(c, t, l, top + LH / 2 + k * LH)
    for k, l in enumerate(post): sline(c, t, l, cy + B / 2 + G + LH / 2 + k * LH)
def paper(c, t, st, t0, cy=CY):
    """torn white paper strip sliding open, the words in dark ink appear with the voice"""
    lines = wrap(range(st[0], st[1] + 1), 19)
    fs = eg.fit([' '.join(s for s, _, _ in l) for l in lines], 52, 800, 0, 660); f = mont(fs, 800); lh = int(fs * 1.3)
    w_ = int(max(f.getlength(' '.join(s for s, _, _ in l)) for l in lines) + 64); h_ = 28 + lh * len(lines)
    P_ = Image.new('RGBA', (w_, h_), (0, 0, 0, 0)); rng = np.random.default_rng(st[0])
    top = [(x, rng.uniform(0, 7)) for x in range(0, w_ + 1, 10)]; bot = [(x, h_ - rng.uniform(0, 7)) for x in range(w_, -1, -10)]
    d = ImageDraw.Draw(P_); d.polygon(top + bot, fill=(232, 230, 224, 255))
    for i, l in enumerate(lines):
        tot = f.getlength(' '.join(s for s, _, _ in l)); x = (w_ - tot) / 2
        for s_, wa, w in l:
            al = clamp((t - wa + 0.04) / 0.2)
            if al > 0: d.text((x, 14 + i * lh), s_, font=f, fill=((150, 40, 30) if KEY.match(bare(w)) else INK) + (int(255 * al),))
            x += f.getlength(s_ + ' ')
    gm = grunge(9).crop((0, 0, w_, h_)); P_.putalpha(ImageChops.multiply(P_.getchannel('A'), gm))
    k = eg.eout((t - t0) / 0.45); m = np.clip((k * (w_ + 60) - np.arange(w_)) / 60, 0, 1)
    P_.putalpha(Image.fromarray((np.asarray(P_.getchannel('A'), np.float32) * m[None, :]).astype(np.uint8)))
    put(c, P_, 540, cy)
def subs(c, t):
    k = max([i for i, a in enumerate(VS) if a <= t] or [-1])
    if k < 0: return
    pg = PG[k]
    if pg[0] == 'EM': emph(c, t, pg[1])
    elif pg[0] == 'ST': paper(c, t, pg[1], VS[k])
    else:
        n = len(pg[1])
        for i, l in enumerate(pg[1]): sline(c, t, l, CY - (n - 1) * 37 + i * 74)

# pictures and camera from pr.py, without its titles/quotes; subtitles drawn on the screen on top
def _noop(*a, **k): return None
def silent(fn):
    def g(*a):
        q, ti = pr.quote, pr.title; pr.quote = pr.title = _noop
        try: fn(*a)
        finally: pr.quote, pr.title = q, ti
    return g
pr.SCN = [(a, silent(f)) for a, f in pr.SCN]
_tf = pr.table_frame
def table_frame(t):
    can = _tf(t).convert('RGBA'); subs(can, t); return can
pr.table_frame = table_frame

if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        ts = [float(x) for x in sys.argv[3:]]; n = len(ts); P_ = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = pr.frame(t).convert('RGBA'); d = ImageDraw.Draw(f)
            d.rectangle((930, 680, W, 1580), outline=(0, 255, 255, 255), width=4); d.text((10, 300), '%.2f' % t, fill=(255, 0, 255, 255))
            P_.paste(f.convert('RGB').resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P_.save(E + sys.argv[2], quality=85); sys.exit()
    a, b = float(sys.argv[2]), float(sys.argv[3])
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '10M', '-preset', 'medium', E + sys.argv[1]], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        p.stdin.write(np.asarray(pr.frame(n / FPS).convert('RGB')).tobytes())
        if n % 30 == 0: print('t', n / FPS, flush=True)
    p.stdin.close(); p.wait(); print('rc', p.returncode)
