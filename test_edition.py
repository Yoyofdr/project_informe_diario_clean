#!/usr/bin/env python
"""
Script para probar la obtención del número de edición
"""
import time
try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    
    def test_edition_number():
        print("=== TEST DE NÚMERO DE EDICIÓN ===\n")
        
        fecha = "11-07-2025"
        url_select = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/select_edition.php?date={fecha}"
        
        print(f"Fecha: {fecha}")
        print(f"URL: {url_select}")
        print("-" * 50)
        
        driver = None
        try:
            options = uc.ChromeOptions()
            # Probar sin headless para ver qué pasa
            # options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            print("Iniciando Chrome...")
            driver = uc.Chrome(options=options)
            
            print("Navegando a la página de selección...")
            driver.get(url_select)
            
            print("Esperando 5 segundos...")
            time.sleep(5)
            
            # Tomar screenshot
            driver.save_screenshot("edition_select.png")
            print("Screenshot guardado: edition_select.png")
            
            # Buscar enlaces
            links = driver.find_elements(By.TAG_NAME, 'a')
            print(f"\nTotal de enlaces encontrados: {len(links)}")
            
            # Buscar específicamente enlaces con edition
            edition_links = []
            for link in links:
                href = link.get_attribute('href')
                text = link.text
                
                if href:
                    if 'edition=' in href:
                        edition_links.append((href, text))
                        print(f"\nEnlace con edición encontrado:")
                        print(f"  Texto: {text}")
                        print(f"  URL: {href}")
                        
                        # Extraer número de edición
                        import re
                        match = re.search(r'edition=([0-9]+)', href)
                        if match:
                            print(f"  Número de edición: {match.group(1)}")
            
            if not edition_links:
                print("\nNo se encontraron enlaces con número de edición")
                print("Guardando HTML para inspección...")
                
                html = driver.page_source
                with open("edition_page.html", "w", encoding="utf-8") as f:
                    f.write(html)
                print("HTML guardado: edition_page.html")
                
                # Buscar si hay algún mensaje de error
                body_text = driver.find_element(By.TAG_NAME, "body").text
                if "no hay" in body_text.lower() or "no existe" in body_text.lower():
                    print(f"\nPosible mensaje de error en la página: {body_text[:200]}...")
            
        except Exception as e:
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            if driver:
                print("\nCerrando navegador...")
                driver.quit()
    
    test_edition_number()
    
except ImportError as e:
    print(f"Error de importación: {e}")
    print("Asegúrate de tener instalado undetected-chromedriver")