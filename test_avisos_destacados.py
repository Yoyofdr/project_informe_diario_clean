#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def explorar_avisos_destacados(fecha="12-07-2025", edition="44197"):
    """Explora las diferentes formas de acceder a avisos destacados"""
    
    print(f"Explorando avisos destacados para {fecha} (edición {edition})")
    print("="*80)
    
    # URLs a probar
    urls = [
        f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}",
        f"https://www.diariooficial.interior.gob.cl/edicionelectronica/avisos_destacados.php?date={fecha}&edition={edition}",
        f"https://www.diariooficial.interior.gob.cl/avisos_destacados.php?date={fecha}&edition={edition}",
    ]
    
    for url in urls:
        print(f"\n\nProbando URL: {url}")
        print("-"*80)
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Buscar sección de avisos destacados
                print("\n--- Buscando 'AVISOS DESTACADOS' en el HTML ---")
                
                # Buscar en diferentes tipos de elementos
                for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'b', 'strong', 'td', 'th', 'div']:
                    elementos = soup.find_all(tag)
                    for elem in elementos:
                        texto = elem.get_text(strip=True)
                        if 'AVISOS DESTACADOS' in texto.upper():
                            print(f"Encontrado en <{tag}>: {texto}")
                            
                            # Buscar contenido cercano
                            parent = elem.parent
                            if parent:
                                # Buscar tabla o contenedor cercano
                                tabla = parent.find_next('table')
                                if tabla:
                                    print("\n--- Contenido de la tabla de avisos ---")
                                    filas = tabla.find_all('tr')
                                    for i, fila in enumerate(filas[:10]):  # Primeras 10 filas
                                        print(f"\nFila {i+1}:")
                                        celdas = fila.find_all(['td', 'th'])
                                        for celda in celdas:
                                            texto_celda = celda.get_text(strip=True)
                                            if texto_celda:
                                                print(f"  - {texto_celda[:100]}...")
                                            # Buscar enlaces
                                            enlaces = celda.find_all('a', href=True)
                                            for enlace in enlaces:
                                                print(f"    Link: {enlace['href']}")
                
                # Buscar licitaciones en todo el HTML
                print("\n--- Buscando 'LICITACIÓN' en todo el HTML ---")
                texto_completo = soup.get_text().lower()
                if 'licitación' in texto_completo:
                    print("¡Se encontró la palabra 'licitación'!")
                    
                    # Buscar en todas las filas
                    todas_filas = soup.find_all('tr')
                    for fila in todas_filas:
                        texto_fila = fila.get_text(strip=True)
                        if 'licitación' in texto_fila.lower():
                            print(f"\nFila con licitación: {texto_fila[:200]}...")
                            enlaces = fila.find_all('a', href=True)
                            for enlace in enlaces:
                                if enlace['href'].endswith('.pdf'):
                                    print(f"  PDF: {enlace['href']}")
                
                # Buscar enlaces a la sección de avisos destacados
                print("\n--- Buscando enlaces a avisos_destacados.php ---")
                enlaces_avisos = soup.find_all('a', href=lambda x: x and 'avisos_destacados' in x)
                for enlace in enlaces_avisos:
                    print(f"Enlace encontrado: {enlace['href']} - Texto: {enlace.get_text(strip=True)}")
                
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    explorar_avisos_destacados()