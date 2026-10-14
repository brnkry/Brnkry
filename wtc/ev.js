const { chromium } = require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--allow-file-access-from-files']});
const p=await b.newPage();await p.goto('file://'+path.join(__dirname,'scene01.html'));await p.evaluate(()=>window.__ready);fs.writeFileSync('events01.json',JSON.stringify(await p.evaluate(()=>window.EV)));await b.close()})();
