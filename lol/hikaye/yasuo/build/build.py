"""Yasuo story, first ~102 s (cold open, narrator intro, title, I. Iki kardes). 16:9, 2.35 letterbox, cinematic grade.
Uncut KIN scenes, transitions only at the cinematic's own cuts.
usage: python3 build.py base | mix | frames | final"""
import subprocess, sys, os
S = '/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad'
KIN = S + '/yasuo/kin.mp4'; AN = S + '/yasuo/anim'; OUT = S + '/yasuo/out'; os.makedirs(OUT, exist_ok=True)
NARR = 29.3   # narrator starts right after the slash into the Yasuo splash
END = 101.9
TITLE_END = 49.0
GRADE = ('eq=contrast=1.08:saturation=0.88:gamma=0.97,'
         'colorbalance=rs=-0.04:gs=0.0:bs=0.05:rm=0.01:bm=-0.01:rh=0.05:gh=0.01:bh=-0.04,'
         'vignette=angle=PI/4.6,noise=alls=5:allf=t')
BOX = 'pad=1920:1080:0:132:black,setsar=1,format=yuv420p'
# (out start, length, kind, params, transition into this piece)
PLAN = [
    (0.0, 23.71, 'K', (16.96, None), None),            # Yone close-up -> dialogue -> KIN's own white flash
    (23.71, 5.33, 'K', (70.46, None), 'white'),         # "Affet beni kardesim"; ends under the diagonal slash flash
    (29.04, 5.66, 'L', ('yasuo_login', 18.0, .45, 1.0, 1.06), None),
    (34.2, 5.84, 'L', ('yone_login', 2.0, .30, 1.08, 1.0), 'x'),
    (40.04, TITLE_END - 40.04, 'SPLIT', None, None),    # hard cut under the vertical slash flash, fades to black
    (49.0, 13.4, 'K', (107.6, None), 'black'),          # dawn over the mountain shrine, the village festival (N1)
    (61.8, 22.0, 'K', (213.0, None), 'x'),              # "Kaybettiklerini hatirla" -> childhood memory, red field
    (83.8, 3.9, 'K', (235.0, 'mute'), None),            # river (N2: Abisi Yone...)
    (87.2, 3.9, 'L', ('yasuo_login', 40.0, .45, 1.0, 1.05), 'x'),   # Yasuo sabirsiz...
    (90.6, 4.8, 'L', ('yone_login', 30.0, .30, 1.0, 1.06), 'x'),    # Yone ise sakin...
    (94.9, 7.0, 'K', (247.25, 'fadeout'), 'x'),         # growing up montage (Iki zit kutup...)
]
# narration clips (file, out time)
NARRS = [('alex_deneme_2.mp3', 29.3), ('an_koy.mp3', 49.6), ('an_kardes.mp3', 84.0)]
# (file, time, gain dB)
SFX = [('kin_kilic.wav', 23.42, -3), ('slash_1.mp3', 28.78, -5), ('slash_1.mp3', 39.78, -5), ('impact_2.mp3', 43.98, -3)]
XF = 0.5

def piece(i, p):
    a, L, k, q, tr = p
    n = round(L * 30); o = f'{OUT}/v{i}.mp4'
    if k == 'K':
        ss, fx = q
        vf = 'fps=30,crop=1920:816:0:132'
        if fx == 'eye':  # accelerate into Yasuo's eyes over the last 0.75 s, then burn to white
            t0 = L - 0.6
            vf += (f",scale=3840:1632,zoompan=z='if(gte(in_time,{t0}),1+1.6*pow((in_time-{t0})/0.6,2),1)'"
                   f":x='iw/2-iw/zoom/2':y='ih*0.47-ih/zoom/2':d=1:s=1920x816:fps=30,fade=t=out:st={L - 0.25:.2f}:d=0.25:color=white")
        if fx == 'fadeout': vf += f',fade=t=out:st={L - 0.8:.2f}:d=0.8'
        if i == 0: vf += f',fade=t=out:st={L - 0.12:.2f}:d=0.12:color=white'
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', KIN, '-vf', vf + ',' + GRADE + ',' + BOX]
    elif k == 'L':
        name, ss, fx, z0, z1 = q
        z = f"{z0}+({z1}-{z0})*on/{n}"
        vf = (f"fps=30,scale=3840:-2:flags=lanczos,crop=3840:1632:0:(ih-1632)*{fx},"
              f"zoompan=z='{z}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x816:fps=30,eq=brightness=-0.04,{GRADE},{BOX}")
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', f'{AN}/{name}.mp4', '-vf', vf]
    else:  # Yasuo | Yone, animated, gold divider
        e = "pow(max(0,1-t/0.6),3)"
        f = (f"[0]fps=30,scale=-2:816:flags=lanczos,crop=960:816:iw-960:0,zoompan=z='1+0.04*on/{n}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=960x816:fps=30,setpts=PTS-STARTPTS[a];"
             f"[1]fps=30,scale=-2:816:flags=lanczos,crop=960:816:(iw-960)*0.35:0,zoompan=z='1+0.04*on/{n}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=960x816:fps=30,setpts=PTS-STARTPTS[b];"
             f"color=c=black:s=1920x816:r=30[bg];[bg][a]overlay=x=0:y='70*{e}':shortest=1[ab];[ab][b]overlay=x=960:y='-70*{e}':shortest=1,"
             f"eq=brightness=-0.08,{GRADE},fade=t=out:st={L - 0.5:.2f}:d=0.5,{BOX}[v]")
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', '26', '-i', f'{AN}/yasuo_login.mp4', '-ss', '8', '-i', f'{AN}/yone_login.mp4',
               '-filter_complex', f, '-map', '[v]']
    if tr in ('white', 'black'):
        cmd[-1] = cmd[-1].replace(BOX, f"fade=t=in:d={0.45 if tr == 'white' else 0.6}:color={tr},{BOX}")
    subprocess.run(cmd + ['-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '15', '-pix_fmt', 'yuv420p', o], check=True)
    return o

def base():
    vids = [piece(i, p) for i, p in enumerate(PLAN)]
    inp = []
    for v in vids: inp += ['-i', v]
    fc = [f'[{i}:v]settb=AVTB,setpts=PTS-STARTPTS[i{i}]' for i in range(len(vids))]; cur = '[i0]'
    for i in range(1, len(PLAN)):
        lab = f'[x{i}]'
        if PLAN[i][4] == 'x': fc.append(f'{cur}[i{i}]xfade=transition=fade:duration={XF}:offset={PLAN[i][0]:.2f}{lab}')
        else: fc.append(f'{cur}[i{i}]concat=n=2:v=1:a=0,settb=AVTB{lab}')
        cur = lab
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', cur, '-t', str(END),
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '15', '-pix_fmt', 'yuv420p', f'{OUT}/base.mp4'], check=True)
    print('base ok')

