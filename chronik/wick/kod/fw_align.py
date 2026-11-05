# word timing for the Teil 2 voice: faster-whisper word timestamps, then the script's own words mapped onto them (difflib)
import json, re, sys, difflib
from faster_whisper import WhisperModel
D = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/wick/'
m = WhisperModel('base', device='cpu', compute_type='int8', cpu_threads=4)
import subprocess, numpy as np
au = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', D + 'vcut.wav', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
segs, _ = m.transcribe(au, language='de', word_timestamps=True, beam_size=5, vad_filter=False)
H = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
json.dump(H, open(D + 'heard.json', 'w'), ensure_ascii=False)
def n(w): return re.sub(r'[^a-zäöüß0-9]', '', w.lower())
T = open(D + 'code/script.txt').read().split()
a = [n(w) for w in T]; b = [n(w[0]) for w in H]
out = [None] * len(T)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1): out[i1 + k] = [T[i1 + k], H[j1 + k][1], H[j1 + k][2]]
    elif j2 > j1:   # spread the script words over the heard span
        t0, t1 = H[j1][1], H[j2 - 1][2]; L = i2 - i1
        for k in range(L): out[i1 + k] = [T[i1 + k], t0 + (t1 - t0) * k / L, t0 + (t1 - t0) * (k + 1) / L]
for i in range(len(out)):   # words not heard at all: between their neighbours
    if out[i] is None:
        p = next(x for x in out[i::-1] if x) if any(out[:i]) else [None, 0, 0]
        q = next((x for x in out[i:] if x), [None, p[2] + 0.3, p[2] + 0.3])
        out[i] = [T[i], p[2], max(p[2] + 0.05, q[1])]
json.dump([[w, round(a_, 3), round(b_, 3)] for w, a_, b_ in out], open(D + 'words.json', 'w'), ensure_ascii=False)
print(len(H), len(T), sum(1 for t in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if t[0] != 'equal'))
