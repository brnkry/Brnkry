# ink drawings shared by the series (from Teil 1): static and moving (tank, biplane, U-boat, monoplane, bread), waving flags
import math
import numpy as np
from PIL import Image, ImageDraw
from magazine import eout, lerp, clamp, poly, arc, hatch, ink
def fade_col(c, k, bg=249): return tuple(int(lerp(bg, v, k)) for v in c)
# ---------- ink illustrations ----------
def T_(cx, cy, s, pts): return [(cx + x * s, cy + y * s) for x, y in pts]
def biplane(cx, cy, s=1.0):
    """a First World War biplane, side view"""
    P = lambda pts: poly(T_(cx, cy, s, pts), 6)
    fus = P([(-190, -10), (-150, -30), (150, -18), (230, -6), (230, 6), (150, 14), (-150, 30), (-190, 12), (-190, -10)])
    wings = [P([(-120, -95), (120, -95), (125, -84), (-118, -84), (-120, -95)]), P([(-110, 32), (110, 32), (115, 42), (-108, 42), (-110, 32)])]
    struts = [P([(-80, -84), (-70, 32)]), P([(80, -84), (75, 32)]), P([(-20, -84), (-30, -28)]), P([(20, -84), (10, -28)])]
    tail = [P([(170, -14), (215, -60), (235, -60), (230, -6)]), P([(175, 8), (250, 10), (255, 18), (180, 16)])]
    gear = [P([(-100, 30), (-115, 85)]), P([(-60, 30), (-110, 85)])] + [arc(cx - 112 * s, cy + 95 * s, 18 * s)]
    prop = [P([(-196, -60), (-190, 0), (-196, 60)])]; cock = [arc(cx - 40 * s, cy - 26 * s, 18 * s, 180, 360)]
    shade = hatch(T_(cx, cy, s, [(-150, 5), (150, 0), (150, 14), (-150, 30)]), 7, 60) + hatch(T_(cx, cy, s, [(-110, 36), (110, 36), (115, 42), (-108, 42)]), 6, 60)
    return [fus] + wings + struts + tail + gear + prop + cock, shade
def uboat(cx, cy, s=1.0):
    """a U-boat, side view, on the waterline"""
    P = lambda pts: poly(T_(cx, cy, s, pts), 6)
    hull = P([(-320, 0), (-260, -24), (260, -24), (330, -6), (300, 18), (-280, 22), (-320, 0)])
    tower = P([(-40, -24), (-30, -78), (60, -78), (75, -24)]); peri = [P([(20, -78), (20, -120), (32, -120)])]
    gun = [P([(-110, -24), (-110, -40), (-60, -46)]), P([(-120, -40), (-95, -40)])]
    rail = [P([(-250, -30), (240, -30)])]; water = [P([(-360, 6), (360, 6)]), P([(-330, 14), (-250, 14)]), P([(220, 14), (330, 14)])]
    shade = hatch(T_(cx, cy, s, [(-300, 2), (310, 2), (300, 18), (-280, 22)]), 7, 60) + hatch(T_(cx, cy, s, [(-30, -70), (60, -70), (70, -26), (-38, -26)]), 7, 60)
    return [hull, tower] + peri + gun + rail + water, shade
def loaf(cx, cy, s=1.0):
    P = lambda pts: poly(T_(cx, cy, s, pts), 5)
    out = [arc(cx, cy, 1, 0, 0)]
    oval = [(cx + 170 * s * math.cos(a), cy + 80 * s * math.sin(a) - 10 * s * max(0, -math.sin(a))) for a in np.linspace(0, 2 * math.pi, 60)]
    cuts = [P([(x - 30, -55), (x + 30, -20)]) for x in (-90, -30, 30, 90)]
    base = P([(-160, 40), (160, 40)])
    shade = hatch(T_(cx, cy, s, [(-150, 20), (150, 20), (120, 70), (-120, 70)]), 7, 60)
    return [oval] + cuts + [base], shade
def banknote(cx, cy, w=760, h=380):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    L = [poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], 10), poly([(x0 + 22, y0 + 22), (x1 - 22, y0 + 22), (x1 - 22, y1 - 22), (x0 + 22, y1 - 22), (x0 + 22, y0 + 22)], 10)]
    for px, py in ((x0 + 90, y0 + 90), (x1 - 90, y0 + 90), (x0 + 90, y1 - 90), (x1 - 90, y1 - 90)): L += [arc(px, py, 46), arc(px, py, 30)]
    L += [poly([(x0 + 160, cy + 70), (x1 - 160, cy + 70)], 10)]
    shade = hatch([(x0 + 22, y0 + 22), (x1 - 22, y0 + 22), (x1 - 22, y1 - 22), (x0 + 22, y1 - 22)], 16, 35)
    return L, shade[::3]
