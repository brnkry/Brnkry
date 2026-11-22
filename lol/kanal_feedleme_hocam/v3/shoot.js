const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:800,height:2500}});
await p.goto('file://'+path.join(__dirname,'logo.html'));await p.evaluate(async()=>{await window.ready});await p.waitForTimeout(400);
for(const i of [1,2,3]) await p.locator('#l'+i).screenshot({path:path.join(__dirname,`logo_${i}.png`)});await b.close()})();
