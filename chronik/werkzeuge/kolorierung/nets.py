# Real-ESRGAN (SRVGGNetCompact, realesr-general-x4v3) and Zhang et al. SIGGRAPH17 colorizer, plain torch
import torch, torch.nn as nn, torch.nn.functional as F
class SRVGG(nn.Module):
    def __init__(s, nf=64, nc=32, up=4):
        super().__init__(); L = [nn.Conv2d(3, nf, 3, 1, 1), nn.PReLU(nf)]
        for _ in range(nc): L += [nn.Conv2d(nf, nf, 3, 1, 1), nn.PReLU(nf)]
        L += [nn.Conv2d(nf, 3 * up * up, 3, 1, 1)]; s.body = nn.Sequential(*L); s.ps = nn.PixelShuffle(up); s.up = up
    def forward(s, x): return s.ps(s.body(x)) + F.interpolate(x, scale_factor=s.up, mode='nearest')
def C(i, o, d=1): return nn.Conv2d(i, o, 3, 1, d, dilation=d)
class SIG17(nn.Module):
    def __init__(s):
        super().__init__(); R = lambda: nn.ReLU(True)
        s.model1 = nn.Sequential(C(4, 64), R(), C(64, 64), R(), nn.BatchNorm2d(64))
        s.model2 = nn.Sequential(C(64, 128), R(), C(128, 128), R(), nn.BatchNorm2d(128))
        s.model3 = nn.Sequential(C(128, 256), R(), C(256, 256), R(), C(256, 256), R(), nn.BatchNorm2d(256))
        s.model4 = nn.Sequential(C(256, 512), R(), C(512, 512), R(), C(512, 512), R(), nn.BatchNorm2d(512))
        s.model5 = nn.Sequential(C(512, 512, 2), R(), C(512, 512, 2), R(), C(512, 512, 2), R(), nn.BatchNorm2d(512))
        s.model6 = nn.Sequential(C(512, 512, 2), R(), C(512, 512, 2), R(), C(512, 512, 2), R(), nn.BatchNorm2d(512))
        s.model7 = nn.Sequential(C(512, 512), R(), C(512, 512), R(), C(512, 512), R(), nn.BatchNorm2d(512))
        s.model8up = nn.Sequential(nn.ConvTranspose2d(512, 256, 4, 2, 1)); s.model3short8 = nn.Sequential(C(256, 256))
        s.model8 = nn.Sequential(R(), C(256, 256), R(), C(256, 256), R(), nn.BatchNorm2d(256))
        s.model9up = nn.Sequential(nn.ConvTranspose2d(256, 128, 4, 2, 1)); s.model2short9 = nn.Sequential(C(128, 128))
        s.model9 = nn.Sequential(R(), C(128, 128), R(), nn.BatchNorm2d(128))
        s.model10up = nn.Sequential(nn.ConvTranspose2d(128, 128, 4, 2, 1)); s.model1short10 = nn.Sequential(C(64, 128))
        s.model10 = nn.Sequential(R(), C(128, 128), nn.LeakyReLU(0.2))
        s.model_class = nn.Sequential(nn.Conv2d(256, 529, 1)); s.model_out = nn.Sequential(nn.Conv2d(128, 2, 1), nn.Tanh())
    def forward(s, L):   # L: (n,1,h,w) in 0..100
        A = (L - 50) / 100; z = torch.zeros_like(A)
        c1 = s.model1(torch.cat([A, z, z, z], 1)); c2 = s.model2(c1[:, :, ::2, ::2]); c3 = s.model3(c2[:, :, ::2, ::2])
        c4 = s.model4(c3[:, :, ::2, ::2]); c7 = s.model7(s.model6(s.model5(c4)))
        c8 = s.model8(s.model8up(c7) + s.model3short8(c3)); c9 = s.model9(s.model9up(c8) + s.model2short9(c2))
        c10 = s.model10(s.model10up(c9) + s.model1short10(c1)); return s.model_out(c10) * 110
def load(B):
    sr = SRVGG(); sd = torch.load(B + 'models/realesr-general-x4v3.pth', map_location='cpu'); sr.load_state_dict(sd.get('params', sd)); sr.eval()
    co = SIG17(); r = co.load_state_dict(torch.load(B + 'models/siggraph17.pth', map_location='cpu'), strict=False); co.eval()
    return sr, co, r
