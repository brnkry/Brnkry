// ================= main: narrator + render loop + events =================
KEYS.sort((a,b)=>a[0]-b[0]);const poseAt=poser(POSE,KEYS);

const TAIL=8.0;const VO_END=351.32;
window.render=function(t){
 renderCaptions(t);capEl.style.opacity=1-P(t,VO_END+.1,.3);flash.style.opacity=0;flash.style.background='#FFB000';black.style.opacity=0;
 const st=t>PB-.6;show(st?1:0,studio,bug);
 if(st){const pz=poseAt(t);const m=t<VO_END?mouthAt(t):0;let o={smile:.5,browWorry:0,browUp:.1+.25*m};
  for(const [a,b,mo] of MOODS)if(t>=a&&t<b)Object.assign(o,mo);
  const pointing=!['rest','open','one','thumb','stop','shrug','wave','hug'].includes(pz.name);const R={...pz.R};if(pz.name==='wave')R.rot=-80+18*Math.sin(t*9);
  guy.set({mouth:.9*m,smile:o.smile,browUp:o.browUp,browWorry:o.browWorry,eyes:blinkAt(t,3.3,.5),pupil:1,look:pointing?[.85,-.15]:[.08*Math.sin(t*.7),0],tilt:2*Math.sin(t*1.1),nod:2.2*m,amber:0,hands:{L:pz.L,R}});
  studio.presG.setAttribute('transform',`translate(430 ${560+4*Math.sin(t*1.6)})`)}
 RENDER.forEach(f=>f(t));
};
window.DUR=+(VO_END+TAIL).toFixed(2);
window.EV=(()=>{const E=[];const A=(t,type,d=0,v=1)=>E.push([+t.toFixed(3),type,d,v]);EVF.forEach(f=>f(A));return E.sort((a,b)=>a[0]-b[0])})();
window.__ready=document.fonts.ready.then(()=>{fitCaptions();window.render(0);return true});
