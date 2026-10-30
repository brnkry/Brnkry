# Real-ESRGAN x4plus (RRDBNet) with tiling, CPU
import torch, torch.nn as nn, torch.nn.functional as F, numpy as np, cv2, sys
class RDB(nn.Module):
    def __init__(s, nf=64, gc=32):
        super().__init__()
        s.conv1 = nn.Conv2d(nf, gc, 3, 1, 1); s.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1); s.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1)
        s.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1); s.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1); s.l = nn.LeakyReLU(0.2, True)
    def forward(s, x):
        x1 = s.l(s.conv1(x)); x2 = s.l(s.conv2(torch.cat((x, x1), 1))); x3 = s.l(s.conv3(torch.cat((x, x1, x2), 1)))
        x4 = s.l(s.conv4(torch.cat((x, x1, x2, x3), 1))); return s.conv5(torch.cat((x, x1, x2, x3, x4), 1)) * 0.2 + x
class RRDB(nn.Module):
    def __init__(s): super().__init__(); s.rdb1, s.rdb2, s.rdb3 = RDB(), RDB(), RDB()
    def forward(s, x): return s.rdb3(s.rdb2(s.rdb1(x))) * 0.2 + x
class RRDBNet(nn.Module):
    def __init__(s, nb=23):
        super().__init__(); s.conv_first = nn.Conv2d(3, 64, 3, 1, 1); s.body = nn.Sequential(*[RRDB() for _ in range(nb)])
        s.conv_body = nn.Conv2d(64, 64, 3, 1, 1); s.conv_up1 = nn.Conv2d(64, 64, 3, 1, 1); s.conv_up2 = nn.Conv2d(64, 64, 3, 1, 1)
        s.conv_hr = nn.Conv2d(64, 64, 3, 1, 1); s.conv_last = nn.Conv2d(64, 3, 3, 1, 1); s.l = nn.LeakyReLU(0.2, True)
    def forward(s, x):
        f = s.conv_first(x); f = f + s.conv_body(s.body(f))
        f = s.l(s.conv_up1(F.interpolate(f, scale_factor=2, mode='nearest'))); f = s.l(s.conv_up2(F.interpolate(f, scale_factor=2, mode='nearest')))
        return s.conv_last(s.l(s.conv_hr(f)))
@torch.no_grad()
def upscale(img, tile=160, pad=12):
    net = RRDBNet(); sd = torch.load(sys.path[0] + '/x4plus.pth', map_location='cpu'); net.load_state_dict(sd.get('params_ema', sd)); net.eval(); torch.set_num_threads(4)
    h, w = img.shape[:2]; x = torch.from_numpy(img.astype(np.float32) / 255).permute(2, 0, 1)[None]; out = torch.zeros(1, 3, h * 4, w * 4)
    for y0 in range(0, h, tile):
        for x0 in range(0, w, tile):
            ya, xa = max(0, y0 - pad), max(0, x0 - pad); yb, xb = min(h, y0 + tile + pad), min(w, x0 + tile + pad)
            o = net(x[:, :, ya:yb, xa:xb]); y1, x1 = min(h, y0 + tile), min(w, x0 + tile)
            out[:, :, y0 * 4:y1 * 4, x0 * 4:x1 * 4] = o[:, :, (y0 - ya) * 4:(y0 - ya + y1 - y0) * 4, (x0 - xa) * 4:(x0 - xa + x1 - x0) * 4]
    return (out[0].clamp(0, 1).permute(1, 2, 0).numpy() * 255).round().astype(np.uint8)
if __name__ == '__main__':
    g = cv2.imread(sys.argv[1]); import time; t = time.time(); u = upscale(cv2.cvtColor(g, cv2.COLOR_BGR2RGB)); print('%.0f s' % (time.time() - t), u.shape)
    cv2.imwrite(sys.argv[2], cv2.cvtColor(u, cv2.COLOR_RGB2BGR))
