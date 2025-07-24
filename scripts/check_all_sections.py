#!/usr/bin/env python3
"""
Script para verificar todas las posibles secciones del Diario Oficial
en múltiples fechas para entender la estructura completa
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

def check_sections_comprehensive(fecha):
    """Verifica todas las secciones posibles de forma exhaustiva"""
    url_base = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}"
    
    try:
        response = requests.get(url_base, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Buscar TODAS las celdas con background="#E0E0E0" que suelen ser encabezados de sección
        secciones = set()
        
        # Estrategia 1: Buscar celdas con fondo gris (encabezados de sección)
        for td in soup.find_all('td', bgcolor="#E0E0E0"):
            texto = td.get_text(strip=True)
            if texto and len(texto) < 50:
                secciones.add(texto)
        
        # Estrategia 2: Buscar celdas con colspan que suelen ser encabezados
        for td in soup.find_all('td', colspan=True):
            texto = td.get_text(strip=True)
            if texto and len(texto) < 50 and any(word in texto.upper() for word in ['NORMA', 'AVISO', 'MUNICIPALIDAD', 'EXTRACTO']):
                secciones.add(texto)
        
        # Estrategia 3: Buscar texto en negrita que podría ser sección
        for tag in soup.find_all(['b', 'strong']):
            texto = tag.get_text(strip=True)
            if texto and len(texto) < 50 and texto.isupper():
                secciones.add(texto)
        
        # Contar documentos
        total_docs = len(soup.find_all('tr', class_='content'))
        
        # Buscar edición para avisos destacados
        edition_match = re.search(r'edition=(\d+)', response.text)
        avisos_count = 0
        if edition_match:
            edition = edition_match.group(1)
            url_avisos = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/avisos_destacados.php?date={fecha}&edition={edition}"
            try:
                resp_avisos = requests.get(url_avisos, timeout=30)
                if resp_avisos.status_code == 200:
                    soup_avisos = BeautifulSoup(resp_avisos.text, "html.parser")
                    avisos_count = sum(1 for row in soup_avisos.find_all('tr') if row.find('a', href=re.compile(r'\.pdf$')))
            except:
                pass
        
        return secciones, total_docs, avisos_count
        
    except Exception as e:
        return set(), 0, 0

def main():
    print("=== Análisis exhaustivo de secciones del Diario Oficial ===\n")
    
    todas_las_secciones = set()
    fechas_analizadas = []
    
    # Analizar últimos 10 días hábiles (usar fechas pasadas para asegurar datos)
    fecha_actual = datetime(2024, 12, 20)  # Fecha pasada con datos
    dias_analizados = 0
    
    while dias_analizados < 10:
        # Solo días hábiles
        if fecha_actual.weekday() < 5:  # Lunes a Viernes
            fecha_str = fecha_actual.strftime("%d-%m-%Y")
            print(f"\nAnalizando {fecha_str}...")
            
            secciones, docs_main, docs_avisos = check_sections_comprehensive(fecha_str)
            
            if secciones:
                print(f"  Documentos: {docs_main} (principal) + {docs_avisos} (avisos) = {docs_main + docs_avisos}")
                print(f"  Secciones encontradas:")
                for seccion in sorted(secciones):
                    print(f"    - {seccion}")
                    todas_las_secciones.add(seccion)
                fechas_analizadas.append((fecha_str, docs_main + docs_avisos))
            else:
                print(f"  Sin datos disponibles")
            
            dias_analizados += 1
        
        fecha_actual -= timedelta(days=1)
    
    print("\n" + "="*60)
    print("\n=== RESUMEN DE TODAS LAS SECCIONES ENCONTRADAS ===")
    
    # Categorizar secciones
    normas = []
    avisos = []
    municipalidades = []
    otros = []
    
    for seccion in sorted(todas_las_secciones):
        seccion_upper = seccion.upper()
        if 'NORMA' in seccion_upper:
            normas.append(seccion)
        elif 'AVISO' in seccion_upper:
            avisos.append(seccion)
        elif 'MUNICIPALIDAD' in seccion_upper:
            municipalidades.append(seccion)
        else:
            otros.append(seccion)
    
    if normas:
        print("\nNORMAS:")
        for n in normas:
            print(f"  - {n}")
    
    if avisos:
        print("\nAVISOS:")
        for a in avisos:
            print(f"  - {a}")
    
    if municipalidades:
        print("\nMUNICIPALIDADES:")
        for m in municipalidades:
            print(f"  - {m}")
    
    if otros:
        print("\nOTROS:")
        for o in otros:
            print(f"  - {o}")
    
    print("\n=== ESTADÍSTICAS DE DOCUMENTOS ===")
    if fechas_analizadas:
        total_docs = sum(docs for _, docs in fechas_analizadas)
        promedio = total_docs / len(fechas_analizadas)
        print(f"\nPromedio de documentos por día: {promedio:.1f}")
        print(f"Rango: {min(docs for _, docs in fechas_analizadas)} - {max(docs for _, docs in fechas_analizadas)}")

if __name__ == "__main__":
    main()