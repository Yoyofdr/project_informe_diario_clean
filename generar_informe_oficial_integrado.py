#!/usr/bin/env python
"""
Script de referencia para generar informes del Diario Oficial
SIEMPRE USAR ESTE SCRIPT COMO BASE
"""
import os
import sys
import django
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

# IMPORTANTE: Usar SIEMPRE el scraper oficial del proyecto
from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
from alerts.scraper_sii import obtener_novedades_tributarias_sii
from alerts.utils.sii_utils import SECCIONES_SII, clasificar_tipo_documento_sii, obtener_seccion_sii
from django.template import engines

def generar_informe_diario_oficial(fecha=None):
    """
    Genera y envía el informe del Diario Oficial usando el sistema oficial
    
    Args:
        fecha (str): Fecha en formato DD-MM-YYYY. Si no se proporciona, usa hoy.
    """
    
    if fecha is None:
        fecha = datetime.now().strftime("%d-%m-%Y")
    
    print(f"=== GENERANDO INFORME OFICIAL DEL {fecha} ===\n")
    
    # PASO 1: Usar el scraper oficial (NO crear uno nuevo)
    print("1. Ejecutando scraper oficial del Diario Oficial...")
    resultado = obtener_sumario_diario_oficial(fecha)
    
    if not resultado:
        print("❌ Error: No se obtuvieron resultados del scraper")
        return False
    
    publicaciones = resultado.get('publicaciones', [])
    valores_monedas = resultado.get('valores_monedas', {})
    total_documentos = resultado.get('total_documentos', 0)
    
    print(f"\n✅ Resultados del scraper del Diario Oficial:")
    print(f"   - Total documentos analizados: {total_documentos}")
    print(f"   - Publicaciones relevantes: {len(publicaciones)}")
    
    # PASO 1B: Obtener novedades tributarias del SII
    print("\n1B. Obteniendo novedades tributarias del SII...")
    # Convertir fecha string a datetime object para filtrado
    fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
    novedades_sii = obtener_novedades_tributarias_sii(fecha_referencia=fecha_obj)
    
    print(f"✅ Resultados del scraper del SII:")
    print(f"   - Circulares: {len(novedades_sii['circulares'])}")
    print(f"   - Resoluciones Exentas: {len(novedades_sii['resoluciones_exentas'])}")
    print(f"   - Jurisprudencia Administrativa: {len(novedades_sii['jurisprudencia_administrativa'])}")
    print(f"   - Total novedades SII: {novedades_sii['total_novedades']}")
    
    # ==================== PASO 2: ORGANIZAR POR SECCIONES ====================
    # Definir estructura de secciones del informe
    secciones_dict = {
        'NORMAS GENERALES': {
            'nombre': 'NORMAS GENERALES',
            'descripcion': 'Leyes, decretos supremos y resoluciones de alcance general',
            'publicaciones': []
        },
        'NORMAS PARTICULARES': {
            'nombre': 'NORMAS PARTICULARES', 
            'descripcion': 'Resoluciones específicas, nombramientos y concesiones',
            'publicaciones': []
        },
        'AVISOS DESTACADOS': {
            'nombre': 'AVISOS DESTACADOS',
            'descripcion': 'Licitaciones, concursos públicos y avisos importantes',
            'publicaciones': []
        },
        'SII_CIRCULARES': {
            'nombre': 'SERVICIO DE IMPUESTOS INTERNOS - CIRCULARES',
            'descripcion': 'Circulares y normativas generales del SII',
            'publicaciones': []
        },
        'SII_RESOLUCIONES': {
            'nombre': 'SERVICIO DE IMPUESTOS INTERNOS - RESOLUCIONES',
            'descripcion': 'Resoluciones exentas y normativas específicas del SII',
            'publicaciones': []
        },
        'SII_JURISPRUDENCIA': {
            'nombre': 'SERVICIO DE IMPUESTOS INTERNOS - JURISPRUDENCIA',
            'descripcion': 'Jurisprudencia administrativa tributaria del SII',
            'publicaciones': []
        }
    }
    
    # ==================== PROCESAMIENTO DEL DIARIO OFICIAL ====================
    # Clasificar publicaciones del Diario Oficial en las secciones correspondientes
    for pub in publicaciones:
        seccion = pub.get('seccion', 'NORMAS GENERALES').upper()
        
        # Si es contenido SII, clasificar en la subsección correspondiente
        if pub.get('es_sii', False):
            tipo_doc = clasificar_tipo_documento_sii(pub.get('titulo', ''))
            seccion_sii = obtener_seccion_sii(tipo_doc)
            
            # Solo agregar a subsecciones específicas si existen
            if seccion_sii in secciones_dict:
                secciones_dict[seccion_sii]['publicaciones'].append(pub)
            else:
                # Fallback a resoluciones si no existe la sección
                secciones_dict['SII_RESOLUCIONES']['publicaciones'].append(pub)
        else:
            # Clasificar en las secciones normales del Diario Oficial
            if seccion in secciones_dict:
                secciones_dict[seccion]['publicaciones'].append(pub)
            else:
                # Si la sección no existe, usar NORMAS GENERALES por defecto
                secciones_dict['NORMAS GENERALES']['publicaciones'].append(pub)
    
    # ==================== PROCESAMIENTO DE NOVEDADES SII ====================
    # Agregar contenido del scraper específico del SII
    if novedades_sii['total_novedades'] > 0:
        
        # 1. Procesar Circulares
        for circular in novedades_sii['circulares']:
            pub_sii = {
                'titulo': f"Circular N° {circular['numero']} - {circular['fecha']}",
                'resumen': circular['titulo'],
                'url_pdf': circular['url_pdf'],
                'es_sii': True,
                'fuente': circular.get('fuente', 'SII - Subdirección de Fiscalización')
            }
            secciones_dict['SII_CIRCULARES']['publicaciones'].append(pub_sii)
        
        # 2. Procesar Resoluciones Exentas
        for resolucion in novedades_sii['resoluciones_exentas']:
            pub_sii = {
                'titulo': f"Resolución Exenta SII N° {resolucion['numero']} - {resolucion['fecha']}",
                'resumen': resolucion['titulo'],
                'url_pdf': resolucion['url_pdf'],
                'es_sii': True,
                'fuente': resolucion.get('fuente', 'SII - Subdirección Jurídica')
            }
            secciones_dict['SII_RESOLUCIONES']['publicaciones'].append(pub_sii)
        
        # 3. Procesar Jurisprudencia Administrativa
        for juris in novedades_sii['jurisprudencia_administrativa']:
            pub_sii = {
                'titulo': f"Jurisprudencia N° {juris['numero']} - {juris['fecha']}",
                'resumen': juris['titulo'],
                'url_pdf': juris['url_pdf'],
                'es_sii': True,
                'fuente': juris.get('fuente', 'SII - Jurisprudencia')
            }
            secciones_dict['SII_JURISPRUDENCIA']['publicaciones'].append(pub_sii)
    
    secciones = [s for s in secciones_dict.values() if s['publicaciones']]
    
    # PASO 3: Usar la plantilla OFICIAL (no crear una nueva)
    print("\n2. Generando HTML con la plantilla oficial...")
    
    with open('templates/informe_diario_oficial_plantilla.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    django_engine = engines['django']
    template = django_engine.from_string(template_content)
    
    # Preparar contexto
    fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_formato = f"{fecha_obj.day} de {meses[fecha_obj.month]}, {fecha_obj.year}"
    
    # Obtener número de edición del caché
    edicion = "N/A"
    try:
        import json
        with open('edition_cache.json', 'r') as f:
            cache = json.load(f)
            edicion = cache.get(fecha, "N/A")
    except:
        pass
    
    context = {
        'fecha': fecha,
        'fecha_formato': fecha_formato,
        'edicion_numero': edicion,
        'total_documentos': total_documentos,
        'publicaciones_relevantes': len(publicaciones),
        'secciones': secciones,
        'valores_monedas': valores_monedas
    }
    
    html = template.render(context)
    
    # Guardar copia
    filename = f"informe_diario_oficial_{fecha.replace('-', '_')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"📄 Informe guardado en: {filename}")
    
    # PASO 4: Enviar con las direcciones CORRECTAS
    print("\n3. Enviando email...")
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Informe Diario Oficial - {fecha_formato} (Edición {edicion})"
    msg['From'] = "rodrigo@carvuk.com"  # SIEMPRE esta dirección
    msg['To'] = "rfernandezdelrio@uc.cl"  # SIEMPRE esta dirección
    
    html_part = MIMEText(html, 'html')
    msg.attach(html_part)
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("rodrigo@carvuk.com", "swqjlcwjaoooyzcb")
        server.send_message(msg)
        server.quit()
        
        print("\n✅ INFORME ENVIADO EXITOSAMENTE")
        print(f"   De: rodrigo@carvuk.com")
        print(f"   Para: rfernandezdelrio@uc.cl")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error enviando email: {str(e)}")
        return False

if __name__ == "__main__":
    # Si se ejecuta directamente, generar informe de hoy
    import sys
    
    if len(sys.argv) > 1:
        # Permitir especificar fecha como argumento
        fecha = sys.argv[1]
    else:
        fecha = None
    
    generar_informe_diario_oficial(fecha)