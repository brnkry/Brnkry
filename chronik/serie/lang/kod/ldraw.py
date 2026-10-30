# new ink drawings, charts and flags for the long version (page coordinates); moving ones take the running phase ph
import math
import numpy as np
from PIL import Image, ImageDraw
from lcore import poly, arc, hatch, ink, eout, eio, clamp, lerp, fade_col, serif, sans, italic, TXT, GREY, ACC, PAPER, stamp_ink
from drawings import drawing, T_, wave_flag, paint_weimar, paint_uk, paint_fr
def closed(pts): return poly(pts + [pts[0]])

# ---------- moving drawings: make(ph) -> (lines, shade, [(paths, alpha)]) ----------
def factory_m(cx, cy, s, ph):
    """Ruhr works: saw-tooth roofs, two chimneys, smoke rolling out and drifting"""
    P = lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
    lines = [closed(P([(-330, 0), (330, 0), (330, 160), (-330, 160)]))]
    for i in range(5):
        x = -330 + i * 132; lines.append(poly(P([(x, 0), (x + 40, -70), (x + 132, 0)]))); lines.append(poly(P([(x + 40, -70), (x + 40, 0)])))
    for x in (-250, -150, -50, 50, 150, 250): lines.append(closed(P([(x - 22, 50), (x + 22, 50), (x + 22, 110), (x - 22, 110)])))
    for cxh, top in ((-210, -330), (130, -290)): lines.append(closed(P([(cxh - 26, 0), (cxh - 18, top), (cxh + 18, top), (cxh + 26, 0)])))
    shade = hatch(P([(-330, 120), (330, 120), (330, 160), (-330, 160)]), 9, 60) + hatch(P([(-236, 0), (-228, -330), (-192, -330), (-184, 0)]), 8, 60)
    smoke = []
    for cxh, top in ((-210, -330), (130, -290)):
        for k in range(5):
            u = ((ph * 0.35) + k / 5) % 1.0; r_ = (16 + 46 * u) * s
            smoke.append(arc(cx + (cxh + 160 * u) * s, cy + (top - 30 - 190 * u) * s, r_, n=18))
    return lines, shade, [(smoke, 0.45)]
def coins_m(cx, cy, s, ph, n_max=9):
    """a stack of gold marks growing coin by coin: each coin a rim seen from the side, the top one as a full disc with its edge"""
    n = min(n_max, int(ph / 0.22) + 1); lines = []; rx, ry, th = 120 * s, 36 * s, 24 * s
    def coin(y, top):
        lines.append(poly([(cx - rx, y), (cx - rx, y + th)])); lines.append(poly([(cx + rx, y), (cx + rx, y + th)]))
        lines.append(arc(cx, y + th, rx, 0, 180, 50)[::-1] if False else [(cx + rx * math.cos(math.radians(a)), y + th + ry * math.sin(math.radians(a))) for a in range(0, 181, 6)])
        if top: lines.append([(cx + rx * math.cos(math.radians(a)), y + ry * math.sin(math.radians(a))) for a in range(0, 361, 6)]); lines.append([(cx + rx * 0.7 * math.cos(math.radians(a)), y + ry * 0.7 * math.sin(math.radians(a))) for a in range(0, 361, 8)])
    for i in range(n): coin(cy - i * th, i == n - 1)
    if n < n_max:   # the next coin falling
        u = (ph % 0.22) / 0.22; y = cy - n * th - (1 - u) * 220 * s; coin(y, True)
    return lines, [], []
def notes_m(x0, y0, w, h, ph, n=14, seed=3):
    """banknotes fluttering down"""
    r = np.random.default_rng(seed); out = []
    for i in range(n):
        sp = r.uniform(0.18, 0.32); u = ((ph * sp) + r.random()) % 1.0; x = x0 + r.random() * w + 40 * math.sin(ph * 2 + i); y = y0 + u * h
        a = math.radians(30 * math.sin(ph * 2.5 + i * 1.3)); cw, ch = 90, 46
        pts = [(x + dx * math.cos(a) - dy * math.sin(a), y + dx * math.sin(a) * 0.6 + dy * math.cos(a)) for dx, dy in ((-cw, -ch), (cw, -ch), (cw, ch), (-cw, ch))]
        out.append(closed(pts)); out.append(poly([((pts[0][0] + pts[2][0]) / 2 - 20, (pts[0][1] + pts[2][1]) / 2), ((pts[0][0] + pts[2][0]) / 2 + 20, (pts[0][1] + pts[2][1]) / 2)]))
    return out
