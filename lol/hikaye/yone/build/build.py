"""Yone story (sequel to the Yasuo video). Same style as yasuo/build/build2.py: 2.35 letterbox, grade,
visuals laid out on the aligned narration (narr.json), word-by-word quotes.
usage: python3 build.py plan | sheet | base | mix | frames | final"""
import subprocess, sys, os, json, hashlib
S = '/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad'
Y = S + '/yasuo'; OUT = S + '/yone/out'; os.makedirs(OUT, exist_ok=True)
ANS = [S + '/yone/anim', Y + '/anim']
SEP = Y + '/sep/htdemucs'
NARR = {p['row']: p for p in json.load(open('narr.json'))}
REPW = json.load(open('rep_words.json')); REPV = S + '/yone/rep/yone_rep.mp4'  # official Turkish Yone voice lines
YS = '../../yasuo/ses/'; MS = '../ses/'
XF = 0.5
GRADE = ('eq=contrast=1.08:saturation=0.88:gamma=0.97,'
         'colorbalance=rs=-0.04:gs=0.0:bs=0.05:rm=0.01:bm=-0.01:rh=0.05:gh=0.01:bh=-0.04,'
         'vignette=angle=PI/4.6,noise=alls=5:allf=t')
BOX = 'pad=1920:1080:0:132:black,setsar=1,format=yuv420p'
VID = {'K': Y + '/kin.mp4', 'N': Y + '/anim/noxus.mp4', 'P': Y + '/anim/the_path.mp4', 'H': Y + '/anim/here_tomorrow.mp4'}
CROP = {'K': 'crop=1920:816:0:132', 'N': 'scale=1920:816', 'P': 'crop=1920:816:0:132', 'H': 'crop=1920:816:0:132'}

def ai(name):
    for d in ANS:
        if os.path.exists(f'{d}/{name}.mp4'): return f'{d}/{name}.mp4'
    raise FileNotFoundError(name)

