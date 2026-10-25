# English subtitle track for the German Udet short, timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Dieses Geräusch war kein Zufall.", "This sound was no accident."),
 ("Die Idee dazu wird einem einzigen Mann zugeschrieben,", "The idea is credited to a single man,"),
 ("und sein eigener Tod wurde später vom Staat vertuscht.", "and his own death was later covered up by the state."),
 ("Sein Name war Ernst Udet.", "His name was Ernst Udet."),
 ("Im Ersten Weltkrieg schoss er 62 Flugzeuge ab,", "In the First World War he shot down 62 aircraft,"),
 ("mehr als jeder andere deutsche Pilot außer Manfred von Richthofen.", "more than any other German pilot except Manfred von Richthofen."),
 ("In Amerika sah er Sturzkampfbomber,", "In America he saw dive bombers"),
 ("die fast senkrecht auf ihr Ziel herabstürzten.", "plunging almost vertically onto their target."),
 ("Mit Geld von Hermann Göring kaufte er 1933", "With money from Hermann Göring, in 1933 he bought"),
 ("zwei dieser Maschinen und brachte sie nach Deutschland.", "two of these aircraft and brought them to Germany."),
 ("Viele Offiziere hielten Sturzkampfbomber für zu gefährlich,", "Many officers thought dive bombers were too dangerous,"),
 ("doch Udet setzte sich durch.", "but Udet got his way."),
 ("Er wurde zum wichtigsten Förderer der Junkers Ju 87, der Stuka.", "He became the main champion of the Junkers Ju 87, the Stuka."),
 ("An ihren Fahrwerksbeinen saßen kleine Propeller.", "Small propellers sat on its landing gear legs."),
 ("Der Fahrtwind trieb sie an,", "The airstream drove them,"),
 ("und je schneller die Maschine stürzte, desto lauter heulten sie.", "and the faster the plane dived, the louder they howled."),
 ("Man nannte sie Jericho-Trompeten.", "They were called Jericho Trumpets."),
 ("In Polen und Frankreich versetzte dieses Heulen Soldaten und Zivilisten in Panik,", "In Poland and France this howl spread panic among soldiers and civilians"),
 ("noch bevor eine Bombe fiel.", "before a single bomb fell."),
 ("Doch die Sirenen bremsten die Maschine,", "But the sirens slowed the aircraft down,"),
 ("und später wurden sie bei vielen Stukas wieder abgebaut.", "and later they were removed from many Stukas."),
 ("Udet stieg zum Generalluftzeugmeister auf", "Udet rose to head of Luftwaffe equipment"),
 ("und war nun für die gesamte Flugzeugproduktion verantwortlich.", "and was now responsible for all aircraft production."),
 ("Für diese Aufgabe war der einstige Kunstflieger nicht geschaffen.", "The former stunt pilot was not made for this job."),
 ("Als die Luftwaffe immer mehr Maschinen verlor,", "As the Luftwaffe lost more and more aircraft,"),
 ("gab Göring ihm die Schuld.", "Göring blamed him."),
 ("Am 17. November 1941 erschoss sich Ernst Udet.", "On 17 November 1941, Ernst Udet shot himself."),
 ("Offiziell hieß es,", "Officially, it was announced"),
 ("er sei beim Erproben einer neuen Waffe tödlich verunglückt.", "that he had died in an accident while testing a new weapon."),
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
