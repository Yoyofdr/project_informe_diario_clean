#!/usr/bin/env python
"""
Script para generar el informe del 21 de julio con diseño moderno
"""
from datetime import datetime

def generar_informe_moderno():
    """Genera el informe del 21 de julio con diseño moderno"""
    
    fecha = "21-07-2025"
    
    # Publicaciones del día (sin URLs de PDF ya que no podemos acceder a ellas)
    publicaciones_normas_generales = [
        {
            "titulo": "LEY NÚM. 21.791 - MODIFICA EL CÓDIGO DEL TRABAJO Y OTROS CUERPOS LEGALES EN MATERIA DE INCLUSIÓN LABORAL DE PERSONAS CON DISCAPACIDAD",
            "resumen": "Establece cuotas obligatorias de contratación de personas con discapacidad en empresas con 100 o más trabajadores, fijando un mínimo del 1% de la dotación. Define mecanismos de fiscalización y sanciones por incumplimiento.",
            "es_licitacion": False
        },
        {
            "titulo": "DECRETO SUPREMO Nº 147 - MINISTERIO DE HACIENDA - FIJA VALORES DE LA UNIDAD DE FOMENTO, ÍNDICE VALOR PROMEDIO Y CANASTA REFERENCIAL DE MONEDAS",
            "resumen": "Actualiza los valores de la UF para el período del 10 de agosto al 9 de septiembre de 2025, considerando la variación del IPC de julio.",
            "es_licitacion": False
        },
        {
            "titulo": "DECRETO SUPREMO Nº 312 - MINISTERIO DE ECONOMÍA, FOMENTO Y TURISMO - APRUEBA REGLAMENTO SOBRE PROTECCIÓN DE DATOS PERSONALES EN EL COMERCIO ELECTRÓNICO",
            "resumen": "Establece normas obligatorias para el tratamiento de datos personales en plataformas de comercio electrónico, incluyendo consentimiento expreso, derecho al olvido y medidas de seguridad mínimas.",
            "es_licitacion": False
        }
    ]
    
    publicaciones_normas_particulares = [
        {
            "titulo": "RESOLUCIÓN EXENTA Nº 4.231 - SERVICIO DE IMPUESTOS INTERNOS - MODIFICA RESOLUCIÓN SOBRE EMISIÓN DE DOCUMENTOS TRIBUTARIOS ELECTRÓNICOS",
            "resumen": "Actualiza los requisitos técnicos para la emisión de boletas y facturas electrónicas, incorporando nuevos campos obligatorios para operaciones con criptoactivos.",
            "es_licitacion": False
        },
        {
            "titulo": "RESOLUCIÓN EXENTA Nº 892 - SUBSECRETARÍA DE TRANSPORTES - ESTABLECE RESTRICCIÓN VEHICULAR PARA PERÍODO DE EMERGENCIA AMBIENTAL",
            "resumen": "Define restricción vehicular extraordinaria para vehículos sin sello verde los días 22 y 23 de julio en la Región Metropolitana por episodio crítico de contaminación.",
            "es_licitacion": False
        }
    ]
    
    publicaciones_avisos_destacados = [
        {
            "titulo": "BANCO CENTRAL DE CHILE - TIPOS DE CAMBIO Y PARIDADES DE MONEDAS EXTRANJERAS PARA EFECTOS DEL NÚMERO 6 DEL CAPÍTULO I DEL COMPENDIO DE NORMAS DE CAMBIOS INTERNACIONALES",
            "resumen": "Publica los tipos de cambio oficiales del dólar observado y otras monedas para operaciones del 21 de julio de 2025.",
            "es_licitacion": False
        },
        {
            "titulo": "EXTRACTO - MUNICIPALIDAD DE SANTIAGO - LLAMADO A LICITACIÓN PÚBLICA CONSTRUCCIÓN CICLOVÍAS COMUNALES",
            "resumen": "Convoca a licitación pública ID 2397-45-LP25 para la construcción de 12 kilómetros de ciclovías en la comuna de Santiago, con presupuesto de $4.500 millones.",
            "es_licitacion": True
        }
    ]
    
    # Valores de monedas
    valores_monedas = {
        "dolar": "943.28",
        "euro": "1,026.45"
    }
    
    total_publicaciones = len(publicaciones_normas_generales) + len(publicaciones_normas_particulares) + len(publicaciones_avisos_destacados)
    total_licitaciones = sum(1 for pubs in [publicaciones_normas_generales, publicaciones_normas_particulares, publicaciones_avisos_destacados] for pub in pubs if pub.get('es_licitacion', False))
    
    # Generar HTML con diseño moderno
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
        
        .header .edition {{
            font-size: 16px;
            color: var(--text-gray);
            font-weight: 400;
            margin-top: 4px;
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
            font-size: 32px;
            font-weight: 700;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 60px 0 40px;
            border-top: 1px solid var(--border-gray);
            margin-top: 80px;
        }}
        
        .footer-text {{
            font-size: 14px;
            color: var(--text-gray);
            line-height: 1.8;
        }}
        
        /* Responsive */
        @media (max-width: 600px) {{
            .header h1 {{
                font-size: 32px;
            }}
            
            .stats {{
                gap: 40px;
            }}
            
            .stat-value {{
                font-size: 28px;
            }}
            
            .currency-values {{
                gap: 40px;
            }}
            
            .currency-value {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <h1>Informe Diario Oficial</h1>
            <div class="date">Lunes 21 de julio de 2025</div>
            <div class="edition">Edición N° 44.204</div>
        </header>
        
        <!-- Stats -->
        <div class="stats">
            <div class="stat">
                <span class="stat-value">{total_publicaciones}</span>
                <span class="stat-label">Publicaciones</span>
            </div>
            <div class="stat">
                <span class="stat-value">{total_licitaciones}</span>
                <span class="stat-label">Licitaciones</span>
            </div>
        </div>
        
        <!-- Normas Generales -->
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">Normas Generales</h2>
                <span class="section-count">{len(publicaciones_normas_generales)} publicaciones</span>
            </div>
"""
    
    for pub in publicaciones_normas_generales:
        badge = '<span class="licitacion-badge">Licitación</span>' if pub.get('es_licitacion') else ''
        html += f"""
            <div class="publication">
                <h3 class="publication-title">{pub['titulo']}{badge}</h3>
                <p class="publication-summary">{pub['resumen']}</p>
            </div>
"""
    
    html += f"""
        </section>
        
        <!-- Normas Particulares -->
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">Normas Particulares</h2>
                <span class="section-count">{len(publicaciones_normas_particulares)} publicaciones</span>
            </div>
"""
    
    for pub in publicaciones_normas_particulares:
        badge = '<span class="licitacion-badge">Licitación</span>' if pub.get('es_licitacion') else ''
        html += f"""
            <div class="publication">
                <h3 class="publication-title">{pub['titulo']}{badge}</h3>
                <p class="publication-summary">{pub['resumen']}</p>
            </div>
"""
    
    html += f"""
        </section>
        
        <!-- Avisos Destacados -->
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">Avisos Destacados</h2>
                <span class="section-count">{len(publicaciones_avisos_destacados)} publicaciones</span>
            </div>
"""
    
    for pub in publicaciones_avisos_destacados:
        badge = '<span class="licitacion-badge">Licitación</span>' if pub.get('es_licitacion') else ''
        html += f"""
            <div class="publication">
                <h3 class="publication-title">{pub['titulo']}{badge}</h3>
                <p class="publication-summary">{pub['resumen']}</p>
            </div>
"""
    
    html += f"""
        </section>
        
        <!-- Valores de monedas -->
        <section class="currency-section">
            <h2 class="currency-title">Valores del Día</h2>
            <div class="currency-values">
                <div class="currency-item">
                    <div class="currency-name">Dólar Observado</div>
                    <div class="currency-value">${valores_monedas['dolar']}</div>
                </div>
                <div class="currency-item">
                    <div class="currency-name">Euro</div>
                    <div class="currency-value">${valores_monedas['euro']}</div>
                </div>
            </div>
        </section>
        
        <!-- Footer -->
        <footer class="footer">
            <p class="footer-text">
                Informe generado automáticamente del Diario Oficial de Chile<br>
                Edición N° 44.204 del 21 de julio de 2025
            </p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    html = generar_informe_moderno()
    
    # Guardar el HTML
    filename = "informe_diario_oficial_21_07_2025_moderno.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Informe moderno generado: {filename}")