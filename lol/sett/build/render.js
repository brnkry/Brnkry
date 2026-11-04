// node render.js preview t1 t2 ...   -> prev/t.png (over checker gray)
// node render.js frames OUTDIR FPS START END -> OUTDIR/%05d.png (transparent)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const [mode, ...args] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: fs.existsSync('/opt/pw-browsers/chromium') && fs.statSync('/opt/pw-browsers/chromium').isFile() ? '/opt/pw-browsers/chromium' : undefined });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(__dirname, 'overlay.html'));
  await page.evaluate(async () => {
    await Promise.all(['400 40px Osw', '600 40px Osw', '700 40px Osw', '600 30px Int', '800 30px Int'].map(f => document.fonts.load(f, 'İşğüçöÖÇŞĞÜ AZaz')));
    await window.ready;
  });
  const info = await page.evaluate(() => ({ missing: MISSING, cues: CUES }));
  console.log('missing cues:', JSON.stringify(info.missing));
  fs.writeFileSync(path.join(__dirname, 'cues.json'), JSON.stringify(info.cues, null, 1));
  if (mode === 'preview') {
    fs.mkdirSync(path.join(__dirname, 'prev'), { recursive: true });
    for (const t of args) {
      await page.evaluate(t => { document.body.style.background = '#556'; window.render(+t) }, t);
      await page.screenshot({ path: path.join(__dirname, 'prev', `${t}.png`) });
    }
  } else {
    const [out, fps, start, end] = args;
    fs.mkdirSync(out, { recursive: true });
    const F = +fps, s = Math.round(+start * F), e = Math.round(+end * F);
    for (let i = s; i < e; i++) {
      await page.evaluate(t => window.render(t), i / F);
      await page.screenshot({ path: path.join(out, String(i).padStart(5, '0') + '.png'), omitBackground: true });
      if (i % 300 === 0) console.log('frame', i, '/', e);
    }
  }
  await browser.close();
})();
