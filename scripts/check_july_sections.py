#!/usr/bin/env python3
"""
Check sections for specific July 2025 dates we know have data
"""

import requests
from bs4 import BeautifulSoup
import re

def analyze_complete_structure(fecha):
    """Analiza la estructura completa del Diario Oficial"""
    print(f"\n=== Analizando estructura para {fecha} ===")
    
    url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}"
    
    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 1. Buscar edición
        edition = None
        edition_select = soup.find('select', id='ediciones')
        if edition_select:
            selected = edition_select.find('option', selected=True)
            if selected and selected.get('value'):
                match = re.search(r'edicion-(\d+)', selected['value'])
                if match:
                    edition = match.group(1)
        
        if not edition:
            # Buscar en URL actual
            match = re.search(r'edition=(\d+)', response.text)
            if match:
                edition = match.group(1)
        
        print(f"Edición: {edition if edition else 'No encontrada'}")
        
        # 2. Analizar estructura de tablas
        print("\nEstructura de tablas:")
        all_tables = soup.find_all('table')
        for i, table in enumerate(all_tables):
            # Buscar encabezados de sección (celdas con bgcolor específico)
            headers = []
            for td in table.find_all('td'):
                bgcolor = td.get('bgcolor', '').upper()
                if bgcolor in ['#E0E0E0', '#CCCCCC', '#D0D0D0']:
                    texto = td.get_text(strip=True)
                    if texto and len(texto) < 100:
                        headers.append(texto)
            
            # Contar filas de contenido
            content_rows = table.find_all('tr', class_='content')
            
            if headers or content_rows:
                print(f"\n  Tabla {i+1}:")
                if headers:
                    print(f"    Encabezados encontrados:")
                    for h in headers:
                        print(f"      - {h}")
                if content_rows:
                    print(f"    Documentos: {len(content_rows)}")
                    # Mostrar primeros 2 documentos
                    for j, tr in enumerate(content_rows[:2]):
                        tds = tr.find_all('td')
                        if len(tds) >= 2:
                            titulo = tds[0].get_text(strip=True)[:60] + "..."
                            print(f"      Doc {j+1}: {titulo}")
        
        # 3. Buscar todas las posibles secciones
        print("\n\nTodas las secciones detectadas:")
        secciones = set()
        
        # Buscar en diferentes lugares
        for tag in soup.find_all(['td', 'th', 'b', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5']):
            texto = tag.get_text(strip=True).upper()
            # Patrones comunes de secciones
            if any(patron in texto for patron in ['NORMA', 'AVISO', 'MUNICIPALIDAD', 'EXTRACTO', 'NOTIFICACI']):
                if len(texto) < 50 and texto not in ['VER PDF']:
                    # Verificar si es un encabezado real (no parte de un título de documento)
                    parent = tag.parent
                    if parent and parent.name == 'td':
                        # Verificar si tiene bgcolor o colspan
                        if parent.get('bgcolor') or parent.get('colspan'):
                            secciones.add(texto)
                    elif tag.name in ['b', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5']:
                        secciones.add(texto)
        
        for seccion in sorted(secciones):
            print(f"  - {seccion}")
        
        # 4. Verificar avisos destacados
        if edition:
            url_avisos = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/avisos_destacados.php?date={fecha}&edition={edition}"
            try:
                resp = requests.get(url_avisos, timeout=30)
                if resp.status_code == 200:
                    soup_avisos = BeautifulSoup(resp.text, "html.parser")
                    avisos = sum(1 for row in soup_avisos.find_all('tr') if row.find('a', href=re.compile(r'\.pdf$')))
                    print(f"\nAvisos destacados (página separada): {avisos}")
            except:
                print("\nNo se pudo acceder a avisos destacados")
        
    except Exception as e:
        print(f"Error: {e}")

# Analizar fechas específicas de julio 2025
fechas_julio = [
    "19-07-2025",  # Sabemos que tiene datos
    "17-07-2025",
    "16-07-2025",
    "15-07-2025",
    "12-07-2025",
    "11-07-2025",
]

for fecha in fechas_julio:
    analyze_complete_structure(fecha)