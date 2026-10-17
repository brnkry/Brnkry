// ================= PART B: where the habit came from (carburetor vs fuel injection) =================
const PC=Gs('c1')-.1;
// carburetor cutaway
const carb=g();const carbIn=g(carb);
el('path',{d:'M-190 -280 L-110 -280 L-110 -90 Q-70 0 -110 90 L-110 280 L-190 280 Z',fill:'#6A6A76'},carbIn);
el('path',{d:'M190 -280 L110 -280 L110 -90 Q70 0 110 90 L110 280 L190 280 Z',fill:'#6A6A76'},carbIn);
const throat=el('path',{d:'M-110 -280 L110 -280 L110 -90 Q70 0 110 90 L110 280 L-110 280 L-110 90 Q-70 0 -110 -90 Z',fill:'#1B1B21'},carbIn);carb.insertBefore(throat,carbIn);carbIn.insertBefore(throat,carbIn.firstChild);
const frost=el('path',{d:'M-110 -90 Q-70 0 -110 90 M110 -90 Q70 0 110 90',fill:'none',stroke:ICE,'stroke-width':10,opacity:0},carbIn);
const bowl=g(carbIn,{transform:'translate(300 20)'});el('rect',{x:-110,y:-120,width:220,height:240,rx:20,fill:'#6A6A76'},bowl);el('rect',{x:-90,y:-100,width:180,height:200,rx:12,fill:'#1B1B21'},bowl);
const fuelLvl=el('rect',{x:-90,y:-10,width:180,height:110,rx:8,fill:AMBER,opacity:.85},bowl);const floatB=el('rect',{x:-40,y:-30,width:80,height:30,rx:10,fill:'#9AA0AE'},bowl);txt(bowl,0,160,24,'mic mut','FUEL BOWL');
el('path',{d:'M190 70 L210 70 L210 70 M-4 0 L190 0',stroke:'#9AA0AE','stroke-width':16,fill:'none'},carbIn);el('path',{d:'M-4 0 L190 0',stroke:AMBER,'stroke-width':6,fill:'none'},carbIn);
const choke=el('rect',{x:-100,y:-7,width:200,height:14,rx:7,fill:'#C9CED8'},g(carbIn,{transform:'translate(0 -230)'}));const throttle=el('rect',{x:-100,y:-7,width:200,height:14,rx:7,fill:'#C9CED8'},g(carbIn,{transform:'translate(0 220)'}));
const airP=[...Array(16)].map(()=>el('path',{d:'M0 -14 L0 14 M-8 6 L0 14 L8 6',fill:'none',stroke:ICE,'stroke-width':5,'stroke-linecap':'round',opacity:0},carbIn));
const drops=[...Array(26)].map(()=>el('circle',{r:4,fill:AMBER,opacity:0},carbIn));
const wallDrops=[...Array(8)].map((_,i)=>el('ellipse',{cx:(i%2?1:-1)*(88+((i*13)%10)),cy:30+i*24,rx:9,ry:14,fill:AMBER,opacity:0},carbIn));
txt(carb,-260,-250,26,'mic mut','AIR IN','end');txt(carb,0,330,26,'mic mut','TO THE ENGINE');
const carbLab=pill(carb,'CARBURETOR',GRAPH,CHALK,300);const carbSnow=flake(carb,.7);const vapP=pill(carb,"DOESN'T VAPORIZE",COLD,CHALK,340);
const sepiaT=el('rect',{x:-420,y:-420,width:840,height:840,rx:40,fill:SEPIA,opacity:0,style:'mix-blend-mode:color'},carb);
const necS=stamp(carb,'NECESSARY',AMBER,460);const backThen=txt(carb,0,0,30,'mic','BACK THEN');backThen.setAttribute('fill',AMBER);
// engine rpm trace monitor
const mon=g();el('rect',{x:-230,y:-150,width:460,height:300,rx:24,fill:'#0E0E12',stroke:'#30303A','stroke-width':6},mon);txt(mon,-200,-110,22,'mic mut','ENGINE SPEED','start');
const trace=el('path',{fill:'none',stroke:LIME,'stroke-width':6,'stroke-linejoin':'round'},mon);const monChips=['STUMBLE','HESITATE','STALL'].map((s,i)=>pill(mon,s,i===2?RED:'#3A3A46',CHALK,i===2?130:170,22));
// year counter + injector
const yr=g();const yrCard=card(yr,520,200,'#22222A');const yrT=txt(yr,0,40,120,'bold ink','1985');const yrLab=txt(yr,0,-120,28,'mic mut','EVERY NEW CAR SOLD IN AMERICA');
function injector(p,s=1){const j=g(p,{transform:`scale(${s})`});el('rect',{x:-40,y:-200,width:80,height:60,rx:12,fill:'#2A2A33'},j);el('rect',{x:-56,y:-150,width:112,height:180,rx:24,fill:'#5A6A86'},j);el('rect',{x:-56,y:-60,width:112,height:22,fill:'#3E4A60'},j);
  el('path',{d:'M-30 30 L30 30 L14 110 L-14 110 Z',fill:'#9AA0AE'},j);el('rect',{x:-8,y:108,width:16,height:20,rx:4,fill:'#C9CED8'},j);
  const spray=g(j,{transform:'translate(0 128)'});const mist=[...Array(30)].map((_,i)=>el('circle',{r:3+(i%3),fill:AMBER},spray));j.spray=spray;j.mist=mist;
  j.upd=(t,k,rate=0)=>{mist.forEach((m,i)=>{const ph=((t*(1.2+rate)+i/30*1.0))%1;const a=(-28+56*((i*37)%30)/30)*Math.PI/180;const d=ph*170;m.setAttribute('cx',Math.sin(a)*d);m.setAttribute('cy',Math.cos(a)*d);m.setAttribute('opacity',k*(1-ph)*.9)})};return j}
