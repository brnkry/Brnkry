# shot list on the global timeline + assembly (picture, sound, finish)
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ee import *
I, V = 'img', 'vid'
LC = U + 'img/Legion_Condor__Bild_146-1974-082-60.jpg'; LC2 = U + 'img/Legion_Condor__Bild_183-59017-0002.jpg'
SH = [
 (0, V, 'conv2', 108.0),                                   # radio: pilot in the cockpit
 ('So soll der letzte', I, 15), ('Ein Kamerad wollte', I, 20), ('Sicher ist nur: Wenige', I, 23),
 ('Und nur fünf Monate', I, 3), ('Das ist seine Geschichte', I, 7), ('Heinrich Ehrler wurde am 14.', I, 11), ('Er wuchs in einer', I, 14),
 ('1935 ging er', V, 'dw', 391.0), ('Ende 1936 kam er', I, LC), ('Fast ein Jahr', V, 'dw', 320.0), ('Doch er wollte selbst', V, 'S', 14.0),
 ('Im Januar 1940 beantragte', V, 'dw', 604.0), ('Im Februar 1941 kam', I, 4), ('Im Mai 1942 wurde', I, 19), ('Man nannte es', I, 10),
 ('Hier oben war', I, 21), ('Im Winter ging', I, 2), ('Schneestürme, Nebel und', I, 19), ('Nicht weit entfernt lag', V, 'conv', 7.0),
 ('Am Himmel trafen', I, 24), ('Ehrler meldete Abschuss', I, 9), ('Im Sommer 1942 wurde', I, 1), ('Am 8. Juni 1943', I, 13),
 ('Doch auch er war', V, 'conv2', 76.0), ('Er sprang mit dem', V, 'dw', 213.0), ('Im August 1943 erhielt', I, 12), ('Im Mai 1944 meldete', I, 20),
 ('Am 1. August 1944', I, 11), ('Doch im Herbst brach', V, 'dw', 640.0), ('Im Oktober überrannte', V, 'tir', 135.0), ('Dort, an der Küste', V, 'dw', 284.0),
 ('Jahrelang hatte sie', V, 'conv', 30.0), ('Im September 1944 traf', I, 22), ('Ein einziger Treffer', V, 'tb', 27.6), ('Großadmiral Dönitz ließ', I, 5),
 ('Mitte Oktober ankerte', V, 'conv', 22.0), ('Am 29. Oktober griffen', V, 'tir', 6.0), ('Kurz vor dem Ziel', V, 'tb', 22.3), ('Danach wurden Jäger', I, 9),
 ('Doch die Einheit hatte', V, 'dw', 612.0), ('Viele Piloten waren', I, 10), ('Ehrler kam am 9.', I, 24), ('Am Morgen des 12.', V, 'tir', 9.0),
 ('Über dreißig Lancaster', V, 'tb', 46.7), ('Deutsche Beobachtungsposten sahen', V, 'dw', 326.0), ('Die Meldungen erreichten', V, 'conv', 44.0),
 ('Erst etwa eine Viertelstunde', I, 21), ('Eine Ju 52', V, 'dw', 606.0), ('Ehrler startete als Erster', I, 4), ('In der Luft merkte', V, 'b17', 245.0),
 ('Die Bomber fand er', V, 'tir', 11.0), ('Von Weitem sah er', V, 'tir', 44.0), ('Über Håkøya warfen', V, 'tb', 54.8), ('Zwei trafen das Schiff', V, 'tir', 58.0),
 ('Die Tirpitz neigte', I, 3), ('Hunderte Seeleute waren', V, 'tir', 62.0), ('Je nach Quelle', V, 'conv', 18.0), ('Dann begann die Suche', I, 7),
 ('Im Dezember 1944 stand', I, 11), ('Man verurteilte ihn', I, 14), ('Kameraden setzten sich', I, 0), ('Die Strafe wurde ausgesetzt', I, 24),
 ('Ende Februar 1945 holte', I, 6), ('Ihre Maschine war', I, 17), ('Sie flog über 850', I, 18), ('Doch es gab zu', I, 2),
 ('Und die Amerikaner schickten', V, 'b17', 100.0), ('Am 21. März 1945', V, 'b17', 160.0), ('Am nächsten Tag folgte', V, 'b17', 201.0), ('In nur vier Tagen', I, 12),
 ('Dann kam der April', V, 'tir', 150.0), ('Am 4. April stieg', I, 23), ('Was danach geschah', V, 'b17', 232.0), ('Nach der bekanntesten Fassung', V, 'conv2', 103.0),
 ('Dann war seine Munition', I, 14), ('Walter Schuck erinnerte', I, 0), (R2 - 0.6, I, 6), ('Andere erinnerten sich', I, 13),
 ('Ob Ehrler wirklich', V, 'conv2', 104.0), ('Sicher ist nur: Seine', I, 18), ('Am 7. April wurde', I, 8), ('Heinrich Ehrler wurde 27', I, 12),
 ('Ihm werden 208', I, 9), ('Und selbst sein Grab', I, 13), ('Ein Mann, den man', I, 3), ('Ein Pilot, um dessen', I, 7), ('Fünf Wochen nach', I, 15)]
