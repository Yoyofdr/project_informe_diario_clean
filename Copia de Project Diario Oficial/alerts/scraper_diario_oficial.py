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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from alerts.services.cache_service import cache_service
from alerts.services.pdf_extractor import pdf_extractor
from alerts.services.metrics_service import metrics_collector, api_metrics
from alerts.utils.retry_utils import retry_requests, retry_selenium, retry_pdf_extraction
from alerts.utils.rate_limiter import rate_limiter, rate_limited
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php"

SECCIONES_VALIDAS = [
    "NORMAS GENERALES",
    "NORMAS PARTICULARES"
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

@retry_pdf_extraction()
def extraer_texto_pdf_mixto(url_pdf, titulo=""):
    """
    Extrae texto del PDF usando el servicio mejorado con múltiples métodos de fallback.
    Usa caché para evitar descargas repetidas y registra métricas.
    """
    if url_pdf.startswith('http'):
        url_completa = url_pdf
    else:
        url_completa = f"https://www.diariooficial.interior.gob.cl{url_pdf}"
    
    with metrics_collector.track_pdf_processing(url_completa, titulo) as pdf_metric:
        # Intentar obtener del caché primero
        pdf_content = cache_service.get_pdf_content(url_completa)
        desde_cache = bool(pdf_content)
        
        if not pdf_content:
            @retry_requests()
            @rate_limited
            def download_pdf(url):
                start_time = time.time()
                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
                download_time = time.time() - start_time
                return resp.content, download_time
            
            try:
                pdf_content, download_time = download_pdf(url_completa)
                # Guardar en caché para futuras consultas
                cache_service.set_pdf_content(url_completa, pdf_content)
                if pdf_metric:
                    pdf_metric.tiempo_descarga = download_time
            except Exception as e:
                logger.error(f"Error descargando PDF {url_completa}: {e}")
                raise
        
        # Registrar si vino del caché
        metrics_collector.record_pdf_download(0 if desde_cache else pdf_metric.tiempo_descarga, desde_cache)
        if pdf_metric:
            pdf_metric.desde_cache = desde_cache
        
        # Obtener información del PDF
        pdf_info = pdf_extractor.get_pdf_info(pdf_content)
        if pdf_metric:
            metrics_collector.record_pdf_info(pdf_metric, pdf_info['num_pages'], pdf_info['size_bytes'])
        
        # Extraer texto con el nuevo servicio
        start_time = time.time()
        texto, metodo = pdf_extractor.extract_text(pdf_content, max_pages=2)
        extraction_time = time.time() - start_time
        
        if pdf_metric:
            metrics_collector.record_pdf_extraction(pdf_metric, metodo, extraction_time)
        
        if not texto:
            logger.warning(f"No se pudo extraer texto del PDF: {url_completa}")
        
        return texto

@retry_requests()
def resumen_con_gemini(texto, titulo=None):
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or not texto or len(texto) < 40:
        print('[Gemini] No hay API key o el texto es muy corto.')
        return None
    
    with api_metrics.track_api_call('gemini', 'generate_content') as api_metric:
        try:
            # Aplicar rate limiting para Gemini API
            rate_limiter.acquire_for_url('https://api.gemini.google.com/v1/generate')
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = (
            "Eres un asistente experto en explicar normas oficiales en lenguaje simple. "
            "Resume en máximo 3 frases, en español claro y directo, el hecho principal y su consecuencia práctica. "
            "Si el texto menciona montos, cifras, fechas o nombres relevantes, inclúyelos en el resumen. "
            "No repitas el título ni el número de decreto, ni copies frases textuales del título. "
            "No cites normas, leyes, artículos ni uses frases como 'de acuerdo a', 'según', 'conforme a', 'establecido en', 'dispuesto en', 'n°', 'decreto', 'ley', 'artículo', 'constitución', 'reglamento', 'norma', 'regula', 'texto refundido'. "
            "Explica solo el hecho principal y su consecuencia. "
            "Ejemplo: 'Se sube el sueldo mínimo a $500.000 a partir de julio de 2025.'\n"
            f"Título: {titulo}\nTexto: {texto[:3000]}"
        )
        print('\n[Gemini] Texto enviado a Gemini:\n', texto[:1000], '\n---')
        response = model.generate_content(prompt)
        print('[Gemini] Respuesta cruda:', response.text)
        resumen = response.text.strip()
        frases = [f.strip() for f in resumen.split('.') if f.strip()]
        frases_filtradas = []
        for f in frases:
            if titulo and (f.lower().startswith(titulo.lower()) or f.lower() in titulo.lower()):
                continue
            if any(pal in f.lower() for pal in ["artículo", "constitución", "ley", "decreto", "n°", "según", "conforme a", "de acuerdo a", "de acuerdo con", "dispuesto en", "establecido en", "reglamento", "norma", "regula", "texto refundido"]):
                continue
            frases_filtradas.append(f)
        resumen = '. '.join(frases_filtradas[:3])
        if resumen and not resumen.endswith('.'):
            resumen += '.'
        return resumen
    except Exception as e:
        print('[Gemini] Error:', e)
    return None

@retry_requests()
def resumen_con_huggingface(texto, titulo=None):
    from dotenv import load_dotenv
    load_dotenv()
    api_token = os.environ.get('HF_API_TOKEN')
    if not api_token or not texto or len(texto) < 40:
        return None
    endpoint = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {api_token}"}
    prompt = (
        f"<|system|>\nEres un asistente experto en explicar normas oficiales en lenguaje simple. Resume en máximo 3 frases, en español claro y directo, el hecho principal y su consecuencia práctica. No repitas el título ni el número de decreto, ni copies frases textuales del título. No cites normas, leyes, artículos ni uses frases como 'de acuerdo a', 'según', 'conforme a', 'establecido en', 'dispuesto en', 'n°', 'decreto', 'ley', 'artículo', 'constitución', 'reglamento', 'norma', 'regula', 'texto refundido'. Explica solo el hecho principal y su consecuencia. Ejemplo: 'Se nombra a un nuevo representante en la Comisión Chilena del Cobre, quien participará en la toma de decisiones de la entidad.'\n<|user|>\nTítulo: {titulo}\nTexto: {texto[:3000]}\n<|assistant|>"
    )
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 80}}
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        resumen = None
        if isinstance(data, list) and len(data) > 0 and 'generated_text' in data[0]:
            resumen = data[0]['generated_text']
        elif isinstance(data, dict) and 'generated_text' in data:
            resumen = data['generated_text']
        if resumen:
            resumen = resumen.strip()
            if '<|assistant|>' in resumen:
                resumen = resumen.split('<|assistant|>')[-1].strip()
            # Filtrar repeticiones del título y referencias legales
            frases = [f.strip() for f in resumen.split('.') if f.strip()]
            frases_filtradas = []
            for f in frases:
                if titulo and (f.lower().startswith(titulo.lower()) or f.lower() in titulo.lower()):
                    continue
                if any(pal in f.lower() for pal in ["artículo", "constitución", "ley", "decreto", "n°", "según", "conforme a", "de acuerdo a", "de acuerdo con", "dispuesto en", "establecido en", "reglamento", "norma", "regula", "texto refundido"]):
                    continue
                frases_filtradas.append(f)
            resumen = '. '.join(frases_filtradas[:3])
            if resumen and not resumen.endswith('.'):
                resumen += '.'
            return resumen
    except Exception as e:
        print('[HF] Error:', e)
    return None

