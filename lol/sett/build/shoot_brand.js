// node shoot_brand.js -> renders logo, banner and thumbnails from brand2.html into ../export/kanal
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 2560, height: 5200 } });
  await p.goto('file://' + __dirname + '/brand2.html');
  await p.evaluate(async () => {
    await Promise.all(['900 80px Cin', '700 40px Cin', '400 80px Ant', '700 40px Osw'].map(f => document.fonts.load(f, 'İŞĞÜÇÖ4')));
    await Promise.all([...document.images].map(i => i.decode().catch(() => { })));
  });
  for (const [id, f] of [['logo', 'logo_800.png'], ['banner', 'banner_2560x1440.png'], ['t1', 'thumb1.png'], ['t2', 'thumb2.png'], ['t3', 'thumb3.png']])
    await p.locator('#' + id).screenshot({ path: __dirname + '/../export/kanal/' + f });
  await b.close();
})();