LAB = [('Heinrich Ehrler wurde am 14.', 'HEINRICH EHRLER', '14. September 1917 · Oberbalbach'), ('Ende 1936 kam er', 'LEGION CONDOR', 'Spanien, 1936 bis 1937'),
       ('Im Mai 1942 wurde', 'JAGDGESCHWADER 5', 'Petsamo · Finnland'), ('Im Sommer 1942 wurde', 'RITTERKREUZ', '4. September 1942'),
       ('Am 1. August 1944', 'KOMMODORE', 'Jagdgeschwader 5 · August 1944'), ('Mitte Oktober ankerte', 'TIRPITZ', 'Håkøya bei Tromsø'),
       ('Am Morgen des 12.', '12. NOVEMBER 1944', 'Angriff auf die Tirpitz'), ('Im Dezember 1944 stand', 'REICHSKRIEGSGERICHT', 'Oslo · Dezember 1944'),
       ('Ende Februar 1945 holte', 'JAGDGESCHWADER 7', 'Messerschmitt Me 262'), ('Am 4. April stieg', '4. APRIL 1945', 'Letzter Einsatz'),
       ('Walter Schuck erinnerte', 'WALTER SCHUCK', 'Pilot im Jagdgeschwader 5 und 7'), ('Am 10. April wurde', 'STENDAL', 'Beigesetzt am 10. April 1945')]
def _one(args):
    i, s, d, out = args
    if not os.path.exists(out):
        if s[1] == I: img_shot(s[2], d, out, i % 2 == 0)
        elif s[2] == 'fly': fly_shot(s[3], d, out)
        else: vid_shot(s[2], s[3], d, out)
    return i
def shots():
    from multiprocessing import Pool
    st = [K(s[0]) for s in SH]; st[0] = 0.0
    assert all(b > a + 1.5 for a, b in zip(st, st[1:]))
    jobs = []
    for i, s in enumerate(SH):
        t1 = st[i + 1] if i + 1 < len(SH) else TOTAL; d = t1 - st[i] + XF; jobs.append((i, s, d, OUT + 'shots/%03d.mp4' % i))
    with Pool(os.cpu_count()) as pool:
        for i in pool.imap_unordered(_one, jobs): print('shot', i, flush=True)
    return [(j[3], j[2]) for j in jobs]
