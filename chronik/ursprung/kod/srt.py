import json, re
S = json.load(open('sents.json')); E = [l.strip() for l in open('en.txt') if l.strip()]
assert len(S) == len(E), (len(S), len(E))
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return ('%02d:%02d:%06.3f'%(h,m,s)).replace('.',',')
def chunks(txt, mx=14):
    w = txt.split()
    if len(w) <= mx + 3: return [txt]
    n = -(-len(w) // mx); tgt = len(w) / n; out, cur = [], []
    for i, x in enumerate(w):
        cur.append(x); left = len(w) - i - 1
        if left and len(cur) >= tgt * 0.6 and (re.search(r'[,:;]$', x) or len(cur) >= tgt * 1.25) and left >= 4:
            out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    return out
def wrap(c, mx=42):
    if len(c) <= mx: return c
    w = c.split(); best = min(range(1, len(w)), key=lambda k: abs(len(' '.join(w[:k])) - len(' '.join(w[k:]))))
    return ' '.join(w[:best]) + '\n' + ' '.join(w[best:])
cues = []
for k, ((de, a, b, starts), en) in enumerate(zip(S, E)):
    nxt = S[k+1][1] if k + 1 < len(S) else b + 2
    end = min(b + 0.3, nxt - 0.04)
    cs = chunks(en); tot = sum(len(c.split()) for c in cs); acc = 0; N = len(starts)
    for j, c in enumerate(cs):
        f0 = acc / tot; acc += len(c.split()); f1 = acc / tot
        t0 = starts[min(int(round(f0 * N)), N - 1)] if j else a
        t1 = starts[min(int(round(f1 * N)), N - 1)] - 0.04 if j < len(cs) - 1 else end
        cues.append((t0, t1, wrap(c)))
open('captions.en_US.srt', 'w').write('\n'.join('%d\n%s --> %s\n%s\n' % (i + 1, ts(a), ts(b), t) for i, (a, b, t) in enumerate(cues)))
print(len(cues), 'cues; bad:', sum(1 for a, b, t in cues if b - a < 0.6))
