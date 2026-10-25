// Episode 05: "Tell me a color and I'll guess it" -> the AI says the answer out loud -> "Red" -> "How did you guess it?"
const EP={};
chair(250,1,'#2C8CD6');chair(828,-1,'#7B6BE0');
const HU=makeStick('L','neat'),RB=makeStick('R','neat');
table();
// ---------- human (left): hoodie hood line, plain face ----------
(()=>{const h=HU.head;el('path',{d:'M-74 40 Q-84 -78 0 -84 Q80 -80 74 30',fill:'#2C8CD6',stroke:INK,'stroke-width':6},h);
  el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h);el('path',{d:'M-58 -22 Q-50 -64 4 -64 Q50 -62 60 -24 Q24 -40 -8 -34 Q-36 -30 -58 -22 Z',fill:'#3B2A20',stroke:INK,'stroke-width':4},h);
  h.eyes=G(h);el('circle',{cx:14,cy:-4,r:6,fill:INK},h.eyes);el('circle',{cx:44,cy:-4,r:6,fill:INK},h.eyes);
  h.brows=G(h);ln(h.brows,4,-22,24,-24,5);ln(h.brows,36,-24,54,-22,5);
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h);
  h.front=G(h);el('circle',{cx:-18,cy:0,r:7,fill:INK},h.front);el('circle',{cx:18,cy:0,r:7,fill:INK},h.front);ln(h.front,-28,-20,-8,-16,5);ln(h.front,8,-16,28,-20,5);pth(h.front,'M-14 30 Q0 24 14 30',{'stroke-width':5});
})();
// ---------- Gemini (right): head is the blue-violet four-point sparkle, face drawn in white on it ----------
(()=>{const h=RB.head;const d=el('defs',{},h);const gr=el('linearGradient',{id:'gem',x1:0,y1:0,x2:1,y2:1},d);
  [[0,'#4285F4'],[.55,'#9B72CB'],[1,'#D96570']].forEach(([o,c])=>el('stop',{offset:o,'stop-color':c},gr));
  h.star=el('path',{d:'M0 -96 C10 -30 30 -10 96 0 C30 10 10 30 0 96 C-10 30 -30 10 -96 0 C-30 -10 -10 -30 0 -96 Z',fill:'url(#gem)',stroke:INK,'stroke-width':7,'stroke-linejoin':'round'},h);
  const face=G(h);h.face=face;const g=()=>{const e=G(face);e.style.display='none';return e};const W_='#fff';
  h.F={};h.F.neutral=g();[-16,16].forEach(x=>el('ellipse',{cx:x,cy:-8,rx:6,ry:10,fill:W_},h.F.neutral));
  h.F.happy=g();pth(h.F.happy,'M-24 -4 l8 -12 l8 12 M8 -4 l8 -12 l8 12',{stroke:W_,'stroke-width':5});
  h.F.think=g();h.spin=el('circle',{r:16,fill:'none',stroke:W_,'stroke-width':5,'stroke-dasharray':'50 50'},h.F.think);
  h.F.red=g();el('circle',{r:30,fill:'#E0353B',stroke:W_,'stroke-width':4},h.F.red);el('text',{x:0,y:8,'text-anchor':'middle','font-size':22,class:'mk',fill:'#fff'},h.F.red).textContent='RED';
  h.F.wink=g();pth(h.F.wink,'M-24 -8 h14',{stroke:W_,'stroke-width':5});el('ellipse',{cx:16,cy:-8,rx:6,ry:10,fill:W_},h.F.wink);
  h.F.shock=g();el('circle',{cx:-16,cy:-8,r:10,fill:'none',stroke:W_,'stroke-width':5},h.F.shock);el('circle',{cx:16,cy:-8,r:10,fill:'none',stroke:W_,'stroke-width':5},h.F.shock);
  h.mouth=el('rect',{x:-12,y:14,width:24,height:5,rx:2.5,fill:W_},h);
})();

const HPOSE={ask:{lean:4,tilt:6,n:[115,0],f:[50,140]},idle:{lean:2,n:[70,135],f:[50,140]},wait:{lean:8,tilt:-6,n:[60,60],f:[40,70]},
  psychic:{lean:4,n:[46,-98],f:[50,140]},kid:{lean:4,n:[90,120],f:[80,126]}};
const HKEYS=[[0,'ask'],[1.6,'wait'],[4.5,'idle'],[6.3,'psychic'],[7.3,'idle'],[10.9,'kid']];
const RPOSE={idle:{lean:2,n:[70,135],f:[60,140]},talk:{lean:8,n:[125,-10],f:[60,140]},hush:{lean:6,n:[56,-60],f:[60,140]},cheer:{lean:-4,n:[110,-140],f:[-60,-140]}};
const RKEYS=[[0,'idle'],[1.6,'hush'],[2.6,'talk'],[5.8,'idle'],[7.9,'cheer'],[11.0,'talk']];
const hPose=poser(HPOSE,HKEYS,.25),rPose=poser(RPOSE,RKEYS,.22);

