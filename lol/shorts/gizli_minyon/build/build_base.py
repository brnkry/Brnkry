"""Base video for the 'gizli minyon' Short. usage: python3 build_base.py SRC.mp4 OUT_DIR
1) crop+scale source to 1080x1920 (drops burned-in captions + watermark), inpaint burned-in overlays (clean.py)
2) cut segments in source time and retime them to the VO sections (seg.json)"""
import subprocess, sys, os, json
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, 'seg.json')))
clean = os.path.join(OUT, 'clean.mp4')
if not os.path.exists(clean):
    subprocess.run([sys.executable, '-I', os.path.join(HERE, 'clean.py'), SRC, clean], check=True)
parts = []
FPS = 30
for i, (a, b, s, e, mode) in enumerate(P['segs']):
    dur = b - a; nfr = round(b * FPS) - round(a * FPS)
    out = os.path.join(OUT, f'seg{i:02d}.mp4'); parts.append(out)
    if mode == 'freeze':
        vf = f"trim=start={s}:duration=0.05,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={dur+1},zoompan=z='1.0+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        cmd = ['ffmpeg', '-v', 'error', '-y', '-i', clean, '-vf', vf]
    else:
        sp = (e - s) / dur
        vf = f"trim=start={s}:end={e},setpts=(PTS-STARTPTS)/{sp:.5f},fps=30,tpad=stop_mode=clone:stop_duration=1"
        if mode == 'blur': vf += ',gblur=sigma=16,eq=brightness=-0.06'
        cmd = ['ffmpeg', '-v', 'error', '-y', '-i', clean, '-vf', vf]
        print(f'seg{i:02d} {a:.2f}-{b:.2f} speed {sp:.2f}')
    cmd += ['-frames:v', str(nfr), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '30', out]
    subprocess.run(cmd, check=True)
with open(os.path.join(OUT, 'list.txt'), 'w') as f:
    f.writelines(f"file '{p}'\n" for p in parts)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(OUT, 'list.txt'), '-c', 'copy', os.path.join(OUT, 'base.mp4')], check=True)
print('done')
