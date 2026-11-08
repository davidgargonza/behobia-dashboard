// Captura og.html a og.png (1200x630). Requiere playwright.
const { chromium } = require('playwright'); const path = require('path');
(async () => { const root = path.resolve(__dirname, '..'); const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(root, 'og.html')); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(root, 'og.png') }); await b.close(); })();
