"""Mix for the gizli minyon Short: VO + ducked music + grouped UI sfx (confetti/pop/card/swish) + quiet Bozgun sound. usage: python3 mix.py OUT.wav"""
import json, subprocess, sys
D = 70.3
GAIN = {'pop': -12, 'card': -14, 'swish': -13, 'stamp': -1, 'item': -10, 'ring': -6, 'bubble': -15, 'tek': -14}
FILE = {k: f'../ses/{k}.wav' for k in GAIN}
ev = json.load(open('sfx.json'))
inp = ['-i', '../ses/vo.wav', '-stream_loop', '-1', '-i', '../../../rengar/muzik.mp3']
fc = ['[0]aresample=44100,aformat=channel_layouts=stereo,volume=8dB,apad=whole_dur=%s,asplit[vo][sc]' % D,
      '[1]aresample=44100,aformat=channel_layouts=stereo,atrim=0:%s,volume=-2dB,afade=t=in:d=0.4,afade=t=out:st=%s:d=1.4[m0]' % (D, D - 1.5),
      '[m0][sc]sidechaincompress=threshold=0.06:ratio=2.5:attack=20:release=400[mus]']
lab = []
for i, (n, t, g) in enumerate(ev):
    inp += ['-i', FILE[n]]
    j = i + 2
    trim = ',atrim=0:1.0,afade=t=out:st=0.7:d=0.3' if n in ('card', 'stamp', 'item', 'ring', 'tek') else ''
    fc.append(f'[{j}]aresample=44100,aformat=channel_layouts=stereo{trim},volume={GAIN[n] + g}dB,adelay={int(t * 1000)}:all=1[s{i}]')
    lab.append(f'[s{i}]')
fc.append('[vo][mus]' + ''.join(lab) + f'amix=inputs={len(lab) + 2}:normalize=0:duration=first,atrim=0:{D},loudnorm=I=-14:TP=-1.5:LRA=11[out]')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[out]', '-ar', '48000', sys.argv[1]], check=True)
