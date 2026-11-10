# English subtitle track for the German Allerberger short, timed to the German words (words.json): one cue per German sentence
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [
 ('Er begann als Maschinengewehrschütze und wurde der zweiterfolgreichste Scharfschütze der Wehrmacht.', 'He began as a machine gunner and became the second most successful sniper of the Wehrmacht.'),
 ('Sein Name war Josef Allerberger, genannt Sepp.', 'His name was Josef Allerberger, known as Sepp.'),
 ('Er wurde 1924 in Österreich geboren, als Sohn eines Tischlers, und lernte selbst das Tischlerhandwerk.', 'He was born in Austria in 1924, the son of a carpenter, and trained as a carpenter himself.'),
 ('1942 wurde er eingezogen und als Maschinengewehrschütze ausgebildet.', 'In 1942 he was called up and trained as a machine gunner.'),
 ('Im Sommer 1942 kam er zum Gebirgsjäger-Regiment 144 der 3. Gebirgs-Division an die Ostfront.', 'In the summer of 1942 he joined Mountain Infantry Regiment 144 of the 3rd Mountain Division on the Eastern Front.'),
 ('Kurz darauf wurde er verwundet.', 'Shortly afterwards he was wounded.'),
 ('Während er sich erholte, nahm er ein erbeutetes sowjetisches Scharfschützengewehr in die Hand und erzielte damit 27 Abschüsse.', 'While he was recovering, he picked up a captured Soviet sniper rifle and scored 27 kills with it.'),
 ('Danach schickte man ihn auf die Scharfschützenschule auf der Seetaler Alpe in der Steiermark.', 'He was then sent to the sniper school on the Seetaler Alpe in Styria.'),
 ('Mit einem Karabiner 98k mit Zielfernrohr kehrte er zu seiner Division zurück.', 'He returned to his division with a Karabiner 98k with a telescopic sight.'),
 ('Bis Kriegsende kämpfte er in der Ukraine, in Rumänien, Ungarn und der Slowakei.', 'Until the end of the war he fought in Ukraine, Romania, Hungary and Slovakia.'),
 ('Ihm wurden 257 Abschüsse zugeschrieben.', 'He was credited with 257 kills.'),
 ('Nur Matthäus Hetzenauer aus demselben Regiment kam auf mehr.', 'Only Matthäus Hetzenauer from the same regiment had more.'),
 ('Nach eigenen Angaben erhielt er im April 1945 noch das Ritterkreuz, ein amtlicher Beleg dafür ist nicht erhalten.', "By his own account he received the Knight's Cross in April 1945, but no official record of it survives."),
 ('Im Mai 1945 legte er sein Gewehr ab und schlug sich zu Fuß nach Österreich durch.', 'In May 1945 he laid down his rifle and made his way back to Austria on foot.'),
 ('Danach arbeitete er wieder als Tischler.', 'After that he worked as a carpenter again.'),
 ('Über den Krieg sprach er erst Jahrzehnte später, mit dem Autor Albrecht Wacker.', 'He only spoke about the war decades later, with the author Albrecht Wacker.'),
 ('Josef Allerberger starb 2010 im Alter von 85 Jahren.', 'Josef Allerberger died in 2010 at the age of 85.'),
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
