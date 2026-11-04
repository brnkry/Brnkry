# Teil 2 archive film cuts (grey jpg frames at 30 fps, lcore.clip_frame format), chosen from contact sheets
import os, subprocess
D = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t2/dl/'
O = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t2l/clips/'
CR = 'crop=iw*0.96:ih*0.95:iw*0.02:ih*0.02'                 # worn frame edge of the UfA scans
CC = 'crop=iw*0.86:ih*0.86:iw*0.12:ih*0.12'                 # colour film: its channel logo sits top left
CP = 'crop=iw*0.80:ih*0.80:iw*0.10:ih*0.03'                 # Periscope scans: pillarbox and burnt-in timecode at the bottom
CUT = {'tanks': ('color.mp4', 33, 8, CC), 'stuka': ('color.mp4', 77.5, 5, CC), 'barrier': ('ufa470.mkv', 580, 20, CR),
       'moto': ('ufa470.mkv', 600, 12, CR), 'panzer': ('ufa470.mkv', 643, 17, CR), 'ship': ('ufa470.mkv', 940, 35, CR),
       'ship2': ('ufa473.mkv', 834, 14, CR), 'bridges': ('ufa471.mkv', 323, 47, CR), 'pontoon': ('ufa471.mkv', 371, 21, CR),
       'pows': ('ufa471.mkv', 670, 20, CR), 'smoke': ('ufa473.mkv', 849, 10, CR), 'officers': ('ufa473.mkv', 680, 28, CR),
       'brest': ('brest.mp4', 4, 40, 'crop=iw*0.98:ih*0.80:iw*0.01:0'), 'ribbentrop': ('ufa474.mkv', 76, 9.5, CR),
       'wruins': ('siege.mp4', 130, 28, CP), 'wfire': ('siege.mp4', 290, 37, CP), 'hosp': ('siege.mp4', 400, 47, CP)}
for k, (f, ss, d, cr) in CUT.items():
    o = O + k; os.makedirs(o, exist_ok=True)
    if len(os.listdir(o)) > 10: continue
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', D + f, '-t', str(d), '-vf', cr + ',scale=960:-2:flags=lanczos,fps=30,format=gray', '-q:v', '4', o + '/f%04d.jpg'], check=True)
    print(k, len(os.listdir(o)), flush=True)
