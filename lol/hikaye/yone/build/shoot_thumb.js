const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1280,height:1600}});
await p.goto('file://'+path.join(__dirname,'thumb.html'));await p.evaluate(async()=>{await window.ready});await p.waitForTimeout(400);
await p.locator('#yasuo').screenshot({path:path.join(__dirname,'../../yasuo/export/thumbnail_seri.png')});
await p.locator('#yone').screenshot({path:path.join(__dirname,'../export/thumbnail.png')});
await b.close()})();