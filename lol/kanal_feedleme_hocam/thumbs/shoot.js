const {chromium}=require('/home/user/Brnkry/lol/sett/build/node_modules/playwright');const path=require('path');const ids=require('./ids.json');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1300,height:2000}});
await p.goto('file://'+path.join(__dirname,'thumbs.html'));await p.evaluate(async()=>{await document.fonts.load('40px PB');await document.fonts.ready});await p.waitForTimeout(500);
for(const id of ids)await p.locator('#'+id).screenshot({path:path.join(__dirname,id+'.png')});await b.close()})();