# N: (row, [(src, start, weight)], transition in, extra tail)   T: title   V: KIN visual + sound only
# none of the shots below were used in the Yasuo video (checked against its plan)
EV = [
    # SOGUK ACILIS
    ('N', 1, [('P', 4.0, 1)], 'black', 0.3),
    ('T', 'P', 168.0, 4.6),
    # I. KORUYUCU
    ('N', 3, [('yone_battleacademia', 0, 1)], 'black', 0),
    ('Q', 'onur', [['BİR ZAMANLAR ONUR', 'HER ŞEYİN ÜZERİNDEYDİ.']], ('P', 22.0), 'x', 0.8),
    ('N', 4, [('K', 135.5, 6), ('H', 72.6, 6)], 'x', 0),
    ('N', 5, [('H', 27.0, 3), ('H', 36.0, 3.5), ('H', 78.5, 4)], 'x', 0),
    ('N', 6, [('yone_tohum', 0, 1)], 'x', 0.4),
    ('N', 7, [('H', 112.6, 5), ('P', 14.0, 6)], 'x', 0),
    ('N', 8, [('yone_sb', 5, 5), ('K', 143.0, 6)], 'x', 0),
    # II. KILIFSIZ BIR KILIC
    ('N', 9, [('N', 100.0, 5), ('N', 124.0, 5)], 'black', 0),
    ('N', 10, [('H', 160.5, 4), ('K', 292.5, 5)], 'x', 0),
    ('N', 11, [('yone_inkshadow', 0, 1)], 'x', 0),
    ('N', 12, [('K', 345.0, 4), ('K', 336.0, 4)], 'x', 0),
    ('N', 13, [('BLACK', 0, 1)], 'black', 0.5),
    ('N', 14, [('K', 52.3, 5.5), ('K', 63.0, 3.5)], 'x', 0),
    ('Q', 'oldu', [['YAŞARKEN BİRBİRİMİZİN', 'ELİNDE ÖLDÜK.']], ('BLACK', 0), 'black', 0.8),
    # III. RUHLAR DUNYASI
    ('N', 15, [('P', 36.0, 1)], 'flash', 0),
    ('Q', 'huzur', [['ÖLÜM HUZUR', 'GETİRİR SANMIŞTIM.'], ['NE BÜYÜK SAFLIK.']], ('P', 46.5), 'x', 0.8),
    ('N', 16, [('P', 62.0, 7), ('P', 88.0, 7)], 'x', 0),
    ('N', 17, [('P', 100.0, 1)], 'x', 0),
    ('N', 18, [('P', 124.0, 4), ('P', 174.0, 4.5)], 'x', 0),
    ('N', 19, [('BLACK', 0, 1)], 'black', 3.2),
    # IV. MASKE
    ('N', 20, [('K', 425.5, 1)], 'black', 0),
    ('Q', 'cevirdi', [['ÖLÜM BENİ', 'GERİ ÇEVİRDİ.']], ('K', 435.0), 'x', 0.8),
    ('N', 21, [('K', 374.0, 4), ('yone_maskedjustice', 0, 6)], 'x', 0),
    ('Q', 'tanidi', [['RUHLAR ALEMİNDE KARŞIMA ÇIKTIĞINDA', 'ŞU YÜZÜMDEKİ AZAKANA', 'BENİ TANIYORDU.']], ('K', 378.0), 'x', 0.8),
    ('N', 22, [('K', 417.0, 5), ('K', 466.0, 10)], 'x', 0),
    ('Q', 'cizgi', [['AZAKANALARIN HER ÖZELLİĞİ', 'BİR ÇİZGİDİR.'], ['ÇİZGİLER BİR ARAYA GELİP', 'GERÇEK ADLARINI İFŞA EDER.']], ('P', 129.0), 'x', 0.8),
    # V. ANDU
    ('N', 23, [('K', 385.5, 6), ('yone_severed', 0, 6)], 'black', 0),
    ('N', 24, [('yone_varsayilan', 0, 1)], 'x', 0),
    ('N', 25, [('K', 364.0, 1)], 'x', 0.3),
    ('N', 26, [('H', 136.0, 5), ('H', 146.0, 5)], 'x', 0),
    ('N', 27, [('K', 395.0, 1)], 'flash', 0),
    ('Q', 'korku', [['KORKUNUN ADI VARSA,', 'GÜCÜ YOKTUR.']], ('K', 409.0), 'x', 0.8),
    ('N', 28, [('K', 300.5, 1)], 'x', 0),
    ('N', 29, [('P', 143.0, 1)], 'x', 0.3),
    ('N', 30, [('yone_severed', 6.5, 1)], 'x', 0),
    ('N', 31, [('P', 201.0, 4.5), ('P', 149.8, 5.5)], 'x', 0.4),
    ('N', 32, [('K', 500.0, 1)], 'x', 0.6),
    # VI. KARDESE DONUS
    ('N', 33, [('K', 476.0, 1)], 'black', 0),
    ('Q', 'kardes', [['KARDEŞİM...'], ['YOLLARIMIZ YİNE KESİŞTİ.'], ['KILIÇLARIMIZ DA', 'KESECEK Mİ?']], ('K', 487.0), 'x', 0.8),
    ('V', 'K', 455.5, 466.0, 'x', -6),
    ('N', 35, [('yone_login', 45, 1)], 'x', 0),
    # KAPANIS
    ('N', 36, [('H', 152.5, 6), ('K', 603.0, 5)], 'x', 0),
    ('Q', 'ruzgar', [['ESKİDEN HAYLAZ', 'RÜZGARIN PEŞİNDEYDİM.'], ['ARTIK KARANLIK', 'FIRTINAYI AVLIYORUM.']], ('P', 56.0), 'x', 0.8),
    ('N', 37, [('BLACK', 0, 1)], 'black', 1.2),
    ('N', 38, [('K', 576.5, 4), ('riven_championship', 8, 6)], 'x', 0.2),
    ('Q', 'riven', [['CÜRÜM PEŞİNİ', 'BIRAKMIYOR, RIVEN.'], ['KENDİNİ AFFET.']], ('K', 584.0), 'x', 1.8),
]
LEAD = 0.45; TAIL = 0.65

