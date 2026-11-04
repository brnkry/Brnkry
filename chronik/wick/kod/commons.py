# search Wikimedia Commons for Wick material, list files with metadata, download 2000px versions; honours Retry-After
import json, sys, time, urllib.request, urllib.parse, os
UA = 'CDM-research/1.0 (history documentary research)'
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
def get(url, binary=False):
    for k in range(8):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60); d = r.read(); return d if binary else json.loads(d)
        except urllib.error.HTTPError as e:
            if e.code == 429: w = int(e.headers.get('Retry-After', '30')) + 2; print('429, waiting', w, flush=True); time.sleep(w); continue
            raise
    raise RuntimeError('gave up')
API = 'https://commons.wikimedia.org/w/api.php?'
Q = ['Helmut Wick', 'Wick Jagdgeschwader 2', 'Jagdgeschwader 2 Richthofen 1940', 'Bundesarchiv Bf 109 E 1940 Frankreich', 'Werner Mölders 1940', 'John Dundas RAF',
     '609 Squadron Spitfire 1940', 'Isle of Wight 1940', 'Cherbourg 1940 Luftwaffe', 'Battle of Britain Spitfire 1940', 'Seenotdienst 1940 Luftwaffe', 'Eichenlaub Ritterkreuz 1940 Jagdflieger',
     'Bf 109 Kanalküste 1940', 'Luftwaffe pilot dinghy 1940', 'Jagdgeschwader 53 1939']
seen = {}
for q in Q:
    d = get(API + urllib.parse.urlencode(dict(action='query', list='search', srsearch=q, srnamespace=6, srlimit=40, format='json')))
    for x in d['query']['search']:
        t = x['title']
        if t.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webm', '.ogv')) and t not in seen: seen[t] = q
    print(q, len(d['query']['search']), flush=True); time.sleep(2)
titles = list(seen); meta = {}
for i in range(0, len(titles), 40):
    d = get(API + urllib.parse.urlencode(dict(action='query', titles='|'.join(titles[i:i + 40]), prop='imageinfo', iiprop='url|size|extmetadata', iiurlwidth=2000, format='json')))
    for p in d['query']['pages'].values():
        ii = (p.get('imageinfo') or [{}])[0]; em = ii.get('extmetadata', {})
        meta[p['title']] = dict(q=seen.get(p['title']), url=ii.get('thumburl') or ii.get('url'), orig=ii.get('url'), w=ii.get('width'), h=ii.get('height'),
                                desc=em.get('ImageDescription', {}).get('value', '')[:400], date=em.get('DateTimeOriginal', {}).get('value', '')[:60], lic=em.get('LicenseShortName', {}).get('value', ''))
    time.sleep(2)
json.dump(meta, open(OUT + '/../commons_meta.json', 'w'), ensure_ascii=False, indent=1); print('meta', len(meta), flush=True)
