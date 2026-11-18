"""Yasuo story, part 2 (II. Ruzgar .. XI. Kapanis), placed after part 1 (build.py, 98.5 s).
Visuals are laid out on the narration's aligned word times (narr2.json) and the aligned KIN dialogue (dial2.json).
usage: python3 build2.py plan | base | mix | frames | final | join"""
import subprocess, sys, os, json
S = '/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad'
Y = S + '/yasuo'; AN = Y + '/anim'; OUT = Y + '/out2'; os.makedirs(OUT, exist_ok=True)
SEP = Y + '/sep/htdemucs'
NARR = json.load(open(Y + '/narr2.json')); DIAL = json.load(open(Y + '/dial2.json'))
XF = 0.5
GRADE = ('eq=contrast=1.08:saturation=0.88:gamma=0.97,'
         'colorbalance=rs=-0.04:gs=0.0:bs=0.05:rm=0.01:bm=-0.01:rh=0.05:gh=0.01:bh=-0.04,'
         'vignette=angle=PI/4.6,noise=alls=5:allf=t')
BOX = 'pad=1920:1080:0:132:black,setsar=1,format=yuv420p'
VID = {'K': Y + '/kin.mp4', 'A': Y + '/awaken.mp4', 'N': AN + '/noxus.mp4', 'P': AN + '/the_path.mp4', 'H': AN + '/here_tomorrow.mp4'}
CROP = {'K': 'crop=1920:816:0:132', 'A': 'crop=1920:816:0:132', 'N': 'scale=1920:816', 'P': 'crop=1920:816:0:132', 'H': 'crop=1920:816:0:132'}

def dl(i):  # dialogue line i -> (first word time, end time, words)
    w = DIAL[i]['words']; return w[0][1], w[-1][2], w

