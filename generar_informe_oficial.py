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
    
    print(f"\n✅ Resultados del scraper:")
    print(f"   - Total documentos analizados: {total_documentos}")
    print(f"   - Publicaciones relevantes: {len(publicaciones)}")
    
    # PASO 2: Organizar por secciones OFICIALES (no inventar nuevas)
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
        }
    }
    
    for pub in publicaciones:
        seccion = pub.get('seccion', 'NORMAS GENERALES').upper()
        if seccion in secciones_dict:
            secciones_dict[seccion]['publicaciones'].append(pub)
    
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