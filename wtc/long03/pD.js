// ================= PART D: the oil (multigrade, 0W-20) =================
const PE=Gs('e1')-.1;
const oilG=g();const bottle=g(oilG);
el('path',{d:'M-120 -160 L40 -160 L40 -230 Q40 -250 60 -250 L100 -250 Q120 -250 120 -230 L120 200 Q120 230 90 230 L-90 230 Q-120 230 -120 200 Z',fill:'#E9C46A'},bottle);
el('path',{d:'M-120 -160 L-40 -160 L-40 -60 L-120 -60 Z',fill:'#121216',opacity:.25},bottle);el('rect',{x:46,y:-290,width:68,height:46,rx:10,fill:RED},bottle);
const labelC=g(bottle);el('rect',{x:-100,y:-20,width:200,height:200,rx:14,fill:CHALK},labelC);const labTop=txt(labelC,0,24,24,'mic','MOTOR OIL');labTop.setAttribute('fill','#6A6A76');
const labMulti=txt(labelC,0,70,26,'bold','MULTIGRADE');labMulti.setAttribute('fill',ASPH);const labVisc=g(labelC);const v0=txt(labVisc,-44,150,64,'bold','0');const vW=txt(labVisc,0,150,64,'bold','W');const v20=txt(labVisc,56,150,64,'bold','-20');[v0,vW,v20].forEach(x=>x.setAttribute('fill',ASPH));
const drip=el('path',{fill:'#C9962E'},oilG);const thickQ=pill(oilG,'TOO THICK WHEN COLD?',GRAPH,CHALK,400,28);const oilFl=flake(oilG,.6);
const winterW=g(oilG);const wBig=txt(winterW,0,0,160,'bold acc','W');const wWord=txt(winterW,0,70,56,'bold ink','= WINTER');
const scale=g();el('rect',{x:-420,y:-20,width:840,height:40,rx:20,fill:'#2A2A33'},scale);const grades=['0W','5W','10W','15W','20W'].map((s,i)=>{const x=-360+i*180;const c=el('circle',{cx:x,r:34,fill:'#3A3A46'},scale);const tt_=txt(scale,x,10,26,'bold ink',s);return {c,tt_,x}});
const lowArrow=g(scale);el('path',{d:'M0 -110 L0 -60 M-20 -80 L0 -56 L20 -80',fill:'none',stroke:LIME,'stroke-width':10,'stroke-linecap':'round'},lowArrow);const flowsP=pill(scale,'FLOWS BETTER IN THE COLD',LIME,ASPH,460,28);
const flowRow=[...Array(5)].map((_,i)=>{const r=g(scale,{transform:`translate(${-360+i*180} 110)`});el('rect',{x:-8,y:0,width:16,height:150,rx:8,fill:'#22222A'},r);const d=el('circle',{r:10,fill:'#E9C46A'},r);return {r,d,sp:1.6-i*.3}});
// lubrication circuit
const lube=g();el('rect',{x:-340,y:-230,width:680,height:460,rx:40,fill:'#22222A'},lube);
const lpath='M-200 170 L-200 -150 L200 -150 L200 170';el('path',{d:lpath,fill:'none',stroke:'#3A3A46','stroke-width':22,'stroke-linecap':'round'},lube);
const lfill=el('path',{d:lpath,fill:'none',stroke:'#E9C46A','stroke-width':14,'stroke-linecap':'round',pathLength:1000,'stroke-dasharray':'0 1000'},lube);
el('path',{d:'M-260 160 L260 160 L230 220 L-230 220 Z',fill:'#4A4A56'},lube);el('path',{d:'M-244 176 L244 176 L228 212 L-228 212 Z',fill:'#C9962E'},lube);
const lparts=[[-200,-60,'CRANK'],[0,-150,'CAMS'],[200,-60,'BEARINGS']].map(([x,y,s])=>{const p=g(lube,{transform:`translate(${x} ${y})`});const c=el('circle',{r:42,fill:'#3A3A46',stroke:'#6A6A76','stroke-width':6},p);txt(p,0,80,22,'mic mut',s);p.c=c;return p});
const sw=stopwatch(lube,100);const pressP=pill(lube,'OIL PRESSURE',LIME,ASPH,260,26);

