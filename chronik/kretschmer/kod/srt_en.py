# English subtitle track for the German Otto Kretschmer short, timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Ein Torpedo, ein Schiff.", "One torpedo, one ship."),
 ("Nach dieser Regel wurde Otto Kretschmer, gemessen an der versenkten Tonnage, zum erfolgreichsten U-Boot-Kommandanten des Zweiten Weltkriegs,", "By this rule Otto Kretschmer became, measured by tonnage sunk, the most successful U-boat commander of the Second World War,"),
 ("und doch war sein Krieg schon im März 1941 vorbei.", "and yet his war was already over in March 1941."),
 ("Mit U 99 griff er Geleitzüge vor allem nachts an, aufgetaucht und oft mitten zwischen den Kolonnen der Handelsschiffe.", "With U-99 he attacked convoys mostly at night, surfaced and often right between the columns of merchant ships."),
 ("Statt mehrere Torpedos auf einmal abzufeuern, kam er so nah heran, dass meist ein einziger Schuss genügte.", "Instead of firing several torpedoes at once, he got so close that a single shot was usually enough."),
 ("Weil er auf Feindfahrt kaum Funksprüche absetzte, nannte man ihn den schweigsamen Otto.", "Because he rarely sent radio messages on patrol, he was called Silent Otto."),
 ("In einer einzigen Nacht im Oktober 1940 versenkte er sieben Schiffe des Geleitzugs SC 7.", "In a single night in October 1940 he sank seven ships of convoy SC 7."),
 ("Gut zwei Wochen später traf es in einer Nacht die britischen Hilfskreuzer Laurentic und Patroclus.", "A little over two weeks later, in one night, the British armed merchant cruisers Laurentic and Patroclus were hit."),
 ("Insgesamt werden ihm 47 versenkte Schiffe mit rund 274.000 Bruttoregistertonnen zugeschrieben.", "In total he is credited with 47 ships sunk, about 274,000 gross register tons."),
 ("Auf diesen Schiffen kamen Hunderte Seeleute ums Leben.", "Hundreds of sailors died on these ships."),
 ("Im März 1941 griff er den Geleitzug HX 112 an.", "In March 1941 he attacked convoy HX 112."),
 ("In derselben Nacht verlor die Kriegsmarine auch Joachim Schepke und sein Boot U 100.", "On the same night the German navy also lost Joachim Schepke and his boat U-100."),
 ("Wasserbomben des britischen Zerstörers Walker zwangen U 99 an die Oberfläche.", "Depth charges from the British destroyer Walker forced U-99 to the surface."),
 ("Kretschmer ließ das Boot versenken.", "Kretschmer had the boat scuttled."),
 ("Drei Männer starben, 40 wurden gerettet und kamen in Gefangenschaft.", "Three men died; 40 were rescued and taken prisoner."),
 ("Der britische Kommandant Donald Macintyre behielt Kretschmers Fernglas als Andenken.", "The British commander Donald Macintyre kept Kretschmer's binoculars as a souvenir."),
 ("Kretschmer kam später in ein Lager in Kanada und plante dort die Flucht.", "Kretschmer was later sent to a camp in Canada, where he planned an escape."),
 ("Er und drei weitere Offiziere sollten durch einen Tunnel entkommen.", "He and three other officers were to escape through a tunnel."),
 ("Vor der Küste von New Brunswick sollte sie ein deutsches U-Boot abholen.", "A German U-boat was to pick them up off the coast of New Brunswick."),
 ("Doch die Kanadier lasen die verschlüsselten Briefe mit und warteten dort mit Kriegsschiffen.", "But the Canadians were reading the coded letters and waited there with warships."),
 ("Die Flucht scheiterte, und das U-Boot entkam nur knapp.", "The escape failed, and the U-boat barely got away."),
 ("Kretschmer blieb bis 1947 in Gefangenschaft.", "Kretschmer remained a prisoner until 1947."),
 ("Später diente er in der Bundesmarine und bei der NATO, zuletzt als Flottillenadmiral.", "He later served in the West German navy and with NATO, finally as a flotilla admiral."),
 ("Er starb 1998 nicht auf See, sondern nach einem Sturz bei einer Bootsfahrt auf der Donau, während er mit seiner Frau die goldene Hochzeit feierte.", "He died in 1998, not at sea, but after a fall during a boat trip on the Danube while celebrating his golden wedding anniversary with his wife."),
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
