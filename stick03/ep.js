// Episode 03: "bogos binted". The photo guy (left) and the disguised alien (right) swap languages, and bodies, at SWAP.
const EP={};
chair(250,1,'#7AC943');chair(828,-1,'#9B7BD9');
const AG=makeStick('L','neat'),BG=makeStick('R','crossed');
table();
const SW=window.SWAP,ALIEN='#8FD14F';
// alien head kit: green skull, antennae, big black eyes. Drawn into a head group, facing dir f (+1 right, -1 left)
function alienKit(h,f){const k=G(h);const ant=G(k);[[-22,-50,-40,-104],[22,-50,40,-104]].forEach(([x1,y1,x2,y2])=>{pth(ant,`M${x1} ${y1} Q${x1*1.4} ${(y1+y2)/2} ${x2} ${y2}`,{'stroke-width':6});el('circle',{cx:x2,cy:y2,r:11,fill:'#F2C230',stroke:INK,'stroke-width':4},ant)});
  k.skull=el('path',{d:'M0 -66 C48 -66 66 -30 62 6 C58 44 28 68 0 68 C-28 68 -58 44 -62 6 C-66 -30 -48 -66 0 -66 Z',fill:ALIEN,stroke:INK,'stroke-width':8},k);
  k.eyes=G(k);el('ellipse',{cx:f*8,cy:-6,rx:16,ry:24,fill:INK,transform:`rotate(${-20*f} ${f*8} -6)`},k.eyes);el('ellipse',{cx:f*44,cy:-6,rx:13,ry:21,fill:INK,transform:`rotate(${20*f} ${f*44} -6)`},k.eyes);
  el('circle',{cx:f*4,cy:-14,r:5,fill:'#fff'},k.eyes);el('circle',{cx:f*40,cy:-14,r:4,fill:'#fff'},k.eyes);
  k.mouth=el('path',{fill:'#2E4A1A',stroke:INK,'stroke-width':4,'stroke-linejoin':'round'},k);k.ant=ant;return k}
// ---------- A: friendly photo guy (left) ----------
(()=>{const h=AG.head;h.human=G(h);
  el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h.human);el('path',{d:'M-60 -14 Q-58 -62 -2 -64 Q46 -64 58 -30 Q20 -44 -18 -40 Q-40 -30 -60 -14 Z',fill:'#7A4A2A',stroke:INK,'stroke-width':5},h.human);
  h.eyes=G(h.human);el('circle',{cx:14,cy:-6,r:6,fill:INK},h.eyes);el('circle',{cx:44,cy:-6,r:6,fill:INK},h.eyes);
  h.brows=G(h.human);ln(h.brows,4,-24,24,-26,5);ln(h.brows,36,-26,54,-22,5);
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h.human);
  h.alien=alienKit(h,1);
})();
// ---------- B: alien in a terrible disguise (right): fedora with antennae poking out, nose-glasses, moustache ----------
(()=>{const h=BG.head;h.alien=alienKit(h,-1);
  op(h.alien.ant,0);h.human=G(h);el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h.human);h.hEyes=G(h.human);el('circle',{cx:-14,cy:-6,r:6,fill:INK},h.hEyes);el('circle',{cx:-44,cy:-6,r:6,fill:INK},h.hEyes);
  h.hMouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h.human);
  h.disguise=G(h);el('circle',{cx:-24,cy:-8,r:17,fill:'rgba(255,255,255,.25)',stroke:INK,'stroke-width':5},h.disguise);el('circle',{cx:-58,cy:-8,r:14,fill:'rgba(255,255,255,.25)',stroke:INK,'stroke-width':5},h.disguise);ln(h.disguise,-41,-10,-44,-10,5);
  el('path',{d:'M-46 0 q-10 22 4 26',fill:'#F2B79A',stroke:INK,'stroke-width':4},h.disguise);el('path',{d:'M-70 30 q14 -14 26 -4 q12 -10 26 4 q-12 10 -26 0 q-14 10 -26 0 Z',fill:INK},h.disguise);
  h.hat=G(h);el('path',{d:'M-84 -40 H84 Q90 -30 80 -28 H-80 Q-90 -30 -84 -40 Z',fill:'#3A3A40',stroke:INK,'stroke-width':5},h.hat);el('path',{d:'M-46 -40 L-40 -86 Q0 -100 40 -86 L46 -40 Z',fill:'#4A4A52',stroke:INK,'stroke-width':6,'stroke-linejoin':'round'},h.hat);
  el('rect',{x:-45,y:-56,width:90,height:12,fill:'#9B7BD9'},h.hat);
  h.hatAnt=G(h.hat);[[-14,-94,-30,-130],[14,-94,30,-130]].forEach(([x1,y1,x2,y2])=>{pth(h.hatAnt,`M${x1} ${y1} L${x2} ${y2}`,{'stroke-width':6});el('circle',{cx:x2,cy:y2,r:11,fill:'#F2C230',stroke:INK,'stroke-width':4},h.hatAnt)});
  // printed photos in B's near hand
  BG.photos=G(BG.prop);[[-26,-10,-14],[0,-16,0],[26,-10,14]].forEach(([x,y,r])=>{const p=G(BG.photos,{transform:`translate(${x} ${y}) rotate(${r})`});el('rect',{x:-26,y:-32,width:52,height:62,rx:3,fill:'#fff',stroke:INK,'stroke-width':4},p);el('rect',{x:-20,y:-26,width:40,height:36,fill:'#BFE3F5'},p);el('path',{d:'M-20 10 l12 -14 l10 10 l8 -6 l10 10 Z',fill:'#7AC943'},p)});
})();

