#!/usr/bin/env python
"""
Script actualizado para generar informes usando la plantilla oficial
"""
import os
import sys
import django
from datetime import datetime
from django.template import Template, Context

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial

def generar_informe_con_plantilla(fecha=None):
    """Genera el informe usando la plantilla oficial"""
    
    if fecha is None:
        fecha = datetime.now().strftime("%d-%m-%Y")
    
    print(f"Generando informe para: {fecha}")
    
    # Obtener datos del scraper
    resultado = obtener_sumario_diario_oficial(fecha)
    
    publicaciones = resultado.get('publicaciones', [])
    valores_monedas = resultado.get('valores_monedas', {})
    total_documentos = resultado.get('total_documentos', 0)
    
    # Organizar publicaciones por sección
    secciones = {
        'NORMAS GENERALES': {
            'nombre': 'Normas Generales',
            'descripcion': 'Normativas de aplicación general',
            'publicaciones': []
        },
        'NORMAS PARTICULARES': {
            'nombre': 'Normas Particulares', 
            'descripcion': 'Resoluciones y normativas específicas',
            'publicaciones': []
        },
        'AVISOS DESTACADOS': {
            'nombre': 'Avisos Destacados',
            'descripcion': 'Avisos de interés público y licitaciones',
            'publicaciones': []
        }
    }
    
    # Clasificar publicaciones
    for pub in publicaciones:
        seccion = pub.get('seccion', 'NORMAS GENERALES').upper()
        if seccion in secciones:
            secciones[seccion]['publicaciones'].append(pub)
    
    # Convertir a lista para la plantilla
    secciones_lista = []
    for key in ['NORMAS GENERALES', 'NORMAS PARTICULARES', 'AVISOS DESTACADOS']:
        if secciones[key]['publicaciones']:
            secciones_lista.append(secciones[key])
    
    # Formatear fecha
    try:
        fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
                 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        
        dia_semana = dias_semana[fecha_obj.weekday()]
        dia = fecha_obj.day
        mes = meses[fecha_obj.month - 1]
        año = fecha_obj.year
        
        fecha_formato = f"{dia_semana} {dia} de {mes} de {año}"
    except:
        fecha_formato = fecha
    
    # Leer la plantilla
    plantilla_path = os.path.join(os.path.dirname(__file__), 'templates', 'informe_diario_oficial_plantilla.html')
    
    if os.path.exists(plantilla_path):
        with open(plantilla_path, 'r', encoding='utf-8') as f:
            plantilla_html = f.read()
    else:
        # Si no existe la plantilla, usar HTML embebido
        plantilla_html = PLANTILLA_HTML_EMBEBIDA
    
    # Crear contexto
    context = {
        'fecha': fecha,
        'fecha_formato': fecha_formato,
        'total_documentos': total_documentos,
        'publicaciones_relevantes': len(publicaciones),
        'secciones': secciones_lista,
        'valores_monedas': valores_monedas if valores_monedas else None,
        'edicion_numero': resultado.get('edicion_numero', '')
    }
    
    # Renderizar plantilla
    template = Template(plantilla_html)
    html = template.render(Context(context))
    
    # Guardar archivo
    filename = f"informe_diario_oficial_{fecha.replace('-', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nInforme generado: {filename}")
    print(f"Total documentos: {total_documentos}")
    print(f"Publicaciones relevantes: {len(publicaciones)}")
    
    return filename, html

# Plantilla HTML embebida como respaldo
PLANTILLA_HTML_EMBEBIDA = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diario Oficial • {{ fecha }}</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f8fafc; color: #1e293b; line-height: 1.6;">
    
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8fafc;">
        <tr>
            <td align="center" style="padding: 20px 0;">
                
                <!-- Wrapper -->
                <table width="672" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); overflow: hidden;">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 48px 32px; text-align: center;">
                            <h1 style="margin: 0 0 8px 0; font-size: 28px; font-weight: 700; color: #ffffff; letter-spacing: -0.025em;">
                                Diario Oficial
                            </h1>
                            <p style="margin: 0; color: #cbd5e1; font-size: 14px; font-weight: 500;">
                                {{ fecha_formato }}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Content aquí... -->
                    
                </table>
            </td>
        </tr>
    </table>
    
</body>
</html>"""

if __name__ == "__main__":
    # Generar informe de hoy o de una fecha específica
    import sys
    
    if len(sys.argv) > 1:
        fecha = sys.argv[1]
    else:
        fecha = None
    
    generar_informe_con_plantilla(fecha)