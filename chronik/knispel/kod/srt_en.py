# English subtitle track for the German Dönitz short, timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Fast siebzig Jahre lag er in einem namenlosen Grab hinter einer Kirchenmauer,", "For almost seventy years he lay in a nameless grave behind a church wall,"),
 ("und am Ende erkannte man ihn an einer kleinen Metallmarke.", "and in the end he was identified by a small metal tag."),
 ("Sein Name war Kurt Knispel.", "His name was Kurt Knispel."),
 ("Er war Panzersoldat der Wehrmacht,", "He was a Wehrmacht tank soldier,"),
 ("erst Ladeschütze, dann Richtschütze,", "first a loader, then a gunner,"),
 ("zuletzt Kommandant eines Tigers in der schweren Panzerabteilung 503.", "and finally commander of a Tiger in Heavy Panzer Battalion 503."),
 ("Mit ihr kämpfte er an der Ostfront, 1943 auch bei Kursk.", "With it he fought on the Eastern Front, in 1943 also at Kursk."),
 ("In vielen Büchern werden ihm 168 abgeschossene Panzer zugeschrieben,", "Many books credit him with 168 destroyed tanks,"),
 ("angeblich 126 davon als Richtschütze und 42 als Kommandant.", "supposedly 126 as a gunner and 42 as a commander."),
 ("Genau belegen lässt sich diese Zahl nicht,", "That number cannot be confirmed,"),
 ("denn seine Abteilung zählte keine Abschüsse für einzelne Besatzungen.", "because his battalion did not count kills for individual crews."),
 ("Auch manche Geschichten über ihn gelten unter Historikern als ausgeschmückt.", "Historians also consider some of the stories about him embellished."),
 ("Sicher ist, dass er 1944 das Deutsche Kreuz in Gold erhielt.", "What is certain is that in 1944 he received the German Cross in Gold."),
 ("Das Ritterkreuz bekam er nie, und über den Rang eines Feldwebels kam er nicht hinaus.", "He never received the Knight's Cross and never rose above the rank of sergeant."),
 ("Berichten zufolge galt er als unbequem, widersprach offen seinen Vorgesetzten", "Reportedly he was seen as difficult and openly contradicted his superiors,"),
 ("und trug Haare und Bart länger, als die Vorschrift erlaubte.", "and wore his hair and beard longer than regulations allowed."),
 ("Ende April 1945, wenige Tage vor Kriegsende, wurde sein Königstiger in Südmähren getroffen.", "In late April 1945, days before the end of the war, his King Tiger was hit in South Moravia."),
 ("Nach Angaben seines Funkers verletzte ihn ein Granatsplitter am Kopf.", "According to his radio operator, a shell splinter wounded him in the head."),
 ("Knispel starb in einem Feldlazarett im Dorf Urbau, dem heutigen Vrbovec.", "Knispel died in a field hospital in the village of Urbau, today Vrbovec."),
 ("Danach verlor sich seine Spur.", "After that, all trace of him was lost."),
 ("Erst 2013 fanden Archäologen dort ein Grab mit sechzehn deutschen Soldaten.", "Only in 2013 did archaeologists find a grave there with sixteen German soldiers."),
 ("Bei einem von ihnen lag seine Erkennungsmarke.", "His identity tag lay with one of them."),
 ("Im November 2014 setzte ihn der Volksbund Deutsche Kriegsgräberfürsorge auf dem Soldatenfriedhof in Brünn bei,", "In November 2014 the German War Graves Commission reburied him in the military cemetery in Brno,"),
 ("zwischen Gefallenen, deren Namen kaum noch jemand kennt.", "among fallen soldiers whose names hardly anyone still knows."),
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
