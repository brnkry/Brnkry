# film segments -> jpg frames at 25 fps. 'p' = panel clips (low-resolution sources, shown in a framed card, kept whole; the Laconia documentary loses its top strip with the channel bug),
# 'v' = full-frame clips (cropped to a 3:4 window around cx, 1080 high; the 9:16 slice is taken later)
import subprocess, os, sys
E = '../kret/drive/v_epic.mp4'; D = 'drive/v_laconia.mp4'; G = 'drive/v_gloire.mp4'; B24 = 'drive/v_b24.mp4'; W2 = '../kret/drive/v_ww2p2.mp4'
SEG = {'torp': (E, 203.82, 8.8, 'v', 0.5), 'esurf': (E, 180.8, 3.35, 'v', 0.5), 'radiobg': (E, 143.8, 7.68, 'v', 0.5),
       'ship': (D, 165.8, 2.7, 'p'), 'pax': (D, 171.08, 4.95, 'p'), 'women': (D, 1180.5, 9.5, 'p'), 'side': (D, 373.6, 3.3, 'p'), 'water': (D, 376.96, 2.78, 'p'),
       'b24top': (D, 1278.2, 4.9, 'p'), 'uair': (D, 1283.16, 6.7, 'p'), 'boom': (D, 1289.96, 3.35, 'p'), 'tow': (D, 1299.56, 3.7, 'p'), 'crew': (D, 1026.0, 8.55, 'p'), 'sea': (D, 1590.5, 11.0, 'p'),
       'b24fly': (B24, 65.22, 2.18, 'p'), 'b24up': (B24, 67.95, 2.83, 'p'), 'gl1': (G, 0.0, 18.0, 'p'), 'gl2': (G, 37.04, 8.68, 'p'), 'wdive': (W2, 44.05, 3.4, 'p')}
only = sys.argv[1:]
for k, v in SEG.items():
    if only and k not in only: continue
    f, a, d, kind = v[:4]
    if kind == 'v':
        sw, sh = 1920, 1080; cw = int(sh * 0.75) // 2 * 2; x0 = int(min(max(v[4] * sw - cw / 2, 0), sw - cw)); vf = f'fps=25,crop={cw}:{sh}:{x0}:0'
    else:
        vf = 'fps=25,crop=390:256:0:30' if f == D else 'fps=25'
    os.makedirs('clip/' + k, exist_ok=True)
    for x in os.listdir('clip/' + k): os.remove('clip/%s/%s' % (k, x))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', str(d), '-i', f, '-vf', vf, '-q:v', '2', f'clip/{k}/%05d.jpg'], check=True)
    print(k, len(os.listdir('clip/' + k)))
