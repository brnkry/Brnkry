# Forced alignment of a voice file against its script with pocketsphinx (bundled en-us model).
# usage: python3 align.py voice.mp3 script.txt out.json   -> [[word, start, end], ...]
import sys, subprocess, json, re
from pocketsphinx import Decoder
SR = 16000
raw = subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-f','s16le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
text = open(sys.argv[2]).read().lower().replace('1996','nineteen ninety six')
text = re.sub(r"[^a-z' ]+", ' ', text)
words = text.split()
d = Decoder(samprate=SR, bestpath=False)
SUBS = {'misfires': ['miss', 'fires'], 'misfiring': ['miss', 'firing'], 'misfire': ['miss', 'fire']}
fixed = []; merge = []   # merge: (output word, number of aligned words it spans)
for w in words:
    if w in SUBS: fixed.extend(SUBS[w]); merge.append((w, len(SUBS[w]))); continue
    n0 = len(fixed)
    if d.lookup_word(w) is None:
        w2 = w.replace("'", "")
        if d.lookup_word(w2) is not None: fixed.append(w2); merge.append((w2, 1)); continue
        if all(d.lookup_word(c) is not None for c in w2): fixed.extend(list(w2)); merge.extend((c, 1) for c in w2); continue
        print('OOV', w, file=sys.stderr); continue
    fixed.append(w); merge.append((w, 1))
d.set_align_text(' '.join(fixed))
d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
seg = [[s.word, round(s.start_frame / 100, 2), round((s.end_frame + 1) / 100, 2)] for s in d.seg() if s.word not in ('<s>', '</s>', '<sil>', '[NOISE]')]
out = []; i = 0
for w, n in merge:
    part = seg[i:i + n]; i += n
    if part: out.append([w, part[0][1], part[-1][2]])
json.dump(out, open(sys.argv[3], 'w'))
print(len(fixed), 'words in script,', len(out), 'aligned')
