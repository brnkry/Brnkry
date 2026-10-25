// Episode 02: "what is gaslight?" (bernard_io gets gaslit about what gaslighting is)
const EP={};
chair(250,1,'#4A90D9');chair(828,-1,'#D9534F');
const BE=makeStick('L','neat'),GZ=makeStick('R','lazy');
table();
// ---------- Bernard (left, facing right): cowlick, worried brows ----------
(()=>{const h=BE.head;
  h.skull=el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h);
  h.onion=G(h);el('path',{d:'M0 -78 C46 -60 72 -20 64 22 C56 60 24 70 0 70 C-24 70 -56 60 -64 22 C-72 -20 -46 -60 0 -78 Z',fill:'#E9C9D8',stroke:INK,'stroke-width':8},h.onion);
  ['M-30 -50 Q-50 0 -30 60','M30 -50 Q50 0 30 60','M0 -74 Q-8 0 0 68'].forEach(d=>pth(h.onion,d,{stroke:'#B07A96','stroke-width':4}));pth(h.onion,'M0 -78 q-6 -22 -20 -30 M0 -78 q6 -24 22 -28',{stroke:'#5E9E3A','stroke-width':6});
  h.fur=G(h);{let d='';for(let i=0;i<=36;i++){const a=i/36*Math.PI*2,rr=i%2?66:78;d+=(i?'L':'M')+(rr*Math.cos(a)).toFixed(1)+' '+(rr*Math.sin(a)*.94+6).toFixed(1)}
    el('circle',{cx:-46,cy:-58,r:18,fill:'#9CC9E8',stroke:INK,'stroke-width':5},h.fur);el('circle',{cx:46,cy:-58,r:18,fill:'#9CC9E8',stroke:INK,'stroke-width':5},h.fur);el('path',{d:d+'Z',fill:'#9CC9E8',stroke:INK,'stroke-width':6},h.fur);
    el('ellipse',{cx:-30,cy:30,rx:30,ry:22,fill:'#DCEEF8'},h.fur);el('ellipse',{cx:30,cy:30,rx:30,ry:22,fill:'#DCEEF8'},h.fur);pth(h.fur,'M-40 22 l-30 -6 M-40 30 l-30 4 M40 22 l30 -6 M40 30 l30 4',{'stroke-width':3})}
  h.hair=pth(h,'M-10 -60 q-6 -26 10 -30 q16 -2 10 16 q-6 12 -14 2',{'stroke-width':6});
  h.face=G(h);
  h.eyes=G(h.face);h.eA=G(h.eyes);el('circle',{cx:12,cy:-8,r:12,fill:'#fff',stroke:INK,'stroke-width':4},h.eA);h.pA=el('circle',{cx:16,cy:-8,r:5,fill:INK},h.eA);
  h.eB=G(h.eyes);el('circle',{cx:44,cy:-8,r:11,fill:'#fff',stroke:INK,'stroke-width':4},h.eB);h.pB=el('circle',{cx:47,cy:-8,r:5,fill:INK},h.eB);
  h.spiral=G(h.face);[[12,-8],[44,-8]].forEach(([x,y])=>{let d='';for(let i=0;i<=40;i++){const a=i*.45,r=1+i*.32;d+=(i?'L':'M')+(x+r*Math.cos(a)).toFixed(1)+' '+(y+r*Math.sin(a)).toFixed(1)}pth(h.spiral,d,{'stroke-width':3})});
  h.brA=ln(h.face,0,-30,22,-38,5);h.brB=ln(h.face,36,-36,58,-30,5);
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h.face);
  h.nose=el('circle',{cx:62,cy:10,r:14,fill:RED,stroke:INK,'stroke-width':4},h.face);
  h.sweat=el('path',{d:'M-40 -40 q-10 16 0 22 q10 -6 0 -22 Z',fill:'#9FD3F0',stroke:'#4C9CC9','stroke-width':3},h);
  h.tears=G(h);for(let i=0;i<6;i++)el('circle',{r:6,fill:'#9FD3F0',stroke:'#4C9CC9','stroke-width':2},h.tears);
  h.stare=G(h.face);el('circle',{cx:-22,cy:-6,r:8,fill:INK},h.stare);el('circle',{cx:22,cy:-6,r:8,fill:INK},h.stare);ln(h.stare,-36,-20,-10,-18,4);ln(h.stare,10,-18,36,-20,4);pth(h.stare,'M-8 18 q8 6 16 0',{'stroke-width':4});
  // phone (in the near hand)
  BE.phone=G(BE.prop);el('rect',{x:-16,y:-28,width:32,height:56,rx:7,fill:'#2B2B31',stroke:INK,'stroke-width':4},BE.phone);el('rect',{x:-11,y:-22,width:22,height:40,rx:3,fill:'#BFE3F5'},BE.phone);
})();
// ---------- Gheeze (right, facing left): backwards cap, shades, smirk ----------
(()=>{const h=GZ.head;
  el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h);
  h.cap=G(h);el('path',{d:'M-60 -18 A60 60 0 0 1 60 -18 Z',fill:RED,stroke:INK,'stroke-width':7,'stroke-linejoin':'round'},h.cap);el('path',{d:'M58 -24 h28 q8 0 4 8 h-32 Z',fill:RED,stroke:INK,'stroke-width':6,'stroke-linejoin':'round'},h.cap);el('circle',{cx:0,cy:-60,r:6,fill:RED,stroke:INK,'stroke-width':3},h.cap);
  h.face=G(h);
  h.eyes=G(h.face);pth(h.eyes,'M-60 -8 q10 -8 20 0 M-32 -8 q10 -8 20 0',{'stroke-width':5});
  h.shades=G(h.face);el('rect',{x:-66,y:-22,width:30,height:22,rx:6,fill:INK},h.shades);el('rect',{x:-30,y:-22,width:30,height:22,rx:6,fill:INK},h.shades);ln(h.shades,-36,-16,-30,-16,5);ln(h.shades,0,-16,40,-22,5);
  pth(h.shades,'M-58 -16 l8 -2 M-22 -16 l8 -2',{stroke:'#fff','stroke-width':3});
  h.brow=ln(h.face,-62,-34,-36,-40,5);
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h.face);
  // cup with straw (in the near hand for the sip)
  GZ.cup=G(GZ.prop);el('path',{d:'M-18 -30 h36 l-5 52 h-26 Z',fill:'#fff',stroke:INK,'stroke-width':5,'stroke-linejoin':'round'},GZ.cup);el('rect',{x:-20,y:-36,width:40,height:8,rx:3,fill:RED,stroke:INK,'stroke-width':4},GZ.cup);ln(GZ.cup,4,-36,-14,-70,5,INK);
})();

