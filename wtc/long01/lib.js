// Shared helpers for the long video parts (16:9). Part 01 keeps its own copy; parts 02+ use this file.
const NS="http://www.w3.org/2000/svg";const svg=document.getElementById('ill');
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));const P=(t,t0,d)=>cl((t-t0)/d);
const eo=x=>1-Math.pow(1-x,3);const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const back=x=>{const c1=1.7,c3=c1+1;return x<=0?0:1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const V=(t,a,b,fi=.3,fo=.25)=>Math.min(eo(P(t,a,fi)),1-P(t,b-fo,fo));
const lerp=(a,b,k)=>a+(b-a)*k;
function el(tag,attrs={},parent=svg){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);parent.appendChild(e);return e}
function g(parent=svg,attrs={}){return el('g',attrs,parent)}
function tr(e,x,y,s=1,r=0,o=1){e.setAttribute('transform',`translate(${x} ${y}) rotate(${r}) scale(${s})`);e.style.opacity=o}
function show(v,...els){els.forEach(e=>e.style.display=v>0?'':'none')}
function txt(parent,x,y,size,cls,s,anchor='middle'){const t=el('text',{x,y,'font-size':size,'text-anchor':anchor,class:cls},parent);t.textContent=s;return t}
const H=BRAND.hex;const AMBER='#FFB000',RED=H.brake,LIME=H.lime,OFF='#34343E',CHALK=H.chalk,ASPH=H.asphalt,GRAPH=H.graphite;
const LAMP_D='M-150 -40 h40 v-30 h70 v-25 h80 v25 h50 l30 30 h40 v-30 h30 v150 h-30 v-30 h-40 l-40 50 h-150 l-40 -40 h-40 v40 h-20 v-110 h20 v20 Z';
// BMW chime rule: a lamp is dark until the ding, lit c+0.03 .. c+1.0
const lampBlink=(t,cs)=>{for(const c of cs){const d=t-c;if(d>=0.03&&d<1.0)return 1}return 0};

// ---------- captions ----------
const cap=document.getElementById('cap');const groups=[];const WT={};
function buildCaptions(G){Object.keys(G).forEach(id=>{
  const div=document.createElement('div');div.className='grp';cap.appendChild(div);const words=[];let emph=false;
  G[id].forEach(([s,e,tx])=>{const toks=tx.split(' ');const W=toks.reduce((a,x)=>a+x.length+1,0);let acc=0;
    toks.forEach(tok=>{let st=tok.startsWith('*');if(st){emph=true;tok=tok.slice(1)}let en=tok.endsWith('*');if(en)tok=tok.slice(0,-1);
      const span=document.createElement('span');span.className='w'+(emph?' e':'');span.textContent=tok;div.appendChild(span);
      const ts=s+(e-s)*acc/W;acc+=tok.length+1;words.push({span,ts});const key=id+':'+tok.replace(/[.,:?]/g,'');if(!(key in WT))WT[key]=ts;if(en)emph=false})});
  groups.push({id,div,words,start:G[id][0][0]})});
  groups.forEach((gr,i)=>{gr.end=i<groups.length-1?groups[i+1].start:99})}
const W_=(id,w)=>{const k=id+':'+w;if(!(k in WT))throw new Error('no word '+k);return WT[k]};
function renderCaptions(t){groups.forEach(gr=>{const out=P(t,gr.end-.16,.16);const vis=t>=gr.start-.2&&t<gr.end+.04;gr.div.style.display=vis?'flex':'none';if(!vis)return;
  gr.words.forEach(({span,ts})=>{const k=eo(P(t,ts-.08,.3));span.style.opacity=k*(1-out);span.style.transform=`translateY(${(1-k)*22-out*18}px) scale(${.94+.06*k})`;span.style.filter=`blur(${(1-k)*10+out*6}px)`})})}
function fitCaptions(){groups.forEach(gr=>{const d=gr.div;d.style.display='flex';let fs=parseFloat(getComputedStyle(d).fontSize);
  [...d.children].forEach(x=>{x.style.transform='none';x.style.filter='none'});
  const box=()=>{const r=[...d.children].map(x=>x.getBoundingClientRect());return Math.max(...r.map(x=>x.bottom))-Math.min(...r.map(x=>x.top))};
  while(box()>140&&fs>40){fs-=2;d.style.fontSize=fs+'px'}d.style.display='none'})}

