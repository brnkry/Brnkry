"""Yasuo story, first ~42 s (cold open + narrator intro + title). 16:9.
usage: python3 build.py base | mix"""
import subprocess, sys, json, os
S = '/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad'
KIN = S + '/yasuo/kin.mp4'; OUT = S + '/yasuo/out'; os.makedirs(OUT, exist_ok=True)
NARR = 24.2   # narrator starts here
END = 42.6
# (out a, out b, kind, src/param)
PLAN = [
    (0.0, 10.6, 'K', 18.7),       # Yone: hesap ver ... yemin etmistin
    (10.6, 15.6, 'K', 35.6),      # onurun topragi lekeliyor / onursuzluktan iyidir
    (15.6, 19.4, 'K', 54.0),      # clash
    (19.4, 24.0, 'K', 70.1),      # affet beni kardesim
    (24.0, 28.8, 'I', ('Yasuo_0', 1.0, 1.12, .45, .35)),   # image, zoom from-to, focus x,y
    (28.8, 34.2, 'I', ('Yone_0', 1.12, 1.0, .5, .3)),
    (34.2, 39.2, 'SPLIT', ('Yasuo_0', 'Yone_0')),
    (39.2, END, 'BLACK', None),
]
def piece(i, p):
    a, b, k, q = p; L = b - a + (0.5 if i + 1 < len(PLAN) and PLAN[i + 1][2] != 'K' else 0); n = round(L * 30)
    o = f'{OUT}/v{i}.mp4'
    if k == 'K':
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(q), '-i', KIN, '-vf', 'fps=30,setsar=1,format=yuv420p']
    elif k == 'I':
        img, z0, z1, fx, fy = q
        z = f"{z0}+({z1}-{z0})*on/{n}"
        cmd = ['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', f'assets/{img}.jpg', '-vf',
               f"scale=3840:-2,zoompan=z='{z}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':d={n}:s=1920x1080:fps=30,eq=brightness=-0.06,crop=1920:816:0:132,pad=1920:1080:0:132:black,setsar=1,format=yuv420p"]
    elif k == 'SPLIT':
        l, r = q
        f = (f"[0]scale=-2:1080,crop=960:1080:(iw-960)*0.78:0,zoompan=z='1+0.05*on/{n}':d={n}:s=960x1080:fps=30[a];"
             f"[1]scale=-2:1080,crop=960:1080:(iw-960)*0.62:0,zoompan=z='1+0.05*on/{n}':d={n}:s=960x1080:fps=30[b];[a][b]hstack,eq=brightness=-0.1,crop=1920:816:0:132,pad=1920:1080:0:132:black,drawbox=x=957:y=132:w=6:h=816:color=0xE9C46A@0.9:t=fill,setsar=1,format=yuv420p[v]")
        cmd = ['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', f'assets/{l}.jpg', '-loop', '1', '-i', f'assets/{r}.jpg', '-filter_complex', f, '-map', '[v]']
    else:
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1920x1080:r=30', '-vf', 'format=yuv420p']
    subprocess.run(cmd + ['-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', o], check=True)
    return o, L
def base():
    vids = [piece(i, p) for i, p in enumerate(PLAN)]
    inp = []
    for v, _ in vids: inp += ['-i', v]
    fc = [f'[{i}:v]settb=AVTB,setpts=PTS-STARTPTS[i{i}]' for i in range(len(vids))]; cur = '[i0]'
    for i in range(1, len(PLAN)):
        lab = f'[x{i}]'
        if PLAN[i][2] == 'K': fc.append(f'{cur}[i{i}]concat=n=2:v=1:a=0,settb=AVTB{lab}')
        else: fc.append(f'{cur}[i{i}]xfade=transition=fade:duration=0.5:offset={PLAN[i][0]:.2f}{lab}')
        cur = lab
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', cur, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', f'{OUT}/base.mp4'], check=True)
    print('base ok')
def mix():
    # dialogue: original KIN audio for the cold open pieces; bed: KIN 0-16 (rain + score, no dialogue)
    parts = [p for p in PLAN if p[2] == 'K']
    inp = []; fc = []
    for i, (a, b, k, ss) in enumerate(parts):
        inp += ['-ss', str(ss), '-t', f'{b - a:.3f}', '-i', KIN]
        fc.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.04,afade=t=out:st={b - a - 0.06:.3f}:d=0.06,adelay={int(a * 1000)}:all=1[k{i}]')
    n = len(parts)
    inp += ['-i', '../ses/alex_deneme_2.mp3', '-ss', '0', '-t', '19', '-i', KIN]
    fc.append(f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume=3dB,adelay={int(NARR * 1000)}:all=1,apad=whole_dur={END},asplit[nv][sc]')
    fc.append(f'[{n + 1}:a]aresample=48000,aformat=channel_layouts=stereo,volume=-6dB,afade=t=in:d=1.2,afade=t=out:st=17:d=2,adelay={int(23.4 * 1000)}:all=1,apad=whole_dur={END}[bed0]')
    fc.append('[bed0][sc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=500[bed]')
    lab = ''.join(f'[k{i}]' for i in range(n))
    fc.append(f'{lab}[nv][bed]amix=inputs={n + 2}:normalize=0:duration=longest,atrim=0:{END},afade=t=out:st={END - 1.2}:d=1.2,loudnorm=I=-15:TP=-1.5:LRA=11[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', f'{OUT}/mix.wav'], check=True)
    print('mix ok')
{'base': base, 'mix': mix}[sys.argv[1]]()
