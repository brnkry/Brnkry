const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1280,height:720}});
await p.goto('file://'+path.join(__dirname,'thumb_mc.html'));await p.evaluate(async()=>{await window.ready});await p.waitForTimeout(400);
await p.locator('#a').screenshot({path:path.join(__dirname,'../export/thumbnail_mc.png')});await b.close()})();
