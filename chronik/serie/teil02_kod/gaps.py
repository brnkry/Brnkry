# breathing room for the page turns: 3.0 s of silence before the first word of every new spread (voice speed untouched)
import json, re, numpy as np
from scipy.io import wavfile
D = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t2l/'
W = json.load(open(D + 'words_orig.json')); n = lambda w: re.sub(r'[^a-zäöüß0-9]', '', w.lower())
def find(ph):
    p = [n(x) for x in ph.split()]; hits = [i for i in range(len(W)) if [n(w[0]) for w in W[i:i + len(p)]] == p]
    assert len(hits) == 1, (ph, hits); return hits[0]
STARTS = ['Am Morgen des 1.', 'Die Wehrmacht verfügte', 'In denselben Minuten', 'Am Abend des ersten', 'Zwei Tage später kam', 'An der Front stießen',
          'Während die Armee kämpfte', 'Am frühen Morgen', 'An der Ostsee hielt', 'Warschau wurde nun', 'Doch Polen hatte nicht', 'Den Westen Polens', 'Für Polen begann']
LONG = {'Am Morgen des 1.', 'In denselben Minuten', 'An der Front stießen', 'Warschau wurde nun', 'An der Ostsee hielt'}
GP = {find(s): (5.0 if s in LONG else 3.0) for s in STARTS}
idx = sorted(GP)
sr, x = wavfile.read(D + 'vcut.wav'); x = x.astype(np.float32)
cuts = [(W[i - 1][2] + W[i][1]) / 2 for i in idx]
parts = []; pos = 0
for i, c in zip(idx, cuts): parts += [x[int(pos * sr):int(c * sr)], np.zeros(int(GP[i] * sr), np.float32)]; pos = c
parts.append(x[int(pos * sr):]); y = np.concatenate(parts)
wavfile.write(D + 'vcut2.wav', sr, y.astype(np.int16))
out = []; 
for k, (w, a, b) in enumerate(W):
    sh = sum(GP[i] for i in idx if k >= i); out.append([w, round(a + sh, 3), round(b + sh, 3)])
json.dump(out, open(D + 'words.json', 'w'), ensure_ascii=False); print(len(y) / sr, out[-1])
