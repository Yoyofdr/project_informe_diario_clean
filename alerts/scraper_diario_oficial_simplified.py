"""
Versión simplificada del scraper del Diario Oficial
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
from alerts.scraper_diario_oficial import (
    BASE_URL, SECCIONES_VALIDAS, es_relevante,
    extraer_texto_pdf_mixto, generar_resumen_desde_texto,
    extraer_valores_dolar_euro
)

def obtener_sumario_diario_oficial_simple(fecha=None):
    """
    Versión simplificada que intenta primero con requests directo
    """
    if fecha is None:
        fecha = datetime.now().strftime("%d-%m-%Y")
    
    print(f"[SCRAPER SIMPLE] Intentando obtener sumario para {fecha}")
    
    # URL con parámetros específicos
    url = f"{BASE_URL}?date={fecha}&edition=&v=1"
    
    # Intentar con requests primero (más rápido)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Referer': 'https://www.diariooficial.interior.gob.cl/'
    }
    
    try:
        print("[SCRAPER SIMPLE] Intentando con requests...")
        session = requests.Session()
        
        # Primera visita para obtener cookies
        session.get("https://www.diariooficial.interior.gob.cl/", headers=headers, timeout=10)
        time.sleep(1)
        
        # Segunda visita con la fecha
        response = session.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            html = response.text
            print(f"[SCRAPER SIMPLE] HTML obtenido: {len(html)} caracteres")
            
            # Si el HTML es muy corto o es una página de redirección, usar Selenium
            if len(html) < 10000 or "NORMAS" not in html.upper():
                print("[SCRAPER SIMPLE] HTML no válido, usando Selenium...")
                return obtener_con_selenium_simple(fecha, url)
            
            # Procesar el HTML
            return procesar_html_simple(html, fecha)
            
    except Exception as e:
        print(f"[SCRAPER SIMPLE] Error con requests: {e}")
        return obtener_con_selenium_simple(fecha, url)

def obtener_con_selenium_simple(fecha, url):
    """Fallback con Selenium básico"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        print("[SELENIUM SIMPLE] Intentando con Selenium estándar...")
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)
        
        try:
            driver.get(url)
            
            # Esperar un poco
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(5)
            
            html = driver.page_source
            print(f"[SELENIUM SIMPLE] HTML obtenido: {len(html)} caracteres")
            
            return procesar_html_simple(html, fecha)
            
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"[SELENIUM SIMPLE] Error: {e}")
        return {"publicaciones": [], "valores_monedas": None, "total_documentos": 0}

def procesar_html_simple(html, fecha):
    """Procesa el HTML de forma simplificada"""
    soup = BeautifulSoup(html, "html.parser")
    publicaciones = []
    valores_monedas = None
    total_documentos = 0
    
    # Buscar todos los enlaces PDF
    pdfs = soup.find_all("a", href=lambda x: x and x.endswith(".pdf"))
    print(f"[PARSER] Encontrados {len(pdfs)} PDFs")
    
    for pdf_link in pdfs[:10]:  # Limitar a los primeros 10 para prueba
        href = pdf_link.get("href", "")
        if not href:
            continue
            
        total_documentos += 1
        
        # Obtener texto cercano como título
        parent = pdf_link.find_parent("tr") or pdf_link.find_parent("td") or pdf_link.parent
        titulo = ""
        if parent:
            titulo = parent.get_text(strip=True)
            # Limpiar el título
            titulo = re.sub(r"Ver PDF.*", "", titulo).strip()
            titulo = re.sub(r"\s+", " ", titulo).strip()
        
        if not titulo:
            titulo = "Documento sin título"
        
        # Para prueba rápida, incluir algunos documentos
        if total_documentos <= 3:
            publicaciones.append({
                "seccion": "NORMAS GENERALES",
                "titulo": titulo[:200],  # Limitar longitud
                "url_pdf": href,
                "relevante": True,
                "resumen": "Documento del Diario Oficial"
            })
        
        # Buscar valores de monedas
        if "TIPOS DE CAMBIO" in titulo.upper() or "MONEDAS" in titulo.upper():
            try:
                texto_pdf = extraer_texto_pdf_mixto(href)
                valores_monedas = extraer_valores_dolar_euro(texto_pdf)
            except:
                pass
    
    print(f"[PARSER] Total documentos: {total_documentos}")
    print(f"[PARSER] Publicaciones incluidas: {len(publicaciones)}")
    
    return {
        "publicaciones": publicaciones,
        "valores_monedas": valores_monedas,
        "total_documentos": total_documentos
    }