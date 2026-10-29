# English subtitle track for the German Dönitz short, timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Im April 1943 ließ eine deutsche Besatzung in Tunesien einen fast unversehrten Tiger zurück,", "In April 1943 a German crew in Tunisia left behind an almost undamaged Tiger,"),
 ("und genau dieser Panzer fährt bis heute.", "and this very tank still runs today."),
 ("Sein Name ist Tiger 131, nach der Turmnummer:", "Its name is Tiger 131, after the turret number:"),
 ("erste Kompanie, dritter Zug, erster Panzer.", "first company, third platoon, first tank."),
 ("Er gehörte zur schweren Panzerabteilung 504", "It belonged to Heavy Panzer Battalion 504"),
 ("und kämpfte in den Hügeln bei Medjez el Bab gegen britische Churchill-Panzer.", "and fought in the hills near Medjez el Bab against British Churchill tanks."),
 ("Ein Treffer verklemmte den Drehkranz seines Turms,", "One hit jammed its turret ring,"),
 ("ein zweiter beschädigte die Höhenrichtung der Kanone.", "a second damaged the gun's elevation."),
 ("Die Besatzung stieg aus und gab den Panzer auf.", "The crew climbed out and abandoned the tank."),
 ("Für die Briten war das ein Glücksfall,", "For the British it was a stroke of luck,"),
 ("denn einen Tiger hatten sie bis dahin nie aus der Nähe untersuchen können.", "because until then they had never been able to study a Tiger up close."),
 ("Mit Luken und Teilen aus zerstörten Tigern setzten sie ihn wieder instand", "With hatches and parts from destroyed Tigers they repaired it"),
 ("und stellten ihn in Tunis aus, wo ihn auch König Georg der Sechste besichtigte.", "and put it on display in Tunis, where King George VI also inspected it."),
 ("Im Oktober 1943 kam er nach England.", "In October 1943 it came to England."),
 ("Die britische Schule für Panzertechnik vermaß seine Panzerung, prüfte Motor und Kanone", "The British School of Tank Technology measured its armour, tested engine and gun"),
 ("und schrieb lange Berichte über jede Schwäche.", "and wrote long reports on every weakness."),
 ("1951 übernahm ihn das Panzermuseum in Bovington.", "In 1951 the Tank Museum at Bovington took it over."),
 ("Ab 1990 wurde er zusammen mit Werkstätten der Armee fast vollständig zerlegt und restauriert.", "From 1990, together with army workshops, it was almost completely dismantled and restored."),
 ("Als Antrieb diente ein Maybach-Motor aus dem Königstiger des Museums,", "It was powered by a Maybach engine from the museum's King Tiger,"),
 ("und seit 2003 fährt Tiger 131 wieder aus eigener Kraft.", "and since 2003 Tiger 131 has been running under its own power again."),
 ("Bei einer zweiten Überholung bauten Techniker viele Teile wieder nach den Originalplänen aus dem Krieg.", "In a second overhaul, technicians rebuilt many parts to the original wartime plans."),
 ("2014 rollte er sogar im Kinofilm Fury vor die Kamera.", "In 2014 it even rolled in front of the camera in the film Fury."),
 ("Heute ist Tiger 131 der einzige fahrbereite Tiger I der Welt.", "Today Tiger 131 is the only running Tiger I in the world."),
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
