# Bäke long 16:9: shot list on the narration timeline + assembly (picture, sound); finish runs in fin_par.py
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bb import *
I, V = 'img', 'vid'
def t(m): a, b = m.split(':'); return int(a) * 60 + float(b)
SH = [
 (0, I, 22), ('Wenige Jahre später', V, 'tg', 26.0), ('Sein Name war', I, 15), ('Er war Zahnarzt, und', I, 17),
 ('Franz Bäke wurde am', I, 2), ('Im Mai 1915 meldete', I, 20), ('Nach dem Krieg studierte', I, 0), ('Doktor Bäke war Zahnarzt', I, 22),
 ('Doch in den dreißiger', V, '674', t('16:50')), ('1937 übte Bäke', I, 14), ('Im August 1939 wurde', I, 13), ('Mit der späteren 6.', V, '674', t('16:24')),
 ('Er wurde mehrfach verwundet', I, 21), ('Im Juni 1941 begann', V, '672', t('16:10')), ('Bäke diente nun im', I, 18), ('Im Juni 1942 übernahm', I, 12),
 ('Im Dezember 1942 rollte', V, '705', t('7:16')), ('Der Entsatzangriff kam', V, '705', t('9:14')), ('Die 6. Armee wurde', V, '705', t('11:32')),
 ('Bäke erhielt im Januar', I, 16), ('Im Sommer 1943 kämpfte', V, '672', t('18:22')), ('in einer der größten', I, 8), ('Am 1. August 1943', I, 20),
 ('Im September überreichte es', I, 11), ('Im November 1943 übernahm', I, 23), ('Ein Zahnarzt aus Hagen', I, 21), ('Die Lage im Süden', V, '672', t('16:20')),
 ('Anfang 1944 stellte die', I, 3), ('Rund 34 Panzer Tiger', V, 'tg', 35.0), ('Man nannte ihn das', I, 4), ('Seine erste große Schlacht', V, 'tg', 15.0),
 ('Nach deutschen Meldungen vernichtete', V, '674', t('22:47')), ('Historiker halten solche', I, 5), ('Dann kam der Kessel', I, 10), ('Bei Korsun waren', V, '703', t('11:12')),
 ('Am 4. Februar 1944', V, '712', t('9:24')), ('Es war Winter, doch', V, '712', t('9:10')), ('Panzer blieben stecken,', V, '712', t('9:00')),
 ('Die Panzer kamen bis', V, '712', t('9:54')), ('Am 16. Februar brachen', V, '703', t('13:58')), ('Viele erreichten die', V, '703', t('15:46')),
 ('Für diese Kämpfe erhielt', I, 1), ('Außerdem trug er das', I, 0), ('Es wurde für feindliche', V, '672', t('16:32')),
 ('Im Sommer 1944 brach', V, '672', t('22:59')), ('Bäke, inzwischen Oberst,', I, 17), ('In der Nacht zum', V, '674', t('21:14')), ('Der Angriff scheiterte.', V, '672', t('20:16')),
 ('Im März 1945 übernahm', V, '712', t('10:38')), ('Im April 1945 wurde', I, 2), ('Am 8. Mai 1945', V, '703', t('15:53')), ('Nach den meisten Quellen', I, 14),
 ('Und dann tat er', I, 22), ('Er ging zurück nach', I, 0), ('Der Mann, der Panzerregimenter', I, 13), ('Am 12. Dezember 1978', I, 19),
 ('Ein Zahnarzt, der zu', I, 15), ('Und der nach dem', I, 21)]
LAB = [('Franz Bäke wurde am', 'FRANZ BÄKE', '28. Februar 1898 · Schwarzenfels'), ('Mit der späteren 6.', '6. PANZER-DIVISION', 'Polen 1939 · Frankreich 1940'),
       ('Bäke diente nun im', 'PANZER-REGIMENT 11', 'Ostfront · 1941'), ('Im Dezember 1942 rollte', 'STALINGRAD', 'Entsatzangriff · Dezember 1942'),
       ('Im Sommer 1943 kämpfte', 'KURSK', 'Juli 1943'), ('Im September überreichte es', 'FÜHRERHAUPTQUARTIER', 'Eichenlaub · September 1943'),
       ('Man nannte ihn das', 'SCHWERES PANZER-REGIMENT BÄKE', 'Januar 1944'), ('Dann kam der Kessel', 'TSCHERKASSY', 'Februar 1944'),
       ('Für diese Kämpfe erhielt', 'SCHWERTER', '21. Februar 1944'), ('Bäke, inzwischen Oberst,', 'PANZERBRIGADE 106', 'Feldherrnhalle · September 1944'),
       ('Im April 1945 wurde', 'GENERALMAJOR', 'April 1945'), ('Am 12. Dezember 1978', 'FRANZ BÄKE', '1898 bis 1978')]