# Events.  N: (para, [clips], trans-in)   clip = (src, start, weight)  src in VID keys or an AI file name or 'BLACK'
#          D: (KIN from, KIN to, [(dial idx, display lines, position)], trans-in, ambience dB)
#          V: (src, from, to, trans-in, ambience dB)    (visual + KIN sound only)
EV = [
    # II. RUZGAR
    ('N', 0, [('placidium', 0, 6), ('H', 66.2, 5)], 'black'),
    ('N', 1, [('P', 31.0, 4), ('H', 27.5, 5), ('yasuo_sb', 0, 7)], 'x'),
    ('N', 2, [('H', 120.2, 5), ('K', 58.6, 2.4)], 'x'),
    # III. GOREV
    ('N', 3, [('N', 44.5, 3), ('A', 72.5, 2.2), ('A', 93.4, 2.4)], 'flash'),
    ('N', 4, [('A', 39.0, 4), ('K', 253.6, 3)], 'x'),
    ('D', 254.3, 285.4, [(0, ['SENİN YERİN BURASI,'], 'SKY'), (1, ["USTA SOUMA'NIN YANI."], 'L2'), (2, ['BENİ BUNUN İÇİN EĞİTTİ O.'], 'SKY'),
                          (3, ['YARDIMIMLA SAVAŞ BİTEBİLİR.'], 'SKY'), (4, ['SENİN VAZİFEN', 'BU OKULA.'], 'L2'), (5, ['USTANA.'], 'SKY'),
                          (6, ["IONIA'YA."], 'SKY'), (7, ['O ZAMAN GİDİP', 'ONU KORUMAM LAZIM.'], 'SKY'),
                          (8, ['SENİ YÜZÜSTÜ', 'BIRAKMAYACAĞIM,', 'YONE.'], 'R2'), (9, ['BEN SENİ', 'YÜZÜSTÜ', 'BIRAKMIŞIM BİLE.'], 'R2')], 'x', -14),
    ('N', 5, [('K', 286.0, 4), ('N', 220.0, 3), ('A', 98.6, 3)], 'x'),
    # IV. CESET
    ('N', 6, [('bloodmoon', 0, 5), ('K', 0.2, 2)], 'black'),
    ('N', 7, [('K', 2.3, 5), ('K', 7.3, 5)], 'x'),
    # V. AV
    ('N', 8, [('K', 11.4, 4), ('P', 136.5, 5)], 'x'),
    ('R', [(23, ['KARDEŞİM,', 'NE HALE GELDİN?']), (24, ['ANLATSAM,', 'DİNLER MİYDİN?']), (25, ['SUÇ İŞLEDİN,', 'ARANIYORSUN.']),
           (26, ['KATİL DEĞİLİM BEN.']), (27, ['YAPTIKLARININ', 'HESABINI VER.'])], ('P', 155.0), 'flash'),
    ('N', 9, [('K', 13.96, 3), ('K', 16.96, 3)], 'x'),
    # VI. DUELLO
    ('N', 10, [('K', 41.0, 9.5)], 'flash'),
    ('N', 11, [('K', 76.0, 5), ('K', 85.5, 2.6), ('P', 183.0, 4)], 'x'),
    ('N', 12, [('K', 96.04, 2.6), ('K', 98.8, 2.4), ('K', 101.3, 5)], 'x'),
    # VII. GERCEK
    ('N', 13, [('BLACK', 0, 1)], 'black'),
    ('N', 14, [('A', 78.0, 6), ('rivensplash2', 0, 6)], 'x'),
    ('N', 15, [('rivensplash1', 0, 6), ('placidium', 4.0, 4)], 'flash'),
    ('N', 16, [('K', 89.04, 1.75), ('K', 96.2, 3)], 'x'),
    # VIII. RIVEN
    ('N', 17, [('riven', 0, 10)], 'black'),
    ('N', 18, [('riven_sb', 0, 8), ('H', 171.0, 6)], 'x'),
    ('N', 19, [('H', 114.0, 5)], 'x'),
    # IX. RUH CICEGI
    ('N', 20, [('K', 121.0, 4), ('K', 129.5, 4.5)], 'black'),
    ('D', 203.4, 212.6, [(10, ['BIRAK SULAR', 'SENİ ARINDIRSIN.'], 'SKY'), (11, ['AKINTI TAŞIDIĞIN YÜKÜ', 'ALSIN GÖTÜRSÜN.'], 'SKY')], 'x', -14),
    ('N', 21, [('K', 304.0, 6), ('K', 310.0, 6)], 'x'),
    ('D', 316.9, 320.8, [(12, ['BAZEN İBLİSLERİMİZİ', 'BİZİM BULMAMIZ GEREKİR.'], 'BOT')], 'x', -14),
    ('V', 'K', 326.0, 334.0, 'x', -6),
    ('N', 22, [('K', 352.0, 5), ('K', 358.0, 4), ('yone_sb', 0, 5)], 'x'),
    ('V', 'K', 440.0, 452.0, 'x', -6),
    # X. HUKUM
    ('N', 23, [('K', 505.0, 4), ('K', 510.0, 4)], 'x'),
    ('D', 517.2, 551.4, [(13, ['İNTİKAMINI AL, KARDEŞİM.'], 'SKY'), (14, ['BELKİ SENİN HAKKIN ÖLÜM.'], 'SKY'), (15, ['AMA BENİM ELİMDEN DEĞİL.'], 'SKY'),
                          (16, ["O HALDE IONIA'DA", 'BANA BİR ŞEY KALMADI.'], 'SKY'), (17, ['RÜZGÂRIN BİLE', 'BİR YOLU VARDIR, KARDEŞİM.'], 'SKY'),
                          (18, ['ELVEDA, YONE.'], 'SKY'), (19, ["IONIA'NIN RUHU", 'SANA YOL GÖSTERSİN.'], 'SKY')], 'x', -14),
    ('N', 24, [('K', 551.4, 4), ('H', 150.0, 5)], 'x'),
    # XI. YENI YOL
    ('N', 25, [('K', 564.6, 3), ('bilgewater', 0, 4)], 'x'),
    ('D', 567.3, 574.3, [(20, ['GEÇMİŞE BAKMAK', 'KOLAY, DEĞİL Mİ?'], 'SKY'), (21, ['ASIL MESELE', 'OLACAKLARI GÖREBİLMEK.'], 'SKY')], 'x', -14),
    ('D', 597.8, 600.8, [(22, ['BENCE ORADA', 'ÇOK ŞEY BULACAĞIZ.'], 'SKY')], 'x', -14),
    ('N', 26, [('yone_dawnbringer', 0, 6)], 'black'),
]
LEAD = 0.45; TAIL = 0.65

