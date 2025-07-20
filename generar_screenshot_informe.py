#!/usr/bin/env python3
"""
Script para generar screenshot del informe del 12 de julio
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Configurar Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1200,1600')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    # Buscar el archivo HTML del informe
    archivo_informe = None
    posibles_archivos = [
        'informe_corregido_12_07_2025.html',
        'informe_historico_12_07_2025.html',
        'informe_12_07_2025.html'
    ]
    
    for archivo in posibles_archivos:
        if os.path.exists(archivo):
            archivo_informe = archivo
            break
    
    if not archivo_informe:
        print("No se encontró el archivo del informe del 12 de julio")
        exit(1)
    
    # Abrir el archivo HTML
    file_path = f"file://{os.path.abspath(archivo_informe)}"
    print(f"Abriendo: {file_path}")
    driver.get(file_path)
    
    # Esperar a que se cargue
    time.sleep(3)
    
    # Tomar screenshot
    screenshot_path = 'static/img/ejemplo_informe_12_julio.png'
    os.makedirs('static/img', exist_ok=True)
    driver.save_screenshot(screenshot_path)
    
    print(f"Screenshot guardado en: {screenshot_path}")
    
finally:
    driver.quit()