# Bäke Shorts (9:16): the short narration starts at once
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vv
from bb import E, U, XF, run, norm
OD = E + 'build_ks/'; os.makedirs(OD, exist_ok=True)
T1 = 0.0
WD = [(w, a + T1, b + T1) for w, a, b in json.load(open(E + 'ks/words.json'))]
TOTAL = WD[-1][2] + 2.6; TOK = [norm(w[0]) for w in WD]
def K(ph):
    if isinstance(ph, (int, float)): return float(ph)
    p = [norm(x) for x in ph.split()]; h = [k for k in range(len(TOK) - len(p) + 1) if TOK[k:k + len(p)] == p]
    assert h, ph; return WD[h[0]][1] - 0.15
def t(m): a, b = m.split(':'); return int(a) * 60 + float(b)
I, V = 'img', 'vid'
SH = [(0, I, 17), ('höchstdekorierten Panzerkommandeure', V, 'tg', 35.0), ('Sein Name war', I, 15), ('Im Ersten Weltkrieg kämpfte', I, 20), ('danach studierte er', I, 13),
      ('Im August 1939 wurde', I, 14), ('Mit der 6.', V, '705', t('7:16')), ('in Frankreich und an', V, '672', t('18:20')), ('Ende 1943 führte', I, 21),
      ('Anfang 1944 stellte die', I, 3), ('rund 34 Tiger', V, 'tg', 15.0), ('das Schwere Panzer-Regiment', I, 12), ('Im Februar 1944 sollte', V, '703', t('13:58')),
      ('Doch Tauwetter verwandelte', V, '712', t('9:10')), ('und die Panzer blieben', V, '712', t('9:20')), ('Bäke erhielt die Schwerter', I, 1),
      ('Im April 1945 wurde', I, 2), ('Und nach dem Krieg', I, 0), ('Er ging zurück nach', I, 22)]
LAB = [('Sein Name war', 'FRANZ BÄKE', 'Zahnarzt aus Hagen'), ('das Schwere Panzer-Regiment', 'SCHWERES PANZER-REGIMENT BÄKE', 'Januar 1944'),
       ('Im Februar 1944 sollte', 'TSCHERKASSY', 'Februar 1944')]
vv.IMGCX.update({1: .5, 3: .55, 10: .5})
def starts():
    st = [K(s[0]) for s in SH]; st[0] = 0.0
    for a, b, s in zip(st, st[1:], SH[1:]): assert b > a + 2.0, (s, round(b - a, 2))
    return st
def sound(out):
    if os.path.exists(out): return
    fl = (f"[0]aformat=sample_rates=48000:channel_layouts=stereo[v];[1]atrim=0:{TOTAL:.3f},afade=t=in:d=1.5,afade=t=out:st={TOTAL - 3:.3f}:d=3,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.14[m];"
          "[v]asplit[v1][v2];[m][v2]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=900[md];[v1][md]amix=inputs=2:normalize=0:duration=longest,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    run(['ffmpeg', '-v', 'error', '-y', '-i', E + 'ks/vcut.wav', '-ss', '20', '-i', U + 't1/musik.mp3', '-filter_complex', fl, '-map', '[a]', '-t', f'{TOTAL:.3f}', '-c:a', 'aac', '-b:a', '192k', out])
if __name__ == '__main__':
    st = starts(); print('TOTAL', round(TOTAL, 1), flush=True)
    if 'check' in sys.argv: sys.exit()
    c = vv.shots(SH, st, TOTAL, OD); vv.xfade(c, OD + 'cut.mp4', TOTAL, OD); print('cut ok', flush=True)
    sound(OD + 'mix.m4a'); print('sound ok', flush=True)
    vv.finish(OD + 'cut.mp4', OD + 'mix.m4a', WD, [], [(K(p) + 0.4, b, s) for p, b, s in LAB], TOTAL, OD, E + 'Franz_Baeke_Shorts_DE.mp4'); print('KS_DONE', flush=True)
