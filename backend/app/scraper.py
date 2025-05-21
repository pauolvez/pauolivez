from playwright.async_api import async_playwright

async def buscar_productos_aliexpress(query: str):
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        url = f"https://www.aliexpress.com/wholesale?SearchText={query}"
        await page.goto(url)
        await page.wait_for_selector('a._3t7zg._2f4Ho', timeout=10000)

        productos = await page.query_selector_all('a._3t7zg._2f4Ho')

        for producto in productos[:5]:
            titulo_el = await producto.query_selector('h1, h2, h3, .title, span')
            enlace = await producto.get_attribute('href')
            titulo = await titulo_el.inner_text() if titulo_el else "Sin título"
            resultados.append({
                "titulo": titulo,
                "enlace": f"https:{enlace}" if enlace and enlace.startswith("//") else enlace,
            })

        await browser.close()

    return resultados
