# English subtitle track for the German Berlin 1945 short, timed to the German words (words.json) plus the 0.2 s voice delay of the mix
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json')); OFF = 0.2
CUES = [
 ('Die Amerikaner standen an der Elbe, nur 85 Kilometer vor Berlin.', 'The Americans stood on the Elbe, just 85 kilometres from Berlin.'),
 ('Dann hielten sie an.', 'Then they stopped.'),
 ('Eisenhower hatte Stalin geschrieben, er werde nicht auf Berlin vorstoßen.', 'Eisenhower had written to Stalin that he would not push on to Berlin.'),
 ('Stalin antwortete, Berlin habe keine Bedeutung mehr.', 'Stalin replied that Berlin no longer mattered.'),
 ('Gleichzeitig befahl er den Angriff.', 'At the same time, he ordered the attack.'),
 ('Am 16. April 1945 griffen 2,5 Millionen sowjetische und polnische Soldaten an.', 'On 16 April 1945, 2.5 million Soviet and Polish soldiers attacked.'),
 ('Schukow sollte frontal über die Oder vorstoßen, Konew von Süden herum.', 'Zhukov was to strike head-on across the Oder, Konev around from the south.'),
 ('An den Seelower Höhen ließ Schukow 143 Scheinwerfer einschalten, um die Verteidiger zu blenden.', 'At the Seelow Heights, Zhukov switched on 143 searchlights to blind the defenders.'),
 ('Doch sie beleuchteten nur Rauch und Staub, und seine Panzer blieben im Sumpf stecken.', 'But they only lit up smoke and dust, and his tanks got stuck in the marshes.'),
 ('Konew kam schneller voran.', 'Konev advanced faster.'),
 ('Am 25. April war Berlin eingeschlossen.', 'By 25 April, Berlin was surrounded.'),
 ('Am selben Tag trafen sich Amerikaner und Sowjets bei Torgau an der Elbe.', 'That same day, Americans and Soviets met at Torgau on the Elbe.'),
 ('In der Stadt wurde um jede Straße gekämpft.', 'Inside the city, every street was fought over.'),
 ('Am 30. April stürmten sowjetische Soldaten den Reichstag.', 'On 30 April, Soviet soldiers stormed the Reichstag.'),
 ('Am Nachmittag nahm sich Hitler im Bunker das Leben.', 'That afternoon, Hitler killed himself in his bunker.'),
 ('Am 2. Mai kapitulierte Berlin.', 'On 2 May, Berlin surrendered.'),
 ('Die Rote Armee verlor über 350.000 Mann an Toten und Verwundeten, rund 100.000 deutsche Soldaten starben, dazu Zehntausende Zivilisten.', 'The Red Army lost over 350,000 men killed and wounded, around 100,000 German soldiers died, along with tens of thousands of civilians.'),
 ('Die Inschriften der sowjetischen Soldaten stehen bis heute an den Wänden des Reichstags.', "The Soviet soldiers' inscriptions are still on the walls of the Reichstag today."),
]
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return ('%02d:%02d:%06.3f' % (h, m, s)).replace('.', ',')
i = 0; out = []
for k, (de, en) in enumerate(CUES):
    n = len(de.split()); ws = W_[i:i + n]; assert [w[0] for w in ws] == de.split(), (de, [w[0] for w in ws]); i += n
    a = ws[0][1] + OFF; b = ws[-1][2] + OFF + 0.2
    if i < len(W_): b = min(b, W_[i][1] + OFF - 0.02)
    out.append('%d\n%s --> %s\n%s\n' % (k + 1, ts(a), ts(b), en))
assert i == len(W_)
open(sys.argv[2], 'w').write('\n'.join(out)); print(len(out), 'cues')
