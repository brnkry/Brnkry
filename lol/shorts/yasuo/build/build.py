"""Yasuo Short (1080x1920): 'Yasuo abisini oldurdu. Ama katil o degildi.'
Shots: cinematic band scaled to 1500 px tall, cropped around the subject, blurred copy behind.
usage: python3 build.py plan | base | mix | frames | final | preview"""
import subprocess, sys, os, json
S = '/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad'
Y = S + '/yasuo'; AN = Y + '/anim'; OUT = Y + '/short'; os.makedirs(OUT, exist_ok=True)
SEP = Y + '/sep/htdemucs/kinfull/vocals.wav'
NARR = json.load(open(Y + '/short_narr.json'))
VID = {'K': Y + '/kin.mp4', 'A': Y + '/awaken.mp4'}
XF = 0.3; LEAD = 0.15; TAIL = 0.35; BH = 1500
GRADE = 'eq=contrast=1.08:saturation=0.95:gamma=0.97,colorbalance=rs=-0.04:bs=0.05:rh=0.05:bh=-0.04,vignette=angle=PI/5'
# N: (para, [(src, start, weight, focus x)], transition in)   D: (kin from, kin to, video from, focus, lines)
EV = [
    ('N', 0, [('K', 59.0, 1, .48)], None),
    ('N', 1, [('K', 254.6, 2.6, .56), ('A', 93.6, 2.4, .42)], 'x'),
    ('N', 2, [('bloodmoon', 0, 4, .55), ('K', 1.0, 3, .5)], 'x'),
    ('N', 3, [('K', 16.96, 1, .2)], 'x'),
    ('D', 18.7, 20.75, 18.7, .2, ['YAPTIKLARIN', 'İÇİN HESAP VER.']),
    ('N', 4, [('K', 13.96, 2.5, .58), ('K', 76.0, 3, .42)], 'x'),
    ('D', 69.95, 71.4, 71.5, .45, ['AFFET BENİ,', 'KARDEŞİM.']),
    ('N', 5, [('BLACK', 0, 1.6, .5), ('A', 78.5, 3, .55), ('rivensplash2', 0, 2.6, .45)], 'flash'),
    ('N', 6, [('K', 90.04, .75, .5), ('K', 96.04, 3, .68)], 'x'),
    ('N', 7, [('K', 360.0, 1.6, .6), ('K', 376.0, 1.8, .53)], 'x'),
    ('N', 8, [('END', 0, 1, .5)], 'x'),
]
DIAL_TXT = {18.7: "Yaptıkların için hesap ver.", 69.95: "Affet beni kardeşim."}

def caption_rows(words, a, maxc=18):
    """narration sentence -> rows of word-timed words, <= maxc chars per row"""
    rows = []; cur = []; n = 0
    for w, s, e in words:
        if cur and n + len(w) + 1 > maxc: rows.append(cur); cur = []; n = 0
        cur.append([w.upper().replace('Ağ'.upper(), 'A').replace('AĞBİSİ', 'ABİSİ'), round(s + a, 3)]); n += len(w) + 1
    if cur: rows.append(cur)
    return rows

