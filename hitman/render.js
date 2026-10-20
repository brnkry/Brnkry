// usage: node render.js outdir [fps] [from] [to]  -> outdir/f00000.jpg ...
const { chromium } = require('../wtc/node_modules/playwright'); const fs=require('fs');
(async()=>{const out=process.argv[2], fps=+(process.argv[3]||12); fs.mkdirSync(out,{recursive:true});
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>{console.log('ERR',e.message);process.exit(1)});
await p.goto('http://localhost:8765/film.html');await p.waitForFunction(()=>window.ready,null,{timeout:120000});
const D=await p.evaluate(()=>DURATION); const n=Math.round(D*fps); const a=+(process.argv[4]||0), z=+(process.argv[5]||n);
for(let i=a;i<z;i++){await p.evaluate(t=>R(t),i/fps);await p.screenshot({path:`${out}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});if(i%60==0)console.log(i,'/',n);}
await b.close()})();
