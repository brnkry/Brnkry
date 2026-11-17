import sys, os, numpy as np, subprocess, wave
sys.argv = ['x', 'T']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlib import K, T_END, B
SR = 48000; N = int((T_END + 0.5) * SR); fx = np.zeros(N, np.float32); rng = np.random.default_rng(3)
def whoosh(t, d=0.5, g=0.35):
    n = int(d * SR); x = rng.standard_normal(n).astype(np.float32); env = np.sin(np.linspace(0, np.pi, n)) ** 2
    k = np.linspace(0.02, 0.25, n); y = np.zeros(n, np.float32); a = 0
    for i in range(n): a += k[i] * (x[i] - a); y[i] = a
    i0 = int((t - d * 0.6) * SR); i0 = max(0, i0); fx[i0:i0 + n] += (y * env * g * 3)[:N - i0]
def boom(t, g=0.6):
    n = int(1.2 * SR); tt = np.arange(n) / SR; y = np.sin(2 * np.pi * (55 - 20 * tt) * tt) * np.exp(-tt * 4) + rng.standard_normal(n) * np.exp(-tt * 18) * 0.3
    i0 = int(t * SR); fx[i0:i0 + n] += (y * g).astype(np.float32)[:N - i0]
for ph in ['Ein Jahr zuvor', 'Juni 1942:', 'Bei Gazala', 'Churchill befahl', 'Am 20. Juni', 'Pioniere überbrückten', 'Um 13 Uhr', 'Am Abend brannte', 'Am nächsten Morgen', 'Hitler ernannte', 'Mit dem erbeuteten', 'Heute liegen']: whoosh(K(ph))
for ph in ['kapitulierte Klopper.', 'gestoppt wurde.', 'bombardierten Stukas']: boom(K(ph))
boom(0.2, 0.5)
fx = np.clip(fx, -1, 1); w = wave.open(B + 'fx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((fx * 32000).astype(np.int16).tobytes()); w.close()
print(T_END)
