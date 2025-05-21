import sys
import json
from scrapegraphai.graphs import SmartScraperGraph

def scrapear_web(url: str, instrucciones: str) -> str:
    prompt = f"Extrae los datos relevantes de esta web: {instrucciones}"

    config = {
        "llm": {
            "provider": "ollama",
            "config": {
                "model": "mistral",
                "base_url": "http://localhost:11434",
            },
        }
    }

    graph = SmartScraperGraph(
        prompt=prompt,
        source=url,
        config=config,
    )

    resultado = graph.run()
    return resultado

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        url = sys.argv[1]
        instrucciones = sys.argv[2]
        try:
            resultado = scrapear_web(url, instrucciones)
            print(json.dumps({"resultado": resultado}))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
    else:
        print(json.dumps({"error": "Faltan argumentos: URL e instrucciones"}))