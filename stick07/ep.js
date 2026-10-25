// Episode 07: "What abt USA it's only 2 letters" -> "United States of America has 21 letters" -> "United stays of America is a diff county then USA"
const EP={};
chair(250,1,'#5BB8C9');chair(828,-1,'#8A8F99');
const IB=makeStick('L','lazy'),FF=makeStick('R','neat');
table();
// ---------- ibz2craftyy (left): crown, confident grin ----------
(()=>{const h=IB.head;el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h);
  h.crown=el('path',{d:'M-44 -50 L-44 -92 L-22 -70 L0 -100 L22 -70 L44 -92 L44 -50 Z',fill:'#F2C230',stroke:INK,'stroke-width':6,'stroke-linejoin':'round'},h);
  h.eyes=G(h);el('circle',{cx:14,cy:-6,r:6,fill:INK},h.eyes);el('circle',{cx:44,cy:-6,r:6,fill:INK},h.eyes);
  h.lids=G(h);ln(h.lids,4,-14,24,-12,5);ln(h.lids,34,-12,54,-14,5);
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h)})();
// ---------- 2001 Ford Focus (right): side part, tired eyes ----------
(()=>{const h=FF.head;el('circle',{r:62,fill:PAPER,stroke:INK,'stroke-width':9},h);
  el('path',{d:'M-60 -14 Q-62 -66 -6 -66 Q52 -66 60 -18 Q30 -34 6 -40 Q-22 -26 -60 -14 Z',fill:'#6B5A50',stroke:INK,'stroke-width':5},h);
  h.eyes=G(h);el('circle',{cx:-16,cy:-4,r:6,fill:INK},h.eyes);el('circle',{cx:-46,cy:-4,r:6,fill:INK},h.eyes);
  h.brows=G(h);ln(h.brows,-6,-22,-26,-24,5);ln(h.brows,-36,-24,-56,-22,5);
  h.mouth=el('path',{fill:'#5A1E22',stroke:INK,'stroke-width':5,'stroke-linejoin':'round','stroke-linecap':'round'},h)})();

const IPOSE={talk:{lean:2,tilt:6,n:[115,0],f:[50,140]},idle:{lean:-6,n:[70,135],f:[50,140]},two:{lean:6,n:[120,-60],f:[50,140]},cross:{lean:-10,n:[55,55],f:[40,60]}};
const IKEYS=[[0,'talk'],[2.6,'two'],[3.6,'idle'],[8.3,'talk'],[12.1,'cross']];
const FPOSE={idle:{lean:2,n:[70,135],f:[60,140]},count:{lean:8,n:[110,-60],f:[60,140]},facepalm:{lean:12,tilt:14,n:[48,-92],f:[60,140]}};
const FKEYS=[[0,'idle'],[4.6,'count'],[7.2,'idle'],[13.4,'facepalm']];
const iPose=poser(IPOSE,IKEYS,.25),fPose=poser(FPOSE,FKEYS,.25);

// ---------- stickers: just what the lines say ----------
function tile(p,ch,col){const g=G(p);el('rect',{x:-30,y:-34,width:60,height:68,rx:8,fill:'#fff',stroke:INK,'stroke-width':5},g);T(g,0,18,ch,46,'mk',col);g.n=T(g,24,-40,'',22,'hand',GREY);return g}
const usa=G(fx);const usaT=['U','S','A'].map((c,i)=>{const g=tile(usa,c,BLUE);g.setAttribute('transform',`translate(${(i-1)*76} 0)`);g.n.textContent=String(i+1);return g});
const twoB=badge(fx,'= 2 ?',PAPER,RED,50,170,80);
const long=G(fx);const words=['UNITED','STATES','OF','AMERICA'];let cx=-381;const longW=words.map((w,i)=>{const g=G(long);const wd=w.length*30+24;el('rect',{x:0,y:-34,width:wd,height:68,rx:8,fill:'#fff',stroke:INK,'stroke-width':5},g);T(g,wd/2,16,w,40,'mk',BLUE);g.setAttribute('transform',`translate(${cx} 0)`);cx+=wd+12;return g});
const cnt=badge(fx,'0 letters',PAPER,GREEN,42,260,70);
const stays=G(fx);el('rect',{x:-330,y:-40,width:660,height:80,rx:10,fill:'#fff',stroke:INK,'stroke-width':6},stays);T(stays,0,16,'UNITED STAYS OF AMERICA',38,'mk',RED);
const neq=badge(fx,'≠ USA 😒',PAPER,INK,48,260,80);
const q=T(fx,0,0,'?!',120,'mk',RED);q.setAttribute('stroke',INK);q.setAttribute('stroke-width',7);q.setAttribute('paint-order','stroke');

