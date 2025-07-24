#!/usr/bin/env python
"""
Script para generar y enviar el informe del Diario Oficial con formato estructurado por ministerios
"""
import os
import sys
import django
from datetime import datetime
import re
import pytz

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')

# Cargar variables del .env ANTES de django.setup()
from dotenv import load_dotenv
load_dotenv()

django.setup()

from django.core.mail import EmailMessage
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def extraer_ministerio(titulo):
    """Extrae el ministerio del título del documento"""
    # Patrones comunes de ministerios
    ministerios = {
        'HACIENDA': 'MINISTERIO DE HACIENDA',
        'ENERGÍA': 'MINISTERIO DE ENERGÍA',
        'SALUD': 'MINISTERIO DE SALUD',
        'EDUCACIÓN': 'MINISTERIO DE EDUCACIÓN',
        'TRABAJO': 'MINISTERIO DEL TRABAJO Y PREVISIÓN SOCIAL',
        'INTERIOR': 'MINISTERIO DEL INTERIOR Y SEGURIDAD PÚBLICA',
        'JUSTICIA': 'MINISTERIO DE JUSTICIA Y DERECHOS HUMANOS',
        'DEFENSA': 'MINISTERIO DE DEFENSA NACIONAL',
        'ECONOMÍA': 'MINISTERIO DE ECONOMÍA, FOMENTO Y TURISMO',
        'AGRICULTURA': 'MINISTERIO DE AGRICULTURA',
        'OBRAS PÚBLICAS': 'MINISTERIO DE OBRAS PÚBLICAS',
        'VIVIENDA': 'MINISTERIO DE VIVIENDA Y URBANISMO',
        'TRANSPORTES': 'MINISTERIO DE TRANSPORTES Y TELECOMUNICACIONES',
        'MINERÍA': 'MINISTERIO DE MINERÍA',
        'DESARROLLO SOCIAL': 'MINISTERIO DE DESARROLLO SOCIAL Y FAMILIA',
        'MEDIO AMBIENTE': 'MINISTERIO DEL MEDIO AMBIENTE',
        'MUJER': 'MINISTERIO DE LA MUJER Y LA EQUIDAD DE GÉNERO',
        'DEPORTE': 'MINISTERIO DEL DEPORTE',
        'CULTURA': 'MINISTERIO DE LAS CULTURAS, LAS ARTES Y EL PATRIMONIO',
        'CIENCIA': 'MINISTERIO DE CIENCIA, TECNOLOGÍA, CONOCIMIENTO E INNOVACIÓN',
        'BANCO CENTRAL': 'BANCO CENTRAL DE CHILE',
        'CONTRALORÍA': 'CONTRALORÍA GENERAL DE LA REPÚBLICA'
    }
    
    titulo_upper = titulo.upper()
    
    for key, nombre_completo in ministerios.items():
        if key in titulo_upper:
            return nombre_completo
    
    # Si no se encuentra, buscar "MINISTERIO DE" en el título
    if "MINISTERIO DE" in titulo_upper:
        match = re.search(r'MINISTERIO DE[^,;.]+', titulo_upper)
        if match:
            return match.group(0)
    
    return "OTROS ORGANISMOS"

def formatear_documento(titulo):
    """Formatea el título del documento de manera concisa"""
    # Limpiar y formatear el título
    titulo = titulo.strip()
    
    # Buscar patrones comunes
    patterns = [
        (r'(Decreto|DECRETO)\s*(número|Nº|N°)?\s*(\d+\w*)', r'Decreto número \3'),
        (r'(Resolución|RESOLUCIÓN)\s*(exenta)?\s*(número|Nº|N°)?\s*(\d+)', r'Resolución exenta número \4'),
        (r'(Ley|LEY)\s*(número|Nº|N°)?\s*(\d+\.\d+)', r'Ley Nº \3'),
        (r'(Extracto|EXTRACTO)\s*de\s*(.*)', r'Extracto de \2'),
    ]
    
    for pattern, replacement in patterns:
        titulo = re.sub(pattern, replacement, titulo, flags=re.IGNORECASE)
    
    # Quitar fechas del final si existen
    titulo = re.sub(r',?\s*de\s*\d{4}\s*\.?$', ', de 2025', titulo)
    
    # Agregar punto final si no lo tiene
    if not titulo.endswith('.'):
        titulo += '.'
    
    # Limitar longitud y agregar descripción si es necesario
    if len(titulo) > 200:
        titulo = titulo[:197] + "..."
    
    return titulo

