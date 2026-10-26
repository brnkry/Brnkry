// Episode 08: claustrophobic = "hating Santa for no reason" (Claus-trophobic)
const EP={};
chair(250,1,'#4A5A7A');chair(828,-1,'#7B6BE0');
const LV=makeStick('L','neat'),AS=makeStick('R','lazy');
table();
// ---------- levi (left): beanie-less, round confused eyes ----------
(()=>{const h=LV.head;el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h);
  el('path',{d:'M-58 -20 Q-54 -66 0 -66 Q54 -64 60 -20 Q40 -40 20 -30 Q0 -44 -20 -30 Q-40 -42 -58 -20 Z',fill:'#2A2A30',stroke:INK,'stroke-width':4},h);
  h.eyes=G(h);[14,44].forEach(x=>{el('circle',{cx:x,cy:-4,r:10,fill:'#fff',stroke:INK,'stroke-width':4},h.eyes);el('circle',{cx:x+2,cy:-4,r:4,fill:INK},h.eyes)});
  h.brows=G(h);ln(h.brows,2,-24,24,-28,5);ln(h.brows,34,-28,56,-22,5);
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h)})();
// ---------- astral the goat (right): goat horns, smug; turns into the creepy grin at the end ----------
(()=>{const h=AS.head;h.glow=el('circle',{r:160,fill:'#FF6A1A',opacity:0},h);
  h.horns=G(h);pth(h.horns,'M-30 -54 q-10 -40 -40 -46 M30 -54 q10 -40 40 -46',{stroke:'#8A7A60','stroke-width':12});
  h.skull=el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h);
  h.normal=G(h);el('circle',{cx:-16,cy:-4,r:6,fill:INK},h.normal);el('circle',{cx:-46,cy:-4,r:6,fill:INK},h.normal);ln(h.normal,-6,-16,-26,-14,5);ln(h.normal,-36,-14,-56,-16,5);
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h.normal);
  h.creep=G(h);el('ellipse',{cx:-20,cy:-14,rx:14,ry:10,fill:'#2A2A30'},h.creep);el('ellipse',{cx:22,cy:-14,rx:14,ry:10,fill:'#2A2A30'},h.creep);
  pth(h.creep,'M-44 -34 l18 8 M44 -34 l-18 8',{'stroke-width':6});
  el('path',{d:'M-46 14 Q0 70 46 14 Q0 30 -46 14 Z',fill:'#3A0E12',stroke:INK,'stroke-width':5},h.creep);
  for(let i=-3;i<=3;i++)el('path',{d:`M${i*12-5} ${20+Math.abs(i)*-1} l5 12 l5 -12 Z`,fill:'#F6F2E8',stroke:INK,'stroke-width':2},h.creep);
})();

const LPOSE={idle:{lean:2,n:[70,135],f:[50,140]},ask:{lean:6,tilt:10,n:[115,-10],f:[50,140]},scratch:{lean:0,tilt:-8,n:[30,-150],f:[50,140]},recoil:{lean:-20,tilt:-8,n:[70,-90],f:[50,-80]}};
const LKEYS=[[0,'idle'],[3.7,'ask'],[5.2,'scratch'],[6.5,'idle'],[9.4,'recoil']];
const APOSE={idle:{lean:-6,n:[-25,-120],f:[-45,-112]},tell:{lean:8,n:[130,-10],f:[-45,-112]},creep:{lean:18,n:[120,-80],f:[100,-60]}};
const AKEYS=[[0,'idle'],[6.5,'tell'],[8.4,'idle'],[9.4,'creep']];
const lPose=poser(LPOSE,LKEYS,.25),aPose=poser(APOSE,AKEYS,.3);

