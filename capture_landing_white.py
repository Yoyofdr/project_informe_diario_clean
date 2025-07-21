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
    time.sleep(3)
    
    # Tomar screenshot
    driver.save_screenshot("landing_white_hero.png")
    print("Screenshot guardado como landing_white_hero.png")
    
finally:
    driver.quit()