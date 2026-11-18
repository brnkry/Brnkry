const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1280,height:2200}});
await p.goto('file://'+path.join(__dirname,'thumb.html'));await p.evaluate(async()=>{await window.ready});await p.waitForTimeout(400);
for(const id of ['a','b','c']) await p.locator('#'+id).screenshot({path:path.join(__dirname,`../export/thumbnail_${id}.png`)});
await b.close()})();
