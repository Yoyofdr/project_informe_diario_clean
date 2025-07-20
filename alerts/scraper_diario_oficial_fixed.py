"""
Versión corregida del scraper del Diario Oficial
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os
import time
import json
from alerts.services.cache_service import cache_service
from alerts.services.pdf_extractor import PDFExtractor
from alerts.utils.rate_limiter import rate_limited
from alerts.utils.retry_utils import retry
from django.core.mail import send_mail

BASE_URL = "https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php"

SECCIONES_VALIDAS = [
    "NORMAS GENERALES",
    "NORMAS PARTICULARES"
]

# Palabras clave estrictas para relevancia
PALABRAS_RELEVANTES = [
    "LEY", "DECRETO SUPREMO", "DECRETO CON FUERZA DE LEY", "RESOLUCIÓN GENERAL", 
    "REGLAMENTO", "REFORMA CONSTITUCIONAL", "MODIFICACIÓN DE LEY", "POLÍTICA NACIONAL", 
    "BENEFICIO NACIONAL", "OBLIGACIÓN GENERAL", "DERECHO GENERAL"
]

# Palabras clave para excluir explícitamente
PALABRAS_NO_RELEVANTES = [
    "DESIGNACIÓN", "NOMBRAMIENTO", "RENUNCIA", "ACEPTA", "CAMBIO DE PERSONA", 
    "AUTORIZA", "PERMISO", "CONCESIÓN", "RECTIFICACIÓN", "MUNICIPALIDAD", 
    "LOCALIDAD", "SECTOR", "NOTARIO", "OFICIAL DEL REGISTRO CIVIL", "EXTRACTO", 
    "INDIVIDUAL", "PERSONAL", "PARTICULAR", "APLICA A", "APLICA EN", 
    "DIRECTOR REGIONAL", "SECRETARÍA REGIONAL", "ZONA", "FUNCIONARIO", "FUNCIONARIA"
]

EXCEPCIONES_RELEVANTES = [
    "MINISTRO DEL INTERIOR", "MINISTRO DE HACIENDA", "PRESIDENTE DE LA REPÚBLICA", 
    "VICEPRESIDENTE DE LA REPÚBLICA", "DIRECTOR NACIONAL", "SUBSECRETARIO DEL INTERIOR", 
    "SUBSECRETARIA DEL INTERIOR"
]

def es_relevante(texto):
    texto_up = texto.upper()
    # Solo relevante si contiene palabra relevante y NO contiene palabra no relevante
    if any(pal in texto_up for pal in PALABRAS_RELEVANTES):
        if not any(pal in texto_up for pal in PALABRAS_NO_RELEVANTES):
            return True
    # Excepción: cargos nacionales de alto nivel
    if any(exc in texto_up for exc in EXCEPCIONES_RELEVANTES):
        return True
    return False

pdf_extractor = PDFExtractor()

@rate_limited
@retry(max_retries=3, backoff_factor=2)
def descargar_pdf_con_cache(url_pdf):
    """Descarga un PDF usando caché y rate limiting"""
    if url_pdf.startswith('http'):
        url_completa = url_pdf
    else:
        url_completa = f"https://www.diariooficial.interior.gob.cl{url_pdf}"
    # Intentar obtener del caché
    content = cache_service.get_pdf_content(url_completa)
    if content:
        return content
    # Descargar y guardar en caché
    resp = requests.get(url_completa, timeout=20)
    resp.raise_for_status()
    cache_service.set_pdf_content(url_completa, resp.content)
    return resp.content

def extraer_texto_pdf_mixto(url_pdf):
    """Extrae texto de un PDF usando caché y extractor robusto."""
    try:
        pdf_content = descargar_pdf_con_cache(url_pdf)
        if not pdf_content:
            print(f"[WARNING] No se pudo descargar el PDF: {url_pdf}")
            return ""
        
        texto, metodo = pdf_extractor.extract_text(pdf_content, max_pages=2)
        return texto
    except Exception as e:
        print(f"[WARNING] Error extrayendo texto del PDF {url_pdf}: {str(e)}")
        return ""

def generar_resumen_desde_texto(texto, titulo=None):
    """Genera un resumen simple del texto"""
    if not texto:
        return "No se pudo extraer el contenido del documento."
    
    # Por ahora, retornar un resumen genérico
    # En producción, aquí iría la lógica de IA
    return "Documento del Diario Oficial que requiere revisión detallada."

def extraer_valores_dolar_euro(texto):
    """Extrae el valor del dólar observado y del euro desde el texto del PDF"""
    import re
    resultado = {'dolar': None, 'euro': None}
    
    # Buscar DÓLAR
    match_dolar = re.search(r'D[ÓO]LAR\s*EE\.?UU\.?\s*\*?\s*([\d\.,]+)', texto, re.IGNORECASE)
    if not match_dolar:
        match_dolar = re.search(r'D[ÓO]LAR OBSERVADO[\s\*]*:?\s*\$?([\d\.,]+)', texto, re.IGNORECASE)
    if match_dolar:
        resultado['dolar'] = match_dolar.group(1).replace('.', '').replace(',', '.')
    
    # Buscar EURO
    match_euro = re.search(r'EURO\s*([\d\.,]+)', texto, re.IGNORECASE)
    if match_euro:
        resultado['euro'] = match_euro.group(1).replace('.', '').replace(',', '.')
    
    return resultado

def obtener_numero_edicion_simple(fecha):
    """Obtiene el número de edición de forma simple y eficiente"""
    
    # Caché de ediciones conocidas
    EDITION_CACHE = {
        "11-07-2025": "44196",
        "10-07-2025": "44195",
        "09-07-2025": "44194",
        "08-07-2025": "44193",
        "07-07-2025": "44192",
        "12-07-2025": "44197",
        "13-07-2025": "44198",
        "14-07-2025": "44199",
        "15-07-2025": "44200"
    }
    
    # Primero buscar en caché
    if fecha in EDITION_CACHE:
        return EDITION_CACHE[fecha]
    
    # Si no está en caché, estimar
    try:
        from datetime import datetime as dt
        base_date = dt.strptime("07-07-2025", "%d-%m-%Y")
        base_edition = 44192
        
        target_date = dt.strptime(fecha, "%d-%m-%Y")
        days_diff = (target_date - base_date).days
        
        # Las ediciones incrementan aproximadamente 1 por día hábil
        # Asumiendo 5 días hábiles por semana
        estimated_edition = base_edition + days_diff
        
        return str(estimated_edition)
    except:
        return ""

def obtener_sumario_diario_oficial(fecha=None):
    """
    Versión simplificada y optimizada del scraper
    """
    from datetime import datetime as dt
    
    # Inicializar variables
    html = None
    resultado_default = {"publicaciones": [], "valores_monedas": None, "total_documentos": 0}
    
    try:
        if fecha is None:
            fecha = datetime.now().strftime("%d-%m-%Y")
        
        fecha_cache = dt.strptime(fecha, "%d-%m-%Y")
        
        # Verificar caché
        resultado_cache = cache_service.get_scraping_result(fecha_cache)
        if resultado_cache and isinstance(resultado_cache, dict) and 'publicaciones' in resultado_cache:
            print(f"[CACHE] Usando resultado desde caché para {fecha}")
            return resultado_cache
        
        # Obtener número de edición
        edition = obtener_numero_edicion_simple(fecha)
        print(f"[INFO] Usando edición: {edition}")
        
        # Construir URL
        url = f"{BASE_URL}?date={fecha}&edition={edition}&v=1"
        print(f"[INFO] URL: {url}")
        
        # Intentar obtener HTML con requests primero (más rápido)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.9'
            }
            
            session = requests.Session()
            # Visitar primero la página de selección
            select_url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/select_edition.php?date={fecha}"
            session.get(select_url, headers=headers, timeout=10)
            time.sleep(1)
            
            # Luego la página principal
            response = session.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200 and len(response.text) > 10000:
                html = response.text
                print("[INFO] HTML obtenido con requests")
        except Exception as e:
            print(f"[WARNING] Requests falló: {e}")
        
        # Si no tenemos HTML válido, usar Selenium
        if not html or "NORMAS" not in html.upper():
            print("[INFO] Intentando con Selenium...")
            html = obtener_html_con_selenium_simple(url)
        
        # Procesar HTML
        if html and len(html) > 1000:
            resultado = procesar_html_diario(html, fecha_cache)
            # Guardar en caché
            cache_service.set_scraping_result(fecha_cache, resultado)
            return resultado
        else:
            print("[ERROR] No se pudo obtener HTML válido")
            return resultado_default
            
    except Exception as e:
        print(f"[ERROR] Error general: {str(e)}")
        # Enviar alerta solo interno
        try:
            send_mail(
                subject='[ALERTA] Error en scraping Diario Oficial',
                message=f'Error procesando fecha {fecha}: {str(e)}',
                from_email='rodrigo@carvuk.com',
                recipient_list=['soporte@informediario.cl'],
                fail_silently=True
            )
        except:
            pass
        return resultado_default

def obtener_html_con_selenium_simple(url):
    """Versión simplificada de Selenium"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        # Deshabilitar imágenes para acelerar
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)
        
        try:
            driver.get(url)
            # Esperar mínimo necesario
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(3)
            
            html = driver.page_source
            return html
            
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"[ERROR] Selenium falló: {str(e)}")
        return None

