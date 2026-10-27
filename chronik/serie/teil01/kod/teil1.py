# "Deutschland im Zweiten Weltkrieg", Teil 1: Der Weg in den Krieg. Magazine look (see serie/code/magazine.py):
# an open glossy magazine, the camera on one page at a time, pages turning with a curl, text set word by word on the
# narration (words.json), one accent colour, fine ink illustrations, archive film as captioned photos, a pen-and-ink map.
import sys, os, json, math, functools, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
T1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, os.path.dirname(T1.rstrip('/')) + '/serie/code')
import magazine as M
from magazine import (W, H, FPS, PW, PH, SW, clamp, eio, eout, lerp, serif, sans, italic, gloss, desk, stamp_ink, words_in, ink, poly, arc,
                      hatch, tank_ink, strike_red, turn, spread_base, TXT, GREY, ACC)
S = M.S
WORDS = json.load(open(T1 + 'words.json'))
def wt(word, after=0.0):
    for w_, a, b in WORDS:
        if a >= after - 0.01 and w_.lower().startswith(word.lower()): return a
    raise KeyError(word)
def ws(word, after=0.0): return wt(word, after) - 0.04
VEND = WORDS[-1][2]; T_END = VEND + 4.4          # the last page (Teil 2) stays a little after the narration

# ---------- page furniture ----------
LIGHT = (215, 215, 215)
def runhead(pg, left_side, page_no):
    d = ImageDraw.Draw(pg); x0, x1 = 150, 980
    for k, c in enumerate((ACC, (150, 150, 150), (205, 205, 205))): d.ellipse((x0 + k * 34, 150, x0 + k * 34 + 22, 172), fill=c)
    d.text((x0 + 120, 161), 'CHRONIK DER MACHT', font=sans(26, 600), fill=GREY, anchor='lm')
    d.text((x1, 161), 'TEIL 1', font=sans(28, 700), fill=ACC, anchor='rm')
    d.line((x0, 200, x1, 200), fill=LIGHT, width=2)
    d.text((x0 if left_side else x1, PH - 160), str(page_no), font=sans(30, 500), fill=GREY, anchor='lm' if left_side else 'rm')
def fade_col(c, k): return tuple(int(lerp(249, v, k)) for v in c)
def label(pg, t, t0, s, xy, font, col=ACC, anchor='la', dur=0.3):
    if t < t0: return
    k = eout((t - t0) / dur); ImageDraw.Draw(pg).text((xy[0], xy[1] + (1 - k) * 12), s, font=font, fill=fade_col(col, k), anchor=anchor)
def rule(pg, t, t0, y, x0=150, x1=980, col=LIGHT, wd=2):
    if t < t0: return
    ImageDraw.Draw(pg).line((x0, y, lerp(x0, x1, eout((t - t0) / 0.5)), y), fill=col, width=wd)
def body(pg, t, x, y, text, after, accent=(), bold=(), size=58, lh=78, maxw=830):
    """a sentence of the narration set in the body face; each word fades in on its own spoken time"""
    spec = []; a = after
    for w_ in text.split():
        key = w_.strip('.,:;')
        try: tw = wt(key, a); a = tw + 0.01
        except KeyError: tw = wt(key, after)     # the page words in another order than spoken
        st = 'a' if key in accent else 'b' if key in bold else 'n'; spec.append((w_, tw - 0.04, st))
    return words_in(pg, t, x, y, spec, lambda st: serif(size, 700 if st in 'ab' else 400), lh, maxw)
def strike(pg, t, t0, a_, b_, wd=7): strike_red(pg, t, t0, a_, b_, wd)

# ---------- archive film as photos ----------
@functools.lru_cache(maxsize=6)
def clipf(d, pre, i, n):
    return Image.open(T1 + '%s/%s%04d.jpg' % (d, pre, max(1, min(n, i)))).convert('RGB')