// ---------- poses ----------
const BPOSE={idle:{lean:2,n:[70,135],f:[50,140]},ask:{lean:4,tilt:8,n:[115,0],f:[50,140]},shake:{lean:0,n:[70,135],f:[50,140]},
  shrug:{lean:-2,tilt:-6,n:[120,-40],f:[-80,-40]},phone:{lean:6,tilt:10,n:[80,-20],f:[50,140]},crazy:{lean:-6,n:[30,-150],f:[-10,-150]},
  stand:{lean:14,n:[150,40],f:[140,50]},slump:{lean:-14,tilt:10,n:[60,140],f:[40,150]},stare:{lean:0,n:[70,135],f:[50,140]}};
const BKEYS=[[0,'ask'],[2.3,'idle'],[4.7,'shake'],[6.0,'idle'],[10.9,'shrug'],[13.0,'ask'],[15.4,'idle'],[20.6,'phone'],[29.2,'crazy'],[35.0,'idle'],[40.1,'stand'],[47.3,'slump'],[54.8,'stare']];
const GPOSE={chill:{lean:-14,n:[-25,-120],f:[-45,-112]},smug:{lean:-6,tilt:-6,n:[110,-10],f:[-45,-112]},sip:{lean:-8,n:[48,-58],f:[-45,-112]},
  point:{lean:6,n:[160,-30],f:[-45,-112]},laugh:{lean:-22,tilt:-14,n:[60,40],f:[40,60]}};
