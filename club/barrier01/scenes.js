// Club 01: skin barrier (9:16). All scenes on one timeline; times come from the aligned captions.
const VO_END=115.07,DUR=117.8;const RENDER=[],EVF=[];const flash=document.getElementById('flash');
const CXp=540,CYp=720;// panel centre
// ---------- shared drawings ----------
function pillT(p,text,fill,ink,fs=30){const c=g(p);const W=text.length*fs*.6+fs*1.6;const r=el('rect',{x:-W/2,y:-fs*.95,width:W,height:fs*1.9,rx:fs*.95,fill},c);const t=txt(c,0,fs*.36,fs,text,ink);c.r=r;c.t=t;c.W=W;return c}
function card(p,w,h,fill='#FFFFFF',rx=48){const c=g(p);el('rect',{x:-w/2,y:-h/2,width:w,height:h,rx,fill,filter:'url(#sh)'},c);return c}
function check(p,s=1,col=GOOD){const c=g(p,{transform:`scale(${s})`});el('circle',{r:30,fill:col},c);el('path',{d:'M-13 1 l9 10 l17 -21',fill:'none',stroke:'#FFFFFF','stroke-width':7,'stroke-linecap':'round','stroke-linejoin':'round'},c);return c}
function xmark(p,s=1){const c=g(p,{transform:`scale(${s})`});el('circle',{r:30,fill:RED},c);el('path',{d:'M-11 -11 L11 11 M11 -11 L-11 11',stroke:'#FFFFFF','stroke-width':7,'stroke-linecap':'round'},c);return c}
function drop(p,s=1,fill=WATER){const d=g(p,{transform:`scale(${s})`});el('path',{d:'M0 -30 Q22 -2 22 12 Q22 32 0 32 Q-22 32 -22 12 Q-22 -2 0 -30 Z',fill},d);el('ellipse',{cx:-7,cy:10,rx:5,ry:8,fill:'#FFFFFF',opacity:.6},d);return d}
function microbe(p,s=1,col='#9DB57A',spiky=true){const m=g(p,{transform:`scale(${s})`});if(spiky)for(let i=0;i<8;i++)el('rect',{x:-3,y:-34,width:6,height:14,rx:3,fill:col,transform:`rotate(${i*45})`},m);el('circle',{r:22,fill:col},m);el('circle',{cx:-7,cy:-4,r:3.5,fill:INK},m);el('circle',{cx:7,cy:-4,r:3.5,fill:INK},m);return m}
function friend(p,s=1,col='#E8C7A0'){const m=g(p,{transform:`scale(${s})`});el('ellipse',{rx:30,ry:22,fill:col},m);el('circle',{cx:-9,cy:-4,r:3.5,fill:INK},m);el('circle',{cx:9,cy:-4,r:3.5,fill:INK},m);el('path',{d:'M-8 6 Q0 13 8 6',fill:'none',stroke:INK,'stroke-width':3,'stroke-linecap':'round'},m);[-12,12].forEach(x=>el('ellipse',{cx:x,cy:4,rx:4,ry:2.5,fill:'#E59A8A',opacity:.7},m));return m}
function irritant(p,s=1){const m=g(p,{transform:`scale(${s})`});el('path',{d:'M0 -26 L8 -8 L26 -8 L12 4 L18 24 L0 12 L-18 24 L-12 4 L-26 -8 L-8 -8 Z',fill:'#A89A8E'},m);return m}
function pollen(p,s=1){const m=g(p,{transform:`scale(${s})`});for(let i=0;i<10;i++)el('circle',{cx:20*Math.cos(i*.628),cy:20*Math.sin(i*.628),r:7,fill:'#E6C25A'},m);el('circle',{r:16,fill:'#EFD27A'},m);return m}
// brick wall: corneocytes (bricks) + lipid mortar
function makeWall(p,cols=5,rows=5,bw=150,bh=62,gap=12){const W=g(p);const width=cols*(bw+gap),height=rows*(bh+gap);const clipId='wc'+Math.random().toString(36).slice(2,7);
  const cp=el('clipPath',{id:clipId},svg.querySelector('defs'));el('rect',{x:-width/2,y:-height/2,width,height,rx:26},cp);
  const inner=g(W,{'clip-path':`url(#${clipId})`});const base=el('rect',{x:-width/2,y:-height/2,width,height,fill:'#EFE4DA'},inner);const mortar=el('rect',{x:-width/2,y:-height/2,width,height,fill:BR},inner);
  const bricks=[];for(let r=0;r<rows;r++)for(let c=-1;c<=cols;c++){const x=-width/2+c*(bw+gap)+(r%2?(bw+gap)/2:0)+gap/2,y=-height/2+r*(bh+gap)+gap/2;
    const b=g(inner,{transform:`translate(${x+bw/2} ${y+bh/2})`});const rc=el('rect',{x:-bw/2,y:-bh/2,width:bw,height:bh,rx:18,fill:'#F7E3D6',stroke:'#E7C2AC','stroke-width':3},b);b.rc=rc;b.x=x+bw/2;b.y=y+bh/2;b.row=r;b.col=c;bricks.push(b)}
  const cracks=g(inner);W.bricks=bricks;W.mortar=mortar;W.cracks=cracks;W.width=width;W.height=height;W.inner=inner;return W}
function crackPath(x0,y0,len,seed){let d=`M${x0} ${y0}`;let x=x0,y=y0;for(let i=0;i<7;i++){x+=(Math.sin(seed*7+i*3.1)*.6)*len/7*1.6;y+=len/7;d+=` L${x.toFixed(1)} ${y.toFixed(1)}`}return d}

// ---------- background decor + logo ----------
const bg=g();[[160,380,240],[930,560,300],[140,1180,260],[940,1500,220]].forEach(([x,y,r],i)=>{const c=el('circle',{cx:x,cy:y,r,fill:'url(#glowB)'},bg);c.i=i});
const logo=el('image',{href:'../brand/logo_wtc.png',x:470,y:70,width:140,height:140});

