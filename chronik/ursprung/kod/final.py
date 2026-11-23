# Final assembly of "Der wahre Ursprung des Zweiten Weltkriegs": the 10 part cuts joined with 1.2 s crossfades,
# one old-film finish over the whole film, one subtitle track and the labels on a single timeline,
# all narration placed on that timeline, ONE continuous music bed (looped with long crossfades, ducked under the voice),
# one loudness normalisation for the whole film, so nothing jumps between the parts.
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Part, U, W, H, FPS, XF, OFF, ass, label_png, run
from shots import P
KEYS = ['t1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10']
F = U + 'final/'; os.makedirs(F, exist_ok=True)
parts = [Part(U + k) for k in KEYS]
S = []; t = 0.0
for p in parts: S.append(t); t += p.end - XF
TOTAL = S[-1] + parts[-1].end
print('total', round(TOTAL, 1), 'starts', [round(x, 1) for x in S], flush=True)
# ---- 1. picture: crossfade the part cuts ----
cut = F + 'cut_all.mp4'
if not os.path.exists(cut):
    inp, fl, prev = [], [], '[0:v]'
    for p in parts: inp += ['-i', p.d + 'cut.mp4']
    for i in range(1, len(parts)):
        o = f'[x{i}]'; fl.append(f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={S[i]:.3f}{o}'); prev = o
    run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', prev, '-t', f'{TOTAL:.3f}', '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', cut])
print('cut ok', flush=True)
# ---- 2. one subtitle track and the labels on the global timeline ----
WD = []
for p, s in zip(parts, S): WD += [[w, a + s, b + s] for w, a, b in p.wd]
ass(WD, F + 'subs.ass')
labs = []
for k, p, s in zip(KEYS, parts, S):
    for j, (ph, big, small) in enumerate(P[k][1]):
        fn = F + 'lab_%s_%02d.png' % (k, j); label_png(big, small, fn); labs.append((p.K(ph) + s, fn))
labs.sort()
# ---- 3. sound: narration on the timeline, one music bed, one loudness pass ----
voice = F + 'voice.wav'
if not os.path.exists(voice):
    inp, fl = [], []
    for i, p in enumerate(parts): inp += ['-i', p.voice]; fl.append(f'[{i}]adelay={int((S[i] + OFF) * 1000)}:all=1,aformat=sample_rates=48000:channel_layouts=stereo[a{i}]')
    fl.append(''.join(f'[a{i}]' for i in range(len(parts))) + f'amix=inputs={len(parts)}:normalize=0:duration=longest,apad,atrim=0:{TOTAL:.3f}[v]')
    run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', '[v]', '-c:a', 'pcm_s16le', voice])
music = F + 'music.wav'
if not os.path.exists(music):
    n = int(TOTAL // 560) + 2; inp = []
    for _ in range(n): inp += ['-ss', '20', '-i', U + 't1/musik.mp3']
    fl = []; prev = '[0]'
    for i in range(1, n): o = f'[m{i}]'; fl.append(f'{prev}[{i}]acrossfade=d=10:c1=tri:c2=tri{o}'); prev = o
    fl.append(f'{prev}atrim=0:{TOTAL:.3f},afade=t=in:d=3,afade=t=out:st={TOTAL - 8:.3f}:d=8,aformat=sample_rates=48000:channel_layouts=stereo[m]')
    run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', '[m]', '-c:a', 'pcm_s16le', music])
mix = F + 'mix.m4a'
if not os.path.exists(mix):
    run(['ffmpeg', '-v', 'error', '-y', '-i', voice, '-i', music, '-filter_complex',
         '[0]asplit[v1][v2];[1]volume=0.14[m];[m][v2]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=900[md];'
         '[v1][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]', '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', mix])
print('sound ok', flush=True)
# ---- 4. finish + mux: sepia, flicker, dust, grain, vignette, labels, subtitles ----
out = U + 'Der_wahre_Ursprung_des_Zweiten_Weltkriegs.mp4'
fc = ("[0:v]format=rgb24,colorchannelmixer=rr=.36:rg=.62:rb=.14:gr=.32:gg=.58:gb=.12:br=.25:bg=.47:bb=.10,"
      "eq=contrast=0.92:brightness=-0.02,eq=brightness='0.012*sin(t*13.1)+0.008*sin(t*29.7)':eval=frame,format=gbrp[a];"
      "[1:v]loop=-1:size=150,setpts=N/30/TB,format=gbrp[d];[a][d]blend=all_mode=screen:all_opacity=0.55,format=yuv420p[b];"
      "[b]noise=alls=9:allf=t,vignette=PI/4.2[n]")
lab_in, prev = [], '[n]'
for j, (t0, fn) in enumerate(labs):
    lab_in += ['-loop', '1', '-t', '6.4', '-itsoffset', f'{t0:.2f}', '-i', fn]
    fc += f";[{j + 3}:v]format=rgba,fade=in:st={t0:.2f}:d=0.6:alpha=1,fade=out:st={t0 + 5.6:.2f}:d=0.6:alpha=1[l{j}];{prev}[l{j}]overlay=0:0:eof_action=pass[o{j}]"; prev = f'[o{j}]'
fc += f";{prev}subtitles={F}subs.ass[v]"
run(['ffmpeg', '-v', 'error', '-stats', '-y', '-i', cut, '-i', U + 't1/dust.mp4', '-i', mix, *lab_in, '-filter_complex', fc, '-map', '[v]', '-map', '2:a',
     '-t', f'{TOTAL:.3f}', '-c:v', 'libx264', '-b:v', '4000k', '-maxrate', '6000k', '-bufsize', '12000k', '-preset', 'medium', '-tune', 'grain', '-pix_fmt', 'yuv420p',
     '-c:a', 'copy', '-movflags', '+faststart', out])
print('FINAL DONE', out, flush=True)
