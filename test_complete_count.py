#!/usr/bin/env python3
"""
Test completo del conteo por secciones
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial

def test_complete_count():
    """Test el conteo completo por secciones"""
    fechas = [
        "19-07-2025",
        "17-07-2025", 
        "15-07-2025"
    ]
    
    for fecha in fechas:
        print(f"\n{'='*60}")
        print(f"Fecha: {fecha}")
        print('='*60)
        
        # Ejecutar el scraper
        resultado = obtener_sumario_diario_oficial(fecha, force_refresh=True)
        
        print(f"\nTotal documentos: {resultado.get('total_documentos', 0)}")
        
        # Contar por sección desde todas las publicaciones
        # (no solo las del sumario final)
        print("\nDesglose esperado basado en los logs anteriores:")
        if fecha == "19-07-2025":
            print("  - Normas Generales: 8")
            print("  - Normas Particulares: 5") 
            print("  - Avisos Destacados: 7")
            print("  - Total esperado: 20")
        elif fecha == "17-07-2025":
            print("  - Normas Generales: 22")
            print("  - Normas Particulares: 44")
            print("  - Avisos Destacados: 16")
            print("  - Total esperado: 82")
        elif fecha == "15-07-2025":
            print("  - Normas Generales: 4")
            print("  - Normas Particulares: 300")
            print("  - Avisos Destacados: 56")
            print("  - Total esperado: 360")

if __name__ == "__main__":
    test_complete_count()