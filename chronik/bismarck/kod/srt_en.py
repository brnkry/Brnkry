# English subtitle track for the German Egon Mayer short, timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Eines der größten Schlachtschiffe Europas wurde von einem langsamen Doppeldecker mit Stoffbespannung gestoppt.", "One of the largest battleships in Europe was stopped by a slow, fabric-covered biplane."),
 ("Ihr Name war Bismarck.", "Her name was Bismarck."),
 ("Im Mai 1941 lief sie zu ihrer ersten und einzigen Feindfahrt aus.", "In May 1941 she set out on her first and only combat sortie."),
 ("In der Dänemarkstraße traf sie auf den britischen Schlachtkreuzer Hood.", "In the Denmark Strait she met the British battlecruiser Hood."),
 ("Nach acht Minuten Feuer flog die Hood in die Luft.", "After eight minutes of firing, the Hood blew up."),
 ("Von über 1.400 Mann überlebten drei.", "Of more than 1,400 men, three survived."),
 ("Doch auch die Bismarck war getroffen.", "But the Bismarck had been hit as well."),
 ("Aus einem Leck im Bug lief Treibstoff aus, und Admiral Lütjens nahm Kurs auf Frankreich.", "Fuel leaked from a hole in her bow, and Admiral Lütjens set course for France."),
 ("Die Royal Navy jagte sie daraufhin mit Dutzenden Schiffen.", "The Royal Navy then hunted her with dozens of ships."),
 ("Zwei Tage später griffen 15 Swordfish-Torpedobomber vom Flugzeugträger Ark Royal an.", "Two days later, 15 Swordfish torpedo bombers from the carrier Ark Royal attacked."),
 ("Ein Torpedo traf das Heck und blockierte das Ruder.", "One torpedo hit the stern and jammed the rudder."),
 ("Die Bismarck konnte nur noch im Kreis fahren und ihren Verfolgern nicht mehr entkommen.", "The Bismarck could only sail in circles and could no longer escape her pursuers."),
 ("Am nächsten Morgen kamen die Schlachtschiffe King George V und Rodney.", "The next morning the battleships King George V and Rodney arrived."),
 ("Ein Treffer zerstörte die Brücke, die Schiffsführung kam vermutlich ums Leben.", "A hit destroyed the bridge; the ship's command was probably killed."),
 ("Der Erste Offizier ließ das Schiff selbst versenken, damit die Besatzung von Bord gehen konnte.", "The executive officer had the ship scuttled so the crew could abandon her."),
 ("Von über 2.200 Mann überlebten 114.", "Of more than 2,200 men, 114 survived."),
 ("Ihr Wrack fand fast fünfzig Jahre später Robert Ballard, der auch die Titanic entdeckt hatte, in fast fünf Kilometern Tiefe.", "Almost fifty years later her wreck was found by Robert Ballard, who had also discovered the Titanic, almost five kilometres down."),
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