CLIPS = {'f1a': ('f1', 'a', len([f for f in os.listdir(T1 + 'f1') if f.startswith('a')])), 'f1b': ('f1', 'b', len([f for f in os.listdir(T1 + 'f1') if f.startswith('b')])),
         'f3': ('f3', 'a', len(os.listdir(T1 + 'f3'))), 'f4': ('f4', 'a', len(os.listdir(T1 + 'f4')))}
def photo(pg, t, t0, clip, box, caption, rate=1.0):
    if t < t0: return
    k = eout((t - t0) / 0.4); x0, y0, w_, h_ = box; d_, p_, n = CLIPS[clip]
    fr = clipf(d_, p_, int((t - t0) * FPS * rate) + 1, n); fr = ImageEnhance.Contrast(ImageEnhance.Color(fr).enhance(0.0)).enhance(1.08)
    sc = max(w_ / fr.width, h_ / fr.height); cw, ch = w_ / sc, h_ / sc   # cover the box, centred crop
    fr = fr.resize((w_, h_), Image.LANCZOS, box=(max(0, (fr.width - cw) / 2), max(0, (fr.height - ch) / 2), min(fr.width, (fr.width + cw) / 2), min(fr.height, (fr.height + ch) / 2)))
    if k < 1: fr = Image.blend(Image.new('RGB', fr.size, (249, 248, 245)), fr, k)
    pg.paste(fr, (x0, y0)); d = ImageDraw.Draw(pg)
    d.line((x0, y0 + h_ + 24, x0 + 140, y0 + h_ + 24), fill=fade_col(ACC, k), width=5)
    d.text((x0, y0 + h_ + 44), caption, font=italic(28), fill=fade_col(GREY, k))
@functools.lru_cache(None)
def soldier():
    """the photo Boran supplied (a soldier in front of a lorry); the eagle on his chest blurred (CDM)"""
    im = Image.open(T1 + 'drive/BG2_Bild_4.jpg').convert('RGB'); r = 9; x, y = 113, 84
    reg = im.crop((x - r * 2, y - r * 2, x + r * 2, y + r * 2)); bl = reg.resize((4, 4), Image.BILINEAR).resize(reg.size, Image.BICUBIC)
    m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).ellipse((r * 2 - r - 3, r * 2 - r - 3, r * 2 + r + 3, r * 2 + r + 3), fill=255)
    im.paste(Image.composite(bl, reg, m.filter(ImageFilter.GaussianBlur(2))), (x - r * 2, y - r * 2))
    return ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(0.0)).enhance(1.05)
def still(pg, t, t0, im, box, caption):
    if t < t0: return
    k = eout((t - t0) / 0.4); x0, y0, w_, h_ = box; fr = im.resize((w_, h_), Image.LANCZOS)
    if k < 1: fr = Image.blend(Image.new('RGB', fr.size, (249, 248, 245)), fr, k)
    pg.paste(fr, (x0, y0)); d = ImageDraw.Draw(pg)
    d.line((x0, y0 + h_ + 24, x0 + 140, y0 + h_ + 24), fill=fade_col(ACC, k), width=5); d.text((x0, y0 + h_ + 44), caption, font=italic(28), fill=fade_col(GREY, k))

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

# ---------- the map, 1936 to 1939 ----------
GJ = json.load(open(S + 'sch/ne50.geojson'))
def country(name):
    out = []
    for f in GJ['features']:
        if f['properties'].get('NAME') == name:
            g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            out += [p[0] for p in polys]
    return out
LON0, LON1, LAT0, LAT1 = 4.6, 24.2, 46.0, 56.0
MX0, MY0, MW = 150, 380, 830
def mp(lon, lat):
    k = MW / (LON1 - LON0); y = math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
    y1 = math.degrees(math.log(math.tan(math.pi / 4 + math.radians(LAT1) / 2)))
    return MX0 + (lon - LON0) * k, MY0 + (y1 - y) * k
