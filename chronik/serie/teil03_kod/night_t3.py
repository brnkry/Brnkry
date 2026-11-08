# Teil 3 photos, unattended: Bundesarchiv priority list (patient retries, no circumvention), Commons picks (Retry-After),
# then 4096 px RGB copies in zips under 95 MB and a source list, pushed to the orphan branch teil3-fotos.
import json, os, subprocess, time, re, urllib.request, urllib.error, zipfile, glob
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
T = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t3/'
K = os.path.dirname(os.path.abspath(__file__)) + '/'
def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)
BA = ['121-0485', '121-0486', '183-B17024', '183-S53854', '183-L15658', '134-B4218', '134-D062', '134-C2593', '101II-MW-5618-16', '134-C1760', '146-1980-078-06A',
      '183-H12959', '183-L11297', '146-1975-020-20A', '183-S61243', '183-L05069', '146-1984-093-23', '146-1984-021-14', '146-2005-0003', '146-1984-021-17',
      '101I-382-0248-32A', 'RH_82_Bild-00165', '146-1978-062-24', '101I-769-0229-10A', '146-1972-045-02', '101I-383-0313-22', '101I-749-0016-11',
      '101II-MW-1160-38', '116-483-081', '116-483-084', '183-L11769', '183-L05360', 'B_145_Bild-P50284', '146-1982-089-18', '183-M1112-500', '183-H28708',
      '183-B15308', '183-2005-1202-500', '146-1981-064-22A', '121-0362']
CM = ['Winston Churchill As Prime Minister 1940-1945 MH26392.jpg', 'Reynaud-Pétain-Weygand-mai1940-A.jpg', 'Charles de Gaulle micro BBC Londres.jpg',
      'De Gaulle - à tous les Français.jpg', 'Koningin Wilhelmina Radio Oranje.jpg', 'Bundesarchiv Erich von Manstein bunt.jpg', 'Pétain-Baschet-mai 1940-A.jpg',
      'Dunkirk 1940 HU1137.jpg', 'The British Army in the UK- Evacuation From Dunkirk, May-June 1940 H1619.jpg', 'The British Army in the UK- Evacuation From Dunkirk, May-June 1940 H1661.jpg',
      'Senkingen av Blücher (5654571951).jpg', 'Rotterdam, Laurenskerk, na bombardement van mei 1940.jpg', 'Bombardement Rotterdam, Bestanddeelnr 120-0455.jpg',
      'Narvik harbor in 1940 with broken German Destroyer.jpg', 'German Army and Luftwaffe Enigma Machine - A16991 in Bletchley Park.jpg', 'Bletchley Park Mansion.jpg',
      'Aufputschmittel Pervitin Deutschlandmuseum Berlin, CC BY-SA 4.0.jpg']
sel = {x['key']: x for x in json.load(open(K + 'ba_sel.json'))}
allba = {x['sig'].replace('Bild ', '').replace(' ', '_'): x for x in json.load(open(K + 'ba_t3.json')) + json.load(open(K + 'ba_t3b.json'))}
def ok(f): return os.path.exists(f) and os.path.getsize(f) > 1e5
# 1. Bundesarchiv: several patient rounds; a reset costs a long pause, never a workaround
for rnd in range(6):
    todo = [k for k in BA if not ok(T + 'ba/%s.jpg' % k)]
    log('BA round', rnd, 'missing', len(todo))
    if not todo: break
    for k in todo:
        x = sel.get(k) or allba.get(k)
        if not x or not x.get('url'): log('no url', k); continue
        f = T + 'ba/%s.jpg' % k
        subprocess.run(['curl', '-sSL', '-m', '240', '-A', 'Mozilla/5.0 (CDM research)', '-o', f, x['url']])
        if ok(f): log('ok', k); time.sleep(4)
        else:
            if os.path.exists(f): os.remove(f)
            log('fail', k); time.sleep(90)
    time.sleep(600)
