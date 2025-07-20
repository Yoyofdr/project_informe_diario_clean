import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from io import BytesIO
from pdfminer.high_level import extract_text
from pdf2image import convert_from_bytes
import pytesseract
import PyPDF2
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from alerts.services.cache_service import cache_service
from alerts.services.pdf_extractor import PDFExtractor
from alerts.utils.rate_limiter import rate_limited
from alerts.utils.retry_utils import retry
from django.core.mail import send_mail

BASE_URL = "https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php"

SECCIONES_VALIDAS = [
    "NORMAS GENERALES",
    "NORMAS PARTICULARES",
    "Normas Generales",
    "Normas Particulares"
]

# Palabras clave estrictas para relevancia
PALABRAS_RELEVANTES = [
    "LEY", "DECRETO SUPREMO", "DECRETO CON FUERZA DE LEY", "RESOLUCIÓN GENERAL", "REGLAMENTO", "REFORMA CONSTITUCIONAL", "MODIFICACIÓN DE LEY", "POLÍTICA NACIONAL", "BENEFICIO NACIONAL", "OBLIGACIÓN GENERAL", "DERECHO GENERAL"
]
# Palabras clave para excluir explícitamente
PALABRAS_NO_RELEVANTES = [
    "DESIGNACIÓN", "NOMBRAMIENTO", "RENUNCIA", "ACEPTA", "CAMBIO DE PERSONA", "AUTORIZA", "PERMISO", "CONCESIÓN", "RECTIFICACIÓN", "MUNICIPALIDAD", "LOCALIDAD", "SECTOR", "NOTARIO", "OFICIAL DEL REGISTRO CIVIL", "EXTRACTO", "INDIVIDUAL", "PERSONAL", "PARTICULAR", "APLICA A", "APLICA EN", "DIRECTOR REGIONAL", "SECRETARÍA REGIONAL", "ZONA", "FUNCIONARIO", "FUNCIONARIA"
]

EXCEPCIONES_RELEVANTES = [
    "MINISTRO DEL INTERIOR", "MINISTRO DE HACIENDA", "PRESIDENTE DE LA REPÚBLICA", "VICEPRESIDENTE DE LA REPÚBLICA", "DIRECTOR NACIONAL", "SUBSECRETARIO DEL INTERIOR", "SUBSECRETARIA DEL INTERIOR"
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

# Palabras/frases clave para licitaciones públicas - EXPANDIDO
LICITACION_KEYWORDS = [
    'licitación pública',
    'llamado a licitación pública',
    'concurso público',
    'llamado a concurso',
    'bases de licitación',
    'licitación de obras',
    'licitación',
    'propuesta pública',
    'contratación pública',
    'proceso de licitación',
    'apertura de ofertas',
    'llamado público',
    'convocatoria pública',
]

def es_licitacion_publica(titulo):
    """Retorna True si el título contiene alguna frase clave de licitación pública."""
    t = titulo.lower()
    return any(kw in t for kw in LICITACION_KEYWORDS)

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
    """
    Extrae texto de un PDF usando caché y extractor robusto.
    """
    try:
        pdf_content = descargar_pdf_con_cache(url_pdf)
        if not pdf_content:
            print(f"[WARNING] No se pudo descargar el PDF: {url_pdf}")
            return ""
        
        texto, metodo = pdf_extractor.extract_text(pdf_content, max_pages=8)
        return texto
    except Exception as e:
        print(f"[WARNING] Error extrayendo texto del PDF {url_pdf}: {str(e)}")
        return ""

def resumen_con_gemini(texto, titulo=None):
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or not texto or len(texto) < 40:
        return None
    try:
        # Limitar el texto al primer párrafo relevante (hasta el primer salto doble de línea o 800 caracteres)
        primer_parrafo = texto.split('\n\n')[0]
        if len(primer_parrafo) < 40:
            primer_parrafo = texto[:1200]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            "Eres un asistente experto en explicar normas oficiales en lenguaje simple. "
            "Resume en máximo 4 frases, en español claro y directo, el hecho principal y su consecuencia práctica. "
            "Ignora frases de trámite, fechas, números de resolución, y fórmulas legales. "
            "No repitas el título ni el número de decreto, ni copies frases textuales del título. "
            "No cites normas, leyes, artículos ni uses frases como 'de acuerdo a', 'según', 'conforme a', 'establecido en', 'dispuesto en', 'n°', 'decreto', 'ley', 'artículo', 'constitución', 'reglamento', 'norma', 'regula', 'texto refundido'. "
            "Explica solo el hecho principal y su consecuencia práctica, como si se lo explicaras a un ciudadano común. "
            "Ejemplo: 'Se sube el sueldo mínimo a $500.000 a partir de julio de 2025.'\n"
            f"Título: {titulo}\nTexto: {primer_parrafo}"
        )
        response = model.generate_content(prompt)
        resumen = response.text.strip()
        frases = [f.strip() for f in resumen.split('.') if f.strip()]
        frases_filtradas = []
        for f in frases:
            if titulo and (f.lower().startswith(titulo.lower()) or f.lower() in titulo.lower()):
                continue
            if any(pal in f.lower() for pal in ["artículo", "constitución", "ley", "decreto", "n°", "según", "conforme a", "de acuerdo a", "de acuerdo con", "dispuesto en", "establecido en", "reglamento", "norma", "regula", "texto refundido"]):
                continue
            if len(f) < 30:
                continue
            frases_filtradas.append(f)
        resumen = '. '.join(frases_filtradas[:4])
        if resumen and not resumen.endswith('.'):
            resumen += '.'
        return resumen
    except Exception as e:
        pass
    return None

