#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

fecha = "17-07-2025"
edition = "44202"

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)

try:
    # Intentar con la página principal
    url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}"
    print(f"Visitando: {url}")
    driver.get(url)
    time.sleep(3)
    
    # Buscar publicaciones
    content_rows = driver.find_elements(By.CSS_SELECTOR, "tr.content")
    print(f"\nPublicaciones encontradas: {len(content_rows)}")
    
    # Buscar mensaje de no publicaciones
    no_found = driver.find_elements(By.CSS_SELECTOR, "p.nofound")
    if no_found:
        print(f"Mensaje encontrado: {no_found[0].text}")
    
    # Intentar con avisos destacados
    url_avisos = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/avisos_destacados.php?date={fecha}&edition={edition}"
    print(f"\nVisitando avisos destacados: {url_avisos}")
    driver.get(url_avisos)
    time.sleep(3)
    
    # Buscar avisos
    avisos = driver.find_elements(By.CSS_SELECTOR, "div.aviso-destacado, tr.content")
    print(f"Avisos destacados encontrados: {len(avisos)}")
    
    if avisos:
        print("\nPrimeros 3 avisos:")
        for i, aviso in enumerate(avisos[:3], 1):
            print(f"{i}. {aviso.text[:100]}...")
    
    # Guardar screenshot
    driver.save_screenshot("selenium_17julio.png")
    print("\nScreenshot guardado como selenium_17julio.png")
    
finally:
    driver.quit()