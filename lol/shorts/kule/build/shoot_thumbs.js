const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, 'thumbs.html'));
  await p.evaluate(async () => { await Promise.all(['400 40px Ant', '700 40px Osw'].map(f => document.fonts.load(f, 'İŞĞÜÇÖ'))); });
  await p.waitForTimeout(300);
  for (const id of ['t1', 't2', 't3']) await p.locator('#' + id).screenshot({ path: path.join(__dirname, '../export/kanal', `kule_thumb_${id.slice(1)}.png`) });
  await b.close(); })();
