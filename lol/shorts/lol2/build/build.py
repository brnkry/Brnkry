"""LoL 2 Short v2: full-screen 9:16 from the official New Dawn video, quick slide transitions,
the official video's own sound under the voice-over.
usage: python3 build.py timeline | base | check | mix
Modes: G  full-height 9:16 crop (x may be an ffmpeg expression in t),
       Z  zoomed 9:16 crop (w, x, y),
       C  cinematic crop (top 900 px, burned-in subtitles left out),
       S  still frame panned left to right (x0, x1),
       FC still frame crop (x, darken),
       F  blurred still (cards sit on top),
       T  text card (logo / date) on its own dark background, (hold_until_src)."""
import subprocess, sys, json, os
S = '/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad/lol2'
SRC = S + '/official.mp4'; OUT = S + '/out2'; os.makedirs(OUT, exist_ok=True)
END = 69.6; D = 0.2   # slide length
VX = 'clip((t+{o})*560,0,560)'  # follow Vayne through the wall (o = src start - 107.5)
# out a, out b, mode, src, params, speed, slide into this segment (L/R/None)
PLAN = [
    (0.00, 1.25, 'G', 107.75, (VX.format(o=.25),), 1, None),   # Vayne through the wall
    (1.25, 1.95, 'G', 98.0, (680,), 1, 'L'),                    # new champ select
    (1.95, 2.75, 'G', 98.76, (1200,), 1, 'R'),                  # Blitz pick, 3 choices
    (2.75, 3.65, 'G', 105.25, (760,), 1, 'L'),                  # minions
    (3.65, 4.45, 'G', 101.7, (540,), 1, 'R'),                   # Garen sword
    (4.45, 5.15, 'G', 109.15, (700,), 1, 'L'),                  # Baron
    (5.15, 7.45, 'C', 91.0, (610, .3), 1, 'R'),                 # Ahri (hayir)
    (7.45, 10.75, 'C', 55.5, (1000, .1), 1, 'L'),               # Blitz rising
    (10.75, 12.4, 'G', 107.38, (VX.format(o=-.12),), 1, 'R'),   # Vayne, normal speed
    (12.4, 14.3, 'Z', 107.45, (520, 'clip((t-.05)*560,0,560)+44', 160), .75, 'L'),
    (14.3, 17.2, 'G', 107.38, (VX.format(o=-.12),), .55, 'R'),   # slow: passes the wall before the condemn
    (17.2, 18.95, 'Z', 107.9, (440, 'clip((t+.4)*560,0,560)+84', 200), .6, 'L'),
    (18.95, 19.75, 'G', 97.95, (680,), 1, 'R'),                 # champ select lobby
    (19.75, 20.22, 'G', 98.76, (1240,), 1, None),               # source cut inside the official video
    (20.22, 24.04, 'FC', 99.23, (1240, 0), 1, None),            # 3 choices (ring on top)
    (24.04, 26.55, 'FC', 99.23, (1240, .45), 1, 'L'),           # VOLT vs YUCE EL cards on top
    (26.55, 27.45, 'G', 100.05, (580,), 1, 'R'),                # new rift textures
    (27.45, 28.4, 'G', 100.05, (60,), 1, 'L'),
    (28.4, 29.35, 'G', 100.05, (1250,), 1, 'R'),
    (29.35, 34.25, 'S', 100.3, (450, 1100), 1, 'L'),             # 2014 / 12 yil over the rift
    (34.25, 35.85, 'G', 100.96, (540,), 1, 'R'),                # Garen ult
    (35.85, 36.9, 'Z', 101.5, (440, 625, 150), 1, 'L'),
    (36.9, 38.0, 'G', 101.45, (540,), 1, 'R'),
    (38.0, 39.95, 'C', 85.0, (800, .1), 1, 'L'),                # Jhin (sinematik ultiler)
    (39.95, 41.15, 'G', 102.6, (650,), 1, 'R'),                 # Morgana ult
    (41.15, 43.1, 'Z', 102.6, (480, 760, 170), .6, 'L'),        # slow, zoom on Ashe getting healed
    (43.1, 45.1, 'C', 72.9, (930, .1), 1, 'R'),                 # Poppy (yetenek modlari)
    (45.1, 46.45, 'G', 103.8, (500,), 1, 'L'),                  # meteor
    (46.45, 47.8, 'Z', 103.8, (440, 580, 100), 1, 'R'),
    (47.8, 50.4, 'C', 78.35, (700, .1), 1, 'L'),                # Volibear storm (ejder ruhu)
    (50.4, 51.4, 'G', 105.2, (760,), 1, 'R'),                   # minions
    (51.4, 52.4, 'Z', 105.22, (460, 720, 90), 1, 'L'),
    (52.4, 53.55, 'G', 106.22, (560,), 1, 'R'),                 # dragon pit
    (53.55, 54.7, 'Z', 106.22, (440, 680, 110), 1, 'L'),
    (54.7, 55.85, 'G', 106.22, (300,), 1, 'R'),
    (55.85, 57.0, 'G', 106.22, (1000,), 1, 'L'),
    (57.0, 57.45, 'G', 106.9, (560,), 1, 'R'),
    (57.45, 58.2, 'G', 109.15, (700,), 1, 'L'),                 # Baron, then again slowed
    (58.2, 59.5, 'Z', 109.15, (520, 740, 0), .55, 'R'),
    (59.5, 62.65, 'F', 76.5, (), 1, 'L'),                       # client card
    (62.65, 65.95, 'T', 117.1, (120.3,), 1, 'R'),               # 2027 / Ocak
    (65.95, END, 'T', 111.8, (115.25,), 1, 'L'),                # logo, YENI BASLANGIC, end card
]
SCUTS = [97.42, 98.71, 99.58, 100.96, 102.58, 103.79, 105.17, 106.21, 107.38, 109.12, 109.92, 115.4, 121.5]  # scene cuts in the official video
BG = 'scale=-2:1920,crop=1080:1920:(iw-1080)/2:0,gblur=sigma=28,eq=brightness=-0.18:saturation=1.1'
FEATHER = "format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(X,W-X)/90)*min(1,min(Y,H-Y)/70)'"

