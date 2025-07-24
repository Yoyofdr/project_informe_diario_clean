#!/usr/bin/env python
"""
Script para probar la detección automática de ediciones
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_numero_edicion

print("=== PRUEBA DE DETECCIÓN AUTOMÁTICA DE EDICIONES ===\n")

# Probar con el 18 de julio (no está en caché)
fecha = "18-07-2025"
print(f"Probando fecha: {fecha}")
print("Esta fecha NO está en el caché, por lo que se detectará automáticamente...\n")

edicion = obtener_numero_edicion(fecha)

print(f"\n✓ Edición detectada: {edicion}")

# Verificar si se actualizó el caché
import json
cache_file = os.path.join(os.path.dirname(__file__), 'edition_cache.json')
if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
        cache = json.load(f)
        if fecha in cache:
            print(f"✓ El caché fue actualizado automáticamente")
            print(f"  {fecha}: {cache[fecha]}")
        else:
            print("✗ El caché no fue actualizado")