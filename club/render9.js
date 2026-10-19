// usage: node render9.js page.html out.jpg [query]
const { chromium } = require('../wtc/node_modules/playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+path.resolve(process.argv[2])+(process.argv[4]?'?'+process.argv[4]:''));await p.evaluate(()=>window.__ready);await p.waitForTimeout(300);
await (await p.$('#stage')).screenshot({path:process.argv[3],type:'jpeg',quality:85});if(errs.length)console.log(errs);await b.close()})();