EAST = [(14.2, 53.95), (15.0, 54.05), (16.2, 54.4), (17.0, 54.7), (17.6, 54.8), (17.4, 54.0), (16.9, 53.4), (16.6, 52.9), (15.9, 52.35), (16.4, 51.8), (17.0, 51.5), (17.8, 51.2),
        (18.2, 50.9), (18.6, 50.4), (18.3, 49.95), (17.7, 50.1), (16.9, 50.4), (16.3, 50.65), (15.5, 50.8), (14.85, 50.9), (14.8, 51.6), (14.6, 52.3), (14.4, 53.0), (14.2, 53.95)]
EPRUSSIA = [(19.3, 54.35), (19.6, 54.45), (20.0, 54.6), (20.6, 54.95), (21.2, 55.25), (22.2, 55.05), (22.8, 54.85), (22.9, 54.35), (22.8, 53.95), (22.0, 53.5), (21.0, 53.25),
            (20.2, 53.2), (19.7, 53.45), (19.2, 53.9), (19.3, 54.35)]
RHINE = [(5.95, 51.8), (6.2, 51.85), (7.4, 51.9), (8.0, 51.3), (8.5, 50.6), (8.9, 50.0), (8.7, 49.3), (8.3, 48.97), (7.6, 49.05), (6.4, 49.5), (6.1, 49.9), (6.1, 50.6), (5.95, 51.0), (5.95, 51.8)]
@functools.lru_cache(None)
def map_masks():
    def mask(polys):
        m = Image.new('L', (PW, PH), 0); d = ImageDraw.Draw(m)
        for p in polys: d.polygon([mp(*q) for q in p], fill=255)
        return m
    reich = mask(country('Germany') + [EAST, EPRUSSIA]); rhine = ImageChops.multiply(mask([RHINE]), reich)
    aut = mask(country('Austria')); cz = mask(country('Czechia'))
    core = cz.filter(ImageFilter.MinFilter(41)); sud = ImageChops.subtract(cz, core)
    return reich, rhine, aut, sud, core
def outline(m):
    e = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(5)), m.filter(ImageFilter.MinFilter(3))); return e
def hatch_fill(pg, m, k, col=ACC, step=14, ang=45, a=0.75):
    """red hatching over a region, swept in from the left as k goes 0..1"""
    if k <= 0: return
    yy, xx = np.mgrid[0:PH, 0:PW]; ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    lines = (np.abs(((xx * ca + yy * sa) % step) - step / 2) < 2.2)
    bb = m.getbbox(); x_edge = lerp(bb[0], bb[2], eout(k)) if bb else 0
    A = (np.asarray(m) > 0) & lines & (xx <= x_edge)
    stamp_ink(pg, Image.fromarray((A * 255 * a).astype(np.uint8)), (0, 0), col)
    E = np.asarray(outline(m)).astype(np.float32) * (xx <= x_edge); stamp_ink(pg, Image.fromarray((E * 0.9).astype(np.uint8)), (0, 0), col)
