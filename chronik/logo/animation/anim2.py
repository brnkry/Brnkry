# logo outro v3 (1920x1080, 30 fps): starts exactly as the CDM avatar, ends exactly as the banner (blurred B-17 photo, CHRONIK [DER MACHT], tagline)
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D = sys.argv[1] + '/'; F = D + '../sch/fonts/'
W, H, FPS, T = 1920, 1080, 30, 6.0
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
K = 1920 / 2560                     # banner (2560 wide) scaled to this frame
S = 186 * K; f = ImageFont.truetype(F + 'Anton-Regular.ttf', round(S)); ft = ImageFont.truetype(F + 'BebasNeue-Regular.ttf', round(80 * K))
CY, TAG_Y = 680 * K, 888 * K
# proportions per font size: avatar (cdm.py, size 380) and banner (bg.py, size 186)
LOGO = dict(gap=30 / 380, pad=26 / 380, top=26 / 380, bot=22 / 380, r0=44 / 380, r1=58 / 380, rend=140 / 380)
BANN = dict(gap=48 / 186, pad=34 / 186, top=30 / 186, bot=26 / 186, r0=38 / 186, r1=50 / 186, rend=220 / 186)
Z0 = 2.6                            # CDM shown this much larger at the start
def clamp(x): return max(0.0, min(1.0, x))
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def lerp(a, b, u): return a + (b - a) * u
def offs(word): return [f.getlength(word[:i]) for i in range(len(word))]
wC, wCH, wDM, wDE = f.getlength('C'), f.getlength('CHRONIK'), f.getlength('DM'), f.getlength('DER MACHT')
oCH, oDE = offs('CHRONIK'), offs('DER MACHT')
bb = f.getbbox('DM', anchor='lm'); BT, BB = CY + bb[1], CY + bb[3]   # cap top / baseline of the text line

def geom(u):
    p = {k: lerp(LOGO[k], BANN[k], u) * S for k in LOGO}
    wl = lerp(wC, wCH, u); wr = lerp(wDM, wDE, u)
    x0 = W / 2 - (wl + p['gap'] + 2 * p['pad'] + wr) / 2
    pl = x0 + wl + p['gap']; return p, x0, pl, pl + 2 * p['pad'] + wr

# background = the banner photo, blurred and darkened; at the start almost black
src = Image.open(D + '../sb/img/p04.jpg').convert('RGB')
s = max(W / src.width, H / src.height); src = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.LANCZOS)
src = src.crop(((src.width - W) // 2, (src.height - H) // 2, (src.width - W) // 2 + W, (src.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(8))
src = Image.blend(ImageEnhance.Color(src).enhance(0.55), Image.new('RGB', (W, H), (10, 11, 13)), 0.52)
PHOTO = np.asarray(src).astype(np.float32); BLACK = np.full_like(PHOTO, 0); BLACK[:] = DARK
rng = np.random.default_rng(1)

def letter(can, ch, x, col, a=1.0, clip=None, dy=0.0):
    if a <= 0.01: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).text((x, CY + dy), ch, font=f, fill=col + (int(255 * a),), anchor='lm')
    if clip: m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle(clip, fill=255); L.putalpha(Image.composite(L.getchannel('A'), Image.new('L', (W, H), 0), m))
    can.alpha_composite(L)

def frame(t):
    u = eio((t - 1.45) / 1.0)          # opening
    kb = eio((t - 1.3) / 1.4)          # photo fades in behind
    bg = lerp(BLACK, PHOTO, kb) + rng.normal(0, 4, (H, W))[..., None]
    img = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert('RGBA')
    p, x0, pl, pr = geom(u)
    if kb > 0:   # soft dark field behind the title, as on the banner
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((x0 - 120 * K, 520 * K, pr + 120 * K, 930 * K), fill=(0, 0, 0, int(150 * kb))); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(80 * K)))
    can = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    k_in = eout((t - 0.15) / 0.5)
    letter(can, 'C', x0, WHITE, k_in, dy=(1 - k_in) * 20)
    if u > 0:   # HRONIK unrolls out of the C
        edge = x0 + wC + (wCH - wC) * u
        for ch, o in zip('HRONIK', oCH[1:]): letter(can, ch, x0 + o, WHITE, 1.0, clip=(x0 + wC * 0.85, 0, edge, H))
    if t > 0.35:   # yellow plate: opens, then stretches from DM to DER MACHT
        kp = eout((t - 0.35) / 0.45); mid = (pl + pr) / 2; hw = (pr - pl) / 2 * kp
        clip = (mid - hw, BT - p['top'], mid + hw, BB + p['bot'])
        ImageDraw.Draw(can).rectangle(clip, fill=YEL + (255,))
        ka = clamp((t - 0.55) / 0.25) * (1 - clamp(u / 0.25)); tx = pl + p['pad']
        letter(can, 'D', tx, DARK, ka, clip); letter(can, 'M', tx + f.getlength('D'), DARK, ka, clip)
        if u > 0.12:
            kv = clamp((u - 0.12) / 0.2)
            for ch, o in zip('DER MACHT', oDE):
                if ch != ' ': letter(can, ch, tx + o, DARK, kv, clip)
        kr = eout((t - 0.7) / 0.35)   # red rule under the left part of the plate
        if kr > 0: ImageDraw.Draw(can).rectangle((pl, BB + p['r0'], pl + (p['pad'] + p['rend']) * kr, BB + p['r1']), fill=RED + (255,))
    z = lerp(Z0, 1.0, u)
    if abs(z - 1) > 1e-3: can = can.transform((W, H), Image.AFFINE, (1 / z, 0, W / 2 - W / 2 / z, 0, 1 / z, CY - CY / z), Image.BICUBIC)
    ktag = eout((t - 2.7) / 0.6)
    if ktag > 0: ImageDraw.Draw(can).text((W / 2, TAG_Y + (1 - ktag) * 16), 'GESCHICHTE  ·  QUELLEN  ·  ORIGINALAUFNAHMEN', font=ft, fill=(215, 210, 200, int(255 * ktag)), anchor='mm')
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 160), (0, 0), can.getchannel('A')); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (4, 7))
    img.alpha_composite(can)
    fade = clamp((t - (T - 0.6)) / 0.6) if t > T - 0.6 else clamp(1 - t / 0.15)
    if fade > 0: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * fade))))
    return img.convert('RGB')

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'preview':
        ts = [1.0, 1.7, 2.0, 2.3, 3.0, 4.5]; P = Image.new('RGB', (3 * 640, 2 * 360))
        for i, t in enumerate(ts): P.paste(frame(t).resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
        P.save(D + 'anim_preview.jpg', quality=85); frame(4.5).save(D + 'anim_end.jpg', quality=92); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', D + 'logo_v.mp4'], stdin=subprocess.PIPE)
    for n in range(int(T * FPS)): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