def monoplane(cx, cy, s=1.0):
    """a 1930s monoplane fighter, side view"""
    P = lambda pts: poly(T_(cx, cy, s, pts), 6)
    fus = P([(-250, 0), (-225, -26), (-60, -34), (40, -46), (100, -30), (250, -16), (275, -10), (275, 4), (120, 18), (-150, 26), (-245, 14), (-250, 0)])
    can = P([(10, -40), (40, -64), (95, -60), (105, -32)]); wing = P([(-120, 14), (80, 10), (95, 22), (-115, 30), (-120, 14)])
    tail = [P([(200, -18), (240, -78), (268, -78), (275, -10)]), P([(215, 0), (300, 2), (305, 10), (220, 10)])]
    gear = [P([(-60, 26), (-75, 80)]), arc(cx - 77 * s, cy + 92 * s, 15 * s)]; prop = [P([(-256, -70), (-250, 0), (-256, 70)])]
    shade = hatch(T_(cx, cy, s, [(-245, 6), (275, 0), (275, 4), (120, 18), (-150, 26)]), 7, 60)
    return [fus, can, wing] + tail + gear + prop, shade
def union_jack(pg, x, y, w, h, k):
    im = Image.new('RGB', (w, h), (1, 33, 105)); d = ImageDraw.Draw(im)
    for a, b in (((0, 0), (w, h)), ((w, 0), (0, h))): d.line((a, b), fill=(255, 255, 255), width=int(h * 0.2))
    for a, b in (((0, 0), (w, h)), ((w, 0), (0, h))): d.line((a, b), fill=(200, 16, 46), width=int(h * 0.07))
    d.rectangle((w / 2 - h * 0.17, 0, w / 2 + h * 0.17, h), fill=(255, 255, 255)); d.rectangle((0, h / 2 - h * 0.17, w, h / 2 + h * 0.17), fill=(255, 255, 255))
    d.rectangle((w / 2 - h * 0.1, 0, w / 2 + h * 0.1, h), fill=(200, 16, 46)); d.rectangle((0, h / 2 - h * 0.1, w, h / 2 + h * 0.1), fill=(200, 16, 46))
    pg.paste(Image.blend(Image.new('RGB', (w, h), (249, 248, 245)), im, k), (int(x), int(y)))
def tricolore(pg, x, y, w, h, k):
    d = ImageDraw.Draw(pg)
    for i, c in enumerate(((0, 85, 164), (255, 255, 255), (239, 65, 53))): d.rectangle((x + i * w / 3, y, x + (i + 1) * w / 3, y + h), fill=fade_col(c, k))
    d.rectangle((x, y, x + w, y + h), outline=fade_col((200, 200, 200), k), width=2)
def weimar(pg, x, y, w, h, k):
    d = ImageDraw.Draw(pg)
    for i, c in enumerate(((22, 22, 22), (205, 24, 24), (250, 196, 0))): d.rectangle((x, y + i * h / 3, x + w, y + (i + 1) * h / 3), fill=fade_col(c, k))


# ---------- moving drawings: once drawn, they keep running in place ----------
def drawing(pg, t, t0, dur, make, wd=3):
    """make(ph) -> (lines, shade, motion): the drawing is inked in over dur, its shading after it, then the motion marks
    (dust, speed lines, waves, steam) fade in; everything is rebuilt each frame from the running phase ph = t - t0"""
    if t < t0: return
    lines, shade, motion = make(t - t0)
    ink(pg, t, t0, dur, lines, wd=wd); ink(pg, t, t0 + dur, dur * 0.4, shade, wd=2, a=0.6)
    if t > t0 + dur and motion:
        k = eout((t - t0 - dur) / 0.4)
        for paths, a in motion: ink(pg, t, -1, 0.001, paths, wd=2, a=a * k)
