#!/usr/bin/env python
"""
Script para hacer scraping con Selenium del Diario Oficial
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_diario_oficial_selenium():
    """Intenta scrapear el Diario Oficial del 21 de julio usando Selenium"""
    
    # Configurar Chrome options
    options = Options()
    # No usar headless para ver qué pasa
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Crear driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Navegar a la página principal primero
        print("Navegando a la página principal...")
        driver.get("https://www.diariooficial.interior.gob.cl/")
        time.sleep(3)
        
        # Intentar con la URL de la edición electrónica
        fecha = "21-07-2025"
        edition = "44204"
        url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}"
        
        print(f"\nNavegando a: {url}")
        driver.get(url)
        
        # Esperar un poco más para que cargue
        print("Esperando que cargue la página...")
        time.sleep(5)
        
        # Buscar publicaciones
        try:
            # Esperar a que aparezcan elementos de contenido
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            # Buscar tr.content
            content_rows = driver.find_elements(By.CSS_SELECTOR, "tr.content")
            print(f"\nEncontrados {len(content_rows)} tr.content")
            
            # Buscar enlaces PDF
            pdf_links = driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")
            print(f"Encontrados {len(pdf_links)} enlaces PDF")
            
            # Mostrar algunos títulos
            for i, row in enumerate(content_rows[:5]):
                try:
                    titulo = row.find_element(By.TAG_NAME, "td").text
                    print(f"\n{i+1}. {titulo[:100]}...")
                except:
                    pass
            
            # Guardar el HTML
            html = driver.page_source
            with open('selenium_output_21_07_2025.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("\nHTML guardado en selenium_output_21_07_2025.html")
            
            # Tomar screenshot
            driver.save_screenshot("diario_oficial_screenshot.png")
            print("Screenshot guardado en diario_oficial_screenshot.png")
            
        except Exception as e:
            print(f"Error buscando contenido: {str(e)}")
            
            # Guardar HTML de todas formas
            html = driver.page_source
            with open('selenium_error_output.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
    except Exception as e:
        print(f"Error general: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\nCerrando navegador...")
        driver.quit()

if __name__ == "__main__":
    scrape_diario_oficial_selenium()