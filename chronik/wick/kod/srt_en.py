# English subtitle track for the German Wick short, timed to the German words (words.json): one cue per German sentence
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German sentence, English)
 ("Er wurde der erfolgreichste Jagdflieger der Luftwaffe, und nur zwei Stunden später verschwand er über dem Ärmelkanal.", "He became the Luftwaffe's most successful fighter pilot, and only two hours later he vanished over the English Channel."),
 ("Sein Name war Helmut Wick.", "His name was Helmut Wick."),
 ("Er wurde 1915 in Mannheim geboren und trat 1936 in die Luftwaffe ein.", "He was born in Mannheim in 1915 and joined the Luftwaffe in 1936."),
 ("In der Ausbildung galt er als durchschnittlicher Flieger, einen Lehrgang bestand er erst im zweiten Anlauf.", "In training he was seen as an average pilot, and he passed one course only at the second attempt."),
 ("Im Jagdgeschwader 53 lernte er die Messerschmitt Bf 109 unter Werner Mölders kennen.", "In Fighter Wing 53 he learned to fly the Messerschmitt Bf 109 under Werner Mölders."),
 ("Bei Kriegsbeginn kam er zum Jagdgeschwader 2 Richthofen.", "When the war began he joined Fighter Wing 2 Richthofen."),
 ("Im November 1939 schoss er bei Nancy ein französisches Jagdflugzeug ab, seinen ersten Luftsieg.", "In November 1939 he shot down a French fighter near Nancy, his first victory."),
 ("Im Frankreichfeldzug und in der Luftschlacht um England stiegen seine Zahlen schnell.", "In the Battle of France and the Battle of Britain his score rose quickly."),
 ("Im Oktober 1940 erhielt er als vierter Soldat der Wehrmacht das Eichenlaub zum Ritterkreuz.", "In October 1940 he became the fourth soldier of the Wehrmacht to receive the Oak Leaves to the Knight's Cross."),
 ("Kurz darauf wurde er mit 25 Jahren Kommodore des Geschwaders, der jüngste der Luftwaffe.", "Shortly afterwards, at 25, he became commander of the wing, the youngest in the Luftwaffe."),
 ("Die Propaganda stellte ihn der ausländischen Presse als Helden vor.", "Propaganda presented him to the foreign press as a hero."),
 ("Am 28. November 1940 flog er mit seinem Stabsschwarm zur Isle of Wight und schoss eine Spitfire ab, seinen 55. Luftsieg.", "On 28 November 1940 he flew with his staff flight to the Isle of Wight and shot down a Spitfire, his 55th victory."),
 ("Damit lag er vor Mölders.", "That put him ahead of Mölders."),
 ("Nach der Landung in Cherbourg ließ er tanken und startete erneut.", "After landing in Cherbourg he had his aircraft refuelled and took off again."),
 ("Über der Insel schoss er eine weitere Spitfire ab.", "Over the island he shot down another Spitfire."),
 ("Kurz darauf griffen Spitfires der britischen 609. Staffel seinen Schwarm an.", "Shortly afterwards, Spitfires of the British 609 Squadron attacked his flight."),
 ("Wicks Maschine wurde getroffen, wahrscheinlich von dem britischen Piloten John Dundas.", "Wick's aircraft was hit, probably by the British pilot John Dundas."),
 ("Sein Rottenflieger Rudolf Pflanz schoss die Spitfire sofort ab, Dundas stürzte mit ihr ins Meer.", "His wingman Rudolf Pflanz shot down the Spitfire at once, and Dundas went into the sea with it."),
 ("Pflanz hatte gesehen, wie der deutsche Pilot mit dem Fallschirm absprang, und berichtete später von einem Schlauchboot.", "Pflanz had seen the German pilot bail out with his parachute, and later reported a dinghy."),
 ("Torpedoboote suchten die ganze Nacht, am nächsten Tag Flugzeuge und Seenotdienst.", "Torpedo boats searched all night, and the next day aircraft and the sea rescue service."),
 ("Wick wurde nie gefunden.", "Wick was never found."),
 ("Ihm wurden 56 Luftsiege zugeschrieben, es war sein 168. Feindflug.", "He was credited with 56 victories, and it was his 168th combat mission."),
 ("Helmut Wick wurde 25 Jahre alt.", "Helmut Wick was 25 years old."),
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
