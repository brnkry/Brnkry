const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.join(__dirname,'thumb.html'));await p.evaluate(async()=>{await window.ready});await p.waitForTimeout(400);
await p.locator('#s').screenshot({path:path.join(__dirname,'../export/thumbnail_short.png')});await b.close()})();
