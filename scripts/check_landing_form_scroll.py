from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1400,3000")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Navegar a la página
    driver.get("http://localhost:8000/landing/")
    
    # Esperar a que la página cargue
    time.sleep(2)
    
    # Hacer scroll hasta el final
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    
    # Buscar el formulario
    forms = driver.find_elements(By.TAG_NAME, "form")
    print(f"Formularios encontrados: {len(forms)}")
    
    if forms:
        # Ver el contenido del formulario
        form_html = forms[0].get_attribute('outerHTML')
        print(f"HTML del formulario:\n{form_html[:1000]}")
    
    # Tomar screenshot completo
    driver.save_screenshot("landing_completo.png")
    print("\nScreenshot guardado como landing_completo.png")
    
finally:
    driver.quit()