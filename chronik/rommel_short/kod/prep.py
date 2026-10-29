# film segments -> jpg frames at 25 fps, 1280 wide. v1: German newsreel (4:3, black frame edges), v2: colourised compilation (channel logo top right, supers)
import subprocess, os
SEG = {'storch': ('v1', 19.2, 4.6), 'meet': ('v1', 35.2, 8.5), 'map1': ('v1', 71.0, 6.0), 'walk': ('v1', 85.0, 4.8), 'pris': ('v1', 202.0, 8.0), 'pris2': ('v1', 226.0, 8.0),
       'car': ('v1', 266.0, 5.5), 'car2': ('v1', 276.0, 3.8), 'tank1': ('v1', 350.0, 9.0), 'dust': ('v1', 362.0, 10.0), 'gun': ('v1', 190.0, 5.0),
       'port': ('v2', 10.5, 9.0), 'crane': ('v2', 24.0, 10.0), 'rom1': ('v2', 47.2, 7.5), 'rom2': ('v2', 55.0, 5.5), 'cam': ('v2', 63.6, 2.3),
       'rom3': ('v2', 82.0, 5.0), 'tankc': ('v2', 90.0, 2.0), 'sal': ('v2', 113.5, 6.0), 'goggle': ('v2', 189.0, 4.6), 'stand': ('v2', 194.2, 3.6),
       'arty': ('v2', 284.0, 3.0), 'road': ('v2', 287.0, 3.0), 'cars': ('v2', 297.0, 9.0), 'jeep': ('v2', 307.0, 8.0)}
for k, (f, a, d) in SEG.items():
    os.makedirs('clip/' + k, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', str(d), '-i', f'drive/{f}.mp4', '-vf', 'fps=25,scale=1280:-2', '-q:v', '4', f'clip/{k}/%05d.jpg'], check=True)
    print(k, len(os.listdir('clip/' + k)))
