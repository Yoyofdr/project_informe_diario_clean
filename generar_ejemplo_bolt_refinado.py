#!/usr/bin/env python
"""
Script para generar un ejemplo del informe con el diseño Bolt refinado
Mantiene los degradados sutiles y toques azules que gustaron
"""
from datetime import datetime
from utils_fecha import formatear_fecha_espanol

def generar_informe_html(fecha):
    """Genera el informe en formato HTML con diseño Bolt refinado"""
    
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
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 48px 32px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(45deg, rgba(55, 65, 81, 0.1) 0%, rgba(0, 0, 0, 0.1) 100%);
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
        }}
        
        .date {{
            color: #cbd5e1;
            font-size: 14px;
            font-weight: 500;
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
            color: #2563eb;
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
            background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%);
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
            margin: 32px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
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
                <div class="stat-number documents">{total_documentos}</div>
                <div class="stat-label documents">Total Documentos</div>
            </div>
            <div class="stat">
                <div class="stat-number relevant">{len(publicaciones)}</div>
                <div class="stat-label relevant">Relevantes</div>
            </div>
        </div>
        
        <div class="content">
"""
    
    # Agregar publicaciones por sección
    orden_secciones = ['NORMAS GENERALES', 'NORMAS PARTICULARES', 'AVISOS DESTACADOS']
    
    secciones_config = {
        'NORMAS GENERALES': 'Normativas de aplicación general',
        'NORMAS PARTICULARES': 'Normativas específicas y sectoriales',
        'AVISOS DESTACADOS': 'Avisos de interés público y licitaciones'
    }
    
    for seccion in orden_secciones:
        if seccion in publicaciones_por_seccion and publicaciones_por_seccion[seccion]:
            pubs = publicaciones_por_seccion[seccion]
            subtitle = secciones_config.get(seccion, '')
            
            html += f"""
            <div class="section">
                <div class="section-header">
                    <div class="section-content">
                        <div class="section-title">{seccion.title()}</div>
                        <div class="section-subtitle">{subtitle}</div>
                    </div>
                    <div class="section-count">{len(pubs)} elemento{'s' if len(pubs) != 1 else ''}</div>
                </div>
                
                <div class="publications">
"""
            
            for pub in pubs:
                es_licitacion = 'licitación' in pub.get('titulo', '').lower()
                
                html += f"""
                    <div class="publication">
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
    filename = f"ejemplo_bolt_refinado_{fecha_hoy.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nEjemplo generado: {filename}")
    print(f"Abre el archivo para ver el diseño Bolt refinado")