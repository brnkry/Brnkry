# English subtitle track for the German Wunderlich short, timed to the German words (words.json, voice text) plus the 0.4 s voice delay
import json, sys
W_ = json.load(open(sys.argv[1])); OFF = 0.4
CUES = [
 ('Das Grab eines Piloten, der 73 Jahre lang in seinem Flugzeug lag.', 'The grave of a pilot who lay in his plane for 73 years.'),
 ('Im März 2017 testete der vierzehnjährige Daniel Rom Kristiansen mit seinem Vater | auf dem Feld der Familie bei Birkelse in Nordjütland einen Metalldetektor, für ein Schulprojekt.', 'In March 2017, 14-year-old Daniel Rom Kristiansen and his father | were testing a metal detector on the family field near Birkelse in North Jutland, for a school project.'),
 ('Das Gerät schlug immer wieder aus.', 'The detector kept going off.'),
 ('Mit einem Bagger gruben sie nach und stießen in sieben bis acht Metern Tiefe | auf die Trümmer einer Messerschmitt Bf hundertneun, | des wichtigsten Jagdflugzeugs der Luftwaffe, von dem über dreiunddreißigtausend Stück gebaut wurden.', 'They dug with an excavator and, seven to eight metres down, | hit the wreckage of a Messerschmitt Bf 109, | the Luftwaffe\'s most important fighter, of which more than 33,000 were built.'),
 ('Doch im Wrack lag noch mehr:', 'But there was more in the wreck:'),
 ('die sterblichen Überreste des Piloten.', 'the remains of the pilot.'),
 ('Neben seinen Knochen fanden die Archäologen des Historischen Museums Nordjütland persönliche Gegenstände, | eine Brieftasche, Ausweispapiere und Reste seiner Uniform.', 'Next to his bones, archaeologists from the North Jutland Historical Museum found personal belongings, | a wallet, identity papers and remnants of his uniform.'),
 ('Mit ihrer Hilfe und mit deutschen Wehrmachtsunterlagen wurde der Pilot identifiziert:', 'With their help and German military records, the pilot was identified:'),
 ('Hans Wunderlich, geboren am 22. Juli 1925.', 'Hans Wunderlich, born on 22 July 1925.'),
 ('Er war 19 Jahre alt, als seine Maschine am 10. Oktober 1944 bei Aalborg abstürzte.', 'He was 19 when his plane crashed near Aalborg on 10 October 1944.'),
 ('Ob ein Luftkampf oder ein technischer Defekt die Ursache war, ist bis heute nicht geklärt.', 'Whether air combat or a technical fault caused it remains unclear to this day.'),
 ('Der feuchte, sauerstoffarme Boden hatte Wrack und Überreste über sieben Jahrzehnte bewahrt.', 'The damp, oxygen-poor soil had preserved the wreck and the remains for more than seven decades.'),
 ('73 Jahre nach seinem Tod wurde Hans Wunderlich schließlich beigesetzt.', '73 years after his death, Hans Wunderlich was finally laid to rest.'),
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
