
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

// ─────────────────────────────────────────────
// CONFIGURACIÓN
const CONFIG_PATH = path.join(__dirname, 'sites.json');
const OUTPUT_FILE = 'productos.csv';
const WAIT_TIME = 2000;
const NAV_TIMEOUT = 10000;

// ─────────────────────────────────────────────
// FUNCIONES
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function acceptCookies(page) {
  const cookieSelectors = [
    'button[aria-label*="Aceptar"]',
    'button:has-text("Aceptar")',
    'button:has-text("aceptar")',
    'button:has-text("Accept")',
    'button:has-text("OK")'
  ];
  for (let selector of cookieSelectors) {
    try {
      const btn = await page.$(selector);
      if (btn) {
        await btn.click();
        console.log("🍪 Cookies aceptadas.");
        await page.waitForTimeout(1000);
        break;
      }
    } catch (_) {}
  }
}

async function scrapePage(page) {
  const blocks = await page.$$('div, article, li, section');
  const results = [];

  for (let el of blocks) {
    try {
      const text = await el.innerText();
      if (text.length < 20) continue;

      const visible = await el.boundingBox();
      if (!visible || visible.width < 50 || visible.height < 50) continue;

      const title = await el.$('h1, h2, h3, .title, .product-title');
      const price = await el.$('.price, .product-price, .prices__price--current');
      const img = await el.$('img');
      const link = await el.$('a[href]');

      const data = {
        nombre: title ? (await title.innerText()).trim() : '',
        precio: price ? (await price.innerText()).trim() : '',
        imagen: img ? await img.getAttribute('src') : '',
        url: link ? await link.getAttribute('href') : ''
      };

      if (data.nombre || data.precio || data.imagen || data.url) {
        results.push(data);
      }
    } catch (_) {}
  }

  return results;
}

async function scrapeSite(browser, startUrl, nextSelector) {
  const page = await browser.newPage();
  await page.goto(startUrl, { waitUntil: 'domcontentloaded' });
  await acceptCookies(page);

  const allData = [];

  while (true) {
    await page.waitForTimeout(WAIT_TIME);
    const data = await scrapePage(page);
    console.log(`📦 Productos en esta página (${page.url()}): ${data.length}`);
    allData.push(...data);

    const currentUrl = page.url();
    const next = await page.$(nextSelector);
    if (!next) {
      console.log("⛔ Botón 'siguiente' no encontrado.");
      break;
    }

    const isDisabled = await next.getAttribute('disabled');
    const classAttr = await next.getAttribute('class') || '';
    if (isDisabled !== null || classAttr.includes('disabled')) {
      console.log("⛔ Botón 'siguiente' deshabilitado.");
      break;
    }

    console.log("➡️ Haciendo clic en 'siguiente'...");
    await Promise.all([
      next.click(),
      page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: NAV_TIMEOUT }).catch(() => {})
    ]);

    if (page.url() === currentUrl) {
      console.log("⚠️ No cambió la URL tras hacer clic.");
      break;
    }
  }

  await page.close();
  return allData;
}

async function main() {
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  const browser = await chromium.launch({ headless: false });
  const allResults = [];

  for (const entry of config.sites) {
    console.log(`🌐 Iniciando scraping de: ${entry.url}`);
    const data = await scrapeSite(browser, entry.url, entry.next_button_selector);
    allResults.push(...data);
  }

  // Guardar CSV
  const header = "nombre,precio,imagen,url\n";
  const rows = allResults.map(d =>
    `"${d.nombre.replace(/"/g, '""')}","${d.precio}","${d.imagen}","${d.url}"`
  ).join("\n");

  fs.writeFileSync(OUTPUT_FILE, header + rows, 'utf8');
  console.log(`✅ Scraping finalizado. Archivo generado: ${OUTPUT_FILE}`);

  await browser.close();
}

main();
