#!/usr/bin/env python
"""
Script para generar y enviar el informe del Diario Oficial por correo
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')

# Cargar variables del .env ANTES de django.setup()
from dotenv import load_dotenv
load_dotenv()

django.setup()

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def obtener_publicaciones_diario(fecha):
    """Obtiene las publicaciones del Diario Oficial usando el scraper completo"""
    
    # Importar el scraper original para usar sus funciones
    from alerts.scraper_diario_oficial import (
        obtener_sumario_diario_oficial,
        es_relevante,
        extraer_texto_pdf_mixto,
        generar_resumen_desde_texto
    )
    
    print(f"Obteniendo publicaciones del {fecha}")
    
    # Usar el scraper original que ya tiene toda la lógica
    try:
        resultado = obtener_sumario_diario_oficial(fecha)
        
        if resultado and resultado.get('publicaciones'):
            publicaciones = resultado['publicaciones']
            valores_monedas = resultado.get('valores_monedas')
            
            # Si no hay resúmenes, intentar generarlos
            for pub in publicaciones[:5]:  # Limitar a las primeras 5 para no demorar mucho
                if not pub.get('resumen') or pub['resumen'] == 'No se pudo generar un resumen relevante.':
                    try:
                        # Intentar extraer texto del PDF y generar resumen
                        texto_pdf = extraer_texto_pdf_mixto(pub['url_pdf'])
                        if texto_pdf:
                            resumen = generar_resumen_desde_texto(texto_pdf, pub['titulo'])
                            pub['resumen'] = resumen
                    except:
                        pass
            
            print(f"Publicaciones encontradas: {len(publicaciones)}")
            return publicaciones, valores_monedas
        else:
            print("No se encontraron publicaciones con el scraper original")
            return [], None
            
    except Exception as e:
        print(f"Error usando scraper original: {e}")
        
        # Fallback: método simplificado
        print("Usando método simplificado como fallback...")
        
        EDITIONS = {
            "11-07-2025": "44196",
            "12-07-2025": "44197",
            "10-07-2025": "44195",
        }
        
        if fecha in EDITIONS:
            edition = EDITIONS[fecha]
        else:
            try:
                base_date = datetime.strptime("07-07-2025", "%d-%m-%Y")
                target_date = datetime.strptime(fecha, "%d-%m-%Y")
                days_diff = (target_date - base_date).days
                edition = str(44192 + days_diff)
            except:
                edition = ""
        
        url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}&v=1"
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        publicaciones = []
        
        try:
            driver.get(url)
            time.sleep(5)
            
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            pdfs = soup.find_all("a", href=lambda x: x and x.endswith(".pdf"))
            
            for pdf in pdfs[:10]:  # Limitar para no demorar
                href = pdf.get('href')
                
                if 'sumarios' in href:
                    continue
                    
                parent = pdf.find_parent('tr')
                titulo = "Sin título"
                
                if parent:
                    celdas = parent.find_all('td')
                    for celda in celdas:
                        texto = celda.get_text(strip=True)
                        if texto and not texto.startswith("Ver PDF") and len(texto) > 10:
                            titulo = texto
                            break
                
                url_completa = href if href.startswith('http') else f"https://www.diariooficial.interior.gob.cl{href}"
                
                # Intentar obtener resumen
                resumen = "Documento oficial del Diario Oficial"
                try:
                    from alerts.scraper_diario_oficial import extraer_texto_pdf_mixto, generar_resumen_desde_texto
                    texto_pdf = extraer_texto_pdf_mixto(url_completa)
                    if texto_pdf:
                        resumen = generar_resumen_desde_texto(texto_pdf, titulo)
                except:
                    pass
                
                publicaciones.append({
                    'titulo': titulo,
                    'url_pdf': url_completa,
                    'seccion': 'NORMAS GENERALES',
                    'relevante': es_relevante(titulo),
                    'resumen': resumen
                })
                
        finally:
            driver.quit()
        
        return publicaciones, None

def generar_html_informe(fecha, publicaciones, valores_monedas=None):
    """Genera el HTML del informe con el diseño profesional"""
    
    # Filtrar publicaciones relevantes
    relevantes = [p for p in publicaciones if p['relevante']][:5]
    if not relevantes:
        relevantes = publicaciones[:5]
    
    # Calcular tiempo de lectura estimado
    tiempo_lectura = max(2, len(relevantes))
    
    # Formatear fecha
    from datetime import datetime as dt
    import locale
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES')
        except:
            pass
    
    fecha_obj = dt.strptime(fecha, '%d-%m-%Y')
    fecha_formato = fecha_obj.strftime('%d-%m-%Y')
    
    # Generar bloques de noticias
    noticias_html = ""
    for pub in relevantes:
        # Limpiar título
        titulo = pub['titulo']
        if len(titulo) > 150:
            titulo = titulo[:147] + "..."
            
        # Generar resumen
        resumen = pub.get('resumen', '')
        if not resumen or resumen == 'Documento del Diario Oficial':
            # Generar resumen basado en el título
            if "LEY" in titulo.upper():
                resumen = "Nueva legislación que establece regulaciones y normativas de interés general."
            elif "DECRETO" in titulo.upper():
                resumen = "Decreto oficial que establece nuevas disposiciones administrativas."
            elif "RESOLUCIÓN" in titulo.upper():
                resumen = "Resolución administrativa con efectos en el ámbito público."
            else:
                resumen = "Documento oficial publicado en el Diario Oficial de la República."
        
        noticias_html += f"""
        <div style='border-left:5px solid #2563eb; padding-left:20px; margin-bottom:22px; background:#f8fafc; border-radius:10px; padding-top:14px; padding-bottom:14px; padding-right:20px; box-shadow:0 2px 12px #2563eb0a;'>
          <div style='font-size:1.18em; font-weight:800; margin-bottom:4px; color:#1e293b; letter-spacing:-0.5px;'>{titulo}</div>
          <div style='color:#334155; font-size:1.04em; margin-bottom:7px; line-height:1.6;'>{resumen}</div>
          <a href='{pub['url_pdf']}' target='_blank' style='color:#2563eb; text-decoration:underline; font-size:1em; font-weight:600;'>Ver documento</a>
        </div>"""
    
    # TODO: Agregar valores reales de monedas cuando estén disponibles
    valores_monedas_html = """
      <div style='padding:0 32px 0 32px;'>
        <div style='margin-top:24px; margin-bottom:24px; padding:22px; background:#f8f9fa; border-radius:14px; border:1.5px solid #e0e0e0; color:#222; font-size:1.13em; font-weight:600; box-shadow:0 2px 12px #2563eb0a;'>
          <span style='color:#2563eb; font-weight:800;'>Valores de referencia publicados por el Banco Central de Chile:</span><br>
          <span style='color:#64748b; font-size:0.95em;'>Los valores de monedas se actualizarán cuando estén disponibles en el Diario Oficial.</span>
        </div>
      </div>"""
    
    html = f"""<html>
