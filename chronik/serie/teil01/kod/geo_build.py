# historical map shapes for Teil 1 (from aourednik/historical-basemaps 1930/1938 and Natural Earth rivers):
# Reich 1930s, Rhineland zone (left bank + 50 km strip right of the Rhine), Austria, Sudetenland, Bohemia and Moravia
import json, sys
from shapely.geometry import shape, mapping, LineString, Polygon
from shapely.ops import unary_union, linemerge
from shapely.affinity import scale
G = sys.argv[1]
def get(f, name):
    g = json.load(open(G + f)); return unary_union([shape(x['geometry']).buffer(0) for x in g['features'] if x['properties'].get('NAME') == name])
de30, at30, cs30 = get('world_1930.geojson', 'Germany'), get('world_1930.geojson', 'Austria'), get('world_1930.geojson', 'Czechoslovakia')
de38, cs38 = get('world_1938.geojson', 'Germany'), get('world_1938.geojson', 'Czechoslovakia')
# the Reich of 1936: Germany 1930, East Prussia, and the Saar (back in 1935; in the 1930 map still under France's column)
saar = get('world_1930.geojson', 'France').intersection(de38).buffer(0)
saar = unary_union([g for g in (saar.geoms if hasattr(saar, 'geoms') else [saar]) if g.area > 0.05])
de30 = unary_union([de30, get('world_1930.geojson', 'East Prussia'), saar]).buffer(0)
ne = json.load(open(sys.argv[2])); sk = unary_union([shape(f['geometry']).buffer(0) for f in ne['features'] if f['properties'].get('NAME') in ('Slovakia', 'Ukraine')])
rv = json.load(open(G + 'rivers.geojson'))
rh = [shape(f['geometry']) for f in rv['features'] if (f['properties'].get('name') or '') in ('Rhine', 'Rhein', 'Rhin')]
rhine = unary_union(rh)
# Rhineland zone: German territory west of the Rhine, plus a 50 km strip east of it (in a local km frame: 1 deg lon = 71 km, lat = 111 km at 50 N)
K = lambda geom, inv=False: scale(geom, 71 if not inv else 1 / 71, 111 if not inv else 1 / 111, origin=(0, 0))
strip = K(K(rhine).buffer(50), True)
lines = list(linemerge(rhine).geoms) if rhine.geom_type == 'MultiLineString' else [rhine]
west = Polygon([(3.0, 52.2), (3.0, 47.4), (7.6, 47.4)] + [], ).buffer(0)
# west of the river: for each latitude band, everything west of the river's x there
import numpy as np
pts = sorted([p for l in (linemerge(rhine).geoms if hasattr(linemerge(rhine), 'geoms') else [linemerge(rhine)]) for p in l.coords if 47.3 < p[1] < 52.2], key=lambda p: p[1])
band = []
for y in np.arange(47.4, 52.1, 0.02):
    near = [p for p in pts if abs(p[1] - y) < 0.05]
    if near: band.append((max(p[0] for p in near), y))
westpoly = Polygon([(2.5, band[0][1])] + band + [(2.5, band[-1][1])]).buffer(0)
rhineland = de30.intersection(unary_union([westpoly, strip])).buffer(0)
sudeten = cs30.intersection(de38).buffer(0)
if sudeten.area < 0.1: sudeten = cs30.difference(cs38).buffer(0)
bohemia = cs38.difference(sk).intersection(Polygon([(11, 48), (19.2, 48), (19.2, 51.5), (11, 51.5)])).buffer(0)
bohemia = unary_union([g for g in (bohemia.geoms if hasattr(bohemia, 'geoms') else [bohemia]) if g.area > 0.05])
out = {'reich': de30, 'rhineland': rhineland, 'austria': at30, 'sudeten': sudeten, 'bohemia': bohemia, 'cs30': cs30, 'rhine': rhine}
for k, v in out.items(): print(k, round(v.area, 3), v.geom_type)
json.dump({k: mapping(v) for k, v in out.items()}, open(G + 'shapes.json', 'w'))
# neighbours as in 1930
g = json.load(open(G + 'world_1930.geojson')); nb = {}
for x in g['features']:
    n = x['properties'].get('NAME')
    if n in ('France', 'Belgium', 'Netherlands', 'Luxembourg', 'Switzerland', 'Italy', 'Poland', 'Lithuania', 'Hungary', 'Denmark', 'Yugoslavia', 'Danzig', 'Czechoslovakia', 'Austria', 'Latvia', 'Romania', 'Liechtenstein', 'Sweden'):
        nb.setdefault(n, []).append(x['geometry'])
json.dump(nb, open(G + 'neighbours.json', 'w')); print(sorted(nb))
