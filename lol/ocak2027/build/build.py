"""LoL 2027 long video (16:9, Feedleme Hocam).
usage: python3 build.py base | mix
Sources: B = official New Dawn video (1080p), A = Season 2027 dev video (720p, Turkish subtitles burned in at the bottom).
Modes: B    B full frame              BC  B top 1600x900 at x (cinematic, subtitles left out)
       A    A top 1102x620 scaled up  BL  blurred, darkened copy (cards on top)
       Z    zoomed B crop (w, x, y, speed)
       FC   still frame of B          FBL blurred still frame
       S    still frame of B panned (x0, x1)
       SPLIT two panels (B logo video, A dev video) on a dark background"""
import subprocess, sys, json, os
S = '/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad'
SRC = {'B': S + '/lol2/official.mp4', 'A': S + '/ocak/sezon2027.mp4'}
OUT = S + '/ocak/out'; os.makedirs(OUT, exist_ok=True)
D = 0.2
# scene cuts of each source, so no piece runs into the next shot
CUTS = {'B': [41.0, 43.9, 48.4, 59.79, 63.13, 66.08, 72.67, 75.17, 78.25, 81.21, 88.17, 94.46, 97.42, 98.71, 100.96, 102.58, 103.79, 105.17, 106.21, 107.38, 109.12, 109.92, 115.4, 121.5],
        'A': [4.46, 11.85, 14.64, 21.65, 29.32, 42.67, 48.17, 58.77, 68.90, 83.46, 86.29, 92.22, 95.64, 106.94, 118.78, 129.21, 134.76, 157.53, 163.96, 189.61, 191.78, 199.41, 201.03, 203.87, 205.46, 207.92, 214.55, 222.76, 326.7]}
