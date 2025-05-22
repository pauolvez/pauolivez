from scrapegraphai.graphs import SmartScraperGraph
from concurrent.futures import ThreadPoolExecutor
import asyncio

executor = ThreadPoolExecutor()

def _scrap_sync(prompt: str, url: str):
    config = {
        "llm": {
            "api_base": "http://localhost:11434",  # Dirección local del servidor de Ollama
            "api_key": "ollama",  # No se usa, pero requerido por la estructura
            "model": "mistral",  # Nombre del modelo cargado en Ollama
            "type": "ollama"  # Tipo de LLM que estamos usando
        }
    }

    graph = SmartScraperGraph(
        prompt=prompt,
        source=url,
        config=config
    )

    return graph.run()

async def ejecutar_scraping_web(url: str, instrucciones: str):
    prompt = f"Extrae la información más útil de la web: {instrucciones}"
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, _scrap_sync, prompt, url)
    return result