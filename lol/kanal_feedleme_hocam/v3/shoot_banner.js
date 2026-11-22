const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:2560,height:1440}});
await p.goto('file://'+path.join(__dirname,'banner.html'));await p.evaluate(async()=>{await window.ready});await p.waitForTimeout(500);
await p.locator('#b').screenshot({path:path.join(__dirname,'banner.png')});await b.close()})();