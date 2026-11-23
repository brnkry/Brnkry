# YouTube cover for "Der wahre Ursprung des Zweiten Weltkriegs" (CDM), layout after the reference video's cover:
# portrait left, torn old map with blood marks and arrows top right, 1939 photo bottom right, three white text boxes
import json, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageChops
random.seed(7); np.random.seed(7)
W, H = 1280, 720; FD = '/tmp/claude-0/fonts/'
IMG = '../img/'
cv = Image.new('RGB', (W, H), (12, 12, 12))
# ---- portrait (armband and badges blurred) ----
h = Image.open('hitler.jpg').convert('L')
bm = Image.new('L', h.size, 0); ImageDraw.Draw(bm).ellipse((380, 400, 485, 590), fill=255); h = Image.composite(h.filter(ImageFilter.GaussianBlur(16)), h, bm.filter(ImageFilter.GaussianBlur(14)))
h = ImageOps.autocontrast(h, cutoff=1).crop((0, 0, 505, 590)); s = H / 590; h = h.resize((int(505 * s), H), Image.LANCZOS)
cv.paste(h.convert('RGB'), (-95, 0))
# ---- bottom right photo: 1 September 1939 ----
p = Image.open(IMG + 'Polen_1939__Bild_146-1979-056-18A.jpg').convert('L'); p = p.crop((20, 20, 2960, 2040))
p = ImageOps.autocontrast(p, cutoff=1); pw = 760; p = p.resize((pw, int(pw * p.size[1] / p.size[0])), Image.LANCZOS)
cv.paste(p.convert('RGB'), (W - pw, H - p.size[1] + 40))
def torn(y0, amp, x0=0, x1=W):
    pts = []; y = y0
    for x in range(x0, x1 + 8, 8): y = y0 + amp * (0.6 * math.sin(x / 37) + 0.4 * random.uniform(-1, 1)); pts.append((x, y))
    return pts
