# Short version (Shorts / Reels, 9:16): radio message, then the corrected short narration (1:46).
import os, sys, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vv
from ee import E, U, XF, run, RD, norm
OD = E + 'build_ks/'; os.makedirs(OD, exist_ok=True)
R1 = 0.4; T1 = R1 + RD + 0.4
WD = [(w, a + T1, b + T1) for w, a, b in json.load(open(E + 'ks/words.json'))]
TOTAL = WD[-1][2] + 3.0; TOK = [norm(w[0]) for w in WD]
def K(ph):
    if isinstance(ph, (int, float)): return float(ph)
    p = [norm(x) for x in ph.split()]; h = [k for k in range(len(TOK) - len(p) + 1) if TOK[k:k + len(p)] == p]
    assert h, ph; return WD[h[0]][1] - 0.15
I, V = 'img', 'vid'
SH = [(0, V, 'conv2', 108.0), ('Das sollen die letzten', I, 15), ('Ehrler war einer der', I, 12), ('Mit dem Jagdgeschwader 5', I, 19), ('über Lappland, der Barentssee', I, 10),
      ('in Schneestürmen und Polarnacht', I, 4), ('Ihm wurden fast 200', I, 9), ('er trug das Ritterkreuz', I, 11), ('und wurde Kommodore seines', I, 23),
      ('Doch am 12. November', V, 'tir', 4.0), ('Britische Lancaster-Bomber griffen', V, 'tb', 54.8), ('Ihre über fünf Tonnen', V, 'tb', 27.6), ('die Tirpitz kenterte', I, 3),
      ('Die Jäger aus dem', I, 21), ('Warnungen kamen zu spät', V, 'dw', 326.0), ('Die Führung brauchte einen', I, 2),
      ('Ein Kriegsgericht verurteilte', I, 14), ('Die Strafe wurde ausgesetzt', I, 24), ('Im Februar 1945 kam', I, 6), ('auf die Messerschmitt Me', I, 17),
      ('Im April 1945 stieg', V, 'b17', 100.0), ('Nach den Berichten schoss', V, 'dw', 216.0), ('Dann war seine Munition', V, 'b17', 245.0), ('Ob er den dritten', V, 'conv2', 76.0),
      ('Sicher ist nur: Seine', I, 18), ('Heinrich Ehrler wurde 27', I, 8), ('Gut einen Monat später', I, 7)]
LAB = [('Mit dem Jagdgeschwader 5', 'JAGDGESCHWADER 5', 'Petsamo · Finnland'), ('Doch am 12. November', '12. NOVEMBER 1944', 'Angriff auf die Tirpitz'),
       ('Im Februar 1945 kam', 'JAGDGESCHWADER 7', 'Messerschmitt Me 262'), ('Im April 1945 stieg', 'APRIL 1945', 'Letzter Einsatz')]
def sound(out):
    if os.path.exists(out): return
    fl = (f"[0]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(R1 * 1000)}:all=1[r];[1]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(T1 * 1000)}:all=1[n];"
          f"[r][n]amix=inputs=2:normalize=0:duration=longest[v];[2]atrim=0:{TOTAL:.3f},afade=t=in:d=2,afade=t=out:st={TOTAL - 4:.3f}:d=4,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.14[m];"
          "[v]asplit[v1][v2];[m][v2]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=900[md];[v1][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    run(['ffmpeg', '-v', 'error', '-y', '-i', E + 'Telsiz_Final.mp3', '-i', E + 'ks/vcut.wav', '-ss', '20', '-i', U + 't1/musik.mp3', '-filter_complex', fl,
         '-map', '[a]', '-t', f'{TOTAL:.3f}', '-c:a', 'aac', '-b:a', '192k', out])
if __name__ == '__main__':
    st = [K(s[0]) for s in SH]; st[0] = 0.0
    assert all(b > a + 1.5 for a, b in zip(st, st[1:])), 'shot too short'
    print('TOTAL', round(TOTAL, 1), flush=True)
    c = vv.shots(SH, st, TOTAL, OD); vv.xfade(c, OD + 'cut.mp4', TOTAL, OD); print('cut ok', flush=True)
    sound(OD + 'mix.m4a'); print('sound ok', flush=True)
    vv.finish(OD + 'cut.mp4', OD + 'mix.m4a', WD, [R1], [(K(p) + 0.4, b, s) for p, b, s in LAB], TOTAL, OD, E + 'Ehrler_Shorts_DE.mp4'); print('KS_DONE', flush=True)
