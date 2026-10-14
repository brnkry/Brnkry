// What the Car? brand: palette, confused car mark, car side view, wordmark helpers
// Font: Bricolage Grotesque (variable: wght 200..800, wdth 75..100, opsz 12..96)
window.BRAND={
  name:'What the Car?',
  font:'WTC',
  // dark is the main theme for videos
  dark:{bg:[18,18,22],ink:[244,241,234],card:[34,34,41],muted:[138,138,150],line:[48,48,58],acc:[212,255,58],acc2:[255,61,90]},
  light:{bg:[244,241,234],ink:[18,18,22],card:[255,255,255],muted:[118,116,110],line:[221,216,205],acc:[18,18,22],acc2:[255,61,90],hi:[212,255,58]},
  hex:{asphalt:'#121216',chalk:'#F4F1EA',lime:'#D4FF3A',brake:'#FF3D5A',graphite:'#22222A',smoke:'#8A8A96',line:'#30303A'},
};
const _NS="http://www.w3.org/2000/svg";
function bel(tag,attrs={},parent){const e=document.createElementNS(_NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);if(parent)parent.appendChild(e);return e}

// Front view "confused car": body, windshield, headlight eyes, one raised brow, grille mouth, floating "?"
// Drawn around (0,0), roughly 440 wide x 400 tall incl. the "?" . opts: {body,ink,eye,q,glass}
window.makeFace=function(parent,o={}){
  const C=Object.assign({body:'#D4FF3A',ink:'#121216',eye:'#F4F1EA',q:'#FF3D5A',glass:'#121216',tyre:'#34343E',line:null,question:true},o);
  const L=C.line||C.ink;const g=bel('g',{},parent);
  // tyres peeking under the body
  bel('rect',{x:-182,y:92,width:74,height:78,rx:18,fill:C.tyre},g);
  bel('rect',{x:108,y:92,width:74,height:78,rx:18,fill:C.tyre},g);
  // body
  const body='M-118 -132 Q-112 -158 -84 -160 L84 -160 Q112 -158 118 -132 L146 -46 Q200 -40 204 6 L204 96 Q204 128 172 128 L-172 128 Q-204 128 -204 96 L-204 6 Q-200 -40 -146 -46 Z';
  bel('path',{d:body,fill:C.body},g);
  // windshield
  bel('path',{d:'M-96 -136 Q-92 -144 -80 -144 L80 -144 Q92 -144 96 -136 L120 -60 Q122 -52 112 -52 L-112 -52 Q-122 -52 -120 -60 Z',fill:C.glass},g);
  // wiper glint on glass
  bel('path',{d:'M-60 -70 L-8 -126',stroke:C.body,'stroke-width':10,'stroke-linecap':'round',opacity:.35},g);
  // mirrors
  bel('rect',{x:-226,y:-40,width:30,height:22,rx:8,fill:C.body},g);
  bel('rect',{x:196,y:-40,width:30,height:22,rx:8,fill:C.body},g);
  // eyes (headlights)
  const eyes=[];
  [[-112,18],[112,18]].forEach(([x,y])=>{
    const e=bel('g',{transform:`translate(${x} ${y})`},g);
    bel('circle',{r:44,fill:C.ink},e);
    bel('circle',{r:34,fill:C.eye},e);
    const p=bel('circle',{cx:9,cy:-10,r:15,fill:C.ink},e);
    eyes.push({g:e,pupil:p});
  });
  // brows: left flat-ish, right raised
  const browL=bel('path',{d:'M-152 -22 Q-114 -32 -76 -22',stroke:L,'stroke-width':13,'stroke-linecap':'round',fill:'none'},g);
  const browR=bel('path',{d:'M74 -30 Q110 -52 150 -40',stroke:L,'stroke-width':13,'stroke-linecap':'round',fill:'none'},g);
  // grille mouth: small wavy "huh"
  const mouth=bel('path',{d:'M-46 84 Q-30 70 -14 84 Q2 98 18 84 Q34 70 48 82',stroke:L,'stroke-width':12,'stroke-linecap':'round',fill:'none'},g);
  // plate slot
  bel('rect',{x:-150,y:100,width:300,height:10,rx:5,fill:C.ink,opacity:.18},g);
  // question mark
  let q=null;
  if(C.question){
    q=bel('g',{transform:'translate(150 -214) rotate(14)'},g);
    bel('path',{d:'M-30 -34 Q-30 -76 4 -76 Q38 -76 38 -44 Q38 -22 14 -10 Q2 -4 2 14 L2 22',stroke:C.q,'stroke-width':22,'stroke-linecap':'round','stroke-linejoin':'round',fill:'none'},q);
    bel('circle',{cx:2,cy:56,r:14,fill:C.q},q);
  }
  g.eyes=eyes;g.browL=browL;g.browR=browR;g.mouth=mouth;g.q=q;
  // look direction helper: dx,dy in -1..1
  g.look=(dx,dy)=>eyes.forEach(e=>{e.pupil.setAttribute('cx',(dx*14).toFixed(1));e.pupil.setAttribute('cy',(dy*14).toFixed(1))});
  return g;
};

