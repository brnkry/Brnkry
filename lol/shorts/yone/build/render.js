// node render.js preview t1 t2 ... -> prev/t.png ; node render.js frames OUT FPS START END ; node render.js info
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const [mode, ...args] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => console.log('ERR', e.message));
  await page.goto('file://' + path.join(__dirname, process.env.PAGE || 'overlay.html'));
  await page.evaluate(async () => { await document.fonts.load('100px AC', 'AZÇÖÜ'); await window.ready; });
  await page.evaluate(async () => {  });
  if (mode === 'info') { const i = await page.evaluate(() => window.SFX); fs.writeFileSync(path.join(__dirname, 'sfx.json'), JSON.stringify(i)); console.log(i.length, 'sfx'); }
  else if (mode === 'preview') { fs.mkdirSync(path.join(__dirname, 'prev'), { recursive: true });
    for (const t of args) { await page.evaluate(t => window.render(+t), t); await page.waitForTimeout(30); await page.screenshot({ path: path.join(__dirname, 'prev', `${t}.png`), omitBackground: true }); } }
  else { const [out, fps, start, end] = args; fs.mkdirSync(out, { recursive: true });
    const F = +fps, s = Math.round(+start * F), e = Math.round(+end * F);
    let blank = null;
    for (let i = s; i < e; i++) { const vis = await page.evaluate(t => window.render(t), i / F);
      const f = path.join(out, String(i).padStart(5, '0') + '.png');
      if (vis === false && blank) { fs.copyFileSync(blank, f); continue; }
      await page.screenshot({ path: f, omitBackground: true }); if (vis === false) blank = f; } }
  await browser.close();
})();
