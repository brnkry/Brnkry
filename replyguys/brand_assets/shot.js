// usage: node shot.js  -> logo_800.png, banner_2560x1440.png, logo_1024x576.png
const { chromium } = require('../../wtc/node_modules/playwright');const path=require('path');
(async()=>{const br=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args:['--allow-file-access-from-files']});
 for(const [m,w,h,out] of [['logo',800,800,'logo_800.png'],['banner',2560,1440,'banner_2560x1440.png'],['wide',1024,576,'logo_1024x576.png']]){
  const p=await br.newPage({viewport:{width:w,height:h}});await p.goto('file://'+path.join(__dirname,'brand.html#'+m));
  await p.waitForFunction(()=>window.__done);await p.waitForTimeout(300);await (await p.$('#stage')).screenshot({path:path.join(__dirname,out)});await p.close()}
 await br.close()})();
