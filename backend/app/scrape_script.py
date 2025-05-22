# scrape_script.py
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

    prompt = ( f"Devuelve los datos en formato JSON válido, sin explicaciones, sin comentarios y sin texto adicional. " f"Tu salida debe comenzar y terminar con llaves. {instrucciones}")

    try:
        graph = SmartScraperGraph(prompt=prompt, source=url, config=config)
        resultado = graph.run()

        # ✅ Devuelve el resultado directamente, sin anidarlo en "resultado"
        sys.stdout.write(json.dumps(resultado))
        sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(json.dumps({"error": str(e)}))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