def map_page(pg, t, t0):
    """pen-and-ink map: neighbours in light grey, the Reich of 1937 in ink, then each step hatched in red with its year"""
    if t < t0: return
    reich, rhine, aut, sud, core = map_masks(); k = eout((t - t0) / 0.8)
    nb = Image.new('L', (PW, PH), 0); d = ImageDraw.Draw(nb)
    for n in ('France', 'Belgium', 'Netherlands', 'Luxembourg', 'Switzerland', 'Italy', 'Poland', 'Lithuania', 'Hungary', 'Slovakia', 'Denmark', 'Austria', 'Czechia', 'Slovenia'):
        for p in country(n): d.polygon([mp(*q) for q in p], outline=255)
    clip = Image.new('L', (PW, PH), 0); ImageDraw.Draw(clip).rectangle((MX0, MY0, MX0 + MW, MY0 + 900), fill=255)
    nb = ImageChops.multiply(nb.filter(ImageFilter.MaxFilter(3)), clip)
    stamp_ink(pg, nb.point(lambda v: int(v * 0.45 * k)), (0, 0), (150, 150, 150))
    stamp_ink(pg, ImageChops.multiply(outline(reich), clip).point(lambda v: int(v * k)), (0, 0), TXT)
    stamp_ink(pg, ImageChops.multiply(reich, clip).point(lambda v: int(v * 0.07 * k)), (0, 0), TXT)
    ImageDraw.Draw(pg).rectangle((MX0, MY0, MX0 + MW, MY0 + 900), outline=fade_col((200, 200, 200), k), width=2)
    label(pg, t, t0 + 0.3, 'DEUTSCHES REICH', mp(9.6, 52.4), sans(30, 700), GREY, 'mm')
    steps = ((ws('Rheinland') - 0.6, rhine, '1936', 'Rheinland', (9.4, 50.3), 'mm', (0, 0)), (ws('Österreich'), aut, '1938', 'Österreich', (14.4, 47.4), 'mm', (0, 50)),
             (ws('Sudetenland'), sud, '1938', 'Sudetenland', (13.0, 51.3), 'mm', (0, -30)), (ws('Tschechoslowakei'), core, '1939', 'Böhmen und Mähren', (17.6, 49.0), 'mm', (40, 70)))
    for ts, m, yr, nm, ll, anc, off in steps:
        if t < ts: continue
        hatch_fill(pg, ImageChops.multiply(m, clip), clamp((t - ts) / 0.6))
        x, y = mp(*ll); label(pg, t, ts + 0.2, yr, (x + off[0], y + off[1] - 26), serif(44, 800), ACC, 'mm'); label(pg, t, ts + 0.3, nm, (x + off[0], y + off[1] + 14), sans(26, 700), TXT, 'mm')

# ---------- the pages ----------
@functools.lru_cache(None)
def base(n, left):
    pg = gloss(n).copy(); runhead(pg, left, n + 1); return pg
@functools.lru_cache(None)
def p1_base():
    pg = base(1, False).copy(); d = ImageDraw.Draw(pg)
    d.text((150, 245), 'DEUTSCHLAND', font=serif(112, 900), fill=TXT); d.text((150, 380), 'IM ZWEITEN WELTKRIEG', font=serif(68, 400), fill=TXT)
    d.text((150, 488), 'TEIL 1', font=sans(34, 800), fill=ACC); d.text((300, 484), 'Der Weg in den Krieg', font=serif(38, 400), fill=GREY)
    d.line((150, 555, 980, 555), fill=LIGHT, width=2); return pg
def P1(t):
    pg = p1_base().copy()
    label(pg, t, 0.0, '1919', (150, 575), serif(124, 800), ACC, dur=0.01)
    spec = [('20', 0.0, 'a'), ('Jahre', ws('Jahre'), 'n'), ('vor', ws('vor'), 'n'), ('dem', ws('dem'), 'n'), ('Zweiten', ws('Zweiten'), 'b'), ('Weltkrieg', ws('Weltkrieg'), 'b'),
            ('durfte', ws('durfte'), 'n'), ('Deutschland', ws('Deutschland'), 'b'), ('keinen', ws('keinen'), 'a'), ('einzigen', ws('einzigen'), 'a'), ('Panzer', ws('Panzer'), 'a'), ('besitzen.', ws('besitzen'), 'n')]
    words_in(pg, t, 150, 760, spec, lambda st: serif(60, 700 if st in 'ab' else 400), 80, 840)
    if t > ws('Deutschland'):
        k = eout((t - ws('Deutschland')) / 0.3); weimar(pg, 150, 1105, 130, 78, k)
        label(pg, t, ws('Deutschland'), 'Weimarer Republik', (300, 1120), sans(30, 600), TXT); label(pg, t, ws('Deutschland'), 'Flagge ab 1919', (300, 1158), italic(26), GREY)
    lines, shade = tank_ink(540, 1360, 0.74); ink(pg, t, ws('keinen'), 0.75, lines, wd=3); ink(pg, t, ws('keinen') + 0.75, 0.35, shade, wd=2, a=0.6)
    strike(pg, t, ws('besitzen'), (230, 1200), (900, 1500)); label(pg, t, ws('besitzen'), 'Abb. 1 · Panzer: verboten', (150, 1530), italic(30), GREY)
    return pg
