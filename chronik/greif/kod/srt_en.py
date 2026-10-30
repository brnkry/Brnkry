# English subtitle track for the German Unternehmen Greif short, timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Im Dezember 1944 mussten amerikanische Generäle beweisen, dass sie Amerikaner waren,", "In December 1944 American generals had to prove that they were American,"),
 ("denn hinter ihren Linien fuhren deutsche Soldaten in amerikanischen Uniformen.", "because German soldiers in American uniforms were driving behind their lines."),
 ("Der Plan hieß Unternehmen Greif.", "The plan was called Operation Greif."),
 ("Geführt wurde er von Otto Skorzeny, dem SS-Offizier,", "It was led by Otto Skorzeny, the SS officer"),
 ("der ein Jahr zuvor Mussolini aus seiner Haft in den Abruzzen befreit hatte.", "who a year earlier had freed Mussolini from captivity in the Abruzzo mountains."),
 ("Für die Ardennenoffensive sollte er eine Truppe aufstellen, die wie Amerikaner aussah und sprach.", "For the Ardennes offensive he was to raise a unit that looked and spoke like Americans."),
 ("Doch es meldeten sich viel zu wenige Freiwillige mit gutem Englisch,", "But far too few volunteers with good English came forward,"),
 ("und statt Hunderter amerikanischer Fahrzeuge bekam Skorzeny nur einige Jeeps, Lastwagen und einen einzigen Sherman.", "and instead of hundreds of American vehicles Skorzeny got only a few jeeps, trucks and a single Sherman."),
 ("Die anderen Panzer wurden mit Blech und Farbe getarnt.", "The other tanks were disguised with sheet metal and paint."),
 ("Am 16. Dezember begann die Offensive.", "On 16 December the offensive began."),
 ("Kleine Kommandos in erbeuteten Jeeps drehten Wegweiser um,", "Small commando teams in captured jeeps turned signposts around,"),
 ("kappten Telefonleitungen und schickten Kolonnen in die falsche Richtung.", "cut telephone lines and sent columns the wrong way."),
 ("Nur wenige Teams kamen durch,", "Only a few teams got through,"),
 ("doch das Gerücht verbreitete sich schneller als sie selbst.", "but the rumour spread faster than they did."),
 ("An jeder Kreuzung stellten amerikanische Posten nun Fangfragen:", "At every crossroads American sentries now asked trick questions:"),
 ("Wer spielt bei den Yankees?", "Who plays for the Yankees?"),
 ("Wie heißt die Freundin von Micky Maus?", "What is the name of Mickey Mouse's girlfriend?"),
 ("General Omar Bradley wurde nach der Hauptstadt von Illinois gefragt.", "General Omar Bradley was asked for the capital of Illinois."),
 ("Gefangene Kommandos behaupteten, ein Team sei unterwegs nach Paris, um Eisenhower zu töten.", "Captured commandos claimed that a team was on its way to Paris to kill Eisenhower."),
 ("Belegt ist das nicht,", "There is no evidence for it,"),
 ("trotzdem verbrachte der Oberbefehlshaber Weihnachten unter strenger Bewachung.", "yet the Supreme Commander spent Christmas under heavy guard."),
 ("Drei Männer wurden bei Aywaille in einem Jeep gestellt.", "Three men were stopped in a jeep near Aywaille."),
 ("Sie kannten das Passwort nicht,", "They did not know the password,"),
 ("ein Militärgericht verurteilte sie als Spione,", "a military court sentenced them as spies,"),
 ("und noch vor Weihnachten wurden sie erschossen.", "and before Christmas they were shot."),
 ("Skorzeny selbst stand 1947 in Dachau vor Gericht und wurde freigesprochen.", "Skorzeny himself stood trial in Dachau in 1947 and was acquitted."),
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
