const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1280,height:2200}});
await p.goto('file://'+path.join(__dirname,'thumb3.html'));await p.evaluate(async()=>{await window.ready});await p.waitForTimeout(500);
await p.locator('#yone').screenshot({path:path.join(__dirname,'../export/thumbnail_c.png')});
await p.locator('#yasuo_a').screenshot({path:path.join(__dirname,'../../yasuo/export/thumbnail_seri_a.png')});
await p.locator('#yasuo_b').screenshot({path:path.join(__dirname,'../../yasuo/export/thumbnail_seri_b.png')});
await b.close()})();
