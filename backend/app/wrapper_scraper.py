# wrapper_scraper.py
import subprocess
import sys
import json
import os

def ejecutar_scrape_externo(url: str, instrucciones: str) -> dict:
    try:
        result = subprocess.run(
            [sys.executable, os.path.join("app", "scrape_script.py"), url, instrucciones],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            return {
                "error": "El script falló",
                "stderr": result.stderr.strip(),
                "stdout": result.stdout.strip()
            }

        last_line = result.stdout.strip().splitlines()[-1]
        resultado_json = json.loads(last_line)

        # ✅ Solo aquí se devuelve con "resultado"
        return {"resultado": resultado_json}

    except Exception as e:
        return {"error": str(e)}