#!/usr/bin/env python
"""
Script para obtener datos reales del 21 de julio usando Selenium
"""
import os
import sys
import django
from datetime import datetime
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

def scraper_selenium_diario():
    """Obtiene las publicaciones del 21 de julio usando Selenium"""
    
    fecha = "21-07-2025"
    edition = "44204"
    
    print("=== SCRAPER SELENIUM DIARIO OFICIAL ===")
    print(f"Fecha: {fecha}")
    print(f"Edición: {edition}")
    
    # Configurar undetected-chromedriver
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # No usar headless para debug
    # options.add_argument('--headless')
    
    driver = None
    publicaciones = []
    
    try:
        print("\nIniciando navegador...")
        driver = uc.Chrome(options=options)
        
        # Primero navegar a la página principal
        print("Navegando a la página principal...")
        driver.get("https://www.diariooficial.interior.gob.cl/")
        time.sleep(3)
        
        # Luego ir a la edición específica
        url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}"
        print(f"\nNavegando a: {url}")
        driver.get(url)
        
        # Esperar más tiempo para que cargue
        print("Esperando que cargue el contenido...")
        time.sleep(5)
        
        # Intentar diferentes selectores
        selectors_to_try = [
            ("tr.content", "tabla con class content"),
            ("table.tabla_contenido tr", "tabla de contenido"),
            ("div.publicacion", "divs de publicación"),
            ("a[href$='.pdf']", "enlaces PDF")
        ]
        
        for selector, description in selectors_to_try:
            print(f"\nBuscando: {description} ({selector})")
            elementos = driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"Encontrados: {len(elementos)} elementos")
            
            if elementos and selector == "tr.content":
                # Procesar publicaciones
                for i, tr in enumerate(elementos):
                    try:
                        tds = tr.find_elements(By.TAG_NAME, "td")
                        if len(tds) >= 2:
                            titulo = tds[0].text.strip()
                            
                            # Buscar enlace PDF
                            link_element = tds[1].find_element(By.TAG_NAME, "a")
                            pdf_url = link_element.get_attribute("href") if link_element else ""
                            
                            if titulo and pdf_url:
                                publicacion = {
                                    "titulo": titulo,
                                    "url_pdf": pdf_url,
                                    "seccion": "NORMAS GENERALES"  # Determinar después
                                }
                                publicaciones.append(publicacion)
                                print(f"\n✓ Publicación {i+1}:")
                                print(f"  Título: {titulo[:80]}...")
                                print(f"  PDF: {pdf_url}")
                    except Exception as e:
                        print(f"  Error procesando elemento {i}: {str(e)}")
        
        # Si no encontramos por selectores, buscar texto
        if not publicaciones:
            print("\nBuscando publicaciones por texto...")
            page_text = driver.page_source
            
            # Verificar si hay contenido del Diario Oficial
            if "Diario Oficial" in page_text:
                print("✓ Se encontró 'Diario Oficial' en la página")
            
            if "Normas Generales" in page_text:
                print("✓ Se encontró 'Normas Generales' en la página")
                
            # Buscar todos los enlaces PDF
            pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
            print(f"\n📎 Enlaces PDF encontrados: {len(pdf_links)}")
            
            for i, link in enumerate(pdf_links[:10]):
                try:
                    href = link.get_attribute("href")
                    # Buscar el texto asociado
                    parent = link.find_element(By.XPATH, "./..")
                    texto = parent.text.strip()
                    
                    if href and texto:
                        publicacion = {
                            "titulo": texto,
                            "url_pdf": href,
                            "seccion": "GENERAL"
                        }
                        publicaciones.append(publicacion)
                        print(f"\n✓ PDF {i+1}:")
                        print(f"  Texto: {texto[:80]}...")
                        print(f"  URL: {href}")
                except Exception as e:
                    pass
        
        # Guardar captura de pantalla
        screenshot_file = "screenshot_21_julio.png"
        driver.save_screenshot(screenshot_file)
        print(f"\n📸 Captura guardada: {screenshot_file}")
        
        # Guardar HTML
        with open("selenium_21_julio.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 HTML guardado: selenium_21_julio.html")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            print("\nCerrando navegador...")
            driver.quit()
    
    # Resumen
    print(f"\n{'='*50}")
    print(f"RESUMEN:")
    print(f"Publicaciones encontradas: {len(publicaciones)}")
    if publicaciones:
        print("\nPRIMERAS 3 PUBLICACIONES:")
        for i, pub in enumerate(publicaciones[:3]):
            print(f"\n{i+1}. {pub['titulo'][:100]}...")
            print(f"   PDF: {pub['url_pdf']}")
    print(f"{'='*50}")
    
    return publicaciones

if __name__ == "__main__":
    publicaciones = scraper_selenium_diario()
    
    # Generar informe si hay publicaciones
    if publicaciones:
        print("\n✅ Se encontraron publicaciones reales")
    else:
        print("\n⚠️  No se encontraron publicaciones")