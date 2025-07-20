#!/usr/bin/env python
"""
Script para probar los resúmenes más cortos
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')

# Cargar variables del .env
from dotenv import load_dotenv
load_dotenv()

django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial

# Probar con fecha actual
fecha = "18-07-2025"
print(f"Generando informe con resúmenes cortos para: {fecha}")

resultado = obtener_sumario_diario_oficial(fecha, force_refresh=True)

print("\n=== RESULTADOS ===")
print(f"Total documentos: {resultado.get('total_documentos', 0)}")
print(f"Publicaciones relevantes: {len(resultado.get('publicaciones', []))}")

print("\n=== RESÚMENES ===")
for i, pub in enumerate(resultado.get('publicaciones', []), 1):
    print(f"\n{i}. {pub.get('titulo', 'Sin título')[:80]}...")
    print(f"   Sección: {pub.get('seccion', 'Sin sección')}")
    resumen = pub.get('resumen', 'Sin resumen')
    print(f"   Resumen ({len(resumen.split())} palabras, {len(resumen)} caracteres):")
    print(f"   {resumen}")
    print("   " + "-"*60)