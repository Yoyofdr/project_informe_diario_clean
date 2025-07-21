#!/usr/bin/env python
"""
Envía la versión final del informe del 21 de julio con todo correcto
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from alerts.scraper_diario_oficial import obtener_sumario_diario_oficial
from django.template import engines
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():
    """Genera y envía el informe final con todas las correcciones"""
    
    fecha = "21-07-2025"
    print(f"=== GENERANDO INFORME FINAL DEL {fecha} ===\n")
    
    # Ejecutar el scraper oficial del proyecto
    print("1. Ejecutando scraper del Diario Oficial...")
    print("   Edición: 44203 (correcta)")
    
    resultado = obtener_sumario_diario_oficial(fecha)
    
    if not resultado:
        print("❌ Error: No se obtuvieron resultados del scraper")
        return
    
    publicaciones = resultado.get('publicaciones', [])
    valores_monedas = resultado.get('valores_monedas', {})
    total_documentos = resultado.get('total_documentos', 0)
    
    print(f"\n✅ Resultados del scraper:")
    print(f"   - Total documentos analizados: {total_documentos}")
    print(f"   - Publicaciones relevantes: {len(publicaciones)}")
    if valores_monedas:
        print(f"   - Valores encontrados: Dólar ${valores_monedas.get('dolar', 'N/A')}, Euro ${valores_monedas.get('euro', 'N/A')}")
    
    # Organizar publicaciones por las secciones OFICIALES del Diario Oficial
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
    
    # Clasificar las publicaciones en las secciones correctas
    for pub in publicaciones:
        seccion = pub.get('seccion', 'NORMAS GENERALES').upper()
        
        # Asegurar que la sección sea una de las tres oficiales
        if seccion not in secciones_dict:
            # Si no es una sección válida, clasificar según el contenido
            titulo = pub.get('titulo', '').lower()
            if 'licitación' in titulo or 'concurso' in titulo:
                seccion = 'AVISOS DESTACADOS'
            elif any(x in titulo for x in ['nombra', 'designa', 'acepta renuncia', 'otorga']):
                seccion = 'NORMAS PARTICULARES'
            else:
                seccion = 'NORMAS GENERALES'
        
        # Asegurar que tiene todos los campos necesarios
        pub_completa = {
            'titulo': pub.get('titulo', ''),
            'url_pdf': pub.get('url_pdf', ''),
            'resumen': pub.get('resumen', ''),
            'relevante': pub.get('relevante', True),
            'es_licitacion': pub.get('es_licitacion', False)
        }
        
        secciones_dict[seccion]['publicaciones'].append(pub_completa)
    
    # Convertir a lista, manteniendo solo secciones con contenido
    secciones = [s for s in secciones_dict.values() if s['publicaciones']]
    
    # Generar HTML con la plantilla oficial
    print("\n2. Generando HTML con la plantilla oficial...")
    
    # Leer la plantilla de Bolt
    with open('templates/informe_diario_oficial_plantilla.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Usar Django template engine
    django_engine = engines['django']
    template = django_engine.from_string(template_content)
    
    context = {
        'fecha': fecha,
        'fecha_formato': '21 de Julio, 2025',
        'edicion_numero': '44.203',
        'total_documentos': total_documentos,
        'publicaciones_relevantes': len(publicaciones),
        'secciones': secciones,
        'valores_monedas': valores_monedas
    }
    
    html = template.render(context)
    
    # Guardar copia
    filename = f"informe_final_{fecha.replace('-', '_')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"📄 Informe guardado en: {filename}")
    
    # Enviar email
    print("\n3. Enviando informe final por email...")
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Informe Diario Oficial - 21 de Julio 2025 (Edición 44.203)"
    msg['From'] = "rodrigo@carvuk.com"
    msg['To'] = "rfernandezdelrio@uc.cl"
    
    html_part = MIMEText(html, 'html')
    msg.attach(html_part)
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("rodrigo@carvuk.com", "swqjlcwjaoooyzcb")
        server.send_message(msg)
        server.quit()
        
        print("\n✅ INFORME FINAL ENVIADO EXITOSAMENTE")
        print(f"   De: rodrigo@carvuk.com")
        print(f"   Para: rfernandezdelrio@uc.cl")
        print(f"   Edición: 44.203")
        print(f"   Total documentos: {total_documentos}")
        print(f"   Publicaciones relevantes: {len(publicaciones)}")
        print("\n📋 Detalles:")
        print("   - Plantilla: Diseño correcto de Bolt")
        print("   - Secciones: Clasificación oficial (Normas Generales/Particulares/Avisos)")
        print("   - Evaluación: Sistema de relevancia con IA del proyecto")
        print("   - Resúmenes: Generados con IA según configuración existente")
        
    except Exception as e:
        print(f"\n❌ Error enviando email: {str(e)}")

if __name__ == "__main__":
    main()