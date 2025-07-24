#!/usr/bin/env python
"""
Script para generar el informe del Diario Oficial con diseño tipo The Morning Brew / Axios
Diseño profesional de newsletter moderna
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
    """Genera el informe en formato HTML con diseño tipo newsletter moderna"""
    
    print(f"Generando informe newsletter para: {fecha}")
    
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
    
    # Definir orden de secciones con emojis
    secciones_config = {
        'NORMAS GENERALES': {'emoji': '⚖️', 'color': '#059669'},
        'NORMAS PARTICULARES': {'emoji': '📋', 'color': '#7c3aed'},
        'AVISOS DESTACADOS': {'emoji': '📢', 'color': '#dc2626'}
    }
    
    # HTML template tipo newsletter moderna
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Diario Oficial • {fecha}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f9fafb;
            color: #111827;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        .wrapper {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 48px 32px;
            text-align: center;
        }}
        
        .logo {{
            font-size: 32px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -1px;
            margin-bottom: 8px;
        }}
        
        .date {{
            color: #cbd5e1;
            font-size: 14px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* Quick Stats */
        .stats-container {{
            padding: 24px 32px;
            background-color: #f1f5f9;
            display: flex;
            justify-content: space-around;
            border-bottom: 3px solid #e2e8f0;
        }}
        
        .stat {{
            text-align: center;
            flex: 1;
        }}
        
        .stat-number {{
            font-size: 36px;
            font-weight: 700;
            color: #1e293b;
            line-height: 1;
        }}
        
        .stat-label {{
            font-size: 12px;
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }}
        
        /* Main Content */
        .content {{
            padding: 32px;
        }}
        
        /* Section Headers */
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid #e5e7eb;
        }}
        
        .section-emoji {{
            font-size: 24px;
            margin-right: 12px;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 700;
            color: #1f2937;
            flex: 1;
        }}
        
        .section-count {{
            font-size: 14px;
            color: #6b7280;
            font-weight: 500;
        }}
        
        /* Publications */
        .publication {{
            background-color: #f9fafb;
            border-left: 4px solid #e5e7eb;
            padding: 20px;
            margin-bottom: 16px;
            transition: all 0.3s ease;
        }}
        
        .publication:hover {{
            border-left-color: #3b82f6;
            background-color: #f3f4f6;
        }}
        
        .pub-title {{
            font-size: 16px;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        
        .pub-summary {{
            font-size: 14px;
            color: #4b5563;
            line-height: 1.6;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-radius: 4px;
            margin-left: 8px;
        }}
        
        .badge-licitacion {{
            background-color: #dbeafe;
            color: #1e40af;
        }}
        
        /* Currency Section */
        .currency-section {{
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            padding: 32px;
            margin: 32px;
            border-radius: 12px;
            text-align: center;
        }}
        
        .currency-title {{
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .currency-grid {{
            display: flex;
            justify-content: center;
            gap: 48px;
        }}
        
        .currency-item {{
            background-color: rgba(255, 255, 255, 0.2);
            padding: 16px 24px;
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }}
        
        .currency-name {{
            font-size: 12px;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.9);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }}
        
        .currency-value {{
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
        }}
        
        /* Empty State */
        .empty-state {{
            text-align: center;
            padding: 60px 32px;
        }}
        
        .empty-icon {{
            font-size: 48px;
            margin-bottom: 16px;
            opacity: 0.3;
        }}
        
        .empty-text {{
            font-size: 16px;
            color: #6b7280;
        }}
        
        /* Footer */
        .footer {{
            background-color: #f3f4f6;
            padding: 32px;
            text-align: center;
            border-top: 1px solid #e5e7eb;
        }}
        
        .footer-text {{
            font-size: 13px;
            color: #6b7280;
            line-height: 1.5;
        }}
        
        .divider {{
            height: 1px;
            background-color: #e5e7eb;
            margin: 32px 0;
        }}
        
        /* Responsive */
        @media (max-width: 600px) {{
            .header {{
                padding: 32px 20px;
            }}
            
            .logo {{
                font-size: 28px;
            }}
            
            .stats-container {{
                padding: 20px;
            }}
            
            .stat-number {{
                font-size: 28px;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .currency-grid {{
                flex-direction: column;
                gap: 16px;
            }}
            
            .currency-section {{
                margin: 20px;
                padding: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <!-- Header -->
        <div class="header">
            <div class="logo">📰 Diario Oficial</div>
            <div class="date">{formatear_fecha_espanol(fecha).upper()}</div>
        </div>
        
        <!-- Quick Stats -->
        <div class="stats-container">
            <div class="stat">
                <div class="stat-number">{total_documentos}</div>
                <div class="stat-label">Analizados</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(publicaciones)}</div>
                <div class="stat-label">Relevantes</div>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="content">
"""
    
    if not publicaciones:
        html += """
            <div class="empty-state">
                <div class="empty-icon">📄</div>
                <div class="empty-text">No se encontraron publicaciones relevantes para esta fecha.</div>
            </div>
"""
    else:
        # Agregar publicaciones por sección
        first_section = True
        for seccion, config in secciones_config.items():
            if seccion in publicaciones_por_seccion and publicaciones_por_seccion[seccion]:
                pubs = publicaciones_por_seccion[seccion]
                
                if not first_section:
                    html += '<div class="divider"></div>\n'
                first_section = False
                
                html += f"""
            <div class="section">
                <div class="section-header">
                    <span class="section-emoji">{config['emoji']}</span>
                    <h2 class="section-title">{seccion.title()}</h2>
                    <span class="section-count">{len(pubs)}</span>
                </div>
"""
                
                for pub in pubs:
                    es_licitacion = 'licitación' in pub.get('titulo', '').lower()
                    
                    html += f"""
                <div class="publication" style="border-left-color: {config['color']};">
                    <h3 class="pub-title">
                        {pub.get('titulo', 'Sin título')}
                        {f'<span class="badge badge-licitacion">Licitación</span>' if es_licitacion else ''}
                    </h3>
                    <p class="pub-summary">
                        {pub.get('resumen') if pub.get('resumen') and pub.get('resumen') != 'No se pudo generar un resumen relevante.' else 'Resumen no disponible.'}
                    </p>
                </div>
"""
                
                html += """
            </div>
"""
    
    html += """
        </div>
"""
    
    # Currency section
    if valores_monedas:
        html += f"""
        <!-- Currency Values -->
        <div class="currency-section">
            <h3 class="currency-title">💱 Valores del Día</h3>
            <div class="currency-grid">
                <div class="currency-item">
                    <div class="currency-name">USD</div>
                    <div class="currency-value">${valores_monedas.get('dolar', 'N/A')}</div>
                </div>
                <div class="currency-item">
                    <div class="currency-name">EUR</div>
                    <div class="currency-value">${valores_monedas.get('euro', 'N/A')}</div>
                </div>
            </div>
        </div>
"""
    
    html += """
        <!-- Footer -->
        <div class="footer">
            <p class="footer-text">
                Información obtenida directamente del sitio diariooficial.interior.gob.cl
            </p>
        </div>
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
    filename = f"informe_newsletter_{fecha_hoy.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nInforme generado: {filename}")
    print(f"Diseño tipo newsletter moderna con:")
    print("- Estilo inspirado en The Morning Brew / Axios")
    print("- Gradientes sutiles y colores vibrantes") 
    print("- Emojis para mejor legibilidad")
    print("- Secciones con códigos de color")
    print("- Diseño completamente responsive")