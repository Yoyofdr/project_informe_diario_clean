#!/usr/bin/env python
"""
Test rápido sin usar Selenium para obtener edición
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
import json

# Guardar temporalmente la función original
from alerts import scraper_diario_oficial
original_obtener_numero_edicion = scraper_diario_oficial.obtener_numero_edicion

# Reemplazar con una versión que solo usa el caché
def obtener_numero_edicion_simple(fecha, driver=None):
    # Caché hardcodeado
    editions = {
        "11-07-2025": "44196",
        "10-07-2025": "44195",
        "09-07-2025": "44194",
        "08-07-2025": "44193",
        "07-07-2025": "44192"
    }
    
    if fecha in editions:
        edition = editions[fecha]
        print(f"[EDITION-SIMPLE] Usando edición del caché: {edition}")
        return edition
    
    # Estimación simple
    from datetime import datetime
    base_date = datetime.strptime("07-07-2025", "%d-%m-%Y")
    base_edition = 44192
    
    try:
        target_date = datetime.strptime(fecha, "%d-%m-%Y")
        days_diff = (target_date - base_date).days
        estimated_edition = base_edition + days_diff
        print(f"[EDITION-SIMPLE] Usando edición estimada: {estimated_edition}")
        return str(estimated_edition)
    except:
        return ""

# Reemplazar la función
scraper_diario_oficial.obtener_numero_edicion = obtener_numero_edicion_simple

# Ahora ejecutar el scraper
print("=== TEST RÁPIDO DEL SCRAPER ===\n")
fecha = "11-07-2025"
print(f"Fecha: {fecha}")

resultado = obtener_sumario_diario_oficial(fecha)

if resultado:
    publicaciones = resultado.get('publicaciones', [])
    print(f"\nPublicaciones encontradas: {len(publicaciones)}")
    
    for i, pub in enumerate(publicaciones[:3], 1):
        print(f"\n{i}. {pub['titulo'][:100]}...")
        print(f"   Relevante: {pub.get('relevante')}")
else:
    print("\nNo se obtuvo resultado")

# Restaurar la función original
scraper_diario_oficial.obtener_numero_edicion = original_obtener_numero_edicion