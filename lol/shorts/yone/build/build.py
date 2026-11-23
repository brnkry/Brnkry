"""Yone Short (1080x1920): continues the Yasuo Short ('Cunku Yone geri dondu').
No new voice: Alex lines cut from the long Yone video narration, Yone's own lines from the official Turkish voice lines.
usage: python3 build.py plan | base | mix | frames | final"""
import subprocess, sys, os, json
S = '/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad'
Y = S + '/yasuo'; OUT = S + '/yone/short'; os.makedirs(OUT, exist_ok=True)
YB = '/home/user/Brnkry/lol/hikaye/yone/build'; YS = '/home/user/Brnkry/lol/hikaye/yone/ses/'; XS = '/home/user/Brnkry/lol/hikaye/yasuo/ses/'
SN = json.load(open('short_narr.json'))  # the Short's own narration (anlatim.txt), aligned
REPW = json.load(open('rep_short.json')); REPV = S + '/yone/rep/yone_rep.mp4'
VID = {'K': Y + '/kin.mp4', 'P': Y + '/anim/the_path.mp4'}
AI = S + '/yone/anim'
IMG = {'face': '/home/user/Brnkry/lol/hikaye/yasuo/build/assets/thumb/yone_ikiyuz_v.jpg'}
XF = 0.3; LEAD = 0.15; TAIL = 0.35; BH = 1500
GRADE = 'eq=contrast=1.08:saturation=0.95:gamma=0.97,colorbalance=rs=-0.04:bs=0.05:rh=0.05:bh=-0.04,vignette=angle=PI/5'
# N: (row, first word, last word (excl, None = to the end), [(src, start, weight, focus x)], transition in)
# R: (voice line key, [(src, start, weight, focus x)], transition in)
EV = [
    ('N', 0, [('K', 377.2, 1, .5)], None),
    ('N', 1, [('K', 52.3, 3, .55), ('P', 36.0, 2.6, .5)], 'x'),
    ('N', 2, [('P', 62.0, 3, .5), ('K', 417.0, 3.6, .5)], 'x'),
    ('N', 3, [('P', 100.0, 4.5, .45), ('P', 174.0, 4.3, .4)], 'x'),
    ('N', 4, [('K', 425.5, 4.4, .5), ('K', 374.0, 4.0, .5)], 'black'),
    ('N', 5, [('face', 0, 1, .77)], 'x'),
    ('N', 6, [('K', 470.0, 3.6, .5), ('K', 395.0, 3.4, .45)], 'x'),
    ('N', 7, [('yone_varsayilan', 0, 4.6, .62), ('P', 200.0, 3.4, .5)], 'x'),
    ('R', 'maske', [('yone_inkshadow', 0, 1, .58)], 'black'),
]
LAUGH = {3: 'kahkahaydı.', 7: 'adı.'}

def tr_upper(w):
    return w.replace('i', 'İ').replace('ı', 'I').upper().replace('AĞBİSİNİ', 'ABİSİNİ').replace('Â', 'A')

def rows_of(words, st, maxc=14):
    rows = []; cur = []; n = 0
    for w, s, e in words:
        if cur and n + len(w) + 1 > maxc: rows.append(cur); cur = []; n = 0
        cur.append([tr_upper(w), round(s - st, 3)]); n += len(w) + 1
    if cur: rows.append(cur)
    return rows

def idx(ws, k, default):
    if k is None: return default
    if isinstance(k, int): return k
    return next(i for i, w in enumerate(ws) if w[0] == k)

