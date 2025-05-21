import subprocess
import sys
import json
import os

def ejecutar_scrape_externo(url: str, instrucciones: str) -> dict:
    """
    Ejecuta scrape_script.py como un proceso separado y recoge su salida JSON.
    """
    ruta_script = os.path.join(os.path.dirname(__file__), "scrape_script.py")
    try:
        resultado = subprocess.run(
            [sys.executable, ruta_script, url, instrucciones],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(resultado.stdout)
    except subprocess.CalledProcessError as e:
        return {"error": f"Error en script externo: {e.stderr}"}
    except Exception as e:
        return {"error": str(e)}