// ---------- stickers ----------
const pal=G(fx);el('path',{d:'M-80 0 C-80 -60 20 -76 70 -40 C110 -10 70 20 40 10 C10 0 20 40 0 50 C-40 70 -80 40 -80 0 Z',fill:'#F3E2C4',stroke:INK,'stroke-width':6},pal);
[['#E0353B',-40,-24],['#2463D9',0,-40],['#7AC943',36,-24],['#F2C230',-50,16]].forEach(([c,x,y])=>el('circle',{cx:x,cy:y,r:12,fill:c,stroke:INK,'stroke-width':3},pal));T(pal,110,20,'?',90,'mk',INK);
const secret=G(fx);el('rect',{x:-200,y:-70,width:400,height:140,rx:10,fill:'#F3E2C4',stroke:INK,'stroke-width':6},secret);T(secret,0,-20,'TOP SECRET 🤫',40,'mk',INK);
const secRed=T(secret,0,46,'answer: RED',44,'mk',RED);const stamp=badge(secret,'LEAKED',PAPER,RED,40,200,64);
const ball=G(fx);el('circle',{cx:0,cy:-10,r:60,fill:'#C9B8F5',stroke:INK,'stroke-width':6},ball);el('rect',{x:-50,y:44,width:100,height:24,rx:8,fill:'#7A4A2A',stroke:INK,'stroke-width':5},ball);const ballT=T(ball,0,110,'psychic powers',34,'hand',INK);
const conf=G(fx);for(let i=0;i<26;i++)el('rect',{x:-6,y:-10,width:12,height:20,rx:3,fill:['#E0353B','#2463D9','#F2C230','#7AC943','#FF3DA5'][i%5]},conf);
const acc=badge(fx,'🎉 CORRECT! 100% ACCURACY',PAPER,GREEN,40,560,86);
const iq=badge(fx,'IQ: ∞',PAPER,'#7B6BE0',54,220,86);

EP.render=function(t){
  const stare=P(t,M.stare[0],.25);
  // ----- human -----
  let hp=hPose(t);const hm=talkMouth('H',t);if(hp.name==='ask')hp.n[1]+=Math.sin(t*8)*10;
  placeStick(HU,hp,t,{});
  {const h=HU.head;const front=stare>.5;op(h.eyes,front?0:1);op(h.brows,front?0:1);op(h.mouth,front?0:1);op(h.front,front?1:0);
    const bl=blink(t,3.2,.3);h.eyes.setAttribute('transform',`translate(0 -4) scale(1 ${bl}) translate(0 4)`);
    const flat=V(t,2.7,6.3);tr(h.brows,0,4*flat);
    const o=hm*24,mx=32;h.mouth.setAttribute('d',o<3?(flat>.5?`M${mx-14} 30 H${mx+14}`:`M${mx-16} 26 Q${mx} 36 ${mx+16} 26`):`M${mx-18} 22 Q${mx} 20 ${mx+18} 22 Q${mx+16} ${26+o} ${mx} ${28+o} Q${mx-16} ${28+o} ${mx-18} 22 Z`);h.mouth.setAttribute('fill',o<3?'none':'#5A1E22')}
  // ----- robot -----
  let rp=rPose(t);const rm=talkMouth('A',t);if(rp.name==='talk')rp.n[1]+=Math.sin(t*8)*10;if(rp.name==='cheer'){rp.n[1]+=Math.sin(t*14)*16;rp.f[1]+=Math.cos(t*14)*16}
  placeStick(RB,rp,t,{rot:rp.name==='cheer'?Math.sin(t*10)*6:0});
  {const h=RB.head;let f='neutral';
    if(t>=1.5&&t<2.7)f='think';else if(t>=2.7&&t<4.3)f='happy';else if(t>=4.3&&t<4.84)f='red';else if(t>=4.84&&t<6.6)f='wink';else if(t>=6.6&&t<8.1)f='shock';else if(t>=8.1&&t<11.0)f='happy';
    for(const k in h.F)h.F[k].style.display=k===f?'':'none';h.spin.setAttribute('transform',`rotate(${t*360})`);
    h.star.setAttribute('fill',f==='red'&&Math.floor(t*8)%2?'#E0353B':'url(#gem)');
    h.mouth.setAttribute('height',6+rm*20);h.mouth.setAttribute('y',24-rm*6);op(h.mouth,f==='red'?0:1);
    h.star.setAttribute('transform',`rotate(${Math.sin(t*1.5)*6})`)}
  camera([[eio(P(t,M.stare[0],2.5)),1.4,540,1060]],0,t);
  // ----- stickers -----
  pop(pal,620,topOf('h1')-100,t,.37,1.5,-6);
  {const k=pop(secret,560,topOf('a1')-110,t,3.4,6.4,-3);secRed.style.opacity=t>=4.42?1:0;op(stamp,t>=4.6&&t<6.65?1:0);tr(stamp,120,-60,back(P(t,4.6,.25))*1,12)}
  {pop(ball,HU.Cs[0]+150,HU.Cs[1]-110,t,6.4,7.9,0,.9)}
  {const o=t>=8.2&&t<11.0?1-P(t,10.8,.2):0;op(conf,o);[...conf.children].forEach((c,i)=>{const a=-Math.PI/2+(i/26-.5)*2.4;const k=P(t,8.2,1.4);const d=60+k*(380+i%5*40);c.setAttribute('transform',`translate(${RB.Cs[0]-120+Math.cos(a)*d} ${RB.Cs[1]-120+Math.sin(a)*d+k*k*300}) rotate(${t*400+i*40})`)})}
  pop(acc,540,topOf('a2')-90,t,8.6,10.9,-3,.95);pop(iq,820,topOf('a2')-190,t,9.5,10.9,8);
};
EP.init=function(){};