def tr_up(s): return s.replace('i', 'İ').replace('ı', 'I').upper()

# on-screen quotes: row -> [(first word index, display lines, size, position)]; lines must hold exactly the spoken words
QUOTES = {
    6: [(0, ['BİR TOHUM SADECE BİR TOHUMDUR.', 'AMA ZAMAN VERİLİRSE,', 'İÇİNDE TAŞIDIĞI GÜZELLİK', 'GÖRÜLEBİLİR.'], 92, 'SKY')],
    13: [(0, ['YARIN İLK IŞIKLA YOLA ÇIKACAĞIM.', 'KILIFSIZ BİR KILICI YAKALAMAK İÇİN:', 'KARDEŞİM YASUO.'], 96, 'SKY2')],
    25: [(0, ['KORKMAN GEREKEN', 'BEN DEĞİLİM.'], 120, 'SKY')],
    27: [(4, ["TAAN KO'AU."], 130, 'SKY')],
    29: [(0, ['SADECE SENİN ACILARINLA', 'BESLENEN BİR KABUS.'], 100, 'SKY'), (6, ['AMA ARTIK SENİ', 'O TANIMLAMIYOR.'], 100, 'SKY')],
    31: [(0, ['SEVDİKLERİMİZ, BİZİ EN ÇOK', 'YARALAYAN ŞEYLERİ SÖYLER.'], 96, 'SKY'),
         (7, ['UMUTSUZLUK AKLIN KILIĞINA GİRER,', 'AMA BİZE SADECE KENDİMİZİN', 'ÇARPIK BİR YANSIMASINI GÖSTERİR.'], 88, 'SKY')],
    32: [(8, ['İYİ OLACAKSIN,', 'ANDU.'], 120, 'SKY')],
    37: [(0, ['PEKİ O KAHKAHA', 'KİME AİT?'], 120, 'SKY2'), (5, ['VE YÜZÜNDEKİ MASKE,', 'BİR GÜN ONU DA YUTACAK MI?'], 110, 'SKY2')],
    38: [(13, ['NOXUSLU ASKER:', 'RIVEN.'], 130, 'SKY')],
}
LAUGH = {16: 'kahkaha', 19: 'kahkahaydı.', 37: None}

def words_rows(disp, ws, st, z):
    rows = []; wi = 0
    assert sum(len(l.split()) for l in disp) == len(ws), (disp, [w[0] for w in ws])
    for li, l in enumerate(disp):
        words = [[w, round(ws[wi + m][1] - st, 3)] for m, w in enumerate(l.split())]; wi += len(words)
        rows.append([words, z, 'C' if li < len(disp) - 1 else 'G'])
    return rows

