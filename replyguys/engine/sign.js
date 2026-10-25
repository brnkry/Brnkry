// Small "Reply Guys" neon sign hanging at the top of the frame. Flickers now and then and keeps changing:
// logo + name (colour changes every cycle) -> "EPISODE 01" -> back, with a neon switch-flicker between states.
(function(){
const NS='http://www.w3.org/2000/svg';const el=(t,a={},p)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e};
const svg=document.getElementById('sign');const d=el('defs',{},svg);
const gf=el('filter',{id:'sgl',x:'-30%',y:'-80%',width:'160%',height:'260%'},d);el('feGaussianBlur',{in:'SourceGraphic',stdDeviation:7,result:'a'},gf);el('feGaussianBlur',{in:'SourceGraphic',stdDeviation:16,result:'b'},gf);
{const m=el('feMerge',{},gf);['b','a','a'].forEach(x=>el('feMergeNode',{in:x},m))}
const CX=540,CY=252,W=520,H=104;
const root=el('g',{},svg);
el('line',{x1:CX-170,y1:0,x2:CX-170,y2:CY-H/2,stroke:'#3A3640','stroke-width':4},root);el('line',{x1:CX+170,y1:0,x2:CX+170,y2:CY-H/2,stroke:'#3A3640','stroke-width':4},root);
el('rect',{x:CX-W/2+6,y:CY-H/2+10,width:W,height:H,rx:24,fill:'rgba(0,0,0,.18)'},root);
el('rect',{x:CX-W/2,y:CY-H/2,width:W,height:H,rx:24,fill:'#17141F',stroke:'#2D2838','stroke-width':6},root);
const COLS=[['#FF3DA5','#FFD3EA'],['#3DE6FF','#D6FAFF'],['#C6FF3D','#F1FFD0'],['#B76BFF','#EBDCFF']];
function ntext(p,x,y,size,str,anchor='middle'){const g=el('g',{},p);const a={x,y,'font-family':'Neon','font-size':size,'letter-spacing':3,'text-anchor':anchor};
  const glow=el('text',{...a,filter:'url(#sgl)'},g);const core=el('text',a,g);glow.textContent=core.textContent=str;
  g.col=i=>{const [c,pl]=COLS[i%COLS.length];glow.setAttribute('fill',c);core.setAttribute('fill',pl)};g.glow=glow;return g}
const A=el('g',{},root);const mk=el('g',{transform:`translate(${CX-186} ${CY+13}) scale(.25)`},A);const mark=makeMark(svg,mk,{word:false});
const name=ntext(A,CX-116,CY+21,60,'REPLY GUYS','start');
const B=el('g',{},root);const ep=ntext(B,CX,CY+21,58,window.EPISODE||'EPISODE 01');
// short videos (<20 s) use a faster cycle so the episode label still shows up
const PER=(window.DUR||60)<20?window.DUR/2:13,SPLIT=PER*(PER<13?.6:9.5/13);
const hash=n=>{const x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x)};
window.renderSign=function(t){
  const cyc=Math.floor(t/PER),u=t-cyc*PER;const showA=u<SPLIT;
  // switch flicker around each state change
  const sw=Math.min(Math.abs(u),Math.abs(u-SPLIT),Math.abs(u-PER));let on=1;
  if(t>0.6&&sw<(PER<13?.22:.45)){on=hash(Math.floor(t*20))>.45?1:.08}
  else if(hash(Math.floor(t*15)+7)<.025)on=.25; // random buzz
  const g=on;A.style.display=showA?'':'none';B.style.display=showA?'none':'';
  name.col(cyc);ep.col(cyc+2);name.style.opacity=ep.style.opacity=.15+.85*g;name.glow.style.opacity=ep.glow.style.opacity=g;
  // the two reply bubbles take turns lighting up, like a back-and-forth
  const P=mark.parts,side=Math.floor(t/1.6)%2;P.L.set(g*(side?1:.55));P.R.set(g*(side?.55:1));P.Q.set(g*(.6+.4*Math.abs(Math.sin(t*2))));
};
})();
