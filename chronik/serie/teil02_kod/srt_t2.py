# German and English subtitle tracks for Teil 2 v2, timed to the German words (words.json with the inserted gaps, +1 s film intro)
import json, sys, os
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'; W_ = json.load(open(B + 'words.json')); OFF = 1.0
CUES = [tuple(x.strip() for x in l.split(' | ')) for l in open(B + 'cues.txt', encoding='utf-8') if l.strip()]
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return ('%02d:%02d:%06.3f' % (h, m, s)).replace('.', ',')
def wrap(s, n=42):
    if len(s) <= n: return s
    w = s.split(); best = min(range(1, len(w)), key=lambda i: abs(len(' '.join(w[:i])) - len(' '.join(w[i:])))); return ' '.join(w[:best]) + '\n' + ' '.join(w[best:])
i = 0; de, en = [], []
for k, (g, e) in enumerate(CUES):
    n = len(g.split()); ws = W_[i:i + n]; assert [w[0] for w in ws] == g.split(), (g, [w[0] for w in ws]); i += n
    a = ws[0][1] + OFF; b = ws[-1][2] + OFF + 0.35
    if i < len(W_): b = min(b, W_[i][1] + OFF - 0.02)
    de.append('%d\n%s --> %s\n%s\n' % (k + 1, ts(a), ts(b), wrap(g))); en.append('%d\n%s --> %s\n%s\n' % (k + 1, ts(a), ts(b), wrap(e)))
assert i == len(W_), (i, len(W_))
open(B + 'untertitel/captions.de.srt', 'w').write('\n'.join(de)); open(B + 'untertitel/captions.en_US.srt', 'w').write('\n'.join(en)); print(len(de), 'cues')
