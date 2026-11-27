# German and English SRT for the Bäke long film and the Shorts, timed by the word alignment (one cue per sentence, long ones split in two)
import sys, re, json
E = '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/baeke/'
U = '/home/user/Brnkry/chronik/baeke/untertitel/'
def words(d, off): return [(w, a + off, b + off) for w, a, b in json.load(open(E + d + '/words.json'))]
def sents(WD):
    out, cur = [], []
    for i, w in enumerate(WD):
        cur.append(w); prev = WD[i - 1][0].lower() if i else ''
        ordinal = re.fullmatch(r'([0-9]+|[IVX]+)\.', w[0]) and prev not in ('panzer-regiment',)
        if w[0][-1] in '.:?!' and not ordinal: out.append(cur); cur = []
    if cur: out.append(cur)
    return out
def ts(t): t = max(t, 0); ms = int(round(t * 1000)); return '%02d:%02d:%02d,%03d' % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)
def split2(s):
    if len(s) <= 84: return [s]
    w = s.split(); k = min(range(1, len(w)), key=lambda k: abs(len(' '.join(w[:k])) - len(s) / 2)); return [' '.join(w[:k]), ' '.join(w[k:])]
def build(WD, TX, out):
    S = sents(WD); assert len(S) == len(TX), (out, len(S), len(TX)); assert not any(re.search('[—–]', t) for t in TX); cues = []
    for i, (s, e) in enumerate(zip(S, TX)):
        a, b = s[0][1], s[-1][2]; nxt = S[i + 1][0][1] if i + 1 < len(S) else b + 1.5; b2 = min(b + 0.6, nxt - 0.05); p = split2(e)
        if len(p) == 1: cues.append((a, b2, e))
        else: m = a + (b - a) * len(p[0]) / len(e); cues += [(a, m, p[0]), (m, b2, p[1])]
    open(out, 'w').write('\n'.join(f'{k}\n{ts(a)} --> {ts(b)}\n{t}\n' for k, (a, b, t) in enumerate(cues, 1))); print(out, len(cues))
