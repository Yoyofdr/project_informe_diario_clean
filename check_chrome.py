#!/usr/bin/env python
"""
Script para verificar la instalación de Chrome y ChromeDriver
"""
import subprocess
import os

def check_chrome():
    """Verifica la versión de Chrome instalada"""
    print("=== VERIFICACIÓN DE CHROME ===\n")
    
    # Verificar Chrome
    try:
        # En macOS, Chrome está en una ubicación específica
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chrome.app/Contents/MacOS/Chrome",
            "/usr/bin/google-chrome",
            "/usr/bin/chromium"
        ]
        
        chrome_found = False
        for path in chrome_paths:
            if os.path.exists(path):
                result = subprocess.run([path, "--version"], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Chrome encontrado: {path}")
                    print(f"Versión: {result.stdout.strip()}")
                    chrome_found = True
                    break
        
        if not chrome_found:
            print("Chrome no encontrado en las rutas estándar")
            
    except Exception as e:
        print(f"Error verificando Chrome: {e}")
    
    print("\n=== VERIFICACIÓN DE CHROMEDRIVER ===\n")
    
    # Verificar ChromeDriver
    try:
        result = subprocess.run(["chromedriver", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"ChromeDriver: {result.stdout.strip()}")
        else:
            print("ChromeDriver no encontrado en PATH")
    except:
        print("ChromeDriver no está instalado o no está en PATH")
    
    # Verificar undetected-chromedriver
    print("\n=== VERIFICACIÓN DE UNDETECTED-CHROMEDRIVER ===\n")
    try:
        import undetected_chromedriver as uc
        print(f"undetected-chromedriver instalado: versión {uc.__version__ if hasattr(uc, '__version__') else 'desconocida'}")
        
        # Verificar el directorio de drivers
        driver_path = os.path.expanduser("~/.local/share/undetected_chromedriver")
        if os.path.exists(driver_path):
            print(f"Directorio de drivers: {driver_path}")
            drivers = os.listdir(driver_path)
            print(f"Drivers encontrados: {len(drivers)}")
            for driver in drivers[:5]:  # Mostrar los primeros 5
                print(f"  - {driver}")
    except ImportError:
        print("undetected-chromedriver no está instalado")
    except Exception as e:
        print(f"Error verificando undetected-chromedriver: {e}")

if __name__ == "__main__":
    check_chrome()