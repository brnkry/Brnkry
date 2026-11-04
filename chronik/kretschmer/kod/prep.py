# film segments -> jpg frames at 25 fps, cropped to a 3:4 window around cx and scaled to 1080 high (the 9:16 slice is taken later).
# mov is a screen recording with repeated frames: only changed frames are kept and played back at 25 fps.
import subprocess, os, sys, numpy as np
from PIL import Image
SEG = {'kclose': ('mov', 2.22, 1.83, 0.30, 1), 'bow': ('epic', 13.4, 4.9, 0.5, 0), 'peri': ('epic', 121.02, 1.97, 0.55, 0), 'cross': ('ww2p2', 25.12, 2.06, 0.55, 0),
       'flash': ('epic', 189.25, 2.9, 0.5, 0), 'radio': ('epic', 134.25, 2.8, 0.55, 0), 'sc7': ('epic', 197.02, 6.76, 0.5, 0), 'smoke': ('epic', 105.85, 6.2, 0.55, 0),
       'seaburn': ('epic', 221.85, 4.0, 0.5, 0), 'surface': ('epic', 177.55, 3.2, 0.5, 0), 'dive': ('epic', 18.45, 3.3, 0.5, 0), 'nightbg': ('epic', 140.15, 6.5, 0.5, 0),
       'tallybg': ('epic', 27.05, 5.0, 0.5, 0), 'dcbg': ('epic', 54.95, 4.2, 0.5, 0), 'interview': ('otto720', 26.0, 6.0, 0.5, 0), 'mapbg': ('epic', 151.55, 5.1, 0.5, 0), 'mapbg2': ('epic', 156.75, 2.0, 0.5, 0), 'yearsbg': ('epic', 44.25, 3.7, 0.5, 0), 'canbg': ('epic', 156.75, 13.0, 0.5, 0), 'letbg': ('epic', 72.15, 3.7, 0.5, 0), 'trapbg': ('epic', 85.85, 6.0, 0.5, 0)}
SRC = {'mov': (3214, 1716), 'epic': (1920, 1080), 'ww2p2': (640, 360), 'otto720': (1280, 720)}
EXT = {'mov': 'mov'}
only = sys.argv[1:]
for k, (v, a, d, cx, dedup) in SEG.items():
    if only and k not in only: continue
    sw, sh = SRC[v]; cw = int(sh * 0.75) // 2 * 2; x0 = int(min(max(cx * sw - cw / 2, 0), sw - cw))
    os.makedirs('clip/' + k, exist_ok=True)
    for f in os.listdir('clip/' + k): os.remove('clip/' + k + '/' + f)
    vf = f'crop={cw}:{sh}:{x0}:0,scale=-2:1080' + ('' if dedup else ',fps=25')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', str(d), '-i', f'drive/v_{v}.{EXT.get(v, "mp4")}', '-vf', vf, '-q:v', '3', f'clip/{k}/%05d.jpg'], check=True)
    if dedup:
        fs = sorted(os.listdir('clip/' + k)); keep = []; prev = None
        for f in fs:
            g = np.asarray(Image.open('clip/%s/%s' % (k, f)).convert('L').resize((96, 128)), np.float32)
            if prev is None or np.abs(g - prev).mean() > 0.6: keep.append(f); prev = g
        for f in fs:
            if f not in keep: os.remove('clip/%s/%s' % (k, f))
        for i, f in enumerate(keep): os.rename('clip/%s/%s' % (k, f), 'clip/%s/%05d.jpg' % (k, i + 1))
    print(k, len(os.listdir('clip/' + k)))
