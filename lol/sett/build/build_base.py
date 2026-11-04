"""Builds the 240 s base video (no overlays) from the original guide footage and Riot ability clips.
usage: python3 build_base.py SRC_DIR OUT_DIR
SRC_DIR must contain sett.mp4 and riot/ab_{P1,Q1,W1,E1,R1}.mp4
"""
import subprocess, sys, os
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
O = os.path.join(SRC, 'sett.mp4')
R = lambda k: os.path.join(SRC, 'riot', f'ab_{k}.mp4')
FPS = 30
# (vo_start, vo_end, [(file, in, out, blur_chat)])  file None = black (full graphic scene drawn by overlay)
SEG = [
    (0.00, 14.40, None),
    (14.40, 31.22, [(O, 14.2, 29.2, 0)]),
    (31.22, 40.40, [(O, 29.2, 39.3, 0)]),
    (40.40, 58.68, [(O, 39.3, 54.2, 0), (R('W1'), 2.0, 6.0, 0)]),
    (58.68, 67.90, [(O, 54.2, 64.4, 0)]),
    (67.90, 83.48, [(O, 65.0, 83.6, 0)]),
    (83.48, 98.26, [(O, 84.0, 95.7, 0), (R('Q1'), 1.0, 4.4, 0)]),
    (98.26, 144.72, None),
    (144.72, 187.66, [(O, 123.6, 162.5, 1)]),
    (187.66, 211.90, [(O, 162.5, 173.4, 1), (R('R1'), 0.0, 6.6, 0), (O, 173.4, 179.9, 1)]),
    (211.90, 240.00, [(R('E1'), 0.0, 6.6, 0), (R('Q1'), 0.0, 6.7, 0), (R('R1'), 0.0, 6.6, 0)]),
]
parts = []
for i, (a, b, src) in enumerate(SEG):
    dur = b - a
    out = os.path.join(OUT, f'seg{i:02d}.mp4')
    parts.append(out)
    if src is None:
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=black:s=1920x1080:r={FPS}:d={dur:.3f}']
    else:
        total = sum(o - s for _, s, o, _ in src)
        speed = total / dur
        inputs, fc, labels = [], [], []
        for j, (f, s, o, blur) in enumerate(src):
            inputs += ['-ss', f'{s:.3f}', '-t', f'{o - s:.3f}', '-i', f]
            chain = (f'[{j}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,'
                     f'fps={FPS},setpts=(PTS-STARTPTS)/{speed:.5f}')
            if blur:
                fc.append(chain + f'[w{j}];[w{j}]split[v{j}][c{j}];[c{j}]crop=440:280:30:550,boxblur=18:2[bl{j}];[v{j}][bl{j}]overlay=30:550[p{j}]')
            else:
                fc.append(chain + f'[p{j}]')
            labels.append(f'[p{j}]')
        fc.append(''.join(labels) + f'concat=n={len(src)}:v=1:a=0,trim=duration={dur:.3f},tpad=stop_mode=clone:stop_duration=1,trim=duration={dur:.3f}[out]')
        cmd = ['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[out]']
        print(f'seg{i:02d} speed {speed:.3f}')
    cmd += ['-frames:v', str(round(b * FPS) - round(a * FPS)), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(FPS), out]
    subprocess.run(cmd, check=True)
with open(os.path.join(OUT, 'list.txt'), 'w') as f:
    f.writelines(f"file '{p}'\n" for p in parts)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(OUT, 'list.txt'), '-c', 'copy', os.path.join(OUT, 'base.mp4')], check=True)
print('done')
