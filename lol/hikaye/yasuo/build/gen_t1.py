"""Part 1 on-screen dialogue, word by word, from the forced alignment (dial1.json, out times)."""
import json
D = json.load(open('/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad/yasuo/dial1.json'))
# (phrase idx, display lines, size, position, end)
L = [(0, ['YAPTIKLARIN', 'İÇİN', 'HESAP VER'], 170, 'R', 3.62), (1, ['YONE,', 'GERİ DÖN.'], 130, 'L2', 7.1),
     (2, ['ONURUMUZU', 'YERE SERDİN.'], 130, 'SKY', 9.8), (3, ['ONU KORUMAYA', 'YEMİN ETMİŞTİN.'], 130, 'SKY', 12.5),
     (4, ["SEN DE IONIA'YI", 'KORUMAYA...'], 130, 'SKY', 15.8), (5, ['ETRAFINA BİR BAK,', 'KARDEŞİM.'], 130, 'SKY', 18.1),
     (6, ['ONURUN', 'TOPRAĞI', 'LEKELİYOR.'], 120, 'L2', 21.3), (7, ['ONURSUZLUKTAN', 'İYİDİR.'], 120, 'R2', 23.62),
     (8, ['AFFET BENİ', 'KARDEŞİM'], 150, 'R', 25.7), (9, ['SENİ BİR DAHA', 'UTANDIRMAYACAĞIM.'], 120, 'RB', 28.75),
     (10, ['KAYBETTİKLERİNİ', 'HATIRLA.'], 130, 'SKY', 62.4), (11, ['BIRAK BENİ YONE!', 'YENECEKTİM!'], 110, 'TR', 66.75),
     (12, ['İRİ OĞLANI', 'NASIL ALIYORDUM,', 'GÖRDÜN MÜ?'], 85, 'BL', 69.5), (13, ['ONURUNU', 'AYAKLAR ALTINA', 'ALIYORDU.'], 85, 'TR', 71.55),
     (14, ['AMA SEN DE...'], 100, 'TL', 75.1), (15, ['MECBURSAM', 'DÖVÜŞÜRÜM.', 'KEYİF İÇİN DEĞİL.'], 95, 'TL', 77.85),
     (16, ['SENİN KANITLAYACAK', 'BİR ŞEYİN YOK Kİ.'], 100, 'BR', 80.45)]
T = []
for pi, lines, z, pos, end in L:
    ws = D[pi]; st = round(ws[0][1] - 0.03, 3); rows = []; wi = 0
    assert sum(len(l.split()) for l in lines) == len(ws), (pi, lines, [w[0] for w in ws])
    for li, l in enumerate(lines):
        words = [[w, round(ws[wi + m][1] - st, 3)] for m, w in enumerate(l.split())]; wi += len(words)
        rows.append([words, z, 'C' if li < len(lines) - 1 else 'G'])
    T.append([st, end, pos, rows])
T.append([44.0, 46.0, 'left:0;top:330px;width:1920px;align-items:center', [['YASUO', 250, '#E9C46A', 0, 'slam'], ['ABİSİNİ NEDEN ÖLDÜRDÜ?', 96, 'C', .45]]])
T.sort(key=lambda b: b[0])
open('t1.js', 'w').write('window.T1=' + json.dumps(T, ensure_ascii=False) + ';')
print(len(T), 'blocks')
