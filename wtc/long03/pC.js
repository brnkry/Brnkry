// ================= PART C: what idling a cold gas engine actually does =================
const PD=Gs('d1')-.1;
const badge=g();const bNum=[1,2,3,4].map(n=>numBadge(badge,n));const bTitle=txt(badge,80,16,46,'bold ink','','start');
// c1: idling in the cold
const idleG=g();const idTach=tach(idleG,170);const idCar=carIcon(idleG,.34,{body:LIME});const idPuffs=puffs(idleG,10,'#C9D3E3');const idFl=flake(idleG,.5);
const idP=pill(idleG,'IDLING IN THE COLD',COLD,CHALK,380,30);
// c2..c4: warm-up chart
const chartC=g();el('rect',{x:-470,y:-250,width:940,height:500,rx:28,fill:GRAPH},chartC);
const band=el('rect',{x:-400,y:-200,width:830,height:60,fill:LIME,opacity:.14},chartC);const bandT=txt(chartC,-390,-162,24,'mic acc','OPERATING TEMPERATURE','start');
el('path',{d:'M-400 -210 L-400 190 L440 190',fill:'none',stroke:'#4A4A56','stroke-width':6},chartC);txt(chartC,-420,-60,22,'mic mut','ENGINE TEMP','middle').setAttribute('transform','rotate(-90 -420 -60)');
[0,5,10].forEach(m=>txt(chartC,-400+m*84,226,22,'mic mut',m+' MIN'));
const lineIdle=el('path',{fill:'none',stroke:COLD,'stroke-width':10,'stroke-linecap':'round'},chartC);const lineDrive=el('path',{fill:'none',stroke:WARM,'stroke-width':10,'stroke-linecap':'round'},chartC);
const labIdle=pill(chartC,'IDLING',COLD,CHALK,170,24);const labDrive=pill(chartC,'DRIVING',WARM,ASPH,190,24);const heatP=pill(chartC,'VERY LITTLE HEAT',GRAPH,CHALK,330,26);
const idleT=m=>170-260*(1-Math.exp(-m/14)),driveT=m=>170-345*(1-Math.exp(-m/2.6));// y for minutes m
// c5: richer mixture
const mix=g();el('rect',{x:-420,y:-70,width:840,height:140,rx:24,fill:'#0E0E12'},mix);const mixAir=el('rect',{x:-410,y:-60,width:0,height:120,rx:18,fill:COLD},mix);const mixFuel=el('rect',{x:0,y:-60,width:0,height:120,rx:18,fill:AMBER},mix);
const mixA=txt(mix,0,14,40,'bold ink','AIR');const mixF=txt(mix,0,14,34,'bold','FUEL');mixF.setAttribute('fill',ASPH);const extra=pill(mix,'EXTRA FUEL',AMBER,ASPH,260,28);const richT=txt(mix,0,-110,30,'mic mut','COLD START: RICHER MIXTURE');
// c6..c8: cylinder wash
const cyl=g();el('rect',{x:-190,y:-300,width:40,height:470,fill:'#6A6A76'},cyl);el('rect',{x:150,y:-300,width:40,height:470,fill:'#6A6A76'},cyl);el('rect',{x:-190,y:-330,width:380,height:40,rx:8,fill:'#6A6A76'},cyl);
const filmL=el('rect',{x:-150,y:-290,width:12,height:460,fill:'#E9C46A'},cyl),filmR=el('rect',{x:138,y:-290,width:12,height:460,fill:'#E9C46A'},cyl);
const washL=el('rect',{x:-150,y:-290,width:12,height:0,fill:'#1B1B21'},cyl),washR=el('rect',{x:138,y:-290,width:12,height:0,fill:'#1B1B21'},cyl);
const piston=g(cyl);el('rect',{x:-136,y:0,width:272,height:120,rx:10,fill:'#9AA0AE'},piston);[14,32].forEach(y=>el('rect',{x:-136,y,width:272,height:7,fill:'#5A5A66'},piston));el('rect',{x:-24,y:110,width:48,height:160,rx:12,fill:'#7A7A86'},piston);
const injC=g(cyl,{transform:'translate(0 -330)'});el('rect',{x:-20,y:-60,width:40,height:70,rx:8,fill:'#5A6A86'},injC);
const cylDrops=[...Array(18)].map(()=>el('circle',{r:7,fill:AMBER,opacity:0},cyl));const wallRun=[...Array(10)].map(()=>el('ellipse',{rx:7,ry:12,fill:AMBER,opacity:0},cyl));
const pan=g(cyl,{transform:'translate(0 260)'});el('path',{d:'M-230 0 L230 0 L200 110 L-200 110 Z',fill:'#4A4A56'},pan);const panOil=el('path',{d:'M-214 40 L214 40 L200 100 L-200 100 Z',fill:'#C9962E'},pan);const panLab=txt(pan,0,82,26,'bold','ENGINE OIL');panLab.setAttribute('fill',ASPH);
const noBurn=pill(cyl,"DOESN'T BURN",AMBER,ASPH,270,26);const washP=pill(cyl,'WASHES OIL OFF THE WALLS',RED,CHALK,460,26);const dilP=pill(cyl,'DILUTED OIL',AMBER,ASPH,250,26);
const lastBar=g(cyl);el('rect',{x:-230,y:-14,width:460,height:28,rx:14,fill:'#2A2A33'},lastBar);const lastFill=el('rect',{x:-230,y:-14,width:0,height:28,rx:14,fill:COLD},lastBar);txt(lastBar,-230,-30,22,'mic mut','IDLE TIME','start');
// c9..c10: catalytic converter
function catConv(p,hot){const c=g(p);el('rect',{x:-360,y:-26,width:150,height:52,fill:'#4A4A56'},c);el('rect',{x:210,y:-26,width:150,height:52,fill:'#4A4A56'},c);
  const body=el('rect',{x:-220,y:-90,width:440,height:180,rx:80,fill:hot?'#7A4A2A':'#3E4A60'},c);const glow=el('rect',{x:-220,y:-90,width:440,height:180,rx:80,fill:'url(#heat)',opacity:hot?1:0},c);
  for(let i=0;i<9;i++)el('rect',{x:-150+i*34,y:-60,width:16,height:120,rx:4,fill:hot?'#E8A060':'#22324A'},c);
  const inP=puffs(c,7,'#5A5A66'),outP=puffs(c,7,hot?'#F4F7FB':'#5A5A66');c.inP=inP;c.outP=outP;const th=therm(c,90);th.setAttribute('transform','translate(0 -150) scale(.55)');th.set(hot?85:20,-20,90);th.lab.style.display='none';
  const lab=txt(c,-380,-60,26,'mic',hot?'HOT':'COLD','end');lab.setAttribute('fill',hot?WARM:COLD);return c}
