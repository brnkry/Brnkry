# Schnaufer short: film cuts for the style-A table prints (25 fps, landscape) and the 9:16 hook background (30 fps)
import os, subprocess
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
D = E + 'dl/'
CUT = {'ws744': (D + 'ws744.mkv', 160.5, 29.0, 'crop=690:500:16:14'),          # Schnaufer receives the Diamonds (DW 744)
       'flak': (D + 'raf43.mp4', 76.0, 18.0, 'crop=620:350:10:5'),           # night raid: searchlights, flak
       'bomber': (D + 'target_berlin.mp4', 604.0, 30.0, 'crop=470:316:81:0'), # RAF bomber in flight (timecode below cut off)
       'lanc': (D + 'lanc_news.mp4', 190.0, 30.0, 'crop=630:378:112:0')}      # Lancasters in flight
for k, (f, ss, d, cr) in CUT.items():
    o = E + 'clipL/' + k; os.makedirs(o, exist_ok=True)
    if len(os.listdir(o)) > 10: continue
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', f, '-t', str(d), '-vf', cr + ",scale=1000:-2:flags=lanczos,fps=25", '-q:v', '3', o + '/%05d.jpg'], check=True)
    print(k, len(os.listdir(o)), flush=True)
o = E + 'clip/hook'; os.makedirs(o, exist_ok=True)
if len(os.listdir(o)) < 10:   # Lancasters above the clouds (lanc_news 202-216 s), a slow 9:16 pan from left to right
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '202', '-i', D + 'lanc_news.mp4', '-t', '14', '-vf', "crop=630:378:112:0,hqdn3d=3:3:6:6,scale=1214:728:flags=lanczos,crop=410:728:'402*t/14':0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,fps=30", '-q:v', '3', o + '/%05d.jpg'], check=True)
    print('hook', len(os.listdir(o)))
