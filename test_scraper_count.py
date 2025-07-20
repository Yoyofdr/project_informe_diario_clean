#!/usr/bin/env python3
"""
Test para verificar que el scraper cuenta correctamente todos los documentos
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial

def test_document_count():
    """Test el conteo de documentos para el 19 de julio"""
    print("=== Test de conteo de documentos ===\n")
    
    fecha = "19-07-2025"
    print(f"Fecha: {fecha}")
    
    # Ejecutar el scraper
    resultado = obtener_sumario_diario_oficial(fecha, force_refresh=True)
    
    print(f"\nResultados del scraper:")
    print(f"- Total documentos reportados: {resultado.get('total_documentos', 0)}")
    print(f"- Publicaciones en sumario: {len(resultado.get('publicaciones', []))}")
    
    # Mostrar desglose por sección
    secciones = {}
    for pub in resultado.get('publicaciones', []):
        seccion = pub.get('seccion', 'Sin sección')
        if seccion not in secciones:
            secciones[seccion] = 0
        secciones[seccion] += 1
    
    print("\nPublicaciones por sección en el sumario:")
    for seccion, count in sorted(secciones.items()):
        print(f"  - {seccion}: {count}")

if __name__ == "__main__":
    test_document_count()