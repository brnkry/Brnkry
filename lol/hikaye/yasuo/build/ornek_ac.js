const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.join(__dirname,'ornek_ac.html'));await p.evaluate(async()=>{await document.fonts.load('40px AC','YAPTIKLARIN');await window.ready});await p.waitForTimeout(500);
await p.locator('#a').screenshot({path:path.join(__dirname,'../export/font_american_captain.png')});await b.close()})();
