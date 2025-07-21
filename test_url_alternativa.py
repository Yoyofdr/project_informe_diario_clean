#!/usr/bin/env python
"""
Script para probar URLs alternativas del Diario Oficial
"""
import requests
from bs4 import BeautifulSoup

# Probar diferentes URLs basadas en el patrón de URLs anteriores
urls_a_probar = [
    # URL directa con edición
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/01/2447764.pdf",
    # URL de la publicación por fecha
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/edicion-44204/",
    # URL base de publicaciones
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/",
    # URL con parámetros diferentes
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/21/44204/"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Referer': 'https://www.diariooficial.interior.gob.cl/'
}

for url in urls_a_probar:
    print(f"\nProbando: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        print(f"Status: {response.status_code}")
        print(f"URL final: {response.url}")
        
        if response.status_code == 200:
            if url.endswith('.pdf'):
                print("Es un PDF, tamaño:", len(response.content), "bytes")
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Buscar indicadores de contenido real
                title = soup.find('title')
                if title:
                    print(f"Título: {title.text.strip()}")
                
                # Buscar publicaciones
                publicaciones = soup.find_all(['a', 'div', 'tr'], text=lambda t: t and 'LEY' in t)
                if publicaciones:
                    print(f"Encontradas {len(publicaciones)} posibles publicaciones")
                
                # Guardar si parece tener contenido útil
                if len(response.text) > 5000 and 'TSPD' not in response.text[:1000]:
                    filename = f"test_html_{url.split('/')[-2]}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"HTML guardado en {filename}")
                    
    except Exception as e:
        print(f"Error: {str(e)}")