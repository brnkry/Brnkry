# Facebook: the long version in 9:16 (same shot list, timeline and sound as the 16:9 film)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vv, build
from ee import E, R1, R2, TOTAL, WD, K
OD = E + 'build_fb/'; os.makedirs(OD, exist_ok=True)
if __name__ == '__main__':
    st = [K(s[0]) for s in build.SH]; st[0] = 0.0
    c = vv.shots(build.SH, st, TOTAL, OD); vv.xfade(c, OD + 'cut.mp4', TOTAL, OD); print('cut ok', flush=True)
    vv.finish(OD + 'cut.mp4', build.OUT + 'mix.m4a', WD, [R1, R2], [(K(p) + 0.4, b, s) for p, b, s in build.LAB], TOTAL, OD, E + 'Heinrich_Ehrler_lang_9x16.mp4'); print('FB_DONE', flush=True)
