# film segments -> jpg frames at 30 fps, 1280 wide (archive films are soft anyway; panels are 1000 px)
import subprocess, os, glob
KU = glob.glob('drive/Battle_of_Kursk*.mp4')[0]; TI = glob.glob('drive/Rare_WW2*.mp4')[0]
R1 = 'drive/Ekran_Kayd__2026-10-29_17.05.13.mov'; R2 = 'drive/Ekran_Kayd__2026-10-29_17.11.02.mov'
SEG = {'ku_sol': (KU, 95.5, 8.7), 'ku_burn': (KU, 425.5, 15.1), 'ku_t34': (KU, 488.2, 5.4), 'ku_col': (KU, 775.6, 5.1), 'ku_tig': (KU, 788.1, 10.9), 'ku_grp': (KU, 708.3, 4.1),
       'ti': (TI, 0.0, 18.7), 'kt': (R1, 0.0, 13.9), 'dig': (R2, 0.0, 27.0)}
for k, (f, a, d) in SEG.items():
    os.makedirs('clip/' + k, exist_ok=True)
    vf = 'fps=30,scale=1280:-2' if k != 'dig' else 'fps=30,scale=1600:-2'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', str(d), '-i', f, '-vf', vf, '-q:v', '3', f'clip/{k}/%05d.jpg'], check=True)
    print(k, len(os.listdir('clip/' + k)))
