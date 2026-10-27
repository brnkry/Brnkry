// Episode 09, "GTA Radio" #1: the Non-Stop-Pop ident (DJ, left) and the host's horror-screenplay joke (right).
// The hanging neon sign shows GTA RADIO (window.SERIES). The song at the end: everyone vibes.
const EP={};
chair(250,1,'#FF3DA5');chair(828,-1,'#3DE6FF');
const DJ=makeStick('L','wide'),HO=makeStick('R','crossed');
table();
// ---------- DJ (left): headphones, shades, backwards cap ----------
(()=>{const h=DJ.head;el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h);
  el('path',{d:'M-60 -18 A60 60 0 0 1 60 -18 Z',fill:'#FF3DA5',stroke:INK,'stroke-width':6,'stroke-linejoin':'round'},h);el('path',{d:'M-58 -24 h-28 q-8 0 -4 8 h32 Z',fill:'#FF3DA5',stroke:INK,'stroke-width':5},h);
  pth(h,'M-66 6 Q-70 -84 0 -86 Q70 -84 66 6',{'stroke-width':8});el('rect',{x:-80,y:-14,width:22,height:40,rx:8,fill:'#2B2B31',stroke:INK,'stroke-width':4},h);el('rect',{x:58,y:-14,width:22,height:40,rx:8,fill:'#2B2B31',stroke:INK,'stroke-width':4},h);
  h.shades=G(h);el('rect',{x:2,y:-20,width:30,height:20,rx:6,fill:INK},h.shades);el('rect',{x:36,y:-20,width:28,height:20,rx:6,fill:INK},h.shades);ln(h.shades,32,-14,36,-14,4);
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h);
  h.scared=G(h);el('circle',{cx:16,cy:-10,r:12,fill:'#fff',stroke:INK,'stroke-width':4},h.scared);el('circle',{cx:46,cy:-10,r:10,fill:'#fff',stroke:INK,'stroke-width':4},h.scared);el('circle',{cx:16,cy:-10,r:3,fill:INK},h.scared);el('circle',{cx:46,cy:-10,r:3,fill:INK},h.scared)})();
