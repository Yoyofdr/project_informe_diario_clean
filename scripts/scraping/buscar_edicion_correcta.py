#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

fecha = "17-07-2025"
BASE_URL = "https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php"

# Probar con diferentes números de edición
for edition in range(44200, 44205):
    url = f"{BASE_URL}?date={fecha}&edition={edition}"
    print(f"\nProbando edición {edition}...")
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Buscar el número de edición en la página
        edition_text = soup.find(text=lambda x: x and f"Edición Núm. {edition}" in x)
        if edition_text:
            print(f"✓ Edición {edition} corresponde al {fecha}")
            
        # Buscar publicaciones
        content_rows = soup.find_all('tr', class_='content')
        no_found = soup.find('p', class_='nofound')
        
        if content_rows:
            print(f"  → Encontradas {len(content_rows)} publicaciones")
            # Guardar este HTML
            with open(f'html_edicion_{edition}.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"  → HTML guardado como html_edicion_{edition}.html")
            break
        elif no_found:
            print(f"  → No hay publicaciones (mensaje: {no_found.text.strip()[:50]}...)")
        else:
            print(f"  → Estructura HTML diferente")
            
    except Exception as e:
        print(f"  → Error: {e}")

# También probar sin número de edición
print("\nProbando sin número de edición...")
url = f"{BASE_URL}?date={fecha}"
try:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    content_rows = soup.find_all('tr', class_='content')
    print(f"Publicaciones encontradas: {len(content_rows)}")
    if content_rows:
        with open('html_sin_edicion.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("HTML guardado como html_sin_edicion.html")
except Exception as e:
    print(f"Error: {e}")