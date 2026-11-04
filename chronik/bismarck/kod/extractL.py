# landscape cuts for the style-A table (prints show the film playing), 25 fps, max 1000 px wide;
# crop boxes keep channel names out ("HF" top left in 00, "Battles Campaigns Commanders" top right in 08, "@Archives_Reloaded" and the logo in 01, AP, Pathé)
import os, subprocess, sys, glob
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
def f(n): return glob.glob(E + 'drive/%s_*' % n)[0]
C00 = (560, 0, 2880, 2160); C08 = (240, 130, 1320, 950); C02 = (150, 0, 1620, 1080); C12 = (480, 140, 2880, 2020)
CUT = {'dist': ('02', 66.0, 7.5, C02), 'esc': ('00', 12.0, 9.0, C00), 'fire1': ('00', 80.3, 5.4, C00), 'flash': ('00', 63.0, 5.5, C00),
       'smk': ('00', 136.0, 6.0, C00), 'bow': ('00', 30.0, 9.5, C00), 'hor': ('00', 112.0, 8.0, (960, 0, 2880, 2160)),
       'plot': ('08', 69.3, 5.6, C08), 'sword': ('08', 84.0, 7.9, C08), 'torp': ('08', 92.0, 7.9, C08), 'fleet': ('08', 103.0, 10.5, C08),
       'surv': ('08', 121.5, 8.5, C08), 'hood': ('08', 24.9, 3.0, C08), 'scut': ('02', 147.0, 9.0, C02), 'splash': ('02', 162.2, 6.5, C02),
       'wreck': ('12', 9.0, 12.0, C12), 'wreck2': ('12', 25.0, 12.0, C12), 'side': ('01', 71.0, 2.9, (880, 40, 1040, 700)),
       'sw': ('04', 75.5, 4.0, (80, 60, 400, 300)), 'kgv': ('07', 4.0, 8.0, (0, 110, 640, 370)), 'rod': ('10', 3.0, 8.0, (0, 0, 540, 480))}
if __name__ == '__main__':
    for k, (n, ss, d, (x, y, w, h)) in CUT.items():
        if sys.argv[1:] and k not in sys.argv[1:]: continue
        o = E + 'clipL/' + k; os.makedirs(o, exist_ok=True)
        if len(os.listdir(o)) > 10: continue
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', f(n), '-t', str(d), '-vf', "crop=%d:%d:%d:%d,scale='min(1000,iw)':-2:flags=lanczos,fps=25" % (w, h, x, y), '-q:v', '3', o + '/%05d.jpg'], check=True)
        print(k, len(os.listdir(o)), flush=True)
