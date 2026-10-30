# English subtitle track for the German Dönitz short, timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Die Briten nannten ihn den Wüstenfuchs,", "The British called him the Desert Fox,"),
 ("doch am Ende tötete ihn nicht der Feind, sondern sein eigenes Regime.", "but in the end it was not the enemy who killed him, it was his own regime."),
 ("Sein Name war Erwin Rommel.", "His name was Erwin Rommel."),
 ("Am 12. Februar 1941 landete er in Tripolis.", "On 12 February 1941 he landed in Tripoli."),
 ("Er sollte die Italiener in Libyen stützen und abwarten,", "He was meant to support the Italians in Libya and wait,"),
 ("doch Rommel griff an und trieb die Briten bis an die Grenze Ägyptens zurück.", "but Rommel attacked and drove the British back to the Egyptian border."),
 ("Er führte von vorne, oft aus einem kleinen Fieseler Storch.", "He led from the front, often from a small Fieseler Storch."),
 ("Nur Tobruk hielt stand, fast acht Monate lang.", "Only Tobruk held out, for almost eight months."),
 ("Seine Gegner sprachen so oft von ihm,", "His enemies talked about him so often"),
 ("dass der britische Oberbefehlshaber Claude Auchinleck seinen Kommandeuren schrieb,", "that the British commander-in-chief Claude Auchinleck wrote to his commanders"),
 ("man solle nicht mehr von Rommel reden, sondern nur noch von den Deutschen.", "to stop talking about Rommel and speak only of the Germans."),
 ("Im Juni 1942 fiel Tobruk, und Rommel wurde mit 50 Jahren Generalfeldmarschall.", "In June 1942 Tobruk fell, and at 50 Rommel became a field marshal."),
 ("Wenige Monate später scheiterte er bei El Alamein.", "A few months later he failed at El Alamein."),
 ("Hitler befahl Sieg oder Tod, Rommel zog sich trotzdem zurück.", "Hitler ordered victory or death, Rommel retreated anyway."),
 ("1944 ließ er am Atlantikwall Millionen Minen verlegen", "In 1944 he had millions of mines laid on the Atlantic Wall"),
 ("und Pfähle in die Strände rammen, die Rommelspargel.", "and stakes driven into the beaches, known as Rommel's asparagus."),
 ("Doch nach der Landung der Alliierten hielt er den Krieg für verloren und sagte das offen.", "But after the Allied landings he considered the war lost and said so openly."),
 ("Nach dem Attentat vom 20. Juli fiel sein Name in den Verhören der Verschwörer.", "After the assassination attempt of 20 July, his name came up in the interrogations of the conspirators."),
 ("Am 14. Oktober 1944 hielten zwei Generäle vor seinem Haus in Herrlingen.", "On 14 October 1944 two generals stopped outside his house in Herrlingen."),
 ("Sie stellten ihn vor die Wahl: Volksgerichtshof oder Gift.", "They gave him a choice: the People's Court or poison."),
 ("Rommel verabschiedete sich von seiner Frau und seinem Sohn und stieg in den Wagen.", "Rommel said goodbye to his wife and son and got into the car."),
 ("Wenig später war er tot.", "Shortly afterwards he was dead."),
 ("Offiziell starb er an seinen Verwundungen.", "Officially, he died of his wounds."),
 ("Hitler schickte einen Kranz,", "Hitler sent a wreath,"),
 ("und bei der Trauerfeier in Ulm sagte Generalfeldmarschall von Rundstedt: Sein Herz gehörte dem Führer.", "and at the funeral in Ulm Field Marshal von Rundstedt said: His heart belonged to the Führer."),
 ("Die Wahrheit erfuhr die Welt erst nach dem Krieg, von seinem Sohn Manfred.", "The world only learned the truth after the war, from his son Manfred."),
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