def plan():
    t = 0.0; pieces = []; narr = []; amb = []; texts = []; sfx = []; chap = {}; reps = []
    def add_piece(src, ss, vis, tr):
        if pieces and pieces[-1]['src'] == src and src in VID:
            q = pieces[-1]
            if q['ss'] <= ss <= q['ss'] + q['vis'] + XF + 1.5:
                q['vis'] += vis; return
        pieces.append({'src': src, 'ss': ss, 'vis': vis, 'tr': tr})
    for ev in EV:
        k = ev[0]
        if k == 'N':
            _, r, clips, tr, extra = ev; p = NARR[r]; chap[r] = t
            dur = p['end'] - p['start'] + LEAD + TAIL + extra
            narr.append((r, t + LEAD)); tw = sum(c[2] for c in clips)
            for j, (src, ss, w) in enumerate(clips): add_piece(src, ss, dur * w / tw, tr if j == 0 else 'x')
            a = t + LEAD - p['start']; ws = p['words']
            qs = QUOTES.get(r, [])
            for qi, (i0, disp, z, pos) in enumerate(qs):
                n = sum(len(l.split()) for l in disp); st = a + ws[i0][1] - .03
                end = (a + ws[qs[qi + 1][0]][1] - .1) if qi + 1 < len(qs) else min(t + dur - .1, a + ws[i0 + n - 1][2] + 2.2)
                texts.append([round(st, 3), round(end, 2), pos, words_rows(disp, [(w[0], a + w[1], a + w[2]) for w in ws[i0:i0 + n]], st, z)])
            if r in LAUGH:
                key = LAUGH[r]
                at = a + next(w[2] for w in ws if w[0] == key) + 0.15 if key else t + 0.2
                sfx.append(('kahkaha.mp3', at, -9 if key else -12))
            if tr == 'flash': sfx.append(('slash_1.mp3', t + 0.12, -12))
            t += dur
        elif k == 'T':
            _, src, ss, L = ev; add_piece(src, ss, L, 'x')
            texts.append([round(t + 0.35, 3), round(t + L - 0.2, 2), 'SKY2', [['YONE', 220, 'G', 0, 'slam'], ['ÖLDÜKTEN SONRA NE OLDU?', 96, 'C', 0.55, None]]])
            sfx.append(('impact_kucuk.wav', t + 0.3, -11)); chap['T'] = t
            t += L
        elif k == 'Q':  # Yone's own voice line, word-by-word text
            _, key, blocks, (src, ss), tr, tail = ev; ws = REPW[key]
            r0 = ws[0][1] - 0.5; r1 = ws[-1][2] + tail
            add_piece(src, ss, r1 - r0, tr); reps.append((r0, r1, t))
            wi = 0
            for bi, disp in enumerate(blocks):
                n = sum(len(l.split()) for l in disp); bw = ws[wi:wi + n]; st = t + bw[0][1] - r0 - .03
                end = t + bw[-1][2] - r0 + (0.6 if bi + 1 < len(blocks) else min(tail, 1.2))
                texts.append([round(st, 3), round(end, 2), 'SKY', words_rows(disp, [(w[0], t + w[1] - r0, t + w[2] - r0) for w in bw], st, 110 if len(disp) > 1 else 120)])
                wi += n
            assert wi == len(ws), key
            t += r1 - r0
        elif k == 'V':
            _, src, a0, b0, tr, g = ev
            add_piece(src, a0, b0 - a0, tr); amb.append((a0, b0, t, g)); t += b0 - a0
    texts.sort(key=lambda x: x[0])
    for i in range(len(texts) - 1):
        if texts[i][1] > texts[i + 1][0] - .05: texts[i][1] = round(texts[i + 1][0] - .05, 2)
    json.dump({'pieces': pieces, 'narr': narr, 'reps': reps, 'amb': amb, 'texts': texts, 'sfx': sfx, 'chap': chap, 'end': round(t, 2)},
              open(OUT + '/plan.json', 'w'), ensure_ascii=False, indent=0)
    open('t.js', 'w').write('window.T2=' + json.dumps(texts, ensure_ascii=False) + ';')
    print('end', round(t, 2), 'pieces', len(pieces), 'texts', len(texts))
    tt = 0
    for i, p in enumerate(pieces): print(i, f'{tt:7.2f}', p['src'], p['ss'], round(p['vis'], 2), p['tr']); tt += p['vis']