# 2. Commons picks
m = json.load(open(T + 'commons_meta.json')); os.makedirs(T + 'cmp', exist_ok=True)
UA = 'CDM-research/1.0 (history documentary research)'
for p in CM:
    v = m.get('File:' + p); fn = T + 'cmp/' + re.sub(r'[^A-Za-z0-9._-]+', '_', p)
    if not v: log('commons missing', p); continue
    if ok(fn): continue
    url = v.get('orig') if (v.get('w') or 0) <= 6000 else v.get('url')
    for a in range(8):
        try:
            d = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=120).read(); open(fn, 'wb').write(d); log('cm ok', p, len(d)); break
        except urllib.error.HTTPError as e:
            w = int(e.headers.get('Retry-After', '30')) + 2 if e.code == 429 else 20; log('cm', e.code, 'wait', w); time.sleep(w)
        except Exception as e: log('cm err', e); time.sleep(30)
    time.sleep(5)
# 3. 4096 px RGB copies, zips under 95 MB, source list, push
out = T + 'gh/'; subprocess.run(['rm', '-rf', out]); os.makedirs(out + 'Teil3_4K', exist_ok=True)
lines = ['Teil 3 (Der Krieg im Westen) - Bildquellen (4096 px, RGB)', '', 'Bundesarchiv (Signatur, Datum, Titel):']
for k in BA:
    f = T + 'ba/%s.jpg' % k
    if not ok(f): lines.append('  FEHLT ' + k); continue
    im = Image.open(f).convert('RGB'); im.thumbnail((4096, 4096), Image.LANCZOS); im.save(out + 'Teil3_4K/BA_%s.jpg' % k, quality=92, subsampling=0)
    x = sel.get(k) or allba.get(k, {}); lines.append('  %s | %s | %s' % (k, x.get('date', ''), x.get('head', '')))
lines += ['', 'Wikimedia Commons (Datei, Lizenz):']
for p in CM:
    fn = T + 'cmp/' + re.sub(r'[^A-Za-z0-9._-]+', '_', p)
    if not ok(fn): lines.append('  FEHLT ' + p); continue
    im = Image.open(fn).convert('RGB'); im.thumbnail((4096, 4096), Image.LANCZOS); im.save(out + 'Teil3_4K/CM_' + os.path.basename(fn).rsplit('.', 1)[0] + '.jpg', quality=92, subsampling=0)
    lines.append('  %s | %s' % (p, m.get('File:' + p, {}).get('lic', '')))
lines += ['', 'Hinweis: Hakenkreuze sind in diesen Rohbildern noch NICHT unkenntlich gemacht. Das geschieht nach der Kolorierung, klein und genau auf dem Symbol.']
open(out + 'Teil3_Bildquellen.txt', 'w').write('\n'.join(lines) + '\n')
fs = sorted(glob.glob(out + 'Teil3_4K/*.jpg')); n = 1; size = 0; z = None
for f in fs:
    s = os.path.getsize(f)
    if z is None or size + s > 90e6:
        if z: z.close()
        z = zipfile.ZipFile(out + 'Teil3_Bilder_%d.zip' % n, 'w', zipfile.ZIP_STORED); n += 1; size = 0
    z.write(f, os.path.basename(f)); size += s
if z: z.close()
log('files', len(fs), 'zips', n - 1)
cmds = [['git', 'init', '-q'], ['git', 'checkout', '-q', '--orphan', 'teil3-fotos'], ['git', 'add', '.'],
        ['git', 'commit', '-qm', 'Teil 3 photos at 4096 px for colourising\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_018jCuxbPzYK1g1VtNs2hrtw'],
        ['git', 'remote', 'add', 'origin', 'https://github.com/brnkry/Brnkry']]
for c in cmds: subprocess.run(c, cwd=out)
for a in range(5):
    r = subprocess.run(['git', 'push', '-q', 'origin', 'teil3-fotos'], cwd=out, capture_output=True, text=True); log('push', r.returncode, r.stderr[-200:])
    if subprocess.run(['git', 'ls-remote', 'origin', 'teil3-fotos'], cwd=out, capture_output=True, text=True).stdout.strip(): log('PUSHED'); break
    time.sleep(2 ** (a + 1))
log('ALLDONE')
