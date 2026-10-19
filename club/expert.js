// "The driver / narrator": front-view vector character with a 2-bone arm rig.
// Origin = base of the neck. Head centre ~(0,-170). Torso goes down to y ~520.
// rig.set({mouth,smile,browUp,browWorry,eyes,pupil,look:[dx,dy],tilt,nod,amber,hands:{L:{x,y,shape,rot},R:{...}}})
(function(){
const NS="http://www.w3.org/2000/svg";
function E(tag,a={},p){const e=document.createElementNS(NS,tag);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
const SKIN='#EFC3A4',SKIN_D='#D49E7E',HAIR='#4A2E22',LIP='#C0665E',MOUTH='#5A2A26',JACKET='#FBF8F3',JACKET_D='#E4DBD0',TEE='#744834',LIME='#744834';
const SH={L:[-182,46],R:[182,46]},L1=160,L2=150;
function ik(S,T,bend){let dx=T[0]-S[0],dy=T[1]-S[1];let d=Math.hypot(dx,dy);const mx=L1+L2-1;if(d>mx){dx*=mx/d;dy*=mx/d;d=mx}d=Math.max(d,40);
  const a=Math.atan2(dy,dx);const c=Math.min(1,Math.max(-1,(L1*L1+d*d-L2*L2)/(2*L1*d)));const b=Math.acos(c);
  // pick the elbow that hangs lower and sits on the outside (bend = outward x sign)
  const cand=[a+b,a-b].map(q=>[S[0]+L1*Math.cos(q),S[1]+L1*Math.sin(q)]);const sc=e=>e[1]+0.6*bend*(e[0]-S[0]);
  return {E:sc(cand[0])>=sc(cand[1])?cand[0]:cand[1],W:[S[0]+dx,S[1]+dy]}}
function hand(p){const h=E('g',{},p);const shapes={};
  const fist=()=>{const g=E('g',{},h);E('rect',{x:-8,y:-29,width:58,height:58,rx:24,fill:SKIN},g);E('path',{d:'M30 -18 v36 M40 -14 v28',stroke:SKIN_D,'stroke-width':4,'stroke-linecap':'round'},g);return g};
  shapes.fist=fist();
  shapes.open=E('g',{},h);E('ellipse',{cx:22,cy:0,rx:30,ry:30,fill:SKIN},shapes.open);[-21,-7,7,21].forEach((y,i)=>E('rect',{x:34,y:y-6,width:i==0||i==3?36:44,height:12,rx:6,fill:SKIN},shapes.open));E('rect',{x:4,y:-50,width:13,height:32,rx:6,fill:SKIN,transform:'rotate(-25 10 -20)'},shapes.open);
  shapes.point=E('g',{},h);E('rect',{x:-8,y:-29,width:52,height:58,rx:24,fill:SKIN},shapes.point);E('rect',{x:30,y:-28,width:62,height:15,rx:7.5,fill:SKIN},shapes.point);E('rect',{x:6,y:-40,width:30,height:13,rx:6,fill:SKIN},shapes.point);
  shapes.thumb=E('g',{},h);E('rect',{x:-8,y:-29,width:58,height:58,rx:24,fill:SKIN},shapes.thumb);E('rect',{x:2,y:-74,width:18,height:52,rx:9,fill:SKIN},shapes.thumb);E('path',{d:'M30 -14 v28 M40 -10 v20',stroke:SKIN_D,'stroke-width':4,'stroke-linecap':'round'},shapes.thumb);
  h.shape=s=>{for(const k in shapes)shapes[k].style.display=k===s?'':'none'};h.shape('fist');return h}

window.makeExpert=function(parent){
  const root=E('g',{},parent);
  const body=E('g',{},root);
  // torso: jacket, tee, zipper
  E('path',{d:'M-60 -14 Q-172 -6 -212 70 L-238 560 L238 560 L212 70 Q172 -6 60 -14 Z',fill:JACKET},body);
  E('path',{d:'M-58 -14 L0 96 L58 -14 Z',fill:TEE},body);
  E('path',{d:'M-62 -14 L-8 120 M62 -14 L8 120',stroke:JACKET_D,'stroke-width':6,fill:'none'},body);
  E('path',{d:'M-58 -14 L-20 150 L-110 60 Z M58 -14 L20 150 L110 60 Z',fill:'#F1EBE3'},body);E('path',{d:'M0 150 L0 560',stroke:'#E4DBD0','stroke-width':4},body);
  const badge=E('g',{transform:'translate(-120 190)'},body);E('rect',{x:-58,y:-22,width:116,height:44,rx:10,fill:'#744834'},badge);const bt=E('text',{x:0,y:8,'text-anchor':'middle','font-size':20,fill:'#FBF8F3',style:'font-family:QS;font-weight:700;letter-spacing:.04em'},badge);bt.textContent='WTC EXPERT';
  E('path',{d:'M-212 70 Q-150 40 -100 40 M212 70 Q150 40 100 40',stroke:JACKET_D,'stroke-width':5,fill:'none'},body);
  const props=E('g',{},root); // seat belt etc. go here (between torso and head/arms)
  // neck + head
  const headG=E('g',{},root);
  const hairBack=E('path',{d:'M-128 -210 Q-150 -330 -40 -350 Q60 -364 120 -318 Q160 -280 150 -180 Q156 -40 176 60 Q120 90 70 40 L-70 40 Q-120 90 -176 60 Q-150 -40 -128 -210 Z',fill:'#4A2E22'},headG);
  E('path',{d:'M-38 -70 L-40 0 Q0 22 40 0 L38 -70 Z',fill:SKIN_D},headG);
  const head=E('g',{},headG);
  [[-104,1],[104,-1]].forEach(([x,s])=>{E('ellipse',{cx:x,cy:-172,rx:20,ry:30,fill:SKIN},head);E('path',{d:`M${x+s*-2} -186 q${s*10} 12 0 26`,stroke:SKIN_D,'stroke-width':4,fill:'none'},head)});
  const FACE='M-96 -228 Q-100 -136 -66 -92 Q-34 -56 0 -54 Q34 -56 66 -92 Q100 -136 96 -228 Q92 -300 0 -304 Q-92 -300 -96 -228 Z';
  E('path',{d:FACE,fill:SKIN},head);
  E('path',{d:'M30 -296 Q100 -280 100 -228 Q104 -128 72 -86 Q48 -58 20 -50 Q70 -110 70 -200 Q70 -270 30 -296 Z',fill:SKIN_D,opacity:.35},head);
  [-62,62].forEach(x=>E('ellipse',{cx:x,cy:-138,rx:22,ry:12,fill:'#E89A8A',opacity:.35},head)); // blush
  const amber=E('path',{d:FACE,fill:'#FFB000',opacity:0,style:'mix-blend-mode:screen'},head);
  // eyes
  const eyes=[-40,40].map(x=>{const g=E('g',{transform:`translate(${x} -186)`},head);
    E('ellipse',{rx:21,ry:14,fill:'#FFFFFF'},g);const iris=E('g',{},g);E('circle',{r:10.5,fill:'#5B3A22'},iris);const pup=E('circle',{r:5,fill:'#120C08'},iris);E('circle',{cx:3.5,cy:-4,r:2.6,fill:'#FFFFFF'},iris);
    const lid=E('rect',{x:-24,y:-18,width:48,height:0,fill:SKIN},g);const lash=E('path',{d:'M-24 2 Q0 -18 24 2 M18 -4 l10 -6',stroke:'#2A1A14','stroke-width':5,fill:'none','stroke-linecap':'round'},g);
    return {g,iris,pup,lid,lash}});
  const brows=[-1,1].map(s=>E('path',{fill:'none',stroke:HAIR,'stroke-width':11,'stroke-linecap':'round'},head));
  E('path',{d:'M-4 -178 Q-12 -140 -18 -128 Q-6 -118 12 -126',stroke:SKIN_D,'stroke-width':5,fill:'none','stroke-linecap':'round'},head);
  const mouthIn=E('path',{fill:MOUTH},head);const teeth=E('path',{fill:'#FFFFFF'},head);const lip=E('path',{fill:'none',stroke:LIP,'stroke-width':6.5,'stroke-linecap':'round','stroke-linejoin':'round'},head);
  // hair on top: soft side-swept fringe + side curtains framing the face
  E('path',{d:'M-112 -200 Q-126 -310 -30 -330 Q60 -346 112 -296 Q130 -262 112 -196 Q100 -250 40 -262 Q-10 -282 -60 -250 Q-96 -228 -112 -200 Z',fill:HAIR},head);
  E('path',{d:'M-112 -220 Q-130 -120 -112 -30 Q-96 -90 -96 -180 Z',fill:HAIR},head);E('path',{d:'M112 -220 Q130 -120 112 -30 Q96 -90 96 -180 Z',fill:HAIR},head);
  E('path',{d:'M-40 -300 Q30 -320 90 -280',stroke:'#6A4434','stroke-width':6,fill:'none','stroke-linecap':'round'},head);
  [-1,1].forEach(s=>E('circle',{cx:s*106,cy:-150,r:7,fill:'#E9C9A0'},head)); // small earrings
  // arms (sleeves) + hands on top
  const arms=E('g',{},root);
  const arm={};['L','R'].forEach(k=>{const g=E('g',{},arms);const o=E('path',{fill:'none',stroke:JACKET_D,'stroke-width':76,'stroke-linecap':'round','stroke-linejoin':'round'},g);const f=E('path',{fill:'none',stroke:JACKET,'stroke-width':64,'stroke-linecap':'round','stroke-linejoin':'round'},g);
    const cuff=E('circle',{r:30,fill:JACKET_D},g);const held=E('g',{},g);const h=hand(g);arm[k]={o,f,cuff,h,held}});
  const st={mouth:0,smile:0,browUp:0,browWorry:0,eyes:1,pupil:1,look:[0,0],tilt:0,nod:0,amber:0,
    hands:{L:{x:-200,y:330,shape:'fist'},R:{x:200,y:330,shape:'fist'}}};
  root.head=head;root.props=props;root.arm=arm;root.SH=SH;
  root.set=function(opts){Object.assign(st,opts);
    head.setAttribute('transform',`translate(0 ${st.nod*6}) rotate(${st.tilt} 0 -60)`);
    // eyes
    eyes.forEach(e=>{e.iris.setAttribute('transform',`translate(${st.look[0]*9} ${st.look[1]*5}) scale(${st.pupil})`);
      const open=Math.max(0,Math.min(1,st.eyes));const sc=1+.25*Math.max(0,st.browUp);e.g.setAttribute('transform',`translate(${e===eyes[0]?-40:40} -186) scale(1 ${sc})`);
      e.lid.setAttribute('height',28*(1-open)+ (open<1?2:0));e.lid.setAttribute('y',-18+(1-open)*0);e.lash.setAttribute('transform',`translate(0 ${-14*open+14})`);e.lash.style.opacity=open<.6?1:0});
    // brows: s=-1 left, 1 right
    brows.forEach((b,i)=>{b.setAttribute('stroke-width',8);const s=i?1:-1;const up=st.browUp*16,w=st.browWorry*12;
      const xi=s*18,xo=s*68;const yi=-214-up-w,yo=-212-up+w*0.6;b.setAttribute('d',`M${xi} ${yi} Q${s*44} ${-226-up} ${xo} ${yo}`)});
    // mouth: corners (±w, y0), opening o, smile s
    const o=Math.max(0,st.mouth),s=st.smile;const w=40+7*s-6*o;const y0=-98-7*s;
    const up=-100-3*o-(s>0?2*s:0),lo=-98+40*o+12*Math.max(0,s)-6*Math.min(0,s);
    const d=`M${-w} ${y0} Q0 ${up} ${w} ${y0} Q0 ${lo} ${-w} ${y0} Z`;
    mouthIn.setAttribute('d',d);mouthIn.style.opacity=o>.04?1:0;
    teeth.setAttribute('d',`M${-w*.7} ${y0+1} Q0 ${up+2} ${w*.7} ${y0+1} L${w*.6} ${y0+3+6*o} Q0 ${up+6+8*o} ${-w*.6} ${y0+3+6*o} Z`);teeth.style.opacity=o>.25&&s>-.3?1:0;
    lip.setAttribute('d',o>.04?d:`M${-w} ${y0} Q0 ${lo+2} ${w} ${y0}`);
    amber.setAttribute('opacity',.45*st.amber);
    // arms
    ['L','R'].forEach(k=>{const hd=st.hands[k];const S=SH[k];const r=ik(S,[hd.x,hd.y],k==='L'?-1:1);const A=arm[k];
      const dd=`M${S[0]} ${S[1]} L${r.E[0].toFixed(1)} ${r.E[1].toFixed(1)} L${r.W[0].toFixed(1)} ${r.W[1].toFixed(1)}`;A.o.setAttribute('d',dd);A.f.setAttribute('d',dd);
      const fa=Math.atan2(r.W[1]-r.E[1],r.W[0]-r.E[0])*180/Math.PI;const rot=hd.rot!==undefined?hd.rot:fa;const flip=Math.cos(rot*Math.PI/180)<0?-1:1;
      const cx=r.W[0]-Math.cos(fa*Math.PI/180)*18,cy=r.W[1]-Math.sin(fa*Math.PI/180)*18;A.cuff.setAttribute('cx',cx);A.cuff.setAttribute('cy',cy);
      A.h.setAttribute('transform',`translate(${r.W[0]} ${r.W[1]}) rotate(${rot}) scale(1 ${flip})`);A.h.shape(hd.shape||'fist');
      A.held.setAttribute('transform',`translate(${r.W[0]} ${r.W[1]})`);root['W'+k]=r.W})};
  root.set({});return root};
})();