EN = [
"He treated teeth in Hagen.",
"A few years later he led one of the strongest armoured units on the Eastern Front.",
"His name was Franz Bäke.",
"He was a dentist, and he became one of the most highly decorated panzer commanders of the Wehrmacht.",
"Franz Bäke was born on 28 February 1898 in Schwarzenfels, a small village in Hesse.",
"In May 1915, at 17, he volunteered for the army.",
"He fought in the First World War and received the Iron Cross.",
"After the war he studied dentistry in Würzburg and earned his doctorate in 1923.",
"Then he opened his own practice in Hagen.",
"Doctor Bäke was a dentist, not an officer.",
"But in the 1930s Germany rearmed.",
"In 1937 Bäke trained as a reservist, and at the end of the year he became a reserve lieutenant.",
"In August 1939 he was called up.",
"He was 41 years old.",
"With what later became the 6th Panzer Division he went to Poland, and in 1940 to France.",
"He was wounded several times and came back every time.",
"In June 1941 the war against the Soviet Union began.",
"Bäke now served in Panzer Regiment 11.",
"In June 1942 he took over its 2nd Battalion, and soon after he became a reserve major.",
"In December 1942 his division rolled south to relieve the 6th Army, trapped at Stalingrad.",
"The relief attack came to within about 50 kilometres, then it stalled.",
"The 6th Army was not relieved.",
"Bäke received the Knight's Cross in January 1943.",
"In summer 1943 he fought at Kursk, in one of the largest tank battles in history.",
"On 1 August 1943 he was awarded the Oak Leaves to the Knight's Cross.",
"In September Hitler presented them to him at the Führer headquarters.",
"In November 1943 Bäke took over the whole of Panzer Regiment 11.",
"A dentist from Hagen now led a panzer regiment.",
"The situation in the south of the Eastern Front kept getting worse.",
"In early 1944 the Wehrmacht formed an unusual unit.",
"Around 34 Tiger and 46 Panther tanks, plus artillery and engineers, were brought together under a single command.",
"It was called Heavy Panzer Regiment Bäke.",
"Its first big battle took place at the end of January near Balabanovka.",
"According to German reports, the regiment destroyed more than 250 Soviet tanks there in a few days and lost only a few of its own.",
"Historians, however, often consider such figures too high.",
"Then came the Cherkassy pocket.",
"At Korsun, tens of thousands of German soldiers were encircled.",
"On 4 February 1944 Bäke's regiment attacked to free them.",
"It was winter, but suddenly a thaw set in.",
"The roads sank into mud.",
"Tanks got stuck, supplies could not get through, fuel and ammunition ran short.",
"The tanks came to within about 20 kilometres of the encircled troops.",
"They could go no further.",
"On 16 February the trapped troops broke out on their own, through snow, mud and enemy fire.",
"Many reached the German lines, thousands did not.",
"For this fighting Bäke received the Swords to the Knight's Cross on 21 February 1944, the 49th soldier of the Wehrmacht to do so.",
"He also wore the special badge for destroying tanks single-handed.",
"It was awarded for enemy tanks a soldier had destroyed alone in close combat, without a tank or anti-tank gun of his own.",
"In summer 1944 the front in the West collapsed.",
"Bäke, now a colonel, led Panzer Brigade 106 Feldherrnhalle.",
"On the night of 8 September 1944 it attacked the US 90th Infantry Division near Mairy in Lorraine.",
"The attack failed.",
"According to American figures, the brigade lost around 30 tanks, 60 half-tracks and almost 100 other vehicles.",
"In March 1945 he took over the 13th Panzer Division in Hungary, soon renamed Panzer Division Feldherrnhalle 2.",
"In April 1945 he became a major general, at 47.",
"On 8 May 1945 Franz Bäke was taken prisoner.",
"According to most sources it was American captivity, from which he was released in 1947.",
"And then he did something hardly any general did.",
"He went back to Hagen and worked as a dentist again.",
"The man who had led panzer regiments was treating teeth again.",
"Franz Bäke died in Bochum on 12 December 1978, after a car accident.",
"He was 80 years old.",
"A dentist who became one of the most highly decorated panzer commanders of the Wehrmacht.",
"And who after the war simply went back to where he had started:",
"his practice in Hagen."]
EN_S = [
"He was a dentist in Hagen, and he became one of the most highly decorated panzer commanders of the Wehrmacht.",
"His name was Franz Bäke.",
"In the First World War he fought as a young volunteer, then he studied dentistry and opened a practice.",
"In August 1939, at 41, he was called up.",
"With the 6th Panzer Division he fought in Poland, in France and on the Eastern Front, before Stalingrad and at Kursk.",
"By the end of 1943 the dentist was leading an entire panzer regiment.",
"In early 1944 the Wehrmacht formed a special unit for him:",
"around 34 Tigers and 46 Panthers under one command, Heavy Panzer Regiment Bäke.",
"In February 1944 it was to free the troops trapped in the Cherkassy pocket.",
"But a thaw turned the roads into mud, and the tanks got stuck about 20 kilometres short of the pocket.",
"Bäke received the Swords to the Knight's Cross, the 49th soldier of the Wehrmacht to do so.",
"In April 1945 he became a major general.",
"And after the war he did something hardly any general did.",
"He went back to Hagen and worked as a dentist again."]
if __name__ == '__main__':
    L, S = words('p1', 0.6), words('ks', 0.0)
    de = lambda WD: [' '.join(w[0] for w in s) for s in sents(WD)]
    build(L, de(L), U + 'captions.de.srt'); build(L, EN, U + 'captions.en_US.srt')
    build(S, de(S), U + 'short.de.srt'); build(S, EN_S, U + 'short.en_US.srt')
