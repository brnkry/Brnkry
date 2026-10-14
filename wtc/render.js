const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const mode = process.argv[2] || 'preview';
  const browser = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--allow-file-access-from-files']});
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.goto('file://' + path.join(__dirname, 'scene01.html'));
  await page.evaluate(() => window.__ready);
  await page.waitForTimeout(300);
  if (errs.length) { console.log('ERR', errs); }
  const stage = await page.$('#stage');
  if (mode === 'preview') {
    const times = process.argv.slice(3).map(Number);
    fs.mkdirSync('prev', { recursive: true });
    for (const t of times) {
      await page.evaluate(t => window.render(t), t);
      await stage.screenshot({ path: `prev/t_${String(t).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 70 });
    }
  } else {
    const fps = 30, dur = Number(process.argv[3] || 66.9);
    const [from, to] = [Number(process.argv[4] || 0), Number(process.argv[5] || Math.ceil(dur * fps))];
    fs.mkdirSync('frames', { recursive: true });
    for (let f = from; f < to; f++) {
      await page.evaluate(t => window.render(t), f / fps);
      await stage.screenshot({ path: `frames/f_${String(f).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92 });
    }
  }
  if (errs.length) console.log('ERR', errs);
  await browser.close();
})();