const catG=g();const catCold=catConv(catG,false),catHot=catConv(catG,true);txt(catCold,0,140,26,'mic mut','CATALYTIC CONVERTER');
const cleanP=pill(catG,'CLEANS THE EXHAUST',LIME,ASPH,380,26);const dirtyP=pill(catG,'NOT CLEANING YET',RED,CHALK,340,26);const dirtRing=el('rect',{x:-470,y:-130,width:940,height:260,rx:40,fill:'none',stroke:RED,'stroke-width':8,opacity:0},catG);const dirtiest=stamp(catG,'DIRTIEST',RED,440);
// c11..c12: x-ray car
const xr=g();const xrCar=g(xr);const xc=makeCar(xrCar,{body:'#22324A',ink:'#0E0E12',acc:'#9ADFFF'});xc.setAttribute('transform','scale(.95)');
const roadX=g(xr);el('rect',{x:-560,y:200,width:1120,height:8,rx:4,fill:'#30303A'},roadX);const dashes=[...Array(8)].map(()=>el('rect',{y:222,width:70,height:8,rx:4,fill:'#30303A'},roadX));
const parts=[['engine',[320,0],'ENGINE'],['transmission',[90,10],'TRANSMISSION'],['bearings',[-264,86],'WHEEL BEARINGS'],['steering',[150,-90],'STEERING'],['suspension',[-264,-10],'SUSPENSION']].map(([k,[x,y],lab])=>{
  const p=g(xr,{transform:`translate(${x} ${y})`});const glow=el('circle',{r:k==='engine'?140:90,fill:'url(#heat)',opacity:0},p);let shape;
  if(k==='engine')shape=engineBlock(p,.42,'#4A5A76');if(k==='transmission'){shape=g(p);el('path',{d:'M-110 -40 L60 -60 L60 60 L-110 40 Z',fill:'#4A5A76'},shape)}
  if(k==='bearings'){shape=g(p);[0,555].forEach(dx=>{el('circle',{cx:dx,r:30,fill:'#4A5A76'},shape);el('circle',{cx:dx,r:14,fill:'#0E0E12'},shape)})}
  if(k==='steering'){shape=g(p);el('circle',{r:40,fill:'none',stroke:'#4A5A76','stroke-width':12},shape);el('rect',{x:-6,y:30,width:12,height:110,fill:'#4A5A76',transform:'rotate(-30)'},shape)}
  if(k==='suspension'){shape=g(p);[0,555].forEach(dx=>{el('path',{d:`M${dx-20} -50 l40 12 l-40 12 l40 12 l-40 12 l40 12 l-40 12`,fill:'none',stroke:'#4A5A76','stroke-width':9,'stroke-linecap':'round'},shape)})}
  const tag=pill(xr,lab,'#22324A',ICE,lab.length*17+60,24);return {k,p,glow,shape,tag,x,y}});