def P2(t):
    pg = base(2, True).copy()
    label(pg, t, ws('Der', 5), 'Der Vertrag', (150, 250), serif(100, 400), TXT)
    label(pg, t, ws('Versailles'), 'von Versailles', (150, 365), serif(100, 800), ACC)
    label(pg, t, ws('Versailles') + 0.3, 'Unterzeichnet am 28. Juni 1919', (150, 505), sans(34, 600), GREY)
    photo(pg, t, ws('Versailles') + 0.2, 'f1a', (150, 580, 830, 520), 'Archivaufnahme, 1919')
    rule(pg, t, ws('Heer') - 0.2, 1225)
    label(pg, t, ws('Heer') - 0.1, 'DAS HEER', (150, 1250), sans(34, 700), GREY)
    label(pg, t, ws('hunderttausend'), '100.000', (140, 1280), serif(150, 800), ACC)
    label(pg, t, ws('Mann'), 'Mann', (730, 1365), serif(64, 400), TXT)
    return pg
def P3(t):
    pg = base(3, False).copy()
    body(pg, t, 150, 250, 'Luftwaffe und U-Boote: verboten.', 10.0, accent=('verboten',), bold=('Luftwaffe', 'U-Boote'), size=62)
    l1, s1 = biplane(340, 560, 0.66); ink(pg, t, ws('Luftwaffe'), 0.6, l1, wd=3); ink(pg, t, ws('Luftwaffe') + 0.6, 0.3, s1, wd=2, a=0.6)
    l2, s2 = uboat(700, 790, 0.62); ink(pg, t, ws('U-Boote'), 0.6, l2, wd=3); ink(pg, t, ws('U-Boote') + 0.6, 0.3, s2, wd=2, a=0.6)
    strike(pg, t, ws('verboten', 11), (170, 470), (930, 860))
    label(pg, t, ws('verboten', 11) + 0.3, 'Abb. 2 · Luftwaffe und U-Boote: verboten', (150, 900), italic(30), GREY)
    rule(pg, t, ws('und', 12), 990)
    body(pg, t, 150, 1020, 'Das Land sollte Milliarden an Reparationen zahlen.', 12.4, accent=('Milliarden',), bold=('Reparationen',), size=58)
    label(pg, t, ws('zahlen') + 0.1, 'Festgelegt 1921:', (150, 1230), sans(32, 600), GREY)
    label(pg, t, ws('zahlen') + 0.3, '132 Mrd. Goldmark', (150, 1275), serif(84, 800), ACC)
    return pg
def P4(t):
    pg = base(4, True).copy()
    body(pg, t, 150, 250, 'Dann brach das Geld zusammen.', 16.0, bold=('Geld',), size=62)
    label(pg, t, ws('1923'), '1923', (150, 420), serif(150, 800), ACC)
    l, s_ = loaf(760, 515, 0.9); ink(pg, t, ws('kostete'), 0.6, l, wd=3); ink(pg, t, ws('kostete') + 0.6, 0.3, s_, wd=2, a=0.6)
    body(pg, t, 150, 640, 'Ein Brot in Berlin kostete', 19.5, bold=('Brot',), size=56)
    label(pg, t, ws('Hunderte'), 'Hunderte Milliarden Mark', (150, 715), serif(64, 800), ACC)
    L, sh = banknote(565, 1010, 760, 340); ink(pg, t, ws('Hunderte') + 0.2, 0.7, L, wd=3); ink(pg, t, ws('Hunderte') + 0.9, 0.3, sh, wd=2, a=0.35)
    label(pg, t, ws('Mark') + 0.1, 'REICHSBANKNOTE', (565, 935), sans(30, 700), TXT, 'mm')
    label(pg, t, ws('Mark') + 0.2, '100 000 000 000', (565, 1005), serif(60, 800), TXT, 'mm'); label(pg, t, ws('Mark') + 0.3, 'Mark', (565, 1070), serif(40, 400), TXT, 'mm')
    strike(pg, t, ws('wertlos'), (200, 860), (930, 1170), 9)
    body(pg, t, 150, 1230, 'Die Ersparnisse eines ganzen Lebens waren über Nacht wertlos.', 23.4, accent=('wertlos',), bold=('Ersparnisse',), size=56, lh=74)
    return pg
