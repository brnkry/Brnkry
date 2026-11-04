import re, subprocess, sys, os, hashlib, urllib.parse
from PIL import Image
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'
out = sys.argv[1]; pages = sys.argv[2:]
for pg in pages:
    html = subprocess.run(['curl', '-sSL', '-m', '40', '-A', UA, pg], capture_output=True).stdout.decode('utf8', 'ignore')
    urls = set(re.findall(r'(?:src|href|data-src|content|data-lazy-src)=["\']([^"\']+?\.(?:jpe?g|png|webp)(?:\?[^"\']*)?)["\']', html, re.I))
    urls |= set(re.findall(r'srcset=["\']([^"\' ]+\.(?:jpe?g|png|webp))', html, re.I))
    host = re.sub(r'\W', '_', urllib.parse.urlparse(pg).netloc)[:20]; n = 0
    for u in urls:
        u = urllib.parse.urljoin(pg, u.replace('&amp;', '&'))
        if any(k in u.lower() for k in ('logo', 'icon', 'avatar', 'sprite', 'banner', 'emoji', 'button', 'flag')): continue
        f = os.path.join(out, '%s_%s.%s' % (host, hashlib.md5(u.encode()).hexdigest()[:8], 'jpg'))
        subprocess.run(['curl', '-sSL', '-m', '40', '-A', UA, '-e', pg, '-o', f, u])
        try:
            im = Image.open(f); im.load()
            if min(im.size) < 250: os.remove(f); continue
            im.convert('RGB').save(f, quality=95); n += 1
        except Exception: 
            if os.path.exists(f): os.remove(f)
    print(pg, len(urls), 'kept', n, flush=True)
