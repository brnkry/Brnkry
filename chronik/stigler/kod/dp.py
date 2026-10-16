import re, sys, json, numpy as np
sys.path.insert(0, sys.argv[1]); from spoken import TEXT, SPOKEN
def syl(w):
    w=SPOKEN.get(w,w)
    if w=='B F': return 2
    if w.startswith('B '): return 1+syl(w[2:])
    return max(1,len(re.findall(r'(?:ei|ie|au|eu|äu|aa|ee|oo|[aeiouyäöü])',w.lower())))
P=[(5.08,5.61),(6.43,7.14),(9.44,9.64),(10.73,11.83),(23.30,23.81),(24.23,24.36),(24.99,25.74),(28.25,28.72),(31.80,32.07),(33.50,34.15),(36.65,36.98),(38.75,39.72),(46.08,46.64),(49.71,50.24),(53.96,54.48),(57.05,57.18),(58.21,58.43),(60.49,60.72),(62.06,63.03),(65.41,65.98),(67.15,67.55),(71.99,72.56),(74.37,74.58),(75.41,76.27),(78.61,79.10),(81.12,81.39),(83.16,83.86),(87.57,88.08),(92.11,92.67),(96.12,96.59),(97.81,97.98),(99.34,100.28),(104.62,105.02),(108.63,109.34),(110.64,111.12)]
segs=[]; s=0.09
for a,b in P: segs.append((s,a)); s=b
segs.append((s,112.48))
W=TEXT; sy=[syl(w) for w in W]; cs=np.concatenate([[0],np.cumsum(sy)])
r=sum(b-a for a,b in segs)/cs[-1]
def bpen(i):  # boundary after word i-1
    w=W[i-1]
    if w[-1] in '.!?“': return 0
    if w[-1]==',': return 0.3
    return 2.5
N=len(W); M=len(segs); INF=1e9
D=np.full((M+1,N+1),INF); B=np.zeros((M+1,N+1),int); D[0,0]=0
for m in range(1,M+1):
    a,b=segs[m-1]; d=b-a
    for j in range(1,N+1):
        for i in range(max(0,j-40),j):
            if D[m-1,i]>=INF: continue
            n=cs[j]-cs[i]; c=(d-n*r)**2/max(d,0.5)+(bpen(j) if j<N else 0)
            if D[m-1,i]+c<D[m,j]: D[m,j]=D[m-1,i]+c; B[m,j]=i
j=N; cuts=[]
for m in range(M,0,-1): i=B[m,j]; cuts.append((i,j)); j=i
cuts=cuts[::-1]
for (i,j),(a,b) in zip(cuts,segs):
    print(f"{a:6.2f}-{b:6.2f} {b-a:5.2f}s syl{cs[j]-cs[i]:3d} exp{(cs[j]-cs[i])*r:5.2f} | {' '.join(W[i:j])}")
json.dump({'cuts':[list(map(int,c)) for c in cuts],'segs':segs},open(sys.argv[2],'w'))
