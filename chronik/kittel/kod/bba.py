# search the Bundesarchiv picture database and list hits with signature, date, title, original caption, file url
import re, html, json, sys, subprocess, urllib.parse
def search(q, page=1):
    u = 'https://www.bild.bundesarchiv.de/dba/de/search/?' + urllib.parse.urlencode({'query': q, 'page': page})
    s = html.unescape(subprocess.run(['curl', '-sSL', '-m', '60', '-A', 'Mozilla/5.0 (CDM research)', u], capture_output=True, text=True).stdout); out = []; seen = set()
    for m in re.finditer(r'"DC5Signatur":"([^"]*)"', s):
        if m.group(1) in seen: continue
        seen.add(m.group(1)); a = s.rfind('"headline"', 0, m.start()); seg = s[max(0, a - 200):m.start() + 6000]
        def g(k):
            x = re.search(r'"%s":"((?:[^"\\]|\\.)*)"' % k, seg); return re.sub('<[^>]+>', '', json.loads('"' + x.group(1) + '"')) if x else ''
        out.append(dict(q=q, sig=m.group(1), head=g('headline'), orig=g('DC5OrigTitel')[:400], date=g('DC5Datvoll'), url=g('DC5FileURL')))
    return out
if __name__ == '__main__':
    R = []
    for q in sys.argv[2:]:
        r = search(q); R += r; print('==', q, len(r))
        for x in r: print('  ', x['sig'], '|', x['date'], '|', x['head'][:90], '|', x['orig'][:160].replace('\n', ' '))
    json.dump(R, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
