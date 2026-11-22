const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:3900}});
await p.goto('file://'+path.join(__dirname,'thumb_mc.html'));await p.evaluate(async()=>{await window.ready});await p.waitForTimeout(500);
await p.locator('#yone').screenshot({path:path.join(__dirname,'../export/thumbnail_short.png')});
await p.locator('#yasuo').screenshot({path:path.join(__dirname,'../../yasuo/export/thumbnail_short_mc.png')});await b.close()})();
