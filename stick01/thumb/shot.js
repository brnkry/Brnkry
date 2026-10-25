// usage: node shot.js -> thumbnail_1280x720.png, cover_1080x1920.png (thumb.html over bg.png from ../thumbshot.js)
const { chromium } = require('../../wtc/node_modules/playwright');const path=require('path');
(async()=>{const br=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args:['--allow-file-access-from-files']});
 for(const [m,w,h,out] of [['wide',1280,720,'thumbnail_1280x720.png'],['tall',1080,1920,'cover_1080x1920.png']]){
  const p=await br.newPage({viewport:{width:w,height:h}});await p.goto('file://'+path.join(__dirname,'thumb.html#'+m));await p.waitForFunction(()=>window.__done);await p.waitForTimeout(200);
  await (await p.$('#stage')).screenshot({path:path.join(__dirname,out)});await p.close()}
 await br.close()})();
