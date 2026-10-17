// ================= PART E: the right way for a gas car =================
const PF=Gs('f1')-.1;
const track=g();const tSteps=['START','BUCKLE UP','30 SECONDS','DRIVE GENTLY'].map((s,i)=>{const c=g(track,{transform:`translate(${(i-1.5)*240} 0)`});const bg=el('rect',{x:-112,y:-34,width:224,height:68,rx:34,fill:'#2A2A33'},c);const tt_=txt(c,0,10,24,'mic mut',s);c.bg=bg;c.tt_=tt_;return c});
const gasHead=g();const gh=pill(gasHead,'GAS CAR: THE RIGHT WAY',LIME,ASPH,480,32);
// start button
const btn=g();el('circle',{r:130,fill:'#2A2A33'},btn);const btnRing=el('circle',{r:118,fill:'none',stroke:'#4A4A56','stroke-width':10},btn);txt(btn,0,-14,34,'bold ink','ENGINE');txt(btn,0,26,26,'mic mut','START  STOP');
// buckle, mirror
const buckle=g();const bLatch=g(buckle);el('rect',{x:-150,y:-34,width:150,height:68,rx:14,fill:'#9AA0AE'},bLatch);el('rect',{x:-260,y:-22,width:120,height:44,fill:'#3A3A46'},bLatch);
const bBody=g(buckle);el('rect',{x:-10,y:-50,width:150,height:100,rx:20,fill:RED},bBody);el('rect',{x:20,y:-14,width:90,height:28,rx:6,fill:'#7A2232'},bBody);el('rect',{x:140,y:-22,width:120,height:44,fill:'#3A3A46'},bBody);
const mirror=g();el('path',{d:'M-120 -70 Q0 -96 120 -70 L110 70 Q0 90 -110 70 Z',fill:'#6A6A76'},mirror);el('path',{d:'M-100 -54 Q0 -76 100 -54 L92 54 Q0 72 -92 54 Z',fill:'#8FB4E0'},mirror);el('rect',{x:-20,y:70,width:40,height:60,fill:'#4A4A56'},mirror);
const mirCar=carIcon(mirror,.1);const sw30=stopwatch(svg,130);
// drive gently
const gentle=g();const roadE=g(gentle);el('rect',{x:-460,y:120,width:920,height:10,rx:5,fill:'#30303A'},roadE);const dashE=[...Array(7)].map(()=>el('rect',{y:146,width:70,height:8,rx:4,fill:'#30303A'},roadE));
const carE=carIcon(gentle,.42,{body:LIME});const exE=puffs(gentle,8,'#C9D3E3');
const tachE=tach(svg,150);const tenP=pill(svg,'FIRST 5 TO 10 MINUTES',GRAPH,CHALK,420,28);const noHard=pill(svg,'NO HARD ACCELERATION',RED,CHALK,420,26);const noRev=pill(svg,'NO HIGH REVS',RED,CHALK,280,26);
const tgE=tempGauge(svg,120);const fastP=pill(svg,'FASTEST WAY TO WARM UP',LIME,ASPH,440,26);
const vent=g();el('rect',{x:-150,y:-70,width:300,height:140,rx:30,fill:'#2A2A33'},vent);[-40,-10,20,50].forEach(y=>el('rect',{x:-120,y:y-10,width:240,height:10,rx:5,fill:'#4A4A56'},vent));const waves=[0,1,2].map(i=>el('path',{fill:'none',stroke:WARM,'stroke-width':10,'stroke-linecap':'round'},vent));const cabinP=pill(vent,'CABIN HEAT SOONER',WARM,ASPH,340,26);
// brutally cold
const brut=g();const thE=therm(brut,300);const frostE=flake(brut,.9);const minP=g(brut);const sw2=stopwatch(minP,110);const minT=txt(minP,0,-150,30,'mic ink','GIVE IT');const man=manual(brut,.9);
const advice=g(brut);const page=card(advice,360,300,CHALK);txt(page,0,-90,26,'bold','COLD WEATHER').setAttribute('fill',ASPH);[-40,0,40,80].forEach((y,i)=>el('rect',{x:-130,y,width:i===3?160:260,height:14,rx:7,fill:'#C9CED8'},page));const pF=flake(page,.35);pF.setAttribute('transform','translate(130 -96) scale(.35)');
// block heater
const bh=g();const eb=engineBlock(bh,1.2,'#5A5A66');const coil=el('path',{d:'M-60 40 q15 -30 30 0 t30 0 t30 0 t30 0',fill:'none',stroke:'#3A3A46','stroke-width':12,'stroke-linecap':'round'},bh);
const bhGlow=el('circle',{cx:0,cy:40,r:150,fill:'url(#heat)',opacity:0},bh);bh.insertBefore(bhGlow,eb);const cord=el('path',{d:'M90 40 Q260 60 260 200 Q260 260 330 260',fill:'none',stroke:'#1C1C24','stroke-width':14,'stroke-linecap':'round'},bh);
const plugE=g(bh,{transform:'translate(350 260)'});el('rect',{x:-24,y:-30,width:60,height:60,rx:12,fill:'#3A3A46'},plugE);el('rect',{x:36,y:-16,width:24,height:8,fill:'#C9CED8'},plugE);el('rect',{x:36,y:8,width:24,height:8,fill:'#C9CED8'},plugE);
const bhP=pill(bh,'ENGINE BLOCK HEATER',WARM,ASPH,400,28);const bigD=pill(bh,'BIG DIFFERENCE',LIME,ASPH,300,28);

