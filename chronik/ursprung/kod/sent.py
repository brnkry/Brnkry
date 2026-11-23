import sys, json, re
sys.path.insert(0, '.')
from engine import Part, U, XF, OFF
KEYS = ['t1','p2','p3','p4','p5','p6','p7','p8','p9','p10']
parts = [Part(U + k) for k in KEYS]; S = []; t = 0.0
for p in parts: S.append(t); t += p.end - XF
WD = []
for p, s in zip(parts, S): WD += [[w, a + s + OFF, b + s + OFF] for w, a, b in p.wd]
sents, cur = [], []
for w in WD:
    cur.append(w)
    if re.search(r'[.!?]["“”]?$', w[0]) and not re.fullmatch(r'\d+\.', w[0]): sents.append(cur); cur = []
if cur: sents.append(cur)
json.dump([[ ' '.join(x[0] for x in s), s[0][1], s[-1][2], [x[1] for x in s]] for s in sents], open(U + 'pak/sents.json', 'w'), ensure_ascii=False)
with open(U + 'pak/sents_de.txt', 'w') as f:
    for i, s in enumerate(sents): f.write('%d %s\n' % (i, ' '.join(x[0] for x in s)))
print(len(sents), len(WD))
