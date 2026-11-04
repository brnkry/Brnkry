# moving pen drawings for Teil 2 (same pen as drawings.py): make(ph) -> (lines, shade, motion)
import math
from magazine import poly, arc, hatch
def _P(cx, cy, s): return lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
def closed(pts): return poly(pts + [pts[0]])
def _leg(P, hx, hy, a, l1=72, l2=70):
    kx, ky = hx + l1 * math.sin(a), hy + l1 * math.cos(a); b = a - 0.35 * abs(math.sin(a)) - 0.05
    fx, fy = kx + l2 * math.sin(b), ky + l2 * math.cos(b); return poly(P([(hx, hy), (kx, ky), (fx, fy), (fx + 18, fy)]))
def _ground(P, ph, speed, w=170):
    return [poly(P([(x, 0), (x + 20, 0)])) for x in [((k * 40 - ph * speed) % (2 * w)) - w for k in range(int(2 * w / 40))]]
def soldier_m(cx, gy, s, ph):
    """a soldier marching on the spot: legs and arms swing, the slung rifle bobs, the ground runs past"""
    P = _P(cx, gy, s); a = 0.42 * math.sin(ph * 5.2); bob = 3 * abs(math.sin(ph * 5.2))
    hip = (0, -142 - bob); sh = (0, -250 - bob)
    lines = [_leg(P, hip[0], hip[1], a), _leg(P, hip[0], hip[1], -a), poly(P([hip, sh]))]
    for k in (1, -1):   # arms
        aa = -k * a * 0.8; ex, ey = sh[0] + 52 * math.sin(aa), sh[1] + 52 * math.cos(aa); lines.append(poly(P([sh, (ex, ey), (ex + 46 * math.sin(aa * 1.2), ey + 46 * math.cos(aa * 1.2))])))
    lines.append(arc(cx, gy + (-282 - bob) * s, 24 * s, n=24))
    lines.append(poly(P([(-38, -290 - bob), (-30, -318 - bob), (0, -330 - bob), (30, -318 - bob), (38, -290 - bob), (44, -284 - bob)])))   # helmet
    lines.append(poly(P([(18, -262 - bob), (-42, -150 - bob)])))   # rifle on the back
    lines.append(closed(P([(-6, -246 - bob), (-40, -240 - bob), (-40, -180 - bob), (-6, -176 - bob)])))   # pack
    shade = hatch(P([(-40, -240 - bob), (-6, -246 - bob), (-6, -176 - bob), (-40, -180 - bob)]), 7, 60)
    return lines, shade, [(_ground(P, ph, 110), 0.6)]
def civilian_m(cx, gy, s, ph):
    """a refugee walking: coat, hat, a suitcase in one hand, slower steps"""
    P = _P(cx, gy, s); a = 0.32 * math.sin(ph * 3.6); bob = 2 * abs(math.sin(ph * 3.6))
    hip = (0, -138 - bob); sh = (0, -248 - bob)
    lines = [_leg(P, hip[0], hip[1], a), _leg(P, hip[0], hip[1], -a)]
    lines.append(closed(P([(-30, -250 - bob), (30, -250 - bob), (44, -110 - bob), (-44, -110 - bob)])))   # coat
    aa = a * 0.5; hx, hy = 34 + 10 * math.sin(aa), -150 - bob
    lines.append(poly(P([(28, -240 - bob), (36, -195 - bob), (hx, hy)])))
    lines.append(closed(P([(hx - 22, hy), (hx + 30, hy), (hx + 30, hy + 44), (hx - 22, hy + 44)])))   # suitcase
    lines.append(poly(P([(-28, -240 - bob), (-40, -190 - bob + 8 * math.sin(ph * 3.6)), (-44, -150 - bob)])))
    lines.append(arc(cx, gy + (-278 - bob) * s, 22 * s, n=24))
    lines.append(poly(P([(-36, -296 - bob), (36, -296 - bob)]))); lines.append(closed(P([(-20, -296 - bob), (20, -296 - bob), (16, -322 - bob), (-16, -322 - bob)])))
    shade = hatch(P([(-30, -250 - bob), (30, -250 - bob), (44, -110 - bob), (-44, -110 - bob)]), 9, 55)
    return lines, shade, [(_ground(P, ph, 60), 0.6)]
def truck_m(cx, gy, s, ph):
    """a lorry of the gold convoy driving on the spot: wheels turn, road runs past"""
    P = _P(cx, gy, s); b = 2 * math.sin(ph * 9)
    lines = [closed(P([(-200, -50 + b), (60, -50 + b), (60, -170 + b), (-200, -170 + b)])), closed(P([(60, -50 + b), (170, -50 + b), (170, -100 + b), (140, -140 + b), (60, -140 + b)])),
             closed(P([(80, -100 + b), (130, -100 + b), (120, -130 + b), (80, -130 + b)]))]
    for wx in (-140, 110):
        lines.append(arc(cx + wx * s, gy - 30 * s, 30 * s, n=28))
        for k in range(3):
            an = ph * 7 + k * 2.094; lines.append(poly(P([(wx, -30), (wx + 26 * math.cos(an), -30 + 26 * math.sin(an))])))
    shade = hatch(P([(-200, -170 + b), (60, -170 + b), (60, -50 + b), (-200, -50 + b)]), 10, 50)
    return lines, shade, [(_ground(P, ph, 160, 260), 0.6)]
