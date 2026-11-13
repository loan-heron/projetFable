// Captures des 6 pages : écran d'accueil (1440×900) et mobile (390×844), en JPEG.
// Usage : node captures.cjs <urlDeBase> <dossierSortie>
const { chromium } = require('playwright');
(async () => {
  const [BASE = 'http://localhost:8765', OUT = __dirname + '/../captures'] = process.argv.slice(2);
  const b = await chromium.launch();
  for (const boutique of ['celadon', 'foulee', 'vrac']) for (const version of ['avant', 'apres']) {
    for (const [nom, w, h] of [['ecran', 1440, 900], ['mobile', 390, 844]]) {
      const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
      await p.goto(`${BASE}/${boutique}/${version}.html?capture`, { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
      await p.screenshot({ path: `${OUT}/${boutique}-${version}-${nom}.jpg`, type: 'jpeg', quality: 82 });
      await p.close();
    }
  }
  await b.close();
})();
