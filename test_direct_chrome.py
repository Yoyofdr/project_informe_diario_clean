#!/usr/bin/env python
"""
Test directo con Chrome sin headless para ver qué pasa
"""
import time

try:
    import undetected_chromedriver as uc
    
    print("=== TEST DIRECTO CHROME ===\n")
    
    # URL con edición conocida
    fecha = "11-07-2025"
    edition = "44196"
    url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}&v=1"
    
    print(f"URL: {url}")
    print("Abriendo Chrome en modo visible...\n")
    
    options = uc.ChromeOptions()
    # NO usar headless para ver qué pasa
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = uc.Chrome(options=options)
    
    try:
        print("1. Navegando a la URL...")
        driver.get(url)
        
        print("2. Esperando 10 segundos para carga completa...")
        time.sleep(10)
        
        # Verificar título
        title = driver.title
        print(f"\nTítulo de la página: {title}")
        
        # Verificar URL actual (por si hay redirección)
        current_url = driver.current_url
        print(f"URL actual: {current_url}")
        
        # Buscar elementos clave
        try:
            # Buscar tablas
            tables = driver.find_elements(uc.By.TAG_NAME, "table")
            print(f"\nTablas encontradas: {len(tables)}")
            
            # Buscar texto "NORMAS"
            body_text = driver.find_element(uc.By.TAG_NAME, "body").text
            if "NORMAS GENERALES" in body_text:
                print("✓ Se encontró 'NORMAS GENERALES'")
            else:
                print("✗ No se encontró 'NORMAS GENERALES'")
                
            # Buscar PDFs
            pdfs = driver.find_elements(uc.By.XPATH, "//a[contains(@href, '.pdf')]")
            print(f"\nEnlaces PDF encontrados: {len(pdfs)}")
            
            if pdfs:
                print("\nPrimeros 3 PDFs:")
                for i, pdf in enumerate(pdfs[:3]):
                    href = pdf.get_attribute('href')
                    text = pdf.text or "Sin texto"
                    print(f"{i+1}. {text[:50]}... -> {href}")
                    
        except Exception as e:
            print(f"\nError buscando elementos: {e}")
        
        # Guardar screenshot
        driver.save_screenshot("test_chrome_visible.png")
        print("\nScreenshot guardado: test_chrome_visible.png")
        
        # Guardar HTML
        html = driver.page_source
        with open("test_chrome_visible.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("HTML guardado: test_chrome_visible.html")
        
        print(f"\nLongitud del HTML: {len(html)} caracteres")
        
        # Verificar si hay algún mensaje de error
        if "error" in html.lower() or "no se encontr" in html.lower():
            print("\n⚠️  Posible mensaje de error en la página")
            
        input("\nPresiona ENTER para cerrar el navegador...")
        
    finally:
        driver.quit()
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()