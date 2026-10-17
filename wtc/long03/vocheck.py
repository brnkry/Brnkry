import numpy as np,subprocess,json
from scipy.io import wavfile
sr,m=wavfile.read('master.wav');m=m.astype(float)/32768
raw=subprocess.run(['ffmpeg','-v','error','-i','voice.mp3','-f','s16le','-ac','1','-ar',str(sr),'-'],capture_output=True).stdout
v=np.frombuffer(raw,np.int16).astype(float)/32768;n=min(len(m),len(v))
E=json.load(open('events_scene.json'));out=[]
for s in np.arange(0,n/sr-1,0.5):
    a,b=int(s*sr),int((s+1)*sr);vv=v[a:b];mm=m[a:b]
    if np.sqrt(np.mean(vv**2))<0.02: continue
    gg=np.dot(mm,vv)/np.dot(vv,vv);res=mm-gg*vv
    r=20*np.log10(np.sqrt(np.mean((gg*vv)**2))/np.sqrt(np.mean(res**2)))
    if r<4: out.append((round(s,1),round(r,1),[e[1] for e in E if s-1.2<e[0]<s+1]))
for o in out: print(o)
