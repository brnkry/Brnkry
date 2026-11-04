# Teil 2: photos from Europeana (aggregates Polish, German and other archives), one search per chapter of the script
import json, subprocess, urllib.parse, os, hashlib, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
D = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t2/eu/'
Q = {'01_angriff': ['Polen 1939 Wehrmacht', 'Poland 1939 invasion', 'wrzesień 1939 Niemcy', 'Polenfeldzug', 'kampania wrześniowa'],
     '02_westerplatte': ['Westerplatte', 'Schleswig-Holstein Danzig 1939'],
     '03_wielun': ['Wieluń 1939', 'Wielun'],
     '04_post_danzig': ['Poczta Polska Gdańsk 1939', 'Polnische Post Danzig'],
     '05_danzig': ['Danzig 1939', 'Gdańsk 1939'],
     '06_kavallerie': ['kawaleria 1939', 'ułani 1939', 'polnische Kavallerie'],
     '07_bromberg': ['Bromberg 1939', 'Bydgoszcz 1939'],
     '08_warschau': ['Warszawa 1939', 'Warschau 1939', 'oblężenie Warszawy', 'Warsaw 1939 siege', 'Starzyński'],
     '09_bzura': ['Bzura 1939', 'jeńcy polscy 1939'],
     '10_fluechtlinge': ['uchodźcy 1939', 'refugees Poland 1939'],
     '11_rote_armee': ['Armia Czerwona 1939', 'Brest-Litowsk 1939', 'Brześć 1939'],
     '12_hel_marine': ['Hel 1939', 'ORP Orzeł', 'ORP Błyskawica', 'Unrug'],
     '13_westfront': ['Saar 1939 französische', 'drôle de guerre 1939', 'Phoney War'],
     '14_besatzung': ['Generalgouvernement', 'Hans Frank Krakau', 'Sonderaktion Krakau', 'getto Piotrków', 'okupacja 1939'],
     '15_katyn': ['Katyń', 'Katyn'],
     '16_exil': ['Sikorski 1939', 'Polish army France 1940'],
     '17_enigma': ['Enigma Rejewski', 'Enigma szyfr', 'Biuro Szyfrów'],
     '18_vertrag': ['Ribbentrop Molotow', 'Ribbentrop Mołotow 1939']}
def search(q):
    out = []
    for start in (1, 101):
        u = 'https://api.europeana.eu/record/v2/search.json?' + urllib.parse.urlencode({'wskey': 'api2demo', 'query': q, 'qf': 'TYPE:IMAGE', 'rows': 100, 'start': start, 'profile': 'rich'})
        try: d = json.loads(subprocess.run(['curl', '-sS', '-m', '60', u], capture_output=True, text=True).stdout)
        except Exception: break
        for it in d.get('items', []):
            yr = ' '.join(it.get('year', []) or []); t = (it.get('title') or [''])[0]
            url = (it.get('edmIsShownBy') or [None])[0]
            if url: out.append((url, t, yr, (it.get('dataProvider') or [''])[0], it.get('guid', '')))
        if d.get('totalResults', 0) <= start + 99: break
    return out
meta = []; seen = set()
for ch, qs in Q.items():
    n = 0
    for q in qs:
        for url, t, yr, prov, guid in search(q):
            if url in seen: continue
            if yr and not any(y in yr for y in ('1938', '1939', '1940', '1941', '1942', '1943', '1944')): continue   # only the war years (or undated)
            seen.add(url); meta.append((ch, url, t, yr, prov, guid)); n += 1
    print(ch, n, flush=True)
def get(m):
    ch, url, t, yr, prov, guid = m
    os.makedirs(D + 'img/' + ch, exist_ok=True)
    f = D + 'img/%s/%s.jpg' % (ch, hashlib.md5(url.encode()).hexdigest()[:10])
    if os.path.exists(f): return f
    subprocess.run(['curl', '-sSL', '-m', '60', '-A', 'BrnkryResearch/1.0 (history education)', '-o', f, url], capture_output=True)
    try:
        im = Image.open(f); im.load()
        if min(im.size) < 400: os.remove(f); return None
        im.convert('RGB').save(f, quality=93); return f
    except Exception:
        if os.path.exists(f): os.remove(f)
        return None
with ThreadPoolExecutor(6) as ex: res = list(ex.map(get, meta))
rows = [(m, r) for m, r in zip(meta, res) if r]
with open(D + 'quellen.tsv', 'w') as fh:
    fh.write('datei\tkapitel\ttitel\tjahr\tarchiv\teuropeana\n')
    for (ch, url, t, yr, prov, guid), r in rows: fh.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (os.path.relpath(r, D + 'img'), ch, t.replace('\t', ' '), yr, prov, guid))
print('kept', len(rows), 'of', len(meta))
