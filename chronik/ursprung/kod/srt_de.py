# German subtitle track, cut into readable cues on the German word timings (sents.json from sent.py)
import json, re
S = json.load(open('sents.json'))
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return ('%02d:%02d:%06.3f'%(h,m,s)).replace('.',',')
def wrap(c, mx=42):
    if len(c) <= mx: return c
    w = c.split(); k = min(range(1, len(w)), key=lambda k: abs(len(' '.join(w[:k])) - len(' '.join(w[k:]))))
    return ' '.join(w[:k]) + '\n' + ' '.join(w[k:])
cues = []
for i, (de, a, b, st) in enumerate(S):
    w = de.split(); nxt = S[i + 1][1] if i + 1 < len(S) else b + 2; end = min(b + 0.3, nxt - 0.04)
    mx = 13; n = -(-len(w) // mx) if len(w) > mx + 3 else 1; tgt = len(w) / n; cut = [0]; cur = 0
    for j, x in enumerate(w):
        cur += 1; left = len(w) - j - 1
        if n > 1 and left >= 4 and cur >= tgt * 0.6 and (re.search(r'[,:;]$', x) or cur >= tgt * 1.25): cut.append(j + 1); cur = 0
    cut.append(len(w))
    for k in range(len(cut) - 1):
        t0 = st[cut[k]] if k else a; t1 = st[cut[k + 1]] - 0.04 if k < len(cut) - 2 else end
        cues.append((t0, t1, wrap(' '.join(w[cut[k]:cut[k + 1]]))))
open('captions.de.srt', 'w').write('\n'.join('%d\n%s --> %s\n%s\n' % (i + 1, ts(a), ts(b), t) for i, (a, b, t) in enumerate(cues)))
print(len(cues))
