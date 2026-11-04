# clip enhancement: burned-in subtitle removal, light denoise, colourisation (SIGGRAPH17), 9:16 slice, Real-ESRGAN x4
import sys, glob, time, numpy as np, cv2, torch
sys.path.insert(0, sys.argv[1] + 'code'); import nets
B = sys.argv[1]; MODE = sys.argv[2]
torch.set_num_threads(4); sr, co, _ = nets.load(B)
def unsub(g):
    """mask the white subtitle letters plus their dark outline in the lower band, inpaint from surroundings"""
    h = g.shape[0]; m = np.zeros_like(g); band = slice(int(h * 0.68), int(h * 0.95))
    m[band] = (g[band] > 200).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((13, 13), np.uint8)); return cv2.inpaint(g, m, 9, cv2.INPAINT_NS), m
@torch.no_grad()
def colorize(g):
    L = cv2.resize(g, (256, 256), interpolation=cv2.INTER_AREA).astype(np.float32) / 255 * 100
    ab = co(torch.from_numpy(L)[None, None])[0].numpy().transpose(1, 2, 0)
    ab = cv2.GaussianBlur(ab, (0, 0), 10)   # the net's colour is blotchy and striped at 256 px: keep only the broad colour
    return cv2.resize(ab, (g.shape[1], g.shape[0]), interpolation=cv2.INTER_CUBIC)
def lab2rgb(g, ab, sat=1.1):
    lab = np.dstack([g.astype(np.float32) / 255 * 100, ab * sat]).astype(np.float32)
    return (np.clip(cv2.cvtColor(lab, cv2.COLOR_LAB2RGB), 0, 1) * 255).astype(np.uint8)
@torch.no_grad()
def upscale(rgb):
    x = torch.from_numpy(rgb.astype(np.float32) / 255).permute(2, 0, 1)[None]
    return (sr(x)[0].clamp(0, 1).permute(1, 2, 0).numpy() * 255).round().astype(np.uint8)
files = sorted(glob.glob(B + 'fr/*.png'))
if MODE == 'test':
    g = cv2.imread(files[60], 0); t0 = time.time(); u, m = unsub(g); t1 = time.time(); ab = colorize(u); t2 = time.time()
    rgb = lab2rgb(u, ab); W_ = int(round(g.shape[0] * 9 / 16)); x0 = int(g.shape[1] * 0.5 - W_ / 2); sl = rgb[:, x0:x0 + W_]
    up = upscale(sl); t3 = time.time(); print('unsub %.2f colour %.2f sr %.2f s' % (t1 - t0, t2 - t1, t3 - t2), up.shape)
    cv2.imwrite(B + 'test_full_before.jpg', g); cv2.imwrite(B + 'test_full_after.jpg', cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    cv2.imwrite(B + 'test_slice_up.jpg', cv2.cvtColor(up, cv2.COLOR_RGB2BGR))

if MODE == 'run':
    import subprocess
    n = len(files); prev = None; out = B + 'out/'; import os; os.makedirs(out, exist_ok=True); t0 = time.time()
    for i, f in enumerate(files):
        g = cv2.imread(f, 0); u, _ = unsub(g); u = cv2.fastNlMeansDenoising(u, None, 4, 5, 15)
        ab = colorize(u); ab = ab if prev is None else 0.6 * prev + 0.4 * ab; prev = ab   # temporal smoothing: no colour flicker
        rgb = lab2rgb(u, ab); Wd = int(round(g.shape[0] * 9 / 16)); cx = g.shape[1] * (0.36 + 0.30 * i / (n - 1))   # slow pan along the barrel
        x0 = int(min(max(cx - Wd / 2, 0), g.shape[1] - Wd))
        up = cv2.resize(upscale(rgb[:, x0:x0 + Wd]), (1080, 1920), interpolation=cv2.INTER_AREA)
        bef = cv2.resize(g[:, x0:x0 + Wd], (1080, 1920), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(out + 'a_%04d.png' % i, cv2.cvtColor(up, cv2.COLOR_RGB2BGR)); cv2.imwrite(out + 'b_%04d.png' % i, bef)
        if i % 20 == 0: print(i, n, '%.0f s' % (time.time() - t0), flush=True)