def tower_m(cx, base_y, s, ph):
    """the wooden radio tower of Gleiwitz: a tall tapering lattice, radio waves pulsing from the top"""
    H_ = 900 * s; top = base_y - H_; lines = []
    L = lambda y: (lerp(150, 14, (base_y - y) / H_) * s)
    lines.append(poly([(cx - 150 * s, base_y), (cx - 14 * s, top)])); lines.append(poly([(cx + 150 * s, base_y), (cx + 14 * s, top)]))
    ys = np.linspace(base_y, top, 14)
    for a, b in zip(ys, ys[1:]):
        lines.append(poly([(cx - L(a), a), (cx + L(b), b)])); lines.append(poly([(cx + L(a), a), (cx - L(b), b)])); lines.append(poly([(cx - L(b), b), (cx + L(b), b)]))
    lines.append(poly([(cx, top), (cx, top - 60 * s)]))
    waves = []
    for k in range(3):
        u = ((ph * 0.7) + k / 3) % 1.0; r_ = (40 + 260 * u) * s
        waves.append(arc(cx, top - 60 * s, r_, -150, -30, 40))
    ground = [poly([(cx - 420 * s, base_y), (cx + 420 * s, base_y)])]
    return lines, [], [(waves, 0.55), (ground, 0.7)]
def paper_m(cx, cy, s, ph):
    """a sheet of paper held up and fluttering (Chamberlain's agreement)"""
    w, h = 220 * s, 300 * s; pts = []
    for i in range(21):
        x = cx - w / 2 + w * i / 20; dy = 10 * s * math.sin(ph * 4 + i * 0.5) * (i / 20)
        pts.append((x, cy - h / 2 + dy))
    right = [(cx + w / 2, cy - h / 2 + 10 * s * math.sin(ph * 4 + 10)), (cx + w / 2 + 6 * s * math.sin(ph * 3), cy + h / 2)]
    bottom = [(cx - w / 2 + w * i / 20, cy + h / 2 + 8 * s * math.sin(ph * 4 + i * 0.5) * (i / 20)) for i in range(20, -1, -1)]
    outline = poly(pts + right + bottom + [pts[0]], 6)
    txt = [poly([(cx - w / 2 + 30 * s, cy - h / 2 + (60 + 28 * j) * s), (cx + w / 2 - 40 * s, cy - h / 2 + (60 + 28 * j) * s + 6 * s * math.sin(ph * 4 + 6))]) for j in range(6)]
    sig = [poly([(cx - 40 * s, cy + 100 * s), (cx - 10 * s, cy + 85 * s), (cx + 20 * s, cy + 105 * s), (cx + 60 * s, cy + 90 * s)])]
    return [outline], [], [(txt, 0.5), (sig, 0.8)]
def helmet(cx, cy, s):
    """German steel helmet, model 1916, side view facing right: dome, short visor, deep flared neck guard, side lug"""
    P = lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
    shell = P([(250, 30), (215, 2), (205, -80), (160, -160), (60, -205), (-60, -205), (-160, -160), (-215, -80), (-232, 0), (-265, 85), (-305, 140), (-255, 152), (-205, 98), (-180, 40), (190, 40), (250, 30)])
    lines = [poly(shell), poly(P([(-180, 40), (-150, 18), (170, 18), (215, 2)])), arc(cx + 40 * s, cy - 92 * s, 20 * s), arc(cx + 40 * s, cy - 92 * s, 9 * s)]
    shade = hatch(P([(-160, -160), (-215, -80), (-232, 0), (-265, 85), (-305, 140), (-255, 152), (-205, 98), (-180, 40), (-120, 18), (-100, -120)]), 10, 60)
    return lines, shade
def book(cx, cy, s):
    P = lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
    lines = [closed(P([(-160, -220), (160, -220), (160, 220), (-160, 220)])), closed(P([(160, -220), (190, -200), (190, 240), (-130, 240), (-160, 220)])), poly(P([(160, 220), (190, 240)]))]
    for j in range(8): lines.append(poly(P([(165 + j * 3, -205 + j * 3), (165 + j * 3, 225 + j * 1.5)])))
    shade = hatch(P([(160, -220), (190, -200), (190, 240), (160, 220)]), 7, 80)
    return lines, shade
def prison(cx, cy, s):
    """a barred prison window"""
    P = lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
    lines = [closed(P([(-180, -200), (180, -200), (180, 200), (-180, 200)])), closed(P([(-210, -230), (210, -230), (210, 230), (-210, 230)]))]
    for x in (-108, -36, 36, 108): lines.append(poly(P([(x, -200), (x, 200)])))
    lines.append(poly(P([(-180, 0), (180, 0)])))
    return lines, hatch(P([(-210, -230), (210, -230), (180, -200), (-180, -200)]), 8, 30)
