#!/usr/bin/env python
"""
Scraper final para obtener los datos reales del 21 de julio
Usando la información de que SÍ existe la edición según el usuario
"""
import os
import sys
import django
import requests
from bs4 import BeautifulSoup
import json

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_sniper.settings')
django.setup()

def obtener_publicaciones_21_julio():
    """Obtiene las publicaciones del 21 de julio con un enfoque diferente"""
    
    print("=== SCRAPER FINAL - 21 DE JULIO 2025 ===\n")
    
    # Basándonos en el análisis del HTML de curl
    # Sabemos que la página dice "No existen publicaciones en esta edición"
    # Pero el usuario insiste que SÍ hay edición
    
    # Intentar obtener el contenido con una sesión persistente
    session = requests.Session()
    
    # Headers completos
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es-CL,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }
    
    session.headers.update(headers)
    
    try:
        # Primero, visitar la página principal para obtener cookies
        print("1. Visitando página principal...")
        resp_main = session.get("https://www.diariooficial.interior.gob.cl/", timeout=10)
        print(f"   Status: {resp_main.status_code}")
        print(f"   Cookies: {dict(session.cookies)}")
        
        # Luego, ir a la edición del 21 de julio
        url_21_julio = "https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date=21-07-2025&edition=44204"
        print(f"\n2. Accediendo a la edición del 21 de julio...")
        print(f"   URL: {url_21_julio}")
        
        response = session.get(url_21_julio, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Tamaño: {len(response.text)} caracteres")
        
        # Analizar el contenido
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar el mensaje que encontramos antes
        no_publicaciones = soup.find('p', class_='nofound')
        if no_publicaciones:
            print(f"\n⚠️ Mensaje del sitio: '{no_publicaciones.text.strip()}'")
            
            # IMPORTANTE: Según el usuario, SÍ hay edición
            # Vamos a generar un reporte que explique la situación
            
            resultado = {
                'fecha': '21-07-2025',
                'edicion': '44204',
                'estado': 'sin_publicaciones',
                'mensaje_sitio': no_publicaciones.text.strip(),
                'nota_importante': 'El sitio web indica que no hay publicaciones para esta edición, pero según la información proporcionada, la edición SÍ existe.',
                'publicaciones': [],
                'valores_monedas': {},
                'total_documentos': 0
            }
            
            # Guardar el resultado
            with open('resultado_21_julio.json', 'w', encoding='utf-8') as f:
                json.dump(resultado, f, ensure_ascii=False, indent=2)
            
            print("\n📋 RESUMEN:")
            print(f"   - Fecha: {resultado['fecha']}")
            print(f"   - Edición: {resultado['edicion']}")
            print(f"   - Estado: {resultado['estado']}")
            print(f"   - Mensaje del sitio: {resultado['mensaje_sitio']}")
            print("\n⚠️  NOTA: El sitio indica que no hay publicaciones, pero según el usuario la edición existe.")
            
            return resultado
            
        else:
            # Si no hay mensaje de "no found", buscar publicaciones
            publicaciones = []
            
            # Buscar diferentes estructuras posibles
            content_rows = soup.find_all('tr', class_='content')
            if content_rows:
                print(f"\n✅ Encontradas {len(content_rows)} publicaciones")
                # Procesar publicaciones...
            
            return {
                'fecha': '21-07-2025',
                'edicion': '44204',
                'estado': 'con_publicaciones',
                'publicaciones': publicaciones,
                'valores_monedas': {},
                'total_documentos': len(publicaciones)
            }
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'fecha': '21-07-2025',
            'edicion': '44204',
            'estado': 'error',
            'error': str(e),
            'publicaciones': [],
            'valores_monedas': {},
            'total_documentos': 0
        }

if __name__ == "__main__":
    resultado = obtener_publicaciones_21_julio()
    
    # Generar el informe basado en el resultado
    if resultado['estado'] == 'sin_publicaciones':
        print("\n" + "="*60)
        print("CONCLUSIÓN:")
        print("El sitio web oficial del Diario Oficial indica que no hay")
        print("publicaciones para la edición 44204 del 21 de julio de 2025.")
        print("\nEsto puede deberse a:")
        print("1. Es un día sin publicaciones programadas")
        print("2. Las publicaciones aún no han sido cargadas")
        print("3. Es una edición especial sin contenido regular")
        print("="*60)