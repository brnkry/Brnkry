// Episode 04: "is there a word in between yes and no" -> "maybe" -> "Ok well what is it then?"
const EP={};
chair(250,1,'#D9534F');chair(828,-1,'#9B7BD9');
const VK=makeStick('L','wide'),PY=makeStick('R','crossed');
table();
// ---------- Viktor (left): buzz cut, big angry brows, loud ----------
(()=>{const h=VK.head;el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h);
  pth(h,'M-56 -26 Q-50 -60 0 -64 Q50 -60 58 -26',{stroke:'#555','stroke-width':4,'stroke-dasharray':'2 7'});
  h.eyes=G(h);el('circle',{cx:14,cy:-4,r:6,fill:INK},h.eyes);el('circle',{cx:44,cy:-4,r:6,fill:INK},h.eyes);
  h.brA=el('path',{d:'M-2 -26 L26 -20',stroke:INK,'stroke-width':9,'stroke-linecap':'round'},h);h.brB=el('path',{d:'M34 -20 L60 -28',stroke:INK,'stroke-width':9,'stroke-linecap':'round'},h);
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h);})();
// ---------- perynyc (right): beanie, half-lidded eyes, calm smirk ----------
(()=>{const h=PY.head;el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h);
  h.beanie=G(h);el('path',{d:'M-62 -16 Q-62 -76 0 -78 Q62 -76 62 -16 Z',fill:'#9B7BD9',stroke:INK,'stroke-width':6,'stroke-linejoin':'round'},h.beanie);el('rect',{x:-66,y:-28,width:132,height:20,rx:8,fill:'#7B5BB9',stroke:INK,'stroke-width':5},h.beanie);el('circle',{cx:0,cy:-82,r:12,fill:'#F2C230',stroke:INK,'stroke-width':4},h.beanie);
  h.eyes=G(h);[-16,-46].forEach(x=>{el('circle',{cx:x,cy:2,r:6,fill:INK},h.eyes);ln(h.eyes,x-11,-4,x+11,-4,5)});
  h.front=G(h);el('circle',{cx:-18,cy:0,r:6,fill:INK},h.front);el('circle',{cx:18,cy:0,r:6,fill:INK},h.front);ln(h.front,-30,-6,-6,-6,5);ln(h.front,6,-6,30,-6,5);pth(h.front,'M-14 28 H14',{'stroke-width':5});
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h);})();

const VPOSE={idle:{lean:-4,n:[70,135],f:[50,140]},listen:{lean:6,tilt:6,n:[60,60],f:[40,70]},demand:{lean:16,n:[150,-60],f:[-60,-80]},wait:{lean:10,tilt:-6,n:[120,-20],f:[-70,-40]}};
const VKEYS=[[0,'listen'],[3.7,'idle'],[5.3,'demand'],[7.6,'wait']];
const YPOSE={idle:{lean:2,n:[70,135],f:[60,140]},think:{lean:4,tilt:-6,n:[48,-96],f:[60,140]},answer:{lean:6,n:[130,-10],f:[60,140]},stare:{lean:0,n:[70,135],f:[60,140]}};
const YKEYS=[[0,'idle'],[1.9,'think'],[3.05,'answer'],[4.0,'idle'],[7.6,'stare']];
const vPose=poser(VPOSE,VKEYS,.22),yPose=poser(YPOSE,YKEYS,.25);

// ---------- live caller screen (Cam asks the question) ----------
const scr=G(fx);el('rect',{x:-390,y:-150,width:780,height:300,rx:24,fill:'#22202B',stroke:INK,'stroke-width':8},scr);el('rect',{x:-390,y:-150,width:780,height:66,rx:24,fill:RED,stroke:INK,'stroke-width':8},scr);
T(scr,0,-104,'📞 LIVE CALLER',40,'mk','#fff');el('circle',{cx:-330,cy:-30,r:28,fill:USERS.C.color,stroke:'#fff','stroke-width':4},scr);T(scr,-286,-38,USERS.C.name,30,'hand','#A9A6B5','start');
const camT=T(scr,-286,6,'',44,'hand','#fff','start');const camT2=T(scr,-286,52,'',44,'hand','#fff','start');const camLk=T(scr,360,126,'♥ 23.1K',30,'hand',RED,'end');
// the attached "big brain" pic: little guy tapping his temple
const brain=G(scr,{transform:'translate(300 20)'});el('rect',{x:-56,y:-56,width:112,height:112,rx:10,fill:'#3A3442',stroke:'#fff','stroke-width':3},brain);el('circle',{cx:0,cy:-8,r:26,fill:PAPER,stroke:INK,'stroke-width':4},brain);
const tap=G(brain);ln(tap,30,52,24,-16,6,PAPER);el('circle',{cx:24,cy:-18,r:6,fill:PAPER},tap);ln(brain,-8,-12,-2,-12,3);ln(brain,8,-12,14,-12,3);pth(brain,'M-8 4 q8 6 16 0',{stroke:INK,'stroke-width':3});
// yes / no meter
const meter=G(fx);el('rect',{x:-330,y:-24,width:660,height:48,rx:24,fill:'#fff',stroke:INK,'stroke-width':6},meter);
el('rect',{x:-330,y:-24,width:200,height:48,rx:24,fill:'#FADADC'},meter);el('rect',{x:130,y:-24,width:200,height:48,rx:24,fill:'#DDF2D5'},meter);el('rect',{x:-330,y:-24,width:660,height:48,rx:24,fill:'none',stroke:INK,'stroke-width':6},meter);
T(meter,-260,-44,'NO',44,'mk',RED);T(meter,260,-44,'YES',44,'mk',GREEN);const midQ=T(meter,0,-44,'???',44,'mk',GREY);
const knob=G(meter);el('circle',{r:30,fill:'#F2C230',stroke:INK,'stroke-width':6},knob);
const maybeB=badge(fx,'✓ MAYBE',PAPER,GREEN,56,280,90);
const dots=T(fx,0,0,'...',120,'mk',INK);
const bigQ=T(fx,0,0,'?',180,'mk',RED);bigQ.setAttribute('stroke',INK);bigQ.setAttribute('stroke-width',8);bigQ.setAttribute('paint-order','stroke');

