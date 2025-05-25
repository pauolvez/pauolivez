import json, sys, time, requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import cloudscraper
from scraper_graph import ejecutar_scraping_web
from flaresolverr_manager import start_flaresolverr


def obtener_html_cloudscraper(url):
    print("[SCRAPER] Intentando obtener HTML con Cloudscraper...")
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        if response.status_code == 200:
            print("[SCRAPER] Cloudscraper obtuvo respuesta 200")
            return response.text
        else:
            print(f"[SCRAPER] Cloudscraper fallo con código {response.status_code}")
            return None
    except Exception as e:
        print(f"[SCRAPER] Error con Cloudscraper: {e}")
        return None


def obtener_html_tor(url):
    print("[SCRAPER] Intentando obtener HTML vía Tor...")
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=15)
        if response.status_code == 200:
            print("[SCRAPER] HTML recibido correctamente por Tor")
            return response.text
        else:
            print(f"[SCRAPER] Tor devolvió código: {response.status_code}")
            return None
    except Exception as e:
        print(f"[SCRAPER] Error usando Tor: {e}")
        return None


def obtener_selectores_y_plan_con_html(url: str, html: str) -> dict:
    prompt_system = (
        "Eres un extractor experto de selectores de scraping web en formato CSS. "
        "Devuelve únicamente un JSON válido, sin comentarios, sin explicaciones. "
        "Estructura exacta: { 'selectores': {...}, 'scroll': true/false, 'click_mas': '...', 'apartados': [...] }. "
        "No pongas 'scroll', 'click_mas' ni 'apartados' dentro de 'selectores'."
    )
    prompt_user = f"""
Analiza esta página {url} y responde solo con el JSON siguiente:
{{
  "selectores": {{"nombre": "...", "precio": "...", "disponibilidad": "..."}},
  "scroll": true/false,
  "click_mas": "...",
  "apartados": ["...", "..."]
}}
Devuélvelo sin explicaciones, solo el JSON.
HTML:
{html[:6000]}
"""
    try:
        r = requests.post(
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
        data = r.json()
        content = data["message"]["content"]
        print("[DEBUG] Respuesta cruda de la IA:", content)

        try:
            plan = json.loads(content)
            if not all(k in plan for k in ["selectores", "scroll", "click_mas", "apartados"]):
                raise ValueError("Plan incompleto o mal estructurado")
            return plan
        except Exception as je:
            print(f"[ERROR] La IA devolvió un JSON inválido o incompleto: {je}")
            with open("error_respuesta_ia.txt", "w", encoding="utf-8") as f:
                f.write(content)
            return {}

    except Exception as e:
        print(f"[ERROR] Fallo al obtener planificación de la IA: {e}")
        return {}


def extraer_productos_en_pagina(driver, plan):
    productos = []
    contenedores = driver.find_elements(By.CSS_SELECTOR, plan["apartados"][0])
    print(f"[LOG] Contenedores detectados: {len(contenedores)}")

    for cont in contenedores:
        try:
            nombre = cont.find_element(By.CSS_SELECTOR, plan["selectores"]["nombre"]).text.strip()
        except:
            nombre = "Desconocido"
        try:
            precio = cont.find_element(By.CSS_SELECTOR, plan["selectores"]["precio"]).text.strip()
        except:
            precio = "No disponible"
        try:
            disponibilidad = cont.find_element(By.CSS_SELECTOR, plan["selectores"]["disponibilidad"]).text.strip()
        except:
            disponibilidad = "Desconocida"

        productos.append({
            "nombre": nombre,
            "precio": precio,
            "disponibilidad": disponibilidad
        })
    return productos


def navegar_y_extraer(driver, url, plan):
    productos = []
    secciones_visitadas = set()

    def procesar():
        if plan.get("scroll"):
            for _ in range(5):
                driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                time.sleep(1)

        if plan.get("click_mas"):
            while True:
                try:
                    btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, plan["click_mas"]))
                    )
                    driver.execute_script("arguments[0].click();", btn)
                    print("[SCRAPER] Click en botón 'más'")
                    time.sleep(2)
                except:
                    break

        productos.extend(extraer_productos_en_pagina(driver, plan))

    print(f"[SCRAPER] Navegando sección principal: {url}")
    driver.get(url)
    time.sleep(3)
    procesar()

    for selector in plan["apartados"]:
        enlaces = driver.find_elements(By.CSS_SELECTOR, selector)
        for a in enlaces:
            try:
                href = a.get_attribute("href")
                if href and href not in secciones_visitadas:
                    secciones_visitadas.add(href)
                    print(f"[SCRAPER] Visitando sección: {href}")
                    driver.get(href)
                    time.sleep(3)
                    procesar()
            except:
                continue
    return productos


def ejecutar_scraping(url: str, instrucciones: str):
    print("[SCRAPER] Iniciando FlareSolverr...")
    flaresolverr_proc = start_flaresolverr()
    print("[SCRAPER] FlareSolverr iniciado.")

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.headless = False

    driver = uc.Chrome(options=options)

    try:
        stealth(driver,
                languages=["es-ES", "es"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        print("[SCRAPER] Abriendo página en navegador UC...")
        driver.get(url)
        time.sleep(4)

        html = driver.page_source
        print("[DEBUG] HTML enviado a la IA (recortado):\n", html[:2000])

        if "challenge" in html or "verificación" in html.lower():
            print("[ERROR] Bloqueo detectado en Selenium. Intentando Cloudscraper...")
            html = obtener_html_cloudscraper(url)
            if html:
                plan = obtener_selectores_y_plan_con_html(url, html)
                if plan:
                    return ejecutar_scraping_ligero(html, plan)
                else:
                    return {"error": "Cloudscraper no generó plan"}

            print("[ERROR] Cloudscraper falló. Probando Tor...")
            html = obtener_html_tor(url)
            if html:
                plan = obtener_selectores_y_plan_con_html(url, html)
                if plan:
                    return ejecutar_scraping_ligero(html, plan)
                else:
                    return {"error": "Tor no generó plan"}

            print("[ERROR] Todos los métodos fallaron. Usando scraper alternativo.")
            return ejecutar_scraping_web(url, instrucciones)

        plan = obtener_selectores_y_plan_con_html(url, html)
        if not plan or "selectores" not in plan:
            return {"error": "No se pudo obtener planificación de la IA"}

        print("[DEBUG] Plan de la IA:\n", json.dumps(plan, indent=2))
        productos = navegar_y_extraer(driver, url, plan)
        print(f"[LOG] Total de productos recopilados: {len(productos)}")
        return {"productos": productos, "fuente": "selenium_uc"}

    except Exception as e:
        print(f"[ERROR] Fallo en scraping: {str(e)}")
        return {"error": str(e)}

    finally:
        driver.quit()
        if flaresolverr_proc:
            flaresolverr_proc.terminate()
            print("[SCRAPER] FlareSolverr detenido.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "URL e instrucciones requeridas"}))
    else:
        url = sys.argv[1]
        instrucciones = sys.argv[2]
        resultado = ejecutar_scraping(url, instrucciones)
        print(json.dumps(resultado, indent=2))