def gold_m(cx, cy, s, ph):
    """a stack of gold bars; small glints flicker on them"""
    P = _P(cx, cy, s); lines = []
    for r, (n, y) in enumerate(((4, 0), (3, -46), (2, -92))):
        for i in range(n):
            x = (i - (n - 1) / 2) * 92; lines.append(closed(P([(x - 44, y), (x + 44, y), (x + 32, y - 40), (x - 32, y - 40)])))
    shade = hatch(P([(-228, 0), (228, 0), (60, -132), (-60, -132)]), 11, 60)
    gl = []
    for k, (gx, gy) in enumerate(((-120, -20), (40, -66), (-20, -112), (120, -20))):
        u = (ph * 0.9 + k * 0.27) % 1.0
        if u < 0.35: r = 10 + 20 * u; gl += [poly(P([(gx - r, gy), (gx + r, gy)])), poly(P([(gx, gy - r), (gx, gy + r)]))]
    return lines, shade, [(gl, 0.8)]
def radio_m(cx, cy, s, ph):
    """a radio set with its loudspeaker; sound waves go out from it"""
    P = _P(cx, cy, s)
    lines = [closed(P([(-90, 70), (90, 70), (90, -70), (-90, -70)])), arc(cx - 30 * s, cy, 42 * s, n=36), arc(cx - 30 * s, cy, 26 * s, n=28),
             arc(cx + 55 * s, cy - 30 * s, 10 * s, n=16), arc(cx + 55 * s, cy + 10 * s, 10 * s, n=16), poly(P([(-70, 70), (-70, 86)])), poly(P([(70, 70), (70, 86)]))]
    shade = hatch(P([(-90, 70), (90, 70), (90, 50), (-90, 50)]), 7, 60); waves = []
    for k in range(3):
        u = (ph * 0.8 + k / 3) % 1.0; r = (100 + 90 * u) * s
        waves.append([(cx + r * math.cos(a), cy + r * math.sin(a)) for a in [(-0.6 + 1.2 * i / 20) for i in range(21)]])
    return lines, shade, [(waves, 0.7)]
def train_m(cx, gy, s, ph):
    """a goods train rolling on the spot: wheels turn, smoke drifts back"""
    P = _P(cx, gy, s); lines = []
    for i in range(3):   # wagons
        x0 = -420 + i * 190; lines.append(closed(P([(x0, -40), (x0 + 170, -40), (x0 + 170, -170), (x0, -170)]))); lines.append(poly(P([(x0 + 60, -60), (x0 + 60, -150), (x0 + 110, -150), (x0 + 110, -60)])))
        for wx in (x0 + 35, x0 + 135):
            lines.append(arc(cx + wx * s, gy - 20 * s, 20 * s, n=20)); an = ph * 6; lines.append(poly(P([(wx, -20), (wx + 17 * math.cos(an), -20 + 17 * math.sin(an))])))
    x0 = 160; lines.append(closed(P([(x0, -40), (x0 + 220, -40), (x0 + 220, -120), (x0 + 150, -120), (x0 + 150, -190), (x0 + 60, -190), (x0 + 60, -120), (x0, -120)])))
    lines.append(closed(P([(x0 + 10, -120), (x0 + 40, -120), (x0 + 40, -170), (x0 + 10, -170)])))
    for wx in (x0 + 40, x0 + 110, x0 + 180):
        lines.append(arc(cx + wx * s, gy - 22 * s, 22 * s, n=20)); an = ph * 6 + wx; lines.append(poly(P([(wx, -22), (wx + 19 * math.cos(an), -22 + 19 * math.sin(an))])))
    lines.append(poly(P([(-440, 0), (420, 0)])))
    shade = hatch(P([(x0 + 150, -120), (x0 + 220, -120), (x0 + 220, -40), (x0 + 150, -40)]), 8, 60); smoke = []
    for k in range(4):
        u = (ph * 0.5 + k / 4) % 1.0; smoke.append(arc(cx + (x0 + 25 - 260 * u) * s, gy + (-190 - 60 * u) * s, (12 + 26 * u) * s, n=18))
    return lines, shade, [(smoke, 0.5)]
def enigma_m(cx, cy, s, ph):
    """the Enigma: a wooden box, three rotor windows turning, a lamp board where one lamp lights up after the other, a keyboard"""
    P = _P(cx, cy, s); lines = [closed(P([(-230, 150), (230, 150), (230, -150), (-230, -150)])), poly(P([(-230, -90), (230, -90)]))]
    for i in range(3):
        x = -60 + i * 60; lines.append(closed(P([(x - 18, -140), (x + 18, -140), (x + 18, -100), (x - 18, -100)])))
        off = ((ph * 2.2 + i * 0.7) % 1.0) * 30; lines.append(poly(P([(x - 12, -126 + off * 0.6), (x + 12, -126 + off * 0.6)])))
    lamps = []; hot = int(ph * 2.5) % 26
    for r, n in enumerate((9, 8, 9)):
        for i in range(n):
            x = (i - (n - 1) / 2) * 44; y = -60 + r * 34; lines.append(arc(cx + x * s, cy + y * s, 12 * s, n=14))
            if r * 9 + i == hot: lamps += [arc(cx + x * s, cy + y * s, rr * s, n=14) for rr in (9, 6, 3)]
    for r, n in enumerate((9, 8, 9)):
        for i in range(n): x = (i - (n - 1) / 2) * 44; lines.append(arc(cx + x * s, cy + (50 + r * 32) * s, 9 * s, n=12))
    shade = hatch(P([(-230, 150), (230, 150), (230, 130), (-230, 130)]), 7, 60)
    return lines, shade, [(lamps, 1.0)]
