from scrapegraphai.graphs import SmartScraperGraph
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

def run_graph_sync(prompt, url):
    graph_config = {
        "llm": {
            "model": "ollama/mistral",
            "api_base": "http://localhost:11434",
            "api_key": "ollama",
            "type": "ollama"
        }
    }

    graph = SmartScraperGraph(
        prompt=prompt,
        source=url,
        config=graph_config,
    )

    return graph.run()

async def ejecutar_scraping_web(url: str, instrucciones: str) -> dict:
    prompt = (
        "Extrae información relevante de la siguiente web y devuélvela como JSON. "
        f"Instrucciones específicas: {instrucciones}"
    )

    loop = asyncio.get_event_loop()
    resultado = await loop.run_in_executor(executor, run_graph_sync, prompt, url)
    return resultado