def vf(p):
    a, b, m, ss, q, sp, tr = p
    if m in 'GZ':  # never run past the next scene cut of the official video
        lim = min(c for c in SCUTS if c > ss + 0.05) - ss - 0.03
        pre = f'trim=end={lim:.3f},'
    if m == 'G':
        return pre + f"crop=608:1080:'{q[0]}':0,scale=1080:1920:flags=lanczos"
    if m == 'Z':
        w, x, y = q; h = round(w * 16 / 9)
        return pre + f"crop={w}:{h}:'{x}':{y},scale=1080:1920:flags=lanczos"
    if m == 'C':
        x, dk = q
        return f'crop=506:900:{x}:0,scale=1080:1920:flags=lanczos,eq=brightness=-{dk}'
    if m == 'S':
        x0, x1 = q; d = b - a + D
        return f"trim=end_frame=1,tpad=stop_mode=clone:stop_duration=30,crop=608:1080:'{x0}+({x1}-{x0})*t/{d:.2f}':0,scale=1080:1920:flags=lanczos,eq=brightness=-0.12"
    if m == 'FC':
        x, dk = q
        return f'trim=end_frame=1,tpad=stop_mode=clone:stop_duration=30,crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,eq=brightness=-{dk}'
    if m == 'F':
        return f'trim=end_frame=1,tpad=stop_mode=clone:stop_duration=30,crop=iw:900:0:0,{BG}'
    if m == 'T':
        hold = q[0]
        return (f"trim=end={hold - ss:.3f},tpad=stop_mode=clone:stop_duration=30,split[a][b];[a]crop=290:1080:0:0,scale=1080:1920,gblur=sigma=6[bg];"
                f"[b]crop=1320:720:300:200,scale=1080:-2:flags=lanczos,{FEATHER}[fg];[bg][fg]overlay=0:(H-h)/2")

def seglen(i):
    p = PLAN[i]; nxt = PLAN[i + 1] if i + 1 < len(PLAN) else None
    return p[1] - p[0] + (D if nxt and nxt[6] else 0)