def speech_edges(w0, w1):
    a = w0 - 1.0
    r = subprocess.run(['ffmpeg', '-ss', f'{a:.3f}', '-t', f'{w1 - w0 + 2.2:.3f}', '-i', S + '/yone/rep/rep.wav', '-af', 'silencedetect=n=-40dB:d=0.12', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [a + float(l.split('silence_start: ')[1]) for l in r.splitlines() if 'silence_start' in l]
    en = [a + float(l.split('silence_end: ')[1].split()[0]) for l in r.splitlines() if 'silence_end' in l]
    return max([e for e in en if e <= w0 + 0.05], default=w0 - 0.1) - 0.06, min([x for x in st if x >= w1 - 0.25], default=w1 + 0.15) + 0.08

def plan():
    t = 0.0; pieces = []; vox = []; texts = []; sfx = []
    def put(clips, dur, tr):
        tw = sum(c[2] for c in clips)
        for j, (src, ss, w, fx) in enumerate(clips): pieces.append({'src': src, 'ss': ss, 'vis': dur * w / tw, 'fx': fx, 'tr': tr if j == 0 else 'x'})
    for ev in EV:
        if ev[0] == 'N':
            _, r, clips, tr = ev; p = SN[r]; ws = p['words']
            s0, s1 = ws[0][1], ws[-1][2]
            dur = s1 - s0 + LEAD + TAIL + (0.3 if r == 7 else 0)
            f = '/home/user/Brnkry/lol/shorts/yone/ses/anlatim.mp3'
            vox.append((f, s0 - 0.06, s1 + 0.2, t + LEAD - 0.06, -14.0))
            a = t + LEAD - s0
            put(clips, dur, tr)
            sent = []
            for w in ws:
                sent.append(w)
                if w[0][-1] in '.:?!' or w is ws[-1]:
                    # max 3 rows on screen: split long sentences into chunks of words
                    chunks = []; cur = []
                    for x in sent:
                        cur.append(x)
                        if len(rows_of([(y[0], 0, 0) for y in cur], 0)) > 3: cur.pop(); chunks.append(cur); cur = [x]
                    chunks.append(cur)
                    if len(chunks) > 1 and len(chunks[-1]) <= 2: last = chunks.pop(); chunks[-1] += last
                    for ch in chunks:
                        st = ch[0][1] + a - .03
                        texts.append([round(st, 3), round(ch[-1][2] + a + .3, 3), 'CAP', [[rw, 110 if r == 0 else 94, 'G' if r == 0 else 'C'] for rw in rows_of([(x[0], x[1] + a, x[2]) for x in ch], st)]])
                    sent = []
            if r in LAUGH:
                at = a + next(w[2] for w in p['words'] if w[0] == LAUGH[r]) + 0.15
                sfx.append((YS + 'kahkaha.mp3', at, -10, '') if r == 3 else (YS + 'kahkaha.mp3', at - 0.4, -8, 'lowpass=f=420,aecho=0.8:0.6:90|160:0.35|0.2'))
            if tr == 'flash': sfx.append((XS + 'slash_1.mp3', t + .1, -12, ''))
            t += dur
        else:  # Yone's own line, big gold text at the top
            _, key, clips, tr = ev; ws = REPW[key]
            a_s, a_e = speech_edges(ws[0][1], ws[-1][2])
            dur = (a_e - a_s) + 0.25 + 0.3
            vox.append((REPV, a_s, a_e, t + 0.25, -15.0))
            off = t + 0.25 - a_s
            put(clips, dur, tr)
            rows = rows_of([(w[0], w[1] + off, w[2]) for w in ws], ws[0][1] + off - .03, maxc=18)
            texts.append([round(ws[0][1] + off - .03, 3), round(t + dur - .05, 3), 'DLG', [[rw, 96, 'C' if i < len(rows) - 1 else 'G'] for i, rw in enumerate(rows)]])
            if key == 'maske': sfx.append((XS + 'impact_kucuk.wav', t + 0.05, -13, ''))
            t += dur
    texts.sort(key=lambda x: x[0])
    for i in range(len(texts) - 1):
        if texts[i][1] > texts[i + 1][0] - .05: texts[i][1] = round(texts[i + 1][0] - .05, 3)
    json.dump({'pieces': pieces, 'vox': vox, 'texts': texts, 'sfx': sfx, 'end': round(t, 2)}, open(OUT + '/plan.json', 'w'), ensure_ascii=False)
    open('ts.js', 'w').write('window.TS=' + json.dumps(texts, ensure_ascii=False) + ';')
    print('end', round(t, 2), 'pieces', len(pieces))
    for tx in texts: print(round(tx[0], 2), round(tx[1], 2), tx[2], ' / '.join(' '.join(w[0] for w in r[0]) for r in tx[3]))

def piece(i, p, last):
    L = p['vis'] + (0 if last else XF); n = round(L * 30); o = f'{OUT}/p{i:02d}.mp4'; src = p['src']; fx = p['fx']
    W = round(1920 / 816 * BH / 2) * 2
    frame = (f"split[bg][fg];[bg]scale=-2:1920,crop=1080:1920:(iw-1080)*{fx}:0,gblur=sigma=28,eq=brightness=-0.25[b];"
             f"[fg]scale={W}:{BH}:flags=lanczos,crop=1080:{BH}:({W}-1080)*{fx}:0[f];[b][f]overlay=0:{(1920 - BH) // 2},{GRADE},setsar=1,format=yuv420p")
    if src in VID:
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(p['ss']), '-i', VID[src], '-filter_complex', f"[0:v]fps=30,crop=1920:816:0:132,{frame}[v]", '-map', '[v]']
    elif src == 'BLACK':
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:r=30', '-vf', 'format=yuv420p']
    elif src in ('yone_varsayilan', 'yone_inkshadow', 'yone_severed', 'yone_maskedjustice', 'yone_tohum', 'yone_battleacademia'):
        f_ = f'{AI}/{src}.mp4'
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f_], capture_output=True, text=True).stdout)
        fct = max(1.0, L / (dur - .1)); slow = f'setpts={fct:.4f}*PTS,minterpolate=fps=30:mi_mode=blend,' if fct > 1 else ''
        cmd = ['ffmpeg', '-v', 'error', '-y', '-i', f_, '-filter_complex', f"[0:v]{slow}fps=30,crop=1920:816:0:132,{frame}[v]", '-map', '[v]']
    else:  # still image (the half old / half masked face): slow push in
        cmd = ['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', IMG[src], '-filter_complex',
               f"[0:v]fps=30,scale=1920:1080,crop=1920:816:0:132,zoompan=z='1+0.06*on/{n}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)/2':d=1:s=1920x816:fps=30,{frame}[v]", '-map', '[v]']
    subprocess.run(cmd + ['-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', o], check=True)
    return o

