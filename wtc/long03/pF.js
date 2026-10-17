// ================= PART F: diesels (4 steps) =================
const PG=Gs('g1')-.1;
const S=(e,t,a,b,f)=>{if(vis(e,t,a,b)>0)f()};
// header + step tracker
const dHead=g();const dTitle=txt(dHead,0,40,160,'bold','DIESEL');dTitle.setAttribute('fill',DIESEL);const truck=makeTruck(dHead,{body:'#3E5A44',acc:'#FFF6D0'});
const dTrack=g();const dSteps=['GLOW PLUGS','SHORT IDLE','BLOCK HEATER','FUEL'].map((s,i)=>{const c=g(dTrack,{transform:`translate(${(i-1.5)*240} 0)`});const bg=el('rect',{x:-112,y:-34,width:224,height:68,rx:34,fill:'#2A2A33'},c);const n=txt(c,-80,10,26,'bold mut',String(i+1));const tt_=txt(c,14,10,22,'mic mut',s);c.bg=bg;c.n=n;c.tt_=tt_;return c});
// cylinders (gas vs diesel)
function cylinder(p,kind){const c=g(p);el('rect',{x:-130,y:-200,width:24,height:330,fill:'#6A6A76'},c);el('rect',{x:106,y:-200,width:24,height:330,fill:'#6A6A76'},c);el('rect',{x:-130,y:-224,width:260,height:30,rx:6,fill:'#6A6A76'},c);
  const air=el('rect',{x:-106,y:-194,width:212,height:150,fill:COLD,opacity:.35},c);const flame=el('circle',{cx:0,cy:-150,r:0,fill:'url(#heat)'},c);
  const pis=g(c);el('rect',{x:-104,y:0,width:208,height:100,rx:8,fill:'#9AA0AE'},pis);el('rect',{x:-18,y:96,width:36,height:110,rx:10,fill:'#7A7A86'},pis);
  const plug=g(c,{transform:'translate(0 -224)'});if(kind==='gas'){el('rect',{x:-16,y:-80,width:32,height:60,rx:6,fill:CHALK},plug);el('rect',{x:-10,y:-24,width:20,height:30,fill:'#9AA0AE'},plug)}
  else{el('rect',{x:-14,y:-70,width:28,height:70,rx:6,fill:'#5A6A86'},plug);el('rect',{x:-6,y:0,width:12,height:16,fill:'#C9CED8'},plug)}
  const gp=g(c,{transform:'translate(70 -224) rotate(25)'});if(kind==='diesel'){el('rect',{x:-9,y:-60,width:18,height:70,rx:5,fill:'#C9CED8'},gp)}const gpTip=el('rect',{x:-6,y:6,width:12,height:28,rx:5,fill:'#9AA0AE'},gp);
  const spark=g(c,{transform:'translate(0 -186)'});[0,60,120,180,240,300].forEach(a=>el('rect',{x:-3,y:-26,width:6,height:20,rx:3,fill:LIME,transform:`rotate(${a})`},spark));
  const mist=[...Array(14)].map(()=>el('circle',{r:4,fill:AMBER,opacity:0},c));
  c.air=air;c.flame=flame;c.pis=pis;c.spark=spark;c.gpTip=gpTip;c.mist=mist;c.plug=plug;
  c.lab=txt(c,0,250,34,'bold',kind==='gas'?'GAS':'DIESEL');c.lab.setAttribute('fill',kind==='gas'?CHALK:DIESEL);return c}
const cyls=g();const gpP=pill(svg,'GLOW PLUG HEATS THE CYLINDER',WARM,ASPH,520,26);const cGas=cylinder(cyls,'gas'),cDsl=cylinder(cyls,'diesel');const noPlug=XMARK(cyls,1.2);const compP=pill(cyls,'HEAT OF COMPRESSED AIR',WARM,ASPH,440,26);
const hardP=pill(cyls,'STARTING IS HARDER',COLD,CHALK,380,26);const rulesP=pill(cyls,'THE RULES CHANGE',DIESEL,ASPH,360,28);const cylFl=flake(cyls,.6);
// step 1: key, glow plug light
const keyG=g();const ign=g(keyG);el('circle',{r:150,fill:'#22222A'},ign);el('circle',{r:70,fill:'#3A3A46'},ign);
const pos=[['OFF',-80],['ACC',-30],['ON',20],['START',70]].map(([s,a])=>{const r=118;const tt_=txt(ign,r*Math.sin(a*Math.PI/180),-r*Math.cos(a*Math.PI/180)+9,24,'mic mut',s);return {tt_,a}});
const keyB=g(ign);el('rect',{x:-16,y:-90,width:32,height:120,rx:8,fill:'#C9CED8'},keyB);el('rect',{x:-50,y:-150,width:100,height:70,rx:24,fill:'#3A3A46'},keyB);
function glowLamp(p){const l=g(p);const glow=el('circle',{r:150,fill:AMBER,opacity:0,filter:'url(#soft)'},l);
  const coilP=el('path',{d:'M-110 30 L-80 30 Q-80 -40 -50 -40 Q-20 -40 -20 30 Q-20 -40 10 -40 Q40 -40 40 30 Q40 -40 70 -40 Q100 -40 100 30 L120 30',fill:'none','stroke-width':16,'stroke-linecap':'round','stroke-linejoin':'round'},l);
  const ends=[el('path',{d:'M-110 30 L-110 70 M120 30 L120 70',fill:'none','stroke-width':16,'stroke-linecap':'round'},l)];
  l.set=v=>{const c=v>.5?AMBER:OFF;coilP.setAttribute('stroke',c);ends.forEach(e=>e.setAttribute('stroke',c));glow.setAttribute('opacity',.3*v)};l.set(0);return l}
