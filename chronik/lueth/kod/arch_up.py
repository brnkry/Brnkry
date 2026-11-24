# archive segments -> 9:16 center crop -> Real-ESRGAN x4 -> blend 65% with plain upscale -> 1080x1920 mp4 (source fps)
import subprocess, sys, os, numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/up')
from esr import up
L = os.path.dirname(os.path.abspath(__file__)) + '/'
V = {'d6': 'vid/n-anhang-u-boot-bericht-dw-686-video.mp4', 'd0': 'vid/n-anhang-u-boot-bericht-dw-690-video.mp4', 'nu': 'vid/n-anhang-grosser-empfang-fur-wolfgang-luth-in-neustadt-in-holstein-video.mp4'}
SEG = [('A1', 'd6', 2.0, 7.4, .55), ('A2', 'd0', 134.0, 6.7, .5), ('A3', 'd6', 113.5, 4.5, .45), ('A4', 'd6', 135.4, 4.7, .55),
       ('A5', 'd6', 10.0, 5.8, .5), ('A6', 'd6', 79.0, 4.5, .5), ('A7', 'nu', 23.0, 3.7, .55), ('A8', 'nu', 15.5, 7.0, .5), ('A9', 'd6', 14.0, 4.4, .5)]
for name, k, ss, dur, cx in SEG:
    out = L + 'arch/%s.mp4' % name
    if os.path.exists(out): continue
    f = L + V[k]
    w, h, fr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height,r_frame_rate', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip().split(',')
    w, h = int(w), int(h); cw = int(h * 9 / 16) // 2 * 2; x0 = int(min(max(cx * w - cw / 2, 0), w - cw))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-t', str(dur), '-i', f, '-vf', f'crop={cw}:{h}:{x0}:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    n = len(raw) // (cw * h * 3)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', fr, '-i', '-', '-c:v', 'libx264', '-crf', '15', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(n):
        im = Image.fromarray(np.frombuffer(raw[i * cw * h * 3:(i + 1) * cw * h * 3], np.uint8).reshape(h, cw, 3))
        e = up(im).resize((1080, 1920), Image.LANCZOS); b = im.resize((1080, 1920), Image.LANCZOS)
        p.stdin.write(Image.blend(b, e, 0.65).tobytes())
    p.stdin.close(); p.wait(); print(name, n, flush=True)
print('ARCH DONE', flush=True)
