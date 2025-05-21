import json
import sys
from scrapegraphai.graphs import SmartScraperGraph

def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "URL e instrucciones requeridas"}))
        return

    url = sys.argv[1]
    instrucciones = sys.argv[2]

    config = {
        "llm": {
            "model": "mistral",
            "api_base": "http://localhost:11434",
            "api_key": "ollama",  # requerido pero no se valida
            "type": "ollama"
        }
    }

    prompt = f"Extrae información útil en formato JSON. Instrucciones: {instrucciones}"

    try:
        graph = SmartScraperGraph(prompt=prompt, source=url, config=config)
        resultado = graph.run()
        print(json.dumps({"resultado": resultado}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()