import json, re, difflib, subprocess, numpy as np
from faster_whisper import WhisperModel
au = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','voice.mp3','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout, np.float32)
m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=4)
segs, _ = m.transcribe(au, language='de', word_timestamps=True, beam_size=5)
H = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
def n(w): return re.sub(r'[^a-zäöüß0-9]', '', w.lower())
T = open('/home/user/Brnkry/chronik/lueth/script_de.txt').read().split()
a = [n(w) for w in T]; b = [n(w[0]) for w in H]; out = [None]*len(T)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag == 'equal':
        for k in range(i2-i1): out[i1+k] = [T[i1+k], H[j1+k][1], H[j1+k][2]]
    elif j2 > j1:
        t0, t1 = H[j1][1], H[j2-1][2]; L_ = i2-i1
        for k in range(L_): out[i1+k] = [T[i1+k], t0+(t1-t0)*k/L_, t0+(t1-t0)*(k+1)/L_]
for i in range(len(out)):
    if out[i] is None:
        p = out[i-1]; out[i] = [T[i], p[2], p[2]+0.2]
json.dump(out, open('words.json','w'), ensure_ascii=False); print(len(out), out[-1])
