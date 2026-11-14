# Teil 4 archive film cuts (grey jpg frames at 30 fps, lcore.clip_frame format), chosen from contact sheets
import os, subprocess
D = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t4/dl/'
O = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t4l/clips/'
CR = 'crop=iw*0.96:ih*0.95:iw*0.02:ih*0.02'                 # worn frame edge of the newsreel scans
CB = 'crop=iw*0.78:ih*0.74:iw*0.03:ih*0.06'                 # DW 522: BA logo top right, French subtitles at the bottom
CP = 'crop=iw*0.70:ih*0.84:iw*0.15:ih*0.04'                 # Periscope scan: pillarbox and burnt-in timecode at the bottom
CW = 'crop=iw*0.94:ih*0.92:iw*0.03:ih*0.04'
CUT = {'bombers2': ('dw520.mp4', 1335, 14, CR), 'crash': ('dw524.mp4', 776, 10, CR), 'london_air': ('dw524.mp4', 975, 16, CR),
       'he111_start': ('dw524.mp4', 1125, 14, CR), 'night_raid': ('dw524.mp4', 1218, 22, CR), 'bf109_start': ('dw524.mp4', 667.5, 3.5, CR),
       'stuka_att': ('dw522.mp4', 800, 9, CB), 'convoy_bombs': ('wwf4_battle_of_britain.mp4', 778, 2.8, CW), 'he111_below': ('wwf4_battle_of_britain.mp4', 862, 6, CW),
       'searchlights': ('london_can_take_it.mp4', 164, 20, CP), 'shelter': ('london_can_take_it.mp4', 206, 12, CP), 'morning': ('london_can_take_it.mp4', 350, 30, CP),
       'firehose': ('london_can_take_it.mp4', 462, 14, CP), 'balloons': ('london_can_take_it.mp4', 510, 8, CP)}
for k, (f, ss, d, cr) in CUT.items():
    o = O + k; os.makedirs(o, exist_ok=True)
    if len(os.listdir(o)) > 10: continue
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', D + f, '-t', str(d), '-vf', cr + ',scale=960:-2:flags=lanczos,fps=30,format=gray', '-q:v', '4', o + '/f%04d.jpg'], check=True)
    print(k, len(os.listdir(o)), flush=True)