def _rot(cx, cy, r, a): return (cx + r * math.cos(a), cy + r * math.sin(a))
def tank_m(cx, cy, s, ph):
    """the tank drives on the spot: body rocks, road wheels turn, track links run, the ground and dust slide away behind"""
    bob = 2.2 * math.sin(ph * 15); cyb = cy + bob
    P = lambda pts, yy=cyb: [(cx + x * s, yy + y * s) for x, y in pts]
    hull = P([(-330, -10), (-300, -95), (250, -95), (330, -30), (330, 25), (-330, 25)])
    tur = P([(-150, -110), (-120, -205), (120, -205), (165, -110)])
    lines = [poly(hull + [hull[0]]), poly(P([(-300, -95), (-270, -110), (210, -110), (250, -95)])), poly(tur + [tur[0]]),
             poly(P([(-80, -205), (-70, -240), (10, -240), (20, -205)]) + [P([(-80, -205)])[0]]), poly(P([(150, -170), (470, -168), (470, -150), (150, -146), (150, -170)])),
             poly(P([(140, -185), (178, -185), (178, -132), (140, -132), (140, -185)])), poly(P([(-360, 20), (330, 20), (380, 70), (330, 150), (-330, 150), (-385, 75), (-360, 20)], cy))]
    rot = ph * 7.0
    for wx in np.linspace(-270, 230, 7):
        c = (cx + wx * s, cy + 105 * s); r = 34 * s; lines.append(arc(c[0], c[1], r))
        for k in range(3): lines.append(poly([c, _rot(c[0], c[1], r * 0.8, rot + k * 2.094)], 4))
    for c_, r_ in (((cx + 330 * s, cy + 72 * s), 40 * s), ((cx - 335 * s, cy + 75 * s), 40 * s)):
        lines.append(arc(c_[0], c_[1], r_))
        for k in range(4): lines.append(poly([c_, _rot(c_[0], c_[1], r_ * 0.85, rot + k * 1.571)], 4))
    sp = 28; off = (ph * 160) % sp
    for k in range(-1, 26):   # links on the bottom run move back with the ground, those on top run forward
        xb = -330 + k * sp - off; xt = -320 + k * sp + off
        if -335 < xb < 330: lines.append(poly(P([(xb, 146), (xb + 6, 156)], cy)))
        if -350 < xt < 320: lines.append(poly(P([(xt, 18), (xt + 6, 28)], cy)))
    for k in range(9): lines.append(arc(cx + lerp(-260, 220, k / 8) * s, cyb - 70 * s, 4 * s, n=6))
    shade = hatch(P([(-330, -10), (330, -30), (330, 25), (-330, 25)]), 10, 60) + hatch(P([(-330, 120), (330, 120), (330, 150), (-330, 150)], cy), 8, 60)
    gy = cy + 162 * s; ground = [poly([(cx - 480 * s, gy), (cx + 480 * s, gy)], 10)]
    goff = (ph * 160 * s) % (90 * s)
    for k in range(13):
        x0 = cx - 520 * s + k * 90 * s - goff
        if cx - 480 * s < x0 < cx + 460 * s: ground.append(poly([(x0, gy + 14 * s), (x0 + 30 * s, gy + 14 * s)], 6))
    dust = []
    for k in range(4):
        u = ((ph * 0.9) + k / 4) % 1.0; r_ = (10 + 26 * u) * s
        dust.append(arc(cx - (400 + 160 * u) * s, gy - (16 + 40 * u) * s, r_, n=14))
    return lines, shade, [(ground, 0.8), (dust, 0.35)]
def speedlines(cx, cy, s, ph, x0, ys, length=120, span=260):
    out = []
    for i, y in enumerate(ys):
        u = ((ph * 1.6) + i * 0.37) % 1.0; xa = cx + (x0 + 40 + span * u) * s
        out.append(poly([(xa, cy + y * s), (xa + length * s * (1 - u), cy + y * s)], 6))
    return out
def biplane_m(cx, cy, s, ph):
    """flying on the spot: a gentle rise and fall, the propeller turning, air streaming past the tail"""
    cy = cy + 6 * math.sin(ph * 2.2) * s
    lines, shade = biplane(cx, cy, s); lines = lines[:-2] + [lines[-1]]   # without the static propeller
    c = abs(math.cos(ph * 38)); lines.append(poly([(cx - 196 * s, cy - 60 * s * c), (cx - 196 * s, cy + 60 * s * c)], 4))
    disc = [poly([(cx - 199 * s, cy - 62 * s), (cx - 193 * s, cy - 62 * s)], 4), poly([(cx - 199 * s, cy + 62 * s), (cx - 193 * s, cy + 62 * s)], 4)]
    return lines, shade, [(speedlines(cx, cy, s, ph, 240, (-80, -20, 30, 60)), 0.45), (disc, 0.4)]
