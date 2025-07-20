from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1400,1000")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Navegar a la página
    driver.get("http://localhost:8000/landing/")
    
    # Esperar a que la página cargue
    time.sleep(2)
    
    # Buscar campos del formulario
    print("Buscando campos del formulario...")
    
    # Buscar por ID
    nombre_field = driver.find_elements(By.ID, "id_nombre")
    apellido_field = driver.find_elements(By.ID, "id_apellido")
    email_field = driver.find_elements(By.ID, "id_email")
    
    print(f"Campo nombre encontrado: {len(nombre_field) > 0}")
    print(f"Campo apellido encontrado: {len(apellido_field) > 0}")
    print(f"Campo email encontrado: {len(email_field) > 0}")
    
    # Buscar por name
    nombre_by_name = driver.find_elements(By.NAME, "nombre")
    apellido_by_name = driver.find_elements(By.NAME, "apellido")
    email_by_name = driver.find_elements(By.NAME, "email")
    
    print(f"\nPor atributo name:")
    print(f"Campo nombre: {len(nombre_by_name) > 0}")
    print(f"Campo apellido: {len(apellido_by_name) > 0}")
    print(f"Campo email: {len(email_by_name) > 0}")
    
    # Ver el HTML del formulario
    form = driver.find_element(By.TAG_NAME, "form")
    print(f"\nHTML del formulario:")
    print(form.get_attribute('innerHTML')[:500])
    
    # Tomar screenshot
    driver.save_screenshot("landing_form_debug.png")
    print("\nScreenshot guardado como landing_form_debug.png")
    
finally:
    driver.quit()