KEYS.push([PE+.1,'thumb'],[Gs('e2'),'mid'],[Gs('e3'),'mid'],[Gs('e4'),'right'],[Gs('e5'),'one'],[W_('e5','hard')-.3,'stop'],[Gs('e6'),'mid'],[Gs('e7'),'shrug'],[Gs('e7')+1,'mid'],[Gs('e8'),'one'],[W_('e8','manual')-.4,'right'],[Gs('e9'),'mid'],[Gs('e10'),'mid'],[W_('e10','big')-.3,'thumb']);
RENDER.push(t=>{
 if(t<PE-.5||t>PF+.5){show(0,track,gasHead,btn,buckle,mirror,sw30,gentle,tachE,tenP,noHard,noRev,tgE,fastP,vent,brut,bh);return}capMode('studio');
 const tr1=V(t,PE,Gs('e7')-.1);show(tr1,track);track.style.opacity=tr1;track.setAttribute('transform',`translate(${CX} 130)`);
 const lit=[Gs('e2'),W_('e3','Buckle')-.2,W_('e3','30')-.2,W_('e4','gently')-.3];tSteps.forEach((s,i)=>{const a=t>lit[i];s.bg.setAttribute('fill',a?LIME:'#2A2A33');s.tt_.style.fill=a?ASPH:H.smoke;s.setAttribute('transform',`translate(${(i-1.5)*240} 0) scale(${a?1+.1*(1-P(t,lit[i],.3)):1})`)});
 if(vis(gasHead,t,PE,Gs('e2')-.1)>0)tr(gasHead,CX,440,pop(t,PE),0,1);
 if(vis(btn,t,Gs('e2')-.1,Gs('e3')-.1)>0){const pr=V(t,W_('e2','Start')-.05,W_('e2','Start')+.25,.05,.1);tr(btn,CX,450,pop(t,Gs('e2')-.1)*(1-.06*pr),0,1);btnRing.setAttribute('stroke',t>W_('e2','Start')?LIME:'#4A4A56')}
 const e3a=Gs('e3')-.1,e3b=Gs('e4')-.1;
 if(vis(buckle,t,e3a,W_('e3','mirrors')-.3)>0){const k=eio(P(t,W_('e3','Buckle')-.3,.4));tr(buckle,CX,440,pop(t,e3a),0,1);bLatch.setAttribute('transform',`translate(${lerp(-120,0,k)} 0)`)}
 if(vis(mirror,t,W_('e3','mirrors')-.3,W_('e3','30')-.3)>0){tr(mirror,CX,440,pop(t,W_('e3','mirrors')-.3)*1.2,0,1);mirCar.setAttribute('transform',`translate(${-40+30*Math.sin(t*1.5)} 10)`)}
 if(vis(sw30,t,W_('e3','30')-.3,e3b)>0){tr(sw30,CX,450,pop(t,W_('e3','30')-.3),0,1);const k=P(t,W_('e3','30')-.1,1.4);sw30.set(k,Math.round(30*k)+'s')}
 if(vis(gentle,t,e3b,Gs('e7')-.1)>0){gentle.setAttribute('transform',`translate(${CX} ${t<Gs('e5')-.1?420:640}) scale(${t<Gs('e5')-.1?1:.6})`);carE.setAttribute('transform','translate(0 40)');const sp=t<Gs('e5')?.5:1;
  dashE.forEach((d,i)=>d.setAttribute('x',((i*150-t*300*sp)%1050+1050)%1050-525));carE.firstChild.setAttribute('transform',`scale(.42) translate(0 ${1.2*Math.sin(t*20)})`);exE.upd(t,-200,70,-60,-20,2,1,14)}
 const t5=Gs('e5')-.1;
 if(vis(tenP,t,t5,Gs('e6')-.1)>0)tr(tenP,CX,250,pop(t,t5),0,1);
 if(vis(tachE,t,W_('e5','hard')-.3,Gs('e6')-.1)>0){tr(tachE,CX-170,470,.9*pop(t,W_('e5','hard')-.3),0,1);tachE.zone.setAttribute('opacity',1);tachE.set(1.5+.8*(.5+.5*Math.sin(t*1.4)))}
 if(vis(noHard,t,W_('e5','hard')-.3,Gs('e6')-.1)>0)tr(noHard,CX+230,420,pop(t,W_('e5','hard')-.3),0,1);
 if(vis(noRev,t,W_('e5','revs')-.4,Gs('e6')-.1)>0)tr(noRev,CX+230,520,pop(t,W_('e5','revs')-.4),0,1);
 if(vis(tgE,t,Gs('e6')-.1,Gs('e7')-.1)>0){tr(tgE,CX-190,330,pop(t,Gs('e6')-.1),0,1);tgE.set(lerp(.05,.5,eo(P(t,Gs('e6')+.2,2.4))));tr(fastP,CX-190,200,pop(t,W_('e6','fastest')-.3),0,on(t,W_('e6','fastest')-.3))}
 if(vis(vent,t,W_('e6','heat')-.4,Gs('e7')-.1)>0){tr(vent,CX+230,330,pop(t,W_('e6','heat')-.4),0,1);waves.forEach((w,i)=>{const y=-90-((t*60+i*30)%90);w.setAttribute('d',`M${-80+i*80} ${y+40} q15 -15 0 -30 q-15 -15 0 -30`);w.style.opacity=1-((t*60+i*30)%90)/90});cabinP.setAttribute('transform','translate(0 130)')}
 if(vis(brut,t,Gs('e7')-.1,Gs('e10')-.1)>0){brut.setAttribute('transform',`translate(${CX} 0)`);const tb=W_('e7','0')-.4;tr(thE,-290,420,.9*pop(t,Gs('e7')-.1),0,1);thE.set(lerp(20,0,eo(P(t,tb,.8))),-20,90);tr(frostE,-190,240,.7*pop(t,W_('e7','brutally')-.2),t*20,on(t,W_('e7','brutally')-.2));
  const tm=W_('e8','minute')-.3;tr(minP,40,440,pop(t,tm),0,on(t,tm));sw2.set(eo(P(t,tm,1.6))*.9,'1-2 MIN');const tmn=W_('e8','manual')-.4;tr(man,330,440,.8*pop(t,tmn),0,on(t,tmn));
  const ta=W_('e9','advice')-.6;tr(advice,330,440,pop(t,ta),4,on(t,ta));man.style.opacity=on(t,tmn)*(1-on(t,ta))}
 if(vis(bh,t,Gs('e10')-.1,PF+.05)>0){tr(bh,CX-60,440,.8*pop(t,Gs('e10')-.1),0,1);const k=eo(P(t,W_('e10','heater')-.2,1));coil.setAttribute('stroke',k>.5?WARM:'#3A3A46');bhGlow.setAttribute('opacity',k);tr(bhP,0,-300,pop(t,W_('e10','engine')-.3),0,on(t,W_('e10','engine')-.3));tr(bigD,0,370,pop(t,W_('e10','big')-.3),0,on(t,W_('e10','big')-.3))}
});
EVF.push(A=>{
 A(PE,'whoosh',.4,.4);A(PE+.1,'pop',0,.5);A(W_('e2','Start')-.05,'click',0,.8);A(W_('e2','Start')+.1,'start',0,.4);A(W_('e2','Start')+.3,'idle',1.0,.25);
 A(W_('e3','Buckle')-.05,'click',0,.9);A(W_('e3','mirrors')-.3,'pop',0,.5);A(W_('e3','30')-.1,'gearticks',1.4,.4);A(W_('e4','gently')-.3,'check',0,.6);
 A(Gs('e5')-.1,'pop',0,.5);A(W_('e5','hard')-.3,'pop',0,.5);A(W_('e5','revs')-.4,'pop',0,.5);A(Gs('e6')-.1,'whoosh',.4,.35);A(W_('e6','fastest')-.3,'riserE',.8,.25);A(W_('e6','heat')-.4,'air',1.2,.3);
 A(Gs('e7')-.1,'whoosh',.4,.4);A(W_('e7','brutally')-.2,'pop',0,.5);A(W_('e7','0')-.4,'pop',0,.4);A(W_('e8','minute')-.3,'gearticks',1.6,.35);A(W_('e8','manual')-.4,'pop',0,.5);A(W_('e9','advice')-.6,'whoosh',.3,.3);
 A(Gs('e10')-.1,'whoosh',.4,.4);A(W_('e10','heater')-.2,'glow',1.2,.4);A(W_('e10','big')-.3,'check',0,.6);
});
