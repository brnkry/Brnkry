# map data for the long version (historical-basemaps 1914 / 1930 / 1938 + the Teil 1 shapes): Germany 1914 and the losses of
# 1919, the Reich and the steps 1936-39 (from teil1/geo/shapes.json), Poland, Danzig, the USSR and the neighbours, all clipped to Europe
import json, os
from shapely.geometry import shape, mapping, box
from shapely.ops import unary_union
S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
G = S + 'teil1/geo/'; BB = box(-1, 43, 32, 60.5)
def load(y, names):
    g = json.load(open(G + 'world_%s.geojson' % y)); out = {}
    for f in g['features']:
        n = f['properties'].get('NAME')
        if n in names: out.setdefault(n, []).append(shape(f['geometry']).buffer(0))
    return {k: unary_union(v).intersection(BB) for k, v in out.items()}
sh = {k: shape(v) for k, v in json.load(open(G + 'shapes.json')).items()}
de14 = load(1914, ['German Empire'])['German Empire']
n30 = load(1930, ['Poland', 'Danzig', 'Lithuania', 'Latvia', 'Estonia', 'Romania', 'Hungary', 'Czechoslovakia', 'Austria', 'Italy', 'Switzerland', 'France', 'Belgium',
                  'Netherlands', 'Luxembourg', 'Denmark', 'Sweden', 'Yugoslavia', 'Norway', 'Finland', 'United Kingdom of Great Britain and Ireland', 'White Russia'])
n38 = load(1938, ['USSR'])
reich = sh['reich']; lost = de14.difference(reich.buffer(0.02)).buffer(-0.01).buffer(0.01)
lost = unary_union([g for g in (lost.geoms if hasattr(lost, 'geoms') else [lost]) if g.area > 0.02])
out = {'de1914': de14, 'lost1919': lost, 'reich': reich, 'rhineland': sh['rhineland'], 'austria': sh['austria'], 'sudeten': sh['sudeten'], 'bohemia': sh['bohemia'],
       'poland': n30['Poland'], 'danzig': n30['Danzig'], 'ussr': n38['USSR'].intersection(BB)}
nb = {k: v for k, v in n30.items() if k not in ('Poland', 'Danzig')}
for k, v in out.items(): print(k, round(v.area, 2))
json.dump({k: mapping(v.simplify(0.01)) for k, v in out.items()}, open(S + 'lang/geo/shapes.json', 'w'))
json.dump({k: mapping(v.simplify(0.01)) for k, v in nb.items()}, open(S + 'lang/geo/neighbours.json', 'w'))
