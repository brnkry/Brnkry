// Long 03 (winter warm-up): shared drawings, studio narrator, part registry.
const CX=1290;const flash=document.getElementById('flash');const black=document.getElementById('black');
const RENDER=[],EVF=[],KEYS=[[0,"rest"]],MOODS=[];const VO_END_=351.32;
const vis=(e,t,a,b,fi=.3,fo=.3)=>{const v=V(t,a,b,fi,fo);show(v,e);if(v>0)e.style.opacity=v;return v};
const pop=(t,a,d=.4)=>back(P(t,a,d));
const on=(t,a)=>t>a?1:0;
const ICE='#9ADFFF',COLD='#4FA3FF',WARM='#FF8A3D',SEPIA='#C9A57A',DIESEL='#2FB36B';

// ---------- studio + narrator (scarf for winter) ----------
const studio=makeStudio();const guy=studio.guy;
{const sc=g(guy.props);
 el('path',{d:'M-84 -22 Q0 26 84 -22 L92 22 Q0 74 -92 22 Z',fill:RED},sc);
 [-60,-30,0,30,60].forEach(x=>el('path',{d:`M${x-6} ${-4+Math.abs(x)*-.25} l0 ${36}`,stroke:'#C92E47','stroke-width':6,'stroke-linecap':'round'},sc));
 const tail=g(sc,{transform:'translate(44 30) rotate(-8)'});el('rect',{x:-22,y:0,width:46,height:170,rx:12,fill:RED},tail);
 [40,80,120].forEach(y=>el('rect',{x:-22,y,width:46,height:10,fill:CHALK,opacity:.85},tail));
 [-14,-2,10].forEach(x=>el('rect',{x,y:168,width:6,height:20,rx:3,fill:RED},tail))}
const bug=el('text',{x:1856,y:76,'text-anchor':'end',class:'bold','font-size':40,opacity:.6});[['WHAT THE ',CHALK],['CAR',LIME],['?',RED]].forEach(([s,c])=>{const sp=el('tspan',{fill:c},bug);sp.textContent=s});

// ---------- shared drawings ----------
function card(p,w,h,fill){const c=g(p);el('rect',{x:-w/2,y:-h/2,width:w,height:h,rx:28,fill:fill||GRAPH},c);return c}
function pill(p,text,fill,ink,w,fs=28){const c=g(p);const W=w||text.length*17+70;el('rect',{x:-W/2,y:-32,width:W,height:64,rx:32,fill},c);const t=txt(c,0,10,fs,'mic',text);t.setAttribute('fill',ink);c.t=t;return c}
const CHECK=(p,s=1)=>{const x=g(p,{transform:`scale(${s})`});el('circle',{r:30,fill:LIME},x);el('path',{d:'M-13 0 l9 10 l17 -20',fill:'none',stroke:ASPH,'stroke-width':7,'stroke-linecap':'round'},x);return x};
const XMARK=(p,s=1)=>{const x=g(p,{transform:`scale(${s})`});el('circle',{r:30,fill:RED},x);el('path',{d:'M-12 -12 L12 12 M12 -12 L-12 12',stroke:CHALK,'stroke-width':7,'stroke-linecap':'round'},x);return x};
function flake(p,s=1,c=ICE){const f=g(p,{transform:`scale(${s})`});for(let i=0;i<6;i++){const a=i*60;el('rect',{x:-5,y:-60,width:10,height:120,rx:5,fill:c,transform:`rotate(${a})`},f);el('path',{d:'M-16 -44 L0 -30 L16 -44',fill:'none',stroke:c,'stroke-width':8,'stroke-linecap':'round',transform:`rotate(${a})`},f)}return f}
function therm(p,h=320){const T=g(p);el('rect',{x:-26,y:-h/2,width:52,height:h,rx:26,fill:CHALK},T);const m=el('rect',{x:-12,y:0,width:24,height:0,rx:12,fill:RED},T);const bulb=el('circle',{cy:h/2+20,r:46,fill:RED},T);const lab=txt(T,0,-h/2-30,52,'bold ink','');
  T.set=(deg,lo=-20,hi=90)=>{const k=cl((deg-lo)/(hi-lo));const hh=(h-30)*k;m.setAttribute('y',h/2-hh);m.setAttribute('height',hh+20);const c=deg<40?COLD:(deg<65?'#E9C46A':RED);m.setAttribute('fill',c);bulb.setAttribute('fill',c);lab.textContent=Math.round(deg)+'°F'};T.lab=lab;return T}
