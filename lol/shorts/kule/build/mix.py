"""Mix for the Kule Short: VO + ducked music + user's turret sound + UI sfx (whoosh/ding/tick). usage: python3 mix.py OUT.wav"""
import json, subprocess, sys
D = 45.0
GAIN = {'turret': -5.2, 'whoosh': -11, 'ding': 1.6, 'tick': 12}
FILE = {'turret': '../ses/turret_target.wav', 'whoosh': '../ses/whoosh.wav', 'ding': '../ses/ding.wav', 'tick': '../ses/tick.wav'}
ev = json.load(open('sfx.json'))
inp = ['-i', '../ses/vo_kule.wav', '-stream_loop', '-1', '-i', '../../../sett/ses/muzik.mp3']
fc = ['[0]aresample=44100,aformat=channel_layouts=stereo,volume=15dB,apad=whole_dur=%s,asplit[vo][sc]' % D,
      '[1]aresample=44100,aformat=channel_layouts=stereo,atrim=0:%s,volume=-19dB,afade=t=in:d=0.4,afade=t=out:st=%s:d=1.4[m0]' % (D, D - 1.5),
      '[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[mus]']
lab = []
for i, (n, t, g) in enumerate(ev):
    inp += ['-i', FILE[n]]
    j = i + 2
    trim = ',atrim=0:1.0,afade=t=out:st=0.7:d=0.3' if n == 'whoosh' else ''
    fc.append(f'[{j}]aresample=44100,aformat=channel_layouts=stereo{trim},volume={GAIN[n] + g}dB,adelay={int(t * 1000)}:all=1[s{i}]')
    lab.append(f'[s{i}]')
fc.append('[vo][mus]' + ''.join(lab) + f'amix=inputs={len(lab) + 2}:normalize=0:duration=first,atrim=0:{D},loudnorm=I=-14:TP=-1.5:LRA=11[out]')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[out]', '-ar', '48000', sys.argv[1]], check=True)
