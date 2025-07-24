#!/usr/bin/env python
"""
Script para verificar publicaciones del SII y CMF en el Diario Oficial del 23 de julio de 2025
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

def buscar_contenido_sii_cmf():
    """Busca publicaciones del SII y CMF en el Diario Oficial"""
    
    # URL del 23 de julio de 2025 con parámetros de edición
    fecha = "23-07-2025"
    edition = "44205"
    url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}"
    
    print("=== VERIFICACIÓN DE CONTENIDO SII/CMF ===")
    print(f"URL: {url}")
    print(f"Fecha: 23 de julio de 2025")
    print("="*50)
    
    # Configurar Chrome
    options = Options()
    options.add_argument('--headless')  # Modo headless para no abrir ventana
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
        r'Res\. Ex\. SII'
    ]
    
    patrones_cmf = [
        r'Comisión para el Mercado Financiero',
        r'CMF',
        r'Resolución Exenta CMF'
    ]
    
    publicaciones_sii = []
    publicaciones_cmf = []
    
    try:
        print("\nNavegando a la página...")
        driver.get(url)
        
        # Esperar a que la página cargue
        print("Esperando que la página cargue completamente...")
        time.sleep(10)
        
        # Obtener el HTML completo
        html = driver.page_source
        
        print(f"\nTamaño del HTML: {len(html)} caracteres")
        
        # Verificar si es la página correcta
        if "Diario Oficial" not in html:
            print("⚠️  ADVERTENCIA: No parece ser la página del Diario Oficial")
            driver.save_screenshot("verificacion_pagina.png")
            print("Screenshot guardado: verificacion_pagina.png")
        
        # Buscar todas las publicaciones
        print("\nBuscando publicaciones...")
        
        # Intentar diferentes selectores para encontrar las publicaciones
        selectores = [
            "//div[@class='publicacion']",
            "//div[contains(@class, 'item')]",
            "//div[contains(@class, 'publication')]",
            "//li[contains(@class, 'list-item')]",
            "//div[contains(@class, 'content')]//a",
            "//a[contains(@href, 'pdf')]",
            "//td//a",
            "//p//a"
        ]
        
        elementos_encontrados = []
        for selector in selectores:
            try:
                elementos = driver.find_elements(By.XPATH, selector)
                if elementos:
                    print(f"Encontrados {len(elementos)} elementos con selector: {selector}")
                    elementos_encontrados.extend(elementos)
            except:
                pass
        
        print(f"\nTotal de elementos encontrados: {len(elementos_encontrados)}")
        
        # Buscar en el texto completo de la página
        print("\n" + "="*50)
        print("BÚSQUEDA EN TEXTO COMPLETO")
        print("="*50)
        
        # Buscar SII
        print("\nBuscando menciones del SII:")
        for patron in patrones_sii:
            matches = re.finditer(patron, html, re.IGNORECASE)
            for match in matches:
                # Obtener contexto alrededor del match
                start = max(0, match.start() - 200)
                end = min(len(html), match.end() + 200)
                contexto = html[start:end]
                contexto = re.sub(r'<[^>]+>', ' ', contexto)  # Limpiar HTML
                contexto = ' '.join(contexto.split())  # Normalizar espacios
                
                print(f"\n✓ Encontrado '{match.group()}':")
                print(f"  Contexto: ...{contexto}...")
                
                # Buscar título cercano
                titulo_match = re.search(r'([^<>]{20,200})', contexto)
                if titulo_match:
                    publicaciones_sii.append({
                        'patron': match.group(),
                        'contexto': contexto,
                        'titulo_posible': titulo_match.group(1).strip()
                    })
        
        # Buscar CMF
        print("\n\nBuscando menciones de CMF:")
        for patron in patrones_cmf:
            matches = re.finditer(patron, html, re.IGNORECASE)
            for match in matches:
                # Obtener contexto alrededor del match
                start = max(0, match.start() - 200)
                end = min(len(html), match.end() + 200)
                contexto = html[start:end]
                contexto = re.sub(r'<[^>]+>', ' ', contexto)  # Limpiar HTML
                contexto = ' '.join(contexto.split())  # Normalizar espacios
                
                print(f"\n✓ Encontrado '{match.group()}':")
                print(f"  Contexto: ...{contexto}...")
                
                # Buscar título cercano
                titulo_match = re.search(r'([^<>]{20,200})', contexto)
                if titulo_match:
                    publicaciones_cmf.append({
                        'patron': match.group(),
                        'contexto': contexto,
                        'titulo_posible': titulo_match.group(1).strip()
                    })
        
        # Buscar específicamente en secciones
        print("\n" + "="*50)
        print("BÚSQUEDA POR SECCIONES")
        print("="*50)
        
        secciones = ["Normas Generales", "Normas Particulares", "Avisos"]
        for seccion in secciones:
            if seccion in html:
                print(f"\n✓ Sección '{seccion}' encontrada")
                # Extraer contenido de la sección
                seccion_pattern = f"{seccion}.*?(?=Normas|Avisos|</div>|$)"
                seccion_match = re.search(seccion_pattern, html, re.DOTALL | re.IGNORECASE)
                if seccion_match:
                    contenido_seccion = seccion_match.group()
                    
                    # Buscar SII en esta sección
                    for patron in patrones_sii:
                        if re.search(patron, contenido_seccion, re.IGNORECASE):
                            print(f"  → SII encontrado en sección {seccion}")
                    
                    # Buscar CMF en esta sección
                    for patron in patrones_cmf:
                        if re.search(patron, contenido_seccion, re.IGNORECASE):
                            print(f"  → CMF encontrado en sección {seccion}")
        
        # Guardar evidencia
        driver.save_screenshot("verificacion_sii_cmf.png")
        print("\nScreenshot guardado: verificacion_sii_cmf.png")
        
        with open("verificacion_sii_cmf.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("HTML completo guardado: verificacion_sii_cmf.html")
        
        # Resumen final
        print("\n" + "="*50)
        print("RESUMEN FINAL")
        print("="*50)
        print(f"\nPublicaciones del SII encontradas: {len(publicaciones_sii)}")
        if publicaciones_sii:
            print("\nDetalles SII:")
            for i, pub in enumerate(publicaciones_sii, 1):
                print(f"\n{i}. {pub['patron']}")
                if 'titulo_posible' in pub:
                    print(f"   Título posible: {pub['titulo_posible']}")
        
        print(f"\nPublicaciones de CMF encontradas: {len(publicaciones_cmf)}")
        if publicaciones_cmf:
            print("\nDetalles CMF:")
            for i, pub in enumerate(publicaciones_cmf, 1):
                print(f"\n{i}. {pub['patron']}")
                if 'titulo_posible' in pub:
                    print(f"   Título posible: {pub['titulo_posible']}")
        
        if not publicaciones_sii and not publicaciones_cmf:
            print("\n⚠️  NO SE ENCONTRARON PUBLICACIONES DEL SII NI CMF")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Guardar screenshot de error
        try:
            driver.save_screenshot("error_verificacion.png")
            print("\nScreenshot de error guardado: error_verificacion.png")
        except:
            pass
    
    finally:
        driver.quit()
        print("\n✓ Driver cerrado")

if __name__ == "__main__":
    buscar_contenido_sii_cmf()