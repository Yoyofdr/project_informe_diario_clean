#!/usr/bin/env python
"""
Script para testear el scraping directo del Diario Oficial del 21 de julio
"""
import requests
from bs4 import BeautifulSoup
import json

# URL con el número de edición correcto
fecha = "21-07-2025"
edition = "44204"
url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}&v=1"

print(f"Probando URL: {url}")

try:
    # Hacer la petición
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar publicaciones
        publicaciones_encontradas = 0
        
        # Buscar en tr.content
        content_rows = soup.find_all('tr', class_='content')
        print(f"\nEncontrados {len(content_rows)} tr.content")
        
        # Buscar cualquier PDF
        pdfs = soup.find_all('a', href=lambda x: x and x.endswith('.pdf'))
        print(f"Encontrados {len(pdfs)} enlaces PDF")
        
        # Mostrar algunos títulos
        for i, tr in enumerate(content_rows[:5]):
            tds = tr.find_all('td')
            if len(tds) >= 2:
                titulo = tds[0].get_text(strip=True)
                print(f"\n{i+1}. {titulo[:100]}...")
        
        # Buscar valores de monedas
        for pdf in pdfs:
            texto = pdf.get_text(strip=True)
            if "TIPOS DE CAMBIO" in texto.upper():
                print(f"\nEncontrado certificado de monedas: {texto}")
        
        # Guardar HTML para inspección
        with open('diario_oficial_21_07_2025.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("\nHTML guardado en diario_oficial_21_07_2025.html")
        
    else:
        print(f"Error: Status code {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()