const onlyEng=pill(xr,'IDLING WARMS ONLY THE ENGINE',GRAPH,CHALK,520,26);const movesP=pill(xr,'THE CAR HAS TO MOVE',LIME,ASPH,400,28);
// c13..c15: fuel cost
function jug(p,s=1){const j=g(p,{transform:`scale(${s})`});const clip='jc'+Math.random().toString(36).slice(2,7);const cp=el('clipPath',{id:clip},svg.querySelector('defs'));el('path',{d:'M-110 -150 L50 -150 L110 -90 L110 170 L-110 170 Z'},cp);
  el('path',{d:'M-110 -150 L50 -150 L110 -90 L110 170 L-110 170 Z',fill:'#22222A'},j);const f=el('rect',{x:-110,y:170,width:220,height:0,fill:AMBER,'clip-path':`url(#${clip})`},j);
  el('path',{d:'M-110 -150 L50 -150 L110 -90 L110 170 L-110 170 Z',fill:'none',stroke:CHALK,'stroke-width':10,'stroke-linejoin':'round'},j);el('rect',{x:-80,y:-190,width:70,height:40,rx:8,fill:CHALK},j);
  el('path',{d:'M110 -60 Q170 -40 150 60',fill:'none',stroke:CHALK,'stroke-width':10},j);j.set=k=>{f.setAttribute('y',170-320*k);f.setAttribute('height',320*k)};j.set(0);return j}
const cost=g();const bigJug=jug(cost,1);const qT=txt(cost,0,0,64,'bold acc','');const perH=pill(cost,'PER HOUR AT IDLE',GRAPH,CHALK,330,28);const gal=txt(cost,0,0,26,'mic mut','GALLON');
const marks=[.25,.5].map(k=>{const m=g(cost);el('rect',{x:-130,y:-3,width:40,height:6,fill:CHALK},m);txt(m,-140,10,26,'bold ink',k===.25?'1/4':'1/2','end');m.k=k;return m});
const winter=g();const calW=g(winter);el('rect',{x:-110,y:-100,width:220,height:210,rx:20,fill:CHALK},calW);el('rect',{x:-110,y:-100,width:220,height:56,rx:20,fill:COLD},calW);el('rect',{x:-110,y:-64,width:220,height:20,fill:COLD},calW);
const calM=txt(calW,0,-60,28,'mic ink','DEC');const calD=txt(calW,0,60,90,'bold','1');calD.setAttribute('fill',ASPH);const tenMin=pill(winter,'10 MIN EVERY MORNING',GRAPH,CHALK,400,26);
const jugs=[...Array(5)].map(()=>jug(winter,.32));const sevP=pill(winter,'SEVERAL GALLONS',AMBER,ASPH,340,30);
const zero=g();const odoZ=card(zero,560,220,'#0E0E12');txt(odoZ,0,40,130,'bold acc','0');txt(odoZ,170,40,40,'bold ink','MILES');txt(odoZ,0,-80,24,'mic mut','DISTANCE DRIVEN');

