# English subtitle track for the German Egon Mayer short, timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Wer amerikanische Bomber von hinten angriff, flog direkt in ihr Abwehrfeuer.", "Anyone who attacked American bombers from behind flew straight into their defensive fire."),
 ("Egon Mayer griff sie deshalb von vorne an.", "So Egon Mayer attacked them head-on."),
 ("Er wurde 1917 in Konstanz geboren und ging 1937 zur Luftwaffe.", "He was born in Konstanz in 1917 and joined the Luftwaffe in 1937."),
 ("Ab Dezember 1939 flog er im Jagdgeschwader 2 „Richthofen“.", "From December 1939 he flew with Fighter Wing 2 \"Richthofen\"."),
 ("In der Luftschlacht um England wurde er auch selbst abgeschossen.", "In the Battle of Britain he was shot down himself."),
 ("Einmal schwamm er eine Stunde im Ärmelkanal, bis man ihn rettete.", "Once he swam in the English Channel for an hour before he was rescued."),
 ("Ab August 1942 griffen amerikanische B-17 bei Tag Ziele in Frankreich an.", "From August 1942 American B-17s attacked targets in France by day."),
 ("Sie flogen in dichten Formationen und deckten sich gegenseitig mit schweren Maschinengewehren.", "They flew in tight formations and covered each other with heavy machine guns."),
 ("Nur die Nase der Bomber war schwach bewaffnet.", "Only the nose of the bombers was lightly armed."),
 ("Am 23. November 1942 griff Mayer über St. Nazaire frontal an", "On 23 November 1942 Mayer attacked head-on over St Nazaire"),
 ("und meldete zwei B-17 und eine B-24 als abgeschossen.", "and claimed two B-17s and a B-24 shot down."),
 ("Mit Georg-Peter Eder entwickelte er daraus eine Taktik:", "With Georg-Peter Eder he turned this into a tactic:"),
 ("von vorne anfliegen, kurz feuern, dann steil wegziehen.", "come in from the front, fire a short burst, then pull away steeply."),
 ("Der Frontalangriff wurde weitgehend zum Standardverfahren der deutschen Jäger.", "The head-on attack largely became the standard method of German fighters."),
 ("Die Amerikaner bauten später einen zusätzlichen Waffenturm unter die Nase der B-17.", "The Americans later added an extra gun turret under the nose of the B-17."),
 ("Im Juli 1943 wurde Mayer Kommodore seines Geschwaders.", "In July 1943 Mayer became commander of his wing."),
 ("Im September 1943 wurden ihm drei B-17 innerhalb von 19 Minuten zugeschrieben.", "In September 1943 he was credited with three B-17s within 19 minutes."),
 ("Im Februar 1944 erreichte er als erster Jagdflieger an der Kanalfront 100 Luftsiege.", "In February 1944 he became the first fighter pilot on the Channel front to reach 100 victories."),
 ("Am 2. März 1944 führte er einen Angriff auf B-17 bei Sedan.", "On 2 March 1944 he led an attack on B-17s near Sedan."),
 ("Amerikanische Begleitjäger vom Typ P-47 schossen seine Focke-Wulf ab.", "American P-47 escort fighters shot down his Focke-Wulf."),
 ("Sie stürzte bei Montmédy ab.", "It crashed near Montmédy."),
 ("Egon Mayer wurde 26 Jahre alt.", "Egon Mayer was 26 years old."),
 ("Ihm wurden 102 Luftsiege zugeschrieben, alle im Westen.", "He was credited with 102 aerial victories, all in the West."),
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
