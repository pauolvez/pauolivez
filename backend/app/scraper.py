from app.wrapper_scraper import ejecutar_scrape_externo

async def ejecutar_scraping_web(url: str, instrucciones: str) -> dict:
    """
    Ejecuta el scraping llamando a un script externo usando subprocess,
    lo que permite evitar los errores de asyncio y playwright en Windows.
    """

    resultado = ejecutar_scrape_externo(url, instrucciones)

    # Si el resultado ya es un diccionario válido, lo retornamos.
    if isinstance(resultado, dict):
        return {"resultado": resultado}
    else:
        # Si hubo algún error inesperado
        return {"resultado": {"error": "Respuesta inesperada del script externo"}}