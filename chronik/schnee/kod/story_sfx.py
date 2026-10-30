import sys
sys.path.insert(0, sys.argv[1])
from sfxlib import *
sr, base = wavfile.read(sys.argv[2]); base = base.astype(float) / 32768
n = int(6.85 * SR); out[:n] += base[:n] * np.linspace(1, 1, n)[:, None]
add(6.9, whoosh(1.0, 150, 900), 0.09)
add(7.25, thud(0.9, 80), 0.12); add(7.55, whoosh(0.5, 300, 1500), 0.05); add(7.85, thud(1.0, 70), 0.12)
for i in range(3): add(8.65 + i * 0.35, thud(0.6, 120 + 20 * i), 0.10)
y = out[:int(11.0 * SR)]; y /= max(1.0, np.abs(y).max() / 0.95)
wavfile.write(sys.argv[3], SR, (y * 32767).astype(np.int16)); print('ok')
