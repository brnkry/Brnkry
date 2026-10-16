import sys, json, re, numpy as np
OUTP=sys.argv[4]; d=json.load(open(sys.argv[2])); nuc=np.load(sys.argv[3])
sys.argv=[sys.argv[0],sys.argv[1],'/dev/null']
exec(open(sys.argv[1]+'/dp.py').read().split('P=[')[0])  # get syl, TEXT
cuts=d['cuts']; segs=d['segs']
# override: split chunk 3/4
b2=cuts[2][1]; cuts[2]=[cuts[2][0],b2-3]; cuts[3]=[b2-3,b2]; cuts[4]=[b2,cuts[4][1]]
ss=segs
out=[]
for (i,j),(a,b) in zip(cuts,ss):
    ws=TEXT[i:j]; sl=[syl(w) for w in ws]; n=sum(sl)
    nn=[t for t in nuc if a-0.02<=t<=b+0.02]
    if len(nn)>=2 and abs(len(nn)-n)<=max(3,0.35*n):
        g=np.interp(np.linspace(0,len(nn)-1,n),np.arange(len(nn)),nn)
        on=np.concatenate([[a],(g[:-1]+g[1:])/2])
    else: on=a+(b-a)*np.arange(n)/n
    k=0
    for w,s in zip(ws,sl):
        x=float(on[k]); k+=s; y=float(on[k]) if k<n else b
        out.append([w,round(x,2),round(y,2)])
    print(f"{a:6.2f}-{b:6.2f} | {' '.join(ws)}")
json.dump(out,open(OUTP,'w'),ensure_ascii=False)
print(len(out),'words')
