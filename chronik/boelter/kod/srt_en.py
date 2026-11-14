# English subtitle track for the German Bölter short, timed to the German words (words.json): one cue per German sentence
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [
 ('Zwei Tiger gegen 22 sowjetische Panzer, und 15 davon schoss er selbst ab.', 'Two Tigers against 22 Soviet tanks, and he knocked out 15 of them himself.'),
 ('Siebenmal wurde er im Krieg verwundet, und trotzdem überlebte er.', 'He was wounded seven times in the war, and yet he survived.'),
 ('Sein Name war Johannes Bölter.', 'His name was Johannes Bölter.'),
 ('Er wurde 1915 geboren.', 'He was born in 1915.'),
 ('Schon 1941 wurde er an der Ostfront vor Leningrad verwundet.', 'As early as 1941 he was wounded on the Eastern Front outside Leningrad.'),
 ('Später kam er zur schweren Panzer-Abteilung 502 und erhielt einen Tiger.', 'Later he joined Heavy Tank Battalion 502 and was given a Tiger.'),
 ('Am 7. April 1944 zerstörte er südlich von Pskow zusammen mit einem zweiten Tiger 22 sowjetische Panzer, 15 davon selbst.', 'On 7 April 1944, south of Pskov, he and a second Tiger destroyed 22 Soviet tanks, 15 of them by himself.'),
 ('Dafür erhielt er das Ritterkreuz.', "For this he received the Knight's Cross."),
 ('Im September 1944 folgte als Leutnant das Eichenlaub.', 'In September 1944, as a lieutenant, he was awarded the Oak Leaves.'),
 ('Einen Monat zuvor war er zum siebten Mal verwundet worden.', 'A month earlier he had been wounded for the seventh time.'),
 ('An die Front kehrte er nicht mehr zurück und bildete bis Kriegsende Panzerunteroffiziere aus.', 'He never returned to the front and trained tank NCOs until the end of the war.'),
 ('Ihm werden rund 139 abgeschossene Panzer zugeschrieben, die Angaben schwanken zwischen 89 und 144.', 'He is credited with about 139 tanks destroyed; figures range from 89 to 144.'),
 ('Johannes Bölter starb 1987 mit 72 Jahren.', 'Johannes Bölter died in 1987 at the age of 72.'),
]
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return '%02d:%02d:%06.3f' % (h, m, s)
i = 0; out = []
for k, (de, en) in enumerate(CUES):
    n = len(de.split()); ws = W_[i:i + n]; assert [w[0] for w in ws] == de.split(), (de, [w[0] for w in ws]); i += n
    a = ws[0][1]; b = ws[-1][2] + 0.2
    if i < len(W_): b = min(b, W_[i][1] - 0.02)
    out.append('%d\n%s --> %s\n%s\n' % (k + 1, ts(a).replace('.', ','), ts(b).replace('.', ','), en))
assert i == len(W_)
open(B + 'untertitel/captions.en_US.srt', 'w').write('\n'.join(out)); print(len(out), 'cues')