const dash=g();el('rect',{x:-260,y:-170,width:520,height:340,rx:40,fill:'#0E0E12'},dash);el('rect',{x:-260,y:-170,width:520,height:340,rx:40,fill:'none',stroke:'#30303A','stroke-width':6},dash);
const gl=glowLamp(g(dash,{transform:'translate(0 -20) scale(.9)'}));const glLab=txt(dash,0,120,26,'mic mut','GLOW PLUG LIGHT');const waitP=pill(dash,'WAIT FOR IT TO GO OUT',AMBER,ASPH,420,26);
const pushB=g();el('circle',{r:120,fill:'#2A2A33'},pushB);const pbRing=el('circle',{r:108,fill:'none',stroke:'#4A4A56','stroke-width':12,pathLength:1000},pushB);txt(pushB,0,-8,32,'bold ink','ENGINE');txt(pushB,0,30,24,'mic mut','START');const autoP=pill(pushB,'AUTOMATIC',DIESEL,ASPH,240,26);
const crankBar=g();el('rect',{x:-330,y:-26,width:660,height:52,rx:26,fill:'#2A2A33'},crankBar);const cbFill=el('rect',{x:-330,y:-26,width:0,height:52,rx:26,fill:AMBER},crankBar);el('rect',{x:300,y:-44,width:8,height:88,fill:RED},crankBar);
const cbT=txt(crankBar,0,-60,30,'bold ink','CRANKING');const cbMax=txt(crankBar,304,84,28,'bold red','15 SEC MAX');const restP=g(crankBar);el('circle',{r:56,fill:COLD},restP);el('rect',{x:-20,y:-24,width:12,height:48,rx:4,fill:CHALK},restP);el('rect',{x:8,y:-24,width:12,height:48,rx:4,fill:CHALK},restP);txt(restP,0,100,28,'bold ink','LET IT REST');
// step 2: idle
const s2=g();const clk=g(s2);el('circle',{r:110,fill:CHALK},clk);el('circle',{r:96,fill:'#1B1B21'},clk);const hM=el('rect',{x:-5,y:-80,width:10,height:84,rx:5,fill:CHALK},clk);const hH=el('rect',{x:-6,y:-54,width:12,height:58,rx:6,fill:DIESEL},clk);const clkX=XMARK(s2,1.3);
const s2P=pill(s2,"DON'T IDLE FOR LONG",RED,CHALK,380,28);
const heatBars=g();[['GAS IDLE',.55,WARM],['DIESEL IDLE',.25,DIESEL]].forEach(([s,k,c],i)=>{const r=g(heatBars,{transform:`translate(0 ${i*120})`});txt(r,-380,12,30,'bold',s,'start').setAttribute('fill',c);el('rect',{x:-80,y:-30,width:500,height:60,rx:30,fill:'#2A2A33'},r);r.b=el('rect',{x:-80,y:-30,width:0,height:60,rx:30,fill:WARM},r);r.k=k});
const hbT=txt(heatBars,0,-90,30,'mic mut','HEAT AT IDLE');const lfP=pill(heatBars,'VERY LITTLE FUEL',DIESEL,ASPH,340,26);
const slowG=g();const tgD=tempGauge(slowG,140);const clk2=g(slowG);el('circle',{r:70,fill:'none',stroke:CHALK,'stroke-width':10},clk2);const c2h=el('rect',{x:-5,y:-56,width:10,height:58,rx:5,fill:CHALK},clk2);const longP=pill(slowG,'A VERY LONG TIME',COLD,CHALK,340,26);
// exhaust / wet stacking
const exG=g();el('rect',{x:-420,y:-60,width:700,height:120,rx:20,fill:'#4A4A56'},exG);el('rect',{x:-420,y:-44,width:700,height:88,fill:'#22222A'},exG);el('rect',{x:280,y:-74,width:60,height:148,rx:14,fill:'#5A5A66'},exG);
const goo=[...Array(14)].map((_,i)=>el('ellipse',{cx:-360+i*48,cy:40,rx:22,ry:0,fill:'#0A0A0A'},exG));const tipDrips=[0,1,2].map(i=>el('ellipse',{cx:330+i*6,cy:80,rx:9,ry:14,fill:'#0A0A0A',opacity:0},exG));
const fuelIn=[...Array(10)].map(()=>el('circle',{r:7,fill:AMBER,opacity:0},exG));const residueP=pill(exG,'BLACK, OILY RESIDUE',GRAPH,CHALK,380,26);const wetS=stamp(exG,'WET STACKING',RED,620);
const dpfG=g();const oilD=g(dpfG);el('path',{d:'M0 -110 Q70 -10 70 40 Q70 110 0 110 Q-70 110 -70 40 Q-70 -10 0 -110 Z',fill:'#C9962E'},oilD);const oilDots=[...Array(6)].map((_,i)=>el('circle',{cx:-30+(i%3)*30,cy:20+Math.floor(i/3)*40,r:9,fill:AMBER,opacity:0},oilD));txt(oilD,0,170,26,'mic ink','DILUTED OIL');
const dpf=g(dpfG);el('rect',{x:-230,y:-110,width:460,height:220,rx:90,fill:'#4A4A56'},dpf);const cells=[];for(let r=0;r<4;r++)for(let c=0;c<9;c++)cells.push(el('rect',{x:-160+c*36,y:-70+r*36,width:28,height:28,rx:4,fill:'#9AA0AE'},dpf));
txt(dpf,0,170,26,'mic ink','DIESEL PARTICULATE FILTER');const dpfT=txt(dpf,0,-140,40,'bold','DPF');dpfT.setAttribute('fill',DIESEL);const sootP=pill(dpf,'SOOT',GRAPH,CHALK,140,26);
const hiG=g();const tachD=tach(hiG,150);const hiP=pill(hiG,'HIGH IDLE',DIESEL,ASPH,220,28);const manD=manual(hiG,.7);const warnT=g(hiG);el('path',{d:'M0 -60 L56 40 L-56 40 Z',fill:AMBER},warnT);el('rect',{x:-5,y:-28,width:10,height:40,rx:4,fill:ASPH},warnT);el('circle',{cy:26,r:6,fill:ASPH},warnT);
const regenP=pill(hiG,"CAN'T CLEAN ITSELF",RED,CHALK,360,26);
const smooth=g();el('rect',{x:-380,y:-90,width:760,height:180,rx:24,fill:'#0E0E12'},smooth);const smW=el('path',{fill:'none',stroke:DIESEL,'stroke-width':6},smooth);txt(smooth,-350,-56,22,'mic mut','SHORT IDLE','start');const smP=pill(smooth,'RUNS SMOOTHLY',DIESEL,ASPH,300,26);
const drv=g();const roadD=g(drv);el('rect',{x:-500,y:150,width:1000,height:10,rx:5,fill:'#30303A'},roadD);const dashD=[...Array(8)].map(()=>el('rect',{y:176,width:70,height:8,rx:4,fill:'#30303A'},roadD));const truckD=makeTruck(drv,{body:'#3E5A44',acc:'#FFF6D0'});const loadP=pill(drv,'GENTLY, LIGHT LOAD',LIME,ASPH,380,28);
// step 3: block heater
const s3=g();const truck3=makeTruck(s3,{body:'#3E5A44',acc:'#FFF6D0'});const xray3=g(s3,{transform:'translate(400 -10)'});const eng3=engineBlock(xray3,.36,'#6A6A76');const heat3=el('circle',{r:110,fill:'url(#heat)',opacity:0},xray3);xray3.insertBefore(heat3,eng3);
const cord3=el('path',{d:'M500 -20 Q540 30 520 80',fill:'none',stroke:'#1C1C24','stroke-width':12,'stroke-linecap':'round'},s3);const plug3=g(s3,{transform:'translate(520 90)'});el('rect',{x:-22,y:-10,width:44,height:50,rx:10,fill:'#1C1C24'},plug3);el('rect',{x:-14,y:38,width:8,height:20,fill:'#C9CED8'},plug3);el('rect',{x:6,y:38,width:8,height:20,fill:'#C9CED8'},plug3);
const mag=el('circle',{cx:510,cy:20,r:130,fill:'none',stroke:LIME,'stroke-width':10,opacity:0},s3);const builtP=pill(s3,'BUILT IN',DIESEL,ASPH,200,28);const grilleP=pill(s3,'GRILLE OR FRONT BUMPER',LIME,ASPH,440,26);
const outlet=g();el('rect',{x:-90,y:-130,width:180,height:260,rx:24,fill:CHALK},outlet);[-50,50].forEach(y=>{el('rect',{x:-30,y:y-24,width:12,height:34,rx:4,fill:ASPH},outlet);el('rect',{x:18,y:y-24,width:12,height:34,rx:4,fill:ASPH},outlet)});
const timerD=g();el('circle',{r:120,fill:'#2A2A33'},timerD);el('circle',{r:100,fill:'#0E0E12'},timerD);const tdArc=el('circle',{r:80,fill:'none',stroke:WARM,'stroke-width':30,pathLength:1000,transform:'rotate(-90)','stroke-dasharray':'0 1000'},timerD);txt(timerD,0,170,28,'bold ink','TIMER');
const hrsT=g();const hrsN=txt(hrsT,0,0,96,'bold','2 TO 4');hrsN.setAttribute('fill',WARM);txt(hrsT,0,60,34,'bold ink','HOURS BEFORE');const extCord=el('path',{fill:'none',stroke:'#E9C46A','stroke-width':12,'stroke-linecap':'round'},svg);
const tempQ=g();const man3=manual(tempQ,.75);const th3=therm(tempQ,220);th3.lab.style.display='none';const q3=txt(tempQ,0,0,90,'bold acc','?');
// step 4: fuel
const s4=g();const drop4=g(s4);el('path',{d:'M0 -180 Q120 -20 120 60 Q120 170 0 170 Q-120 170 -120 60 Q-120 -20 0 -180 Z',fill:'#D9B44A'},drop4);const wax=[...Array(16)].map((_,i)=>el('rect',{x:-70+(i%4)*40,y:-10+Math.floor(i/4)*40,width:14,height:14,rx:3,fill:'#FFFFFF',opacity:0,transform:`rotate(${i*23} ${-63+(i%4)*40} ${-3+Math.floor(i/4)*40})`},drop4));
const waxP=pill(s4,'WAX',CHALK,ASPH,140,30);const s4P=pill(s4,'WATCH THE FUEL',DIESEL,ASPH,320,28);
const line=g();el('rect',{x:-480,y:-24,width:400,height:48,rx:24,fill:'#2A2A33'},line);el('rect',{x:140,y:-24,width:300,height:48,rx:24,fill:'#2A2A33'},line);
const filt=g(line);el('rect',{x:-90,y:-110,width:220,height:220,rx:30,fill:'#6A6A76'},filt);el('rect',{x:-70,y:-90,width:180,height:180,rx:16,fill:'#22222A'},filt);for(let i=0;i<7;i++)el('rect',{x:-56+i*24,y:-80,width:8,height:160,rx:4,fill:'#4A4A56'},filt);
const clog=el('rect',{x:-70,y:90,width:180,height:0,fill:'#F4F1EA',opacity:.85},filt);txt(filt,20,150,26,'mic ink','FUEL FILTER');
const flowD=[...Array(12)].map(()=>el('circle',{r:9,fill:'#D9B44A'},line));const crys=[...Array(10)].map(()=>flake(line,.12,'#FFFFFF'));const starveP=pill(line,'ENGINE STARVES',RED,CHALK,320,26);const crysP=pill(line,'WAX CRYSTALS',CHALK,ASPH,280,26);
const cloud=g();const th4=therm(cloud,320);th4.lab.style.display='none';const band4=el('rect',{x:-50,y:0,width:100,height:0,rx:12,fill:COLD,opacity:.35},cloud);cloud.insertBefore(band4,th4);
const b4a=txt(cloud,80,0,30,'bold ink','AROUND FREEZING (32°F)','start');const b4b=txt(cloud,80,0,30,'bold ink','DOWN TO THE TEENS','start');
const jar=g(cloud,{transform:'translate(-300 40)'});el('rect',{x:-90,y:-140,width:180,height:280,rx:30,fill:'none',stroke:CHALK,'stroke-width':8},jar);const jarF=el('rect',{x:-80,y:-100,width:160,height:230,rx:22,fill:'#D9B44A'},jar);const jarC=el('rect',{x:-80,y:-100,width:160,height:230,rx:22,fill:'#FFFFFF',opacity:0},jar);txt(jar,0,190,28,'bold ink','#2 DIESEL');
const cloudP=pill(cloud,'CLOUDING',CHALK,ASPH,220,26);
const pump=g();el('rect',{x:-130,y:-230,width:260,height:460,rx:30,fill:'#2A2A33'},pump);el('rect',{x:-100,y:-200,width:200,height:120,rx:16,fill:'#0E0E12'},pump);txt(pump,0,-130,36,'bold','DIESEL').setAttribute('fill',DIESEL);
const wbS=g(pump,{transform:'translate(0 20)'});el('rect',{x:-110,y:-50,width:220,height:100,rx:14,fill:COLD},wbS);txt(wbS,0,-6,30,'bold ink','WINTER');txt(wbS,0,30,26,'bold ink','BLEND');const pumpFl=flake(pump,.35);pumpFl.setAttribute('transform','translate(90 -30) scale(.35)');
el('path',{d:'M130 -40 Q220 -40 220 60 L220 160',fill:'none',stroke:'#1C1C24','stroke-width':18},pump);const nz=g(pump,{transform:'translate(220 170)'});el('rect',{x:-30,y:-20,width:60,height:90,rx:14,fill:DIESEL},nz);
const add=g();const bot=g(add);el('rect',{x:-80,y:-150,width:160,height:270,rx:26,fill:'#2E6BD8'},bot);el('rect',{x:-30,y:-200,width:60,height:56,rx:10,fill:CHALK},bot);txt(bot,0,-40,36,'bold ink','ANTI');txt(bot,0,4,36,'bold ink','GEL');const bF=flake(bot,.3);bF.setAttribute('transform','translate(0 70) scale(.3)');
const tank=g(add);el('rect',{x:-200,y:-100,width:400,height:200,rx:40,fill:'#3A3A46'},tank);const tankF=el('rect',{x:-180,y:-80,width:360,height:0,rx:26,fill:'#D9B44A'},tank);const swirl=el('path',{fill:'none',stroke:'#2E6BD8','stroke-width':8,'stroke-linecap':'round',opacity:0},tank);
const ord=[pill(add,'1  ADD IT FIRST',DIESEL,ASPH,300,26),pill(add,'2  THEN FILL UP',DIESEL,ASPH,300,26)];const beforeP=pill(add,'BEFORE THE COLD HITS',COLD,CHALK,400,28);const mixP=pill(add,'MIXES IN',LIME,ASPH,220,26);
const verd=g();const vOk=card(verd,420,300,'#1E3326');const vOkC=CHECK(vOk,1.5);vOkC.setAttribute('transform','translate(0 -50) scale(1.5)');txt(vOk,0,60,40,'bold acc','PREVENTS');txt(vOk,0,104,30,'mic ink','GELLING');
const vNo=card(verd,420,300,'#3A2228');const vNoX=XMARK(vNo,1.5);vNoX.setAttribute('transform','translate(0 -50) scale(1.5)');txt(vNo,0,60,36,'bold red',"USUALLY WON'T FIX");txt(vNo,0,104,30,'mic ink','GELLED FUEL');

