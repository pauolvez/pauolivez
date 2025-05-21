import subprocess
import json

def ejecutar_scrape_externo(url: str, instrucciones: str) -> dict:
    try:
        result = subprocess.run(
            ["python", "app/scrape_script.py", url, instrucciones],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            raise RuntimeError(f"Error en script externo: {result.stderr}")

        output = result.stdout.strip()
        return json.loads(output)

    except Exception as e:
        return {"error": str(e)}