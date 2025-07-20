#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_avisos_destacados

fecha = "17-07-2025"
edition = "44202"

print(f"\n=== Probando avisos destacados para {fecha} ===\n")

avisos = obtener_avisos_destacados(fecha, edition)

print(f"Total de avisos encontrados: {len(avisos)}")

if avisos:
    print("\nPrimeros 5 avisos:")
    for i, aviso in enumerate(avisos[:5], 1):
        print(f"\n{i}. {aviso.get('titulo', 'Sin título')}")
        print(f"   Sección: {aviso.get('seccion', 'Sin sección')}")
        print(f"   URL PDF: {aviso.get('url_pdf', 'Sin URL')}")
else:
    print("\nNo se encontraron avisos destacados.")