def plan():
    t = 0.0; pieces = []; narr = []; dial = []; amb = []; texts = []; sfx = []
    for ev in EV:
        k = ev[0]
        if k == 'N':
            _, pi, clips, tr = ev; p = NARR[pi]
            dur = p['end'] - p['start'] + LEAD + TAIL
            if pi == 26: dur += 2.2
            narr.append((pi, t + LEAD)); tw = sum(c[2] for c in clips)
            for j, (src, ss, w) in enumerate(clips):
                pieces.append({'src': src, 'ss': ss, 'vis': dur * w / tw, 'tr': tr if j == 0 else 'x'})
            if pi == 13:  # black card: "SOUMA'YI OLDUREN / YASUO DEGILDI." on the narration words
                ws = p['words']; a = t + LEAD - p['start']
                w0 = next(x for x in ws if x[0].startswith("Souma")); w1 = next(x for x in ws if x[0].startswith('Yasuo'))
                texts.append([round(a + w0[1] - .03, 2), round(t + dur - .1, 2), 'SKY2', [["SOUMA'YI ÖLDÜREN", 130, 'C', 0], ['YASUO DEĞİLDİ.', 130, 'G', round(w1[1] - w0[1], 2)]]])
            if pi == 18:  # the judge's words
                ws = p['words']; a = t + LEAD - p['start']
                i0 = next(i for i, x in enumerate(ws) if x[0].startswith('Sorumluluğu')); i1 = next(i for i, x in enumerate(ws) if x[0].startswith('Kendini'))
                s0 = a + ws[i0][1]; texts.append([round(s0 - .03, 2), round(a + ws[i1][1] - .1, 2), 'SKY', [['SORUMLULUĞU KABUL ETMEK,', 100, 'C', 0], ['KEFARETİN İLK ADIMIDIR.', 100, 'G', round(ws[i0 + 3][1] - ws[i0][1], 2)]]])
                s1 = a + ws[i1][1]; texts.append([round(s1 - .03, 2), round(t + dur - .1, 2), 'SKY', [['KENDİNİ AFFETMEK', 100, 'C', 0], ['İSE İKİNCİSİ.', 100, 'G', round(ws[i1 + 2][1] - ws[i1][1], 2)]]])
            if pi == 26:
                ws = p['words']; a = t + LEAD - p['start']
                texts.append([round(a + ws[0][1] - .03, 2), round(t + dur, 2), 'SKY', [['PEKİ SEN OLSAN,', 120, 'C', 0], ['KARDEŞİNİ AFFEDER MİYDİN?', 120, 'G', round(ws[3][1] - ws[0][1], 2)]]])
            if tr == 'flash': sfx.append(('slash_1.mp3', t - 0.08, -12))
            t += dur
        elif k in ('D', 'V'):
            if k == 'D': _, a, b, lines, tr, g = ev; src = 'K'
            else: _, src, a, b, tr, g = ev; lines = []
            pieces.append({'src': src, 'ss': a, 'vis': b - a, 'tr': tr})
            amb.append((a, b, t, g))
            if k == 'D': dial.append(('K', a, b, t))
            for (di, disp, pos) in lines:
                w0, w1, ws = dl(di); st = t + w0 - a - .03
                # each display line starts on its first word
                rows = []; wi = 0
                for li, txt in enumerate(disp):
                    n = len(txt.split()); rows.append([txt, 110 if len(disp) > 1 else 120, 'C' if li < len(disp) - 1 else 'G', round(ws[min(wi, len(ws) - 1)][1] - w0, 2)])
                    wi += n
                texts.append([round(st, 2), round(t + w1 - a + .45, 2), pos, rows])
            if tr == 'flash': sfx.append(('slash_1.mp3', t - 0.08, -12))
            t += b - a
        elif k == 'R':  # game voice lines over a The Path shot
            _, lines, (src, ss), tr = ev
            r0 = DIAL[lines[0][0]]['words'][0][1] - 0.5; r1 = DIAL[lines[-1][0]]['words'][-1][2] + 0.6
            pieces.append({'src': src, 'ss': ss, 'vis': r1 - r0, 'tr': tr}); dial.append(('R', r0, r1, t))
            for di, disp in lines:
                w0, w1, ws = dl(di); rows = []; wi = 0
                for li, txt in enumerate(disp):
                    rows.append([txt, 120, 'C' if li < len(disp) - 1 else 'G', round(ws[min(wi, len(ws) - 1)][1] - w0, 2)]); wi += len(txt.split())
                texts.append([round(t + w0 - r0 - .03, 2), round(t + w1 - r0 + .35, 2), 'SKY', rows])
            if tr == 'flash': sfx.append(('kin_kilic.wav', t - 0.3, -10))
            t += r1 - r0
    # overlaps must never clash
    texts.sort(key=lambda x: x[0])
    for i in range(len(texts) - 1):
        if texts[i][1] > texts[i + 1][0] - .05: texts[i][1] = round(texts[i + 1][0] - .05, 2)
    json.dump({'pieces': pieces, 'narr': narr, 'dial': dial, 'amb': amb, 'texts': texts, 'sfx': sfx, 'end': round(t, 2)}, open(OUT + '/plan.json', 'w'), ensure_ascii=False, indent=0)
    open('t2.js', 'w').write('window.T2=' + json.dumps(texts, ensure_ascii=False) + ';')
    print('end', round(t, 2), 'pieces', len(pieces), 'texts', len(texts))

