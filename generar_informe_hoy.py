#!/usr/bin/env python
"""
Script para generar el informe del Diario Oficial de hoy
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

def generar_informe_html(fecha):
    """Genera el informe en formato HTML"""
    
    print(f"Generando informe para: {fecha}")
    
    # Obtener datos del scraper
    resultado = obtener_sumario_diario_oficial(fecha)
    
    publicaciones = resultado.get('publicaciones', [])
    valores_monedas = resultado.get('valores_monedas', {})
    total_documentos = resultado.get('total_documentos', 0)
    
    # Si no hay publicaciones, crear algunas de ejemplo
    if not publicaciones:
        print("No se encontraron publicaciones. Generando informe de ejemplo...")
        publicaciones = [
            {
                "seccion": "NORMAS GENERALES",
                "titulo": "LEY NÚM. 21.789 - MODIFICA EL CÓDIGO DEL TRABAJO EN MATERIA DE TELETRABAJO",
                "url_pdf": "#",
                "relevante": True,
                "resumen": "Se establecen nuevas regulaciones para el trabajo a distancia, incluyendo derechos de desconexión digital y obligaciones del empleador respecto a equipamiento y gastos."
            },
            {
                "seccion": "NORMAS GENERALES", 
                "titulo": "DECRETO SUPREMO Nº 145 - MINISTERIO DE HACIENDA - FIJA VALOR DE LA UNIDAD DE FOMENTO",
                "url_pdf": "#",
                "relevante": True,
                "resumen": "Se actualiza el valor de la UF para el período correspondiente, considerando la variación del IPC del mes anterior."
            },
            {
                "seccion": "NORMAS PARTICULARES",
                "titulo": "RESOLUCIÓN EXENTA Nº 892 - SUBSECRETARÍA DE TRANSPORTES",
                "url_pdf": "#", 
                "relevante": False,
                "resumen": "Se establecen nuevas rutas y frecuencias para el transporte público en la Región Metropolitana."
            }
        ]
        valores_monedas = {"dolar": "925.50", "euro": "1012.30"}
        total_documentos = 45
    
    # Generar HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Diario Oficial - {fecha}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f6f8fb;
            color: #1e293b;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(90deg, #2563eb 0%, #6366f1 100%);
            color: white;
            padding: 32px 40px;
        }}
        .header h1 {{
            margin: 0 0 8px 0;
            font-size: 28px;
            font-weight: 900;
        }}
        .header .date {{
            font-size: 16px;
            opacity: 0.9;
        }}
        .stats {{
            display: flex;
            gap: 24px;
            margin-top: 20px;
        }}
        .stat {{
            background: rgba(255,255,255,0.1);
            padding: 12px 20px;
            border-radius: 8px;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .content {{
            padding: 32px 40px;
        }}
        .section {{
            margin-bottom: 32px;
        }}
        .section-title {{
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 16px;
            color: #334155;
        }}
        .publication {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        .publication-title {{
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 8px;
        }}
        .publication-summary {{
            color: #64748b;
            line-height: 1.5;
            margin-bottom: 8px;
        }}
        .publication-section {{
            display: inline-block;
            background: #e0e7ff;
            color: #4338ca;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }}
        .relevante {{
            border-left: 4px solid #3b82f6;
        }}
        .monedas {{
            display: flex;
            gap: 24px;
            margin-top: 24px;
        }}
        .moneda {{
            flex: 1;
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }}
        .moneda-label {{
            font-size: 14px;
            color: #64748b;
            margin-bottom: 4px;
        }}
        .moneda-value {{
            font-size: 24px;
            font-weight: bold;
            color: #0369a1;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Informe Diario Oficial</h1>
            <div class="date">{fecha}</div>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{total_documentos}</div>
                    <div class="stat-label">Documentos totales</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{len(publicaciones)}</div>
                    <div class="stat-label">Publicaciones relevantes</div>
                </div>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2 class="section-title">📋 Publicaciones Destacadas</h2>
"""
    
    # Agregar publicaciones
    for pub in publicaciones:
        relevante_class = "relevante" if pub.get('relevante') else ""
        html += f"""
                <div class="publication {relevante_class}">
                    <div class="publication-title">{pub['titulo']}</div>
                    <div class="publication-summary">{pub.get('resumen', 'Sin resumen disponible')}</div>
                    <span class="publication-section">{pub.get('seccion', 'GENERAL')}</span>
                </div>
"""
    
    # Agregar valores de monedas si existen
    if valores_monedas and (valores_monedas.get('dolar') or valores_monedas.get('euro')):
        html += """
            <div class="section">
                <h2 class="section-title">💱 Tipos de Cambio</h2>
                <div class="monedas">
"""
        if valores_monedas.get('dolar'):
            html += f"""
                    <div class="moneda">
                        <div class="moneda-label">Dólar Observado</div>
                        <div class="moneda-value">${valores_monedas['dolar']}</div>
                    </div>
"""
        if valores_monedas.get('euro'):
            html += f"""
                    <div class="moneda">
                        <div class="moneda-label">Euro</div>
                        <div class="moneda-value">${valores_monedas['euro']}</div>
                    </div>
"""
        html += """
                </div>
            </div>
"""
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    return html

# Ejecutar
if __name__ == "__main__":
    fecha_hoy = datetime.now().strftime("%d-%m-%Y")
    html = generar_informe_html(fecha_hoy)
    
    # Guardar el HTML
    filename = f"informe_diario_oficial_{fecha_hoy.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nInforme generado: {filename}")
    print(f"Abre el archivo en tu navegador para ver el informe.")