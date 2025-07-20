from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1400,800")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Navegar a la página
    driver.get("http://localhost:8000/landing/")
    
    # Esperar a que la página cargue
    time.sleep(2)
    
    # Verificar el título de la página
    print(f"Título de la página: {driver.title}")
    
    # Buscar el formulario de registro
    forms = driver.find_elements(By.TAG_NAME, "form")
    print(f"Número de formularios encontrados: {len(forms)}")
    
    # Buscar el contenido principal
    h2_elements = driver.find_elements(By.TAG_NAME, "h2")
    if h2_elements:
        print(f"Primer H2 encontrado: {h2_elements[0].text}")
    
    # Verificar si estamos en la página correcta
    card_elements = driver.find_elements(By.CLASS_NAME, "card")
    print(f"Elementos con clase 'card': {len(card_elements)}")
    
    # Hacer scroll para ver todo el contenido
    driver.execute_script("window.scrollTo(0, 300)")
    time.sleep(1)
    
    # Tomar screenshot
    driver.save_screenshot("landing_page_full.png")
    print("Screenshot guardado como landing_page_full.png")
    
finally:
    driver.quit()