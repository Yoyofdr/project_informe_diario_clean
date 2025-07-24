#!/usr/bin/env python
"""
Script para generar un ejemplo del informe sobrio sin necesidad de scraping
"""
from datetime import datetime
from utils_fecha import formatear_fecha_espanol

def generar_informe_html(fecha):
    """Genera el informe en formato HTML con diseño sobrio estilo Bolt"""
    
    # Datos de ejemplo
    publicaciones = [
        {
            'seccion': 'NORMAS GENERALES',
            'titulo': 'Resolución exenta número 244, de 2025.- Instruye un procedimiento administrativo para iniciar el proceso de consulta previa de las medidas que indica, y convoca a las instituciones representativas del pueblo mapuche en las regiones del Biobío, La Araucanía, Los Ríos y Los Lagos',
            'resumen': 'La resolución exenta número 244 del 27 de junio de 2025 instruye el inicio de un proceso de consulta previa sobre un nuevo sistema de tierras para las comunidades y organizaciones indígenas Mapuche en las regiones del Biobío, La Araucanía, Los Ríos y Los Lagos, convocando a sus instituciones representativas a una reunión de planificación.'
        },
        {
            'seccion': 'AVISOS DESTACADOS',
            'titulo': 'Fomento a la inversión privada en obras de riego y drenaje ley N° 18.450',
            'resumen': 'La Comisión Nacional de Riego del Ministerio de Agricultura de Chile informa sobre los resultados del "Primer concurso de obras civiles del sur" bajo la Ley N° 18.450, cuyos puntajes de proyectos admitidos y no admitidos se publicarán el 18 de julio de 2025.'
        }
    ]
    
    total_documentos = 10
    valores_monedas = {'dolar': '966.78', 'euro': '1120.00'}
    
    # Organizar publicaciones por sección
    from collections import defaultdict
    publicaciones_por_seccion = defaultdict(list)
    for pub in publicaciones:
        seccion = pub.get('seccion', 'Sin sección').upper()
        publicaciones_por_seccion[seccion].append(pub)
    
    # Configuración de secciones
    secciones_config = {
        'NORMAS GENERALES': {
            'subtitle': 'Normativas de aplicación general',
            'color': '#059669'
        },
        'NORMAS PARTICULARES': {
            'subtitle': 'Normativas específicas y sectoriales',
            'color': '#7c3aed'
        },
        'AVISOS DESTACADOS': {
            'subtitle': 'Avisos de interés público y licitaciones',
            'color': '#dc2626'
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
            background: #f8fafc;
            color: #1e293b;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}
        
        .wrapper {{
            max-width: 672px;
            margin: 0 auto;
            background-color: #ffffff;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        /* Header */
        .header {{
            background: #1e293b;
            padding: 48px 32px;
            text-align: center;
        }}
        
        .logo {{
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.025em;
            margin-bottom: 8px;
        }}
        
        .date {{
            color: #cbd5e1;
            font-size: 14px;
            font-weight: 500;
        }}
        
        /* Stats */
        .stats-container {{
            background: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
            display: grid;
            grid-template-columns: 1fr 1fr;
        }}
        
        .stat {{
            text-align: center;
            padding: 24px;
            border-right: 1px solid #e2e8f0;
        }}
        
        .stat:last-child {{
            border-right: none;
        }}
        
        .stat-number {{
            font-size: 32px;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 4px;
            color: #1e293b;
        }}
        
        .stat-label {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748b;
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
            border-bottom: 1px solid #e2e8f0;
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
            color: #64748b;
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
            border-radius: 8px;
            padding: 24px;
            transition: all 0.2s ease;
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
            border-color: #cbd5e1;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
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
        }}
        
        .pub-summary {{
            font-size: 14px;
            color: #64748b;
            line-height: 1.6;
        }}
        
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-radius: 4px;
            margin-left: 8px;
            background-color: #e2e8f0;
            color: #475569;
        }}
        
        /* Currency Section */
        .currency-section {{
            margin: 32px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 24px;
        }}
        
        .currency-title {{
            font-size: 14px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            text-align: center;
        }}
        
        .currency-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }}
        
        .currency-item {{
            text-align: center;
            padding: 16px;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
        }}
        
        .currency-name {{
            font-size: 12px;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }}
        
        .currency-value {{
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
        }}
        
        /* Footer */
        .footer {{
            background-color: #f8fafc;
            padding: 24px 32px;
            text-align: center;
            border-top: 1px solid #e2e8f0;
            font-size: 13px;
            color: #64748b;
            line-height: 1.5;
        }}
        
        /* Specific section colors - subtle */
        .publication.normas-generales::before {{
            background: #059669;
        }}
        
        .publication.normas-particulares::before {{
            background: #7c3aed;
        }}
        
        .publication.avisos-destacados::before {{
            background: #dc2626;
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
                border-bottom: 1px solid #e2e8f0;
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
            <div class="logo">Diario Oficial</div>
            <div class="date">{formatear_fecha_espanol(fecha)}</div>
        </div>
        
        <div class="stats-container">
            <div class="stat">
                <div class="stat-number">{total_documentos}</div>
                <div class="stat-label">Total Documentos</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(publicaciones)}</div>
                <div class="stat-label">Relevantes</div>
            </div>
        </div>
        
        <div class="content">
"""
    
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
                            {pub.get('resumen', 'Resumen no disponible.')}
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
    fecha_hoy = "18-07-2025"
    
    html = generar_informe_html(fecha_hoy)
    
    # Guardar el HTML
    filename = f"ejemplo_sobrio_{fecha_hoy.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nEjemplo generado: {filename}")
    print(f"Abre el archivo para ver el diseño sobrio")