// ---------- building blocks ----------
function engineLamp(parent,fill=AMBER){const l=g(parent);const glow=el('circle',{r:240,fill,opacity:0,filter:'url(#soft)'},l);const p=el('path',{d:LAMP_D,fill},l);l.glow=glow;l.p=p;l.set=v=>{p.setAttribute('fill',v>0.5?fill:OFF);glow.setAttribute('opacity',.3*v)};return l}
function gauge(parent,r,label){const G0=g(parent);const rad=a=>a*Math.PI/180;const p=a=>[r*Math.cos(rad(a)),r*Math.sin(rad(a))];
  const [x0,y0]=p(135),[x1,y1]=p(405);el('path',{d:`M${x0} ${y0} A${r} ${r} 0 1 1 ${x1} ${y1}`,fill:'none','stroke-width':r*.12,class:'sLine','stroke-linecap':'round'},G0);
  const prog=el('path',{d:`M${x0} ${y0} A${r} ${r} 0 1 1 ${x1} ${y1}`,fill:'none','stroke-width':r*.12,class:'sAcc','stroke-linecap':'round',pathLength:1000},G0);
  for(let i=0;i<=8;i++){const a=135+i*33.75;const c=Math.cos(rad(a)),s=Math.sin(rad(a));el('line',{x1:c*r*.66,y1:s*r*.66,x2:c*r*.78,y2:s*r*.78,'stroke-width':r*.045,class:'sMut','stroke-linecap':'round'},G0)}
  const nd=g(G0);el('path',{d:`M${-r*.06} 0 L0 ${-r*.8} L${r*.06} 0 Z`,class:'ink'},nd);el('circle',{r:r*.13,class:'ink'},nd);el('circle',{r:r*.05,class:'bgf'},nd);
  if(label)txt(G0,0,r*.62,r*.17,'mic mut',label);
  G0.set=v=>{nd.setAttribute('transform',`rotate(${-135+270*v})`);prog.setAttribute('stroke-dasharray',`${v*1000} 1000`)};G0.set(0);return G0}
function makeCluster(parent){const c=g(parent);
  el('rect',{x:-390,y:-180,width:780,height:360,rx:150,class:'card'},c);el('rect',{x:-390,y:-180,width:780,height:360,rx:150,fill:'none','stroke-width':6,class:'sLine'},c);
  c.L=gauge(c,118,'MPH');c.L.setAttribute('transform','translate(-230 10)');c.R=gauge(c,118,'RPM ×1000');c.R.setAttribute('transform','translate(230 10)');
  const h=g(c,{transform:'translate(0 -10) scale(.44)'});c.lamp=engineLamp(h);return c}
function iconBattery(p){const g1=g(p);el('rect',{x:-40,y:-24,width:80,height:52,rx:6,fill:'currentColor'},g1);el('rect',{x:-30,y:-34,width:14,height:10,fill:'currentColor'},g1);el('rect',{x:16,y:-34,width:14,height:10,fill:'currentColor'},g1);el('rect',{x:-28,y:-2,width:18,height:6,fill:GRAPH},g1);el('rect',{x:10,y:-2,width:18,height:6,fill:GRAPH},g1);el('rect',{x:16,y:-8,width:6,height:18,fill:GRAPH},g1);return g1}
function iconOil(p){const g1=g(p);el('path',{d:'M-46 10 L-10 -20 L30 -20 L46 -36 L52 -30 L36 -10 L36 20 L-40 20 Z',fill:'currentColor'},g1);el('circle',{cx:56,cy:14,r:6,fill:'currentColor'},g1);return g1}
function iconABS(p){const g1=g(p);el('circle',{r:34,fill:'none','stroke-width':7,stroke:'currentColor'},g1);el('text',{x:0,y:9,'text-anchor':'middle','font-size':24,class:'bold',fill:'currentColor'},g1).textContent='ABS';return g1}
function iconBag(p){const g1=g(p);el('circle',{cx:-14,cy:-26,r:10,fill:'currentColor'},g1);el('path',{d:'M-26 -12 L-4 -12 L4 22 L-24 22 Z',fill:'currentColor'},g1);el('circle',{cx:22,cy:-2,r:20,fill:'currentColor'},g1);return g1}
function iconEngine(p){const l=g(p);el('path',{d:LAMP_D,fill:'currentColor',transform:'scale(.22)'},l);return l}