def table(cx, cy, s, empty_flag=None):
    """the conference table in Munich seen from above at an angle: four chairs taken, one standing apart and empty"""
    P = lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
    lines = [closed(P([(-420, -90), (420, -90), (470, 90), (-470, 90)])), poly(P([(-470, 90), (-470, 110), (470, 110), (470, 90)]))]
    chairs = [(-300, -140), (-100, -140), (100, -140), (300, -140)]
    for x, y in chairs:
        lines.append(closed(P([(x - 60, y - 40), (x + 60, y - 40), (x + 50, y + 20), (x - 50, y + 20)]))); lines.append(closed(P([(x - 60, y - 40), (x + 60, y - 40), (x + 60, y - 110), (x - 60, y - 110)])))
    ex, ey = 0, 250   # the empty chair, away from the table
    lines.append(closed(P([(ex - 60, ey - 40), (ex + 60, ey - 40), (ex + 50, ey + 20), (ex - 50, ey + 20)]))); lines.append(closed(P([(ex - 60, ey + 20), (ex + 60, ey + 20), (ex + 60, ey + 90), (ex - 60, ey + 90)])))
    shade = hatch(P([(-470, 90), (470, 90), (470, 110), (-470, 110)]), 7, 60)
    return lines, shade
def ship_m(cx, cy, s, ph):
    """the old battleship Schleswig-Holstein, side view, guns firing: muzzle flash and smoke"""
    P = lambda pts, yy=0: [(cx + x * s, cy + (y + yy) * s) for x, y in pts]
    b = 3 * math.sin(ph * 1.7)
    hull = P([(-430, 0), (420, 0), (460, -40), (-440, -40), (-430, 0)], b)
    sup = [closed(P([(-160, -40), (120, -40), (120, -90), (-160, -90)], b)), closed(P([(-90, -90), (40, -90), (40, -150), (-90, -150)], b)),
           poly(P([(-20, -150), (-20, -300)], b)), poly(P([(-60, -250), (20, -250)], b)), poly(P([(180, -40), (180, -200)], b)),
           closed(P([(-60, -150), (-20, -150), (-25, -200), (-55, -200)], b)), closed(P([(30, -90), (70, -90), (66, -170), (34, -170)], b))]
    tur = [closed(P([(200, -40), (290, -40), (280, -70), (210, -70)], b)), poly(P([(280, -60), (400, -66)], b)),
           closed(P([(-330, -40), (-240, -40), (-250, -70), (-320, -70)], b)), poly(P([(-330, -60), (-440, -66)], b))]
    lines = [poly(hull)] + sup + tur
    shade = hatch(P([(-430, 0), (420, 0), (460, -40), (-440, -40)], b), 9, 60)
    fire = []; u = (ph % 2.4) / 2.4
    if u < 0.5:   # flash and a smoke ball from the forward guns
        r_ = (20 + 140 * u) * s; fire.append(arc(cx + (420 + 80 * u) * s, cy + (-66 - 30 * u + b) * s, r_, n=24))
        fire.append(arc(cx + (420 + 30 * u) * s, cy + (-66 + b) * s, (30 + 40 * u) * s, n=16))
    waves = [[(cx + x * s, cy + (12 + 5 * math.sin(x / 40 - ph * 3)) * s) for x in range(-520, 540, 10)]]
    return lines, shade, [(fire, 0.55), (waves, 0.6)]
def stock(pg, t, t0, dur, box, pts_u, crash_at=0.62, wd=6):
    """a price line drawn on: black while it climbs, red from the crash"""
    if t < t0: return
    x0, y0, w, h = box; P = [(x0 + u * w, y0 + h - v * h) for u, v in pts_u]; n = len(P) - 1
    m = clamp((t - t0) / dur) * n; d = ImageDraw.Draw(pg)
    for i in range(int(min(n, math.ceil(m)))):
        a, b = P[i], P[i + 1]; u = min(1, m - i); e = (lerp(a[0], b[0], u), lerp(a[1], b[1], u))
        d.line((a, e), fill=ACC if i / n >= crash_at else TXT, width=wd)
def axes(pg, t, t0, box, col=(190, 190, 190)):
    if t < t0: return
    x0, y0, w, h = box; d = ImageDraw.Draw(pg); k = eout((t - t0) / 0.4)
    d.line((x0, y0 + h, x0 + w * k, y0 + h), fill=col, width=3); d.line((x0, y0 + h, x0, y0 + h - h * k), fill=col, width=3)
