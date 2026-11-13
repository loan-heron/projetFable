// Usage : node capture.cjs <url> <sortie.png> [largeur] [hauteur] [pleinePage 0|1]
const { chromium } = require('playwright');
(async () => {
  const [url, out, w = '1440', h = '900', full = '0'] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1 });
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  await p.screenshot({ path: out, fullPage: full === '1' });
  await b.close();
})();
