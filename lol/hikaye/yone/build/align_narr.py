import sys, json; sys.path.insert(0,'/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad')
from align import align; from rows import rows
T=open('../anlatim.txt').read().strip(); R=rows(T)
W=align('../ses/anlatim.mp3',0,332.6,T)
assert len(W)==len(T.split())
out=[];i=0
for r,t in R:
    n=len(t.split()); ws=W[i:i+n]; i+=n
    out.append({'row':r,'text':t,'start':ws[0][1],'end':ws[-1][2],'words':[list(w) for w in ws]})
json.dump(out,open('narr.json','w'),ensure_ascii=False,indent=0)
for o in out: print(o['row'],o['start'],o['end'],o['text'][:40])
