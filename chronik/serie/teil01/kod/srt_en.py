# English subtitle track for Teil 1 (German voice), timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Zwanzig Jahre vor dem Zweiten Weltkrieg", "Twenty years before the Second World War,"),
 ("durfte Deutschland keinen einzigen Panzer besitzen.", "Germany was not allowed a single tank."),
 ("Der Vertrag von Versailles hatte das Heer auf hunderttausend Mann begrenzt,", "The Treaty of Versailles had limited the army to 100,000 men,"),
 ("Luftwaffe und U-Boote waren verboten,", "an air force and U-boats were banned,"),
 ("und das Land sollte Milliarden an Reparationen zahlen.", "and the country was to pay billions in reparations."),
 ("Dann brach das Geld zusammen.", "Then the money collapsed."),
 ("1923 kostete ein Brot in Berlin Hunderte Milliarden Mark,", "In 1923 a loaf of bread in Berlin cost hundreds of billions of marks,"),
 ("die Ersparnisse eines ganzen Lebens waren über Nacht wertlos.", "and a lifetime of savings was worthless overnight."),
 ("Kaum hatte sich das Land erholt, kam die Weltwirtschaftskrise,", "The country had barely recovered when the Great Depression struck,"),
 ("und 1932 waren sechs Millionen Deutsche arbeitslos.", "and by 1932 six million Germans were out of work."),
 ("In dieser Lage wurde Adolf Hitler am 30. Januar 1933 Reichskanzler.", "In this situation, on 30 January 1933, Adolf Hitler became Chancellor."),
 ("Innerhalb weniger Monate schaltete seine Regierung", "Within a few months his government"),
 ("Parteien, Gewerkschaften und freie Presse aus.", "eliminated the parties, the trade unions and the free press."),
 ("Gleichzeitig rüstete Deutschland auf, zuerst heimlich, dann offen.", "At the same time Germany rearmed, first in secret, then openly."),
 ("1935 kehrte die Wehrpflicht zurück,", "In 1935 conscription returned,"),
 ("und die Luftwaffe wurde offiziell vorgestellt.", "and the Luftwaffe was officially unveiled."),
 ("1936 marschierten Soldaten in das entmilitarisierte Rheinland,", "In 1936 soldiers marched into the demilitarised Rhineland,"),
 ("und niemand hielt sie auf.", "and nobody stopped them."),
 ("1938 folgten Österreich und das Sudetenland,", "In 1938 came Austria and the Sudetenland,"),
 ("im März 1939 die übrige Tschechoslowakei.", "in March 1939 the rest of Czechoslovakia."),
 ("Jedes Mal hofften Großbritannien und Frankreich,", "Each time, Britain and France hoped"),
 ("es sei der letzte Schritt.", "it would be the last step."),
 ("Am 1. September 1939 um 4 Uhr 45", "On 1 September 1939 at 4:45 a.m."),
 ("eröffnete das Linienschiff Schleswig-Holstein", "the battleship Schleswig-Holstein"),
 ("das Feuer auf die Westerplatte bei Danzig.", "opened fire on the Westerplatte near Danzig."),
 ("Zwei Tage später erklärten Großbritannien und Frankreich Deutschland den Krieg.", "Two days later Britain and France declared war on Germany."),
 ("Er sollte sechs Jahre dauern", "It would last six years"),
 ("und mehr als sechzig Millionen Menschen das Leben kosten.", "and cost more than sixty million people their lives."),
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
