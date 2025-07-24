#!/usr/bin/env python
"""
Genera el informe mejorado del 21 de julio con evaluación de relevancia y resúmenes IA
"""
import os
import sys
import django
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from django.template import engines
from alerts.evaluador_relevancia import EvaluadorRelevancia
from alerts.scraper_diario_oficial import generar_resumen_desde_texto, extraer_texto_pdf_mixto

def procesar_publicaciones_con_ia():
    """Procesa las publicaciones con evaluación de relevancia y resúmenes IA"""
    
    print("=== PROCESANDO PUBLICACIONES CON IA ===\n")
    
    # Leer el HTML con las publicaciones
    with open('edicion_correcta_21_julio.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Inicializar evaluador
    evaluador = EvaluadorRelevancia()
    
    # Diccionario para organizar por secciones
    secciones_dict = {}
    todas_las_publicaciones = []
    
    content_rows = soup.find_all('tr', class_='content')
    total = len(content_rows)
    
    print(f"Total de publicaciones a procesar: {total}\n")
    
    for i, tr in enumerate(content_rows, 1):
        tds = tr.find_all('td')
        if len(tds) >= 2:
            titulo = tds[0].get_text(strip=True)
            link = tds[1].find('a', href=True)
            pdf_url = link['href'] if link else ""
            
            if pdf_url and not pdf_url.startswith('http'):
                pdf_url = f"https://www.diariooficial.interior.gob.cl{pdf_url}"
            
            print(f"[{i}/{total}] Procesando: {titulo[:80]}...")
            
            # Determinar sección
            if "decreto" in titulo.lower():
                seccion = "DECRETOS"
            elif "resolución" in titulo.lower():
                seccion = "RESOLUCIONES"
            elif "ley" in titulo.lower():
                seccion = "LEYES"
            else:
                seccion = "NORMAS GENERALES"
            
            # Descargar y extraer texto del PDF para mejor evaluación
            texto_pdf = ""
            try:
                texto_pdf = extraer_texto_pdf_mixto(pdf_url)
                if texto_pdf:
                    print(f"   ✓ PDF descargado ({len(texto_pdf)} caracteres)")
                else:
                    print(f"   ⚠ No se pudo extraer texto del PDF")
            except Exception as e:
                print(f"   ⚠ Error descargando PDF: {str(e)}")
            
            # Evaluar relevancia con IA (usa el texto del PDF si está disponible)
            es_relevante, razon_relevancia = evaluador.evaluar_relevancia(titulo, texto_pdf)
            
            # Para este informe específico, aplicar criterios adicionales más flexibles
            # ya que el usuario quiere ver las publicaciones importantes del día
            if not es_relevante:
                # Revisar si es importante para empresas o ciudadanos aunque no sea de alcance nacional
                palabras_importantes = [
                    "modifica", "aprueba", "establece", "fija", "tarifas", 
                    "subsidio", "licitación", "concurso", "proyecto",
                    "regulaciones", "procedimientos", "normas", "reglamento"
                ]
                if any(palabra in titulo.lower() for palabra in palabras_importantes):
                    es_relevante = True
                    razon_relevancia = "Documento de interés empresarial o ciudadano"
            
            print(f"   Relevante: {'SÍ' if es_relevante else 'NO'} - {razon_relevancia}")
            
            # Generar resumen solo para publicaciones relevantes
            resumen = ""
            if es_relevante and texto_pdf:
                try:
                    resumen = generar_resumen_desde_texto(texto_pdf, titulo)
                    if resumen:
                        print(f"   ✓ Resumen generado con IA")
                    else:
                        resumen = f"Documento oficial que {titulo.lower()[:150]}..."
                except Exception as e:
                    print(f"   ⚠ Error generando resumen: {str(e)}")
                    resumen = f"Documento oficial que {titulo.lower()[:150]}..."
            elif es_relevante:
                resumen = f"Documento oficial que {titulo.lower()[:150]}..."
            
            # Determinar si es licitación
            es_licitacion = "licitación" in titulo.lower() or "concurso" in titulo.lower()
            
            publicacion = {
                'titulo': titulo,
                'url_pdf': pdf_url,
                'relevante': es_relevante,
                'es_licitacion': es_licitacion,
                'resumen': resumen,
                'razon_relevancia': razon_relevancia,
                'seccion': seccion
            }
            
            todas_las_publicaciones.append(publicacion)
            
            # Pequeña pausa para no sobrecargar la API
            if i % 5 == 0:
                time.sleep(1)
    
    # Filtrar solo las relevantes para el informe
    publicaciones_relevantes = [p for p in todas_las_publicaciones if p['relevante']]
    
    print(f"\n{'='*60}")
    print(f"RESUMEN DEL PROCESAMIENTO:")
    print(f"Total procesadas: {len(todas_las_publicaciones)}")
    print(f"Relevantes: {len(publicaciones_relevantes)}")
    print(f"{'='*60}\n")
    
    # Organizar por secciones
    for pub in publicaciones_relevantes:
        seccion = pub['seccion']
        if seccion not in secciones_dict:
            secciones_dict[seccion] = {
                'nombre': seccion,
                'descripcion': f'Documentos oficiales de tipo {seccion.lower()}',
                'publicaciones': []
            }
        secciones_dict[seccion]['publicaciones'].append(pub)
    
    # Convertir a lista ordenada
    secciones = list(secciones_dict.values())
    orden_prioridad = ['LEYES', 'DECRETOS', 'RESOLUCIONES', 'NORMAS GENERALES']
    secciones.sort(key=lambda x: orden_prioridad.index(x['nombre']) if x['nombre'] in orden_prioridad else 999)
    
    return secciones, len(todas_las_publicaciones), len(publicaciones_relevantes)

def generar_html_con_plantilla(secciones, total_docs, total_relevantes):
    """Genera el HTML usando la plantilla correcta"""
    
    # Leer la plantilla
    with open('templates/informe_diario_oficial_plantilla.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Preparar contexto
    django_engine = engines['django']
    template = django_engine.from_string(template_content)
    
    context = {
        'fecha': '21-07-2025',
        'fecha_formato': '21 de Julio, 2025',
        'edicion_numero': '44.203',
        'total_documentos': total_docs,
        'publicaciones_relevantes': total_relevantes,
        'secciones': secciones,
        'valores_monedas': {}  # No hay valores en esta edición
    }
    
    return template.render(context)

def enviar_informe(html_content):
    """Envía el informe por email"""
    
    # Configuración SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "rodrigo@carvuk.com"
    smtp_password = "swqjlcwjaoooyzcb"
    
    remitente = "rodrigo@carvuk.com"
    destinatario = "rfernandezdelrio@uc.cl"
    
    print("Enviando informe mejorado...")
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Informe Diario Oficial - 21 de Julio 2025 (Edición 44.203)"
    msg['From'] = remitente
    msg['To'] = destinatario
    
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Informe enviado exitosamente de {remitente} a {destinatario}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Procesar publicaciones con IA
    secciones, total_docs, total_relevantes = procesar_publicaciones_con_ia()
    
    # Generar HTML
    print("Generando informe HTML...")
    html = generar_html_con_plantilla(secciones, total_docs, total_relevantes)
    
    # Guardar copia
    filename = "informe_mejorado_21_julio_2025.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📄 Informe guardado en: {filename}")
    
    # Enviar
    print("\n📧 Enviando informe...")
    if enviar_informe(html):
        print("\n✅ Proceso completado exitosamente")
    else:
        print("\n⚠️ Error al enviar el informe")