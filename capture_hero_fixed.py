from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1400,1000")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Navegar a la página
    driver.get("http://localhost:8000/")
    
    # Esperar a que la página cargue
    time.sleep(2)
    
    # Tomar screenshot del hero
    driver.save_screenshot("hero_texto_corregido.png")
    print("Screenshot del hero con texto corregido guardado")
    
finally:
    driver.quit()