def _one(args):
    i, s, d, out = args
    if not os.path.exists(out):
        if s[1] == I: img_shot(s[2], d, out, i % 2 == 0)
        else: vid_shot(s[2], s[3], d, out)
    return i
def starts():
    st = [K(s[0]) for s in SH]; st[0] = 0.0
    for a, b, s in zip(st, st[1:], SH[1:]): assert b > a + 2.0, (s, round(b - a, 2))
    return st
def shots():
    from multiprocessing import Pool
    st = starts(); jobs = []
    for i, s in enumerate(SH):
        t1 = st[i + 1] if i + 1 < len(SH) else TOTAL; d = t1 - st[i] + XF; jobs.append((i, s, d, OUT + 'shots/%03d.mp4' % i))
    with Pool(os.cpu_count()) as pool:
        for i in pool.imap_unordered(_one, jobs): print('shot', i, flush=True)
    return [(j[3], j[2]) for j in jobs]
def xfade(clips, out):
    if os.path.exists(out): return
    G = 16; parts = []; PR = []
    for g in range(0, len(clips), G):
        sub = clips[g:g + G]; po = OUT + 'cut_%02d.mp4' % (g // G); dur = sum(d for _, d in sub) - XF * (len(sub) - 1)
        if not os.path.exists(po):
            inp, fl, prev, acc = [], [], '[0:v]', sub[0][1] - XF
            for c, _ in sub: inp += ['-i', c]
            for i in range(1, len(sub)):
                o = f'[x{i}]'; fl.append(f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={acc:.3f}{o}'); prev = o; acc += sub[i][1] - XF
            PR.append((subprocess.Popen(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', prev, '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', po + '.part.mp4']), po))
        parts.append((po, dur))
    for pr, po in PR: pr.wait(); os.replace(po + '.part.mp4', po)
    inp, fl, prev, acc = [], [], '[0:v]', parts[0][1] - XF
    for c, _ in parts: inp += ['-i', c]
    for i in range(1, len(parts)):
        o = f'[y{i}]'; fl.append(f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={acc:.3f}{o}'); prev = o; acc += parts[i][1] - XF
    run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', prev, '-t', f'{TOTAL:.3f}', '-c:v', 'libx264', '-crf', '15', '-preset', 'veryfast', out + '.part.mp4'])
    os.replace(out + '.part.mp4', out)
def sound(out):
    if os.path.exists(out): return
    v = OUT + 'voice.wav'
    run(['ffmpeg', '-v', 'error', '-y', '-i', E + 'p1/vcut.wav', '-af', f'aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(T1 * 1000)}:all=1', '-t', f'{TOTAL:.3f}', '-c:a', 'pcm_s16le', v])
    run(['ffmpeg', '-v', 'error', '-y', '-i', v, '-ss', '20', '-i', U + 't1/musik.mp3', '-filter_complex',
         f'[1]atrim=0:{TOTAL:.3f},afade=t=in:d=3,afade=t=out:st={TOTAL - 6:.3f}:d=6,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.14[mm];'
         '[0]asplit[v1][v2];[mm][v2]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=900[md];'
         '[v1][md]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]', '-map', '[a]', '-t', f'{TOTAL:.3f}', '-c:a', 'aac', '-b:a', '192k', out])
if __name__ == '__main__':
    print('TOTAL', round(TOTAL, 1), flush=True)
    if 'check' in sys.argv:
        st = starts(); print(len(SH), 'shots', 'min', round(min(b - a for a, b in zip(st, st[1:])), 2), 'max', round(max(b - a for a, b in zip(st, st[1:])), 2))
        for s, a, b in zip(SH, st, st[1:] + [TOTAL]): print(round(a, 1), round(b - a, 1), s[0], s[2:])
        sys.exit()
    c = shots(); xfade(c, OUT + 'cut.mp4'); print('cut ok', flush=True)
    sound(OUT + 'mix.m4a'); print('sound ok', flush=True)
