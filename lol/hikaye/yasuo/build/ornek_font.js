const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1920,height:3240}});
await p.goto('file://'+path.join(__dirname,'ornek_font.html'));await p.evaluate(async()=>{for(const f of ['Chorus','Might','Themora'])await document.fonts.load('40px '+f,'YAPTIKLARIN');await window.ready});await p.waitForTimeout(500);
for(const id of ['c','m','t'])await p.locator('#'+id).screenshot({path:path.join(__dirname,'../export/font_'+id+'.png')});await b.close()})();
