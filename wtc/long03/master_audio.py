# One continuous soundtrack for the whole long video: every part's voice + SFX placed on the
# timeline, one uninterrupted music bed ducked under the voice. Parts overlap by XF (video xfade).
# usage: python3 master_audio.py   (reads PARTS below, writes master.wav and offsets.json)
import json, subprocess, numpy as np
src = open('audio_hook.py').read().split('\n')
i0 = next(i for i,l in enumerate(src) if l.startswith('sfx = np.zeros(N + SR * 3)'))
i1 = next(i for i,l in enumerate(src) if l.startswith('# ---------------- MUSIC'))
i2 = next(i for i,l in enumerate(src) if l.startswith('music *= fo'))
prefix = '\n'.join(src[:i0])            # SFX synths + GEN
music_src = '\n'.join(src[i1:i2 + 1])    # MUSIC section
ns = {}; exec(prefix, ns)
SR = ns['SR']; np_ = np
XF = 0.35
# per-type trims so low/long effects never mask the voice
VOLMUL = dict(thud=.3, rev=.35, starter=.45, catch=.4, stutter=.4, bloom=.45, squeeze=.45, whoosh=.65, pump=.55, alarm=.5, idle=.6, boot=.6, air=.7, glow=.7, puff=.6, hiss=.7, whir=.6)
PARTS = json.load(open('parts.json'))    # [[events_json, voice_mp3, duration], ...]
offs = []; o = 0.0
for i, (_, _, d) in enumerate(PARTS):
    offs.append(round(o, 3)); o += d - XF
TOTAL = offs[-1] + PARTS[-1][2]
N = int(SR * TOTAL)
def load(f):
    raw = subprocess.run(['ffmpeg','-v','error','-i',f,'-f','s16le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float64) / 32768
v = np.zeros(N + SR * 4); sfx = np.zeros(N + SR * 4)
for (ev, vo, d), off in zip(PARTS, offs):
    x = load(vo); s = int(off * SR); v[s:s + len(x)] += x
    for t0, typ, dd, vol in json.load(open(ev)):
        y = (ns['crank'](dd, t0) if typ == 'crank' else ns['GEN'][typ](dd)) * vol * VOLMUL.get(typ, 1.0)
        s = int((off + t0) * SR); sfx[s:s + len(y)] += y
v = v[:N]; sfx = sfx[:N]
# music bed over the full length
ns['DUR'] = TOTAL; ns['N'] = N
exec(music_src.replace('music_end = 37.2', f'music_end = {TOTAL - 0.8}'), ns)
music = ns['music']
def movavg(x, w):
    c = np.cumsum(np.insert(x, 0, 0.0)); y = (c[w:] - c[:-w]) / w
    return np.concatenate([np.full(w // 2, y[0]), y, np.full(len(x) - len(y) - w // 2, y[-1])])
env = np.sqrt(np.maximum(movavg(v ** 2, int(0.08 * SR)), 0))
act = np.clip(env / (np.percentile(env[env > 0.01], 50) + 1e-9), 0, 1)
act = movavg(act, int(0.25 * SR))
mduck = 1 - 0.55 * np.clip(act, 0, 1)
rms = lambda x: np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2))
vr = rms(v)
music = music / rms(music) * vr * 0.32 * mduck
sfx_level = vr / (rms(sfx) + 1e-9) * 0.42
mix = v + music + sfx * sfx_level
mix = mix / np.max(np.abs(mix)) * 0.93
ns['wavfile'].write('master.wav', SR, (mix * 32767).astype(np.int16))
json.dump({'offsets': offs, 'total': TOTAL, 'xf': XF}, open('offsets.json', 'w'))
print('total', round(TOTAL, 2), 'offsets', offs)
