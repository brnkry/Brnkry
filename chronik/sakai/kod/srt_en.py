# English subtitle track for the German Sakai short, timed to the German words (words.json): one cue per German sentence
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [
 ('Ein Geschoss traf ihn am Kopf, und trotzdem flog er fast fünf Stunden zurück zu seinem Stützpunkt.', 'A bullet hit him in the head, and yet he flew almost five hours back to his base.'),
 ('Sein Name war Saburō Sakai.', 'His name was Saburō Sakai.'),
 ('Er wurde 1916 in der Präfektur Saga auf der Insel Kyūshū geboren.', 'He was born in 1916 in Saga Prefecture on the island of Kyūshū.'),
 ('Mit 16 Jahren trat er in die japanische Marine ein.', 'At 16 he joined the Japanese Navy.'),
 ('1937 schloss er die Pilotenschule in Tsuchiura als Jahrgangsbester ab und erhielt dafür eine silberne Uhr vom Kaiser.', 'In 1937 he graduated from the pilot school at Tsuchiura at the top of his class and received a silver watch from the Emperor.'),
 ('Ab 1938 flog er Einsätze über China.', 'From 1938 he flew missions over China.'),
 ('Im Pazifikkrieg kam er zum Tainan-Geschwader und flog die Mitsubishi Zero, zuerst über den Philippinen, dann von Rabaul auf Neubritannien aus.', 'In the Pacific War he joined the Tainan Air Group and flew the Mitsubishi Zero, first over the Philippines, then from Rabaul on New Britain.'),
 ('Am 7. August 1942 landeten die Amerikaner auf Guadalcanal.', 'On 7 August 1942 the Americans landed on Guadalcanal.'),
 ('Sakai hielt eine Gruppe amerikanischer Flugzeuge für Jäger und griff sie von hinten an.', 'Sakai took a group of American aircraft for fighters and attacked them from behind.'),
 ('Es waren Sturzkampfbomber vom Typ Dauntless, und ihre Heckschützen hatten ihn kommen sehen.', 'They were Dauntless dive bombers, and their rear gunners had seen him coming.'),
 ('Ein Geschoss traf ihn am Kopf.', 'A bullet hit him in the head.'),
 ('Sein rechtes Auge war blind, seine linke Körperhälfte gelähmt.', 'His right eye was blind, the left side of his body paralysed.'),
 ('Er flog trotzdem zurück, rund 1000 Kilometer über das Meer, 4 Stunden und 47 Minuten lang.', 'He still flew back, about 1,000 kilometres over the sea, for 4 hours and 47 minutes.'),
 ('In Rabaul erstattete er noch Meldung, dann brach er zusammen.', 'In Rabaul he still made his report, then he collapsed.'),
 ('In Japan wurde er operiert, doch auf dem rechten Auge sah er nie wieder richtig.', 'He was operated on in Japan, but he never saw properly with his right eye again.'),
 ('Im Juni 1944 flog er mit einem Auge wieder Einsätze.', 'In June 1944 he flew missions again with one eye.'),
 ('Über Iwo Jima hielt er 15 amerikanische Hellcats für japanische Maschinen und entkam ihnen trotzdem.', 'Over Iwo Jima he took 15 American Hellcats for Japanese aircraft and still escaped them.'),
 ('In seinen Memoiren ist von 64 Luftsiegen die Rede, in den japanischen Unterlagen sind rund 28 verzeichnet, viele davon geteilt.', 'His memoirs speak of 64 victories; Japanese records list about 28, many of them shared.'),
 ('Jahrzehnte nach dem Krieg traf er Harold Jones, einen der Heckschützen vom 7. August 1942, und gab ihm die Hand.', 'Decades after the war he met Harold Jones, one of the rear gunners of 7 August 1942, and shook his hand.'),
 ('Saburō Sakai starb im September 2000 im Alter von 84 Jahren.', 'Saburō Sakai died in September 2000 at the age of 84.'),
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
