import sys; sys.argv = ['x']
exec(open('th_serie.py').read().split('J = [')[0])
def warm(im, k=1.0):
    g = np.asarray(ImageOps.grayscale(im.convert('RGB')), np.float32)
    w = np.stack([g * 1.05 + 18, g * 0.92 + 8, g * 0.75], -1).clip(0, 255).astype(np.uint8); o = Image.fromarray(w).convert('RGBA'); o.putalpha(im.getchannel('A')); return o.filter(ImageFilter.UnsharpMask(2, 90, 2))
def put(can, name, h, cx, warmit=False, dx=0):
    im = cut(name, h=h)
    if warmit: im = warm(im)
    else: im = im.filter(ImageFilter.UnsharpMask(2, 80, 2))
    shadow_paste(can, im, (cx - im.width // 2 + dx, TH - im.height + 8), 22, 0.7, (0, 10))
def vign(can):
    vig = np.clip(np.hypot((np.arange(TW)[None, :] - TW / 2) / TW, (np.arange(TH)[:, None] - TH / 2) / TH) - 0.32, 0, 1) * 300
    v = Image.new('RGBA', (TW, TH), (0, 0, 0, 0)); v.putalpha(Image.fromarray(vig.clip(0, 150).astype(np.uint8))); can.alpha_composite(v)
P = {1: dict(Bfg=[('rede_c', 480, 640)], Cfg=[('chamberlain', 460, 1010), ('rede_c', 520, 560)]),
     2: dict(Bfg=[('t2_panzer', 400, 640)], Cfg=[('t2_panzer', 430, 640)]),
     3: dict(Bfg=[('duenk_c', 330, 640)], Cfg=[('churchill_c', 460, 250), ('degaulle_c', 470, 1030), ('manstein', 540, 640)])}
J = [(1, '1933', 'DER WEG', 'IN DEN KRIEG', 't1_brand.jpg', 0.5, 0.0, 't1_brand.jpg', 'DER WEG IN DEN KRIEG', 't1_brand.jpg', 0.5, 0.3),
     (2, '1939', 'DER ÜBERFALL', 'AUF POLEN', 't2_warschau.jpg', 0.5, 0.0, 't2_brand.jpg', 'DER ÜBERFALL AUF POLEN', 't2_brand.jpg', 0.5, 0.4),
     (3, '1940', 'DER KRIEG', 'IM WESTEN', 't3_duenk.jpg', 0.5, 0.0, 't3_duenk.jpg', 'DER KRIEG IM WESTEN', 't3_duenk.jpg', 0.5, 0.4)]
for n, y, l1, l2, sky, sfx, sfy, fill, title, cb, cfx, cfy in J:
    b = B(n, y, l1, l2, sky, sfx, sfy, fill)
    for nm, h, cx in P[n]['Bfg']: put(b, nm, h, cx, warmit=True)
    logo(b); badge(b, 36, 28, 'TEIL %d' % n); b.convert('RGB').save(O + 'Teil%d_Stil_B_%s.jpg' % (n, y), quality=95)
    c = C(n, y, title, cb, cfx, cfy)
    for nm, h, cx in P[n]['Cfg']: put(c, nm, h, cx)
    vign(c); logo(c); badge(c, 36, 28, 'TEIL %d' % n); c.convert('RGB').save(O + 'Teil%d_Stil_C_%s.jpg' % (n, y), quality=95); print(n)