def uboat_m(cx, cy, s, ph):
    """riding the swell: the boat rises and falls, the sea runs past"""
    b = 5 * math.sin(ph * 2.0) * s
    lines, shade = uboat(cx, cy + b, s); lines = lines[:-3]
    waves = []
    for row, (yy, amp, sp) in enumerate(((10, 6, 1.0), (24, 4, 0.7))):
        pts = [(cx + x * s, cy + (yy + amp * math.sin(x / 30 - ph * 4 * sp)) * s) for x in range(-380, 381, 8)]
        waves.append(pts)
    bow = [poly([(cx + 330 * s, cy + (2 + b / s) * s), (cx + 370 * s, cy - 6 * s + 4 * math.sin(ph * 6) * s)], 4)]
    return lines, shade, [(waves, 0.7), (bow, 0.5)]
def monoplane_m(cx, cy, s, ph):
    cy = cy + 6 * math.sin(ph * 2.0) * s
    lines, shade = monoplane(cx, cy, s); lines = lines[:-1]
    c = abs(math.cos(ph * 40)); lines.append(poly([(cx - 256 * s, cy - 70 * s * c), (cx - 256 * s, cy + 70 * s * c)], 4))
    return lines, shade, [(speedlines(cx, cy, s, ph, 290, (-60, -10, 20, 50), 80, 120), 0.45)]
def loaf_m(cx, cy, s, ph):
    lines, shade = loaf(cx, cy, s); steam = []
    for k in range(3):
        u = ((ph * 0.5) + k / 3) % 1.0; x0 = cx + (-70 + k * 70) * s; ya = cy - (90 + 120 * u) * s
        steam.append([(x0 + 12 * s * math.sin((y - ya) / (18 * s) + ph * 3 + k), y) for y in np.linspace(ya, ya - 70 * s, 14)])
    return lines, shade, [(steam, 0.35)]
def wave_flag(pg, t, t0, x, y, w, h, paint, pole=True):
    """a cloth flag on a pole, waving: columns shifted by a travelling sine, light and shade on the folds"""
    if t < t0: return
    k = eout((t - t0) / 0.3); ph = t - t0
    F = Image.new('RGB', (w, h)); paint(F); a = np.asarray(F, np.float32); A_ = h * 0.09; out = np.full((h + int(2 * A_) + 4, w, 3), 249, np.float32)
    msk = np.zeros((h + int(2 * A_) + 4, w), np.float32)
    for xx in range(w):
        f = (xx / w) ** 0.8; ang = 2 * math.pi * xx / (w * 0.75) - ph * 5.5
        dy = int(round(A_ * f * math.sin(ang) + A_ + 2)); sh = 1 + 0.22 * f * math.cos(ang)
        out[dy:dy + h, xx] = a[:, xx] * sh; msk[dy:dy + h, xx] = 1
    out = out * k + 249 * (1 - k)
    reg = np.asarray(pg.crop((x, y - int(A_) - 2, x + w, y - int(A_) - 2 + out.shape[0])), np.float32); m = msk[..., None]
    pg.paste(Image.fromarray((reg * (1 - m) + out * m).clip(0, 255).astype(np.uint8)), (x, y - int(A_) - 2))
    if pole: ImageDraw.Draw(pg).line((x - 4, y - 30, x - 4, y + h + 70), fill=fade_col((60, 56, 50), k), width=7)
def paint_weimar(F):
    d = ImageDraw.Draw(F); w, h = F.size
    for i, c in enumerate(((22, 22, 22), (205, 24, 24), (250, 196, 0))): d.rectangle((0, i * h / 3, w, (i + 1) * h / 3), fill=c)
def paint_uk(F):
    w, h = F.size; d = ImageDraw.Draw(F); d.rectangle((0, 0, w, h), fill=(1, 33, 105))
    for a_, b_ in (((0, 0), (w, h)), ((w, 0), (0, h))): d.line((a_, b_), fill=(255, 255, 255), width=int(h * 0.2))
    for a_, b_ in (((0, 0), (w, h)), ((w, 0), (0, h))): d.line((a_, b_), fill=(200, 16, 46), width=int(h * 0.07))
    d.rectangle((w / 2 - h * 0.17, 0, w / 2 + h * 0.17, h), fill=(255, 255, 255)); d.rectangle((0, h / 2 - h * 0.17, w, h / 2 + h * 0.17), fill=(255, 255, 255))
    d.rectangle((w / 2 - h * 0.1, 0, w / 2 + h * 0.1, h), fill=(200, 16, 46)); d.rectangle((0, h / 2 - h * 0.1, w, h / 2 + h * 0.1), fill=(200, 16, 46))
def paint_fr(F):
    w, h = F.size; d = ImageDraw.Draw(F)
    for i, c in enumerate(((0, 85, 164), (255, 255, 255), (239, 65, 53))): d.rectangle((i * w / 3, 0, (i + 1) * w / 3, h), fill=c)

