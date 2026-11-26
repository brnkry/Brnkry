# English SRT for the long Ehrler film: one English sentence per German sentence, timed by the word alignment,
# long sentences split into two cues; the radio message (twice) as its own cues.
import sys, re
sys.path.insert(0, '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/ehrler/kod')
import ee
EN = [
"That is said to have been Heinrich Ehrler's last radio message, in April 1945, in the sky over Stendal.",
"A comrade claimed to have heard it over the loudspeaker in the command post.",
"Whether those were really the words, nobody knows today.",
"Only this is certain:",
"A few weeks before the end of the war, one of the Luftwaffe's most successful fighter pilots died.",
"And just five months earlier he had been blamed for one of the German navy's greatest disasters.",
"This is his story.",
"Heinrich Ehrler was born on 14 September 1917 in Oberbalbach, a small village in northern Baden.",
"He grew up in a large working-class family and trained as a butcher.",
"In 1935, at 18, he joined the Wehrmacht, first the artillery, then the anti-aircraft branch.",
"At the end of 1936 he went to Spain with the Condor Legion, into the Spanish Civil War.",
"For almost a year he manned anti-aircraft guns there and only saw the planes from below.",
"But he wanted to fly himself.",
"In January 1940 he applied for a transfer to the fighter arm.",
"In February 1941 he joined Jagdgeschwader 77 in Stavanger as a young lieutenant, on Norway's west coast.",
"In May 1942 he was sent even further north, to the 6th Staffel of Jagdgeschwader 5 in Petsamo, in the far north of Finland.",
"It was called the Arctic Ocean Wing.",
"Up here the war was different.",
"In winter the sun did not rise for weeks, in summer it did not set for weeks.",
"Snowstorms, fog and icy cold shaped every mission.",
"Not far away lay Murmansk, the ice-free port through which the Allies shipped tanks, aircraft and ammunition to the Soviet Union.",
"In the sky the Messerschmitt Bf 109s met Soviet fighters, but also American P-40s and British Hurricanes that had reached the Red Army through that very port.",
"Ehrler reported victory after victory.",
"In summer 1942 he became squadron leader, and on 4 September he received the Knight's Cross.",
"On 8 June 1943 he reported his hundredth aerial victory.",
"He was only the fortieth Luftwaffe pilot to do so.",
"But he was not invulnerable either.",
"On 21 June 1943 he was shot down himself near Alakurtti.",
"He bailed out by parachute, behind Soviet lines.",
"That same day a seaplane brought him back.",
"In August 1943 he received the Oak Leaves to the Knight's Cross, for 112 victories.",
"That same year he took over an entire group of the wing.",
"In May 1944 he reported nine victories within 24 hours.",
"On 1 August 1944 he became commander of Jagdgeschwader 5, at the age of 26.",
"But in autumn everything in the far north collapsed.",
"In September Finland signed an armistice with the Soviet Union.",
"In October the Red Army overran Petsamo and Kirkenes.",
"The German troops withdrew to northern Norway, and the fighters with them.",
"There, off the coast near Tromsø, lay the largest battleship Germany had ever built:",
"the Tirpitz.",
"For years she had lain in Norway's fjords.",
"Her presence alone tied down British battleships in the Arctic.",
"In September 1944 a British Tallboy bomb hit her in Kåfjord.",
"A single hit wrecked her bow; she could no longer fight.",
"Grand Admiral Dönitz had her moved to Tromsø.",
"There she was to defend the coast as a floating battery.",
"In mid-October she anchored off the island of Håkøya.",
"It was believed the water there was shallow enough to keep her from sinking.",
"That was a mistake.",
"On 29 October British Lancaster bombers attacked again.",
"Just before the target clouds moved in, and no bomb hit directly.",
"Afterwards fighters of Jagdgeschwader 5 were moved to Bardufoss, not far from Tromsø.",
"But the unit had only just withdrawn from Kirkenes ahead of the Red Army.",
"Many pilots were young and inexperienced.",
"And apparently no one had properly told them that the Tirpitz lay close by.",
"Ehrler arrived in Bardufoss on 9 November.",
"He was actually on his way to Alta.",
"But he stayed to give the young pilots some quick training.",
"On the morning of 12 November 1944 the sky over Tromsø was clear.",
"More than thirty Lancasters of British Squadrons 617 and 9 had taken off in Scotland.",
"German observation posts saw the bombers coming.",
"But many believed they were flying on to the Soviet Union.",
"The reports reached the Tirpitz late and Bardufoss barely at all.",
"Only about a quarter of an hour before the attack were the fighters alerted.",
"A Ju 52 that was just landing blocked the runway.",
"Ehrler took off first.",
"In the air he noticed that his radio was not transmitting.",
"He could not reach anyone.",
"He did not find the bombers.",
"From a distance he only saw a cloud of smoke over the fjord.",
"Over Håkøya 29 Lancasters dropped their Tallboys, each weighing over five tons.",
"Two hit the ship directly.",
"The Tirpitz listed to port, further and further.",
"An ammunition magazine exploded, and an entire gun turret was torn from its mounting.",
"A few minutes after the hits the ship capsized.",
"Hundreds of sailors were trapped inside the hull.",
"Rescuers cut holes in the steel and pulled some out alive.",
"But for most, any help came too late.",
"Depending on the source, between about 900 and over 1,200 men died.",
"The British did not lose a single man.",
"Then the search for someone to blame began.",
"Many had made mistakes.",
"Reports between the navy and the Luftwaffe only went through detours, and the anchorage was not shallow enough.",
"But soon one man was at the centre:",
"the commander of Jagdgeschwader 5. In December 1944 Heinrich Ehrler stood before the Reich Military Court in Oslo.",
"The charge of cowardice before the enemy was dropped.",
"But the court accused him of leaving his command post to hunt for his two-hundredth victory himself.",
"He was sentenced to three years in prison for disobedience.",
"He lost his command and was demoted.",
"Many later saw him as a scapegoat.",
"Comrades spoke up for him, among them Walter Schuck, a pilot of his wing.",
"The sentence was suspended.",
"Ehrler was to prove himself at the front.",
"At the end of February 1945 his friend Theodor Weissenberger brought him to his unit.",
"Weissenberger commanded Jagdgeschwader 7, the world's first operational jet fighter unit.",
"Its aircraft was the Messerschmitt Me 262.",
"It flew over 850 kilometres per hour, faster than any Allied fighter.",
"But there were too few of them, too little fuel and too few trained pilots.",
"And on some days the Americans sent more than a thousand heavy bombers over Germany.",
"On 21 March 1945 Ehrler flew his first jet mission and reported a B-17.",
"A second followed the next day, two B-24s over Chemnitz on 23 March, and another B-17 near Dessau on 24 March.",
"In just four days he had scored five victories in the jet.",
"Then came April 1945.",
"The Red Army stood on the Oder, the Western Allies had crossed the Rhine.",
"On 4 April Ehrler took off with his wing's jets against a large American bomber formation.",
"What happened next is known only from reports, and they contradict each other.",
"According to the best-known version he shot down two bombers.",
"Then his ammunition was gone.",
"Walter Schuck later recalled hearing Ehrler's voice over the loudspeaker.",
"Theo was Theodor Weissenberger, his commander.",
"Others remembered different words.",
"Some sources even give 6 April as the day he died.",
"Whether Ehrler really rammed a bomber or was shot down by American escort fighters is still unclear today.",
"Only this is certain:",
"His Me 262 crashed near Stendal.",
"On 7 April a body was recovered and identified as Heinrich Ehrler.",
"On 10 April he was buried in Stendal.",
"Heinrich Ehrler was 27 years old.",
"He is credited with 208 aerial victories, almost all in the far north, eight of them in the jet.",
"Some historians believe the real number is lower, because his wing's records are incomplete.",
"And even his grave holds a mystery.",
"In 2018 researchers of missing soldiers found wreckage of his aircraft and human remains near Stendal.",
"According to them, Ehrler does not lie in the grave that bears his name.",
"A man who was blamed for the sinking of the Tirpitz.",
"A pilot whose last words became a legend that no one can prove to this day.",
"Five weeks after his death the war in Europe was over."]
RADIO = [(0.25, 3.45, 'Radio message: "Theo, Heinrich here. Have shot down two bombers."'), (3.5, 5.7, '"Out of ammunition. I\'m ramming now."'),
         (5.85, 8.7, '"Goodbye, see you in Valhalla."')]
