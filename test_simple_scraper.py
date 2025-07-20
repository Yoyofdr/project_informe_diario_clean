#!/usr/bin/env python
"""
Test simple del scraper sin usar Django
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    
    print("=== TEST SIMPLE DE SELENIUM ===\n")
    
    url = "https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date=10-07-2025&edition=&v=1"
    print(f"URL: {url}")
    
    driver = None
    try:
        options = uc.ChromeOptions()
        # Modo visible para debugging
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        print("Iniciando Chrome...")
        driver = uc.Chrome(options=options)
        
        print("Navegando a la página...")
        driver.get(url)
        
        print("Esperando 10 segundos para carga completa...")
        time.sleep(10)
        
        # Tomar screenshot
        driver.save_screenshot("diario_oficial_test.png")
        print("Screenshot guardado como diario_oficial_test.png")
        
        # Obtener HTML
        html = driver.page_source
        print(f"\nLongitud del HTML: {len(html)} caracteres")
        
        # Buscar contenido relevante
        if "NORMAS" in html.upper():
            print("✓ Se encontró contenido de NORMAS")
        else:
            print("✗ No se encontró contenido de NORMAS")
            
        # Buscar tablas
        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"\nTablas encontradas: {len(tables)}")
        
        # Buscar PDFs
        pdfs = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
        print(f"Enlaces PDF encontrados: {len(pdfs)}")
        
        if pdfs:
            print("\nPrimeros 5 PDFs:")
            for i, pdf in enumerate(pdfs[:5]):
                href = pdf.get_attribute('href')
                text = pdf.text or pdf.find_element(By.XPATH, "..").text
                print(f"  {i+1}. {href}")
                print(f"     Texto: {text[:100]}...")
        
        # Guardar HTML
        with open("diario_oficial_test.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("\nHTML guardado como diario_oficial_test.html")
        
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            print("\nCerrando navegador...")
            driver.quit()
            
except ImportError as e:
    print(f"ERROR: Falta instalar dependencias: {e}")
    print("Ejecuta: pip install undetected-chromedriver selenium")