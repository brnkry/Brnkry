# English subtitle track for the German Kittel short, timed to the German words (words.json): one cue per German sentence
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German sentence, English)
 ("Er schoss 94 sowjetische Schlachtflugzeuge vom Typ Il-2 ab, und am Ende traf ihn der Bordschütze einer Il-2.", "He shot down 94 Soviet Il-2 ground-attack aircraft, and in the end the rear gunner of an Il-2 hit him."),
 ("Sein Name war Otto Kittel.", "His name was Otto Kittel."),
 ("Er wurde 1917 in Kronsdorf im Sudetenland geboren, als Sohn eines Landwirts, und arbeitete kurz als Kraftfahrzeugmechaniker.", "He was born in 1917 in Kronsdorf in the Sudetenland, the son of a farmer, and worked briefly as a car mechanic."),
 ("1939 trat er in die Luftwaffe ein.", "In 1939 he joined the Luftwaffe."),
 ("Im Februar 1941 kam er zum Jagdgeschwader 54, das an der Ostfront vor Leningrad eingesetzt wurde.", "In February 1941 he joined Fighter Wing 54, which was deployed on the Eastern Front before Leningrad."),
 ("Am 19. Februar 1943 erzielte er seinen 39. Luftsieg, zugleich den 4000. seines Geschwaders.", "On 19 February 1943 he scored his 39th victory, which was also the 4,000th of his wing."),
 ("Vier Wochen später fiel bei einem Einsatz der Motor seiner Focke-Wulf 190 aus.", "Four weeks later the engine of his Focke-Wulf 190 failed during a mission."),
 ("Er musste rund 60 Kilometer hinter der sowjetischen Front notlanden.", "He had to make a forced landing about 60 kilometres behind the Soviet front."),
 ("Zu Fuß schlug er sich durch, über den zugefrorenen Ilmensee, und erreichte nach etwa drei Tagen die deutschen Linien.", "He made his way back on foot, across frozen Lake Ilmen, and reached the German lines after about three days."),
 ("Danach stiegen seine Zahlen schnell.", "After that his score rose quickly."),
 ("Im September 1943 erzielte er seinen 100. Luftsieg, im Oktober erhielt er das Ritterkreuz, im April 1944 das Eichenlaub.", "In September 1943 he scored his 100th victory, in October he received the Knight's Cross, and in April 1944 the Oak Leaves."),
 ("Im November 1944 bekam er als Oberleutnant und Staffelkapitän die Schwerter.", "In November 1944, as a first lieutenant and squadron leader, he was awarded the Swords."),
 ("Zu dieser Zeit lag sein Geschwader im Kurland-Kessel in Lettland, abgeschnitten vom Reich.", "By then his wing was in the Courland Pocket in Latvia, cut off from the Reich."),
 ("Im Februar 1945 griff er im Tiefflug eine Gruppe Il-2 an.", "In February 1945 he attacked a group of Il-2s at low level."),
 ("Seine Maschine wurde vom Abwehrfeuer getroffen und stürzte bei Džūkste ab.", "His aircraft was hit by defensive fire and crashed near Džūkste."),
 ("Kein deutscher Zeuge sah den Absturz.", "No German witness saw the crash."),
 ("Ihm wurden 267 Luftsiege zugeschrieben, alle an der Ostfront, in 583 Einsätzen.", "He was credited with 267 victories, all on the Eastern Front, in 583 missions."),
 ("Er war der erfolgreichste deutsche Jagdflieger, der im Kampf fiel.", "He was the most successful German fighter pilot to be killed in action."),
 ("Otto Kittel wurde 27 Jahre alt.", "Otto Kittel was 27 years old."),
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
