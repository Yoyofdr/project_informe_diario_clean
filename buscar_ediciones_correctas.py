#!/usr/bin/env python3
"""
Script para buscar las ediciones correctas de fechas específicas
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def buscar_edicion_con_selenium(fecha):
    """Busca la edición navegando directamente a la fecha"""
    print(f"\nBuscando edición para {fecha}...")
    
    # Configurar Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        # URL directa para la fecha
        url = f"https://www.diariooficial.interior.gob.cl/publicaciones/{fecha.replace('-', '/')}/"
        print(f"Navegando a: {url}")
        
        driver.get(url)
        time.sleep(3)
        
        # Buscar el selector de ediciones o el número de edición en la página
        try:
            # Opción 1: Buscar en el selector
            edition_select = driver.find_element(By.ID, "edition")
            selected_option = edition_select.find_element(By.CSS_SELECTOR, "option[selected]")
            edition = selected_option.get_attribute("value")
            print(f"✓ Edición encontrada en selector: {edition}")
            return edition
        except:
            pass
        
        # Opción 2: Buscar en el texto de la página
        try:
            # Buscar patrones como "Edición N° 44197"
            page_text = driver.find_element(By.TAG_NAME, "body").text
            import re
            match = re.search(r'Edición N[°º]\s*(\d+)', page_text)
            if match:
                edition = match.group(1)
                print(f"✓ Edición encontrada en texto: {edition}")
                return edition
        except:
            pass
        
        # Opción 3: Revisar la URL después de redirección
        current_url = driver.current_url
        if "edition=" in current_url:
            edition = current_url.split("edition=")[1].split("&")[0]
            print(f"✓ Edición encontrada en URL: {edition}")
            return edition
        
        # Opción 4: Buscar en links de descarga
        try:
            pdf_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='.pdf']")
            if pdf_links:
                href = pdf_links[0].get_attribute("href")
                # Extraer edición del path del PDF
                import re
                match = re.search(r'/(\d{5})/', href)
                if match:
                    edition = match.group(1)
                    print(f"✓ Edición encontrada en link PDF: {edition}")
                    return edition
        except:
            pass
        
        print(f"✗ No se pudo encontrar la edición para {fecha}")
        
        # Guardar screenshot para debug
        driver.save_screenshot(f"debug_{fecha.replace('-', '_')}.png")
        
        return None
        
    finally:
        driver.quit()

# Buscar ediciones para las fechas problemáticas
fechas_buscar = ["12-07-2025", "14-07-2025", "15-07-2025"]

print("=== BÚSQUEDA DE EDICIONES CORRECTAS ===")

ediciones_encontradas = {}
for fecha in fechas_buscar:
    edicion = buscar_edicion_con_selenium(fecha)
    if edicion:
        ediciones_encontradas[fecha] = edicion
    time.sleep(2)  # Pausa entre búsquedas

print("\n=== RESUMEN ===")
print("Ediciones encontradas:")
for fecha, edicion in ediciones_encontradas.items():
    print(f"  {fecha}: {edicion}")

# Si encontramos ediciones, actualizar el caché
if ediciones_encontradas:
    print("\nActualizando caché de ediciones...")
    import json
    
    # Leer caché actual
    try:
        with open('edition_cache.json', 'r') as f:
            cache = json.load(f)
    except:
        cache = {}
    
    # Actualizar con las nuevas ediciones
    cache.update(ediciones_encontradas)
    
    # Guardar caché actualizado
    with open('edition_cache.json', 'w') as f:
        json.dump(cache, f, indent=2)
    
    print("✓ Caché actualizado")