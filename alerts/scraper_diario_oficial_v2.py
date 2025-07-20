"""
Versión mejorada del scraper del Diario Oficial con múltiples estrategias de fallback
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os
import time
from typing import Dict, List, Optional, Tuple

# Selenium imports con manejo de errores
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("[WARNING] Selenium no disponible, usando solo requests")

# Undetected chromedriver con manejo de errores
try:
    import undetected_chromedriver as uc
    UC_AVAILABLE = True
except ImportError:
    UC_AVAILABLE = False
    print("[WARNING] Undetected ChromeDriver no disponible")

from alerts.services.cache_service import cache_service
from alerts.services.pdf_extractor import PDFExtractor
from alerts.utils.rate_limiter import rate_limited
from alerts.utils.retry_utils import retry
from alerts.scraper_diario_oficial import (
    BASE_URL, SECCIONES_VALIDAS, PALABRAS_RELEVANTES, 
    PALABRAS_NO_RELEVANTES, EXCEPCIONES_RELEVANTES,
    es_relevante, descargar_pdf_con_cache, extraer_texto_pdf_mixto,
    resumen_con_gemini, generar_resumen_desde_texto, extraer_valores_dolar_euro
)

class DiarioOficialScraper:
    """Scraper mejorado con múltiples estrategias de obtención de contenido"""
    
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        
    def _get_html_with_uc(self, url: str, max_attempts: int = 3) -> Optional[str]:
        """Intenta obtener HTML usando undetected-chromedriver"""
        if not UC_AVAILABLE:
            return None
            
        for attempt in range(max_attempts):
            driver = None
            try:
                options = uc.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                
                driver = uc.Chrome(options=options, version_main=None)
                driver.set_page_load_timeout(45)
                
                print(f"[UC] Intento {attempt + 1}/{max_attempts}")
                driver.get(url)
                
                # Esperar carga inicial
                time.sleep(5)
                
                # Esperar elementos
                try:
                    WebDriverWait(driver, 30).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    )
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                except TimeoutException:
                    print(f"[UC] Timeout esperando elementos")
                
                html = driver.page_source
                
                if html and len(html) > 1000:
                    return html
                    
            except Exception as e:
                print(f"[UC] Error intento {attempt + 1}: {str(e)[:100]}")
            finally:
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
                        
            if attempt < max_attempts - 1:
                time.sleep(5)
                
        return None
    
    def _get_html_with_selenium(self, url: str) -> Optional[str]:
        """Intenta obtener HTML usando Selenium estándar"""
        if not SELENIUM_AVAILABLE:
            return None
            
        driver = None
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            # Intentar con ChromeDriverManager
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except:
                # Fallback a driver por defecto
                driver = webdriver.Chrome(options=options)
            
            driver.set_page_load_timeout(45)
            print("[Selenium] Navegando a URL...")
            driver.get(url)
            
            time.sleep(5)
            
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            html = driver.page_source
            if html and len(html) > 1000:
                return html
                
        except Exception as e:
            print(f"[Selenium] Error: {str(e)[:100]}")
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
                    
        return None
    
    def _get_html_with_requests(self, url: str) -> Optional[str]:
        """Intenta obtener HTML usando requests (puede no funcionar si hay protección anti-bot)"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            print("[Requests] Intentando obtener HTML...")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            if response.text and len(response.text) > 1000:
                return response.text
                
        except Exception as e:
            print(f"[Requests] Error: {str(e)[:100]}")
            
        return None
    
    def obtener_html(self, url: str, use_cache: bool = True) -> Optional[str]:
        """Obtiene HTML usando múltiples estrategias con fallback"""
        
        # Estrategia 1: Undetected ChromeDriver (más confiable para sitios con protección)
        html = self._get_html_with_uc(url)
        if html and "NORMAS" in html.upper():
            print("[SUCCESS] HTML obtenido con undetected-chromedriver")
            return html
        
        # Estrategia 2: Selenium estándar
        html = self._get_html_with_selenium(url)
        if html and "NORMAS" in html.upper():
            print("[SUCCESS] HTML obtenido con Selenium estándar")
            return html
        
        # Estrategia 3: Requests (más rápido pero puede fallar con protección anti-bot)
        html = self._get_html_with_requests(url)
        if html:
            print("[SUCCESS] HTML obtenido con requests")
            return html
        
        print("[ERROR] No se pudo obtener HTML con ninguna estrategia")
        return None
    
    def obtener_sumario(self, fecha: str = None) -> Dict:
        """Obtiene el sumario del Diario Oficial para una fecha específica"""
        from datetime import datetime as dt
        
        if fecha is None:
            fecha = datetime.now().strftime("%d-%m-%Y")
            
        fecha_cache = dt.strptime(fecha, "%d-%m-%Y")
        
        # Verificar caché
        resultado_cache = cache_service.get_scraping_result(fecha_cache)
        if resultado_cache and isinstance(resultado_cache, dict) and 'publicaciones' in resultado_cache:
            print(f"[CACHE] Usando resultado desde caché para {fecha}")
            return resultado_cache
        
        # Construir URL
        edition = "44192" if fecha == "07-07-2025" else ""
        url = f"{BASE_URL}?date={fecha}&edition={edition}&v=1"
        
        print(f"[SCRAPER] Obteniendo sumario para fecha: {fecha}")
        print(f"[SCRAPER] URL: {url}")
        
        # Obtener HTML
        html = self.obtener_html(url)
        
        if not html:
            print("[ERROR] No se pudo obtener HTML del Diario Oficial")
            return {"publicaciones": [], "valores_monedas": None, "total_documentos": 0}
        
        # Procesar HTML
        try:
            resultado = self._procesar_html(html, fecha_cache)
            
            # Guardar en caché
            cache_service.set_scraping_result(fecha_cache, resultado)
            
            return resultado
            
        except Exception as e:
            print(f"[ERROR] Error procesando HTML: {str(e)}")
            return {"publicaciones": [], "valores_monedas": None, "total_documentos": 0}
    
    def _procesar_html(self, html: str, fecha_cache) -> Dict:
        """Procesa el HTML y extrae las publicaciones"""
        soup = BeautifulSoup(html, "html.parser")
        sumario = []
        vistos = set()
        seccion_actual = None
        valores_monedas = None
        total_documentos = 0
        no_relevantes = []
        
        # Buscar secciones y publicaciones
        for tag in soup.find_all(['b', 'strong', 'h3', 'h2', 'h1', 'td', 'th']):
            texto = tag.get_text(strip=True).upper()
            
            if texto in SECCIONES_VALIDAS:
                seccion_actual = texto
                print(f"[PARSER] Sección encontrada: {seccion_actual}")
                
            elif seccion_actual in SECCIONES_VALIDAS:
                # Buscar enlaces PDF en esta sección
                for link in tag.find_all_next("a", href=True):
                    href = link["href"]
                    
                    if href.endswith(".pdf"):
                        total_documentos += 1
                        
                        # Obtener título
                        parent = link.find_parent("tr") or link.find_parent("li") or link.parent
                        titulo = None
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
                        
                        # Procesar monedas
                        es_certificado_monedas = (
                            "TIPOS DE CAMBIO" in titulo.upper() and 
                            "PARIDADES DE MONEDAS EXTRANJERAS" in titulo.upper()
                        )
                        
                        if es_certificado_monedas and valores_monedas is None:
                            texto_pdf = extraer_texto_pdf_mixto(href)
                            valores_monedas = extraer_valores_dolar_euro(texto_pdf)
                        
                        # Procesar publicación
                        if relevante or ("DÓLAR" in titulo.upper() or "EURO" in titulo.upper()):
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
                            # Guardar no relevantes para fallback
                            texto_pdf = extraer_texto_pdf_mixto(href)
                            resumen = generar_resumen_desde_texto(texto_pdf, titulo)
                            
                            no_relevantes.append({
                                "seccion": seccion_actual,
                                "titulo": titulo,
                                "url_pdf": href,
                                "relevante": False,
                                "resumen": resumen
                            })
                    
                    # Verificar si salimos de la sección
                    siguiente_texto = link.find_next(string=True)
                    if siguiente_texto and siguiente_texto.strip().upper() in SECCIONES_VALIDAS:
                        break
        
        # Si no hay publicaciones relevantes, incluir una no relevante
        if not sumario and no_relevantes:
            PALABRAS_CLAVE = [
                "decreto", "resolución", "plan", "cambio", "beneficio", 
                "subsidio", "proyecto", "programa", "tarifa", "reforma", 
                "ley", "reglamento", "asignación", "nombramiento", 
                "prórroga", "modificación"
            ]
            
            seleccionada = None
            for pub in no_relevantes:
                texto_busqueda = (pub["titulo"] + " " + pub["resumen"]).lower()
                if any(pal in texto_busqueda for pal in PALABRAS_CLAVE):
                    seleccionada = pub
                    break
            
            if not seleccionada and no_relevantes:
                seleccionada = no_relevantes[0]
            
            if seleccionada:
                sumario.append(seleccionada)
        
        print(f"[PARSER] Total documentos: {total_documentos}")
        print(f"[PARSER] Publicaciones relevantes: {len(sumario)}")
        
        return {
            "publicaciones": sumario,
            "valores_monedas": valores_monedas,
            "total_documentos": total_documentos
        }


# Función para mantener compatibilidad con el código existente
def obtener_sumario_diario_oficial(fecha=None):
    """Función wrapper para mantener compatibilidad"""
    scraper = DiarioOficialScraper()
    return scraper.obtener_sumario(fecha)