def piece(i, p, last):
    L = p['vis'] + (0 if last else XF); n = round(L * 30); src = p['src']; ss = p['ss']
    h = hashlib.md5(f'{src}|{ss}|{n}|{i % 2}'.encode()).hexdigest()[:10]; o = f'{OUT}/c_{h}.mp4'
    if os.path.exists(o): return o
    if src == 'BLACK':
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1920x1080:r=30', '-vf', 'format=yuv420p']
    elif src in VID:
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', VID[src], '-vf', f'fps=30,{CROP[src]},{GRADE},{BOX}']
    else:  # animated splash: slow push in/out; slowed down smoothly if shorter than the shot (no loop)
        z0, z1 = (1.0, 1.06) if i % 2 == 0 else (1.06, 1.0); f_ = ai(src)
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f_], capture_output=True, text=True).stdout)
        avail = dur - ss - 0.08; f = max(1.0, L / avail)
        slow = f'setpts={f:.4f}*PTS,minterpolate=fps=30:mi_mode=blend,' if f > 1.0 else ''
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', f_, '-vf',
               f"{slow}fps=30,scale=3840:2160:flags=lanczos,crop=3840:1632:0:(ih-1632)*0.35,zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x816:fps=30,eq=brightness=-0.04,{GRADE},{BOX}"]
    subprocess.run(cmd + ['-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '15', '-pix_fmt', 'yuv420p', o], check=True)
    return o

def sheet():
    # one still from the middle of every piece, labelled, to check the shots before the full render
    P = json.load(open(OUT + '/plan.json')); ps = P['pieces']; os.makedirs(OUT + '/sh', exist_ok=True)
    for i, p in enumerate(ps):
        o = f'{OUT}/sh/{i:02d}.jpg'; m = p['ss'] + p['vis'] / 2
        src = VID.get(p['src']) or (ai(p['src']) if p['src'] != 'BLACK' else None)
        if src is None: subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=384x216', '-frames:v', '1', o]); continue
        if p['src'] not in VID: m = min(m, 9.5)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(m), '-i', src, '-vf', f"scale=384:216,drawtext=text='{i} {p['src']} {p['ss']}':fontcolor=yellow:fontsize=20:x=4:y=4", '-frames:v', '1', o])
    subprocess.run(f"ffmpeg -v error -y -pattern_type glob -i '{OUT}/sh/*.jpg' -vf tile=8x{(len(ps) + 7) // 8} -frames:v 1 {OUT}/sheet.jpg", shell=True)

def base():
    P = json.load(open(OUT + '/plan.json')); ps = P['pieces']
    files = [piece(i, p, i == len(ps) - 1) for i, p in enumerate(ps)]
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
        chain([files[i] for i in sub], [ps[i]['tr'] for i in sub], [ps[i]['vis'] for i in sub], o)
        chunks.append((o, ps[sub[0]]['tr'], sum(ps[i]['vis'] for i in sub)))
    chain([c[0] for c in chunks], [c[1] for c in chunks], [c[2] for c in chunks], f'{OUT}/base.mp4')
    print('base ok')

def MUSIC(P):
    c = P['chap']; end = P['end']
    return [('muzik_karanlik.mp3', 0.0, c['T'] + 0.4, 25.0, -7),        # cold open, cut under the title impact
            ('muzik_cocukluk_nv.wav', c[3] - 0.3, c[9] + 0.6, 0.0, -6),  # I. childhood
            ('muzik_savas.mp3', c[9], c[15] + 0.6, 0.0, -6),           # II. war, the hunt, the duel
            ('muzik_mistik.mp3', c[15], c[23] + 0.6, 4.0, -6),         # III-IV. spirit world, the mask
            ('muzik_huzun.mp3', c[23], c[33] + 0.6, 0.0, -6),          # V. Andu
            ('muzik_karanlik.mp3', c[33], end, 0.0, -6)]               # VI + closing

