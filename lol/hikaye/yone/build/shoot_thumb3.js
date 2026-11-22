const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1280,height:4600}});
await p.goto('file://'+path.join(__dirname,'thumb3.html'));await p.evaluate(async()=>{await window.ready});await p.waitForTimeout(500);
const E=path.join(__dirname,'../export/'),Y=path.join(__dirname,'../../yasuo/export/');
for(const [id,f] of [['yone',E+'thumbnail_1.png'],['yone2',E+'thumbnail_2.png'],['yone3',E+'thumbnail_3.png'],['yasuo_a',Y+'thumbnail_seri_a.png'],['yasuo_b',Y+'thumbnail_seri_b.png'],['yasuo_c',Y+'thumbnail_seri_c.png']])
 await p.locator('#'+id).screenshot({path:f});
await b.close()})();