// ---------- live caller screen (michael) ----------
const scr=G(fx);el('rect',{x:-390,y:-130,width:780,height:260,rx:24,fill:'#22202B',stroke:INK,'stroke-width':8},scr);el('rect',{x:-390,y:-130,width:780,height:66,rx:24,fill:RED,stroke:INK,'stroke-width':8},scr);
T(scr,0,-84,'📞 LIVE CALLER',40,'mk','#fff');el('circle',{cx:-330,cy:-8,r:28,fill:USERS.MI.color,stroke:'#fff','stroke-width':4},scr);T(scr,-286,-16,USERS.MI.name,30,'hand','#A9A6B5','start');
const miT=T(scr,-286,40,'',44,'hand','#fff','start');const miLk=T(scr,360,108,'♥ 7,431',30,'hand',RED,'end');
// stickers: only what the lines say
const word=badge(fx,'CLAUSTROPHOBIC',PAPER,BLUE,54,520,90);
const qm=T(fx,0,0,'?',150,'mk',RED);qm.setAttribute('stroke',INK);qm.setAttribute('stroke-width',7);qm.setAttribute('paint-order','stroke');
const dict=G(fx);el('rect',{x:-330,y:-90,width:660,height:180,rx:14,fill:'#FFF8E4',stroke:INK,'stroke-width':6},dict);
T(dict,-300,-38,'Claus·tro·pho·bic',46,'mk',INK,'start');const defT=T(dict,-300,26,'',40,'hand',INK,'start');
const santa=G(fx);el('path',{d:'M-60 30 Q-40 -60 50 -50 Q30 -20 40 30 Z',fill:'#E0353B',stroke:INK,'stroke-width':6},santa);el('rect',{x:-72,y:22,width:124,height:30,rx:14,fill:'#fff',stroke:INK,'stroke-width':6},santa);el('circle',{cx:56,cy:-50,r:16,fill:'#fff',stroke:INK,'stroke-width':5},santa);
const ban=G(santa);el('circle',{cx:-6,cy:0,r:92,fill:'none',stroke:RED,'stroke-width':14},ban);ln(ban,-70,-64,58,64,14,RED);

EP.render=function(t){
  const grin=P(t,M.grin[0],.25);const g=V(t,M.grin[0],M.grin[1],.25,.01);
  let lp=lPose(t);const lm=talkMouth('LV',t);if(lp.name==='ask')lp.n[1]+=Math.sin(t*8)*10;if(lp.name==='scratch')lp.n[0]+=Math.sin(t*22)*8;
  placeStick(LV,lp,t,{});
  {const h=LV.head;const bl=blink(t,3.1,.4);h.eyes.setAttribute('transform',`translate(0 -4) scale(${1+.4*g} ${bl*(1+.4*g)}) translate(0 4)`);
    const o=Math.max(lm*24,g*14),mx=30;h.mouth.setAttribute('d',o<3?`M${mx-12} 30 Q${mx} 24 ${mx+12} 30`:`M${mx-14} 20 Q${mx} 18 ${mx+14} 20 Q${mx+12} ${24+o} ${mx} ${26+o} Q${mx-12} ${26+o} ${mx-14} 20 Z`);h.mouth.setAttribute('fill',o<3?'none':'#5A1E22')}
  let ap=aPose(t);const am=talkMouth('AS',t);if(ap.name==='tell')ap.n[1]+=Math.sin(t*8)*10;
  placeStick(AS,ap,t,{s:1+.25*eio(grin)});
  {const h=AS.head;op(h.normal,grin>.5?0:1);op(h.creep,grin>.5?1:0);h.glow.setAttribute('opacity',.45*g*(.8+.2*Math.sin(t*18)));
    h.skull.setAttribute('fill',grin>.5?'#E8E6EE':PAPER);
    const o=am*22,mx=-32;h.mouth.setAttribute('d',o<3?`M${mx-16} 28 Q${mx-2} 34 ${mx+16} 22`:`M${mx-16} 20 Q${mx} 18 ${mx+16} 20 Q${mx+14} ${24+o} ${mx} ${26+o} Q${mx-14} ${26+o} ${mx-16} 20 Z`);h.mouth.setAttribute('fill',o<3?'none':'#5A1E22')}
  camera([[eio(P(t,M.grin[0],1.2)),1.9,AS.Cs[0],AS.Cs[1]+40]],g*.35,t);
  if(g>0)tint.style.background=`rgba(255,106,26,${.14*g})`;
  // caller
  {const o=t<3.4?1-P(t,3.2,.2):0;op(scr,o);tr(scr,540,560,1);let a='';ID.m1.w.forEach(([w,ts])=>{if(t>=ts-.05)a+=(a?' ':'')+w});miT.textContent=a;op(miLk,t>2.3?1:0)}
  pop(word,540,800,t,1.64,3.3,-3,.9);
  pop(qm,LV.Cs[0]+150,LV.Cs[1]-40,t,4.86,6.5,10,.8);
  {const k=pop(dict,540,topOf('a1')-150,t,4.2,9.3,-2,.95);const d='(n.) hating Santa for no reason';defT.textContent=t<6.65?'= ???':d.slice(0,Math.floor(cl((t-6.65)/1.5)*d.length))}
  pop(santa,820,topOf('a1')-330,t,6.94,9.3,8,.8);op(ban,t>=7.37?1:0);
};
EP.init=function(){};
