#!/usr/bin/env python
import sys
import os
from datetime import datetime

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar solo las funciones necesarias
from alerts.scraper_diario_oficial import (
    es_licitacion_publica, 
    LICITACION_KEYWORDS,
    extraer_avisos_destacados_tabla
)

def test_deteccion_licitaciones():
    """Prueba la detección de licitaciones en diferentes títulos"""
    
    print("="*60)
    print("PRUEBA DE DETECCIÓN DE LICITACIONES")
    print("="*60)
    
    # Casos de prueba
    casos_prueba = [
        "Extracto de resolución número 2, de 2025.- Aprueba Bases de Licitación y sus Anexos para la Concesión del Uso de las Vías de las Unidades de Servicios N°s 20, 21 y 22",
        "Llamado a Licitación Pública para construcción de hospital",
        "Decreto número 57, de 2024.- Fija fórmulas tarifarias",
        "Concurso público para cargo de Director",
        "Resolución de nombramiento de funcionario",
        "Bases de licitación para proyecto vial",
        "Licitación de obras públicas",
        "Extracto de contrato de suministro"
    ]
    
    print("\nPalabras clave configuradas:")
    for kw in LICITACION_KEYWORDS:
        print(f"  - {kw}")
    
    print("\n\nResultados de detección:")
    print("-"*60)
    
    for titulo in casos_prueba:
        es_licitacion = es_licitacion_publica(titulo)
        print(f"\nTítulo: {titulo}")
        print(f"¿Es licitación? {'SÍ' if es_licitacion else 'NO'}")
        
        # Mostrar qué palabra clave coincidió
        if es_licitacion:
            titulo_lower = titulo.lower()
            coincidencias = [kw for kw in LICITACION_KEYWORDS if kw in titulo_lower]
            print(f"Coincidencias: {', '.join(coincidencias)}")

def test_html_real():
    """Prueba con HTML real del Diario Oficial"""
    print("\n\n" + "="*60)
    print("PRUEBA CON HTML REAL")
    print("="*60)
    
    # HTML de ejemplo con la estructura real
    html_ejemplo = '''
    <tr class="content">
        <td>Extracto de resolución número 2, de 2025.- Aprueba Bases de Licitación y sus Anexos para la Concesión del Uso de las Vías de las Unidades de Servicios N°s 20, 21 y 22 <span class="border dotted"></span></td>
        <td><a target="_blank" href="https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/11/44196/01/2671475.pdf" title="">Ver PDF (CVE-2671475)</a><span class="border dotted"></span></td>
    </tr>
    '''
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_ejemplo, 'html.parser')
    
    avisos = extraer_avisos_destacados_tabla(soup)
    
    print(f"\nAvisos de licitación encontrados: {len(avisos)}")
    for aviso in avisos:
        print(f"\nTítulo: {aviso['titulo']}")
        print(f"URL: {aviso['url_pdf']}")
        print(f"Relevante: {aviso['relevante']}")

if __name__ == "__main__":
    test_deteccion_licitaciones()
    test_html_real()