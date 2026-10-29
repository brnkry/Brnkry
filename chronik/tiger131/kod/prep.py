# film segments -> jpg frames at the source's own 25 fps (no repeated frames); the old footage is already 9:16
import subprocess, os, glob
O = 'drive/tiger_131_old_footage.mp4'; N = glob.glob('drive/Tiger_Tank_131_Still*.mp4')[0]; M = glob.glob('drive/___Tiger*.mp4')[0]
SEG = {'o_dust': (O, 36.5, 6.85), 'o_field': (O, 99.7, 9.0), 'o_smoke': (O, 55.45, 6.7), 'o_grass': (O, 122.15, 2.85), 'o_sil': (O, 49.05, 6.3), 'o_land': (O, 63.7, 6.7), 'o_tunis': (O, 110.85, 3.0),
       'o_deck': (O, 45.25, 3.7), 'o_mov': (O, 90.8, 8.7), 'o_work': (O, 165.45, 4.0), 'o_flat': (O, 154.85, 6.4),
       'm_close': (M, 99.0, 9.0), 'm_rain': (M, 2.0, 8.0), 'n_a': (N, 58.0, 6.0), 'n_b': (N, 118.0, 9.0)}
for k, (f, a, d) in SEG.items():
    os.makedirs('clip/' + k, exist_ok=True)
    vf = 'fps=25' if k.startswith('o_') else 'fps=25,scale=1440:-2'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', str(d), '-i', f, '-vf', vf, '-q:v', '4', f'clip/{k}/%05d.jpg'], check=True)
    print(k, len(os.listdir('clip/' + k)))