def generar_resumen_desde_texto(texto, titulo=None):
    resumen_ia = resumen_con_gemini(texto, titulo)
    if resumen_ia:
        return resumen_ia
    if not texto:
        return "No se pudo extraer el contenido del documento."
    return "No se pudo generar un resumen relevante."

def extraer_valores_dolar_euro(texto):
    """
    Extrae el valor del dólar observado (o DÓLAR EE.UU.) y del euro desde el texto del PDF del Banco Central.
    Retorna un dict: {'dolar': valor, 'euro': valor}
    """
    import re
    resultado = {'dolar': None, 'euro': None}
    # Buscar DÓLAR EE.UU. (formato tabla actual)
    match_dolar = re.search(r'D[ÓO]LAR\s*EE\.?UU\.?\s*\*?\s*([\d\.,]+)', texto, re.IGNORECASE)
    if not match_dolar:
        # Fallback: DÓLAR OBSERVADO (formato antiguo)
        match_dolar = re.search(r'D[ÓO]LAR OBSERVADO[\s\*]*:?\s*\$?([\d\.,]+)', texto, re.IGNORECASE)
    if match_dolar:
        resultado['dolar'] = match_dolar.group(1).replace('.', '').replace(',', '.')
    # Buscar EURO (formato tabla actual)
    match_euro = re.search(r'EURO\s*([\d\.,]+)', texto, re.IGNORECASE)
    if match_euro:
        resultado['euro'] = match_euro.group(1).replace('.', '').replace(',', '.')
    return resultado