def sents(WD):
    out, cur = [], []
    for w in WD:
        cur.append(w)
        if w[0][-1] in '.:?!' and not (w[0][:-1].isdigit() and int(w[0][:-1]) <= 31): out.append(cur); cur = []
    if cur: out.append(cur)
    return out
def ts(t): t = max(t, 0); return '%02d:%02d:%02d,%03d' % (t // 3600, t % 3600 // 60, int(t % 60), int(round((t % 1) * 1000)) % 1000)
def split2(s):
    if len(s) <= 84: return [s]
    words = s.split(); best = min(range(1, len(words)), key=lambda k: abs(len(' '.join(words[:k])) - len(s) / 2)); return [' '.join(words[:best]), ' '.join(words[best:])]
def build(WD, EN, radios, out):
    S = sents(WD); assert len(S) == len(EN), (len(S), len(EN)); cues = []
    for r0 in radios:
        for a, b, t in RADIO: cues.append((r0 + a, r0 + b, t))
    for i, (s, e) in enumerate(zip(S, EN)):
        a, b = s[0][1], s[-1][2]; nxt = S[i + 1][0][1] if i + 1 < len(S) else b + 1.5; b2 = min(b + 0.6, nxt - 0.05)
        parts = split2(e)
        if len(parts) == 1: cues.append((a, b2, e))
        else:
            m = a + (b - a) * len(parts[0]) / len(e); cues.append((a, m, parts[0])); cues.append((m, b2, parts[1]))
    cues.sort(); L = []
    for k, (a, b, t) in enumerate(cues, 1): L.append(f'{k}\n{ts(a)} --> {ts(b)}\n{t}\n')
    open(out, 'w').write('\n'.join(L)); print(out, len(cues))
if __name__ == '__main__':
    assert not any(re.search('[—–]', e) for e in EN)
    build(ee.WD, EN, [ee.R1, ee.R2], '/home/user/Brnkry/chronik/ehrler/untertitel/captions.en_US.srt')
