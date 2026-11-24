# Tiger I short (German, CDM): the square colour footage from Boran's TIGER.mp4 reframed to 9:16, the window follows the tank in every shot
# (eased pan + slow push in), cinematic Marcellus labels, Thomas Schendel narration, generated orchestral score.
import os, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)) + '/'
W, H, FPS = 1080, 1920, 30
SRC = D + 'dl/TIGER.mp4'; SQ = 720; WIN = SQ * 9 / 16
VO = 0.6
SH = json.load(open(D + 'shots.json'))
# per shot: window centre (fraction of the square) at start and end, zoom start and end
CX = [(.45, .50), (.70, .62), (.35, .60), (.65, .72), (.45, .50), (.45, .40), (.55, .40), (.40, .42), (.40, .42), (.45, .45), (.50, .50),
      (.50, .50), (.50, .50), (.50, .50), (.45, .45), (.32, .36), (.65, .66), (.55, .60), (.50, .60), (.50, .45), (.40, .55), (.60, .60),
      (.55, .45), (.45, .40), (.55, .57), (.50, .50), (.45, .45), (.65, .62), (.50, .50), (.40, .50), (.65, .70)]
assert len(CX) == len(SH), (len(CX), len(SH))
FD = '/tmp/claude-0/fonts/'
GOLD, WHITE = (214, 178, 100), (246, 244, 238)
LABELS = [(5.02, 'TIGER I', 'Panzerkampfwagen VI'), (11.5, '8,8 CM', 'Kampfwagenkanone 36'), (17.48, '100 MM', 'Frontpanzerung'),
          (26.84, '57 TONNEN', 'Kampfgewicht'), (42.94, '1.350', 'Tiger I gebaut'), (48.74, 'T-34', 'Zehntausende gebaut')]
LDUR = 3.6

def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)

def label_layer(t):
    for t0, big, small in LABELS:
        t0 += VO; u = t - t0
        if 0 <= u <= LDUR:
            a = min(ease(u / 0.6), ease((LDUR - u) / 0.6))
            track = 46 - 34 * ease(u / 1.4)          # letters close up as the word lands
            im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            size = 160
            while True:
                fb = ImageFont.truetype(FD + 'Marcellus-Regular.ttf', size)
                if sum(fb.getlength(c) for c in big) + 46 * (len(big) - 1) <= 940: break
                size -= 6
            fs = ImageFont.truetype(FD + 'Marcellus-Regular.ttf', 48)
            ws = [fb.getlength(c) for c in big]; tw = sum(ws) + track * (len(big) - 1); x = (W - tw) / 2; y = 430
            band = Image.new('L', (W, H), 0); ImageDraw.Draw(band).ellipse((W / 2 - 620, y - 230, W / 2 + 620, y + 190), fill=int(175 * a))
            dark = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dark.putalpha(band.filter(ImageFilter.GaussianBlur(70)))
            for c, w_ in zip(big, ws): d.text((x, y), c, font=fb, fill=WHITE + (int(255 * a),), anchor='ls'); x += w_ + track
            sw = fs.getlength(small); ly = y + 70
            d.text((W / 2, ly), small, font=fs, fill=GOLD + (int(255 * a),), anchor='mm')
            gl = 150 * ease((u - 0.3) / 0.8)
            if gl > 1:
                d.line((W / 2 - sw / 2 - 30 - gl, ly, W / 2 - sw / 2 - 30, ly), fill=GOLD + (int(230 * a),), width=3)
                d.line((W / 2 + sw / 2 + 30, ly, W / 2 + sw / 2 + 30 + gl, ly), fill=GOLD + (int(230 * a),), width=3)
            sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').point(lambda v: int(v * 0.85)))
            out = dark; out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16))); out.alpha_composite(im); return out
    return None

def main():
    n_src = int(round(61.45 * FPS))
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', SRC, '-vf', f'crop={SQ}:{SQ}:0:280,fps={FPS}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', D + 'pic.mp4'], stdin=subprocess.PIPE)
    k = 0
    while True:
        raw = dec.stdout.read(SQ * SQ * 3)
        if len(raw) < SQ * SQ * 3: break
        t = k / FPS; i = max(j for j, (a, b) in enumerate(SH) if a <= t + 1e-6)
        a, b = SH[i]; u = ease((t - a) / max(b - a, 0.01)); c0, c1 = CX[i]
        z = 1.0 + 0.04 * u                                  # slow push in over the shot, framing fixed on the tank (no sideways drift)
        ww = WIN / z; hh = SQ / z; cx = (c0 + c1) / 2 * SQ
        x0 = min(max(cx - ww / 2, 0), SQ - ww); y0 = (SQ - hh) / 2
        fr = Image.frombytes('RGB', (SQ, SQ), raw).resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + ww, y0 + hh))
        L = label_layer(t)
        if L is not None: fr = fr.convert('RGBA'); fr.alpha_composite(L); fr = fr.convert('RGB')
        enc.stdin.write(fr.tobytes()); k += 1
    enc.stdin.close(); enc.wait(); dec.wait(); T = k / FPS; print('frames', k, round(T, 2), flush=True)
    # sound: narration in front, the score evenly underneath and ducked
    fl = (f"[0:a]adelay={int(VO * 1000)}:all=1,aformat=sample_rates=48000:channel_layouts=stereo[v];"
          f"[1:a]atrim=0:{T},aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-31:LRA=6:TP=-6,afade=t=out:st={T - 1.0}:d=1.0[m];"
          f"[v][m]amix=inputs=2:normalize=0:duration=longest,atrim=0:{T},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', D + 'voice.mp3', '-i', D + 'music2.mp3', '-filter_complex', fl, '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', D + 'mix.m4a'], check=True)
    # finish: light grain, vignette, a touch of contrast
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', D + 'pic.mp4', '-i', D + 'mix.m4a', '-filter_complex',
                    '[0:v]eq=contrast=1.05:saturation=0.95,noise=alls=5:allf=t,vignette=PI/5,fade=t=out:st=%.2f:d=0.8[v]' % (T - 0.8),
                    '-map', '[v]', '-map', '1:a', '-shortest', '-c:v', 'libx264', '-b:v', '10M', '-maxrate', '14M', '-bufsize', '20M', '-preset', 'faster',
                    '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', D + 'Tiger_Shorts_DE_v3.mp4'], check=True)
    print('DONE', flush=True)

if __name__ == '__main__':
    main()
