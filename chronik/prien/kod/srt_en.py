# English subtitle track for the German Egon Mayer short, timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Er versenkte ein britisches Schlachtschiff mitten im wichtigsten Stützpunkt der Royal Navy, und anderthalb Jahre später verschwand er spurlos im Atlantik.", "He sank a British battleship in the heart of the Royal Navy's most important base, and a year and a half later he vanished without a trace in the Atlantic."),
 ("Sein Name war Günther Prien.", "His name was Günther Prien."),
 ("Er wurde 1908 in Osterfeld geboren und fuhr schon als Jugendlicher zur See, zuerst auf einem Segelschiff.", "He was born in Osterfeld in 1908 and went to sea as a teenager, first on a sailing ship."),
 ("In der Weltwirtschaftskrise verlor er seine Stelle bei der Handelsmarine.", "In the Great Depression he lost his job in the merchant navy."),
 ("Er trat in die NSDAP ein und ging zur Reichsmarine.", "He joined the Nazi party and entered the Reichsmarine."),
 ("Bei Kriegsbeginn kommandierte er das U-Boot U 47.", "When the war began he commanded the submarine U-47."),
 ("In der Nacht zum 14. Oktober 1939 drang er in Scapa Flow ein, den Stützpunkt der britischen Heimatflotte auf den Orkney-Inseln.", "On the night of 14 October 1939 he slipped into Scapa Flow, the base of the British Home Fleet in the Orkney Islands."),
 ("Er schlich durch eine schmale Durchfahrt zwischen versenkten Blockschiffen.", "He crept through a narrow channel between sunken blockships."),
 ("Die meisten Schiffe waren ausgelaufen, doch das Schlachtschiff Royal Oak lag vor Anker.", "Most ships had left, but the battleship Royal Oak lay at anchor."),
 ("Der erste Angriff traf nur den Bug.", "The first attack only hit the bow."),
 ("Prien ließ nachladen und griff ein zweites Mal an.", "Prien had the tubes reloaded and attacked a second time."),
 ("Diesmal trafen drei Torpedos.", "This time three torpedoes hit."),
 ("Die Royal Oak kenterte innerhalb von 13 Minuten.", "The Royal Oak capsized within 13 minutes."),
 ("835 Mann starben, mehr als hundert von ihnen waren Jungen unter 18 Jahren.", "835 men died, more than a hundred of them boys under 18."),
 ("U 47 entkam auf demselben Weg.", "U-47 escaped the same way it came."),
 ("In Berlin empfing Hitler die Besatzung, die Propaganda machte Prien zum Stier von Scapa Flow.", "In Berlin Hitler received the crew, and propaganda made Prien the Bull of Scapa Flow."),
 ("Danach versenkte er im Atlantik rund 30 Handelsschiffe.", "He went on to sink around 30 merchant ships in the Atlantic."),
 ("Eines davon war die Arandora Star.", "One of them was the Arandora Star."),
 ("Sie brachte deutsche und italienische Internierte nach Kanada, mehr als 800 Menschen kamen ums Leben.", "She was carrying German and Italian internees to Canada; more than 800 people died."),
 ("Im März 1941 griff U 47 im Nordatlantik einen Geleitzug an.", "In March 1941 U-47 attacked a convoy in the North Atlantic."),
 ("Danach kam kein Funkspruch mehr.", "After that, no further radio message came."),
 ("Die Marineführung verschwieg den Verlust über zehn Wochen lang.", "The naval command kept the loss secret for more than ten weeks."),
 ("Bald hieß es, Prien sei in einem Straflager verschwunden.", "Soon rumours spread that Prien had disappeared into a penal camp."),
 ("Was mit U 47 und seinen 45 Mann geschah, ist bis heute nicht geklärt.", "What happened to U-47 and its 45 men remains unresolved to this day."),
 ("Günther Prien wurde 33 Jahre alt.", "Günther Prien was 33 years old."),
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
