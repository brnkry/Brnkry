// ================= PART G: rules for everyone =================
const PH=Gs('h1')-.1;
const evr=g();const evP=pill(evr,'RULES FOR EVERYONE',LIME,ASPH,420,32);const evGas=g(evr);el('rect',{x:-60,y:-80,width:120,height:160,rx:24,fill:CHALK},evGas);txt(evGas,0,10,30,'bold','GAS').setAttribute('fill',ASPH);
const evDsl=g(evr);el('rect',{x:-60,y:-80,width:120,height:160,rx:24,fill:DIESEL},evDsl);txt(evDsl,0,10,26,'bold','DIESEL').setAttribute('fill',ASPH);
// snowy car
const snowCar=g();const scCar=makeCar(snowCar,{body:LIME,ink:ASPH,acc:'#FFF6D0'});
const mir=g(snowCar,{transform:'translate(270 -70)'});el('path',{d:'M0 0 L44 -10 L50 26 L6 30 Z',fill:LIME},mir);el('path',{d:'M6 4 L40 -4 L44 22 L10 26 Z',fill:'#1B1B21'},mir);
const SN='#F4F7FB';const snowParts={
 windshield:el('path',{d:'M84 -118 L194 -118 Q250 -114 290 -60 L84 -60 Z',fill:SN},snowCar),
 windows:el('path',{d:'M-170 -60 Q-112 -112 -32 -118 L60 -118 L60 -60 Z',fill:SN},snowCar),
 mirrors:el('path',{d:'M274 -72 L322 -84 L330 -42 L280 -38 Z',fill:SN},snowCar),
 lights:g(snowCar),roof:el('path',{d:'M-210 -112 Q-150 -178 40 -184 Q220 -178 310 -108 Q230 -138 40 -142 Q-120 -138 -210 -112 Z',fill:SN},snowCar)};
el('ellipse',{cx:444,cy:-6,rx:30,ry:24,fill:SN},snowParts.lights);el('ellipse',{cx:-452,cy:6,rx:20,ry:26,fill:SN},snowParts.lights);
const scraper=g(snowCar);el('rect',{x:-14,y:-10,width:28,height:120,rx:10,fill:'#2E6BD8'},scraper);el('path',{d:'M-50 -10 L50 -10 L40 -40 L-40 -40 Z',fill:'#9ADFFF'},scraper);
const allSnow=pill(snowCar,'CLEAR ALL OF IT',COLD,CHALK,320,32);
const defr=g();const ws=el('path',{d:'M-170 60 Q0 -40 170 60 L140 120 Q0 50 -140 120 Z',fill:'none',stroke:CHALK,'stroke-width':14,'stroke-linejoin':'round'},defr);
const defArrows=[-80,0,80].map(x=>el('path',{d:`M${x} 100 q-14 -20 0 -40 q14 -20 0 -40 M${x-12} 30 L${x} 14 L${x+12} 30`,fill:'none',stroke:WARM,'stroke-width':10,'stroke-linecap':'round','stroke-linejoin':'round'},defr));
const defP=pill(defr,'DEFROSTER ON',WARM,ASPH,300,28);const oneP=pill(defr,'THE ONE GOOD REASON',LIME,ASPH,400,28);
// garage + CO
const gar=g();el('path',{d:'M-360 -200 L0 -330 L360 -200 L360 220 L-360 220 Z',fill:'#3A3550'},gar);el('rect',{x:-300,y:-160,width:600,height:380,fill:'#141420'},gar);
const garCar=carIcon(gar,.5,{body:LIME});garCar.setAttribute('transform','translate(0 140)');const garPuffs=puffs(gar,10,'#8A8A96');
const coCloud=[...Array(9)].map((_,i)=>el('circle',{cx:-220+(i%5)*110,cy:120,r:0,fill:'#8A8A96',opacity:.0},gar));
const door=el('rect',{x:-300,y:-160,width:600,height:380,fill:'#6A6A86'},gar);[...Array(6)].forEach((_,i)=>el('rect',{x:-300,y:-160+i*64,width:600,height:4,fill:'#4A4A66'},gar));const doorLines=[...gar.children].slice(-6);
const coT=txt(gar,0,0,90,'bold','CO');coT.setAttribute('fill',CHALK);const garX=XMARK(gar,2);const neverP=pill(gar,'NEVER INSIDE A GARAGE',RED,CHALK,440,28);const smellP=pill(gar,"YOU CAN'T SMELL IT",RED,CHALK,380,28);
// unattended car + thief
const unat=g();el('rect',{x:-460,y:120,width:920,height:10,rx:5,fill:'#30303A'},unat);const unCar=carIcon(unat,.55,{body:LIME});unCar.setAttribute('transform','translate(-60 30)');const unPuffs=puffs(unat,10,'#C9D3E3');
const thief=g(unat);el('circle',{cx:0,cy:-150,r:46,fill:'#0A0A0E'},thief);el('path',{d:'M-70 120 L-60 -80 Q0 -110 60 -80 L70 120 Z',fill:'#0A0A0E'},thief);el('rect',{x:-40,y:-160,width:80,height:20,rx:8,fill:'#2A2A33'},thief);
const unP=pill(unat,'UNATTENDED',AMBER,ASPH,280,28);const illP=pill(unat,'ILLEGAL IN SOME STATES',RED,CHALK,440,28);
const fob=g();el('rect',{x:-90,y:-170,width:180,height:340,rx:70,fill:'#2A2A33'},fob);const fbBtns=[['LOCK',-90],['UNLOCK',-10],['START',80]].map(([s,y])=>{const b=g(fob,{transform:`translate(0 ${y})`});const c=el('circle',{r:32,fill:'#3A3A46'},b);txt(b,0,8,16,'mic ink',s);b.c=c;return b});
const sig=[0,1,2].map(i=>el('path',{fill:'none',stroke:LIME,'stroke-width':8,'stroke-linecap':'round'},fob));const lockI=g(fob);el('rect',{x:-50,y:-30,width:100,height:80,rx:14,fill:LIME},lockI);el('path',{d:'M-30 -30 v-24 a30 30 0 0 1 60 0 v24',fill:'none',stroke:LIME,'stroke-width':12},lockI);
const lockP=pill(fob,'DOORS STAY LOCKED',LIME,ASPH,380,28);const rsP=pill(fob,'REMOTE STARTER',GRAPH,CHALK,320,28);

