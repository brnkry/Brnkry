# cut the chosen segments of the Drive clips into 30 fps JPEG frames: full-screen 9:16 crops (placed to keep channel logos out),
# and the low-resolution clips cropped clear of their logos for use as prints on the table
import os, subprocess, sys, glob
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
def f(n): return glob.glob(E + 'drive/%s_*' % n)[0]
FULL = {'hook': ('02', 91.5, 8.0, .5), 's1941': ('02', 66.0, 6.5, .5), 'dk': ('00', 80.3, 5.6, .58), 'fire': ('00', 63.0, 6.0, .5),
        'smoke': ('00', 136.0, 6.0, .56), 'leak': ('01', 84.4, 9.5, .87), 'plot': ('08', 69.3, 5.6, .5), 'sword': ('08', 84.0, 7.9, .5),
        'torp': ('08', 92.0, 7.9, .5), 'circ': ('00', 112.0, 6.0, .66), 'fleet': ('08', 104.0, 6.9, .48), 'hit': ('02', 162.2, 7.0, .6),
        'scut': ('02', 147.0, 9.0, .5), 'surv': ('08', 121.5, 8.5, .5), 'wreck': ('12', 9.0, 12.0, .5)}
PRT = {'sw': ('04', 75.5, 4.0, (80, 60, 480, 300)), 'hood': ('08', 24.9, 2.6, (240, 130, 1440, 950)), 'kgv': ('07', 4.0, 8.0, (0, 110, 640, 370)),
       'rod': ('10', 3.0, 8.0, (0, 0, 540, 480))}
def run(k, n, ss, d, vf):
    o = E + 'clip/' + k; os.makedirs(o, exist_ok=True)
    if len(os.listdir(o)) > 10: return
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', f(n), '-t', str(d), '-vf', vf + ',fps=30', '-q:v', '3', o + '/%05d.jpg'], check=True)
    print(k, len(os.listdir(o)), flush=True)
for k, (n, ss, d, c) in FULL.items():
    if sys.argv[1:] and k not in sys.argv[1:]: continue
    vf = "crop=trunc(ih*9/16/2)*2:ih:trunc((iw*%.3f-ih*9/32)/2)*2:0,scale='min(1080,iw)':-2:flags=lanczos" % c
    if k == 'wreck': vf = 'crop=1148:2040:1346:120,scale=1080:1920:flags=lanczos'   # a faint channel name runs along the top edge
    run(k, n, ss, d, vf)
for k, (n, ss, d, (x, y, w, h)) in PRT.items():
    if sys.argv[1:] and k not in sys.argv[1:]: continue
    run(k, n, ss, d, 'crop=%d:%d:%d:%d' % (w, h, x, y))