def plan():
    t = 0.0; pieces = []; narr = []; dial = []; texts = []; sfx = []
    for ev in EV:
        if ev[0] == 'N':
            _, pi, clips, tr = ev; p = NARR[pi]
            dur = p['end'] - p['start'] + LEAD + TAIL + (1.2 if pi == 8 else 0)
            narr.append((pi, t + LEAD)); tw = sum(c[2] for c in clips); a = t + LEAD - p['start']
            for j, (src, ss, w, fx) in enumerate(clips):
                pieces.append({'src': src, 'ss': ss, 'vis': dur * w / tw, 'fx': fx, 'tr': tr if j == 0 else 'x'})
            # captions: one block per sentence, word by word
            ws = [list(x) for x in p['words']]; sent = []
            for w in ws:
                sent.append(w)
                if w[0][-1] in '.:?!' or w is ws[-1]:
                    st = sent[0][1] + a - .03; rows = caption_rows(sent, -st + a)
                    texts.append([round(st, 3), round(sent[-1][2] + a + .3, 3), 'CAP', [[r, 104 if pi else 128, 'G' if pi == 0 and i == len(rows) - 1 else 'C'] for i, r in enumerate(rows)]])
                    sent = []
            if tr == 'flash': sfx.append(('slash_1.mp3', t + .1, -12))
            if pi == 0: sfx.append(('kin_kilic.wav', t, -9))
            if pi == 7: sfx.append(('impact_kucuk.wav', t + dur * 1.6 / 3.4, -14))
            t += dur
        else:
            _, a0, b0, vs, fx, disp = ev
            L = b0 - a0 + .25
            pieces.append({'src': 'K', 'ss': vs, 'vis': L, 'fx': fx, 'tr': 'x'})
            dial.append((a0, b0, t + .1))
            sys.path.insert(0, S); from align import align
            ws = align(SEP, a0, b0, DIAL_TXT[a0]); st = t + .1 + ws[0][1] - a0 - .03; rows = []; wi = 0
            for li, l in enumerate(disp):
                rows.append([[[w, round(t + .1 + ws[wi + m][1] - a0 - st, 3)] for m, w in enumerate(l.split())], 120, 'C' if li < len(disp) - 1 else 'G']); wi += len(l.split())
            texts.append([round(st, 3), round(t + L - .05, 3), 'DLG', rows])
            t += L
    texts.sort(key=lambda x: x[0])
    for i in range(len(texts) - 1):
        if texts[i][1] > texts[i + 1][0] - .05: texts[i][1] = round(texts[i + 1][0] - .05, 3)
    json.dump({'pieces': pieces, 'narr': narr, 'dial': dial, 'texts': texts, 'sfx': sfx, 'end': round(t, 2)}, open(OUT + '/plan.json', 'w'), ensure_ascii=False)
    open('ts.js', 'w').write('window.TS=' + json.dumps(texts, ensure_ascii=False) + ';')
    print('end', round(t, 2), 'pieces', len(pieces))

def piece(i, p, last):
    L = p['vis'] + (0 if last else XF); n = round(L * 30); o = f'{OUT}/p{i:02d}.mp4'; src = p['src']; fx = p['fx']
    W = round(1920 / 816 * BH / 2) * 2
    frame = (f"split[bg][fg];[bg]scale=-2:1920,crop=1080:1920:(iw-1080)*{fx}:0,gblur=sigma=28,eq=brightness=-0.25[b];"
             f"[fg]scale={W}:{BH}:flags=lanczos,crop=1080:{BH}:({W}-1080)*{fx}:0[f];[b][f]overlay=0:{(1920 - BH) // 2},{GRADE},setsar=1,format=yuv420p")
    if src in VID:
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(p['ss']), '-i', VID[src], '-filter_complex', f"[0:v]fps=30,crop=1920:816:0:132,{frame}[v]", '-map', '[v]']
    elif src == 'BLACK':
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:r=30', '-vf', 'format=yuv420p']
    elif src == 'END':
        cmd = ['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', '/home/user/Brnkry/lol/hikaye/yasuo/export/thumbnail_g.png', '-filter_complex',
               f"[0:v]fps=30,split[bg][fg];[bg]scale=-2:1920,crop=1080:1920,gblur=sigma=70,eq=brightness=-0.5[b];[fg]scale=1080:-2,zoompan=z='1+0.04*on/{n}':d=1:s=1080x608:fps=30[f];[b][f]overlay=0:656,setsar=1,format=yuv420p[v]", '-map', '[v]']
    else:  # AI splash, 1920x1080
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{AN}/{src}.mp4'], capture_output=True, text=True).stdout)
        f = max(1.0, L / (dur - .1)); slow = f'setpts={f:.4f}*PTS,minterpolate=fps=30:mi_mode=blend,' if f > 1 else ''
        cmd = ['ffmpeg', '-v', 'error', '-y', '-i', f'{AN}/{src}.mp4', '-filter_complex', f"[0:v]{slow}fps=30,crop=1920:816:0:132,{frame}[v]", '-map', '[v]']
    subprocess.run(cmd + ['-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', o], check=True)
    return o