<body style='margin:0; padding:0; background:#f6f8fb; font-family: Segoe UI, Arial, sans-serif; color:#1e293b;'>
  <div style='width:100%; background:#f6f8fb;'>
    <div style='background:#fff; width:100%; max-width:100%; margin:0; border-radius:0; box-shadow:none; padding:0;'>
      <!-- Header ordenado -->
      <div style="background:linear-gradient(90deg,#2563eb 0%,#6366f1 100%); color:#fff; padding:32px 40px 24px 40px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <div>
            <div style="font-size:1.5em; font-weight:800; margin-bottom:2px;">Informe Diario</div>
            <div style="font-size:1em; color:#e0e7ff; margin-bottom:10px;">informes@informediario.cl</div>
          </div>
          <div style="font-size:1.1em; color:#e0e7ff; font-weight:600; margin-top:4px;">Hoy, 08:00</div>
        </div>
        <div style="font-size:2em; font-weight:900; margin-top:18px; letter-spacing:-1.5px; text-shadow:0 2px 8px #0001;">
          Resumen del Diario Oficial - {fecha_formato}
        </div>
      </div>
      <!-- Badges -->
      <div style='padding:20px 32px 0 32px;'>
        <div style='display:flex; gap:12px; margin-bottom:8px;'>
          <span style='display:inline-block; background:#e0e7ff; color:#2563eb; font-weight:700; border-radius:14px; padding:7px 18px; font-size:1em; box-shadow:0 2px 8px #2563eb11;'>
            {len(publicaciones)} documentos analizados
          </span>
          <span style='display:inline-block; background:#d1fae5; color:#059669; font-weight:700; border-radius:14px; padding:7px 18px; font-size:1em; box-shadow:0 2px 8px #05966911;'>
            {tiempo_lectura} min de lectura
          </span>
        </div>
      </div>
      <!-- Separador -->
      <div style='height:1px; background:#e5e7eb; margin:18px 32px 0 32px;'></div>
      <!-- Lista de hechos -->
      <div style='padding:18px 32px 0 32px;'>
        {noticias_html}
      </div>
      <!-- Separador -->
      <div style='height:1px; background:#e5e7eb; margin:18px 32px 0 32px;'></div>
      <!-- Valores de monedas -->
      {valores_monedas_html}
      <!-- Separador -->
      <div style='height:1px; background:#e5e7eb; margin:18px 32px 0 32px;'></div>
      <!-- Footer -->
      <div style='padding:24px 32px 0 32px;'>
        <div style='display:flex; align-items:center; justify-content:space-between; border-top:1px solid #e5e7eb; padding-top:18px; margin-top:10px;'>
          <div style='color:#64748b; font-size:1.05em; text-align:left; font-weight:500;'>
            Tiempo de lectura: {tiempo_lectura} minutos
          </div>
          <a href='https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}' style='background:#2563eb; color:#fff; font-weight:800; border-radius:10px; padding:13px 30px; text-decoration:none; font-size:1.08em; box-shadow:0 2px 12px 0 #2563eb33; border:0; display:inline-block;'>Ver informe completo →</a>
        </div>
      </div>
      <!-- Footer legal -->
      <div style='background:#f6f8fb; color:#64748b; font-size:1em; text-align:center; padding:26px 32px 20px 32px; border-radius:0;'>
        Para gestionar tus suscripciones, visita <a href='#' style='color:#2563eb; text-decoration:none; font-weight:600;'>tu dashboard</a>.<br>
        &copy; 2025 Informe Diario. Todos los derechos reservados.
      </div>
    </div>
  </div>
