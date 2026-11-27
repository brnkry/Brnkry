# 9:16 Shorts version of the Bäke film (engine from Ehrler) (Facebook long version, Shorts/Reels short version).
# Portraits fill the frame (faces in the upper part), landscape photos and archive films sit full width slightly above the centre
# on a blurred, darkened copy of themselves (nothing is cropped away). Subtitles in the Shorts safe zone, labels below the top UI.
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bb as ee
from bb import E, U, FPS, XF, run, ease, load_img, VID, label_png as _lp
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
WV, HV = 1080, 1920
CY = 0.42                                   # vertical centre of landscape material
def pipe(out):
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WV}x{HV}', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out + '.part.mp4'], stdin=subprocess.PIPE)
IMGCX = {}                                   # set by ks.py
def frame_v(im, key=None):
    """9:16 canvas at 2x: every photo fills the frame; landscape photos are cropped around their subject (IMGCX), portraits keep the upper part"""
    w, h = im.size; W2, H2 = WV * 2, HV * 2
    s = max(W2 / w, H2 / h); im2 = im.resize((int(w * s + 1), int(h * s + 1)), Image.LANCZOS)
    if w / h <= 0.8:
        x0 = (im2.width - W2) // 2; y0 = int((im2.height - H2) * 0.25)
    else:
        cx = next((v for k, v in IMGCX.items() if (k == key) or (isinstance(k, str) and isinstance(key, str) and k in key)), 0.5)
        x0 = int(min(max(cx * im2.width - W2 / 2, 0), im2.width - W2)); y0 = (im2.height - H2) // 2
    return im2.crop((x0, y0, x0 + W2, y0 + H2))
def img_shot(src, d, out, zin):
    S = frame_v(load_img(src), src); n = int(round(d * FPS)); p = pipe(out); z0, z1 = (1.0, 1.07) if zin else (1.07, 1.0)
    for f in range(n):
        z = z0 + (z1 - z0) * (ease(f / max(1, n - 1)) * 0.7 + f / max(1, n - 1) * 0.3); a = 2 / z
        p.stdin.write(S.transform((WV, HV), Image.AFFINE, (a, 0, WV - a * WV / 2, 0, a, HV * CY * 2 - a * HV * CY), resample=Image.BILINEAR).tobytes())
    p.stdin.close(); p.wait(); os.replace(out + '.part.mp4', out)
CX = {}                                      # set by ks.py: (clip, start) -> horizontal centre
def vid_shot(key, ss, d, out):
    """archive film zoomed to fill 9:16: the window (full height) sits on the subject of the shot"""
    src, cr = VID[key]
    if cr: x, y, w, h = cr
    else:
        w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', src],
                                       capture_output=True, text=True).stdout.strip().split(',')[:2]); x = y = 0
    ww = int(h * 9 / 16) // 2 * 2; cx = CX.get((key, ss), 0.5); x0 = int(min(max(x + cx * w - ww / 2, x), x + w - ww))
    vf = f'crop={ww}:{h}:{x0}:{y},scale={WV}:{HV}:flags=lanczos,fps={FPS},' + ('' if key in ee.COLOR else 'format=gray,') + f'format=yuv420p,setsar=1'
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-i', src, '-t', f'{d:.3f}', '-vf', vf, '-an', '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', out + '.part.mp4'])
    os.replace(out + '.part.mp4', out)
def _one(a):
    i, s, d, out = a
    if not os.path.exists(out):
        if s[1] == 'img': img_shot(s[2], d, out, i % 2 == 0)
        else: vid_shot(s[2], s[3], d, out)
    return i
def shots(SH, st, total, od):
    from multiprocessing import Pool
    os.makedirs(od + 'shots', exist_ok=True); jobs = []
    for i, s in enumerate(SH):
        t1 = st[i + 1] if i + 1 < len(SH) else total; jobs.append((i, s, t1 - st[i] + XF, od + 'shots/%03d.mp4' % i))
    with Pool(os.cpu_count()) as pool:
        for i in pool.imap_unordered(_one, jobs): print('vshot', i, flush=True)
    return [(j[3], j[2]) for j in jobs]
