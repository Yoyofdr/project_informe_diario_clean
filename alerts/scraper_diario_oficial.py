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
        texto, metodo = pdf_extractor.extract_text(pdf_content, max_pages=2)
        print(f"[ExtractorRobusto] Método: {metodo}, Texto extraído: {texto[:500]}")
        return texto
    except Exception as e:
        print("[EXTRAER PDF] Error general:", e)
        return ""

def resumen_con_gemini(texto, titulo=None):
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or not texto or len(texto) < 40:
        print('[Gemini] No hay API key o el texto es muy corto.')
        return None
    try:
        # Limitar el texto al primer párrafo relevante (hasta el primer salto doble de línea o 800 caracteres)
        primer_parrafo = texto.split('\n\n')[0]
        if len(primer_parrafo) < 40:
            primer_parrafo = texto[:800]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            "Eres un asistente experto en explicar normas oficiales en lenguaje simple. "
            "Resume en máximo 2 frases, en español claro y directo, el hecho principal y su consecuencia práctica. "
            "Ignora frases de trámite, fechas, números de resolución, y fórmulas legales. "
            "No repitas el título ni el número de decreto, ni copies frases textuales del título. "
            "No cites normas, leyes, artículos ni uses frases como 'de acuerdo a', 'según', 'conforme a', 'establecido en', 'dispuesto en', 'n°', 'decreto', 'ley', 'artículo', 'constitución', 'reglamento', 'norma', 'regula', 'texto refundido'. "
            "Explica solo el hecho principal y su consecuencia práctica, como si se lo explicaras a un ciudadano común. "
            "Ejemplo: 'Se sube el sueldo mínimo a $500.000 a partir de julio de 2025.'\n"
            f"Título: {titulo}\nTexto: {primer_parrafo}"
        )
        print('\n[Gemini] Texto enviado a Gemini:\n', primer_parrafo[:1000], '\n---')
        response = model.generate_content(prompt)
        print('[Gemini] Respuesta cruda:', response.text)
        resumen = response.text.strip()
        frases = [f.strip() for f in resumen.split('.') if f.strip()]
        frases_filtradas = []
        for f in frases:
            if titulo and (f.lower().startswith(titulo.lower()) or f.lower() in titulo.lower()):
                continue
            if any(pal in f.lower() for pal in ["artículo", "constitución", "ley", "decreto", "n°", "según", "conforme a", "de acuerdo a", "de acuerdo con", "dispuesto en", "establecido en", "reglamento", "norma", "regula", "texto refundido", "resuelve", "a contar de", "a partir de", "vigente desde", "publicado en"]):
                continue
            if len(f) < 30:
                continue
            frases_filtradas.append(f)
        resumen = '. '.join(frases_filtradas[:2])
        if resumen and not resumen.endswith('.'):
            resumen += '.'
        return resumen
    except Exception as e:
        print('[Gemini] Error:', e)
    return None

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
    print("\n--- TEXTO EXTRAÍDO DEL PDF PARA MONEDAS ---\n")
    print(texto)
    print("\n--- FIN DEL TEXTO EXTRAÍDO ---\n")
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
    print("[DEBUG] Resultado extracción monedas:", resultado)
    return resultado