const carRow=g(yr);[...Array(5)].forEach((_,i)=>carIcon(carRow,.13).setAttribute('transform',`translate(${(i-2)*150} 0)`));const inj1=injector(yr,.9);const fiP=pill(yr,'FUEL INJECTION',LIME,ASPH,340,30);
// ECU + sensors
const ecuG=g();const ecuLines=[[-330,-210],[330,-210]].map(()=>el('path',{fill:'none',stroke:'#3A3A46','stroke-width':8},ecuG));
const pulses=[0,1].map(()=>[...Array(3)].map(()=>el('circle',{r:9,fill:LIME,opacity:0},ecuG)));
const ecu=g(ecuG);el('rect',{x:-150,y:-110,width:300,height:220,rx:24,fill:'#2A2A33'},ecu);[-120,-80,-40,0,40,80,120].forEach(x=>{el('rect',{x:x-6,y:-136,width:12,height:28,rx:3,fill:'#9AA0AE'},ecu);el('rect',{x:x-6,y:108,width:12,height:28,rx:3,fill:'#9AA0AE'},ecu)});
const scr=g(ecu);el('rect',{x:-110,y:-70,width:220,height:110,rx:12,fill:'#0E0E12'},scr);const scrT=txt(scr,0,-2,30,'bold acc','COMPUTER');const scrT2=txt(scr,0,30,22,'mic mut','');txt(ecu,0,86,22,'mic mut','ENGINE COMPUTER');
const sensors=[['ENGINE TEMP','th'],['AIR TEMP','air']].map(([lab,k],i)=>{const s=g(ecuG,{transform:`translate(${i?330:-330} -230)`});el('circle',{r:96,fill:'#22222A'},s);el('circle',{r:96,fill:'none',stroke:COLD,'stroke-width':6},s);
  if(k==='th'){const T=therm(s,90);T.setAttribute('transform','translate(0 -14) scale(.6)');T.set(20);T.lab.style.display='none'}else{[-24,0,24].forEach((y,j)=>el('path',{d:`M-50 ${y} Q-10 ${y-18} 20 ${y} T60 ${y}`,fill:'none',stroke:ICE,'stroke-width':8,'stroke-linecap':'round'},s))}
  txt(s,0,140,26,'mic ink',lab);const v=txt(s,0,62,30,'bold',"20°F");v.setAttribute('fill',ICE);return s});
const inj2=injector(ecuG,.75);const pulseG=g(ecuG);el('rect',{x:-260,y:-60,width:520,height:120,rx:18,fill:'#0E0E12'},pulseG);const pw=el('path',{fill:'none',stroke:AMBER,'stroke-width':6,'stroke-linejoin':'round'},pulseG);txt(pulseG,-240,-30,20,'mic mut','INJECTOR','start');
const mtps=pill(ecuG,'MANY TIMES PER SECOND',AMBER,ASPH,440,28);
const knowP=g();const coldMode=card(knowP,520,240,'#0E0E12');const cmF=flake(coldMode,.55);cmF.setAttribute('transform','translate(-170 0) scale(.55)');txt(coldMode,50,-14,44,'bold acc','COLD START');txt(coldMode,50,36,28,'mic mut','MODE: ON');
const forYou=pill(knowP,'HANDLED FOR YOU',LIME,ASPH,360,30);const fyChk=CHECK(knowP,1.2);

