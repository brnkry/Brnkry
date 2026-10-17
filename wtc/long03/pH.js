// ================= PART H: short version + close + end card =================
const sv=g();const svT=pill(sv,'THE SHORT VERSION',LIME,ASPH,400,32);
function column(p,title,col,items){const c=g(p);el('rect',{x:-250,y:-60,width:500,height:120+items.length*84,rx:30,fill:GRAPH},c);const h=txt(c,0,20,46,'bold',title);h.setAttribute('fill',col);
  c.rows=items.map((s,i)=>{const r=g(c,{transform:`translate(-200 ${110+i*84})`});const ck=CHECK(r,.85);const tt_=txt(r,50,10,30,'bold ink',s,'start');r.ck=ck;r.tt_=tt_;return r});return c}
const colGas=column(sv,'GAS',CHALK,['START IT','BUCKLE UP','30 SECONDS','DRIVE GENTLY']);
const colDsl=column(sv,'DIESEL',DIESEL,['GLOW PLUG LIGHT','BLOCK HEATER','SHORT IDLE','DRIVE GENTLY','WINTER FUEL']);
const vs=g();const old=g(vs);const oldC=card(old,420,380,'#3A2E22');const oldCar=g(oldC,{transform:'translate(0 -40)'});el('path',{d:'M-150 30 L-150 -6 L-110 -10 L-84 -54 L60 -54 L90 -10 L150 -4 L150 30 Z',fill:SEPIA},oldCar);[-90,90].forEach(x=>el('circle',{cx:x,cy:32,r:28,fill:'#1C140C'},oldCar));
txt(oldC,0,80,30,'mic','GRANDPA’S CAR').setAttribute('fill',SEPIA);const oldT=txt(oldC,0,150,70,'bold','10 MIN');oldT.setAttribute('fill',SEPIA);
const neu=g(vs);const neuC=card(neu,420,380,'#1E3326');const nc=carIcon(neuC,.3,{body:LIME});nc.setAttribute('transform','translate(0 -40)');txt(neuC,0,80,30,'mic acc','YOURS');const neuT=txt(neuC,0,150,70,'bold acc','30 SEC');
const foot=pill(vs,'+ A LIGHT RIGHT FOOT',LIME,ASPH,420,30);
const bubC=g();el('path',{d:'M-330 -140 h660 a40 40 0 0 1 40 40 v180 a40 40 0 0 1 -40 40 h-480 l-80 70 v-70 h-100 a40 40 0 0 1 -40 -40 v-180 a40 40 0 0 1 40 -40 Z',fill:GRAPH},bubC);
const bq=txt(bubC,-290,-60,32,'bold ink','HOW LONG DO YOU WARM UP?','start');const bA=txt(bubC,-290,0,30,'mic acc','','start');const bB=txt(bubC,-290,50,30,'mic mut','','start');
const comIc=g(bubC,{transform:'translate(300 -170)'});el('circle',{r:46,fill:RED},comIc);el('path',{d:'M-22 -14 h44 v26 h-24 l-12 10 v-10 h-8 Z',fill:CHALK},comIc);
// end card (after the voice): logo top, empty areas for YouTube end-screen elements
const endG=g();el('rect',{x:0,y:0,width:1920,height:1080,fill:ASPH},endG);el('circle',{cx:960,cy:330,r:520,fill:'url(#spot)'},endG);
const face=makeFace(endG);if(face.q)face.q.style.display='none';
const wm=el('text',{x:0,y:0,'text-anchor':'middle'},endG);[['WHAT THE ',CHALK,60,'700'],['CAR',LIME,130,'800'],['?',RED,130,'800']].forEach(([s,c,fs,fw])=>{const sp=el('tspan',{fill:c,'font-size':fs,style:`font-family:WTC;font-weight:${fw};font-stretch:75%;letter-spacing:.02em`},wm);sp.textContent=s});
const nextT=txt(endG,520,690,30,'mic mut','WATCH NEXT');const subT2=txt(endG,1400,690,30,'mic mut','SUBSCRIBE');const endFl=snowfall(endG,40);