def generar_resumen_desde_texto(texto, titulo=None, pdf_metric=None):
    """Genera un resumen del texto usando IA y registra métricas"""
    if not texto or len(texto.strip()) < 40:
        return "No se pudo extraer el contenido del documento."
    
    start_time = time.time()
    resumen_ia = resumen_con_gemini(texto, titulo)
    analysis_time = time.time() - start_time
    
    if pdf_metric:
        metrics_collector.record_pdf_analysis(pdf_metric, analysis_time)
    
    if resumen_ia:
        return resumen_ia
    return "No se pudo generar un resumen relevante."

def extraer_valores_dolar_euro(texto):
    """
    Extrae el valor del dólar observado y del euro desde el texto del PDF del Banco Central.
    Retorna un dict: {'dolar': valor, 'euro': valor}
    """
    import re
    resultado = {'dolar': None, 'euro': None}
    # Buscar línea con DÓLAR OBSERVADO
    match_dolar = re.search(r'D[ÓO]LAR OBSERVADO\s*:?\s*\$?([\d\.\,]+)', texto, re.IGNORECASE)
    if match_dolar:
        resultado['dolar'] = match_dolar.group(1).replace('.', '').replace(',', '.')
    # Buscar línea con EURO
    match_euro = re.search(r'EURO\s*:?\s*\$?([\d\.\,]+)', texto, re.IGNORECASE)
    if match_euro:
        resultado['euro'] = match_euro.group(1).replace('.', '').replace(',', '.')
    return resultado

