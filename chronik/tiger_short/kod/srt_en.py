# English subtitle track for the German Tiger I short, timed to the German words (words.json, voice text) plus the 0.6 s voice delay
import json, sys
W_ = json.load(open(sys.argv[1])); OFF = 0.6
CUES = [
 ('Ein einziger Panzer, und ganze Kompanien zogen sich zurück.', 'A single tank, and whole companies pulled back.'),
 ('Der Tiger I kam im August 1942 bei Leningrad zum ersten Mal an die Front.', 'The Tiger I first reached the front near Leningrad in August 1942.'),
 ('Seine acht Komma acht Zentimeter Kanone durchschlug feindliche Panzer auf über einen Kilometer, | seine Frontpanzerung war zehn Zentimeter dick.', 'Its 8.8 cm gun knocked out enemy tanks at more than a kilometre, | and its front armour was ten centimetres thick.'),
 ('Viele alliierte Geschosse prallten einfach ab.', 'Many Allied shells simply bounced off.'),
 ('Doch der Tiger hatte seinen Preis.', 'But the Tiger came at a price.'),
 ('Er wog 57 Tonnen, verbrauchte mehrere hundert Liter Benzin auf hundert Kilometer | und fiel oft wegen technischer Probleme aus.', 'It weighed 57 tonnes, burned several hundred litres of petrol per hundred kilometres | and often broke down.'),
 ('Viele Tiger gingen nicht im Kampf verloren, | sondern blieben liegen und wurden von ihren eigenen Besatzungen gesprengt.', 'Many Tigers were not lost in battle, | they broke down and were blown up by their own crews.'),
 ('Nur rund eintausenddreihundertfünfzig Stück wurden gebaut.', 'Only about 1,350 were built.'),
 ('Die Sowjetunion baute im gleichen Zeitraum Zehntausende T vierunddreißig.', 'In the same period the Soviet Union built tens of thousands of T-34s.'),
 ('Der Tiger war gefürchtet, | aber er kam zu spät und in zu kleiner Zahl, um den Krieg zu wenden.', 'The Tiger was feared, | but it came too late and in too small numbers to turn the war.'),
]
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return ('%02d:%02d:%06.3f' % (h, m, s)).replace('.', ',')
i = 0; out = []
for de, en in CUES:
    for dp, ep in zip(de.split(' | '), en.split(' | ')):
        n = len(dp.split()); ws = W_[i:i + n]; assert [w[0] for w in ws] == dp.split(), (dp, [w[0] for w in ws]); i += n
        a = ws[0][1] + OFF; b = ws[-1][2] + OFF + 0.25
        if i < len(W_): b = min(b, W_[i][1] + OFF - 0.02)
        out.append((a, b, ep))
assert i == len(W_)
open(sys.argv[2], 'w').write('\n'.join('%d\n%s --> %s\n%s\n' % (k + 1, ts(a), ts(b), t) for k, (a, b, t) in enumerate(out)))
print(len(out), 'cues')
