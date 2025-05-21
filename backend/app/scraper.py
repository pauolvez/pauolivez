from playwright.async_api import async_playwright

async def buscar_productos_aliexpress(query: str, max_resultados: int = 5):
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = f"https://www.aliexpress.com/wholesale?SearchText={query}"
        await page.goto(url)

        await page.wait_for_selector("div[data-widget='productCard']")

        items = await page.query_selector_all("div[data-widget='productCard']")[:max_resultados]

        for item in items:
            nombre = await item.query_selector_eval("a", "el => el.innerText") if await item.query_selector("a") else "Sin nombre"
            enlace = await item.query_selector_eval("a", "el => el.href") if await item.query_selector("a") else ""
            imagen = await item.query_selector_eval("img", "el => el.src") if await item.query_selector("img") else ""
            precio = await item.query_selector_eval(".manhattan--price-sale", "el => el.innerText") if await item.query_selector(".manhattan--price-sale") else "?"

            resultados.append({
                "nombre": nombre.strip(),
                "enlace": enlace,
                "imagen": imagen,
                "precio": precio.strip()
            })

        await browser.close()

    return resultados
