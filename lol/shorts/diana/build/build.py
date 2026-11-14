"""Diana Short: base video + mix. usage: python3 build.py base|mix"""
import subprocess, sys, json, re, os
P = '/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad/diana'
N = P + '/norm'; OUT = P + '/out'; os.makedirs(OUT, exist_ok=True)
END = 50.9
ZC = 'crop=866:1540:107:150,scale=1080:1920:flags=lanczos'  # combos: hide trainer title and Q/E/W/AA bar
PLAN = [(0, 4.0, 'eclipse', 1, ''), (4.0, 9.7, 'w', 2, ''), (9.7, 15.2, 'combos', 12, ZC), (15.2, 25.3, 'w', 8, ''),
        (25.3, 31.8, 'gameplay', 3, 'gblur=sigma=6,eq=brightness=-0.08'), (31.8, 36.2, 'gameplay', 10, 'gblur=sigma=6,eq=brightness=-0.08'),
        (36.2, 41.1, 'combos', 45, ZC), (41.1, 46.1, 'gameplay', 15, ''), (46.1, END, 'combos', 57, ZC + ',fade=t=out:st=4.0:d=0.8')]
def base():
    parts = []
    for i, (a, b, c, ss, vf) in enumerate(PLAN):
        o = f'{OUT}/p{i}.mp4'; parts.append(o); n = round(b * 30) - round(a * 30)
        f = (vf + ',' if vf else '') + 'tpad=stop_mode=clone:stop_duration=3,setsar=1,fps=30'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', f'{N}/{c}.mp4', '-vf', f, '-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', o], check=True)
    open(f'{OUT}/list.txt', 'w').writelines(f"file '{x}'\n" for x in parts)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list.txt', '-c', 'copy', f'{OUT}/base.mp4'], check=True)
def mix():
    s = open('overlay.html').read(); import ast; ev = ast.literal_eval(re.search(r"window.SFX=(\[.*?\]);", s, re.S).group(1))
    G = {'yazi_vurus': -13, 'pop': -19, 'card': -17, 'stamp_dan': -10, 'levelup': -12}
    inp = ['-i', '../ses/vo.mp3', '-stream_loop', '-1', '-i', '../../../sett/ses/muzik.mp3']
    fc = [f'[0]aresample=44100,aformat=channel_layouts=stereo,volume=4dB,apad=whole_dur={END},asplit[vo][sc]',
          f'[1]aresample=44100,aformat=channel_layouts=stereo,atrim=0:{END},volume=-15dB,afade=t=in:d=0.4,afade=t=out:st={END - 1.5}:d=1.5[m0]',
          '[m0][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=400[m]']; lab = ['[vo]', '[m]']
    for i, (n, t, g) in enumerate(ev):
        inp += ['-i', f'../ses/{n}.wav']; fc.append(f'[{i + 2}]aresample=44100,aformat=channel_layouts=stereo,volume={G[n] + g}dB,adelay={int(t * 1000)}:all=1[s{i}]'); lab.append(f'[s{i}]')
    fc.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0:duration=first,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', f'{OUT}/mix.wav'], check=True)
{'base': base, 'mix': mix}[sys.argv[1]]()
