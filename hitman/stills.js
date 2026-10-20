// usage: node stills.js out_prefix t1 t2 ...  -> contact sheet frames
const { chromium } = require('../wtc/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('console',m=>{if(!/404/.test(m.text()))console.log(m.text())});p.on('pageerror',e=>{console.log('ERR',e.message);process.exit(1)});
await p.goto('http://localhost:8765/film.html');await p.waitForFunction(()=>window.ready,null,{timeout:120000});
const ts=process.argv.slice(3).map(Number);for(const t of ts){await p.evaluate(t=>R(t),t);await p.screenshot({path:`${process.argv[2]}_${t.toFixed(2)}.jpg`,type:'jpeg',quality:85});}
console.log(await p.evaluate(()=>JSON.stringify([DURATION,SHOTS])));await b.close()})();
