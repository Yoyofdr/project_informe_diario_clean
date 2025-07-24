#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

fecha = "17-07-2025"
edition = "44202"
BASE_URL = "https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php"

url = f"{BASE_URL}?date={fecha}&edition={edition}&v=1"
print(f"URL generada: {url}")

# Hacer la petición
try:
    response = requests.get(url, timeout=30)
    print(f"\nStatus code: {response.status_code}")
    print(f"Content length: {len(response.text)}")
    
    # Analizar el HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Buscar elementos tr.content
    content_rows = soup.find_all('tr', class_='content')
    print(f"\nElementos tr.content encontrados: {len(content_rows)}")
    
    # Buscar avisos destacados
    avisos = soup.find_all('div', class_='aviso-destacado')
    print(f"Avisos destacados encontrados: {len(avisos)}")
    
    # Buscar cualquier enlace PDF
    pdf_links = soup.find_all('a', href=lambda x: x and '.pdf' in x)
    print(f"Enlaces PDF encontrados: {len(pdf_links)}")
    
    # Mostrar primeros 5 enlaces PDF si existen
    if pdf_links:
        print("\nPrimeros 5 enlaces PDF:")
        for i, link in enumerate(pdf_links[:5], 1):
            print(f"{i}. {link.get('href')}")
    
    # Guardar HTML para inspección
    with open('debug_17julio.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("\nHTML guardado en debug_17julio.html")
    
except Exception as e:
    print(f"Error: {e}")