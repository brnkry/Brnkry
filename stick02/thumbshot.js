// usage: node thumbshot.js <t> <out.png> [clean]  -> clean hides bubbles, stickers, the neon sign and ON AIR (for thumbnail backgrounds)
const { chromium } = require('../wtc/node_modules/playwright');const path=require('path');
(async()=>{const [t,out,clean]=process.argv.slice(2);
 const br=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args:['--allow-file-access-from-files']});
 const p=await br.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+path.join(__dirname,'scene.html'));await p.evaluate(()=>window.__ready);await p.waitForTimeout(300);
 await p.evaluate(([t,clean])=>{window.render(+t);if(clean){['bubbles','texts','fx','sign'].forEach(i=>document.getElementById(i).style.visibility='hidden');document.querySelector('#room g[transform="translate(540 1052)"]').style.visibility='hidden'}},[t,clean]);
 await (await p.$('#stage')).screenshot({path:out});await br.close()})();
