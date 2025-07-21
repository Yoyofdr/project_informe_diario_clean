from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    
    # Hacer scroll directo hasta la sección del informe
    driver.execute_script("window.scrollTo(0, 1600)")
    time.sleep(2)
    
    # Tomar screenshot
    driver.save_screenshot("informe_completo_seccion.png")
    print("Screenshot guardado como informe_completo_seccion.png")
    
finally:
    driver.quit()