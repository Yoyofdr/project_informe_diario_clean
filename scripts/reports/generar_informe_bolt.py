#!/usr/bin/env python
"""
Script para generar el informe del Diario Oficial con diseño inspirado en Bolt
Mantiene elementos clave: secciones por tipo y valores de monedas
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
    """Genera el informe en formato HTML con diseño moderno, sobrio y colorido"""
    
    print(f"Generando informe estilo Bolt para: {fecha}")
    
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
    
    # Configuración de secciones con iconos y colores
    secciones_config = {
        'NORMAS GENERALES': {
            'emoji': '⚖️',
            'subtitle': 'Normativas de aplicación general',
            'gradient': 'linear-gradient(135deg, #059669 0%, #10b981 100%)'
        },
        'NORMAS PARTICULARES': {
            'emoji': '📋',
            'subtitle': 'Normativas específicas y sectoriales',
            'gradient': 'linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%)'
        },
        'AVISOS DESTACADOS': {
            'emoji': '📢',
            'subtitle': 'Avisos de interés público y licitaciones',
            'gradient': 'linear-gradient(135deg, #dc2626 0%, #ef4444 100%)'
        }
    }
    
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
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            color: #1e293b;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}
        
        .wrapper {{
            max-width: 672px;
            margin: 0 auto;
            background-color: #ffffff;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -1px rgb(0 0 0 / 0.06);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, #000000 0%, #1f2937 50%, #374151 100%);
            padding: 48px 32px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(45deg, rgba(55, 65, 81, 0.3) 0%, rgba(0, 0, 0, 0.2) 100%);
        }}
        
        .header-content {{
            position: relative;
            z-index: 10;
        }}
        
        .logo {{
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.025em;
            margin-bottom: 8px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }}
        
        .date {{
            color: #d1d5db;
            font-size: 14px;
            font-weight: 500;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }}
        
        .date::before {{
            content: '📅';
            font-size: 16px;
        }}
        
        /* Stats */
        .stats-container {{
            background: linear-gradient(90deg, #eff6ff 0%, #eef2ff 100%);
            border-bottom: 1px solid #dbeafe;
            display: grid;
            grid-template-columns: 1fr 1fr;
        }}
        
        .stat {{
            text-align: center;
            padding: 24px;
            border-right: 1px solid #dbeafe;
            position: relative;
        }}
        
        .stat:last-child {{
            border-right: none;
        }}
        
        .stat-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 8px;
        }}
        
        .stat-icon.documents::before {{
            content: '📊';
            font-size: 24px;
        }}
        
        .stat-icon.relevant::before {{
            content: '🏆';
            font-size: 24px;
        }}
        
        .stat-number {{
            font-size: 32px;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 4px;
        }}
        
        .stat-number.documents {{
            color: #1d4ed8;
        }}
        
        .stat-number.relevant {{
            color: #059669;
        }}
        
        .stat-label {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .stat-label.documents {{
            color: #2563eb;
        }}
        
        .stat-label.relevant {{
            color: #059669;
        }}
        
        /* Content */
        .content {{
            padding: 32px;
        }}
        
        /* Section */
        .section {{
            margin-bottom: 40px;
        }}
        
        .section:last-child {{
            margin-bottom: 0;
        }}
        
        /* Section Header */
        .section-header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid #eff6ff;
        }}
        
        .section-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #eff6ff 0%, #eef2ff 100%);
            border-radius: 8px;
            margin-right: 16px;
            font-size: 20px;
        }}
        
        .section-content {{
            flex: 1;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 2px;
        }}
        
        .section-subtitle {{
            font-size: 14px;
            color: #64748b;
        }}
        
        .section-count {{
            font-size: 14px;
            color: #6366f1;
            font-weight: 500;
        }}
        
        /* Publications */
        .publications {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        
        .publication {{
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .publication::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .publication:hover {{
            border-color: #dbeafe;
            box-shadow: 0 20px 25px -5px rgb(59 130 246 / 0.1), 0 10px 10px -5px rgb(59 130 246 / 0.04);
            transform: translateY(-4px);
        }}
        
        .publication:hover::before {{
            transform: scaleX(1);
        }}
        
        .pub-title {{
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 12px;
            line-height: 1.4;
            transition: color 0.3s ease;
        }}
        
        .publication:hover .pub-title {{
            color: #1d4ed8;
        }}
        
        .pub-summary {{
            font-size: 14px;
            color: #64748b;
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
            background-color: #dbeafe;
            color: #1e40af;
        }}
        
        /* Currency Section */
        .currency-section {{
            margin: 40px 32px 32px;
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            border-radius: 12px;
            padding: 32px;
            text-align: center;
            box-shadow: 0 10px 15px -3px rgb(251 191 36 / 0.1), 0 4px 6px -2px rgb(251 191 36 / 0.05);
        }}
        
        .currency-title {{
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }}
        
        .currency-title::before {{
            content: '💱';
            font-size: 20px;
        }}
        
        .currency-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }}
        
        .currency-item {{
            background-color: rgba(255, 255, 255, 0.2);
            padding: 16px;
            border-radius: 8px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
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
            color: #64748b;
        }}
        
        .empty-icon {{
            font-size: 48px;
            margin-bottom: 16px;
            opacity: 0.3;
        }}
        
        .empty-text {{
            font-size: 16px;
        }}
        
        /* Footer */
        .footer {{
            background-color: #f8fafc;
            padding: 24px 32px;
            text-align: center;
            border-top: 1px solid #e5e7eb;
            font-size: 13px;
            color: #64748b;
            line-height: 1.5;
        }}
        
        /* Specific section colors */
        .publication.normas-generales::before {{
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        }}
        
        .publication.normas-particulares::before {{
            background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%);
        }}
        
        .publication.avisos-destacados::before {{
            background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        }}
        
        /* Responsive */
        @media (max-width: 640px) {{
            .wrapper {{
                margin: 16px;
                max-width: none;
            }}
            
            .header, .content {{
                padding: 24px 20px;
            }}
            
            .stats-container {{
                grid-template-columns: 1fr;
            }}
            
            .stat {{
                border-right: none;
                border-bottom: 1px solid #dbeafe;
            }}
            
            .stat:last-child {{
                border-bottom: none;
            }}
            
            .currency-grid {{
                grid-template-columns: 1fr;
            }}
            
            .currency-section {{
                margin: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header">
            <div class="header-content">
                <div class="logo">Diario Oficial</div>
                <div class="date">{formatear_fecha_espanol(fecha)}</div>
            </div>
        </div>
        
        <div class="stats-container">
            <div class="stat">
                <div class="stat-icon documents"></div>
                <div class="stat-number documents">{total_documentos}</div>
                <div class="stat-label documents">Total Documentos</div>
            </div>
            <div class="stat">
                <div class="stat-icon relevant"></div>
                <div class="stat-number relevant">{len(publicaciones)}</div>
                <div class="stat-label relevant">Relevantes</div>
            </div>
        </div>
        
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
        orden_secciones = ['NORMAS GENERALES', 'NORMAS PARTICULARES', 'AVISOS DESTACADOS']
        
        for seccion in orden_secciones:
            if seccion in publicaciones_por_seccion and publicaciones_por_seccion[seccion]:
                pubs = publicaciones_por_seccion[seccion]
                config = secciones_config.get(seccion, {})
                
                # Clase CSS para el tipo de sección
                seccion_class = seccion.lower().replace(' ', '-')
                
                html += f"""
            <div class="section">
                <div class="section-header">
                    <div class="section-icon">{config.get('emoji', '📄')}</div>
                    <div class="section-content">
                        <div class="section-title">{seccion.title()}</div>
                        <div class="section-subtitle">{config.get('subtitle', '')}</div>
                    </div>
                    <div class="section-count">{len(pubs)} elemento{'s' if len(pubs) != 1 else ''}</div>
                </div>
                
                <div class="publications">