// coolant temperature gauge: C ... H half arc
function tempGauge(p,r=150){const G=g(p);el('path',{d:`M${-r} 0 A${r} ${r} 0 0 1 ${r} 0`,fill:'none',stroke:'#2A2A33','stroke-width':r*.2,'stroke-linecap':'round'},G);
  el('path',{d:`M${-r} 0 A${r} ${r} 0 0 1 ${-r*Math.cos(Math.PI*.33)} ${-r*Math.sin(Math.PI*.33)}`,fill:'none',stroke:COLD,'stroke-width':r*.2,'stroke-linecap':'round'},G);
  el('path',{d:`M${r*Math.cos(Math.PI*.2)} ${-r*Math.sin(Math.PI*.2)} A${r} ${r} 0 0 1 ${r} 0`,fill:'none',stroke:RED,'stroke-width':r*.2,'stroke-linecap':'round'},G);
  txt(G,-r,r*.45,r*.24,'bold',"C").setAttribute('fill',COLD);txt(G,r,r*.45,r*.24,'bold',"H").setAttribute('fill',RED);
  const ic=g(G,{transform:`translate(0 ${r*.38}) scale(${r/150})`});el('rect',{x:-6,y:-34,width:12,height:46,rx:6,fill:CHALK},ic);el('circle',{cy:16,r:14,fill:CHALK},ic);[-22,-10,2].forEach(y=>el('rect',{x:8,y,width:16,height:5,rx:2,fill:CHALK},ic));
  const n=g(G);el('path',{d:`M-7 0 L0 ${-(r-16)} L7 0 Z`,fill:CHALK},n);el('circle',{r:r*.1,fill:CHALK},n);
  G.set=v=>n.setAttribute('transform',`rotate(${-90+180*cl(v)})`);G.set(0);return G}
// tachometer 0..8 (x1000 rpm)
function tach(p,r=170){const G=g(p);el('circle',{r,fill:'#1B1B21'},G);el('circle',{r,fill:'none',stroke:'#3A3A46','stroke-width':8},G);
  const ga=a=>(-135+270*a)*Math.PI/180;const red=el('path',{d:'',fill:'none',stroke:RED,'stroke-width':14},G);
  {const a0=ga(6/8),a1=ga(1),rr=r-24;red.setAttribute('d',`M${rr*Math.sin(a0)} ${-rr*Math.cos(a0)} A${rr} ${rr} 0 0 1 ${rr*Math.sin(a1)} ${-rr*Math.cos(a1)}`)}
  const zone=el('path',{d:'',fill:'none',stroke:LIME,'stroke-width':14,opacity:0},G);{const a0=ga(0),a1=ga(3/8),rr=r-24;zone.setAttribute('d',`M${rr*Math.sin(a0)} ${-rr*Math.cos(a0)} A${rr} ${rr} 0 0 1 ${rr*Math.sin(a1)} ${-rr*Math.cos(a1)}`)}
  for(let v=0;v<=8;v++){const a=ga(v/8);el('line',{x1:(r-34)*Math.sin(a),y1:-(r-34)*Math.cos(a),x2:(r-58)*Math.sin(a),y2:-(r-58)*Math.cos(a),stroke:CHALK,'stroke-width':6},G);txt(G,(r-84)*Math.sin(a),-(r-84)*Math.cos(a)+10,r*.15,'mic ink',String(v))}
  txt(G,0,r*.62,r*.1,'mic mut','RPM ×1000');const n=g(G);el('path',{d:`M-8 0 L0 ${-(r-40)} L8 0 Z`,fill:RED},n);el('circle',{r:r*.1,fill:CHALK},n);
  G.zone=zone;G.set=v=>n.setAttribute('transform',`rotate(${-135+270*cl(v/8)})`);G.set(0);return G}