def base():
    P = json.load(open(OUT + '/plan.json')); ps = P['pieces']
    fs = [piece(i, p, i == len(ps) - 1) for i, p in enumerate(ps)]
    inp = []
    for f in fs: inp += ['-i', f]
    fc = [f'[{i}:v]settb=AVTB,setpts=PTS-STARTPTS[i{i}]' for i in range(len(fs))]; cur = '[i0]'; off = 0
    for i in range(1, len(fs)):
        off += ps[i - 1]['vis']; tr = {'x': 'fade', 'flash': 'fadewhite', 'black': 'fadeblack'}[ps[i]['tr']]
        fc.append(f'{cur}[i{i}]xfade=transition={tr}:duration={XF}:offset={off:.3f}[x{i}]'); cur = f'[x{i}]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', cur, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', f'{OUT}/base.mp4'], check=True)
    print('base ok')

def gain(f, ss, L, target):
    r = subprocess.run(['ffmpeg', '-ss', f'{ss:.3f}', '-t', f'{L:.3f}', '-i', f, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return round(target - float([l for l in r.splitlines() if ' I:' in l][-1].split()[1]), 2)

def mix():
    P = json.load(open(OUT + '/plan.json')); END = P['end']; inp = []; fc = []; ii = 0; vx = []
    for f, a, b, at, tgt in P['vox']:
        L = b - a; g = gain(f, a, L, tgt); inp += ['-ss', f'{a:.3f}', '-t', f'{L:.3f}', '-i', f]
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,afade=t=in:d=0.03,afade=t=out:st={L - .1:.3f}:d=0.1,adelay={int(at * 1000)}:all=1,apad=whole_dur={END}[a{ii}]'); vx.append(f'[a{ii}]'); ii += 1
    fc.append(''.join(vx) + f'amix=inputs={len(vx)}:normalize=0,asplit[vv][sc]')
    inp += ['-stream_loop', '-1', '-ss', '60', '-i', XS + 'muzik_mistik.mp3']
    fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{END},volume=-4dB,afade=t=in:d=0.4,afade=t=out:st={END - 1.2:.2f}:d=1.2[m0]'); ii += 1
    fc.append('[m0][sc]sidechaincompress=threshold=0.025:ratio=6:attack=15:release=400[mus]')
    lab = '[vv][mus]'; cnt = 2
    for j, (f, at, g, fx) in enumerate(P['sfx']):
        inp += ['-i', f]
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,{fx + "," if fx else ""}volume={g}dB,adelay={int(max(at, 0) * 1000)}:all=1[s{j}]'); lab += f'[s{j}]'; ii += 1; cnt += 1
    fc.append(f'{lab}amix=inputs={cnt}:normalize=0:duration=longest,atrim=0:{END},afade=t=out:st={END - 0.5:.2f}:d=0.5,loudnorm=I=-14:TP=-1.5:LRA=11[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', f'{OUT}/mix.wav'], check=True)
    print('mix ok')

def frames():
    P = json.load(open(OUT + '/plan.json')); subprocess.run(['rm', '-rf', f'{OUT}/fr'])
    subprocess.run(['node', 'render.js', 'frames', f'{OUT}/fr', '30', '0', str(P['end'])], check=True)

def final():
    P = json.load(open(OUT + '/plan.json'))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/base.mp4', '-framerate', '30', '-i', f'{OUT}/fr/%05d.png', '-i', f'{OUT}/mix.wav',
                    '-filter_complex', '[0][1]overlay=0:0:shortest=1,format=yuv420p[v]', '-map', '[v]', '-map', '2:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
                    '-c:a', 'aac', '-b:a', '192k', '-t', str(P['end']), '../export/yone_short.mp4'], check=True)
    print('final ok')

{'plan': plan, 'base': base, 'mix': mix, 'frames': frames, 'final': final}[sys.argv[1]]()
