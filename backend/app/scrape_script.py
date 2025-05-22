from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time, json, sys
import requests

def obtener_selectores_y_plan(url: str, instrucciones: str) -> dict:
    prompt = (
        f"A partir de la URL {url}, responde en JSON puro: {{"
        "\"selectores\": {{\"nombre\": \"css\", \"precio\": \"css\", \"disponibilidad\": \"css\"}}, "
        "\"scroll\": true/false, \"click_mas\": \"selector\", \"apartados\": [\"url1\", \"url2\"]}}. "
        "Extrae los selectores más probables para nombre, precio y disponibilidad de productos, "
        "detecta si se necesita scroll para cargar más, si hay botón de 'cargar más' y si hay más secciones de productos."
    )
    try:
        respuesta = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        texto = respuesta.json()["response"]
        return json.loads(texto)
    except Exception as e:
        print(f"[ERROR] Fallo al obtener planificación de la IA: {e}")
        return {}

def ejecutar_scraping(url: str, instrucciones: str):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(3)

        for selector in [
            "button[mode='primary']",
            ".cookies__button",
            ".accept-cookies",
            "#onetrust-accept-btn-handler",
            "button.btn-accept"
        ]:
            try:
                boton = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                boton.click()
                time.sleep(2)
                break
            except:
                continue

        print("[LOG] Solicitando plan de scraping a la IA...")
        plan = obtener_selectores_y_plan(url, instrucciones)
        if not plan or "selectores" not in plan:
            return {"error": "No se pudo obtener planificación de la IA"}

        productos = []
        urls = [url] + plan.get("apartados", [])

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
        print(json.dumps(resultado))