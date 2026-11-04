# English subtitle track for the German Laconia short, timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Er versenkte ein Schiff, rettete danach Hunderte Schiffbrüchige und wurde dafür bombardiert.", "He sank a ship, then rescued hundreds of survivors and was bombed for it."),
 ("Im September 1942 lag U 156 vor der Küste Westafrikas.", "In September 1942 U-156 was off the coast of West Africa."),
 ("Am Abend des 12. September torpedierte Kommandant Werner Hartenstein das britische Truppentransportschiff Laconia.", "On the evening of 12 September, commander Werner Hartenstein torpedoed the British troopship Laconia."),
 ("An Bord waren rund 2.700 Menschen:", "About 2,700 people were on board:"),
 ("britische Soldaten, Zivilisten mit Frauen und Kindern, polnische Wachsoldaten und etwa 1.800 italienische Kriegsgefangene.", "British soldiers, civilians including women and children, Polish guards and about 1,800 Italian prisoners of war."),
 ("Als U 156 auftauchte, hörte die Besatzung aus dem Wasser Hilferufe auf Italienisch.", "When U-156 surfaced, the crew heard cries for help in Italian from the water."),
 ("Hartenstein begriff, dass er auch Soldaten des eigenen Verbündeten getroffen hatte, und begann eine Rettung.", "Hartenstein realised he had also hit soldiers of his own ally, and began a rescue."),
 ("Er nahm Schiffbrüchige an Bord, bis das Deck voller Menschen war, und nahm Rettungsboote ins Schlepptau.", "He took survivors on board until the deck was full of people, and took lifeboats in tow."),
 ("Dann funkte er offen auf Englisch: Er werde kein Schiff angreifen, das den Schiffbrüchigen hilft, solange er selbst nicht angegriffen werde.", "Then he radioed openly in English that he would not attack any ship helping the survivors, as long as he was not attacked himself."),
 ("Dönitz schickte weitere U-Boote, und auch ein italienisches U-Boot kam zu Hilfe.", "Dönitz sent more U-boats, and an Italian submarine came to help as well."),
 ("Am 16. September fuhr U 156 mit einer großen Rotkreuzflagge auf der Brücke den französischen Schiffen entgegen, die die Überlebenden übernehmen sollten.", "On 16 September U-156, with a large Red Cross flag on the bridge, headed for the French ships that were to take over the survivors."),
 ("Da tauchte ein amerikanischer Bomber vom Typ B-24 auf.", "Then an American B-24 bomber appeared."),
 ("Die Besatzung meldete den Fund nach Ascension, und von dort kam der Befehl zum Angriff.", "The crew reported the sighting to Ascension, and from there came the order to attack."),
 ("Eine Bombe schlug zwischen den Rettungsbooten ein, Dutzende Schiffbrüchige starben.", "A bomb struck among the lifeboats, and dozens of survivors died."),
 ("Hartenstein musste die Menschen auf seinem Deck ins Wasser schicken und tauchte ab.", "Hartenstein had to send the people on his deck into the water and dived."),
 ("Am nächsten Tag nahmen französische Kriegsschiffe die meisten Überlebenden auf.", "The next day French warships picked up most of the survivors."),
 ("Trotzdem kamen insgesamt mehr als 1.600 Menschen ums Leben, die meisten von ihnen italienische Gefangene.", "Even so, more than 1,600 people died in total, most of them Italian prisoners."),
 ("Dönitz reagierte mit dem Laconia-Befehl: Kein U-Boot sollte mehr Schiffbrüchige retten.", "Dönitz responded with the Laconia Order: no U-boat was to rescue survivors any more."),
 ("Nach dem Krieg wurde ihm dieser Befehl in Nürnberg vorgeworfen.", "After the war this order was held against him at Nuremberg."),
 ("Das Gericht sah jedoch nicht als erwiesen an, dass er damit die Tötung von Schiffbrüchigen angeordnet hatte.", "But the court did not find it proven that he had thereby ordered the killing of survivors."),
 ("Hartenstein erlebte das nicht mehr.", "Hartenstein did not live to see it."),
 ("Im März 1943 versenkte ein amerikanisches Flugzeug U 156 östlich von Barbados, und die gesamte Besatzung kam ums Leben.", "In March 1943 an American aircraft sank U-156 east of Barbados, and the entire crew was lost."),
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
