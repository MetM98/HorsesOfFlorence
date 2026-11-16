/*
 * Crea le immagini raster del marchio a partire dagli SVG di assets/img/brand/:
 * favicon-32.png, apple-touch-icon.png, icon-192.png, icon-512.png e og-image.jpg (1200×630).
 *
 *   npm install playwright   (oppure un Playwright già installato)
 *   node tools/render_brand.js
 *
 * Va rilanciato solo se cambiano il logo (tools/logo.py) o la foto di apertura.
 */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const BRAND = path.join(ROOT, 'assets', 'img', 'brand');
const url = (p) => 'file://' + path.join(ROOT, p);

const icons = [
  ['favicon-32.png', 32],
  ['apple-touch-icon.png', 180],
  ['icon-192.png', 192],
  ['icon-512.png', 512],
];

const og = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: Montserrat; src: url("${url('assets/fonts/montserrat.woff2')}"); font-weight: 300 600; }
@font-face { font-family: Cormorant; src: url("${url('assets/fonts/cormorant-garamond-italic.woff2')}"); font-style: italic; }
@font-face { font-family: Jost; src: url("${url('assets/fonts/jost.woff2')}"); }
html, body { margin: 0; width: 1200px; height: 630px; overflow: hidden; }
body { position: relative; background: #f7f3eb; font-family: Jost, sans-serif; color: #14223d; }
.photo { position: absolute; inset: 0 430px 0 0; background: url("${url('assets/img/photos/mane-1600.webp')}") 40% 38% / cover; }
.veil { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(247,243,235,0) 38%, rgba(247,243,235,.85) 58%, #f7f3eb 66%); }
.panel { position: absolute; top: 0; bottom: 0; right: 0; width: 470px; display: flex; flex-direction: column; justify-content: center; padding: 0 64px 0 30px; box-sizing: border-box; }
.logo { display: flex; align-items: center; gap: 22px; margin-bottom: 34px; }
.logo img { height: 150px; }
.name { font-family: Montserrat; font-weight: 400; text-transform: uppercase; letter-spacing: .06em; font-size: 25px; line-height: 1.35; }
.name span { font-size: 1.3em; }
.tag { font-family: Cormorant; font-style: italic; font-weight: 500; font-size: 38px; line-height: 1.15; }
.place { margin-top: 26px; font-size: 14px; letter-spacing: .26em; text-transform: uppercase; color: #2f4f86; }
.rule { width: 60px; height: 1px; background: #b9c0ca; margin: 0 0 26px; }
</style></head><body>
<div class="photo"></div><div class="veil"></div>
<div class="panel">
  <div class="logo"><img src="${url('assets/img/brand/mark-navy.svg')}" alt=""><div class="name"><span>H</span>orses<br>of <span>F</span>lorence</div></div>
  <div class="rule"></div>
  <div class="tag">A cavallo in viaggio<br>verso l’armonia.</div>
  <div class="place">Nel cuore del Chianti fiorentino</div>
</div>
</body></html>`;

(async () => {
  const browser = await chromium.launch();
  const tmp = path.join(BRAND, '.render.html');
  for (const [name, size] of icons) {
    // l'icona di iOS non ha trasparenze: il fondo blu arriva fino ai bordi
    const full = name === 'apple-touch-icon.png';
    fs.writeFileSync(tmp, `<!doctype html><style>html,body{margin:0;background:${full ? '#14223d' : 'transparent'}}img{width:${size}px;height:${size}px;display:block}</style><img src="${url('assets/img/brand/favicon.svg')}">`);
    const page = await browser.newPage({ viewport: { width: size, height: size } });
    await page.goto('file://' + tmp);
    await page.waitForFunction(() => document.images[0].complete && document.images[0].naturalWidth > 0);
    await page.screenshot({ path: path.join(BRAND, name), omitBackground: !full });
    await page.close();
    console.log('✓ assets/img/brand/' + name);
  }
  fs.writeFileSync(tmp, og);
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.goto('file://' + tmp);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(BRAND, 'og-image.jpg'), type: 'jpeg', quality: 86 });
  fs.unlinkSync(tmp);
  console.log('✓ assets/img/brand/og-image.jpg');
  await browser.close();
})();
