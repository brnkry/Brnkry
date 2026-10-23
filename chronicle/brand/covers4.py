# Four 9:16 covers in the fixed layout of the Yamamoto cover Boran picked (yama/code/thumbs.py, cover A):
# full-bleed portrait, logo centred at y 340 on a soft dark backing, big Oswald lines at y 1110 / 1250, yellow plate at y 1400 with a red rule.
# Positions never change; only the photo, the words and the sizes do. Swastikas: each project's own lib9.src (blur on the German channel).
import sys, os, importlib
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
VW, VH = 1080, 1920; MAXW = 780            # 780: keeps clear of the right-hand buttons (x > 930)
LOGO_Y, L1, L2, PL = 340, 1110, 1250, 1400  # fixed positions
def project(code):
    sys.path.insert(0, S + code); sys.modules.pop('lib9', None); L = importlib.import_module('lib9'); sys.path.pop(0); return L
def curve(can, a, c, b, col, w=9, head=30):
    """curved arrow a -> b through control point c, dark edge so it reads on the photo"""
    pts = [((1 - v) ** 2 * a[0] + 2 * (1 - v) * v * c[0] + v * v * b[0], (1 - v) ** 2 * a[1] + 2 * (1 - v) * v * c[1] + v * v * b[1]) for v in np.linspace(0, 1, 40)]
    L = Image.new('RGBA', can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); e, q = pts[-1], pts[-4]; import math; ang = math.atan2(e[1] - q[1], e[0] - q[0])
    tri = [(e[0] + 8 * math.cos(ang), e[1] + 8 * math.sin(ang)), (e[0] - head * math.cos(ang - .5), e[1] - head * math.sin(ang - .5)), (e[0] - head * math.cos(ang + .5), e[1] - head * math.sin(ang + .5))]
    for wd, cl in ((w + 7, (0, 0, 0, 170)), (w, col + (255,))):
        d.line(pts[:-3], fill=cl, width=wd, joint='curve')
        d.polygon(tri, fill=cl) if wd == w else d.polygon([(x + 2, y + 2) for x, y in tri], fill=cl)
    can.alpha_composite(L)
def shared_arrows(can, fs, lines, pf, pl, py_, pb, col):
    """Wainwright: one arrow from the last word of line 1 (TO / VOR) and one from the first word of the plate's 2nd line (IT / ES) into the shared JAPAN"""
    f1, f2 = fs; s1, s2 = lines[0][0], lines[1][0]; w1 = s1.split(' ')[-1]
    x1 = VW / 2 - f1.getlength(s1) / 2; to_x = x1 + f1.getlength(s1[:-len(w1)]) + f1.getlength(w1) / 2; to_y = L1 + f1.size * 0.62   # starts clearly under TO
    jl, jr = VW / 2 - f2.getlength(s2) / 2, VW / 2 + f2.getlength(s2) / 2
    curve(can, (to_x, to_y), (to_x + 10, L2 - 10), (jr + 14, L2 - 8), col)
    k = len(pl) - 1; lh = (pb[3] - pb[1] - 24) / len(pl); iy = pb[1] + 12 + lh * (k + 0.5)
    it_x = VW / 2 - pf.getlength(pl[k]) / 2
    curve(can, (it_x - 14, iy), (pb[0] - 150, iy + 10), (jl - 16, L2 + 6), col)   # from right beside IT, over the plate, swinging out left and up
