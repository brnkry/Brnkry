# fx track from ElevenLabs sound effects, kept low under the voice
import sys, os, subprocess, wave, numpy as np
sys.argv = ['x', 'T']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlib import K, T_END, B
SR = 48000
def load(n):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', B + 'sfx/' + n + '.mp3', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
    return a / (np.abs(a).max() + 1e-9)
WH, IM, ST = load('whoosh'), load('impact'), load('stuka')
N = int((T_END + 1) * SR); fx = np.zeros(N, np.float32)
def put(x, t, db, align_peak=False):
    i0 = int(t * SR) - (int(np.argmax(np.abs(x))) if align_peak else 0); i0 = max(0, i0)
    seg = x[:N - i0] * 10 ** (db / 20); fx[i0:i0 + len(seg)] += seg
for ph in ['Ein Jahr zuvor', 'Juni 1942:', 'Bei Gazala', 'Churchill befahl', 'Am 20. Juni', 'Pioniere überbrückten', 'Um 13 Uhr', 'Am Abend brannte', 'Am nächsten Morgen', 'Hitler ernannte', 'Mit dem erbeuteten', 'Heute liegen']: put(WH, K(ph), -20, True)
for ph in ['kapitulierte Klopper.', 'gestoppt wurde.']: put(IM, K(ph), -14, True)
put(ST, K('bombardierten Stukas'), -18)
w = wave.open(B + 'fx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(fx, -1, 1) * 32000).astype(np.int16).tobytes()); w.close(); print('ok')
