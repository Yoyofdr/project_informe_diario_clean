#!/usr/bin/env python
"""
Script para verificar el 18 de julio sin especificar edición
"""
import requests
from bs4 import BeautifulSoup

# Probar sin especificar edición
url = "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/18/"

print(f"=== VERIFICANDO {url} ===\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
    print(f"Content Length: {len(response.text)} caracteres")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar título de la página
        title = soup.find('title')
        if title:
            print(f"\nTítulo de la página: {title.text.strip()}")
        
        # Buscar el selector de ediciones
        edition_select = soup.find('select', {'id': 'ediciones'})
        if edition_select:
            print(f"\n✓ Selector de ediciones encontrado!")
            options = edition_select.find_all('option')
            print(f"Ediciones disponibles: {len(options)}")
            for opt in options[:5]:
                value = opt.get('value', '')
                text = opt.text.strip()
                selected = 'selected' in opt.attrs
                marker = " [SELECCIONADA]" if selected else ""
                print(f"  - {value}: {text}{marker}")
        else:
            print("\n✗ No se encontró selector de ediciones")
        
        # Buscar publicaciones de diferentes formas
        print("\nBuscando publicaciones...")
        
        # Método 1: h5.light
        h5_light = soup.find_all('h5', class_='light')
        print(f"  h5.light: {len(h5_light)} encontradas")
        
        # Método 2: Enlaces PDF
        pdf_links = [a for a in soup.find_all('a', href=True) if '.pdf' in a['href']]
        print(f"  Enlaces PDF: {len(pdf_links)}")
        
        # Método 3: Divs con clase 'publication' o similar
        divs_pub = soup.find_all('div', class_=lambda x: x and 'public' in x.lower() if x else False)
        print(f"  Divs con 'public': {len(divs_pub)}")
        
        # Buscar contenido del diario
        content_divs = soup.find_all('div', class_='content')
        print(f"  Divs de contenido: {len(content_divs)}")
        
        # Si encontramos publicaciones, mostrar algunas
        if h5_light:
            print("\nPrimeras publicaciones encontradas:")
            for i, pub in enumerate(h5_light[:3], 1):
                print(f"  {i}. {pub.text.strip()}")
        
        # Guardar HTML para análisis
        with open('debug_18julio_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("\n✓ HTML guardado en debug_18julio_response.html para análisis")
        
    else:
        print(f"\n✗ Error HTTP: {response.status_code}")
        print(f"Razón: {response.reason}")
        
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    print(f"Tipo de error: {type(e).__name__}")