def build(code, img, crop, mark, lines, sub, sub_size, out, arrows=False):
    L = project(code); oswald = L.oswald; YEL, RED, WHITE, DARK = L.YEL, L.RED, L.WHITE, L.DARK
    def fitf(s, size, maxw=MAXW):
        f = oswald(size)
        while f.getlength(s) > maxw and size > 20: size -= 4; f = oswald(size)
        return f
    def T(can, y, s, size, col):
        f = fitf(s, size); La = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(La).text((VW / 2, y), s, font=f, fill=col + (255,), anchor='mm')
        sh = Image.new('RGBA', can.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 230), (0, 0), La.getchannel('A')); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (5, 9)); can.alpha_composite(La)
        return f
    def plate(can, y, s, size):
        """yellow plate; a long line goes onto two lines so the words stay big"""
        f = fitf(s, size, MAXW - 56)
        if '\n' in s:   # split given by the caller
            f = oswald(int(size * 0.9))
            while max(f.getlength(x) for x in s.split('\n')) > MAXW - 56: f = oswald(f.size - 4)
            y += 42
        elif f.size < size * 0.85 and ' ' in s:
            w_ = s.split(' '); k = min(range(1, len(w_)), key=lambda i: abs(len(' '.join(w_[:i])) - len(' '.join(w_[i:])))); s = ' '.join(w_[:k]) + '\n' + ' '.join(w_[k:])
            f = oswald(int(size * 0.9))
            while max(f.getlength(x) for x in s.split('\n')) > MAXW - 56: f = oswald(f.size - 4)
            y += 42   # two lines: centre a little lower, the plate stays between the big line and the bottom overlay
        d = ImageDraw.Draw(can); b = d.multiline_textbbox((VW / 2, y), s, font=f, anchor='mm', align='center', spacing=2); px, py = 28, 12
        s_ = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(s_).rectangle((b[0] - px + 8, b[1] - py + 10, b[2] + px + 8, b[3] + py + 10), fill=(0, 0, 0, 190)); can.alpha_composite(s_.filter(ImageFilter.GaussianBlur(14)))
        d = ImageDraw.Draw(can); d.rectangle((b[0] - px, b[1] - py, b[2] + px, b[3] + py), fill=YEL); d.multiline_text((VW / 2, y), s, font=f, fill=DARK, anchor='mm', align='center', spacing=2)
        d.rectangle((b[0] - px, b[3] + py + 14, b[0] - px + 150, b[3] + py + 24), fill=RED)
        return f, s.split('\n'), y, (b[0] - px, b[1] - py, b[2] + px, b[3] + py)
    def logo(can, a, bpart, h=80):
        """channel logo centred on the screen: white a, bpart on a yellow plate, red rule; soft dark backing like the Yamamoto cover"""
        f = oswald(int(h * 0.86)); d = ImageDraw.Draw(can); wa = d.textlength(a, font=f); wb = d.textlength(bpart, font=f); gap, pad = h * 0.06, h * 0.08
        x = VW / 2 - (wa + gap + 2 * pad + wb) / 2; y = LOGO_Y; cy = y + h * 0.48; xd = x + wa + gap + pad; b = d.textbbox((xd, cy), bpart, font=f, anchor='lm')
        s_ = Image.new('RGBA', can.size, (0, 0, 0, 0)); ImageDraw.Draw(s_).rounded_rectangle((x - h * 0.22, y - h * 0.16, b[2] + pad + h * 0.22, y + h * 1.12), h * 0.12, fill=(8, 9, 11, 170))
        can.alpha_composite(s_.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(can)
        d.text((x, cy), a, font=f, fill=WHITE, anchor='lm'); d.rectangle((b[0] - pad, b[1] - h * 0.08, b[2] + pad, b[3] + h * 0.07), fill=YEL)
        d.text((xd, cy), bpart, font=f, fill=DARK, anchor='lm'); d.rectangle((b[0] - pad, b[3] + h * 0.13, b[0] + h * 0.36, b[3] + h * 0.17), fill=RED)
    im = L.src(img) if hasattr(L, 'src') else Image.open(L.B + 'img/' + img + '.jpg').convert('RGB')
    cx, cy, z = crop; cw = min(im.width, im.height * VW / VH) / z; ch = cw * VH / VW
    x0 = min(max(im.width * cx - cw / 2, 0), im.width - cw); y0 = min(max(im.height * cy - ch / 2, 0), im.height - ch)
    can = im.resize((VW, VH), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGB')
    can = ImageEnhance.Contrast(Image.blend(ImageEnhance.Color(can).enhance(0.85), Image.new('RGB', can.size, (92, 70, 40)), 0.10)).enhance(1.1).convert('RGBA')
    g = np.clip(np.minimum((np.arange(VH) - 1050 + 160) / 160, (1400 + 160 - np.arange(VH)) / 160), 0, 1) * 215   # dark band behind the text block
    B_ = Image.new('RGBA', can.size, (6, 7, 9, 0)); B_.putalpha(Image.fromarray(np.repeat(g.astype(np.uint8)[:, None], VW, 1))); can.alpha_composite(B_)
    logo(can, *mark)
    fs = [T(can, y, s, size, {'w': WHITE, 'y': YEL}[col]) for y, (s, size, col) in zip((L1, L2), lines)]
    pf, pl, py_, pb = plate(can, PL, sub, sub_size)
    if arrows: shared_arrows(can, fs, lines, pf, pl, py_, pb, WHITE)
    os.makedirs(os.path.dirname(out), exist_ok=True); can.convert('RGB').save(out, quality=93); return out
JOBS = {
 'yamamoto': ('yama/code', 's3-5', (0.5, 0.36, 1.12), ('C', 'P'), [('HE KNEW JAPAN', 130, 'w'), ('WOULD LOSE', 130, 'y')], 'THEN HE PLANNED PEARL HARBOR', 88, S + 'yama/thumbs/EN_A_He_Knew.jpg'),
 'rommel': ('en/code', 'r12', (0.48, 0.44, 1.12), ('C', 'P'), [('THE DESERT FOX', 130, 'w'), ('WHY HE TOOK POISON', 130, 'y')], 'HITLER GAVE HIM A CHOICE', 88, S + 'en/thumbs/EN_Desert_Fox_Poison.jpg'),
 'wainwright': ('wain/code', 'w08', (0.506, 0.56, 1.12), ('C', 'P'), [('1942: SURRENDERED TO', 130, 'w'), ('JAPAN', 158, 'y')], '1945: WATCHED IT SURRENDER', 88, S + 'wain/thumbs/EN_Wainwright_Arrows.jpg', True),
 'wainwright_de': ('wain/code', 'w08', (0.506, 0.56, 1.12), ('C', 'DM'), [('1942: KAPITULIERTE VOR', 130, 'w'), ('JAPAN', 158, 'y')], '1945: SAH ER\nES KAPITULIEREN', 88, S + 'wain/thumbs/DE_Wainwright_Kapitulation.jpg', True),
 'balck': ('balck/code', 'b16', (0.5, 0.40, 1.0), ('C', 'DM'), [('HERMANN', 150, 'w'), ('BALCK', 158, 'y')], 'LEHRER ODER TÄTER?', 90, S + 'balck/thumbs/DE_Balck_Lehrer_oder_Taeter.jpg'),
}
if __name__ == '__main__':
    outs = [build(*JOBS[k]) for k in (sys.argv[1:] or JOBS)]
    P = Image.new('RGB', (len(outs) * 400, 711))
    for i, o in enumerate(outs):
        im = Image.open(o).resize((400, 711)); d = ImageDraw.Draw(im); s = 400 / VW
        d.rectangle((930 * s, 680 * s, 400, 1580 * s), outline=(0, 255, 255)); d.rectangle((0, 1580 * s, 400, 711), outline=(0, 255, 255)); P.paste(im, (i * 400, 0))
    P.save(S + 'thumb/covers4.jpg', quality=88); print('ok')