ONLY = []
def base(chain_only=False):
    vids = []
    for i, p in enumerate(PLAN):
        o = f'{OUT}/v{i:02d}.mp4'; vids.append(o); L = seglen(i); sp = p[5]
        if chain_only and i not in ONLY: continue
        f = f'[0:v]{vf(p)},setpts=PTS/{sp},fps=30,tpad=stop_mode=clone:stop_duration=3,setsar=1,format=yuv420p[v]'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(p[3]), '-i', SRC, '-filter_complex', f, '-map', '[v]', '-frames:v', str(round(L * 30)),
                        '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '15', '-pix_fmt', 'yuv420p', o], check=True)
        # the official video's own sound for this stretch (slowed to match when the picture is slowed)
        af = f'atempo={sp},' if sp != 1 else ''
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(p[3]), '-i', SRC, '-af', f'{af}aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{p[1] - p[0]:.4f},afade=t=in:d=0.02,afade=t=out:st={max(0, p[1] - p[0] - 0.03):.4f}:d=0.03',
                        '-vn', f'{OUT}/a{i:02d}.wav'], check=True)
        print('part', i, flush=True)
    # video: chain with quick slides (outgoing piece is held for the slide length)
    inp, fc, cur, t = [], [], '[0:v]', seglen(0)
    for v in vids: inp += ['-i', v]
    pre = [f'[{i}:v]fps=30,setpts=PTS-STARTPTS,settb=AVTB[i{i}]' for i in range(len(vids))]; cur = '[i0]'
    for i in range(1, len(PLAN)):
        tr = PLAN[i][6]; lab = f'[x{i}]'
        if tr:
            kind = 'slideleft' if tr == 'L' else 'slideright'
            off = PLAN[i][0]
            fc.append(f'{cur}[i{i}]xfade=transition={kind}:duration={D}:offset={off:.3f}{lab}')
        else:
            fc.append(f'{cur}[i{i}]concat=n=2:v=1:a=0,settb=AVTB{lab}')
        cur = lab
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(pre + fc), '-map', cur, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '15', '-pix_fmt', 'yuv420p', f'{OUT}/base.mp4'], check=True)
    open(f'{OUT}/alist.txt', 'w').writelines(f"file '{OUT}/a{i:02d}.wav'\n" for i in range(len(PLAN)))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/alist.txt', '-c', 'copy', f'{OUT}/src_audio.wav'], check=True)

def timeline():
    open('timeline.js', 'w').write('// generated by build.py\nconst PLAN=' + json.dumps([[p[0], p[1], p[2]] for p in PLAN]) + f';\nconst END={END};\n')

def mix():
    subprocess.run(['node', 'render.js', 'info'], check=True); ev = json.load(open('sfx.json'))
    G = {'impact': -15, 'stamp_dan': -10, 'yazi_vurus': -15, 'card': -17, 'pop': -19, 'click': -14}
    inp = ['-i', '../ses/vo.mp3', '-stream_loop', '-1', '-i', '../../../sett/ses/muzik.mp3']
    fc = [f'[0]aresample=48000,aformat=channel_layouts=stereo,volume=4dB,apad=whole_dur={END},asplit[vo][sc]',
          f'[1]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{END},volume=-15dB,afade=t=in:d=0.3,afade=t=out:st={END - 0.5}:d=0.5[m0]',
          '[m0][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=400[m]']; lab = ['[vo]', '[m]']
    for i, (n, t, g) in enumerate(ev):
        inp += ['-i', f'../ses/{n}.wav']
        fc.append(f'[{i + 2}]aresample=48000,aformat=channel_layouts=stereo,volume={G[n] + g}dB,adelay={int(t * 1000)}:all=1[s{i}]'); lab.append(f'[s{i}]')
    fc.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0:duration=first,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', f'{OUT}/mix.wav'], check=True)
    print('mix ok')

def check():  # three frames of every piece
    os.makedirs(f'{OUT}/chk', exist_ok=True)
    for i, p in enumerate(PLAN):
        d = p[1] - p[0]
        for k, t in enumerate([0.02, d / 2, d - 0.1]):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', f'{OUT}/v{i:02d}.mp4', '-frames:v', '1', '-vf', 'scale=216:384', f'{OUT}/chk/{i:02d}_{k}.png'], check=True)

if __name__ == '__main__':
    {'timeline': timeline, 'base': base, 'chain': lambda: base(True), 'mix': mix, 'check': check}[sys.argv[1]]()
