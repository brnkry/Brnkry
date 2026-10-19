# Soft skincare-style soundtrack: gentle pad + felt piano + delicate SFX, voice ducking, two-pass loudnorm happens in encode.
# usage: python3 ../audio9.py voice.mp3 events.json DUR out.wav
import sys, json, subprocess, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
SR=44100; rng=np.random.default_rng(11)
voice_f, ev_f, DUR, out_f = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
N=int(SR*DUR)
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],'bandpass',fs=SR,output='sos'),x)
def lp(x,f,o=2): return sosfilt(butter(o,f,'lowpass',fs=SR,output='sos'),x)
def hp(x,f,o=2): return sosfilt(butter(o,f,'highpass',fs=SR,output='sos'),x)
def tt(d): return np.arange(int(SR*d))/SR
def noise(d): return rng.standard_normal(int(SR*d))
def env(d,k): return np.exp(-tt(d)*k)
def norm(x,p=1.): return x/(np.max(np.abs(x))+1e-9)*p
def sine(f,d): return np.sin(2*np.pi*f*tt(d))
def bell(f,d=1.2,k=4): t=tt(d); return (np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2.0*f*t)+.12*np.sin(2*np.pi*3.01*f*t))*np.exp(-t*k)*np.minimum(1,t/.004)
def put(o,x,t0):
    s=int(t0*SR); e=min(len(o),s+len(x));
    if e>s: o[s:e]+=x[:e-s]
# ---- SFX ----
def whoosh(d): d=max(d,.3); t=tt(d); return norm(bp(noise(d),300,2500)*np.sin(np.pi*t/d)**1.5,.35)
def pop(d=0): t=tt(.12); return norm(np.sin(2*np.pi*np.cumsum(500+700*np.exp(-t*40))/SR)*np.exp(-t*35),.45)
def tap(d=0): t=tt(.08); return norm(np.sin(2*np.pi*320*t)*np.exp(-t*60)+.3*bp(noise(.08),1500,5000)*np.exp(-t*90),.4)
def tick(d=0): return norm(bell(1760,.5,9)+.6*bell(2637,.5,10),.35)
def chime(d=0):
    o=np.zeros(int(SR*1.6))
    for i,f in enumerate([1046.5,1318.5,1568]): put(o,bell(f,1.3,4.5)*(.9-.15*i),i*.07)
    return norm(o,.4)
def shimmer(d):
    d=max(d,.6); o=np.zeros(int(SR*(d+1)))
    for i in range(int(d*14)): put(o,bell(rng.choice([2093,2349,2637,3136,3520]),.6,8)*(.4+.6*rng.random()),i/14)
    return norm(o*np.minimum(1,np.arange(len(o))/(SR*.2)),.25)
def sparkle(d): return shimmer(d)
def lens(d=0): return norm(whoosh(.5)*.6+np.concatenate([np.zeros(int(SR*.35)),bell(1568,.8,6)])[:int(SR*.5)]*.6,.4)
def crack(d=0):
    o=np.zeros(int(SR*.7))
    for k in range(7): put(o,hp(noise(.03),1800)*env(.03,120)*(1-k*.1),k*.06+rng.random()*.02)
    return norm(o+.3*lp(noise(.7),400)*env(.7,8),.55)
def zoom(d): d=max(d,.4); t=tt(d); return norm(bp(noise(d),200,3000)*(t/d)**1.5*np.minimum(1,(d-t)/.05)+.3*np.sin(2*np.pi*np.cumsum(200+600*t/d)/SR)*(t/d),.35)
def swell(d): d=max(d,1); t=tt(d); return norm(sum(np.sin(2*np.pi*f*t) for f in [261.6,329.6,392,493.9])*np.sin(np.pi*t/d)**2,.25)
def squish(d): d=max(d,.4); t=tt(d); return norm(np.sin(2*np.pi*np.cumsum(300-150*t/d)/SR)*np.sin(np.pi*t/d)*.6+.3*lp(noise(d),900)*np.sin(np.pi*t/d),.3)
def flow(d): d=max(d,.6); t=tt(d); return norm(lp(noise(d),700)*(.6+.4*np.sin(2*np.pi*3*t))*np.sin(np.pi*t/d),.3)
def drip(d=0): t=tt(.16); return norm(np.sin(2*np.pi*np.cumsum(600+1600*t/.16)/SR)*np.exp(-t*30),.35)
def drips(d):
    o=np.zeros(int(SR*(d+.3)));
    for k in range(int(d*4)): put(o,drip()*(.6+.4*rng.random()),k/4+rng.random()*.08)
    return o
