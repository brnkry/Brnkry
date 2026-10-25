// Reply Guys neon brand mark. makeMark(svg,parent) -> group with .parts {L: left bubble, R: right bubble, Q: mic, word} (each has .set(on 0..1))
// Mark is drawn around (0,0): mic in the middle, reply bubbles left/right, wordmark below. Needs fonts "Neon" loaded.
(function(){
const NS='http://www.w3.org/2000/svg';
function el(tag,a={},p){const e=document.createElementNS(NS,tag);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
const C={pink:'#FF3DA5',cyan:'#3DE6FF',lime:'#C6FF3D',pale:{pink:'#FFD3EA',cyan:'#D6FAFF',lime:'#F1FFD0'}};
let fid=0;
function defs(svg){let d=svg.querySelector('defs')||el('defs',{},svg);const id='ng'+(fid++);
  const f=el('filter',{id,x:'-60%',y:'-60%',width:'220%',height:'220%'},d);
  el('feGaussianBlur',{in:'SourceGraphic',stdDeviation:6,result:'a'},f);el('feGaussianBlur',{in:'SourceGraphic',stdDeviation:18,result:'b'},f);
  const m=el('feMerge',{},f);el('feMergeNode',{in:'b'},m);el('feMergeNode',{in:'b'},m);el('feMergeNode',{in:'a'},m);return id}
// tube(parent, color, width, draw(g, stroke, width)) : glow + tube + white-ish core
function tube(svg,parent,color,w,draw){const g=el('g',{},parent);const id=defs(svg);
  const glow=el('g',{filter:`url(#${id})`},g);draw(glow,color,w*1.5);const mid=el('g',{},g);draw(mid,color,w);const core=el('g',{},g);draw(core,C.pale[color===C.pink?'pink':color===C.cyan?'cyan':'lime'],w*.4);
  g.set=v=>{g.style.opacity=.18+.82*v;glow.style.opacity=v};return g}
const P=(g,d,s,w)=>el('path',{d,fill:'none',stroke:s,'stroke-width':w,'stroke-linecap':'round','stroke-linejoin':'round'},g);
const Ci=(g,cx,cy,r,s,w)=>el('circle',{cx,cy,r,fill:'none',stroke:s,'stroke-width':w},g);
window.makeMark=function(svg,parent,opts={}){const root=el('g',{},parent);const parts={};
  // left reply bubble (?) and right reply bubble (!) arguing across a podcast mic: works for any cast of characters
  const bub=(g,s,w,x,dir,ch)=>{P(g,`M${x-70} -60 H${x+70} Q${x+92} -60 ${x+92} -38 V24 Q${x+92} 46 ${x+70} 46 H${x+dir*30} L${x+dir*52} 78 L${x+dir*4} 46 H${x-70} Q${x-92} 46 ${x-92} 24 V-38 Q${x-92} -60 ${x-70} -60 Z`,s,w);
    el('text',{x,y:30,'text-anchor':'middle','font-family':'Neon','font-size':96,fill:s,stroke:'none'},g).textContent=ch};
  parts.L=tube(svg,root,C.pink,7,(g,s,w)=>bub(g,s,w,-150,1,'?'));
  parts.R=tube(svg,root,C.cyan,7,(g,s,w)=>bub(g,s,w,150,-1,'!'));
  parts.Q=tube(svg,root,C.lime,7,(g,s,w)=>{P(g,'M-26 -120 H26 Q40 -120 40 -106 V-20 Q40 -6 26 -6 H-26 Q-40 -6 -40 -20 V-106 Q-40 -120 -26 -120 Z',s,w);
    P(g,'M-40 -84 H40 M-40 -56 H40 M-52 -50 V-26 Q-52 22 0 22 Q52 22 52 -26 V-50 M0 22 V64 M-34 66 H34',s,w)});
  if(opts.word!==false)parts.word=tube(svg,root,C.pink,0,(g,s)=>{el('text',{x:0,y:opts.wordY||200,'text-anchor':'middle','font-family':'Neon','font-size':opts.wordSize||92,'letter-spacing':4,fill:s},g).textContent='REPLY GUYS'});
  root.parts=parts;return root};
window.NEON=C;
})();
