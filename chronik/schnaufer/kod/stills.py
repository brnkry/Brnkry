import subprocess, numpy as np, os
from PIL import Image
J = {'brillanten': (3,6,9,13,16,19,20,21,22.5,25,27,29.5), 'nachtgespenst': (48,212,246,266,272),
     'nightriders': (270,300,540,840,930,1080,1110,1170,1560,1590,1650,1860,2040,2130,2250,2280,2670,2730,2760,2820,2850,2880),
     'raf43': (64,80,96), 'lanc_news': (192,200,208,216), 'target_berlin': (432,464,472,608,624,736,808,920,1000)}
CUT = {'lanc_news': (0, 0.09), 'target_berlin': (0, 0.09), 'nightriders': (0.0, 0.0)}
for k, ts in J.items():
    for t in ts:
        o = 'fotos/%s_%s.png' % (k, str(t).replace('.', '_'))
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i','dl/%s.mp4' % k,'-frames:v','1',o])
        im = np.asarray(Image.open(o).convert('RGB')).astype(np.float32); h, w = im.shape[:2]
        top, bot = CUT.get(k, (0, 0)); im = im[int(h*top):h-int(h*bot)]
        m = im.mean(2); cols = np.where(m.mean(0) > 18)[0]; rows = np.where(m.mean(1) > 18)[0]
        if len(cols) and len(rows): im = im[rows[0]:rows[-1]+1, cols[0]:cols[-1]+1]
        Image.fromarray(im.astype(np.uint8)).save(o.replace('.png', '.jpg'), quality=95); os.remove(o)
print(len(os.listdir('fotos')))
