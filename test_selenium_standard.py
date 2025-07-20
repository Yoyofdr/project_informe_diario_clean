#!/usr/bin/env python
"""
Test con Selenium estándar
"""
import time

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    
    print("=== TEST SELENIUM ESTÁNDAR ===\n")
    
    # URL con edición conocida
    fecha = "11-07-2025"
    edition = "44196"
    url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}&v=1"
    
    print(f"URL: {url}")
    
    options = Options()
    # Probar sin headless primero
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    print("Instalando/verificando ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    
    print("Iniciando Chrome...")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        print("Navegando a la página...")
        driver.get(url)
        
        print("Esperando 10 segundos...")
        time.sleep(10)
        
        # Información básica
        print(f"\nTítulo: {driver.title}")
        print(f"URL actual: {driver.current_url}")
        
        # Buscar contenido
        html = driver.page_source
        print(f"Longitud HTML: {len(html)}")
        
        # Verificar contenido específico
        if "NORMAS" in html:
            print("✓ Contiene 'NORMAS'")
        else:
            print("✗ NO contiene 'NORMAS'")
            
        # Buscar mensaje de protección
        if "checking your browser" in html.lower():
            print("⚠️  Detectado: Página de verificación de navegador")
        
        # Guardar evidencia
        driver.save_screenshot("selenium_standard.png")
        print("\nScreenshot: selenium_standard.png")
        
        with open("selenium_standard.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("HTML: selenium_standard.html")
        
        # Contar PDFs
        pdfs = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
        print(f"\nPDFs encontrados: {len(pdfs)}")
        
        input("\nPresiona ENTER para cerrar...")
        
    finally:
        driver.quit()
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()