// ================= HOOK: face, lens, cracks (c1..c5) =================
const face=g();const faceIn=g(face);
el('path',{d:'M40 -330 Q92 -300 96 -232 Q100 -206 112 -186 L166 -98 Q172 -82 150 -74 L132 -70 Q143 -56 139 -46 Q152 -36 136 -28 Q142 -16 131 -6 Q114 10 118 26 Q126 62 94 80 Q62 96 40 100 L40 240 L-140 240 L-150 -40 Q-190 -300 40 -330 Z',fill:'#F4D9C8'},faceIn);
el('path',{d:'M40 -330 Q92 -300 96 -232 Q100 -206 112 -186 L166 -98 Q172 -82 150 -74 L132 -70 Q143 -56 139 -46 Q152 -36 136 -28 Q142 -16 131 -6 Q114 10 118 26 Q126 62 94 80 Q62 96 40 100 L40 240',fill:'none',stroke:BR,'stroke-width':7,'stroke-linecap':'round','stroke-linejoin':'round'},faceIn);
el('path',{d:'M40 -332 Q-60 -430 -210 -330 Q-320 -200 -270 10 Q-240 160 -310 290 Q-200 310 -150 240 Q-120 140 -150 -40 Q-160 -200 -40 -250 Q20 -270 40 -332 Z',fill:BR},faceIn);
el('path',{d:'M58 -190 Q80 -196 92 -186',fill:'none',stroke:BR,'stroke-width':6,'stroke-linecap':'round'},faceIn);el('path',{d:'M60 -160 Q76 -150 92 -160',fill:'none',stroke:BR,'stroke-width':5,'stroke-linecap':'round'},faceIn);
const cheekBlush=el('ellipse',{cx:40,cy:-70,rx:110,ry:80,fill:'url(#blush)',opacity:0},faceIn);
const lens=g(face,{transform:'translate(30 -60)'});const lensIn=g(lens,{'clip-path':'url(#lensC)'});el('circle',{r:170,fill:'#EFE4DA'},lensIn);
const lensWall=makeWall(lensIn,4,5,110,46,10);const lensCr=[0,1,2].map(i=>el('path',{d:crackPath(-60+i*60,-140,300,i+1),fill:'none',stroke:'#3B2A22','stroke-width':6,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':'0 1'},lensIn));
el('circle',{r:170,fill:'none',stroke:CREAM,'stroke-width':14},lens);el('circle',{r:178,fill:'none',stroke:BR,'stroke-width':5},lens);
const sym=[['Gerginlik','gerilir'],['Kızarıklık','kızarır'],['Yanma','yakmaya']].map(([s,w],i)=>{const p=pillT(svg,s,i===1?RED:BR,CREAM,34);p.w=w;return p});
const title=g();const titT=txt(title,0,0,104,'CİLT BARİYERİ',INK,700);const titS=txt(title,0,70,40,'görünmez duvarın',BR,500);
RENDER.push(t=>{const t5=Gs('c6')-.2;
 if(vis(face,t,-1,Gs('c5')+.9)>0){const k=eo(P(t,0,1.4));const z=lerp(1.08,1,k);tr(face,560,820,z*(1-.35*eo(P(t,Gs('c5')-.1,.7))),0,1);face.setAttribute('transform',face.getAttribute('transform').replace(/translate\([^)]*\)/,`translate(560 ${lerp(820,600,eo(P(t,Gs('c5')-.1,.7)))})`));
  const tl=W_('c1','yüzünde')-.2;const lk=eo(P(t,tl,.6));lens.setAttribute('transform',`translate(30 -60) scale(${lk})`);lens.style.opacity=lk;
  lensWall.setAttribute('transform',`scale(${lerp(.6,1,eo(P(t,W_('c2','görünmez')-.2,1.0)))})`);
  const tc=W_('c3','çatladığında')-.2;lensCr.forEach((c,i)=>c.setAttribute('stroke-dasharray',`${eo(P(t,tc+i*.15,.5))} 1`));
  cheekBlush.setAttribute('opacity',.9*eo(P(t,W_('c4','kızarır')-.2,.8)));
}
 sym.forEach((p,i)=>{const a=W_(i?'c4':'c3',p.w)-.25;const v=on(t,a)*(1-P(t,Gs('c5')-.2,.3));show(v,p);if(v>0)tr(p,[290,820,300][i],[300,330,1080][i],pop(t,a),[-4,4,-3][i],v)});
 if(vis(title,t,Gs('c5')-.1,t5+.1)>0){tr(title,540,1060,1,0,1);titT.setAttribute('transform',`scale(${lerp(.9,1,eo(P(t,Gs('c5'),.6)))})`);titS.style.opacity=eo(P(t,W_('c5','bariyeri')-.1,.5))}
});
EVF.push(A=>{A(.1,'swell',2.2,.35);A(W_('c1','yüzünde')-.2,'lens',0,.6);A(W_('c2','görünmez')-.2,'shimmer',1.2,.4);A(W_('c3','çatladığında')-.2,'crack',0,.7);
 A(W_('c3','gerilir')-.25,'pop',0,.5);A(W_('c4','kızarır')-.25,'pop',0,.5);A(W_('c4','yakmaya')-.25,'pop',0,.5);A(Gs('c5')-.1,'whoosh',.5,.4);A(W_('c5','bariyeri')-.1,'chime',0,.5)});

// ================= LAYERS (c8..c17) =================
const panel=g();const panelIn=g(panel,{'clip-path':'url(#panelC)'});el('rect',{x:-450,y:-430,width:900,height:860,fill:'#FFFFFF'},panelIn);
const LY=[{n:'fat',y:170,h:260,fill:'#F6E3BF'},{n:'der',y:-120,h:290,fill:'#EFC2B4'},{n:'epi',y:-320,h:200,fill:'#F4D2C2'},{n:'sc',y:-430,h:110,fill:BR}];
const layers=LY.map(L=>{const l=g(panelIn);el('rect',{x:-450,y:L.y,width:900,height:L.h,fill:L.fill},l);l.L=L;return l});
for(let i=0;i<14;i++)el('ellipse',{cx:-400+(i%7)*130+(i>6?65:0),cy:i>6?370:250,rx:62,ry:52,fill:'#FBEFD6',stroke:'#E9CF9E','stroke-width':4},layers[0]);
for(let i=0;i<6;i++)el('path',{d:`M-450 ${-80+i*44} q112 -26 225 0 t225 0 t225 0 t225 0`,fill:'none',stroke:'#E3A797','stroke-width':6},layers[1]);
for(let r=0;r<3;r++)for(let i=0;i<10;i++)el('rect',{x:-460+i*104+(r%2?52:0),y:-308+r*60,width:96,height:50,rx:22,fill:'#F7DCCF',stroke:'#E9B9A6','stroke-width':3},layers[2]);
for(let r=0;r<3;r++)for(let i=0;i<9;i++)el('rect',{x:-460+i*118+(r%2?59:0),y:-424+r*35,width:110,height:28,rx:7,fill:'#F7EBDF'},layers[3]);
const scGlow=el('rect',{x:-450,y:-430,width:900,height:110,fill:'#FFFFFF',opacity:0},panelIn);
const labels=[['YAĞ DOKUSU',300],['DERMİS',25],['EPİDERMİS',-220]].map(([s,y])=>{const p=pillT(panel,s,'rgba(255,255,255,.92)',BR,30);p.y=y;return p});
const scLab=pillT(svg,'STRATUM KORNEUM',BR,CREAM,34);const scBr=g();el('path',{d:'M-470 -440 L-490 -440 L-490 -310 L-470 -310 M470 -440 L490 -440 L490 -310 L470 -310',fill:'none',stroke:BR,'stroke-width':8,'stroke-linecap':'round'},scBr);panel.appendChild(scBr);
const outside=g();const sun=g(outside);el('circle',{r:34,fill:'#EFC66A'},sun);for(let i=0;i<8;i++)el('rect',{x:-4,y:-58,width:8,height:16,rx:4,fill:'#EFC66A',transform:`rotate(${i*45})`},sun);
const outM=[0,1,2].map(i=>microbe(outside,.8));const outD=[0,1,2,3,4].map(i=>el('circle',{r:6,fill:'#B8A89A'},outside));const outT=pillT(outside,'DIŞ DÜNYA',SAND,BR,26);
const qMark=g();txt(qMark,0,0,300,'?',BR,700);const strongP=pillT(qMark,'Nasıl bu kadar güçlü?',BR,CREAM,34);
RENDER.push(t=>{const a=Gs('c8')-.25,b=Gs('c18')-.1;
 if(vis(panel,t,a,b,.4,.35)>0){const zin=eio(P(t,Gs('c17')+.2,1.0));const ps=lerp(lerp(.92,1,eo(P(t,a,.6))),3.2,zin);panel.setAttribute('transform',`translate(${CXp} ${lerp(CYp-375,720,zin)+375*ps}) scale(${ps})`);
  const ts=[W_('c9','yağ'),W_('c10','dermis'),W_('c11','epidermis'),W_('c13','stratum')].map(x=>x-.3);ts[0]=Math.min(ts[0],Gs('c8')+.6);
  layers.forEach((l,i)=>{const k=eo(P(t,i===0?Gs('c8'):ts[i],.6));l.setAttribute('transform',`translate(0 ${(1-k)*60})`);l.style.opacity=k});
  labels.forEach((p,i)=>tr(p,-430+p.W/2,p.y,pop(t,ts[i]),0,on(t,ts[i])*(1-P(t,Gs('c14')-.2,.3))));
  const tsc=ts[3];scGlow.setAttribute('opacity',.35*Math.max(0,Math.sin((t-tsc)*4))*on(t,tsc)*(1-on(t,Gs('c17'))));scBr.style.opacity=on(t,Gs('c12')+.4)*(1-on(t,Gs('c17')))}
 if(vis(scLab,t,W_('c13','stratum')-.3,Gs('c17')+.2)>0)tr(scLab,540,250,pop(t,W_('c13','stratum')-.3),0,1);
 if(vis(outside,t,Gs('c14')-.1,Gs('c15')-.1)>0){outside.setAttribute('transform','translate(0 0)');tr(sun,180,260,.9,t*20,1);outM.forEach((m,i)=>{const ph=((t*.7)+i/3)%1;tr(m,420+i*170,lerp(180,262,Math.abs(Math.sin(ph*Math.PI))),.8,0,1)});
  outD.forEach((d,i)=>{d.setAttribute('cx',330+i*130);d.setAttribute('cy',230+20*Math.sin(t*3+i))});tr(outT,900,180,1,0,1)}
 if(vis(qMark,t,Gs('c15')-.1,Gs('c17')-.05)>0){tr(qMark,540,700,pop(t,Gs('c15')-.1,.6),-6+4*Math.sin(t*2),1);tr(strongP,0,140,pop(t,W_('c16','güçlü')-.3),0,on(t,W_('c16','güçlü')-.3))}
 panel.style.filter=(t>Gs('c15')-.1&&t<Gs('c17'))?'blur(6px)':'none';
});
EVF.push(A=>{A(Gs('c8')-.25,'whoosh',.5,.35);[W_('c9','yağ'),W_('c10','dermis'),W_('c11','epidermis')].forEach(x=>A(x-.3,'pop',0,.5));A(W_('c13','stratum')-.3,'chime',0,.5);
 A(Gs('c14'),'shimmer',1.2,.3);A(Gs('c15')-.1,'whoosh',.4,.35);A(W_('c16','güçlü')-.3,'pop',0,.5);A(Gs('c17')+.2,'zoom',1.0,.5)});

// ================= WALL (c18..c23) =================
const wallS=g();const wall=makeWall(wallS,5,6,150,62,12);const korP=pillT(wallS,'KORNEOSİT',BEIGE,BR,32);const lipP=pillT(wallS,'LİPİTLER',BR,CREAM,32);
const cellDemo=g(wallS);const cellR=el('rect',{fill:'#F7E3D6',stroke:BR,'stroke-width':5},cellDemo);const cellArrow=txt(cellDemo,0,0,40,'→',BR);
const donut=g();const DN=[['SERAMİD',.5,BR,'seramid'],['KOLESTEROL',.25,BR2,'kolesterol'],['YAĞ ASİTLERİ',.25,'#D2B49C','yağ']];
el('circle',{r:110,fill:'none',stroke:'#EFE4DA','stroke-width':54},donut);const dSegs=DN.map(([,f,c])=>el('circle',{r:110,fill:'none',stroke:c,'stroke-width':54,pathLength:1000,transform:'rotate(-90)','stroke-dasharray':'0 1000'},donut));const dCenter=txt(donut,0,14,34,'LİPİT',BR);
const dLegend=DN.map(([s,,c],i)=>{const r=g(donut,{transform:`translate(190 ${-70+i*70})`});el('rect',{x:0,y:-20,width:36,height:36,rx:10,fill:c},r);txt(r,52,10,32,s,INK,700,'start');return r});
const halfP=pillT(donut,'YAKLAŞIK YARISI',BEIGE,BR,26);
const balance=g();[0,1,2].forEach(i=>{const a=-Math.PI/2+i*2*Math.PI/3;el('circle',{cx:70*Math.cos(a),cy:70*Math.sin(a),r:34,fill:DN[i][2]},balance)});el('path',{d:'M0 -70 L60.6 35 L-60.6 35 Z',fill:'none',stroke:BR,'stroke-width':4,opacity:.5},balance);const balC=check(balance,1.2);const solidP=pillT(balance,'SAĞLAM DUVAR',GOOD,'#FFFFFF',30);
RENDER.push(t=>{const a=Gs('c18')-.2,b=Gs('c24')-.1;
 if(vis(wallS,t,a,b,.3,.3)>0){const shrink=eio(P(t,Gs('c21')-.3,.7));wallS.setAttribute('transform',`translate(540 ${lerp(700,520,shrink)}) scale(${lerp(1,.78,shrink)})`);
  const tb=W_('c18','tuğla')-.3;wall.bricks.forEach(br=>{const d=tb+(5-br.row)*.13+(br.col+1)*.03;const k=eo(P(t,d,.4));br.setAttribute('transform',`translate(${br.x} ${br.y-(1-k)*260})`);br.style.opacity=k});
  const tl=W_('c20','lipitler')-.5;wall.mortar.setAttribute('opacity',eo(P(t,tl,1.0)));
  const tk=W_('c19','korneosit')-.3;tr(korP,0,-300,pop(t,tk),0,on(t,tk)*(1-on(t,Gs('c20')-.1)));tr(lipP,0,-300,pop(t,tl+.2),0,on(t,tl+.2)*(1-on(t,Gs('c21')-.3)));
  const tf=W_('c19','düzleşmiş')-.3;const fk=eio(P(t,tf,.8));show(V(t,tf-.1,Gs('c20')-.1),cellDemo);cellDemo.setAttribute('transform','translate(0 330)');
  const w_=lerp(110,190,fk),h_=lerp(110,66,fk);cellR.setAttribute('x',-w_/2);cellR.setAttribute('y',-h_/2);cellR.setAttribute('width',w_);cellR.setAttribute('height',h_);cellR.setAttribute('rx',lerp(55,20,fk));cellArrow.style.display='none'}
 if(vis(donut,t,Gs('c21')-.2,Gs('c23')-.1)>0){donut.setAttribute('transform','translate(330 1000)');let acc=0;const ts=[W_('c21','seramid'),W_('c22','kolesterol'),W_('c22','yağ')].map(x=>x-.3);
  dSegs.forEach((s,i)=>{const k=eo(P(t,ts[i],.6));s.setAttribute('stroke-dasharray',`${Math.max(0,DN[i][1]*1000*k-6)} 1000`);s.setAttribute('stroke-dashoffset',-acc*1000);acc+=DN[i][1];dLegend[i].style.opacity=on(t,ts[i])});
  tr(halfP,0,-170,pop(t,W_('c21','yarısı')-.3),0,on(t,W_('c21','yarısı')-.3))}
 if(vis(balance,t,Gs('c23')-.2,Gs('c24')-.1)>0){tr(balance,540,1000,pop(t,Gs('c23')-.2),0,1);const td=W_('c23','dengede')-.2;balance.firstChild.setAttribute('transform',`rotate(0)`);tr(balC,0,0,1.2*pop(t,td),0,on(t,td));tr(solidP,0,140,pop(t,W_('c23','sağlam')-.3),0,on(t,W_('c23','sağlam')-.3))}
});
EVF.push(A=>{A(Gs('c18')-.2,'whoosh',.4,.3);for(let i=0;i<6;i++)A(W_('c18','tuğla')-.3+i*.13,'tap',0,.35);A(W_('c19','korneosit')-.3,'pop',0,.5);A(W_('c19','düzleşmiş')-.3,'squish',.6,.4);
 A(W_('c20','lipitler')-.5,'flow',1.0,.4);[W_('c21','seramid'),W_('c22','kolesterol'),W_('c22','yağ')].forEach(x=>A(x-.3,'pop',0,.5));A(W_('c23','dengede')-.2,'chime',0,.5)});

// ================= NMF (c24..c26) =================
const nmf=g();const bigBrick=card(nmf,820,420,'#F7E3D6',60);el('rect',{x:-410,y:-210,width:820,height:420,rx:60,fill:'none',stroke:'#E7C2AC','stroke-width':6},nmf);
const nmfDots=[...Array(18)].map((_,i)=>{const d=g(nmf,{transform:`translate(${-300+(i%6)*120} ${-90+Math.floor(i/6)*90})`});el('circle',{r:20,fill:BR2},d);el('circle',{r:9,fill:CREAM,opacity:.7},d);return d});
const nmfLab=txt(nmf,0,-260,96,'NMF',BR);const nmfSub=txt(nmf,0,-200,30,'Doğal Nemlendirici Faktör',BR2,500);
const nmfDrops=[...Array(14)].map(()=>drop(nmf,.8));const magnet=g(nmf,{transform:'translate(0 320)'});el('path',{d:'M-60 -50 L-60 10 A60 60 0 0 0 60 10 L60 -50 L28 -50 L28 10 A28 28 0 0 1 -28 10 L-28 -50 Z',fill:BR},magnet);el('rect',{x:-60,y:-70,width:32,height:24,fill:'#C9CED8'},magnet);el('rect',{x:28,y:-70,width:32,height:24,fill:'#C9CED8'},magnet);
const inBrickT=pillT(nmf,'TUĞLANIN İÇİNDE',CREAM,BR,28);
RENDER.push(t=>{const a=Gs('c24')-.2,b=Gs('c27')-.1;
 if(vis(nmf,t,a,b)>0){tr(nmf,540,720,lerp(.6,1,eo(P(t,a,.6))),0,1);tr(inBrickT,0,260,1,0,on(t,a+.3)*(1-on(t,W_('c26','mıknatıs')-.3)));
  nmfDots.forEach((d,i)=>{const k=eo(P(t,W_('c24','doğal')-.2+i*.04,.4));d.style.opacity=k;d.setAttribute('transform',`translate(${-300+(i%6)*120} ${-90+Math.floor(i/6)*90}) scale(${k*(1+.06*Math.sin(t*4+i))})`)});
  const tn=Gs('c25')-.1;nmfLab.style.opacity=eo(P(t,tn,.4));nmfLab.setAttribute('transform',`translate(0 ${-20*(1-eo(P(t,tn,.4)))})`);nmfSub.style.opacity=eo(P(t,tn+.4,.4));
  const tm=W_('c26','mıknatıs')-.4;const mk=eio(P(t,tm,1.2));tr(magnet,0,320,pop(t,tm),0,on(t,tm));
  nmfDrops.forEach((d,i)=>{const tgt=nmfDots[(i*5)%18];const tx=-300+((i*5)%18%6)*120,ty=-90+Math.floor(((i*5)%18)/6)*90;const sx=-520+((i*137)%1040),sy=i%2?-380:380;
   tr(d,lerp(sx,tx+22,mk),lerp(sy,ty-22,mk),.6,0,on(t,tm))})}
});
EVF.push(A=>{A(Gs('c24')-.2,'whoosh',.4,.35);A(W_('c24','doğal')-.2,'bubbles',1.0,.4);A(Gs('c25')-.1,'pop',0,.55);A(W_('c26','mıknatıs')-.4,'drips',1.2,.45)});

// ================= ACID MANTLE + pH + friends (c27..c30) =================
const mant=g();const mWall=makeWall(mant,5,4,150,62,12);const filmR=g(mant);el('rect',{x:-410,y:-190,width:820,height:46,rx:23,fill:ROSE,opacity:.75},filmR);const filmHi=el('rect',{x:-410,y:-182,width:160,height:12,rx:6,fill:'#FFFFFF',opacity:.7},filmR);filmR.style.opacity=0;const filmT=pillT(mant,'ASİT MANTOSU',ROSE,INK,32);
const friends=[0,1,2,3].map(i=>friend(mant,.9,['#E8C7A0','#D9C2E0','#C7DDBF','#F0CFB0'][i]));const dostP=pillT(mant,'DOST BAKTERİLER',GOOD,'#FFFFFF',28);
const ph=g();el('rect',{x:-380,y:-26,width:760,height:52,rx:26,fill:'url(#phg)'},ph);[0,7,14].forEach(v=>txt(ph,-380+v/14*760,70,28,String(v),BR2,700));txt(ph,-380,-50,26,'ASİDİK',RED,700,'start');txt(ph,380,-50,26,'BAZİK',RED==='x'?'':'#6E86B8',700,'end');
const phM=g(ph);el('path',{d:'M0 -40 L18 -66 L-18 -66 Z',fill:INK},phM);el('rect',{x:-4,y:-40,width:8,height:80,rx:4,fill:INK},phM);const phV=pillT(phM,'≈ 4,7',INK,CREAM,32);const phLab=txt(ph,0,-110,34,'SAĞLIKLI CİLT pH',INK);
RENDER.push(t=>{const a=Gs('c27')-.2,b=Gs('c31')-.1;
 if(vis(mant,t,a,b)>0){const up=eio(P(t,Gs('c29')-.3,.6));tr(mant,540,lerp(720,600,up),lerp(.95,.8,up),0,1);const tf=W_('c27','film')-.4;filmR.style.opacity=eo(P(t,tf,.8));filmHi.setAttribute('x',-410+((t*260)%660));
  tr(filmT,0,-330,pop(t,W_('c28','asit')-.3),0,on(t,W_('c28','asit')-.3));const tdo=W_('c30','dostu')-.3;
  friends.forEach((f,i)=>{const x=-300+i*200+30*Math.sin(t*1.3+i*2);tr(f,x,-235-8*Math.abs(Math.sin(t*4+i)),1.4*pop(t,tdo+i*.12),0,on(t,tdo+i*.12))});tr(dostP,0,250,pop(t,tdo+.3),0,on(t,tdo+.3))}
 if(vis(ph,t,Gs('c29')-.2,Gs('c30')-.1)>0){tr(ph,540,1030,pop(t,Gs('c29')-.2),0,1);const tp=W_('c29','beşin')-.4;const k=eio(P(t,tp,1.0));phM.setAttribute('transform',`translate(${-380+lerp(7,4.7,k)/14*760} 0)`);phV.setAttribute('transform','translate(0 -110)');phV.style.opacity=on(t,tp+.6);phLab.style.opacity=1-on(t,tp+.6)}
});
EVF.push(A=>{A(Gs('c27')-.2,'whoosh',.4,.35);A(W_('c27','film')-.4,'shimmer',1.2,.4);A(W_('c28','asit')-.3,'pop',0,.5);A(Gs('c29')-.2,'pop',0,.5);A(W_('c29','beşin')-.4,'slide',1.0,.35);A(W_('c30','dostu')-.3,'bubbles',.8,.4)});

// ================= TWO-WAY BARRIER (c31..c35) =================
const qCard=g();const qc=card(qCard,760,300,'#FFFFFF');const qT=txt(qCard,0,70,60,'',BR);const qQ=txt(qCard,0,-10,110,'?',BR2);
const two=g();const tWall=makeWall(two,6,2,130,56,10);const inLab=pillT(two,'İÇERİDEKİ SU',WATER,'#FFFFFF',28);
const upArr=g(two);el('path',{d:'M0 60 L0 -60 M-24 -36 L0 -60 L24 -36',fill:'none',stroke:WATER,'stroke-width':12,'stroke-linecap':'round'},upArr);const dnArr=g(two);el('path',{d:'M0 -60 L0 60 M-24 36 L0 60 L24 36',fill:'none',stroke:'#A89A8E','stroke-width':12,'stroke-linecap':'round'},dnArr);
const twoT=pillT(two,'İKİ YÖNLÜ',BR,CREAM,34);
const wDrops=[...Array(6)].map(()=>drop(two,.9));const irr=[0,1].map(()=>irritant(two,1.1)),pol=[0,1].map(()=>pollen(two,1)),mic=[0,1].map(()=>microbe(two,1));const wLabs=[['Tahriş ediciler','tahriş'],['Alerjenler','alerjenleri'],['Mikroplar','mikropları']].map(([s,w])=>{const p=pillT(two,s,'#FFFFFF',BR,26);p.w=w;return p});
const bounce=(t,t0,per)=>{const ph=((t-t0)/per)%1;return Math.abs(Math.sin(ph*Math.PI))};
RENDER.push(t=>{
 const qs=[[Gs('c31')-.2,Gs('c32')-.1,'Ne işe yarar?'],[Gs('c36')-.2,Gs('c37')-.1,'Sağlıklı bariyer?']];let qv=0;
 qs.forEach(([a,b,s])=>{const v=V(t,a,b,.3,.25);if(v>0){qv=v;qT.textContent=s;tr(qCard,540,720,pop(t,a)*1,0,v)}});show(qv,qCard);
 if(vis(two,t,Gs('c32')-.15,Gs('c36')-.2)>0){two.setAttribute('transform','translate(540 720)');const tw=Gs('c33')-.1;const wk=eo(P(t,tw,.5));tWall.style.opacity=wk;
  tr(twoT,0,0,pop(t,Gs('c32')-.15),0,1-on(t,tw));tr(upArr,-120,0,1,0,1-on(t,tw));tr(dnArr,120,0,1,0,1-on(t,tw));
  const ts=W_('c33','suyu')-.3;wDrops.forEach((d,i)=>{const b=bounce(t,ts+i*.17,1.1);tr(d,-330+i*130,lerp(330,95,b),.9,0,on(t,ts))});tr(inLab,0,420,pop(t,ts),0,on(t,ts));
  const tt=[W_('c34','tahriş'),W_('c34','alerjenleri'),W_('c35','mikropları')].map(x=>x-.3);
  [irr,pol,mic].forEach((arr,j)=>arr.forEach((m,i)=>{const b=bounce(t,tt[j]+i*.3,1.2);tr(m,-330+j*260+i*120,lerp(-330,-100,b),1,t*30*(j===0),on(t,tt[j]))}));
  wLabs.forEach((p,j)=>tr(p,-300+j*300,-420,pop(t,tt[j]),0,on(t,tt[j])))}
});
EVF.push(A=>{A(Gs('c31')-.2,'whoosh',.4,.35);A(Gs('c32')-.15,'pop',0,.5);A(W_('c33','suyu')-.3,'drips',1.2,.4);[W_('c34','tahriş'),W_('c34','alerjenleri'),W_('c35','mikropları')].forEach(x=>A(x-.3,'tap',0,.45));A(Gs('c35'),'block',0,.35);A(Gs('c36')-.2,'whoosh',.4,.35)});

// ================= HEALTHY CHECKLIST (c37..c40) =================
const hc=card(svg,880,700,'#FFFFFF');const hcT=txt(hc,0,-270,40,'SAĞLIKLI BARİYER',BR);
const hRows=[['Yumuşak ve nemli','yumuşak','c37'],['Yıkadıktan sonra gerilmez','gerilmez','c38'],['Yanma, batma yok','yanmaz','c39'],['Kızarıklık, pullanma yok','kızarıklık','c40']].map(([s,w,id],i)=>{const r=g(hc,{transform:`translate(-360 ${-160+i*120})`});const ck=check(r,1.1);const tt_=txt(r,60,12,40,s,INK,700,'start');r.ck=ck;r.tt_=tt_;r.w=w;r.id=id;return r});
const sparkle=[...Array(6)].map(()=>{const s=el('path',{d:'M0 -18 L4 -4 L18 0 L4 4 L0 18 L-4 4 L-18 0 L-4 -4 Z',fill:'#E6C25A'},hc);return s});
RENDER.push(t=>{if(vis(hc,t,Gs('c37')-.2,Gs('c41')-.1)>0){tr(hc,540,700,lerp(.92,1,eo(P(t,Gs('c37')-.2,.5))),0,1);
  hRows.forEach(r=>{const a=W_(r.id,r.w)-.3;r.ck.setAttribute('transform',`scale(${1.1*pop(t,a)})`);r.ck.style.opacity=on(t,a);r.tt_.style.fill=t>a?INK:'#C9B8A8'});
  sparkle.forEach((s,i)=>{const ph=((t*.6)+i/6)%1;s.setAttribute('transform',`translate(${-380+i*150} ${-330+30*Math.sin(i)}) scale(${Math.sin(ph*Math.PI)})`)})}});
EVF.push(A=>{hRows.forEach(r=>A(W_(r.id,r.w)-.3,'tick',0,.55));A(Gs('c37'),'sparkle',1.2,.3)});

// ================= DAMAGE (c41..c45) =================
const dmg=g();const dWall=makeWall(dmg,5,5,150,62,12);
const causes=[['Aşırı yıkama','aşırı','c41'],['Sert temizleyici','sert','c41'],['Sık peeling','sık','c42'],['Soğuk, kuru hava','soğuk','c42']].map(([s,w,id],i)=>{const c=g(dmg);const ic=g(c,{transform:'translate(0 -10)'});
  if(i===0){[0,1,2].forEach(k=>drop(ic,.7).setAttribute('transform',`translate(${-30+k*30} ${k%2?10:-10}) scale(.7)`));}
  if(i===1){el('rect',{x:-26,y:-30,width:52,height:70,rx:12,fill:'#9DB5C9'},ic);el('rect',{x:-10,y:-48,width:20,height:20,rx:4,fill:BR2},ic)}
  if(i===2){el('circle',{r:34,fill:'#EDE1D6'},ic);for(let k=0;k<10;k++)el('circle',{cx:22*Math.cos(k*2.4)*Math.sqrt(k/10),cy:22*Math.sin(k*2.4)*Math.sqrt(k/10),r:5,fill:BR2},ic)}
  if(i===3){[0,60,120].forEach(a=>el('rect',{x:-4,y:-36,width:8,height:72,rx:4,fill:'#8FB2CF',transform:`rotate(${a})`},ic))}
  const p=pillT(c,s,'#FFFFFF',BR,26);p.setAttribute('transform','translate(0 70)');c.w=w;c.id=id;return c});
const cracksD=[0,1,2,3].map(i=>el('path',{d:crackPath(-280+i*180,-190,400,i+3),fill:'none',stroke:INK,'stroke-width':8,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':'0 1'},dWall.inner));
const leak=[...Array(6)].map(()=>drop(dmg,.7));const sneak=[...Array(4)].map((_,i)=>i%2?irritant(dmg,.9):microbe(dmg,.8));const crackP=pillT(dmg,'ÇATLAKLAR',RED,'#FFFFFF',30);
RENDER.push(t=>{const a=Gs('c41')-.2,b=Gs('c46')-.1;
 if(vis(dmg,t,a,b)>0){dmg.setAttribute('transform','translate(540 700)');const ta=W_('c43','aşındırabilir')-.3;const er=eo(P(t,ta,1.2));
  causes.forEach((c,i)=>{const t0=W_(c.id,c.w)-.3;const hit=eo(P(t,t0,.5));const pos=[[-300,-330],[300,-330],[-300,330],[300,330]][i];tr(c,lerp(pos[0]*1.6,pos[0],hit),pos[1],1,0,on(t,t0)*(1-P(t,Gs('c44')-.2,.3)))});
  let hits=0;causes.forEach(c=>{if(t>W_(c.id,c.w))hits++});dWall.mortar.setAttribute('opacity',1-.18*hits-.25*er);
  dWall.bricks.forEach((br,i)=>{const dz=er*((i*37)%10)/10;br.setAttribute('transform',`translate(${br.x+dz*6*Math.sin(i)} ${br.y+dz*5}) rotate(${dz*6*Math.sin(i*3)})`)});
  const tc=W_('c44','çatlaklar')-.3;cracksD.forEach((c,i)=>c.setAttribute('stroke-dasharray',`${eo(P(t,tc+i*.12,.5))} 1`));tr(crackP,0,-300,pop(t,tc),0,on(t,tc)*(1-on(t,Gs('c45')-.1)));
  const tl=W_('c45','su')-.3;leak.forEach((d,i)=>{const ph=((t-tl)*.7+i/6)%1;tr(d,-250+i*100,lerp(60,-420,ph),.7,0,on(t,tl)*(1-ph))});
  const ts=W_('c45','sızar')-.8;sneak.forEach((m,i)=>{const ph=((t-ts)*.6+i/4)%1;tr(m,-200+i*130,lerp(-380,120,ph),.8,0,on(t,ts)*(1-ph))})}
});
EVF.push(A=>{A(Gs('c41')-.2,'whoosh',.4,.35);[['c41','aşırı'],['c41','sert'],['c42','sık'],['c42','soğuk']].forEach(([id,w])=>A(W_(id,w)-.1,'thump',0,.4));A(W_('c43','aşındırabilir')-.3,'crumble',1.0,.35);
 A(W_('c44','çatlaklar')-.3,'crack',0,.7);A(W_('c45','su')-.3,'drips',1.0,.4)});

// ================= END (c46..c48 + tail) =================
const nxt=g();const nc=card(nxt,880,520,'#FFFFFF');txt(nxt,0,-170,34,'SIRADAKİ',BR2);txt(nxt,0,-90,62,'Bariyer nasıl',INK);txt(nxt,0,-10,62,'onarılır?',BR);
const rWall=makeWall(nxt,4,2,140,52,10);rWall.setAttribute('transform','translate(0 140) scale(.8)');const dots=txt(nxt,0,250,60,'',BR2);
const follow=g();const fb=el('rect',{x:-210,y:-56,width:420,height:112,rx:56,fill:BR},follow);const fT=txt(follow,0,16,46,'Takip Et',CREAM);const tap=el('circle',{r:20,fill:'none',stroke:BR,'stroke-width':6,opacity:0},follow);
RENDER.push(t=>{const a=Gs('c46')-.2;
 if(vis(nxt,t,a,999)>0){tr(nxt,540,720,lerp(.9,1,eo(P(t,a,.6))),0,1);const k=eio(P(t,W_('c47','onarabileceğimizi')-.3,1.6));
  rWall.bricks.forEach((br,i)=>{const off=((i*53)%7-3)*14*(1-k*.6);br.setAttribute('transform',`translate(${br.x} ${br.y+off}) rotate(${off*.5})`)});rWall.mortar.setAttribute('opacity',.25+.4*k);
  dots.textContent='.'.repeat(1+Math.floor(t*2.5)%3)}
 const tf=W_('c48','takipte')-.3;if(vis(follow,t,tf,999)>0){tr(follow,540,1120,pop(t,tf),0,1);const tp=tf+.5;const c=t>tp;fb.setAttribute('fill',c?BR2:BR);fT.textContent=c?'Takiptesin ✓':'Takip Et';tap.setAttribute('r',20+70*P(t,tp,.5));tap.style.opacity=c?1-P(t,tp,.5):0}
});
EVF.push(A=>{A(Gs('c46')-.2,'whoosh',.45,.4);A(W_('c47','onarabileceğimizi')-.3,'shimmer',1.4,.35);A(W_('c48','takipte')-.3,'pop',0,.5);A(W_('c48','takipte')+.2,'tick',0,.6);A(VO_END+.3,'chime',0,.5)});

// ================= WTC EXPERT (portrait circle <-> corner bubble) =================
const ex=g();const exBg=el('circle',{r:140,fill:BEIGE},ex);const exClip=g(ex,{'clip-path':'url(#bubC)'});const exG=g(exClip);const expert=makeExpert(exG);
const exRing=el('circle',{r:142,fill:'none',stroke:BR,'stroke-width':6},ex);const exTag=pillT(ex,'WTC Expert',BR,CREAM,34);const bubR=document.getElementById('bubR');
const BIG={x:540,y:720,r:330,s:1.0,oy:60},SMALL={x:150,y:1600,r:120,s:.42,oy:44},END={x:540,y:1640,r:170,s:.56,oy:74};
const exMode=t=>{const big1=V(t,Gs('c6')-.25,Gs('c8')-.05,.45,.55),big2=eo(P(t,Gs('c46')-.4,.6))*(1-eo(P(t,Gs('c46')+.2,.6)));
  const inBub=t>Gs('c8')-.4;return {big:big1,show:t>Gs('c6')-.25?1:0,bub:inBub?1:0}};
RENDER.push(t=>{const m=exMode(t);show(m.show,ex);if(!m.show)return;const k=m.big;const ap=eo(P(t,Gs('c6')-.25,.5));
 const ke=eio(P(t,Gs('c46')-.3,.7));const T=t>Gs('c46')-.3?END:BIG;const kk=t>Gs('c46')-.3?ke:k;const S=t<Gs('c8')-.4?BIG:{x:lerp(SMALL.x,T.x,kk),y:lerp(SMALL.y,T.y,kk),r:lerp(SMALL.r,T.r,kk),s:lerp(SMALL.s,T.s,kk),oy:lerp(SMALL.oy,T.oy,kk)};
 const r=S.r*(t<Gs('c8')-.4?ap:1);ex.setAttribute('transform',`translate(${S.x} ${S.y})`);exBg.setAttribute('r',r);exRing.setAttribute('r',r+2);bubR.setAttribute('r',r);exG.setAttribute('transform',`translate(0 ${S.oy+S.r*.02}) scale(${S.s*(t<Gs('c8')-.4?lerp(.9,1,ap):1)})`);
 tr(exTag,0,r+50,pop(t,W_('c6','wtc')-.2),0,V(t,W_('c6','wtc')-.2,Gs('c8')-.2));
 const mo=t<VO_END?mouthAt(t):0;const wave=V(t,Gs('c6')-.1,Gs('c7')+.4)*(t<Gs('c7')?1:0);
 expert.set({mouth:.85*mo,smile:.65,browUp:.15+.25*mo,eyes:blinkAt(t,3.7,.4),look:[t>Gs('c8')?.35:0,0],tilt:2*Math.sin(t*1.1),nod:2*mo,
  hands:{L:{x:-190,y:330,shape:'fist'},R:wave>0?{x:300,y:-30,shape:'open',rot:-80+16*Math.sin(t*9)}:{x:190,y:330,shape:'fist'}}})});
EVF.push(A=>{A(Gs('c6')-.25,'bloom',.6,.45);A(Gs('c7')+.4,'zoom',1.2,.45)});

// ================= dive transition + main loop =================
const iris=el('circle',{cx:540,cy:720,r:0,fill:BEIGE});
window.render=function(t){flash.style.opacity=0;renderCaptions(t);
 const ti=Gs('c7')+.6,te=Gs('c8')-.25;const kin=eio(P(t,ti,te-ti-.2)),kout=eo(P(t,te-.2,.5));iris.setAttribute('r',1300*kin*(1-kout));iris.style.opacity=1-kout;
 RENDER.forEach(f=>f(t));svg.appendChild(iris);svg.appendChild(ex)};
window.DUR=DUR;
window.EV=(()=>{const E=[];const A=(t,type,d=0,v=1)=>E.push([+t.toFixed(3),type,d,v]);EVF.forEach(f=>f(A));return E.sort((a,b)=>a[0]-b[0])})();
window.__ready=document.fonts.ready.then(()=>{fitCaptions();window.render(0);return true});
