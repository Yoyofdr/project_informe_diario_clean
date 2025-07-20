from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1400,3000")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Navegar a la página raíz
    driver.get("http://localhost:8000/")
    
    # Esperar a que la página cargue
    time.sleep(3)
    
    # Tomar screenshot
    driver.save_screenshot("landing_moderna_correcta.png")
    print("Screenshot guardado como landing_moderna_correcta.png")
    
finally:
    driver.quit()