function fuelGauge(p,r=110){const G=g(p);el('path',{d:`M${-r} 0 A${r} ${r} 0 0 1 ${r} 0`,fill:'none',stroke:'#2A2A33','stroke-width':r*.18,'stroke-linecap':'round'},G);
  txt(G,-r,r*.42,r*.26,'bold red','E');txt(G,r,r*.42,r*.26,'bold ink','F');
  const pumpI=g(G,{transform:`translate(0 ${r*.32}) scale(${r/220})`});el('rect',{x:-26,y:-40,width:44,height:70,rx:6,fill:CHALK},pumpI);el('rect',{x:-18,y:-32,width:28,height:20,rx:3,fill:ASPH},pumpI);el('path',{d:'M18 -20 L34 -8 L34 24',fill:'none',stroke:CHALK,'stroke-width':7,'stroke-linecap':'round'},pumpI);
  const n=g(G);el('path',{d:`M-6 0 L0 ${-(r-14)} L6 0 Z`,fill:AMBER},n);el('circle',{r:r*.11,fill:CHALK},n);
  G.set=v=>n.setAttribute('transform',`rotate(${-90+180*cl(v)})`);G.set(1);return G}
function manual(p,s=1){const m=g(p,{transform:`scale(${s})`});el('rect',{x:-130,y:-170,width:260,height:340,rx:16,fill:'#2E6BD8'},m);el('rect',{x:-130,y:-170,width:28,height:340,fill:'#1F4FA8'},m);txt(m,14,-40,36,'bold ink',"OWNER'S");txt(m,14,4,36,'bold ink','MANUAL');
  const ic=g(m,{transform:'translate(14 90) scale(.5)'});makeCar(ic,{body:CHALK,ink:'#1F4FA8',acc:AMBER}).setAttribute('transform','scale(.22)');return m}
function stopwatch(p,r=150){const S=g(p);el('rect',{x:-22,y:-r-40,width:44,height:30,rx:8,fill:CHALK},S);el('circle',{r:r+12,fill:CHALK},S);el('circle',{r,fill:'#1B1B21'},S);
  const arc=el('circle',{r:r-18,fill:'none',stroke:LIME,'stroke-width':20,pathLength:1000,transform:'rotate(-90)','stroke-dasharray':'0 1000'},S);const tt_=txt(S,0,r*.16,r*.42,'bold ink','');
  S.set=(k,label)=>{arc.setAttribute('stroke-dasharray',`${cl(k)*1000} 1000`);tt_.textContent=label};S.arc=arc;return S}
function numBadge(p,n,fill=LIME){const b=g(p);el('circle',{r:58,fill},b);txt(b,0,24,72,'bold',String(n)).setAttribute('fill',ASPH);return b}
function stamp(p,text,col=RED,w){const s=g(p);const W=w||text.length*36+80;el('rect',{x:-W/2,y:-62,width:W,height:124,rx:18,fill:'none',stroke:col,'stroke-width':10},s);txt(s,0,22,64,'bold',text).setAttribute('fill',col);return s}
// small generic engine block (side), centred
function engineBlock(p,s=1,fill='#6A6A76'){const e=g(p,{transform:`scale(${s})`});el('rect',{x:-150,y:-70,width:300,height:160,rx:20,fill},e);el('rect',{x:-120,y:-120,width:240,height:60,rx:14,fill:'#8A8A96'},e);
  [-80,-27,27,80].forEach(x=>el('rect',{x:x-14,y:-150,width:28,height:36,rx:6,fill:'#4A4A56'},e));el('rect',{x:-170,y:-20,width:30,height:70,rx:8,fill:'#4A4A56'},e);return e}