@retry_selenium()
def obtener_sumario_diario_oficial(fecha=None, force_refresh=False):
    """
    Scrapea el sumario del Diario Oficial para la fecha dada (formato dd-mm-aaaa).
    Retorna una lista de dicts con título, enlace al PDF, relevancia y resumen, solo de Normas Generales y Particulares, sin duplicados.
    Además, retorna los valores del dólar y euro si están disponibles.
    Usa caché para evitar scrapeos repetidos a menos que force_refresh=True.
    """
    if fecha is None:
        fecha = datetime.now().strftime("%d-%m-%Y")
    
    # Convertir fecha a formato datetime para el caché
    fecha_dt = datetime.strptime(fecha, "%d-%m-%Y")
    
    # Intentar obtener del caché si no es force_refresh
    if not force_refresh:
        cached_result = cache_service.get_scraping_result(fecha_dt)
        if cached_result:
            logger.info(f"Usando resultados del caché para fecha {fecha}")
            return cached_result
    
    # Iniciar registro de métricas
    metric = metrics_collector.start_scraping(fecha_dt.date())
    
    try:
        url = f"{BASE_URL}?date={fecha}"
        
        # Aplicar rate limiting antes de abrir el navegador
        rate_limiter.acquire_for_url(url)
        
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        with uc.Chrome(options=options) as driver:
        driver.get(url)
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
        except Exception as e:
            print("[Selenium] Advertencia: No se encontró tabla en el HTML renderizado.", e)
        html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    sumario = []
    vistos = set()
    seccion_actual = None
    valores_monedas = None
    for tag in soup.find_all(['b', 'strong', 'h3', 'h2', 'h1', 'td', 'th']):
        texto = tag.get_text(strip=True).upper()
        if texto in SECCIONES_VALIDAS:
            seccion_actual = texto
        elif seccion_actual in SECCIONES_VALIDAS:
            for link in tag.find_all_next("a", href=True):
                href = link["href"]
                if href.endswith(".pdf"):
                    parent = link.find_parent("tr") or link.find_parent("li") or link.parent
                    titulo = None
                    if parent:
                        titulo = parent.get_text(" ", strip=True)
                        titulo = re.sub(r"Ver PDF.*", "", titulo).strip()
                    if not titulo:
                        titulo = "(Sin título)"
                    clave = (titulo, href)
                    if clave in vistos:
                        continue
                    vistos.add(clave)
                    relevante = es_relevante(titulo)
                    incluir_moneda = (
                        seccion_actual == "NORMAS GENERALES" and (
                            "DÓLAR" in titulo.upper() or "EURO" in titulo.upper()
                        )
                    )
                    # Detectar el PDF de tipos de cambio y paridades
                    es_certificado_monedas = (
                        "TIPOS DE CAMBIO" in titulo.upper() and "PARIDADES DE MONEDAS EXTRANJERAS" in titulo.upper()
                    )
                    resumen = ""
                    # Registrar publicación
                    metrics_collector.add_publicacion(relevante or incluir_moneda)
                    
                    if relevante or incluir_moneda:
                        texto_pdf = extraer_texto_pdf_mixto(href, titulo)
                        resumen = generar_resumen_desde_texto(texto_pdf, titulo)
                        sumario.append({
                            "seccion": seccion_actual,
                            "titulo": titulo,
                            "url_pdf": href,
                            "relevante": relevante or incluir_moneda,
                            "resumen": resumen
                        })
                    # Si es el certificado de monedas, extraer valores
                    if es_certificado_monedas and valores_monedas is None:
                        texto_pdf = extraer_texto_pdf_mixto(href, titulo)
                        valores_monedas = extraer_valores_dolar_euro(texto_pdf)
                siguiente_texto = link.find_next(string=True)
                if siguiente_texto and siguiente_texto.strip().upper() in SECCIONES_VALIDAS:
                    break
        result = {"publicaciones": sumario, "valores_monedas": valores_monedas}
        
        # Guardar en caché si hay resultados
        if sumario:
            cache_service.set_scraping_result(fecha_dt, result)
            logger.info(f"Resultados guardados en caché para fecha {fecha}")
        
        # Finalizar métricas con éxito
        metrics_collector.end_scraping(exitoso=True)
        
        return result
        
    except Exception as e:
        # Registrar error en métricas
        metrics_collector.end_scraping(exitoso=False, mensaje_error=str(e))
        logger.error(f"Error en scraping: {str(e)}")
        raise 