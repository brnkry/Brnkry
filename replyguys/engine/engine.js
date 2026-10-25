// Reply Guys episode engine (9:16, 1080x1920, 30 fps). Shared by every episode from stick02 on.
// Episode supplies: window.LINES/MEMES/USERS/EPISODE/DUR (lines.js), window.MOUTH (mouth.js) and an ep.js that
// draws the two heads, poses, stickers and memes, and defines EP.render(t).
//
// Layout (from a real YouTube Shorts screenshot on an iPhone): the phone crops ~47 px off each side, the top
// icons sit above y≈215, the channel name + title cover y>1530 and the like/comment buttons sit at x>880 for
// y>1035. So: everything is centred, the floor is at y=1500, both heads stay inside x 160..870,
// bubbles span x 110..970 (only above y 1000) and the neon sign hangs at y≈250.
const NS='http://www.w3.org/2000/svg';
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)),P=(t,t0,d)=>cl((t-t0)/d),lerp=(a,b,k)=>a+(b-a)*k;
const eo=x=>1-Math.pow(1-x,3),eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const back=x=>{const c1=2.2,c3=c1+1;return x<=0?0:1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const V=(t,a,b,fi=.25,fo=.2)=>Math.min(eo(P(t,a,fi)),1-P(t,b-fo,fo));
function el(tag,a={},p){const e=document.createElementNS(NS,tag);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
const G=(p,a={})=>el('g',a,p);
const tr=(e,x,y,s=1,r=0)=>e.setAttribute('transform',`translate(${x} ${y}) rotate(${r}) scale(${s})`);
const op=(e,o)=>{e.style.opacity=o;e.style.display=o>0.001?'':'none'};
const INK='#1B1B1F',RED='#E0353B',BLUE='#2463D9',PAPER='#F6F2E8',GREY='#8C8A84',LIME='#9BC53D',GREEN='#2E8B3A';
const ln=(p,x1,y1,x2,y2,w=9,c=INK)=>el('line',{x1,y1,x2,y2,stroke:c,'stroke-width':w,'stroke-linecap':'round'},p);
const T=(p,x,y,s,size,cls,fill=INK,anchor='middle')=>{const e=el('text',{x,y,'font-size':size,class:cls,fill,'text-anchor':anchor},p);e.textContent=s;return e};
const pth=(p,d,a={})=>el('path',{d,fill:'none',stroke:INK,'stroke-width':6,'stroke-linecap':'round','stroke-linejoin':'round',...a},p);
const L=window.LINES,M=window.MEMES||{};const ID={};L.forEach(l=>ID[l.id]=l);
const inM=(t,k,pad=0)=>M[k]&&t>=M[k][0]-pad&&t<M[k][1]+pad;
const mouthAt=t=>{const A=window.MOUTH;const f=t*30,i=Math.floor(f);return lerp(A[i]||0,A[i+1]||0,f-i)};
const speaking=(who,t)=>L.some(l=>l.who===who&&t>=l.w[0][1]-.1&&t<l.end);
const talkMouth=(who,t)=>speaking(who,t)?mouthAt(t):0;
const blink=(t,per,off)=>{const p=((t+off)%per+per)%per;return p<.13?1-Math.sin(p/.13*Math.PI):1};
function poser(POSE,KEYS,d=.3){return t=>{let i=0;while(i<KEYS.length-1&&t>=KEYS[i+1][0])i++;const a=POSE[KEYS[Math.max(0,i-1)][1]],b=POSE[KEYS[i][1]];const k=eio(P(t,KEYS[i][0],d));
  const o={name:KEYS[i][1],k};for(const key of ['lean','tilt'])o[key]=lerp(a[key]||0,b[key]||0,k);
  for(const h of ['n','f'])o[h]=[lerp(a[h][0],b[h][0],k),lerp(a[h][1],b[h][1],k)];return o}}

// ---------- layout: world (drawing) coords -> screen ----------
const SC=.97,FY=1500,WFLOOR=1572;const W=(x,y)=>[540+(x-540)*SC,FY-(WFLOOR-y)*SC];
const HIP={L:[252,1392],R:[826,1392]};

// ---------- DOM ----------
document.body.insertAdjacentHTML('afterbegin',`<div id="stage"><div id="cam">
<svg id="world" viewBox="0 0 1080 1920" width="1080" height="1920"><defs>
 <filter id="boil" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence id="turb" type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="1"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter>
 <radialGradient id="spot" cx="50%" cy="0%" r="100%"><stop offset="0" stop-color="#FFF3B0" stop-opacity=".9"/><stop offset="1" stop-color="#FFF3B0" stop-opacity="0"/></radialGradient></defs>
 <g id="back" filter="url(#boil)"></g>
 <g transform="translate(540 ${FY}) scale(${SC}) translate(-540 -${WFLOOR})"><g id="room" filter="url(#boil)"></g><g id="actors" filter="url(#boil)"></g></g>
 <g id="bubbles" filter="url(#boil)"></g></svg>
<div id="texts"></div>
<svg id="front" viewBox="0 0 1080 1920" width="1080" height="1920"><defs><filter id="boil2" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence id="turb2" type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="1"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter></defs><g id="fx" filter="url(#boil2)"></g></svg>
</div><div id="tint"></div><svg id="sign" viewBox="0 0 1080 1920" width="1080" height="1920"></svg></div>`);
const $=id=>document.getElementById(id);const room=$('room'),actors=$('actors'),bubG=$('bubbles'),texts=$('texts'),fx=$('fx'),backG=$('back');

// ---------- room ----------
(()=>{ln(backG,0,FY,1080,FY,7);for(let x=30;x<1080;x+=90)ln(backG,x,FY+14,x+40,FY+14,4,'#CFC8B8');
  el('ellipse',{cx:540,cy:WFLOOR-2,rx:330,ry:14,fill:'#E9DFC9',stroke:'#CFC2A6','stroke-width':4},room)})();
const onair=G(room,{transform:'translate(540 1052)'});const oaBox=el('rect',{x:-82,y:-30,width:164,height:60,rx:14,fill:'#3A3A40',stroke:INK,'stroke-width':6},onair);
const oaTxt=T(onair,0,13,'ON AIR',38,'mk','#77777E');ln(onair,0,-30,0,-70,4,'#999');
function chair(x,f,col='#D9534F'){const g=G(room);el('path',{d:`M${x-75*f} 1405 H${x+65*f}`,stroke:INK,'stroke-width':10,'stroke-linecap':'round',fill:'none'},g);
  ln(g,x-70*f,1405,x-80*f,1150,9);ln(g,x-70*f,1405,x-62*f,WFLOOR,8);ln(g,x+58*f,1405,x+66*f,WFLOOR,8);
  el('rect',{x:Math.min(x-92*f,x-62*f),y:1170,width:30,height:150,rx:12,fill:col,stroke:INK,'stroke-width':6,transform:`rotate(${-2*f} ${x-77*f} 1240)`},g);return g}

// ---------- stick figures (heads are drawn by the episode into r.head, centred at 0,0, r≈62) ----------
const L1=86,L2=84;
function ik(S,Tg,bend){let dx=Tg[0]-S[0],dy=Tg[1]-S[1];let d=Math.hypot(dx,dy);const mx=L1+L2-1;if(d>mx){dx*=mx/d;dy*=mx/d;d=mx}d=Math.max(d,30);
  const a=Math.atan2(dy,dx);const c=cl((L1*L1+d*d-L2*L2)/(2*L1*d),-1,1);const b=Math.acos(c);
  const cand=[a+b,a-b].map(q=>[S[0]+L1*Math.cos(q),S[1]+L1*Math.sin(q)]);const sc=e=>e[1]-0.5*bend*(e[0]-S[0]);
  return {E:sc(cand[0])>=sc(cand[1])?cand[0]:cand[1],W:[S[0]+dx,S[1]+dy]}}
const LEGS={lazy:(x,y,f)=>[[[x,y],[x+120*f,y-22],[x+150*f,WFLOOR-4],[x+182*f,WFLOOR-4]],[[x,y],[x+100*f,y+10],[x+92*f,WFLOOR-4],[x+124*f,WFLOOR-4]]],
  crossed:(x,y,f)=>[[[x,y],[x+112*f,y+4],[x+118*f,WFLOOR-4],[x+150*f,WFLOOR-4]],[[x,y],[x+108*f,y-22],[x+178*f,y+70],[x+206*f,y+60]]],
  wide:(x,y,f)=>[[[x,y],[x+115*f,y-30],[x+165*f,WFLOOR-4],[x+198*f,WFLOOR-4]],[[x,y],[x+95*f,y+25],[x+70*f,WFLOOR-4],[x+102*f,WFLOOR-4]]],
  neat:(x,y,f)=>[[[x,y],[x+110*f,y],[x+112*f,WFLOOR-4],[x+144*f,WFLOOR-4]],[[x,y],[x+104*f,y+6],[x+100*f,WFLOOR-4],[x+132*f,WFLOOR-4]]]};
function makeStick(side,legs){const f=side==='L'?1:-1,hip=HIP[side];const r={f,hip,side};const g=G(actors);r.g=g;
  const pl=()=>el('polyline',{fill:'none',stroke:INK,'stroke-width':9,'stroke-linecap':'round','stroke-linejoin':'round'},g);
  r.armF=pl();r.handF=el('circle',{r:10,fill:INK},g);r.legs=G(g);r.legP=LEGS[legs](hip[0],hip[1],f).map(pts=>{const p=el('polyline',{fill:'none',stroke:INK,'stroke-width':9,'stroke-linecap':'round','stroke-linejoin':'round'},r.legs);p.setAttribute('points',pts.map(q=>q.join(',')).join(' '));return p});
  r.torso=el('line',{stroke:INK,'stroke-width':10,'stroke-linecap':'round'},g);r.neck=G(g);r.head=G(g);r.armN=pl();r.handN=el('circle',{r:10,fill:INK},g);r.prop=G(g);return r}
function placeStick(r,pz,t,face={}){const f=r.f,[hx,hy0]=r.hip,hy=hy0+(face.rise||0),rad=pz.lean*Math.PI/180;const breathe=Math.sin(t*2.1+(f>0?0:1.7))*3;
  const N=[hx+Math.sin(rad)*178*f,hy-Math.cos(rad)*178+breathe];const S=[lerp(hx,N[0],.86),lerp(hy,N[1],.86)];
  r.torso.setAttribute('x1',hx);r.torso.setAttribute('y1',hy);r.torso.setAttribute('x2',N[0]);r.torso.setAttribute('y2',N[1]);
  const C=[N[0]+Math.sin(rad)*66*f+(face.dx||0),N[1]-Math.cos(rad)*66+(face.dy||0)];r.C=C;r.N=N;r.S=S;
  tr(r.head,C[0],C[1],face.s||1,(pz.tilt||0)*f+(face.rot||0));r.Cs=W(C[0],C[1]);tr(r.neck,N[0],N[1]);
  const arm=(pl,hd,tg,bend)=>{const Wp=[S[0]+tg[0]*f,S[1]+tg[1]];const k=ik(S,Wp,bend);pl.setAttribute('points',`${S[0]},${S[1]} ${k.E[0]},${k.E[1]} ${k.W[0]},${k.W[1]}`);hd.setAttribute('cx',k.W[0]);hd.setAttribute('cy',k.W[1]);return k.W};
  r.Wn=arm(r.armN,r.handN,pz.n,-f);r.Wf=arm(r.armF,r.handF,pz.f,-f);r.Wns=W(...r.Wn);return r}
// table with two mics; call after the actors so it sits in front of the hips
function table(){const g=G(actors);el('rect',{x:420,y:1318,width:240,height:18,rx:6,fill:'#C88D58',stroke:INK,'stroke-width':6},g);ln(g,540,1336,540,WFLOOR-6,10);ln(g,488,WFLOOR-4,592,WFLOOR-4,10);
  [[455,1,352,1188],[625,-1,712,1188]].forEach(([x,f,mx,my])=>{ln(g,x,1318,x,1240,7);ln(g,x,1240,mx+28*f,my+12,7);
    el('rect',{x:mx-16,y:my-34,width:32,height:62,rx:16,fill:'#3A3A40',stroke:INK,'stroke-width':5,transform:`rotate(${-60*f} ${mx} ${my})`},g)});return g}

// ---------- bubbles (Instagram-comment style) ----------
const BX=110,BW=860,BOTTOM=950;
const TIP={L:[258,1022],R:[808,1022]};const BASE={L:[236,316],R:[750,830]};
const U=window.USERS;
function bubblePath(x,y,w,h,s){const r=44,[t0,t1]=BASE[s],[tx,ty]=TIP[s];
  return `M${x+r} ${y} H${x+w-r} Q${x+w} ${y} ${x+w} ${y+r} V${y+h-r} Q${x+w} ${y+h} ${x+w-r} ${y+h} H${t1} L${tx} ${ty} L${t0} ${y+h} H${x+r} Q${x} ${y+h} ${x} ${y+h-r} V${y+r} Q${x} ${y} ${x+r} ${y} Z`}
const BUBL=L.filter(l=>U[l.who].side);
BUBL.forEach(l=>{const d=document.createElement('div');d.className='bt';d.style.left=(BX+40)+'px';d.style.width=(BW-80)+'px';texts.appendChild(d);
  l.spans=l.w.map(([w],j)=>{const s=document.createElement('span');s.textContent=w;if((l.em||[]).includes(j))s.className='e'+U[l.who].side;d.appendChild(s);return s});l.div=d});
function layoutBubbles(){BUBL.forEach((l,i)=>{const s=U[l.who].side;const th=l.div.getBoundingClientRect().height;const h=86+th+62,y=BOTTOM-h;l.top=y;l.div.style.top=(y+82)+'px';
  const g=G(bubG);l.g=g;el('path',{d:bubblePath(BX,y,BW,h,s),fill:'#fff',stroke:INK,'stroke-width':7,'stroke-linejoin':'round'},g);
  const av=G(g,{transform:`translate(${BX+54} ${y+48})`});el('circle',{r:21,fill:U[l.who].color,stroke:INK,'stroke-width':4},av);
  T(g,BX+86,y+59,U[l.who].name+'  '+(U[l.who].age||'3w'),32,'hand',GREY,'start');
  l.foot=G(g);if(!l.likes)l.foot.style.visibility='hidden';T(l.foot,BX+42,y+h-20,'Reply',28,'hand',GREY,'start');
  l.heart=el('path',{d:'M0 8 C-16 -4 -14 -18 -6 -18 C-2 -18 0 -14 0 -12 C0 -14 2 -18 6 -18 C14 -18 16 -4 0 8 Z',fill:'none',stroke:INK,'stroke-width':4,'stroke-linejoin':'round'},l.foot);l.hx=BX+BW-150;l.hy=y+h-32;
  T(l.foot,BX+BW-126,y+h-20,l.likes||'',30,'hand',INK,'start');l.show=i===0?-1:l.w[0][1]-.3});
  BUBL.forEach((l,i)=>{const nx=BUBL[i+1];l.hide=l.hideAt||(nx?nx.show:99);for(const k in M){if(M[k][0]>l.w[0][1]&&M[k][0]<l.hide)l.hide=M[k][0]}});
  BUBL.forEach(l=>{for(const k in M){if(l.show<M[k][1]&&l.show>M[k][0]-.5)l.show=M[k][1]}})}
function renderBubbles(t){BUBL.forEach((l,i)=>{const vis=t>=l.show&&t<l.hide+.2;op(l.g,vis?1:0);l.div.style.display=vis?'':'none';if(!vis)return;
  const kin=i===0?1:back(P(t,l.show,.32)),kout=P(t,l.hide,.18);const s=kin*(1-kout*.9);const tp=TIP[U[l.who].side];
  const tf=`translate(${tp[0]}px,${tp[1]}px) scale(${s}) translate(${-tp[0]}px,${-tp[1]}px)`;l.g.style.transform=tf;l.div.style.transform=tf;l.div.style.transformOrigin='0 0';l.g.style.opacity=l.div.style.opacity=1-kout;
  l.spans.forEach((sp,j)=>{const k=P(t,l.w[j][1]-.06,.22);sp.style.opacity=eo(k);sp.style.transform=`translateY(${(1-eo(k))*16}px) scale(${.7+.3*back(k)})`;
    if(sp.className){const pulse=Math.sin(P(t,l.w[j][1],.35)*Math.PI)*.12;sp.style.transform+=` scale(${1+pulse})`}});
  const lk=P(t,l.end-.1,.3);op(l.foot,eo(P(t,l.end-.25,.25)));l.heart.setAttribute('fill',lk>.3?RED:'none');l.heart.setAttribute('stroke',lk>.3?RED:INK);
  l.heart.setAttribute('transform',`translate(${l.hx} ${l.hy}) scale(${1.2+Math.sin(lk*Math.PI)*.6})`)})}
const topOf=id=>ID[id].top;

// ---------- stickers ----------
function badge(p,txt,fill,col,size,w,h){const g=G(p);el('rect',{x:-w/2,y:-h/2,width:w,height:h,rx:14,fill,stroke:INK,'stroke-width':6},g);g.t=T(g,0,size*.36,txt,size,'mk',col);return g}
const pop=(e,x,y,t,t0,t1,rot=0,sc=1)=>{const k=back(P(t,t0,.3)),o=t>=t0&&t<t1+.25?1-P(t,t1,.25):0;op(e,o);tr(e,x,y,k*sc*(1+P(t,t1,.25)*.3),rot);return k};

// ---------- camera: zooms = [[k, scale, x, y], ...] in screen coords, clamped inside the frame ----------
const cam=$('cam'),tint=$('tint');
function camera(zooms,shake=0,t=0){let cs=1,cx=540,cy=960;for(const [k,s,x0,y0] of zooms){if(k<=0)continue;const hw=540/s,hh=960/s;const x=cl(x0,hw,1080-hw),y=cl(y0,hh,1920-hh);cs=lerp(cs,s,k);cx=lerp(cx,x,k);cy=lerp(cy,y,k)}
  const sx=shake?Math.sin(t*83)*14*shake:0,sy=shake?Math.cos(t*67)*10*shake:0;cam.style.transform=`translate(${540-cx*cs+sx}px,${960-cy*cs+sy}px) scale(${cs})`}

// ---------- main loop ----------
window.render=function(t){const seed=1+Math.floor(t*10)%6;$('turb').setAttribute('seed',seed);$('turb2').setAttribute('seed',seed+3);
  if(window.renderSign)renderSign(t);
  const talking=L.some(l=>t>=l.w[0][1]-.1&&t<l.end);oaBox.setAttribute('fill',talking?RED:'#3A3A40');oaTxt.setAttribute('fill',talking?'#fff':'#77777E');
  tint.style.background='none';EP.render(t);renderBubbles(t)};
window.__ready=new Promise(res=>{document.fonts.load('40px Neon').then(()=>document.fonts.load('56px Hand')).then(()=>document.fonts.load('40px Marker')).then(()=>document.fonts.ready).then(()=>{layoutBubbles();if(EP.init)EP.init();window.render(0);res()})});