// ---------- poses ----------
const APOSE={ask:{lean:4,tilt:6,n:[115,0],f:[50,140]},idle:{lean:2,n:[70,135],f:[50,140]},what:{lean:-12,tilt:-8,n:[120,-50],f:[-70,-50]},
  alien:{lean:6,n:[120,-60],f:[40,-60]},vorp:{lean:2,tilt:16,n:[90,-20],f:[50,140]},beam:{lean:0,n:[60,-160],f:[-30,-160]}};
const AKEYS=[[0,'ask'],[1.75,'idle'],[2.75,'what'],[3.45,'alien'],[5.8,'idle'],[6.85,'vorp'],[7.55,'beam']];
const BPOSE={idle:{lean:2,n:[70,135],f:[60,140]},talk:{lean:8,n:[120,-20],f:[60,140]},show:{lean:10,n:[150,-40],f:[60,140]},shrug:{lean:0,tilt:-8,n:[120,-40],f:[-80,-40]}};
const BKEYS=[[0,'idle'],[1.8,'talk'],[2.5,'idle'],[3.5,'shrug'],[5.85,'show'],[6.8,'idle']];
const aPose=poser(APOSE,AKEYS,.22),bPose=poser(BPOSE,BKEYS,.22);

// ---------- stickers ----------
const camQ=badge(fx,'📸 ?',PAPER,INK,54,150,90);
const glyph=G(fx);el('rect',{x:-230,y:-56,width:460,height:112,rx:16,fill:'#1E2A1A',stroke:INK,'stroke-width':6},glyph);T(glyph,0,20,'⏃⌰⟟⟒⋏ ⏁⟒⌖⏁',54,'mk','#9BFF5C');
const bigQ=T(fx,0,0,'?',220,'mk',RED);bigQ.setAttribute('stroke',INK);bigQ.setAttribute('stroke-width',8);bigQ.setAttribute('paint-order','stroke');
const flash=document.createElement('div');flash.style.cssText='position:absolute;inset:0;pointer-events:none';document.getElementById('stage').appendChild(flash);
const swapB=badge(fx,'⚠ LANGUAGE SWAP',PAPER,RED,46,460,84);
const pics=G(fx);[[-120,-8],[0,4],[120,-4]].forEach(([x,r])=>{const p=G(pics,{transform:`translate(${x} 0) rotate(${r})`});el('rect',{x:-56,y:-66,width:112,height:132,rx:4,fill:'#fff',stroke:INK,'stroke-width':5},p);el('rect',{x:-44,y:-54,width:88,height:80,fill:'#BFE3F5'},p);el('circle',{cx:20,cy:-34,r:10,fill:'#F2C230'},p);el('path',{d:'M-44 26 l26 -30 l22 20 l16 -12 l24 22 Z',fill:'#7AC943'},p)});
const ok=T(fx,0,0,'✓',90,'mk',GREEN);
const seen=T(fx,0,0,'✓ Seen 12:53am',40,'hand',GREY,'end');
const ufo=G(fx);const beam=el('path',{d:'M-60 30 L-190 900 L190 900 L60 30 Z',fill:'#FFF59A',opacity:.55},ufo);el('ellipse',{cx:0,cy:0,rx:160,ry:44,fill:'#B9B3C6',stroke:INK,'stroke-width':7},ufo);
el('path',{d:'M-70 -16 Q0 -100 70 -16 Z',fill:'#BFE3F5',stroke:INK,'stroke-width':6},ufo);[-100,-50,0,50,100].forEach(x=>el('circle',{cx:x,cy:8,r:9,fill:'#F2C230',stroke:INK,'stroke-width':3},ufo));

