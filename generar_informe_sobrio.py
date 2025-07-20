#!/usr/bin/env python
"""
Script para generar el informe del Diario Oficial con diseño sobrio y profesional
Estilo corporativo minimalista sin elementos decorativos
"""
import os
import sys
import django
from datetime import datetime
from collections import defaultdict
from utils_fecha import formatear_fecha_espanol

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial

def generar_informe_html(fecha):
    """Genera el informe en formato HTML con diseño sobrio y corporativo"""
    
    print(f"Generando informe sobrio para: {fecha}")
    
    # Obtener datos del scraper
    resultado = obtener_sumario_diario_oficial(fecha, force_refresh=True)
    
    publicaciones = resultado.get('publicaciones', [])
    valores_monedas = resultado.get('valores_monedas', {})
    total_documentos = resultado.get('total_documentos', 0)
    
    # Organizar publicaciones por sección
    publicaciones_por_seccion = defaultdict(list)
    for pub in publicaciones:
        seccion = pub.get('seccion', 'Sin sección').upper()
        
        # Normalizar nombres de secciones
        if 'NORMAS GENERALES' in seccion:
            seccion = 'NORMAS GENERALES'
        elif 'NORMAS PARTICULARES' in seccion:
            seccion = 'NORMAS PARTICULARES'
        elif 'AVISOS' in seccion or 'DESTACADO' in seccion:
            seccion = 'AVISOS DESTACADOS'
        
        publicaciones_por_seccion[seccion].append(pub)
    
    # Definir orden de secciones
    orden_secciones = ['NORMAS GENERALES', 'NORMAS PARTICULARES', 'AVISOS DESTACADOS']
    
    # HTML template sobrio y profesional
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Diario Oficial - {fecha}</title>
    <style>
        /* Reset */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        /* Base */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            font-size: 15px;
            line-height: 1.5;
            color: #2d3748;
            background-color: #ffffff;
        }}
        
        /* Container */
        .container {{
            max-width: 720px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        /* Header */
        .header {{
            border-bottom: 2px solid #2d3748;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 24px;
            font-weight: 400;
            color: #1a202c;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }}
        
        .header .date {{
            font-size: 14px;
            color: #718096;
            font-weight: 400;
        }}
        
        /* Summary */
        .summary {{
            background-color: #f7fafc;
            padding: 20px;
            margin-bottom: 40px;
            border: 1px solid #e2e8f0;
        }}
        
        .summary-title {{
            font-size: 13px;
            font-weight: 600;
            color: #4a5568;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }}
        
        .summary-stats {{
            display: flex;
            gap: 40px;
        }}
        
        .summary-item {{
            flex: 1;
        }}
        
        .summary-value {{
            font-size: 28px;
            font-weight: 300;
            color: #1a202c;
            line-height: 1;
        }}
        
        .summary-label {{
            font-size: 13px;
            color: #718096;
            margin-top: 4px;
        }}
        
        /* Sections */
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-header {{
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 8px;
            margin-bottom: 20px;
        }}
        
        .section-title {{
            font-size: 16px;
            font-weight: 600;
            color: #2d3748;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Publications */
        .publication {{
            margin-bottom: 24px;
            padding-left: 20px;
            border-left: 2px solid #e2e8f0;
        }}
        
        .publication-title {{
            font-size: 15px;
            font-weight: 500;
            color: #1a202c;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        
        .publication-summary {{
            font-size: 14px;
            color: #4a5568;
            line-height: 1.6;
        }}
        
        .badge {{
            display: inline-block;
            font-size: 11px;
            font-weight: 600;
            color: #2b6cb0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 2px 6px;
            border: 1px solid #2b6cb0;
            margin-left: 8px;
        }}
        
        /* Currency */
        .currency {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid #e2e8f0;
        }}
        
        .currency-title {{
            font-size: 13px;
            font-weight: 600;
            color: #4a5568;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
        }}
        
        .currency-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}
        
        .currency-item {{
            background-color: #f7fafc;
            padding: 16px;
            border: 1px solid #e2e8f0;
        }}
        
        .currency-name {{
            font-size: 12px;
            color: #718096;
            font-weight: 500;
            margin-bottom: 4px;
        }}
        
        .currency-value {{
            font-size: 20px;
            font-weight: 400;
            color: #1a202c;
        }}
        
        /* Footer */
        .footer {{
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
            font-size: 13px;
            color: #718096;
            text-align: center;
        }}
        
        /* Empty state */
        .empty {{
            text-align: center;
            padding: 60px 0;
            color: #718096;
            font-size: 15px;
        }}
        
        /* Print */
        @media print {{
            body {{
                font-size: 11pt;
            }}
            
            .container {{
                max-width: 100%;
                padding: 0;
            }}
            
            .publication {{
                page-break-inside: avoid;
            }}
            
            .currency {{
                page-break-before: always;
            }}
        }}
        
        /* Mobile */
        @media (max-width: 640px) {{
            .container {{
                padding: 20px 16px;
            }}
            
            .summary-stats {{
                flex-direction: column;
                gap: 16px;
            }}
            
            .currency-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>INFORME DIARIO OFICIAL</h1>
            <div class="date">{formatear_fecha_espanol(fecha)}</div>
        </header>
        
        <div class="summary">
            <div class="summary-title">Resumen Ejecutivo</div>
            <div class="summary-stats">
                <div class="summary-item">
                    <div class="summary-value">{total_documentos}</div>
                    <div class="summary-label">Documentos analizados</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{len(publicaciones)}</div>
                    <div class="summary-label">Publicaciones relevantes</div>
                </div>
            </div>
        </div>
"""
    
    if not publicaciones:
        html += """
        <div class="empty">
            No se encontraron publicaciones relevantes para esta fecha.
        </div>
"""
    else:
        # Agregar publicaciones por sección
        for seccion in orden_secciones:
            if seccion in publicaciones_por_seccion and publicaciones_por_seccion[seccion]:
                pubs = publicaciones_por_seccion[seccion]
                
                html += f"""
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">{seccion}</h2>
            </div>
"""
                
                for pub in pubs:
                    es_licitacion = 'licitación' in pub.get('titulo', '').lower()
                    
                    html += f"""
            <article class="publication">
                <h3 class="publication-title">
                    {pub.get('titulo', 'Sin título')}
                    {f'<span class="badge">Licitación</span>' if es_licitacion else ''}
                </h3>
                <p class="publication-summary">
                    {pub.get('resumen') if pub.get('resumen') and pub.get('resumen') != 'No se pudo generar un resumen relevante.' else 'Resumen no disponible.'}
                </p>
            </article>
"""
                
                html += """
        </section>
"""
    
    # Valores de monedas
    if valores_monedas:
        html += f"""
        <div class="currency">
            <div class="currency-title">Valores de Referencia</div>
            <div class="currency-grid">
                <div class="currency-item">
                    <div class="currency-name">DÓLAR OBSERVADO</div>
                    <div class="currency-value">${valores_monedas.get('dolar', 'N/A')}</div>
                </div>
                <div class="currency-item">
                    <div class="currency-name">EURO</div>
                    <div class="currency-value">${valores_monedas.get('euro', 'N/A')}</div>
                </div>
            </div>
        </div>
"""
    
    html += """
        <footer class="footer">
            Información obtenida directamente del sitio diariooficial.interior.gob.cl
        </footer>
    </div>
</body>
</html>
"""
    
    return html

# Ejecutar
if __name__ == "__main__":
    import sys
    
    # Permitir especificar fecha como argumento
    if len(sys.argv) > 1:
        fecha_hoy = sys.argv[1]
    else:
        fecha_hoy = "18-07-2025"
    
    html = generar_informe_html(fecha_hoy)
    
    # Guardar el HTML
    filename = f"informe_sobrio_{fecha_hoy.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nInforme generado: {filename}")
    print(f"Diseño sobrio y profesional con:")
    print("- Tipografía limpia sin decoraciones")
    print("- Paleta de grises neutros")
    print("- Sin emojis ni elementos gráficos")
    print("- Estructura clara y jerarquizada")
    print("- Estilo corporativo minimalista")