def barchart(pg, t, x0, base_y, bw, gap, hmax, vmax, data, fmt, size=40):
    """data: [(label, value, t_on, accent)]: bars grow from the base line, the value counts up with them"""
    d = ImageDraw.Draw(pg)
    for i, (lb, v, t1, acc) in enumerate(data):
        if t < t1: continue
        u = eout((t - t1) / 0.7); x = x0 + i * (bw + gap); hh = hmax * v / vmax * u
        d.rectangle((x, base_y - hh, x + bw, base_y), fill=ACC if acc else (52, 52, 58))
        d.text((x + bw / 2, base_y - hh - 18), fmt(v * u), font=sans(size, 700), fill=ACC if acc else TXT, anchor='md')
        d.text((x + bw / 2, base_y + 20), lb, font=sans(int(size * 0.8), 500), fill=GREY, anchor='ma')
def counter(pg, t, t0, dur, v1, xy, font, col=ACC, anchor='la', fmt=None, expo=True, suffix=''):
    """a number counting up (exponentially for inflation), set in German style with dots"""
    if t < t0: return
    u = eio((t - t0) / dur); v = math.exp(lerp(0, math.log(v1), u)) if expo else v1 * u
    s = fmt(v) if fmt else '{:,.0f}'.format(v).replace(',', '.')
    ImageDraw.Draw(pg).text(xy, s + suffix, font=font, fill=fade_col(col, eout((t - t0) / 0.3)), anchor=anchor)

# ---------- more flags (cloth, for wave_flag) ----------
def paint_be(F):
    w, h = F.size; d = ImageDraw.Draw(F)
    for i, c in enumerate(((20, 20, 20), (253, 218, 36), (239, 51, 64))): d.rectangle((i * w / 3, 0, (i + 1) * w / 3, h), fill=c)
def paint_it(F):
    w, h = F.size; d = ImageDraw.Draw(F)
    for i, c in enumerate(((0, 140, 69), (244, 245, 240), (205, 33, 42))): d.rectangle((i * w / 3, 0, (i + 1) * w / 3, h), fill=c)
def paint_pl(F):
    w, h = F.size; d = ImageDraw.Draw(F); d.rectangle((0, 0, w, h / 2), fill=(246, 246, 246)); d.rectangle((0, h / 2, w, h), fill=(220, 20, 60))
def paint_at(F):
    w, h = F.size; d = ImageDraw.Draw(F); d.rectangle((0, 0, w, h), fill=(200, 16, 46)); d.rectangle((0, h / 3, w, 2 * h / 3), fill=(246, 246, 246))
def paint_cs(F):
    w, h = F.size; d = ImageDraw.Draw(F); d.rectangle((0, 0, w, h / 2), fill=(246, 246, 246)); d.rectangle((0, h / 2, w, h), fill=(215, 20, 26))
    d.polygon([(0, 0), (w / 2, h / 2), (0, h)], fill=(17, 69, 126))
def paint_ussr(F):
    w, h = F.size; d = ImageDraw.Draw(F); d.rectangle((0, 0, w, h), fill=(204, 0, 0)); y = (255, 216, 0); u = h / 10
    cx, cy = w * 0.16, h * 0.18; pts = []
    for i in range(10):
        r = u * 0.55 if i % 2 == 0 else u * 0.22; a = -math.pi / 2 + i * math.pi / 5; pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, outline=y, width=max(1, int(u * 0.12)))
    hx, hy = w * 0.16, h * 0.42
    d.arc((hx - u * 1.1, hy - u * 1.1, hx + u * 1.1, hy + u * 1.1), 200, 40, fill=y, width=max(2, int(u * 0.35)))
    d.line((hx - u * 0.8, hy + u * 0.8, hx + u * 0.6, hy - u * 0.6), fill=y, width=max(2, int(u * 0.35))); d.line((hx + u * 0.3, hy - u * 0.9, hx + u * 0.9, hy - u * 0.3), fill=y, width=max(2, int(u * 0.45)))
FLAGS = {'de': paint_weimar, 'uk': paint_uk, 'fr': paint_fr, 'be': paint_be, 'it': paint_it, 'pl': paint_pl, 'at': paint_at, 'cs': paint_cs, 'su': paint_ussr}
def flag(pg, t, t0, code, x, y, w=180, h=110, name=None, sub=None, pole=True, size=34):
    wave_flag(pg, t, t0, int(x), int(y), w, h, FLAGS[code], pole)
    if name and t >= t0:
        k = eout((t - t0) / 0.3); d = ImageDraw.Draw(pg)
        d.text((x + w + 30, y + h / 2 - (14 if sub else 0)), name, font=sans(size, 700), fill=fade_col(TXT, k), anchor='lm')
        if sub: d.text((x + w + 30, y + h / 2 + 26), sub, font=italic(int(size * 0.8)), fill=fade_col(GREY, k), anchor='lm')
