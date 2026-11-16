# Teil 1-3 thumbnails in styles B and C, without people (Boran places the person himself)
import sys; sys.argv = ['x']
from th4b import *
def B(n, year, l1, l2, sky, skyfx, skyfy, fill):
    s_ = cover(S + sky, TW, TH, skyfx, skyfy, 1.0).filter(ImageFilter.GaussianBlur(1.5)); s_ = ImageEnhance.Color(s_).enhance(0.25); s_ = ImageEnhance.Brightness(s_).enhance(1.15)
    can = s_.convert('RGBA'); can.alpha_composite(Image.new('RGBA', (TW, TH), (235, 238, 240, 120)))
    M = Image.new('L', (TW, TH), 0); ImageDraw.Draw(M).text((TW / 2, 475), year, font=font('Anton', 480), fill=255, anchor='mm')
    fl = ImageOps.colorize(ImageOps.grayscale(cover(S + fill, TW, TH, 0.5, 0.5)), (40, 60, 72), (190, 205, 212)).convert('RGBA'); fl.putalpha(M.point(lambda v: int(v * 0.78))); can.alpha_composite(fl)
    gl = np.clip((np.arange(TH)[:, None] / TH - 0.7) / 0.3, 0, 1) * 0.55 * np.ones((1, TW))
    glow = Image.new('RGBA', (TW, TH), (170, 30, 20, 0)); glow.putalpha(Image.fromarray((gl * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30))); can.alpha_composite(glow)
    text(can, (TW / 2, 162), l1, fit_font('Anton', l1, 880, 92), RED, 'ms', shadow=6)
    text(can, (TW / 2, 258), l2, fit_font('Anton', l2, 880, 84), (30, 30, 32), 'ms', shadow=4)
    logo(can); badge(can, 36, 28, 'TEIL %d' % n); return can
def C(n, year, title, bgimg, fx, fy):
    base = np.ones((TH, TW, 3), np.float32) * 38; base += noise(TW, TH, 1, 3, 2.5)[..., None] * 34 + noise(TW, TH, 1, 9, 0.7)[..., None] * 16
    can = Image.fromarray(base.clip(0, 255).astype(np.uint8)).convert('RGBA')
    sk = ImageOps.grayscale(cover(S + bgimg, TW, TH, fx, fy)); sl = Image.new('RGBA', (TW, TH), (20, 20, 22, 0)); sl.putalpha(sk.point(lambda v: int(v * 0.22))); can.alpha_composite(sl)
    M = Image.new('L', (TW, TH), 0); ImageDraw.Draw(M).text((TW / 2, 395), year, font=font('Anton', 520), fill=255, anchor='mm')
    yx = np.linspace(0, 1, TW)[None, :]; col = np.stack([248 + 0 * yx, 178 + 40 * yx, 92 + 0 * yx], -1).repeat(TH, 0)
    col = col * (1 + noise(TW, TH, 1, 11, 1.5)[..., None] * 0.18); col[rng(12).random((TH, TW)) < 0.004] *= 0.6
    Y = Image.fromarray(col.clip(0, 255).astype(np.uint8)).convert('RGBA'); Y.putalpha(M); can.alpha_composite(Y)
    text(can, (TW / 2, 30), title, fit_font('Anton', title, 890, 96), (240, 240, 240), 'mt', shadow=5)
    vig = np.clip(np.hypot((np.arange(TW)[None, :] - TW / 2) / TW, (np.arange(TH)[:, None] - TH / 2) / TH) - 0.32, 0, 1) * 300
    v = Image.new('RGBA', (TW, TH), (0, 0, 0, 0)); v.putalpha(Image.fromarray(vig.clip(0, 150).astype(np.uint8))); can.alpha_composite(v)
    logo(can); badge(can, 36, 28, 'TEIL %d' % n); return can
J = [(1, '1933', 'DER WEG', 'IN DEN KRIEG', 't1_brand.jpg', 0.5, 0.0, 't1_brand.jpg', 'DER WEG IN DEN KRIEG', 't1_brand.jpg', 0.5, 0.3),
     (2, '1939', 'DER ÜBERFALL', 'AUF POLEN', 't2_warschau.jpg', 0.5, 0.0, 't2_brand.jpg', 'DER ÜBERFALL AUF POLEN', 't2_brand.jpg', 0.5, 0.4),
     (3, '1940', 'DER KRIEG', 'IM WESTEN', 't3_duenk.jpg', 0.5, 0.0, 't3_duenk.jpg', 'DER KRIEG IM WESTEN', 't3_duenk.jpg', 0.5, 0.4)]
for n, y, l1, l2, sky, sfx, sfy, fill, title, cb, cfx, cfy in J:
    B(n, y, l1, l2, sky, sfx, sfy, fill).convert('RGB').save(O + 'Teil%d_Stil_B_%s_leer.jpg' % (n, y), quality=95)
    C(n, y, title, cb, cfx, cfy).convert('RGB').save(O + 'Teil%d_Stil_C_%s_leer.jpg' % (n, y), quality=95); print(n)
