#!/usr/bin/env python
"""
Script para generar el informe del Diario Oficial con diseño minimalista
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
    """Genera el informe en formato HTML con diseño minimalista en blanco y negro"""
    
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
    
    # HTML template minimalista
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Informe Diario Oficial - {fecha}</title>
    <style>
        /* Reset y tipografía base */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            font-size: 16px;
            line-height: 1.8;
            color: #000;
            background-color: #fff;
            padding: 40px 20px;
        }}
        
        /* Contenedor principal */
        .container {{
            max-width: 700px;
            margin: 0 auto;
        }}
        
        /* Encabezado */
        .header {{
            text-align: center;
            margin-bottom: 60px;
            border-bottom: 2px solid #000;
            padding-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 28px;
            font-weight: normal;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 15px;
        }}
        
        .header .date {{
            font-size: 16px;
            font-style: italic;
            margin-bottom: 20px;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            font-size: 14px;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }}
        
        /* Valores de monedas */
        .currency-section {{
            margin-bottom: 50px;
            padding: 20px;
            border: 1px solid #000;
        }}
        
        .currency-title {{
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
            text-align: center;
        }}
        
        .currency-values {{
            display: flex;
            justify-content: space-around;
            text-align: center;
        }}
        
        .currency-item {{
            flex: 1;
        }}
        
        .currency-name {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        
        .currency-value {{
            font-size: 20px;
            font-weight: bold;
        }}
        
        /* Secciones */
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-header {{
            border-bottom: 1px solid #000;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: normal;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        
        .section-count {{
            font-size: 12px;
            font-style: italic;
            float: right;
            margin-top: 4px;
        }}
        
        /* Publicaciones */
        .publication {{
            margin-bottom: 35px;
            padding-bottom: 25px;
            border-bottom: 1px dotted #ccc;
        }}
        
        .publication:last-child {{
            border-bottom: none;
        }}
        
        .publication-title {{
            font-size: 16px;
            font-weight: bold;
            line-height: 1.4;
            margin-bottom: 10px;
        }}
        
        .publication-summary {{
            font-size: 14px;
            line-height: 1.6;
            text-align: justify;
            color: #333;
        }}
        
        /* Licitaciones - marca especial */
        .licitacion-marker {{
            display: inline-block;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border: 1px solid #000;
            padding: 2px 8px;
            margin-left: 10px;
            vertical-align: middle;
        }}
        
        /* Mensaje vacío */
        .empty-section {{
            text-align: center;
            padding: 80px 0;
            font-style: italic;
            color: #666;
        }}
        
        /* Pie de página */
        .footer {{
            margin-top: 80px;
            padding-top: 30px;
            border-top: 1px solid #000;
            text-align: center;
            font-size: 12px;
            line-height: 1.6;
            color: #666;
        }}
        
        /* Responsive */
        @media (max-width: 600px) {{
            body {{
                padding: 20px 15px;
            }}
            
            .header h1 {{
                font-size: 22px;
            }}
            
            .stats {{
                flex-direction: column;
                gap: 20px;
            }}
            
            .currency-values {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
        
        /* Para impresión */
        @media print {{
            body {{
                padding: 0;
            }}
            
            .publication {{
                page-break-inside: avoid;
            }}
            
            .section {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Informe Diario Oficial</h1>
            <div class="date">{formatear_fecha_espanol(fecha).title()}</div>
            <div class="stats">
                <div class="stat">
                    <span class="stat-value">{total_documentos}</span>
                    <span>Documentos analizados</span>
                </div>
                <div class="stat">
                    <span class="stat-value">{len(publicaciones)}</span>
                    <span>Publicaciones relevantes</span>
                </div>
            </div>
        </div>
        
        <div class="content">
"""
    
    # Agregar sección de valores de monedas si existen
    if valores_monedas:
        html += f"""
            <div class="currency-section">
                <div class="currency-title">Valores de Referencia</div>
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
            </div>
"""
    
    # Si no hay publicaciones
    if not publicaciones:
        html += """
            <div class="empty-section">
                <p>No se encontraron publicaciones relevantes para esta fecha.</p>
            </div>
"""
    else:
        # Agregar publicaciones por sección
        for seccion in orden_secciones:
            if seccion in publicaciones_por_seccion and publicaciones_por_seccion[seccion]:
                pubs = publicaciones_por_seccion[seccion]
                
                # Header de sección
                html += f"""
            <div class="section">
                <div class="section-header">
                    <h2 class="section-title">{seccion}</h2>
                    <span class="section-count">{len(pubs)} publicacion{'es' if len(pubs) != 1 else ''}</span>
                    <div style="clear: both;"></div>
                </div>
"""
                
                # Publicaciones de la sección
                for pub in pubs:
                    es_licitacion = 'licitación' in pub.get('titulo', '').lower()
                    
                    html += f"""
                <div class="publication">
                    <div class="publication-title">
                        {pub.get('titulo', 'Sin título')}
                        {f'<span class="licitacion-marker">Licitación</span>' if es_licitacion else ''}
                    </div>
                    <div class="publication-summary">
                        {pub.get('resumen') if pub.get('resumen') and pub.get('resumen') != 'No se pudo generar un resumen relevante.' else 'Resumen no disponible.'}
                    </div>
                </div>
"""
                
                html += """
            </div>
"""
        
        # Agregar secciones adicionales que no estén en el orden predefinido
        for seccion, pubs in publicaciones_por_seccion.items():
            if seccion not in orden_secciones and pubs:
                html += f"""
            <div class="section">
                <div class="section-header">
                    <h2 class="section-title">{seccion}</h2>
                    <span class="section-count">{len(pubs)} publicacion{'es' if len(pubs) != 1 else ''}</span>
                    <div style="clear: both;"></div>
                </div>
"""
                for pub in pubs:
                    html += f"""
                <div class="publication">
                    <div class="publication-title">{pub.get('titulo', 'Sin título')}</div>
                    <div class="publication-summary">
                        {pub.get('resumen') if pub.get('resumen') and pub.get('resumen') != 'No se pudo generar un resumen relevante.' else 'Resumen no disponible.'}
                    </div>
                </div>
"""
                html += """
            </div>
"""
    
    html += """
        </div>
        
        <div class="footer">
            <p>Información obtenida directamente del sitio diariooficial.interior.gob.cl</p>
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
        fecha_hoy = "17-07-2025"
    
    html = generar_informe_html(fecha_hoy)
    
    # Guardar el HTML
    filename = f"informe_minimalista_{fecha_hoy.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nInforme generado: {filename}")
    print(f"Diseño minimalista en blanco y negro")