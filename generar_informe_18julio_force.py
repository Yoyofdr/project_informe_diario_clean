#!/usr/bin/env python
"""
Script para generar el informe del 18 de julio con force_refresh
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial, obtener_numero_edicion
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Primero, intentar obtener el número de edición correcto
fecha = "18-07-2025"
print(f"=== GENERANDO INFORME DEL {fecha} ===\n")

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

driver = None
try:
    driver = webdriver.Chrome(options=chrome_options)
    
    # Obtener número de edición
    print("Buscando número de edición...")
    numero_edicion = obtener_numero_edicion(fecha, driver)
    print(f"Número de edición encontrado: {numero_edicion}")
    
finally:
    if driver:
        driver.quit()

# Ahora obtener el sumario con el número de edición correcto
print("\nObteniendo sumario del Diario Oficial...")
resultado = obtener_sumario_diario_oficial(fecha, force_refresh=True)

publicaciones = resultado.get('publicaciones', [])
valores_monedas = resultado.get('valores_monedas', {})
total_documentos = resultado.get('total_documentos', 0)

print(f"\nResultados:")
print(f"- Total documentos: {total_documentos}")
print(f"- Publicaciones relevantes: {len(publicaciones)}")
print(f"- Valores monedas: {valores_monedas}")

if publicaciones:
    print(f"\nPublicaciones encontradas:")
    for i, pub in enumerate(publicaciones, 1):
        print(f"\n{i}. {pub.get('titulo', 'Sin título')}")
        print(f"   Sección: {pub.get('seccion', 'Sin sección')}")
        if pub.get('resumen'):
            print(f"   Resumen: {pub['resumen'][:200]}...")

# Generar el informe HTML
from generar_informe_secciones import generar_informe_html

html = generar_informe_html(fecha)

# Guardar el HTML
filename = f"informe_secciones_{fecha.replace('-', '_')}.html"
with open(filename, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✓ Informe generado: {filename}")