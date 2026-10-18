# logo outro for long videos (1920x1080, 30 fps): CDM appears, then opens into CHRONIK [DER MACHT], red rule, tagline
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = sys.argv[1] + '/'; F = D + '../sch/fonts/'
W, H, FPS, T = 1920, 1080, 30, 5.5
YEL, RED, WHITE, DARK = (244, 199, 15), (196, 38, 40), (245, 245, 240), (14, 15, 18)
S = 210; f = ImageFont.truetype(F + 'Anton-Regular.ttf', S); ft = ImageFont.truetype(F + 'BebasNeue-Regular.ttf', 64)
GAP, PAD, CY = S * 0.14, S * 0.11, 520
def clamp(x): return max(0.0, min(1.0, x))
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def lerp(a, b, u): return a + (b - a) * u
def xs(word, x0):
    """x of each letter when the word starts at x0"""
    out = []; x = x0
    for i, ch in enumerate(word): out.append(x); x = x0 + f.getlength(word[:i + 1])
    return out
wC, wCH, wDM, wDE = f.getlength('C'), f.getlength('CHRONIK'), f.getlength('DM'), f.getlength('DER MACHT')
# start: C [DM]
a0 = W / 2 - (wC + GAP + 2 * PAD + wDM) / 2; pl0 = a0 + wC + GAP; dm0 = xs('DM', pl0 + PAD); pr0 = pl0 + 2 * PAD + wDM
# end: CHRONIK [DER MACHT]
a1 = W / 2 - (wCH + GAP + 2 * PAD + wDE) / 2; ch1 = xs('CHRONIK', a1); pl1 = a1 + wCH + GAP; de1 = xs('DER MACHT', pl1 + PAD); pr1 = pl1 + 2 * PAD + wDE
bb = f.getbbox('DMACHT', anchor='lm'); TOP, BOT = CY + bb[1] - S * 0.09, CY + bb[3] + S * 0.08
# background: dark with a soft centre light, fresh grain every frame
y, x = np.mgrid[0:H, 0:W]; r = np.sqrt(((x - W / 2) / (W * 0.55)) ** 2 + ((y - H / 2) / (H * 0.6)) ** 2)
BG = (np.ones((H, W, 3)) * np.array(DARK, float) * (1 + 0.8 * np.clip(1 - r, 0, 1))[..., None]).astype(np.float32)
rng = np.random.default_rng(1)

def letter(can, ch, x, col, a=1.0, clip=None, dy=0.0):
    if a <= 0.01: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).text((x, CY + dy), ch, font=f, fill=col + (int(255 * a),), anchor='lm')
    if clip: m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle(clip, fill=255); L.putalpha(Image.composite(L.getchannel('A'), Image.new('L', (W, H), 0), m))
    can.alpha_composite(L)

def frame(t):
    img = Image.fromarray(np.clip(BG + rng.normal(0, 4, (H, W))[..., None], 0, 255).astype(np.uint8)).convert('RGBA')
    can = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    k_in = eout((t - 0.15) / 0.5)          # CDM arrives
    u = eio((t - 1.35) / 0.9)              # opening
    # shadow layer for everything drawn on can
    # C, then HRONIK revealed from behind it
    cx = lerp(a0, ch1[0], u)
    letter(can, 'C', cx, WHITE, k_in, dy=(1 - k_in) * 30)
    if u > 0:   # HRONIK unrolls out of the C, moving with it
        edge = cx + wC + (wCH - wC) * u
        for ch, xx in zip('HRONIK', ch1[1:]): letter(can, ch, cx + xx - ch1[0], WHITE, 1.0, clip=(cx + wC * 0.85, 0, edge, H))
    # yellow plate grows from DM to DER MACHT; DM fades out, DER MACHT unrolls from the plate's left edge
    if t > 0.35:
        kp = eout((t - 0.35) / 0.45)
        pl, pr = lerp(pl0, pl1, u), lerp(pr0, pr1, u)
        mid = (pl + pr) / 2; hw = (pr - pl) / 2 * kp
        ImageDraw.Draw(can).rectangle((mid - hw, TOP, mid + hw, BOT), fill=YEL + (255,))
        clip = (mid - hw, TOP, mid + hw, BOT); ka = clamp((t - 0.55) / 0.25) * (1 - clamp(u / 0.25))
        letter(can, 'D', lerp(dm0[0], pl + PAD, u), DARK, ka, clip)
        letter(can, 'M', dm0[1] + (pl - pl0), DARK, ka, clip)
        if u > 0.12:
            kv = clamp((u - 0.12) / 0.2)
            for i, ch in enumerate('DER MACHT'):
                if ch != ' ': letter(can, ch, pl + PAD + (de1[i] - de1[0]), DARK, kv, clip)
    # red rule under the plate, drawn after the opening
    kr = eio((t - 2.35) / 0.4)
    if kr > 0:
        pl = lerp(pl0, pl1, u); ImageDraw.Draw(can).rectangle((pl, BOT + S * 0.11, pl + S * 1.1 * kr, BOT + S * 0.16), fill=RED + (255,))
    # tagline
    ktag = eout((t - 2.6) / 0.6)
    if ktag > 0:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).text((W / 2, BOT + S * 0.62 + (1 - ktag) * 20), 'GESCHICHTE  ·  QUELLEN  ·  ORIGINALAUFNAHMEN', font=ft, fill=(215, 210, 200, int(255 * ktag)), anchor='mm'); can.alpha_composite(L)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (0, 0), can.getchannel('A')); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (6, 10))
    img.alpha_composite(can)
    fade = clamp((t - (T - 0.6)) / 0.6) if t > T - 0.6 else clamp(1 - t / 0.15)
    if fade > 0: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * fade))))
    return img.convert('RGB')

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'preview':
        ts = [0.4, 0.9, 1.5, 1.8, 2.1, 2.6, 3.4, 5.0]; P = Image.new('RGB', (4 * 480, 2 * 270))
        for i, t in enumerate(ts): P.paste(frame(t).resize((480, 270)), ((i % 4) * 480, (i // 4) * 270))
        P.save(D + 'anim_preview.jpg', quality=85); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'medium', D + 'logo_v.mp4'], stdin=subprocess.PIPE)
    for n in range(int(T * FPS)): p.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    p.stdin.close(); p.wait(); print('rc', p.returncode)
