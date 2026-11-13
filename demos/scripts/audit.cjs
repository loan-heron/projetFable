// Audit automatique des démos : axe-core (WCAG 2.2 A/AA) + score accessibilité Lighthouse.
// Usage : node audit.cjs <urlDeBase> <dossierSortie>
// Prérequis : npm i axe-core lighthouse chrome-launcher, Playwright + Chromium.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

const BASE = process.argv[2] || 'http://localhost:8765';
const OUT = process.argv[3] || path.join(__dirname, '..', 'audits');
const PAGES = ['celadon', 'foulee', 'vrac'].flatMap(b => ['avant', 'apres'].map(v => ({ boutique: b, version: v })));

async function lighthouseScore(url) {
  const lighthouse = (await import('lighthouse')).default;
  const chromeLauncher = await import('chrome-launcher');
  const chrome = await chromeLauncher.launch({ chromePath: process.env.CHROME_PATH || '/opt/pw-browsers/chromium/chrome-linux64/chrome', chromeFlags: ['--headless=new', '--no-sandbox'] });
  try {
    const r = await lighthouse(url, { port: chrome.port, onlyCategories: ['accessibility'], logLevel: 'error' });
    return Math.round(r.lhr.categories.accessibility.score * 100);
  } finally { await chrome.kill(); }
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const synthese = [];
  for (const { boutique, version } of PAGES) {
    const url = `${BASE}/${boutique}/${version}.html?capture`;
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.addScriptTag({ content: axeSource });
    const res = await page.evaluate(() => axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } }));
    // Tests clavier : commandes cliquables impossibles à atteindre au Tab, et focus invisible.
    const clavier = await page.evaluate(() => {
      const natif = el => el.matches('a[href],button,input,select,textarea,summary,[tabindex]:not([tabindex="-1"])') || el.closest('label');
      const cliquables = [...document.querySelectorAll('[onclick],[data-f],.faux-select,.faux-options div,.favori,.vignette,.teinte,.qte-btn,.entete-acc')].filter(el => !natif(el));
      return { horsClavier: cliquables.length };
    });
    let focusInvisible = 0, arrets = 0;
    await page.mouse.click(1, 1).catch(() => {});
    for (let k = 0; k < 120; k++) {
      await page.keyboard.press('Tab');
      const f = await page.evaluate(() => {
        const el = document.activeElement; if (!el || el === document.body) return null;
        const cs = getComputedStyle(el), cs2 = getComputedStyle(el, '::after');
        const ext = el.closest('label') ? getComputedStyle(el.closest('label').querySelector('span') || el) : cs;
        const visible = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) || cs.boxShadow !== 'none' || (cs2.outlineStyle !== 'none' && parseFloat(cs2.outlineWidth) > 0) || (ext.outlineStyle !== 'none' && parseFloat(ext.outlineWidth) > 0);
        return { id: el.outerHTML.slice(0, 60), visible };
      });
      if (!f) break; arrets++; if (!f.visible) focusInvisible++;
    }
    clavier.arretsTab = arrets; clavier.focusInvisible = focusInvisible;
    await page.close();
    const violations = res.violations.map(v => ({ id: v.id, impact: v.impact, aide: v.help, criteres: v.tags.filter(t => /^wcag\d{3,}$/.test(t)), occurrences: v.nodes.length, url: v.helpUrl }));
    const lh = await lighthouseScore(url);
    const ligne = { boutique, version, lighthouse: lh, regles: violations.length, occurrences: violations.reduce((s, v) => s + v.occurrences, 0), critiques: violations.filter(v => v.impact === 'critical').length, graves: violations.filter(v => v.impact === 'serious').length, ...clavier };
    synthese.push(ligne);
    fs.writeFileSync(path.join(OUT, `${boutique}-${version}.json`), JSON.stringify({ url, date: new Date().toISOString(), ...ligne, violations }, null, 2));
    console.log(JSON.stringify(ligne));
  }
  fs.writeFileSync(path.join(OUT, 'synthese.json'), JSON.stringify(synthese, null, 2));
  await browser.close();
})();