UNEMP = ((1929, 1.9), (1930, 3.1), (1931, 4.5), (1932, 6.0))
def P5(t):
    pg = base(5, False).copy()
    body(pg, t, 150, 250, 'Kaum hatte sich das Land erholt, kam die Weltwirtschaftskrise,', 27.3, accent=('Weltwirtschaftskrise',), size=56, lh=74)
    t0 = ws('Weltwirtschaftskrise'); label(pg, t, t0 + 0.3, 'ARBEITSLOSE IN DEUTSCHLAND (MIO.)', (150, 520), sans(28, 700), GREY)
    rule(pg, t, t0 + 0.3, 1170, 150, 980, (170, 170, 170), 3)
    d = ImageDraw.Draw(pg)
    for i, (yr, v) in enumerate(UNEMP):
        ts = t0 + 0.5 + i * 0.45
        if t < ts: continue
        k = eout((t - ts) / 0.5); x = 190 + i * 200; h = v / 6.0 * 520 * k; col = ACC if yr == 1932 else (60, 60, 64)
        d.rectangle((x, 1170 - h, x + 130, 1170), fill=col)
        d.text((x + 65, 1210), str(yr), font=sans(32, 600), fill=GREY, anchor='mm')
        if k > 0.6: d.text((x + 65, 1170 - h - 32), ('%.1f' % v).replace('.', ','), font=sans(34, 700), fill=col, anchor='mm')
    label(pg, t, ws('sechs'), '6 Millionen', (150, 1270), serif(104, 800), ACC)
    label(pg, t, ws('arbeitslos'), 'Deutsche ohne Arbeit, 1932', (150, 1410), serif(52, 400), TXT)
    return pg
def P6(t):
    pg = base(6, True).copy()
    body(pg, t, 150, 250, 'In dieser Lage wurde', 35.5, size=56)
    label(pg, t, ws('Adolf'), 'Adolf Hitler', (150, 320), serif(104, 800), TXT)
    label(pg, t, ws('30.'), '30. Januar 1933', (150, 455), serif(56, 700), ACC)
    label(pg, t, ws('Reichskanzler'), 'Reichskanzler.', (560, 455), serif(56, 400), TXT)
    photo(pg, t, ws('Adolf') + 0.2, 'f3', (150, 560, 830, 484), 'Archivaufnahme, 1930er Jahre')
    label(pg, t, ws('Innerhalb') , 'INNERHALB WENIGER MONATE AUSGESCHALTET:', (150, 1150), sans(28, 700), GREY)
    for i, (wd_, s_) in enumerate((('Parteien', 'Parteien'), ('Gewerkschaften', 'Gewerkschaften'), ('freie', 'Freie Presse'))):
        y = 1200 + i * 92; ts = ws(wd_, 42); label(pg, t, ts, s_, (150, y), serif(64, 700), TXT)
        if t > ws('aus', 47.5): f = serif(64, 700); strike(pg, t, ws('aus', 47.5) + i * 0.12, (140, y + 48), (160 + f.getlength(s_), y + 40), 7)
    return pg
