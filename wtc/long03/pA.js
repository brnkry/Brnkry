// ================= PART A: hook (outdoor, cold morning driveway) =================
const PB=Gs('b1')-.15;
const hook=g();
const skyA=el('rect',{x:0,y:0,width:1920,height:1080,fill:'url(#dawn)'},hook);const skyB=el('rect',{x:0,y:0,width:1920,height:1080,fill:'url(#dawn2)',opacity:0},hook);
const stars=[...Array(40)].map((_,i)=>el('circle',{cx:(i*211)%1920,cy:(i*97)%520,r:1.5+(i%3)*.7,fill:'#FFFFFF',opacity:.6},hook));
// far hills + trees
el('path',{d:'M0 640 Q260 560 520 610 Q800 660 1080 590 Q1380 520 1920 600 L1920 760 L0 760 Z',fill:'#3B4A70',opacity:.8},hook);
[...Array(9)].forEach((_,i)=>{const x=60+i*120+(i%2)*30,h=110+(i%3)*30;const tr_=g(hook,{transform:`translate(${x} 650)`});el('path',{d:`M0 ${-h} L${h*.32} 0 L${-h*.32} 0 Z`,fill:'#2A3658'},tr_);el('path',{d:`M0 ${-h} L${h*.16} ${-h*.5} L${-h*.16} ${-h*.5} Z`,fill:'#E8EEF6',opacity:.9},tr_)});
// ground (snow) + driveway
el('rect',{x:0,y:740,width:1920,height:340,fill:'#DDE6F2'},hook);el('path',{d:'M0 740 Q480 728 960 740 T1920 736 L1920 760 L0 760 Z',fill:'#F4F7FB'},hook);
el('path',{d:'M180 1080 L380 770 L1000 770 L1250 1080 Z',fill:'#AEB9CC'},hook);el('path',{d:'M380 770 L1000 770 L1012 786 L372 786 Z',fill:'#C7D0DE'},hook);
// house
const house=g(hook);el('rect',{x:1180,y:420,width:620,height:340,fill:'#3A3550'},house);el('rect',{x:1180,y:420,width:620,height:22,fill:'#000',opacity:.2},house);
el('path',{d:'M1130 430 L1490 200 L1850 430 Z',fill:'#2A2540'},house);el('path',{d:'M1120 436 L1490 196 L1860 436',fill:'none',stroke:'#F4F7FB','stroke-width':26,'stroke-linejoin':'round','stroke-linecap':'round'},house);
el('rect',{x:1640,y:236,width:60,height:110,fill:'#2A2540'},house);el('rect',{x:1632,y:228,width:76,height:20,rx:8,fill:'#F4F7FB'},house);
const chim=puffs(house,7,'#C9D3E3');
const doorG=g(house);el('rect',{x:1236,y:580,width:112,height:180,rx:6,fill:'#5A3A2A'},doorG);const doorLight=el('rect',{x:1236,y:580,width:112,height:180,rx:6,fill:'#FFD27A',opacity:0},doorG);el('circle',{cx:1330,cy:675,r:6,fill:'#E9C46A'},doorG);
const winGlow=el('ellipse',{cx:1570,cy:545,rx:260,ry:180,fill:'url(#warmWin)'},house);
const winG=g(house,{transform:'translate(1570 545)'});el('rect',{x:-162,y:-112,width:324,height:224,rx:10,fill:'#F4F7FB'},winG);
const room=g(winG,{'clip-path':'url(#winClip)'});el('rect',{x:-150,y:-100,width:300,height:200,fill:'#F2C77E'},room);el('rect',{x:-150,y:30,width:300,height:70,fill:'#D9A35A'},room);
el('rect',{x:70,y:-80,width:60,height:80,rx:4,fill:'#C98A4A'},room);el('circle',{cx:-100,cy:-60,r:22,fill:'#FFF3D6'},room);
const homeGuy=makeGuy(g(room));homeGuy.parentNode.setAttribute('transform','translate(-10 72) scale(.42)');
const mug=g(homeGuy.arm.R.held);el('rect',{x:-4,y:-96,width:62,height:74,rx:10,fill:RED},mug);el('path',{d:'M58 -80 q26 4 22 26 q-4 18 -22 14',fill:'none',stroke:RED,'stroke-width':10},mug);el('rect',{x:4,y:-88,width:46,height:10,rx:4,fill:'#7A2232'},mug);
const mugSteam=[0,1,2].map(i=>el('path',{fill:'none',stroke:'#FFFFFF','stroke-width':5,'stroke-linecap':'round',opacity:0},mug));
el('path',{d:'M0 -112 V112 M-162 0 H162',stroke:'#F4F7FB','stroke-width':12},winG);
el('rect',{x:-186,y:110,width:372,height:18,rx:6,fill:'#F4F7FB'},winG);
// footprints from the car door to the house door
const steps=[...Array(12)].map((_,i)=>{const k=i/11;const x=lerp(820,1280,k),y=lerp(860,772,k)+(i%2?10:-10);return el('ellipse',{cx:x,cy:y,rx:17,ry:9,fill:'#7D8FAE',opacity:0,transform:`rotate(-8 ${x} ${y})`},hook)});
// the car
const carG=g(hook);const beam=el('path',{d:'M0 -20 L560 -150 L560 150 Z',fill:'url(#beam)',opacity:0},carG);
const carBody=g(carG);const car=makeCar(carBody,{body:LIME,ink:ASPH,acc:'#FFF6D0'});car.setAttribute('transform','scale(.6)');
el('path',{d:'M-180 -76 Q-120 -98 30 -100 Q140 -98 176 -70 Q120 -88 30 -90 Q-110 -88 -180 -76 Z',fill:'#FFFFFF'},carBody);// snow on the roof
el('path',{d:'M-102 -78 Q-70 -98 0 -100 L36 -100 L36 -80 Z',fill:'#CFE3F5',opacity:.55},carBody);el('path',{d:'M48 -100 L114 -100 Q140 -96 166 -78 L48 -78 Z',fill:'#CFE3F5',opacity:.55},carBody);
el('rect',{x:-286,y:28,width:30,height:12,rx:5,fill:'#3A3A46'},carBody);// exhaust pipe
const exh=puffs(carG,14,'#EEF3F9');
// HUD + overlays
const hookDim=el('rect',{x:0,y:0,width:1920,height:1080,fill:'#0B0E18',opacity:0},hook);
const thCard=g(hook);el('rect',{x:-150,y:-200,width:300,height:400,rx:30,fill:'#141B2E',opacity:.88},thCard);const thA=therm(thCard,190);thA.setAttribute('transform','translate(-50 0) scale(.9)');const thFl=flake(thCard,.55);thFl.setAttribute('transform','translate(70 -60) scale(.55)');
const thBig=txt(thCard,60,100,84,'bold',"20°");thBig.setAttribute('fill',ICE);txt(thCard,60,146,30,'mic mut','F');thA.lab.style.display='none';
const timer=g(hook);el('rect',{x:-170,y:-56,width:340,height:112,rx:56,fill:'#141B2E',opacity:.92},timer);const tDot=el('circle',{cx:-118,cy:0,r:14,fill:RED},timer);txt(timer,-90,-10,22,'mic mut','IDLING','start');const tTxt=txt(timer,-90,34,52,'bold ink','0:00','start');
const pol=[['DAD',-7],['GRANDPA',6]].map(([lab,rot],i)=>{const p_=g(hook);el('rect',{x:-170,y:-200,width:340,height:390,rx:8,fill:'#F7F2E6'},p_);el('rect',{x:-150,y:-180,width:300,height:270,fill:'url(#sepia)'},p_);
  el('rect',{x:-150,y:40,width:300,height:50,fill:'#B79268'},p_);const oc=g(p_,{transform:'translate(-6 20)'});
  if(i===0){el('path',{d:'M-120 20 L-120 -10 L-80 -14 L-50 -50 L60 -50 L90 -14 L124 -8 L124 20 Z',fill:'#5E4630'},oc)}else{el('path',{d:'M-130 20 L-130 -6 L-96 -10 L-74 -44 L44 -44 L70 -10 L130 -6 L130 20 Z',fill:'#5E4630'},oc);el('rect',{x:-134,y:8,width:268,height:8,fill:'#D9C4A0'},oc)}
  [-80,80].forEach(x=>el('circle',{cx:x,cy:22,r:22,fill:'#3A2A1C'},oc));const pp=puffs(p_,6,'#F3E6CF');p_.pp=pp;
  txt(p_,0,150,44,'bold',lab).setAttribute('fill','#3A2A1C');p_.rot=rot;return p_});