def piece(i, p, last):
    L = p['vis'] + (0 if last else XF); n = round(L * 30); src = p['src']; ss = p['ss']
    import hashlib; h = hashlib.md5(f'{src}|{ss}|{n}|{i % 2}'.encode()).hexdigest()[:10]; o = f'{OUT}/c_{h}.mp4'
    if os.path.exists(o): return o
    if src == 'BLACK':
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1920x1080:r=30', '-vf', 'format=yuv420p']
    elif src in VID:
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', VID[src], '-vf', f'fps=30,{CROP[src]},{GRADE},{BOX}']
    else:  # AI animated splash: slow push in or out
        z0, z1 = (1.0, 1.06) if i % 2 == 0 else (1.06, 1.0)
        cmd = ['ffmpeg', '-v', 'error', '-y', '-stream_loop', '-1', '-ss', str(ss), '-i', f'{AN}/{src}.mp4', '-vf',
               f"fps=30,scale=3840:2160:flags=lanczos,crop=3840:1632:0:(ih-1632)*0.35,zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x816:fps=30,eq=brightness=-0.04,{GRADE},{BOX}"]
    subprocess.run(cmd + ['-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '15', '-pix_fmt', 'yuv420p', o], check=True)
    return o

def base():
    P = json.load(open(OUT + '/plan.json')); ps = P['pieces']
    files = [piece(i, p, i == len(ps) - 1) for i, p in enumerate(ps)]
    # chain in chunks of 12 to keep the graph small, then join chunks the same way
    def chain(fs, trs, vis, out):
        inp = []
        for f in fs: inp += ['-i', f]
        fc = [f'[{i}:v]settb=AVTB,setpts=PTS-STARTPTS[i{i}]' for i in range(len(fs))]; cur = '[i0]'; off = 0
        for i in range(1, len(fs)):
            off += vis[i - 1]; tr = {'x': 'fade', 'flash': 'fadewhite', 'black': 'fadeblack'}[trs[i]]
            fc.append(f'{cur}[i{i}]xfade=transition={tr}:duration={XF}:offset={off:.3f}[x{i}]'); cur = f'[x{i}]'
        subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', cur, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '15', '-pix_fmt', 'yuv420p', out], check=True)
    C = 12; chunks = []
    for c in range(0, len(ps), C):
        sub = list(range(c, min(c + C, len(ps)))); o = f'{OUT}/chunk{c // C}.mp4'
        last = sub[-1] == len(ps) - 1
        chain([files[i] for i in sub], [ps[i]['tr'] for i in sub], [ps[i]['vis'] for i in sub], o)
        chunks.append((o, ps[sub[0]]['tr'], sum(ps[i]['vis'] for i in sub)))
    chain([c[0] for c in chunks], [c[1] for c in chunks], [c[2] for c in chunks], f'{OUT}/base.mp4')
    print('base ok')

def mix():
    P = json.load(open(OUT + '/plan.json')); END = P['end']; inp = []; fc = []; ii = 0; vox = []; bed = []
    for pi, at in P['narr']:
        p = NARR[pi]; a = p['start'] - 0.08; L = p['end'] - p['start'] + 0.35
        if pi == 4: L = 6.75; inp += ['-i', '../ses/anlatim_2_p4.wav']   # "Yasuo'ya" with the mid-word pause cut out
        else: inp += ['-ss', f'{a:.3f}', '-t', f'{L:.3f}', '-i', '../ses/anlatim_2.mp3']
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-16:TP=-2:LRA=7,aresample=48000,volume=7.5dB,afade=t=in:d=0.03,afade=t=out:st={L - 0.12:.3f}:d=0.12,adelay={int((at - 0.08) * 1000)}:all=1,apad=whole_dur={END}[a{ii}]'); vox.append(f'[a{ii}]'); ii += 1
    for src, a, b, at in P['dial']:
        stem = f'{SEP}/kinfull/vocals.wav' if src == 'K' else f'{SEP}/repfull/vocals.wav'; g = 9 if src == 'K' else 6
        inp += ['-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', stem]
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-17:TP=-2:LRA=7,aresample=48000,volume=6dB,afade=t=in:d=0.05,afade=t=out:st={b - a - 0.3:.3f}:d=0.3,adelay={int(at * 1000)}:all=1,apad=whole_dur={END}[a{ii}]'); vox.append(f'[a{ii}]'); ii += 1
    fc.append(''.join(vox) + f'amix=inputs={len(vox)}:normalize=0,asplit[vv][sc]')
    for a, b, at, g in P['amb']:
        inp += ['-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', f'{SEP}/kinfull/no_vocals.wav']
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,afade=t=in:d=0.5,afade=t=out:st={b - a - 0.5:.3f}:d=0.5,adelay={int(at * 1000)}:all=1,apad=whole_dur={END}[a{ii}]'); bed.append(f'[a{ii}]'); ii += 1
    for fn, at, end, off, g in MUSIC(P):
        L = end - at
        inp += ['-ss', str(off), '-i', f'../ses/{fn}']
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{L:.3f},volume={g}dB,afade=t=in:d=1.5,afade=t=out:st={L - 2.0:.3f}:d=2.0,adelay={int(at * 1000)}:all=1,apad=whole_dur={END}[a{ii}]'); bed.append(f'[a{ii}]'); ii += 1
    fc.append(''.join(bed) + f'amix=inputs={len(bed)}:normalize=0[b0]')
    fc.append('[b0][sc]sidechaincompress=threshold=0.025:ratio=6:attack=15:release=450[bed]')
    lab = '[vv][bed]'; cnt = 2
    for j, (fn, at, g) in enumerate(P['sfx']):
        inp += ['-i', f'../ses/{fn}']
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,adelay={int(max(at, 0) * 1000)}:all=1[s{j}]'); lab += f'[s{j}]'; ii += 1; cnt += 1
    fc.append(f'{lab}amix=inputs={cnt}:normalize=0:duration=longest,atrim=0:{END},afade=t=in:d=0.5,afade=t=out:st={END - 2}:d=2,loudnorm=I=-15:TP=-1.5:LRA=11[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', f'{OUT}/mix.wav'], check=True)
    print('mix ok')

def MUSIC(P):
    # chapter start times from the plan: II at 0, III at the Noxus para, VI at the duel, IX at the festival
    starts = {}
    for pi, at in P['narr']: starts[pi] = at - LEAD
    t3, t6, t9, end = starts[3], starts[10], starts[20], P['end']
    return [('muzik_cocukluk_nv.wav', 0.0, t3 + 0.6, 0.0, -6),   # II: the childhood theme carries on
            ('muzik_savas.mp3', t3, t6 + 0.6, 0.0, -6),           # III-V: war, then cold and empty
            ('muzik_huzun.mp3', t6, t9 + 0.6, 0.0, -6),           # VI-VIII: grief
            ('muzik_mistik.mp3', t9, end, 4.0, -6)]               # IX-XI: ethereal, spirit battle, finale

def frames():
    P = json.load(open(OUT + '/plan.json'))
    subprocess.run(['rm', '-rf', f'{OUT}/fr'])
    subprocess.run(['node', 'render.js', 'frames', f'{OUT}/fr', '30', '0', str(P['end'])], check=True, env=dict(os.environ, PAGE='overlay2.html'))

def final():
    P = json.load(open(OUT + '/plan.json'))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/base.mp4', '-framerate', '30', '-i', f'{OUT}/fr/%05d.png', '-i', f'{OUT}/mix.wav',
                    '-filter_complex', '[0][1]overlay=0:0:shortest=1,format=yuv420p[v]', '-map', '[v]', '-map', '2:a',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-b:a', '192k', '-t', str(P['end']), f'{OUT}/part2.mp4'], check=True)
    print('final ok')

def join():
    # part 1 (fades to black at its end) + part 2 (opens from black) back to back
    open(f'{OUT}/list.txt', 'w').write(f"file '{os.path.abspath('../export/yasuo_ilk100.mp4')}'\nfile '{OUT}/part2.mp4'\n")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list.txt', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
                    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '../export/yasuo_tam.mp4'], check=True)
    print('join ok')

{'plan': plan, 'base': base, 'mix': mix, 'frames': frames, 'final': final, 'join': join}[sys.argv[1]]()
