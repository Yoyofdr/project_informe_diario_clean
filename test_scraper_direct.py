#!/usr/bin/env python
"""
Test directo del scraper con el número de edición conocido
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

import requests
from bs4 import BeautifulSoup
import time

def test_direct_scraping():
    print("=== TEST DIRECTO DE SCRAPING ===\n")
    
    fecha = "11-07-2025"
    edition = "44196"  # Número de edición que encontramos
    
    # URL directa con el número de edición
    url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}&v=1"
    
    print(f"URL: {url}")
    print("-" * 50)
    
    # Intentar primero con requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Referer': 'https://www.diariooficial.interior.gob.cl/edicionelectronica/select_edition.php'
    }
    
    try:
        print("Intentando con requests...")
        session = requests.Session()
        
        # Primero visitar la página de selección
        select_url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/select_edition.php?date={fecha}"
        session.get(select_url, headers=headers)
        time.sleep(1)
        
        # Luego la página principal
        response = session.get(url, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Longitud HTML: {len(response.text)}")
        
        if "NORMAS" in response.text.upper():
            print("✓ Contenido de NORMAS encontrado!")
        else:
            print("✗ No se encontró contenido de NORMAS")
            
        # Analizar con BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Buscar PDFs
        pdfs = soup.find_all("a", href=lambda x: x and x.endswith(".pdf"))
        print(f"\nPDFs encontrados: {len(pdfs)}")
        
        if pdfs:
            print("\nPrimeros 5 PDFs:")
            for i, pdf in enumerate(pdfs[:5]):
                print(f"{i+1}. {pdf.get('href')}")
                
    except Exception as e:
        print(f"Error con requests: {e}")
        
    # Si requests no funciona, probar con Selenium
    print("\n" + "="*50)
    print("Probando con Selenium undetected...")
    
    try:
        import undetected_chromedriver as uc
        
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = uc.Chrome(options=options)
        driver.set_page_load_timeout(30)
        
        print(f"Navegando a: {url}")
        driver.get(url)
        
        print("Esperando 5 segundos...")
        time.sleep(5)
        
        html = driver.page_source
        print(f"Longitud HTML: {len(html)}")
        
        if "NORMAS" in html.upper():
            print("✓ Contenido de NORMAS encontrado!")
            
            # Guardar HTML para análisis
            with open("diario_oficial_content.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("HTML guardado en: diario_oficial_content.html")
            
            # Contar PDFs
            soup = BeautifulSoup(html, "html.parser")
            pdfs = soup.find_all("a", href=lambda x: x and x.endswith(".pdf"))
            print(f"\nPDFs encontrados: {len(pdfs)}")
            
            if pdfs:
                print("\nPrimeros 5 PDFs:")
                for i, pdf in enumerate(pdfs[:5]):
                    href = pdf.get('href')
                    text = pdf.text or pdf.find_parent().text
                    print(f"{i+1}. {href}")
                    print(f"   Texto: {text[:80]}...")
                    
        else:
            print("✗ No se encontró contenido de NORMAS")
            print("Primeros 500 caracteres del HTML:")
            print(html[:500])
            
        driver.quit()
        
    except Exception as e:
        print(f"Error con Selenium: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_scraping()