def xfade(clips, out):
    if os.path.exists(out): return
    G = 20; parts = []; acc_all = 0.0; PR = []
    for g in range(0, len(clips), G):
        sub = clips[g:g + G]; po = OUT + 'cut_%02d.mp4' % (g // G); dur = sum(d for _, d in sub) - XF * (len(sub) - 1)
        if not os.path.exists(po):
            inp, fl, prev, acc = [], [], '[0:v]', sub[0][1] - XF
            for c, _ in sub: inp += ['-i', c]
            for i in range(1, len(sub)):
                o = f'[x{i}]'; fl.append(f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={acc:.3f}{o}'); prev = o; acc += sub[i][1] - XF
            if fl: PR.append((subprocess.Popen(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', prev, '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', po + '.part.mp4']), po))
            else: run(['ffmpeg', '-v', 'error', '-y', '-i', sub[0][0], '-c', 'copy', po + '.part.mp4']); os.replace(po + '.part.mp4', po)
        parts.append((po, dur))
    for pr, po in PR: pr.wait(); os.replace(po + '.part.mp4', po)
    inp, fl, prev, acc = [], [], '[0:v]', parts[0][1] - XF
    for c, _ in parts: inp += ['-i', c]
    for i in range(1, len(parts)):
        o = f'[y{i}]'; fl.append(f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={acc:.3f}{o}'); prev = o; acc += parts[i][1] - XF
    run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', prev, '-t', f'{TOTAL:.3f}', '-c:v', 'libx264', '-crf', '15', '-preset', 'ultrafast', out + '.part.mp4'])
    os.replace(out + '.part.mp4', out)
def sound(out):
    if os.path.exists(out): return
    v = OUT + 'voice.wav'
    fl = (f"[0]aformat=sample_rates=48000:channel_layouts=stereo,asplit[ra][rb];[ra]adelay={int(R1 * 1000)}:all=1[r1];[rb]adelay={int(R2 * 1000)}:all=1[r2];"
          f"[1]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(T1 * 1000)}:all=1[a];[2]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(T2 * 1000)}:all=1[b];"
          f"[3]aformat=sample_rates=48000:channel_layouts=stereo,asplit[p3a][p3b];"
          f"[p3a]atrim=0:{CUT_A:.3f},afade=t=out:st={CUT_A - 0.15:.3f}:d=0.15,adelay={int(T3 * 1000)}:all=1[c];"
          f"[p3b]atrim=start={CUT_B:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.08,adelay={int((T3B + CUT_B) * 1000)}:all=1[d];"
          f"[r1][r2][a][b][c][d]amix=inputs=6:normalize=0:duration=longest[v]")
    run(['ffmpeg', '-v', 'error', '-y', '-i', RADIO, '-i', E + 'p1/vcut.wav', '-i', E + 'p2/vcut.wav', '-i', E + 'p3/vcut.wav', '-filter_complex', fl,
         '-map', '[v]', '-t', f'{TOTAL:.3f}', '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', v])
    m = OUT + 'music.wav'; n = int(TOTAL // 560) + 2; inp = []
    for _ in range(n): inp += ['-ss', '20', '-i', U + 't1/musik.mp3']
    fl, prev = [], '[0]'
    for i in range(1, n): o = f'[m{i}]'; fl.append(f'{prev}[{i}]acrossfade=d=10:c1=tri:c2=tri{o}'); prev = o
    fl.append(f'{prev}atrim=0:{TOTAL:.3f},afade=t=in:d=3,afade=t=out:st={TOTAL - 6:.3f}:d=6,aformat=sample_rates=48000:channel_layouts=stereo[m]')
    run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', '[m]', '-c:a', 'pcm_s16le', m])
    run(['ffmpeg', '-v', 'error', '-y', '-i', v, '-i', m, '-filter_complex',
         '[0]asplit[v1][v2];[1]volume=0.14[mm];[mm][v2]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=900[md];'
         '[v1][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]', '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', out])
def finish(cut, mix, out):
    sub = OUT + 'subs.ass'; ass(sub)
    # light old-film finish over colour: slightly muted and warm, soft flicker, light dust, grain, vignette
    fc = ("[0:v]format=rgb24,eq=contrast=0.96:saturation=0.82:gamma=1.0,colorbalance=rs=0.03:gs=0.01:bs=-0.04:rm=0.02:bm=-0.03,"
          "eq=brightness='0.008*sin(t*13.1)+0.006*sin(t*29.7)':eval=frame,format=gbrp[a];"
          "[1:v]loop=-1:size=150,setpts=N/30/TB,format=gbrp[d];[a][d]blend=all_mode=screen:all_opacity=0.32,format=yuv420p[b];"
          "[b]noise=alls=6:allf=t,vignette=PI/4.8[n]")
    lab_in, prev = [], '[n]'
    for j, (ph, big, small) in enumerate(LAB):
        t0 = K(ph) + 0.4; fn = OUT + 'lab%02d.png' % j; label_png(big, small, fn)
        lab_in += ['-loop', '1', '-t', '6.4', '-itsoffset', f'{t0:.2f}', '-i', fn]
        fc += f";[{j + 3}:v]format=rgba,fade=in:st={t0:.2f}:d=0.6:alpha=1,fade=out:st={t0 + 5.6:.2f}:d=0.6:alpha=1[l{j}];{prev}[l{j}]overlay=0:0:eof_action=pass[o{j}]"; prev = f'[o{j}]'
    fc += f";{prev}subtitles={sub},fade=t=out:st={TOTAL - 2.0:.2f}:d=2.0[v]"
    run(['ffmpeg', '-v', 'error', '-stats', '-y', '-i', cut, '-i', U + 't1/dust.mp4', '-i', mix, *lab_in, '-filter_complex', fc, '-map', '[v]', '-map', '2:a',
         '-t', f'{TOTAL:.3f}', '-c:v', 'libx264', '-b:v', '6000k', '-maxrate', '8000k', '-bufsize', '16000k', '-preset', 'medium', '-tune', 'grain', '-pix_fmt', 'yuv420p',
         '-c:a', 'copy', '-movflags', '+faststart', out + '.part.mp4'])
    os.replace(out + '.part.mp4', out)
if __name__ == '__main__':
    print('TOTAL', round(TOTAL, 1), flush=True)
    c = shots(); xfade(c, OUT + 'cut.mp4'); print('cut ok', flush=True)
    sound(OUT + 'mix.m4a'); print('sound ok', flush=True)
    finish(OUT + 'cut.mp4', OUT + 'mix.m4a', E + 'Heinrich_Ehrler_lang_v1.mp4'); print('DONE', flush=True)
