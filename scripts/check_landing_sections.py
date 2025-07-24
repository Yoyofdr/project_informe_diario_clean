from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1400,2000")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Navegar a la página
    driver.get("http://localhost:8000/")
    
    # Esperar a que la página cargue
    time.sleep(3)
    
    # Buscar las secciones principales
    sections = {
        "Hero": driver.find_elements(By.CLASS_NAME, "modern-hero"),
        "Benefits": driver.find_elements(By.CLASS_NAME, "benefits-section"),
        "Example": driver.find_elements(By.ID, "ejemplo"),
        "Footer": driver.find_elements(By.CLASS_NAME, "modern-footer")
    }
    
    print("Secciones encontradas:")
    for name, elements in sections.items():
        print(f"- {name}: {'✓' if elements else '✗'} ({len(elements)} elementos)")
    
    # Verificar altura del body
    body_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    print(f"\nAltura del body: {body_height}px")
    print(f"Altura del viewport: {viewport_height}px")
    
    # Verificar contenido HTML
    page_source = driver.page_source
    if "benefits-section" in page_source:
        print("\n✓ HTML de benefits-section está presente")
    if "ejemplo" in page_source:
        print("✓ HTML de ejemplo está presente")
    if "modern-footer" in page_source:
        print("✓ HTML de modern-footer está presente")
        
    # Hacer scroll y capturar diferentes partes
    positions = [0, 800, 1600, 2400]
    for i, pos in enumerate(positions):
        driver.execute_script(f"window.scrollTo(0, {pos})")
        time.sleep(0.5)
        driver.save_screenshot(f"landing_section_{i}.png")
        print(f"\nCapturado screenshot en posición {pos}px")
    
finally:
    driver.quit()