</body>
</html>"""
    
    return html

def enviar_informe_email(destinatario, fecha, html_content):
    """Envía el informe por correo"""
    
    # Configurar el correo
    asunto = f"Informe Diario Oficial - {fecha}"
    
    from django.conf import settings
    
    email = EmailMessage(
        subject=asunto,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Usar el email configurado
        to=[destinatario],
    )
    
    # Configurar como HTML
    email.content_subtype = "html"
    
    # Enviar
    try:
        email.send()
        print(f"✅ Informe enviado exitosamente a: {destinatario}")
        return True
    except Exception as e:
        print(f"❌ Error enviando correo: {e}")
        return False

def main():
    """Función principal"""
    
    # Obtener fecha de hoy
    fecha_hoy = datetime.now().strftime("%d-%m-%Y")
    
    print(f"\n=== GENERANDO INFORME DEL DIARIO OFICIAL ===")
    print(f"Fecha: {fecha_hoy}\n")
    
    # Obtener publicaciones (la función devuelve una tupla)
    publicaciones, valores_monedas = obtener_publicaciones_diario(fecha_hoy)
    
    if not publicaciones:
        print("No se encontraron publicaciones")
        return
    
    # Generar HTML
    print("\nGenerando informe HTML...")
    html_content = generar_html_informe(fecha_hoy, publicaciones, valores_monedas)
    
    # Guardar copia local
    filename = f"informe_email_{fecha_hoy.replace('-', '_')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Informe guardado localmente: {filename}")
    
    # Solicitar destinatario
    destinatario = input("\nIngrese el email destinatario (o presione ENTER para cancelar): ").strip()
    
    if destinatario:
        # Enviar por correo
        enviar_informe_email(destinatario, fecha_hoy, html_content)
    else:
        print("Envío cancelado")

if __name__ == "__main__":
    main()