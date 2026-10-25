// usage: node thumb.js <episode dir> <t>  -> <dir>/thumb/{bg.png,thumbnail_1280x720.png,cover_1080x1920.png} (needs <dir>/thumb/cfg.js)
const { chromium } = require('../../wtc/node_modules/playwright');const path=require('path');
(async()=>{const [dir,t]=process.argv.slice(2);const ep=path.resolve(dir),out=path.join(ep,'thumb');
 const br=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args:['--allow-file-access-from-files']});
 let p=await br.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+path.join(ep,'scene.html'));await p.evaluate(()=>window.__ready);await p.waitForTimeout(300);
 await p.evaluate(t=>{window.render(t);['bubbles','texts','fx','sign'].forEach(i=>document.getElementById(i).style.visibility='hidden');document.querySelector('#room g[transform="translate(540 1052)"]').style.visibility='hidden'},+t);
 await (await p.$('#stage')).screenshot({path:path.join(out,'bg.png')});await p.close();
 for(const [m,w,h,f] of [['wide',1280,720,'thumbnail_1280x720.png'],['tall',1080,1920,'cover_1080x1920.png']]){
  p=await br.newPage({viewport:{width:w,height:h}});await p.goto('file://'+path.join(__dirname,'thumb.html')+'#'+encodeURIComponent(path.relative(__dirname,path.join(out,'cfg.js'))+'|'+m));
  await p.waitForFunction(()=>window.__done);await p.waitForTimeout(200);await (await p.$('#stage')).screenshot({path:path.join(out,f)});await p.close()}
 await br.close()})();