def obtener_numero_edicion(fecha, driver=None):
    """
    Obtiene el número de edición para una fecha específica del Diario Oficial.
    """
    print(f"[EDITION] Buscando número de edición para fecha: {fecha}")
    
    # Primero intentar con caché local
    try:
        import json
        cache_file = os.path.join(os.path.dirname(__file__), '..', 'edition_cache.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache = json.load(f)
                if fecha in cache:
                    edition = cache[fecha]
                    print(f"[EDITION] Número de edición encontrado en caché: {edition}")
                    return edition
    except Exception as e:
        print(f"[EDITION] Error leyendo caché: {e}")
    
    # Si no está en caché, intentar con estimación
    # El número de edición parece incrementar diariamente
    base_date = datetime.strptime("07-07-2025", "%d-%m-%Y")
    base_edition = 44192
    
    try:
        target_date = datetime.strptime(fecha, "%d-%m-%Y")
        days_diff = (target_date - base_date).days
        estimated_edition = base_edition + days_diff
        print(f"[EDITION] Usando edición estimada: {estimated_edition}")
        return str(estimated_edition)
    except:
        pass
    
    # Como último recurso, intentar con Selenium
    try:
        # Si no se proporciona driver, crear uno temporal
        driver_temporal = False
        if driver is None:
            driver_temporal = True
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(30)
        
        # Navegar a la página de selección de edición
        url_select = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/select_edition.php?date={fecha}"
        print(f"[EDITION] Navegando a: {url_select}")
        driver.get(url_select)
        time.sleep(3)
        
        # Buscar enlaces con edition parameter
        links = driver.find_elements(By.TAG_NAME, 'a')
        print(f"[EDITION] Enlaces encontrados: {len(links)}")
        
        editions_found = []
        for link in links:
            href = link.get_attribute('href')
            if href and 'edition=' in href and 'index.php' in href:
                # Extraer el número de edición (ahora acepta letras también)
                import re
                match = re.search(r'edition=([0-9]+(?:-[A-Z])?)', href)
                if match:
                    edition = match.group(1)
                    editions_found.append(edition)
                    print(f"[EDITION] Edición encontrada: {edition} - URL: {href}")
        
        if editions_found:
            # Usar la primera edición encontrada (generalmente solo hay una)
            edition = editions_found[0]
            print(f"[EDITION] Usando edición: {edition}")
            if driver_temporal:
                driver.quit()
            return edition
        
        print("[EDITION] No se encontraron enlaces con número de edición")
        if driver_temporal:
            driver.quit()
        return ""
        
    except Exception as e:
        print(f"[EDITION] Error obteniendo número de edición: {str(e)}")
        if driver_temporal and driver:
            try:
                driver.quit()
            except:
                pass
        return ""

def procesar_todas_las_publicaciones(soup, seccion_actual=None):
    """
    Procesa TODAS las publicaciones de una página, detectando especialmente licitaciones.
    """
    publicaciones = []
    
    # Buscar todas las filas de contenido
    for tr in soup.find_all('tr', class_='content'):
        tds = tr.find_all('td')
        if len(tds) >= 2:
            titulo = tds[0].get_text(strip=True)
            # Limpiar el título
            titulo = re.sub(r"Ver PDF.*", "", titulo).strip()
            titulo = titulo.replace(' <span class="border dotted"></span>', '').strip()
            
            link_tag = tds[1].find('a', href=True)
            if link_tag and link_tag['href'].endswith('.pdf'):
                href = link_tag['href']
                
                # IMPORTANTE: Siempre incluir si es licitación pública
                if es_licitacion_publica(titulo):
                    print(f"[LICITACIÓN DETECTADA] {titulo}")
                    publicaciones.append({
                        "seccion": seccion_actual or "NORMAS GENERALES",
                        "titulo": titulo,
                        "url_pdf": href,
                        "relevante": True,  # Las licitaciones siempre son relevantes
                        "es_licitacion": True,
                        "resumen": ""
                    })
                else:
                    # Para otras publicaciones, aplicar filtro de relevancia normal
                    relevante = es_relevante(titulo)
                    publicaciones.append({
                        "seccion": seccion_actual or "NORMAS GENERALES",
                        "titulo": titulo,
                        "url_pdf": href,
                        "relevante": relevante,
                        "es_licitacion": False,
                        "resumen": ""
                    })
    
    return publicaciones

def obtener_html_con_reintentos(url, max_intentos=3):
    """
    Intenta obtener el HTML de una URL con varios métodos de fallback.
    """
    # Método 1: Requests simple
    for intento in range(max_intentos):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            if len(response.text) > 1000:
                return response.text
        except Exception as e:
            print(f"[REQUESTS] Intento {intento + 1} falló: {str(e)[:100]}")
    
    # Método 2: Selenium con Chrome normal
    try:
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        driver.quit()
        
        if len(html) > 1000:
            return html
    except Exception as e:
        print(f"[SELENIUM] Error: {str(e)[:100]}")
    
    # Método 3: Undetected Chrome
    try:
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = uc.Chrome(options=options)
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        driver.quit()
        
        if len(html) > 1000:
            return html
    except Exception as e:
        print(f"[UC] Error: {str(e)[:100]}")
    
    return None

def obtener_sumario_diario_oficial(fecha=None, force_refresh=False):
    """
    Scrapea el sumario del Diario Oficial para la fecha dada (formato dd-mm-aaaa).
    Retorna una lista de dicts con título, enlace al PDF, relevancia y resumen.
    SIEMPRE incluye llamados a licitación pública.
    """
    from datetime import datetime as dt
    
    # Inicializar variables por defecto
    resultado_default = {"publicaciones": [], "valores_monedas": None, "total_documentos": 0}
    
    try:
        if fecha is None:
            fecha = datetime.now().strftime("%d-%m-%Y")
        fecha_cache = dt.strptime(fecha, "%d-%m-%Y")
        
        # --- CACHÉ RESULTADO FINAL ---
        if not force_refresh:
            resultado_cache = cache_service.get_scraping_result(fecha_cache)
            if resultado_cache and isinstance(resultado_cache, dict) and 'publicaciones' in resultado_cache:
                print(f"[CACHE] Usando resultado final del scraping desde caché para {fecha}")
                return resultado_cache
        
        # Obtener número de edición
        edition = obtener_numero_edicion(fecha)
        if not edition:
            print(f"[INFO] No se pudo obtener número de edición para {fecha}, usando valor vacío")
            edition = ""
        else:
            print(f"[INFO] Número de edición obtenido: {edition}")
        
        # Lista de todas las publicaciones encontradas
        todas_publicaciones = []
        vistos = set()  # Para evitar duplicados
        valores_monedas = None
        total_documentos = 0
        
        # Secciones a procesar
        secciones = [
            ("index.php", "NORMAS GENERALES"),
            ("normas_particulares.php", "NORMAS PARTICULARES"),
            ("avisos_destacados.php", "AVISOS DESTACADOS")
        ]
        
        for archivo, nombre_seccion in secciones:
            try:
                if archivo == "index.php":
                    url = f"{BASE_URL}?date={fecha}&edition={edition}&v=1"
                else:
                    url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/{archivo}?date={fecha}&edition={edition}&v=1"
                
                print(f"\n[PROCESANDO] {nombre_seccion} - {url}")
                
                # Obtener HTML
                html = obtener_html_con_reintentos(url)
                if not html:
                    print(f"[WARNING] No se pudo obtener HTML para {nombre_seccion}")
                    continue
                
                soup = BeautifulSoup(html, "html.parser")
                
                # Procesar todas las publicaciones de esta sección
                publicaciones_seccion = procesar_todas_las_publicaciones(soup, nombre_seccion)
                
                # Agregar publicaciones únicas
                for pub in publicaciones_seccion:
                    clave = (pub['titulo'], pub['url_pdf'])
                    if clave not in vistos:
                        vistos.add(clave)
                        todas_publicaciones.append(pub)
                        total_documentos += 1
                        
                        # Si es certificado de monedas, extraer valores
                        if "TIPOS DE CAMBIO" in pub['titulo'].upper() and "PARIDADES DE MONEDAS EXTRANJERAS" in pub['titulo'].upper():
                            texto_pdf = extraer_texto_pdf_mixto(pub['url_pdf'])
                            valores_monedas = extraer_valores_dolar_euro(texto_pdf)
                
                print(f"[INFO] Encontradas {len(publicaciones_seccion)} publicaciones en {nombre_seccion}")
                
            except Exception as e:
                print(f"[ERROR] Error procesando {nombre_seccion}: {str(e)}")
        
        # Separar licitaciones del resto
        licitaciones = [p for p in todas_publicaciones if p.get('es_licitacion', False)]
        otras_relevantes = [p for p in todas_publicaciones if p['relevante'] and not p.get('es_licitacion', False)]
        no_relevantes = [p for p in todas_publicaciones if not p['relevante'] and not p.get('es_licitacion', False)]
        
        print(f"\n[RESUMEN] Total documentos: {total_documentos}")
        print(f"[RESUMEN] Licitaciones encontradas: {len(licitaciones)}")
        print(f"[RESUMEN] Otras relevantes: {len(otras_relevantes)}")
        print(f"[RESUMEN] No relevantes: {len(no_relevantes)}")
        
        # Construir lista final priorizando licitaciones
        publicaciones_finales = []
        
        # 1. SIEMPRE incluir TODAS las licitaciones
        for lic in licitaciones:
            texto_pdf = extraer_texto_pdf_mixto(lic['url_pdf'])
            lic['resumen'] = generar_resumen_desde_texto(texto_pdf, lic['titulo'])
            publicaciones_finales.append(lic)
        
        # 2. Incluir otras publicaciones relevantes
        for pub in otras_relevantes:
            texto_pdf = extraer_texto_pdf_mixto(pub['url_pdf'])
            pub['resumen'] = generar_resumen_desde_texto(texto_pdf, pub['titulo'])
            publicaciones_finales.append(pub)
        
        # 3. Si no hay publicaciones, incluir al menos una no relevante
        if not publicaciones_finales and no_relevantes:
            # Buscar una con palabras clave
            PALABRAS_CLAVE = [
                "decreto", "resolución", "plan", "cambio", "beneficio", "subsidio", 
                "proyecto", "programa", "tarifa", "reforma", "ley", "reglamento", 
                "asignación", "nombramiento", "prórroga", "modificación"
            ]
            
            seleccionada = None
            for pub in no_relevantes:
                if any(pal in pub['titulo'].lower() for pal in PALABRAS_CLAVE):
                    seleccionada = pub
                    break
            
            if not seleccionada:
                seleccionada = no_relevantes[0]
            
            texto_pdf = extraer_texto_pdf_mixto(seleccionada['url_pdf'])
            seleccionada['resumen'] = generar_resumen_desde_texto(texto_pdf, seleccionada['titulo'])
            publicaciones_finales.append(seleccionada)
        
        resultado = {
            "publicaciones": publicaciones_finales, 
            "valores_monedas": valores_monedas, 
            "total_documentos": total_documentos
        }
        
        # Guardar en caché
        cache_service.set_scraping_result(fecha_cache, resultado)
        
        return resultado
        
    except Exception as e:
        print(f"[ERROR GENERAL] {str(e)}")
        send_mail(
            subject='[ALERTA] Error general en scraping Diario Oficial',
            message=f'No se pudo procesar la edición del Diario Oficial para la fecha {fecha}.\nError: {str(e)}',
            from_email='rodrigo@carvuk.com',
            recipient_list=['soporte@informediario.cl'],  # SOLO INTERNO
            fail_silently=True
        )
        return resultado_default