# ---- map on aged paper ----
MW, MH = 760, 350; L0, L1, B0, B1 = -15, 140, 2, 66
def xy(lon, lat): return ((lon - L0) / (L1 - L0) * MW, (B1 - lat) / (B1 - B0) * MH)
paper = np.full((MH, MW, 3), (214, 198, 164), np.float32)
n = np.array(Image.fromarray((np.random.rand(MH // 6, MW // 6) * 255).astype(np.uint8)).resize((MW, MH), Image.BICUBIC), np.float32) / 255
paper *= (0.86 + 0.2 * n)[..., None]; paper += np.random.randn(MH, MW, 1) * 6
mp = Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(mp)
G = json.load(open('geo.json'))
for f in G['features']:
    g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    for poly in polys:
        ring = [xy(lo, la) for lo, la in poly[0]]
        if len(ring) > 2: d.polygon(ring, fill=(190, 172, 135), outline=(92, 74, 52))
mp = mp.filter(ImageFilter.GaussianBlur(0.6))
# stains and darkened edges
st = Image.new('L', (MW, MH), 0); ds = ImageDraw.Draw(st)
for _ in range(14): x, y, r = random.uniform(0, MW), random.uniform(0, MH), random.uniform(20, 70); ds.ellipse((x - r, y - r, x + r, y + r), fill=random.randint(20, 55))
st = st.filter(ImageFilter.GaussianBlur(25)); mp = Image.composite(Image.new('RGB', (MW, MH), (120, 90, 55)), mp, st)
yy, xx = np.mgrid[0:MH, 0:MW]; e = np.minimum(np.minimum(xx, MW - xx), np.minimum(yy, MH - yy)) / 60.0
mp = Image.fromarray((np.array(mp, np.float32) * (0.55 + 0.45 * np.clip(e, 0, 1))[..., None]).astype(np.uint8))
def blood(lon, lat, r):
    global mp
    cx, cy = xy(lon, lat); m = Image.new('L', (MW, MH), 0); dm = ImageDraw.Draw(m)
    for _ in range(40):
        a = random.uniform(0, 2 * math.pi); q = random.uniform(0, r * 0.7); rr = random.uniform(r * 0.25, r * 0.6)
        x, y = cx + q * math.cos(a), cy + q * math.sin(a); dm.ellipse((x - rr, y - rr, x + rr, y + rr), fill=random.randint(190, 245))
    for _ in range(10):
        a = random.uniform(0, 2 * math.pi); q = random.uniform(r * 0.8, r * 1.4); rr = random.uniform(2, 6)
        x, y = cx + q * math.cos(a), cy + q * math.sin(a); dm.ellipse((x - rr, y - rr, x + rr, y + rr), fill=200)
    m = m.filter(ImageFilter.GaussianBlur(3)); core = m.point(lambda v: 255 if v > 150 else 0).filter(ImageFilter.GaussianBlur(5)); mp = Image.composite(Image.new('RGB', (MW, MH), (128, 16, 12)), mp, m); mp = Image.composite(Image.new('RGB', (MW, MH), (78, 6, 6)), mp, core.point(lambda v: int(v * 0.6)))
SP, ET, MA, EU = (-4, 40), (39.5, 9.5), (125, 44), (13, 51)
for c in (SP, ET, MA): blood(*c, 46)
d = ImageDraw.Draw(mp); fb = ImageFont.truetype(FD + 'Oswald.ttf', 22); fs = ImageFont.truetype(FD + 'Oswald.ttf', 19)
def lab(lon, lat, a, b, dy=0, col=(245, 232, 210)):
    x, y = xy(lon, lat); y += dy
    for t, f, yo in ((a, fb, -12), (b, fs, 12)):
        d.text((x, y + yo), t, font=f, fill=col, anchor='mm', stroke_width=3, stroke_fill=(40, 10, 8))
lab(*SP, 'SPANIEN', '1936'); lab(*ET, 'ÄTHIOPIEN', '1935'); lab(*MA, 'MANDSCHUREI', '1931')
lab(*EU, 'EUROPA', '1939', col=(255, 255, 255))
def arrow(p0, p1, bend):
    (x0, y0), (x1, y1) = p0, p1; mx, my = (x0 + x1) / 2 - (y1 - y0) * bend, (y0 + y1) / 2 + (x1 - x0) * bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1) for t in np.linspace(0, 1, 40)]
    d.line(pts, fill=(28, 20, 14), width=5, joint='curve')
    ax, ay = pts[-1]; bx, by = pts[-4]; ang = math.atan2(ay - by, ax - bx); hl = 18
    d.polygon([(ax + 4 * math.cos(ang), ay + 4 * math.sin(ang)), (ax - hl * math.cos(ang - .5), ay - hl * math.sin(ang - .5)), (ax - hl * math.cos(ang + .5), ay - hl * math.sin(ang + .5))], fill=(28, 20, 14))
ex, ey = xy(*EU)
arrow((xy(*SP)[0] + 40, xy(*SP)[1] - 18), (ex - 52, ey + 6), 0.25)
arrow((xy(*ET)[0] - 6, xy(*ET)[1] - 30), (ex + 6, ey + 30), -0.2)
arrow((xy(*MA)[0] - 70, xy(*MA)[1] - 4), (ex + 58, ey - 4), 0.12)
# torn bottom edge of the map, slight tilt, shadow
mask = Image.new('L', (MW, MH), 255); ImageDraw.Draw(mask).polygon([(0, MH)] + [(x, y) for x, y in torn(MH - 16, 7, 0, MW)] + [(MW, MH)], fill=0)
mk = Image.new('L', (MW, MH), 0); ImageDraw.Draw(mk).polygon([(0, 0), (MW, 0)] + [(x, y) for x, y in torn(MH - 16, 7, 0, MW)][::-1], fill=255)
mk = Image.composite(mk, Image.new('L', (MW, MH), 0), mask)
rgba = mp.convert('RGBA'); rgba.putalpha(mk); rgba = rgba.rotate(-1.5, expand=True, resample=Image.BICUBIC)
sh = Image.new('RGBA', rgba.size, (0, 0, 0, 0)); sh.putalpha(rgba.getchannel('A').point(lambda v: int(v * 0.8)))
cvA = cv.convert('RGBA'); cvA.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (W - rgba.size[0] + 18, -2))
cvA.alpha_composite(rgba, (W - rgba.size[0] + 10, -10)); cv = cvA.convert('RGB')
# soft blend between portrait and the right column
g = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(g)
for i in range(70): gd.line(((W - 760) + i - 35, 330, (W - 760) + i - 35, H), fill=int(255 * (1 - i / 70)))
left = Image.new('RGB', (W, H)); left.paste(h.convert('RGB'), (-95, 0))
cv = Image.composite(left, cv, g.filter(ImageFilter.GaussianBlur(8)))
# subtle film grain over everything
gr = (np.random.randn(H, W, 1) * 7).astype(np.float32); cv = Image.fromarray(np.clip(np.array(cv, np.float32) + gr, 0, 255).astype(np.uint8))
# ---- text in the channel's own style: Oswald Bold, dark / white / yellow plates, red bar, CDM badge ----
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
osw = lambda z: ImageFont.truetype(FD + 'Oswald.ttf', z)
cvA = cv.convert('RGBA')
def plate(x, y, txt, size, bg, fg, px=18, py=10, maxw=None):
    f = osw(size)
    while maxw and f.getlength(txt) > maxw: size -= 2; f = osw(size)
    d = ImageDraw.Draw(cvA); b = d.textbbox((0, 0), txt, font=f); w, hh = b[2] - b[0], b[3] - b[1]
    box = (x, y, x + w + 2 * px, y + hh + 2 * py)
    sh = Image.new('RGBA', cvA.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((box[0] + 7, box[1] + 9, box[2] + 7, box[3] + 9), fill=(0, 0, 0, 200))
    cvA.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(cvA); d.rectangle(box, fill=bg); d.text((x + px - b[0], y + py - b[1]), txt, font=f, fill=fg); return box
T1, T2 = 'DER ECHTE URSPRUNG DES 2. WK', 'ER BEGANN NICHT'
sz = 80
while osw(sz).getlength(T1) > 690: sz -= 1
b1 = plate(30, 378, T1, sz, WHITE, DARK)
b2 = plate(30, b1[3] + 10, T2, sz, WHITE, DARK)
f2 = osw(sz); d2 = ImageDraw.Draw(cvA); bb2 = d2.textbbox((0, 0), T2, font=f2); d2.text((30 + 18 - bb2[0] + f2.getlength('ER BEGANN '), b2[1] + 10 - bb2[1]), 'NICHT', font=f2, fill=RED)
b3 = plate(30, b2[3] + 10, '1939', 150, YEL, DARK, px=24, py=14)
ImageDraw.Draw(cvA).rectangle((b3[0], b3[3] + 10, b3[0] + 150, b3[3] + 20), fill=RED)
cvA.convert('RGB').save('cover_ursprung.jpg', quality=93); print('ok')
