#!/usr/bin/env python
"""
Script para buscar la edición correcta del 18 de julio
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def buscar_edicion_18_julio():
    """Busca la edición del 18 de julio usando Selenium"""
    
    # Configurar Chrome en modo headless
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Primero, ir a la página base del 18 de julio sin especificar edición
        url_base = "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/18/"
        print(f"Visitando: {url_base}")
        
        driver.get(url_base)
        time.sleep(3)  # Esperar carga completa
        
        # Buscar el selector de ediciones
        try:
            edition_select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ediciones"))
            )
            
            # Obtener todas las opciones
            options = edition_select.find_elements(By.TAG_NAME, "option")
            print(f"\nEdiciones encontradas: {len(options)}")
            
            edition_number = None
            for option in options:
                value = option.get_attribute("value")
                text = option.text.strip()
                selected = option.get_attribute("selected")
                
                if selected:
                    print(f"* {value} - {text} [SELECCIONADA]")
                    # Extraer número de edición
                    if "edicion-" in value:
                        edition_number = value.split("edicion-")[1].rstrip("/")
                else:
                    print(f"  {value} - {text}")
            
            if edition_number:
                print(f"\nNúmero de edición del 18-07-2025: {edition_number}")
                
                # Ahora visitar la URL con la edición correcta
                url_correcta = f"https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/18/edicion-{edition_number}/"
                print(f"\nVisitando URL con edición correcta: {url_correcta}")
                
                driver.get(url_correcta)
                time.sleep(3)
                
                # Buscar publicaciones
                publicaciones = driver.find_elements(By.CLASS_NAME, "light")
                print(f"\nPublicaciones encontradas: {len(publicaciones)}")
                
                if publicaciones:
                    print("\nPrimeras 5 publicaciones:")
                    for i, pub in enumerate(publicaciones[:5], 1):
                        titulo = pub.text.strip()
                        print(f"{i}. {titulo}")
                
                return edition_number
            else:
                print("\nNo se pudo determinar el número de edición")
                
        except Exception as e:
            print(f"Error buscando selector de ediciones: {e}")
            
            # Intentar buscar publicaciones directamente
            publicaciones = driver.find_elements(By.CLASS_NAME, "light")
            print(f"\nPublicaciones encontradas (sin selector): {len(publicaciones)}")
            
    except Exception as e:
        print(f"Error general: {e}")
        
    finally:
        if driver:
            driver.quit()
    
    return None

if __name__ == "__main__":
    print("=== BUSCANDO EDICIÓN DEL 18 DE JULIO DE 2025 ===\n")
    
    edition = buscar_edicion_18_julio()
    
    if edition:
        print(f"\n✓ Edición encontrada: {edition}")
        print(f"\nPara actualizar el caché, agrega esta línea a edition_cache.json:")
        print(f'"18-07-2025": "{edition}"')
    else:
        print("\n✗ No se pudo encontrar la edición")