KEYS.push([PF+.1,'open'],[Gs('f2'),'mid'],[Gs('f3'),'mid'],[Gs('f4'),'shrug'],[Gs('f5'),'one'],[W_('f5','on')-.4,'mid'],[Gs('f6'),'top'],[Gs('f7'),'mid'],[Gs('f8'),'right'],[Gs('f9'),'mid'],[Gs('f10'),'stop'],[Gs('f11'),'mid'],
 [Gs('f12'),'one'],[W_('f12','long')-.3,'stop'],[Gs('f13'),'mid'],[Gs('f14'),'shrug'],[Gs('f15'),'mid'],[Gs('f16'),'right'],[Gs('f17'),'mid'],[Gs('f18'),'top'],[Gs('f19'),'mid'],[Gs('f20'),'mid'],[W_('f20','light')-.3,'thumb'],
 [Gs('f21'),'one'],[W_('f21','block')-.3,'mid'],[Gs('f23'),'right'],[Gs('f24'),'mid'],[Gs('f25'),'right'],[Gs('f26'),'mid'],[Gs('f27'),'one'],[Gs('f28'),'mid'],[Gs('f29'),'mid'],[W_('f29','starves')-.3,'shrug'],[Gs('f30'),'mid'],[Gs('f31'),'right'],
 [Gs('f32'),'one'],[W_('f32','before')-.3,'mid'],[Gs('f33'),'mid'],[Gs('f34'),'left'],[Gs('f35'),'right']);
