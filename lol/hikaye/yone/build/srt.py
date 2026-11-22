import json,re,sys
P=json.load(open('/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad/yone/out/plan.json'))
NARR={p['row']:p for p in json.load(open('narr.json'))}; REPW=json.load(open('rep_words.json'))
words=[]
for r,at in P['narr']:
    p=NARR[r]
    for w,a,b in p['words']: words.append([w,at+a-p['start'],at+b-p['start'],'n'])
qkeys=[l.split("'")[3] for l in open('build.py').read().split('\n') if l.strip().startswith("('Q',")]
for (a_s,a_e,at),k in zip(P['reps'],qkeys):
    for w,a,b in REPW[k]: words.append([w,at+a-a_s,at+b-a_s,'y'])
words.sort(key=lambda x:x[1])
fix={'Azakana':'azakana','bırakmıyor':'bırakmıyor,','ağbisini':'abisini',"İyonya'ya":"Ionia'ya",'rüzgarın':'rüzgârın','Kardeşim':'Kardeşim...','Riven.':'Riven.'}
for w in words: w[0]=fix.get(w[0],w[0])
cues=[];cur=[]
def flush():
    if cur: cues.append(cur[:]); cur.clear()
for w in words:
    gap = 1.3 if w[3] == 'y' else 0.6
    if cur and (w[3]!=cur[-1][3] or w[1]-cur[-1][2]>gap): flush()
    if cur and len(' '.join(x[0] for x in cur+[w]))>98:
        k = max([i for i, x in enumerate(cur) if x[0].endswith(',') and i >= 2] or [len(cur) - 1])
        rest = cur[k + 1:]; del cur[k + 1:]; flush(); cur.extend(rest)
    cur.append(w)
    if re.search(r'[.?!:]$',w[0]) and len(' '.join(x[0] for x in cur))>25: flush()
flush()
def ts(x):
    ms=int(round(x*1000)); return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
C=[]
for i,c in enumerate(cues):
    st=max(0,c[0][1]-0.05); en=c[-1][2]+0.35
    if i+1<len(cues): en=min(en,cues[i+1][0][1]-0.08)
    C.append((ts(st),ts(en),' '.join(x[0] for x in c),c[0][3]))
json.dump(C,open('cues.json','w'),ensure_ascii=False,indent=0)
print(len(C))
for i,c in enumerate(C): print(i,c[3],c[2])
