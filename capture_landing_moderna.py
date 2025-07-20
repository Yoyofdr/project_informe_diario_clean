from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1400,2000")
chrome_options.add_argument("--force-device-scale-factor=2")
chrome_options.add_argument("--high-dpi-support=2")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Navegar a la página
    driver.get("http://localhost:8000/landing-explicativa/")
    
    # Esperar a que la página cargue completamente
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modern-hero"))
    )
    
    # Scroll para capturar toda la página
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(1)
    
    # Tomar screenshot
    driver.save_screenshot("landing_moderna_completa.png")
    print("Screenshot guardado como landing_moderna_completa.png")
    
    # También capturar solo el hero
    hero_element = driver.find_element(By.CLASS_NAME, "modern-hero")
    hero_element.screenshot("landing_hero_section.png")
    print("Hero section guardado como landing_hero_section.png")
    
    # Capturar la sección de ejemplo
    driver.execute_script("document.getElementById('ejemplo').scrollIntoView()")
    time.sleep(1)
    ejemplo_element = driver.find_element(By.ID, "ejemplo")
    ejemplo_element.screenshot("landing_ejemplo_section.png")
    print("Ejemplo section guardado como landing_ejemplo_section.png")
    
finally:
    driver.quit()