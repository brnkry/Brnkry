# English subtitle track (.srt) for the German Manstein short, timed to the voice (words.json = timeline of the final video)
import json, re, textwrap
B = '../'
W = json.load(open(B + 'words.json')); T = open(B + 'code/script.txt').read().strip()
SENT = re.split(r'(?<=[^\d][.!?])\s+', T)
EN = {0: "His own superiors did not want his plan.", 1: "It led to victory over France in six weeks.",
      2: "Erich von Manstein was born in Berlin in 1887 as Fritz Erich von Lewinski.", 3: "He grew up with his uncle and from then on bore his name.",
      4: "In the First World War he was badly wounded.",
      5: ["In 1939 he proposed sending the tanks through the Ardennes,", "a forest region the French thought tanks could barely cross."],
      6: "The army command set the plan aside and sent him off to command a corps.", 7: "But the plan still made its way to the top.",
      8: "In May 1940 the tanks pushed through the Ardennes all the way to the Channel.", 9: "In 1941 Manstein took over the 11th Army in Crimea.",
      10: "On November 20 he signed an order.", 11: "In it he demanded that his soldiers understand harsh measures against Jews.",
      12: "In his area of command, Einsatzgruppe D murdered tens of thousands of people.", 13: "In July 1942 Sevastopol fell, and Manstein became a field marshal.",
      14: "In December he was to relieve the encircled 6th Army at Stalingrad.", 15: "His troops got to within about 50 kilometers.",
      16: "Then the attack was called off.", 17: "In March 1944 he was dismissed.", 18: "In 1949 he stood before a British military court in Hamburg.",
      19: ["He was found guilty on nine of seventeen counts,", "partly because he had not protected civilians."],
      20: "The verdict: 18 years in prison.", 21: "By 1953 he was free again.", 22: "Two years later his book appeared: Lost Victories.",
      23: "In it, the blame for the defeats lay mostly with others.", 24: "The crimes in his area of command barely appeared.",
      25: "For decades he was seen as the clean strategist.", 26: "Historians see it differently today.",
      27: "Did you know this story?", 28: "Tell us in the comments!"}
SPLIT = {5: 'schicken,', 19: 'gesprochen,'}   # German word after which the second English line starts
cues = []; i = 0
for k, s in enumerate(SENT):
    ws = W[i:i + len(s.split())]; i += len(s.split())
    if k in SPLIT:
        j = [w[0] for w in ws].index(SPLIT[k]) + 1
        cues += [(ws[0][1], ws[j - 1][2], EN[k][0]), (ws[j][1], ws[-1][2], EN[k][1])]
    else: cues.append((ws[0][1], ws[-1][2], EN[k]))
assert i == len(W) and len(EN) == len(SENT)
def ts(x): h, r = divmod(int(round(x * 1000)), 3600000); m, r = divmod(r, 60000); s_, ms = divmod(r, 1000); return f'{h:02d}:{m:02d}:{s_:02d},{ms:03d}'
out = []
for n, (a, b, txt) in enumerate(cues):
    nxt = cues[n + 1][0] if n + 1 < len(cues) else b + 1.0
    b = min(max(b + 0.35, a + 1.2), nxt - 0.04)
    if len(txt) <= 42: lines = [txt]
    else:   # two balanced lines, break at the space nearest the middle
        sp = [m.start() for m in re.finditer(' ', txt)]; c = min(sp, key=lambda x: abs(x - len(txt) / 2)); lines = [txt[:c], txt[c + 1:]]
        assert max(map(len, lines)) <= 46, txt
    out.append(f'{n + 1}\n{ts(a)} --> {ts(b)}\n' + '\n'.join(lines) + '\n')
open(B + 'captions.en_US.srt', 'w', encoding='utf-8').write('\n'.join(out)); print(len(cues), 'cues')
