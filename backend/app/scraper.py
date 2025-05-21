from app.wrapper_scraper import ejecutar_scrape_externo

async def ejecutar_scraping_web(url: str, instrucciones: str) -> dict:
    """
    Ejecuta el scraping llamando a un script externo usando subprocess,
    lo que permite evitar los errores de asyncio y playwright en Windows.
    """
    return ejecutar_scrape_externo(url, instrucciones)