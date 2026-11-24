# English subtitle track for the German Lüth short, timed to the German words (words.json) plus the 0.3 s voice delay.
# A long sentence is cut into two cues at a German word boundary (the '|' in the German line).
import json, sys
W_ = json.load(open(sys.argv[1])); OFF = 0.3
CUES = [
 ('Warum erschoss einer seiner eigenen Männer | einen der höchstdekorierten U-Boot-Kommandanten des Zweiten Weltkriegs?', 'Why did one of his own men shoot | one of the most decorated U-boat commanders of the Second World War?'),
 ('In den frühen Morgenstunden des 14. Mai 1945, Deutschland hatte bereits kapituliert, | starb ein Kapitän zur See durch die Kugel eines 18-jährigen deutschen Matrosen.', 'In the early hours of 14 May 1945, after Germany had already surrendered, | a naval captain was killed by the bullet of an 18-year-old German sailor.'),
 ('Der Offizier war Wolfgang Lüth, ein U-Boot-Ass, das vier Jahre Seekrieg überlebt hatte.', 'The officer was Wolfgang Lüth, a U-boat ace who had survived four years of war at sea.'),
 ('Geboren 1913 in Riga, damals Teil des Russischen Kaiserreichs, | trat er im April 1933 in die Reichsmarine ein.', 'Born in 1913 in Riga, then part of the Russian Empire, | he joined the Reichsmarine in April 1933.'),
 ('Zwischen Ende 1939 und Anfang 1942 führte Lüth drei U-Boote.', 'Between late 1939 and early 1942, Lüth commanded three U-boats.'),
 ('Mit U 9 versenkte er das französische U-Boot Doris, das einzige Kriegsschiff seiner Laufbahn.', 'With U-9 he sank the French submarine Doris, the only warship of his career.'),
 ('Mit U 138 erhielt er im Oktober 1940 das Ritterkreuz.', 'With U-138 he received the Knight\'s Cross in October 1940.'),
 ('Und mit U 43 gehörte er Ende 1941 zu den aktiven Kommandanten mit den meisten versenkten Schiffen.', 'And with U-43, by the end of 1941, he was among the serving commanders with the most ships sunk.'),
 ('1942 übernahm er U 181 und erreichte damit den Höhepunkt seines Ruhms.', 'In 1942 he took over U-181, which brought him to the height of his fame.'),
 ('Auf der ersten Feindfahrt versenkte er zwölf Handelsschiffe und erhielt noch auf See das Eichenlaub.', 'On his first patrol he sank twelve merchant ships and received the Oak Leaves while still at sea.'),
 ('Seine zweite Feindfahrt dauerte über 200 Tage ohne einen einzigen Hafen, eine der längsten des ganzen Krieges.', 'His second patrol lasted more than 200 days without a single port call, one of the longest of the entire war.'),
 ('Im April 1943 bekam er die Schwerter | und im August, als erster Offizier der Kriegsmarine, die Brillanten.', 'In April 1943 he received the Swords, | and in August, as the first officer of the Kriegsmarine, the Diamonds.'),
 ('Im Oktober überreichte Hitler sie ihm persönlich.', 'In October, Hitler presented them to him in person.'),
 ('Doch es sollte seine letzte Fahrt sein.', 'But it would be his last patrol.'),
 ('Danach bildete er Offiziere aus.', 'After that, he trained officers.'),
 ('Im September 1944 wurde er Kommandeur der Marineschule Mürwik in Flensburg.', 'In September 1944 he became commandant of the Naval Academy at Mürwik in Flensburg.'),
 ('Genau dort richtete Dönitz acht Monate später als Hitlers Nachfolger die letzte Reichsregierung ein.', 'It was there, eight months later, that Dönitz, as Hitler\'s successor, set up the last government of the Reich.'),
 ('Nach der Kapitulation erlaubten die Briten Lüth, die Schule weiter von bewaffneten Posten bewachen zu lassen.', 'After the surrender, the British allowed Lüth to keep armed sentries guarding the academy.'),
 ('Er selbst hatte befohlen, auf jeden zu schießen, der die Parole nicht nannte.', 'He himself had ordered them to shoot anyone who did not give the password.'),
 ('In der Nacht zum 14. Mai ging Lüth zu seiner Unterkunft.', 'On the night of 14 May, Lüth was walking to his quarters.'),
 ('Der Posten, Matrosengefreiter Mathias Gottlob, sah eine Gestalt in der Dunkelheit, erkannte sie aber nicht.', 'The sentry, Able Seaman Mathias Gottlob, saw a figure in the darkness but did not recognise it.'),
 ('Laut Aussage der Posten blieb Lüth beim ersten Halt stehen, antwortete aber auf keinen der drei Anrufe.', 'According to the sentries, Lüth stopped at the first call to halt, but answered none of the three challenges.'),
 ('Gottlob gab einen einzigen Schuss ab.', 'Gottlob fired a single shot.'),
 ('Er habe in die Luft schießen wollen, sagte er später.', 'He later said he had meant to fire into the air.'),
 ('Doch die Kugel traf Lüth in die Stirn, er war sofort tot.', 'But the bullet struck Lüth in the forehead, killing him instantly.'),
 ('Sein Biograf Jordan Vause hält es für wahrscheinlich, dass Lüth sehr wohl antwortete | und Wind, Regen oder Nervosität den Posten nichts hören ließen.', 'His biographer Jordan Vause thinks it likely that Lüth did answer, | and that wind, rain or nerves kept the sentry from hearing him.'),
 ('Wie auch immer es war:', 'Whatever the truth:'),
 ('Vier Jahre Seekrieg hatte er überlebt, | nur um nach der Kapitulation durch einen Schuss zu sterben, den er selbst befohlen hatte.', 'he had survived four years of war at sea, | only to die after the surrender from a shot he himself had ordered.'),
]
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return ('%02d:%02d:%06.3f' % (h, m, s)).replace('.', ',')
i = 0; out = []
for de, en in CUES:
    for dp, ep in zip(de.split(' | '), en.split(' | ')):
        n = len(dp.split()); ws = W_[i:i + n]; assert [w[0] for w in ws] == dp.split(), (dp, [w[0] for w in ws]); i += n
        a = ws[0][1] + OFF; b = ws[-1][2] + OFF + 0.25
        if i < len(W_): b = min(b, W_[i][1] + OFF - 0.02)
        out.append((a, b, ep))
assert i == len(W_)
open(sys.argv[2], 'w').write('\n'.join('%d\n%s --> %s\n%s\n' % (k + 1, ts(a), ts(b), t) for k, (a, b, t) in enumerate(out)))
print(len(out), 'cues')
