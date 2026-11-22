const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1280,height:1440}});
await p.goto('file://'+path.join(__dirname,'thumb2.html'));await p.evaluate(async()=>{await window.ready});await p.waitForTimeout(400);
await p.locator('#yone').screenshot({path:path.join(__dirname,'../export/thumbnail_b.png')});await p.locator('#yasuo').screenshot({path:path.join(__dirname,'../../yasuo/export/thumbnail_seri.png')});await b.close()})();