def bubbles(d):
    o=np.zeros(int(SR*(d+.3)))
    for k in range(int(d*9)): t=tt(.07); put(o,np.sin(2*np.pi*np.cumsum((800+900*rng.random())*(1+3*t))/SR)*np.exp(-t*50)*.5,k/9+rng.random()*.05)
    return norm(o,.3)
def slide(d): d=max(d,.5); t=tt(d); return norm(np.sin(2*np.pi*np.cumsum(500+500*(t/d))/SR)*np.sin(np.pi*t/d)*.4,.25)
def block(d=0): return norm(tap()*1.2,.4)
def thump(d=0): t=tt(.25); return norm(np.sin(2*np.pi*np.cumsum(140*np.exp(-t*8)+60)/SR)*np.exp(-t*18),.4)
def crumble(d):
    o=np.zeros(int(SR*(d+.2)))
    for k in range(int(d*30)): put(o,bp(noise(.02),800,4000)*env(.02,150)*rng.random(),rng.random()*d)
    return norm(o,.3)
def bloom(d): d=max(d,.4); t=tt(d); return norm((bell(784,d,3)+bell(1175,d,3.5))*np.minimum(1,t/.08),.35)
GEN=dict(whoosh=whoosh,pop=pop,tap=tap,tick=tick,chime=chime,shimmer=shimmer,sparkle=sparkle,lens=lens,crack=crack,zoom=zoom,swell=swell,squish=squish,flow=flow,
         drips=drips,bubbles=bubbles,slide=slide,block=block,thump=thump,crumble=crumble,bloom=bloom)
sfx=np.zeros(N+SR*3)
for t0,typ,d,v in json.load(open(ev_f)): put(sfx,GEN[typ](d)*v,t0)
sfx=sfx[:N]
# ---- music: 76 BPM, Fmaj9 - Am7 - Dm9 - Bbmaj7, soft pad + felt piano arpeggio ----
BPM=76; beat=60/BPM; bar=4*beat
def mtof(m): return 440*2**((m-69)/12)
CH=[[53,57,60,64,67],[57,60,64,67],[50,53,57,60,64],[46,50,53,57,62]]
pad=np.zeros(N); pno=np.zeros(N)
for b in range(int(DUR/bar)+1):
    t0=b*bar; ch=CH[b%4]; d=bar+.6
    seg=sum(np.sin(2*np.pi*mtof(m)*tt(d))+.3*np.sin(2*np.pi*mtof(m)*2.003*tt(d)) for m in ch)*np.minimum(1,tt(d)/.8)*np.minimum(1,(d-tt(d))/.6)
    put(pad,seg,t0)
    if b>=1:
        seq=[ch[0]+12,ch[2]+12,ch[1]+24,ch[3]+12,ch[2]+24,ch[1]+12,ch[3]+24,ch[2]+12]
        for k in range(8): put(pno,bell(mtof(seq[k]),1.4,3.2)*(.9 if k%4==0 else .6),t0+k*beat/2)
pad=lp(pad,1400); music=norm(pad,1)*.5+norm(pno,1)*.42
fo=np.ones(N); ts=np.arange(N)/SR; fo*=np.clip(ts/2,0,1)*np.clip((DUR-.3-ts)/2.5,0,1); music*=fo
# ---- voice + mix ----
raw=subprocess.run(['ffmpeg','-v','error','-i',voice_f,'-f','s16le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
v=np.zeros(N); x=np.frombuffer(raw,np.int16).astype(float)/32768; v[:min(N,len(x))]=x[:N]
def movavg(x,w): c=np.cumsum(np.insert(x,0,0.)); y=(c[w:]-c[:-w])/w; return np.concatenate([np.full(w//2,y[0]),y,np.full(len(x)-len(y)-w//2,y[-1])])
envv=np.sqrt(np.maximum(movavg(v**2,int(.08*SR)),0)); act=movavg(np.clip(envv/(np.percentile(envv[envv>.01],50)+1e-9),0,1),int(.3*SR))
rms=lambda x: np.sqrt(np.mean(x[np.abs(x)>1e-4]**2)); vr=rms(v)
music=music/rms(music)*vr*.26*(1-.5*np.clip(act,0,1)); sfx=sfx/(rms(sfx)+1e-9)*vr*.32
mix=v+music+sfx; mix=mix/np.max(np.abs(mix))*.93
wavfile.write(out_f,SR,(mix*32767).astype(np.int16)); print('ok',DUR)
