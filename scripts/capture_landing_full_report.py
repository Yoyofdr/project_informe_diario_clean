from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1400,3000")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Navegar a la página
    driver.get("http://localhost:8000/")
    
    # Esperar a que la página cargue
    time.sleep(3)
    
    # Hacer scroll hasta la sección del ejemplo
    driver.execute_script("document.getElementById('ejemplo').scrollIntoView({behavior: 'smooth', block: 'start'})")
    time.sleep(2)
    
    # Tomar screenshot
    driver.save_screenshot("landing_con_informe_completo.png")
    print("Screenshot guardado como landing_con_informe_completo.png")
    
finally:
    driver.quit()