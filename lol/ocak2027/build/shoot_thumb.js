const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.join(__dirname,'thumb.html'));await p.evaluate(async()=>{await document.fonts.load('40px PB');await document.fonts.load('900 40px Cin');await document.fonts.load('900 40px Mon');await document.fonts.ready});await p.waitForTimeout(500);
await p.locator('#t').screenshot({path:path.join(__dirname,'../export/thumbnail_full.png')});await b.close()})();
