#!/usr/bin/env python
"""
Script para generar el informe del Diario Oficial con diseño moderno
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
    """Genera el informe en formato HTML con diseño moderno y elegante"""
    
    print(f"Generando informe para: {fecha}")
    
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
    
    # HTML template moderno
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Diario Oficial - {fecha}</title>
    <style>
        /* Variables de diseño */
        :root {{
            --primary-color: #1a1a1a;
            --accent-color: #0066ff;
            --text-gray: #666;
            --border-gray: #e0e0e0;
            --bg-gray: #f8f8f8;
            --max-width: 800px;
        }}
        
        /* Reset y base */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: var(--primary-color);
            background-color: #fff;
        }}
        
        /* Contenedor principal */
        .container {{
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Header */
        .header {{
            padding: 60px 0 40px;
            text-align: center;
            position: relative;
        }}
        
        .header::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 2px;
            background: var(--accent-color);
        }}
        
        .header h1 {{
            font-size: 42px;
            font-weight: 300;
            letter-spacing: -1px;
            margin-bottom: 8px;
        }}
        
        .header .date {{
            font-size: 18px;
            color: var(--text-gray);
            font-weight: 400;
        }}
        
        /* Stats */
        .stats {{
            display: flex;
            justify-content: center;
            gap: 60px;
            margin: 50px 0;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 36px;
            font-weight: 700;
            color: var(--accent-color);
            display: block;
            line-height: 1;
            margin-bottom: 8px;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: var(--text-gray);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Secciones */
        .section {{
            margin: 60px 0;
        }}
        
        .section-header {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border-gray);
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: 600;
            letter-spacing: -0.5px;
        }}
        
        .section-count {{
            font-size: 14px;
            color: var(--text-gray);
            font-weight: 400;
        }}
        
        /* Publicaciones */
        .publication {{
            margin-bottom: 30px;
            padding: 25px;
            background: var(--bg-gray);
            border-radius: 8px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .publication:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }}
        
        .publication-title {{
            font-size: 18px;
            font-weight: 600;
            line-height: 1.4;
            margin-bottom: 12px;
            color: var(--primary-color);
        }}
        
        .publication-summary {{
            font-size: 15px;
            line-height: 1.7;
            color: var(--text-gray);
        }}
        
        /* Licitación badge */
        .licitacion-badge {{
            display: inline-block;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 4px 10px;
            background: var(--accent-color);
            color: white;
            border-radius: 4px;
            margin-left: 12px;
            vertical-align: middle;
        }}
        
        /* Valores de monedas */
        .currency-section {{
            margin: 80px 0 40px;
            padding: 40px;
            background: var(--primary-color);
            color: white;
            border-radius: 12px;
        }}
        
        .currency-title {{
            font-size: 20px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 30px;
            letter-spacing: -0.5px;
        }}
        
        .currency-values {{
            display: flex;
            justify-content: center;
            gap: 80px;
        }}
        
        .currency-item {{
            text-align: center;
        }}
        
        .currency-name {{
            font-size: 14px;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .currency-value {{
            font-size: 28px;
            font-weight: 700;
        }}
        
        /* Empty state */
        .empty-section {{
            text-align: center;
            padding: 100px 0;
            color: var(--text-gray);
        }}
        
        .empty-icon {{
            font-size: 64px;
            margin-bottom: 20px;
            opacity: 0.2;
        }}
        
        .empty-message {{
            font-size: 18px;
        }}
        
        /* Footer */
        .footer {{
            margin-top: 80px;
            padding: 40px 0;
            border-top: 1px solid var(--border-gray);
            text-align: center;
            font-size: 14px;
            color: var(--text-gray);
        }}
        
        /* Responsive */
        @media (max-width: 600px) {{
            .header h1 {{
                font-size: 32px;
            }}
            
            .stats {{
                flex-direction: column;
                gap: 30px;
            }}
            
            .stat-value {{
                font-size: 32px;
            }}
            
            .section-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }}
            
            .currency-values {{
                flex-direction: column;
                gap: 30px;
            }}
            
            .publication {{
                padding: 20px;
            }}
        }}
        
        /* Print styles */
        @media print {{
            body {{
                font-size: 12pt;
            }}
            
            .publication {{
                page-break-inside: avoid;
                background: none;
                border: 1px solid var(--border-gray);
            }}
            
            .currency-section {{
                background: none;
                border: 2px solid var(--primary-color);
                color: var(--primary-color);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>Informe Diario Oficial</h1>
            <div class="date">{formatear_fecha_espanol(fecha)}</div>
        </header>
        
        <div class="stats">
            <div class="stat">
                <span class="stat-value">{total_documentos}</span>
                <span class="stat-label">Documentos analizados</span>
            </div>
            <div class="stat">
                <span class="stat-value">{len(publicaciones)}</span>
                <span class="stat-label">Publicaciones relevantes</span>
            </div>
        </div>
        
        <main class="content">
"""
    
    # Si no hay publicaciones
    if not publicaciones:
        html += """
            <div class="empty-section">
                <div class="empty-icon">📄</div>
                <p class="empty-message">No se encontraron publicaciones relevantes para esta fecha.</p>
            </div>
"""
    else:
        # Agregar publicaciones por sección
        for seccion in orden_secciones:
            if seccion in publicaciones_por_seccion and publicaciones_por_seccion[seccion]:
                pubs = publicaciones_por_seccion[seccion]
                
                # Header de sección
                html += f"""
            <section class="section">
                <div class="section-header">
                    <h2 class="section-title">{seccion.title()}</h2>
                    <span class="section-count">{len(pubs)} publicacion{'es' if len(pubs) != 1 else ''}</span>
                </div>
"""
                
                # Publicaciones de la sección
                for pub in pubs:
                    es_licitacion = 'licitación' in pub.get('titulo', '').lower()
                    
                    html += f"""
                <article class="publication">
                    <h3 class="publication-title">
                        {pub.get('titulo', 'Sin título')}
                        {f'<span class="licitacion-badge">Licitación</span>' if es_licitacion else ''}
                    </h3>
                    <p class="publication-summary">
                        {pub.get('resumen') if pub.get('resumen') and pub.get('resumen') != 'No se pudo generar un resumen relevante.' else 'Resumen no disponible.'}
                    </p>
                </article>
"""
                
                html += """
            </section>
"""
        
        # Agregar secciones adicionales que no estén en el orden predefinido
        for seccion, pubs in publicaciones_por_seccion.items():
            if seccion not in orden_secciones and pubs:
                html += f"""
            <section class="section">
                <div class="section-header">
                    <h2 class="section-title">{seccion.title()}</h2>
                    <span class="section-count">{len(pubs)} publicacion{'es' if len(pubs) != 1 else ''}</span>
                </div>
"""
                for pub in pubs:
                    html += f"""
                <article class="publication">
                    <h3 class="publication-title">{pub.get('titulo', 'Sin título')}</h3>
                    <p class="publication-summary">
                        {pub.get('resumen') if pub.get('resumen') and pub.get('resumen') != 'No se pudo generar un resumen relevante.' else 'Resumen no disponible.'}
                    </p>
                </article>
"""
                html += """
            </section>
"""
    
    html += """
        </main>
"""
    
    # Agregar valores de monedas al final
    if valores_monedas:
        html += f"""
        <section class="currency-section">
            <h2 class="currency-title">Valores de Referencia del Día</h2>
            <div class="currency-values">
                <div class="currency-item">
                    <div class="currency-name">Dólar Observado</div>
                    <div class="currency-value">${valores_monedas.get('dolar', 'N/A')}</div>
                </div>
                <div class="currency-item">
                    <div class="currency-name">Euro</div>
                    <div class="currency-value">${valores_monedas.get('euro', 'N/A')}</div>
                </div>
            </div>
        </section>
"""
    
    html += """
        <footer class="footer">
            <p>Información obtenida directamente del sitio diariooficial.interior.gob.cl</p>
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
    filename = f"informe_moderno_{fecha_hoy.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nInforme generado: {filename}")
    print(f"Diseño moderno con valores de moneda al final")