// usage: node render.js <scene.html> preview t1 t2 ...   |   node render.js <scene.html> full DUR from to
const { chromium } = require('../wtc/node_modules/playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const [scene, mode] = [process.argv[2], process.argv[3] || 'preview'];
  const browser = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args:['--allow-file-access-from-files']});
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.goto('file://' + path.join(__dirname, scene));
  await page.evaluate(() => window.__ready);
  await page.waitForTimeout(300);
  const stage = await page.$('#stage');
  const tag = path.basename(scene, '.html');
  if (mode === 'preview') {
    fs.mkdirSync('prev', { recursive: true });
    for (const t of process.argv.slice(4).map(Number)) {
      await page.evaluate(t => window.render(t), t);
      await stage.screenshot({ path: `prev/${tag}_${t.toFixed(2).padStart(6, '0')}.jpg`, type: 'jpeg', quality: 70 });
    }
  } else if (mode === 'events') {
    fs.writeFileSync(`events_${tag}.json`, JSON.stringify(await page.evaluate(() => window.EV)));
    console.log('DUR', await page.evaluate(() => window.DUR));
  } else {
    const fps = 30, dur = Number(process.argv[4]);
    const [from, to] = [Number(process.argv[5] || 0), Number(process.argv[6] || Math.ceil(dur * fps))];
    const dir = `frames_${tag}`; fs.mkdirSync(dir, { recursive: true });
    for (let f = from; f < to; f++) {
      await page.evaluate(t => window.render(t), f / fps);
      await stage.screenshot({ path: `${dir}/f_${String(f).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92 });
    }
  }
  if (errs.length) console.log('ERR', errs);
  await browser.close();
})();