const respP=g(hook);const respC=pill(respP,'THE RESPONSIBLE THING?',LIME,ASPH,520,32);const respChk=CHECK(respP,1.1);respChk.setAttribute('transform','translate(250 -36) scale(1.1)');
const yrs=g(hook);const yrC=card(yrs,620,300,'#141B2E');txt(yrC,0,-70,28,'mic mut','ALMOST ANY CAR BUILT IN THE');const yrN=txt(yrC,-60,70,150,'bold acc','30');txt(yrC,100,40,56,'bold ink','LAST');txt(yrC,100,96,40,'bold ink','YEARS');
const harm=g(hook);const harmS=stamp(harm,'MORE HARM THAN GOOD',RED,900);
const hud=[0,1,2].map(i=>{const c=card(hook,380,300,'#141B2E');return c});
const hFuel=fuelGauge(hud[0],110);hFuel.setAttribute('transform','translate(0 40)');txt(hud[0],0,-96,26,'mic mut','FUEL BURNED');
const odo=g(hud[1],{transform:'translate(0 20)'});el('rect',{x:-150,y:-56,width:300,height:112,rx:14,fill:'#0B0E18'},odo);txt(odo,40,26,80,'bold acc','0.0');txt(odo,40,-70,26,'mic mut','DISTANCE');txt(odo,130,26,30,'mic mut','MI');
const hTemp=tempGauge(hud[2],110);hTemp.setAttribute('transform','translate(0 50)');txt(hud[2],0,-96,26,'mic mut','ENGINE TEMP');const stillCold=pill(hud[2],'STILL COLD',COLD,CHALK,240,26);stillCold.setAttribute('transform','translate(0 120)');
const tit=g(hook);const tit1=txt(tit,0,0,92,'bold ink','WHERE DID THIS');const tit1b=txt(tit,0,100,92,'bold acc','HABIT COME FROM?');
const tit2=txt(tit,0,0,92,'bold ink','WHAT SHOULD YOU');const tit2b=txt(tit,0,100,92,'bold acc','ACTUALLY DO?');
const rew=g(tit);el('circle',{r:70,fill:'none',stroke:CHALK,'stroke-width':10},rew);const rewH=el('rect',{x:-5,y:-55,width:10,height:58,rx:5,fill:CHALK},rew);el('path',{d:'M-90 -20 L-70 10 L-50 -20 Z',fill:CHALK},rew);
function nozzle(p,lab,col){const n=g(p);el('rect',{x:-70,y:-150,width:140,height:190,rx:30,fill:col},n);el('path',{d:'M40 -110 L170 -150 L180 -126 L60 -80 Z',fill:'#3A3A46'},n);el('path',{d:'M-30 40 Q-30 110 -90 130',fill:'none',stroke:'#3A3A46','stroke-width':22},n);txt(n,0,-46,40,'bold',lab).setAttribute('fill',ASPH);return n}
const fuels=g(hook);const nozGas=nozzle(fuels,'GAS',CHALK);const nozDsl=nozzle(fuels,'DIESEL',DIESEL);nozDsl.lastChild.setAttribute('font-size','30');
const endBar=g(fuels);el('rect',{x:-420,y:-12,width:840,height:24,rx:12,fill:'#2A2A33'},endBar);const endFill=el('rect',{x:-420,y:-12,width:0,height:24,rx:12,fill:DIESEL},endBar);const endFlag=g(endBar,{transform:'translate(420 0)'});el('circle',{r:30,fill:DIESEL},endFlag);
const stayT=txt(endBar,-420,-36,30,'mic ink','STAY TO THE END','start');
const diffP=pill(fuels,'DIFFERENT RULES',DIESEL,ASPH,380,30);
const snowA=snowfall(hook,70);

