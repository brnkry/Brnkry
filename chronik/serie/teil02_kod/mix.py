# Teil 2 mix: voice (+1 s, as lcore.OFF), calm ElevenLabs bed under it (ducked by the voice), a soft page sound at each turn only
import sys, subprocess
sys.path.insert(0, 'code'); import teil2 as T
TE = T.T_END; tl = [x + 0.15 for x in T.TURNS]
d = ''.join('[%d:a]aresample=48000,aformat=channel_layouts=stereo,volume=6,adelay=%d|%d,apad[s%d];' % (k + 2, int(t * 1000), int(t * 1000), k) for k, t in enumerate(tl))
inp = ['-i', 'vn_full.wav', '-stream_loop', '-1', '-i', 'el/bed2.mp3'] + sum([['-i', 'el/turn%d.mp3' % (1 + k % 2)] for k in range(len(tl))], [])
fc = ('[0:a]adelay=1000,aformat=channel_layouts=stereo,apad,asplit[v][k];'
      '[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:%.2f,volume=0.30,afade=t=in:d=1.5,afade=t=out:st=%.2f:d=4,apad[b0];[b0][k]sidechaincompress=threshold=0.06:ratio=2.5:attack=30:release=500[b];' % (TE, TE - 4) + d +
      '[v][b]' + ''.join('[s%d]' % k for k in range(len(tl))) + 'amix=inputs=%d:normalize=0:duration=longest,alimiter=limit=0.93[o]' % (2 + len(tl)))
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', fc, '-map', '[o]', '-ar', '48000', '-t', '%.2f' % TE, 'mix.wav'], check=True); print('mix ok', TE)
