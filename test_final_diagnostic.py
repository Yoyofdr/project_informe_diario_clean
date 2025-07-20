#!/usr/bin/env python
"""
Diagnóstico final del problema
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')

# NO cargar Django completo para evitar timeouts
# import django
# django.setup()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

print("=== DIAGNÓSTICO FINAL ===\n")

fecha = "11-07-2025"
edition = "44196"
url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition={edition}&v=1"

print(f"URL: {url}")

# Configurar Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

print("\n1. Instalando ChromeDriver...")
service = Service(ChromeDriverManager().install())

print("2. Iniciando Chrome...")
driver = webdriver.Chrome(service=service, options=options)

try:
    print("3. Navegando...")
    driver.get(url)
    
    print("4. Esperando 5 segundos...")
    time.sleep(5)
    
    html = driver.page_source
    print(f"5. HTML obtenido: {len(html)} caracteres")
    
    # Analizar con BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    
    # Buscar secciones
    print("\n6. Buscando secciones...")
    secciones_encontradas = []
    for tag in soup.find_all(['td']):
        texto = tag.get_text(strip=True)
        if "Normas" in texto and ("Generales" in texto or "Particulares" in texto):
            secciones_encontradas.append(texto)
            print(f"   - Sección encontrada: {texto}")
    
    # Buscar PDFs
    print("\n7. Buscando PDFs...")
    pdfs = soup.find_all("a", href=lambda x: x and x.endswith(".pdf"))
    print(f"   - Total PDFs: {len(pdfs)}")
    
    if pdfs:
        print("\n8. Primeros 3 PDFs:")
        for i, pdf in enumerate(pdfs[:3]):
            href = pdf.get('href')
            # Buscar el título en el padre
            parent = pdf.find_parent('tr')
            titulo = "Sin título"
            if parent:
                # Buscar en las celdas anteriores
                celdas = parent.find_all('td')
                for celda in celdas:
                    texto = celda.get_text(strip=True)
                    if texto and not texto.startswith("Ver PDF"):
                        titulo = texto
                        break
            
            print(f"   {i+1}. {titulo}")
            print(f"      URL: {href}")
    
    # Guardar evidencia
    with open("diagnostic_output.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\n9. HTML guardado en: diagnostic_output.html")
    
    print("\n✅ Diagnóstico completado exitosamente")
    
finally:
    driver.quit()
    print("\n10. Chrome cerrado")