def base():
    P = json.load(open(OUT + '/plan.json')); ps = P['pieces']
    fs = [piece(i, p, i == len(ps) - 1) for i, p in enumerate(ps)]
    inp = []
    for f in fs: inp += ['-i', f]
    fc = [f'[{i}:v]settb=AVTB,setpts=PTS-STARTPTS[i{i}]' for i in range(len(fs))]; cur = '[i0]'; off = 0
    for i in range(1, len(fs)):
        off += ps[i - 1]['vis']; tr = {'x': 'fade', 'flash': 'fadewhite'}[ps[i]['tr']]
        fc.append(f'{cur}[i{i}]xfade=transition={tr}:duration={XF}:offset={off:.3f}[x{i}]'); cur = f'[x{i}]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', cur, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', f'{OUT}/base.mp4'], check=True)
    print('base ok')

def gain(f, ss, L, target):
    r = subprocess.run(['ffmpeg', '-ss', f'{ss:.3f}', '-t', f'{L:.3f}', '-i', f, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return round(target - float([l for l in r.splitlines() if ' I:' in l][-1].split()[1]), 2)

def mix():
    P = json.load(open(OUT + '/plan.json')); END = P['end']; inp = []; fc = []; ii = 0; vox = []
    for pi, at in P['narr']:
        p = NARR[pi]; f = '../ses/' + p.get('file', 'anlatim.mp3'); a = max(0, p['start'] - .06); L = p['end'] - p['start'] + .3
        g = gain(f, a, L, -14.0); inp += ['-ss', f'{a:.3f}', '-t', f'{L:.3f}', '-i', f]
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,afade=t=out:st={L - .1:.3f}:d=0.1,adelay={int((at - (p["start"] - a)) * 1000)}:all=1,apad=whole_dur={END}[a{ii}]'); vox.append(f'[a{ii}]'); ii += 1
    for a0, b0, at in P['dial']:
        g = gain(SEP, a0, b0 - a0, -15.0); inp += ['-ss', f'{a0:.3f}', '-t', f'{b0 - a0:.3f}', '-i', SEP]
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,afade=t=out:st={b0 - a0 - .2:.3f}:d=0.2,adelay={int(at * 1000)}:all=1,apad=whole_dur={END}[a{ii}]'); vox.append(f'[a{ii}]'); ii += 1
    fc.append(''.join(vox) + f'amix=inputs={len(vox)}:normalize=0,asplit[vv][sc]')
    inp += ['-ss', '6', '-i', '/home/user/Brnkry/lol/hikaye/yasuo/ses/muzik_karanlik.mp3']
    fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{END},volume=-5dB,afade=t=in:d=0.5,afade=t=out:st={END - 1.5}:d=1.5[m0]'); ii += 1
    fc.append('[m0][sc]sidechaincompress=threshold=0.025:ratio=6:attack=15:release=400[mus]')
    lab = '[vv][mus]'; cnt = 2
    for j, (fn, at, g) in enumerate(P['sfx']):
        inp += ['-i', f'/home/user/Brnkry/lol/hikaye/yasuo/ses/{fn}']
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,adelay={int(at * 1000)}:all=1[s{j}]'); lab += f'[s{j}]'; ii += 1; cnt += 1
    fc.append(f'{lab}amix=inputs={cnt}:normalize=0:duration=longest,atrim=0:{END},afade=t=out:st={END - 0.8:.2f}:d=0.8,loudnorm=I=-14:TP=-1.5:LRA=11[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', f'{OUT}/mix.wav'], check=True)
    print('mix ok')

def frames():
    P = json.load(open(OUT + '/plan.json')); subprocess.run(['rm', '-rf', f'{OUT}/fr'])
    subprocess.run(['node', 'render.js', 'frames', f'{OUT}/fr', '30', '0', str(P['end'])], check=True)

def final():
    P = json.load(open(OUT + '/plan.json'))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/base.mp4', '-framerate', '30', '-i', f'{OUT}/fr/%05d.png', '-i', f'{OUT}/mix.wav',
                    '-filter_complex', '[0][1]overlay=0:0:shortest=1,format=yuv420p[v]', '-map', '[v]', '-map', '2:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
                    '-c:a', 'aac', '-b:a', '192k', '-t', str(P['end']), '../export/yasuo_short.mp4'], check=True)
    print('final ok')

{'plan': plan, 'base': base, 'mix': mix, 'frames': frames, 'final': final}[sys.argv[1]]()
