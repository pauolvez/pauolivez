from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, sys
import requests

def obtener_selectores_y_plan_con_html(url: str, html: str) -> dict:
    prompt_system = (
        "Eres un extractor experto de selectores de scraping. Tu trabajo es analizar HTML real y "
        "devolver un JSON estructurado con selectores CSS válidos para nombre, precio y disponibilidad de productos. "
        "No escribas explicaciones. Devuelve solo el JSON."
    )

    prompt_user = (
        f"Dado el siguiente HTML de la página {url}, analiza su estructura y responde con un JSON así:\n"
        f"{{\n"
        f"  \"selectores\": {{\n"
        f"    \"nombre\": \"...\",\n"
        f"    \"precio\": \"...\",\n"
        f"    \"disponibilidad\": \"...\"\n"
        f"  }},\n"
        f"  \"scroll\": true or false,\n"
        f"  \"click_mas\": \"...\",\n"
        f"  \"apartados\": [\"...\", \"...\"]\n"
        f"}}\n\n"
        f"No des explicaciones. Solo JSON válido.\n\n"
        f"HTML:\n{html[:5000]}"
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "mistral",
                "stream": False,
                "messages": [
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": prompt_user}
                ]
            }
        )
        try:
            json_data = response.json()
            if "message" in json_data and "content" in json_data["message"]:
                texto = json_data["message"]["content"]
                print("[DEBUG] Respuesta de la IA:\n", texto)
                return json.loads(texto)
            else:
                print("[ERROR] Formato inesperado de respuesta:", json_data)
                return {}
        except json.JSONDecodeError as e:
            print(f"[ERROR] Fallo al parsear JSON: {e}")
            print("[DEBUG] Texto recibido:", response.text)
            return {}

    except Exception as e:
        print(f"[ERROR] Fallo al obtener planificación de la IA: {e}")
        return {}

def ejecutar_scraping(url: str, instrucciones: str):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)

        # Aceptar cookies si existen
        for selector in [
            "button[mode='primary']",
            ".cookies__button",
            ".accept-cookies",
            "#onetrust-accept-btn-handler",
            "button.btn-accept"
        ]:
            try:
                boton = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                boton.click()
                time.sleep(1)
                break
            except:
                continue

        print("[LOG] Solicitando plan de scraping a la IA...")

        for _ in range(20):
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1.5)

        html = driver.page_source

        # ✅ Detector de Cloudflare u otras protecciones
        if "cf-challenge" in html or "<title>Un momento" in html or "Checking your browser" in html:
            print("[ERROR] La página está protegida por un challenge (Cloudflare u otro).")
            return {"error": "Bloqueo por protección anti-bot (Cloudflare u otro)"}

        print("[DEBUG] HTML enviado a la IA (recortado):\n")
        print(html[:2000])

        plan = obtener_selectores_y_plan_con_html(url, html)
        if not plan or "selectores" not in plan:
            return {"error": "No se pudo obtener planificación de la IA"}

        print("[DEBUG] Plan de la IA:", json.dumps(plan, indent=2))

        productos = []
        urls = [url]

        for apartado in plan.get("apartados", []):
            if apartado.startswith("http"):
                urls.append(apartado)
            elif apartado.startswith("/"):
                base = "/".join(url.split("/")[:3])
                urls.append(base + apartado)

        for current_url in urls:
            print(f"[LOG] Procesando: {current_url}")
            driver.get(current_url)
            time.sleep(2)

            if plan.get("scroll"):
                print("[LOG] Ejecutando scroll automático")
                for _ in range(10):
                    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                    time.sleep(1)

            if plan.get("click_mas"):
                print("[LOG] Intentando hacer clic en botón 'Cargar más'")
                try:
                    while True:
                        boton = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, plan["click_mas"]))
                        )
                        driver.execute_script("arguments[0].click();", boton)
                        time.sleep(2)
                except:
                    print("[LOG] No hay más botones de 'Cargar más' o no clicable")

            contenedores = driver.find_elements(By.CSS_SELECTOR, plan["selectores"]["nombre"])
            print(f"[LOG] Contenedores detectados: {len(contenedores)}")

            for cont in contenedores:
                try:
                    nombre = cont.text
                except:
                    nombre = "Desconocido"
                try:
                    precio = cont.find_element(By.CSS_SELECTOR, plan["selectores"]["precio"]).text
                except:
                    precio = "No disponible"
                try:
                    disponibilidad = cont.find_element(By.CSS_SELECTOR, plan["selectores"]["disponibilidad"]).text
                except:
                    disponibilidad = "Desconocida"

                productos.append({
                    "nombre": nombre.strip(),
                    "precio": precio.strip(),
                    "disponibilidad": disponibilidad.strip()
                })

        print(f"[LOG] Total de productos recopilados: {len(productos)}")
        return {"productos": productos}

    except Exception as e:
        print(f"[ERROR] Fallo en scraping: {str(e)}")
        return {"error": str(e)}

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "URL e instrucciones requeridas"}))
    else:
        url = sys.argv[1]
        instrucciones = sys.argv[2]
        resultado = ejecutar_scraping(url, instrucciones)
        print(json.dumps(resultado, indent=2))
