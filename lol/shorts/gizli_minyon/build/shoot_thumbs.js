const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, 'thumbs.html'));
  await p.evaluate(async () => { await Promise.all(['900 40px Bf', '900 40px Mon'].map(f => document.fonts.load(f, 'İŞĞÜÇÖ'))); });
  const SAFE = 0.76;  // mobile safe area: shrink the text/icons toward the centre, background stays full-bleed
  await p.evaluate(S => { if (S === 1) return; document.querySelectorAll('.th').forEach(th => { const w = document.createElement('div'); w.style.cssText = `position:absolute;inset:0;transform:scale(${S});transform-origin:540px 960px`;
    [...th.children].filter(c => !c.classList.contains('bg') && !c.classList.contains('sh')).forEach(c => w.appendChild(c)); th.appendChild(w); }); }, SAFE);
  await p.waitForTimeout(300);
  for (const id of ['t1', 't2', 't3']) await p.locator('#' + id).screenshot({ path: path.join(__dirname, '../export', `thumb_${id.slice(1)}.png`) });
  await b.close(); })();
