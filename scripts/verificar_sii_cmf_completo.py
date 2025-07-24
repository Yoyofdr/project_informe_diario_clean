#!/usr/bin/env python
"""
Script completo para verificar publicaciones del SII y CMF en todas las secciones del Diario Oficial
"""
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def buscar_contenido_sii_cmf_completo():
    """Busca publicaciones del SII y CMF en todas las secciones del Diario Oficial"""
    
    fecha = "23-07-2025"
    edition = "44205"
    
    # URLs de las diferentes secciones
    secciones = {
        "Normas Generales": f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}",
        "Normas Particulares": f"https://www.diariooficial.interior.gob.cl/edicionelectronica/normas_particulares.php?date={fecha}&edition={edition}",
        "Avisos Destacados": f"https://www.diariooficial.interior.gob.cl/edicionelectronica/avisos_destacados.php?date={fecha}&edition={edition}",
        "Publicaciones Judiciales": f"https://www.diariooficial.interior.gob.cl/edicionelectronica/publicaciones_judiciales.php?date={fecha}&edition={edition}",
        "Empresas y Cooperativas": f"https://www.diariooficial.interior.gob.cl/edicionelectronica/empresas_cooperativas.php?date={fecha}&edition={edition}"
    }
    
    print("=== VERIFICACIÓN COMPLETA DE CONTENIDO SII/CMF ===")
    print(f"Fecha: 23 de julio de 2025")
    print(f"Edición: {edition}")
    print("="*60)
    
    # Configurar Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Iniciar driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Patrones de búsqueda
    patrones_sii = [
        r'Servicio de Impuestos Internos',
        r'SII',
        r'Resolución Ex\. SII',
        r'Resolución Exenta SII',
        r'Res\. Ex\. SII',
        r'Res\. Ex\. N° \d+.*SII',
        r'Resolución Ex\. N° \d+.*SII'
    ]
    
    patrones_cmf = [
        r'Comisión para el Mercado Financiero',
        r'CMF',
        r'Resolución Exenta CMF',
        r'Res\. Ex\. CMF'
    ]
    
    todos_los_hallazgos = []
    
    try:
        for nombre_seccion, url in secciones.items():
            print(f"\n{'='*60}")
            print(f"ANALIZANDO SECCIÓN: {nombre_seccion}")
            print(f"{'='*60}")
            print(f"URL: {url}")
            
            driver.get(url)
            time.sleep(5)  # Esperar carga
            
            html = driver.page_source
            print(f"Tamaño del HTML: {len(html)} caracteres")
            
            publicaciones_seccion = []
            
            # Buscar contenido específico en tablas
            try:
                # Buscar todas las filas de contenido
                filas = driver.find_elements(By.XPATH, "//tr[@class='content']")
                print(f"Filas de contenido encontradas: {len(filas)}")
                
                for fila in filas:
                    try:
                        texto_fila = fila.text
                        
                        # Buscar SII
                        for patron in patrones_sii:
                            if re.search(patron, texto_fila, re.IGNORECASE):
                                # Obtener el título completo
                                titulo_elem = fila.find_element(By.XPATH, ".//td[1]")
                                pdf_elem = fila.find_element(By.XPATH, ".//td[2]//a")
                                
                                publicacion = {
                                    'seccion': nombre_seccion,
                                    'organismo': 'SII',
                                    'titulo': titulo_elem.text.strip(),
                                    'cve': pdf_elem.text if pdf_elem else 'Sin CVE',
                                    'pdf_url': pdf_elem.get_attribute('href') if pdf_elem else 'Sin URL'
                                }
                                publicaciones_seccion.append(publicacion)
                                print(f"\n✓ SII ENCONTRADO:")
                                print(f"  Título: {publicacion['titulo']}")
                                print(f"  CVE: {publicacion['cve']}")
                                break
                        
                        # Buscar CMF
                        for patron in patrones_cmf:
                            if re.search(patron, texto_fila, re.IGNORECASE):
                                # Obtener el título completo
                                titulo_elem = fila.find_element(By.XPATH, ".//td[1]")
                                pdf_elem = fila.find_element(By.XPATH, ".//td[2]//a")
                                
                                publicacion = {
                                    'seccion': nombre_seccion,
                                    'organismo': 'CMF',
                                    'titulo': titulo_elem.text.strip(),
                                    'cve': pdf_elem.text if pdf_elem else 'Sin CVE',
                                    'pdf_url': pdf_elem.get_attribute('href') if pdf_elem else 'Sin URL'
                                }
                                publicaciones_seccion.append(publicacion)
                                print(f"\n✓ CMF ENCONTRADO:")
                                print(f"  Título: {publicacion['titulo']}")
                                print(f"  CVE: {publicacion['cve']}")
                                break
                                
                    except Exception as e:
                        pass
            
            except Exception as e:
                print(f"Error al buscar filas: {e}")
            
            # Búsqueda adicional en el HTML completo
            print(f"\nBúsqueda adicional en HTML completo de {nombre_seccion}:")
            
            # Buscar en todo el HTML
            for patron in patrones_sii:
                matches = list(re.finditer(patron, html, re.IGNORECASE))
                if matches:
                    print(f"  → Patrón '{patron}' encontrado {len(matches)} veces")
            
            for patron in patrones_cmf:
                matches = list(re.finditer(patron, html, re.IGNORECASE))
                if matches:
                    print(f"  → Patrón '{patron}' encontrado {len(matches)} veces")
            
            # Agregar hallazgos de esta sección
            todos_los_hallazgos.extend(publicaciones_seccion)
            
            if not publicaciones_seccion:
                print(f"\n⚠️  No se encontraron publicaciones del SII ni CMF en {nombre_seccion}")
            
            # Guardar HTML de cada sección
            with open(f"seccion_{nombre_seccion.replace(' ', '_').lower()}.html", "w", encoding="utf-8") as f:
                f.write(html)
            print(f"\nHTML guardado: seccion_{nombre_seccion.replace(' ', '_').lower()}.html")
        
        # Resumen final
        print("\n" + "="*60)
        print("RESUMEN FINAL DE TODAS LAS SECCIONES")
        print("="*60)
        
        publicaciones_sii = [p for p in todos_los_hallazgos if p['organismo'] == 'SII']
        publicaciones_cmf = [p for p in todos_los_hallazgos if p['organismo'] == 'CMF']
        
        print(f"\nTotal publicaciones SII encontradas: {len(publicaciones_sii)}")
        if publicaciones_sii:
            print("\nDetalle publicaciones SII:")
            for i, pub in enumerate(publicaciones_sii, 1):
                print(f"\n{i}. Sección: {pub['seccion']}")
                print(f"   Título: {pub['titulo']}")
                print(f"   {pub['cve']}")
                print(f"   URL: {pub['pdf_url']}")
        
        print(f"\nTotal publicaciones CMF encontradas: {len(publicaciones_cmf)}")
        if publicaciones_cmf:
            print("\nDetalle publicaciones CMF:")
            for i, pub in enumerate(publicaciones_cmf, 1):
                print(f"\n{i}. Sección: {pub['seccion']}")
                print(f"   Título: {pub['titulo']}")
                print(f"   {pub['cve']}")
                print(f"   URL: {pub['pdf_url']}")
        
        if not todos_los_hallazgos:
            print("\n⚠️  NO SE ENCONTRARON PUBLICACIONES DEL SII NI CMF EN NINGUNA SECCIÓN")
        
        # Guardar resumen
        with open("resumen_sii_cmf.txt", "w", encoding="utf-8") as f:
            f.write(f"VERIFICACIÓN DIARIO OFICIAL - 23 de julio de 2025\n")
            f.write(f"="*60 + "\n\n")
            f.write(f"Total publicaciones SII: {len(publicaciones_sii)}\n")
            f.write(f"Total publicaciones CMF: {len(publicaciones_cmf)}\n\n")
            
            if publicaciones_sii:
                f.write("PUBLICACIONES SII:\n")
                for i, pub in enumerate(publicaciones_sii, 1):
                    f.write(f"\n{i}. {pub['titulo']}\n")
                    f.write(f"   Sección: {pub['seccion']}\n")
                    f.write(f"   {pub['cve']}\n")
            
            if publicaciones_cmf:
                f.write("\nPUBLICACIONES CMF:\n")
                for i, pub in enumerate(publicaciones_cmf, 1):
                    f.write(f"\n{i}. {pub['titulo']}\n")
                    f.write(f"   Sección: {pub['seccion']}\n")
                    f.write(f"   {pub['cve']}\n")
        
        print("\nResumen guardado en: resumen_sii_cmf.txt")
        
    except Exception as e:
        print(f"\nERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.quit()
        print("\n✓ Driver cerrado")

if __name__ == "__main__":
    buscar_contenido_sii_cmf_completo()