// ---------- studio + narrator ----------
const mouthAt=t=>{const M=window.MOUTH||[];const f=t*30;const i=Math.floor(f);const a=M[i]||0,b=M[i+1]||0;return lerp(a,b,f-i)};
const blinkAt=(t,per=3.3,off=0)=>{const p=((t+off)%per+per)%per;return p<.14?1-Math.sin(p/.14*Math.PI):1};
function makeStudio(){const s=g();el('rect',{x:0,y:0,width:1920,height:1080,fill:ASPH},s);el('circle',{cx:430,cy:520,r:620,fill:'url(#spot)'},s);
  [...Array(9)].forEach((_,i)=>el('circle',{cx:1290+(i%3-1)*520,cy:200+Math.floor(i/3)*300,r:3,fill:'#2A2A33'},s));
  const presG=g(s);const guy=makeGuy(presG);s.presG=presG;s.guy=guy;return s}
const REST={L:{x:-195,y:350,shape:'fist'},R:{x:195,y:350,shape:'fist'}};
function poser(POSE,KEYS){return t=>{let i=0;while(i<KEYS.length-1&&t>=KEYS[i+1][0])i++;const prev=POSE[KEYS[Math.max(0,i-1)][1]],cur=POSE[KEYS[i][1]];const k=eio(P(t,KEYS[i][0],.38));
  const mixH=(a,b)=>({x:lerp(a.x,b.x,k),y:lerp(a.y,b.y,k),shape:k<.5?a.shape:b.shape,rot:k>.5?b.rot:a.rot});
  return {L:mixH(prev.L,cur.L),R:mixH(prev.R,cur.R),name:KEYS[i][1]}}}

// ---------- captions timed from forced alignment (align.py) ----------
// G: {id:[[s,e,"text *emph*"],...]} (s/e ignored) ; A: [[word,start,end],...] in script order
const WL={};const WL_=(id,w)=>{const k=id+':'+w;if(!(k in WL))throw new Error('no word '+k);return WL[k]};
const DIG=['zero','one','two','three','four','five','six','seven','eight','nine'];
function spoken(tok){let t=tok.toLowerCase().replace(/\*/g,'').replace(/[.,:?!;"]/g,'');
  const map={'1996':['nineteen','ninety','six'],'16':['sixteen'],'obd-ii':['o','b','d','two'],'ecu':['e','c','u'],'$1,000':['thousand']};
  if(map[t])return map[t];let m=t.match(/^p(\d{4})$/);if(m)return ['p',...m[1].split('').map(d=>DIG[+d])];
  t=t.replace(/[^a-z']/g,'');return t?[t]:[]}
function buildCaptionsA(G,A){const AW=A.map(([w,s,e])=>[w.replace(/\(\d+\)$/,''),s,e]);let k=0,last=0;
  Object.keys(G).forEach(id=>{const div=document.createElement('div');div.className='grp';cap.appendChild(div);const words=[];let emph=false;
    G[id].forEach(seg=>{const tx=typeof seg==='string'?seg:seg[2];tx.split(' ').forEach(tok=>{let st=tok.startsWith('*');if(st){emph=true;tok=tok.slice(1)}let en=tok.endsWith('*');if(en)tok=tok.slice(0,-1);
      const sp=spoken(tok);let ts=last;
      if(sp.length){let j=k;while(j<Math.min(AW.length,k+4)&&AW[j][0]!==sp[0])j++;if(j<AW.length&&AW[j][0]===sp[0])k=j;else console.warn('align miss',id,tok,AW[k]&&AW[k][0]);
        if(k<AW.length){ts=AW[k][1];k+=sp.length;last=ts}}
      const span=document.createElement('span');span.className='w'+(emph?' e':'');span.textContent=tok;div.appendChild(span);words.push({span,ts});
      const key=id+':'+tok.replace(/[.,:?]/g,'');if(!(key in WT))WT[key]=ts;WL[key]=ts;if(en)emph=false})});
    groups.push({id,div,words,start:words[0].ts-.05})});
  groups.forEach((gr,i)=>{gr.end=i<groups.length-1?groups[i+1].start:99})}
