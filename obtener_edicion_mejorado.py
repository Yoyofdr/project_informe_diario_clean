#!/usr/bin/env python
"""
Función mejorada para obtener el número de edición automáticamente
"""
import os
import sys
import django
import time
import json
from datetime import datetime

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def obtener_numero_edicion_mejorado(fecha, driver=None):
    """
    Obtiene el número de edición para una fecha específica del Diario Oficial.
    Versión mejorada que detecta automáticamente la edición correcta.
    """
    print(f"[EDITION] Buscando número de edición para fecha: {fecha}")
    
    # Primero intentar con caché local
    try:
        cache_file = os.path.join(os.path.dirname(__file__), 'edition_cache.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache = json.load(f)
                if fecha in cache:
                    edition = cache[fecha]
                    print(f"[EDITION] Número de edición encontrado en caché: {edition}")
                    return edition
    except Exception as e:
        print(f"[EDITION] Error leyendo caché: {e}")
    
    # Si no está en caché, usar Selenium para detectar automáticamente
    driver_temporal = False
    driver_creado = driver
    
    try:
        if driver_creado is None:
            driver_temporal = True
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            # Agregar user agent para evitar detección
            options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            driver_creado = webdriver.Chrome(options=options)
            driver_creado.set_page_load_timeout(30)
        
        # Convertir fecha al formato que usa la URL (YYYY/MM/DD)
        dia, mes, anio = fecha.split('-')
        
        # Estrategia 1: Ir directamente a la URL de la fecha sin edición
        url_fecha = f"https://www.diariooficial.interior.gob.cl/publicaciones/{anio}/{mes}/{dia}/"
        print(f"[EDITION] Navegando a: {url_fecha}")
        driver_creado.get(url_fecha)
        time.sleep(3)
        
        # Buscar el selector de ediciones
        try:
            # Esperar a que el selector de ediciones esté presente
            edition_select_element = WebDriverWait(driver_creado, 10).until(
                EC.presence_of_element_located((By.ID, "ediciones"))
            )
            
            # Obtener la opción seleccionada
            select = Select(edition_select_element)
            selected_option = select.first_selected_option
            
            # El value contiene la URL completa con la edición
            selected_value = selected_option.get_attribute("value")
            print(f"[EDITION] Valor seleccionado: {selected_value}")
            
            # Extraer el número de edición de la URL
            import re
            match = re.search(r'/edicion-(\d+)/?', selected_value)
            if match:
                edition_number = match.group(1)
                print(f"[EDITION] Número de edición detectado: {edition_number}")
                
                # Actualizar el caché
                try:
                    cache_file = os.path.join(os.path.dirname(__file__), 'edition_cache.json')
                    cache = {}
                    if os.path.exists(cache_file):
                        with open(cache_file, 'r') as f:
                            cache = json.load(f)
                    
                    cache[fecha] = edition_number
                    
                    with open(cache_file, 'w') as f:
                        json.dump(cache, f, indent=2)
                    
                    print(f"[EDITION] Caché actualizado con {fecha}: {edition_number}")
                except Exception as e:
                    print(f"[EDITION] Error actualizando caché: {e}")
                
                return edition_number
                
        except Exception as e:
            print(f"[EDITION] No se encontró selector de ediciones: {e}")
        
        # Estrategia 2: Buscar en el HTML actual si ya estamos en una página con edición
        current_url = driver_creado.current_url
        match = re.search(r'/edicion-(\d+)/?', current_url)
        if match:
            edition_number = match.group(1)
            print(f"[EDITION] Edición detectada en URL actual: {edition_number}")
            return edition_number
        
        # Estrategia 3: Buscar publicaciones y verificar si hay contenido
        # Esto ayuda a confirmar si la edición existe
        publicaciones = driver_creado.find_elements(By.CLASS_NAME, "light")
        if publicaciones:
            print(f"[EDITION] Se encontraron {len(publicaciones)} publicaciones")
            # Si hay publicaciones, la URL actual debe tener la edición correcta
            # aunque no la hayamos detectado
        
        print("[EDITION] No se pudo detectar el número de edición")
        
        # Como último recurso, usar estimación basada en días hábiles
        return estimar_edicion_por_dias_habiles(fecha)
        
    except Exception as e:
        print(f"[EDITION] Error obteniendo número de edición: {str(e)}")
        return estimar_edicion_por_dias_habiles(fecha)
        
    finally:
        if driver_temporal and driver_creado:
            try:
                driver_creado.quit()
            except:
                pass

def estimar_edicion_por_dias_habiles(fecha):
    """
    Estima el número de edición basándose en días hábiles.
    El Diario Oficial se publica solo en días hábiles.
    """
    try:
        # Fechas y ediciones conocidas
        referencias = [
            ("07-07-2025", 44192),
            ("08-07-2025", 44193),
            ("09-07-2025", 44194),
            ("10-07-2025", 44195),
            ("11-07-2025", 44196),
            ("12-07-2025", 44197),  # Sábado (edición especial)
            ("17-07-2025", 44200),  # Jueves (saltó fin de semana)
            ("18-07-2025", 44201),  # Viernes
        ]
        
        # Buscar la referencia más cercana
        fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
        
        mejor_ref = None
        menor_diff = float('inf')
        
        for ref_fecha, ref_edicion in referencias:
            ref_fecha_obj = datetime.strptime(ref_fecha, "%d-%m-%Y")
            diff = abs((fecha_obj - ref_fecha_obj).days)
            if diff < menor_diff:
                menor_diff = diff
                mejor_ref = (ref_fecha_obj, ref_edicion)
        
        if mejor_ref:
            ref_fecha_obj, ref_edicion = mejor_ref
            dias_diff = (fecha_obj - ref_fecha_obj).days
            
            # Contar solo días hábiles
            dias_habiles = 0
            fecha_temp = ref_fecha_obj
            incremento = 1 if dias_diff > 0 else -1
            
            for _ in range(abs(dias_diff)):
                fecha_temp = fecha_temp.replace(day=fecha_temp.day + incremento)
                # Si es lunes a viernes, contar como día hábil
                if fecha_temp.weekday() < 5:  # 0=lunes, 4=viernes
                    dias_habiles += 1
            
            edicion_estimada = ref_edicion + (dias_habiles * incremento)
            print(f"[EDITION] Edición estimada basada en días hábiles: {edicion_estimada}")
            return str(edicion_estimada)
            
    except Exception as e:
        print(f"[EDITION] Error en estimación: {e}")
    
    # Valor por defecto
    return "44200"

# Prueba
if __name__ == "__main__":
    fechas_prueba = ["18-07-2025", "19-07-2025", "21-07-2025", "22-07-2025"]
    
    for fecha in fechas_prueba:
        print(f"\n{'='*50}")
        edicion = obtener_numero_edicion_mejorado(fecha)
        print(f"Fecha: {fecha} -> Edición: {edicion}")