def mix():
    P = json.load(open(OUT + '/plan.json')); END = P['end']; inp = []; fc = []; ii = 0; vox = []; bed = []
    def gain(f, ss, L, target):
        r = subprocess.run(['ffmpeg', '-v', 'info', '-ss', f'{ss:.3f}', '-t', f'{L:.3f}', '-i', f, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
        I = float([l for l in r.splitlines() if ' I:' in l][-1].split()[1]); return round(target - I, 2)
    f = MS + 'anlatim.mp3'
    for r, at in P['narr']:
        p = NARR[r]; a = p['start'] - 0.08; L = p['end'] - p['start'] + 0.35
        g = gain(f, a, L, -14.5)
        inp += ['-ss', f'{a:.3f}', '-t', f'{L:.3f}', '-i', f]
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,afade=t=in:d=0.03,afade=t=out:st={L - 0.12:.3f}:d=0.12,adelay={int((at - 0.08) * 1000)}:all=1,apad=whole_dur={END}[a{ii}]'); vox.append(f'[a{ii}]'); ii += 1
    for a, b, at in P['reps']:
        g = gain(REPV, a, b - a, -15.0)
        inp += ['-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', REPV]
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,afade=t=in:d=0.05,afade=t=out:st={b - a - 0.3:.3f}:d=0.3,adelay={int(at * 1000)}:all=1,apad=whole_dur={END}[a{ii}]'); vox.append(f'[a{ii}]'); ii += 1
    fc.append(''.join(vox) + f'amix=inputs={len(vox)}:normalize=0,asplit[vv][sc]')
    for a, b, at, g in P['amb']:
        inp += ['-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', f'{SEP}/kinfull/no_vocals.wav']
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,afade=t=in:d=0.5,afade=t=out:st={b - a - 0.5:.3f}:d=0.5,adelay={int(at * 1000)}:all=1,apad=whole_dur={END}[a{ii}]'); bed.append(f'[a{ii}]'); ii += 1
    for fn, at, end, off, g in MUSIC(P):
        L = end - at
        inp += ['-ss', str(off), '-i', YS + fn]
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{L:.3f},volume={g}dB,afade=t=in:d=1.5,afade=t=out:st={L - 2.0:.3f}:d=2.0,adelay={int(at * 1000)}:all=1,apad=whole_dur={END}[a{ii}]'); bed.append(f'[a{ii}]'); ii += 1
    fc.append(''.join(bed) + f'amix=inputs={len(bed)}:normalize=0[b0]')
    fc.append('[b0][sc]sidechaincompress=threshold=0.025:ratio=6:attack=15:release=450[bed]')
    lab = '[vv][bed]'; cnt = 2
    for j, (fn, at, g) in enumerate(P['sfx']):
        inp += ['-i', (MS if fn == 'kahkaha.mp3' else YS) + fn]
        fc.append(f'[{ii}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,adelay={int(max(at, 0) * 1000)}:all=1[s{j}]'); lab += f'[s{j}]'; ii += 1; cnt += 1
    fc.append(f'{lab}amix=inputs={cnt}:normalize=0:duration=longest,atrim=0:{END},afade=t=out:st={END - 1.5}:d=1.5,loudnorm=I=-15:TP=-1.5:LRA=11[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', f'{OUT}/mix.wav'], check=True)
    print('mix ok')

def frames():
    P = json.load(open(OUT + '/plan.json'))
    subprocess.run(['rm', '-rf', f'{OUT}/fr'])
    subprocess.run(['node', 'render.js', 'frames', f'{OUT}/fr', '30', '0', str(P['end'])], check=True, env=dict(os.environ, PAGE='overlay.html'))

def final():
    P = json.load(open(OUT + '/plan.json'))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/base.mp4', '-framerate', '30', '-i', f'{OUT}/fr/%05d.png', '-i', f'{OUT}/mix.wav',
                    '-filter_complex', '[0][1]overlay=0:0:shortest=1,fade=t=in:d=0.8,format=yuv420p[v]', '-map', '[v]', '-map', '2:a',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-b:a', '192k', '-t', str(P['end']), '../export/yone_tam.mp4'], check=True)
    print('final ok')

{'plan': plan, 'sheet': sheet, 'base': base, 'mix': mix, 'frames': frames, 'final': final}[sys.argv[1]]()
