# English subtitle track for the German Tobruk 1942 short, timed to the German words (words.json) plus the 0.2 s voice delay of the mix
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json')); OFF = 0.2
CUES = [
 ('Warum ergaben sich hier fast 33.000 alliierte Soldaten nach nur einem Tag Kampf?', 'Why did almost 33,000 Allied soldiers surrender here after just one day of fighting?'),
 ('Ein Jahr zuvor hatte dieselbe Festung Rommel fast acht Monate lang standgehalten.', 'A year earlier, the same fortress had held out against Rommel for almost eight months.'),
 ('Juni 1942: Rommels Afrikakorps gegen Südafrikaner, Briten und Inder.', 'June 1942: Rommel\'s Afrika Korps against South Africans, Britons and Indians.'),
 ('Bei Gazala hatte Rommel die britische Linie im Süden umgangen.', 'At Gazala, Rommel had outflanked the British line in the south.'),
 ('Von rund 850 britischen Panzern waren nur noch etwa 70 einsatzbereit.', 'Of around 850 British tanks, only about 70 were still fit for action.'),
 ('Churchill befahl trotzdem, Tobruk zu halten.', 'Churchill still ordered Tobruk to be held.'),
 ('Doch der rund 50 Kilometer lange Verteidigungsring war verfallen, und der neue Kommandant, General Klopper, führte seine Division erst seit gut einem Monat.', 'But the 50-kilometre defensive ring had fallen into disrepair, and the new commander, General Klopper, had led his division for barely a month.'),
 ('Am 20. Juni um 5:20 Uhr bombardierten Stukas eine Ecke des Rings.', 'On 20 June at 5:20 a.m., Stukas bombed one corner of the ring.'),
 ('Pioniere überbrückten den Panzergraben, und um 7:45 Uhr waren die deutschen Panzer durch.', 'Engineers bridged the anti-tank ditch, and by 7:45 the German tanks were through.'),
 ('Um 13 Uhr hielten sie die Höhen über der Stadt.', 'By 1 p.m. they held the heights above the town.'),
 ('Am Abend brannte der Hafen.', 'By evening, the harbour was burning.'),
 ('Am nächsten Morgen kapitulierte Klopper.', 'The next morning, Klopper surrendered.'),
 ('Für Südafrika war es die schwerste militärische Niederlage seiner Geschichte.', 'For South Africa, it was the worst military defeat in its history.'),
 ('Hitler ernannte Rommel zum Generalfeldmarschall.', 'Hitler promoted Rommel to field marshal.'),
 ('Mit dem erbeuteten Treibstoff fuhr Rommel weiter nach Ägypten, bis er bei El Alamein gestoppt wurde.', 'With the captured fuel, Rommel drove on into Egypt until he was stopped at El Alamein.'),
 ('Heute liegen über 6.000 deutsche Gefallene in einem Ehrenmal bei Tobruk, das selbst wie eine Festung aussieht.', 'Today, more than 6,000 German dead lie in a memorial near Tobruk that itself looks like a fortress.'),
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