const GKEYS=[[0,'chill'],[2.4,'smug'],[4.2,'chill'],[7.4,'point'],[8.8,'sip'],[10.8,'chill'],[15.8,'smug'],[19.9,'chill'],[25.7,'smug'],[29.0,'chill'],[36.2,'point'],[38.2,'chill'],[48.2,'laugh'],[54.8,'chill']];
const bPose=poser(BPOSE,BKEYS),gPose=poser(GPOSE,GKEYS);

// ---------- stickers ----------
const lamp=G(fx);{ln(lamp,0,0,0,170,10);ln(lamp,-34,170,34,170,10);el('path',{d:'M-34 -70 h68 l-10 70 h-48 Z',fill:'#FFF8D8',stroke:INK,'stroke-width':7,'stroke-linejoin':'round'},lamp);
  el('path',{d:'M-44 -70 L0 -104 L44 -70 Z',fill:'#3A3A40',stroke:INK,'stroke-width':6,'stroke-linejoin':'round'},lamp);}
const flame=el('path',{d:'',fill:'#FFB000',stroke:'#E0353B','stroke-width':4},lamp);const lampGlow=el('circle',{cx:0,cy:-36,r:70,fill:'#FFE45C',opacity:0},lamp);lamp.insertBefore(lampGlow,lamp.firstChild);
const gasT=badge(fx,'GASLIGHT?',PAPER,BLUE,50,300,80);
const wink=G(fx);el('circle',{r:56,fill:'#F2C230',stroke:INK,'stroke-width':6},wink);pth(wink,'M-28 -12 q10 -8 20 0',{'stroke-width':6});el('circle',{cx:20,cy:-12,r:7,fill:INK},wink);pth(wink,'M-24 22 q20 12 40 -6',{'stroke-width':6});T(wink,0,96,'you know 😏',36,'hand');
const xB=badge(fx,'✗ I DO NOT',PAPER,RED,50,330,84),okB=badge(fx,'✓ YES YOU DO',PAPER,GREEN,50,380,84);
const cloud=G(fx);el('path',{d:'M-160 40 q-40 -60 20 -80 q20 -60 90 -40 q50 -50 110 0 q70 -10 70 50 q40 50 -20 80 q-30 40 -100 20 q-60 30 -110 0 q-70 10 -60 -30 Z',fill:'#fff',stroke:INK,'stroke-width':6},cloud);
const weed=G(cloud);{for(let i=0;i<5;i++)el('circle',{cx:Math.cos(i*1.3)*10,cy:Math.sin(i*1.3)*10,r:24-i*2,fill:'none',stroke:'#A07A3A','stroke-width':4},weed)}T(cloud,0,-50,'brain.exe',30,'hand',GREY);
const mem=G(fx);el('rect',{x:-240,y:-60,width:480,height:120,rx:16,fill:'#fff',stroke:INK,'stroke-width':6},mem);const memT=T(mem,-210,-18,'MEMORY.EXE',34,'mk',INK,'start');el('rect',{x:-210,y:6,width:420,height:30,rx:8,fill:'#EEE',stroke:INK,'stroke-width':4},mem);
const memBar=el('rect',{x:-210,y:6,width:0,height:30,rx:8,fill:GREEN},mem);const memErr=T(mem,170,-16,'ERROR',34,'mk',RED);
const search=G(fx);el('rect',{x:-330,y:-46,width:660,height:92,rx:46,fill:'#fff',stroke:INK,'stroke-width':6},search);el('circle',{cx:-280,cy:-6,r:16,fill:'none',stroke:INK,'stroke-width':5},search);ln(search,-268,6,-256,18,5);
const sTxt=T(search,-240,14,'',40,'hand',INK,'start');const spin=el('circle',{cx:280,cy:0,r:20,fill:'none',stroke:BLUE,'stroke-width':6,'stroke-dasharray':'60 70'},search);
const result=G(fx);el('rect',{x:-300,y:-60,width:600,height:120,rx:14,fill:'#fff',stroke:INK,'stroke-width':5},result);T(result,-270,-14,'Top result:',30,'hand',GREY,'start');T(result,-270,32,'"you know what it is"',44,'hand',BLUE,'start');
const swirl=G(fx);[0,1,2,3].forEach(i=>T(swirl,0,0,['?','!','?','!?'][i],60,'mk',[RED,INK,BLUE,RED][i]));
const clown=badge(fx,'🤡',PAPER,INK,80,140,120);
const help=badge(fx,'HELP!!',RED,'#fff',72,300,110);
// call-in screen (the three listeners)
const scr=G(fx);el('rect',{x:-380,y:-230,width:760,height:470,rx:24,fill:'#22202B',stroke:INK,'stroke-width':8},scr);el('rect',{x:-380,y:-230,width:760,height:70,rx:24,fill:RED,stroke:INK,'stroke-width':8},scr);
T(scr,0,-180,'📞 LIVE CALLERS',42,'mk','#fff');
const callers=['c1','c2','c3'].map((id,i)=>{const g=G(scr,{transform:`translate(-340 ${-110+i*118})`});const u=USERS[ID[id].who];
  el('circle',{cx:30,cy:30,r:26,fill:u.color,stroke:'#fff','stroke-width':4},g);T(g,74,18,u.name,30,'hand','#A9A6B5','start');const tx=T(g,74,60,'',44,'hand','#fff','start');
  const lk=T(g,670,44,'♥ '+ID[id].likes,30,'hand',RED,'end');return {g,tx,lk,l:ID[id]}});