KEYS.push([PB+.2,'mid'],[Gs('b3'),'top'],[Gs('b4'),'right'],[Gs('b5'),'one'],[Gs('b6'),'mid'],[Gs('b7'),'top'],[Gs('b8'),'low'],[Gs('b9'),'mid'],[W_('b9','handles')-.2,'thumb']);
RENDER.push(t=>{
 if(t<PB-.6||t>PC+.5){show(0,carb,mon,yr,ecuG,knowP);return}capMode('studio');
 // carburetor b1..b5
 if(vis(carb,t,PB,Gs('b6')-.1)>0){const k0=pop(t,PB,.5);const sh=Gs('b4')<t&&t<W_('b4','until')?(Math.sin(t*40)*4*(t<W_('b4','stall')+.3?1:0)):0;
  carb.setAttribute('transform',`translate(${1060+sh} 470) scale(${.84*k0})`);tr(carbLab,0,-360,1,0,1);
  const tAir=W_('b2','air')-.3,tFuel=W_('b2','fuel')-.3,tCold=W_('b3','cold')-.2,tVap=W_('b3','vaporize')-.3;
  airP.forEach((a,i)=>{const ph=((t*.9)+i/16)%1;const x=((i*47)%160)-80;const y=-300+ph*600;const nar=1-.35*Math.exp(-(y*y)/(90*90));a.setAttribute('transform',`translate(${x*nar} ${y})`);a.setAttribute('opacity',on(t,tAir)*.8*Math.sin(Math.PI*ph))});
  const cold=eo(P(t,tVap,.6));frost.setAttribute('opacity',.8*eo(P(t,tCold,.5)));
  drops.forEach((d,i)=>{const ph=((t*1.3)+i/26)%1;const sp=(((i*29)%26)/26-.5);const x=lerp(sp*130*ph,sp*40,cold),y=ph*lerp(260,120,cold);d.setAttribute('cx',x);d.setAttribute('cy',y);d.setAttribute('r',lerp(3,10,cold));d.setAttribute('opacity',on(t,tFuel)*(1-ph)*lerp(.9,.8,cold))});
  wallDrops.forEach((w,i)=>w.setAttribute('opacity',cold*eo(P(t,tVap+.3+i*.12,.3))));
  fuelLvl.setAttribute('y',-10+4*Math.sin(t*2));choke.parentNode.setAttribute('transform',`translate(0 -230) rotate(${lerp(0,-70,eo(P(t,tCold,.6)))})`);throttle.parentNode.setAttribute('transform',`translate(0 220) rotate(${30+10*Math.sin(t*2)})`);
  tr(carbSnow,-300,-200,.7*pop(t,tCold),t*20,on(t,tCold));tr(vapP,0,-300,pop(t,tVap),0,on(t,tVap)*(1-on(t,Gs('b5')-.1)));carbLab.style.opacity=t>tVap?0:1;
  const tb=Gs('b5')-.05;sepiaT.setAttribute('opacity',.9*eo(P(t,tb,.5)));const tn=W_('b5','necessary')-.25;tr(necS,0,0,lerp(1.6,1,eo(P(t,tn,.25))),-8,on(t,tn));tr(backThen,0,-90,1,-8,on(t,tn));
  // engine trace monitor (b4)
  const km=vis(mon,t,Gs('b4')-.1,Gs('b5')-.1);if(km>0){tr(mon,1690,300,.78*pop(t,Gs('b4')-.1),0,km);const t1=W_('b4','stumble'),t2=W_('b4','hesitate'),t3=W_('b4','stall'),t4=W_('b4','warmed');
   let d='';for(let i=0;i<=80;i++){const x=-200+i*5;const tx=t-(80-i)*.03;let y=-10*Math.sin(tx*14);if(tx>t1-.1&&tx<t4)y+=28*Math.sin(tx*37)*(tx<t2?1:.4);if(tx>t2-.1&&tx<t3)y+=40*eo(P(tx,t2,.3));if(tx>t3-.1&&tx<t4+.2)y=80;if(tx>=t4+.2)y=-10*Math.sin(tx*14);d+=(i?'L':'M')+x+' '+(20+y).toFixed(1)}
   trace.setAttribute('d',d);trace.setAttribute('stroke',t>t3-.1&&t<t4+.2?RED:LIME);
   [t1,t2,t3].forEach((a,i)=>tr(monChips[i],[-150,20,175][i],205,pop(t,a-.2),0,on(t,a-.2)))}}
 // year + injection b6
 if(vis(yr,t,Gs('b6')-.1,Gs('b7')-.1)>0){yr.setAttribute('transform',`translate(${CX} 0)`);tr(yrCard,0,220,pop(t,Gs('b6')-.1),0,1);const ty=W_('b6','nineties')-.5;yrT.textContent=String(Math.round(lerp(1985,1995,eio(P(t,ty,.8)))));yrT.setAttribute('transform','translate(0 220)');
  tr(yrLab,0,0,1,0,on(t,W_('b6','every')-.2));yrLab.setAttribute('y',-100+220);const te=W_('b6','every')-.2;tr(carRow,0,450,1,0,on(t,te)*(1-P(t,W_('b6','injection')-.8,.3)));[...carRow.children].forEach((c,i)=>c.style.opacity=eo(P(t,te+i*.12,.25)));
  const ti=W_('b6','injection')-.7;tr(inj1,0,520,.9*pop(t,ti),0,on(t,ti));inj1.upd(t,on(t,ti),.8);tr(fiP,250,560,pop(t,ti+.2),0,on(t,ti+.2))}
 // ECU b7..b8
 if(vis(ecuG,t,Gs('b7')-.1,Gs('b9')-.1)>0){ecuG.setAttribute('transform',`translate(${CX} 470)`);tr(ecu,0,0,pop(t,Gs('b7')-.1),0,1);
  const ts=[W_('b7','engine')-.3,W_('b7','air')-.3];sensors.forEach((s,i)=>{tr(s,i?330:-330,-210,pop(t,ts[i]),0,on(t,ts[i]));const L=ecuLines[i];L.setAttribute('d',`M${i?236:-236} -170 Q${i?200:-200} -90 ${i?150:-150} -40`);L.style.opacity=on(t,ts[i]+.2);
   pulses[i].forEach((p,j)=>{const ph=((t*1.2)+j/3)%1;const x=lerp(i?236:-236,i?150:-150,ph),y=lerp(-170,-40,ph);p.setAttribute('cx',x);p.setAttribute('cy',y);p.setAttribute('opacity',on(t,ts[i]+.3))})});
  const tb8=Gs('b8')-.1;const k8=eo(P(t,tb8,.5));ecu.setAttribute('transform',`translate(0 ${-60*k8}) scale(${1-.2*k8})`);
  tr(inj2,0,150,.6*pop(t,tb8+.2),0,on(t,tb8+.2));inj2.upd(t,on(t,tb8+.2)*(Math.sin(t*30)>0?1:.25),2.5);
  tr(pulseG,0,330,pop(t,tb8+.3),0,on(t,tb8+.3));{let d='';for(let i=0;i<=100;i++){const x=-230+i*4.6;const ph=((i*.08)-t*6)%1;const hi=((ph+1)%1)<.35;d+=(i?'L':'M')+x+' '+(hi?-20:30)}pw.setAttribute('d',d)}
  const tm=W_('b8','many')-.3;tr(mtps,0,250,pop(t,tm),0,on(t,tm));scrT2.textContent=t>tb8?'ADJUSTING FUEL':'READING SENSORS';scrT2.style.opacity=on(t,ts[0])}
 // b9
 if(vis(knowP,t,Gs('b9')-.1,PC+.05)>0){knowP.setAttribute('transform',`translate(${CX} 0)`);tr(coldMode,0,360,pop(t,Gs('b9')-.1),0,1);const th=W_('b9','handles')-.3;tr(forYou,0,590,pop(t,th),0,on(t,th));tr(fyChk,200,560,1.2*pop(t,th+.3),0,on(t,th+.3))}
});
EVF.push(A=>{
 A(PB+.05,'pop',0,.5);A(W_('b2','fuel')-.3,'air',2.6,.3);A(W_('b3','cold')-.2,'pop',0,.5);A(W_('b3','vaporize')-.3,'drip',0,.5);A(W_('b3','vaporize')+.1,'drip',0,.4);
 A(Gs('b4')-.1,'whoosh',.35,.3);A(W_('b4','stumble')-.1,'stutter',W_('b4','stall')-W_('b4','stumble')+.2,.45);A(W_('b4','stall')+.1,'engine_off_thunk',0,.5);
 A(W_('b5','necessary')-.25,'thud',0,.45);A(Gs('b6')-.1,'whoosh',.4,.4);A(W_('b6','nineties')-.5,'gearticks',.8,.45);A(W_('b6','injection')-.7,'inject',.7,.5);A(W_('b6','injection')-.5,'pop',0,.5);
 A(Gs('b7')-.1,'whoosh',.4,.4);A(W_('b7','engine')-.3,'pop',0,.5);A(W_('b7','air')-.3,'pop',0,.5);A(Gs('b8')+.2,'inject',1.5,.4);A(W_('b8','many')-.3,'pop',0,.5);
 A(Gs('b9')-.1,'boot',0,.5);A(W_('b9','handles')-.3,'check',0,.7);
});