def P7(t):
    pg = base(7, False).copy()
    body(pg, t, 150, 250, 'Gleichzeitig rüstete Deutschland auf, zuerst heimlich, dann offen.', 48.7, accent=('offen',), bold=('rüstete',), size=56, lh=74)
    label(pg, t, ws('1935'), '1935', (150, 410), serif(130, 800), ACC)
    still(pg, t, ws('Wehrpflicht') - 0.1, soldier(), (150, 600, 400, 388), 'Soldat der Wehrmacht')
    label(pg, t, ws('Wehrpflicht'), 'Wehrpflicht', (600, 620), serif(66, 800), TXT); label(pg, t, ws('zurück'), 'kehrt zurück', (600, 700), serif(50, 400), GREY)
    label(pg, t, ws('Luftwaffe', 56), 'Luftwaffe', (600, 820), serif(66, 800), TXT); label(pg, t, ws('vorgestellt'), 'offiziell vorgestellt', (600, 900), serif(50, 400), GREY)
    l, s_ = monoplane(560, 1200, 0.95); ink(pg, t, ws('Luftwaffe', 56), 0.9, l, wd=3); ink(pg, t, ws('Luftwaffe', 56) + 0.9, 0.4, s_, wd=2, a=0.6)
    label(pg, t, ws('vorgestellt') + 0.3, 'Abb. 2 · Jagdflugzeug der 1930er Jahre', (150, 1340), italic(30), GREY)
    return pg
def P8(t):
    pg = base(8, True).copy()
    label(pg, t, ws('1936') - 0.3, 'Schritt für Schritt', (150, 250), serif(78, 800), TXT)
    map_page(pg, t, ws('1936') - 0.2)
    label(pg, t, ws('niemand'), 'Niemand hielt sie auf.', (150, 1300), serif(54, 400), TXT)
    return pg
def P9(t):
    pg = base(9, False).copy()
    label(pg, t, ws('Jedes') - 0.2, '“', (130, 200), serif(220, 800), ACC)
    body(pg, t, 230, 290, 'Jedes Mal hofften Großbritannien und Frankreich, es sei der letzte Schritt.', 74.8, bold=('Großbritannien', 'Frankreich'), size=54, lh=72, maxw=740)
    rule(pg, t, ws('Am', 79), 590)
    label(pg, t, ws('September', 79), '1. September 1939', (150, 620), serif(56, 700), TXT)
    label(pg, t, ws('Uhr', 82), '4:45', (140, 680), serif(190, 800), ACC); label(pg, t, ws('45', 82) + 0.2, 'Uhr', (590, 790), serif(60, 400), TXT)
    photo(pg, t, ws('eröffnete'), 'f4', (150, 930, 830, 482), 'Linienschiff Schleswig-Holstein vor der Westerplatte')
    return pg
def P10(t):
    pg = base(10, True).copy()
    label(pg, t, ws('Zwei', 89), '3. September 1939', (150, 250), serif(56, 700), ACC)
    label(pg, t, ws('erklärten'), 'Kriegserklärung', (150, 320), serif(96, 800), TXT)
    if t > ws('Großbritannien', 90): k = eout((t - ws('Großbritannien', 90)) / 0.3); union_jack(pg, 150, 480, 180, 100, k); label(pg, t, ws('Großbritannien', 90), 'Großbritannien', (360, 530), sans(40, 700), TXT, 'lm')
    if t > ws('Frankreich', 91): k = eout((t - ws('Frankreich', 91)) / 0.3); tricolore(pg, 150, 620, 180, 100, k); label(pg, t, ws('Frankreich', 91), 'Frankreich', (360, 670), sans(40, 700), TXT, 'lm')
    rule(pg, t, ws('Er', 94), 790)
    label(pg, t, ws('sechs', 94), '6 Jahre', (150, 820), serif(130, 800), TXT); label(pg, t, ws('dauern') , 'Krieg', (590, 880), serif(70, 400), GREY)
    label(pg, t, ws('sechzig'), 'über 60', (150, 1010), serif(170, 800), ACC); label(pg, t, ws('Millionen', 97), 'Millionen Tote', (150, 1220), serif(70, 700), TXT)
    return pg