EP.render=function(t){
  // ----- Viktor -----
  let vp=vPose(t);const vm=talkMouth('V',t);if(vp.name==='demand')vp.n[1]+=Math.sin(t*9)*14;
  placeStick(VK,vp,t,{});
  {const h=VK.head;const ang=Math.max(V(t,5.3,8.7,.2,.01),.25);
    h.brA.setAttribute('d',`M-2 ${-30+8*ang} L26 ${-22+2*ang}`);h.brB.setAttribute('d',`M34 ${-22+2*ang} L60 ${-30+8*ang}`);
    const bl=blink(t,2.9,.5);h.eyes.setAttribute('transform',`translate(0 -4) scale(1 ${bl}) translate(0 4)`);
    const o=vm*34,mx=32;h.mouth.setAttribute('d',o<3?`M${mx-16} 32 Q${mx} 26 ${mx+16} 32`:`M${mx-20} 22 Q${mx} 18 ${mx+20} 22 Q${mx+18} ${26+o} ${mx} ${28+o} Q${mx-18} ${28+o} ${mx-20} 22 Z`);h.mouth.setAttribute('fill',o<3?'none':'#5A1E22')}
  // ----- perynyc -----
  let yp=yPose(t);const ym=talkMouth('Y',t);
  const turn=eio(P(t,7.7,.4));placeStick(PY,yp,t,{});
  {const h=PY.head;op(h.eyes,1-turn>.5?1:0);op(h.front,turn>.5?1:0);
    const o=ym*22,mx=-32;h.mouth.setAttribute('d',turn>.5?'':(o<3?`M${mx-16} 30 Q${mx-2} 34 ${mx+16} 24`:`M${mx-18} 22 Q${mx} 20 ${mx+18} 22 Q${mx+16} ${26+o} ${mx} ${28+o} Q${mx-16} ${28+o} ${mx-18} 22 Z`));h.mouth.setAttribute('fill',o<3?'none':'#5A1E22')}
  camera([[eio(P(t,7.75,.8)),1.6,PY.Cs[0],PY.Cs[1]+60]],0,t);
  // ----- caller screen -----
  {const o=t<3.0?1-P(t,2.8,.2):0;op(scr,o);tr(scr,540,560,1);const L0=ID.c1;let a='',b='';L0.w.forEach(([w,ts],j)=>{if(t>=ts-.05){if(j<5)a+=(a?' ':'')+w;else b+=(b?' ':'')+w}});camT.textContent=a;camT2.textContent=b;op(camLk,t>1.7?1:0);
    tap.setAttribute('transform',`rotate(${Math.sin(t*10)*6} 24 -16)`)}
  // ----- meter: knob wanders between YES and NO, settles on "maybe" -----
  {const o=t>=1.2&&t<5.3?1-P(t,5.1,.2):0;op(meter,o);tr(meter,540,t<3?830:ID.y1.top-90,back(P(t,1.2,.3)));
    const x=t<3.2?Math.sin(t*5)*260:lerp(Math.sin(3.2*5)*260,0,eo(P(t,3.2,.35)));knob.setAttribute('transform',`translate(${x} 0)`);midQ.textContent=t>=3.2?'MAYBE':'???';midQ.setAttribute('fill',t>=3.2?GREEN:GREY)}
  pop(maybeB,770,ID.y1.top-190,t,3.3,5.3,6);
  pop(bigQ,VK.Cs[0]+150,VK.Cs[1]-30,t,7.4,8.7,10,.75);
  {const o=t>7.9?eo(P(t,7.9,.3)):0;op(dots,o);dots.setAttribute('x',PY.Cs[0]-40);dots.setAttribute('y',PY.Cs[1]-120)}
};
EP.init=function(){};