// ---------- per frame ----------
function flamePath(sz,t){const w=12+sz*14,hh=18+sz*40,j=Math.sin(t*14)*3*sz;return `M0 -12 C${-w} ${-18-hh*.3} ${-w*.4+j} ${-20-hh*.8} 0 ${-24-hh} C${w*.4+j} ${-20-hh*.8} ${w} ${-18-hh*.3} 0 -12 Z`}
EP.render=function(t){
  const sip=V(t,M.sip[0],M.sip[1],.15,.18),onion=V(t,M.onion[0],M.onion[1],.12,.15),stare=P(t,M.stare[0],.2);
  // ----- Bernard -----
  let bp=bPose(t);const bm=talkMouth('B',t);
  if(bp.name==='ask'||bp.name==='stand')bp.n[1]+=Math.sin(t*8)*10;
  if(bp.name==='crazy'){bp.n[0]+=Math.sin(t*20)*14;bp.f[0]+=Math.cos(t*20)*14}
  const shake=bp.name==='shake'?Math.sin(t*28)*14*(1-P(t,5.6,.3)):0;
  const rise=-60*eio(V(t,40.1,47.3,.35,.4));
  placeStick(BE,bp,t,{rot:shake,rise,s:1+.25*onion+.12*stare});
  {const h=BE.head;const crazy=V(t,29.3,35.0,.2,.3);const isOnion=onion>.4,isFur=stare>.5;
    op(h.onion,isOnion?1:0);op(h.fur,isFur?1:0);op(h.skull,isOnion||isFur?0:1);op(h.hair,isOnion||isFur?0:1);
    op(h.eyes,crazy>.5||isFur?0:1);op(h.spiral,crazy>.5&&!isFur?1:0);op(h.stare,isFur?1:0);
    const look=Math.sin(t*.8)*3;h.pA.setAttribute('cx',16+look);h.pB.setAttribute('cx',47+look);
    const bl=blink(t,3.4,.6);h.eyes.setAttribute('transform',`translate(0 -8) scale(1 ${bl}) translate(0 8)`);
    h.spiral.setAttribute('transform',`rotate(${t*200} 28 -8)`);
    const worry=Math.max(V(t,4.7,6.2),V(t,10.9,15.4),V(t,16,20.5),crazy,V(t,36.2,38.3),V(t,47.3,54.8));
    h.brA.setAttribute('y1',-30-8*worry);h.brA.setAttribute('y2',-38+6*worry);h.brB.setAttribute('y1',-36+6*worry);h.brB.setAttribute('y2',-30-8*worry);
    op(h.brA,isFur?0:1);op(h.brB,isFur?0:1);
    const o=Math.max(bm*28,crazy*6),mx=34;
    if(o<3){h.mouth.setAttribute('fill','none');h.mouth.setAttribute('d',`M${mx-16} ${30} Q${mx} ${24+worry*10} ${mx+16} 30`)}
    else{h.mouth.setAttribute('fill','#5A1E22');h.mouth.setAttribute('d',`M${mx-18} 24 Q${mx} 22 ${mx+18} 24 Q${mx+16} ${28+o} ${mx} ${30+o} Q${mx-16} ${30+o} ${mx-18} 24 Z`)}
    op(h.mouth,isFur?0:1);
    op(h.nose,t>=37.38&&t<M.stare[0]&&!isOnion?1:0);tr(h.nose,0,0,back(P(t,37.38,.3)));
    op(h.sweat,Math.max(V(t,11,15.3),V(t,20.6,25),V(t,40.5,47))>.3?1:0);
    op(h.tears,onion>0?1:0);[...h.tears.children].forEach((c,i)=>{const ph=(t*1.6+i/6)%1;c.setAttribute('cx',(i%2?40:-30)+(i%2?1:-1)*ph*30);c.setAttribute('cy',-4+ph*90)});
    // phone while googling
    const ph=bp.name==='phone'?bp.k:0;op(BE.phone,ph);tr(BE.phone,BE.Wn[0]+8,BE.Wn[1]-20,1,-10)}
  // ----- Gheeze -----
  let gp=gPose(t);const gm=talkMouth('G',t);
  if(gp.name==='point'||gp.name==='smug')gp.n[1]+=Math.sin(t*7)*10;
  if(gp.name==='laugh'){gp.lean+=Math.sin(t*18)*4}
  placeStick(GZ,gp,t,{});
  {const h=GZ.head;const slide=eio(Math.max(V(t,M.sip[0]+.2,M.sip[1],.3,.2),V(t,48.2,54.6,.3,.3)));tr(h.shades,0,22*slide);
    h.brow.setAttribute('transform',`translate(0 ${-6*Math.max(V(t,2.4,4.2),V(t,15.9,19.9),V(t,25.8,28.9))*(Math.sin(t*16)>0?1:0)})`);
    const o=Math.max(gm*24,V(t,48.2,54.6)*18);const mx=-32;
    if(o<3){h.mouth.setAttribute('fill','none');h.mouth.setAttribute('d',`M${mx-18} 28 Q${mx-2} 34 ${mx+18} 18`)}
    else{h.mouth.setAttribute('fill','#5A1E22');h.mouth.setAttribute('d',`M${mx-20} 24 Q${mx} 18 ${mx+20} 16 Q${mx+16} ${24+o} ${mx} ${28+o} Q${mx-16} ${28+o} ${mx-20} 24 Z`)}
    const hold=gp.name==='sip'?gp.k:0;op(GZ.cup,hold);tr(GZ.cup,GZ.Wn[0]-6,GZ.Wn[1]-26,1.4,8)}
  // ----- camera -----
  const crazyCam=V(t,30.1,34.6,.3,.3);
  camera([[eio(sip),1.7,GZ.Cs[0],GZ.Cs[1]+60],[eio(onion),1.8,BE.Cs[0],BE.Cs[1]+40],[eio(P(t,M.stare[0],2.5)),1.9,BE.Cs[0],BE.Cs[1]]],P(t,40.26,.08)*(1-P(t,40.6,.3))+crazyCam*.25,t);
  if(crazyCam>0)cam.style.transform+=` rotate(${Math.sin(t*2.5)*2.5*crazyCam}deg)`;
  if(onion>0)tint.style.background=`rgba(233,201,216,${.25*onion})`;if(stare>0)tint.style.background=`rgba(156,201,232,${.12*stare})`;
  // ----- stickers -----
  // gas lamp: lights at "gaslight" and burns brighter after every gaslighting reply
  {const o=t>=.81&&t<M.stare[0]?1:0;op(lamp,o*(t<M.onion[0]||t>M.onion[1]?1:0));tr(lamp,170,470,back(P(t,.81,.35))*.9);
    const lv=[2.54,7.64,15.97,25.89,36.34].filter(x=>t>=x).length;const sz=.3+lv*.32+.1*Math.sin(t*9);flame.setAttribute('d',flamePath(sz,t));lampGlow.setAttribute('opacity',.08+lv*.08);lampGlow.setAttribute('r',50+lv*16)}
  pop(gasT,560,topOf('b1')-80,t,.81,2.25,-4);
  pop(wink,620,topOf('g1')-100,t,2.6,3.95,6);
  pop(xB,560,topOf('b2')-80,t,5.4,8.9,-4);pop(okB,600,topOf('g2')-70,t,7.64,8.9,5);
  {const o=t>=11.6&&t<15.4?1-P(t,15.2,.2):0;op(cloud,o);tr(cloud,600,topOf('b3')-120,back(P(t,11.6,.3))*.85);weed.setAttribute('transform',`translate(${((t-11.6)*160)%320-160} ${30-Math.abs(Math.sin(t*6))*20}) rotate(${t*300})`)}
  {const o=t>=17.5&&t<20.4?1-P(t,20.2,.2):0;op(mem,o);tr(mem,600,topOf('g3')-90,back(P(t,17.5,.3))*.9);const k=P(t,17.7,1.2);memBar.setAttribute('width',420*Math.min(k,.85));memBar.setAttribute('fill',t>19.06?RED:GREEN);op(memErr,t>19.06?1:0)}
  {const o=t>=22.6&&t<29.0?1-P(t,28.8,.2):0;op(search,o);const y=t<25.5?topOf('b4')-80:topOf('g4')-150;tr(search,560,y,back(P(t,22.6,.3))*.82);
    const q='what is gaslight';sTxt.textContent=q.slice(0,Math.floor(cl((t-22.74)/.9)*q.length))+(Math.floor(t*3)%2?'|':'');op(spin,t>26.4&&t<27.8?1:0);spin.setAttribute('transform',`rotate(${t*400} 280 0)`)}
  pop(result,560,topOf('g4')-45,t,27.83,28.9,-2,.82);
  {const o=V(t,29.4,35.0);op(swirl,o);[...swirl.children].forEach((c,i)=>{const a=t*3+i*Math.PI/2;c.setAttribute('x',BE.Cs[0]+Math.cos(a)*120);c.setAttribute('y',BE.Cs[1]-150+Math.sin(a)*40)})}
  pop(clown,700,topOf('g5')-90,t,37.38,37.95,8);
  {const k=pop(help,560,topOf('b6')-90,t,44.04,47.6,-3);if(t>44&&t<47.6)help.setAttribute('transform',help.getAttribute('transform')+` rotate(${Math.sin(t*30)*4})`)}
  // call-in screen
  {const o=t>=47.6&&t<M.stare[0]+.2?1-P(t,M.stare[0],.2):0;op(scr,o);tr(scr,540,620,back(P(t,47.6,.35))*.95);
    callers.forEach(({g,tx,lk,l})=>{const s=l.w[0][1]-.2;op(g,t>=s?eo(P(t,s,.25)):0);let txt='';l.w.forEach(([w,ts])=>{if(t>=ts-.05)txt+=(txt?' ':'')+w});tx.textContent=txt;op(lk,t>l.end-.2?1:0)})}
};
EP.init=function(){};