// ---------- host (right): big blonde hair, earrings ----------
(()=>{const h=HO.head;el('path',{d:'M-80 60 Q-96 -90 0 -92 Q96 -90 80 60 Q60 20 40 40 Q0 -10 -40 40 Q-60 20 -80 60 Z',fill:'#F2C230',stroke:INK,'stroke-width':6},h);
  el('circle',{r:58,fill:PAPER,stroke:INK,'stroke-width':8},h);el('path',{d:'M-58 -10 Q-56 -66 6 -66 Q54 -60 58 -14 Q20 -46 -20 -30 Q-40 -22 -58 -10 Z',fill:'#F2C230',stroke:INK,'stroke-width':5},h);
  el('circle',{cx:-58,cy:24,r:7,fill:'#3DE6FF',stroke:INK,'stroke-width':3},h);
  h.eyes=G(h);[-16,-44].forEach(x=>{el('circle',{cx:x,cy:-2,r:7,fill:INK},h.eyes);ln(h.eyes,x-6,-12,x-14,-18,3);ln(h.eyes,x+2,-13,x,-21,3)});
  h.mouth=el('path',{fill:'#C2394A',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h)})();

const DPOSE={hype:{lean:6,n:[120,-90],f:[-60,-100]},idle:{lean:-8,n:[70,130],f:[40,140]},listen:{lean:4,tilt:8,n:[60,60],f:[40,70]},scream:{lean:-26,tilt:-8,n:[60,-120],f:[30,-120]},dance:{lean:0,n:[110,-120],f:[-70,-120]}};
const DKEYS=[[0,'hype'],[4.7,'idle'],[7.0,'listen'],[12.4,'scream'],[13.3,'dance']];
const HPOSE={idle:{lean:2,n:[70,135],f:[60,140]},tell:{lean:8,n:[125,-10],f:[60,140]},phone:{lean:6,n:[52,-60],f:[60,140]},dance:{lean:0,n:[110,-120],f:[-70,-120]}};
const HKEYS=[[0,'idle'],[5.0,'tell'],[8.9,'phone'],[10.0,'tell'],[13.3,'dance']];
const dPose=poser(DPOSE,DKEYS,.25),hPose=poser(HPOSE,HKEYS,.25);

// ---------- stickers: what the lines say ----------
const dial=G(fx);el('rect',{x:-230,y:-60,width:460,height:120,rx:18,fill:'#22202B',stroke:INK,'stroke-width':6},dial);
for(let i=0;i<=20;i++)ln(dial,-190+i*19,-20,-190+i*19,i%5?-6:4,3,'#7D7A8C');const needle=ln(dial,0,-34,0,20,6,'#FF3DA5');const freq=T(dial,0,48,'',34,'mk','#3DE6FF');
const nsp=G(fx);['NON','STOP','POP!'].forEach((w,i)=>{const b=badge(nsp,w,['#FF3DA5','#3DE6FF','#C6FF3D'][i],INK,54,170+(i===2?20:0),84);b.setAttribute('transform',`translate(${(i-1)*200} 0)`)});
const script=G(fx);el('rect',{x:-150,y:-110,width:300,height:220,rx:6,fill:'#fff',stroke:INK,'stroke-width':6},script);T(script,0,-62,'HORROR',44,'mk',RED);T(script,0,-24,'a screenplay',30,'hand',GREY);
['FADE IN:','INT. HOUSE - NIGHT'].forEach((s,i)=>T(script,-120,24+i*36,s,26,'hand',INK,'start'));
const phone=G(fx);el('rect',{x:-70,y:-120,width:140,height:240,rx:20,fill:'#2B2B31',stroke:INK,'stroke-width':6},phone);const scrn=el('rect',{x:-56,y:-100,width:112,height:196,rx:10,fill:'#BFE3F5'},phone);
const callT=T(phone,0,-40,'',30,'mk',INK);const callS=T(phone,0,-6,'',24,'hand',GREY);const waves=G(phone);[0,1].forEach(i=>{pth(waves,`M${80+i*18} -40 q14 40 0 80`,{'stroke-width':5});pth(waves,`M${-80-i*18} -40 q-14 40 0 80`,{'stroke-width':5})});
const scream=badge(fx,'😱 AAAAAH!',PAPER,RED,56,330,92);
const notes=G(fx);for(let i=0;i<8;i++)T(notes,0,0,['♪','♫'][i%2],70,'mk',['#FF3DA5','#3DE6FF','#C6FF3D','#B76BFF'][i%4]);

EP.render=function(t){
  const song=P(t,window.SONG,.3);
  // ----- DJ -----
  let dp=dPose(t);const dm=talkMouth('D',t);
  if(dp.name==='hype'||dp.name==='dance'){dp.n[1]+=Math.sin(t*9)*18;dp.f[1]+=Math.cos(t*9)*18;dp.lean+=Math.sin(t*4.5)*6}
  placeStick(DJ,dp,t,{});
  {const h=DJ.head;const sc=V(t,12.3,13.6,.08,.3);op(h.shades,sc>.5?0:1);op(h.scared,sc>.5?1:0);
    const o=Math.max(dm*28,sc*34),mx=32;h.mouth.setAttribute('d',o<3?`M${mx-18} 22 Q${mx} 38 ${mx+18} 22`:`M${mx-18} 20 Q${mx} 18 ${mx+18} 20 Q${mx+16} ${24+o} ${mx} ${26+o} Q${mx-16} ${26+o} ${mx-18} 20 Z`);h.mouth.setAttribute('fill',o<3?'none':'#5A1E22')}
  // ----- host -----
  let hp=hPose(t);const hm=talkMouth('H',t);if(hp.name==='tell')hp.n[1]+=Math.sin(t*7)*10;if(hp.name==='dance'){hp.n[1]+=Math.sin(t*9+1)*18;hp.f[1]+=Math.cos(t*9+1)*18;hp.lean+=Math.sin(t*4.5+1)*6}
  placeStick(HO,hp,t,{});
  {const h=HO.head;const bl=blink(t,3.4,.9);h.eyes.setAttribute('transform',`translate(0 -2) scale(1 ${bl}) translate(0 2)`);
    const o=hm*24,mx=-30;h.mouth.setAttribute('d',o<3?`M${mx-16} 24 Q${mx} 36 ${mx+16} 24`:`M${mx-16} 20 Q${mx} 18 ${mx+16} 20 Q${mx+14} ${24+o} ${mx} ${26+o} Q${mx-14} ${26+o} ${mx-16} 20 Z`);h.mouth.setAttribute('fill',o<3?'none':'#C2394A')}
  camera([],V(t,12.34,13.3,.05,.3)*.5,t);
  if(t>12.3&&t<13.4)tint.style.background=`rgba(224,53,59,${.18*V(t,12.34,13.3,.05,.2)})`;
  if(song>0)tint.style.background=`rgba(${Math.floor(t*4)%2?'255,61,165':'61,230,255'},${.08*song})`;
  // ----- stickers -----
  {const k=pop(dial,540,topOf('d1')-100,t,.6,2.6,-2,.95);const x=lerp(-190,190,eo(P(t,.91,1.0))*.535);needle.setAttribute('transform',`translate(${x} 0)`);freq.textContent=t>=.91?'100.7 FM':''}
  {const o=t>=2.71&&t<4.9?1-P(t,4.7,.2):0;op(nsp,o);tr(nsp,540,topOf('d1')-100,1);[...nsp.children].forEach((b,i)=>{const s=[2.71,3.0,3.42][i];const s2=[3.78,3.92,4.28][i];const k=back(P(t,s,.25))*(1+.15*Math.sin(P(t,s2,.25)*Math.PI));b.setAttribute('transform',`translate(${(i-1)*200} 0) scale(${k})`)})}
  pop(script,250,topOf('h1')-150,t,5.58,8.0,-6,.9);
  {const o=t>=8.11&&t<13.2?1-P(t,13.0,.2):0;op(phone,o);const ring=t<9.33;tr(phone,800,topOf('h1')-170,back(P(t,8.11,.3))*.8,ring?Math.sin(t*40)*8:0);op(waves,ring?1:0);
    const mom=t>=10.54;scrn.setAttribute('fill',mom?(t>=11.57&&Math.floor(t*8)%2?'#E0353B':'#5A1E22'):'#BFE3F5');callT.textContent=mom?'MOM':'📞';callT.setAttribute('fill',mom?'#fff':INK);callS.textContent=mom?'calling...':'';callS.setAttribute('fill',mom?'#FFD3D3':GREY)}
  pop(scream,DJ.Cs[0]+190,DJ.Cs[1]-20,t,12.34,13.4,-6,.75);
  {op(notes,song);[...notes.children].forEach((n,i)=>{const ph=(t*.5+i/8)%1;n.setAttribute('x',150+(i%4)*260+Math.sin(t*3+i)*20);n.setAttribute('y',980-ph*620);n.style.opacity=Math.sin(ph*Math.PI)})}
};
EP.init=function(){};