// Side view car facing right (generic hatchback), 1000x340 box centred at origin
window.makeCar=function(parent,o={}){
  const C=Object.assign({body:'#F4F1EA',ink:'#121216',acc:'#D4FF3A'},o);
  const g=bel('g',{},parent);const inner=bel('g',{transform:'translate(-500 -200)'},g);
  bel('path',{d:'M40 258 L40 200 Q46 168 104 160 L300 138 Q372 66 470 60 L700 60 Q770 64 820 120 L880 168 Q960 176 964 220 L964 258 Q964 278 944 278 L886 278 A72 72 0 0 0 742 278 L300 278 A72 72 0 0 0 156 278 L58 278 Q40 278 40 258 Z',fill:C.body},inner);
  bel('path',{d:'M330 140 Q388 88 468 82 L560 82 L560 140 Z',fill:C.ink},inner);
  bel('path',{d:'M582 82 L694 82 Q750 86 790 140 L582 140 Z',fill:C.ink},inner);
  const lamp=bel('path',{d:'M926 184 L962 190 L962 210 L926 206 Z',fill:C.acc},inner);
  bel('rect',{x:40,y:196,width:16,height:22,rx:4,fill:'#FF3D5A'},inner);
  [228,814].forEach(x=>{bel('circle',{cx:x,cy:278,r:60,fill:C.ink},inner);bel('circle',{cx:x,cy:278,r:28,fill:C.body},inner);bel('circle',{cx:x,cy:278,r:10,fill:C.ink},inner)});
  g.lamp=lamp;g.inner=inner;g.pt=(x,y)=>[x-500,y-200];
  return g;
};

// Wordmark as HTML: <div class="wm"><span class="a">WHAT THE</span><span class="b">CAR<i>?</i></span></div>
window.makeWordmark=function(host,o={}){
  const C=Object.assign({ink:'#F4F1EA',car:'#D4FF3A',q:'#FF3D5A',size:200,stack:true},o);
  const d=document.createElement('div');
  d.style.cssText=`font-family:WTC;line-height:.82;color:${C.ink};font-size:${C.size}px;display:inline-flex;flex-direction:${C.stack?'column':'row'};align-items:${C.stack?'flex-start':'baseline'};gap:${C.stack?0:.22}em`;
  d.innerHTML=`<span style="font-weight:700;font-stretch:75%;font-size:.42em;letter-spacing:.06em;margin:0 0 .1em .06em">WHAT THE</span><span style="font-weight:800;font-stretch:75%;letter-spacing:-.02em;color:${C.car}">CAR<span style="color:${C.q}">?</span></span>`;
  host.appendChild(d);return d;
};
