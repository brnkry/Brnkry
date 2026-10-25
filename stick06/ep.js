// Episode 06: "What's the movie name?" -> "ready or not" -> "Ready"
const EP={};
chair(250,1,'#FF8FC8');chair(828,-1,'#6B5A50');
const SA=makeStick('L','neat'),AS=makeStick('R','crossed');
table();
// ---------- Samara (left): pink hair with two buns ----------
(()=>{const h=SA.head;[-46,46].forEach(x=>el('circle',{cx:x,cy:-58,r:22,fill:'#FF8FC8',stroke:INK,'stroke-width':6},h));
  el('path',{d:'M-70 50 Q-80 -70 0 -74 Q80 -70 70 50 Z',fill:'#FF8FC8',stroke:INK,'stroke-width':6},h);
  el('circle',{r:58,fill:PAPER,stroke:INK,'stroke-width':8},h);el('path',{d:'M-56 -16 Q-50 -62 6 -62 Q50 -58 58 -20 Q30 -36 4 -28 Q-26 -40 -56 -16 Z',fill:'#FF8FC8',stroke:INK,'stroke-width':5},h);
  h.eyes=G(h);[16,42].forEach(x=>{el('circle',{cx:x,cy:-2,r:8,fill:INK},h.eyes);el('circle',{cx:x+2,cy:-5,r:2.5,fill:'#fff'},h.eyes)});
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h);
  h.blush=G(h);[6,50].forEach(x=>el('ellipse',{cx:x,cy:16,rx:8,ry:4,fill:'#FF8FC8',opacity:.7},h.blush))})();
// ---------- ash (right): messy dark hair ----------
(()=>{const h=AS.head;el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h);
  el('path',{d:'M-62 -10 Q-70 -70 -10 -72 Q50 -76 64 -20 L50 -30 L44 -14 L30 -32 L18 -18 L2 -34 L-12 -20 L-26 -36 L-40 -18 Z',fill:'#3B2A20',stroke:INK,'stroke-width':5,'stroke-linejoin':'round'},h);
  h.eyes=G(h);el('circle',{cx:-16,cy:-2,r:6,fill:INK},h.eyes);el('circle',{cx:-46,cy:-2,r:6,fill:INK},h.eyes);
  h.brows=G(h);ln(h.brows,-6,-20,-26,-22,5);ln(h.brows,-36,-22,-56,-20,5);
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h)})();

const SPOSE={ask:{lean:4,tilt:6,n:[115,0],f:[50,140]},idle:{lean:2,n:[70,135],f:[50,140]},ready:{lean:10,n:[110,-60],f:[90,-50]}};
const SKEYS=[[0,'ask'],[1.2,'idle'],[4.45,'ready']];
const APOSE={idle:{lean:2,n:[70,135],f:[60,140]},tell:{lean:8,n:[125,-10],f:[60,140]},facepalm:{lean:12,tilt:14,n:[48,-92],f:[60,140]}};
const AKEYS=[[0,'idle'],[2.15,'tell'],[3.0,'idle'],[5.0,'facepalm']];
const sPose=poser(SPOSE,SKEYS,.22),aPose=poser(APOSE,AKEYS,.25);

// ---------- stickers (what the lines say, nothing more) ----------
const clap=G(fx);el('rect',{x:-90,y:-30,width:180,height:110,rx:8,fill:'#2B2B31',stroke:INK,'stroke-width':6},clap);T(clap,0,46,'???',50,'mk','#fff');
const clapTop=G(clap);el('rect',{x:-90,y:-62,width:180,height:30,rx:4,fill:'#fff',stroke:INK,'stroke-width':6},clapTop);[-60,-20,20,60].forEach(x=>el('path',{d:`M${x-12} -62 l20 0 l-12 30 l-20 0 Z`,fill:INK},clapTop));
const poster=G(fx);el('rect',{x:-130,y:-170,width:260,height:340,rx:10,fill:'#2B2230',stroke:INK,'stroke-width':7},poster);
T(poster,0,-90,'READY',62,'mk','#fff');T(poster,0,-40,'OR NOT',50,'mk',RED);
el('circle',{cx:0,cy:60,r:40,fill:'#fff',stroke:INK,'stroke-width':5},poster);pth(poster,'M-14 52 l6 0 M8 52 l6 0 M-12 74 q12 -10 24 0',{'stroke-width':5});T(poster,0,150,'🎬 MOVIE',30,'hand','#A9A6B5');
const readyB=badge(fx,'✔ READY!',PAPER,GREEN,56,280,90);
const q=T(fx,0,0,'?!',120,'mk',RED);q.setAttribute('stroke',INK);q.setAttribute('stroke-width',7);q.setAttribute('paint-order','stroke');

EP.render=function(t){
  let sp=sPose(t);const sm=talkMouth('S',t);if(sp.name==='ask')sp.n[1]+=Math.sin(t*8)*10;if(sp.name==='ready'){sp.n[1]+=Math.sin(t*10)*8;sp.f[1]+=Math.sin(t*10)*8}
  placeStick(SA,sp,t,{});
  {const h=SA.head;const bl=blink(t,3.0,.4);h.eyes.setAttribute('transform',`translate(0 -2) scale(1 ${bl}) translate(0 2)`);
    const o=sm*24,mx=30;h.mouth.setAttribute('d',o<3?`M${mx-14} 24 Q${mx} 34 ${mx+14} 24`:`M${mx-16} 20 Q${mx} 18 ${mx+16} 20 Q${mx+14} ${24+o} ${mx} ${26+o} Q${mx-14} ${26+o} ${mx-16} 20 Z`);h.mouth.setAttribute('fill',o<3?'none':'#5A1E22')}
  let ap=aPose(t);const am=talkMouth('A',t);if(ap.name==='tell')ap.n[1]+=Math.sin(t*8)*10;
  placeStick(AS,ap,t,{});
  {const h=AS.head;const bl=blink(t,3.6,1.1);h.eyes.setAttribute('transform',`translate(0 -2) scale(1 ${bl}) translate(0 2)`);
    const fr=V(t,4.7,6.6,.2,.01);tr(h.brows,0,6*fr);
    const o=am*24,mx=-32;h.mouth.setAttribute('d',o<3?`M${mx-14} ${28+fr*4} Q${mx} ${32-fr*10} ${mx+14} ${28+fr*4}`:`M${mx-16} 20 Q${mx} 18 ${mx+16} 20 Q${mx+14} ${24+o} ${mx} ${26+o} Q${mx-14} ${26+o} ${mx-16} 20 Z`);h.mouth.setAttribute('fill',o<3?'none':'#5A1E22')}
  pop(clap,700,topOf('s1')-110,t,.42,2.2,6);clapTop.setAttribute('transform',`rotate(${-18*(1-P(t,.81,.12))} -90 -32)`);
  pop(poster,540,topOf('a1')-230,t,2.3,4.4,-3,.85);
  pop(readyB,560,topOf('s2')-90,t,4.59,6.6,-4);
  pop(q,AS.Cs[0]-120,AS.Cs[1]-150,t,5.1,6.6,-8,.8);
};
EP.init=function(){};