O = 23.77            # body voice-over starts here
END = round(O + 252.93, 2)
# out a, out b, mode, source, src start, params, slide into this piece
INTRO = [
    (0.0, 3.5, 'BC', 'B', 44.4, (0, 0), None),        # rift at dawn: 2027
    (3.5, 4.7, 'BL', 'A', 97.0, (), 'L'),             # rank emblems drop to Iron IV
    (4.7, 5.65, 'B', 'B', 100.05, (), 'R'),           # new map
    (5.65, 6.95, 'A', 'A', 165.2, (), 'L'),           # items
    (6.95, 7.7, 'B', 'B', 97.95, (), 'R'),            # new champ select
    (7.7, 9.4, 'B', 'B', 98.76, (), None),            # Blitz pick, keeps playing
    (9.4, 13.6, 'SPLIT', 'B', 110.3, (4.6,), 'L'),    # two videos
    (13.6, 18.4, 'BL', 'A', 136.0, (), 'R'),          # chapter list
    (18.4, O, 'BC', 'B', 89.1, (.2,), 'L'),           # Ahri: the tip at the end
]
BODY = [  # body voice-over times (O is added)
    (0, 2.54, 'B', 'B', 110.3, (), 'R'),              # 1 YENI BASLANGIC
    (2.54, 6.96, 'BC', 'B', 55.3, (.05,), 'L'),
    (6.96, 9.34, 'BC', 'B', 63.3, (.05,), 'R'),
    (9.34, 11.1, 'B', 'B', 107.38, (), 'L'),          # Vayne
    (11.1, 12.9, 'Z', 'B', 107.9, (960, 300, 330, .6), 'R'),
    (12.9, 13.7, 'B', 'B', 97.95, (), 'L'),           # champ select
    (13.7, 14.18, 'B', 'B', 98.76, (), None),
    (14.18, 17.72, 'FC', 'B', 99.23, (), None),
    (17.72, 21.34, 'FBL', 'B', 99.23, (), 'R'),       # versions
    (21.34, 22.3, 'B', 'B', 100.05, (), 'L'),         # rift
    (22.3, 25.8, 'BC', 'B', 44.4, (0, 0), 'R'),
    (25.8, 28.32, 'S', 'B', 100.3, (0, 320), 'L'),
    (28.32, 29.92, 'B', 'B', 100.96, (), 'R'),        # Garen
    (29.92, 30.97, 'Z', 'B', 101.5, (1100, 300, 100, 1), 'L'),
    (30.97, 32.0, 'B', 'B', 101.5, (), 'R'),
    (32.0, 33.76, 'BC', 'B', 85.2, (.1,), 'L'),       # Jhin: sinematik
    (33.76, 34.96, 'B', 'B', 102.6, (), 'R'),         # Morgana
    (34.96, 36.62, 'Z', 'B', 102.6, (960, 520, 345, .6), 'L'),
    (36.62, 38.62, 'BC', 'B', 72.9, (.1,), 'R'),      # Poppy: modlar
    (38.62, 39.97, 'B', 'B', 103.8, (), 'L'),         # meteor
    (39.97, 41.16, 'Z', 'B', 103.8, (1000, 450, 250, 1), 'R'),
    (41.16, 42.06, 'B', 'B', 105.2, (), 'L'),         # minions, dragon pit, Baron
    (42.06, 43.2, 'B', 'B', 106.22, (), 'R'),
    (43.2, 44.44, 'Z', 'B', 109.15, (1920, 0, 0, .6), 'L'),
    (44.44, 48.14, 'FBL', 'B', 76.5, (), 'R'),        # client
    (48.14, 52.32, 'B', 'B', 117.1, (), 'L'),         # Ocak / 2027 card
    (52.32, 57.3, 'FBL', 'B', 61.5, (), 'R'),         # sign-up site
    (57.3, 60.08, 'B', 'B', 112.4, (), 'L'),          # logo, YENI BASLANGIC
    (60.08, 82.0, 'BL', 'A', 135.0, (), 'R'),         # 2 DERECELI
    (82.0, 99.18, 'BL', 'A', 164.0, (), 'L'),
    (99.18, 112.02, 'A', 'A', 69.0, (), 'R'),         # 3 RUNLER: Arakci
    (112.02, 117.9, 'A', 'A', 86.35, (), 'L'),        # Devdogan
    (117.9, 128.9, 'A', 'A', 95.7, (), 'R'),
    (128.9, 129.88, 'A', 'A', 88.0, (), 'L'),
    (129.88, 138.38, 'A', 'A', 135.0, (), 'R'),       # 4 ESYALAR
    (138.38, 156.06, 'A', 'A', 139.8, (), 'L'),
    (156.06, 170.38, 'A', 'A', 164.0, (), 'R'),       # Kader Vergisi
    (170.38, 179.96, 'A', 'A', 178.4, (), 'L'),       # Vadiyaran, Cançiçegi
    (179.96, 186.08, 'A', 'A', 191.85, (), 'R'),      # Yilan Disi
    (186.08, 188.9, 'A', 'A', 201.05, (), 'L'),       # Mezar Belasi
    (188.9, 190.4, 'A', 'A', 203.9, (), 'R'),
    (190.4, 192.8, 'A', 'A', 144.0, (), 'L'),
    (192.8, 194.1, 'A', 'A', 150.0, (), 'R'),
    (194.1, 200.6, 'A', 'A', 208.0, (), 'L'),         # 5 HARITA: Peri Isiklari
    (200.6, 210.16, 'BL', 'A', 136.0, (), 'R'),
    (210.16, 216.7, 'BC', 'B', 66.2, (.15,), 'L'),    # 6 ARAM
    (216.7, 219.68, 'BC', 'B', 72.75, (.15,), 'R'),
    (219.68, 222.62, 'BC', 'B', 75.25, (.15,), 'L'),
    (222.62, 225.5, 'BC', 'B', 78.3, (.15,), 'R'),
    (225.5, 228.82, 'BC', 'B', 81.3, (.15,), 'L'),
    (228.82, 232.22, 'BC', 'B', 84.6, (.15,), 'R'),
    (232.22, 243.78, 'BL', 'A', 69.0, (), 'L'),       # 7 SON: taktik
    (243.78, 247.92, 'A', 'A', 164.0, (), 'R'),
    (247.92, 252.93, 'B', 'B', 110.3, (), 'L'),
]
PLAN = INTRO + [(round(p[0] + O, 3), round(p[1] + O, 3)) + tuple(p[2:]) for p in BODY]
BLUR = 'gblur=sigma=22,eq=brightness=-0.1:saturation=1.15'

def lim(src, ss):
    return min(c for c in CUTS[src] if c > ss + 0.05) - ss - 0.03

def vf(p):
    a, b, m, src, ss, q, tr = p
    pre = f'trim=end={lim(src, ss):.3f},'
    still = 'trim=end_frame=1,tpad=stop_mode=clone:stop_duration=60,'
    sc = 'scale=1920:1080:flags=lanczos'
    if m == 'B': return pre + sc
    if m == 'BC': return pre + f'crop=1600:900:{q[1] if len(q) > 1 else 160}:0,{sc},eq=brightness=-{q[0]}'
    if m == 'A': return pre + f'crop=1102:620:89:0,{sc}'
    if m == 'BL': return pre + (f'crop=1102:620:89:0,{sc},' if src == 'A' else f'{sc},') + BLUR
    if m == 'Z':
        w, x, y, sp = q; h = round(w * 9 / 16)
        return pre + f'crop={w}:{h}:{x}:{y},{sc},setpts=PTS/{sp}'
    if m == 'FC': return still + sc
    if m == 'FBL': return still + 'crop=iw:900:0:0,' + sc + ',' + BLUR
    if m == 'S':
        x0, x1 = q; d = b - a + D
        return still + f"crop=1600:900:'{x0}+({x1}-{x0})*t/{d:.2f}':0,{sc},eq=brightness=-0.1"

