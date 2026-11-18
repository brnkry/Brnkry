const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1920,height:2160}});
await p.goto('file://'+path.join(__dirname,'ornek.html'));await p.evaluate(async()=>{await document.fonts.load('500 40px Cin','İÇ');await document.fonts.load('300 40px Mon','ı');await window.ready});await p.waitForTimeout(400);
for(const id of ['a','b'])await p.locator('#'+id).screenshot({path:path.join(__dirname,'../export/ornek_yazi_'+id+'.png')});await b.close()})();