KEYS.push([PH+.1,'mid'],[Gs('h2'),'left'],[Gs('h3'),'right'],[Gs('h4'),'mid'],[Gs('h5'),'thumb'],[Gs('h6'),'open'],[Gs('h7'),'wave'],[VO_END_+.6,'rest']);
MOODS.push([Gs('h4'),999,{smile:.75}]);
RENDER.push(t=>{
 if(t<PH-.5){show(0,sv,vs,bubC,endG);return}capMode('studio');
 if(vis(sv,t,PH,Gs('h4')-.1)>0){sv.setAttribute('transform',`translate(${CX} 0)`);tr(svT,0,150,pop(t,PH),0,1);tr(colGas,-270,270,.9*pop(t,Gs('h2')-.1),0,on(t,Gs('h2')-.1));tr(colDsl,270,270,.9*pop(t,Gs('h3')-.1),0,on(t,Gs('h3')-.1));
  const tg=[W_('h2','start'),W_('h2','buckle'),W_('h2','30'),W_('h2','drive')];colGas.rows.forEach((r,i)=>{const a=tg[i]-.2;r.ck.style.opacity=on(t,a);r.ck.setAttribute('transform',`scale(${.85*pop(t,a,.3)})`);r.tt_.style.fill=t>a?CHALK:H.smoke});
  const td=[W_('h3','glow'),W_('h3','block'),W_('h3','short'),W_('h3','drive'),W_('h3','winter')];colDsl.rows.forEach((r,i)=>{const a=td[i]-.2;r.ck.style.opacity=on(t,a);r.ck.setAttribute('transform',`scale(${.85*pop(t,a,.3)})`);r.tt_.style.fill=t>a?CHALK:H.smoke})}
 if(vis(vs,t,Gs('h4')-.1,Gs('h6')-.1)>0){vs.setAttribute('transform',`translate(${CX} 0)`);tr(old,-230,420,pop(t,Gs('h4')-.1),-3,1);const tn=Gs('h5')-.1;tr(neu,230,420,pop(t,tn),3,on(t,tn));tr(foot,230,700,pop(t,W_('h5','light')-.3),0,on(t,W_('h5','light')-.3))}
 if(vis(bubC,t,Gs('h6')-.1,VO_END_+.4)>0){tr(bubC,CX,420,pop(t,Gs('h6')-.1),0,1);const s1='Like 5 minutes... oops.',s2='30 seconds from now on!';bA.textContent=s1.slice(0,Math.round(s1.length*P(t,Gs('h6')+.8,1.2)));bB.textContent=s2.slice(0,Math.round(s2.length*P(t,Gs('h7'),1.0)));
  tr(comIc,300,-170,pop(t,W_('h7','comments')-.3),0,on(t,W_('h7','comments')-.3))}
 const ke=V(t,VO_END_+.2,999,.5,.1);show(ke,endG);if(ke>0){endG.style.opacity=ke;tr(face,960,300,.85*pop(t,VO_END_+.3,.5),0,1);face.look(Math.sin(t*1.2)*.5,-.2);wm.setAttribute('transform','translate(960 560)');wm.style.opacity=eo(P(t,VO_END_+.6,.4));
  nextT.style.opacity=subT2.style.opacity=eo(P(t,VO_END_+1,.4));endFl.upd(t,.6)}
});
EVF.push(A=>{
 A(PH,'whoosh',.45,.45);A(Gs('h2')-.1,'pop',0,.5);[W_('h2','start'),W_('h2','buckle'),W_('h2','30'),W_('h2','drive')].forEach(x=>A(x-.2,'check',0,.45));
 A(Gs('h3')-.1,'pop',0,.5);[W_('h3','glow'),W_('h3','block'),W_('h3','short'),W_('h3','drive'),W_('h3','winter')].forEach(x=>A(x-.2,'check',0,.45));
 A(Gs('h4')-.1,'whoosh',.4,.4);A(Gs('h5')-.1,'pop',0,.6);A(W_('h5','light')-.3,'check',0,.6);A(Gs('h6')-.1,'pop',0,.5);A(Gs('h6')+.8,'typing',1.2,.5);A(Gs('h7'),'typing',1.0,.5);A(W_('h7','comments')-.3,'pop',0,.6);
 A(VO_END_+.2,'whoosh',.5,.45);A(VO_END_+.4,'stinger',0,.8);
});