// side view pickup truck (facing right), ~1000 wide, origin centre bottom-ish
function makeTruck(p,o={}){const C=Object.assign({body:'#4E6A8C',ink:ASPH,glass:'#1B2433',acc:AMBER},o);const T=g(p);
  el('path',{d:'M-480 40 L-480 -60 Q-478 -80 -456 -80 L60 -80 L60 -60 L120 -60 L190 -190 Q200 -205 222 -205 L380 -205 Q410 -205 420 -180 L470 -90 Q500 -84 500 -50 L500 40 Q500 56 484 56 L-464 56 Q-480 56 -480 40 Z',fill:C.body},T);
  el('path',{d:'M146 -70 L206 -184 Q212 -192 224 -192 L300 -192 L300 -70 Z',fill:C.glass},T);el('path',{d:'M316 -192 L376 -192 Q396 -192 404 -176 L450 -90 L450 -70 L316 -70 Z',fill:C.glass},T);
  el('rect',{x:-470,y:-80,width:520,height:14,rx:6,fill:'#000',opacity:.18},T);const lamp=el('path',{d:'M478 -70 L500 -64 L500 -36 L478 -40 Z',fill:C.acc},T);
  el('rect',{x:-484,y:-50,width:12,height:30,rx:4,fill:RED},T);
  const wheels=[-300,320].map(x=>{const w=g(T,{transform:`translate(${x} 56)`});el('circle',{r:92,fill:C.ink},w);el('circle',{r:46,fill:'#9AA0AE'},w);const hub=g(w);[0,72,144,216,288].forEach(a=>el('rect',{x:-6,y:-40,width:12,height:24,rx:4,fill:'#5A5A66',transform:`rotate(${a})`},hub));el('circle',{r:12,fill:C.ink},w);w.hub=hub;return w});
  T.wheels=wheels;T.lamp=lamp;return T}
// car silhouette for icons (makeCar wrapper)
function carIcon(p,s=.3,o={}){const c=g(p);makeCar(c,Object.assign({body:CHALK,ink:ASPH,acc:AMBER},o)).setAttribute('transform',`scale(${s})`);return c}
// smoke / steam puffs: returns list, call upd(t, x0, y0, rate)
function puffs(p,n=10,col='#E8EEF6'){const L=[...Array(n)].map(()=>el('circle',{fill:col,opacity:0},p));
  L.upd=(t,x0,y0,vx=-60,vy=-40,life=2.2,on=1,size=26)=>{L.forEach((c,i)=>{const ph=((t/life)+i/n)%1;const age=ph*life;c.setAttribute('cx',x0+vx*age+8*Math.sin(age*3+i));c.setAttribute('cy',y0+vy*age-age*age*6);c.setAttribute('r',size*(.5+age*1.1));c.setAttribute('opacity',on*.55*(1-ph)*Math.min(1,ph*8))})};return L}
// deterministic falling snow over an area
function snowfall(p,n=60,area=[0,0,1920,1080]){const L=[...Array(n)].map((_,i)=>el('circle',{r:2+((i*37)%5),fill:'#FFFFFF',opacity:.75},p));
  L.upd=(t,speed=1)=>{const [x,y,w,h]=area;L.forEach((c,i)=>{const sp=(40+((i*53)%60))*speed;const yy=y+((i*97+t*sp)%h);const xx=x+((i*131)%w)+18*Math.sin(t*.8+i);c.setAttribute('cx',xx);c.setAttribute('cy',yy)})};return L}

// caption box placement: full width (outdoor) or right of the narrator (studio)
const capEl=document.getElementById('cap');
function capMode(m){if(capEl._m===m)return;capEl._m=m;if(m==='wide'){capEl.style.left='210px';capEl.style.width='1500px'}else{capEl.style.left='720px';capEl.style.width='1140px'}}

// narrator poses (pointing at the right-hand stage)
const SHP=[612,606];const ptTo=(x,y,shape='point')=>{const a=Math.atan2(y-SHP[1],x-SHP[0]);return {L:REST.L,R:{x:182+300*Math.cos(a),y:46+300*Math.sin(a),shape}}};
const POSE={rest:REST,open:{L:{x:-300,y:190,shape:'open'},R:{x:300,y:190,shape:'open'}},one:{L:REST.L,R:{x:240,y:-50,shape:'point',rot:-90}},thumb:{L:REST.L,R:{x:320,y:140,shape:'thumb',rot:0}},
 shrug:{L:{x:-290,y:140,shape:'open'},R:{x:290,y:140,shape:'open'}},stop:{L:REST.L,R:{x:330,y:20,shape:'open',rot:-90}},wave:{L:REST.L,R:{x:300,y:-40,shape:'open',rot:-80}},
 hug:{L:{x:-120,y:240,shape:'fist'},R:{x:120,y:240,shape:'fist'}},
 mid:ptTo(CX,420),top:ptTo(CX,240),low:ptTo(CX,640),left:ptTo(1040,420),right:ptTo(1560,420)};
