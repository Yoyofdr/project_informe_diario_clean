#!/usr/bin/env python
"""
Script para generar el informe del 17 de julio con criterios más estrictos
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial

# Fecha objetivo
fecha = "17-07-2025"

print(f"\n=== Generando informe con criterios estrictos para: {fecha} ===\n")

# Obtener datos del scraper forzando actualización
resultado = obtener_sumario_diario_oficial(fecha, force_refresh=True)

publicaciones = resultado.get('publicaciones', [])
valores_monedas = resultado.get('valores_monedas', {})
total_documentos = resultado.get('total_documentos', 0)

print(f"\nTotal de documentos procesados: {total_documentos}")
print(f"Publicaciones que pasaron el filtro estricto: {len(publicaciones)}")

if publicaciones:
    print("\nPublicaciones incluidas en el informe:")
    for i, pub in enumerate(publicaciones, 1):
        print(f"\n{i}. {pub.get('titulo', 'Sin título')}")
        print(f"   Sección: {pub.get('seccion', 'Sin sección')}")
        if pub.get('resumen'):
            print(f"   Resumen: {pub['resumen'][:200]}...")

# Generar HTML del informe
html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Informe Diario Oficial - {fecha}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .publication {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .publication-title {{
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 10px;
        }}
        .publication-section {{
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 12px;
            border-radius: 4px;
            display: inline-block;
            font-size: 12px;
            margin-bottom: 10px;
        }}
        .summary {{
            color: #666;
            line-height: 1.5;
        }}
        .currency-info {{
            background: #fff3e0;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 40px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Informe Diario Oficial</h1>
        <h2>{fecha}</h2>
        <p>Edición con criterios de relevancia estrictos</p>
    </div>
"""

if valores_monedas:
    html += f"""
    <div class="currency-info">
        <h3>Valores de Referencia</h3>
        <p>Dólar: ${valores_monedas.get('dolar', 'N/A')}</p>
        <p>Euro: ${valores_monedas.get('euro', 'N/A')}</p>
    </div>
    """

if publicaciones:
    html += "<h3>Publicaciones Relevantes</h3>"
    for pub in publicaciones:
        html += f"""
        <div class="publication">
            <div class="publication-section">{pub.get('seccion', 'Sin sección')}</div>
            <div class="publication-title">{pub.get('titulo', 'Sin título')}</div>
            <div class="summary">{pub.get('resumen', 'Sin resumen disponible.')}</div>
        </div>
        """
else:
    html += """
    <div class="publication">
        <p>No se encontraron publicaciones que cumplan con los criterios estrictos de relevancia nacional.</p>
    </div>
    """

html += f"""
    <div class="footer">
        <p>Este informe incluye solo publicaciones de alcance nacional o de impacto significativo en sectores económicos completos.</p>
        <p>Total de documentos analizados: {total_documentos}</p>
    </div>
</body>
</html>
"""

# Guardar el HTML
filename = f"informe_estricto_{fecha.replace('-', '_')}.html"
with open(filename, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nInforme generado: {filename}")
print("Este informe usa criterios más estrictos de relevancia.")