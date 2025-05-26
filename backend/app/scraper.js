const fs = require('fs');
const readline = require('readline');
const { chromium } = require('playwright');

async function prompt(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => rl.question(question, answer => {
    rl.close();
    resolve(answer);
  }));
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function scrapePage(page, selector) {
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
    } catch (e) {}
  }

  return results;
}

async function main() {
  const url = await prompt("🔗 Introduce la URL de la primera página: ");
  const nextSelector = await prompt("➡️ Introduce el selector CSS del botón de 'siguiente página': ");

  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto(url);

  const allData = [];

  while (true) {
    await page.waitForTimeout(2000);
    const data = await scrapePage(page, nextSelector);
    console.log(`📦 Productos en esta página: ${data.length}`);
    allData.push(...data);

    const next = await page.$(nextSelector);
    if (!next) break;

    await next.click();
    await delay(3000);
  }

  // Guardar CSV
  const header = "nombre,precio,imagen,url\n";
  const rows = allData.map(d =>
    `"${d.nombre.replace(/"/g, '""')}","${d.precio}","${d.imagen}","${d.url}"`
  ).join("\n");

  fs.writeFileSync('productos.csv', header + rows, 'utf8');
  console.log("✅ ¡Scraping finalizado! Archivo: productos.csv");

  await browser.close();
}

main();