KEYS.push([PG+.1,'open'],[Gs('g2'),'mid'],[Gs('g3'),'one'],[W_('g3','defroster')-.3,'mid'],[Gs('g4'),'stop'],[Gs('g4')+1.2,'mid'],[Gs('g5'),'shrug'],[Gs('g6'),'stop'],[Gs('g6')+1,'mid'],[Gs('g7'),'mid'],[Gs('g8'),'mid'],[W_('g8','locked')-.3,'thumb']);
MOODS.push([Gs('g4'),Gs('g8'),{smile:0,browWorry:.4}]);
RENDER.push(t=>{
 if(t<PG-.5||t>PH+.5){show(0,evr,snowCar,defr,gar,unat,fob);return}capMode('studio');
 if(vis(evr,t,PG,Gs('g2')-.1)>0){evr.setAttribute('transform',`translate(${CX} 0)`);tr(evP,0,250,pop(t,PG),0,1);tr(evGas,-110,470,pop(t,PG+.2),-6,1);tr(evDsl,110,470,pop(t,PG+.35),6,1)}
 if(vis(snowCar,t,Gs('g2')-.1,Gs('g3')-.1)>0){tr(snowCar,CX,470,.8*pop(t,Gs('g2')-.1),0,1);scCar.setAttribute('transform','');
  const keys={windshield:'windshield',windows:'windows',mirrors:'mirrors',lights:'lights',roof:'roof'};let cur=null;
  Object.entries(keys).forEach(([k,w])=>{const tw=W_('g2',w)-.2;const k2=1-eo(P(t,tw,.45));snowParts[k].style.opacity=k2;if(t>tw-.2&&t<tw+.5)cur=k});
  const sp={windshield:[190,-90],windows:[-60,-90],mirrors:[300,-60],lights:[444,-6],roof:[40,-150]};const p=cur?sp[cur]:[600,-300];scraper.setAttribute('transform',`translate(${p[0]+30*Math.sin(t*18)} ${p[1]-60}) rotate(${20*Math.sin(t*18)})`);scraper.style.opacity=cur?1:0;
  tr(allSnow,0,-330,pop(t,W_('g2','all')-.3),0,on(t,W_('g2','all')-.3))}
 if(vis(defr,t,Gs('g3')-.1,Gs('g4')-.1)>0){defr.setAttribute('transform',`translate(${CX} 440)`);tr(oneP,0,-230,pop(t,W_('g3','one')-.3),0,on(t,W_('g3','one')-.3));const td=W_('g3','defroster')-.3;
  ws.setAttribute('stroke',t>td?WARM:CHALK);defArrows.forEach((a,i)=>{a.style.opacity=on(t,td)*(.5+.5*Math.sin(t*6-i));a.setAttribute('transform',`translate(0 ${-8*Math.sin(t*6-i)})`)});tr(defP,0,230,pop(t,td),0,on(t,td))}
 if(vis(gar,t,Gs('g4')-.1,Gs('g6')-.1)>0){tr(gar,CX,500,.85*pop(t,Gs('g4')-.1),0,1);const to=W_('g4','open')-.4;const k=eio(P(t,to,.8));const dh=380*(1-k*.75);door.setAttribute('height',dh);doorLines.forEach((l,i)=>l.style.opacity=(-160+i*64)<-160+dh?1:0);
  garPuffs.upd(t,-160,180,-30,-30,2.6,1,18);tr(garX,240,-200,2*pop(t,W_('g4','Never')-.2),0,on(t,W_('g4','Never')-.2));tr(neverP,0,-400,pop(t,W_('g4','garage')-.3),0,on(t,W_('g4','garage')-.3)*(1-on(t,Gs('g5')-.1)));
  const tc=W_('g5','Carbon')-.3;const ck=eo(P(t,tc,2.2));coCloud.forEach((c,i)=>{c.setAttribute('r',90*ck*(1+.1*Math.sin(t*2+i)));c.setAttribute('cy',120-260*ck*((i%3)/3+.4));c.setAttribute('opacity',.45*ck)});coT.style.opacity=on(t,tc+.4);coT.setAttribute('y',-20);
  tr(smellP,0,-400,pop(t,W_('g5','smell')-.3),0,on(t,W_('g5','smell')-.3))}
 if(vis(unat,t,Gs('g6')-.1,Gs('g8')-.1)>0){unat.setAttribute('transform',`translate(${CX} 470)`);unCar.setAttribute('transform',`translate(-60 ${30+1.2*Math.sin(t*40)})`);unPuffs.upd(t,-360,70,-60,-24,2.2,1,16);
  const tth=Gs('g7')-.1;const k=eo(P(t,tth,1.4));tr(thief,lerp(560,240,k),0,.9,0,on(t,tth));tr(unP,-60,-260,pop(t,W_('g6','unattended')-.3),0,on(t,W_('g6','unattended')-.3)*(1-on(t,tth)));
  const ti=W_('g7','illegal')-.3;tr(illP,-60,-260,pop(t,ti),0,on(t,ti))}
 if(vis(fob,t,Gs('g8')-.1,PH+.05)>0){tr(fob,CX-160,450,pop(t,Gs('g8')-.1),0,1);const tr_=W_('g8','remote')-.3;const pr=V(t,tr_+.2,tr_+.5,.05,.1);fbBtns[2].c.setAttribute('fill',t>tr_+.2?LIME:'#3A3A46');fbBtns[2].setAttribute('transform',`translate(0 80) scale(${1-.1*pr})`);
  sig.forEach((s,i)=>{const r=60+i*40;s.setAttribute('d',`M${130} ${-r*.6} A${r} ${r} 0 0 1 ${130} ${r*.6}`);s.setAttribute('transform',`translate(${i*10} 0)`);s.style.opacity=on(t,tr_+.2)*(.5+.5*Math.sin(t*8-i))});
  tr(rsP,330,-200,pop(t,tr_),0,on(t,tr_));const tl=W_('g8','locked')-.3;tr(lockI,380,10,pop(t,tl),0,on(t,tl));tr(lockP,330,200,pop(t,tl),0,on(t,tl))}
});
EVF.push(A=>{
 A(PG,'whoosh',.45,.45);A(PG+.2,'pop',0,.5);A(Gs('g2')-.1,'whoosh',.4,.4);['windshield','windows','mirrors','lights','roof'].forEach(w=>A(W_('g2',w)-.2,'scrape',.45,.4));
 A(Gs('g3')-.1,'whoosh',.4,.4);A(W_('g3','defroster')-.3,'air',1.4,.35);A(Gs('g4')-.1,'whoosh',.4,.4);A(W_('g4','Never')-.2,'thud',0,.45);A(W_('g4','open')-.4,'whir',.8,.3);A(W_('g5','Carbon')-.3,'hiss',2,.3);A(W_('g5','smell')-.3,'alarm',0,.25);
 A(Gs('g6')-.1,'whoosh',.4,.4);A(Gs('g6'),'idle',2.6,.2);A(W_('g6','unattended')-.3,'pop',0,.5);A(Gs('g7')-.1,'whoosh',.6,.25);A(W_('g7','illegal')-.3,'thud',0,.45);
 A(Gs('g8')-.1,'pop',0,.5);A(W_('g8','remote')-.1,'click',0,.8);A(W_('g8','remote')+.2,'ping',0,.35);A(W_('g8','locked')-.3,'clack',0,.6);
});