KEYS.push([PD+.1,'mid'],[Gs('d2'),'shrug'],[Gs('d3'),'mid'],[Gs('d4'),'top'],[Gs('d5'),'mid'],[Gs('d6'),'mid'],[W_('d6','reaches')-.2,'thumb']);
RENDER.push(t=>{
 if(t<PD-.5||t>PE+.5){show(0,oilG,scale,lube);return}capMode('studio');
 if(vis(oilG,t,PD,Gs('d5')-.1)>0){oilG.setAttribute('transform',`translate(${CX} 0)`);const tilt=lerp(0,100,eio(P(t,PD+.2,.8)))*(1-eio(P(t,Gs('d3')-.3,.6)));
  tr(bottle,-140*(1-eio(P(t,Gs('d3')-.3,.6))),430,.95*pop(t,PD),tilt,1);
  const k=V(t,PD+.9,Gs('d3')-.3,.3,.2);const len=lerp(10,200,(t*0.35)%1);drip.setAttribute('d',`M-14 0 Q-26 ${len*.5} 0 ${len} Q26 ${len*.5} 14 0 Z`);drip.setAttribute('transform','translate(112 560)');drip.style.opacity=k;
  tr(thickQ,120,170,pop(t,Gs('d2')-.1),0,on(t,Gs('d2')-.1)*(1-on(t,Gs('d3')-.2)));tr(oilFl,240,320,.6*pop(t,W_('d2','thick')-.2),t*20,on(t,W_('d2','thick')-.2)*(1-on(t,Gs('d3')-.2)));
  labMulti.style.opacity=on(t,W_('d3','multigrade')-.3);labMulti.setAttribute('fill',t<Gs('d4')?ASPH:'#6A6A76');labVisc.style.opacity=on(t,Gs('d4')-.2);
  const tw=W_('d4','W')-.15,twin=W_('d4','winter')-.3;vW.setAttribute('fill',t>tw?'#2E6BD8':ASPH);
  tr(winterW,280,390,pop(t,tw),0,on(t,tw));wWord.style.opacity=on(t,twin);wWord.setAttribute('transform',`scale(${pop(t,twin)})`)}
 if(vis(scale,t,Gs('d5')-.1,Gs('d6')-.1)>0){tr(scale,CX,340,pop(t,Gs('d5')-.1),0,1);const tl=W_('d5','low')-.3;grades.forEach((gr,i)=>{gr.c.setAttribute('fill',i===0&&t>tl?LIME:'#3A3A46');gr.tt_.style.fill=i===0&&t>tl?ASPH:CHALK});
  tr(lowArrow,-360,0,1,0,on(t,tl));const tf=W_('d5','flows')-.3;tr(flowsP,-160,-160,pop(t,tf),0,on(t,tf));
  flowRow.forEach((f,i)=>{f.r.style.opacity=on(t,tf);f.d.setAttribute('cy',((t-tf)*f.sp*120%150+150)%150)})}
 if(vis(lube,t,Gs('d6')-.1,PE+.05)>0){tr(lube,CX,440,.9*pop(t,Gs('d6')-.1),0,1);const ts=W_('d6','seconds')-.3;const k=eio(P(t,ts,1.6));lfill.setAttribute('stroke-dasharray',`${k*1000} 1000`);
  lparts.forEach((p,i)=>p.c.setAttribute('stroke',k>[.3,.5,.75][i]?'#E9C46A':'#6A6A76'));tr(sw,0,60,.6*pop(t,ts),0,on(t,ts));sw.set(k,Math.min(3,Math.floor(P(t,ts,1.6)*3)+1)+'s');
  const tp=W_('d6','pressure')-.3;tr(pressP,0,-210,pop(t,tp),0,on(t,tp))}
});
EVF.push(A=>{
 A(PD,'whoosh',.4,.4);A(PD+.9,'slurp',1.2,.25);A(Gs('d2')-.1,'pop',0,.5);A(W_('d3','multigrade')-.3,'pop',0,.5);A(W_('d4','W')-.15,'pop',0,.6);A(W_('d4','winter')-.3,'check',0,.6);
 A(Gs('d5')-.1,'whoosh',.4,.4);A(W_('d5','low')-.3,'pop',0,.5);A(W_('d5','flows')-.3,'check',0,.5);
 A(Gs('d6')-.1,'whoosh',.4,.4);A(W_('d6','seconds')-.3,'pump',1.6,.35);A(W_('d6','pressure')-.3,'check',0,.6);
});