"""
                
                for pub in pubs:
                    es_licitacion = 'licitación' in pub.get('titulo', '').lower()
                    
                    html += f"""
                    <div class="publication {seccion_class}">
                        <h3 class="pub-title">
                            {pub.get('titulo', 'Sin título')}
                            {f'<span class="badge">Licitación</span>' if es_licitacion else ''}
                        </h3>
                        <p class="pub-summary">
                            {pub.get('resumen') if pub.get('resumen') and pub.get('resumen') != 'No se pudo generar un resumen relevante.' else 'Resumen no disponible.'}
                        </p>
                    </div>
"""
                
                html += """
                </div>
            </div>
"""
    
    html += """
        </div>
"""
    
    # Valores de monedas
    if valores_monedas:
        html += f"""
        <div class="currency-section">
            <h3 class="currency-title">Valores de Referencia del Día</h3>
            <div class="currency-grid">
                <div class="currency-item">
                    <div class="currency-name">Dólar Observado</div>
                    <div class="currency-value">${valores_monedas.get('dolar', 'N/A')}</div>
                </div>
                <div class="currency-item">
                    <div class="currency-name">Euro</div>
                    <div class="currency-value">${valores_monedas.get('euro', 'N/A')}</div>
                </div>
            </div>
        </div>
"""
    
    html += """
        <div class="footer">
            Información obtenida directamente del sitio diariooficial.interior.gob.cl
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
    filename = f"informe_bolt_{fecha_hoy.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nInforme generado: {filename}")
    print(f"Diseño inspirado en Bolt con:")
    print("- Gradientes sutiles y modernos")
    print("- Secciones diferenciadas por tipo (Normas Generales, Particulares, Avisos)")
    print("- Valores de monedas integrados")
    print("- Efectos hover elegantes")
    print("- Iconos y colores distintivos por sección")