MOODS.push([Gs('f15'),Gs('f20'),{smile:.15,browWorry:.3}],[Gs('f29'),Gs('f31'),{smile:.15,browWorry:.3}]);
RENDER.push(t=>{
 if(t<PF-.5||t>PG+.5){show(0,gpP,dHead,dTrack,cyls,keyG,dash,pushB,crankBar,s2,heatBars,slowG,exG,dpfG,hiG,smooth,drv,s3,outlet,timerD,hrsT,tempQ,s4,line,cloud,pump,add,verd);extCord.style.display='none';return}capMode('studio');
 // step tracker from f5
 const kt=V(t,Gs('f5')-.1,PG);show(kt,dTrack);dTrack.style.opacity=kt;dTrack.setAttribute('transform',`translate(${CX} 130)`);const st=[Gs('f5'),Gs('f12'),Gs('f21'),Gs('f27')];
 dSteps.forEach((s,i)=>{const a=t>=st[i]-.1&&(i===3||t<st[i+1]-.1);const done=t>=(st[i+1]||999)-.1;s.bg.setAttribute('fill',a?DIESEL:(done?'#2C4A36':'#2A2A33'));s.tt_.style.fill=a?ASPH:(done?DIESEL:H.smoke);s.n.style.fill=a?ASPH:(done?DIESEL:H.smoke);s.setAttribute('transform',`translate(${(i-1.5)*240} 0) scale(${a?1.08:1})`)});
 S(dHead,t,PF,Gs('f2')-.1,()=>{tr(dTitle,0,0,1,0,1);dHead.setAttribute('transform',`translate(${CX} 0)`);dTitle.setAttribute('transform',`translate(0 ${300}) scale(${pop(t,PF)})`);truck.setAttribute('transform',`translate(${lerp(700,0,eo(P(t,PF,.8)))} 590) scale(.66)`)});
 const cv=Math.max(V(t,Gs('f2')-.1,Gs('f5')-.1),V(t,Gs('f7')-.1,Gs('f9')-.1));show(cv,cyls);cyls.style.opacity=cv;show(on(t,Gs('f7')-.1)*(1-on(t,Gs('f9')-.1)),gpP);
 if(cv>0&&t<Gs('f5')){show(1,cGas,noPlug,compP,hardP,rulesP,cylFl);cyls.setAttribute('transform',`translate(${CX} 470) scale(.95)`);const t3=Gs('f3')-.1;const solo=eo(P(t,t3,.5));
  tr(cGas,lerp(-200,-200,solo),0,1,0,1-solo);tr(cDsl,lerp(200,0,solo),0,1,0,1);cGas.style.display=solo>.98?'none':'';
  cGas.pis.setAttribute('transform',`translate(0 ${-20+40*Math.sin(t*4)})`);cGas.spark.style.opacity=Math.sin(t*4)>.9?1:0;cGas.air.setAttribute('fill',COLD);
  const np=W_('f2','spark')-.3;tr(noPlug,200,-300,1.2*pop(t,np),0,on(t,np)*(1-solo));cDsl.spark.style.display='none';cGas.gpTip.style.display='none';
  const tc=W_('f3','compressed')-.3;const ph=t<tc?0:((t-tc)/1.6)%1;const up=t<tc?0:Math.min(1,ph/.6);cDsl.pis.setAttribute('transform',`translate(0 ${lerp(-10,-130,eio(up))})`);
  const hot=up>.95?1:0;cDsl.air.setAttribute('height',lerp(180,60,eio(up)));cDsl.air.setAttribute('fill',up>.5?WARM:COLD);cDsl.air.setAttribute('opacity',.35+.3*up);cDsl.flame.setAttribute('r',hot*lerp(30,140,(ph-.6)/.4));
  cDsl.mist.forEach((m,i)=>{const a=(i/14-.5)*1.4;const d=((ph-.58)/.1)*60;m.setAttribute('cx',Math.sin(a)*d);m.setAttribute('cy',-186+Math.cos(a)*d);m.style.opacity=ph>.58&&ph<.7?1:0});
  tr(compP,0,-330,pop(t,tc),0,on(t,tc)*(1-on(t,Gs('f4')-.1)));
  const tcold=W_('f4','cold')-.3;if(t>tcold){cDsl.air.setAttribute('fill',COLD)}tr(cylFl,220,-150,.6*pop(t,tcold),t*20,on(t,tcold));tr(hardP,0,-330,pop(t,W_('f4','harder')-.3),0,on(t,W_('f4','harder')-.3));tr(rulesP,0,340,pop(t,W_('f4','rules')-.3),0,on(t,W_('f4','rules')-.3))}
 // step 1
 const chOn=W_('f5','on')-.1,glOff=W_('f6','out')-.1;
 S(keyG,t,Gs('f5')-.1,Gs('f6')-.1,()=>{tr(keyG,CX,470,pop(t,Gs('f5')-.1),0,1);const a=lerp(-80,20,eio(P(t,chOn-.35,.35)));keyB.setAttribute('transform',`rotate(${a})`);pos.forEach(p=>p.tt_.style.fill=Math.abs(p.a-a)<6?LIME:H.smoke)});
 S(dash,t,Gs('f6')-.1,Gs('f7')-.1,()=>{tr(dash,CX,450,pop(t,Gs('f6')-.1),0,1);gl.set(t>=chOn+.03&&t<glOff?1:0);glLab.style.fill=t>W_('f6','coil')-.3?AMBER:H.smoke;tr(waitP,0,250,pop(t,W_('f6','go')-.4),0,on(t,W_('f6','go')-.4))});
 if(t>=chOn+.03&&t<chOn+.35)flash.style.opacity=.1*(1-P(t,chOn,.35));
 if(cv>0&&t>Gs('f7')-.2){cyls.setAttribute('transform',`translate(${CX} 470) scale(.95)`);cGas.style.display='none';tr(cDsl,0,0,1,0,1);show(0,noPlug,compP,hardP,rulesP,cylFl);
  const gk=eo(P(t,Gs('f7'),.8));cDsl.gpTip.setAttribute('fill',gk>.5?WARM:'#9AA0AE');cDsl.air.setAttribute('fill',gk>.5?WARM:COLD);cDsl.air.setAttribute('height',150);cDsl.air.setAttribute('opacity',.25+.25*gk);
  const tf=W_('f7','fire')-.3;const tcr=W_('f8','crank')-.2;const crank=t>tcr;const ph=crank?((t-tcr)*4)%1:0;cDsl.pis.setAttribute('transform',`translate(0 ${crank?-60+60*Math.cos(ph*Math.PI*2):-10})`);
  cDsl.flame.setAttribute('r',(t>tf&&t<tf+.6?lerp(30,140,P(t,tf,.6)):0)+(crank&&t>tcr+.8?100*Math.max(0,Math.cos(ph*Math.PI*2)):0));
  cDsl.mist.forEach(m=>m.style.opacity=0);cyls.setAttribute('transform',`translate(${CX+(crank&&t<tcr+.8?4*Math.sin(t*50):0)} 470) scale(.95)`);tr(gpP,CX,150+60,pop(t,Gs('f7')-.1),0,1)}
 S(pushB,t,Gs('f9')-.1,Gs('f10')-.1,()=>{tr(pushB,CX,450,pop(t,Gs('f9')-.1),0,1);const k=P(t,Gs('f9')+.3,1.6);pbRing.setAttribute('stroke',k<1?AMBER:LIME);pbRing.setAttribute('stroke-dasharray',`${k*1000} 1000`);tr(autoP,0,190,pop(t,W_('f9','automatically')-.4),0,on(t,W_('f9','automatically')-.4))});
 S(crankBar,t,Gs('f10')-.1,Gs('f12')-.1,()=>{tr(crankBar,CX,430,pop(t,Gs('f10')-.1),0,1);const k=eio(P(t,W_('f10','15')-.6,1.2));cbFill.setAttribute('width',630*k);const tr_=W_('f11','rest')-.4;
  cbT.style.opacity=1-on(t,tr_);tr(restP,0,180,pop(t,tr_),0,on(t,tr_));cbFill.setAttribute('fill',t>tr_?'#3A3A46':AMBER)});
 // step 2
 S(s2,t,Gs('f12')-.1,Gs('f13')-.1,()=>{s2.setAttribute('transform',`translate(${CX} 430)`);tr(clk,0,0,pop(t,Gs('f12')-.1),0,1);hM.setAttribute('transform',`rotate(${t*360})`);hH.setAttribute('transform',`rotate(${t*30})`);const tl=W_('f12','long')-.3;tr(clkX,90,-90,1.3*pop(t,tl),0,on(t,tl));tr(s2P,0,190,pop(t,tl),0,on(t,tl))});
 S(heatBars,t,Gs('f13')-.1,Gs('f14')-.1,()=>{tr(heatBars,CX+40,380,pop(t,Gs('f13')-.1),0,1);[...heatBars.children].slice(0,2).forEach((r,i)=>{r.b.setAttribute('width',500*r.k*eo(P(t,Gs('f13')+.3+i*.4+(i?W_('f13','less')-Gs('f13')-1:0),.8)));r.b.setAttribute('fill',i?DIESEL:WARM)});
  tr(lfP,80,250,pop(t,W_('f13','little')-.3),0,on(t,W_('f13','little')-.3))});
 S(slowG,t,Gs('f14')-.1,Gs('f15')-.1,()=>{slowG.setAttribute('transform',`translate(${CX} 440)`);tr(tgD,-170,40,pop(t,Gs('f14')-.1),0,1);tgD.set(.04+.03*eo(P(t,Gs('f14'),3)));tr(clk2,200,0,pop(t,Gs('f14')),0,1);c2h.setAttribute('transform',`rotate(${t*720})`);
  tr(longP,0,200,pop(t,W_('f14','long')-.3),0,on(t,W_('f14','long')-.3))});
 S(exG,t,Gs('f15')-.1,Gs('f17')-.1,()=>{tr(exG,CX-40,430,.95*pop(t,Gs('f15')-.1),0,1);const tb=W_('f15','black')-.4;const k=eo(P(t,tb,2.4));
  goo.forEach((e,i)=>e.setAttribute('ry',k*(10+6*Math.sin(i*1.7))));tipDrips.forEach((d,i)=>{const ph=((t*.8)+i/3)%1;d.setAttribute('cy',60+ph*120);d.style.opacity=k>.5?1-ph:0});
  fuelIn.forEach((f,i)=>{const ph=((t*.7)+i/10)%1;f.setAttribute('cx',-400+ph*700);f.setAttribute('cy',-10+12*Math.sin(i*2+t*3));f.style.opacity=on(t,Gs('f15'))*(1-ph)});
  tr(residueP,-60,-140,pop(t,tb),0,on(t,tb)*(1-on(t,Gs('f16')-.1)));const tw=W_('f16','wet')-.3;tr(wetS,-60,-160,lerp(1.4,1,eo(P(t,tw,.25))),-5,on(t,tw))});
 S(dpfG,t,Gs('f17')-.1,Gs('f18')-.1,()=>{dpfG.setAttribute('transform',`translate(${CX} 450)`);const to=W_('f17','dilute')-.3;tr(oilD,-330,0,.9*pop(t,to),0,on(t,to));oilDots.forEach((d,i)=>d.style.opacity=on(t,to+.3+i*.12));
  const td=W_('f17','particulate')-.4;tr(dpf,170,0,.85*pop(t,td),0,on(t,td));const ts=W_('f17','soot')-.6;cells.forEach((c,i)=>c.setAttribute('fill',t>ts+((i*7)%36)/36*1.2?'#141414':'#9AA0AE'));tr(sootP,0,0,pop(t,W_('f17','soot')-.2),0,on(t,W_('f17','soot')-.2))});
 S(hiG,t,Gs('f18')-.1,Gs('f20')-.1,()=>{hiG.setAttribute('transform',`translate(${CX} 430)`);const th=W_('f18','high')-.3;tr(tachD,-220,0,.9*pop(t,Gs('f18')-.1),0,1);tachD.set(t>th?lerp(.75,1.4,eo(P(t,th,.6)))+.03*Math.sin(t*9):.75+.03*Math.sin(t*9));tr(hiP,-220,210,pop(t,th),0,on(t,th));
  const tm=W_('f19','manuals')-.4;tr(manD,220,0,.7*pop(t,tm),0,on(t,tm));tr(warnT,330,-110,pop(t,W_('f19','warn')-.3),0,on(t,W_('f19','warn')-.3));tr(regenP,220,210,pop(t,W_('f19','cleaning')-.3),0,on(t,W_('f19','cleaning')-.3))});
 S(smooth,t,Gs('f20')-.1,W_('f20','drive')-.3,()=>{tr(smooth,CX,400,pop(t,Gs('f20')-.1),0,1);const ts=W_('f20','smoothly')-.4;let d='';for(let i=0;i<=120;i++){const x=-350+i*5.8;const tx=t-(120-i)*.02;const rough=tx<ts?1:Math.max(0,1-(tx-ts)*1.5);const y=20*Math.sin(tx*18)+rough*30*Math.sin(tx*53)*Math.sin(tx*7);d+=(i?'L':'M')+x+' '+(10+y).toFixed(1)}smW.setAttribute('d',d);tr(smP,0,140,pop(t,ts),0,on(t,ts))});
 S(drv,t,W_('f20','drive')-.3,Gs('f21')-.1,()=>{drv.setAttribute('transform',`translate(${CX} 420) scale(.62)`);dashD.forEach((d,i)=>d.setAttribute('x',((i*150-t*500)%1200+1200)%1200-600));truckD.wheels.forEach(w=>w.hub.setAttribute('transform',`rotate(${t*360})`));truckD.setAttribute('transform',`translate(0 ${1.2*Math.sin(t*20)})`);tr(loadP,0,-330,pop(t,W_('f20','light')-.3),0,on(t,W_('f20','light')-.3))});
 // step 3
 S(s3,t,Gs('f21')-.1,Gs('f24')-.1,()=>{s3.setAttribute('transform',`translate(${CX-80} 450) scale(.72)`);truck3.setAttribute('transform',`translate(0 ${-30*0})`);const tb=W_('f22','built')-.3;xray3.style.opacity=on(t,W_('f21','block')-.3);heat3.setAttribute('opacity',eo(P(t,W_('f21','heater')-.2,.8)));
  tr(builtP,300,-300,pop(t,tb),0,on(t,tb)*(1-on(t,Gs('f23')-.1)));const tp=W_('f23','plug')-.3;cord3.style.opacity=plug3.style.opacity=on(t,tp);mag.setAttribute('opacity',on(t,W_('f23','grille')-.3));tr(grilleP,300,-300,pop(t,W_('f23','grille')-.3),0,on(t,W_('f23','grille')-.3))});
 S(outlet,t,Gs('f24')-.1,Gs('f26')-.1,()=>{tr(outlet,CX+300,470,pop(t,Gs('f24')-.1),0,1);extCord.style.display='';extCord.style.opacity=outlet.style.opacity;extCord.setAttribute('d',`M${CX+300} 440 Q${CX+120} 640 ${CX-60} 600 Q${CX-200} 560 ${CX-300} 640`)});
 if(!(t>Gs('f24')-.1&&t<Gs('f26')))extCord.style.display='none';
 S(hrsT,t,Gs('f24')-.1,Gs('f25')-.1,()=>tr(hrsT,CX-80,300,pop(t,W_('f24','2')-.4),0,on(t,W_('f24','2')-.4)));
 S(timerD,t,Gs('f25')-.1,Gs('f26')-.1,()=>{tr(timerD,CX-120,400,pop(t,W_('f25','timer')-.4),0,on(t,W_('f25','timer')-.4));tdArc.setAttribute('stroke-dasharray',`${330*eio(P(t,W_('f25','timer'),1))} 1000`)});
 S(tempQ,t,Gs('f26')-.1,Gs('f27')-.1,()=>{tempQ.setAttribute('transform',`translate(${CX} 440)`);tr(man3,-160,0,.75*pop(t,Gs('f26')-.1),0,1);const tq=W_('f26','temperature')-.3;tr(th3,140,-20,.9*pop(t,tq),0,on(t,tq));th3.set(10+15*Math.sin(t*2));tr(q3,250,-80,pop(t,tq+.2),0,on(t,tq+.2))});
 // step 4
 S(s4,t,Gs('f27')-.1,Gs('f29')-.1,()=>{s4.setAttribute('transform',`translate(${CX} 470)`);tr(drop4,0,0,pop(t,Gs('f27')-.1),0,1);tr(s4P,0,-260,pop(t,W_('f27','fuel')-.3),0,on(t,W_('f27','fuel')-.3)*(1-on(t,Gs('f28')-.1)));
  const tw=W_('f28','wax')-.4;wax.forEach((w,i)=>w.style.opacity=on(t,tw+i*.04)*.9);tr(waxP,0,-260,pop(t,tw),0,on(t,tw))});
 S(line,t,Gs('f29')-.1,Gs('f30')-.1,()=>{line.setAttribute('transform',`translate(${CX} 440) scale(.9)`);const tc=W_('f29','crystals')-.4,tclog=W_('f29','clog')-.3,tst=W_('f29','starves')-.3;const ck=eo(P(t,tclog,1.4));
  flowD.forEach((d,i)=>{const ph=((t*.6*(1-ck*.95))+i/12)%1;const x=-480+ph*920;const blocked=x>-90&&x<130;d.setAttribute('cx',x);d.setAttribute('cy',0);d.style.opacity=(blocked?0:1)*(x>130?1-ck:1)});
  crys.forEach((c,i)=>{const k=eo(P(t,tc+i*.08,.4));c.setAttribute('transform',`translate(${-440+i*36} ${(i%2?-6:6)}) scale(${.12*k}) rotate(${t*30})`)});clog.setAttribute('y',90-180*ck);clog.setAttribute('height',180*ck);
  tr(crysP,-280,-90,pop(t,tc),0,on(t,tc));tr(starveP,290,-90,pop(t,tst),0,on(t,tst))});
 S(cloud,t,Gs('f30')-.1,Gs('f31')-.1,()=>{cloud.setAttribute('transform',`translate(${CX+40} 450)`);const tf=W_('f30','freezing')-.3,tt=W_('f30','teens')-.3;const k=eo(P(t,Gs('f30'),Math.max(.5,tt-Gs('f30')+.4)));
  th4.set(lerp(45,15,k),-20,90);tr(th4,0,0,1,0,1);const y=T=>160-(290)*cl((T+20)/110);band4.setAttribute('y',y(32));band4.setAttribute('height',on(t,tf)*(y(15)-y(32))*(t>tt?1:.15));band4.setAttribute('x',-60);band4.setAttribute('width',120);
  b4a.setAttribute('y',y(32)+10);b4a.style.opacity=on(t,tf);b4b.setAttribute('y',y(15)+10);b4b.style.opacity=on(t,tt);const tcl=W_('f30','clouding')-.3;jarC.setAttribute('opacity',.7*eo(P(t,tcl,1.5)));tr(cloudP,-300,-220,pop(t,tcl),0,on(t,tcl))});
 S(pump,t,Gs('f31')-.1,Gs('f32')-.1,()=>tr(pump,CX-60,460,.85*pop(t,Gs('f31')-.1),0,1));
 S(add,t,Gs('f32')-.1,Gs('f34')-.1,()=>{add.setAttribute('transform',`translate(${CX} 470)`);const ta=W_('f32','anti-gel')-.3;const tf=W_('f33','fill')-.3;const pour=V(t,Gs('f33')-.1,tf+.3,.4,.3);
  tr(bot,-260+120*pour,-60-40*pour,.8*pop(t,ta),70*pour,1);tr(tank,140,120,.9,0,1);tankF.setAttribute('height',lerp(20,150,eo(P(t,tf,1.4))));tankF.setAttribute('y',80-lerp(20,150,eo(P(t,tf,1.4))));
  const tb=W_('f32','before')-.3;tr(beforeP,0,-240,pop(t,tb),0,on(t,tb)*(1-on(t,Gs('f33')-.2)));tr(ord[0],-160,-240,pop(t,Gs('f33')-.1),0,on(t,Gs('f33')-.1));tr(ord[1],180,-240,pop(t,tf),0,on(t,tf));
  const tm=W_('f33','mixes')-.3;swirl.setAttribute('d',`M-100 0 Q-50 ${-40*Math.sin(t*4)} 0 0 T100 0`);swirl.setAttribute('opacity',on(t,tm));tr(mixP,140,280,pop(t,tm),0,on(t,tm))});
 S(verd,t,Gs('f34')-.1,PG+.05,()=>{verd.setAttribute('transform',`translate(${CX} 450)`);tr(vOk,-230,0,pop(t,W_('f34','prevents')-.3),0,on(t,W_('f34','prevents')-.3));tr(vNo,230,0,pop(t,W_('f35','fix')-.4),0,on(t,W_('f35','fix')-.4))});
});
EVF.push(A=>{
 A(PF,'whoosh',.5,.45);A(PF+.1,'rev',1.2,.3);A(Gs('f2')-.1,'whoosh',.4,.4);A(W_('f2','spark')-.3,'pop',0,.6);A(W_('f3','compressed')-.3,'squeeze',.9,.4);A(W_('f3','compressed')+.7,'bloom',.6,.45);
 A(W_('f4','cold')-.3,'pop',0,.5);A(W_('f4','harder')-.3,'pop',0,.5);A(W_('f4','rules')-.3,'check',0,.6);
 A(Gs('f5')-.1,'whoosh',.4,.4);A(W_('f5','on')-.45,'key',0,.7);A(W_('f5','on')-.1,'warn',1.0,.4);A(W_('f6','coil')-.3,'pop',0,.4);A(W_('f6','out')-.1,'click',0,.8);
 A(Gs('f7'),'glow',1.2,.35);A(W_('f7','fire')-.3,'bloom',.6,.4);A(WL_('f8','crank')+.3,'starter',.55,.4);
 A(Gs('f9')-.1,'pop',0,.5);A(Gs('f9')+.3,'charge',1.6,.25);A(W_('f9','automatically')-.4,'check',0,.6);A(W_('f10','15')-.6,'starter',1.2,.25);A(W_('f11','rest')-.4,'pop',0,.5);
 A(Gs('f12')-.1,'whoosh',.4,.4);A(W_('f12','long')-.3,'thud',0,.5);A(Gs('f13')-.1,'pop',0,.5);A(W_('f13','little')-.3,'pop',0,.5);A(Gs('f14')-.1,'pop',0,.5);A(Gs('f14'),'gearticks',2.5,.18);
 A(Gs('f15')-.1,'whoosh',.4,.4);A(W_('f15','black')-.4,'drip',0,.5);A(W_('f15','black'),'drip',0,.4);A(W_('f16','wet')-.3,'thud',0,.45);A(W_('f17','dilute')-.3,'pop',0,.5);A(W_('f17','particulate')-.4,'pop',0,.5);A(W_('f17','soot')-.6,'puff',1.2,.4);
 A(Gs('f18')-.1,'pop',0,.5);A(W_('f18','high')-.3,'rev',.8,.25);A(W_('f19','manuals')-.4,'pop',0,.5);A(W_('f19','warn')-.3,'alarm',0,.25);A(W_('f19','cleaning')-.3,'pop',0,.5);
 A(Gs('f20')-.1,'pop',0,.5);A(W_('f20','drive')-.3,'whoosh',.4,.4);A(W_('f20','light')-.3,'check',0,.6);
 A(Gs('f21')-.1,'whoosh',.4,.4);A(W_('f21','heater')-.2,'glow',1,.35);A(W_('f22','built')-.3,'pop',0,.5);A(W_('f23','plug')-.3,'pop',0,.5);A(W_('f23','grille')-.3,'pop',0,.5);
 A(Gs('f24')-.1,'clack',0,.5);A(W_('f24','2')-.4,'pop',0,.5);A(W_('f25','timer')-.4,'gearticks',1,.4);A(Gs('f26')-.1,'pop',0,.5);A(W_('f26','temperature')-.3,'pop',0,.5);
 A(Gs('f27')-.1,'whoosh',.4,.4);A(W_('f27','fuel')-.3,'pop',0,.5);A(W_('f28','wax')-.4,'pop',0,.5);A(W_('f29','crystals')-.4,'crack',0,.25);A(W_('f29','clog')-.3,'squeeze',1.2,.3);A(W_('f29','starves')-.3,'stutter',1.2,.4);
 A(Gs('f30')-.1,'whoosh',.4,.4);A(W_('f30','freezing')-.3,'pop',0,.5);A(W_('f30','teens')-.3,'pop',0,.5);A(Gs('f31')-.1,'pop',0,.5);
 A(Gs('f32')-.1,'whoosh',.4,.4);A(W_('f32','before')-.3,'pop',0,.5);A(Gs('f33'),'splash',.5,.4);A(W_('f33','fill')-.3,'pump',1.2,.35);A(W_('f34','prevents')-.3,'check',0,.7);A(W_('f35','fix')-.4,'thud',0,.5);
});
