const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.join(__dirname,'mock.html'));await p.evaluate(async()=>{await document.fonts.load('40px PB');await document.fonts.load('900 40px Mon');await document.fonts.ready});
for(const k of ['hook','cmp','order','runes','item','end']){await p.evaluate(k=>show(k),k);await p.waitForTimeout(200);await p.screenshot({path:path.join(__dirname,'mock_'+k+'.png'),omitBackground:true});}
await b.close()})();
