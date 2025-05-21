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
            "api_key": "ollama",
            "type": "ollama"
        }
    }

    prompt = f"Extrae información útil en formato JSON. Instrucciones: {instrucciones}"

    try:
        graph = SmartScraperGraph(prompt=prompt, source=url, config=config)
        resultado = graph.run()

        # 🚫 Evita impresiones extras y solo devuelve JSON
        json_output = json.dumps({"resultado": resultado})
        sys.stdout.write(json_output)
        sys.stdout.flush()
    except Exception as e:
        error_output = json.dumps({"error": str(e)})
        sys.stdout.write(error_output)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
