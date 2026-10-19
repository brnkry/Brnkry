// Club (welcometoclub) 9:16 helpers: drawing utils, Turkish captions from align_tr.py, narrator timing.
const NS="http://www.w3.org/2000/svg";const svg=document.getElementById('ill');
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));const P=(t,t0,d)=>cl((t-t0)/d);
const eo=x=>1-Math.pow(1-x,3);const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const back=x=>{const c1=1.5,c3=c1+1;return x<=0?0:1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const V=(t,a,b,fi=.35,fo=.3)=>Math.min(eo(P(t,a,fi)),1-P(t,b-fo,fo));
const lerp=(a,b,k)=>a+(b-a)*k;const on=(t,a)=>t>a?1:0;const pop=(t,a,d=.45)=>back(P(t,a,d));
function el(tag,attrs={},parent=svg){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);parent.appendChild(e);return e}
function g(parent=svg,attrs={}){return el('g',attrs,parent)}
function tr(e,x,y,s=1,r=0,o=1){e.setAttribute('transform',`translate(${x} ${y}) rotate(${r}) scale(${s})`);e.style.opacity=o}
function show(v,...els){els.forEach(e=>e.style.display=v>0?'':'none')}
const vis=(e,t,a,b,fi=.35,fo=.3)=>{const v=V(t,a,b,fi,fo);show(v,e);if(v>0)e.style.opacity=v;return v};
function txt(parent,x,y,size,s,fill='#3B2A22',w=700,anchor='middle'){const t=el('text',{x,y,'text-anchor':anchor,'font-size':size,fill,style:`font-family:QS;font-weight:${w}`},parent);t.textContent=s;return t}
// brand
const BR='#744834',BR2='#9A6A55',INK='#3B2A22',CREAM='#FBF8F3',BEIGE='#F1E2D3',SAND='#E8D5C2',ROSE='#E9B9A6',WATER='#8FC1D9',RED='#D9705F',GOOD='#7FA27B';

// ---------- captions (Turkish, 1 token = 1 aligned word, script order) ----------
const cap=document.getElementById('cap');const groups=[];const WT={};
const trLow=s=>s.replace(/I/g,'ı').replace(/İ/g,'i').toLowerCase().replace(/[^a-zçğıöşüâîû']/g,'');
function buildCaptions(G,A){let k=0;Object.keys(G).forEach(id=>{const div=document.createElement('div');div.className='grp';cap.appendChild(div);const words=[];let emph=false;
  G[id].forEach(seg=>seg.split(' ').forEach(tok=>{let st=tok.startsWith('*');if(st){emph=true;tok=tok.slice(1)}let en=tok.endsWith('*');if(en)tok=tok.slice(0,-1);
    const a=A[k++];if(!a)throw new Error('alignment ran out at '+id+' '+tok);if(a[0]!==trLow(tok).replace(/'/g,''))console.warn('caption/align mismatch',id,tok,a[0]);
    const span=document.createElement('span');span.className='w'+(emph?' e':'');span.textContent=tok;div.appendChild(span);words.push({span,ts:a[1],te:a[2]});
    const key=id+':'+trLow(tok);if(!(key in WT))WT[key]=a[1];if(en)emph=false}));
  groups.push({id,div,words,start:words[0].ts-.06,end:words[words.length-1].te})});
  groups.forEach((gr,i)=>{gr.next=i<groups.length-1?groups[i+1].start:999});if(k!==A.length)console.warn('unused alignment words',A.length-k)}
const W_=(id,w)=>{const k=id+':'+trLow(w);if(!(k in WT))throw new Error('no word '+k);return WT[k]};
const Gs=id=>{const x=groups.find(x=>x.id===id);if(!x)throw new Error('no group '+id);return x.start};
const Ge=id=>groups.find(x=>x.id===id).end;
function renderCaptions(t){groups.forEach(gr=>{const endT=Math.min(gr.next-.16,gr.end+.9);const out=P(t,endT-.14,.14);const visb=t>=gr.start-.15&&t<endT+.02;gr.div.style.display=visb?'flex':'none';if(!visb)return;
  gr.words.forEach(({span,ts})=>{const k=eo(P(t,ts-.07,.28));span.style.opacity=.25+.75*k-out;span.style.transform=`translateY(${(1-k)*14-out*12}px)`})})}
function fitCaptions(){groups.forEach(gr=>{const d=gr.div;d.style.display='flex';let fs=parseFloat(getComputedStyle(d).fontSize);
  const box=()=>{const r=[...d.children].map(x=>x.getBoundingClientRect());return Math.max(...r.map(x=>x.bottom))-Math.min(...r.map(x=>x.top))};
  while(box()>190&&fs>40){fs-=2;d.style.fontSize=fs+'px'}d.style.display='none'})}

// ---------- narrator ----------
const mouthAt=t=>{const M=window.MOUTH||[];const f=t*30;const i=Math.floor(f);const a=M[i]||0,b=M[i+1]||0;return lerp(a,b,f-i)};
const blinkAt=(t,per=3.6,off=0)=>{const p=((t+off)%per+per)%per;return p<.14?1-Math.sin(p/.14*Math.PI):1};
