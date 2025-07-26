#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial

# Obtener datos del Diario Oficial
resultado = obtener_sumario_diario_oficial('25-07-2025')

print('Total publicaciones:', len(resultado.get('publicaciones', [])))
print('\nPublicaciones por sección:')
for pub in resultado.get('publicaciones', []):
    seccion = pub.get('seccion', 'SIN SECCION')
    titulo = pub.get('titulo', '')[:60]
    print(f'- [{seccion}] {titulo}...')

print('\nValores de monedas:', resultado.get('valores_monedas'))
print('Total documentos:', resultado.get('total_documentos'))