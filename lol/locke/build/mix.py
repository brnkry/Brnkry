"""Mix Locke VO + music + ability SFX. usage: python3 mix.py SCRATCH_LOCKE_DIR SFX_DIR(flash/ignite)"""
import json, subprocess, sys
L, SX = sys.argv[1], sys.argv[2]
c = json.load(open('cues.json')); T = c['T']; M = c['marks']
w = json.load(open('words.json'))['words']
def W(k, a):
    for s, e, t in w:
        if s >= a and t.lower().strip(".,?!:'").startswith(k): return s
hayir = W('hayır', T['nanami'][0]); truth = W('gerçekler', T['cta'][0])
sfx = [('q_uc_civi', c['uc'] + 0.1, 0.5), ('w_ruh_yangini', T['w'][0] + 0.25, 0.35), ('e_isinlanma', T['e'][0] + 0.25, 0.4), ('r_araf', M['son_dualar'][1] + 0.05, 0.3),
       ('oto_vurus', hayir, 0.45), ('oto_vurus', truth, 0.45), ('flash', c['flash'] - 0.1, 0.25), ('ignite', c['ignite'] - 0.05, 0.22)]
src = {'flash': f'{SX}/flash.wav', 'ignite': f'{SX}/ignite.wav'}
ins = ['-i', f'{L}/v/vo_new.wav', '-i', f'{L}/v/music.mp3']
fc = ['[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.6,apad=whole_dur=240,asplit[vo][sc]',
      "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.08,volume='if(lt(t,1.6),0,if(between(t,%.2f,%.2f),0,1))':eval=frame,afade=t=out:st=238:d=2[m]" % (M['nocturne'][0] - .1, M['nocturne'][1] + .2),
      '[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md]']
lab = ['[vo]', '[md]']
for i, (n, t, v) in enumerate(sfx):
    ins += ['-i', src.get(n, f'{L}/sfx/{n}.wav')]; j = i + 2; d = int(t * 1000)
    fc.append(f'[{j}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={v},adelay={d}|{d}[s{i}]'); lab.append(f'[s{i}]')
fc.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:240')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-ar', '48000', f'{L}/v/mix.wav'], check=True)
print('mixed', sfx)
