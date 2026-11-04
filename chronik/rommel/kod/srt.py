# Rommel: German + English .srt from the word timings of the final voice track (same timeline for 16:9 and 9:16)
import json, re, sys
W = json.load(open('words.json')); EN = [l.strip() for l in open('code/en.txt') if l.strip()]
TXT = open('code/script.txt').read().strip(); P = re.split(r'(?<=[.!?])\s+', TXT); SENT = []
for x in P:
    if SENT and re.search(r'(^|\s)\d{1,2}\.$', SENT[-1]): SENT[-1] += ' ' + x   # '14.' / '7.' are ordinals, not sentence ends
    else: SENT.append(x)
S = []; i = 0
for x in SENT: n = len(x.split()); S.append(W[i:i + n]); i += n
assert i == len(W)
assert len(S) == len(EN), (len(S), len(EN))
MAXC = 84
def chunks(ws):
    """split a sentence into cues of <= 84 chars, preferring breaks after commas/colons"""
    out = []; i = 0
    while i < len(ws):
        j = i; best = None
        while j < len(ws) and len(' '.join(w for w, _, _ in ws[i:j + 1])) <= MAXC:
            j += 1
            if ws[j - 1][0][-1] in ',:;': best = j
        if j >= len(ws): out.append(ws[i:]); break
        cut = best if best and best - i >= 3 else j
        rest = len(' '.join(w for w, _, _ in ws[cut:]))
        if rest < 18 and cut - i > 4: cut -= 2   # avoid a tiny last cue
        out.append(ws[i:cut]); i = cut
    return out
def wrap(s, n=42):
    if len(s) <= n: return s
    ws = s.split(); best = None
    for k in range(1, len(ws)):
        a, b = ' '.join(ws[:k]), ' '.join(ws[k:]); sc = max(len(a), len(b)) - (6 if a[-1] in ',:;' else 0)
        if best is None or sc < best[0]: best = (sc, a, b)
    return best[1] + '\n' + best[2]
def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'
de, en = [], []
for ws, e in zip(S, EN):
    cs = chunks(ws); T0, T1 = ws[0][1], ws[-1][2]
    for c in cs: de.append([c[0][1], c[-1][2], ' '.join(w for w, _, _ in c)])
    # English: same cue times as the German cues of this sentence, text split at matching proportions
    ew = e.split(); fr = [(c[-1][2] - T0) / max(0.01, T1 - T0) for c in cs[:-1]]; pos = 0; tot = len(e)
    for k, c in enumerate(cs):
        if k == len(cs) - 1: part = ew[pos:]
        else:
            target = fr[k] * tot; acc = len(' '.join(ew[:pos])); best = None
            for q in range(pos + 1, len(ew) - 1):
                L = len(' '.join(ew[:q])); sc = abs(L - target) - (8 if ew[q - 1][-1] in ',:;' else 0)
                if best is None or sc < best[0]: best = (sc, q)
            q = best[1] if best else pos + 1; part = ew[pos:q]; pos = q
        en.append([c[0][1], c[-1][2], ' '.join(part)])
def write(cues, fn):
    with open(fn, 'w', encoding='utf-8') as f:
        for i, (a, b, s) in enumerate(cues):
            nxt = cues[i + 1][0] if i + 1 < len(cues) else b + 1.5
            b = min(max(b + 0.35, a + 1.0), nxt - 0.05)
            f.write(f'{i + 1}\n{ts(max(0, a - 0.05))} --> {ts(b)}\n{wrap(s)}\n\n')
write(de, sys.argv[1] + '/captions.de_DE.srt'); write(en, sys.argv[1] + '/captions.en_US.srt')
print(len(de), 'cues', max(len(s) for *_, s in en), 'max EN chars')
