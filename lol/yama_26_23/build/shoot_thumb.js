const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1280,height:720}});
await p.goto('file://'+path.join(__dirname,'thumb.html'));await p.evaluate(async()=>{await document.fonts.load('40px PB');await document.fonts.ready});await p.waitForTimeout(400);
await p.locator('#t').screenshot({path:path.join(__dirname,'../export/thumbnail.png')});await b.close()})();