EP.render=function(t){
  let ip=iPose(t);const im=talkMouth('I',t);if(ip.name==='talk'||ip.name==='two')ip.n[1]+=Math.sin(t*8)*10;
  placeStick(IB,ip,t,{});
  {const h=IB.head;const bl=blink(t,3.3,.5);h.eyes.setAttribute('transform',`translate(0 -6) scale(1 ${bl}) translate(0 6)`);
    const o=im*26,mx=32;h.mouth.setAttribute('d',o<3?`M${mx-18} 22 Q${mx} 40 ${mx+18} 22`:`M${mx-18} 20 Q${mx} 18 ${mx+18} 20 Q${mx+16} ${24+o} ${mx} ${26+o} Q${mx-16} ${26+o} ${mx-18} 20 Z`);h.mouth.setAttribute('fill',o<3?'none':'#5A1E22')}
  let fp=fPose(t);const fm=talkMouth('F',t);if(fp.name==='count')fp.n[1]+=Math.sin(t*8)*10;
  placeStick(FF,fp,t,{});
  {const h=FF.head;const bl=blink(t,3.7,1.2);h.eyes.setAttribute('transform',`translate(0 -4) scale(1 ${bl}) translate(0 4)`);
    const fr=Math.max(V(t,1.9,4.4),V(t,9.0,14.9,.3,.01));tr(h.brows,0,6*fr);
    const o=fm*24,mx=-32;h.mouth.setAttribute('d',o<3?`M${mx-14} ${28+fr*4} Q${mx} ${32-fr*10} ${mx+14} ${28+fr*4}`:`M${mx-16} 20 Q${mx} 18 ${mx+16} 20 Q${mx+14} ${24+o} ${mx} ${26+o} Q${mx-14} ${26+o} ${mx-16} 20 Z`);h.mouth.setAttribute('fill',o<3?'none':'#5A1E22')}
  // USA tiles numbered 1 2 3, then "= 2 ?"
  {const o=t>=.76&&t<4.6?1-P(t,4.4,.2):0;op(usa,o);tr(usa,430,topOf('i1')-90,1);usaT.forEach((g,i)=>{const k=back(P(t,.76+i*.12,.3));g.setAttribute('transform',`translate(${(i-1)*76} 0) scale(${k})`);op(g.n,t>2.1+i*.15?1:0)})}
  pop(twoB,720,topOf('i1')-90,t,2.77,4.4,5);
  // UNITED STATES OF AMERICA, counter climbs to 21
  {const o=t>=4.75&&t<8.3?1-P(t,8.1,.2):0;op(long,o);tr(long,540,topOf('f1')-170,1);longW.forEach((g,i)=>{const s=[4.75,5.1,5.44,5.6][i];g.style.opacity=t>=s?1:0});
    pop(cnt,540,topOf('f1')-70,t,5.96,8.1,-3);cnt.t.textContent=Math.round(21*eo(P(t,6.0,.8)))+' letters'}
  pop(stays,540,topOf('i2')-170,t,9.1,14.9,-2,.95);pop(neq,700,topOf('i2')-70,t,11.85,14.9,4);
  pop(q,FF.Cs[0]-120,FF.Cs[1]-150,t,13.5,14.9,-8,.8);
};
EP.init=function(){};
