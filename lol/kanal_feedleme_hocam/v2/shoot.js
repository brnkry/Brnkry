const {chromium}=require('/home/user/Brnkry/lol/sett/build/node_modules/playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:2600,height:1500}});
await p.goto('file://'+path.join(__dirname,'brand.html'));await p.evaluate(async()=>{await document.fonts.load('40px PB');await document.fonts.ready});await p.waitForTimeout(400);
for(const id of ['l1','l2','l3'])await p.locator('#'+id).screenshot({path:path.join(__dirname,`logo_${id.slice(1)}.png`),omitBackground:true});
await p.locator('#b').screenshot({path:path.join(__dirname,'banner.png')});await b.close()})();
