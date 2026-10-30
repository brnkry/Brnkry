# pen-and-ink maps for the long version: a Map is a Mercator view of lon/lat onto a canvas; regions are rasterised once,
# hatched in red with a sweep, outlined in ink; labels sit on a paper halo
import json, math, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from lcore import LB, PAPER, TXT, GREY, ACC, stamp_ink, eout, clamp, lerp, fade_col, serif, sans, italic, halo
GEO = json.load(open(LB + 'geo/shapes.json')); NBR = json.load(open(LB + 'geo/neighbours.json'))
def rings(g):
    polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    return [p[0] for p in polys]
def _my(lat): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
class Map:
    def __init__(self, key, size, box, lon0, lon1, lat0):
        """box = (x0, y0, w) on a canvas of size; the map's top latitude follows from the box height"""
        self.key, self.size, self.box, self.lon0, self.lon1, self.lat0 = key, size, box, lon0, lon1, lat0
        self.k = box[2] / (lon1 - lon0); self.h = box[3]
    def mp(self, lon, lat):
        x0, y0, w, h = self.box; return x0 + (lon - self.lon0) * self.k, y0 + h - (_my(lat) - _my(self.lat0)) * self.k
    @functools.lru_cache(None)
    def clip(self):
        c = Image.new('L', self.size, 0); x0, y0, w, h = self.box; ImageDraw.Draw(c).rectangle((x0, y0, x0 + w, y0 + h), fill=255); return c
    @functools.lru_cache(None)
    def mask(self, name):
        g = GEO[name] if name in GEO else NBR[name]; m = Image.new('L', self.size, 0); d = ImageDraw.Draw(m)
        for p in rings(g): d.polygon([self.mp(*q) for q in p], fill=255)
        return ImageChops.multiply(m, self.clip())
    @functools.lru_cache(None)
    def outline(self, name, wd=5):
        m = self.mask(name); return ImageChops.subtract(m.filter(ImageFilter.MaxFilter(wd)), m.filter(ImageFilter.MinFilter(3)))
    @functools.lru_cache(None)
    def ground(self):
        """neighbours as thin grey borders"""
        nb = Image.new('L', self.size, 0); d = ImageDraw.Draw(nb)
        for g in list(NBR.values()) + [GEO['poland'], GEO['danzig'], GEO['ussr']]:
            for p in rings(g): d.line([self.mp(*q) for q in p] + [self.mp(*p[0])], fill=255, width=2, joint='curve')
        return ImageChops.multiply(nb, self.clip())
    @functools.lru_cache(None)
    def bbox(self, name): return self.mask(name).getbbox()
    @functools.lru_cache(None)
    def pattern(self, step=15, ang=45):
        yy, xx = np.mgrid[0:self.size[1], 0:self.size[0]]; ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        return np.abs(((xx * ca + yy * sa) % step) - step / 2) < 2.4
    def frame(self, pg, k):
        x0, y0, w, h = self.box; ImageDraw.Draw(pg).rectangle((x0, y0, x0 + w, y0 + h), outline=fade_col((195, 195, 195), k), width=2)
    def base_layer(self, pg, k, fill=('reich',), outline=('reich',)):
        stamp_ink(pg, self.ground().point(lambda v: int(v * 0.5 * k)), (0, 0), (150, 150, 150))
        for n in fill: stamp_ink(pg, self.mask(n).point(lambda v: int(v * 0.07 * k)), (0, 0), TXT)
        for n in outline: stamp_ink(pg, self.outline(n).point(lambda v: int(v * k)), (0, 0), TXT)
    def tint(self, pg, name, k, col, a=0.12):
        if k > 0: stamp_ink(pg, self.mask(name).point(lambda v: int(v * a * k)), (0, 0), col)
    def hatch(self, pg, name, k, col=ACC, a=0.78, edge=True, step=15, ang=45):
        """red hatching swept in from the left (k 0..1), the region's edge inked in the same sweep"""
        if k <= 0: return
        bb = self.bbox(name)
        if not bb: return
        x0, y0, x1, y1 = bb; xe = lerp(x0, x1, eout(k)); xe_i = int(xe)
        if xe_i <= x0: return
        sub = (slice(y0, y1), slice(x0, xe_i))
        m = np.asarray(self.mask(name))[sub] > 0; P = self.pattern(step, ang)[sub]
        A = (m & P).astype(np.float32) * 255 * a
        if edge: A = np.maximum(A, np.asarray(self.outline(name))[sub].astype(np.float32) * 0.92)
        stamp_ink(pg, Image.fromarray(A.astype(np.uint8)), (x0, y0), col)
    def label(self, pg, t, t0, s, ll, font, col=TXT, anchor='mm', sw=6, dx=0, dy=0):
        x, y = self.mp(*ll); halo(pg, t, t0, s, (x + dx, y + dy), font, col, anchor, sw)
    def line(self, pg, t, t0, dur, pts, col=ACC, wd=6, dash=None):
        """a line drawn on through lon/lat points"""
        if t < t0: return
        P = [self.mp(*q) for q in pts]; segs = list(zip(P, P[1:])); L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs)
        todo = clamp((t - t0) / dur) * L; d = ImageDraw.Draw(pg)
        for a, b in segs:
            l = math.hypot(b[0] - a[0], b[1] - a[1])
            if l <= 0: continue
            u = min(1, todo / l); e = (lerp(a[0], b[0], u), lerp(a[1], b[1], u))
            if dash:
                n = int(l * u / dash)
                for i in range(0, n, 2):
                    p0 = (lerp(a[0], b[0], i * dash / l), lerp(a[1], b[1], i * dash / l)); p1 = (lerp(a[0], b[0], min(u, (i + 1) * dash / l)), lerp(a[1], b[1], min(u, (i + 1) * dash / l)))
                    d.line((p0, p1), fill=col, width=wd)
            else: d.line((a, e), fill=col, width=wd)
            todo -= l
            if todo <= 0: break
    def pin(self, pg, t, t0, ll, col=ACC, r=11):
        if t < t0: return
        k = eout((t - t0) / 0.3); x, y = self.mp(*ll); rr = r * (1.6 - 0.6 * k)
        ImageDraw.Draw(pg).ellipse((x - rr, y - rr, x + rr, y + rr), fill=fade_col(col, k), outline=PAPER, width=3)
