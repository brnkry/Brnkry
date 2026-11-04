# slow, polite Commons download (the shared server IP gets 429 when it asks quickly); retries the misses in later rounds
import hashlib, subprocess, time, urllib.parse, os, json
from PIL import Image
D = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t2/wiki/'
F = json.load(open(D + 'files.json'))
todo = [(a, f) for a, fs in F.items() if a != 'Einsatzgruppen' for f in fs]
os.makedirs(D + 'img', exist_ok=True)
for rnd in range(3):
    for a, f in todo:
        n = f.replace(' ', '_'); o = D + 'img/%s__%s' % (a[:20], n.replace('/', '_'))
        if os.path.exists(o): continue
        h = hashlib.md5(n.encode()).hexdigest()
        url = 'https://upload.wikimedia.org/wikipedia/commons/%s/%s/%s' % (h[0], h[:2], urllib.parse.quote(n))
        r = subprocess.run(['curl', '-sS', '-m', '60', '-A', 'BrnkryResearch/1.0 (history education)', '-o', o + '.part', '-w', '%{http_code}', url], capture_output=True, text=True).stdout
        ok = False
        if r == '200':
            try:
                im = Image.open(o + '.part'); im.load(); ok = min(im.size) >= 250
            except Exception: pass
        if ok: os.rename(o + '.part', o)
        elif os.path.exists(o + '.part'): os.remove(o + '.part')
        print(rnd, r, ok, n, flush=True); time.sleep(45 if r == '429' else 20)
print('done', len(os.listdir(D + 'img')))
