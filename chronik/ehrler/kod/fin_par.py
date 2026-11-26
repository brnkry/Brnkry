# parallel finish: the cut is split into chunks, every chunk runs the same finish on the global timeline, then concat + mix
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import *
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
sub = OUT + 'subs.ass'; ass(sub)
labs = []
for j, (ph, big, small) in enumerate(LAB):
    t0 = K(ph) + 0.4; fn = OUT + 'lab%02d.png' % j; label_png(big, small, fn); labs.append((t0, fn))
L4 = TOTAL / 4
SEG = [(q * L4 / 4, L4 / 4, f'fin_00{chr(97 + q)}') for q in range(4)] + [(L4, L4, 'fin_01')] + [(2 * L4 + q * L4 / 4, L4 / 4, f'fin_02{chr(97 + q)}') for q in range(4)] + [(3 * L4 + q * (TOTAL - 3 * L4) / 4, (TOTAL - 3 * L4) / 4, f'fin_03{chr(97 + q)}') for q in range(4)]
procs = []
for S, d, name in SEG:
    out = OUT + name + '.mp4'
    if os.path.exists(out): continue
    fc = (f"[0:v]setpts=PTS+{S:.3f}/TB,eq=contrast=0.96:saturation=0.82:gamma_r=1.03:gamma_b=0.95,"
          "eq=brightness='0.008*sin(t*13.1)+0.006*sin(t*29.7)':eval=frame,noise=alls=6:allf=t,vignette=PI/4.8[n]")
    lab_in, prev, j2 = [], '[n]', 0
    for t0, fn in labs:
        if t0 + 6.4 < S or t0 > S + d: continue
        lab_in += ['-loop', '1', '-t', '6.4', '-itsoffset', f'{t0:.2f}', '-i', fn]
        fc += f";[{j2 + 1}:v]format=rgba,fade=in:st={t0:.2f}:d=0.6:alpha=1,fade=out:st={t0 + 5.6:.2f}:d=0.6:alpha=1[l{j2}];{prev}[l{j2}]overlay=0:0:eof_action=pass[o{j2}]"; prev = f'[o{j2}]'; j2 += 1
    fc += f";{prev}subtitles={sub},fade=t=out:st={TOTAL - 2.0:.2f}:d=2.0,setpts=PTS-STARTPTS[v]"
    procs.append(subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-ss', f'{S:.3f}', '-t', f'{d:.3f}', '-i', OUT + 'cut.mp4', *lab_in,
        '-filter_complex', fc, '-map', '[v]', '-frames:v', str(int(round(d * FPS))), '-r', str(FPS), '-c:v', 'libx264', '-b:v', '6000k', '-maxrate', '8000k', '-bufsize', '16000k',
        '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out]))
for p in procs: p.wait()
print('chunks', [p.returncode for p in procs], flush=True)
open(OUT + 'list.txt', 'w').write(''.join(f"file '{OUT}{name}.mp4'\n" for _, _, name in SEG))
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', OUT + 'list.txt', '-i', OUT + 'mix.m4a', '-map', '0:v', '-map', '1:a', '-c', 'copy',
     '-t', f'{TOTAL:.3f}', '-movflags', '+faststart', E + 'Heinrich_Ehrler_lang_v1.mp4'])
print('DONE', flush=True)