def seglen(i):
    nxt = PLAN[i + 1] if i + 1 < len(PLAN) else None
    return PLAN[i][1] - PLAN[i][0] + (D if nxt and nxt[6] else 0)

def piece(i, p):
    o = f'{OUT}/v{i:02d}.mp4'; L = seglen(i)
    if p[2] == 'SPLIT':  # left: New Dawn logo video, right: dev video; both small panels, bg dark
        ssa = p[5][0]
        f = (f"color=c=0x0B0B0F:s=1920x1080:r=30:d={L:.3f}[bg];"
             f"[0:v]trim=end={lim('B', p[4]):.3f},scale=1920:1080,{BLUR},setpts=PTS-STARTPTS[bb];[bg][bb]overlay=shortest=1[b0];"
             f"[0:v]trim=end={lim('B', p[4]):.3f},crop=1320:742:300:120,scale=800:450,setpts=PTS-STARTPTS[l];"
             f"[1:v]trim=end={lim('A', ssa):.3f},crop=1102:620:89:0,scale=800:450,setpts=PTS-STARTPTS[r];"
             f"[b0][l]overlay=120:330[b1];[b1][r]overlay=1000:330,fps=30,tpad=stop_mode=clone:stop_duration=3,setsar=1,format=yuv420p[v]")
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(p[4]), '-i', SRC['B'], '-ss', str(ssa), '-i', SRC['A'], '-filter_complex', f, '-map', '[v]']
    else:
        f = f'[0:v]{vf(p)},setpts=PTS-STARTPTS,fps=30,tpad=stop_mode=clone:stop_duration=3,setsar=1,format=yuv420p[v]'
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(p[4]), '-i', SRC[p[3]], '-filter_complex', f, '-map', '[v]']
    subprocess.run(cmd + ['-frames:v', str(round(L * 30)), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', o], check=True)
    return o

def chain(vids, out):
    inp = []
    for v in vids: inp += ['-i', v]
    fc = [f'[{i}:v]fps=30,setpts=PTS-STARTPTS,settb=AVTB[i{i}]' for i in range(len(vids))]; cur = '[i0]'
    for i in range(1, len(vids)):
        tr = PLAN[i][6]; lab = f'[x{i}]'
        if tr: fc.append(f"{cur}[i{i}]xfade=transition={'slideleft' if tr == 'L' else 'slideright'}:duration={D}:offset={PLAN[i][0]:.3f}{lab}")
        else: fc.append(f'{cur}[i{i}]concat=n=2:v=1:a=0,settb=AVTB{lab}')
        cur = lab
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', cur, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', out], check=True)

def base():
    vids = []
    for i, p in enumerate(PLAN):
        vids.append(piece(i, p)); print('piece', i, flush=True)
    chain(vids, f'{OUT}/base.mp4')
    open('timeline.js', 'w').write('// generated by build.py\nconst PLAN=' + json.dumps([[p[0], p[1], p[2]] for p in PLAN]) + f';\nconst END={END},O={O};\n')
    print('base ok')

def mix():
    subprocess.run(['node', 'render.js', 'info'], check=True); ev = json.load(open('sfx.json'))
    G = {'impact': -15, 'stamp_dan': -10, 'yazi_vurus': -15, 'card': -17, 'pop': -19, 'click': -14}
    inp = ['-i', '../ses/giris.mp3', '-i', '../ses/govde.mp3', '-stream_loop', '-1', '-i', '../../sett/ses/muzik.mp3']
    fc = [f'[0]aresample=48000,aformat=channel_layouts=stereo[g];[1]aresample=48000,aformat=channel_layouts=stereo,adelay={int(O * 1000)}:all=1[b];'
          f'[g][b]amix=inputs=2:normalize=0:duration=longest,volume=4dB,apad=whole_dur={END},asplit[vo][sc]',
          f'[2]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{END},volume=-15dB,afade=t=in:d=0.3,afade=t=out:st={END - 1.5}:d=1.5[m0]',
          '[m0][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=400[m]']; lab = ['[vo]', '[m]']
    for i, (n, t, g) in enumerate(ev):
        inp += ['-i', f'../ses/{n}.wav']
        fc.append(f'[{i + 3}]aresample=48000,aformat=channel_layouts=stereo,volume={G[n] + g}dB,adelay={int(t * 1000)}:all=1[s{i}]'); lab.append(f'[s{i}]')
    fc.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0:duration=first,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', f'{OUT}/mix.wav'], check=True)
    print('mix ok')

if __name__ == '__main__':
    {'base': base, 'mix': mix}[sys.argv[1]]()
