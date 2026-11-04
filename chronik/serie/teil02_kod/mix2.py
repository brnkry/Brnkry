# Teil 2 v2 mix: voice with gaps (+1 s), calm bed ducked by the voice, a soft page sound at each turn, clicks on the end page
import sys, subprocess
sys.path.insert(0, 'code'); import teil2b as T
TE = T.T_END; tl = [x + 0.15 for x in T.TURNS]; cl = list(T.CLICKS)
ins = [('el/turn%d.mp3' % (1 + k % 2), t, 5) for k, t in enumerate(tl)] + [('el/click.mp3', t - 0.02, 3) for t in cl]
d = ''.join('[%d:a]aresample=48000,aformat=channel_layouts=stereo,volume=%g,adelay=%d|%d,apad[s%d];' % (k + 2, v, int(t * 1000), int(t * 1000), k) for k, (_, t, v) in enumerate(ins))
inp = ['-i', 'vn2.wav', '-stream_loop', '-1', '-i', 'el/bed2.mp3'] + sum([['-i', f] for f, _, _ in ins], [])
fc = ('[0:a]adelay=1000|1000,aformat=channel_layouts=stereo,apad,asplit[v][k];'
      '[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:%.2f,volume=0.30,afade=t=in:d=1.5,afade=t=out:st=%.2f:d=4,apad[b0];[b0][k]sidechaincompress=threshold=0.06:ratio=2.5:attack=30:release=500[b];' % (TE, TE - 4) + d +
      '[v][b]' + ''.join('[s%d]' % k for k in range(len(ins))) + 'amix=inputs=%d:normalize=0:duration=longest,alimiter=limit=0.93[o]' % (2 + len(ins)))
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', fc, '-map', '[o]', '-ar', '48000', '-t', '%.2f' % TE, 'mix2.wav'], check=True); print('mix ok', TE)
