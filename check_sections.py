#!/usr/bin/env python3
"""
Script para verificar todas las secciones presentes en el Diario Oficial
y contar documentos por sección
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def check_sections_for_date(fecha):
    """Verifica todas las secciones y cuenta documentos"""
    print(f"\n=== Verificando secciones para {fecha} ===\n")
    
    # URL base sin edición
    url_base = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}"
    
    print(f"URL: {url_base}")
    
    try:
        response = requests.get(url_base, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Buscar todas las secciones posibles
        secciones_encontradas = set()
        documentos_por_seccion = {}
        total_documentos = 0
        
        # Estrategia 1: Buscar en encabezados (th, td con estilo especial)
        print("\n1. Buscando secciones en encabezados...")
        for tag in soup.find_all(['th', 'td', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            texto = tag.get_text(strip=True)
            # Detectar patrones de sección
            if any(palabra in texto.upper() for palabra in ['NORMA', 'AVISO', 'MUNICIPALIDAD', 'LICITACI', 'EXTRACTO', 'NOTIFICACI']):
                if len(texto) < 100:  # Evitar títulos de documentos largos
                    secciones_encontradas.add(texto)
                    print(f"   - Posible sección: {texto}")
        
        # Estrategia 2: Buscar todas las filas tr.content y analizar su contexto
        print("\n2. Analizando documentos por tabla...")
        all_tables = soup.find_all('table')
        
        for i, table in enumerate(all_tables):
            rows_content = table.find_all('tr', class_='content')
            if rows_content:
                print(f"\n   Tabla {i+1}: {len(rows_content)} documentos")
                
                # Buscar encabezado de sección antes de esta tabla
                seccion_actual = "Sin clasificar"
                prev_element = table.find_previous(['td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5'])
                if prev_element:
                    texto_prev = prev_element.get_text(strip=True)
                    if len(texto_prev) < 50:
                        seccion_actual = texto_prev
                
                if seccion_actual not in documentos_por_seccion:
                    documentos_por_seccion[seccion_actual] = 0
                
                documentos_por_seccion[seccion_actual] += len(rows_content)
                total_documentos += len(rows_content)
                
                # Mostrar primeros documentos de esta sección
                for j, tr in enumerate(rows_content[:3]):
                    tds = tr.find_all('td')
                    if len(tds) >= 2:
                        titulo = tds[0].get_text(strip=True)[:80] + "..."
                        print(f"      Doc {j+1}: {titulo}")
        
        # Estrategia 3: Buscar patrones específicos en el HTML
        print("\n3. Buscando patrones específicos...")
        
        # Buscar avisos destacados
        avisos_link = soup.find('a', string=re.compile('avisos destacados', re.I))
        if avisos_link:
            print("   - Encontrado enlace a 'Avisos Destacados'")
            secciones_encontradas.add("AVISOS DESTACADOS")
        
        # Buscar municipalidades
        for text in soup.stripped_strings:
            if 'MUNICIPALIDAD' in text.upper() and len(text) < 50:
                secciones_encontradas.add(text)
        
        # Resumen
        print("\n=== RESUMEN ===")
        print(f"\nTotal de documentos encontrados: {total_documentos}")
        
        print("\nDocumentos por sección:")
        for seccion, count in sorted(documentos_por_seccion.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {seccion}: {count} documentos")
        
        print("\nTodas las secciones detectadas:")
        for seccion in sorted(secciones_encontradas):
            print(f"   - {seccion}")
        
        # Verificar si hay página de avisos destacados
        print("\n4. Verificando página de avisos destacados...")
        # Buscar edición en el HTML actual
        edition_match = re.search(r'edition=(\d+)', response.text)
        if edition_match:
            edition = edition_match.group(1)
            url_avisos = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/avisos_destacados.php?date={fecha}&edition={edition}"
            print(f"   URL avisos: {url_avisos}")
            
            try:
                resp_avisos = requests.get(url_avisos, timeout=30)
                if resp_avisos.status_code == 200:
                    soup_avisos = BeautifulSoup(resp_avisos.text, "html.parser")
                    avisos_rows = soup_avisos.find_all('tr')
                    avisos_count = sum(1 for row in avisos_rows if row.find('a', href=re.compile(r'\.pdf$')))
                    print(f"   Avisos destacados encontrados: {avisos_count}")
                    total_documentos += avisos_count
            except:
                print("   No se pudo acceder a la página de avisos destacados")
        
        print(f"\n=== TOTAL FINAL: {total_documentos} documentos ===")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Verificar fecha actual
    fecha_hoy = datetime.now().strftime("%d-%m-%Y")
    check_sections_for_date(fecha_hoy)
    
    # También verificar 18 de julio
    print("\n" + "="*60)
    check_sections_for_date("18-07-2025")