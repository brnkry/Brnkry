import json
S=json.load(open('vo_shift.json'))
def s(t): return round(t if t<S['A'] else (t+S['sh1'] if t<S['B'] else t+S['sh2']),3)
raw=dict(hook=0,vl1=None,why=13.5,passive=28.9,q=46.3,w=52.1,e=69.8,r=87.6,combo=102.9,c2=115.4,c3=124.8,match=137.5,runes=157.8,items=170.9,skills=182.1,summ=192.2,early=194.2,mid=220.9,late=226.6,outro=250.0,end=261.2)
T={k:(s(v) if v is not None else None) for k,v in raw.items()}
T['vl1']=S['v1'][0]; T['vl2']=S['v2'][0]; T['END']=round(S['len'],2)
W={}  # word-level extra cues (raw)
for k,v in dict(nerf=0.8,tekliyor=5.3,tekleyen=6.8,pro1=15.5,pro2=17.0,pro3=18.2,pro4=19.2,con1=20.9,con2=22.5,ninja=27.3,
  p1=31.7,p2=35.4,p3=41.3,q1=48.4,q2=50.0,w1=54.3,w2=56.7,w3=58.2,w4=61.2,w5=64.9,e1=71.5,e2=75.6,e3=79.0,e4=85.4,r1=90.8,r2=93.7,r3=99.2,
  c1s=[104.2,105.1,106.8,108.9,109.7,111.4,112.1,113.3,114.0],c2s=[115.4,116.8,117.7,119.3,120.7],c3s=[126.0,127.1,127.8,128.9,129.8,130.5,131.5,135.1],
  easy=[145.9,146.5,147.0],hard=[149.0,149.6,150.3],joke=151.0,
  ru=[159.2,160.4,161.4,162.4,164.3,164.9,165.8,167.7],it=[171.5,172.5,174.2,175.3,177.3,178.2],sk=[183.9,184.8,185.8,187.0,187.9,189.0,190.3],sm=[193.0,193.7],
  ea1=195.8,ea2=204.9,ea3=209.4,ea4=213.1,mi1=222.9,la1=228.5,la2=232.1,la3=241.3,mist=252.1,kontrol=254.9,gonder=257.9).items():
    W[k]=[s(x) for x in v] if isinstance(v,list) else s(v)
T.update(W)
open('timeline.js','w').write('const TL='+json.dumps(T)+';')
json.dump(T,open('cues.json','w'),indent=1)
print(T['END'],T['passive'],T['outro'],T['end'])