KEYS.push([PC+.1,'mid'],[Gs('c2'),'one'],[Gs('c3'),'mid'],[W_('c4','drove')-.3,'right'],[Gs('c5'),'shrug'],[Gs('c5')+1.2,'mid'],[Gs('c6'),'top'],[Gs('c7'),'mid'],[Gs('c8'),'low'],
 [Gs('c9'),'one'],[Gs('c9')+1.2,'top'],[Gs('c10'),'mid'],[Gs('c11'),'one'],[Gs('c11')+1.2,'right'],[Gs('c12'),'mid'],[W_('c12','moves')-.3,'open'],[Gs('c13'),'mid'],[Gs('c14'),'shrug'],[Gs('c15'),'stop']);
MOODS.push([Gs('c6'),Gs('c11'),{smile:.15,browWorry:.3}],[Gs('c14'),PD,{smile:.1,browWorry:.25}]);
RENDER.push(t=>{
 if(t<PC-.5||t>PD+.5){show(0,badge,idleG,chartC,mix,cyl,catG,xr,cost,winter,zero);return}capMode('studio');
 // numbered heading
 const hs=[[Gs('c2'),Gs('c5'),'WARMS UP SLOWLY'],[Gs('c5'),Gs('c9'),'EXTRA FUEL'],[Gs('c9'),Gs('c11'),'DIRTY EXHAUST'],[Gs('c11'),Gs('c13'),'ONLY THE ENGINE WARMS']];let hv=0;
 hs.forEach(([a,b,ttl],i)=>{const v=V(t,a-.1,b-.1,.3,.25);bNum[i].style.display=v>0?'':'none';if(v>0){hv=v;tr(bNum[i],0,0,pop(t,a-.1),0,1);bTitle.textContent=ttl}});show(hv,badge);badge.style.opacity=hv;badge.setAttribute('transform','translate(840 120)');
 if(vis(idleG,t,PC,Gs('c2')-.1)>0){idleG.setAttribute('transform',`translate(${CX} 0)`);tr(idTach,-200,460,.9*pop(t,PC),0,1);idTach.set(.8+.08*Math.sin(t*9));tr(idCar,240,500,pop(t,PC+.2),0,1);idPuffs.upd(t,240-160,500+10,-70,-30,2.2,1,16);tr(idFl,240,330,.5,t*20,1);tr(idP,0,180,pop(t,PC+.3),0,1)}
 if(vis(chartC,t,Gs('c2')-.1,Gs('c5')-.1)>0){chartC.setAttribute('transform',`translate(${CX} 500) scale(.88)`);const t0=Gs('c2');const mi=lerp(0,10,eio(P(t,t0+.2,Gs('c5')-t0-.6)));
  let d='';for(let i=0;i<=40;i++){const m=mi*i/40;d+=(i?'L':'M')+(-400+m*84).toFixed(1)+' '+idleT(m).toFixed(1)}lineIdle.setAttribute('d',d);tr(labIdle,-400+mi*84+20,idleT(mi)+46,1,0,on(t,t0+.4));
  const td=W_('c4','drove')-.4;const md=lerp(0,10,eio(P(t,td,1.4)));let d2='';for(let i=0;i<=40;i++){const m=md*i/40;d2+=(i?'L':'M')+(-400+m*84).toFixed(1)+' '+driveT(m).toFixed(1)}lineDrive.setAttribute('d',d2);lineDrive.style.opacity=on(t,td);tr(labDrive,-400+Math.min(md,6)*84+40,driveT(Math.min(md,6))-44,1,0,on(t,td));
  const to=W_('c4','operating')-.3;band.setAttribute('opacity',.14+.2*V(t,to,to+1.5));tr(heatP,-140,-40,pop(t,W_('c3','heat')-.3),0,on(t,W_('c3','heat')-.3))}
 if(vis(mix,t,Gs('c5')-.1,Gs('c6')-.1)>0){mix.setAttribute('transform',`translate(${CX} 470)`);const tr_=W_('c5','richer')-.3;const k=eo(P(t,tr_,.7));const fw=lerp(90,240,k);
  mixAir.setAttribute('width',820-fw-10);mixFuel.setAttribute('x',410-fw);mixFuel.setAttribute('width',fw);mixA.setAttribute('x',(-410+410-fw-10)/2);mixF.setAttribute('x',410-fw/2);tr(richT,0,0,1,0,on(t,Gs('c5')+.2));
  tr(extra,410-fw/2,140,pop(t,W_('c5','extra')-.3),0,on(t,W_('c5','extra')-.3))}
 if(vis(cyl,t,Gs('c6')-.1,Gs('c9')-.1)>0){cyl.setAttribute('transform',`translate(${CX} 420) scale(.82)`);const py=-60+70*Math.sin(t*5);piston.setAttribute('transform',`translate(0 ${py})`);
  const tb=W_('c6','burn')-.3,tw=W_('c7','wash')-.3,tdl=W_('c7','diluting')-.3;
  cylDrops.forEach((d,i)=>{const ph=((t*1.5)+i/18)%1;const sp=((i*7)%18)/18-.5;d.setAttribute('cx',sp*220*ph);d.setAttribute('cy',-300+ph*(py+260));d.setAttribute('opacity',on(t,Gs('c6')-.1)*(1-ph*.6))});
  const kw=eo(P(t,tw,2.2));washL.setAttribute('height',400*kw);washR.setAttribute('height',400*kw);
  wallRun.forEach((w,i)=>{const ph=((t*.7)+i/10)%1;w.setAttribute('cx',i%2?144:-144);w.setAttribute('cy',-280+ph*560);w.setAttribute('opacity',on(t,tw)*(ph<.85?1:0))});
  panOil.setAttribute('fill',t>tdl?'#E0B45A':'#C9962E');panOil.style.opacity=1;
  tr(noBurn,0,-400,pop(t,tb),0,on(t,tb)*(1-on(t,tw-.1)));tr(washP,0,-400,pop(t,tw),0,on(t,tw)*(1-on(t,Gs('c8')-.1)));tr(dilP,330,330,pop(t,tdl),0,on(t,tdl));
  const tl=Gs('c8')-.1;tr(lastBar,0,-410,1,0,on(t,tl));lastFill.setAttribute('width',460*eio(P(t,tl+.3,2)))}
 if(vis(catG,t,Gs('c9')-.1,Gs('c11')-.1)>0){catG.setAttribute('transform',`translate(${CX} 0)`);const tc=W_('c9','catalytic')-.3,th=W_('c9','hot')-.3,tdt=W_('c10','dirtiest')-.3;
  tr(catCold,30,330,.8*pop(t,tc),0,on(t,tc));catCold.inP.upd(t,-330,330-300,30,-20,1.6,1,14);catCold.outP.upd(t,330,0,60,-24,1.8,1,16);
  tr(dirtyP,30,505,pop(t,W_('c9','clean')-.2),0,on(t,W_('c9','clean')-.2));
  tr(catHot,30,640,.8*pop(t,th),0,on(t,th)*(1-P(t,tdt-.1,.3)));catHot.outP.upd(t,330,0,60,-24,1.8,1,16);catHot.inP.upd(t,-330,0,30,-20,1.6,1,14);tr(cleanP,30,770,pop(t,th+.3),0,on(t,th+.3)*(1-P(t,tdt-.1,.3)));
  dirtRing.setAttribute('opacity',on(t,tdt));dirtRing.setAttribute('transform','translate(30 330)');tr(dirtiest,30,600,lerp(1.5,1,eo(P(t,tdt,.25))),-6,on(t,tdt))}
 if(vis(xr,t,Gs('c11')-.1,Gs('c13')-.1)>0){xr.setAttribute('transform',`translate(${CX} 430) scale(.8)`);const tm=W_('c12','moves')-.3;const mv=eo(P(t,tm,.6));
  xrCar.setAttribute('transform',`translate(0 ${mv?1.5*Math.sin(t*30):0})`);dashes.forEach((d,i)=>d.setAttribute('x',((i*160-t*700*mv)%1280+1280)%1280-640));
  const te=W_('c11','engine')-.3;const keys={engine:te,transmission:W_('c12','transmission')-.3,bearings:W_('c12','bearings')-.3,steering:W_('c12','steering')-.3,suspension:W_('c12','suspension')-.3};
  const tagPos={engine:[330,-250],transmission:[60,-250],bearings:[-264,250],steering:[300,-330],suspension:[-264,-250]};
  parts.forEach(p=>{const a=keys[p.k];const hot=p.k==='engine'?eo(P(t,te,.6)):mv;p.glow.setAttribute('opacity',hot);p.shape.style.opacity=on(t,p.k==='engine'?Gs('c11')-.2:a)*.95+.05;
   const [x,y]=tagPos[p.k];tr(p.tag,x,y,pop(t,a),0,on(t,a)*(p.k==='engine'?1:1));p.tag.firstChild.setAttribute('fill',hot>.5?WARM:'#22324A');p.tag.t.setAttribute('fill',hot>.5?ASPH:ICE)});
  tr(onlyEng,0,-430,pop(t,te+.3),0,on(t,te+.3)*(1-on(t,Gs('c12')-.1)));tr(movesP,0,-430,pop(t,tm),0,on(t,tm))}
 if(vis(cost,t,Gs('c13')-.1,Gs('c14')-.1)>0){cost.setAttribute('transform',`translate(${CX} 450) scale(.95)`);tr(bigJug,0,0,pop(t,Gs('c13')-.1),0,1);
  const tq=W_('c13','quarter')-.3,thf=W_('c13','half')-.3;const lv=t<thf?.25*eo(P(t,tq,.8)):lerp(.25,.5,eo(P(t,thf,.8)));bigJug.set(lv);
  marks.forEach(m=>{m.setAttribute('transform',`translate(-110 ${170-320*m.k})`);m.style.opacity=on(t,m.k===.25?tq:thf)});tr(perH,0,280,pop(t,W_('c13','hour')-.3),0,on(t,W_('c13','hour')-.3));tr(gal,0,215,1,0,on(t,tq))}
 if(vis(winter,t,Gs('c14')-.1,Gs('c15')-.1)>0){winter.setAttribute('transform',`translate(${CX} 0)`);const t0=Gs('c14');tr(calW,-300,330,pop(t,t0-.1),0,1);const dd=Math.floor(P(t,t0,3.2)*89);
  const dt=new Date(2026,11,1+dd);calM.textContent=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'][dt.getMonth()];calD.textContent=String(dt.getDate());tr(tenMin,-300,520,pop(t,t0+.1),0,1);
  const ts=W_('c14','several')-.4;jugs.forEach((j,i)=>{tr(j,120+i*95,350,.32*pop(t,t0+.3+i*.15),0,on(t,t0+.3+i*.15));j.set(eo(P(t,t0+.4+i*.5,.6)))});tr(sevP,310,560,pop(t,ts),0,on(t,ts))}
 if(vis(zero,t,Gs('c15')-.1,PD+.05)>0){tr(zero,CX,430,pop(t,Gs('c15')-.1),0,1)}
});
EVF.push(A=>{
 A(PC,'whoosh',.4,.4);A(PC+.2,'idle',3.4,.2);A(Gs('c2')-.1,'pop',0,.6);A(Gs('c2')+.2,'riser',2.2,.18);A(W_('c3','heat')-.3,'pop',0,.5);A(W_('c4','drove')-.4,'rev',1.4,.3);
 A(Gs('c5')-.1,'pop',0,.6);A(W_('c5','richer')-.3,'squeeze',.7,.4);A(W_('c5','extra')-.3,'pop',0,.5);
 A(Gs('c6')-.1,'whoosh',.4,.4);A(Gs('c6'),'inject',.7,.4);A(W_('c6','burn')-.3,'pop',0,.5);A(W_('c7','wash')-.3,'drip',0,.5);A(W_('c7','wash'),'drip',0,.4);A(W_('c7','wash')+.3,'drip',0,.35);A(W_('c7','diluting')-.3,'pop',0,.5);A(Gs('c8')-.1,'gearticks',2,.35);
 A(Gs('c9')-.1,'pop',0,.6);A(W_('c9','catalytic')-.3,'whoosh',.35,.35);A(W_('c9','clean')-.2,'pop',0,.5);A(W_('c9','hot')-.3,'bloom',.6,.4);A(W_('c10','dirtiest')-.3,'thud',0,.45);
 A(Gs('c11')-.1,'pop',0,.6);A(W_('c11','engine')-.3,'riserE',.6,.25);['transmission','bearings','steering','suspension'].forEach(w=>A(W_('c12',w)-.3,'pop',0,.5));A(W_('c12','moves')-.3,'rev',1.2,.3);
 A(Gs('c13')-.1,'whoosh',.4,.4);A(W_('c13','quarter')-.3,'pump',.8,.35);A(W_('c13','half')-.3,'pump',.8,.35);A(W_('c13','hour')-.3,'pop',0,.5);
 A(Gs('c14')-.1,'whoosh',.4,.4);A(Gs('c14'),'gearticks',3.2,.35);A(W_('c14','several')-.4,'pop',0,.6);A(Gs('c15')-.1,'thud',0,.45);
});