KEYS.push([0,'rest']);
RENDER.push(t=>{
 if(t>PB+.5){show(0,hook);return}show(1,hook);
 const out=1-P(t,PB-.05,.45);hook.style.opacity=out;
 black.style.opacity=1-P(t,0,.6);
 const tl=eio(P(t,Gs('a3'),Gs('a6')-Gs('a3')));skyB.setAttribute('opacity',tl*.85);stars.forEach(s=>s.setAttribute('opacity',.6*(1-tl)));
 snowA.upd(t,.8);chim.upd(t,1670,220,-30,-50,3,1,18);
 // thermometer sign
 const t20=W_('a1','20')-.25;tr(thCard,250,300,pop(t,t20),0,on(t,t20)*(1-P(t,Gs('a4')-.3,.3)));thA.set(lerp(40,20,eo(P(t,t20,.8))));
 // car start, idle shake, headlights, exhaust
 const ts=W_('a2','start');const run=t>ts;carG.setAttribute('transform','translate(620 697)');
 carBody.setAttribute('transform',`translate(0 ${run?1.4*Math.sin(t*47):0})`);beam.setAttribute('opacity',run?.8*eo(P(t,ts,.3)):0);beam.setAttribute('transform','translate(300 -20)');
 exh.upd(t,-300,40,-70,-30,2.4,run?eo(P(t,ts,.6)):0,22);
 // walk inside: footprints, door light
 const tw=W_('a2','walk');steps.forEach((s,i)=>s.setAttribute('opacity',.8*on(t,tw+i*.12)));
 const ti=W_('a2','inside');doorLight.setAttribute('opacity',V(t,ti-.1,ti+.6,.1,.15));
 // guy at the window with coffee
 const tg=ti+.5;const gk=eo(P(t,tg,.5));const tc=W_('a3','coffee')-.1;const sip=V(t,tc,tc+1.4,.35,.4);
 homeGuy.parentNode.setAttribute('transform',`translate(${lerp(140,-10,gk)} 72) scale(.42)`);homeGuy.style.opacity=gk;
 homeGuy.set({mouth:0,smile:.6+.2*sip,browUp:.1,eyes:sip>.6?.25:blinkAt(t,3.1,.3),look:[-.6,.1],tilt:-3*sip,hands:{L:{x:-200,y:330,shape:'fist'},R:{x:lerp(150,60,sip),y:lerp(110,-30,sip),shape:'fist'}}});
 mugSteam.forEach((s,i)=>{const x=10+i*16;s.setAttribute('d',`M${x} -104 q${10*Math.sin(t*3+i)} -20 0 -40 q${-10*Math.sin(t*3+i)} -20 0 -40`);s.setAttribute('opacity',.6*(1-sip))});
 // idle timer: runs to 10:00 (time lapse)
 const tt0=W_('a3','warms')-.2,tt1=Gs('a6');const sec=600*eio(P(t,W_('a3','10')-.1,tt1-W_('a3','10')-.6));
 tr(timer,620,470,pop(t,tt0),0,on(t,tt0)*(1-P(t,Gs('a11')-.3,.3)));tTxt.textContent=Math.floor(sec/60)+':'+String(Math.floor(sec%60)).padStart(2,'0');tDot.style.opacity=(t>tt1)?1:(Math.sin(t*8)>0?1:.25);tDot.setAttribute('fill',t>W_('a6','truth')-.1?RED:LIME);
 // dim layer for overlays
 hookDim.setAttribute('opacity',Math.max(.55*V(t,Gs('a4')-.1,Gs('a11')+.2),.78*P(t,Gs('a11')-.3,.4)));
 // polaroids
 const td=[W_('a4','dad'),W_('a4','His')].map(x=>x-.3);pol.forEach((p_,i)=>{const k=eo(P(t,td[i],.45));const o=1-P(t,W_('a6','truth')-.1,.3);
  tr(p_,[700,1180][i],lerp(-260,380,k),1,p_.rot+(1-k)*20,on(t,td[i])*o);p_.pp.upd(t,-150,70,-40,-30,2,1,14)});
 const tr_=W_('a5','responsible')-.3;tr(respP,960,740,pop(t,tr_),0,on(t,tr_)*(1-P(t,W_('a6','truth')-.1,.25)));
 if(t>W_('a6','truth')-.1&&t<W_('a6','truth')+.25)flash.style.opacity=.12*(1-P(t,W_('a6','truth')-.1,.35)),flash.style.background=RED;
 const ty_=W_('a7','30')-.4;tr(yrs,960,380,pop(t,Gs('a7')-.05),0,V(t,Gs('a7')-.05,Gs('a8')));yrN.textContent='30';yrN.style.opacity=eo(P(t,ty_,.3));yrN.setAttribute('transform',`translate(-60 70) scale(${back(P(t,ty_,.4))}) translate(60 -70)`);
 const th_=W_('a8','harm')-.2;tr(harm,960,380,lerp(1.5,1,eo(P(t,th_,.25))),-6,on(t,th_)*(1-P(t,Gs('a9')-.2,.25)));
 // HUD tiles
 const hb=W_('a9','burned')-.3,hn=W_('a9','nowhere')-.3,hw=W_('a10','warm')-.4;const hout=1-P(t,Gs('a11')-.25,.3);
 [[hb,530],[hn,960],[Gs('a10')-.1,1390]].forEach(([a,x],i)=>tr(hud[i],x,390,pop(t,a),0,on(t,a)*hout));
 hFuel.set(lerp(.62,.5,eo(P(t,hb+.2,1.2))));hTemp.set(lerp(0,.12,eo(P(t,Gs('a10'),1.0))));tr(stillCold,0,120,pop(t,hw),0,on(t,hw));
 // titles
 const t1=Gs('a11')-.05,t2=W_('a12','actually')-.35,t3=Gs('a13')-.05;
 const k1=V(t,t1,t2+.1,.35,.25),k2=V(t,t2,t3,.3,.25);tit.setAttribute('transform','translate(960 380)');
 [tit1,tit1b].forEach(e=>e.style.opacity=k1);[tit2,tit2b].forEach(e=>e.style.opacity=k2);tit1.setAttribute('y',-20-30*(1-eo(P(t,t1,.4))));tit1b.setAttribute('y',80);tit2.setAttribute('y',-20);tit2b.setAttribute('y',80+30*(1-eo(P(t,t2,.4))));
 tr(rew,0,-200,k1,0,k1);rewH.setAttribute('transform',`rotate(${-t*400})`);
 // gas vs diesel
 const kf=V(t,t3,PB+.2,.3,.2);show(kf,fuels);fuels.style.opacity=kf;fuels.setAttribute('transform','translate(960 400)');
 const tdz=W_('a13','diesel')-.3;tr(nozGas,-220,0,pop(t,t3),0,1-.6*on(t,tdz));tr(nozDsl,220,0,pop(t,t3+.1)*(1+.1*eo(P(t,tdz,.3))),0,1);
 const tend=W_('a13','end')-.6;tr(endBar,0,230,1,0,on(t,tend-.2));endFill.setAttribute('width',840*eio(P(t,tend,1.0)));tr(endFlag,420,0,pop(t,tend+.8),0,1);
 const tdf=W_('a14','different')-.3;tr(diffP,220,-230,pop(t,tdf),-4,on(t,tdf));
 capMode('wide');
});
EVF.push(A=>{
 A(0.2,'wind',PB,.15);A(W_('a1','20')-.25,'pop',0,.5);
 A(W_('a2','start')-.05,'key',0,.6);A(W_('a2','start')+.15,'starter',.7,.35);A(W_('a2','start')+.8,'idle',PB-W_('a2','start')-.6,.12);
 A(W_('a2','inside')+.55,'clunk',0,.45);A(W_('a3','coffee')+.25,'slurp',.65,.45);A(W_('a3','warms')-.2,'pop',0,.45);A(W_('a3','10')-.1,'gearticks',Gs('a6')-W_('a3','10')-.5,.35);
 A(W_('a4','dad')-.3,'whoosh',.35,.35);A(W_('a4','His')-.3,'whoosh',.35,.35);A(W_('a5','responsible')-.3,'check',0,.6);
 A(W_('a6','truth')-.1,'stop',0,.5);A(Gs('a7')-.05,'pop',0,.5);A(W_('a8','harm')-.2,'thud',0,.45);
 A(W_('a9','burned')-.3,'pop',0,.5);A(W_('a9','nowhere')-.3,'pop',0,.5);A(Gs('a10')-.1,'pop',0,.5);
 A(Gs('a11')-.1,'whoosh',.45,.4);A(W_('a12','actually')-.35,'whoosh',.35,.3);A(Gs('a13')-.1,'pop',0,.5);A(W_('a13','diesel')-.3,'pop',0,.6);A(W_('a13','end')-.6,'riser',1.0,.25);
 A(W_('a14','different')-.3,'check',0,.6);A(PB-.1,'whoosh',.5,.45);
});