def obtener_publicaciones_estructuradas(fecha):
    """Obtiene las publicaciones del Diario Oficial organizadas por ministerio"""
    
    EDITIONS = {
        "11-07-2025": "44196",
        "12-07-2025": "44197",
        "10-07-2025": "44195",
        "07-07-2025": "44192",
        "08-07-2025": "44193",
        "13-07-2025": "44198",
        "14-07-2025": "44199",
        "15-07-2025": "44200",
        "16-07-2025": "44201",
        "17-07-2025": "44202",
        "18-07-2025": "44203",
        "19-07-2025": "44204",
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
    
    publicaciones_por_ministerio = {}
    
    try:
        print(f"Obteniendo publicaciones del {fecha}")
        driver.get(url)
        time.sleep(5)
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        # Buscar todos los PDFs
        pdfs = soup.find_all("a", href=lambda x: x and x.endswith(".pdf"))
        
        for pdf in pdfs:
            href = pdf.get('href')
            
            # Omitir sumarios
            if 'sumarios' in href:
                continue
            
            # Buscar título en la tabla
            parent = pdf.find_parent('tr')
            titulo_original = ""
            
            if parent:
                celdas = parent.find_all('td')
                for celda in celdas:
                    texto = celda.get_text(strip=True)
                    if texto and not texto.startswith("Ver PDF") and len(texto) > 10:
                        titulo_original = texto
                        break
            
            if not titulo_original:
                continue
            
            # Extraer ministerio y formatear
            ministerio = extraer_ministerio(titulo_original)
            titulo_formateado = formatear_documento(titulo_original)
            
            # Agregar descripción basada en el tipo
            descripcion = ""
            if "Decreto" in titulo_formateado:
                if "fija" in titulo_original.lower():
                    descripcion = "- " + re.sub(r'^[^-]*- ', '', titulo_original)
                elif "modifica" in titulo_original.lower():
                    descripcion = "- " + re.sub(r'^[^-]*- ', '', titulo_original)
                else:
                    # Buscar el contenido después del primer guión
                    partes = titulo_original.split('-', 1)
                    if len(partes) > 1:
                        descripcion = "- " + partes[1].strip()
            elif "Resolución" in titulo_formateado:
                partes = titulo_original.split('.-', 1)
                if len(partes) > 1:
                    descripcion = "- " + partes[1].strip()
            elif "Extracto" in titulo_formateado:
                # Buscar descripción después de ".-"
                partes = titulo_original.split('.-', 1)
                if len(partes) > 1:
                    descripcion = "- " + partes[1].strip()
            
            # Limpiar descripción
            if descripcion:
                descripcion = descripcion.rstrip('.')
                if len(descripcion) > 150:
                    descripcion = descripcion[:147] + "..."
            
            # Organizar por ministerio
            if ministerio not in publicaciones_por_ministerio:
                publicaciones_por_ministerio[ministerio] = []
            
            publicaciones_por_ministerio[ministerio].append({
                'titulo': titulo_formateado,
                'descripcion': descripcion,
                'url_pdf': href if href.startswith('http') else f"https://www.diariooficial.interior.gob.cl{href}"
            })
    
    finally:
        driver.quit()
    
    return publicaciones_por_ministerio

def generar_html_informe_estructurado(fecha, publicaciones_por_ministerio):
    """Genera el HTML del informe estructurado por ministerios"""
    
    fecha_obj = datetime.strptime(fecha, '%d-%m-%Y')
    # Mapeo de meses en español
    meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    fecha_formato = f"{fecha_obj.day} de {meses[fecha_obj.month]} de {fecha_obj.year}"
    
    # Generar contenido por ministerios
    contenido_ministerios = ""
    numero_romano = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii", "xiii", "xiv", "xv"]
    contador = 0
    
    # Ordenar ministerios alfabéticamente
    ministerios_ordenados = sorted(publicaciones_por_ministerio.keys())
    
    for ministerio in ministerios_ordenados:
        documentos = publicaciones_por_ministerio[ministerio]
        if not documentos:
            continue
            
        contenido_ministerios += f"""
        <div style='margin-bottom:28px;'>
          <div style='font-size:1.15em; font-weight:700; color:#1e293b; margin-bottom:12px;'>
            {numero_romano[contador] if contador < len(numero_romano) else str(contador+1)}. {ministerio}
          </div>"""
        
        for doc in documentos:
            contenido_ministerios += f"""
          <div style='margin-left:20px; margin-bottom:10px;'>
            <div style='color:#334155; font-size:1.02em; line-height:1.6;'>
              • {doc['titulo']}{doc['descripcion']}
            </div>
          </div>"""
        
        contenido_ministerios += "</div>"
        contador += 1
    
    # Calcular estadísticas
    total_docs = sum(len(docs) for docs in publicaciones_por_ministerio.values())
    total_ministerios = len(publicaciones_por_ministerio)
    
    html = f"""<html>
<body style='margin:0; padding:0; background:#f6f8fb; font-family: Segoe UI, Arial, sans-serif; color:#1e293b;'>
  <div style='width:100%; background:#f6f8fb;'>
    <div style='background:#fff; width:100%; max-width:100%; margin:0; border-radius:0; box-shadow:none; padding:0;'>
      <!-- Header -->
      <div style="background:linear-gradient(90deg,#2563eb 0%,#6366f1 100%); color:#fff; padding:32px 40px 24px 40px;">
        <div style="font-size:2.2em; font-weight:900; letter-spacing:-1px; text-shadow:0 2px 8px #0001;">
          Informe Diario Oficial {fecha_formato}
        </div>
      </div>
      <!-- Estadísticas -->
      <div style='padding:20px 40px;'>
        <div style='display:flex; gap:16px;'>
          <span style='background:#e0e7ff; color:#2563eb; font-weight:600; border-radius:8px; padding:6px 16px; font-size:0.95em;'>
            {total_ministerios} ministerios
          </span>
          <span style='background:#d1fae5; color:#059669; font-weight:600; border-radius:8px; padding:6px 16px; font-size:0.95em;'>
            {total_docs} documentos publicados
          </span>
        </div>
      </div>
      <!-- Contenido -->
      <div style='padding:0 40px 30px 40px;'>
        {contenido_ministerios}
      </div>
      <!-- Footer -->
      <div style='background:#f8fafc; padding:20px 40px; border-top:1px solid #e5e7eb;'>
        <div style='text-align:center; color:#64748b; font-size:0.95em;'>
          <a href='https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}' 
             style='color:#2563eb; text-decoration:none; font-weight:600;'>
            Ver edición completa del Diario Oficial
          </a>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""
    
    return html

def main():
    """Función principal"""
    
    # Obtener fecha actual en zona horaria de Chile
    zona_horaria_chile = pytz.timezone('America/Santiago')
    fecha_actual = datetime.now(zona_horaria_chile)
    fecha = fecha_actual.strftime("%d-%m-%Y")
    
    # Solo los domingos no hay edición del Diario Oficial
    if fecha_actual.weekday() == 6:  # Domingo = 6
        print("Es domingo, no hay edición del Diario Oficial, usando la última fecha disponible...")
        fecha = "12-07-2025"  # Última fecha disponible en el mapeo
    
    print(f"\n=== GENERANDO INFORME ESTRUCTURADO DEL DIARIO OFICIAL ===")
    print(f"Fecha: {fecha}\n")
    
    # Obtener publicaciones
    publicaciones_por_ministerio = obtener_publicaciones_estructuradas(fecha)
    
    # Si no se encuentran publicaciones, intentar con fechas anteriores
    fechas_alternativas = ["17-07-2025", "16-07-2025", "15-07-2025", "12-07-2025"]
    
    if not publicaciones_por_ministerio:
        print("No se encontraron publicaciones para la fecha actual, intentando con fechas anteriores...")
        
        for fecha_alt in fechas_alternativas:
            print(f"Intentando con fecha: {fecha_alt}")
            publicaciones_por_ministerio = obtener_publicaciones_estructuradas(fecha_alt)
            if publicaciones_por_ministerio:
                fecha = fecha_alt
                break
        
        if not publicaciones_por_ministerio:
            print("No se encontraron publicaciones en ninguna fecha reciente")
            return
    
    # Generar HTML
    print("\nGenerando informe estructurado...")
    html_content = generar_html_informe_estructurado(fecha, publicaciones_por_ministerio)
    
    # Guardar copia local
    filename = f"informe_estructurado_{fecha.replace('-', '_')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Informe guardado: {filename}")
    
    # Enviar correo
    print("\nEnviando correo a rfernandezdelrio@uc.cl...")
    
    fecha_obj = datetime.strptime(fecha, '%d-%m-%Y')
    meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    fecha_formato = f"{fecha_obj.day} de {meses[fecha_obj.month]} de {fecha_obj.year}"
    
    email = EmailMessage(
        subject=f"Informe Diario Oficial {fecha_formato}",
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['rfernandezdelrio@uc.cl'],
    )
    
    email.content_subtype = "html"
    
    try:
        email.send()
        print("✅ Correo enviado exitosamente!")
    except Exception as e:
        print(f"❌ Error enviando correo: {e}")

if __name__ == "__main__":
    main()