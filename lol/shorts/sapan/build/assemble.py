"""Assemble the Sapan Short voice track.
usage: python3 assemble.py VO_RAW.wav RAW_WORDS.json BODY.wav BODY_WORDS.json
- hook lines are cut from the raw take and placed at fixed times (synced to the reference video)
- the body (pauses trimmed) gets gaps where the Turkish champion/announcer lines are inserted
outputs: ../ses/vo.wav, words.js (caption words), timeline.json (cues for overlay/segments/mix)"""
import sys, json, wave, numpy as np
VO_RAW, RAW_W, BODY, BODY_W = sys.argv[1:5]
SR = 44100
def load(p):
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32); assert w.getframerate() == SR; return a
def db(x, d): return x * (10 ** (d / 20))
def quiet(a, t0, t1):
    best = None
    for t in np.arange(t0, t1, 0.005):
        s = a[int(t * SR):int((t + 0.02) * SR)]; e = float(np.sqrt((s ** 2).mean()) if len(s) else 0)
        if best is None or e < best[1]: best = (t + 0.01, e)
    return best[0]
raw = load(VO_RAW); body = load(BODY)
rw = json.load(open(RAW_W)); bw = json.load(open(BODY_W))
# hook: (raw_start, raw_end, out_time, text)
HOOK = [(0.00, 1.06, 0.15, 'Ahaha, kolaydı!'), (1.20, 1.98, 2.20, 'Bi base atayım.'), (2.30, 2.58, 3.35, 'Lan?'), (2.88, 3.26, 4.05, 'Lan?'),
        (3.58, 4.30, 4.80, 'Noluyo lan?'), (4.58, 5.50, 5.75, 'Yakma lan artık!'), (5.64, 6.60, 6.75, 'Ölücem, ananın...')]
BODY_START = 8.70
# inserts after body words: (word, file, gain_db)
INS = [('vuruyor.', 'vl_teemo_yakacak', -5.5, 39.59, 0.0, 0.18, 0.36), ('kilikap.', 'vl_spiker_kill', -10.2, 44.07, 0.22, 0.06, 0.14)]  # (word, file, gain, cut, trim_head, lead, total_pad)  # cut times = energy minima in the body take
END_PAD = 2.2
out = np.zeros(int(90 * SR), np.float32)
def put(sig, t):
    i = int(t * SR); out[i:i + len(sig)] += sig
for a, b, t, _ in HOOK:
    seg = raw[int(a * SR):int(b * SR)].copy(); n = int(0.02 * SR); seg[:n] *= np.linspace(0, 1, n); seg[-n:] *= np.linspace(1, 0, n); put(seg, t)
TL = {'hook': [{'t': t, 'd': b - a, 'text': x} for a, b, t, x in HOOK], 'beep': HOOK[-1][2] + (HOOK[-1][1] - HOOK[-1][0]) - 0.02, 'body_start': BODY_START, 'inserts': []}
# split body
cuts = []
for word, f, g, c, th, ld, pd in INS:
    cuts.append((c, f, g, th, ld, pd))
pos = 0.0; shift = BODY_START; words = []
def addwords(a, b, sh):
    for s, e, txt in bw:
        if a <= (s + e) / 2 < b: words.append([round(s + sh, 3), round(e + sh, 3), txt])
for c, f, g, th, ld, pd in cuts:
    seg = body[int(pos * SR):int(c * SR)]; put(seg, pos + shift); addwords(pos, c, shift)
    vl = db(load(f'../ses/{f}.wav'), g)[int(th * SR):]; t = c + shift + ld; put(vl, t)
    TL['inserts'].append({'file': f, 't': round(t, 3), 'd': round(len(vl) / SR, 3), 'cut': c})
    shift += len(vl) / SR + pd; pos = c
seg = body[int(pos * SR):]; put(seg, pos + shift); addwords(pos, 1e9, shift)
end = pos + shift + len(seg) / SR
TL['vo_end'] = round(end, 3); TL['end'] = round(end + END_PAD, 3)
out = out[:int(TL['end'] * SR)]
out = np.clip(out, -32767, 32767).astype(np.int16)
w = wave.open('../ses/vo.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()
FIX = {'kilikap.': "kill'i kap.", 'Kilgoldu': 'Kill goldu', 'Bey': 'base', 'satarken': 'atarken', 'hedefi': 'hedefli', 'ürünüyle': 'rünüyle', 'Ölüm': 'Ölümateşi', 'ateşi': '', 'dokunuş': 'Dokunuşu',
       'item': 'item', 'itemın': 'itemın', 'alternatörün': "Alternatör'ün", 'hala': 'hâlâ', 'kılpayı': 'kıl payı', 'Hepsi,': 'hepsi.'}
words = [[s, e, FIX.get(t, t)] for s, e, t in words]; words = [x for x in words if x[2]]
open('words.js', 'w').write('const WORDS=' + json.dumps(words, ensure_ascii=False) + ';')
json.dump(TL, open('timeline.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(TL, ensure_ascii=False))
