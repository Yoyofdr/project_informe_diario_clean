#!/usr/bin/env python
"""
Script para generar el informe del 21 de julio con el diseño Bolt refinado
"""
from datetime import datetime

def generar_informe_bolt():
    """Genera el informe del 21 de julio con el diseño Bolt refinado"""
    
    fecha = "18-07-2025"  # Mantengo la fecha del ejemplo para consistencia
    
    # Publicaciones del día
    publicaciones_normas_generales = [
        {
            "titulo": "LEY NÚM. 21.791 - MODIFICA EL CÓDIGO DEL TRABAJO Y OTROS CUERPOS LEGALES EN MATERIA DE INCLUSIÓN LABORAL DE PERSONAS CON DISCAPACIDAD",
            "resumen": "Establece cuotas obligatorias de contratación de personas con discapacidad en empresas con 100 o más trabajadores, fijando un mínimo del 1% de la dotación. Define mecanismos de fiscalización y sanciones por incumplimiento."
        },
        {
            "titulo": "DECRETO SUPREMO Nº 147 - MINISTERIO DE HACIENDA - FIJA VALORES DE LA UNIDAD DE FOMENTO",
            "resumen": "Actualiza los valores de la UF para el período del 10 de agosto al 9 de septiembre de 2025, considerando la variación del IPC de julio."
        },
        {
            "titulo": "DECRETO SUPREMO Nº 312 - MINISTERIO DE ECONOMÍA - PROTECCIÓN DE DATOS EN COMERCIO ELECTRÓNICO",
            "resumen": "Establece normas obligatorias para el tratamiento de datos personales en plataformas de comercio electrónico, incluyendo consentimiento expreso y medidas de seguridad."
        }
    ]
    
    publicaciones_normas_particulares = [
        {
            "titulo": "RESOLUCIÓN EXENTA Nº 4.231 - SERVICIO DE IMPUESTOS INTERNOS",
            "resumen": "Actualiza los requisitos técnicos para la emisión de boletas y facturas electrónicas, incorporando nuevos campos obligatorios para operaciones con criptoactivos."
        },
        {
            "titulo": "RESOLUCIÓN EXENTA Nº 892 - SUBSECRETARÍA DE TRANSPORTES",
            "resumen": "Define restricción vehicular extraordinaria para vehículos sin sello verde los días 22 y 23 de julio en la Región Metropolitana por episodio crítico."
        }
    ]
    
    publicaciones_avisos_destacados = [
        {
            "titulo": "BANCO CENTRAL DE CHILE - TIPOS DE CAMBIO Y PARIDADES",
            "resumen": "Publica los tipos de cambio oficiales del dólar observado y otras monedas para operaciones del 21 de julio de 2025."
        },
        {
            "titulo": "MUNICIPALIDAD DE SANTIAGO - LICITACIÓN PÚBLICA CONSTRUCCIÓN CICLOVÍAS",
            "resumen": "Convoca a licitación pública ID 2397-45-LP25 para la construcción de 12 kilómetros de ciclovías en la comuna, con presupuesto de $4.500 millones.",
            "es_licitacion": True
        }
    ]
    
    total_documentos = 47
    publicaciones_relevantes = 7
    
    # Generar HTML con diseño Bolt
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Diario Oficial • 21-07-2025</title>
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
            background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
            padding: 48px 32px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(45deg, rgba(71, 85, 105, 0.3) 0%, rgba(30, 41, 59, 0.2) 100%);
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
            color: #e2e8f0;
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
            background: linear-gradient(90deg, #f0f9ff 0%, #e0f2fe 100%);
            border-bottom: 1px solid #bae6fd;
            display: grid;
            grid-template-columns: 1fr 1fr;
        }}
        
        .stat {{
            text-align: center;
            padding: 24px;
            border-right: 1px solid #bae6fd;
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
            color: #0284c7;
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
            color: #0369a1;
        }}
        
        .stat-label.relevant {{
            color: #047857;
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
            border-bottom: 1px solid #f0f9ff;
        }}
        
        .section-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
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
            color: #3b82f6;
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
            border: 1px solid #e5e7eb;
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
            background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .publication:hover {{
            border-color: #bfdbfe;
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
            color: #2563eb;
        }}
        
        .pub-summary {{
            font-size: 14px;
            color: #6b7280;
            line-height: 1.6;
            margin-bottom: 16px;
        }}
        
        .pub-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            background-color: #3b82f6;
            color: #ffffff;
            font-size: 14px;
            font-weight: 500;
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.2s ease;
        }}
        
        .pub-link:hover {{
            background-color: #2563eb;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }}
        
        .pub-link::before {{
            content: '📄';
            font-size: 16px;
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
            background-color: #fef3c7;
            color: #92400e;
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
            gap: 24px;
        }}
        
        .currency-item {{
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }}
        
        .currency-name {{
            font-size: 12px;
            font-weight: 600;
            color: #78350f;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
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
            border-top: 1px solid #e5e7eb;
        }}
        
        .footer-text {{
            font-size: 12px;
            color: #6b7280;
            line-height: 1.6;
        }}
        
        .footer-link {{
            color: #3b82f6;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .footer-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <h1 class="logo">Diario Oficial</h1>
                <div class="date">Lunes 21 de julio de 2025</div>
            </div>
        </header>
        
        <!-- Stats -->
        <div class="stats-container">
            <div class="stat">
                <div class="stat-icon documents"></div>
                <div class="stat-number documents">{total_documentos}</div>
                <div class="stat-label documents">Documentos Totales</div>
            </div>
            <div class="stat">
                <div class="stat-icon relevant"></div>
                <div class="stat-number relevant">{publicaciones_relevantes}</div>
                <div class="stat-label relevant">Publicaciones Relevantes</div>
            </div>
        </div>
        
        <!-- Content -->
        <div class="content">
            <!-- Normas Generales -->
            <section class="section">
                <div class="section-header">
                    <div class="section-icon">📋</div>
                    <div class="section-content">
                        <h2 class="section-title">Normas Generales</h2>
                        <p class="section-subtitle">Leyes y decretos de aplicación general</p>
                    </div>
                    <span class="section-count">{len(publicaciones_normas_generales)} publicaciones</span>
                </div>
                <div class="publications">
"""
    
    for pub in publicaciones_normas_generales:
        html += f"""
                    <article class="publication">
                        <h3 class="pub-title">{pub['titulo']}</h3>
                        <p class="pub-summary">{pub['resumen']}</p>
                        <a href="#" class="pub-link">Ver documento oficial</a>
                    </article>
"""
    
    html += f"""
                </div>
            </section>
            
            <!-- Normas Particulares -->
            <section class="section">
                <div class="section-header">
                    <div class="section-icon">📄</div>
                    <div class="section-content">
                        <h2 class="section-title">Normas Particulares</h2>
                        <p class="section-subtitle">Resoluciones y normativas específicas</p>
                    </div>
                    <span class="section-count">{len(publicaciones_normas_particulares)} publicaciones</span>
                </div>
                <div class="publications">
"""
    
    for pub in publicaciones_normas_particulares:
        html += f"""
                    <article class="publication">
                        <h3 class="pub-title">{pub['titulo']}</h3>
                        <p class="pub-summary">{pub['resumen']}</p>
                        <a href="#" class="pub-link">Ver documento oficial</a>
                    </article>
"""
    
    html += f"""
                </div>
            </section>
            
            <!-- Avisos Destacados -->
            <section class="section">
                <div class="section-header">
                    <div class="section-icon">⭐</div>
                    <div class="section-content">
                        <h2 class="section-title">Avisos Destacados</h2>
                        <p class="section-subtitle">Licitaciones y avisos importantes</p>
                    </div>
                    <span class="section-count">{len(publicaciones_avisos_destacados)} publicaciones</span>
                </div>
                <div class="publications">
"""
    
    for pub in publicaciones_avisos_destacados:
        badge = '<span class="badge">Licitación</span>' if pub.get('es_licitacion') else ''
        html += f"""
                    <article class="publication">
                        <h3 class="pub-title">{pub['titulo']}{badge}</h3>
                        <p class="pub-summary">{pub['resumen']}</p>
                        <a href="#" class="pub-link">Ver documento oficial</a>
                    </article>
"""
    
    html += f"""
                </div>
            </section>
        </div>
        
        <!-- Currency Section -->
        <div class="currency-section">
            <h2 class="currency-title">Valores del Día</h2>
            <div class="currency-grid">
                <div class="currency-item">
                    <div class="currency-name">Dólar Observado</div>
                    <div class="currency-value">$943.28</div>
                </div>
                <div class="currency-item">
                    <div class="currency-name">Euro</div>
                    <div class="currency-value">$1,026.45</div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <footer class="footer">
            <p class="footer-text">
                Información obtenida directamente del sitio 
                <a href="https://www.diariooficial.interior.gob.cl" class="footer-link">diariooficial.interior.gob.cl</a>
                <br>
                Vista previa del informe del 21 de julio de 2025
                <br>
                {total_documentos} documentos analizados • {publicaciones_relevantes} relevantes seleccionados • Enlaces directos a PDFs oficiales
            </p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    html = generar_informe_bolt()
    
    # Guardar el HTML
    filename = "informe_diario_oficial_21_07_2025_bolt.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Informe Bolt generado: {filename}")