def xfade(clips, out, total, od):
    if os.path.exists(out): return
    G = 20; parts, PR = [], []
    for g in range(0, len(clips), G):
        sub = clips[g:g + G]; po = od + 'cut_%02d.mp4' % (g // G); dur = sum(d for _, d in sub) - XF * (len(sub) - 1)
        if not os.path.exists(po):
            inp, fl, prev, acc = [], [], '[0:v]', sub[0][1] - XF
            for c, _ in sub: inp += ['-i', c]
            for i in range(1, len(sub)):
                o = f'[x{i}]'; fl.append(f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={acc:.3f}{o}'); prev = o; acc += sub[i][1] - XF
            if fl: PR.append((subprocess.Popen(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', prev, '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', po + '.part.mp4']), po))
            else: run(['ffmpeg', '-v', 'error', '-y', '-i', sub[0][0], '-c', 'copy', po + '.part.mp4']); os.replace(po + '.part.mp4', po)
        parts.append((po, dur))
    for pr, po in PR: pr.wait(); os.replace(po + '.part.mp4', po)
    if len(parts) == 1: os.replace(parts[0][0], out); return
    inp, fl, prev, acc = [], [], '[0:v]', parts[0][1] - XF
    for c, _ in parts: inp += ['-i', c]
    for i in range(1, len(parts)):
        o = f'[y{i}]'; fl.append(f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={acc:.3f}{o}'); prev = o; acc += parts[i][1] - XF
    run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', prev, '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', out + '.part.mp4'])
    os.replace(out + '.part.mp4', out)
# ---------- text for 9:16 ----------
def chunks(WD, maxlen=30):
    def stop(w, prev): return w[-1] in '.:?!' and not (w[:-1].isdigit() and int(w[:-1]) <= 31 and prev.lower() not in ('jagdgeschwaders', 'staffel'))
    ph, cur = [], []
    for w in WD:
        cur.append(w)
        if stop(w[0], cur[-2][0] if len(cur) > 1 else '') or (w[0][-1] in ',;' and len(cur) >= 2): ph.append(cur); cur = []
    if cur: ph.append(cur)
    out = []
    def split(c):
        txt = ' '.join(x[0] for x in c)
        if len(txt) <= maxlen or len(c) < 3: out.append(c); return
        best, bk = 1e9, None
        for k in range(1, len(c)):
            a = len(' '.join(x[0] for x in c[:k])); pen = abs(a - len(txt) / 2) + (25 if c[k - 1][0].lower() in ee.WEAK else 0) + (60 if c[k][0][:1].isdigit() else 0)
            if pen < best: best, bk = pen, k
        split(c[:bk]); split(c[bk:])
    for c in ph: split(c)
    return [(c[0][1], c[-1][2], ' '.join(x[0] for x in c)) for c in out]
def ass(WD, radios, out):
    def ts(t): t = max(t, 0); return '%d:%02d:%05.2f' % (t // 3600, t % 3600 // 60, t % 60)
    L = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {WV}', f'PlayResY: {HV}', 'WrapStyle: 2', '', '[V4+ Styles]',
         'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
         'Style: Sub,Liberation Serif,62,&H2070C3CD,&H000000FF,&H9E000000,&H9E000000,-1,0,0,0,100,100,0,0,3,9,0,2,80,150,560,1',
         '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    cs = chunks(WD)
    for i, (a, b, t) in enumerate(cs):
        b2 = cs[i + 1][0] - 0.05 if i + 1 < len(cs) and cs[i + 1][0] - b < 0.7 else b + 0.45
        L.append(f'Dialogue: 0,{ts(a)},{ts(b2)},Sub,,0,0,0,,{{\\fad(300,120)}}{t}')
    open(out, 'w').write('\n'.join(L) + '\n')
def label_png(big, small, out):
    GOLD, CREAM = (214, 190, 120), (236, 226, 204)
    im = Image.new('RGBA', (WV, HV), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fb = ImageFont.truetype(ee.LS + 'LiberationSerif-Bold.ttf', 54); fs = ImageFont.truetype(ee.LS + 'LiberationSerif-Italic.ttf', 36)
    bs = ' '.join(big); wb = max(d.textlength(bs, font=fb), d.textlength(small, font=fs)); x = (WV - wb) / 2; y = 300
    d.rectangle((x - 34, y - 28, x + wb + 34, y + 140), fill=(0, 0, 0, 90))
    d.line((x, y - 10, x + wb, y - 10), fill=GOLD + (255,), width=2); d.text((x + (wb - d.textlength(bs, font=fb)) / 2, y), bs, font=fb, fill=CREAM + (255,))
    d.text((x + (wb - d.textlength(small, font=fs)) / 2, y + 72), small, font=fs, fill=GOLD + (255,)); d.line((x, y + 124, x + wb, y + 124), fill=GOLD + (255,), width=2)
    im.save(out)
def finish(cut, mix, WD, radios, labs, total, od, final):
    """parallel finish in 8 chunks on the global timeline, then concat + sound"""
    sub = od + 'subs.ass'; ass(WD, radios, sub)
    L = []
    for j, (t0, big, small) in enumerate(labs): fn = od + 'lab%02d.png' % j; label_png(big, small, fn); L.append((t0, fn))
    N = 8; seg = total / N; procs = []
    for k in range(N):
        S = k * seg; d = min(seg, total - S); out = od + f'fin_{k:02d}.mp4'
        if os.path.exists(out): continue
        fc = (f"[0:v]setpts=PTS+{S:.3f}/TB,eq=contrast=0.96:saturation=0.82:gamma_r=1.03:gamma_b=0.95,"
              "eq=brightness='0.008*sin(t*13.1)+0.006*sin(t*29.7)':eval=frame,noise=alls=6:allf=t,vignette=PI/4.8[n]")
        lab_in, prev, j2 = [], '[n]', 0
        for t0, fn in L:
            if t0 + 6.4 < S or t0 > S + d: continue
            lab_in += ['-loop', '1', '-t', '6.4', '-itsoffset', f'{t0:.2f}', '-i', fn]
            fc += f";[{j2 + 1}:v]format=rgba,fade=in:st={t0:.2f}:d=0.6:alpha=1,fade=out:st={t0 + 5.6:.2f}:d=0.6:alpha=1[l{j2}];{prev}[l{j2}]overlay=0:0:eof_action=pass[o{j2}]"; prev = f'[o{j2}]'; j2 += 1
        fc += f";{prev}subtitles={sub},fade=t=out:st={total - 2.0:.2f}:d=2.0,setpts=PTS-STARTPTS[v]"
        procs.append(subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-ss', f'{S:.3f}', '-t', f'{d:.3f}', '-i', cut, *lab_in, '-filter_complex', fc, '-map', '[v]',
            '-frames:v', str(int(round(d * FPS))), '-r', str(FPS), '-c:v', 'libx264', '-b:v', '5000k', '-maxrate', '7000k', '-bufsize', '14000k', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out]))
    for p in procs: p.wait()
    open(od + 'list.txt', 'w').write(''.join(f"file '{od}fin_{k:02d}.mp4'\n" for k in range(N)))
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', od + 'list.txt', '-i', mix, '-map', '0:v', '-map', '1:a', '-c', 'copy',
         '-t', f'{total:.3f}', '-movflags', '+faststart', final])