def P11(t):
    pg = base(11, False).copy(); t0 = VEND + 0.6
    label(pg, t, t0, 'FORTSETZUNG FOLGT', (150, 300), sans(36, 800), ACC)
    label(pg, t, t0 + 0.2, 'TEIL 2', (140, 350), serif(200, 900), TXT)
    label(pg, t, t0 + 0.45, 'Der Überfall auf Polen', (150, 610), serif(64, 400), GREY)
    rule(pg, t, t0 + 0.7, 730)
    label(pg, t, t0 + 1.0, 'Gefällt dir die Serie?', (150, 790), serif(66, 800), TXT)
    for i, s_ in enumerate(('Liken', 'Teilen', 'Abonnieren')):
        label(pg, t, t0 + 1.3 + i * 0.25, s_, (150, 900 + i * 90), serif(62, 700), ACC if i == 2 else TXT)
    label(pg, t, t0 + 2.2, 'damit du Teil 2 nicht verpasst.', (150, 1190), serif(48, 400), GREY)
    return pg

# ---------- the book: right pages R1, R3, ...; turning R(n) shows L(n+1) on its back ----------
RIGHT = [P1, P3, P5, P7, P9, P11]; LEFT = [None, P2, P4, P6, P8, P10]
TURNS = [(ws('besitzen') + 0.25, 0.85), (ws('Dann') - 0.3, 0.85), (ws('In', 35) - 0.35, 0.85), (ws('1936') - 0.7, 0.85), (ws('Zwei', 89) - 0.45, 0.85)]
PANS = [ws('Luftwaffe') - 0.6, ws('Kaum') - 0.55, ws('Gleichzeitig') - 0.6, ws('Jedes') - 0.6, VEND + 0.1]   # left page -> next right page
@functools.lru_cache(None)
def l0():
    pg = gloss(20).copy(); runhead(pg, True, 1); return pg
def spread(t):
    k = sum(1 for a, d in TURNS if t >= a + d)
    for i, (a, d) in enumerate(TURNS):
        if a <= t < a + d:
            left = l0() if i == 0 else LEFT[i](t)
            return turn(spread_base(left, RIGHT[i + 1](t)), RIGHT[i](t), LEFT[i + 1](t), (t - a) / d)
    return spread_base(l0() if k == 0 else LEFT[k](t), RIGHT[k](t))
CR, CL = PW + 585, 585
M.ANG = 2.0                     # a little less askew, so the text keeps its margins at the top and bottom
def cam(t):
    x = CR
    for i, (a, d) in enumerate(TURNS):
        if t >= a: x = lerp(CR, CL, eio((t - a - 0.1) / (d + 0.2)))
        p = PANS[i]
        if t >= p: x = lerp(CL, CR, eio((t - p) / 0.6))
    return x
def frame(t):
    M.spread = spread; M.cam = cam; return M.frame(t)

if __name__ == '__main__':
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[2:]]; n = len(ts); P = Image.new('RGB', (min(n, 6) * 270, ((n + 5) // 6) * 480))
        for i, t in enumerate(ts):
            f = frame(t); d = ImageDraw.Draw(f)
            if os.environ.get('UI'):
                d.rectangle((0, 0, W, 170), outline=(0, 255, 255), width=4); d.rectangle((940, 700, W, 1580), outline=(0, 255, 255), width=4); d.rectangle((0, 1590, W, H), outline=(0, 255, 255), width=4)
            d.text((10, 300), '%.2f' % t, fill=(255, 0, 255), font=sans(40, 700)); P.paste(f.resize((270, 480)), ((i % 6) * 270, (i // 6) * 480))
        P.save(T1 + sys.argv[2 + n] if False else T1 + 'chk/prev.jpg', quality=85); sys.exit()
    if sys.argv[1] == 'T': print(round(T_END, 3)); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
