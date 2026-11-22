const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1280,height:1500}});
await p.goto('file://'+path.join(__dirname,'thumb2.html'));await p.evaluate(()=>document.fonts.load('100px Anton','YASUOİŞĞ'));await p.waitForTimeout(500);
for(const id of ['a','b']) await p.locator('#'+id).screenshot({path:path.join(__dirname,`../export/thumbnail_vs_${id}.png`)});await b.close()})();