// ---------- per frame ----------
EP.render=function(t){
  const sw=P(t,SW,.25);const glitch=V(t,SW-.08,SW+.28,.05,.12);
  // ----- A -----
  let ap=aPose(t);const am=talkMouth('A',t);if(ap.name==='ask'||ap.name==='alien')ap.n[1]+=Math.sin(t*8)*10;
  const lift=-260*eio(P(t,7.65,.6));
  placeStick(AG,ap,t,{s:1+.12*V(t,2.8,3.3,.08,.2)});AG.g.setAttribute('transform',`translate(0 ${lift})`);
  {const h=AG.head;const isA=t>=SW+.06;op(h.human,isA?0:1);op(h.alien,isA?1:0);
    const bl=blink(t,3.1,.2);h.eyes.setAttribute('transform',`translate(0 -6) scale(1 ${bl}) translate(0 6)`);
    const wide=V(t,2.75,3.4,.08,.1);tr(h.brows,0,-10*wide);
    const o=am*26+wide*16,mx=30;h.mouth.setAttribute('d',o<3?`M${mx-16} 26 Q${mx} 38 ${mx+16} 26`:`M${mx-18} 22 Q${mx} 20 ${mx+18} 22 Q${mx+16} ${26+o} ${mx} ${28+o} Q${mx-16} ${28+o} ${mx-18} 22 Z`);h.mouth.setAttribute('fill',o<3?'none':'#5A1E22');
    const ao=am*22;h.alien.mouth.setAttribute('d',`M14 34 Q28 ${34+ao*.4} 42 34 Q36 ${38+ao} 28 ${40+ao} Q20 ${38+ao} 14 34 Z`);
    h.alien.ant.setAttribute('transform',`rotate(${Math.sin(t*9)*6})`);tr(h.alien,0,0,isA?back(P(t,SW+.06,.25)):1)}
  // ----- B -----
  let bp=bPose(t);const bm=talkMouth('B',t);if(bp.name==='talk')bp.n[1]+=Math.sin(t*8)*10;
  placeStick(BG,bp,t,{});
  {const h=BG.head;const human=t>=SW+.06;op(h.alien,human?0:1);op(h.human,human?1:0);
    const fly=P(t,SW+.02,.6);tr(h.hat,90*fly,-260*fly+300*fly*fly,1,60*fly);op(h.hat,fly<1?1:0);tr(h.disguise,0,200*fly*fly,1,-20*fly);op(h.disguise,fly<1?1:0);
    const o=bm*24;h.alien.mouth.setAttribute('d',`M-42 34 Q-28 ${34+o*.4} -14 34 Q-20 ${38+o} -28 ${40+o} Q-36 ${38+o} -42 34 Z`);
    const mx=-30;h.hMouth.setAttribute('d',o<3?`M${mx-16} 28 Q${mx} 36 ${mx+16} 28`:`M${mx-18} 22 Q${mx} 20 ${mx+18} 22 Q${mx+16} ${26+o} ${mx} ${28+o} Q${mx-16} ${28+o} ${mx-18} 22 Z`);h.hMouth.setAttribute('fill',o<3?'none':'#5A1E22');
    const sh=bp.name==='show'?bp.k:0;op(BG.photos,sh);tr(BG.photos,BG.Wn[0]-10,BG.Wn[1]-30,1.1,-8)}
  // ----- camera, glitch -----
  camera([[eio(P(t,7.55,.5)),1.25,540,900]],glitch*.9,t);
  flash.style.background=glitch>0?`rgba(${Math.floor(t*60)%2?'155,255,92':'255,61,165'},${.35*glitch})`:'none';
  document.getElementById('cam').style.filter=glitch>0?`hue-rotate(${Math.floor(t*30)%2?90:-90}deg)`:'none';
  // ----- stickers -----
  pop(camQ,640,topOf('a1')-80,t,1.04,1.75,-5);
  pop(glyph,540,topOf('b1')-80,t,1.9,2.6,3);
  pop(bigQ,AG.Cs[0]+150,AG.Cs[1]+10,t,2.82,3.3,10,.7);
  pop(swapB,540,topOf('a3')-80,t,SW+.05,5.7,-3);
  pop(pics,560,topOf('b2')-110,t,5.97,6.75,0,.95);pop(ok,800,topOf('b2')-170,t,6.3,6.75,8);
  {const o=t>=7.45?eo(P(t,7.45,.2)):0;op(seen,o);seen.setAttribute('x',930);seen.setAttribute('y',990)}
  {const k=eio(P(t,7.4,.4));op(ufo,t>=7.4?1:0);tr(ufo,lerp(-300,AG.Cs[0],k),360,1);beam.style.opacity=t>7.6?.55*(.8+.2*Math.sin(t*30)):0}
};
EP.init=function(){};
