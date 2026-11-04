# Prien short: film cuts for the style-A table prints (25 fps, landscape) and the 9:16 hook background (30 fps)
import os, subprocess, sys
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
FF = E + 'dl/feindfahrt.mp4'; D534 = E + 'dl/dw534.mp4'; D549 = E + 'dl/dw549.mp4'
C4 = 'crop=1440:1080:240:0'      # the 4:3 picture inside the compilation (its corner logo sits outside)
CD = 'crop=iw*0.96:ih*0.96'       # trims the worn frame edge of the newsreel scans
CUT = {'sea': (D534, 56.0, 14.0, CD), 'launch': (D549, 108.0, 14.0, CD), 'peri': (D534, 156.0, 24.0, CD), 'peri2': (D534, 134.0, 16.0, CD),
       'dive': (D549, 140.0, 17.0, CD), 'arrive': (FF, 209.0, 8.5, C4), 'deck': (FF, 266.0, 15.0, C4), 'march': (FF, 292.0, 4.2, C4)}   # march is re-cut slowed to 0.6x with motion interpolation (see NOTIZEN)
for k, (f, ss, d, cr) in CUT.items():
    o = E + 'clipL/' + k; os.makedirs(o, exist_ok=True)
    if len(os.listdir(o)) > 10: continue
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', f, '-t', str(d), '-vf', cr + ",scale='min(1000,iw)':-2:flags=lanczos,fps=25", '-q:v', '3', o + '/%05d.jpg'], check=True)
    print(k, len(os.listdir(o)), flush=True)
o = E + 'clip/hook'; os.makedirs(o, exist_ok=True)
if len(os.listdir(o)) < 10:   # U-boat bow cutting through the sea, cut to 9:16
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '32', '-i', D534, '-t', '14', '-vf', 'crop=ih*9/16*0.96:ih*0.96,scale=1080:1920:flags=lanczos,fps=30', '-q:v', '3', o + '/%05d.jpg'], check=True)
    print('hook', len(os.listdir(o)))