def obtener_sumario_diario_oficial(fecha=None):
    """
    Scrapea el sumario del Diario Oficial para la fecha dada (formato dd-mm-aaaa).
    Retorna una lista de dicts con título, enlace al PDF, relevancia y resumen, solo de Normas Generales y Particulares, sin duplicados.
    Además, retorna los valores del dólar y euro si están disponibles.
    """
    try:
        if fecha is None:
            fecha = datetime.now().strftime("%d-%m-%Y")
        # Para la fecha 07-07-2025, edition es 44192
        edition = "44192" if fecha == "07-07-2025" else ""
        url = f"{BASE_URL}?date={fecha}&edition={edition}&v=1"
        print(f"[DEBUG] Usando Selenium para obtener el HTML: {url}")
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
            print("\n[DEBUG] HTML OBTENIDO DEL SUMARIO (selenium):\n")
            print(html[:2000])
            print("\n[DEBUG] FIN HTML OBTENIDO (selenium)\n")
        soup = BeautifulSoup(html, "html.parser")
        sumario = []
        vistos = set()
        seccion_actual = None
        valores_monedas = None
        total_documentos = 0
        # Guardar también las no relevantes para el fallback
        no_relevantes = []
        for tag in soup.find_all(['b', 'strong', 'h3', 'h2', 'h1', 'td', 'th']):
            texto = tag.get_text(strip=True).upper()
            if texto in SECCIONES_VALIDAS:
                seccion_actual = texto
            elif seccion_actual in SECCIONES_VALIDAS:
                for link in tag.find_all_next("a", href=True):
                    href = link["href"]
                    if href.endswith(".pdf"):
                        total_documentos += 1
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
                        es_certificado_monedas = (
                            "TIPOS DE CAMBIO" in titulo.upper() and "PARIDADES DE MONEDAS EXTRANJERAS" in titulo.upper()
                        )
                        # Forzar procesamiento del PDF de monedas aunque no sea relevante
                        if es_certificado_monedas and valores_monedas is None:
                            print(f"[DEBUG] Procesando PDF de monedas: {titulo} -> {href}")
                            texto_pdf = extraer_texto_pdf_mixto(href)
                            valores_monedas = extraer_valores_dolar_euro(texto_pdf)
                        if relevante or incluir_moneda:
                            texto_pdf = extraer_texto_pdf_mixto(href)
                            resumen = generar_resumen_desde_texto(texto_pdf, titulo)
                            sumario.append({
                                "seccion": seccion_actual,
                                "titulo": titulo,
                                "url_pdf": href,
                                "relevante": relevante or incluir_moneda,
                                "resumen": resumen
                            })
                        else:
                            texto_pdf = extraer_texto_pdf_mixto(href)
                            resumen = generar_resumen_desde_texto(texto_pdf, titulo)
                            no_relevantes.append({
                                "seccion": seccion_actual,
                                "titulo": titulo,
                                "url_pdf": href,
                                "relevante": False,
                                "resumen": resumen
                            })
                    siguiente_texto = link.find_next(string=True)
                    if siguiente_texto and siguiente_texto.strip().upper() in SECCIONES_VALIDAS:
                        break
        # Si no hay relevantes, incluir la no relevante con palabra clave relevante
        PALABRAS_CLAVE = [
            "decreto", "resolución", "plan", "cambio", "beneficio", "subsidio", "proyecto", "programa", "tarifa", "reforma", "ley", "reglamento", "asignación", "nombramiento", "prórroga", "modificación"
        ]
        seleccionada = None
        if not sumario and no_relevantes:
            for pub in no_relevantes:
                texto_busqueda = (pub["titulo"] + " " + pub["resumen"]).lower()
                if any(pal in texto_busqueda for pal in PALABRAS_CLAVE):
                    seleccionada = pub
                    break
            if not seleccionada:
                seleccionada = no_relevantes[0]
            sumario.append(seleccionada)
        return {"publicaciones": sumario, "valores_monedas": valores_monedas, "total_documentos": total_documentos}
    except Exception as e:
        # Enviar alerta solo a soporte interno, nunca a clientes
        send_mail(
            subject='[ALERTA] Error general en scraping Diario Oficial',
            message=f'No se pudo procesar la edición del Diario Oficial para la fecha {fecha}.\nError: {str(e)}',
            from_email='rodrigo@carvuk.com',
            recipient_list=['soporte@informediario.cl'],  # SOLO INTERNO
            fail_silently=True
        )
        print(f"[ALERTA] Error general en scraping: {e}")
        return {"publicaciones": [], "valores_monedas": None, "total_documentos": 0} 