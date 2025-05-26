
(async () => {
  function isUsefulBlock(el) {
    const text = el.innerText || '';
    const hasTitle = !!el.querySelector('h1, h2, h3, .title, .product-title');
    const hasPrice = !!el.querySelector('.price, .product-price, .prices__price--current');
    const hasImg = !!el.querySelector('img');
    const area = el.getBoundingClientRect();
    const visible = area.width > 50 && area.height > 50;
    return text.length > 20 && visible && (hasTitle || hasPrice || hasImg);
  }

  function getRepeatingBlocks(min = 5) {
    const all = Array.from(document.querySelectorAll("div, li, article, section"));
    const grouped = {};
    all.forEach(el => {
      if (!isUsefulBlock(el)) return;
      const key = el.tagName + "|" + el.className.trim();
      grouped[key] = grouped[key] || [];
      grouped[key].push(el);
    });
    return Object.values(grouped).find(group => group.length >= min) || [];
  }

  function extract(el) {
    const titleEl = el.querySelector('h1, h2, h3, .title, .product-title');
    const priceEl = el.querySelector('.price, .product-price, .prices__price--current');
    const imgEl = el.querySelector('img');
    const linkEl = el.querySelector('a[href]');
    return {
      nombre: titleEl ? titleEl.innerText.trim() : '',
      precio: priceEl ? priceEl.innerText.trim() : '',
      imagen: imgEl ? imgEl.src : '',
      url: linkEl ? linkEl.href : ''
    };
  }

  function exportCSV(data, filename = "scraped_data.csv") {
    const headers = Object.keys(data[0]);
    const rows = data.map(row => headers.map(h => `"${(row[h] || "").replace(/"/g, '""')}"`).join(","));
    const csv = [headers.join(","), ...rows].join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  const nextButtonSelector = prompt("Introduce el selector CSS del botón de 'siguiente página'");

  if (!nextButtonSelector) {
    alert("No se proporcionó selector de botón. Cancelando.");
    return;
  }

  const allData = [];

  while (true) {
    const blocks = getRepeatingBlocks();
    const data = blocks.map(extract).filter(row =>
      row.nombre || row.precio || row.imagen || row.url
    );

    console.log("✅ Página scrapeada:", data.length, "elementos.");
    allData.push(...data);

    const nextBtn = document.querySelector(nextButtonSelector);
    if (!nextBtn || nextBtn.disabled || nextBtn.classList.contains('disabled')) break;

    nextBtn.click();
    await new Promise(r => setTimeout(r, 3000)); // esperar carga
  }

  if (!allData.length) {
    alert("❌ No se encontraron productos.");
    return;
  }

  exportCSV(allData);
})();
