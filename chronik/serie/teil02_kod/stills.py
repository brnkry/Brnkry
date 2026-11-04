# Teil 2 (Polen): stills out of the archive films for the magazine pages (black borders trimmed, burnt-in timecode cut off)
import subprocess, numpy as np, os, sys
from PIL import Image
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
CUT = {'siege': 0.09, 'castle': 0.09}   # Periscope timecode strip at the bottom
def grab(k, ts, top=0.0):
    for t in ts:
        o = E + 'st/%s_%s.jpg' % (k, str(t).replace('.', '_'))
        if os.path.exists(o): continue
        r = subprocess.run(['nice', '-n', '19', 'ffmpeg', '-v', 'error', '-ss', str(t), '-i', E + 'dl/%s.mp4' % k, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
        if not r: continue
        im = Image.open(__import__('io').BytesIO(r)).convert('RGB'); a = np.asarray(im).astype(np.float32); m = a.mean(2)
        cols = np.where(m.mean(0) > 16)[0]; rows = np.where(m.mean(1) > 16)[0]
        if len(cols) and len(rows): a = a[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
        h = a.shape[0]; a = a[int(h * top):h - int(h * CUT.get(k, 0))]
        Image.fromarray(a.astype(np.uint8)).save(o, quality=94)
J = {'siege': [56, 63, 70, 84, 91, 98, 112, 119, 133, 147, 154, 168, 175, 182, 189, 203, 210, 224, 266, 287, 301, 322, 336, 350, 357, 378, 392, 406, 420, 448, 476, 490, 497, 518, 532, 553, 567, 574],
     'castle': [21, 35, 42, 77, 105, 126, 133, 205, 245, 252, 266, 294, 308, 315, 340, 357, 375, 383, 424, 432, 446, 464, 476, 486, 530, 539, 546, 576, 588],
     'color': [10, 14, 22, 30, 36, 42, 60, 66, 70, 76, 84, 96, 108, 120, 128, 132, 160, 164, 184, 188, 192, 200, 204, 208, 224, 236, 240, 244, 252, 260],
     'redarmy': [5, 9, 17, 21, 25, 41, 49]}
for k, ts in J.items(): grab(k, ts)
print(len(os.listdir(E + 'st')))
