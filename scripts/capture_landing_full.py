from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1400,4000")
chrome_options.add_argument("--force-device-scale-factor=0.75")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Navegar a la página
    driver.get("http://localhost:8000/")
    
    # Esperar a que la página cargue
    time.sleep(3)
    
    # Hacer scroll para ver toda la página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(1)
    
    # Tomar screenshot de toda la página
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1400, total_height)
    driver.save_screenshot("landing_completa.png")
    print(f"Screenshot completo guardado (altura: {total_height}px)")
    
finally:
    driver.quit()