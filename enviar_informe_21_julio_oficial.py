#!/usr/bin/env python
"""
Envía el informe del 21 de julio usando el sistema oficial del proyecto
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
    """Genera y envía el informe usando el sistema completo existente"""
    
    fecha = "21-07-2025"
    print(f"=== GENERANDO INFORME OFICIAL DEL {fecha} ===\n")
    
    # IMPORTANTE: Usar el scraper con la edición correcta
    print("1. Ejecutando scraper del Diario Oficial...")
    print("   Edición: 44203")
    
    # El scraper ya tiene toda la lógica de relevancia y resúmenes con IA
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
        print(f"   - Valores de monedas encontrados: {', '.join(valores_monedas.keys())}")
    
    # Organizar publicaciones por sección para la plantilla
    secciones_dict = {}
    
    for pub in publicaciones:
        # Determinar sección
        titulo = pub.get('titulo', '')
        if "decreto" in titulo.lower():
            seccion = "DECRETOS"
        elif "resolución" in titulo.lower():
            seccion = "RESOLUCIONES"
        elif "ley" in titulo.lower():
            seccion = "LEYES"
        else:
            seccion = pub.get('seccion', 'NORMAS GENERALES')
        
        if seccion not in secciones_dict:
            secciones_dict[seccion] = {
                'nombre': seccion,
                'descripcion': f'Documentos oficiales de tipo {seccion.lower()}',
                'publicaciones': []
            }
        
        # Asegurar que tiene todos los campos necesarios
        pub_completa = {
            'titulo': pub.get('titulo', ''),
            'url_pdf': pub.get('url_pdf', ''),
            'resumen': pub.get('resumen', ''),
            'relevante': pub.get('relevante', True),
            'es_licitacion': pub.get('es_licitacion', False)
        }
        
        secciones_dict[seccion]['publicaciones'].append(pub_completa)
    
    # Convertir a lista ordenada
    secciones = list(secciones_dict.values())
    orden_prioridad = ['LEYES', 'DECRETOS', 'RESOLUCIONES', 'NORMAS GENERALES']
    secciones.sort(key=lambda x: orden_prioridad.index(x['nombre']) if x['nombre'] in orden_prioridad else 999)
    
    # Generar HTML con la plantilla oficial
    print("\n2. Generando HTML con la plantilla oficial...")
    
    # Leer la plantilla
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
    filename = f"informe_oficial_{fecha.replace('-', '_')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"📄 Informe guardado en: {filename}")
    
    # Enviar email
    print("\n3. Enviando email...")
    
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
        
        print("\n✅ Informe enviado exitosamente")
        print(f"   De: rodrigo@carvuk.com")
        print(f"   Para: rfernandezdelrio@uc.cl")
        print(f"   Edición: 44.203")
        print(f"   Publicaciones relevantes: {len(publicaciones)}")
        
    except Exception as e:
        print(f"\n❌ Error enviando email: {str(e)}")

if __name__ == "__main__":
    main()