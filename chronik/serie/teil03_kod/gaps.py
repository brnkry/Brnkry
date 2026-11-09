# breathing room for the page turns: silence topped up to about 1.9 s before the first word of every new spread (voice speed untouched)
import json, re, numpy as np
from scipy.io import wavfile
D = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t3l/'
W = json.load(open(D + 'words_orig.json')); n = lambda w: re.sub(r'[^a-zäöüß0-9]', '', w.lower())
def find(ph):
    p = [n(x) for x in ph.split()]; hits = [i for i in range(len(W)) if [n(w[0]) for w in W[i:i + len(p)]] == p]
    assert len(hits) == 1, (ph, hits); return hits[0]
STARTS = ['Nach dem Überfall auf', 'Hitler sah das anders.', 'Sicher ist, dass es', 'Zuerst aber schlug', 'Im Oslofjord fuhr', 'Am Morgen des 10.', 'Am 14. Mai, während',
          'Zur selben Zeit schoben', 'Viele deutsche Soldaten schliefen', 'Die eingeschlossenen Truppen wichen', 'Am 26. Mai begann', 'Am 5. Juni begann', 'Hitler bestimmte den Ort', 'Am frühen Morgen des']
LONG = {'Am Morgen des 1.', 'In denselben Minuten', 'An der Front stießen', 'Warschau wurde nun', 'An der Ostsee hielt'}
GP = {}
for s_ in STARTS:
    i = find(s_); GP[i] = round(max(0.3, 1.9 - (W[i][1] - W[i - 1][2])), 3)   # about 1.9 s of silence in all at a page turn
print(GP)
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
