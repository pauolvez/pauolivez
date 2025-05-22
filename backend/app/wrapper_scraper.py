import subprocess
import sys
import os
import json

def ejecutar_scrape_externo(url: str, instrucciones: str) -> dict:
    script_path = os.path.join(os.path.dirname(__file__), "scrape_script.py")

    result = subprocess.run(
        [sys.executable, script_path, url, instrucciones],
        capture_output=True,
        text=True
    )

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "error": "Error al decodificar la salida del script externo",
            "raw_stdout": result.stdout,
            "raw_stderr": result.stderr,
        }