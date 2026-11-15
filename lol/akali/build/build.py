"""Akali guide: base video + mix. usage: python3 build.py base|mix"""
import subprocess, sys, json, os, ast, re
P = '/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad/akali'
OUT = P + '/out'; os.makedirs(OUT, exist_ok=True)
T = json.load(open('cues.json')); END = T['END']
SRC, SPOT = P + '/srcN.mp4', P + '/spotN.mp4'
BL = 'gblur=sigma=14,eq=brightness=-0.12'
CHAT = 'CHAT'
PLAN = [(0, T['why'], SPOT, 169, 185, ''), (T['why'], T['passive'], SPOT, 185, 200, ''),
        (T['passive'], T['q'], SRC, 13.2, 29.3, ''), (T['q'], T['w'], SRC, 29.3, 34.0, ''), (T['w'], T['e'], SRC, 34.0, 47.5, ''),
        (T['e'], T['r'], SRC, 47.5, 63.8, ''), (T['r'], T['combo'], SRC, 63.8, 75.0, ''), (T['combo'], T['match'], SRC, 75.0, 102.4, ''),
        (T['match'], T['runes'], SPOT, 212, 232, BL), (T['runes'], T['early'], SPOT, 232, 268, BL),
        (T['early'], T['mid'], SRC, 127.8, 152.9, CHAT), (T['mid'], T['late'], SRC, 152.9, 160.0, CHAT), (T['late'], T['outro'], SRC, 160.0, 180.0, CHAT),
        (T['outro'], END, SPOT, 200, 212, '')]
def base():
    parts = []
    for i, (a, b, f, s, e, vf) in enumerate(PLAN):
        o = f'{OUT}/p{i:02d}.mp4'; parts.append(o); n = round(b * 30) - round(a * 30); sp = (e - s) / (b - a)
        chain = f'[0]trim={s}:{e},setpts=(PTS-STARTPTS)/{sp:.5f},fps=30,tpad=stop_mode=clone:stop_duration=2'
        if vf == CHAT: chain += ',split[v][c];[c]crop=520:260:0:550,boxblur=18:2[b];[v][b]overlay=0:550'
        elif vf: chain += ',' + vf
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-filter_complex', chain + ',setsar=1[o]', '-map', '[o]', '-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', o], check=True)
        print('part', i, n, round(sp, 2))
    open(f'{OUT}/list.txt', 'w').writelines(f"file '{x}'\n" for x in parts)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list.txt', '-c', 'copy', f'{OUT}/base.mp4'], check=True)
def mix():
    s = open('overlay.html').read(); js = re.search(r"window\.SFX=(\[.*?\]);\nwindow", s, re.S).group(1)
    node = subprocess.run(['node', '-e', open('timeline.js').read() + ';const T=TL;console.log(JSON.stringify(' + js + '))'], capture_output=True, text=True, check=True)
    ev = json.loads(node.stdout)
    G = {'yazi_vurus': -13, 'pop': -19, 'card': -17, 'stamp_dan': -10, 'levelup': -15, 'gecis': -9, 'click': -14}
    inp = ['-i', '../ses/vo.mp3', '-stream_loop', '-1', '-i', '../../sett/ses/muzik.mp3']
    fc = [f'[0]aresample=44100,aformat=channel_layouts=stereo,volume=4dB,apad=whole_dur={END},asplit[vo][sc]',
          f'[1]aresample=44100,aformat=channel_layouts=stereo,atrim=0:{END},volume=-16dB,afade=t=in:d=0.5,afade=t=out:st={END - 1.0}:d=1.0[m0]',
          '[m0][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=400[m]']; lab = ['[vo]', '[m]']
    for i, (n, t, g) in enumerate(ev):
        inp += ['-i', f'../ses/{n}.wav']; fc.append(f'[{i + 2}]aresample=44100,aformat=channel_layouts=stereo,volume={G[n] + g}dB,adelay={int(t * 1000)}:all=1[s{i}]'); lab.append(f'[s{i}]')
    fc.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0:duration=first,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', f'{OUT}/mix.wav'], check=True)
    print('mix ok', len(ev))
{'base': base, 'mix': mix}[sys.argv[1]]()