def procesar_html_diario(html, fecha_cache):
    """Procesa el HTML del Diario Oficial"""
    soup = BeautifulSoup(html, "html.parser")
    sumario = []
    vistos = set()
    seccion_actual = None
    valores_monedas = None
    total_documentos = 0
    no_relevantes = []
    
    # Buscar secciones y PDFs
    for tag in soup.find_all(['b', 'strong', 'h3', 'h2', 'h1', 'td', 'th']):
        texto = tag.get_text(strip=True).upper()
        
        if texto in SECCIONES_VALIDAS:
            seccion_actual = texto
            
        elif seccion_actual in SECCIONES_VALIDAS:
            # Buscar PDFs en esta sección
            for link in tag.find_all_next("a", href=True):
                href = link["href"]
                
                if href.endswith(".pdf"):
                    total_documentos += 1
                    
                    # Obtener título
                    parent = link.find_parent("tr") or link.find_parent("li") or link.parent
                    titulo = ""
                    if parent:
                        titulo = parent.get_text(" ", strip=True)
                        titulo = re.sub(r"Ver PDF.*", "", titulo).strip()
                    
                    if not titulo:
                        titulo = "(Sin título)"
                    
                    # Evitar duplicados
                    clave = (titulo, href)
                    if clave in vistos:
                        continue
                    vistos.add(clave)
                    
                    # Verificar relevancia
                    relevante = es_relevante(titulo)
                    
                    # Procesar solo los primeros PDFs para evitar timeout
                    if len(sumario) < 10:
                        if relevante:
                            texto_pdf = extraer_texto_pdf_mixto(href)
                            resumen = generar_resumen_desde_texto(texto_pdf, titulo)
                            
                            sumario.append({
                                "seccion": seccion_actual,
                                "titulo": titulo,
                                "url_pdf": href,
                                "relevante": True,
                                "resumen": resumen
                            })
                        else:
                            no_relevantes.append({
                                "seccion": seccion_actual,
                                "titulo": titulo,
                                "url_pdf": href,
                                "relevante": False,
                                "resumen": "Documento no relevante"
                            })
                    
                    # Buscar monedas
                    if "TIPOS DE CAMBIO" in titulo.upper() and valores_monedas is None:
                        try:
                            texto_pdf = extraer_texto_pdf_mixto(href)
                            valores_monedas = extraer_valores_dolar_euro(texto_pdf)
                        except:
                            pass
                
                # Verificar si cambiamos de sección
                siguiente = link.find_next(string=True)
                if siguiente and siguiente.strip().upper() in SECCIONES_VALIDAS:
                    break
    
    # Si no hay relevantes, incluir algunos no relevantes
    if not sumario and no_relevantes:
        sumario = no_relevantes[:3]
    
    print(f"[INFO] Procesamiento completado: {total_documentos} documentos, {len(sumario)} relevantes")
    
    return {
        "publicaciones": sumario,
        "valores_monedas": valores_monedas,
        "total_documentos": total_documentos
    }