def mix():
    # native KIN audio under the KIN pieces (dialogue scenes untouched, music scenes ducked under narration),
    # plus dialogue-free KIN beds under the narration parts: 0-17 (rain + score) and 550.6-567 (ending score)
    inp = []; fc = []; dry = []; wet = []; ii = 0
    for (a, L, k, q, tr) in PLAN:
        if k != 'K' or q[1] == 'mute': continue
        inp += ['-ss', str(q[0]), '-t', f'{L:.3f}', '-i', KIN]
        fin = 0.04 if tr not in ('x', 'black') else 0.6
        g = 5 if q[0] == 213.0 else 0
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,afade=t=in:d={fin},afade=t=out:st={L - 0.4:.3f}:d=0.4,adelay={int(a * 1000)}:all=1,apad=whole_dur={END}[k{ii}]')
        (wet if a >= 49 and a < 61 or a >= 94 else dry).append(f'[k{ii}]'); ii += 1
    for (b, ss, t, at, d, g) in [('b0', 0, 17, 29.1, 17, -6), ('b1', 550.6, 16.5, 83.6, 16.5, -4)]:
        inp += ['-ss', str(ss), '-t', str(t), '-i', KIN]
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,afade=t=in:d=0.6,afade=t=out:st={d - 2}:d=2,adelay={int(at * 1000)}:all=1,apad=whole_dur={END}[{b}]')
        wet.append(f'[{b}]'); ii += 1
    nl = []
    for fn, t in NARRS:
        inp += ['-i', f'../ses/{fn}']
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume=11dB,adelay={int(t * 1000)}:all=1,apad=whole_dur={END}[n{ii}]'); nl.append(f'[n{ii}]'); ii += 1
    fc.append(''.join(nl) + f'amix=inputs={len(nl)}:normalize=0,asplit[nv][sc]')
    fc.append(''.join(wet) + f'amix=inputs={len(wet)}:normalize=0[w0]')
    fc.append('[w0][sc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=500[bed]')
    lab = ''.join(dry) + '[nv][bed]'; cnt = len(dry) + 2
    for j, (fn, t, g) in enumerate(SFX):
        inp += ['-i', f'../ses/{fn}']
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,adelay={int(t * 1000)}:all=1[s{j}]'); lab += f'[s{j}]'; ii += 1; cnt += 1
    fc.append(f'{lab}amix=inputs={cnt}:normalize=0:duration=longest,atrim=0:{END},afade=t=out:st={END - 1.5}:d=1.5,loudnorm=I=-15:TP=-1.5:LRA=11[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', f'{OUT}/mix.wav'], check=True)
    print('mix ok')

def frames():
    subprocess.run(['rm', '-rf', f'{OUT}/fr'])
    subprocess.run(['node', 'render.js', 'frames', f'{OUT}/fr', '30', '0', str(END)], check=True)

def final():
    os.makedirs('../export', exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/base.mp4', '-framerate', '30', '-i', f'{OUT}/fr/%05d.png', '-i', f'{OUT}/mix.wav',
                    '-filter_complex', '[0][1]overlay=0:0:shortest=1,format=yuv420p[v]', '-map', '[v]', '-map', '2:a',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-b:a', '192k', '-t', str(END), '../export/yasuo_ilk100.mp4'], check=True)
    print('final ok')

{'base': base, 'mix': mix, 'frames': frames, 'final': final}[sys.argv[1]]()
