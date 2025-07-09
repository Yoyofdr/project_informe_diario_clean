import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import os
import io
import json

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from alerts.models import Empresa, HechoEsencial

# --- Nuevas importaciones ---
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuración de la IA ---
def analizar_contenido_pdf(pdf_bytes):
    """
    Analiza el contenido de un PDF usando la API de Gemini para generar un resumen
    y determinar un nivel de relevancia.
    """
    load_dotenv()
    try:
        # Configurar la API Key desde variables de entorno
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: La variable de entorno GEMINI_API_KEY no está configurada.")
            return None, None
        genai.configure(api_key=api_key)

        # Extraer texto del PDF en memoria
        reader = PdfReader(io.BytesIO(pdf_bytes))
        texto_completo = ""
        for page in reader.pages:
            texto_completo += page.extract_text() or ""
        
        if not texto_completo.strip():
            print("Advertencia: No se pudo extraer texto del PDF.")
            return None, None

        # Limitar el texto para no exceder los límites de la API
        texto_completo = texto_completo[:20000]

        # Crear el modelo generativo
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Analiza el siguiente 'Hecho Esencial' de una empresa chilena. Tu tarea es:
        1.  Crear un resumen conciso en español, de 2 a 4 frases, explicando el punto clave del documento.
        2.  Determinar un nivel de relevancia en una escala de 1 a 3, donde:
            - 1 (Baja): Eventos rutinarios, cambios menores, información de poco impacto.
            - 2 (Media): Cambios en la plana ejecutiva, acuerdos comerciales, citaciones a juntas.
            - 3 (Alta): Fusiones, adquisiciones, aumentos de capital, reparto de dividendos significativos, resultados financieros muy positivos o negativos.
        
        Formatea tu respuesta exclusivamente como un objeto JSON con las claves "resumen" y "relevancia". No incluyas nada más en tu respuesta.

        Texto del documento:
        ---
        {texto_completo}
        ---
        """
        
        response = model.generate_content(prompt)
        
        # Limpiar y parsear la respuesta JSON
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        data = json.loads(cleaned_response)
        
        resumen = data.get("resumen")
        relevancia = data.get("relevancia")

        if not isinstance(resumen, str) or not isinstance(relevancia, int):
            raise ValueError("El JSON de respuesta no tiene el formato esperado.")

        return resumen, relevancia

    except json.JSONDecodeError:
        print(f"Error: La respuesta de la IA no es un JSON válido. Respuesta: {response.text}")
        return None, None
    except Exception as e:
        print(f"Error inesperado durante el análisis con IA: {e}")
        return None, None


class Command(BaseCommand):
    """
    Comando de gestión para extraer Hechos Esenciales de la CMF y guardarlos en la base de datos.
    """
    help = 'Extrae y analiza los últimos Hechos Esenciales de la CMF.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando el scraping y análisis de Hechos Esenciales...'))
        
        # Configurar Selenium
        options = uc.ChromeOptions()
        options.add_argument('--headless')  # Activar modo invisible
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        try:
            # Usamos undetected_chromedriver
            with uc.Chrome(options=options) as driver:
                driver.get("https://www.cmfchile.cl/institucional/hechos/hechos_portada.php")
                time.sleep(10)  # Espera fija para que cargue todo el JS
                html_content = driver.page_source

                if html_content is None:
                    self.stdout.write(self.style.WARNING("html_content es None. No se pudo obtener el HTML de la página."))
                    html_content = ''

                # Guardar el HTML para depuración
                with open('debug_scraper.html', 'w', encoding='utf-8') as f:
                    f.write(html_content)

            soup = BeautifulSoup(html_content, 'html.parser')
            tabla = soup.find('table', id='lista_registros')

            if not tabla:
                # Depuración: mostrar todos los IDs de tablas encontradas
                tablas = soup.find_all('table')
                ids = [t.get('id') for t in tablas]
                self.stdout.write(self.style.WARNING(f"IDs de tablas encontradas: {ids}"))
                if tablas:
                    self.stdout.write(self.style.WARNING("Usando la primera tabla encontrada como fallback."))
                    tabla = tablas[0]
                else:
                    self.stderr.write(self.style.ERROR("No se encontró ninguna tabla en el HTML."))
                    return

            filas = tabla.find('tbody').find_all('tr') if tabla.find('tbody') else tabla.find_all('tr')
            self.stdout.write(self.style.WARNING(f"Filas encontradas en la tabla: {len(filas)}"))
            if filas:
                self.stdout.write(self.style.WARNING(f"Celdas en la primera fila: {len(filas[0].find_all('td'))}"))
                self.stdout.write(self.style.WARNING(f"Contenido de la primera fila: {[td.text.strip() for td in filas[0].find_all('td')]}"))

            nuevos = 0
            actualizados = 0
            existentes_sin_cambios = 0
            errores = 0

            for fila in filas:
                celdas = fila.find_all('td')
                self.stdout.write(self.style.WARNING(f"Fila: {filas.index(fila)}, celdas: {len(celdas)}"))
                if not celdas or len(celdas) < 4:
                    continue

                # Loguear el HTML completo de cada celda para depuración
                for idx, celda in enumerate(celdas):
                    self.stdout.write(self.style.WARNING(f"HTML de celdas[{idx}]: {celda}"))

                # Extracción de datos de la nueva estructura
                fecha_hora_str = celdas[0].text.strip()
                # Filtrar solo hechos desde ahora en adelante
                try:
                    fecha_hora_dt = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M:%S")
                except ValueError:
                    self.stdout.write(self.style.WARNING(f"Formato de fecha inválido: {fecha_hora_str}. Saltando."))
                    continue
                if fecha_hora_dt < datetime.now():
                    continue
                # Extraer enlace y texto desde la celda 1
                asunto_link = celdas[1].find('a')
                if not asunto_link:
                    continue
                asunto = asunto_link.text.strip()
                enlace = asunto_link['href']
                if not enlace.startswith('http'):
                    enlace = "https://www.cmfchile.cl" + enlace
                razon_social = celdas[2].text.strip()
                self.stdout.write(self.style.WARNING(f"Extraído: fecha='{fecha_hora_str}', empresa='{razon_social}', asunto='{asunto}', enlace='{enlace}'"))

                # Procesamiento de fecha y hora
                try:
                    fecha_hora_dt = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M:%S")
                    current_year = datetime.now().year
                    if fecha_hora_dt.year > current_year:
                        self.stdout.write(self.style.WARNING(f"  - Fecha futura detectada ({fecha_hora_dt.year}). Corregida a {current_year}."))
                        fecha_hora_dt = fecha_hora_dt.replace(year=current_year)
                    fecha_hora_aware = make_aware(fecha_hora_dt)
                except ValueError:
                    self.stdout.write(self.style.WARNING(f"Formato de fecha inválido para '{razon_social}': {fecha_hora_str}. Saltando."))
                    continue

                empresa, created_empresa = Empresa.objects.get_or_create(nombre=razon_social)
                if created_empresa:
                    self.stdout.write(self.style.NOTICE(f"  - Empresa '{razon_social}' no encontrada. Se ha creado una nueva entrada."))

                hecho, created = HechoEsencial.objects.get_or_create(
                    url=enlace,
                    defaults={
                        'empresa': empresa,
                        'titulo': asunto,
                        'fecha_publicacion': fecha_hora_aware,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"  -> Hecho NUEVO creado en la base de datos."))
                else:
                    self.stdout.write(self.style.WARNING(f"  -> Hecho YA EXISTÍA en la base de datos."))

                # Si no es nuevo y ya tiene resumen, lo saltamos para no re-analizar.
                if not created and hecho.resumen:
                    existentes_sin_cambios += 1
                    continue
                
                self.stdout.write(self.style.NOTICE(f"Analizando: {empresa.nombre} - {hecho.titulo}"))

                # Definir headers para la descarga del PDF
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                }
                # Descargar y analizar el PDF
                pdf_response = requests.get(enlace, headers=headers, timeout=30)
                pdf_response.raise_for_status()
                
                resumen_ia, relevancia_ia = analizar_contenido_pdf(pdf_response.content)

                if resumen_ia and relevancia_ia:
                    hecho.resumen = resumen_ia
                    hecho.relevancia = relevancia_ia
                    hecho.save()
                    if created:
                        nuevos += 1
                        self.stdout.write(self.style.SUCCESS(f"  -> Nuevo hecho guardado y analizado con relevancia {relevancia_ia}."))
                    else:
                        actualizados += 1
                        self.stdout.write(self.style.SUCCESS(f"  -> Hecho existente actualizado con relevancia {relevancia_ia}."))
                else:
                    errores += 1
                    self.stdout.write(self.style.WARNING(f"  -> No se pudo analizar el documento para '{razon_social}'."))

                # Pequeña pausa para no saturar el servidor
                time.sleep(1)

            self.stdout.write(self.style.SUCCESS(f'Proceso completado. Nuevos: {nuevos}, Actualizados: {actualizados}, Ya analizados: {existentes_sin_cambios}, Errores: {errores}.'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error general durante el scraping con Selenium: {e}"))
            import traceback
            traceback.print_exc() 