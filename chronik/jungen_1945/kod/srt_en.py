# English subtitle track for the German "Jungen 1945" short, one cue per German sentence, timed to words.json
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [("Amerikanische Soldaten suchten im Frühjahr 1945 auf diesem Feld nach dem Feind und fanden einen Jungen.", "In the spring of 1945 American soldiers searched this field for the enemy and found a boy."),
 ("Er hatte sich im Gras eingegraben, unter einer Zeltbahn, den Helm voller Halme.", "He had dug himself into the grass, under a groundsheet, his helmet full of straw."),
 ("Dann hob er die Hände.", "Then he raised his hands."),
 ("Viele Jungen seines Alters hatten zuvor als Flakhelfer an den Geschützen gestanden.", "Many boys his age had already served the guns as anti-aircraft auxiliaries."),
 ("In den letzten Kriegsmonaten zog der Volkssturm jeden zwischen 16 und 60 ein.", "In the last months of the war the Volkssturm called up everyone between 16 and 60."),
 ("Zu Tausenden gerieten sie in Gefangenschaft.", "They were taken prisoner by the thousands."),
 ("Für sie endete der Krieg mit erhobenen Händen.", "For them the war ended with their hands raised.")]
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return ('%02d:%02d:%06.3f' % (h, m, s)).replace('.', ',')
i = 0; out = []
for k, (de, en) in enumerate(CUES):
    n = len(de.split()); ws = W_[i:i + n]; assert [w[0] for w in ws] == de.split(), (de, [w[0] for w in ws]); i += n
    a = ws[0][1]; b = ws[-1][2] + 0.2
    if i < len(W_): b = min(b, W_[i][1] - 0.02)
    out.append('%d\n%s --> %s\n%s\n' % (k + 1, ts(a), ts(b), en))
assert i == len(W_)
open(B + 'untertitel/captions.en_US.srt', 'w').write('\n'.join(out)); print(len(out), 'cues')
