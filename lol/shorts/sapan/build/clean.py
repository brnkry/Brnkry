"""Remove (inpaint) or recolour burned-in overlays of the cropped source, by colour mask.
usage: python3 clean.py SRC.mp4 OUT.mp4 [test T1 T2 ...]"""
import sys, json, os, subprocess, numpy as np, cv2
SRC, OUT = sys.argv[1], sys.argv[2]
CFG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clean_cfg.json')))
W, H, FPS = 1080, 1920, 30
def rule_mask(roi, rule, dil=19):
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV); h, s, v = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
    m = np.zeros(h.shape, bool)
    for r in rule.split('+'):
        if r == 'red': m |= ((h < 12) | (h > 165)) & (s > 110) & (v > 130)
        if r == 'green': m |= (h > 25) & (h < 90) & (s > 110) & (v > 150)
        if r == 'blue': m |= (h > 85) & (h < 130) & (s > 90) & (v > 170)
        if r == 'cyan': m |= (h > 78) & (h < 108) & (s > 60) & (v > 190)
        if r == 'gold': m |= (h > 12) & (h < 35) & (s > 90) & (v > 150)
        if r == 'lime': m |= (h > 40) & (h < 92) & (s > 55) & (v > 105)
        if r == 'yellow': m |= (h > 14) & (h < 40) & (s > 55) & (v > 105)
        if r == 'softwhite': m |= (s < 80) & (v > 115)
        if r == 'white': m |= (s < 70) & (v > 185)
        if r == 'all': m |= True
        if r == 'disc':
            yy, xx = np.mgrid[:h.shape[0], :h.shape[1]]; cy, cx = h.shape[0] / 2, h.shape[1] / 2
            m |= ((yy - cy) ** 2 + (xx - cx) ** 2) < (min(cy, cx)) ** 2
    m = m.astype(np.uint8) * 255
    if rule != 'disc':
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
        m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dil, dil)))
    return m
def find_bar(roi):
    v = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)[..., 2]
    d = cv2.morphologyEx((v < 70).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((1, 5), np.uint8))
    rows = []
    for y in range(d.shape[0]):
        r = d[y]; best = (0, 0, 0); run = 0
        for x in range(len(r)):
            run = run + 1 if r[x] else 0
            if run > best[0]: best = (run, x - run + 1, x)
        if 200 < best[0] < 420: rows.append((y, best[1], best[2]))
    if not rows: return None
    ys = [r[0] for r in rows]; y0 = ys[0]; grp = [rows[0]]  # take the first compact band (bar height under 40px)
    for r in rows[1:]:
        if r[0] - y0 < 40: grp.append(r)
    return (min(r[1] for r in grp), min(r[0] for r in grp), max(r[2] for r in grp), max(r[0] for r in grp))
def clean(fr, t):
    for c in CFG:
        if not (c['a'] <= t <= c['b']): continue
        x, y, w, h = c['r']; roi = fr[y:y + h, x:x + w]
        m = rule_mask(roi, c['rule'], c.get('dil', 19))
        if c.get('keepbar'):  # keep the champion health bar untouched (rows with a long dark border line)
            box = find_bar(roi)
            if box: bx0, by0, bx1, by1 = box; m[max(0, by0 - 4):by1 + 26, max(0, bx0 - 8):bx1 + 8] = 0
        if m.max() == 0: continue
        if 'to' in c:  # keep the reference icon but change its colour
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            hsv[..., 0] = np.where(m > 0, c['to'], hsv[..., 0])
            rec = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            a = cv2.GaussianBlur(m, (9, 9), 0)[..., None] / 255.0
            fr[y:y + h, x:x + w] = (roi * (1 - a) + rec * a).astype(np.uint8)
            continue
        sm = cv2.resize(roi, (w // 2, h // 2)); mm = cv2.resize(m, (w // 2, h // 2))
        inp = cv2.inpaint(sm, mm, 6, cv2.INPAINT_TELEA)
        inp = cv2.resize(inp, (w, h))
        a = cv2.GaussianBlur(m, (15, 15), 0)[..., None] / 255.0
        fr[y:y + h, x:x + w] = (roi * (1 - a) + inp * a).astype(np.uint8)
    return fr
pre = ['ffmpeg', '-v', 'error', '-i', SRC, '-vf', 'crop=532:946:94:50,scale=1080:1920:flags=lanczos,fps=30,eq=saturation=1.08:contrast=1.04', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-']
if len(sys.argv) > 3 and sys.argv[3] == 'test':
    for T in sys.argv[4:]:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', T, '-i', SRC, '-frames:v', '1'] + pre[5:], capture_output=True, stdin=subprocess.DEVNULL).stdout
        fr = np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy(); a = fr.copy()
        b = clean(fr, float(T))
        cv2.imwrite(os.path.join(OUT, f'{T}.jpg'), cv2.resize(np.hstack([a, b]), (540, 480)))
    sys.exit()
dec = subprocess.Popen(pre, stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
i = 0
while True:
    raw = dec.stdout.read(W * H * 3)
    if len(raw) < W * H * 3: break
    fr = np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy()
    enc.stdin.write(clean(fr, i / FPS).tobytes()); i += 1
enc.stdin.close(); enc.wait(); print('frames', i)
