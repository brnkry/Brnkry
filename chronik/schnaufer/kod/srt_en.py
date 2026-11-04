# English subtitle track for the German Schnaufer short, timed to the German words (words.json): one cue per German sentence
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German sentence, English)
 ("Der erfolgreichste Nachtjäger der Geschichte überlebte 164 Feindflüge und starb fünf Jahre nach dem Krieg auf einer Landstraße in Frankreich.", "The most successful night fighter pilot in history survived 164 combat missions and died five years after the war on a country road in France."),
 ("Sein Name war Heinz-Wolfgang Schnaufer.", "His name was Heinz-Wolfgang Schnaufer."),
 ("Er wurde 1922 in Calw geboren, wo seine Familie eine Weinkellerei betrieb.", "He was born in Calw in 1922, where his family ran a wine business."),
 ("Mit 17 Jahren machte er Abitur und ging zur Luftwaffe.", "At 17 he finished school and joined the Luftwaffe."),
 ("Nach der Ausbildung kam er zur Nachtjagd und flog eine Messerschmitt Bf 110.", "After training he was posted to the night fighters and flew a Messerschmitt Bf 110."),
 ("Seine Gegner waren die Bomber der Royal Air Force, die nachts deutsche Städte angriffen.", "His opponents were the bombers of the Royal Air Force, which attacked German cities by night."),
 ("Seinen ersten Abschuss erzielte er im Juni 1942, eine Halifax beim Angriff auf Köln.", "He scored his first victory in June 1942, a Halifax during the raid on Cologne."),
 ("Er flog fast immer mit derselben Besatzung, dem Funker Fritz Rumpelhardt und dem Bordschützen Wilhelm Gänsler.", "He almost always flew with the same crew, radio operator Fritz Rumpelhardt and gunner Wilhelm Gänsler."),
 ("Am Ende trugen alle drei das Ritterkreuz.", "In the end all three wore the Knight's Cross."),
 ("Bei den Alliierten hieß er nach seinem Flugplatz in Belgien das Gespenst von St. Trond.", "The Allies called him the Ghost of St. Trond, after his airfield in Belgium."),
 ("Im Oktober 1944 meldete er seinen hundertsten Abschuss.", "In October 1944 he reported his hundredth victory."),
 ("Wenig später wurde er mit 22 Jahren Kommodore des Nachtjagdgeschwaders 4, der jüngste der Luftwaffe.", "Shortly afterwards, at 22, he became commander of Night Fighter Wing 4, the youngest wing commander in the Luftwaffe."),
 ("Am 21. Februar 1945 wurden ihm an einem einzigen Tag neun Lancaster-Bomber zugeschrieben, sieben davon am Abend innerhalb von 19 Minuten.", "On 21 February 1945 he was credited with nine Lancaster bombers in a single day, seven of them in the evening within 19 minutes."),
 ("Insgesamt waren es 121 Abschüsse, fast alle viermotorige Bomber mit je sieben Mann Besatzung.", "In total there were 121 victories, almost all four-engined bombers with a crew of seven each."),
 ("Nach dem Krieg stellten die Briten seine Bf 110 im Londoner Hyde Park aus.", "After the war the British put his Bf 110 on display in London's Hyde Park."),
 ("Ein Seitenleitwerk mit allen 121 Markierungen steht heute im Imperial War Museum.", "A tail fin with all 121 markings is now in the Imperial War Museum."),
 ("Schnaufer kam in britische Gefangenschaft und übernahm danach die Weinkellerei der Familie.", "Schnaufer became a British prisoner of war and afterwards took over the family wine business."),
 ("Im Juli 1950 war er auf Einkaufsreise in Frankreich.", "In July 1950 he was on a buying trip in France."),
 ("Südlich von Bordeaux stieß sein Wagen an einer Kreuzung mit einem Lastwagen zusammen, der leere Gasflaschen geladen hatte.", "South of Bordeaux his car collided at a crossroads with a lorry loaded with empty gas cylinders."),
 ("Zwei Tage später starb er im Krankenhaus.", "Two days later he died in hospital."),
 ("Heinz-Wolfgang Schnaufer wurde 28 Jahre alt.", "Heinz-Wolfgang Schnaufer was 28 years old."),
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
