# film segments -> jpg frames at 30 fps (native 640x480 is kept; scaling happens per frame in the renderer)
import subprocess, os, json
SEG = {'adm_d': ('admiral', 9.75, 2.65), 'adm_c': ('admiral', 14.75, 6.55), 'adm_p': ('admiral', 23.9, 3.45), 'adm_s': ('admiral', 28.95, 8.6),
       'fr_sp': ('freed1956', 3.7, 6.05), 'fr_a': ('freed1956', 29.5, 8.0), 'fr_rel': ('freed1956', 55.0, 6.0), 'nu': ('nuremberg', 198.5, 51.0)}
for k, (f, a, d) in SEG.items():
    os.makedirs('clip/' + k, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', str(d), '-i', f'drive/{f}.mp4', '-vf', 'fps=30', '-q:v', '2', f'clip/{k}/%05d.jpg'], check=True)
    print(k, len(os.listdir('clip/' + k)))
