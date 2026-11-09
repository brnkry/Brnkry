# Teil 3 archive film cuts (grey jpg frames at 30 fps, lcore.clip_frame format), chosen from contact sheets (scratchpad t3/idx)
import os, subprocess
D = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t3/dl/'
O = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t3l/clips/'
CR = 'crop=iw*0.96:ih*0.95:iw*0.02:ih*0.02'                 # worn frame edge of the UfA scans
CY = 'crop=iw*0.74:ih*0.90:iw*0.13:ih*0.03'                 # YouTube 16:9 uploads of 4:3 newsreels (pillarbox, subtitles at the bottom)
CP = 'crop=iw*0.80:ih*0.80:iw*0.10:ih*0.03'                 # Periscope scans: pillarbox and burnt-in timecode at the bottom
CD = 'crop=iw*0.94:ih*0.92:iw*0.03:ih*0.02'                 # Why We Fight scan
CUT = {'westfront': ('u492.mkv', 600, 15, CR), 'trench': ('u497.mkv', 800, 12, CR), 'artillery': ('u497.mkv', 900, 10, CR),
       'harbour_no': ('u504.mkv', 352, 12, CR), 'oscarsborg': ('u504.mkv', 840, 14, CR), 'sea': ('u504.mkv', 880, 12, CR),
       'narvik': ('u508.mp4', 100, 18, CY), 'stuka': ('u508.mp4', 230, 12, CY),
       'paras': ('u507.mkv', 122.5, 12, CR), 'column': ('u507.mkv', 288, 15, CR), 'rotterdam': ('u507.mkv', 480, 15, CR),
       'crossing': ('u507.mkv', 880, 15, CR), 'tanks': ('u507.mkv', 960, 10, CR), 'pows': ('u507.mkv', 1010, 15, CR),
       'map_ardennes': ('dac.mp4', 2700, 15, CD), 'dunkirk': ('castle.mp4', 118, 16, CP), 'refugees': ('castle.mp4', 408, 12, CP),
       'paris': ('w511.mp4', 625, 15, CY), 'eiffel': ('w511.mp4', 576, 8, CY), 'wagon': ('compiegne.mp4', 118, 20, CP), 'delegation': ('compiegne.mp4', 40, 15, CP)}
for k, (f, ss, d, cr) in CUT.items():
    o = O + k; os.makedirs(o, exist_ok=True)
    if len(os.listdir(o)) > 10: continue
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', D + f, '-t', str(d), '-vf', cr + ',scale=960:-2:flags=lanczos,fps=30,format=gray', '-q:v', '4', o + '/f%04d.jpg'], check=True)
    print(k, len(os.listdir(o)), flush=True)
