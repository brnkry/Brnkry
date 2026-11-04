# transcribe the audio of autumn-1940 newsreels (streamed from archive.org, video not stored) and list lines that mention Wick
import subprocess, sys, json, urllib.parse, numpy as np
from faster_whisper import WhisperModel
D = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/wick/'
IT = [('528', '19401016DieDeutscheWochenschauNr.52823m59s720x544', '1940-10-16 - Die Deutsche Wochenschau Nr. 528 (23m 59s, 720x544).ogv'),
      ('530', '1940-10-30-die-deutsche-wochenschau-nr.-530-23m-58s-352x-288', '1940-10-30 - Die Deutsche Wochenschau Nr. 530 (23m 58s, 352x288).mp4'),
      ('531', '19401106DieDeutscheWochenschauNr.53121m59s352x288', '1940-11-06 - Die Deutsche Wochenschau Nr. 531 (21m 59s, 352x288).ogv'),
      ('533', '19401120DieDeutscheWochenschauNr.53323m43s720x544', '1940-11-20 - Die Deutsche Wochenschau Nr. 533 (23m 43s, 720x544).ogv'),
      ('536', '19401211DieDeutscheWochenschauNr.53626m33s640x480FRUntertitel', '1940-12-11 - Die Deutsche Wochenschau Nr. 536 (26m 33s, 640x480, FR Untertitel).ogv')]
m = WhisperModel('base', device='cpu', compute_type='int8', cpu_threads=2)
for n, ident, fn in IT:
    url = 'https://archive.org/download/%s/%s' % (ident, urllib.parse.quote(fn))
    if fn.endswith('.mp4'):
        subprocess.run(['curl', '-sSL', '-o', D + 'tmp.mp4', url]); src = D + 'tmp.mp4'; pre = []
    else: src = '-'; pre = None
    if pre is None:
        c = subprocess.Popen(['curl', '-sSL', url], stdout=subprocess.PIPE); au = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', '-', '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], stdin=c.stdout, capture_output=True).stdout, np.float32)
    else:
        au = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32); subprocess.run(['rm', '-f', src])
    segs, _ = m.transcribe(au, language='de', beam_size=1, vad_filter=True)
    S = [(round(s.start), s.text.strip()) for s in segs]; json.dump(S, open(D + 'tr_%s.json' % n, 'w'), ensure_ascii=False)
    for t, s in S:
        if any(k in s.lower() for k in ('wick', 'wiek', 'wieck', 'richthofen', 'eichenlaub', 'kommodore', 'jagdgeschwader', 'mölders')): print(n, '%d:%02d' % (t // 60, t % 60), s, flush=True)
    print('done', n, len(au) / 16000, flush=True)
