# archive clips for the long version: cut, cropped clear of watermarks / burned-in text, grey, 30 fps jpg sequences in clips/<name>/
import subprocess, os, sys
S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
L, T = S + 'lang/drive/', S + 'teil1/drive/'
CLIPS = {   # name: (source, start, dur, crop w:h:x:y)
 'tanks':   (L + 'video1234.mp4', 0.3, 7.6, '470:264:86:46'),
 'pcrowd':  (L + 'video1234.mp4', 7.8, 2.8, '470:264:86:46'),
 'psquare': (L + 'video1234.mp4', 22.6, 3.6, '470:264:86:46'),
 'psoldier':(L + 'video1234.mp4', 13.8, 2.0, '470:264:86:46'),
 'ptroops': (L + 'video123.mp4', 14.0, 7.5, '320:180:100:38'),
 'pcrowd2': (L + 'video123.mp4', 20.2, 3.5, '320:180:100:38'),
 'street':  (T + '3.mp4', 0.0, 5.6, '533:300:53:0'),
 'crowd':   (T + '3.mp4', 6.0, 4.6, '533:300:53:0'),
 'hitler':  (T + '3.mp4', 112.0, 34.0, '533:300:53:0'),
 'ship1':   (T + '4.mp4', 8.6, 7.0, '482:271:0:15'),
 'captain': (T + '4.mp4', 16.0, 6.5, '482:271:0:15'),
 'ship2':   (T + '4.mp4', 39.6, 8.0, '482:271:0:15'),
 'fire':    (L + 'videooo.mp4', 0.0, 13.0, '470:264:86:46'),
 'ruins':   (L + 'videooo.mp4', 18.0, 9.0, '470:264:86:46'),
 'trial':   (L + 'videooo.mp4', 31.0, 6.0, '470:264:86:46'),
 'kroll':   (L + 'videooo.mp4', 57.0, 8.0, '470:264:86:46'),
 'union':   (L + 'videooo.mp4', 87.6, 4.8, '470:264:86:46'),
}
for n in (sys.argv[1:] or CLIPS):
    src, a, d, cr = CLIPS[n]; o = S + 'lang/clips/' + n; os.makedirs(o, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-i', src, '-t', str(d), '-vf', f'fps=30,crop={cr},format=gray', '-q:v', '2', o + '/f%04d.jpg'], check=True)
    print(n, len(os.listdir(o)))
