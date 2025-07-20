#!/usr/bin/env python
"""
Script para probar diferentes números de edición para el 18 de julio
"""
import requests
from bs4 import BeautifulSoup

fecha = "18-07-2025"
base_url = "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/18"

# Probar un rango de ediciones posibles
# Basándonos en que el 17 fue 44200, probamos alrededor
ediciones_a_probar = [44201, 44202, 44203, 44204]

print(f"=== PROBANDO EDICIONES PARA EL {fecha} ===\n")

for edicion in ediciones_a_probar:
    url = f"{base_url}/edicion-{edicion}/"
    print(f"Probando edición {edicion}...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar indicadores de contenido
            publicaciones = soup.find_all('h5', class_='light')
            pdf_links = soup.find_all('a', href=lambda x: x and '.pdf' in x)
            
            print(f"  Status: {response.status_code} ✓")
            print(f"  Publicaciones encontradas: {len(publicaciones)}")
            print(f"  Enlaces PDF: {len(pdf_links)}")
            
            if publicaciones:
                print(f"  ÉXITO: Esta edición tiene contenido!")
                print(f"  Primeras publicaciones:")
                for i, pub in enumerate(publicaciones[:3], 1):
                    print(f"    {i}. {pub.text.strip()}")
                print(f"\n  ✓ EDICIÓN CORRECTA: {edicion}")
                break
            else:
                print(f"  Sin publicaciones visibles")
                
        else:
            print(f"  Status: {response.status_code} ✗")
            
    except Exception as e:
        print(f"  Error: {str(e)}")
    
    print()