#!/usr/bin/env python
"""
Script de depuración para el scraper del Diario Oficial
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

import requests
from bs4 import BeautifulSoup

def debug_diario_oficial():
    """Depura el acceso al Diario Oficial"""
    print("=== DEBUG DIARIO OFICIAL ===\n")
    
    # URL base
    base_url = "https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php"
    fecha = "10-07-2025"
    url = f"{base_url}?date={fecha}&edition=&v=1"
    
    print(f"URL: {url}")
    print("-" * 50)
    
    # Intentar con requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)} caracteres")
        
        # Analizar HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Buscar tablas
        tables = soup.find_all("table")
        print(f"\nTablas encontradas: {len(tables)}")
        
        # Buscar secciones válidas
        secciones_validas = ["NORMAS GENERALES", "NORMAS PARTICULARES"]
        for seccion in secciones_validas:
            elementos = soup.find_all(text=lambda text: text and seccion in text.upper())
            print(f"\nElementos con '{seccion}': {len(elementos)}")
        
        # Buscar enlaces PDF
        pdfs = soup.find_all("a", href=lambda href: href and href.endswith(".pdf"))
        print(f"\nEnlaces PDF encontrados: {len(pdfs)}")
        
        if pdfs:
            print("\nPrimeros 5 PDFs:")
            for i, pdf in enumerate(pdfs[:5]):
                print(f"  {i+1}. {pdf.get('href', 'N/A')}")
                parent = pdf.find_parent()
                if parent:
                    print(f"     Texto cercano: {parent.get_text(strip=True)[:100]}...")
        
        # Guardar HTML para inspección
        with open("debug_html.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("\nHTML guardado en debug_html.html para inspección manual")
        
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_diario_oficial()