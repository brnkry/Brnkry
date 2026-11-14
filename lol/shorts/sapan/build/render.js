// node render.js preview t1 t2 ... -> prev/t.png ; node render.js frames OUT FPS START END ; node render.js info
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const [mode, ...args] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => console.log('ERR', e.message));
  await page.goto('file://' + path.join(__dirname, 'overlay.html'));
  await page.evaluate(async () => { await Promise.all(['400 40px Ant', '700 40px Osw', '800 40px Mon', '900 40px Mon'].map(f => document.fonts.load(f, 'İşğüçöÖÇŞĞÜ AZaz'))); await window.ready; });
  await page.evaluate(async () => {  });
  if (mode === 'info') { const i = await page.evaluate(() => ({ m: MISSING, T: CUES, SFX })); fs.writeFileSync(path.join(__dirname, 'sfx.json'), JSON.stringify(i.SFX)); console.log(JSON.stringify(i.m), JSON.stringify(i.T)); }
  else if (mode === 'preview') { fs.mkdirSync(path.join(__dirname, 'prev'), { recursive: true });
    for (const t of args) { await page.evaluate(t => window.render(+t), t); await page.waitForTimeout(30); await page.screenshot({ path: path.join(__dirname, 'prev', `${t}.png`), omitBackground: true }); } }
  else { const [out, fps, start, end] = args; fs.mkdirSync(out, { recursive: true });
    const F = +fps, s = Math.round(+start * F), e = Math.round(+end * F);
    for (let i = s; i < e; i++) { await page.evaluate(t => window.render(t), i / F);
      await page.screenshot({ path: path.join(out, String(i).padStart(5, '0') + '.png'), omitBackground: true }); } }
  await browser.close();
})();
