"""Builds the 240 s Locke base video (no overlays).
usage: python3 build_base.py SRC_DIR OUT_DIR
SRC_DIR: rengar.mp4 (original guide), riot/ab_{P1,Q1,W1,E1,R1}.mp4, src/vsult.mp4, src/eyes_freeze.png
"""
import subprocess, sys, os, json
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
O = os.path.join(SRC, 'locke1080.mp4')
R = lambda k: os.path.join(SRC, 'riot', f'ab_{k}.mp4')
FPS = 30
T = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cues.json')))['T']
g = lambda k, i=0: T[k][i]
# blur flag: 0 none, 1 blur the chat box
SEG = [
    (0.0, g('hook2'), None),                                   # splash + hook text (HTML)
    (g('hook2'), g('why'), [(R('Q1'), 0.0, 8.5, 0)]),
    (g('why'), g('nanami'), [(R('P1'), 0.0, 11.8, 0)]),
    (g('nanami'), g('passive'), None),                         # Nanami joke + lore scenes (HTML)
    (g('passive'), g('q'), [(O, 14.2, 19.0, 0)]),
    (g('q'), g('w'), [(O, 19.0, 37.0, 0)]),
    (g('w'), g('e'), [(O, 37.0, 51.0, 0)]),
    (g('e'), g('r'), [(O, 51.0, 63.5, 0)]),
    (g('r'), g('combo'), [(O, 64.5, 76.5, 0), (R('R1'), 0.0, 10.6, 0)]),
    (g('combo'), g('match'), [(O, 86.0, 102.0, 0)]),
    (g('match'), g('early'), None),                            # matchups, build, roast (HTML)
    (g('early'), g('mid'), [(O, 133.2, 150.2, 1)]),
    (g('mid'), g('late'), [(O, 159.5, 167.0, 1)]),
    (g('late'), g('cta'), [(O, 167.1, 179.5, 1)]),
    (g('cta'), 240.0, [(R('W1'), 0.0, 9.2, 0), (R('E1'), 0.0, 9.8, 0)]),
]
parts = []
for i, (a, b, src) in enumerate(SEG):
    dur = b - a
    nfr = round(b * FPS) - round(a * FPS)
    out = os.path.join(OUT, f'seg{i:02d}.mp4')
    parts.append(out)
    if src is None:
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=black:s=1920x1080:r={FPS}:d={dur:.3f}']
    elif src[0][0] == 'IMG':
        # slow push-in on a still frame
        cmd = ['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', str(FPS), '-i', src[0][1], '-vf',
               f"scale=3840:2160,zoompan=z='1+0.06*on/{nfr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps={FPS}"]
    else:
        total = sum(o - s for _, s, o, _ in src)
        speed = total / dur
        inputs, fc, labels = [], [], []
        for j, (f, s, o, blur) in enumerate(src):
            inputs += ['-ss', f'{s:.3f}', '-t', f'{o - s:.3f}', '-i', f]
            chain = (f'[{j}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,'
                     f'fps={FPS},setpts=(PTS-STARTPTS)/{speed:.5f}')
            if blur == 3:
                fc.append(chain + f',crop=1280:720:440:200,scale=1920:1080,eq=brightness=-0.12:saturation=0.7,colorbalance=rs=0.35:gs=-0.15:bs=-0.15[p{j}]')
            elif blur == 4:
                fc.append(chain + f'[w{j}];[w{j}]split[v{j}][c{j}];[c{j}]crop=760:220:660:720,boxblur=16:2[bl{j}];[v{j}][bl{j}]overlay=660:720[p{j}]')
            elif blur == 2:
                fc.append(chain + f',gblur=sigma=7,eq=brightness=-0.05[p{j}]')
            elif blur:
                fc.append(chain + f'[w{j}];[w{j}]split[v{j}][c{j}];[c{j}]crop=440:280:30:550,boxblur=18:2[bl{j}];[v{j}][bl{j}]overlay=30:550[p{j}]')
            else:
                fc.append(chain + f'[p{j}]')
            labels.append(f'[p{j}]')
        fc.append(''.join(labels) + f'concat=n={len(src)}:v=1:a=0,trim=duration={dur:.3f},tpad=stop_mode=clone:stop_duration=1,trim=duration={dur:.3f}[out]')
        cmd = ['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[out]']
        print(f'seg{i:02d} speed {speed:.3f}')
    cmd += ['-frames:v', str(nfr), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(FPS), out]
    subprocess.run(cmd, check=True)
with open(os.path.join(OUT, 'list.txt'), 'w') as f:
    f.writelines(f"file '{p}'\n" for p in parts)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(OUT, 'list.txt'), '-c', 'copy', os.path.join(OUT, 'base.mp4')], check=True)
print('done')
