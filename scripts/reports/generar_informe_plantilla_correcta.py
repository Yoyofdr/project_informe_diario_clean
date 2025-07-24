#!/usr/bin/env python
"""
Genera el informe del 21 de julio usando la plantilla correcta de Bolt
"""
import os
import sys
import django
from datetime import datetime
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from django.template import Template, Context

def obtener_publicaciones_organizadas():
    """Obtiene las publicaciones organizadas por sección"""
    
    with open('edicion_correcta_21_julio.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Diccionario para organizar por secciones
    secciones_dict = {}
    
    content_rows = soup.find_all('tr', class_='content')
    
    for tr in content_rows:
        tds = tr.find_all('td')
        if len(tds) >= 2:
            titulo = tds[0].get_text(strip=True)
            link = tds[1].find('a', href=True)
            pdf_url = link['href'] if link else ""
            
            if pdf_url and not pdf_url.startswith('http'):
                pdf_url = f"https://www.diariooficial.interior.gob.cl{pdf_url}"
            
            # Determinar sección
            if "decreto" in titulo.lower():
                seccion = "DECRETOS"
            elif "resolución" in titulo.lower():
                seccion = "RESOLUCIONES"
            elif "ley" in titulo.lower():
                seccion = "LEYES"
            else:
                seccion = "NORMAS GENERALES"
            
            # Determinar si es relevante
            relevante = any(palabra in titulo.lower() for palabra in [
                'modifica', 'aprueba', 'establece', 'fija', 'reglamenta', 
                'dispone', 'tarifas', 'regulaciones'
            ])
            
            # Determinar si es licitación
            es_licitacion = "licitación" in titulo.lower() or "concurso" in titulo.lower()
            
            publicacion = {
                'titulo': titulo,
                'url_pdf': pdf_url,
                'relevante': relevante,
                'es_licitacion': es_licitacion,
                'resumen': f"Documento oficial que {titulo.lower()[:150]}..."
            }
            
            # Agregar a la sección correspondiente
            if seccion not in secciones_dict:
                secciones_dict[seccion] = {
                    'nombre': seccion,
                    'descripcion': f'Documentos oficiales de tipo {seccion.lower()}',
                    'publicaciones': []
                }
            
            secciones_dict[seccion]['publicaciones'].append(publicacion)
    
    # Convertir a lista ordenada
    secciones = list(secciones_dict.values())
    
    # Ordenar secciones por prioridad
    orden_prioridad = ['LEYES', 'DECRETOS', 'RESOLUCIONES', 'NORMAS GENERALES']
    secciones.sort(key=lambda x: orden_prioridad.index(x['nombre']) if x['nombre'] in orden_prioridad else 999)
    
    return secciones

def generar_informe_con_plantilla():
    """Genera el informe usando la plantilla correcta"""
    
    # Leer la plantilla
    with open('templates/informe_diario_oficial_plantilla.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Obtener datos
    secciones = obtener_publicaciones_organizadas()
    total_documentos = sum(len(s['publicaciones']) for s in secciones)
    publicaciones_relevantes = sum(sum(1 for p in s['publicaciones'] if p['relevante']) for s in secciones)
    
    # Preparar contexto para Django Template
    from django.template import engines
    django_engine = engines['django']
    template = django_engine.from_string(template_content)
    
    context = {
        'fecha': '21-07-2025',
        'fecha_formato': '21 de Julio, 2025',
        'edicion_numero': '44.203',
        'total_documentos': total_documentos,
        'publicaciones_relevantes': publicaciones_relevantes,
        'secciones': secciones,
        'valores_monedas': {}  # No hay valores de monedas en esta edición
    }
    
    # Renderizar
    html_final = template.render(context)
    
    return html_final

def enviar_informe_final(html_content):
    """Envía el informe con las direcciones correctas"""
    
    # Configuración SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "rodrigo@carvuk.com"
    smtp_password = "swqjlcwjaoooyzcb"
    
    # Direcciones
    remitente = "rodrigo@carvuk.com"
    destinatario = "rfernandezdelrio@uc.cl"
    
    print("=== ENVIANDO INFORME CON PLANTILLA CORRECTA ===")
    print(f"De: {remitente}")
    print(f"Para: {destinatario}")
    
    # Crear mensaje
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Informe Diario Oficial - 21 de Julio 2025 (Edición 44.203)"
    msg['From'] = remitente
    msg['To'] = destinatario
    
    # Agregar contenido HTML
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    try:
        print("\nConectando al servidor SMTP...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        print("Enviando email...")
        server.send_message(msg)
        server.quit()
        
        print("\n✅ Email enviado exitosamente con la plantilla correcta")
        print(f"📧 De: {remitente}")
        print(f"📧 Para: {destinatario}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error al enviar email: {str(e)}")
        return False

if __name__ == "__main__":
    print("1. Generando informe con la plantilla correcta...")
    html = generar_informe_con_plantilla()
    
    # Guardar copia local
    filename = "informe_plantilla_correcta_21_julio_2025.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"   📄 Informe guardado en: {filename}")
    
    # Enviar por email
    print("\n2. Enviando informe por email...")
    if enviar_informe_final(html):
        print("\n✅ Proceso completado exitosamente")
    else:
        print("\n⚠️  Error al enviar el informe")