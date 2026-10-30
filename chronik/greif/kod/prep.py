# film segments -> jpg frames at 25 fps, full source resolution, cropped to a 3:4 window around cx (the 9:16 slice is taken later); amer720 has a small archive watermark that is removed (delogo)
import subprocess, os, sys
SEG = {'hook': ('doku', 68.6, 6.8, 0.44), 'road': ('doku', 41.5, 4.9, 0.6), 'muss': ('doku', 61.5, 3.7, 0.58), 'gbg': ('doku', 144.0, 3.0, 0.5), 'ardmap': ('dw2', 33.0, 3.8, 0.5),
       'aim': ('amer720', 15.7, 3.4, 0.45), 'march': ('doku', 3.0, 4.2, 0.5), 'convoy': ('amer720', 30.2, 3.2, 0.5), 'roadbg': ('snow', 7.3, 3.0, 0.5), 'sherman': ('snow', 11.85, 2.8, 0.45),
       'barrage': ('dw2', 39.66, 2.9, 0.5), 'jeep': ('amer720', 22.0, 3.9, 0.6), 'sign': ('snow', 60.40, 1.8, 0.45), 'pole': ('dw2', 136.40, 2.2, 0.72),
       'column': ('snow', 82.15, 3.2, 0.4), 'rumor': ('action', 54.0, 5.4, 0.5), 'post': ('amer720', 49.9, 4.2, 0.55), 'gis': ('doku', 208.8, 4.0, 0.5),
       'paris': ('action', 0.0, 6.0, 0.5), 'ikefilm': ('action', 193.0, 2.6, 0.45), 'ayw': ('snow', 62.3, 3.4, 0.55), 'pw': ('snow', 34.42, 2.0, 0.66),
       'court': ('interrog', 20.0, 3.3, 0.5), 'skint': ('interrog', 300.0, 4.6, 0.47), 'mug': ('doku', 431.0, 2.6, 0.55)}
SRC = {'doku': (1920, 1080), 'dw2': (1920, 1080), 'amer720': (1280, 720), 'snow': (1920, 1080), 'action': (1920, 1080), 'interrog': (1920, 1080)}
only = sys.argv[1:]
for k, (v, a, d, cx) in SEG.items():
    if only and k not in only: continue
    sw, sh = SRC[v]; cw = int(sh * 0.75) // 2 * 2; x0 = int(min(max(cx * sw - cw / 2, 0), sw - cw))
    vf = ('delogo=x=543:y=603:w=200:h=28,' if v == 'amer720' else '') + f'fps=25,crop={cw}:{sh}:{x0}:0'
    os.makedirs('clip/' + k, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', str(d), '-i', f'drive/v_{v}.mp4', '-vf', vf, '-q:v', '3', f'clip/{k}/%05d.jpg'], check=True)
    print(k, len(os.listdir('clip/' + k)))
