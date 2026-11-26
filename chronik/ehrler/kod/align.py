# word alignment: whisper word timestamps mapped onto the script words (difflib), writes words.json [[word,start,end],...]
import sys, json, re, difflib, subprocess
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('small', compute_type='int8')
def norm(w): return re.sub(r'[^a-zäöüßå0-9]', '', w.lower())
for d, txt in zip(sys.argv[1::2], sys.argv[2::2]):
    S = open(txt).read().split()
    au = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', d + '/vcut.wav', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32).copy()
    segs, _ = m.transcribe(au, language='de', word_timestamps=True)
    Wd = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    a = [norm(x) for x in S]; b = [norm(x[0]) for x in Wd]
    T = [None] * len(S)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1): T[i1 + k] = (Wd[j1 + k][1], Wd[j1 + k][2])
        elif j2 > j1:
            t0, t1 = Wd[j1][1], Wd[j2 - 1][2]; n = i2 - i1
            for k in range(n): T[i1 + k] = (t0 + (t1 - t0) * k / n, t0 + (t1 - t0) * (k + 1) / n)
    # fill gaps by interpolation
    for i in range(len(T)):
        if T[i] is None:
            p = next((T[j][1] for j in range(i - 1, -1, -1) if T[j]), 0.0); q = next((T[j][0] for j in range(i + 1, len(T)) if T[j]), p + 0.4)
            T[i] = (p, max(p + 0.05, q))
    miss = sum(1 for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if tag != 'equal')
    json.dump([[w, round(t[0], 3), round(t[1], 3)] for w, t in zip(S, T)], open(d + '/words.json', 'w'), ensure_ascii=False)
    print(d, len(S), 'words, non-equal ops', miss, 'end', round(T[-1][1], 2), flush=True)
